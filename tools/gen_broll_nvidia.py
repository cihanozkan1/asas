#!/usr/bin/env python3
"""Generic B-roll pictures (landscapes, streets, interiors) drawn with NVIDIA-hosted FLUX, vertical 9:16.
Used as full-screen slow-pan scenes or as 'photo' cards. These are AI illustrations, never claimed to be a
real photo of a real place: prompts describe the kind of place (rainforest, salt flat, harbour), no real
people, brands, landmarks or text.

  NVIDIA_API_KEY=... python3 tools/gen_broll_nvidia.py <name> "<what to draw>" [--seed N]

Writes assets/broll/<name>.jpg (1080x1920) and assets/broll/prompts/<name>.json.
"""
import argparse, base64, json, os, sys, time, urllib.request, io
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'broll')
STYLE = ('{desc}. Cinematic vertical photograph, natural light, rich detail, shallow haze, high dynamic range, '
         'no people, no text, no logo, no watermark, no signs')


def generate(prompt, seed, key):
    for model in ['black-forest-labs/flux.1-dev']:
        body = {'prompt': prompt, 'width': 768, 'height': 1344, 'seed': seed, 'steps': 30, 'cfg_scale': 3.5, 'mode': 'base'}
        req = urllib.request.Request(f'https://ai.api.nvidia.com/v1/genai/{model}', data=json.dumps(body).encode(),
                                     headers={'Authorization': f'Bearer {key}', 'Accept': 'application/json', 'Content-Type': 'application/json'})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=240) as r:
                    art = json.load(r)['artifacts'][0]
                if art.get('finishReason') not in (None, 'SUCCESS'):
                    raise RuntimeError(art.get('finishReason'))
                return base64.b64decode(art['base64'])
            except Exception as e:
                print(f'  try {attempt + 1}: {e}', file=sys.stderr)
                time.sleep(6 * (attempt + 1))
    raise SystemExit('image generation failed')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('name'); ap.add_argument('desc'); ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    key = os.environ.get('NVIDIA_API_KEY') or sys.exit('NVIDIA_API_KEY is not set')
    os.makedirs(os.path.join(OUT, 'prompts'), exist_ok=True)
    dst = os.path.join(OUT, a.name + '.jpg')
    if not os.path.exists(dst):
        data = generate(STYLE.format(desc=a.desc), a.seed, key)
        im = Image.open(io.BytesIO(data)).convert('RGB').resize((1080, 1920), Image.LANCZOS)
        im.save(dst, quality=88)
        json.dump({'desc': a.desc, 'seed': a.seed, 'model': 'black-forest-labs/flux.1-dev (NVIDIA)'}, open(os.path.join(OUT, 'prompts', a.name + '.json'), 'w'), indent=1)
    print('ok', a.name)
