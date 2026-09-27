// Sound-effect track: every visual event in the timeline gets a matching sound.
// Each UI kit has its own sound palette (clicks and wood for "block", synth blips for "neon",
// paper and cards for "paper"...), history scenes switch to paper/page sounds, and every event
// picks one of several variants with a small pitch/volume change, so no two videos sound alike
// and repeated events don't sound copy-pasted.
import path from 'node:path';
import { ROOT, SAMPLE_RATE, decodeAudio, writeWav } from './util.mjs';

const DIR = path.join(ROOT, 'assets/sfx');
const cache = new Map();
async function load(name) {
  if (!cache.has(name)) {
    const file = name.includes('/') ? name : name + '.ogg';
    cache.set(name, await decodeAudio(path.join(DIR, file)));
  }
  return cache.get(name);
}

const seq = (pre, from, to, pad = 0, suf = '') => Array.from({ length: to - from + 1 }, (_, i) => `k/${pre}${String(from + i).padStart(pad, '0')}${suf}.ogg`);
const K = {
  click: seq('click_', 1, 5, 3), select: seq('select_', 1, 8, 3), maximize: seq('maximize_', 1, 9, 3), minimize: seq('minimize_', 1, 5, 3),
  glass: seq('glass_', 1, 6, 3), toggle: seq('toggle_', 1, 4, 3), switch: seq('switch_', 1, 7, 3), confirm: seq('confirmation_', 1, 4, 3),
  drop: seq('drop_', 1, 4, 3), scroll: seq('scroll_', 1, 5, 3), open: seq('open_', 1, 4, 3), pluck: seq('pluck_', 1, 2, 3), tick: ['k/tick_001.ogg', 'k/tick_002.ogg', 'k/tick_004.ogg'],
  punch: seq('impactPunch_medium_', 0, 4, 3), wood: seq('impactWood_heavy_', 0, 4, 3), plank: seq('impactPlank_medium_', 0, 4, 3), soft: seq('impactSoft_heavy_', 0, 4, 3),
  glassHit: seq('impactGlass_heavy_', 0, 4, 3), metal: seq('impactMetal_heavy_', 0, 4, 3), plate: seq('impactPlate_medium_', 0, 4, 3), light: seq('impactGeneric_light_', 0, 4, 3),
  pep: seq('pepSound', 1, 5), tones: ['k/twoTone1.ogg', 'k/twoTone2.ogg', 'k/threeTone1.ogg', 'k/threeTone2.ogg'], phaser: seq('phaserUp', 1, 5), power: seq('powerUp', 1, 6),
  force: seq('forceField_', 0, 4, 3), sciMetal: seq('impactMetal_', 0, 4, 3), computer: seq('computerNoise_', 0, 3, 3),
  flip: seq('bookFlip', 1, 3), place: seq('bookPlace', 1, 3), cloth: seq('cloth', 1, 4), card: seq('card-place-', 1, 4), slide: seq('card-slide-', 1, 8),
  chip: seq('chip-lay-', 1, 3), chips: seq('chips-stack-', 1, 4), uiClick: seq('click', 1, 5), roll: seq('rollover', 1, 6),
  whoosh: ['k/whoosh_a.ogg', 'k/whoosh_b.ogg', 'k/whoosh_c.ogg', 'k/whoosh_d.ogg'], sub: ['k/sub_a.ogg', 'k/sub_b.ogg'],
};

