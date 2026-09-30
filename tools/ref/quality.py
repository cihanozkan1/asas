#!/usr/bin/env python3
"""Kalite kapısı: bir videoyu referans kanalın ölçülen değerleriyle kıyaslar.

  python3 tools/ref/quality.py output/<id>/<id>_geo.mp4 [--json out.json] [--strict]

Ölçülenler (10 kare/sn, 90x160 gri): ortalama kare değişimi, hareketli süre payı, durağan kare payı,
en uzun donuk an, kamera kayma hızı (faz korelasyonu), sert kesim/dk (PySceneDetect ile de doğrulanır).
Eşikler `docs/REFERANS_FARKLAR.md` içindeki 16 referans videonun ölçümünden çıkarıldı; alt sınırlar referansın en düşük
ölçümüne çekildi (mean_diff 5.0 ≥ 5.3 min; pan yalnız düz vektör haritada faz korelasyonu zayıf olduğu için 1.5).
"""
import sys, os, json, subprocess
import numpy as np

FF = os.environ.get('FFMPEG_PATH', 'ffmpeg')
GATE = {  # ad: (alt, üst, açıklama)
    'dur': (55, 100, 'süre (sn)'),
    'mean_diff': (5.0, 20, 'ortalama kare değişimi'),
    'moving_share': (0.80, 1.0, 'hareketli süre payı'),
    'still_share': (0.0, 0.05, 'tamamen durağan kare payı'),
    'longest_still_s': (0.0, 1.2, 'en uzun donuk an (sn)'),
    'pan': (1.5, 40, 'kamera kayma hızı'),
    'cuts_per_min': (3, 90, 'sert kesim/dk'),
}


def frames(path, fps=10, w=90, h=160):
    p = subprocess.Popen([FF, '-v', 'error', '-i', path, '-vf', f'fps={fps},scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    n = w * h
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, dtype=np.uint8).reshape(h, w).astype(np.float32)


def shift(a, b):
    A = np.fft.fft2(a - a.mean()); B = np.fft.fft2(b - b.mean())
    R = A * np.conj(B); R /= np.abs(R) + 1e-6
    r = np.fft.ifft2(R).real
    y, x = np.unravel_index(np.argmax(r), r.shape)
    h, w = a.shape
    y = y - h if y > h // 2 else y
    x = x - w if x > w // 2 else x
    return x, y


def measure(path):
    prev, diffs, spd = None, [], []
    for f in frames(path):
        if prev is not None:
            diffs.append(float(np.abs(f - prev).mean()))
            sx, sy = shift(f, prev)
            spd.append(float(np.hypot(sx, sy)))
        prev = f
    d = np.array(diffs)
    dur = len(d) / 10
    still = d < 0.3
    run = best = 0
    for s in still:
        run = run + 1 if s else 0
        best = max(best, run)
    m = {
        'dur': round(dur, 1),
        'mean_diff': round(float(d.mean()), 2),
        'moving_share': round(float((d > 1.5).mean()), 2),
        'still_share': round(float(still.mean()), 3),
        'longest_still_s': round(best / 10, 1),
        'pan': round(float(np.mean(spd) * 10), 1),
        'cuts_per_min': round(float((d > 25).sum() / dur * 60), 1),
    }
    try:
        from scenedetect import detect, ContentDetector
        m['scenes_scenedetect'] = len(detect(path, ContentDetector(threshold=27)))
    except Exception:
        pass
    return m


def judge(m):
    rows, ok = [], True
    for k, (lo, hi, label) in GATE.items():
        v = m[k]
        good = lo <= v <= hi
        ok &= good
        rows.append((k, label, v, f'{lo}–{hi}', good))
    return ok, rows


if __name__ == '__main__':
    path = sys.argv[1]
    m = measure(path)
    ok, rows = judge(m)
    print(f'{os.path.basename(path)}: {"GEÇTİ" if ok else "KALDI"}')
    for k, label, v, rng, good in rows:
        print(f'  {"ok  " if good else "EKSİK"} {label:32s} {v:>7} (hedef {rng})')
    if '--json' in sys.argv:
        json.dump({'metrics': m, 'pass': ok}, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
    if '--strict' in sys.argv and not ok:
        sys.exit(1)
