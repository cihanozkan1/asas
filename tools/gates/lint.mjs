// Gate G1: timeline + script lint (no render needed).
//   leak          an element outlives its scene (or a persistent map element crosses an era/style change)
//   freeze        a once-playing clip is held longer than its frames (frozen last frame)
//   no-reason     an effect clip whose scene narration has no word justifying it (assets/vfx/MEANING.json)
//   unbound       an effect clip placed at a raw number instead of a narration word
//   flag-style    flag markers with different looks (pin / wave) in one scene
// Usage: node tools/gates/lint.mjs <id>...     exit 1 on error
import fs from 'node:fs';
import path from 'node:path';
import { ROOT } from '../../src/util.mjs';

const PERSIST = new Set(['highlight', 'route', 'wall', 'dim', 'grade', 'bridge', 'pathtext', 'crowd', 'scatter', 'tilt']);
const MEANING = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/vfx/MEANING.json'), 'utf8'));

export function lintTimeline(tl) {
  const out = [];
  const sc = tl.scenes;
  tl.elements.forEach((e) => {
    if (e.type === 'title') return;
    const s = sc[e.scene];
    if (!s) return;
    const tag = `${e.type}${e.name ? ' ' + e.name : ''}${e.text ? ' "' + String(e.text).slice(0, 24) + '"' : ''}`;
    if (e.start > s.end + 0.05 || e.start >= tl.duration - 0.3) out.push({ sev: 'error', kind: 'never-visible', t: s.start, msg: `${tag} would start at ${e.start.toFixed(1)}s, after its scene ends (a number passed as the time?)` });
    const over = e.end - s.end;
    if (PERSIST.has(e.type)) {
      if (over > 0.3) {
        for (let j = e.scene + 1; j < sc.length && sc[j].start < e.end - 0.05; j++) {
          if (sc[j].era !== s.era || sc[j].style !== s.style) { out.push({ sev: 'error', kind: 'leak', t: sc[j].start, msg: `${tag} (scene ${e.scene + 1}) is still on screen in scene ${j + 1}, which changes era/style` }); break; }
        }
      }
    } else if (e.screen ? over > 0.85 : over > 0.35) {
      out.push({ sev: 'error', kind: 'leak', t: s.end, msg: `${tag} outlives its scene by ${over.toFixed(1)}s` });
    }
    if (e.type === 'clip' && !e.loop && e.n && e.fps) {
      const dur = e.n / (e.fps * (e.speed || 1)), shown = e.end - e.start;
      if (shown > dur + 0.2) out.push({ sev: 'error', kind: 'freeze', t: e.start + dur, msg: `${tag} is held ${(shown - dur).toFixed(1)}s after its ${dur.toFixed(1)}s of frames (frozen frame)` });
    }
  });
  // retention: something must visibly change at least every ~3 s (element appears, route/clip plays, camera moves, scene cut)
  const spans = sc.map((x) => [x.start, x.start + 0.4]);
  for (const x of sc) for (const c of (x.cameraThen || [])) if (c && Number.isFinite(c.t)) spans.push([c.t, c.t + (c.duration || 1)]);
  for (const e of tl.elements) {
    if (['dim', 'grade', 'tilt'].includes(e.type)) continue;
    const dur = e.type === 'route' ? Math.min(e.end - e.start, e.drawDur || 1) : e.type === 'clip' ? Math.min(e.end - e.start, 1.4) : e.type === 'counter' ? 1.2 : 0.5;
    spans.push([e.start, e.start + dur]);
    for (const st of e.steps || []) if (Number.isFinite(st.t)) spans.push([st.t, st.t + 0.8]);
    for (const c of e.counts || []) if (Number.isFinite(c.t)) spans.push([c.t, c.t + 0.8]);
    if (e.type === 'scatter') spans.push([e.start, e.start + (e.stagger || 0.2) * (e.count || 3) + 0.6]);
  }
  spans.sort((p, q) => p[0] - q[0]);
  let cover = 0;
  for (const [a0, a1] of spans) {
    if (a0 - cover > 3.6 && cover > 0.5) out.push({ sev: a0 - cover > 5.5 ? 'error' : 'warn', kind: 'static-gap', t: cover, msg: `nothing changes on screen for ${(a0 - cover).toFixed(1)}s (add an element/camera move at a spoken word)` });
    cover = Math.max(cover, a1);
  }
  if (tl.duration - cover > 3.8) out.push({ sev: 'warn', kind: 'static-gap', t: cover, msg: `nothing changes on screen for the last ${(tl.duration - cover).toFixed(1)}s` });
  return out;
}

export function lintScript(script) {
  const out = [];
  script.scenes.forEach((s, i) => {
    const text = (s.text || '').toLowerCase();
    const flags = [];
    for (const e of s.show || []) {
      if (e.type === 'flag') flags.push(`${!!e.pin}|${!!e.wave}`);
      if (e.type !== 'clip' || !String(e.name).startsWith('emoji_')) continue;
      const rx = MEANING[e.name];
      const why = e.why ? String(e.why).toLowerCase() : null;
      if (!rx) out.push({ sev: 'error', kind: 'no-reason', t: 0, msg: `scene ${i + 1}: ${e.name} has no entry in assets/vfx/MEANING.json` });
      else if (!(new RegExp(rx, 'i').test(text) || (why && text.includes(why)))) out.push({ sev: 'error', kind: 'no-reason', t: 0, msg: `scene ${i + 1}: ${e.name} is not justified by the narration "${s.text.slice(0, 60)}…" (needs one of: ${rx})` });
      if (typeof e.at === 'number' && e.at > 0.2 && !e.screen) out.push({ sev: 'warn', kind: 'unbound', t: 0, msg: `scene ${i + 1}: ${e.name} placed at ${e.at}s instead of a narration word` });
    }
    if (new Set(flags).size > 1) out.push({ sev: 'error', kind: 'flag-style', t: 0, msg: `scene ${i + 1}: flag markers mix looks (pin/wave): ${[...new Set(flags)].join(', ')}` });
  });
  return out;
}

export function lintVideo(id) {
  const dir = path.join(ROOT, 'output', id);
  const file = fs.readdirSync(dir).filter((f) => /^timeline\..+\.json$/.test(f)).sort((a, b) => fs.statSync(path.join(dir, b)).mtimeMs - fs.statSync(path.join(dir, a)).mtimeMs)[0];
  const tl = JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8'));
  let sp = path.join(ROOT, 'videos', id, 'script.json');
  if (!fs.existsSync(sp)) sp = path.join(ROOT, 'tools/gates/golden', id.replace(/^g_/, ''), 'script.json'); // golden (known-bad) cases
  const script = JSON.parse(fs.readFileSync(sp, 'utf8'));
  return [...lintTimeline(tl), ...lintScript(script)].sort((a, b) => a.t - b.t);
}

if (process.argv[1] && process.argv[1].endsWith('lint.mjs')) {
  let bad = 0;
  for (const id of process.argv.slice(2)) {
    const r = lintVideo(id);
    const err = r.filter((x) => x.sev === 'error').length; bad += err;
    console.log(`\n== ${id}: ${err} error(s), ${r.length - err} warning(s)`);
    for (const x of r) console.log(`  ${x.t.toFixed(1).padStart(5)}s ${x.sev === 'error' ? 'ERROR' : 'warn '} [${x.kind}] ${x.msg}`);
  }
  process.exit(bad ? 1 : 0);
}
