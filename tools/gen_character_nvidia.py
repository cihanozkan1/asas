#!/usr/bin/env python3
"""Generate flat 2D cartoon characters with NVIDIA-hosted FLUX (build.nvidia.com).

  NVIDIA_API_KEY=... python3 tools/gen_character_nvidia.py <id> "<description>" [--seeds 1,2,3] [--out DIR]

Writes <out>/<id>_<seed>.png (raw, white background). Pick the best one and cut it out with
tools/gen_character.py-style background removal (see finalize step in the README).
"""
import argparse, base64, json, os, sys, time, urllib.request

MODELS = ['black-forest-labs/flux.1-dev', 'black-forest-labs/flux.2-klein-4b']
STYLE = ('flat 2D vector cartoon character in the style of a polished educational geography YouTube channel: {desc}. '
         'Exactly one character, full body from the top of the head to the shoes, standing upright facing the viewer, '
         'arms relaxed, holding nothing unless stated, friendly chibi proportions with a slightly large head, clean bold dark outline, '
         'flat colours with soft cel shading, isolated on a plain pure white background, no text, no logo, no frame, no ground shadow, '
         'no other people, no extra objects')


def generate(prompt, seed, key, size=(768, 1344)):
    for model in MODELS:
        body = {'prompt': prompt, 'width': size[0], 'height': size[1], 'seed': seed, 'steps': 30, 'cfg_scale': 3.5, 'mode': 'base'}
        if 'klein' in model:  # the small model takes fewer options
            body = {'prompt': prompt, 'width': 768, 'height': 1344, 'seed': seed, 'steps': 4}
        req = urllib.request.Request(f'https://ai.api.nvidia.com/v1/genai/{model}', data=json.dumps(body).encode(),
                                     headers={'Authorization': f'Bearer {key}', 'Accept': 'application/json', 'Content-Type': 'application/json'})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=240) as r:
                    j = json.load(r)
                art = (j.get('artifacts') or [{}])[0]
                if art.get('finishReason') not in (None, 'SUCCESS'):
                    raise RuntimeError(art.get('finishReason'))
                return base64.b64decode(art['base64']), model
            except Exception as e:  # rate limits / timeouts: back off, then try the next model
                print(f'  {model} try {attempt + 1}: {e}', file=sys.stderr)
                time.sleep(6 * (attempt + 1))
    raise SystemExit('image generation failed')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('id'); ap.add_argument('desc')
    ap.add_argument('--seeds', default='1,2,3'); ap.add_argument('--out', default='gen_nv')
    a = ap.parse_args()
    key = os.environ.get('NVIDIA_API_KEY')
    if not key:
        raise SystemExit('NVIDIA_API_KEY is not set')
    os.makedirs(a.out, exist_ok=True)
    for s in [int(x) for x in a.seeds.split(',')]:
        f = os.path.join(a.out, f'{a.id}_{s}.png')
        if os.path.exists(f):
            continue
        png, model = generate(STYLE.format(desc=a.desc), s, key)
        open(f, 'wb').write(png)
        print('ok', a.id, s, model)


if __name__ == '__main__':
    main()
