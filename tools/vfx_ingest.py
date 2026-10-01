#!/usr/bin/env python3
"""Turn any local VFX video (downloaded free pack, ProRes/MOV/WebM/MP4) into the renderer's frame-sequence format.

  python3 tools/vfx_ingest.py <file> <name> [--key none|alpha|black|green] [--start 0] [--dur 6] [--fps 24] [--width 540]
                              [--license "ActionVFX free licence"] [--source <url>] [--note "..."]

  --key alpha  source already has transparency (ProRes 4444, WebM VP9 alpha, PNG sequence)
  --key black  footage shot on black (fire, smoke, explosions): brightness becomes opacity (luma key)
  --key green  green-screen footage (chroma key)
  --key none   opaque footage (a card / full-frame B-roll)
Writes assets/vfx/<name>/f0001.webp ... + an entry in assets/vfx/MANIFEST.json and a licence line in docs/LISANSLAR.md.
Use in a script:  clip('<name>', at, lat=.., lon=.., size=420, blend='screen'|None)
"""
import sys, os, json, subprocess, datetime, shutil, tempfile
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.environ.get('FFMPEG_PATH', 'ffmpeg')


def arg(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def ingest(src, name, key='none', start=0.0, dur=6.0, fps=24, width=540, lic='', source='', note=''):
    out = os.path.join(ROOT, 'assets/vfx', name)
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.startswith('f') and f.endswith(('.webp', '.jpg')):
            os.remove(os.path.join(out, f))
    tmp = tempfile.mkdtemp()
    vf = f'fps={fps},scale={width}:-2'
    pix = ['-pix_fmt', 'rgba'] if key in ('alpha', 'green') else []
    if key == 'green':
        vf = 'chromakey=0x00ff00:0.28:0.12,' + vf
    subprocess.run([FF, '-v', 'error', '-y', '-ss', str(start), '-t', str(dur), '-i', src, '-vf', vf, *pix, os.path.join(tmp, 'f%04d.png')], check=True)
    frames = sorted(f for f in os.listdir(tmp) if f.endswith('.png'))
    for i, f in enumerate(frames, 1):
        im = Image.open(os.path.join(tmp, f))
        if key == 'black':
            a = np.asarray(im.convert('RGB')).astype(np.float32)
            m = a.max(axis=2)
            alpha = np.clip((m - 6) * 1.25, 0, 255)                    # a little floor so compression noise stays clear
            rgb = np.where(m[..., None] > 0, a * (255.0 / np.maximum(m[..., None], 1)), 0)
            im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha]).astype(np.uint8), 'RGBA')
        elif key in ('alpha', 'green'):
            im = im.convert('RGBA')
        else:
            im = im.convert('RGB')
        im.save(os.path.join(out, f'f{i:04d}.webp'), 'WEBP', quality=82, method=4)
    shutil.rmtree(tmp)
    w, h = Image.open(os.path.join(out, 'f0001.webp')).size
    mp = os.path.join(ROOT, 'assets/vfx/MANIFEST.json')
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    man[name] = {**man.get(name, {}), 'frames': len(frames), 'fps': fps, 'width': w, 'ratio': round(h / w, 4), 'ext': 'webp', 'key': key,
                 'license': lic or man.get(name, {}).get('license', ''), 'source': source or man.get(name, {}).get('source', ''), 'note': note,
                 'added': datetime.date.today().isoformat()}
    json.dump(man, open(mp, 'w'), indent=1, ensure_ascii=False)
    return man[name]


def log_license(name, who, lic, url):
    lp = os.path.join(ROOT, 'docs/LISANSLAR.md')
    t = open(lp).read()
    if f'`{name}`' not in t:
        open(lp, 'a').write(('' if t.endswith('\n') else '\n') + f"- VFX klibi `{name}`: {who}; lisans: {lic}; kaynak: {url}\n")


if __name__ == '__main__':
    src, name = sys.argv[1], sys.argv[2]
    m = ingest(src, name, arg('--key', 'none'), arg('--start', 0.0), arg('--dur', 6.0), arg('--fps', 24), arg('--width', 540), arg('--license', ''), arg('--source', ''), arg('--note', ''))
    if m['license']:
        log_license(name, m['source'] or src, m['license'], m['source'])
    print(name, m['frames'], 'frames', m['key'])
