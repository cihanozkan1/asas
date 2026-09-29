#!/usr/bin/env python3
"""Map illustrations (landmarks, buildings, vehicles, props) drawn with NVIDIA-hosted FLUX, cut out
and saved as assets/art/<name>.png. Scripts use them as icons with "art:<name>".

  NVIDIA_API_KEY=... python3 tools/gen_art_nvidia.py <name> "<what to draw>" [--seeds 1,2] [--pick N]

Without --pick the raw candidates are written to cache/art/<name>_<seed>.png for review;
with --pick N the chosen one is cut out into assets/art/<name>.png.
Vehicles must be drawn in side view facing RIGHT: the renderer mirrors them to the travel direction.
"""
import argparse, base64, json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'cache', 'art')
OUT = os.path.join(ROOT, 'assets', 'art')
MODELS = ['black-forest-labs/flux.1-dev', 'black-forest-labs/flux.2-klein-4b']
STYLE = ('flat 2D vector illustration for an educational geography YouTube channel: {desc}. '
         'A single object, centered, clean bold dark outline, flat colours with soft cel shading, '
         'isolated on a plain solid light grey background, no text, no letters, no logo, no frame, no ground shadow')


def generate(prompt, seed, key):
    for model in MODELS:
        body = {'prompt': prompt, 'width': 1024, 'height': 1024, 'seed': seed, 'steps': 30, 'cfg_scale': 3.5, 'mode': 'base'}
        if 'klein' in model:
            body = {'prompt': prompt, 'width': 1024, 'height': 1024, 'seed': seed, 'steps': 4}
        req = urllib.request.Request(f'https://ai.api.nvidia.com/v1/genai/{model}', data=json.dumps(body).encode(),
                                     headers={'Authorization': f'Bearer {key}', 'Accept': 'application/json', 'Content-Type': 'application/json'})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=240) as r:
                    art = json.load(r)['artifacts'][0]
                if art.get('finishReason') not in (None, 'SUCCESS'):
                    raise RuntimeError(art.get('finishReason'))
                return base64.b64decode(art['base64'])
            except Exception as e:
                print(f'  {model} try {attempt + 1}: {e}', file=sys.stderr)
                time.sleep(5 * (attempt + 1))
    raise SystemExit('image generation failed')


def cutout(src, dst, max_side=420):
    import numpy as np
    from PIL import Image
    from rembg import remove, new_session
    from scipy import ndimage
    img = Image.open(src).convert('RGB')
    cut = remove(img, session=new_session('isnet-general-use'))
    arr = np.array(cut)
    a = arr[..., 3] > 40
    lab, n = ndimage.label(a)
    if n > 1:  # keep the object (and parts close in size), drop specks
        sizes = ndimage.sum(a, lab, range(1, n + 1))
        keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= sizes.max() * 0.08])
        arr[..., 3] = np.where(keep, arr[..., 3], 0)
        # the flat grey ground-shadow ellipse FLUX likes to add under objects: drop it
        a = arr[..., 3] > 40
        lab, n = ndimage.label(a)
        H, W = a.shape
        for i, s in enumerate(ndimage.find_objects(lab), 1):
            h, w = s[0].stop - s[0].start, s[1].stop - s[1].start
            if n > 1 and h < 0.22 * w and w > 0.2 * W and s[0].start > 0.55 * H:
                arr[..., 3] = np.where(lab == i, 0, arr[..., 3])
    cut = Image.fromarray(arr)
    cut = cut.crop(cut.getbbox())
    cut.thumbnail((max_side, max_side), Image.LANCZOS)
    cut.save(dst, optimize=True)
    return cut.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name'); ap.add_argument('desc')
    ap.add_argument('--seeds', default='1,2'); ap.add_argument('--pick', type=int)
    a = ap.parse_args()
    os.makedirs(RAW, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    if a.pick:
        size = cutout(os.path.join(RAW, f'{a.name}_{a.pick}.png'), os.path.join(OUT, a.name + '.png'))
        os.makedirs(os.path.join(OUT, 'prompts'), exist_ok=True)
        json.dump({'desc': a.desc, 'seed': a.pick, 'model': 'black-forest-labs/flux.1-dev (NVIDIA)'},
                  open(os.path.join(OUT, 'prompts', a.name + '.json'), 'w'), indent=1)
        print('saved', a.name, size)
        return
    key = os.environ.get('NVIDIA_API_KEY') or sys.exit('NVIDIA_API_KEY is not set')
    for s in [int(x) for x in a.seeds.split(',')]:
        f = os.path.join(RAW, f'{a.name}_{s}.png')
        if not os.path.exists(f):
            data = generate(STYLE.format(desc=a.desc), s, key)  # nothing is written on failure
            open(f, 'wb').write(data)
        print('ok', a.name, s)


if __name__ == '__main__':
    main()
