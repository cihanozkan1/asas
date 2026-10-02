// Runs every gate for a video and writes output/<id>/gates.json.
//   node tools/gates/run.mjs <id> [--pre]     --pre: before rendering (lint + polygon + frames); default also checks the finished mp4
// Exit code 1 when any gate reports an error. The pipeline calls this; do not skip it to "get the video out".
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT } from '../../src/util.mjs';
import { lintVideo } from './lint.mjs';
import { frameGate } from './frames.mjs';
import { videoGate } from './video.mjs';
import { variety } from './variety.mjs';

export async function runGates(id, { pre = false, file = null, fps = 5 } = {}) {
  const res = { id, when: new Date().toISOString(), gates: {} };
  const take = (name, issues) => { res.gates[name] = { errors: issues.filter((i) => i.sev === 'error'), warnings: issues.filter((i) => i.sev !== 'error') }; };
  take('lint', lintVideo(id));
  const pl = spawnSync('python3', [path.join(ROOT, 'tools/gates/poly_land.py'), id], { encoding: 'utf8' });
  take('poly', [...pl.stdout.matchAll(/(ERROR|warn ) \[poly-land\] (.*)/g)].map((m) => ({ sev: m[1] === 'ERROR' ? 'error' : 'warn', kind: 'poly-land', t: 0, msg: m[2] })));
  take('frames', (await frameGate(id, { fps })).issues);
  try { take('variety', variety(id)); } catch { /* video not in videos/ (golden) */ }
  if (!pre && file) take('video', videoGate(file).issues);
  res.pass = Object.values(res.gates).every((g) => !g.errors.length);
  fs.writeFileSync(path.join(ROOT, 'output', id, 'gates.json'), JSON.stringify(res, null, 1));
  return res;
}

export function printGates(r) {
  for (const [name, g] of Object.entries(r.gates)) {
    console.log(`  gate ${name}: ${g.errors.length} error(s), ${g.warnings.length} warning(s)`);
    for (const i of [...g.errors, ...g.warnings]) console.log(`    ${(i.t ?? 0).toFixed(1).padStart(5)}s ${i.sev === 'error' ? 'ERROR' : 'warn '} [${i.kind}] ${i.msg}${i.dur ? ` (${i.dur}s)` : ''}`);
  }
}

if (process.argv[1] && process.argv[1].endsWith('run.mjs')) {
  const args = process.argv.slice(2);
  const pre = args.includes('--pre');
  let bad = 0;
  for (const id of args.filter((a) => !a.startsWith('--'))) {
    const dir = path.join(ROOT, 'output', id);
    const mp4 = fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => f.startsWith(id + '_') && f.endsWith('.mp4')).map((f) => path.join(dir, f))[0] : null;
    const r = await runGates(id, { pre, file: mp4 });
    console.log(`\n== ${id}: ${r.pass ? 'GATES PASSED' : 'GATES FAILED'}`);
    printGates(r);
    if (!r.pass) bad++;
  }
  process.exit(bad ? 1 : 0);
}