// role -> candidate clips, per kit
const PALETTES = {
  classic: { appear: K.click, place: K.drop, select: K.select, fill: K.maximize, swish: ['k/whoosh_d.ogg'], whoosh: ['k/whoosh_a.ogg', 'k/whoosh_d.ogg'], tick: K.tick, hit: K.punch, count: K.switch, ding: K.confirm },
  block: { appear: K.roll, place: K.card, select: K.toggle, fill: K.slide, swish: ['k/whoosh_b.ogg'], whoosh: ['k/whoosh_b.ogg', 'k/whoosh_a.ogg'], tick: K.chip, hit: K.wood, count: K.chip, ding: K.chips },
  neon: { appear: K.pep, place: K.tones, select: K.pep, fill: K.phaser, swish: ['k/whoosh_b.ogg', 'k/whoosh_d.ogg'], whoosh: ['k/whoosh_b.ogg', 'k/whoosh_d.ogg'], tick: K.computer, hit: K.force, count: K.pep, ding: K.power },
  paper: { appear: K.card, place: K.place, select: K.pluck, fill: K.cloth, swish: K.slide, whoosh: ['k/whoosh_c.ogg', 'k/whoosh_a.ogg'], tick: K.tick, hit: K.soft, count: K.card, ding: K.glass },
  news: { appear: K.uiClick, place: K.open, select: K.select, fill: K.scroll, swish: ['k/whoosh_a.ogg'], whoosh: ['k/whoosh_a.ogg', 'k/whoosh_b.ogg'], tick: K.tick, hit: K.metal, count: K.switch, ding: ['k/bong_001.ogg', ...K.confirm] },
  outline: { appear: K.glass, place: K.drop, select: K.glass, fill: K.minimize, swish: ['k/whoosh_d.ogg'], whoosh: ['k/whoosh_d.ogg', 'k/whoosh_c.ogg'], tick: K.tick, hit: K.glassHit, count: K.light, ding: K.glass },
};
// history scenes: pages, paper and cloth whatever the kit
const HISTORY = { fill: K.cloth, whoosh: ['k/whoosh_c.ogg'], swish: K.slide, appear: K.card, place: K.place, hit: K.soft, tick: K.tick };
// fixed one-offs (original clips)
const FIXED = { question: 'question', glitch: 'glitch', waves: 'waves', boom: 'boom', flip: null };

