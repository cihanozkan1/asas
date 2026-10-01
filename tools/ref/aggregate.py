#!/usr/bin/env python3
"""Aggregate tools/ref/deep.py JSON files into one markdown (docs/TARIF.md).

  python3 tools/ref/aggregate.py /tmp/deep > docs/TARIF.md
Only numbers and short text patterns (first/last sentence) of the reference narration are listed
for pacing analysis; no picture or sound is stored.
"""
import sys, json, glob, statistics as st

d = sys.argv[1] if len(sys.argv) > 1 else '/tmp/deep'
V = [json.load(open(f)) for f in sorted(glob.glob(d + '/*.json'))]
V = [v for v in V if v.get('dur', 0) > 5 and v.get('speech', {}).get('words')]


def q(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return float('nan')
    i = (len(xs) - 1) * p
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def row(name, xs, unit=''):
    xs = [x for x in xs if x is not None]
    return f'| {name} | {q(xs,.1):.2f} | {q(xs,.25):.2f} | **{q(xs,.5):.2f}** | {q(xs,.75):.2f} | {q(xs,.9):.2f} | {unit} |'


def lead_list(v):
    return [e['lead'] for e in v['events'].get('list', []) if e.get('lead') is not None]


print(f'# Referans kanalın ölçülmüş tarifi ({len(V)} video, `tools/ref/deep.py`)\n')
print('Her satır: videolar arası dağılım (p10 / p25 / **medyan** / p75 / p90).\n')
print('| ölçü | p10 | p25 | medyan | p75 | p90 | birim |\n|---|---|---|---|---|---|---|')
print(row('süre', [v['dur'] for v in V], 's'))
print(row('konuşma hızı', [v['speech']['wps'] for v in V], 'kelime/sn'))
print(row('ilk kelime', [v['speech'].get('first_word') for v in V], 's'))
print(row('ilk soru bitişi', [v['speech'].get('first_question_end') for v in V], 's'))
print(row('kesme', [v['cuts']['per_min'] for v in V], 'adet/dk'))
print(row('yeni öğe (olay)', [v['events']['per_min'] for v in V], 'adet/dk'))
for k in ['static', 'zoom_in', 'zoom_out', 'pan', 'mixed', 'cut_or_unknown']:
    print(row('kamera: ' + k, [v['camera']['share'][k] * 100 for v in V], '% süre'))
print(row('zoom-in hızı', [v['camera'].get('zoom_in_pct_s') for v in V], '%/sn'))
print(row('zoom-out hızı', [v['camera'].get('zoom_out_pct_s') for v in V], '%/sn'))
print(row('pan hızı', [v['camera'].get('pan_widths_s') for v in V], 'kare genişliği/sn'))
leads = [x for v in V for x in lead_list(v)]
print(row('olay → kelime ön süresi (tüm olaylar)', leads, 's'))
sc = []
for v in V:
    t = [0] + v['cuts'].get('times', []) + [v['dur']]
    sc += [b - a for a, b in zip(t, t[1:]) if b - a > 0.3]
print(row('sahne uzunluğu (sert kesmeler arası)', sc, 's'))

print('\n## Açılış cümleleri (kanca kalıpları)\n')
for v in V:
    print(f"- ({v['dur']:.0f}s, ilk soru {v['speech'].get('first_question_end')}) {v['speech'].get('first_sentence','')[:140]}")
print('\n## Bitiş cümleleri (döngü kalıpları)\n')
for v in V:
    print(f"- {v['speech'].get('last_sentence','')[:140]}")
