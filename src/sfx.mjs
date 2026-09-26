// Sound-effect track: every visual event in the timeline gets a matching sound
// (pops for labels/flags, whooshes for camera moves, ticks for years...).
import path from 'node:path';
import { ROOT, SAMPLE_RATE, decodeAudio, writeWav } from './util.mjs';

const DIR = path.join(ROOT, 'assets/sfx');
const cache = new Map();
async function load(name) {
  if (!cache.has(name)) cache.set(name, await decodeAudio(path.join(DIR, name + '.ogg')));
  return cache.get(name);
}

export function sfxEvents(tl) {
  const ev = [];
  const add = (t, name, vol = 1) => ev.push({ t: Math.max(0, t), name, vol });
  tl.scenes.forEach((s, i) => {
    if (s.transition === 'film') {
      add(s.start - 0.35, 'glitch', 0.7);
      add(s.start - 0.3, 'whoosh', 0.8);
    } else if (s.transition === 'flash') add(s.start - 0.1, 'whoosh', 0.8);
    else if (i > 0 && s.camera) add(s.start - 0.15, 'whoosh', 0.35);
  });
  if (tl.scenes[0]?.camera) add(0, 'whoosh', 0.6);
  for (const el of tl.elements) {
    const t = el.start;
    switch (el.type) {
      case 'highlight':
        add(t, 'fill', 0.35);
        for (const m of el.morph || []) add(m.t, 'fill', 0.4);
        break;
      case 'label':
        if (el.anim === 'slam') { add(t, 'swish', 0.5); add(t + 0.3, 'thud', 0.45); }
        else add(t, el.style === 'map' || el.style === 'note' ? 'swish' : 'pop1', 0.45);
        break;
      case 'flag':
        add(t, 'pop2', 0.55);
        if (el.moveAt != null) add(el.moveAt, 'swish', 0.45);
        break;
      case 'icon': add(t, 'pop3', 0.5); break;
      case 'badge': add(t, 'pop1', 0.5); break;
      case 'character':
        add(t, 'pop2', 0.6);
        if (el.say) add(t + 0.3, 'select', 0.45);
        break;
      case 'scatter':
        (el._n ?? el.count ?? 10) && Array.from({ length: Math.min(el.count || 10, 14) }).forEach((_, i) => add(t + i * (el.stagger ?? 0.09), i % 2 ? 'pop1' : 'pop3', 0.22));
        break;
      case 'question': add(t, 'question', 0.6); break;
      case 'year': String(el.value).split('').forEach((_, i) => add(t + i * (0.45 / String(el.value).length), 'tick', 0.5)); break;
      case 'stat': add(t + 0.9, 'ding', 0.5); break;
      case 'stamp': add(t, 'thud', 0.9); break;
      case 'ring': add(t, 'scratch', 0.45); break;
      case 'arrow': case 'line': case 'measure': add(t, 'swish', 0.45); break;
      case 'route':
        add(t, 'whoosh', 0.4);
        if (el.mover?.kind === 'ship') add(t, 'waves', 0.35);
        break;
      case 'ghost': add(t + (el.delay ?? 0.3), 'whoosh', 0.5); break;
      case 'ping': add(t, 'select', 0.4); break;
      case 'counter': for (const st of el.steps) add(st.t, 'pop2', 0.55); break;
      case 'shake': add(t, 'boom', 0.9); add(t, 'thud', 0.6); break;
      case 'punch': add(t, 'knock', 0.5); break;
      case 'title': add(t, 'swish', 0.55); add(t + 0.3, 'thud', 0.6); break;
      case 'bars': el.items.forEach((_, i) => add(t + 0.15 + i * (el.stagger ?? 0.18), 'swish', 0.35)); add(t + 0.95 + el.items.length * (el.stagger ?? 0.18), 'ding', 0.4); break;
      case 'vs': add(t, 'whoosh', 0.6); add(t + 0.4, 'thud', 0.8); break;
      case 'timeline': for (const ev of el.events) add(ev.t, 'pop2', 0.5); break;
      case 'clock': for (const st of el.steps) { add(st.t, 'tick', 0.6); add(st.t + 0.45, 'tick', 0.5); } break;
      case 'tilt': add(t, 'whoosh', 0.45); break;
      default: break;
    }
  }
  return ev.sort((a, b) => a.t - b.t);
}

export async function buildSfxTrack(tl, out, volume = 0.5) {
  const n = Math.ceil((tl.duration + 2) * SAMPLE_RATE);
  const buf = new Float32Array(n);
  const events = sfxEvents(tl);
  for (const e of events) {
    const clip = await load(e.name);
    const o = Math.round(e.t * SAMPLE_RATE);
    const g = e.vol * volume;
    for (let i = 0; i < clip.length && o + i < n; i++) buf[o + i] += clip[i] * g;
  }
  writeWav(out, buf);
  return events.length;
}
