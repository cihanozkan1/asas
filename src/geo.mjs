// Node-side resolution of map targets, flags and icons referenced by a script.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { ROOT, readJson } from './util.mjs';
import { ensureAdmin1 } from '../tools/fetch-data.mjs';

const require = createRequire(import.meta.url);
const countries = require('i18n-iso-countries');

let atlas;
function atlasIndex() {
  if (atlas) return atlas;
  const topo = readJson(path.join(ROOT, 'node_modules/world-atlas/countries-10m.json'));
  const geoms = topo.objects.countries.geometries;
  atlas = {
    ids: new Set(geoms.map((g) => g.id).filter(Boolean)),
    names: new Map(geoms.map((g) => [g.properties.name.toLowerCase(), g])),
  };
  return atlas;
}

let admin1;
async function admin1Features() {
  if (!admin1) admin1 = JSON.parse(fs.readFileSync(await ensureAdmin1(), 'utf8')).features;
  return admin1;
}

// "RUS" | "RU" | "643" | "Russia" -> {type:'country', id|name}
function countrySpec(code) {
  const a = atlasIndex();
  const s = String(code).trim();
  let num = null;
  if (/^\d{1,3}$/.test(s)) num = s.padStart(3, '0');
  else if (/^[A-Za-z]{3}$/.test(s)) num = countries.alpha3ToNumeric(s.toUpperCase());
  else if (/^[A-Za-z]{2}$/.test(s)) num = countries.alpha2ToNumeric(s.toUpperCase());
  if (num && a.ids.has(num)) return { type: 'country', id: num };
  const byName = a.names.get(s.toLowerCase());
  if (byName) return byName.id ? { type: 'country', id: byName.id } : { type: 'country', name: byName.properties.name };
  throw new Error(`Bilinmeyen ülke: "${code}"`);
}

export async function resolveTargetSpec(t, videoDir) {
  if (Array.isArray(t)) return { type: 'multi', items: await Promise.all(t.map((x) => resolveTargetSpec(x, videoDir))) };
  if (typeof t === 'string') return countrySpec(t);
  if (t.countries) return { type: 'multi', items: t.countries.map(countrySpec) };
  if (t.geonunit || t.admin1s) {
    // several admin-1 units merged into one shape: a UK home nation, or a list of provinces
    const feats = await admin1Features();
    const iso = t.country ? String(t.country).toUpperCase() : null;
    const wantList = (t.admin1s || []).map((n) => n.toLowerCase());
    const sel = feats.filter((f) => {
      const p = f.properties;
      if (iso && p.adm0_a3 !== iso && p.iso_a2 !== iso) return false;
      if (t.geonunit) return p.geonunit === t.geonunit;
      return [p.name, p.name_en].filter(Boolean).some((n) => wantList.includes(n.toLowerCase()));
    });
    if (!sel.length) throw new Error('admin1 grubu bulunamadı: ' + JSON.stringify(t));
    const polys = sel.flatMap((f) => (f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates));
    return { type: 'feature', feature: { type: 'Feature', properties: {}, geometry: { type: 'MultiPolygon', coordinates: polys } } };
  }
  if (t.country && !t.admin1) return { ...countrySpec(t.country), part: t.part || null };
  if (t.admin1) {
    const feats = await admin1Features();
    const want = t.admin1.toLowerCase();
    const iso = t.country ? String(t.country).toUpperCase() : null;
    const f = feats.find((f) => {
      const p = f.properties;
      const names = [p.name, p.name_en, p.woe_name, p.gn_name, ...(p.name_alt || '').split('|')].filter(Boolean).map((n) => n.toLowerCase());
      const okCountry = !iso || p.adm0_a3 === iso || p.iso_a2 === iso;
      return okCountry && names.includes(want);
    });
    if (!f) throw new Error(`admin1 bölge bulunamadı: ${t.admin1} (${t.country || '?'})`);
    return { type: 'feature', feature: { type: 'Feature', properties: { name: f.properties.name }, geometry: f.geometry } };
  }
  if (t.geojson) {
    const p = path.resolve(videoDir, t.geojson);
    const gj = readJson(p);
    // Merge polygons into one MultiPolygon so the renderer can index/cull it like a country.
    const geoms = gj.type === 'FeatureCollection' ? gj.features.map((f) => f.geometry) : [gj.type === 'Feature' ? gj.geometry : gj];
    const polys = geoms.flatMap((g) => (g.type === 'Polygon' ? [g.coordinates] : g.type === 'MultiPolygon' ? g.coordinates : []));
    if (!polys.length) throw new Error('GeoJSON içinde poligon yok: ' + t.geojson);
    const feature = { type: 'Feature', properties: {}, geometry: { type: 'MultiPolygon', coordinates: polys } };
    return { type: 'feature', feature };
  }
  if (t.circle) return { type: 'circle', lat: t.circle.lat, lon: t.circle.lon, km: t.circle.km };
  if (t.box) {
    // lon/lat rectangle [west, south, east, north], edges densified so parallels stay parallels;
    // clockwise ring (d3-geo's exterior winding)
    const [w, so, e, n] = t.box;
    const ring = [];
    const N = 24;
    for (let i = 0; i <= N; i++) ring.push([w, so + ((n - so) * i) / N]);
    for (let i = 1; i <= N; i++) ring.push([w + ((e - w) * i) / N, n]);
    for (let i = 1; i <= N; i++) ring.push([e, n - ((n - so) * i) / N]);
    for (let i = 1; i <= N; i++) ring.push([e - ((e - w) * i) / N, so]);
    return { type: 'feature', feature: { type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [ring] } } };
  }
  throw new Error('Tanınmayan hedef: ' + JSON.stringify(t));
}

export function flagExists(code) {
  return fs.existsSync(path.join(ROOT, 'node_modules/flag-icons/flags/4x3', `${code}.svg`));
}

// "🏰" or "1f3f0" -> "/node_modules/@twemoji/svg/1f3f0.svg"
export function iconUrl(icon) {
  let code = icon;
  if (!/^[0-9a-f-]+$/i.test(icon)) {
    code = [...icon]
      .map((c) => c.codePointAt(0).toString(16))
      .filter((c) => c !== 'fe0f')
      .join('-');
  }
  const file = path.join(ROOT, 'node_modules/@twemoji/svg', `${code}.svg`);
  if (!fs.existsSync(file)) throw new Error(`İkon bulunamadı: ${icon} (${code})`);
  return `/node_modules/@twemoji/svg/${code}.svg`;
}
