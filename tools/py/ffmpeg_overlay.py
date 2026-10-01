#!/usr/bin/env python3
"""FFmpeg timed overlay: put an emoji / GIF / PNG on a finished video at x,y between t0 and t1 (also a MoviePy v2 version).

  python3 tools/py/ffmpeg_overlay.py in.mp4 out.mp4 overlay.gif --at 540,900 --t 5,8 [--scale 400] [--fade 0.3] [--moviepy]

FFmpeg:  [1:v]scale=W:-1,format=rgba,fade=t=in:st=t0:d=f:alpha=1[o];[0:v][o]overlay=x-w/2:y-h/2:enable='between(t,t0,t1)'
(-stream_loop -1 repeats a short GIF).  Several windows:  enable='between(t,2,5)+between(t,10,15)'.
"""
import sys, subprocess, os
a = [x for x in sys.argv[1:] if not x.startswith('--')]
inp, out, ov = a[0], a[1], a[2]
def opt(n, d): return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
x, y = [float(v) for v in opt('--at', '540,900').split(',')]
t0, t1 = [float(v) for v in opt('--t', '0,3').split(',')]
sc = int(opt('--scale', '400')); fd = float(opt('--fade', '0.25'))
if '--moviepy' in sys.argv:
    from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
    base = VideoFileClip(inp)
    o = ImageClip(ov).with_start(t0).with_duration(t1 - t0).resized(width=sc).with_position((x - sc / 2, y - sc / 2)).with_effects([])
    CompositeVideoClip([base, o]).write_videofile(out, codec='libx264', audio_codec='aac', logger=None)
else:
    ff = os.environ.get('FFMPEG_PATH', 'ffmpeg')
    fc = f"[1:v]scale={sc}:-1,format=rgba,fade=t=in:st={t0}:d={fd}:alpha=1,fade=t=out:st={t1 - fd}:d={fd}:alpha=1[o];[0:v][o]overlay={x}-w/2:{y}-h/2:enable='between(t,{t0},{t1})'"
    subprocess.run([ff, '-y', '-i', inp, '-stream_loop', '-1', '-i', ov, '-filter_complex', fc, '-c:a', 'copy', '-shortest', out], check=True)
