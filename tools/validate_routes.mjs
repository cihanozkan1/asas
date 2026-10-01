#!/usr/bin/env node
// Logic check for routes: a ship must sail on water, a car/bus/train/walker must stay on land.
// Samples the same smoothed curve the renderer draws against the 10 m land polygons.
//   node tools/validate_routes.mjs [videos/<id> ...]      (no args: every video)
// Route element fields used: points, mover.kind / mover.icon, optional medium: 'land' | 'water' | 'air';
// check:false skips a route whose course the 10 m coastline cannot resolve (a strait narrower than ~1 km).
// Routes without a medium are only listed with --all.
import fs from 'node:fs';
import path from 'node:path';
import { geoContains, geoInterpolate, geoDistance } from 'd3-geo';
import { feature } from 'topojson-client';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const topo = JSON.parse(fs.readFileSync(path.join(ROOT, 'node_modules/world-atlas/land-10m.json')));
const lf = feature(topo, topo.objects.land);
const geoms = lf.type === 'FeatureCollection' ? lf.features.map((x) => x.geometry) : [lf.geometry];
const polys = geoms.flatMap((g) => (g.type === 'Polygon' ? [g.coordinates] : g.coordinates)).map((coordinates) => {
  let x0 = 180, y0 = 90, x1 = -180, y1 = -90;
  for (const [x, y] of coordinates[0]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  return { box: [x0, y0, x1, y1], geom: { type: 'Polygon', coordinates } };
});
const isLand = (lon, lat) => polys.some((p) => lon >= p.box[0] && lon <= p.box[2] && lat >= p.box[1] && lat <= p.box[3] && geoContains(p.geom, [lon, lat]));

const toPt = (p) => (Array.isArray(p) ? { lat: p[0], lon: p[1] } : { lat: p.lat, lon: p.lon });
function catmull(points, steps = 10) {
  if (points.length < 3) return points;
  const P = points.map((p) => [p.lon, p.lat]), out = [];
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(P.length - 1, i + 2)];
    for (let k = 0; k < steps; k++) {
      const t = k / steps, t2 = t * t, t3 = t2 * t;
      const f = (a, b, c, d) => 0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3);
      out.push({ lon: f(p0[0], p1[0], p2[0], p3[0]), lat: f(p0[1], p1[1], p2[1], p3[1]) });
    }
  }
  out.push(points[points.length - 1]);
  return out;
}
function sample(pts, rhumb) {
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const a = [pts[i].lon, pts[i].lat], b = [pts[i + 1].lon, pts[i + 1].lat];
    const f = rhumb ? (u) => [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u] : geoInterpolate(a, b);
    const n = Math.max(2, Math.ceil(geoDistance(a, b) / 0.002));
    for (let k = 0; k < n; k++) out.push(f(k / n));
  }
  return out;
}
function medium(el) {
  if (el.medium) return el.medium;
  const m = el.mover;
  if (!m) return null;
  if (m.kind === 'ship') return 'water';
  if (m.kind === 'plane') return 'air';
  if (m.kind === 'character') return 'land';
  if (m.kind === 'icon' && /car|bus|train|truck|walker|horse|camel/.test(m.icon || '')) return 'land';
  return null;
}

const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const ids = args.length ? args.map((a) => path.basename(a)) : fs.readdirSync(path.join(ROOT, 'videos')).filter((d) => fs.existsSync(path.join(ROOT, 'videos', d, 'script.json')));
let bad = 0;
for (const id of ids) {
  const s = JSON.parse(fs.readFileSync(path.join(ROOT, 'videos', id, 'script.json')));
  s.scenes.forEach((sc, si) => {
    for (const el of sc.show || []) {
      if (el.type !== 'route' || !el.points || el.points.length < 2) continue;
      const med = medium(el);
      if (med === 'air' || el.check === false || (!med && !process.argv.includes('--all'))) continue;
      const P = el.points.map(toPt);
      const pts = sample(el.smooth !== false && !el.rhumb ? catmull(P) : P, !!el.rhumb);
      let onLand = 0;
      const runs = [];
      pts.forEach((q, i) => {
        const l = isLand(q[0], q[1]);
        if (l) onLand++;
        const bad = med === 'water' ? l : med === 'land' ? !l : false;
        if (bad) { const last = runs[runs.length - 1]; if (last && last.e === i - 1) last.e = i; else runs.push({ s: i, e: i }); }
      });
      const share = onLand / pts.length;
      const wrong = med === 'water' ? share : med === 'land' ? 1 - share : Math.min(share, 1 - share);
      const limit = med ? 0.06 : 0.12;
      if (wrong > limit) {
        bad++;
        const where = runs.slice(0, 3).map((r) => `${pts[r.s][1].toFixed(2)},${pts[r.s][0].toFixed(2)}→${pts[r.e][1].toFixed(2)},${pts[r.e][0].toFixed(2)}`).join(' | ');
        console.log(`${id} sahne ${si + 1} "${(sc.text || '').slice(0, 40)}": rota ${med || 'belirsiz'} ama %${Math.round(wrong * 100)} yanlış ortamda ${where ? '(' + where + ')' : ''}`);
      }
    }
  });
}
console.log(bad ? `${bad} rota sorunlu` : 'rotalar tutarlı');
process.exit(bad ? 1 : 0);
