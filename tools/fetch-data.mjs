// Downloads the one-time data the pipeline needs:
//  - NASA Blue Marble (public domain) resized to 8192x4096 -> assets/earth/earth-8k.jpg
//  - Natural Earth admin-1 (states/provinces) GeoJSON -> data/cache/ne_10m_admin_1.geojson
// Usage: npm run setup
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, runFfmpeg, log } from '../src/util.mjs';

const EARTH_SOURCES = [
  // Blue Marble Next Generation w/ topography & bathymetry, July 2004 (NASA, public domain).
  // Summer month: least snow over the northern hemisphere.
  'https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73751/world.topo.bathy.200407.3x21600x10800.jpg',
  // Fallback: 4096x2048 copy of Blue Marble hosted on GitHub
  'https://raw.githubusercontent.com/vasturiano/three-globe/master/example/img/earth-blue-marble.jpg',
];
const ADMIN1_URL =
  'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_1_states_provinces.geojson';

export async function download(url, dest) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(dest, buf);
  return dest;
}

export async function ensureEarth() {
  const out = path.join(ROOT, 'assets/earth/earth-8k.jpg');
  if (fs.existsSync(out)) return out;
  for (const url of EARTH_SOURCES) {
    try {
      log('Blue Marble indiriliyor:', url);
      const raw = await download(url, path.join(ROOT, 'data/cache/earth-source.jpg'));
      await runFfmpeg(['-y', '-i', raw, '-vf', 'scale=8192:4096:flags=lanczos', '-q:v', '2', out]);
      fs.rmSync(raw);
      return out;
    } catch (e) {
      log('  olmadı:', e.message.split('\n')[0]);
    }
  }
  throw new Error('Dünya dokusu indirilemedi');
}

// NASA Black Marble 2016 (Earth at night), public domain, resampled like the day texture.
const NIGHT_URL = 'https://eoimages.gsfc.nasa.gov/images/imagerecords/144000/144898/BlackMarble_2016_3km.jpg';
export async function ensureNight() {
  const out = path.join(ROOT, 'assets/earth/night-8k.jpg');
  if (fs.existsSync(out)) return out;
  log('Black Marble (gece) indiriliyor:', NIGHT_URL);
  const raw = await download(NIGHT_URL, path.join(ROOT, 'data/cache/night-source.jpg'));
  await runFfmpeg(['-y', '-i', raw, '-vf', 'scale=8192:4096:flags=lanczos', '-q:v', '2', out]);
  fs.rmSync(raw);
  return out;
}

export async function ensureAdmin1() {
  const out = path.join(ROOT, 'data/cache/ne_10m_admin_1.geojson');
  if (fs.existsSync(out)) return out;
  log('Natural Earth admin-1 indiriliyor (~40 MB)...');
  const tmp = await download(ADMIN1_URL, out + '.tmp');
  // Keep only the fields we use, to make later loads fast.
  const gj = JSON.parse(fs.readFileSync(tmp, 'utf8'));
  const keep = ['name', 'name_en', 'name_alt', 'woe_name', 'gn_name', 'adm0_a3', 'iso_a2', 'admin', 'type_en'];
  for (const f of gj.features) {
    const p = {};
    for (const k of keep) if (f.properties[k] != null) p[k] = f.properties[k];
    f.properties = p;
  }
  fs.writeFileSync(out, JSON.stringify(gj));
  fs.rmSync(tmp);
  return out;
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('fetch-data.mjs')) {
  await ensureEarth();
  await ensureAdmin1();
  log('Veri hazır.');
}
