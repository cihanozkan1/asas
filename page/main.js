// Frame renderer. Everything on screen is a pure function of time t, so headless
// Chrome can step through frames deterministically: GG.init(timeline) then GG.frame(t).
import { geoPath, geoBounds, geoContains, geoCentroid, geoDistance, geoCircle, geoArea } from 'd3-geo';
import { feature as topoFeature, mesh as topoMesh } from 'topojson-client';
import { Raster } from './raster.js';
import { CameraPath, makeProjection, ease, clamp01 } from './camera.js';

const W = 1080;
const H = 1920;
const $ = (id) => document.getElementById(id);

const state = {};

// ---------------------------------------------------------------- loading

function loadImg(url) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => img.decode().then(() => resolve(img), () => resolve(img));
    img.onerror = () => reject(new Error('image failed: ' + url));
    img.src = url;
  });
}

async function loadJson(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error('fetch failed: ' + url);
  return r.json();
}

function rasterize(img, w, h) {
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  c.getContext('2d').drawImage(img, 0, 0, w, h);
  return c;
}

export const flagUrl = (code) => `/node_modules/flag-icons/flags/4x3/${code}.svg`;

// ---------------------------------------------------------------- geo data

function prepareGeo(c50, c10, l50, l10) {
  const f50 = topoFeature(c50, c50.objects.countries).features;
  const f10 = topoFeature(c10, c10.objects.countries).features;
  const land10 = dropPolar(topoFeature(l10, l10.objects.land));
  const land50 = dropPolar(topoFeature(l50, l50.objects.land));
  const borders50 = topoMesh(c50, c50.objects.countries, (a, b) => a !== b);
  const borders10 = topoMesh(c10, c10.objects.countries, (a, b) => a !== b);
  return {
    countries10: f10,
    borders50,
    borders10,
    land50,
    land10,
    cull: {
      land50: indexParts(land50.geometry.coordinates, (p) => p[0]),
      land10: indexParts(land10.geometry.coordinates, (p) => p[0]),
      borders50: indexParts(borders50.coordinates, (l) => l),
      borders10: indexParts(borders10.coordinates, (l) => l),
    },
    byId: new Map(f10.filter((f) => f.id).map((f) => [f.id, f])),
    byName: new Map(f10.map((f) => [f.properties.name.toLowerCase(), f])),
    all50: f50,
  };
}

// Antarctica wraps the pole; in Mercator its ring turns into an inverted fill.
function dropPolar(f) {
  const g = f.type === 'FeatureCollection' ? f.features[0].geometry : f.geometry;
  const polys = g.type === 'MultiPolygon' ? g.coordinates : [g.coordinates];
  // also drop mis-wound tiny islands whose spherical area is "everything but the island"
  const keep = polys.filter(
    (p) => Math.max(...p[0].map((c) => c[1])) > -60 && geoArea({ type: 'Polygon', coordinates: p }) < 2 * Math.PI,
  );
  return { type: 'Feature', properties: {}, geometry: { type: 'MultiPolygon', coordinates: keep } };
}

// Detail imagery only replaces land: water in Sentinel mosaics is flat navy and
// would show up as a dark rectangle against the base texture.
function meanRgb(ctx, w, h) {
  const d = ctx.getImageData(0, 0, w, h).data;
  let r = 0, g = 0, b = 0, n = 0;
  for (let i = 0; i < d.length; i += 16) {
    if (d[i + 3] < 250) continue;
    r += d[i]; g += d[i + 1]; b += d[i + 2]; n++;
  }
  return n ? [r / n, g / n, b / n] : null;
}

function landMasked(img, bbox, land, base) {
  const c = document.createElement('canvas');
  c.width = img.width;
  c.height = img.height;
  const ctx = c.getContext('2d');
  ctx.drawImage(img, 0, 0);
  const [w, s, e, n] = bbox;
  const sx = c.width / (e - w), sy = c.height / (n - s);
  const m = document.createElement('canvas');
  m.width = c.width;
  m.height = c.height;
  const mc = m.getContext('2d');
  mc.filter = 'blur(3px)';
  mc.fillStyle = '#fff';
  mc.beginPath();
  for (const poly of land.geometry.coordinates) {
    for (const ring of poly) {
      ring.forEach(([lon, lat], i) => {
        const x = (lon - w) * sx, y = (n - lat) * sy;
        if (i === 0) mc.moveTo(x, y);
        else mc.lineTo(x, y);
      });
      mc.closePath();
    }
  }
  mc.fill('evenodd');
  ctx.globalCompositeOperation = 'destination-in';
  ctx.drawImage(m, 0, 0);
  // Match the detail's colours to the base texture over the same land, so the
  // boundary between the two imagery sources does not show as a box.
  const bc = document.createElement('canvas');
  bc.width = c.width;
  bc.height = c.height;
  const bx = bc.getContext('2d');
  const BW = base.width, BH = base.height;
  bx.drawImage(base, ((w + 180) / 360) * BW, ((90 - n) / 180) * BH, ((e - w) / 360) * BW, ((n - s) / 180) * BH, 0, 0, c.width, c.height);
  bx.globalCompositeOperation = 'destination-in';
  bx.drawImage(m, 0, 0);
  const a = meanRgb(ctx, c.width, c.height), b = meanRgb(bx, c.width, c.height);
  if (a && b) {
    const img2 = ctx.getImageData(0, 0, c.width, c.height);
    const d = img2.data;
    const gain = [0, 1, 2].map((i) => Math.min(2, Math.max(0.5, b[i] / Math.max(a[i], 1))));
    for (let i = 0; i < d.length; i += 4) {
      d[i] = Math.min(255, d[i] * gain[0]);
      d[i + 1] = Math.min(255, d[i + 1] * gain[1]);
      d[i + 2] = Math.min(255, d[i + 2] * gain[2]);
    }
    ctx.globalCompositeOperation = 'source-over';
    ctx.putImageData(img2, 0, 0);
  }
  return c;
}

