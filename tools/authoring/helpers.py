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


def bridge(a, b, at, **kw):
    """A suspension bridge drawn on the map at its real coordinates, from shore a to shore b."""
    return _put({'type': 'bridge', 'from': list(a), 'to': list(b)}, at, kw)


def wall(points, at, **kw):
    """A fortified wall drawn along its real line (stone band, crenellations, towers)."""
    return _put({'type': 'wall', 'points': [list(p) for p in points]}, at, kw)


def art(name, lat, lon, at, size=150, **kw):
    """A drawn illustration (assets/art/<name>.png) placed on the map, instead of an emoji."""
    return _put({'type': 'icon', 'icon': 'art:' + name, 'lat': lat, 'lon': lon, 'size': size, 'plain': True}, at, kw)


def ship(points, at, rid, emblem='#c1121f', style='caravel', **kw):
    # style: caravel (1400-1700), longship (Viking), steamer (1850-1950), cargo (modern), sailboat (modern yacht)
    return route(points, at, color='#ffffff', width=5, id=rid, dashed=True, dash=[14, 12], glow=False,
                 mover={'kind': 'ship', 'size': 170, 'emblem': emblem, 'style': style}, **kw)


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


def hook(text, at=0.05, size=110, until=None, screen=(0.5, 0.2), accent='#ffd60a', **kw):
    """Big condensed opening title; *word* = accent colour."""
    d = {'type': 'title', 'text': text, 'hook': True, 'size': size, 'anim': 'slam', 'screen': list(screen), 'accent': accent, 'width': 960}
    if until is not None:
        d['until'] = until
    return _put(d, at, kw)


def bars(items, at, orient='h', **kw):
    """items: [(label, value, display, color, flag)] - display/color/flag optional."""
    its = []
    for it in items:
        it = list(it) + [None] * (5 - len(it))
        d = {'label': it[0], 'value': it[1]}
        if it[2] is not None:
            d['display'] = it[2]
        if it[3]:
            d['color'] = it[3]
        if it[4]:
            d['flag'] = it[4]
        its.append(d)
    return _put({'type': 'bars', 'items': its, 'orient': orient}, at, kw)


def vs(left, right, at, **kw):
    """left/right: (flag_code, label)"""
    return _put({'type': 'vs', 'left': {'flag': left[0], 'label': left[1]}, 'right': {'flag': right[0], 'label': right[1]}}, at, kw)


def timeline(events, **kw):
    """events: [(at, year, label)]"""
    d = {'type': 'timeline', 'events': [{'at': a, 'year': y, 'label': l} for a, y, l in events], 'at': events[0][0]}
    d.update(kw)
    return d


def clock(steps, at=None, **kw):
    """steps: [(at, 'HH:MM')]"""
    d = {'type': 'clock', 'steps': [{'at': a, 'time': tm} for a, tm in steps]}
    return _put(d, at if at is not None else steps[0][0], kw)


def tilt(at, deg=38, **kw):
    return _put({'type': 'tilt', 'deg': deg}, at, kw)


def flow(points, at, color='#5ec8ff', width=12, **kw):
    return route(points, at, color=color, width=width, flow=True, arrowHead=True, **kw)


def box(w, s, e, n):
    return {'box': [w, s, e, n]}


import re as _re

# reaction faces chosen from the sentence itself (reference: a face pops up every 10-15 s)
_REACT = [
    ('art:emote_think', r'\b(why|how|what|which|who)\b.*\?'),
    ('art:emote_laugh', r'\b(mocked|folly|funny|joke|silly|laugh|ridiculous)\b'),
    ('art:emote_cry', r'\b(lost|closed|died|dead|sunk|sank|destroyed|collapsed|abandoned|forced)\b'),
    ('art:emote_angry', r'\b(war|conquered|invaded|invasion|dispute|disputed|fight|fought|seized|attacked|claims?)\b'),
    ('art:emote_shock', r'\b(only|just|more than|million|billion|biggest|largest|longest|highest|deepest|tallest|smallest|entire|whole|every)\b'),
    ('art:emote_cool', r'\b(today|still|now|finally)\b'),
]


