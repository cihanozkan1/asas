// Gate G2: frame-by-frame geometry of the real page. Every element reports its box (DOM) or exact shape mask
// (canvas highlights); this finds what a human would see at a glance:
//   text-overlap, text-on-visual, visual-overlap, flag-flag (real shape overlap), flag-on-fill, covers-subject,
//   off-screen, unsafe, caption-cover.
// Usage: node tools/gates/frames.mjs <id>... [--fps 5] [--json out.json]     exit 1 when an error is found
import fs from 'node:fs';
import path from 'node:path';
import { openPage } from '../../src/render.mjs';
import { ROOT } from '../../src/util.mjs';

export const TEXT = new Set(['label', 'counter', 'year', 'title', 'stamp', 'handstamp', 'pathtext', 'measure', 'timebar', 'bars', 'callout', 'tally', 'timeline', 'clock', 'stat', 'nametag', 'vs']);
export const VISUAL = new Set(['flag', 'icon', 'art', 'character', 'react', 'question', 'clip', 'photo', 'avatar', 'pin', 'ellipse', 'disc', 'face', 'badge']);
const COMBOS = [['emoji_collision', 'emoji_fire'], ['emoji_collision', 'emoji_direct-hit'], ['emoji_fire', 'emoji_direct-hit'], ['emoji_rain-cloud', 'emoji_droplet'], ['emoji_snake', 'emoji_mosquito']];
const area = (r) => r.w * r.h;
function inter(a, b) {
  const w = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
  const h = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
  return w > 0 && h > 0 ? w * h : 0;
}
const frac = (a, b) => inter(a, b) / Math.max(1, Math.min(area(a), area(b)));
const label = (e) => `${e.type}${e.name ? ' ' + e.name : ''}${e.text ? ' "' + String(e.text).slice(0, 28) + '"' : ''}`;

