#!/usr/bin/env python3
"""Deep reference analysis: one JSON per video that links picture, camera, narration and pacing.

  python3 tools/ref/deep.py reference/x.mp4 [--out /tmp/deep]   (writes <out>/<name>.json)

Per video:
  camera   per 0.25 s window: global motion from ORB + RANSAC similarity transform -> zoom %/s, pan (frame widths/s), rotation deg/s;
           windows are classed static / zoom_in / zoom_out / pan / mixed; the share of each class and typical speeds are reported
  events   "new things on screen": residual of the motion-compensated frame difference (an element appearing/disappearing, not camera) -> times
  speech   faster-whisper words with timestamps; words/s, time to first word, time of the first question, first/last sentence
  link     for every event: the word being spoken (events lead or lag the word by x s)
  cuts     hard cuts (scene changes) and scene lengths
No picture, sound or text of the reference is kept; only these numbers/times.
"""
import sys, os, json, subprocess, math
import numpy as np, cv2

FF = os.environ.get('FFMPEG_PATH', 'ffmpeg')
FPS, W, H = 4, 270, 480


def frames(path):
    p = subprocess.Popen([FF, '-v', 'error', '-i', path, '-vf', f'fps={FPS},scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    n = W * H
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W)


def duration(path):
    r = subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr
    for l in r.splitlines():
        if 'Duration' in l:
            h, m, s = l.split('Duration:')[1].split(',')[0].strip().split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0


def analyse_motion(path):
    orb = cv2.ORB_create(500)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    prev = pk = pd = None
    rows = []
    for i, f in enumerate(frames(path)):
        kp, de = orb.detectAndCompute(f, None)
        r = {'t': round(i / FPS, 2), 'zoom': 0.0, 'pan': 0.0, 'rot': 0.0, 'res': 0.0, 'ok': False}
        if prev is not None and de is not None and pd is not None and len(kp) > 12 and len(pk) > 12:
            m = bf.match(pd, de)
            if len(m) >= 12:
                a = np.float32([pk[x.queryIdx].pt for x in m]); b = np.float32([kp[x.trainIdx].pt for x in m])
                M, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=2.0)
                if M is not None and inl is not None and inl.sum() >= 8:
                    s = math.hypot(M[0, 0], M[1, 0]); rot = math.degrees(math.atan2(M[1, 0], M[0, 0]))
                    r.update(ok=True, zoom=math.log(max(s, 1e-3)) * FPS * 100, pan=math.hypot(M[0, 2], M[1, 2]) * FPS / W, rot=rot * FPS)
                    warped = cv2.warpAffine(prev, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
                    mask = cv2.warpAffine(np.full_like(prev, 255), M, (W, H)) > 250
                    d = np.abs(warped.astype(np.int16) - f.astype(np.int16))
                    r['res'] = float((d[mask] > 28).mean()) if mask.any() else 0.0
        if not r['ok'] and prev is not None:
            r['res'] = float((np.abs(prev.astype(np.int16) - f.astype(np.int16)) > 28).mean())
        rows.append(r)
        prev, pk, pd = f, kp, de
    return rows


def classify(r):
    if not r['ok']:
        return 'cut_or_unknown'
    z, p = abs(r['zoom']), r['pan']
    if z < 1.5 and p < 0.04:
        return 'static'
    if z >= 1.5 and p < 0.06:
        return 'zoom_in' if r['zoom'] > 0 else 'zoom_out'
    if p >= 0.06 and z < 3:
        return 'pan'
    return 'mixed'


def speech(path):
    wav = f'/tmp/_deep_{os.getpid()}.wav'
    subprocess.run([FF, '-v', 'error', '-y', '-i', path, '-ac', '1', '-ar', '16000', wav], check=True)
    from faster_whisper import WhisperModel
    m = WhisperModel('base.en', device='cpu', compute_type='int8')
    segs, _ = m.transcribe(wav, word_timestamps=True, vad_filter=False)
    words = []
    for s in segs:
        for w in s.words or []:
            words.append({'w': w.word.strip(), 's': round(w.start, 2), 'e': round(w.end, 2)})
    return words


def main():
    path = sys.argv[1]
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/tmp/deep'
    os.makedirs(out, exist_ok=True)
    name = os.path.splitext(os.path.basename(path))[0]
    dur = duration(path)
    rows = analyse_motion(path)
    cls = [classify(r) for r in rows]
    n = max(len(cls), 1)
    share = {k: round(cls.count(k) / n, 3) for k in ('static', 'zoom_in', 'zoom_out', 'pan', 'mixed', 'cut_or_unknown')}
    zi = [r['zoom'] for r, c in zip(rows, cls) if c == 'zoom_in']; zo = [-r['zoom'] for r, c in zip(rows, cls) if c == 'zoom_out']
    pn = [r['pan'] for r, c in zip(rows, cls) if c == 'pan']
    cuts = [r['t'] for r in rows if not r['ok'] and r['res'] > 0.35]
    # events: residual peaks (new/vanishing elements), merged within 0.5 s
    res = np.array([r['res'] for r in rows]); thr = max(0.04, float(np.median(res)) * 2.2)
    ev = []
    for i, v in enumerate(res):
        if v > thr and (i == 0 or v >= res[i - 1]) and (i + 1 >= len(res) or v >= res[i + 1]) and rows[i]['t'] not in cuts:
            if not ev or rows[i]['t'] - ev[-1]['t'] > 0.5:
                ev.append({'t': rows[i]['t'], 'size': round(float(v), 3)})
    try:
        words = speech(path)
    except Exception as e:
        words = []
        print('speech failed', e, file=sys.stderr)
    for e in ev:
        prior = [w for w in words if w['s'] <= e['t'] + 0.3]
        if prior:
            w = prior[-1]; e['word'] = w['w']; e['lead'] = round(e['t'] - w['s'], 2)
    text = ' '.join(w['w'] for w in words)
    sent = [s.strip() for s in text.replace('?', '?|').replace('.', '.|').replace('!', '!|').split('|') if s.strip()]
    firstq = next((w['e'] for w in words if '?' in w['w']), None)
    res_ = {
        'video': name, 'dur': round(dur, 1),
        'camera': {'share': share, 'zoom_in_pct_s': round(float(np.median(zi)), 1) if zi else 0, 'zoom_out_pct_s': round(float(np.median(zo)), 1) if zo else 0, 'pan_widths_s': round(float(np.median(pn)), 3) if pn else 0},
        'cuts': {'n': len(cuts), 'per_min': round(len(cuts) / dur * 60, 1) if dur else 0, 'times': cuts},
        'events': {'n': len(ev), 'per_min': round(len(ev) / dur * 60, 1) if dur else 0, 'list': ev},
        'speech': {'words': len(words), 'wps': round(len(words) / dur, 2) if dur else 0, 'first_word': words[0]['s'] if words else None, 'first_question_end': firstq,
                   'first_sentence': sent[0] if sent else '', 'last_sentence': sent[-1] if sent else '', 'text': text},
    }
    json.dump(res_, open(os.path.join(out, name + '.json'), 'w'), indent=1)
    print(name, dur, share, 'events/min', res_['events']['per_min'], 'cuts/min', res_['cuts']['per_min'])


if __name__ == '__main__':
    main()