function hash(n) {
  const x = Math.sin(n * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
}

export function sfxEvents(tl) {
  const kit = tl.kit?.kit || 'classic';
  const P = PALETTES[kit] || PALETTES.classic;
  const eraAt = (t) => {
    const s = tl.scenes.find((sc) => t >= sc.start - 0.05 && t < sc.end + 0.05);
    return s?.era || 'now';
  };
  const ev = [];
  const add = (t, role, vol = 1) => {
    t = Math.max(0, t);
    if (FIXED[role] !== undefined) {
      if (FIXED[role]) ev.push({ t, name: FIXED[role], vol, rate: 1 });
      else ev.push({ t, name: K.flip[Math.floor(hash(t * 7) * K.flip.length)], vol, rate: 1 });
      return;
    }
    const list = (eraAt(t) === 'history' && HISTORY[role]) || P[role] || PALETTES.classic[role];
    const h = hash(t * 1000 + role.length * 17);
    ev.push({ t, name: list[Math.floor(h * list.length)], vol: vol * (0.85 + 0.3 * hash(t * 31)), rate: 0.94 + 0.12 * hash(t * 53) });
  };
  tl.scenes.forEach((s, i) => {
    if (s.transition === 'film') { add(s.start - 0.35, 'glitch', 0.5); add(s.start - 0.3, 'flip', 0.9); add(s.start - 0.25, 'whoosh', 0.6); }
    else if (s.transition === 'flash') add(s.start - 0.1, 'whoosh', 0.8);
    else if (s.transition === 'zoom' || s.transition === 'slide') add(s.start - 0.15, 'whoosh', 0.55);
    else if (s.transition === 'glitch') add(s.start - 0.1, 'glitch', 0.5);
    else if (i > 0 && s.camera) add(s.start - 0.15, 'whoosh', 0.4);
    if (s.era === 'history' && i > 0 && tl.scenes[i - 1].era !== 'history' && s.transition !== 'film') add(s.start - 0.1, 'flip', 0.8);
  });
  if (tl.scenes[0]?.camera) add(0, 'whoosh', 0.6);
  for (const el of tl.elements) {
    const t = el.start;
    switch (el.type) {
      case 'highlight':
        add(t, 'fill', 0.45);
        for (const m of el.morph || []) add(m.t, 'fill', 0.45);
        break;
      case 'label':
        if (el.anim === 'slam') { add(t, 'swish', 0.5); add(t + 0.3, 'hit', 0.5); }
        else add(t, el.style === 'map' || el.style === 'note' ? 'swish' : 'appear', 0.5);
        break;
      case 'flag':
        add(t, 'place', 0.6);
        if (el.moveAt != null) add(el.moveAt, 'swish', 0.45);
        break;
      case 'icon': add(t, 'place', 0.55); break;
      case 'badge': add(t, 'appear', 0.5); break;
      case 'character':
        add(t, 'place', 0.6);
        if (el.say) add(t + 0.3, 'select', 0.45);
        break;
      case 'scatter':
        for (let i = 0; i < Math.min(el.count || 5, 8); i++) add(t + i * (el.stagger ?? 0.09), 'appear', 0.3);
        break;
      case 'question': add(t, 'question', 0.6); break;
      case 'year': String(el.value).split('').forEach((_, i) => add(t + i * (0.45 / String(el.value).length), 'tick', 0.55)); break;
      case 'stat': add(t + 0.9, 'ding', 0.5); break;
      case 'stamp': add(t, 'hit', 0.9); add(t, 'boom', 0.25); break;
      case 'arrow': case 'line': case 'measure': add(t, 'swish', 0.45); break;
      case 'route':
        add(t, 'swish', 0.45);
        if (el.mover?.kind === 'ship') add(t, 'waves', 0.35);
        break;
      case 'ghost': add(t + (el.delay ?? 0.3), 'whoosh', 0.5); break;
      case 'ping': add(t, 'select', 0.45); break;
      case 'counter':
        el.steps.forEach((st, i) => {
          add(Math.max(st.t, el.start), 'count', 0.6);
          if (i === 0 && /\d/.test(String(st.value)) && !/^(1[0-9]|20)\d\d(\b|:)/.test(String(st.value))) add(Math.max(st.t, el.start) + 0.9, 'ding', 0.4);
        });
        break;
      case 'shake': add(t, 'boom', 0.8); add(t, 'hit', 0.6); break;
      case 'punch': add(t, 'hit', 0.5); break;
      case 'title': add(t, 'swish', 0.55); add(t + 0.3, 'hit', 0.6); break;
      case 'bars': el.items.forEach((_, i) => add(t + 0.15 + i * (el.stagger ?? 0.18), 'swish', 0.35)); add(t + 0.95 + el.items.length * (el.stagger ?? 0.18), 'ding', 0.45); break;
      case 'vs': add(t, 'whoosh', 0.6); add(t + 0.4, 'hit', 0.8); break;
      case 'timeline': for (const e of el.events) add(e.t, 'count', 0.5); break;
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
  // very quiet room-tone/air bed so the gaps between sounds are never dead silent;
  // darker for history-heavy videos, brighter for neon ones
  const kit = tl.kit?.kit || 'classic';
  const cut = { neon: 0.12, news: 0.08, block: 0.08, outline: 0.1, paper: 0.05, classic: 0.06 }[kit] ?? 0.06;
  let lp = 0, lp2 = 0, seed = 12345;
  const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff) * 2 - 1;
  for (let i = 0; i < n; i++) {
    lp += cut * (rnd() - lp);
    lp2 += 0.02 * (lp - lp2);
    const tt = i / SAMPLE_RATE;
    const env = Math.min(1, tt / 1.5) * Math.min(1, Math.max(0, tl.duration + 0.5 - tt) / 1.5);
    buf[i] += lp2 * 0.22 * env * (0.8 + 0.2 * Math.sin(tt * 0.7));
  }
  for (const e of events) {
    const clip = await load(e.name);
    const o = Math.round(e.t * SAMPLE_RATE);
    const g = e.vol * volume;
    const rate = e.rate || 1;
    const len = Math.floor(clip.length / rate);
    for (let i = 0; i < len && o + i < n; i++) {
      const x = i * rate, k = Math.floor(x), f = x - k;
      buf[o + i] += ((clip[k] || 0) * (1 - f) + (clip[k + 1] || 0) * f) * g;
    }
  }
  writeWav(out, buf);
  return events.length;
}