// Bounding boxes per polygon / line so each frame only draws what is on screen.
function indexParts(parts, ring) {
  return parts.map((part) => {
    let x0 = 180, y0 = 90, x1 = -180, y1 = -90;
    for (const [x, y] of ring(part)) {
      if (x < x0) x0 = x; if (x > x1) x1 = x;
      if (y < y0) y0 = y; if (y > y1) y1 = y;
    }
    return { part, box: [x0, y0, x1, y1] };
  });
}

function viewBox(proj, view) {
  if (view.mode === 'globe' && view.k < state.baseK * 2.5) return null; // whole globe visible
  let x0 = 180, y0 = 90, x1 = -180, y1 = -90;
  for (let i = 0; i <= 6; i++) {
    for (let j = 0; j <= 10; j++) {
      const q = proj.invert([(W * i) / 6, (H * j) / 10]);
      if (!q || !isFinite(q[0]) || !isFinite(q[1])) return null;
      x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]);
      y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]);
    }
  }
  if (x1 - x0 > 300) return null;
  const mx = (x1 - x0) * 0.1 + 0.5, my = (y1 - y0) * 0.1 + 0.5;
  return [x0 - mx, y0 - my, x1 + mx, y1 + my];
}

function culled(index, box, type) {
  const parts = box
    ? index.filter(({ box: b }) => b[2] >= box[0] && b[0] <= box[2] && b[3] >= box[1] && b[1] <= box[3]).map((p) => p.part)
    : index.map((p) => p.part);
  return { type, coordinates: parts };
}

function pickPart(feat, pt) {
  if (feat.geometry.type !== 'MultiPolygon') return feat;
  const p = [pt.lon, pt.lat];
  let best = null;
  let bestD = Infinity;
  for (const coords of feat.geometry.coordinates) {
    const poly = { type: 'Feature', geometry: { type: 'Polygon', coordinates: coords } };
    if (geoContains(poly, p)) return poly;
    const d = geoDistance(geoCentroid(poly), p);
    if (d < bestD) { bestD = d; best = poly; }
  }
  return best;
}

function resolveTarget(spec, geo) {
  // spec from Node: {type:'country', id?, name?, part?} | {type:'feature', feature} | {type:'circle', lat, lon, km}
  if (spec.type === 'feature') return [spec.feature];
  if (spec.type === 'circle') {
    const g = geoCircle().center([spec.lon, spec.lat]).radius(spec.km / 111.195).precision(2)();
    return [{ type: 'Feature', geometry: g }];
  }
  if (spec.type === 'country') {
    const f = (spec.id && geo.byId.get(spec.id)) || (spec.name && geo.byName.get(spec.name.toLowerCase()));
    if (!f) throw new Error('unknown country ' + JSON.stringify(spec));
    return [spec.part ? pickPart(f, spec.part) : f];
  }
  if (spec.type === 'multi') return spec.items.flatMap((s) => resolveTarget(s, geo));
  throw new Error('bad target ' + JSON.stringify(spec));
}

// ---------------------------------------------------------------- view helpers

function viewFor(cam, mode) {
  const L = state.tl.config.layout;
  return {
    mode,
    lat: cam.lat,
    lon: cam.lon,
    k: cam.zoom * state.baseK,
    cx: W / 2,
    cy: H * L.mapCenterY,
  };
}

