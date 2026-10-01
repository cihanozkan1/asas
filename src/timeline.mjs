// Turns a script + narration timings into the frame-accurate timeline the page renders.
import fs from 'node:fs';
import path from 'node:path';
import { resolveTargetSpec, flagExists, iconUrl } from './geo.mjs';
import { normWord } from './util.mjs';
import { histYearFor, histBorders } from './historical.mjs';
import { ROOT } from './util.mjs';

const SCREEN_DEFAULTS = { year: [0.5, 0.19], stamp: [0.5, 0.33], stat: [0.5, 0.17], title: [0.5, 0.12], bars: [0.5, 0.3], vs: [0.5, 0.27], timeline: [0.5, 0.24], clock: [0.5, 0.3], timebar: [0.5, 0.26], orbit: [0.5, 0.4], handstamp: [0.5, 0.33], tally: [0.5, 0.26] };
let LEAD = 0.08;   // seconds a word-timed element appears before its word (set from config.timing.lead)

function toPt(p) {
  if (!p) return null;
  if (Array.isArray(p)) return { lat: p[0], lon: p[1] };
  return { lat: p.lat, lon: p.lon };
}

// Find when a word/phrase is spoken inside a scene.
function wordTime(scene, phrase, which = 'start') {
  const want = String(phrase).split(/\s+/).map(normWord).filter(Boolean);
  const ws = scene.words;
  for (let i = 0; i < ws.length; i++) {
    let ok = true;
    for (let j = 0; j < want.length; j++) {
      const w = ws[i + j] ? normWord(ws[i + j].text) : '';
      if (!(w === want[j] || (j === want.length - 1 && w.startsWith(want[j])))) { ok = false; break; }
    }
    if (ok) return which === 'start' ? ws[i].start : ws[i + want.length - 1].end;
  }
  throw new Error(`Sahne ${scene.index + 1}: "${phrase}" kelimesi anlatımda yok ("${scene.text.slice(0, 60)}...")`);
}

function timeSpec(scene, spec, fallback) {
  if (spec == null) return fallback;
  if (typeof spec === 'number') return scene.start + spec;
  if (typeof spec === 'string') return wordTime(scene, spec) - LEAD;
  throw new Error('at/until: sayı veya kelime olmalı');
}

export function buildCaptions(scenes, cfg) {
  const caps = [];
  for (const s of scenes) {
    let cur = [];
    const flush = () => {
      if (!cur.length) return;
      caps.push({ text: cur.map((w) => w.text).join(' '), start: cur[0].start, end: cur[cur.length - 1].end, words: cur.map((w) => ({ text: w.text, start: w.start, end: w.end })) });
      cur = [];
    };
    for (const w of s.words) {
      const len = cur.reduce((a, x) => a + x.text.length + 1, 0) + w.text.length;
      if (cur.length && (cur.length >= cfg.maxWords || len > cfg.maxChars)) flush();
      cur.push(w);
      if (/[.,!?;:]$/.test(w.text)) flush();
    }
    flush();
  }
  // hold each caption until the next one starts (short gaps only)
  for (let i = 0; i < caps.length; i++) {
    const next = caps[i + 1];
    if (!next) caps[i].end += 0.4;
    else caps[i].end = next.start - caps[i].end < 0.6 ? next.start : caps[i].end + 0.25;
  }
  return caps;
}

