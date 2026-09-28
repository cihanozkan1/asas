// Historical borders for history scenes: "historical-basemaps" by André Ourednik
// (https://github.com/aourednik/historical-basemaps, GPL-3.0), fetched on demand into cache/.
import fs from 'node:fs';
import path from 'node:path';
import { geoArea } from 'd3-geo';
import { ROOT, log } from './util.mjs';

export const HIST_YEARS = [1492, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880, 1900, 1914, 1920, 1930, 1938, 1945, 1960];
export const HIST_CREDIT = 'Historical borders: historical-basemaps by André Ourednik (GPL-3.0)';
const DIR = path.join(ROOT, 'cache/historical');

// the map closest to (and not after) the year told in the story
export function histYearFor(year) {
  const y = Number(String(year).match(/\d{3,4}/)?.[0]);
  if (!y || y < 1492) return null;
  let best = null;
  for (const h of HIST_YEARS) if (h <= y + 2) best = h;
  return best;
}

export async function ensureHist(year) {
  const file = path.join(DIR, `world_${year}.geojson`);
  if (!fs.existsSync(file)) {
    fs.mkdirSync(DIR, { recursive: true });
    log(`tarihi sınırlar indiriliyor: ${year}`);
    const res = await fetch(`https://raw.githubusercontent.com/aourednik/historical-basemaps/master/geojson/world_${year}.geojson`);
    if (!res.ok) throw new Error('historical-basemaps ' + res.status);
    fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()));
  }
  return file;
}

const cache = new Map();
async function load(year) {
  if (!cache.has(year)) cache.set(year, JSON.parse(fs.readFileSync(await ensureHist(year), 'utf8')));
  return cache.get(year);
}

// d3-geo wants clockwise exterior rings: flip any polygon that would cover "everything else"
function rewind(polys) {
  return polys.map((p) => (geoArea({ type: 'Polygon', coordinates: p }) > 2 * Math.PI ? p.map((r) => [...r].reverse()) : p));
}
const polysOf = (g) => (g.type === 'Polygon' ? [g.coordinates] : g.type === 'MultiPolygon' ? g.coordinates : []);

// {hist: 1815, name: 'Russian Empire'} or {hist: 1880, names: [...]} -> one MultiPolygon feature
export async function histFeature(t) {
  const gj = await load(t.hist);
  const want = (t.names || [t.name]).map((n) => n.toLowerCase());
  const sel = gj.features.filter((f) => want.includes(String(f.properties.NAME || '').toLowerCase()));
  if (!sel.length) throw new Error(`tarihi bölge bulunamadı: ${want.join(', ')} (${t.hist})`);
  const polys = rewind(sel.flatMap((f) => polysOf(f.geometry)));
  return { type: 'Feature', properties: { name: sel[0].properties.NAME }, geometry: { type: 'MultiPolygon', coordinates: polys } };
}

// all state outlines of one year as a MultiLineString (the page draws them as the old map's borders)
export async function histBorders(year) {
  const out = path.join(DIR, `borders_${year}.json`);
  if (!fs.existsSync(out)) {
    const gj = await load(year);
    const lines = [];
    const r4 = (v) => Math.round(v * 1e3) / 1e3;
    for (const f of gj.features) for (const p of polysOf(f.geometry)) for (const ring of p) if (ring.length > 3) lines.push(ring.map(([x, y]) => [r4(x), r4(y)]));
    fs.writeFileSync(out, JSON.stringify({ type: 'MultiLineString', coordinates: lines }));
  }
  return '/' + path.relative(ROOT, out).split(path.sep).join('/');
}