export async function frameGate(id, { fps = 5, tl: tlIn = null, dir = null } = {}) {
  const odir = dir || path.join(ROOT, 'output', id);
  let tl = tlIn;
  if (!tl) {
    const file = fs.readdirSync(odir).filter((f) => /^timeline\..+\.json$/.test(f)).sort((a, b) => fs.statSync(path.join(odir, b)).mtimeMs - fs.statSync(path.join(odir, a)).mtimeMs)[0];
    if (!file) throw new Error(`${id}: no timeline json`);
    tl = JSON.parse(fs.readFileSync(path.join(odir, file), 'utf8'));
  }
  const W = tl.W, H = tl.H, safe = tl.config.safe || { bottom: 0.17, right: 0.13 };
  const { page, close } = await openPage(tl, 0.25);
  await page.evaluate(() => window.GG.fast(true));
  const hits = new Map(); // key -> {kind, severity, msg, times:[]}
  const hit = (kind, sev, key, msg, t, cross = false) => {
    const k = `${kind}|${key}`;
    if (!hits.has(k)) hits.set(k, { kind, sev, msg, times: [], cross });
    hits.get(k).times.push(t);
  };
  try {
    for (let t = 0; t < tl.duration; t += 1 / fps) {
      await page.evaluate((tt) => window.GG.frame(tt), t);
      const p = await page.evaluate(() => window.GG.probe());
      const els = p.els.filter((e) => e.type !== 'route' && e.type !== 'wall' && e.type !== 'bridge' && e.type !== 'crowd');
      const byIdx = new Map(p.els.map((e) => [e.i, e]));
      for (let a = 0; a < els.length; a++) {
        const A = els[a];
        const aT = TEXT.has(A.type), aV = VISUAL.has(A.type);
        // off-screen: the thing being talked about is not in the frame
        if (aV || (aT && A.anchored)) {
          const vis = inter(A, { x: 0, y: 0, w: W, h: H }) / Math.max(1, area(A));
          if (vis < 0.6 && !(A.type === 'clip' && vis > 0.3)) hit('off-screen', 'error', A.i, `${label(A)} is ${Math.round((1 - vis) * 100)}% outside the frame`, t);
        }
        // safe area (YouTube UI)
        if (aT && A.type !== 'measure') {
          const bottom = A.y + A.h > H * (1 - safe.bottom) + 4, right = A.x + A.w > W * (1 - (safe.right ?? 0.13)) + 4 && A.y + A.h > H * 0.45;
          if (bottom || right) hit('unsafe', 'warn', A.i, `${label(A)} sits in the ${bottom ? 'bottom' : 'right'} YouTube UI zone`, t);
        }
        if (p.cap && (aT || aV) && frac(A, p.cap) > 0.12) hit('caption-cover', 'error', A.i, `${label(A)} covers the captions`, t);
        // marked points / small highlighted areas must stay uncovered
        for (const m of p.markers) {
          if (m.owner === A.i || !(aT || aV)) continue;
          const ov = inter(A, m) / area(m);
          if (ov > 0.25 && !(A.type === 'clip' && /_(sos|police)/.test(A.name || '') === false && false)) hit('covers-subject', 'error', `${A.i}|${m.owner}`, `${label(A)} covers the marked ${m.kind} (${Math.round(ov * 100)}% of it)`, t);
        }
        for (let b = a + 1; b < els.length; b++) {
          const B = els[b];
          const bT = TEXT.has(B.type), bV = VISUAL.has(B.type);
          if (!((aT || aV) && (bT || bV))) continue;
          const f = frac(A, B);
          if (f <= 0) continue;
          const key = `${A.i}|${B.i}`;
          const cross = A.scene !== B.scene; // outgoing and incoming scene elements cross-fade for a moment
          if (aT && bT) { if (f > 0.1) hit('text-overlap', 'error', key, `${label(A)} overlaps ${label(B)}`, t, cross); continue; }
          if ((aT && bV) || (aV && bT)) {
            const V = aV ? A : B;
            if (f > 0.15) hit('text-on-visual', 'error', key, `${label(A)} overlaps ${label(B)}`, t, cross);
            continue;
          }
          // visual vs visual
          if (A.type === 'clip' && B.type === 'clip') {
            // effects may stack only in combinations that read as one event; anything else is clutter (fire on a volcano)
            if (A.name !== B.name && f > 0.4 && !COMBOS.some(([x, y]) => (x === A.name && y === B.name) || (x === B.name && y === A.name))) hit('stacked-effects', 'error', key, `${label(A)} is stacked on ${label(B)}`, t, cross);
            continue;
          }
          const hasFlag = A.type === 'flag' || B.type === 'flag';
          const hasClip = A.type === 'clip' || B.type === 'clip';
          if (f > 0.12) hit('visual-overlap', hasFlag || !hasClip ? 'error' : 'warn', key, `${label(A)} overlaps ${label(B)}`, t, cross);
        }
      }
      // flag fills painted on the map: the real shapes may not overlap each other, nor sit under a flag marker
      for (const q of p.hlPairs) {
        if (!(q.frac > 0.02 && /^flag:/.test(q.fa) && /^flag:/.test(q.fb))) continue;
        // an enclave painted on top of the surrounding country is fine; the smaller flag being covered is not
        const smallerFirst = q.na <= q.nb; // a < b always: a is painted first
        if (smallerFirst) hit('flag-flag', 'error', `${q.a}|${q.b}`, `flag fill ${q.fa} is covered by ${q.fb} (${Math.round(q.frac * 100)}% of the smaller)`, t);
        else if (q.frac < 0.85) hit('flag-flag', 'warn', `${q.a}|${q.b}`, `flag fills ${q.fa} and ${q.fb} partly overlap (${Math.round(q.frac * 100)}%)`, t);
      }
      for (const q of p.hlBoxes) {
        const e = byIdx.get(q.el);
        if (!e || !q.hlFlag) continue;
        if (e.type === 'flag' && q.frac > 0.1) hit('flag-on-fill', 'error', `${q.hl}|${q.el}`, `flag marker ${e.name} sits on the ${q.hlFill} fill (${Math.round(q.frac * 100)}%)`, t);
        else if (VISUAL.has(e.type) && e.type !== 'clip' && q.frac > 0.3) hit('flag-on-fill', 'warn', `${q.hl}|${q.el}`, `${label(e)} sits on the ${q.hlFill} fill`, t);
      }
    }
  } finally {
    await close();
  }
  const dt = 1 / fps;
  const issues = [];
  const MIN = { 'off-screen': 0.5, unsafe: 0.6 };
  for (const h of hits.values()) {
    const dur = h.times.length * dt;
    if (dur < (MIN[h.kind] ?? 0.3) || (h.cross && dur < 0.7)) continue;
    issues.push({ kind: h.kind, sev: h.sev, t: h.times[0], dur: +dur.toFixed(1), msg: h.msg });
  }
  issues.sort((a, b) => a.t - b.t);
  return { id, duration: tl.duration, issues };
}

if (process.argv[1] && process.argv[1].endsWith('frames.mjs')) {
  const args = process.argv.slice(2);
  const opt = (k, d) => { const i = args.indexOf(k); if (i < 0) return d; const v = args[i + 1]; args.splice(i, 2); return v; };
  const fps = Number(opt('--fps', 5)), jsonOut = opt('--json', null);
  let bad = 0; const all = [];
  for (const id of args) {
    const r = await frameGate(id, { fps });
    all.push(r);
    const err = r.issues.filter((i) => i.sev === 'error').length;
    bad += err;
    console.log(`\n== ${id}: ${err} error(s), ${r.issues.length - err} warning(s)`);
    for (const i of r.issues) console.log(`  ${i.t.toFixed(1).padStart(5)}s ${i.sev === 'error' ? 'ERROR' : 'warn '} [${i.kind}] ${i.msg} (${i.dur}s)`);
  }
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(all, null, 1));
  process.exit(bad ? 1 : 0);
}
