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
    const res = await fetch(url);
    const type = res.headers.get('content-type') || '';
    if (!res.ok || !type.includes('image')) throw new Error(`EOX WMS hatası ${res.status} ${type}`);
    fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()));
  }
  return { url: '/' + rel, bbox };
}
