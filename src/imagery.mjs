// High-resolution detail imagery for close-up shots:
// Sentinel-2 cloudless 2016 by EOX (CC BY 4.0), fetched as an equirectangular WMS image.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT, log } from './util.mjs';

export const S2_CREDIT =
  'Satellite imagery: Sentinel-2 cloudless 2016 - https://s2maps.eu by EOX IT Services GmbH (Contains modified Copernicus Sentinel data 2016), CC BY 4.0';
export const BLUE_MARBLE_CREDIT = 'Earth imagery: NASA Blue Marble (NASA Earth Observatory)';
export const NE_CREDIT = 'Map data: Natural Earth';

// bbox: [west, south, east, north] in degrees. width: pixels (height follows the bbox aspect).
export async function ensureDetail({ bbox, width = 4096 }) {
  const [w, s, e, n] = bbox;
  const height = Math.min(4096, Math.round((width * (n - s)) / (e - w)));
  const key = crypto.createHash('sha1').update(JSON.stringify({ bbox, width, height, v: 1 })).digest('hex').slice(0, 12);
  const rel = `cache/imagery/s2_${key}.jpg`;
  const file = path.join(ROOT, rel);
  if (!fs.existsSync(file)) {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    const url =
      'https://tiles.maps.eox.at/wms?service=WMS&request=GetMap&version=1.1.1&layers=s2cloudless&styles=' +
      `&srs=EPSG:4326&bbox=${w},${s},${e},${n}&width=${width}&height=${height}&format=image/jpeg`;
    log(`Sentinel-2 görüntü indiriliyor ${bbox.join(',')} (${width}x${height})`);
    // big WMS images occasionally get cut off mid-transfer: retry a few times
    for (let attempt = 1; ; attempt++) {
      try {
        const res = await fetch(url);
        const type = res.headers.get('content-type') || '';
        if (!res.ok || !type.includes('image')) throw new Error(`EOX WMS hatası ${res.status} ${type}`);
        fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()));
        break;
      } catch (e) {
        if (attempt >= 4) throw e;
        log(`Sentinel-2 indirme hatası (${e.message}), tekrar deneniyor ${attempt}/3`);
        await new Promise((r) => setTimeout(r, 2000 * attempt));
      }
    }
  }
  return { url: '/' + rel, bbox, mask: arguments[0].mask !== false };
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
    const halfLat = half * aspect * Math.cos((lat * Math.PI) / 180);
    views.push({ zoom, span: half * 2, box: [lon - half, lat - halfLat, lon + half, lat + halfLat] });
  };
  script.scenes.forEach((s, i) => {
    const c = s.camera;
    if (!c || c.fit || c.follow || c.lat == null || !(c.zoom >= minZoom)) return;
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
    // merge into a group if the union still gives >= ~0.75 texel per output pixel for its tightest view
    let best = null;
    for (const g of groups) {
      const u = [Math.min(g.box[0], v.box[0]), Math.min(g.box[1], v.box[1]), Math.max(g.box[2], v.box[2]), Math.max(g.box[3], v.box[3])];
      const need = ((u[2] - u[0]) / Math.min(g.span, v.span)) * cfg.video.width * 0.75;
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
      width: Math.max(1536, Math.min(4096, Math.round((((g.box[2] - g.box[0]) / g.span) * cfg.video.width * 0.75) / 256) * 256)),
    }));
}

// Blend order: coarsest (degrees per pixel) first, so sharper imagery ends up on top.
export const byCoarseness = (a, b) => (b.bbox[2] - b.bbox[0]) / (b.width || 4096) - (a.bbox[2] - a.bbox[0]) / (a.width || 4096);