function fitCamera(features, mode, pad, override = {}) {
  const L = state.tl.config.layout;
  const fc = { type: 'FeatureCollection', features };
  const [[w, s], [e, n]] = geoBounds(fc);
  let lon = e >= w ? (w + e) / 2 : ((w + e + 360) / 2 > 180 ? (w + e + 360) / 2 - 360 : (w + e + 360) / 2);
  let lat = (s + n) / 2;
  if (mode === 'globe' && (n - s > 60 || (e - w + 360) % 360 > 120)) [lon, lat] = geoCentroid(fc);
  let cam = { lat, lon, zoom: 1 };
  const availW = W * L.fitWidth;
  const availH = H * L.fitHeight;
  for (let i = 0; i < 3; i++) {
    const proj = makeProjection(viewFor(cam, mode));
    const b = geoPath(proj).bounds(fc);
    const bw = Math.max(b[1][0] - b[0][0], 1);
    const bh = Math.max(b[1][1] - b[0][1], 1);
    const z = cam.zoom * Math.min(availW / bw, availH / bh) * pad;
    const c = proj.invert([(b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2]);
    cam = { lon: c ? c[0] : cam.lon, lat: c ? c[1] : cam.lat, zoom: z };
  }
  cam.zoom = Math.max(mode === 'globe' ? 0.9 : 0.35, Math.min(cam.zoom * (override.zoomMul ?? 1), 800));
  if (override.lat != null) cam.lat = override.lat;
  if (override.lon != null) cam.lon = override.lon;
  if (override.dy) cam.lat += override.dy;
  return cam;
}

// ---------------------------------------------------------------- init

async function init(tl) {
  state.tl = tl;
  const cfg = tl.config;
  state.mode = tl.preset.projection; // 'globe' | 'flat'
  state.baseK = W * cfg.layout.globeRadius;

  for (const id of ['space', 'raster', 'vector', 'paper', 'marks']) {
    $(id).width = W;
    $(id).height = H;
  }

  const [c50, c10, l50, l10, earth] = await Promise.all([
    loadJson('/node_modules/world-atlas/countries-50m.json'),
    loadJson('/node_modules/world-atlas/countries-10m.json'),
    loadJson('/node_modules/world-atlas/land-50m.json'),
    loadJson('/node_modules/world-atlas/land-10m.json'),
    loadImg(tl.assets.earth),
  ]);
  state.geo = prepareGeo(c50, c10, l50, l10);

  state.raster = new Raster($('raster'));
  const rs = cfg.video.rasterScale;
  state.raster.setScale(W, H, rs === 'auto' || rs == null ? (state.raster.software ? 0.6 : 1) : rs);
  state.raster.setBase(earth);
  for (const d of tl.assets.detail || []) state.raster.addDetail(landMasked(await loadImg(d.url), d.bbox, state.geo.land10, earth), d.bbox);

  // targets
  state.targets = {};
  state.targetIdx = {};
  for (const [key, spec] of Object.entries(tl.targets)) {
    state.targets[key] = resolveTarget(spec, state.geo);
    const polys = [];
    for (const f of state.targets[key]) {
      const g = f.geometry;
      if (g.type === 'Polygon') polys.push(g.coordinates);
      else if (g.type === 'MultiPolygon') polys.push(...g.coordinates);
    }
    state.targetIdx[key] = indexParts(polys, (p) => p[0]);
  }

  // images for flags / icons
  state.images = {};
  const wanted = new Set();
  for (const el of tl.elements) {
    if (el.fill && el.fill.startsWith('flag:')) wanted.add(flagUrl(el.fill.slice(5)));
    if (el.type === 'flag') wanted.add(flagUrl(el.code));
    if (el.type === 'icon') wanted.add(el.src);
  }
  await Promise.all([...wanted].map(async (u) => (state.images[u] = await loadImg(u))));
  state.flagCanvas = {};
  for (const u of wanted) if (u.includes('/flags/')) state.flagCanvas[u] = rasterize(state.images[u], 1200, 900);

  // camera
  const mode = state.mode;
  const shots = tl.scenes.map((s) => {
    let target = null;
    if (s.camera) {
      if (s.camera.fit) {
        const feats = s.camera.fit.flatMap((k) => state.targets[k]);
        target = fitCamera(feats, mode, s.camera.pad ?? 0.85, s.camera);
      } else {
        target = { lat: s.camera.lat, lon: s.camera.lon, zoom: s.camera.zoom };
      }
    }
    return { start: s.start, end: s.end, target, duration: s.cameraDuration, lead: s.cameraLead };
  });
  const first = shots.find((s) => s.target)?.target || { lat: 20, lon: 0, zoom: 1 };
  const intro = tl.intro || {};
  const introCam = {
    lat: first.lat + (intro.dLat ?? -8),
    lon: first.lon + (intro.dLon ?? 40),
    zoom: intro.zoom ?? (mode === 'globe' ? 0.95 : Math.max(0.55, first.zoom * 0.35)),
  };
  state.camera = new CameraPath(shots, introCam, { W, baseK: state.baseK, drift: cfg.camera.drift });
  state.sceneShots = shots;

  drawSpace();
  drawPaper();
  buildUi();
  if (tl.guides) drawGuides();
  await document.fonts.ready;
  await Promise.all(
    ['600 40px Montserrat', '700 40px Montserrat', '800 40px Montserrat', '900 40px Montserrat',
      '400 40px "Playfair Display"', '700 40px "Playfair Display"'].map((f) => document.fonts.load(f)),
  );
  return { ok: true, maxTexture: state.raster.maxTex, renderer: state.raster.renderer, rasterScale: $('raster').width / W };
}

// ---------------------------------------------------------------- static layers

function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

function drawSpace() {
  const ctx = $('space').getContext('2d');
  const g = ctx.createRadialGradient(W * 0.5, H * 0.42, 100, W * 0.5, H * 0.42, H * 0.8);
  g.addColorStop(0, '#0b1830');
  g.addColorStop(1, '#010207');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, W, H);
  const r = rng(7);
  for (let i = 0; i < 900; i++) {
    const a = r() * 0.8 + 0.1;
    ctx.fillStyle = `rgba(255,255,255,${a * a})`;
    const s = r() < 0.94 ? 1.2 : 2.4;
    ctx.fillRect(r() * W, r() * H, s, s);
  }
}

