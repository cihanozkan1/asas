#!/usr/bin/env python3
"""Review pack for the independent reviewer (see docs/GOZDEN_GECIRICI.md).
For every scene: frames at +0.5 s, middle, -0.5 s, and 0.6 s after every effect clip / stamp starts, three per sheet
(520 px wide each, so Claude does not downscale them) plus index.md with the narration and the element list.
Usage: review_pack.py <id>   -> output/<id>/review/"""
import glob, json, os, subprocess, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
vid = sys.argv[1]
out = os.path.join(ROOT, 'output', vid)
tls = sorted(glob.glob(os.path.join(out, 'timeline.*.json')), key=os.path.getmtime)
tl = json.load(open(tls[-1])); style = os.path.basename(tls[-1]).split('.')[1]
times = []
for i, s in enumerate(tl['scenes']):
    a, b = s['start'], s['end']
    ts = [a + 0.5, (a + b) / 2, b - 0.5]
    for e in tl['elements']:
        if e['scene'] == i and e['type'] in ('clip', 'stamp', 'handstamp', 'character', 'flag') and a < e['start'] + 0.6 < b:
            ts.append(e['start'] + 0.6)
    times.append(sorted(set(round(min(max(t, a + 0.1), b - 0.1), 2) for t in ts)))
flat = sorted(set(t for ts in times for t in ts))
env = dict(os.environ, FFMPEG_PATH=os.environ.get('FFMPEG_PATH', '/usr/local/bin/ffmpeg'))
subprocess.run(['node', 'scripts/pipeline.mjs', f'videos/{vid}', '--stills', '--times', ','.join(map(str, flat)), '--scale', '0.5', '--workers', '2', '--skip-gates'], cwd=ROOT, env=env, capture_output=True)
sd = os.path.join(out, f'stills_{style}')
pick = lambda t: sorted(glob.glob(os.path.join(sd, 'still_*.jpg')), key=lambda f: abs(float(os.path.basename(f)[6:-4]) - t))[0]
rd = os.path.join(out, 'review'); os.makedirs(rd, exist_ok=True)
for f in glob.glob(os.path.join(rd, '*')): os.remove(f)
md = [f'# Review pack: {vid}\n', 'Look at each sheet at full size. Frames are left-to-right in time. Answer the checklist in docs/GOZDEN_GECIRICI.md per sheet.\n']
for i, (s, ts) in enumerate(zip(tl['scenes'], times)):
    ims = [Image.open(pick(t)).resize((520, 924)) for t in ts]
    for k in range(0, len(ims), 3):
        chunk, tch = ims[k:k + 3], ts[k:k + 3]
        sheet = Image.new('RGB', (520 * len(chunk), 924)); d = ImageDraw.Draw(sheet)
        for j, im in enumerate(chunk):
            sheet.paste(im, (j * 520, 0)); d.rectangle([j * 520, 0, j * 520 + 74, 15], fill='black'); d.text((j * 520 + 3, 2), f'{tch[j]:.1f}s', fill='yellow')
        name = f'scene{i + 1:02d}_{k // 3 + 1}.jpg'
        sheet.save(os.path.join(rd, name), quality=90)
    def desc(e):
        d = e['type'] + (' ' + e['name'] if e.get('name') else '')
        return d + (' "' + str(e.get('text'))[:30] + '"' if e.get('text') else '')
    els = [desc(e) for e in tl['elements'] if e['scene'] == i]
    md.append(f"## Scene {i + 1} ({s['start']:.1f}-{s['end']:.1f}s, era={s['era']}, style={s['style']})\n- narration: {s['text']}\n- elements: {', '.join(els)}\n- sheets: scene{i + 1:02d}_*.jpg\n")
open(os.path.join(rd, 'index.md'), 'w').write('\n'.join(md))
print(rd, len(os.listdir(rd)) - 1, 'sheets')
