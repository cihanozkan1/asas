#!/usr/bin/env python3
"""Ingest Google Noto Animated Emoji (CC BY 4.0, alpha WebM) into the VFX library as clip('emoji_<name>').
Source files: remotion/public/animated-emoji/<name>-1x.webm (clone of remotion-dev/animated-emoji; see docs/ARAC_KUTUSU.md).
  python3 tools/ingest_emoji.py [name ...]      (no names: the curated geo/war/nature set)
Videos using them must credit: "Animated emoji: Google Noto Emoji (CC BY 4.0)" (assets/vfx/MANIFEST.json marks them)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfx_ingest import ingest, log_license
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = ('collision fire volcano tornado fireworks skull rocket comet direct-hit flying-saucer cloud-with-lightning electricity rain-cloud snowflake '
       'droplet blood ocean globe-showing-americas globe-showing-asia-australia globe-showing-europe-africa party-popper sparkles glowing-star '
       'triangular-flag white-flag black-flag chequered-flag police-car-light sos bell eye eyes clap money-with-wings gem-stone sun-with-face '
       'thermometer-face hot-face cold-face melting wind-face bubbles bee mosquito snake crocodile shark whale dolphin t-rex dragon eagle ox '
       'thinking-face scream-cat screaming scared rage cry pleading-face mind-blown crown').split()
names = sys.argv[1:] or SET
ok = 0
for n in names:
    src = os.path.join(ROOT, 'remotion/public/animated-emoji', f'{n}-1x.webm')
    if not os.path.exists(src):
        print('skip (no file):', n); continue
    m = ingest(src, f'emoji_{n}', 'alpha', 0, 4, 24, 320, 'CC BY 4.0 (Google Noto Animated Emoji)', 'https://googlefonts.github.io/noto-emoji-animation/', 'credit: Animated emoji by Google Noto Emoji, CC BY 4.0')
    ok += 1
log_license('emoji_*', 'Google Noto Animated Emoji (animasyonlu emoji kütüphanesi, remotion-dev/animated-emoji üzerinden)', 'CC BY 4.0 — videoda/açıklamada atıf: "Animated emoji: Google Noto Emoji, CC BY 4.0"', 'https://googlefonts.github.io/noto-emoji-animation/')
print(ok, 'emoji clips')