function drawPaper() {
  // Old-paper grain & stains, multiplied over the vintage map.
  const c = $('paper');
  const ctx = c.getContext('2d');
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, W, H);
  const r = rng(42);
  for (let i = 0; i < 60; i++) {
    const x = r() * W, y = r() * H, rad = 80 + r() * 380;
    const g = ctx.createRadialGradient(x, y, 0, x, y, rad);
    const a = 0.05 + r() * 0.08;
    g.addColorStop(0, `rgba(150,120,80,${a})`);
    g.addColorStop(1, 'rgba(150,120,80,0)');
    ctx.fillStyle = g;
    ctx.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  const img = ctx.getImageData(0, 0, W, H);
  const d = img.data;
  for (let i = 0; i < d.length; i += 4) {
    const n = (r() - 0.5) * 34;
    d[i] = Math.min(255, d[i] + n);
    d[i + 1] = Math.min(255, d[i + 1] + n);
    d[i + 2] = Math.min(255, d[i + 2] + n);
  }
  ctx.putImageData(img, 0, 0);
  const v = ctx.createRadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.75);
  v.addColorStop(0, 'rgba(0,0,0,0)');
  v.addColorStop(1, 'rgba(90,60,30,0.35)');
  ctx.fillStyle = v;
  ctx.fillRect(0, 0, W, H);
}

function drawGuides() {
  const s = state.tl.config.safe;
  const g = $('guides');
  const zone = (x, y, w, h) => {
    const d = document.createElement('div');
    d.className = 'zone';
    Object.assign(d.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
    g.appendChild(d);
  };
  zone(0, H * (1 - s.bottom), W, H * s.bottom);
  zone(W * (1 - s.right), H * 0.45, W * s.right, H * (0.55 - s.bottom));
  zone(0, 0, W, H * s.top);
}

// ---------------------------------------------------------------- style mixing

function styleAt(t) {
  // returns satellite vs vintage mix (0..1 each) with crossfades at scene boundaries
  const scenes = state.tl.scenes;
  let cur = scenes[0].style;
  let mix = 1;
  let prev = cur;
  for (let i = 0; i < scenes.length; i++) {
    const s = scenes[i];
    if (s.start > t + 0.25) break;
    if (i > 0 && s.style !== scenes[i - 1].style) {
      const u = clamp01((t - (s.start - 0.2)) / 0.45);
      prev = scenes[i - 1].style;
      cur = s.style;
      mix = u;
    } else {
      prev = s.style;
      cur = s.style;
      mix = 1;
    }
  }
  const sat = (cur === 'satellite' ? mix : 0) + (prev === 'satellite' ? 1 - mix : 0);
  return { sat, vin: 1 - sat };
}

// ---------------------------------------------------------------- timing helpers

function lifeOf(el, t, inDur = 0.35, outDur = 0.25) {
  if (t < el.start || t > el.end) return null;
  const a = clamp01((t - el.start) / inDur);
  const b = el.end >= state.tl.duration - 0.01 ? 1 : clamp01((el.end - t) / outDur);
  return { in: a, out: b, age: t - el.start };
}

// ---------------------------------------------------------------- vector layer

function drawVector(t, proj, view, mix) {
  const ctx = $('vector').getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, W, H);
  const path = geoPath(proj, ctx);
  const detailed = view.k > state.baseK * 5;
  const geo = state.geo;
  const box = viewBox(proj, view);
  state.box = box;
  const land = culled(detailed ? geo.cull.land10 : geo.cull.land50, box, 'MultiPolygon');
  const borders = culled(detailed ? geo.cull.borders10 : geo.cull.borders50, box, 'MultiLineString');
  const V = state.tl.config.vintage;

  if (mix.vin > 0.001) {
    ctx.globalAlpha = mix.vin;
    ctx.fillStyle = V.sea;
    if (view.mode === 'globe') {
      ctx.beginPath();
      path({ type: 'Sphere' });
      ctx.fill();
    } else ctx.fillRect(0, 0, W, H);
    // "water lines" around coasts like old maps
    ctx.save();
    ctx.beginPath();
    path(land);
    ctx.strokeStyle = V.coastGlow;
    ctx.lineWidth = 22;
    ctx.globalAlpha = mix.vin * 0.35;
    ctx.stroke();
    ctx.lineWidth = 9;
    ctx.globalAlpha = mix.vin * 0.5;
    ctx.stroke();
    ctx.restore();
    ctx.globalAlpha = mix.vin;
    ctx.beginPath();
    path(land);
    ctx.fillStyle = V.land;
    ctx.fill();
    ctx.strokeStyle = V.coast;
    ctx.lineWidth = 1.6;
    ctx.stroke();
    ctx.beginPath();
    path(borders);
    ctx.setLineDash([6, 5]);
    ctx.strokeStyle = V.border;
    ctx.lineWidth = 1.4;
    ctx.stroke();
    ctx.setLineDash([]);
  }
  if (mix.sat > 0.001) {
    ctx.globalAlpha = mix.sat * state.tl.config.satellite.borderAlpha;
    ctx.beginPath();
    path(borders);
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.3;
    ctx.stroke();
  }
  ctx.globalAlpha = 1;

  // highlights
  for (const el of state.tl.elements) {
    if (el.type !== 'highlight') continue;
    const life = lifeOf(el, t, 0.45, 0.3);
    if (!life) continue;
    drawHighlight(ctx, path, el, life, mix);
  }
}

