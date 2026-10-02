// Gate self-test: the gates must catch every defect in the golden (known-bad) videos and stay silent on the current ones.
// Also mutates a real timeline to check the lifetime rules. Usage: node tools/gates/selftest.mjs [--current id,id,...]
// Golden timelines are built with: node scripts/pipeline.mjs tools/gates/golden/<name> --timeline-only --skip-route-check
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT } from '../../src/util.mjs';
import { lintVideo, lintTimeline } from './lint.mjs';
import { frameGate } from './frames.mjs';

const expect = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/gates/golden/expect.json'), 'utf8'));
const cur = (process.argv.includes('--current') ? process.argv[process.argv.indexOf('--current') + 1] : 'istanbul,point_roberts,hawaii,darien_gap,chimborazo').split(',');
let fail = 0;
const ok = (c, msg) => { console.log(`${c ? 'PASS' : 'FAIL'}  ${msg}`); if (!c) fail++; };

for (const [id, exp] of Object.entries(expect)) {
  if (id.startsWith('_')) continue;
  if (!fs.existsSync(path.join(ROOT, 'output', id))) { console.log(`skip  ${id}: build its timeline first`); continue; }
  const lint = lintVideo(id).filter((x) => x.sev === 'error').map((x) => x.kind);
  for (const k of exp.lint || []) ok(lint.includes(k), `${id}: lint reports ${k}`);
  if (exp.poly) {
    const r = spawnSync('python3', [path.join(ROOT, 'tools/gates/poly_land.py'), id], { encoding: 'utf8' });
    ok(r.status === 1 && /poly-land/.test(r.stdout), `${id}: polygon spilling into the sea is reported`);
  }
  if (exp.frames) {
    const fr = (await frameGate(id)).issues.filter((x) => x.sev === 'error').map((x) => x.kind);
    for (const k of exp.frames) ok(fr.includes(k), `${id}: frame gate reports ${k}`);
  }
}

// lifetime rules on a mutated copy of a real timeline
const base = cur[0];
const dir = path.join(ROOT, 'output', base);
const tf = fs.readdirSync(dir).filter((f) => /^timeline\..+\.json$/.test(f))[0];
const tl = JSON.parse(fs.readFileSync(path.join(dir, tf), 'utf8'));
const clone = () => JSON.parse(JSON.stringify(tl));
let m = clone(); const clip = m.elements.find((e) => e.type === 'clip' && !e.loop);
if (clip) { clip.end += 3; ok(lintTimeline(m).some((x) => x.kind === 'freeze'), 'mutation: a clip held 3s past its frames is a freeze'); }
m = clone(); const lab = m.elements.find((e) => e.type === 'label' && e.scene < m.scenes.length - 2);
if (lab) { lab.end = m.scenes[lab.scene].end + 4; ok(lintTimeline(m).some((x) => x.kind === 'leak'), 'mutation: a label outliving its scene is a leak'); }
m = clone(); const rt = m.elements.find((e) => e.type === 'highlight' && e.scene < m.scenes.length - 2);
if (rt) { m.scenes[rt.scene + 1].era = m.scenes[rt.scene].era === 'now' ? 'history' : 'now'; rt.end = m.scenes[rt.scene + 1].end; ok(lintTimeline(m).some((x) => x.kind === 'leak'), 'mutation: a map highlight crossing an era change is a leak'); }
m = clone(); const e0 = m.elements.find((e) => e.type === 'year' || e.type === 'counter');
if (e0) { e0.start = m.duration + 5; ok(lintTimeline(m).some((x) => x.kind === 'never-visible'), 'mutation: an element starting after the video is never visible'); }

// the current videos must be clean
for (const id of cur) {
  if (!fs.existsSync(path.join(ROOT, 'output', id))) continue;
  const lint = lintVideo(id).filter((x) => x.sev === 'error');
  const fr = (await frameGate(id)).issues.filter((x) => x.sev === 'error');
  const pl = spawnSync('python3', [path.join(ROOT, 'tools/gates/poly_land.py'), id], { encoding: 'utf8' });
  ok(!lint.length && !fr.length && pl.status === 0, `${id}: no gate errors (${lint.length + fr.length + (pl.status ? 1 : 0)})`);
}
console.log(fail ? `\n${fail} self-test(s) FAILED` : '\nall self-tests passed');
process.exit(fail ? 1 : 0);
