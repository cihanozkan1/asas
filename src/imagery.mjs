// High-resolution detail imagery for close-up shots.
// Source: Copernicus Sentinel-2 L2A open data (AWS), free for any use incl. commercial with the credit below.
// tools/s2_fetch.py builds a cloud-free median mosaic per box. (The EOX "cloudless" mosaics we used before
// carry their own licence with commercial restrictions, so they are not used any more.)
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { ROOT, log } from './util.mjs';

export const S2_CREDIT = 'Satellite imagery: contains modified Copernicus Sentinel data (2023-2026), ESA';
export const BLUE_MARBLE_CREDIT = 'Earth imagery: NASA Blue Marble (NASA Earth Observatory)';
export const NE_CREDIT = 'Map data: Natural Earth';

// bbox: [west, south, east, north] in degrees. width: pixels (height follows the bbox aspect).
export async function ensureDetail({ bbox, width = 4096 }) {
  const [w, s, e, n] = bbox;
  const height = Math.min(4096, Math.round((width * (n - s)) / (e - w)));
  const key = crypto.createHash('sha1').update(JSON.stringify({ bbox, width, height, v: 2 })).digest('hex').slice(0, 12);
  const rel = `cache/imagery/cop_${key}.jpg`;
  const file = path.join(ROOT, rel);
  if (!fs.existsSync(file)) {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    log(`Sentinel-2 mozaiği hazırlanıyor ${bbox.join(',')} (${width}x${height})`);
    let last;
    for (let attempt = 1; attempt <= 3; attempt++) {
      const r = spawnSync('python3', [path.join(ROOT, 'tools/s2_fetch.py'), ...bbox.map(String), String(width), file + '.part'], { encoding: 'utf8', maxBuffer: 1 << 26 });
      if (r.status === 0) { fs.renameSync(file + '.part', file); last = null; break; }
      last = (r.stderr || '').slice(-400);
      log(`Sentinel-2 hatası, tekrar ${attempt}/3: ${last.split('\n').pop()}`);
    }
    if (last) throw new Error('Sentinel-2 mozaiği yapılamadı: ' + last);
  }
  return { url: '/' + rel, bbox, mask: arguments[0].mask !== false, landExtra: arguments[0].landExtra };
}

// Close-up cameras (explicit lat/lon/zoom) get Sentinel-2 detail automatically, so no shot
// falls back to the blurry 8k base or shows a detail box smaller than the screen.
// Returns bboxes (coarse first) that are not already covered by the script's own imagery.
export function autoDetailBoxes(script, cfg, { minZoom = 8, max = 4 } = {}) {
  const R = cfg.layout.globeRadius;
  const aspect = cfg.video.height / cfg.video.width;
  const views = [];
  const addView = (lat, lon, zoom) => {
    const half = (((1 / (zoom * R)) * 180) / Math.PI / 2) * 1.35; // margin for drift/sway/punch
    if (half * 2 > 8) return; // too wide for a Sentinel mosaic; Blue Marble is sharp enough
    const halfLat = half * aspect * Math.cos((lat * Math.PI) / 180);
    views.push({ zoom, span: half * 2, box: [lon - half, lat - halfLat, lon + half, lat + halfLat] });
  };
  script.scenes.forEach((s, i) => {
    const c = s.camera;
    // a camera that follows a route sees every place along it: cover the route's points
    if (c?.follow && s.era !== 'history' && !s.style) {
      const r = script.scenes.slice(0, i + 1).flatMap((x) => x.show || []).find((e) => e.id === c.follow);
      const z = Math.min(c.zoom ?? 3, c.zoomTo ?? c.zoom ?? 3);
      if (r?.points && z >= minZoom) for (const q of r.points) { const la = Array.isArray(q) ? q[0] : q.lat, lo = Array.isArray(q) ? q[1] : q.lon; addView(la, lo, z); }
    }
    if (!c || c.fit || c.follow || c.lat == null || !(c.zoom >= minZoom)) return;
    // parchment / palette scenes never show satellite pixels
    if (s.era === 'history' || s.style) return;
    addView(c.lat, c.lon, c.zoom);
    // the intro flies in from ~0.6x the first shot's zoom (page/main.js)
    if (i === 0 && c.zoom * 0.6 >= minZoom) addView(c.lat, c.lon, c.zoom * 0.6);
  });
  const inside = (a, b) => b[0] <= a[0] && b[1] <= a[1] && b[2] >= a[2] && b[3] >= a[3];
  const explicit = (script.imagery || []).map((d) => d.bbox);
  const groups = [];
  for (const v of views.sort((a, b) => b.zoom - a.zoom)) {
    if (explicit.some((b) => inside(v.box, b))) continue;
    const g = groups.find((g) => inside(v.box, g.box));
    if (g) continue;
    // merge into a group if the union still gives >= 1 texel per output pixel for its tightest view
    // (span includes the 1.35 margin, so the view itself is span / 1.35 wide)
    let best = null;
    for (const g of groups) {
      const u = [Math.min(g.box[0], v.box[0]), Math.min(g.box[1], v.box[1]), Math.max(g.box[2], v.box[2]), Math.max(g.box[3], v.box[3])];
      const need = ((u[2] - u[0]) / (Math.min(g.span, v.span) / 1.35)) * cfg.video.width;
      if (need <= 4096 && (!best || need < best.need)) best = { g, u, need };
    }
    if (best) {
      best.g.box = best.u;
      best.g.span = Math.min(best.g.span, v.span);
      best.g.zoom = Math.max(best.g.zoom, v.zoom);
    } else groups.push({ box: [...v.box], span: v.span, zoom: v.zoom });
  }
  const r4 = (x) => Math.round(x * 1e4) / 1e4;
  return groups
    .sort((a, b) => b.zoom - a.zoom)
    .slice(0, Math.max(0, max - explicit.length))
    .map((g) => ({
      bbox: g.box.map(r4),
      // very close shots: small islands/rocks are missing from the land polygons, so keep the raw image
      mask: g.zoom < 500,
      width: Math.max(1536, Math.min(4096, Math.round((((g.box[2] - g.box[0]) / (g.span / 1.35)) * cfg.video.width) / 256) * 256)),
    }));
}

// Blend order: coarsest (degrees per pixel) first, so sharper imagery ends up on top.
export const byCoarseness = (a, b) => (b.bbox[2] - b.bbox[0]) / (b.width || 4096) - (a.bbox[2] - a.bbox[0]) / (a.width || 4096);
