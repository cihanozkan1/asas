// Policy gate (YouTube "inauthentic content" = mass-produced, templated uploads): compares a video with every other
// script in videos/ and warns when the effect set and the scene skeleton are too alike.
// Usage: node tools/gates/variety.mjs <id>        (warnings only; the human decides)
import fs from 'node:fs';
import path from 'node:path';
import { ROOT } from '../../src/util.mjs';

const sig = (script) => {
  const toks = [], skel = [];
  for (const s of script.scenes) {
    const types = new Set();
    for (const e of s.show || []) {
      const t = e.type === 'clip' ? `clip:${e.name}` : e.type === 'react' ? 'react' : e.type;
      types.add(t); toks.push(t);
    }
    skel.push([s.era, s.style || '', ...[...types].sort().slice(0, 3)].join('/'));
  }
  return { toks: new Map([...new Set(toks)].map((t) => [t, toks.filter((x) => x === t).length])), skel };
};
const jacc = (a, b) => { let i = 0, u = 0; for (const k of new Set([...a.keys(), ...b.keys()])) { i += Math.min(a.get(k) || 0, b.get(k) || 0); u += Math.max(a.get(k) || 0, b.get(k) || 0); } return u ? i / u : 0; };
const lcs = (a, b) => { const d = Array.from({ length: a.length + 1 }, () => new Array(b.length + 1).fill(0)); for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) d[i][j] = a[i - 1] === b[j - 1] ? d[i - 1][j - 1] + 1 : Math.max(d[i - 1][j], d[i][j - 1]); return d[a.length][b.length] / Math.max(a.length, b.length, 1); };

export function variety(id) {
  const me = sig(JSON.parse(fs.readFileSync(path.join(ROOT, 'videos', id, 'script.json'), 'utf8')));
  const out = [];
  for (const o of fs.readdirSync(path.join(ROOT, 'videos'))) {
    if (o === id || !fs.existsSync(path.join(ROOT, 'videos', o, 'script.json'))) continue;
    const sc = JSON.parse(fs.readFileSync(path.join(ROOT, 'videos', o, 'script.json'), 'utf8'));
    if (!sc.scenes) continue;
    const other = sig(sc);
    const j = jacc(me.toks, other.toks), l = lcs(me.skel, other.skel);
    if (j > 0.72 && l > 0.5) out.push({ sev: 'warn', kind: 'template-like', t: 0, msg: `very similar to "${o}" (element mix ${(j * 100).toFixed(0)}%, scene skeleton ${(l * 100).toFixed(0)}%): vary the structure/effects` });
  }
  return out;
}

if (process.argv[1] && process.argv[1].endsWith('variety.mjs')) {
  for (const id of process.argv.slice(2)) { const r = variety(id); console.log(`== ${id}: ${r.length} similar video(s)`); r.forEach((x) => console.log('  warn ' + x.msg)); }
}