function drawHighlight(ctx, path, el, life, mix) {
  const feats = state.box
    ? [{ type: 'Feature', geometry: culled(state.targetIdx[el.target], state.box, 'MultiPolygon') }]
    : state.targets[el.target];
  if (state.box && !feats[0].geometry.coordinates.length) return;
  const alpha = ease.outCubic(life.in) * life.out * (el.opacity ?? 1);
  if (alpha <= 0) return;
  const fc = { type: 'FeatureCollection', features: feats };
  const satLook = mix.sat >= 0.5;
  const strokeColor = el.stroke ?? (satLook ? '#ffffff' : 'rgba(70,45,20,0.75)');
  const strokeW = el.strokeWidth ?? (satLook ? 3 : 2);

  // outer stroke (+glow): stroke at 2x then cover the inner half with the fill
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.beginPath();
  path(fc);
  if (satLook && el.glow !== false) {
    ctx.shadowColor = el.glowColor ?? 'rgba(255,255,255,0.9)';
    ctx.shadowBlur = 18;
  }
  ctx.strokeStyle = strokeColor;
  ctx.lineJoin = 'round';
  ctx.lineWidth = strokeW * 2;
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.globalAlpha = alpha * (el.fillOpacity ?? 0.92);
  ctx.beginPath();
  path(fc);
  if (el.fill && el.fill.startsWith('flag:')) {
    ctx.clip();
    const img = state.flagCanvas[flagUrl(el.fill.slice(5))];
    const b = geoPath(state.proj).bounds(fc);
    const bw = b[1][0] - b[0][0], bh = b[1][1] - b[0][1];
    const s = Math.max(bw / img.width, bh / img.height);
    const dw = img.width * s, dh = img.height * s;
    ctx.drawImage(img, b[0][0] + (bw - dw) / 2, b[0][1] + (bh - dh) / 2, dw, dh);
    // subtle shading so the flag reads as "on the map"
    ctx.fillStyle = 'rgba(0,0,0,0.08)';
    ctx.fillRect(b[0][0], b[0][1], bw, bh);
  } else {
    ctx.fillStyle = el.fill || '#f07a1a';
    ctx.fill();
    if (el.pattern === 'hatch') {
      ctx.clip();
      ctx.strokeStyle = 'rgba(255,255,255,0.25)';
      ctx.lineWidth = 3;
      for (let x = -H; x < W + H; x += 16) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x + H, H);
        ctx.stroke();
      }
    }
  }
  ctx.restore();
}

// ---------------------------------------------------------------- marks (arrows, lines, rings)

function project(pt) {
  const p = state.proj([pt.lon, pt.lat]);
  if (!p) return null;
  if (state.view.mode === 'globe') {
    const d = geoDistance([pt.lon, pt.lat], [state.view.lon, state.view.lat]);
    if (d > Math.PI / 2 - 0.02) return null;
  }
  return p;
}

