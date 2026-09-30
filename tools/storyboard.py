#!/usr/bin/env python3
"""videos/<id>/script.json -> videos/<id>/storyboard.md (kurgu-editoru skill table).
usage: python3 tools/storyboard.py <id> [<id> ...]   (timeline.geo.json, if present, gives the times)"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX = {'flash': 'flash + whoosh', 'film': 'film strip + page turn', 'blast': 'thud + rumble', 'ice': 'crack', 'rewind': 'rewind whirr', 'ink': 'ink drop'}
ICON = {'highlight': 'fill', 'label': 'label', 'counter': 'counter', 'route': 'route', 'ping': 'ping', 'flag': 'flag', 'character': 'character', 'art': 'art', 'box': 'box',
        'pathtext': 'curved text', 'crowd': 'crowd', 'react': 'reaction', 'handstamp': 'hand stamp', 'timebar': 'time bar', 'photo': 'photo card', 'lens': 'lens', 'grade': 'colour grade',
        'particles': 'particles', 'bridge': 'bridge', 'wall': 'wall', 'question': '?', 'pill': 'pill', 'year': 'year', 'face': 'face', 'pin': 'pin'}


def cam(c):
    if not c:
        return 'hold'
    if c.get('follow'):
        return f"follow {c['follow']} z{c.get('zoom')}→{c.get('zoomTo', '')}"
    if c.get('fit'):
        return 'fit ' + ','.join(str(x)[:12] for x in c['fit'])
    then = f" → {len(c['then'])} more move(s)" if c.get('then') else ''
    return f"z{c.get('zoom')} @({c.get('lat')},{c.get('lon')}){then}"


def main(ids):
    for i in ids:
        d = os.path.join(ROOT, 'videos', i)
        s = json.load(open(os.path.join(d, 'script.json')))
        t0 = {}
        tp = os.path.join(ROOT, 'output', i, 'timeline.geo.json')
        if os.path.exists(tp):
            tl = json.load(open(tp))
            for k, sc in enumerate(tl.get('scenes', [])):
                t0[k] = (sc.get('start'), sc.get('end'))
        rows = ['| # | sec | narration | camera | look | visuals | transition | SFX |', '|---|---|---|---|---|---|---|---|']
        for k, sc in enumerate(s['scenes']):
            a, b = t0.get(k, (None, None))
            sec = f'{a:.1f}–{b:.1f}' if a is not None and b is not None else ''
            vis = {}
            for e in sc.get('show', []):
                n = ICON.get(e.get('type'), e.get('type'))
                vis[n] = vis.get(n, 0) + 1
            v = ', '.join(f'{n}×{c}' if c > 1 else n for n, c in vis.items())
            look = sc.get('style') or ('parchment' if sc.get('era') == 'history' else 'satellite')
            tr = sc.get('transition') or ''
            rows.append(f"| {k + 1} | {sec} | {sc['text']} | {cam(sc.get('camera'))} | {look} | {v} | {tr} | {SFX.get(tr, 'pop / swoosh')} |")
        m = s.get('meta', {})
        out = [f"# Storyboard — {i}", '', f"**{m.get('title', '')}**", '', *rows, '',
               '## Retention notes', '- Hook (0–10 s): subject visible from frame 0, question asked by ~10 s.',
               '- New visual event about every 1–1.5 s; camera never holds (drift + per-scene moves).',
               '- Humor / surprise beat every 10–15 s (reaction faces, scale gags, stamps).',
               '- Ends on a punchline fact; the last frame returns to the opening view (loop). No CTA.',
               '- All media is our own render or generated art (docs/LISANSLAR.md).', '']
        open(os.path.join(d, 'storyboard.md'), 'w').write('\n'.join(out))
        print('wrote', i)


if __name__ == '__main__':
    main(sys.argv[1:])