export async function buildTimeline({ script, cfg, preset, narration, videoDir, assets, guides }) {
  LEAD = cfg.timing?.lead ?? 0.08;
  // per-video UI kit (counter/stamp/label/card look), so the videos don't all share one design
  let kit = { kit: 'classic', accent: '#ffd60a' };
  try {
    const kits = JSON.parse(fs.readFileSync(path.join(path.dirname(new URL(import.meta.url).pathname), '..', 'config', 'kits.json'), 'utf8'));
    kit = { ...kit, ...(kits[path.basename(videoDir)] || {}) };
  } catch {}
  kit = { ...kit, ...(script.ui || {}) };

  const targets = {};
  const targetKey = async (t) => {
    const spec = await resolveTargetSpec(t, videoDir);
    const k = JSON.stringify(spec);
    if (!targets[k]) targets[k] = spec;
    return k;
  };
  // Short keys for the page.
  const keyMap = new Map();
  const shortKey = (k) => {
    if (!keyMap.has(k)) keyMap.set(k, 't' + keyMap.size);
    return keyMap.get(k);
  };

  const scenes = narration.scenes.map((n, i) => ({
    index: i,
    text: script.scenes[i].text,
    start: n.start,
    end: n.end,
    words: n.words,
    era: script.scenes[i].era || 'now',
  }));

  // history scenes draw the borders of their own time (the year told in the scene, else the last
  // one told); a scene can pin it with "histYear"
  let lastHist = null;
  const histUrls = {};
  for (let i = 0; i < scenes.length; i++) {
    const src = script.scenes[i];
    if (scenes[i].era !== 'history') continue;
    const yr = (src.show || []).find((e) => e.type === 'year');
    const h = src.histYear ?? (yr ? histYearFor(yr.value) : null) ?? lastHist;
    if (!h) continue;
    lastHist = h;
    scenes[i].histYear = h;
    if (!histUrls[h]) histUrls[h] = await histBorders(h);
  }
  assets.hist = histUrls;

  const elements = [];
  let lastZoom = 0;
  for (let i = 0; i < scenes.length; i++) {
    const sc = scenes[i];
    const src = script.scenes[i];
    sc.style = src.style || script.styles?.[sc.era] || preset.styles[sc.era] || 'satellite';
    // flat palettes only have 1:10M vector data: very close shots switch to satellite imagery
    if (src.camera) lastZoom = src.camera.fit || src.camera.follow ? 0 : src.camera.zoom ?? 0;
    if (!src.style && lastZoom >= 60 && cfg.palettes?.[sc.style]) sc.style = 'satellite';
    // scenes without an explicit transition get the kit's own one every other cut
    const KIT_TR = { classic: 'zoom', block: 'zoom', neon: 'zoom', paper: 'zoom', news: 'zoom', outline: 'zoom' };
    sc.transition = src.transition || (i > 0 && i % 2 === 0 ? KIT_TR[kit.kit] || null : null);
    const sceneDur = sc.end - sc.start;
    // camera
    if (src.camera) {
      const c = src.camera;
      if (c.fit) {
        let list = c.fit;
        if (list === 'highlights') list = (src.show || []).filter((e) => e.type === 'highlight').map((e) => e.target);
        const keys = [];
        for (const t of list) keys.push(shortKey(await targetKey(t)));
        sc.camera = { fit: keys, pad: c.pad, zoomMul: c.zoomMul, lat: c.lat, lon: c.lon, dy: c.dy, bearing: c.bearing };
      } else if (c.follow) {
        const r = script.scenes.slice(0, i + 1).flatMap((x) => x.show || []).find((e) => e.id === c.follow);
        if (!r) throw new Error(`Sahne ${i + 1}: follow "${c.follow}" rotası yok`);
        const p0 = toPt(r.points[0]);
        sc.camera = { lat: p0.lat, lon: p0.lon, zoom: c.zoom ?? 3, follow: c.follow, zoomTo: c.zoomTo, bearing: c.bearing };
      } else sc.camera = { lat: c.lat, lon: c.lon, zoom: c.zoom, bearing: c.bearing };
      sc.cameraThen = [];
      for (const th of c.then || []) {
        const o = { t: timeSpec(sc, th.at, sc.start + 1), duration: th.duration, bearing: th.bearing, pad: th.pad };
        if (th.fit) { o.fit = []; for (const tg of th.fit) o.fit.push(shortKey(await targetKey(tg))); } else { o.lat = th.lat; o.lon = th.lon; o.zoom = th.zoom; }
        sc.cameraThen.push(o);
      }
      // long single-shot scenes get a second move mid-way (push in / ease back), like the reference's multi-zoom shots
      if (!c.fit && !c.follow && !(c.then || []).length && c.lat != null && c.noPush !== true && c.zoom < 400 && cfg.camera.autoPush !== false && sceneDur >= 4.2) {
        const back = i % 2 === 1 && c.zoom <= 200;
        sc.cameraThen.push({ t: sc.start + sceneDur * 0.5, duration: 1.5, lat: c.lat, lon: c.lon, zoom: back ? c.zoom / 1.3 : c.zoom * 1.4, bearing: c.bearing });
      }
      sc.cameraDuration = c.duration ?? (i === 0 ? cfg.camera.introDuration : Math.min(cfg.camera.duration, Math.max(0.6, sceneDur * 0.8)));
      sc.cameraLead = c.lead ?? (i === 0 ? 0 : cfg.camera.lead);
    } else sc.camera = null;

    for (const raw of src.show || []) {
      const el = { ...raw };
      el.start = Math.max(0, timeSpec(sc, raw.at, sc.start + 0.05));
      let end;
      if (raw.hold === 'end') end = narration.duration;
      else if (typeof raw.hold === 'number') end = scenes[Math.min(scenes.length - 1, i + raw.hold)].end;
      else end = sc.end;
      if (raw.until != null) end = typeof raw.until === 'string' ? wordTime(sc, raw.until, 'end') + 0.1 : sc.start + raw.until;
      if (raw.until != null) el._until = true;
      el.end = Math.max(el.start + 0.3, end);
      el.scene = i;
      delete el.at;
      delete el.until;
      delete el.hold;

      if (raw.morph) el.morph = raw.morph.map((m) => ({ ...m, t: timeSpec(sc, m.at, sc.start) }));
      if (raw.moveAt != null || raw.moveTo) el.moveAt = timeSpec(sc, raw.moveAt ?? 0.6, sc.start + 0.6);
      if (raw.moveTo) el.moveTo = raw.moveTo.screen ? raw.moveTo : { ...toPt(raw.moveTo), dx: raw.moveTo.dx, dy: raw.moveTo.dy };
      switch (el.type) {
        case 'counter':
          el.steps = raw.steps.map((st) => ({ value: st.value, t: timeSpec(sc, st.at, sc.start) }));
          el.start = el.steps[0].t - 0.05;
          el.end = Math.max(el.end, el.start + 0.5);
          if (!el.screen) el.screen = [0.5, 0.13];
          break;
        case 'highlight':
          el.target = shortKey(await targetKey(raw.target));
          if (el.fill?.startsWith('flag:') && !flagExists(el.fill.slice(5))) throw new Error('Bayrak yok: ' + el.fill);
          el.key = el.id || `hl|${el.target}|${el.fill}`;
          break;
        case 'flag':
          el.code = el.code.toLowerCase();
          if (!flagExists(el.code)) throw new Error('Bayrak yok: ' + el.code);
          el.key = el.id || `flag|${el.code}|${el.lat}|${el.lon}|${el.screen}`;
          break;
        case 'icon':
          el.src = iconUrl(el.icon);
          // a drawing needs no round badge; it is drawn a bit larger than the badge's emoji
          if (el.src.startsWith('/assets/art/') && !raw.plain) { el.plain = true; el.size = Math.round((raw.size || 110) * 1.3); }
          break;
        case 'arrow':
        case 'line':
          el.from = toPt(raw.from);
          el.to = toPt(raw.to);
          if (el.type === 'line' && raw.label) {
            elements.push({
              type: 'label', text: raw.label, style: raw.labelStyle || '', size: raw.labelSize || 40,
              lat: (el.from.lat + el.to.lat) / 2, lon: (el.from.lon + el.to.lon) / 2,
              dx: raw.labelDx ?? 0, dy: raw.labelDy ?? -40,
              start: el.start + 0.5, end: el.end, scene: i,
            });
          }
          break;
        case 'label':
          el.key = el.id || `label|${el.text}|${el.lat}|${el.lon}|${el.style}`;
          break;
        case 'route':
          el.points = raw.points.map(toPt);
          if (raw.mover && raw.mover.icon) el.mover = { ...raw.mover, src: iconUrl(raw.mover.icon) };
          // planes and ships are drawn illustrations (assets/art), all drawn facing right
          if (raw.mover?.image && !el.mover.src) el.mover = { ...raw.mover };
          if (raw.rider) el.rider = { ...raw.rider, to: toPt(raw.rider.to) };
          if (raw.mover?.kind === 'plane') el.mover = { ...el.mover, src: iconUrl('art:plane_top') };
          if (raw.mover?.kind === 'ship') el.mover = { ...el.mover, src: iconUrl('art:ship_' + (raw.mover.style || 'caravel')) };
          break;
        case 'measure':
          el.points = [toPt(raw.from), toPt(raw.to)];
          break;
        case 'bridge':
          el.points = [toPt(raw.from), toPt(raw.to)];
          break;
        case 'wall':
          el.points = raw.points.map(toPt);
          break;
        case 'scatter':
          el.target = shortKey(await targetKey(raw.target));
          el.src = String(raw.icon).startsWith('flag:') ? `/node_modules/flag-icons/flags/4x3/${String(raw.icon).slice(5).toLowerCase()}.svg` : iconUrl(raw.icon);
          if (el.src.startsWith('/assets/art/') && !String(raw.icon).startsWith('art:')) el.size = Math.round((raw.size || 64) * 1.25);
          break;
        case 'dim':
          el.targets = [];
          for (const t of raw.except || []) el.targets.push(shortKey(await targetKey(t)));
          break;
        case 'ghost':
          el.target = shortKey(await targetKey(raw.target));
          el.to = toPt(raw.to);
          break;
        case 'timeline':
          el.events = raw.events.map((ev) => ({ ...ev, t: timeSpec(sc, ev.at, el.start) }));
          el.start = Math.min(el.start, el.events[0].t - 0.3);
          break;
        case 'clock':
          el.steps = (raw.steps || [{ time: raw.time }]).map((st) => ({ time: st.time, t: timeSpec(sc, st.at, el.start) }));
          break;
        case 'character':
          el.key = el.id ? `char|${el.id}` : null;
          el.seed = elements.length;
          break;
        case 'pathtext':
          el.points = raw.points.map(toPt);
          break;
        case 'box':
          el.from = toPt(raw.from);
          el.to = toPt(raw.to);
          break;
        case 'crowd':
          el.counts = (raw.counts || []).map((c) => ({ n: c.n, t: timeSpec(sc, c.at, sc.start) }));
          el.red = (raw.red || []).map((c) => ({ n: c.n, t: timeSpec(sc, c.at, sc.start) }));
          break;
        case 'face':
          el.target = shortKey(await targetKey(raw.target));
          el.expr = (raw.expr || []).map((e) => ({ e: e.e, t: timeSpec(sc, e.at, sc.start) }));
          if (raw.look) el.look = toPt(raw.look);
          el.seed = elements.length;
          break;
        case 'pin':
          if (raw.icon) el.src = iconUrl(raw.icon);
          break;
        case 'react':
          el.src = iconUrl(raw.icon);
          break;
        case 'photo':
          if (!fs.existsSync(path.join(ROOT, 'assets/broll', el.image + '.jpg'))) throw new Error(`Sahne ${i + 1}: assets/broll/${el.image}.jpg yok`);
          if (el.kind === 'full' && !el.screen) el.screen = [0.5, 0.5];
          if (el.kind !== 'full' && el.lat == null && !el.screen) el.screen = [0.5, 0.42];
          break;
        case 'avatar':
          if (!fs.existsSync(path.join(ROOT, 'assets/characters', el.image + '.png'))) throw new Error(`Sahne ${i + 1}: karakter ${el.image} yok`);
          el.seed = elements.length;
          break;
        case 'timebar':
          break;
        case 'lens':
          if (el.lat == null && !el.screen) el.screen = [0.5, 0.4];
          break;
        default:
          break;
      }
      if (SCREEN_DEFAULTS[el.type] && el.lat == null && !el.screen) el.screen = SCREEN_DEFAULTS[el.type];
      // dark serif years are only readable on parchment
      if (el.type === 'year' && raw.light == null && sc.style !== 'vintage') el.light = true;
      elements.push(el);
    }
  }

  // Minimum screen time: nothing should flash by. Start up to 1 s earlier (never before its
  // scene), then run on; map-anchored things stop shortly after their scene ends.
  const MIN_ON = cfg.video.minOnScreen ?? 2.8;
  const INSTANT = new Set(['shake', 'punch', 'tilt', 'dim']);
  for (const el of elements) {
    if (INSTANT.has(el.type) || (el._until && !el.screen) || el.type === 'title') continue;
    let deficit = (el.type === 'react' ? 1.4 : MIN_ON) - (el.end - el.start);
    if (deficit <= 0) continue;
    const sc = scenes[el.scene];
    // at most a beat (0.3 s) before its word, and never before the element named just before it,
    // so things listed in the narration appear in the same order and rhythm as they are spoken
    const before = elements.filter((o) => o !== el && o.scene === el.scene && o.start < el.start && !INSTANT.has(o.type)).map((o) => o.start);
    const floor = Math.max(sc.start + 0.05, before.length ? Math.max(...before) + 0.25 : -Infinity);
    const pull = Math.max(0, Math.min(deficit, 0.3, el.start - floor));
    el.start -= pull;
    if (el.steps) el.start = Math.min(el.start, el.steps[0].t - 0.05);
    deficit -= pull;
    // map things may run into the next scene only while the view stays the same (no new camera,
    // or the same camera); otherwise they'd float over an unrelated map
    const nx = scenes[el.scene + 1];
    const same = (a, b) => !b || (a && b && !a.fit && !b.fit && Math.abs((a.lat ?? 0) - (b.lat ?? 0)) < 0.5 && Math.abs((a.lon ?? 0) - (b.lon ?? 0)) < 0.5 && Math.abs(Math.log((a.zoom || 1) / (b.zoom || 1))) < 0.35);
    // points, names and icons belong to what is being said: they leave when the narration moves on
    const POINTY = new Set(['ping', 'label', 'icon', 'flag', 'question', 'scatter', 'badge', 'measure']);
    const cap = POINTY.has(el.type) ? sc.end + 0.15 : nx && same(sc.camera, nx.camera) && nx.era === sc.era ? nx.end : sc.end + 0.8;
    const end = el.type === 'react' ? Math.min(el.end + deficit, sc.end + 0.25) : el.screen ? el.end + deficit : Math.min(el.end + deficit, cap);
    el.end = Math.min(Math.max(el.end, end), narration.duration);
  }

  // No dead air: when nothing is on screen for more than ~1.2 s inside a scene, the last thing
  // shown (in this scene, else the previous one) stays up until the next element arrives.
  // Nothing is ever pulled in front of its word.
  const visibleAt = (t) => elements.some((e) => !INSTANT.has(e.type) && e.type !== 'title' && e.start <= t && e.end >= t);
  scenes.forEach((sc, si) => {
    for (let guard = 0; guard < 12; guard++) {
      let gapStart = null, gapEnd = null;
      for (let t = sc.start + 0.2; t < sc.end; t += 0.1) {
        if (visibleAt(t)) { if (gapStart != null && t - gapStart >= 1.2) { gapEnd = t; break; } gapStart = null; continue; }
        if (gapStart == null) gapStart = t;
      }
      if (gapStart == null) break;
      if (gapEnd == null) gapEnd = sc.end;
      if (gapEnd - gapStart < 1.2) break;
      const prev = elements
        .filter((e) => !INSTANT.has(e.type) && e.type !== 'title' && e.type !== 'character' && !e.screen && !e._until && e.end <= gapStart + 0.05 && e.scene >= si - 1 && e.scene <= si)
        .sort((a, b) => b.end - a.end);
      if (!prev.length) break;
      const lastEnd = prev[0].end;
      let moved = false;
      for (const e of prev) if (lastEnd - e.end < 0.6) { e.end = gapEnd + 0.05; moved = true; }
      if (!moved) break;
    }
  });

  const VW = cfg.video.width, VH = cfg.video.height;
  const central = (e) => e.screen && e.lat == null && !e.fixed && e.type !== 'character' && Math.abs(e.screen[0] - 0.5) <= 0.3;

  // Hook title: readable for at least 2.6 s. It gives way to the first card after that;
  // cards that would start earlier wait for it.
  const HOOK_MIN = 2.6;
  for (const h of elements.filter((e) => e.type === 'title' && e.hook)) {
    const cards = elements.filter((o) => o !== h && central(o) && o.start > h.start && o.start < Math.max(h.end, h.start + HOOK_MIN)).sort((a, b) => a.start - b.start);
    const firstLate = cards.find((o) => o.start >= h.start + HOOK_MIN);
    h.end = Math.max(h.start + HOOK_MIN, firstLate ? Math.min(h.end, firstLate.start - 0.05) : h.end);
    for (const o of cards) {
      if (o.start >= h.end) continue;
      const dur = o.end - o.start;
      o.start = h.end + 0.05;
      if (o.steps) o.steps = o.steps.map((st) => ({ ...st, t: Math.max(st.t, o.start + 0.05) }));
      o.end = Math.max(o.end, o.start + Math.min(dur, MIN_ON));
    }
  }

  // Screen cards (years, counters, stamps, charts, pills...) that are on screen together are
  // stacked down the middle instead of being drawn over each other. A card of the same kind
  // replaces the previous one; if there is no room left above the captions, older cards give way.
  const est = (e) => {
    const sz = e.size;
    const txt = (v) => String(v ?? '').length;
    switch (e.type) {
      case 'year': return [txt(e.value) * (sz || 210) * 0.55, (sz || 210) * 1.5];
      case 'counter': return [Math.max(...e.steps.map((st) => txt(st.value))) * (sz || 170) * 0.62, (sz || 170) * 1.1];
      case 'stat': return [txt(e.value) * (sz || 150) * 0.62, (sz || 150) * 1.1 + 60];
      case 'stamp': return [txt(e.text) * (sz || 80) * 0.75 + 90, (sz || 80) * 2.7];
      case 'title': return [e.width || 960, (sz || 72) * 1.1 * Math.ceil((txt(e.text) * (sz || 72) * 0.5) / (e.width || 960))];
      case 'bars': return e.orient === 'v' ? [(e.items?.length || 2) * 270, (e.height || 420) + 150] : [900, (e.items?.length || 2) * 88 + 60];
      case 'vs': return [720, 260];
      case 'timeline': return [e.width || 900, 240];
      case 'clock': return [Math.max(e.size || 200, 320), (e.size || 200) + 70];
      case 'label': return [txt(e.text) * (sz || 44) * 0.62 + 50, (sz || 44) * 1.6];
      default: return null;
    }
  };
  const LIMIT = VH * 0.64;
  const placedCards = [];
  for (const c of elements.filter(central).sort((a, b) => a.start - b.start)) {
    const box = est(c);
    if (!box) continue;
    const [w, h] = box;
    const x = c.screen[0] * VW;
    let y = c.screen[1] * VH;
    const yOrig = y;
    const live = placedCards.filter((p) => p.el.start < c.end - 0.05 && p.el.end > c.start + 0.05);
    for (const p of live) {
      if (p.el.type === c.type && ['counter', 'stat', 'year', 'stamp', 'title'].includes(c.type) && Math.abs(p.y0 - yOrig) < 40) p.el.end = Math.min(p.el.end, Math.max(p.el.start + 0.8, c.start - 0.1));
    }
    const hits = (yy) => live.filter((p) => p.el.end > c.start + 0.05 && Math.abs(p.x - x) < (p.w + w) / 2 - 10 && Math.abs(p.y - yy) < (p.h + h) / 2 + 24);
    let hs = hits(y);
    for (let g = 0; hs.length && g < 6; g++) {
      y = Math.max(...hs.map((p) => p.y + p.h / 2)) + 30 + h / 2;
      hs = hits(y);
    }
    if (y + h / 2 > LIMIT) {
      y = c.screen[1] * VH;
      for (const p of hits(y)) p.el.end = Math.min(p.el.end, Math.max(p.el.start + 0.8, c.start - 0.1));
    } else if (Math.abs(y - c.screen[1] * VH) > 1) c.screen = [c.screen[0], y / VH];
    placedCards.push({ el: c, x, y, y0: yOrig, w, h });
  }

  // Same key in consecutive scenes = one continuous element (no re-animation).
  const merged = [];
  const open = new Map();
  for (const el of elements.sort((a, b) => a.start - b.start)) {
    const prev = el.key && open.get(el.key);
    if (prev && el.start <= prev.end + 0.15) {
      prev.end = Math.max(prev.end, el.end);
      continue;
    }
    merged.push(el);
    if (el.key) open.set(el.key, el);
  }

  const outTargets = {};
  for (const [k, spec] of Object.entries(targets)) outTargets[shortKey(k)] = spec;

  return {
    kit,
    W: cfg.video.width,
    H: cfg.video.height,
    fps: cfg.video.fps,
    duration: narration.duration,
    preset,
    config: cfg,
    intro: script.intro || null,
    flatClose: !!script.flatClose, // schematic close-ups: never show real imagery behind them
    guides: !!guides,
    assets,
    targets: outTargets,
    scenes: scenes.map(({ words, ...s }) => s),
    captions: buildCaptions(scenes, cfg.captions),
    elements: merged,
  };
}
