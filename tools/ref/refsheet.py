#!/usr/bin/env python3
"""refsheet.py video fps start dur [cols] [w] -> rs/<name>_<start>.jpg, frames labelled with time (s)."""
import sys, os, subprocess, glob, shutil, math
from PIL import Image, ImageDraw, ImageFont
SP = os.environ.get('REF_OUT', '/tmp/refsheets'); os.makedirs(SP + '/rs', exist_ok=True)
v, fps, ss, dur = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 10
w = int(sys.argv[6]) if len(sys.argv) > 6 else 180
name = os.path.basename(v)[:-4]
tmp = f'{SP}/rs/_t_{name}'
shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
subprocess.run([os.environ.get('FFMPEG_PATH', 'ffmpeg'), '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', v, '-vf', f'fps={fps},scale={w}:-1', '-q:v', '3', f'{tmp}/f_%04d.jpg'], check=True)
fs = sorted(glob.glob(f'{tmp}/f_*.jpg'))
ims = [Image.open(f) for f in fs]
h = ims[0].size[1]
rows = math.ceil(len(ims) / cols)
sheet = Image.new('RGB', (cols * (w + 2), rows * (h + 2)), 'white')
d = ImageDraw.Draw(sheet)
for i, im in enumerate(ims):
    x, y = (i % cols) * (w + 2), (i // cols) * (h + 2)
    sheet.paste(im, (x, y))
    t = f'{ss + i / fps:.1f}'
    d.rectangle([x, y, x + 34, y + 13], fill='black'); d.text((x + 2, y + 1), t, fill='yellow')
out = f'{SP}/rs/{name}_{int(ss)}.jpg'
sheet.save(out, quality=82)
shutil.rmtree(tmp, ignore_errors=True)
print(out, sheet.size)