def enrich(scenes):
    """Adds cheap, meaningful motion to older scripts: a reaction face every few scenes.
    Skips scenes that already have one, are crowded, or have a character on screen."""
    last = -9
    flip = 0
    for i, sc in enumerate(scenes):
        show = sc.get('show', [])
        if any(e.get('type') == 'react' for e in show):
            last = i
            continue
        if i - last < 3 or len(show) >= 8 or any(e.get('type') in ('character', 'avatar', 'handstamp', 'tally') for e in show):
            continue
        text = sc['text']
        for icon, rx in _REACT:
            m = _re.search(rx, text, _re.I)
            if not m:
                continue
            hit = m.group(1) if m.groups() else m.group(0)
            word = hit.split()[0] if icon != 'art:emote_think' else hit
            word = _re.sub(r"[^\w']", '', word)
            if not word:
                continue
            flip ^= 1
            show.append({'type': 'react', 'icon': icon, 'screen': [0.79, 0.3] if flip else [0.21, 0.3], 'burst': True, 'size': 160, 'at': word})
            sc['show'] = show
            last = i
            break
    return scenes


def save(vid, m, scenes, keywords=None, imagery=None, style='geo', intro=None, styles=None, earth=None, captions=None, config=None):
    for sc in scenes:
        sc['show'] = [e for e in sc.get('show', []) if not (e.get('type') == 'react' and 'emote_shock' in str(e.get('icon')))]
    d = {'id': vid, 'style': style, 'meta': m, 'scenes': scenes}
    cfg = {}
    if keywords or captions:
        cfg['captions'] = dict(captions or {})
        if keywords:
            cfg['captions']['keywords'] = keywords
    if config:
        cfg.update(config)
    if cfg:
        d['config'] = cfg
    if styles:
        d['styles'] = styles
    if earth:
        d['earth'] = earth
    if imagery:
        d['imagery'] = imagery
    if intro:
        d['intro'] = intro
    out = os.path.join(ROOT, 'videos', vid)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'script.json'), 'w') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print('wrote', vid, len(scenes), 'scenes')


# ---------------------------------------------------------------------------------------------
# Reference-toolbox helpers (page/extras.js). Every one returns a `show` item.
# ---------------------------------------------------------------------------------------------
def trace(target, fill, at=None, neon=None, dur=1.4, **kw):
    """Outline drawn around the shape from one point (traceFrom=[lat,lon]), fill follows."""
    d = {'type': 'highlight', 'target': target, 'fill': fill, 'trace': True, 'traceDur': dur}
    if neon:
        d['neon'] = neon
    return _put(d, at, kw)


def giant(text, lat, lon, at, size=110, **kw):
    """A huge extruded name that shrinks onto the map."""
    return lab(text, lat, lon, at, style='extrude', anim='giant', size=size, **kw)


def face(target, expr, at=None, scale=0.5, **kw):
    """The country as a character. expr = [(word_or_sec, 'happy'|'angry'|'worried'|'surprised'|'sad'|'smug'|'talk'), ...]"""
    return _put({'type': 'face', 'target': target, 'expr': [{'at': a, 'e': e} for a, e in expr], 'scale': scale}, at, kw)


def pathtext(text, points, at, size=60, **kw):
    return _put({'type': 'pathtext', 'text': text, 'points': [list(p) for p in points], 'size': size}, at, kw)


def crowd(lat, lon, at, count=24, **kw):
    return _put({'type': 'crowd', 'lat': lat, 'lon': lon, 'count': count}, at, kw)


def pin(lat, lon, icon, at, **kw):
    return _put({'type': 'pin', 'lat': lat, 'lon': lon, 'icon': icon}, at, kw)


def area(a, b, at, **kw):
    """Traced rectangle (buildings, a park) between two corners (lat, lon)."""
    return _put({'type': 'box', 'from': list(a), 'to': list(b)}, at, kw)


def beam(lat, lon, at, **kw):
    return _put({'type': 'beam', 'lat': lat, 'lon': lon}, at, kw)


def cloud(lat, lon, at, **kw):
    return _put({'type': 'cloud', 'lat': lat, 'lon': lon}, at, kw)


