// Gate G4: checks on the rendered mp4 (ffmpeg detectors): black frames, frozen picture, silence gaps, clipping, length.
// Usage: node tools/gates/video.mjs <file.mp4>...      exit 1 on error
import { spawnSync } from 'node:child_process';

export function videoGate(file) {
  const ff = process.env.FFMPEG_PATH || 'ffmpeg';
  const r = spawnSync(ff, ['-hide_banner', '-nostats', '-i', file, '-vf', 'blackdetect=d=0.35:pic_th=0.97:pix_th=0.04,freezedetect=n=-45dB:d=1.5', '-af', 'silencedetect=n=-42dB:d=0.7,volumedetect', '-f', 'null', '-'], { encoding: 'utf8', maxBuffer: 1 << 26 });
  const log = r.stderr || '';
  const issues = [];
  const dur = Number((/Duration: (\d+):(\d+):([\d.]+)/.exec(log) || []).slice(1).reduce((a, v, i) => a + Number(v) * [3600, 60, 1][i], 0));
  for (const m of log.matchAll(/black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)/g)) issues.push({ sev: 'error', kind: 'black', t: +m[1], msg: `black picture for ${(+m[3]).toFixed(1)}s` });
  const fs = [...log.matchAll(/freeze_start: ([\d.]+)/g)].map((m) => +m[1]);
  const fd = [...log.matchAll(/freeze_duration: ([\d.]+)/g)].map((m) => +m[1]);
  fd.forEach((d, i) => issues.push({ sev: d >= 2.5 ? 'error' : 'warn', kind: 'freeze', t: fs[i] ?? 0, msg: `picture hardly changes for ${d.toFixed(1)}s` }));
  const ss = [...log.matchAll(/silence_start: ([\d.]+)/g)].map((m) => +m[1]);
  const sd = [...log.matchAll(/silence_duration: ([\d.]+)/g)].map((m) => +m[1]);
  sd.forEach((d, i) => { if ((ss[i] ?? 0) > 0.2 && (ss[i] ?? 0) + d < dur - 0.3) issues.push({ sev: d >= 1.2 ? 'error' : 'warn', kind: 'silence', t: ss[i], msg: `no sound for ${d.toFixed(1)}s` }); });
  const mx = /max_volume: (-?[\d.]+) dB/.exec(log);
  if (mx && +mx[1] > -0.3) issues.push({ sev: 'warn', kind: 'clipping', t: 0, msg: `peak ${mx[1]} dB (clipping)` });
  if (dur && (dur < 50 || dur > 100)) issues.push({ sev: 'warn', kind: 'length', t: 0, msg: `length ${dur.toFixed(0)}s is outside 50–100 s` });
  return { file, duration: dur, issues: issues.sort((a, b) => a.t - b.t) };
}

if (process.argv[1] && process.argv[1].endsWith('video.mjs')) {
  let bad = 0;
  for (const f of process.argv.slice(2)) {
    const r = videoGate(f);
    const err = r.issues.filter((i) => i.sev === 'error').length; bad += err;
    console.log(`\n== ${f}: ${err} error(s), ${r.issues.length - err} warning(s)`);
    for (const i of r.issues) console.log(`  ${i.t.toFixed(1).padStart(5)}s ${i.sev === 'error' ? 'ERROR' : 'warn '} [${i.kind}] ${i.msg}`);
  }
  process.exit(bad ? 1 : 0);
}
