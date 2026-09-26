"""Small helpers for writing videos/<id>/script.json files from Python.

Each topic module builds a dict with meta + scenes and calls save(). Keeping
scripts as data (JSON) means the render pipeline never depends on this code.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIKI = 'https://en.wikipedia.org/wiki/'


def src(claim, url, quote=None):
    if not url.startswith('http'):
        url = WIKI + url
    d = {'claim': claim, 'url': url}
    if quote:
        d['quote'] = quote
    return d


def S(text, show=(), cam=None, era='now', src=(), style=None, tr=None, no_claim=False, **kw):
    s = {'era': era, 'text': text, 'show': list(show)}
    if cam is not None:
        s['camera'] = cam
    if style:
        s['style'] = style
    if tr:
        s['transition'] = tr
    if src:
        s['sources'] = list(src)
    if no_claim:
        s['noClaim'] = True
    s.update(kw)
    return s


def _put(d, at, kw):
    if at is not None:
        d['at'] = at
    d.update(kw)
    return d


def hl(target, fill=None, at=None, **kw):
    d = {'type': 'highlight', 'target': target}
    if fill:
        d['fill'] = fill
    return _put(d, at, kw)


def blob(target, fill, rim, at=None, **kw):
    return hl(target, fill, at, soft=True, rim=rim, **kw)


def lab(text, lat=None, lon=None, at=None, **kw):
    d = {'type': 'label', 'text': text}
    if lat is not None:
        d.update(lat=lat, lon=lon)
    return _put(d, at, kw)


def slam(text, lat, lon, at, size=96, **kw):
    return lab(text, lat, lon, at, style='map', anim='slam', size=size, **kw)


def pill(text, at, bg='#e63946', screen=(0.5, 0.23), size=46, **kw):
    return lab(text, at=at, style='pill', bg=bg, screen=list(screen), size=size, **kw)


def note(text, lat, lon, at, size=62, rotate=-7, **kw):
    return lab(text, lat, lon, at, style='note', typewriter=True, size=size, rotate=rotate, **kw)


def dot(text, lat, lon, at, dy=-48, size=44, **kw):
    return lab(text, lat, lon, at, dot=True, dy=dy, size=size, **kw)


def cnt(value, at, size=180, color=None, **kw):
    d = {'type': 'counter', 'steps': [{'at': at, 'value': value}], 'size': size}
    if color:
        d['color'] = color
    d.update(kw)
    return d


def cnt_steps(steps, size=180, **kw):
    d = {'type': 'counter', 'steps': [{'at': a, 'value': v} for a, v in steps], 'size': size}
    d.update(kw)
    return d


def ping(lat, lon, at=None, color='#ff3b3b', **kw):
    return _put({'type': 'ping', 'lat': lat, 'lon': lon, 'color': color}, at, kw)


def meas(a, b, label, at, **kw):
    return _put({'type': 'measure', 'from': list(a), 'to': list(b), 'label': label}, at, kw)


def route(points, at, color='#ffd60a', width=9, **kw):
    return _put({'type': 'route', 'points': [list(p) for p in points], 'color': color, 'width': width}, at, kw)


def ship(points, at, rid, emblem='#c1121f', **kw):
    return route(points, at, color='#ffffff', width=5, id=rid, dashed=True, dash=[14, 12], glow=False,
                 mover={'kind': 'ship', 'size': 170, 'emblem': emblem}, **kw)


def mover_icon(points, at, icon, rid=None, size=110, color='#ffffff', **kw):
    d = route(points, at, color=color, width=5, dashed=True, dash=[14, 12], glow=False,
              mover={'kind': 'icon', 'icon': icon, 'size': size}, **kw)
    if rid:
        d['id'] = rid
    return d


def plane(points, at, rid=None, **kw):
    d = route(points, at, color='#ffffff', width=4, dashed=True, dash=[10, 12], glow=False,
              mover={'kind': 'plane', 'size': 120}, **kw)
    if rid:
        d['id'] = rid
    return d


def char(image, at, screen=(0.25, 0.6), **kw):
    return _put({'type': 'character', 'image': image, 'screen': list(screen)}, at, kw)


def icon(emoji, lat, lon, at, size=110, **kw):
    return _put({'type': 'icon', 'icon': emoji, 'lat': lat, 'lon': lon, 'size': size}, at, kw)


def year(v, at, light=False, **kw):
    d = {'type': 'year', 'value': str(v)}
    if light:
        d['light'] = True
    return _put(d, at, kw)


def q(lat, lon, at):
    return {'type': 'question', 'lat': lat, 'lon': lon, 'at': at}


def ghost(target, to, at, fill='#4cc9f0', **kw):
    return _put({'type': 'ghost', 'target': target, 'to': {'lat': to[0], 'lon': to[1]}, 'fill': fill}, at, kw)


def stamp(text, at, size=80, **kw):
    return _put({'type': 'stamp', 'text': text, 'size': size, 'screen': [0.5, 0.33]}, at, kw)


def flag(code, lat, lon, at, size=130, **kw):
    return _put({'type': 'flag', 'code': code, 'lat': lat, 'lon': lon, 'size': size}, at, kw)


def scatter(target, emoji, at, count=12, size=64, **kw):
    return _put({'type': 'scatter', 'target': target, 'icon': emoji, 'count': count, 'size': size}, at, kw)


def ring(lat, lon, at, r=60, **kw):
    return _put({'type': 'ring', 'lat': lat, 'lon': lon, 'r': r}, at, kw)


def arrow(a, b, at, color='#ffffff', **kw):
    return _put({'type': 'arrow', 'from': list(a), 'to': list(b), 'color': color}, at, kw)


def shake(at):
    return {'type': 'shake', 'at': at}


def punch(at):
    return {'type': 'punch', 'at': at}


def fit(*targets, **kw):
    d = {'fit': list(targets)}
    d.update(kw)
    return d


def at_(lat, lon, zoom, **kw):
    d = {'lat': lat, 'lon': lon, 'zoom': zoom}
    d.update(kw)
    return d


def meta(title, description, pinned, tags):
    return {'title': title, 'description': description, 'pinnedComment': pinned, 'tags': tags}


def save(vid, m, scenes, keywords=None, imagery=None, style='geo', intro=None):
    d = {'id': vid, 'style': style, 'meta': m, 'scenes': scenes}
    if keywords:
        d['config'] = {'captions': {'keywords': keywords}}
    if imagery:
        d['imagery'] = imagery
    if intro:
        d['intro'] = intro
    out = os.path.join(ROOT, 'videos', vid)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'script.json'), 'w') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print('wrote', vid, len(scenes), 'scenes')
