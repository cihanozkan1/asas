// Turns a script + narration timings into the frame-accurate timeline the page renders.
import { resolveTargetSpec, flagExists, iconUrl } from './geo.mjs';
import { normWord } from './util.mjs';

const SCREEN_DEFAULTS = { year: [0.5, 0.19], stamp: [0.5, 0.33], stat: [0.5, 0.17], title: [0.5, 0.12], bars: [0.5, 0.3], vs: [0.5, 0.27], timeline: [0.5, 0.24], clock: [0.5, 0.3] };

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
  if (typeof spec === 'string') return wordTime(scene, spec) - 0.08;
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

  const elements = [];
  let lastZoom = 0;
  for (let i = 0; i < scenes.length; i++) {
    const sc = scenes[i];
    const src = script.scenes[i];
    sc.style = src.style || script.styles?.[sc.era] || preset.styles[sc.era] || 'satellite';
    // flat palettes only have 1:10M vector data: very close shots switch to satellite imagery
    if (src.camera) lastZoom = src.camera.fit || src.camera.follow ? 0 : src.camera.zoom ?? 0;
    if (!src.style && lastZoom >= 60 && cfg.palettes?.[sc.style]) sc.style = 'satellite';
    sc.transition = src.transition || null;
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
          if (raw.mover?.kind === 'plane') el.mover = { ...el.mover, src: iconUrl('✈️') };
          break;
        case 'measure':
          el.points = [toPt(raw.from), toPt(raw.to)];
          break;
        case 'scatter':
          el.target = shortKey(await targetKey(raw.target));
          el.src = iconUrl(raw.icon);
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
        default:
          break;
      }
      if (SCREEN_DEFAULTS[el.type] && el.lat == null && !el.screen) el.screen = SCREEN_DEFAULTS[el.type];
      // dark serif years are only readable on parchment
      if (el.type === 'year' && raw.light == null && sc.style !== 'vintage') el.light = true;
      elements.push(el);
    }
  }

  // Minimum screen time: nothing should flash by. Start up to 0.6 s earlier, then run into the
  // next scene; top-of-screen cards stop before the next card takes their place.
  const MIN_ON = cfg.video.minOnScreen ?? 2.4;
  const SLOT = new Set(['counter', 'stat', 'year', 'stamp', 'title', 'bars', 'vs', 'timeline', 'clock']);
  const INSTANT = new Set(['shake', 'punch', 'tilt', 'dim']);
  for (const el of elements) {
    if (INSTANT.has(el.type) || el._until) continue;
    let deficit = MIN_ON - (el.end - el.start);
    if (deficit <= 0) continue;
    const sc = scenes[el.scene];
    const pull = Math.max(0, Math.min(deficit, 1.0, el.start - sc.start - 0.05));
    el.start -= pull;
    if (el.steps) el.start = Math.min(el.start, el.steps[0].t - 0.05);
    deficit -= pull;
    // map-anchored things must not wander far into the next (unrelated) scene
    let end = SLOT.has(el.type) ? el.end + deficit : Math.min(el.end + deficit, sc.end + 0.8);
    if (SLOT.has(el.type)) {
      const next = elements.filter((o) => o !== el && SLOT.has(o.type) && o.start > el.start + 0.1).map((o) => o.start);
      if (next.length) end = Math.min(end, Math.max(el.end, Math.min(...next) - 0.1));
    }
    el.end = Math.min(Math.max(el.end, end), narration.duration);
  }
  // Pulled-forward cards can land on top of an earlier one: the earlier card yields.
  const TOP = new Set(['counter', 'stat', 'year']);
  const tops = elements.filter((e) => TOP.has(e.type) && (!e.screen || Math.abs(e.screen[0] - 0.5) < 0.15)).sort((a, b) => a.start - b.start);
  for (let i = 0; i < tops.length - 1; i++) {
    const a = tops[i], b = tops[i + 1];
    if (a.end > b.start - 0.1) a.end = Math.max(a.start + 0.8, b.start - 0.1);
  }

  // A hook title card shares the top of the screen with counters/years: end it when the first one appears.
  for (const h of elements.filter((e) => e.type === 'title' && e.hook)) {
    const first = elements.filter((e) => ['counter', 'stat', 'year', 'bars', 'vs', 'timeline', 'clock'].includes(e.type) && e.start > h.start && e.start < h.end).sort((a, b) => a.start - b.start)[0];
    if (first) {
      // the hook stays readable for 2 s; cards that would cover it wait until it is gone
      h.end = Math.max(h.start + 2.0, first.start - 0.05);
      for (const o of elements) {
        if (!['counter', 'stat', 'year', 'bars', 'vs', 'timeline', 'clock', 'stamp'].includes(o.type) || o.start >= h.end || o.start <= h.start) continue;
        const shift = h.end + 0.05 - o.start;
        o.start += shift;
        if (o.steps) o.steps = o.steps.map((st) => ({ ...st, t: Math.max(st.t, o.start + 0.05) }));
        o.end = Math.max(o.end, o.start + 1.5);
      }
    }
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
    W: cfg.video.width,
    H: cfg.video.height,
    fps: cfg.video.fps,
    duration: narration.duration,
    preset,
    config: cfg,
    intro: script.intro || null,
    guides: !!guides,
    assets,
    targets: outTargets,
    scenes: scenes.map(({ words, ...s }) => s),
    captions: buildCaptions(scenes, cfg.captions),
    elements: merged,
  };
}
