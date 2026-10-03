#!/usr/bin/env python3
"""Shot-aware, motion-aware, narration-aware and sound-aware study of ONE reference short (ideas and techniques only).

  python3 tools/ref/study.py reference/x.mp4 [--out /tmp/ref_study] [--no-speech]

Why this replaces the fixed-fps contact sheet: a time grid shows arbitrary moments (often mid-transition, before the graphics are in).
This tool cuts the video into SHOTS first and then looks at what matters inside each shot:

  shots     hard cuts (PySceneDetect) + soft transitions (flash/dissolve/wipe found from the frame-difference profile)
  camera    per shot: static / zoom in / zoom out / pan / rotate / mixed, with speed (ORB + RANSAC similarity transform, as deep.py)
  events    every "new thing on screen" (motion-compensated frame difference) with a TYPE guessed from the changed region:
            caption/title text, region fill (flag, colour), outline or line, icon/sprite, light/flash, full-screen change;
            plus where it is (top / middle / caption band / bottom), its size and colour, and the word being spoken
  base      per shot map style: satellite relief, flat light, parchment, dark, globe/space, b-roll (text/paper heavy)
  speech    faster-whisper words with times (hook text, first question, loop line)
  sound     music present?, onsets that are NOT speech (sound effects) and how they line up with the visual events
  sheets    keyframes chosen per shot: one when the graphics have settled (80 % of the shot) and, for shots longer than 2.8 s,
            one right after the entry (25 %); each cell is labelled with shot number, time, camera class and event types.
            Cells are 312x555 and a sheet has 5x3 of them, so nothing is downscaled when the image is read.

Outputs  <out>/<name>.json  (numbers only)   <out>/<name>_<k>.jpg  (sheets, to be read by a person/model)   <out>/<name>.md (auto summary)
Nothing of the reference is kept in the project: sheets and JSON live in <out> (default /tmp/ref_study).
"""
import sys, os, json, subprocess, math, shutil
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deep

FF = os.environ.get('FFMPEG_PATH', 'ffmpeg')
W, H = 270, 480           # analysis size
CW, CH = 312, 555         # sheet cell size
FPS = deep.FPS


