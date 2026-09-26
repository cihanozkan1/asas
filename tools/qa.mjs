// Readability QA for a rendered video's timeline: steps through the page and reports
//  - elements that are on screen too briefly, or pop up at the very end of their scene
//  - UI elements that overlap each other or the captions
//  - UI outside the safe area (bottom YouTube bar, right-hand button column)
// Usage: node tools/qa.mjs <video-id>... [--fps 4] [--json out.json]
import fs from 'node:fs';
import path from 'node:path';
import { openPage } from '../src/render.mjs';
import { ROOT } from '../src/util.mjs';

const args = process.argv.slice(2);
const opt = (k, d) => {
  const i = args.indexOf(k);
  if (i < 0) return d;
  const v = args[i + 1];
  args.splice(i, 2);
  return v;
};
const FPS = Number(opt('--fps', 4));
const jsonOut = opt('--json', null);
const ids = args;

const MIN_VISIBLE = 2.0; // seconds fully visible
const LATE = 1.0; // appears in the last second of its scene...
const GONE = 1.2; // ...and is gone within this long after the scene ends

const area = (r) => r.w * r.h;
function inter(a, b) {
  const w = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
  const h = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
  return w > 0 && h > 0 ? w * h : 0;
}
const fmt = (t) => t.toFixed(1) + 's';

async function qa(id) {
  const dir = path.join(ROOT, 'output', id);
  const file = fs.readdirSync(dir).filter((f) => /^timeline\..+\.json$/.test(f))
    .sort((a, b) => fs.statSync(path.join(dir, b)).mtimeMs - fs.statSync(path.join(dir, a)).mtimeMs)[0];
  if (!file) throw new Error(`${id}: no timeline json (run the pipeline first)`);
  const tl = JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8'));
  const { page, close } = await openPage(tl, 0.25);
  await page.evaluate(() => window.GG.fast(true)); // positions only: skip the raster/vector drawing
  const W = tl.W, H = tl.H;
  const safe = tl.config.safe || { bottom: 0.17 };
  const seen = new Map(); // i -> {el, times:[]}
  const pairs = new Map(); // "i|j" -> {a,b,times:[]}
  const capHits = new Map();
  const unsafe = new Map();
  let scenes = [];
  try {
    for (let t = 0; t < tl.duration; t += 1 / FPS) {
      await page.evaluate((tt) => window.GG.frame(tt), t);
      const p = await page.evaluate(() => window.GG.probe());
      scenes = p.scenes;
      for (const e of p.els) {
        if (!seen.has(e.i)) seen.set(e.i, { el: e, times: [] });
        seen.get(e.i).times.push(t);
        // safe area: bottom bar and the right-hand buttons (like/comment/share) column
        const bottom = e.y + e.h > H * (1 - safe.bottom) + 4;
        const right = e.x + e.w > W * (1 - (safe.right ?? 0.13)) + 4 && e.y + e.h > H * 0.45;
        const off = e.x < -4 || e.x + e.w > W + 4 || e.y < -4;
        if ((bottom || right || off) && e.type !== 'route' && e.type !== 'measure') {
          const k = e.i;
          if (!unsafe.has(k)) unsafe.set(k, { el: e, times: [], why: bottom ? 'bottom' : right ? 'right' : 'off-screen' });
          unsafe.get(k).times.push(t);
        }
        if (p.cap && inter(e, p.cap) > 0.12 * Math.min(area(e), area(p.cap))) {
          if (!capHits.has(e.i)) capHits.set(e.i, { el: e, times: [] });
          capHits.get(e.i).times.push(t);
        }
      }
      for (let a = 0; a < p.els.length; a++) {
        for (let b = a + 1; b < p.els.length; b++) {
          const A = p.els[a], B = p.els[b];
          const ov = inter(A, B);
          if (ov <= 0.15 * Math.min(area(A), area(B))) continue;
          const k = `${A.i}|${B.i}`;
          if (!pairs.has(k)) pairs.set(k, { a: A, b: B, times: [] });
          pairs.get(k).times.push(t);
        }
      }
    }
  } finally {
    await close();
  }
  const issues = [];
  const dt = 1 / FPS;
  for (const { el, times } of seen.values()) {
    const vis = times.length * dt;
    const sc = scenes[el.scene] || [0, tl.duration];
    const first = times[0], last = times[times.length - 1];
    if (vis < MIN_VISIBLE) issues.push({ kind: 'short', t: first, msg: `${el.type} "${el.text}" only ${vis.toFixed(1)}s on screen` });
    else if (first > sc[1] - LATE && last < sc[1] + GONE) issues.push({ kind: 'late', t: first, msg: `${el.type} "${el.text}" appears at the end of its scene and leaves with it` });
  }
  for (const { a, b, times } of pairs.values()) {
    if (times.length * dt < 0.3) continue;
    issues.push({ kind: 'overlap', t: times[0], msg: `${a.type} "${a.text}" overlaps ${b.type} "${b.text}" for ${(times.length * dt).toFixed(1)}s` });
  }
  for (const { el, times } of capHits.values()) {
    if (times.length * dt < 0.3) continue;
    issues.push({ kind: 'caption', t: times[0], msg: `${el.type} "${el.text}" covers the captions for ${(times.length * dt).toFixed(1)}s` });
  }
  for (const { el, times, why } of unsafe.values()) {
    if (times.length * dt < 0.3) continue;
    issues.push({ kind: 'unsafe', t: times[0], msg: `${el.type} "${el.text}" is in the ${why} UI zone for ${(times.length * dt).toFixed(1)}s` });
  }
  issues.sort((x, y) => x.t - y.t);
  return { id, duration: tl.duration, issues };
}

const all = [];
for (const id of ids) {
  const r = await qa(id);
  all.push(r);
  const by = {};
  for (const i of r.issues) by[i.kind] = (by[i.kind] || 0) + 1;
  console.log(`\n== ${id} (${r.duration.toFixed(0)}s): ${r.issues.length} issue(s) ${JSON.stringify(by)}`);
  for (const i of r.issues) console.log(`  ${fmt(i.t).padStart(6)} [${i.kind}] ${i.msg}`);
}
if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(all, null, 1));
