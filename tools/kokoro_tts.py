#!/usr/bin/env python3
"""Local neural TTS with word timings (Kokoro-82M, Apache-2.0 weights, no network service, no usage limits).

Reads a JSON job list on stdin and writes, for every job, <out>/<key>.wav (24 kHz mono) and
<out>/<key>.json ([{text,start,end}] word boundaries in seconds):

  echo '{"voice":"am_michael","speed":1.1,"jobs":[{"key":"abc","text":"Hello world."}]}' | python3 tools/kokoro_tts.py <out>

The model is loaded once for the whole batch (about 15 s), each scene then takes about 1x real time on CPU.
"""
import json, os, sys, warnings
warnings.filterwarnings('ignore')
import numpy as np, soundfile as sf

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
req = json.load(sys.stdin)
from kokoro import KPipeline
pipe = KPipeline(lang_code=req.get('lang', 'a'), repo_id='hexgrad/Kokoro-82M')
for job in req['jobs']:
    audio, bounds, t0 = [], [], 0.0
    for r in pipe(job['text'], voice=req['voice'], speed=req.get('speed', 1.1)):
        a = r.audio.numpy() if hasattr(r.audio, 'numpy') else np.asarray(r.audio)
        for tk in (r.tokens or []):
            if tk.start_ts is None or tk.end_ts is None or not tk.text.strip():
                continue
            bounds.append({'text': tk.text, 'start': t0 + float(tk.start_ts), 'end': t0 + float(tk.end_ts)})
        audio.append(a)
        t0 += len(a) / 24000
    wav = np.concatenate(audio) if audio else np.zeros(2400, dtype=np.float32)
    sf.write(os.path.join(out, job['key'] + '.wav'), wav, 24000)
    json.dump(bounds, open(os.path.join(out, job['key'] + '.json'), 'w'))
    print('ok', job['key'], round(len(wav) / 24000, 2), flush=True)
