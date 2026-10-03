// Sound-effect track. Soft, short, synthesized sounds (plus a real page-turn for history)
// that follow what is on screen: a gentle pop when something is placed, an airy whoosh on
// camera moves, typewriter ticks for years, a soft bell when a number lands, a low thud for
// stamps. Nothing is long, harsh or noisy, events are thinned so they never pile up, and the
// track is ducked under the narration at mix time (src/audio.mjs).
// Each video gets its own tuning (base pitch / brightness) so the videos don't sound identical.
import path from 'node:path';
import { ROOT, SAMPLE_RATE, decodeAudio, writeWav } from './util.mjs';

const SR = SAMPLE_RATE;
const DIR = path.join(ROOT, 'assets/sfx');
const fileCache = new Map();
async function loadFile(name) {
  if (!fileCache.has(name)) fileCache.set(name, await decodeAudio(path.join(DIR, name)));
  return fileCache.get(name);
}

function hash(n) {
  const x = Math.sin(n * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
}
function strHash(s) {
  let h = 2166136261;
  for (const c of String(s)) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  return (h >>> 0) / 4294967296;
}

// ---- synth voices (all return Float32Array at SR) ----
const env = (i, n, a, d) => Math.min(1, i / Math.max(1, a * SR)) * Math.exp(-(i / SR) / d) * (i < n ? 1 : 0);

function pop(f0 = 700, bright = 1) {
  // bubble-like pop: fast downward pitch glide, soft attack, ~90 ms
  const n = Math.round(0.12 * SR), out = new Float32Array(n);
  let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR, f = f0 * (1 + 0.9 * Math.exp(-t / 0.012));
    ph += (2 * Math.PI * f) / SR;
    out[i] = (Math.sin(ph) + 0.18 * bright * Math.sin(2 * ph)) * env(i, n, 0.002, 0.03);
  }
  return out;
}
function tick(f0 = 2200) {
  // small wooden tick (typewriter / clock), ~40 ms
  const n = Math.round(0.05 * SR), out = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    out[i] = (Math.sin(2 * Math.PI * f0 * t) * 0.6 + Math.sin(2 * Math.PI * f0 * 1.51 * t) * 0.3) * env(i, n, 0.0005, 0.008);
  }
  return out;
}
function bell(f0 = 1046, dur = 0.9) {
  // soft marimba/bell: a few inharmonic partials with fast-decaying highs
  const n = Math.round(dur * SR), out = new Float32Array(n);
  const P = [[1, 1, 0.35], [2.0, 0.35, 0.18], [3.01, 0.12, 0.09], [4.2, 0.05, 0.05]];
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    let s = 0;
    for (const [m, a, d] of P) s += a * Math.sin(2 * Math.PI * f0 * m * t) * Math.exp(-t / d);
    out[i] = s * Math.min(1, i / (0.003 * SR)) * 0.8;
  }
  return out;
}
function whoosh(dur = 0.45, bright = 1, seed = 1) {
  // airy swell: noise through a resonant band-pass sweeping up then down, smooth envelope
  const n = Math.round(dur * SR), out = new Float32Array(n);
  let s = (seed * 9301 + 49297) % 233280, lp = 0, bp = 0, lp2 = 0;
  const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280) * 2 - 1;
  for (let i = 0; i < n; i++) {
    const u = i / n;
    const fc = (300 + 1500 * bright * Math.sin(Math.PI * Math.min(1, u * 1.15))) / SR;
    const g = 2 * Math.sin(Math.PI * fc), q = 0.55;
    const x = rnd();
    lp += g * bp;
    const hp = x - lp - q * bp;
    bp += g * hp;
    lp2 += 0.25 * (bp - lp2);
    const e = Math.pow(Math.sin(Math.PI * Math.min(1, u)), 1.6);
    out[i] = lp2 * e * 1.6;
  }
  return out;
}
function thud(f0 = 70) {
  // soft low thud for stamps / big reveals, ~300 ms, no rumble tail
  const n = Math.round(0.32 * SR), out = new Float32Array(n);
  let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR, f = f0 * (1 + 1.2 * Math.exp(-t / 0.03));
    ph += (2 * Math.PI * f) / SR;
    out[i] = Math.sin(ph) * env(i, n, 0.002, 0.08);
  }
  return out;
}
function boom(dur = 0.55) {
  // distant cannon / impact: falling sine + a burst of low noise, quick decay
  const n = Math.round(dur * SR), out = new Float32Array(n);
  let ph = 0, lp = 0, sd = 7;
  const rnd = () => ((sd = (sd * 9301 + 49297) % 233280) / 233280) * 2 - 1;
  for (let i = 0; i < n; i++) {
    const t = i / SR, f = 48 + 90 * Math.exp(-t / 0.07);
    ph += (2 * Math.PI * f) / SR;
    lp += 0.06 * (rnd() - lp);
    out[i] = (Math.sin(ph) * 0.8 + lp * 2.2 * Math.exp(-t / 0.08)) * Math.exp(-t / 0.16) * Math.min(1, t / 0.004);
  }
  return out;
}
function rumble(dur = 1.4) {
  // low volcanic rumble: filtered noise swelling in and out
  const n = Math.round(dur * SR), out = new Float32Array(n);
  let lp = 0, lp2 = 0, sd = 11;
  const rnd = () => ((sd = (sd * 9301 + 49297) % 233280) / 233280) * 2 - 1;
  for (let i = 0; i < n; i++) {
    const u = i / n;
    lp += 0.02 * (rnd() - lp); lp2 += 0.08 * (lp - lp2);
    out[i] = lp2 * 14 * Math.sin(Math.PI * u) ** 1.5;
  }
  return out;
}
function rise(dur = 0.35, f0 = 500) {
  // tiny upward "ping" for question marks / emphasis
  const n = Math.round(dur * SR), out = new Float32Array(n);
  let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR, f = f0 * (1 + 0.6 * (t / dur));
    ph += (2 * Math.PI * f) / SR;
    out[i] = Math.sin(ph) * env(i, n, 0.01, 0.12);
  }
  return out;
}