function drawMarks(t) {
  const ctx = $('marks').getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, W, H);
  for (const el of state.tl.elements) {
    if (el.type !== 'arrow' && el.type !== 'line' && el.type !== 'ring') continue;
    const life = lifeOf(el, t, el.type === 'ring' ? 0.5 : 0.8, 0.25);
    if (!life) continue;
    if (el.type === 'ring') drawRing(ctx, el, life);
    else drawArrowOrLine(ctx, el, life);
  }
}

function drawRing(ctx, el, life) {
  const p = project(el);
  if (!p) return;
  const prog = ease.outCubic(life.in);
  const rx = el.r ?? 90, ry = (el.r ?? 90) * (el.squash ?? 0.85);
  ctx.save();
  ctx.globalAlpha = life.out;
  ctx.strokeStyle = el.color || '#ffd60a';
  ctx.lineWidth = el.width || 7;
  ctx.lineCap = 'round';
  ctx.shadowColor = 'rgba(0,0,0,0.45)';
  ctx.shadowBlur = 8;
  ctx.beginPath();
  const a0 = -Math.PI * 0.6;
  const a1 = a0 + Math.PI * 2.15 * prog;
  for (let a = a0; a <= a1; a += 0.04) {
    const wob = 1 + 0.035 * Math.sin(a * 3 + 1);
    const x = p[0] + (el.dx || 0) + Math.cos(a) * rx * wob;
    const y = p[1] + (el.dy || 0) + Math.sin(a) * ry * wob * (1 + (a - a0) * 0.012);
    if (a === a0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.restore();
}

function drawArrowOrLine(ctx, el, life) {
  const a = project(el.from), b = project(el.to);
  if (!a || !b) return;
  const prog = el.type === 'arrow' ? ease.inOutCubic(life.in) : ease.outCubic(life.in);
  const dx = b[0] - a[0], dy = b[1] - a[1];
  const len = Math.hypot(dx, dy);
  const curve = el.curve ?? (el.type === 'arrow' ? 0.25 : 0);
  const mx = (a[0] + b[0]) / 2 - (dy / len) * len * curve;
  const my = (a[1] + b[1]) / 2 + (dx / len) * len * curve;
  const pt = (u) => [
    (1 - u) * (1 - u) * a[0] + 2 * u * (1 - u) * mx + u * u * b[0],
    (1 - u) * (1 - u) * a[1] + 2 * u * (1 - u) * my + u * u * b[1],
  ];
  const color = el.color || (el.type === 'arrow' ? '#ffffff' : '#ffffff');
  const width = el.width || (el.type === 'arrow' ? 12 : 5);
  ctx.save();
  ctx.globalAlpha = life.out;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  if (el.dashed || el.type === 'line') ctx.setLineDash(el.dash || [16, 12]);
  const steps = 60;
  const tip = pt(prog);
  const trace = () => {
    ctx.beginPath();
    for (let i = 0; i <= steps; i++) {
      const u = (i / steps) * prog;
      const q = pt(u);
      if (i === 0) ctx.moveTo(q[0], q[1]);
      else ctx.lineTo(q[0], q[1]);
    }
  };
  trace();
  ctx.strokeStyle = 'rgba(0,0,0,0.45)';
  ctx.lineWidth = width + 6;
  ctx.stroke();
  trace();
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.stroke();
  ctx.setLineDash([]);
  if (el.type === 'arrow' && prog > 0.05) {
    const back = pt(Math.max(0, prog - 0.04));
    const ang = Math.atan2(tip[1] - back[1], tip[0] - back[0]);
    const s = width * 2.6;
    ctx.beginPath();
    ctx.moveTo(tip[0] + Math.cos(ang) * s * 0.6, tip[1] + Math.sin(ang) * s * 0.6);
    ctx.lineTo(tip[0] + Math.cos(ang + 2.4) * s, tip[1] + Math.sin(ang + 2.4) * s);
    ctx.lineTo(tip[0] + Math.cos(ang - 2.4) * s, tip[1] + Math.sin(ang - 2.4) * s);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.strokeStyle = 'rgba(0,0,0,0.45)';
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.fill();
  }
  if (el.type === 'line') {
    for (const q of [a, prog >= 0.999 ? b : null]) {
      if (!q) continue;
      ctx.beginPath();
      ctx.arc(q[0], q[1], width * 1.6, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
    }
  }
  ctx.restore();
  el._mid = pt(0.5);
}

// ---------------------------------------------------------------- DOM ui

function buildUi() {
  const ui = $('ui');
  ui.innerHTML = '';
  for (const el of state.tl.elements) {
    let html = null;
    switch (el.type) {
      case 'label':
        html = `<div class="inner label ${el.style || ''}" style="font-size:${el.size || 44}px">${el.dot ? '<span class="dot"></span>' : ''}${esc(el.text)}</div>`;
        break;
      case 'flag': {
        const w = el.size || 150;
        html = `<div class="inner flag">${el.pin ? `<div class="pole" style="height:${w * 0.95}px;left:-3px;top:${-w * 0.95}px"></div>` : ''}<img src="${flagUrl(el.code)}" style="width:${w}px;height:${w * 0.75}px;${el.pin ? `position:absolute;left:0;top:${-w * 0.95}px` : ''}"></div>`;
        break;
      }
      case 'icon':
        html = `<div class="inner icon"><img src="${el.src}" style="width:${el.size || 110}px;height:${el.size || 110}px"></div>`;
        break;
      case 'badge':
        html = `<div class="inner badge" style="background:${el.color || '#2b6be0'}">${esc(el.text)}</div>`;
        break;
      case 'question':
        html = `<div class="inner question">${[0, 1, 2].map((i) => `<span class="q" style="position:absolute;font-size:${[110, 150, 120][i]}px">?</span>`).join('')}</div>`;
        break;
      case 'year':
        html = `<div class="inner year ${el.light ? 'light' : ''}" style="font-size:${el.size || 210}px"></div>`;
        break;
      case 'stamp':
        html = `<div class="inner stamp" style="font-size:${el.size || 90}px">${esc(el.text)}</div>`;
        break;
      case 'stat':
        html = `<div class="inner stat"><div class="v" style="font-size:${el.size || 150}px"></div>${el.caption ? `<div class="c">${esc(el.caption)}</div>` : ''}</div>`;
        break;
      case 'title':
        html = `<div class="inner title" style="font-size:${el.size || 72}px;width:${W - 140}px">${esc(el.text)}</div>`;
        break;
      default:
        continue;
    }
    const d = document.createElement('div');
    d.className = 'el';
    d.style.opacity = '0';
    d.innerHTML = html;
    ui.appendChild(d);
    el._node = d;
    el._inner = d.firstElementChild;
  }
  const cap = $('captions');
  cap.innerHTML = '';
  const C = state.tl.config.captions;
  for (const c of state.tl.captions) {
    const d = document.createElement('div');
    d.className = 'cap';
    Object.assign(d.style, {
      top: `${H * C.y}px`,
      fontSize: `${C.size}px`,
      fontWeight: C.weight,
      textShadow: C.shadow,
      webkitTextStroke: C.stroke,
      paintOrder: 'stroke fill',
      display: 'none',
      textTransform: C.uppercase ? 'uppercase' : 'none',
    });
    d.textContent = c.text;
    cap.appendChild(d);
    c._node = d;
  }
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
}

function clampToSafe(x, y, w, h) {
  const s = state.tl.config.safe;
  const x0 = W * s.left + w / 2, x1 = W * (1 - s.right) - w / 2;
  const y0 = H * s.top + h / 2, y1 = H * (1 - s.bottom) - h / 2;
  return [Math.min(Math.max(x, x0), Math.max(x0, x1)), Math.min(Math.max(y, y0), Math.max(y0, y1))];
}

function updateUi(t) {
  for (const el of state.tl.elements) {
    if (!el._node) continue;
    const life = lifeOf(el, t, 0.35, 0.25);
    const node = el._node;
    if (!life) {
      node.style.opacity = '0';
      continue;
    }
    let x, y;
    if (el.screen) {
      x = W * el.screen[0];
      y = H * el.screen[1];
    } else if (el.lat != null) {
      const p = project(el);
      if (!p) {
        node.style.opacity = '0';
        continue;
      }
      // anchor scrolled off the visible map: hide instead of pinning it to an edge
      const sb = state.tl.config.safe.bottom;
      if (p[0] < -40 || p[0] > W + 40 || p[1] < -40 || p[1] > H * (1 - sb)) {
        node.style.opacity = '0';
        continue;
      }
      x = p[0] + (el.dx || 0);
      y = p[1] + (el.dy || 0);
    } else if (el.type === 'label' && el.anchor === 'lineMid' && el._line?._mid) {
      x = el._line._mid[0] + (el.dx || 0);
      y = el._line._mid[1] + (el.dy || 0);
    } else {
      x = W / 2;
      y = H * 0.2;
    }
    const inner = el._inner;
    // update text content first so the measured size matches this frame
    if (el.type === 'year') {
      const txt = String(el.value);
      const n = Math.max(1, Math.round(txt.length * clamp01(life.age / 0.45)));
      inner.textContent = el.typewriter === false ? txt : txt.slice(0, n);
    } else if (el.type === 'stat') {
      inner.querySelector('.v').textContent = countUp(el.value, clamp01(life.age / 0.9));
    }
    const w = inner.offsetWidth, h = inner.offsetHeight;
    if (el.type !== 'flag' || !el.pin) [x, y] = clampToSafe(x, y, w, h);
    let scale = 1;
    let opacity = life.out;
    let rot = el.rotate || 0;
    switch (el.type) {
      case 'year':
        opacity *= clamp01(life.age / 0.15);
        break;
      case 'stat': {
        scale = 0.6 + 0.4 * ease.outBack(life.in);
        break;
      }
      case 'stamp':
        scale = 2.2 - 1.2 * ease.outCubic(clamp01(life.age / 0.22));
        opacity *= clamp01(life.age / 0.1);
        rot = el.rotate ?? -8;
        break;
      case 'question': {
        const qs = inner.querySelectorAll('.q');
        const pos = [[-110, -20], [-10, -90], [100, -10]];
        qs.forEach((q, i) => {
          const u = ease.outBack(clamp01((life.age - i * 0.12) / 0.3));
          const wob = Math.sin(life.age * 5 + i * 2) * 8;
          q.style.transform = `translate(${pos[i][0]}px, ${pos[i][1]}px) translate(-50%,-50%) scale(${u}) rotate(${wob + (i - 1) * 12}deg)`;
        });
        break;
      }
      default:
        scale = ease.outBack(life.in);
    }
    if (el.type === 'flag' && el.pin) {
      node.style.transform = `translate(${x}px, ${y}px)`;
      inner.style.transform = `scale(${scale})`;
      inner.style.transformOrigin = '0 0';
    } else {
      node.style.transform = `translate(${x - w / 2}px, ${y - h / 2}px)`;
      inner.style.transform = `scale(${scale}) rotate(${rot}deg)`;
    }
    node.style.opacity = String(opacity);
  }
}

function countUp(value, u) {
  const m = String(value).match(/^([^0-9]*)([0-9][0-9,]*\.?[0-9]*)(.*)$/);
  if (!m || u >= 1) return String(value);
  const num = parseFloat(m[2].replace(/,/g, ''));
  const dec = (m[2].split('.')[1] || '').length;
  const cur = num * ease.outCubic(u);
  let s = cur.toFixed(dec);
  if (m[2].includes(',')) s = Number(s).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  return m[1] + s + m[3];
}

function updateCaptions(t) {
  for (const c of state.tl.captions) {
    const on = t >= c.start && t < c.end;
    c._node.style.display = on ? 'block' : 'none';
    if (on) {
      const u = clamp01((t - c.start) / 0.09);
      c._node.style.transform = `scale(${0.92 + 0.08 * u})`;
      c._node.style.opacity = String(0.4 + 0.6 * u);
    }
  }
}

// ---------------------------------------------------------------- fx

function updateFx(t) {
  const fx = $('fx');
  let html = '';
  let blur = 0;
  for (const s of state.tl.scenes) {
    const tr = s.transition;
    if (!tr) continue;
    const d = t - s.start;
    if (tr === 'film' && d > -0.35 && d < 0.45) {
      const u = (d + 0.35) / 0.8;
      const a = Math.sin(Math.PI * u);
      const off = (t * 900) % 90;
      html += `<div class="film" style="opacity:${a}"><div class="strip" style="left:0;background-position:center ${off}px"></div><div class="strip" style="right:0;background-position:center ${off}px"></div></div>`;
      blur = Math.max(blur, 10 * a);
    } else if (tr === 'flash' && d > -0.05 && d < 0.3) {
      html += `<div class="flash" style="opacity:${0.85 * (1 - clamp01((d + 0.05) / 0.35))}"></div>`;
    } else if (tr === 'fade' && d > -0.3 && d < 0.3) {
      html += `<div class="black" style="opacity:${1 - Math.abs(d) / 0.3}"></div>`;
    }
  }
  for (const el of state.tl.elements) {
    if (el.type === 'stamp' || el.vignette) {
      const life = lifeOf(el, t, 0.2, 0.25);
      if (life) html += `<div class="vignette" style="opacity:${life.in * life.out}"></div>`;
    }
  }
  fx.innerHTML = html;
  const f = blur > 0.2 ? `blur(${blur}px)` : 'none';
  for (const id of ['raster', 'vector', 'marks']) $(id).style.filter = f;
}

// ---------------------------------------------------------------- frame

function frame(t) {
  const cam = state.camera.at(t);
  const view = viewFor(cam, state.mode);
  state.view = view;
  state.proj = makeProjection(view);
  const mix = styleAt(t);
  const texelsPerPx = state.raster.base.w / (2 * Math.PI) / view.k;
  const detailMix = clamp01((1.2 - texelsPerPx) / 0.9);
  state.raster.draw(view, { alpha: mix.sat, atmo: state.mode === 'globe' ? 1 : 0, detailMix: state.raster.details.length ? Math.max(detailMix, 0) : 0 });
  $('space').style.display = state.mode === 'globe' ? 'block' : 'none';
  $('paper').style.display = mix.vin > 0.001 ? 'block' : 'none';
  $('paper').style.opacity = String(mix.vin * state.tl.config.vintage.paper);
  drawVector(t, state.proj, view, mix);
  drawMarks(t);
  updateUi(t);
  updateCaptions(t);
  updateFx(t);
  return true;
}

window.GG = { init, frame };
