#!/usr/bin/env python3
"""Generate a 3D clay/chibi character with the free Pollinations.ai image API,
remove the background with rembg and save a tight transparent PNG.

  python3 tools/gen_character.py <id> "<description>" [--seed N] [--force]

Output: assets/characters/<id>.png  (prompt log: assets/characters/prompts.json)
"""
import json, sys, time, urllib.parse, urllib.request, io, os, argparse
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'characters')
# v2: flat 2D cartoon (mobile strategy game style) like the reference channels, not clay toys
STYLE = ('cute chibi cartoon mascot sticker of {desc}, standing upright, full body from head to feet, very big head and tiny body, '
         'flat vector art, thick clean dark outline, simple cel shading, bright colors, cartoon game icon style, '
         'facing viewer, centered, isolated on plain white background, no text, no ground, no shadow')

def generate(desc, seed, size=1024):
    prompt = STYLE.format(desc=desc)
    url = ('https://image.pollinations.ai/prompt/' + urllib.parse.quote(prompt) +
           f'?width={size}&height={size}&nologo=true&seed={seed}&model=flux')
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                data = r.read()
            return Image.open(io.BytesIO(data)).convert('RGB'), prompt
        except Exception as e:  # rate limits / timeouts: back off and retry
            print('  retry', attempt + 1, e)
            time.sleep(8 * (attempt + 1))
    raise SystemExit('image generation failed')

def scrub_watermark(img):
    # the free API stamps a small logo in the bottom-right corner: paint it over with
    # the surrounding background colour before cutting the figure out
    from PIL import ImageDraw
    w, h = img.size
    box = (int(w * 0.70), int(h * 0.93), w, h)
    ref = img.crop((int(w * 0.70), int(h * 0.86), w, int(h * 0.90))).resize((1, 1)).getpixel((0, 0))
    img = img.copy()
    ImageDraw.Draw(img).rectangle(box, fill=ref)
    return img

def cutout(img):
    from rembg import remove, new_session
    img = scrub_watermark(img)
    out = remove(img, session=new_session('isnet-general-use'))
    alpha = out.split()[-1].point(lambda a: 255 if a > 40 else 0)
    box = alpha.getbbox()
    out = out.crop(box)
    pad = 12
    canvas = Image.new('RGBA', (out.width + pad * 2, out.height + pad * 2), (0, 0, 0, 0))
    canvas.paste(out, (pad, pad), out)
    return canvas

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('id'); ap.add_argument('desc')
    ap.add_argument('--seed', type=int, default=11); ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, a.id + '.png')
    if os.path.exists(path) and not a.force:
        print('exists', path); return
    img, prompt = generate(a.desc, a.seed)
    cut = cutout(img)
    from strip_pedestal import pedestal_row
    base = pedestal_row(cut)
    if base:  # the model often adds a display stand under the feet
        cut = cut.crop((0, 0, cut.width, base))
        cut = cut.crop(cut.getbbox())
    # keep file sizes sane: max 700px tall
    if cut.height > 700:
        cut = cut.resize((round(cut.width * 700 / cut.height), 700), Image.LANCZOS)
    cut.save(path, optimize=True)
    # one small file per character, so parallel runs never clobber a shared log
    os.makedirs(os.path.join(OUT, 'prompts'), exist_ok=True)
    json.dump({'prompt': prompt, 'seed': a.seed, 'source': 'pollinations.ai (flux)'}, open(os.path.join(OUT, 'prompts', a.id + '.json'), 'w'), indent=2)
    print('saved', path, cut.size)

if __name__ == '__main__':
    main()