function rewind(dur = 0.8, bright = 1) {
  // tape rewind: a whoosh played backwards, with a downward "wow" from a fast wobble
  const w = whoosh(dur, bright, 7);
  const out = new Float32Array(w.length);
  for (let i = 0; i < w.length; i++) out[i] = w[w.length - 1 - i] * (0.75 + 0.25 * Math.sin((i / SR) * 80));
  return out;
}

// relative loudness of each role (the whole track is scaled again at mix time)
const GAIN = { pop: 0.28, tick: 0.14, bell: 0.16, whoosh: 0.2, thud: 0.26, rise: 0.12, page: 0.28, rewind: 0.22, boom: 0.3, rumble: 0.3 };

export function sfxEvents(tl) {
  const tune = strHash(JSON.stringify(tl.kit || '') + tl.duration.toFixed(2));
  const ev = [];
  const add = (t, role, vol = 1) => ev.push({ t: Math.max(0, t), role, vol });
  tl.scenes.forEach((s, i) => {
    if (i === 0) return;
    const prev = tl.scenes[i - 1];
    if (s.era === 'history' && prev.era !== 'history') add(s.start - 0.15, 'page', 1);
    else if (s.era !== 'history' && prev.era === 'history') add(s.start - 0.2, 'whoosh', 0.8);
    else if (s.transition === 'rewind') add(s.start - 0.25, 'rewind', 1);
    else if (s.transition === 'blast') { add(s.start - 0.1, 'thud', 1); add(s.start, 'whoosh', 0.7); }
    else if (s.transition === 'ice') add(s.start - 0.2, 'bell', 0.7);
    else if (s.transition || s.camera) add(s.start - 0.2, 'whoosh', s.transition ? 0.7 : 0.5);
  });
  if (tl.scenes[0]?.camera) add(0.1, 'whoosh', 0.7);
  for (const el of tl.elements) {
    const t = el.start;
    switch (el.type) {
      case 'highlight': add(t, 'whoosh', 0.35); break;
      case 'label': add(t, el.anim === 'slam' ? 'thud' : 'pop', el.anim === 'slam' ? 0.45 : 0.55); break;
      case 'flag': case 'icon': case 'badge': case 'character': add(t, 'pop', 0.8); break;
      case 'scatter': for (let i = 0; i < Math.min(el.count || 4, 5); i++) add(t + i * (el.stagger ?? 0.1), 'pop', 0.45); break;
      case 'question': add(t, 'rise', 1); break;
      case 'year': String(el.value).split('').forEach((_, i) => add(t + i * (0.45 / String(el.value).length), 'tick', 1)); break;
      case 'stat': add(t + 0.9, 'bell', 0.8); break;
      case 'stamp': add(t, 'thud', 1); break;
      case 'arrow': case 'line': case 'measure': case 'route': add(t, 'whoosh', 0.4); break;
      case 'bridge': add(t, 'whoosh', 0.35); add(t + (el.buildDur ?? 1.0) * 0.9, 'pop', 0.7); break;
      case 'wall':
        add(t, 'whoosh', 0.35);
        if (el.siege) {
          // same schedule as the renderer: shot i fires at start + delay + i*T, the ball lands 0.45 s later
          const n = el.siege.shots ?? 11, delay = el.siege.delay ?? 1.4, dur = Math.max(2.5, el.end - el.start);
          const T = Math.max(0.28, (dur * 0.8 - delay) / Math.max(1, n - 1));
          for (let i = 0; i < n; i++) add(el.start + delay + i * T + 0.45, 'boom', i >= n - 2 ? 0.95 : 0.62);
        } else add(t + (el.buildDur ?? 1.4), 'thud', 0.5);
        break;
      case 'eruption': add(t, 'rumble', 0.9); add(t + 0.05, 'boom', 0.7); break;
      case 'ghost': add(t + (el.delay ?? 0.3), 'whoosh', 0.5); break;
      case 'react': add(t, 'pop', 0.9); add(t + 0.05, 'rise', 0.7); break;
      case 'avatar': case 'pin': case 'face': case 'box': add(t, 'pop', 0.7); break;
      case 'photo': add(t, 'whoosh', 0.5); break;
      case 'lens': add(t, 'whoosh', 0.6); add(t + 0.45, 'pop', 0.6); break;
      case 'handstamp': add(t + 0.42, 'thud', 1); break;
      case 'crowd': for (let i = 0; i < 3; i++) add(t + 0.2 + i * 0.25, 'pop', 0.4); break;
      case 'pathtext': add(t, 'whoosh', 0.35); break;
      case 'timebar': add(t, 'whoosh', 0.4); add(t + 1.6, 'bell', 0.7); break;
      case 'link': add(t, 'tick', 0.8); break;
      case 'beam': add(t, 'rise', 0.6); break;
      case 'ping': add(t, 'pop', 0.5); break;
      case 'ban': add(t + 0.3, 'tick', 0.8); add(t + 0.55, 'thud', 0.45); break;
      case 'reason': case 'banner': add(t, 'pop', 0.6); break;
      case 'retext': add(t + (el.strikeAt ?? 0.7), 'tick', 0.8); add(t + (el.strikeAt ?? 0.7) + 0.35, 'pop', 0.6); break;
      case 'clone': case 'section': case 'radii': case 'protest': add(t, 'whoosh', 0.45); break;
      case 'wave': add(t, 'rise', 0.5); break;
      case 'counter': {
        const st = el.steps[0];
        const rolls = /\d/.test(String(st.value)) && !/^(1[0-9]|20)\d\d(\b|:)/.test(String(st.value));
        add(Math.max(st.t, el.start), 'pop', 0.7);
        if (rolls) add(Math.max(st.t, el.start) + 0.9, 'bell', 0.9);
        el.steps.slice(1).forEach((s2) => add(s2.t, 'tick', 1));
        break;
      }
      case 'title': add(t, 'whoosh', 0.6); break;
      case 'bars': el.items.forEach((_, i) => add(t + 0.15 + i * (el.stagger ?? 0.22), 'pop', 0.55)); add(t + 1.0 + el.items.length * (el.stagger ?? 0.22), 'bell', 0.7); break;
      case 'vs': add(t, 'whoosh', 0.6); add(t + 0.4, 'thud', 0.6); break;
      case 'timeline': for (const e of el.events) add(e.t, 'pop', 0.55); break;
      case 'clock': add(t, 'tick', 1); break;
      default: break;
    }
  }
  ev.sort((a, b) => a.t - b.t);
  // sparse on purpose: a sound is a signal, not wallpaper. Each role has its own minimum gap,
  // soft events (vol < 0.6) are dropped about every third time (per-video pattern), and at most
  // one sound per 0.7 s (ticks and page turns excepted).
  const GAP = { pop: 0.9, whoosh: 2.4, thud: 3.0, bell: 2.6, rise: 3.2, tick: 0.12, page: 0.5, rewind: 4, boom: 0.3, rumble: 4 };
  const out = [];
  for (const e of ev) {
    if (e.vol < 0.6 && hash(e.t * 31 + tune * 97) < 0.34) continue;
    const last = [...out].reverse().find((o) => o.role === e.role);
    if (last && e.t - last.t < (GAP[e.role] ?? 1)) continue;
    if (e.role !== 'tick' && e.role !== 'page' && e.role !== 'boom' && out.some((o) => o.role !== 'tick' && e.t - o.t < 0.7)) continue;
    out.push(e);
  }
  return out.map((e, i) => ({ ...e, tune, var: hash(e.t * 97 + i) }));
}

