#!/usr/bin/env node
// Render a Remotion composition (remotion/src/*) as a transparent PNG sequence and add it to the VFX library.
//   node tools/remotion_clip.mjs <Composition> <clipName> [--props '{"country":"792"}'] [--frames 0-59] [--width 540] [--fps 24] [--still]
// Compositions: EmojiPop, LottieBurst, GlowBorder, ArmyArrow, TripsDemo, GlobeArcs, GifLayer (see docs/ARAC_KUTUSU.md).
// Result: assets/vfx/<clipName>/ — use it in a script with  clip('<clipName>', at, lat=, lon=, size=, loop=...).
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const R = path.join(ROOT, 'remotion');
const a = process.argv.slice(2);
const flag = (n, d) => { const i = a.indexOf('--' + n); return i >= 0 ? a[i + 1] : d; };
const [comp, name] = a.filter((x, i) => !x.startsWith('--') && !(i > 0 && a[i - 1].startsWith('--') && a[i - 1] !== '--still'));
if (!comp || !name) { console.error('usage: remotion_clip.mjs <Composition> <clipName> [--props json] [--frames a-b] [--width 540] [--fps 24]'); process.exit(1); }
const out = path.join(R, 'out', 'seq_' + name);
fs.rmSync(out, { recursive: true, force: true });
const args = ['remotion', 'render', 'src/index.ts', comp, out, '--sequence', '--image-format=png', '--timeout=180000', '--chrome-mode=chrome-for-testing', '--browser-executable=' + path.join(R, 'chrome-wrapper.sh')];
if (flag('props')) args.push('--props=' + flag('props'));
if (flag('frames')) args.push('--frames=' + flag('frames'));
let r = spawnSync('npx', args, { cwd: R, stdio: 'inherit' });
if (r.status) process.exit(r.status);
r = spawnSync('python3', [path.join(ROOT, 'tools/vfx_ingest.py'), out, name, '--key', 'alpha', '--width', flag('width', '540'), '--fps', flag('fps', '30'), '--dur', '20', '--source', 'remotion/src/' + comp, '--note', 'rendered with Remotion, transparent'], { stdio: 'inherit' });
process.exit(r.status || 0);