def particles(kind, at=None, **kw):
    return _put({'type': 'particles', 'kind': kind}, at, kw)


def flare(screen, at, **kw):
    return _put({'type': 'flare', 'screen': list(screen)}, at, kw)


def lens(at, screen=(0.5, 0.4), r=330, **kw):
    return _put({'type': 'lens', 'screen': list(screen), 'r': r}, at, kw)


def photo(image, at, kind='full', **kw):
    return _put({'type': 'photo', 'image': image, 'kind': kind}, at, kw)


def avatar(image, screen, at, name=None, **kw):
    d = {'type': 'avatar', 'image': image, 'screen': list(screen)}
    if name:
        d['name'] = name
    return _put(d, at, kw)


def link(a, b, at, **kw):
    return _put({'type': 'link', 'from': list(a), 'to': list(b)}, at, kw)


def react(icon, screen, at, **kw):
    return _put({'type': 'react', 'icon': icon, 'screen': list(screen), 'burst': True}, at, kw)


def timebar(a, b, label, at, **kw):
    return _put({'type': 'timebar', 'from': str(a), 'to': str(b), 'label': label}, at, kw)


def orbit(items, text, at, **kw):
    return _put({'type': 'orbit', 'items': list(items), 'text': text}, at, kw)


def handstamp(text, at, **kw):
    return _put({'type': 'handstamp', 'text': text}, at, kw)


def grade(mode, at, **kw):
    return _put({'type': 'grade', 'mode': mode}, at, kw)


def rider_ship(points, at, rid, rider, to, style='caravel', **kw):
    """A ship that carries a character; on arrival the character jumps to `to` (lat, lon)."""
    rs = kw.pop('rider_size', 120)
    d = ship(points, at, rid, style=style, **kw)
    d['rider'] = {'image': rider, 'size': rs, 'to': {'lat': to[0], 'lon': to[1]}}
    return d


def walker(points, at, image, rid=None, size=170, **kw):
    """A character cut-out walking along a route (hops, flips toward its direction)."""
    d = route(points, at, color='#ffffff', width=5, dashed=True, dash=[14, 12], glow=False, mover={'kind': 'character', 'image': image, 'size': size}, **kw)
    if rid:
        d['id'] = rid
    return d


def callout(text, lat, lon, at, dx=130, dy=-180, **kw):
    """Yellow hand-lettered label on a curved leader line pointing at (lat, lon). Use \n for a smaller second line."""
    return _put({'type': 'callout', 'text': text, 'lat': lat, 'lon': lon, 'dx': dx, 'dy': dy}, at, kw)


def ellipse(lat, lon, at, rx=200, ry=140, **kw):
    """Hand-drawn yellow ellipse drawn around an area."""
    return _put({'type': 'ellipse', 'lat': lat, 'lon': lon, 'rx': rx, 'ry': ry}, at, kw)


def glow(lat, lon, at, km=None, r=None, color='#ff3b1f', **kw):
    """Soft pulsing heat / energy blob (heat maps, spreading warm water, fires)."""
    d = {'type': 'glow', 'lat': lat, 'lon': lon, 'color': color}
    if km: d['km'] = km
    if r: d['r'] = r
    return _put(d, at, kw)


def crack(at, y=0.45, **kw):
    """A black jagged crack opens across the screen (splits, civil wars, rifts)."""
    return _put({'type': 'crack', 'y': y}, at, kw)


def disc(lat, lon, at, km=None, r=None, color='#5ec8ff', **kw):
    """Translucent filled circle with a glowing rim (range circles, signal spheres, zones)."""
    d = {'type': 'disc', 'lat': lat, 'lon': lon, 'color': color}
    if km: d['km'] = km
    if r: d['r'] = r
    return _put(d, at, kw)


def tally(items, at, **kw):
    """Stack of rows that count up: items = [(art_name, label, value[, prefix, suffix])]."""
    rows = []
    for it in items:
        d = {'icon': it[0], 'label': it[1], 'value': it[2]}
        if len(it) > 3: d['prefix'] = it[3]
        if len(it) > 4: d['suffix'] = it[4]
        rows.append(d)
    return _put({'type': 'tally', 'items': rows}, at, kw)