def read_frames(path, fps=FPS):
    p = subprocess.Popen([FF, '-v', 'error', '-i', path, '-vf', f'fps={fps},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    n = W * H * 3
    out = []
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        out.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    return out


def grab(path, t, w=CW, h=CH):
    r = subprocess.run([FF, '-v', 'error', '-ss', f'{max(t, 0):.3f}', '-i', path, '-frames:v', '1', '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True)
    if len(r.stdout) < w * h * 3:
        return np.zeros((h, w, 3), np.uint8)
    return np.frombuffer(r.stdout, np.uint8).reshape(h, w, 3).copy()


# ---------------------------------------------------------------- shots
def detect_shots(path, dur):
    from scenedetect import detect, ContentDetector
    sc = detect(path, ContentDetector(threshold=19.0, min_scene_len=5))
    cuts = [s[0].seconds for s in sc][1:]
    shots, t0 = [], 0.0
    for c in cuts:
        shots.append([round(t0, 2), round(c, 2)])
        t0 = c
    shots.append([round(t0, 2), round(dur, 2)])
    return [s for s in shots if s[1] - s[0] > 0.2]


def soft_transitions(frames):
    """flash / dissolve / wipe: brightness or global colour moves a lot over 2-4 frames without a hard cut"""
    lum = np.array([f.mean() for f in frames])
    out = []
    for i in range(2, len(lum) - 2):
        d = abs(lum[i + 1] - lum[i - 1])
        if d > 38 and not (abs(lum[i] - lum[i - 1]) > 55 and abs(lum[i + 1] - lum[i]) > 55):
            if not out or i / FPS - out[-1] > 0.8:
                out.append(i / FPS)
    return [round(x, 2) for x in out]


# ---------------------------------------------------------------- base style
def base_style(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    hh, ss, vv = hsv[..., 0].astype(float), hsv[..., 1].astype(float), hsv[..., 2].astype(float)
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    tex = float(cv2.Laplacian(cv2.resize(g, (135, 240)), cv2.CV_32F).var())
    h0, w0 = vv.shape
    corners = np.mean([vv[:h0 // 6, :w0 // 6].mean(), vv[:h0 // 6, -w0 // 6:].mean(), vv[-h0 // 6:, :w0 // 6].mean(), vv[-h0 // 6:, -w0 // 6:].mean()])
    center = vv[h0 // 3:2 * h0 // 3, w0 // 3:2 * w0 // 3].mean()
    paper = ((hh > 8) & (hh < 28) & (ss > 40) & (ss < 150) & (vv > 120)).mean()
    blue = ((hh > 85) & (hh < 112) & (ss > 80)).mean()
    mv, ms = vv.mean(), ss.mean()
    if corners < 45 and center > 70 and mv < 110:
        return 'globe/space'
    if mv < 70:
        return 'dark'
    if paper > 0.45 and tex < 60:
        return 'parchment'
    if tex < 25 and mv > 170:
        return 'flat_light'
    if tex < 25:
        return 'flat_color'
    if blue + paper < 0.12 and tex > 150:
        return 'b-roll/paper/text'
    return 'satellite'


# ---------------------------------------------------------------- events with region type
# A map video moves its camera all the time (tilt, perspective), so a global frame difference is always "busy". What a viewer notices
# as an EVENT is an overlay layer changing: outlines, text, flags, icons, effects are drawn in colours the map itself almost never has
# (pure white, yellow, red, magenta, neon cyan, flag colours). The overlay mask of every frame is compared with the previous one
# (previous mask grown by 9 px so a moving overlay is not a new overlay): what is new = appears, what is gone = disappears.
def overlay_mask(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0].astype(np.int16), hsv[..., 1].astype(np.int16), hsv[..., 2].astype(np.int16)
    white = (v > 232) & (s < 28)
    yellow = (h > 20) & (h < 35) & (s > 140) & (v > 190)
    red = ((h < 7) | (h > 172)) & (s > 150) & (v > 150)
    magenta = (h > 135) & (h < 172) & (s > 110) & (v > 130)
    neon = (h > 78) & (h < 96) & (s > 150) & (v > 215)
    flagblue = (h > 100) & (h < 125) & (s > 170) & (v > 100) & (v < 200)
    m = (white | yellow | red | magenta | neon | flagblue).astype(np.uint8)
    m[int(H * 0.585):int(H * 0.77)] = 0       # the caption band
    m[int(H * 0.86):] = 0
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))


def colour_name(bgr):
    h, s, v = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0, 0]
    if v < 60:
        return 'black'
    if s < 45:
        return 'white' if v > 170 else 'grey'
    hue = int(h) * 2
    if hue < 15 or hue >= 345:
        return 'red'
    if hue < 45:
        return 'orange/brown' if v < 200 else 'orange'
    if hue < 70:
        return 'yellow'
    if hue < 165:
        return 'green'
    if hue < 200:
        return 'cyan/teal'
    if hue < 260:
        return 'blue'
    return 'purple/pink'


def comp_type(frame, lab, k, st, appear):
    x, y, w, h, a = [int(z) for z in st[k, :5]]
    fill = a / max(w * h, 1)
    cy = (y + h / 2) / H
    pos = 'top' if cy < 0.28 else 'upper' if cy < 0.45 else 'middle' if cy < 0.6 else 'caption band' if cy < 0.77 else 'bottom'
    px = frame[lab == k]
    col = colour_name(px.mean(axis=0)) if len(px) else '?'
    frac = a / (W * H)
    thin = min(w, h) / H < 0.03
    if thin and max(w, h) / H > 0.10 and fill < 0.55:
        typ = 'line/route/outline'
    elif fill < 0.25 and frac > 0.003:
        typ = 'outline/glow shape'
    elif w > h * 2.0 and h / H < 0.12 and col in ('white', 'yellow', 'red'):
        typ = 'text (title/label/counter)'
    elif frac > 0.03:
        typ = 'region fill / big graphic'
    elif frac > 0.002:
        typ = 'icon/sprite/label'
    else:
        typ = 'tiny detail'
    return {'type': typ + (' appears' if appear else ' leaves'), 'pos': pos, 'size': round(float(frac), 3), 'colour': col}


def overlay_events(frames):
    masks = [overlay_mask(f) for f in frames]
    ker = np.ones((9, 9), np.uint8)
    events = []
    for i in range(1, len(frames)):
        prev, cur = masks[i - 1], masks[i]
        for appear in (True, False):
            new = (cur & (1 - cv2.dilate(prev, ker))) if appear else (prev & (1 - cv2.dilate(cur, ker)))
            new = cv2.morphologyEx(new, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            if new.mean() > 0.40:
                continue
            n, lab, st, _ = cv2.connectedComponentsWithStats(new)
            comps = sorted([(st[k, cv2.CC_STAT_AREA], k) for k in range(1, n) if st[k, cv2.CC_STAT_AREA] >= 0.0025 * W * H], reverse=True)[:2]
            for a_, k in comps:
                e = comp_type(frames[i if appear else i - 1], lab, k, st, appear)
                e['t'] = round(i / FPS, 2)
                events.append(e)
    events.sort(key=lambda e: e['t'])
    # merge the same kind within 0.5 s
    out = []
    for e in events:
        if out and e['t'] - out[-1]['t'] < 0.5 and e['type'] == out[-1]['type'] and e['pos'] == out[-1]['pos']:
            continue
        out.append(e)
    return out


# ---------------------------------------------------------------- audio
def audio_study(path, words):
    wav = f'/tmp/_study_{os.getpid()}.wav'
    subprocess.run([FF, '-v', 'error', '-y', '-i', path, '-ac', '1', '-ar', '16000', wav], check=True)
    import wave
    with wave.open(wav, 'rb') as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    os.remove(wav)
    hop, win = 160, 512
    n = (len(x) - win) // hop
    if n < 10:
        return {}
    frames = np.stack([x[i * hop:i * hop + win] * np.hanning(win) for i in range(n)])
    mag = np.abs(np.fft.rfft(frames, axis=1))
    logm = np.log1p(mag * 20)
    flux = np.maximum(logm[1:] - logm[:-1], 0).sum(axis=1)
    flux = np.convolve(flux, np.ones(3) / 3, mode='same')
    thr = np.median(flux) + 3.2 * np.std(flux)
    peaks = [i for i in range(2, len(flux) - 2) if flux[i] > thr and flux[i] == flux[max(0, i - 6):i + 7].max()]
    on = []
    for i in peaks:
        t = i * hop / 16000
        if not on or t - on[-1] > 0.12:
            on.append(t)
    wstarts = np.array([w['s'] for w in words]) if words else np.array([])
    sfx = [round(t, 2) for t in on if not len(wstarts) or np.abs(wstarts - t).min() > 0.09]
    rms = np.sqrt((frames ** 2).mean(axis=1))
    db = 20 * np.log10(rms + 1e-6)
    speech_mask = np.zeros(n, bool)
    for w in words:
        speech_mask[int(w['s'] * 100):int(w['e'] * 100) + 1] = True
    quiet = db[~speech_mask[:n]] if (~speech_mask[:n]).any() else db
    music = bool(np.percentile(quiet, 60) > -46) if len(quiet) else False
    return {'music_in_gaps': music, 'gap_db_p60': round(float(np.percentile(quiet, 60)), 1), 'onsets': len(on), 'sfx_candidates': sfx}


# ---------------------------------------------------------------- sheet
def label(img, text, colour=(0, 255, 255)):
    cv2.rectangle(img, (0, 0), (img.shape[1], 15), (0, 0, 0), -1)
    cv2.putText(img, text, (3, 11), cv2.FONT_HERSHEY_SIMPLEX, 0.38, colour, 1, cv2.LINE_AA)
    return img


def main():
    a = sys.argv[1:]
    path = a[0]
    out = a[a.index('--out') + 1] if '--out' in a else '/tmp/ref_study'
    os.makedirs(out, exist_ok=True)
    name = os.path.splitext(os.path.basename(path))[0]
    dur = deep.duration(path)
    frames = read_frames(path)
    rows = deep.analyse_motion(path)
    cls = [deep.classify(r) for r in rows]
    shots = detect_shots(path, dur)
    soft = soft_transitions(frames)
    words = [] if '--no-speech' in a else (lambda: deep.speech(path))()
    ev = overlay_events(frames)
    for e in ev:
        prior = [w for w in words if w['s'] <= e['t'] + 0.3]
        if prior:
            e['word'] = prior[-1]['w']; e['lead'] = round(e['t'] - prior[-1]['s'], 2)
    audio = audio_study(path, words)
    # beats: the unit a viewer perceives. Hard cuts, soft transitions, sentence ends and big graphic changes start a new beat;
    # beats are at least 1.6 s and at most 5 s long (a long continuous camera shot is cut into parts so that every part is looked at)
    bnd = {0.0, round(dur, 2)} | {s_[0] for s_ in shots} | set(soft)
    bnd |= {round(w['e'], 2) for w in words if w['w'].endswith(('.', '?', '!'))}
    bnd |= {e['t'] for e in ev if e['size'] > 0.05 and 'appears' in e['type']}
    bl = sorted(bnd)
    beats = [bl[0]]
    for t in bl[1:]:
        if t - beats[-1] >= 1.6 or t == bl[-1]:
            beats.append(t)
    if len(beats) > 1 and beats[-1] - beats[-2] < 1.0:
        beats.pop(-2)
    fin = [beats[0]]
    for t in beats[1:]:
        while t - fin[-1] > 5.0:
            fin.append(round(fin[-1] + 4.0, 2))
        fin.append(t)
    beat_list = [[fin[i], fin[i + 1]] for i in range(len(fin) - 1) if fin[i + 1] - fin[i] > 0.3]
    # per beat
    info = []
    for k, (t0, t1) in enumerate(beat_list):
        idx = [j for j, r in enumerate(rows) if t0 <= r['t'] < t1]
        cl = [cls[j] for j in idx]
        share = {c: round(cl.count(c) / max(len(cl), 1), 2) for c in set(cl)}
        zs = [rows[j]['zoom'] for j in idx if rows[j]['ok']]
        ps = [rows[j]['pan'] for j in idx if rows[j]['ok']]
        rt = [abs(rows[j]['rot']) for j in idx if rows[j]['ok']]
        dom = max(share, key=share.get) if share else 'n/a'
        mid = frames[min(int((t0 + (t1 - t0) * 0.7) * FPS), len(frames) - 1)]
        es = [e for e in ev if t0 <= e['t'] < t1]
        info.append({'k': k + 1, 't0': t0, 't1': t1, 'len': round(t1 - t0, 2), 'camera': dom, 'cam_share': share,
                     'zoom_pct_s': round(float(np.median(zs)), 1) if zs else 0, 'pan_w_s': round(float(np.median(ps)), 3) if ps else 0,
                     'rot_deg_s': round(float(np.median(rt)), 1) if rt else 0, 'base': base_style(mid), 'events': [(e['t'], e['type'] + '|' + e.get('pos', '') + '|' + e.get('colour', '')) for e in es]})
    # keyframes
    cells = []
    for s in info:
        L = s['len']
        pts = [(0.8, 'settled')]
        if L > 2.8:
            pts.insert(0, (0.25, 'entry'))
        for frac, tag in pts:
            t = min(s['t0'] + L * frac, dur - 0.05)
            et = ','.join(sorted({x[1].split('|')[0].split(' ')[0].split('/')[0][:6] for x in s['events']}))[:24]
            img = grab(path, t)
            cells.append((label(img, f"#{s['k']} {t:.1f}s {tag[:3]} {s['camera'][:5]} {s['base'][:5]} {et}"), s['k']))
    per = 15
    sheets = []
    for sidx in range(0, len(cells), per):
        chunk = cells[sidx:sidx + per]
        rows_used = (len(chunk) + 4) // 5
        canvas = np.full((CH * rows_used, CW * 5, 3), 255, np.uint8)
        for j, (img, _) in enumerate(chunk):
            r, c = divmod(j, 5)
            canvas[r * CH:(r + 1) * CH, c * CW:(c + 1) * CW] = img
            cv2.rectangle(canvas, (c * CW, r * CH), ((c + 1) * CW - 1, (r + 1) * CH - 1), (255, 255, 255), 1)
        fn = os.path.join(out, f'{name}_{sidx // per + 1}.jpg')
        cv2.imwrite(fn, canvas, [cv2.IMWRITE_JPEG_QUALITY, 82])
        sheets.append(fn)
    text = ' '.join(w['w'] for w in words)
    cam_total = {c: round(cls.count(c) / max(len(cls), 1), 2) for c in ('static', 'zoom_in', 'zoom_out', 'pan', 'mixed')}
    types = {}
    for e in ev:
        types[e['type']] = types.get(e['type'], 0) + 1
    firstq = next((w['e'] for w in words if '?' in w['w']), None)
    summary = {
        'video': name, 'dur': round(dur, 1), 'shots': len(shots), 'median_shot_s': round(float(np.median([s['len'] for s in info])), 2),
        'cuts_per_min': round(len(shots) / dur * 60, 1), 'soft_transitions': soft, 'camera': cam_total,
        'events': len(ev), 'events_per_min': round(len(ev) / dur * 60, 1), 'event_types': types,
        'beats': len(beat_list), 'bases': [s['base'] for s in info], 'speech': {'words': len(words), 'first_word': words[0]['s'] if words else None, 'first_question_end': firstq, 'text': text},
        'audio': audio, 'sheets': sheets, 'shot_info': info, 'event_list': ev,
    }
    json.dump(summary, open(os.path.join(out, name + '.json'), 'w'), indent=1)
    md = [f"# {name}  ({summary['dur']} s)", '',
          f"shots {summary['shots']} (median {summary['median_shot_s']} s, {summary['cuts_per_min']}/min) · soft transitions at {soft} · camera {cam_total}",
          f"events {summary['events']} ({summary['events_per_min']}/min) · types {types}", f"audio {audio.get('music_in_gaps')} music, {len(audio.get('sfx_candidates', []))} non-speech onsets",
          f"base styles in order: {' > '.join(summary['bases'])}", f"narration: {text}", '']
    open(os.path.join(out, name + '.md'), 'w').write('\n'.join(md))
    print(name, f"shots={len(shots)} ev={len(ev)} sheets={len(sheets)}")


if __name__ == '__main__':
    main()