async function voiceFor(e) {
  // per-video tuning: base pitch within about +-3 semitones, brightness 0.7-1.3
  const k = Math.pow(2, (e.tune - 0.5) * 0.5), v = 1 + (e.var - 0.5) * 0.08, b = 0.7 + e.tune * 0.6;
  switch (e.role) {
    case 'pop': return pop(640 * k * v, b);
    case 'tick': return tick(2100 * k * v);
    case 'bell': return bell(988 * k, 0.9);
    case 'whoosh': return whoosh(0.38 + e.var * 0.14, b, Math.floor(e.var * 1000) + 1);
    case 'thud': return thud(68 * k);
    case 'rise': return rise(0.32, 520 * k);
    case 'rewind': return rewind(0.8, b);
    case 'boom': return boom();
    case 'rumble': return rumble();
    case 'page': return loadFile(`k/bookFlip${1 + Math.floor(e.var * 3)}.ogg`);
    default: return new Float32Array(1);
  }
}

export async function buildSfxTrack(tl, out, volume = 0.5) {
  const n = Math.ceil((tl.duration + 2) * SR);
  const buf = new Float32Array(n);
  const events = sfxEvents(tl);
  for (const e of events) {
    const clip = await voiceFor(e);
    const o = Math.round(e.t * SR);
    const g = e.vol * (GAIN[e.role] ?? 0.3) * volume * 2;
    const len = Math.min(clip.length, Math.round(1.2 * SR));
    for (let i = 0; i < len && o + i < n; i++) {
      const fade = i > len - 480 ? (len - i) / 480 : 1;
      buf[o + i] += clip[i] * g * fade;
    }
  }
  // gentle soft-clip so stacked sounds can never spike
  for (let i = 0; i < n; i++) buf[i] = Math.tanh(buf[i] * 1.2) / 1.2;
  writeWav(out, buf);
  return events.length;
}
