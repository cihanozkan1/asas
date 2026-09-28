// Frame renderer. Everything on screen is a pure function of time t, so headless
// Chrome can step through frames deterministically: GG.init(timeline) then GG.frame(t).
import { geoPath, geoBounds, geoContains, geoCentroid, geoDistance, geoCircle, geoArea, geoInterpolate, geoRotation, geoGraticule10, geoEquirectangular } from 'd3-geo';
import { feature as topoFeature, mesh as topoMesh } from 'topojson-client';
import { Raster } from './raster.js';
import { CameraPath, makeProjection, ease, clamp01 } from './camera.js';
import { characterSvg, shipSvg } from './sprites.js';

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
    // First feature wins: world-atlas lists the country before territories that share its id
    // (e.g. 036 Australia, then Ashmore and Cartier Is.).
    byId: f10.reduce((m, f) => (f.id && !m.has(f.id) ? m.set(f.id, f) : m), new Map()),
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
  if (!n) return null;
  const out = [r / n, g / n, b / n];
  out.n = n;
  return out;
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
  const cx = (w + e) / 2;
  for (const poly of land.geometry.coordinates) {
    for (const ring of poly) {
      // Unwrap longitudes so rings crossing the antimeridian (Chukotka, Fiji...) stay continuous,
      // then shift the ring by a multiple of 360 so it lands next to this bbox.
      let prev = null;
      const pts = ring.map(([lon, lat]) => {
        if (prev != null) lon += Math.round((prev - lon) / 360) * 360;
        prev = lon;
        return [lon, lat];
      });
      let lo = Infinity, hi = -Infinity;
      for (const [lon] of pts) { lo = Math.min(lo, lon); hi = Math.max(hi, lon); }
      const shift = Math.round((cx - (lo + hi) / 2) / 360) * 360;
      if (hi + shift < w - 1 || lo + shift > e + 1) continue;
      pts.forEach(([lon, lat], i) => {
        const x = (lon + shift - w) * sx, y = (n - lat) * sy;
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
  // Skip the match when the land covers only a handful of base pixels (small islands):
  // the base's "land" there is mostly smeared sea colour and would tint the land blue.
  const closeUp = ((e - w) / 360) * BW < 200;
  const a = meanRgb(ctx, c.width, c.height);
  const landBasePx = a ? (a.n / ((c.width * c.height) / 4)) * (((e - w) / 360) * BW) * (((n - s) / 180) * BH) : 0;
  const b = landBasePx < 60 ? null : meanRgb(bx, c.width, c.height);
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
  // Close-up boxes: the 8k base has a smeared coastline at this scale, so fill the water with
  // the base's mean sea colour instead (sharp coast from the land polygons). Wide boxes keep
  // the base's own ocean shading.
  if (closeUp) {
    const wc = document.createElement('canvas');
    wc.width = c.width;
    wc.height = c.height;
    const wx = wc.getContext('2d');
    wx.drawImage(base, ((w + 180) / 360) * BW, ((90 - n) / 180) * BH, ((e - w) / 360) * BW, ((n - s) / 180) * BH, 0, 0, c.width, c.height);
    wx.globalCompositeOperation = 'destination-out';
    wx.drawImage(m, 0, 0);
    const sea = meanRgb(wx, c.width, c.height);
    if (sea) {
      ctx.globalCompositeOperation = 'destination-over';
      ctx.fillStyle = `rgb(${sea.map((v) => Math.round(v)).join(',')})`;
      ctx.fillRect(0, 0, c.width, c.height);
      ctx.globalCompositeOperation = 'source-over';
    }
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

// Random points inside a target (deterministic), spread apart a little.
// Evenly spread points inside the target: a regular grid of candidates, then farthest-point
// sampling so icons form a tidy, balanced pattern instead of random clumps.
// `along` ([[lat,lon],...]) instead places them at equal steps along a path (a row / a wall).
function scatterPoints(feats, n, seed, _minDist, minLat = -90, maxLat = 90, along = null, landOnly = false) {
  if (along && along.length > 1) {
    const P = along.map(([la, lo]) => [lo, la]);
    const seg = [0];
    for (let i = 1; i < P.length; i++) seg.push(seg[i - 1] + geoDistance(P[i - 1], P[i]));
    const tot = seg[seg.length - 1] || 1;
    const out = [];
    for (let k = 0; k < n; k++) {
      const d = n === 1 ? tot / 2 : (tot * k) / (n - 1);
      let i = 1;
      while (i < seg.length - 1 && seg[i] < d) i++;
      const f = (d - seg[i - 1]) / ((seg[i] - seg[i - 1]) || 1);
      out.push(geoInterpolate(P[i - 1], P[i])(f));
    }
    return out;
  }
  const fc = { type: 'FeatureCollection', features: feats };
  let [[w, s], [e, nn]] = geoBounds(fc);
  s = Math.max(s, minLat);
  nn = Math.min(nn, maxLat);
  const span = e >= w ? e - w : e + 360 - w;
  // houses, trees, people... must stand on land, not in the sea next to a small island
  let onLand = () => true;
  if (landOnly && state.geo?.cull?.land10) {
    const parts = state.geo.cull.land10.filter(({ box }) => box[2] >= w - 1 && box[0] <= w + span + 1 && box[3] >= s - 1 && box[1] <= nn + 1);
    const lf = { type: 'Feature', geometry: { type: 'MultiPolygon', coordinates: parts.map((x) => x.part) } };
    onLand = (p) => parts.length > 0 && geoContains(lf, p);
  }
  const cands = [];
  for (let g = 24; g <= 96 && cands.length < n * 6; g += 12) {
    cands.length = 0;
    const step = Math.max(span, nn - s) / g;
    for (let row = 0, lat = s + step / 2; lat < nn; lat += step * 0.866, row++) {
      for (let lon = w + (row % 2 ? step : step / 2); lon < w + span; lon += step) {
        const p = [lon > 180 ? lon - 360 : lon, lat];
        if (feats.some((f) => geoContains(f, p)) && onLand(p)) cands.push(p);
      }
    }
  }
  if (!cands.length) return [];
  // start near the centroid, then keep adding the candidate farthest from all chosen ones
  const cx = cands.reduce((a, p) => a + p[0], 0) / cands.length, cy = cands.reduce((a, p) => a + p[1], 0) / cands.length;
  let first = cands[0], bd = Infinity;
  for (const p of cands) { const d = Math.hypot(p[0] - cx, p[1] - cy); if (d < bd) { bd = d; first = p; } }
  const out = [first];
  const dmin = cands.map((p) => Math.hypot(p[0] - first[0], p[1] - first[1]));
  while (out.length < Math.min(n, cands.length)) {
    let k = 0;
    for (let i = 1; i < cands.length; i++) if (dmin[i] > dmin[k]) k = i;
    if (dmin[k] <= 0) break;
    out.push(cands[k]);
    for (let i = 0; i < cands.length; i++) dmin[i] = Math.min(dmin[i], Math.hypot(cands[i][0] - cands[k][0], cands[i][1] - cands[k][1]));
  }
  return out;
}

// [[lat,lon],...] -> dense [lon,lat] great-circle polyline
function catmullRom(points, steps = 10) {
  if (points.length < 3) return points;
  const P = points.map((p) => [p.lon, p.lat]);
  const out = [];
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(P.length - 1, i + 2)];
    for (let k = 0; k < steps; k++) {
      const t = k / steps, t2 = t * t, t3 = t2 * t;
      const f = (a, b, c, d) => 0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3);
      out.push({ lon: f(p0[0], p1[0], p2[0], p3[0]), lat: f(p0[1], p1[1], p2[1], p3[1]) });
    }
  }
  out.push(points[points.length - 1]);
  return out;
}

function densify(points, rhumb = false) {
  const out = [];
  for (let i = 0; i < points.length - 1; i++) {
    const a = [points[i].lon, points[i].lat], b = [points[i + 1].lon, points[i + 1].lat];
    // rhumb: straight in lon/lat (e.g. a line along a parallel or meridian)
    const f = rhumb ? (u) => [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u] : geoInterpolate(a, b);
    const n = Math.max(2, Math.ceil(geoDistance(a, b) / 0.01));
    for (let k = 0; k < n; k++) out.push(f(k / n));
  }
  const last = points[points.length - 1];
  out.push([last.lon, last.lat]);
  return out;
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
    angle: (cam.bearing || 0) + (state.tl.config.camera.sway || 0) * Math.sin((state.t || 0) * 0.35),
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
  tl.elements.forEach((e, i) => { e._i = i; });
  state.bursts = [];
  $('stage').className = `kit-${tl.kit?.kit || 'classic'}`;
  $('stage').style.setProperty('--kit', tl.kit?.accent || '#ffd60a');
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
  // borders of the past, one set per year used by the history scenes
  state.hist = {};
  for (const [y, url] of Object.entries(tl.assets.hist || {})) state.hist[y] = await loadJson(url);

  state.raster = new Raster($('raster'));
  const rs = cfg.video.rasterScale;
  state.raster.setScale(W, H, rs === 'auto' || rs == null ? (state.raster.software ? 0.6 : 1) : rs);
  state.raster.setBase(earth);
  state.raster.noGrade = /night/.test(tl.assets.earth);
  // land mask for the sea colour (open ocean never picks up JPEG blocks from the base image)
  {
    const lc = document.createElement('canvas');
    lc.width = 4096; lc.height = 2048;
    const lx = lc.getContext('2d');
    lx.fillStyle = '#000'; lx.fillRect(0, 0, lc.width, lc.height);
    const eq = geoEquirectangular().scale(lc.width / (2 * Math.PI)).translate([lc.width / 2, lc.height / 2]);
    lx.fillStyle = '#fff';
    lx.beginPath(); geoPath(eq, lx)(state.geo.land50); lx.fill();
    lx.fillRect(0, eq([0, -60])[1], lc.width, lc.height); // Antarctica is not in land50 here: leave it to colour detection
    state.raster.setLand(lc);
  }
  for (const d of tl.assets.detail || []) state.raster.addDetail(d.mask === false ? await loadImg(d.url) : landMasked(await loadImg(d.url), d.bbox, state.geo.land10, earth), d.bbox);

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
    let best = null, bestA = -1;
    for (const p of polys) {
      const a = geoArea({ type: 'Polygon', coordinates: p });
      if (a < 2 * Math.PI && a > bestA) { bestA = a; best = p; }
    }
    state.targetMain = state.targetMain || {};
    state.targetMain[key] = best ? { type: 'Feature', geometry: { type: 'Polygon', coordinates: best } } : null;
  }

  // per-element geometry
  for (const el of tl.elements) {
    if (el.type === 'scatter') el._pts = scatterPoints(state.targets[el.target] || [], el.count || 12, el.seed || 7, el.minDist ?? 0.25, el.minLat ?? -90, el.maxLat ?? 90, el.along, el.water ? false : !WATER_ICONS.test(el.icon || ''));
    if (el.type === 'ghost') {
      el._fc = { type: 'FeatureCollection', features: state.targets[el.target] };
      el._c = geoCentroid(el._fc);
    }
    if (el.type === 'route' || el.type === 'measure') {
      const pts = el.type === 'route' && el.smooth !== false && !el.rhumb ? catmullRom(el.points) : el.points || [el.from, el.to];
      el._pts = densify(pts, el.rhumb);
      el._cum = [0];
      for (let i = 1; i < el._pts.length; i++) el._cum.push(el._cum[i - 1] + geoDistance(el._pts[i - 1], el._pts[i]));
    }
  }

  // images for flags / icons
  state.images = {};
  const wanted = new Set();
  for (const el of tl.elements) {
    if (el.fill && el.fill.startsWith('flag:')) wanted.add(flagUrl(el.fill.slice(5)));
    if (el.type === 'flag') wanted.add(flagUrl(el.code));
    if (el.src) wanted.add(el.src);
    if (el.mover?.src) wanted.add(el.mover.src);
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
      target.bearing = s.camera.bearing ?? 0;
    }
    return { start: s.start, end: s.end, target, duration: s.cameraDuration, lead: s.cameraLead };
  });
  const first = shots.find((s) => s.target)?.target || { lat: 20, lon: 0, zoom: 1 };
  const intro = tl.intro || {};
  // default fly-in offset shrinks for close first shots so the opening frame stays on the subject
  const introK = mode === 'globe' ? 1 : Math.min(1, 2 / Math.max(first.zoom, 0.1));
  const introCam = {
    lat: first.lat + (intro.dLat ?? (mode === 'globe' ? -8 : -4 * introK)),
    lon: first.lon + (intro.dLon ?? (mode === 'globe' ? 40 : 18 * introK)),
    zoom: intro.zoom ?? (mode === 'globe' ? 0.95 : Math.max(0.9, first.zoom * 0.6)),
  };
  if (mode === 'flat') {
    // don't zoom out so far that the Mercator poles (Antarctica band) fill the frame
    const my = (lat) => Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI) / 360));
    const cy = H * cfg.layout.mapCenterY;
    const kMin = Math.max((H - cy) / (my(introCam.lat) - my(-60)), cy / (my(80) - my(introCam.lat)));
    introCam.zoom = Math.max(introCam.zoom, kMin / state.baseK);
  }
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
  // layout pre-pass: for each group of elements appearing together, solve overlaps once
  state.layoutOnly = true;
  const groups = new Map();
  for (const el of tl.elements) {
    if (!el._node || !isMovable(el)) continue;
    const k = Math.round(el.start * 20) / 20;
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(el);
  }
  for (const [k, els] of [...groups].sort((a, b) => a[0] - b[0])) {
    state.layoutFor = new Set(els);
    frame(Math.max(k + 0.02, Math.min(k + 0.5, Math.min(...els.map((e) => e.end)) - 0.05)));
  }
  state.layoutFor = null;
  // characters stand on whichever side of the screen keeps them clear of labels, icons and cards
  const rectOf = (e) => {
    const op = parseFloat(e._node.style.opacity || '1');
    if (!(op > 0.3)) return null;
    const r = (e._inner || e._node).getBoundingClientRect();
    return r.width > 2 ? r : null;
  };
  const inter = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
  for (const ch of tl.elements) {
    if (ch.type !== 'character' || !ch._node || !ch.screen || ch.side === 'fixed') continue;
    const x0 = ch.screen[0];
    if (Math.abs(x0 - 0.5) < 0.08) continue;
    const ts = [];
    for (let t = ch.start + 0.4; t < ch.end - 0.1; t += 0.5) ts.push(t);
    if (!ts.length) ts.push((ch.start + ch.end) / 2);
    const cost = (x) => {
      ch.screen[0] = x;
      let c = 0;
      for (const t of ts) {
        frame(t);
        const a = rectOf(ch);
        if (!a) continue;
        for (const o of tl.elements) {
          if (o === ch || !o._node || o.type === 'route' || o.type === 'scatter' || o.type === 'measure') continue;
          const b = rectOf(o);
          if (b) c += inter(a, b);
        }
      }
      return c;
    };
    const keep = cost(x0), flip = cost(1 - x0);
    ch.screen[0] = flip < keep * 0.6 ? 1 - x0 : x0;
  }
  // an icon already on the map that a later ping would sit under makes room for it
  for (const pg of tl.elements) {
    if (pg.type !== 'ping') continue;
    frame(Math.min(pg.start + 0.1, pg.end - 0.05));
    const pp = project(pg);
    if (!pp) continue;
    for (const m of tl.elements) {
      if (m.type !== 'icon' || !m._node || m.start > pg.start - 0.1 || m.end < pg.start + 0.3) continue;
      const b = rectOf(m);
      if (b && pp[0] > b.left - 30 && pp[0] < b.right + 30 && pp[1] > b.top - 30 && pp[1] < b.bottom + 30) m.end = Math.max(m.start + 1.5, pg.start + 0.1);
    }
  }
  // an older map label/icon that a later card, stamp or character would cover leaves as it arrives
  const area = (r) => r.width * r.height;
  for (const ob of tl.elements) {
    if (!ob._node || isMovable(ob) || ['route', 'scatter', 'measure'].includes(ob.type)) continue;
    frame(Math.min(ob.start + 0.35, ob.end - 0.05));
    const a = rectOf(ob);
    if (!a) continue;
    for (const m of tl.elements) {
      if (m === ob || !m._node || !(isMovable(m) || (m.screen && ob.screen && m.type !== 'character' && m.type !== 'counter')) || m.start > ob.start - 0.1 || m.end < ob.start + 0.3) continue;
      const b = rectOf(m);
      if (b && inter(a, b) > 0.12 * Math.min(area(a), area(b))) m.end = Math.max(m.start + 1.5, ob.start + 0.1);
    }
  }
  state.layoutOnly = false;
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
  const w = (name) => (cur === name ? mix : 0) + (prev === name ? 1 - mix : 0);
  const pal = {};
  for (const name of Object.keys(state.tl.config.palettes || {})) pal[name] = w(name);
  return { sat: w('satellite'), vin: w('vintage'), pal };
}

// ---------------------------------------------------------------- timing helpers

const WATER_ICONS = /🚢|⛴|🛥|🚤|⛵|🐋|🐳|🐟|🐠|🦈|🛰|🌊|🧊|🐧/u;
const rgb01 = (c) => (hexRgb(c) || [51, 51, 56]).map((v) => v / 255);
const KIT_COLORS = ['#ffd60a', '#4ade80', '#5ec8ff', '#ff6b6b'];

function lifeOf(el, t, inDur = 0.35, outDur = 0.4) {
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
    const fillA = mix.vin * (1 - 0.9 * (state.vinClose || 0));
    ctx.globalAlpha = fillA;
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
    ctx.globalAlpha = mix.vin * 0.35 * (1 - (state.vinClose || 0));
    ctx.stroke();
    ctx.lineWidth = 9;
    ctx.globalAlpha = mix.vin * 0.5 * (1 - (state.vinClose || 0));
    ctx.stroke();
    ctx.restore();
    ctx.globalAlpha = fillA;
    ctx.beginPath();
    path(land);
    ctx.fillStyle = V.land;
    ctx.fill();
    ctx.globalAlpha = mix.vin * (1 - (state.vinClose || 0));
    ctx.strokeStyle = V.coast;
    ctx.lineWidth = 1.6;
    ctx.stroke();
    ctx.beginPath();
    const sceneNow = state.tl.scenes.find((sc) => t >= sc.start - 0.3 && t < sc.end) || state.tl.scenes.at(-1);
    const hb = sceneNow?.histYear && state.hist[sceneNow.histYear];
    path(hb || borders);
    ctx.setLineDash([6, 5]);
    ctx.strokeStyle = V.border;
    ctx.lineWidth = 1.4;
    ctx.stroke();
    ctx.setLineDash([]);
  }
  // flat "infographic" basemaps (dark, atlas, neon...) from config.palettes
  for (const [name, a] of Object.entries(mix.pal)) {
    if (a <= 0.001) continue;
    drawPalette(ctx, path, view, land, borders, box, state.tl.config.palettes[name], a * (1 - 0.9 * (state.palClose || 0)));
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

  // spotlight: darken everything except the given targets
  for (const el of state.tl.elements) {
    if (el.type !== 'dim') continue;
    const life = lifeOf(el, t, 0.5, 0.4);
    if (!life) continue;
    ctx.save();
    ctx.globalAlpha = (el.amount ?? 0.6) * ease.outCubic(life.in) * life.out;
    ctx.fillStyle = el.color || '#05070c';
    ctx.beginPath();
    ctx.rect(0, 0, W, H);
    for (const k of el.targets || []) path({ type: 'FeatureCollection', features: state.targets[k] });
    ctx.fill('evenodd');
    ctx.restore();
  }

  // highlights & ghosts
  for (const el of state.tl.elements) {
    if (el.type !== 'highlight' && el.type !== 'ghost') continue;
    const life = lifeOf(el, t, 0.45, 0.3);
    if (!life) continue;
    if (el.type === 'ghost') drawGhost(ctx, path, el, life, t);
    else drawHighlight(ctx, path, el, life, mix, t);
  }
}

// Flat basemap in one colour palette. Optional per-country pastel fills (political atlas look)
// and a neon glow on coasts/borders.
function drawPalette(ctx, path, view, land, borders, box, P, a) {
  ctx.save();
  ctx.globalAlpha = a;
  ctx.fillStyle = P.sea;
  if (view.mode === 'globe') {
    ctx.beginPath();
    path({ type: 'Sphere' });
    ctx.fill();
    if (P.graticule) {
      ctx.beginPath();
      path(geoGraticule10());
      ctx.strokeStyle = P.graticule;
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  } else {
    ctx.fillRect(0, 0, W, H);
    if (P.graticule) {
      ctx.beginPath();
      path(geoGraticule10());
      ctx.strokeStyle = P.graticule;
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }
  if (P.coastGlow) {
    ctx.beginPath();
    path(land);
    ctx.strokeStyle = P.coastGlow;
    ctx.lineWidth = P.glowWidth ?? 14;
    ctx.globalAlpha = a * 0.35;
    ctx.stroke();
    ctx.globalAlpha = a;
  }
  ctx.beginPath();
  path(land);
  ctx.fillStyle = P.land;
  ctx.fill();
  if (P.countries) {
    // pastel fill per country, stable colour from its id
    const feats = view.k > state.baseK * 5 ? state.geo.countries10 : state.geo.all50;
    for (const f of feats) {
      if (f._skip == null) f._skip = geoArea(f) > 2 * Math.PI || f.id === '010'; // inverted rings / Antarctica
      if (f._skip) continue;
      const b = f._bb || (f._bb = geoBounds(f));
      if (box && !(b[1][0] >= box[0] - 5 && b[0][0] <= box[2] + 5 && b[1][1] >= box[1] - 5 && b[0][1] <= box[3] + 5) && b[1][0] >= b[0][0]) continue;
      let hsh = 0;
      for (const ch of String(f.id || f.properties?.name || '')) hsh = (hsh * 31 + ch.charCodeAt(0)) >>> 0;
      ctx.beginPath();
      path(f);
      ctx.fillStyle = P.countries[hsh % P.countries.length];
      ctx.fill();
    }
  }
  if (P.coast) {
    ctx.beginPath();
    path(land);
    ctx.strokeStyle = P.coast;
    ctx.lineWidth = P.coastWidth ?? 1.6;
    ctx.stroke();
  }
  ctx.beginPath();
  path(borders);
  ctx.strokeStyle = P.border;
  ctx.lineWidth = P.borderWidth ?? 1.3;
  if (P.borderGlow) {
    ctx.shadowColor = P.borderGlow;
    ctx.shadowBlur = 10;
  }
  ctx.stroke();
  ctx.restore();
}

// A country's real outline moved across the globe (rotation keeps its true size).
function drawGhost(ctx, path, el, life, t) {
  const u = ease.inOutCubic(clamp01((life.age - (el.delay ?? 0.3)) / (el.moveDur ?? 1.4)));
  const dest = geoInterpolate(el._c, [el.to.lon, el.to.lat])(u);
  const r1 = geoRotation([-el._c[0], -el._c[1]]);
  const r2 = geoRotation([-dest[0], -dest[1]]);
  const mv = (c) => r2.invert(r1(c));
  const mapGeom = (g) => {
    if (g.type === 'Polygon') return { type: 'Polygon', coordinates: g.coordinates.map((ring) => ring.map(mv)) };
    if (g.type === 'MultiPolygon') return { type: 'MultiPolygon', coordinates: g.coordinates.map((p) => p.map((ring) => ring.map(mv))) };
    return g;
  };
  const fc = { type: 'FeatureCollection', features: el._fc.features.map((f) => ({ type: 'Feature', geometry: mapGeom(f.geometry) })) };
  const a = ease.outCubic(life.in) * life.out;
  ctx.save();
  ctx.globalAlpha = a * (el.fillOpacity ?? 0.75);
  ctx.beginPath();
  path(fc);
  ctx.fillStyle = el.fill || '#4cc9f0';
  ctx.fill();
  ctx.globalAlpha = a;
  ctx.shadowColor = el.stroke || '#ffffff';
  ctx.shadowBlur = 14;
  ctx.strokeStyle = el.stroke || '#ffffff';
  ctx.lineWidth = 3;
  ctx.stroke();
  ctx.restore();
}

// colour states: el.morph = [{t, fill?, neon?}] (times resolved in Node); blends over 0.45s
function hexRgb(h) {
  const m = /^#?([0-9a-f]{6})$/i.exec(h || '');
  if (!m) return null;
  const n = parseInt(m[1], 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function mixColor(a, b, u) {
  const A = hexRgb(a), B = hexRgb(b);
  if (!A || !B) return u < 0.5 ? a : b;
  const c = A.map((v, i) => Math.round(v + (B[i] - v) * u));
  return '#' + c.map((v) => v.toString(16).padStart(2, '0')).join('');
}
function morphState(el, t) {
  let fill = el.fill, neon = el.neon;
  for (const m of el.morph || []) {
    if (t < m.t) break;
    const u = ease.inOutSine(clamp01((t - m.t) / 0.45));
    if (m.fill) fill = mixColor(fill, m.fill, u);
    if (m.neon) neon = mixColor(neon || m.neon, m.neon, u);
  }
  return { fill, neon };
}

// Rounded "blob" look: the shape is dilated with round joins, then rimmed with a glow.
function drawSoftBlob(ctx, path, fc, el, st, alpha, t) {
  const R = el.softness ?? 16;
  const rim = st.neon || el.rim || '#ffb703';
  const fill = st.fill && !st.fill.startsWith('flag:') ? st.fill : '#d62828';
  const pulse = 0.85 + 0.15 * Math.sin(t * 4);
  ctx.save();
  ctx.lineJoin = 'round';
  ctx.lineCap = 'round';
  ctx.globalAlpha = alpha;
  ctx.beginPath();
  path(fc);
  ctx.shadowColor = rim;
  ctx.shadowBlur = 34 * pulse;
  ctx.strokeStyle = rim;
  ctx.lineWidth = R * 2 + (el.rimWidth ?? 9) * 2;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.globalAlpha = alpha * (el.fillOpacity ?? 0.95);
  ctx.strokeStyle = fill;
  ctx.lineWidth = R * 2;
  ctx.stroke();
  ctx.fillStyle = fill;
  ctx.fill();
  // soft inner shading
  const b = geoPath(state.proj).bounds(fc);
  const g = ctx.createRadialGradient((b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2, 10, (b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2, Math.max(b[1][0] - b[0][0], b[1][1] - b[0][1]) * 0.7);
  g.addColorStop(0, 'rgba(255,255,255,0.10)');
  g.addColorStop(1, 'rgba(0,0,0,0.22)');
  ctx.fillStyle = g;
  ctx.fill();
  ctx.restore();
}

function drawHighlight(ctx, path, el, life, mix, t) {
  const idx = state.targetIdx[el.target];
  const feats = state.box && idx.length
    ? [{ type: 'Feature', geometry: culled(idx, state.box, 'MultiPolygon') }]
    : state.targets[el.target];
  if (state.box && idx.length && !feats[0].geometry.coordinates.length) return;
  const alpha = ease.outCubic(life.in) * life.out * (el.opacity ?? 1);
  if (alpha <= 0) return;
  const fc = { type: 'FeatureCollection', features: feats };
  const satLook = mix.vin < 0.5;
  const st = morphState(el, t);
  const neon = st.neon;
  if (el.soft) {
    drawSoftBlob(ctx, path, fc, el, st, alpha, t);
    return;
  }
  const strokeColor = neon || (el.stroke ?? (satLook ? '#ffffff' : 'rgba(70,45,20,0.75)'));
  const strokeW = el.strokeWidth ?? (neon ? 4 : satLook ? 3 : 2);
  ctx.save();
  if ((el.eastOf != null || el.westOf != null) && state.view.mode !== 'globe') {
    const x0 = el.eastOf != null ? state.proj([el.eastOf, state.view.lat])[0] : -10;
    const x1 = el.westOf != null ? state.proj([el.westOf, state.view.lat])[0] : W + 10;
    ctx.beginPath();
    ctx.rect(x0, -10, x1 - x0, H + 20);
    ctx.clip();
  }
  if (el.reveal) {
    // territory spreading out from a point
    const o = project(el.reveal) || [W / 2, H / 2];
    const u = ease.inOutSine(clamp01(life.age / (el.revealDur ?? 1.4)));
    ctx.beginPath();
    ctx.arc(o[0], o[1], Math.max(1, u * Math.hypot(W, H) * 1.1), 0, Math.PI * 2);
    ctx.clip();
  }

  // outer stroke (+glow): stroke at 2x then cover the inner half with the fill
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.beginPath();
  path(fc);
  if (neon) {
    const pulse = 0.75 + 0.25 * Math.sin(t * 5);
    ctx.shadowColor = neon;
    ctx.shadowBlur = 38 * pulse;
    ctx.strokeStyle = neon;
    ctx.lineWidth = strokeW * 2;
    ctx.lineJoin = 'round';
    ctx.stroke();
    ctx.shadowBlur = 14;
  } else if (satLook && el.glow !== false) {
    ctx.shadowColor = el.glowColor ?? 'rgba(255,255,255,0.9)';
    ctx.shadowBlur = 18;
  }
  ctx.strokeStyle = strokeColor;
  ctx.lineJoin = 'round';
  ctx.lineWidth = strokeW * 2;
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.globalAlpha = alpha * (el.fillOpacity ?? (neon && !el.fill ? 0.38 : 0.92));
  ctx.beginPath();
  path(fc);
  if (neon && !st.fill) {
    ctx.fillStyle = neon;
    ctx.fill();
  } else if (st.fill && st.fill.startsWith('flag:')) {
    ctx.clip();
    const img = state.flagCanvas[flagUrl(el.fill.slice(5))];
    // place the flag over the main landmass so big archipelagos don't wash it out
    const b = geoPath(state.proj).bounds(el.flagFit === 'all' || !state.targetMain[el.target] ? fc : state.targetMain[el.target]);
    const bw = b[1][0] - b[0][0], bh = b[1][1] - b[0][1];
    const s = Math.max(bw / img.width, bh / img.height);
    const dw = img.width * s, dh = img.height * s;
    ctx.drawImage(img, b[0][0] + (bw - dw) / 2, b[0][1] + (bh - dh) / 2, dw, dh);
    // subtle shading so the flag reads as "on the map"
    ctx.fillStyle = 'rgba(0,0,0,0.08)';
    ctx.fillRect(b[0][0], b[0][1], bw, bh);
  } else {
    ctx.fillStyle = st.fill || '#f07a1a';
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

// Map markers: each UI kit has its own shape, so not every video uses the same yellow dot.
const MARKER = { classic: 'ripple', block: 'pin', neon: 'diamond', paper: 'tack', news: 'bracket', outline: 'crosshair' };
function markerColor(c) {
  const kit = state.tl.kit?.accent;
  return !c || /^#ffd60a$/i.test(c) ? kit || '#ffd60a' : c;
}
function drawMarker(ctx, p, color, life, k, reach) {
  const style = state.tl.scenes && styleAt(state.time || 0).vin > 0.5 ? 'tack' : MARKER[state.tl.kit?.kit] || 'ripple';
  const inU = ease.outBack(clamp01(life.age / 0.35));
  const [x, y] = p;
  ctx.save();
  ctx.globalAlpha = life.out;
  ctx.lineJoin = 'round';
  if (style === 'ripple') {
    for (let n = 0; n < 2; n++) {
      const ph = (life.age * 0.9 + n * 0.5) % 1;
      ctx.globalAlpha = life.out * (1 - ph) * 0.8;
      ctx.strokeStyle = color; ctx.lineWidth = 4 * k;
      ctx.beginPath(); ctx.arc(x, y, (14 + ph * reach) * k, 0, Math.PI * 2); ctx.stroke();
    }
    ctx.globalAlpha = life.out;
    ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 8;
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, 12 * k * inU, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0; ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, 7.5 * k * inU, 0, Math.PI * 2); ctx.fill();
  } else if (style === 'pin') {
    const drop = (1 - ease.outCubic(clamp01(life.age / 0.35))) * 60 * k;
    const s = 30 * k;
    ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.beginPath(); ctx.ellipse(x, y, 10 * k, 4 * k, 0, 0, Math.PI * 2); ctx.fill();
    ctx.translate(x, y - drop);
    ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 8; ctx.shadowOffsetY = 3;
    ctx.fillStyle = color; ctx.strokeStyle = '#111'; ctx.lineWidth = 3 * k;
    ctx.beginPath(); ctx.moveTo(0, 0);
    ctx.bezierCurveTo(-s * 0.2, -s * 0.6, -s * 0.62, -s * 0.9, -s * 0.62, -s * 1.3);
    ctx.arc(0, -s * 1.3, s * 0.62, Math.PI, 0);
    ctx.bezierCurveTo(s * 0.62, -s * 0.9, s * 0.2, -s * 0.6, 0, 0);
    ctx.fill(); ctx.shadowBlur = 0; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(0, -s * 1.3, s * 0.25, 0, Math.PI * 2); ctx.fill();
  } else if (style === 'diamond') {
    const ph = (life.age * 1.1) % 1;
    ctx.strokeStyle = color; ctx.lineWidth = 3 * k; ctx.shadowColor = color; ctx.shadowBlur = 18;
    const r0 = (16 + ph * reach * 0.8) * k;
    ctx.globalAlpha = life.out * (1 - ph);
    ctx.beginPath(); ctx.moveTo(x, y - r0); ctx.lineTo(x + r0, y); ctx.lineTo(x, y + r0); ctx.lineTo(x - r0, y); ctx.closePath(); ctx.stroke();
    ctx.globalAlpha = life.out;
    const r1 = 13 * k * inU;
    ctx.fillStyle = color; ctx.beginPath(); ctx.moveTo(x, y - r1); ctx.lineTo(x + r1, y); ctx.lineTo(x, y + r1); ctx.lineTo(x - r1, y); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, 3.5 * k, 0, Math.PI * 2); ctx.fill();
  } else if (style === 'tack') {
    const s = 22 * k * inU;
    ctx.strokeStyle = '#3b2b1a'; ctx.lineWidth = 3 * k;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + s * 0.5, y - s * 1.1); ctx.stroke();
    ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 6; ctx.shadowOffsetY = 3;
    const g = ctx.createRadialGradient(x + s * 0.4, y - s * 1.4, 1, x + s * 0.5, y - s * 1.2, s * 0.7);
    g.addColorStop(0, '#fff'); g.addColorStop(0.35, color); g.addColorStop(1, '#00000088');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x + s * 0.5, y - s * 1.2, s * 0.62, 0, Math.PI * 2); ctx.fill();
  } else if (style === 'bracket') {
    const r = (22 + 8 * Math.sin(life.age * 5)) * k * inU, L = 12 * k;
    ctx.strokeStyle = color; ctx.lineWidth = 4 * k; ctx.lineCap = 'square';
    for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
      ctx.beginPath(); ctx.moveTo(x + sx * r, y + sy * (r - L)); ctx.lineTo(x + sx * r, y + sy * r); ctx.lineTo(x + sx * (r - L), y + sy * r); ctx.stroke();
    }
    ctx.fillStyle = color; ctx.fillRect(x - 5 * k, y - 5 * k, 10 * k, 10 * k);
  } else {
    const r = 20 * k * inU, rot = life.age * 0.8;
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 3 * k; ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 6;
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.stroke();
    for (let n = 0; n < 4; n++) {
      const a = rot + (n * Math.PI) / 2;
      ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * r * 0.55, y + Math.sin(a) * r * 0.55); ctx.lineTo(x + Math.cos(a) * r * 1.45, y + Math.sin(a) * r * 1.45); ctx.stroke();
    }
    ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, 5 * k, 0, Math.PI * 2); ctx.fill();
  }
  ctx.restore();
}

function markerPoints(t) {
  const out = [];
  for (const el of state.tl.elements) {
    const isDot = el.type === 'label' && el.dot && el.lat != null;
    if (el.type !== 'ping' && !isDot) continue;
    if (t < el.start - 0.05 || t > el.end) continue;
    const p = project(el);
    if (p) out.push([p[0], p[1], isDot ? 40 : 90]);
  }
  return out;
}

function drawMarks(t) {
  state.time = t;
  const ctx = $('marks').getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, W, H);
  for (const el of state.tl.elements) {
    if (el.type !== 'ping') continue;
    const life = lifeOf(el, t, 0.3, 0.3);
    const p = life && project(el);
    if (!p) continue;
    drawMarker(ctx, p, markerColor(el.color), life, 1, el.r ?? 70);
  }
  for (const el of state.tl.elements) {
    if (el.type !== 'flag' || !el.moveTo || !el._arc) continue;
    const life = lifeOf(el, t);
    if (!life) continue;
    const [a, c, b, u] = el._arc;
    if (u <= 0.02) continue;
    ctx.save();
    ctx.globalAlpha = life.out * 0.9;
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 3.5;
    ctx.setLineDash([2, 10]);
    ctx.lineCap = 'round';
    ctx.beginPath();
    for (let i = 0; i <= 30; i++) {
      const v = (i / 30) * u;
      const x = (1 - v) * (1 - v) * a[0] + 2 * v * (1 - v) * c[0] + v * v * b[0];
      const y = (1 - v) * (1 - v) * a[1] + 2 * v * (1 - v) * c[1] + v * v * b[1];
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.stroke();
    ctx.restore();
  }
  for (const el of state.tl.elements) {
    if (el.type !== 'label' || !el.dot || el.lat == null) continue;
    const life = lifeOf(el, t, 0.3, 0.4);
    const p = life && project(el);
    if (!p) continue;
    drawMarker(ctx, p, markerColor(el.dotColor || el.color), life, 0.62, 40);
  }
  for (const el of state.tl.elements) {
    if (!['arrow', 'line', 'ring', 'route', 'measure'].includes(el.type)) continue;
    const life = lifeOf(el, t, el.type === 'ring' ? 0.5 : 0.8, 0.25);
    if (!life) {
      el._head = null;
      continue;
    }
    if (el.type === 'route') drawRoute(ctx, el, life);
    else if (el.type === 'measure') drawMeasure(ctx, el, life);
    else if (el.type === 'ring') drawRing(ctx, el, life);
    else drawArrowOrLine(ctx, el, life);
  }
}

// points behind the globe are dropped; the next visible point starts a new run (q.brk) instead of a chord
function screenPolyline(pts) {
  const out = [];
  let gap = false;
  for (const p of pts) {
    const q = project({ lon: p[0], lat: p[1] });
    if (!q) { gap = true; continue; }
    const r = [q[0], q[1]];
    if (gap && out.length) r.brk = true;
    out.push(r);
    gap = false;
  }
  return out;
}

function partial(poly, u) {
  let total = 0;
  const seg = [];
  for (let i = 1; i < poly.length; i++) {
    const d = Math.hypot(poly[i][0] - poly[i - 1][0], poly[i][1] - poly[i - 1][1]);
    seg.push(d);
    total += d;
  }
  const want = total * u;
  const out = [poly[0]];
  let acc = 0;
  let ang = 0;
  for (let i = 1; i < poly.length; i++) {
    ang = Math.atan2(poly[i][1] - poly[i - 1][1], poly[i][0] - poly[i - 1][0]);
    if (acc + seg[i - 1] >= want) {
      const f = seg[i - 1] ? (want - acc) / seg[i - 1] : 0;
      out.push([poly[i - 1][0] + (poly[i][0] - poly[i - 1][0]) * f, poly[i - 1][1] + (poly[i][1] - poly[i - 1][1]) * f]);
      return { pts: out, ang };
    }
    acc += seg[i - 1];
    out.push(poly[i]);
  }
  return { pts: out, ang };
}

function strokePoly(ctx, pts) {
  ctx.beginPath();
  pts.forEach((p, i) => (i && !p.brk ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])));
  ctx.stroke();
}

function routeProgress(el, t) {
  const dur = el.drawDur ?? Math.max(0.6, (el.end - el.start) * 0.85);
  return (el.ease === 'linear' ? (x) => x : ease.inOutSine)(clamp01((t - el.start) / dur));
}

// geo points between fractions u0..u1 of the route's length
function geoSlice(el, u0, u1) {
  const total = el._cum[el._cum.length - 1];
  const a = u0 * total, b = u1 * total;
  const at = (d) => {
    let i = 1;
    while (i < el._cum.length - 1 && el._cum[i] < d) i++;
    const seg = el._cum[i] - el._cum[i - 1] || 1;
    return geoInterpolate(el._pts[i - 1], el._pts[i])(clamp01((d - el._cum[i - 1]) / seg));
  };
  const out = [at(a)];
  for (let i = 0; i < el._pts.length; i++) if (el._cum[i] > a && el._cum[i] < b) out.push(el._pts[i]);
  out.push(at(b));
  return out;
}

function routeHeadGeo(el, t) {
  const pts = geoSlice(el, 0, Math.max(routeProgress(el, t), 1e-4));
  return pts[pts.length - 1];
}

function drawRoute(ctx, el, life) {
  const u = routeProgress(el, state.t);
  const tail = el.retract === false ? 0 : 1 - life.out; // on exit the line is wound back from its start
  const pts = screenPolyline(geoSlice(el, Math.min(tail, u), Math.max(u, 1e-4)));
  if (pts.length < 2) return;
  const n = pts.length;
  const ang = Math.atan2(pts[n - 1][1] - pts[Math.max(0, n - 4)][1], pts[n - 1][0] - pts[Math.max(0, n - 4)][0]);
  const color = el.color || '#ffd60a';
  const width = el.width || 9;
  ctx.save();
  ctx.globalAlpha = life.out;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  if (el.dashed) ctx.setLineDash(el.dash || [2, 18]);
  ctx.strokeStyle = 'rgba(0,0,0,0.45)';
  ctx.lineWidth = width + 6;
  strokePoly(ctx, pts);
  ctx.shadowColor = el.glow === false ? 'transparent' : color;
  ctx.shadowBlur = el.glow === false ? 0 : 16;
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  strokePoly(ctx, pts);
  if (el.flow) {
    // current / wind: bright dashes streaming along the line
    ctx.shadowBlur = 0;
    ctx.setLineDash(el.flowDash || [26, 38]);
    ctx.lineDashOffset = -state.t * (el.flowSpeed ?? 150);
    ctx.strokeStyle = el.flowColor || 'rgba(255,255,255,0.9)';
    ctx.lineWidth = Math.max(3, width * 0.45);
    strokePoly(ctx, pts);
  }
  ctx.restore();
  if (el.arrowHead && pts.length > 2) {
    const [hx, hy] = pts[pts.length - 1];
    const s2 = width * 2.6;
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.translate(hx, hy);
    ctx.rotate(ang);
    ctx.fillStyle = color;
    ctx.shadowColor = 'rgba(0,0,0,0.5)';
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.moveTo(s2, 0);
    ctx.lineTo(-s2 * 0.7, -s2 * 0.8);
    ctx.lineTo(-s2 * 0.35, 0);
    ctx.lineTo(-s2 * 0.7, s2 * 0.8);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }
  const head = pts[pts.length - 1];
  if (el.headDot !== false && !el.mover && u < 1) {
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.fillStyle = '#fff';
    ctx.shadowColor = color;
    ctx.shadowBlur = 18;
    ctx.beginPath();
    ctx.arc(head[0], head[1], width * 0.9, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
  el._head = { x: head[0], y: head[1], ang, u };
}

function drawMeasure(ctx, el, life) {
  const poly = screenPolyline(el._pts);
  if (poly.length < 2) return;
  const u = ease.outCubic(clamp01(life.age / 0.6));
  const a = poly[0], b = poly[poly.length - 1];
  const mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
  const half = [(b[0] - a[0]) / 2 * u, (b[1] - a[1]) / 2 * u];
  const p0 = [mid[0] - half[0], mid[1] - half[1]], p1 = [mid[0] + half[0], mid[1] + half[1]];
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
  const color = el.color || '#ffffff';
  ctx.save();
  ctx.globalAlpha = life.out;
  ctx.lineCap = 'round';
  ctx.strokeStyle = 'rgba(0,0,0,0.5)';
  ctx.lineWidth = 11;
  strokePoly(ctx, [p0, p1]);
  ctx.strokeStyle = color;
  ctx.lineWidth = 6;
  strokePoly(ctx, [p0, p1]);
  for (const [p, dir] of [[p0, ang + Math.PI], [p1, ang]]) {
    const s = 26;
    ctx.beginPath();
    ctx.moveTo(p[0] + Math.cos(dir) * 6, p[1] + Math.sin(dir) * 6);
    ctx.lineTo(p[0] + Math.cos(dir + 2.5) * s, p[1] + Math.sin(dir + 2.5) * s);
    ctx.lineTo(p[0] + Math.cos(dir - 2.5) * s, p[1] + Math.sin(dir - 2.5) * s);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
  }
  ctx.restore();
  el._head = { x: mid[0], y: mid[1], ang, u };
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
        html = `<div class="inner label ${el.style || ''} ${el.dot ? 'place' : ''} ${state.tl.scenes[el.scene]?.style === 'vintage' ? 'era-history' : ''}" style="font-size:${el.size || 44}px;${el.color ? `color:${el.color};` : ''}${el.bg ? `background:${el.bg};` : ''}${el.glow ? `text-shadow:0 0 18px ${el.glow},0 0 36px ${el.glow},0 3px 8px rgba(0,0,0,.8);` : ''}">${esc(el.text)}</div>`;
        break;
      case 'flag': {
        const w = el.size || 150;
        html = `<div class="inner flag">${el.pin ? `<div class="pole" style="height:${w * 0.95}px;left:-3px;top:${-w * 0.95}px"></div>` : ''}<img src="${flagUrl(el.code)}" style="width:${w}px;height:${w * 0.75}px;${el.pin ? `position:absolute;left:0;top:${-w * 0.95}px` : ''}"></div>`;
        break;
      }
      case 'icon':
        // icons sit on a round badge (like map markers), so they read as designed markers, not loose emoji
        html = el.plain
          ? `<div class="inner icon"><img src="${el.src}" style="width:${el.size || 110}px;height:${el.size || 110}px"></div>`
          : `<div class="inner icon badged" style="width:${(el.size || 110) * 1.25}px;height:${(el.size || 110) * 1.25}px"><img src="${el.src}" style="width:${(el.size || 110) * 0.78}px;height:${(el.size || 110) * 0.78}px"></div>`;
        break;
      case 'badge':
        html = `<div class="inner badge" style="background:${el.color || '#2b6be0'}">${esc(el.text)}</div>`;
        break;
      case 'question':
        html = `<div class="inner question" style="position:relative;width:330px;height:250px">${[0, 1, 2].map((i) => `<span class="q" style="position:absolute;left:165px;top:175px;font-size:${[110, 150, 120][i]}px">?</span>`).join('')}</div>`;
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
        // *word* marks accent words; "hook" = big condensed opening card
        html = `<div class="inner title ${el.hook ? 'hook' : ''}" style="font-size:${el.size || 72}px;width:${el.width || W - 140}px;${el.accent ? `--accent:${el.accent}` : ''}">${esc(el.text).replace(/\*([^*]+)\*/g, '<em>$1</em>').replace(/\n/g, '<br>')}</div>`;
        break;
      case 'bars': {
        // No boxed panel: stats sit on the map like the reference channels do (big numbers,
        // flag badges, a thin proportional bar), with a soft shadow pool behind for contrast.
        const max = Math.max(...el.items.map((it) => it.value));
        const badge = (it, i) => it.flag
          ? `<span class="badge-c"><img src="${flagUrl(it.flag)}"></span>`
          : it.icon ? `<span class="badge-c emo">${it.icon}</span>` : `<span class="badge-c dot" style="background:${it.color || KIT_COLORS[i % KIT_COLORS.length]}"></span>`;
        if (el.orient === 'v') {
          const hMax = el.height || 420;
          html = `<div class="inner chart-v">${el.items
            .map((it, i) => {
              const h = Math.max(10, (it.value / max) * hMax);
              const col = it.color || KIT_COLORS[i % KIT_COLORS.length];
              const shape = el.shape === 'mountain'
                ? `<svg class="shape" viewBox="0 0 200 100" preserveAspectRatio="none" style="height:${h}px"><defs><linearGradient id="mg${i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}"/><stop offset="1" stop-color="${col}" stop-opacity=".75"/></linearGradient></defs><polygon points="0,100 100,0 200,100" fill="url(#mg${i})"/><polygon points="100,0 128,28 112,24 100,36 88,24 72,28" fill="#fff" opacity=".95"/></svg>`
                : `<div class="shape col-bar" style="height:${h}px;--c:${col}">${it.icon ? `<span class="top-emo">${it.icon}</span>` : ''}</div>`;
              return `<div class="col"><div class="val" data-v="${esc(it.display ?? it.value)}"></div><div class="grow" style="height:${h}px">${shape}</div><div class="lab">${it.flag ? `<img src="${flagUrl(it.flag)}">` : ''}${esc(it.label)}</div></div>`;
            })
            .join('')}<div class="ground"></div></div>`;
        } else {
          const tw = el.trackWidth || 640;
          html = `<div class="inner chart-h">${el.items
            .map((it, i) => `<div class="row">${badge(it, i)}<div class="txt"><div class="lab">${esc(it.label)}</div><div class="val" data-v="${esc(it.display ?? it.value)}"></div><div class="track" style="width:${tw}px"><div class="bar" data-w="${Math.max(0.03, it.value / max) * tw}" style="--c:${it.color || KIT_COLORS[i % KIT_COLORS.length]};width:0"></div></div></div></div>`)
            .join('')}</div>`;
        }
        break;
      }
      case 'vs': {
        const side = (o) => `<div class="side"><img src="${o.flag ? flagUrl(o.flag) : o.src}"><div class="n">${esc(o.label || '')}</div></div>`;
        html = `<div class="inner vs">${side(el.left)}<div class="mid">VS</div>${side(el.right)}</div>`;
        break;
      }
      case 'timeline': {
        const wpx = el.width || 900;
        html = `<div class="inner timeline" style="width:${wpx}px"><div class="axis"></div>${el.events
          .map((ev, i) => `<div class="ev" style="left:${el.events.length === 1 ? 50 : 8 + (i / (el.events.length - 1)) * 84}%"><div class="y">${esc(ev.year || '')}</div><div class="dot"></div><div class="t">${esc(ev.label || '')}</div></div>`)
          .join('')}</div>`;
        break;
      }
      case 'clock': {
        const r = (el.size || 200) / 2;
        const ticks = Array.from({ length: 12 }, (_, i) => {
          const a = (i / 12) * 2 * Math.PI;
          return `<line x1="${r + Math.sin(a) * r * 0.78}" y1="${r - Math.cos(a) * r * 0.78}" x2="${r + Math.sin(a) * r * 0.9}" y2="${r - Math.cos(a) * r * 0.9}" stroke="#222" stroke-width="${i % 3 ? 3 : 6}" stroke-linecap="round"/>`;
        }).join('');
        html = `<div class="inner clock"><svg class="face" width="${2 * r}" height="${2 * r}"><circle cx="${r}" cy="${r}" r="${r - 4}" fill="${el.night ? '#1d2440' : '#fff'}" stroke="#111" stroke-width="8"/>${ticks}<line class="hh" x1="${r}" y1="${r}" x2="${r}" y2="${r * 0.48}" stroke="${el.night ? '#fff' : '#111'}" stroke-width="10" stroke-linecap="round"/><line class="mh" x1="${r}" y1="${r}" x2="${r}" y2="${r * 0.22}" stroke="${el.color || '#e63946'}" stroke-width="6" stroke-linecap="round"/><circle cx="${r}" cy="${r}" r="9" fill="#111"/></svg>${el.label ? `<div class="cl">${esc(el.label)}</div>` : ''}</div>`;
        break;
      }
      case 'character': {
        const sz = el.size || (el.image ? 390 : 300);
        const bodyHtml = el.image
          ? `<img class="body figure" src="/assets/characters/${el.image}.png" style="height:${sz}px;display:block;margin:0 auto">`
          : `<div class="body" style="width:${sz}px;height:${sz * 1.2}px">${characterSvg(el).replace('<svg', `<svg width="${sz}" height="${sz * 1.2}"`)}</div>`;
        const era = state.tl.scenes[el.scene]?.era === 'history' ? 'era-history' : '';
        html = `<div class="inner character ${el.image ? 'figure' : ''} ${era}" style="${el.image ? '' : `width:${sz}px`}">
          ${bodyHtml}
          ${el.name ? `<div class="nametag">${esc(el.name)}</div>` : ''}
          ${el.say ? `<div class="bubble ${el.think ? 'think' : ''} ${el.bubbleSide === 'left' ? 'left' : ''}"><span>${esc(el.say)}</span></div>` : ''}
        </div>`;
        break;
      }
      case 'route': {
        if (!el.mover) continue;
        const m = el.mover;
        const sz = m.size || 150;
        let inner = '';
        if (m.kind === 'ship') inner = shipSvg(m).replace('<svg', `<svg width="${sz}" height="${sz * 0.92}"`);
        else if (m.kind === 'character') inner = characterSvg(m).replace('<svg', `<svg width="${sz}" height="${sz * 1.2}"`);
        else inner = `<img src="${m.src}" style="width:${sz}px;height:${sz}px">`;
        html = `<div class="inner mover ${m.kind}"><div class="spr">${inner}</div></div>`;
        break;
      }
      case 'counter':
        html = `<div class="inner counter" style="font-size:${el.size || 170}px;color:${el.color || '#ffd60a'}"></div>`;
        break;
      case 'measure':
        html = `<div class="inner dim" style="font-size:${el.size || 44}px;--dc:${el.color || '#ffffff'}">${esc(el.label || '')}</div>`;
        break;
      case 'scatter':
        html = `<div class="inner scatter">${el._pts.map(() => `<img src="${el.src}" style="width:${el.size || 70}px;height:${el.size || 70}px">`).join('')}</div>`;
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
  cap.className = C.theme ? `theme-${C.theme}` : '';
  const noStroke = C.theme === 'box';
  for (const c of state.tl.captions) {
    const d = document.createElement('div');
    d.className = 'cap';
    Object.assign(d.style, {
      top: `${H * C.y}px`,
      fontSize: `${C.size}px`,
      fontWeight: C.weight,
      textShadow: C.shadow,
      webkitTextStroke: noStroke ? '0' : C.stroke,
      paintOrder: 'stroke fill',
      display: 'none',
      textTransform: C.uppercase ? 'uppercase' : 'none',
    });
    const kw = C.keywords || {};
    const words = c.words
      .map((w, i) => {
        const key = w.text.toLowerCase().replace(/[^a-z0-9%$]/g, '');
        const color = kw[key] || (C.numberColor && /[0-9]/.test(w.text) ? C.numberColor : null);
        return `<span class="w" data-i="${i}" style="${color ? `color:${color}` : ''}">${esc(w.text)}</span>`;
      })
      .join(' ');
    d.innerHTML = C.theme === 'box' ? `<span class="line">${words}</span>` : words;
    cap.appendChild(d);
    c._node = d;
    c._spans = [...d.querySelectorAll('.w')];
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

// ---- per-kit motion: screen cards enter differently in each UI kit
const KIT_CARDS = new Set(['counter', 'year', 'stat', 'bars', 'timeline', 'clock', 'pill']);
const BURST = new Set(['counter', 'stamp', 'stat']);
function kitEntrance(a) {
  const kit = state.tl.kit?.kit || 'classic';
  const r = { dx: 0, dy: 0, sc: 1, rot: 0, clip: null, blur: 0, op: 1 };
  if (kit === 'block') {
    const u = clamp01(a / 0.45);
    r.dy = (1 - ease.outBack(u)) * 110; r.rot = (1 - ease.outCubic(u)) * -5;
  } else if (kit === 'neon') {
    r.op = a < 0.45 ? ([1, 0.2, 1, 1, 0.35, 1, 1, 1][Math.floor(a * 18) % 8]) * clamp01(a / 0.08) : 1;
  } else if (kit === 'paper') {
    const u = clamp01(a / 0.5);
    r.sc = 0.75 + 0.25 * ease.outBack(u); r.rot = (1 - ease.outCubic(u)) * 7; r.dy = (1 - ease.outCubic(u)) * -50;
  } else if (kit === 'news') {
    const u = ease.outCubic(clamp01(a / 0.4));
    r.clip = u < 1 ? `inset(-20% ${(1 - u) * 100}% -20% -20%)` : null; r.dx = (1 - u) * -24;
  } else if (kit === 'outline') {
    const u = ease.outCubic(clamp01(a / 0.5));
    r.sc = 1.35 - 0.35 * u; r.blur = (1 - u) * 10; r.op = clamp01(u * 1.4);
  }
  return r;
}

function updateUi(t) {
  state.time = t;
  state.bursts = [];
  const placed = [];
  for (const el of state.tl.elements) {
    if (!el._node) continue;
    const life = lifeOf(el, t, 0.35, 0.25);
    const node = el._node;
    if (!life) {
      node.style.opacity = '0';
      continue;
    }
    if (el.type === 'scatter') {
      node.style.opacity = '1';
      node.style.transform = 'none';
      const imgs = el._inner.children;
      el._pts.forEach((pt, i) => {
        const q0 = project({ lon: pt[0], lat: pt[1] });
        const q = q0 && tiltPoint(q0[0], q0[1]);
        const img = imgs[i];
        const u = clamp01((life.age - i * (el.stagger ?? 0.09)) / 0.3);
        if (!q || u <= 0) {
          img.style.opacity = '0';
          return;
        }
        const sz = el.size || 70;
        // decided once, when the icon first appears: drop icons that would touch an earlier one
        el._keep = el._keep || [];
        if (el._keep[i] == null) {
          el._keep[i] = !el._pts.some((pt2, j) => {
            if (j >= i || !el._keep[j]) return false;
            const r = project({ lon: pt2[0], lat: pt2[1] });
            return r && Math.hypot(r[0] - q[0], r[1] - q[1]) < sz * 1.15;
          });
        }
        if (!el._keep[i]) { img.style.opacity = '0'; return; }
        const sc = ease.outBack(u) * (1 + 0.04 * Math.sin(t * 3 + i));
        img.style.cssText = `position:absolute;width:${sz}px;height:${sz}px;left:${q[0] - sz / 2}px;top:${q[1] - sz / 2}px;opacity:${life.out};transform:scale(${sc});filter:drop-shadow(0 4px 6px rgba(0,0,0,.5))`;
      });
      continue;
    }
    let x, y;
    if (el.type === 'route' || el.type === 'measure') {
      if (!el._head) {
        node.style.opacity = '0';
        continue;
      }
      [x, y] = tiltPoint(el._head.x, el._head.y);
      x += el.type === 'measure' ? 0 : el.mover?.dx || 0;
      y += el.type === 'measure' ? 0 : el.mover?.dy || 0;
    } else if (el.screen) {
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
      [x, y] = tiltPoint(p[0], p[1]);
      x += el.dx || 0;
      y += el.dy || 0;
    } else if (el.type === 'label' && el.anchor === 'lineMid' && el._line?._mid) {
      x = el._line._mid[0] + (el.dx || 0);
      y = el._line._mid[1] + (el.dy || 0);
    } else {
      x = W / 2;
      y = H * 0.2;
    }
    const inner = el._inner;
    // update text content first so the measured size matches this frame
    if (el.type === 'counter') {
      let v = el.steps[0].value, since = el.start;
      let k = 0;
      el.steps.forEach((st, i) => { if (t >= st.t) { v = st.value; since = st.t; k = i; } });
      // numbers roll up when they first appear (not years like "1971: 6")
      const rolls = k === 0 && !/^(1[0-9]|20)\d\d(\b|:)/.test(String(v)) && /\d/.test(String(v));
      inner.textContent = rolls ? countUp(v, clamp01((t - el.start) / 0.9)) : String(v);
      el._since = since;
    } else if (el.type === 'label' && el.typewriter) {
      const words = String(el.text).split(' ');
      const n = Math.max(1, Math.ceil(words.length * clamp01(life.age / (el.typeDur ?? 0.8))));
      inner.textContent = words.slice(0, n).join(' ');
    }
    if (el.type === 'year') {
      const txt = String(el.value);
      const n = Math.max(1, Math.round(txt.length * clamp01(life.age / 0.45)));
      inner.textContent = el.typewriter === false ? txt : txt.slice(0, n);
    } else if (el.type === 'stat') {
      inner.querySelector('.v').textContent = countUp(el.value, clamp01(life.age / 0.9));
    }
    // big cards shrink to fit the width instead of running off screen
    if (['counter', 'stamp', 'year'].includes(el.type)) {
      if (el._fs == null) el._fs = parseFloat(inner.style.fontSize) || 0;
      if (el._fs) {
        inner.style.fontSize = el._fs + 'px';
        const maxW = W * (el.type === 'stamp' ? 0.78 : 0.86);
        if (inner.offsetWidth > maxW) inner.style.fontSize = (el._fs * maxW) / inner.offsetWidth + 'px';
      }
    }
    const w = inner.offsetWidth, h = inner.offsetHeight;
    // wide cards (charts, VS, timelines) are scaled down to fit between the safe margins
    const sf = state.tl.config.safe;
    const fit = ['bars', 'vs', 'timeline'].includes(el.type) ? Math.min(1, (W * (1 - sf.left - sf.right)) / Math.max(w, 1)) : 1;
    if (el.type === 'character') y -= h / 2 - 10; // anchor at the feet
    if (el.screen) [x, y] = clampToSafe(x, y, w * fit, h * fit);
    else if (el.type === 'label' || el.type === 'flag') {
      // map labels stay on screen and out of the like/comment/share column
      const s = state.tl.config.safe;
      x = Math.min(Math.max(x, W * s.left * 0.5 + w / 2), W - W * s.left * 0.5 - w / 2);
      if (y + h / 2 > H * 0.45) x = Math.min(x, W * (1 - s.right) - w / 2);
    }
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
      case 'character': {
        scale = ease.outBack(life.in);
        const body = inner.querySelector('.body');
        const bob = Math.sin(life.age * 2 * Math.PI * 0.9) * 4;
        const talking = el.say && life.age > 0.25 && life.age < (el.talkFor ?? 2.2);
        const mouthOpen = talking && Math.floor(life.age * 9 + Math.sin(life.age * 13)) % 2 === 0;
        const blink = (life.age + (el.seed || 0) * 0.7) % 3.1 < 0.12;
        if (el.image) {
          // clay figures: gentle hop while "talking", otherwise a slow sway
          const hop = talking ? Math.abs(Math.sin(life.age * 7)) * 10 : 0;
          const sq = 1 + (talking ? 0.025 * Math.sin(life.age * 14) : 0.012 * Math.sin(life.age * 3));
          body.style.transform = `translateY(${-hop + bob * 0.4}px) scaleX(${(el.flip ? -1 : 1) / sq}) scaleY(${sq}) rotate(${Math.sin(life.age * 2.2) * 2}deg)`;
        } else {
          body.style.transform = `translateY(${bob * 0.6}px) scaleX(${el.flip ? -1 : 1})`;
          body.querySelector('.mouth-open').style.display = mouthOpen ? '' : 'none';
          body.querySelector('.mouth-closed').style.display = mouthOpen ? 'none' : '';
          body.querySelector('.eyes-open').style.display = blink ? 'none' : '';
          body.querySelector('.eyes-closed').style.display = blink ? '' : 'none';
        }
        const bub = inner.querySelector('.bubble');
        if (bub) {
          // bubble goes toward the middle of the screen so it never runs off the edge
          // two talking characters at once: bubbles go above the heads so they never meet in the middle
          if (el._pair == null) el._pair = state.tl.elements.some((o) => o !== el && o.type === 'character' && o.say && o.start < el.end && o.end > el.start);
          bub.classList.toggle('top', el._pair);
          bub.classList.toggle('left', !el._pair && (el.bubbleSide === 'left' || (el.bubbleSide !== 'right' && (el.screen?.[0] ?? 0.5) > 0.55)));
          const bu = clamp01((life.age - 0.3) / 0.25);
          bub.style.opacity = String(bu);
          bub.style.transform = `scale(${ease.outBack(bu)})`;
        }
        break;
      }
      case 'route': {
        const m = el.mover;
        scale = ease.outBack(clamp01(life.age / 0.35));
        const spr = inner.querySelector('.spr');
        const goingLeft = Math.cos(el._head.ang) < 0;
        if (m.kind === 'plane') rot = (el._head.ang * 180) / Math.PI + 45;
        else if (m.kind === 'ship') {
          spr.style.transform = `scaleX(${goingLeft ? -1 : 1}) translateY(${Math.sin(t * 3.2) * 4}px) rotate(${Math.sin(t * 2.3) * 3}deg)`;
        } else if (m.kind === 'character') {
          spr.style.transform = `scaleX(${goingLeft ? -1 : 1}) translateY(${-Math.abs(Math.sin(t * 9)) * 10}px)`;
        }
        if (el._head.u >= 1 && m.hideAtEnd) opacity *= clamp01(1 - (life.age - (el.drawDur ?? 0)) / 0.3);
        break;
      }
      case 'measure': {
        if (el.countUp !== false) inner.textContent = countUp(el.label || '', el._head.u);
        // text always stays horizontal, set beside the line (never along it)
        rot = 0;
        const ang = el._head.ang;
        let nx = -Math.sin(ang), ny = Math.cos(ang);
        if (Math.abs(nx) >= Math.abs(ny)) { if ((x > W / 2) === (nx > 0)) { nx = -nx; ny = -ny; } }
        else if (ny > 0) { nx = -nx; ny = -ny; }
        const off = Math.abs(nx) * (w / 2 + 30) + Math.abs(ny) * (h / 2 + 24);
        x += nx * off;
        y += ny * off + (el.labelDy ?? 0);
        scale = ease.outBack(clamp01((life.age - 0.4) / 0.3));
        break;
      }
      case 'counter':
        scale = 1 + 0.35 * (1 - ease.outCubic(clamp01((t - el._since) / 0.3)));
        opacity *= clamp01(life.age / 0.2);
        break;
      case 'bars': {
        opacity *= clamp01(life.age / 0.3);
        const st = el.stagger ?? 0.22;
        if (el.orient === 'v') {
          inner.querySelectorAll('.col').forEach((col, i) => {
            const u = ease.outCubic(clamp01((life.age - 0.1 - i * st) / 0.8));
            col.querySelector('.shape').style.transform = `scaleY(${u})`;
            const v = col.querySelector('.val');
            v.textContent = countUp(v.dataset.v, u);
            v.style.opacity = String(clamp01(u * 3));
            col.querySelector('.lab').style.opacity = String(clamp01((life.age - i * st) / 0.25));
          });
        } else {
          inner.querySelectorAll('.row').forEach((row, i) => {
            const a = clamp01((life.age - i * st) / 0.3);
            row.style.opacity = String(a);
            row.style.transform = `translateX(${(1 - ease.outCubic(a)) * -40}px)`;
            const u = ease.outCubic(clamp01((life.age - 0.15 - i * st) / 0.8));
            const bar = row.querySelector('.bar');
            bar.style.width = `${Number(bar.dataset.w) * u}px`;
            const v = row.querySelector('.val');
            v.textContent = countUp(v.dataset.v, u);
          });
        }
        break;
      }
      case 'vs': {
        const [l, m, r] = inner.children;
        const u = ease.outBack(clamp01(life.age / 0.45));
        l.style.transform = `translateX(${(1 - u) * -420}px)`;
        r.style.transform = `translateX(${(1 - u) * 420}px)`;
        const mu = clamp01((life.age - 0.35) / 0.3);
        m.style.transform = `scale(${3 - 2 * ease.outCubic(mu)}) rotate(${-8 + 8 * mu}deg)`;
        m.style.opacity = String(clamp01(mu * 4));
        break;
      }
      case 'timeline': {
        const evs = el.events;
        let shown = 0;
        inner.querySelectorAll('.ev').forEach((d, i) => {
          const u = clamp01((t - evs[i].t) / 0.35);
          if (t >= evs[i].t) shown = i;
          d.style.opacity = String(u);
          d.style.transform = `translateX(-50%) translateY(${(1 - ease.outBack(u)) * 30}px) scale(${0.6 + 0.4 * ease.outBack(u)})`;
        });
        const frac = evs.length === 1 ? 1 : 0.08 + (0.84 * shown) / (evs.length - 1);
        const prevFrac = evs.length === 1 ? 0 : shown === 0 ? 0 : 0.08 + (0.84 * (shown - 1)) / (evs.length - 1);
        const k = clamp01((t - evs[shown].t) / 0.5);
        inner.querySelector('.axis').style.transform = `scaleX(${Math.max(0.02, prevFrac + (frac - prevFrac) * ease.outCubic(k))})`;
        break;
      }
      case 'clock': {
        const mins = (str) => {
          const [h, m] = String(str).split(':').map(Number);
          return h * 60 + (m || 0);
        };
        let cur = mins(el.steps[0].time), from = cur, since = el.start;
        for (const stp of el.steps) if (t >= stp.t) { from = cur; cur = mins(stp.time); since = stp.t; }
        const k = ease.inOutCubic(clamp01((t - since) / 0.9));
        let delta = cur - from;
        if (el.forward !== false && delta < 0) delta += 24 * 60;
        const now = from + delta * k;
        const r = (el.size || 200) / 2;
        inner.querySelector('.hh').setAttribute('transform', `rotate(${((now / 60) % 12) * 30} ${r} ${r})`);
        inner.querySelector('.mh').setAttribute('transform', `rotate(${(now % 60) * 6} ${r} ${r})`);
        scale = ease.outBack(life.in);
        break;
      }
      default:
        if (el.anim === 'slam') {
          // arrives huge and settles into place
          const u = ease.outCubic(clamp01(life.age / 0.3));
          scale = 1.6 - 0.6 * u;
          opacity *= clamp01(life.age / 0.12);
        } else if (el.anim === 'fade') {
          scale = 0.96 + 0.04 * ease.outCubic(life.in);
          opacity *= ease.outCubic(life.in);
        } else scale = 0.9 * ease.outBack(life.in) + 0.1 * life.in;
        if (life.out < 1) scale *= 0.9 + 0.1 * life.out;
    }
    if (el.type === 'flag' && el.moveTo) {
      const from = [x, y];
      const tp = el.moveTo.lat != null ? project(el.moveTo) : [W * el.moveTo.screen[0], H * el.moveTo.screen[1]];
      if (tp) {
        const to = [tp[0] + (el.moveTo.dx || 0), tp[1] + (el.moveTo.dy || 0)];
        const u = ease.inOutCubic(clamp01((t - el.moveAt) / (el.moveDur ?? 0.9)));
        const c = [(from[0] + to[0]) / 2, Math.min(from[1], to[1]) - Math.abs(to[0] - from[0]) * 0.35 - 60];
        x = (1 - u) * (1 - u) * from[0] + 2 * u * (1 - u) * c[0] + u * u * to[0];
        y = (1 - u) * (1 - u) * from[1] + 2 * u * (1 - u) * c[1] + u * u * to[1];
        el._arc = [from, c, to, u];
        rot = Math.sin(u * Math.PI) * -10;
      }
    }
    scale *= fit;
    if (el.screen && KIT_CARDS.has(el.type === 'label' ? (el.style === 'pill' ? 'pill' : '') : el.type)) {
      const k = kitEntrance(life.age);
      scale *= k.sc; rot += k.rot; opacity *= k.op; x += k.dx; y += k.dy;
      inner.style.clipPath = k.clip || '';
      inner.style.filter = k.blur > 0.2 ? `blur(${k.blur}px)` : '';
    }
    if (el.screen && BURST.has(el.type) && life.age < 0.9) state.bursts.push({ x, y, w: w * scale, h: h * scale, age: life.age, seed: el._i ?? 0 });
    placed.push({ el, node, inner, x, y, w, h, scale, rot, opacity });
  }
  // Overlap offsets are solved once per element when it appears (init pre-pass) and then kept,
  // so labels never slide around while they are on screen.
  for (const p of placed) if (p.el._off) { p.x += p.el._off[0]; p.y += p.el._off[1]; }
  if (state.layoutFor) {
    const raw = new Map(placed.map((p) => [p.el, [p.x, p.y]]));
    resolveOverlaps(placed, (el) => state.layoutFor.has(el));
    for (const p of placed) {
      if (!state.layoutFor.has(p.el)) continue;
      const r = raw.get(p.el);
      p.el._off = [p.x - r[0], p.y - r[1]];
    }
  }
  // scatter icons never sit under a label, card or character: hide the ones that would
  for (const el of state.tl.elements) {
    if (el.type !== 'scatter' || !el._node || !el._inner) continue;
    [...el._inner.children].forEach((img, i) => {
      if (img.style.opacity === '0' || !img.style.left) return;
      const sz = el.size || 70, x = parseFloat(img.style.left) + sz / 2, y = parseFloat(img.style.top) + sz / 2;
      el._clear = el._clear || [];
      if (el._clear[i] == null) {
        el._clear[i] = !placed.some((p) => p.opacity > 0.3 && p.el.type !== 'route' && Math.abs(p.x - x) < (p.w * p.scale + sz) / 2 && Math.abs(p.y - y) < (p.h * p.scale + sz) / 2)
          && !markerPoints(t).some((m) => Math.abs(m[0] - x) < (m[2] + sz) / 2 && Math.abs(m[1] - y) < (m[2] + sz) / 2);
      }
      if (!el._clear[i]) img.style.opacity = '0';
    });
  }
  for (const p of placed) {
    const { el, node, inner, scale, rot, opacity } = p;
    if (el.type === 'flag' && el.pin) {
      node.style.transform = `translate(${p.x}px, ${p.y}px)`;
      inner.style.transform = `scale(${scale})`;
      inner.style.transformOrigin = '0 0';
    } else {
      node.style.transform = `translate(${p.x - p.w / 2}px, ${p.y - p.h / 2}px)`;
      inner.style.transform = `scale(${scale}) rotate(${rot}deg)`;
    }
    node.style.opacity = String(opacity);
  }
}

// Push overlapping on-screen texts apart. Screen-placed items (counters, stats, stamps,
// characters) and the caption band are fixed obstacles; map labels/flags/icons move.
// Displacement is recomputed from the anchors every frame, so it follows the camera smoothly.
const MOVABLE = new Set(['label', 'flag', 'icon', 'badge', 'question', 'measure', 'stamp']);
// screen cards are already stacked by the timeline; only map-anchored things get nudged
const isMovable = (el) => MOVABLE.has(el.type) && !el.screen && !el.fixed;
function resolveOverlaps(items, canMove = isMovable) {
  const C = state.tl.config.captions;
  const boxes = items
    .filter((p) => p.opacity > 0.02 && !(p.el.type === 'flag' && p.el.pin) && p.el.type !== 'route' && p.el.type !== 'scatter')
    .map((p) => {
      // axis-aligned box of the (possibly rotated) element
      const k = Math.max(p.scale, 0.6), r = ((p.rot || 0) * Math.PI) / 180;
      const c = Math.abs(Math.cos(r)), sn = Math.abs(Math.sin(r));
      return { p, movable: canMove(p.el), w: (p.w * c + p.h * sn) * k, h: (p.w * sn + p.h * c) * k };
    });
  const cap = { p: { x: W / 2, y: H * C.y + C.size * 0.6 }, movable: false, w: W * 0.8, h: C.size * 1.5 };
  boxes.push(cap);
  // marked points (pings, city dots) are never covered by an icon or a label
  for (const m of markerPoints(state.time ?? 0)) boxes.push({ p: { x: m[0], y: m[1] }, movable: false, w: m[2], h: m[2], marker: true });
  // a character's speech bubble sits above its box: add it as an extra obstacle
  for (const p of items) {
    if (p.el.type !== 'character' || !p.el.say || p.opacity <= 0.02) continue;
    const left = p.el.bubbleSide === 'left' || (p.el.bubbleSide !== 'right' && (p.el.screen?.[0] ?? 0.5) > 0.55);
    if (p.el._pair) boxes.push({ p: { x: p.x, y: p.y - p.h / 2 - 70 }, movable: false, w: 380, h: 140 });
    else boxes.push({ p: { x: p.x + (left ? -1 : 1) * (p.w * 0.34 + 200), y: p.y - p.h * 0.3 }, movable: false, w: 400, h: 150 });
  }
  const pad = 14;
  for (let it = 0; it < 14; it++) {
    let moved = false;
    for (let i = 0; i < boxes.length; i++) {
      for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], b = boxes[j];
        if (!a.movable && !b.movable) continue;
        // a label may sit next to its own dot, but no icon may sit on any marked point
        if ((a.marker && b.p.el?.type === 'label') || (b.marker && a.p.el?.type === 'label')) {
          const lab = a.marker ? b : a, mk = a.marker ? a : b;
          if (Math.abs(lab.p.x - mk.p.x) > (lab.w + 20) / 2 || Math.abs(lab.p.y - mk.p.y) > (lab.h + 20) / 2) continue;
        }
        const ox = (a.w + b.w) / 2 + pad - Math.abs(a.p.x - b.p.x);
        const oy = (a.h + b.h) / 2 + pad - Math.abs(a.p.y - b.p.y);
        if (ox <= 0 || oy <= 0) continue;
        moved = true;
        const share = a.movable && b.movable ? 0.5 : 1;
        if (oy < ox) {
          const dir = a.p.y <= b.p.y ? -1 : 1;
          if (a.movable) a.p.y += dir * oy * share;
          if (b.movable) b.p.y -= dir * oy * share;
        } else {
          const dir = a.p.x <= b.p.x ? -1 : 1;
          if (a.movable) a.p.x += dir * ox * share;
          if (b.movable) b.p.x -= dir * ox * share;
        }
      }
    }
    if (!moved) break;
  }
  for (const b of boxes) {
    if (!b.movable) continue;
    b.p.x = Math.min(Math.max(b.p.x, b.w / 2 + 20), W - b.w / 2 - 20);
    b.p.y = Math.min(Math.max(b.p.y, b.h / 2 + 20), H * (1 - state.tl.config.safe.bottom) - b.h / 2);
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
      const C = state.tl.config.captions;
      const u = ease.outBack(clamp01((t - c.start) / 0.14));
      c._node.style.transform = `scale(${0.8 + 0.2 * u})`;
      c._node.style.opacity = String(clamp01(0.3 + u));
      c.words.forEach((w, i) => {
        const sp = c._spans[i];
        const active = C.activeColor && t >= w.start - 0.02 && t < (c.words[i + 1]?.start ?? c.end);
        sp.classList.toggle('active', !!active);
        sp.style.setProperty('--active', C.activeColor || '#ffd60a');
      });
    }
  }
}

// ---------------------------------------------------------------- fx

function hash01(n) {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
}

function updateFx(t) {
  const fx = $('fx');
  let html = '';
  let blur = 0, zoom = 0, shift = 0;
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
      html += `<div class="flash" style="opacity:${0.45 * (1 - clamp01((d + 0.05) / 0.35))}"></div>`;
    } else if (tr === 'wipe' && d > -0.25 && d < 0.35) {
      const u = clamp01((d + 0.25) / 0.6);
      const x = -60 + u * (W + 120);
      html += `<div class="flash" style="opacity:${0.35 * Math.sin(Math.PI * u)}"></div><div style="position:absolute;top:0;bottom:0;left:${x - 14}px;width:28px;background:#fff;box-shadow:0 0 40px 18px rgba(255,255,255,.8)"></div>`;
    } else if (tr === 'fade' && d > -0.3 && d < 0.3) {
      html += `<div class="black" style="opacity:${1 - Math.abs(d) / 0.3}"></div>`;
    } else if (tr === 'zoom' && d > -0.18 && d < 0.3) {
      const a = Math.sin(Math.PI * clamp01((d + 0.18) / 0.48));
      zoom = Math.max(zoom, a);
      blur = Math.max(blur, 7 * a);
    } else if (tr === 'glitch' && d > -0.12 && d < 0.26) {
      const u = clamp01((d + 0.12) / 0.38), a = Math.sin(Math.PI * u);
      const f = Math.floor(t * 30);
      for (let k = 0; k < 6; k++) {
        const r = hash01(f * 13 + k * 7), top = r * H, hh = 20 + hash01(f + k * 31) * 90, off = (hash01(f * 3 + k) - 0.5) * 120 * a;
        html += `<div style="position:absolute;left:0;right:0;top:${top}px;height:${hh}px;transform:translateX(${off}px);background:${k % 2 ? 'rgba(255,0,110,.28)' : 'rgba(0,229,255,.28)'};mix-blend-mode:screen"></div>`;
      }
      shift = 10 * a;
    } else if (tr === 'slide' && d > -0.2 && d < 0.3) {
      const u = clamp01((d + 0.2) / 0.5);
      const x = (1 - ease.inOutCubic(u)) * W * 1.1 - W * 0.05;
      html += `<div style="position:absolute;top:0;bottom:0;left:${x}px;width:${W * 0.1}px;background:var(--kit);opacity:${0.45 * Math.sin(Math.PI * u)};transform:skewX(-12deg);filter:blur(18px)"></div>`;
    }
  }
  // sparks when a number or stamp lands
  const kitC = state.tl.kit?.accent || '#ffd60a';
  for (const b of []) {
    const u = clamp01(b.age / 0.8);
    if (u >= 1) continue;
    for (let k = 0; k < 16; k++) {
      const ang = hash01(b.seed * 97 + k) * Math.PI * 2, sp = 0.6 + hash01(b.seed * 31 + k * 5);
      const dist = ease.outCubic(u) * (Math.max(b.w, 200) * 0.55 + 90) * sp;
      const px = b.x + Math.cos(ang) * dist, py = b.y + Math.sin(ang) * dist * 0.7;
      const sz = (k % 3 ? 10 : 16) * (1 - u);
      html += `<div style="position:absolute;left:${px - sz / 2}px;top:${py - sz / 2}px;width:${sz}px;height:${sz}px;border-radius:${k % 4 ? 50 : 2}%;background:${k % 3 ? kitC : '#fff'};opacity:${1 - u};box-shadow:0 0 12px ${kitC}"></div>`;
    }
  }
  // ambient layer: soft vignette, film grain, and era/kit specific atmosphere
  const mixA = styleAt(t);
  html += `<div class="amb-vig"></div>`;
  for (const el of state.tl.elements) {
    if (el.type === 'stamp' || el.vignette) {
      const life = lifeOf(el, t, 0.2, 0.25);
      if (life) html += `<div class="vignette" style="opacity:${life.in * life.out}"></div>`;
    }
  }
  fx.innerHTML = html;
  // per-kit colour grade on the map, plus transition blur
  const GRADE = { block: 'contrast(1.07) saturate(1.12)', news: 'contrast(1.06) saturate(0.92)', neon: 'saturate(1.18) contrast(1.05)', outline: 'contrast(1.1) brightness(0.96)', paper: 'saturate(1.06) brightness(1.03)' };
  const g = GRADE[state.tl.kit?.kit] || '';
  const f = [g, blur > 0.2 ? `blur(${blur}px)` : ''].filter(Boolean).join(' ') || 'none';
  $('raster').style.filter = f;
  for (const id of ['vector', 'marks']) $(id).style.filter = blur > 0.2 ? `blur(${blur}px)` : 'none';
  $('ui').style.transform = shift ? `translateX(${shift}px)` : '';
  // tilt: the map layers lean back like a 3D table (CSS); UI labels stay upright and are
  // re-positioned with the same maths in tiltPoint()
  const T = state.tilt;
  const zs = 1 + 0.07 * zoom;
  const tf = T ? `perspective(${TILT_P}px) rotateX(${T.deg}deg) scale(${T.s * zs})` : zoom > 0.01 ? `scale(${zs})` : 'none';
  for (const id of ['space', 'raster', 'vector', 'paper', 'marks']) {
    const n = $(id);
    n.style.transformOrigin = `50% ${TILT_OY * 100}%`;
    n.style.transform = tf;
  }
}

// ---------------------------------------------------------------- tilt

const TILT_P = 1500, TILT_OY = 0.62;
function computeTilt(t) {
  let deg = 0;
  for (const el of state.tl.elements) {
    if (el.type !== 'tilt') continue;
    const life = lifeOf(el, t, 0.9, 0.7);
    if (life) deg = Math.max(deg, (el.deg ?? 38) * ease.inOutCubic(life.in) * ease.inOutCubic(life.out));
  }
  // 3D table tilt left an empty band above the map: disabled, the map always fills the frame
  state.tilt = null && deg;
}

// where a point of the flat map ends up on screen once the map layers are tilted
function tiltPoint(x, y) {
  const T = state.tilt;
  if (!T) return [x, y];
  const ox = W / 2, oy = H * TILT_OY;
  const a = (T.deg * Math.PI) / 180;
  const dx = (x - ox) * T.s, dy = (y - oy) * T.s;
  const yy = dy * Math.cos(a), z = dy * Math.sin(a);
  const f = TILT_P / (TILT_P - z);
  return [ox + dx * f, oy + yy * f];
}

// ---------------------------------------------------------------- frame

function frame(t) {
  state.t = t;
  computeTilt(t);
  const cam = { ...state.camera.at(t) };
  // camera follows a moving ship/plane: keep it in the centre of the frame
  for (const s of state.tl.scenes) {
    const f = s.camera?.follow;
    if (!f || t < s.start - 0.3 || t > s.end + 0.3) continue;
    const el = state.tl.elements.find((e) => e.id === f && e.type === 'route');
    if (!el || t < el.start) continue;
    const head = routeHeadGeo(el, t);
    const w = ease.inOutCubic(clamp01((t - el.start) / 0.8)) * (t > s.end ? clamp01(1 - (t - s.end) / 0.3) : 1);
    if (s.camera.zoomTo) {
      // e.g. start close on the route and pull back while it is drawn
      const u = routeProgress(el, t);
      cam.zoom = Math.exp(Math.log(s.camera.zoom) + (Math.log(s.camera.zoomTo) - Math.log(s.camera.zoom)) * u);
    }
    cam.lon += (((head[0] - cam.lon + 540) % 360) - 180) * w;
    cam.lat += (head[1] - cam.lat) * w;
  }
  let dx = 0, dy = 0;
  for (const el of state.tl.elements) {
    if (el.type !== 'shake' && el.type !== 'punch') continue;
    const a = t - el.start;
    const dur = el.dur ?? (el.type === 'shake' ? 0.45 : 0.35);
    if (a < 0 || a > dur) continue;
    const k = 1 - a / dur;
    if (el.type === 'shake') {
      const amp = (el.amp ?? 16) * k * k;
      dx += amp * Math.sin(a * 83);
      dy += amp * Math.cos(a * 71);
    } else cam.zoom *= 1 + (el.amount ?? 0.07) * Math.sin(Math.PI * (a / dur));
  }
  const view = viewFor(cam, state.mode);
  view.cx += dx;
  view.cy += dy;
  state.view = view;
  state.proj = makeProjection(view);
  const mix = styleAt(t);
  const texelsPerPx = state.raster.base.w / (2 * Math.PI) / view.k;
  const detailMix = clamp01((1.2 - texelsPerPx) / 0.9);
  // a detail box that no longer fills the screen fades out, so its edges never show as a rectangle
  const W = $('stage').clientWidth || 1080, H = $('stage').clientHeight || 1920;
  const boxMix = state.raster.details.map((d) => {
    const [w, s, e, n] = d.box;
    const cl = Math.cos((s + n) / 2);
    const wPx = (e - w) * view.k * (state.mode === 'globe' ? cl : 1), hPx = ((n - s) * view.k) / (state.mode === 'globe' ? 1 : cl);
    return Math.max(detailMix, 0) * clamp01((Math.min(wPx / W, hPx / H) - 0.2) / 0.25);
  });
  // close-up history shots: the vector coastlines are too coarse for a tiny island or town, so the
  // real imagery shows through in old-map colours instead of a blobby polygon
  // only where sharp detail imagery covers the view: the 8k base is just a blur this close
  const sharp = state.tl.flatClose ? 0 : Math.min(1, Math.max(0, ...boxMix) * 1.5);
  const zoomNow = view.k / state.baseK;
  const z = clamp01((zoomNow - 20) / 25) * sharp;      // old map: coastlines get blobby early
  const zp = clamp01((zoomNow - 80) / 80) * sharp;     // flat maps: only when shapes are really coarse
  state.vinClose = z;
  state.palClose = zp;
  const tints = [[mix.vin * z, [0.86, 0.79, 0.62], [0.56, 0.69, 0.67]]];
  for (const [name, a] of Object.entries(mix.pal)) {
    const P = state.tl.config.palettes[name];
    if (a > 0.001) tints.push([a * zp, rgb01(P.land), rgb01(P.sea)]);
  }
  const close = tints.reduce((acc, t) => acc + t[0], 0);
  const avg = (k) => [0, 1, 2].map((c) => tints.reduce((acc, t) => acc + t[0] * t[k][c], 0) / (close || 1));
  const rAlpha = Math.min(1, mix.sat + close);
  if (!state.layoutOnly) state.raster.draw(view, { alpha: rAlpha, atmo: state.mode === 'globe' ? 1 : 0, detailMix: boxMix, sepia: rAlpha > 0 ? close / rAlpha : 0, tintLand: avg(1), tintSea: avg(2) });
  $('space').style.display = state.mode === 'globe' ? 'block' : 'none';
  $('paper').style.display = mix.vin > 0.001 ? 'block' : 'none';
  $('paper').style.opacity = String(mix.vin * state.tl.config.vintage.paper);
  if (!state.layoutOnly) drawVector(t, state.proj, view, mix);
  drawMarks(t);
  updateUi(t);
  updateCaptions(t);
  updateFx(t);
  return true;
}

// QA: rects of every UI element that is (mostly) visible right now, plus the caption box
function probe() {
  const out = [];
  state.tl.elements.forEach((el, i) => {
    if (!el._node || el.type === 'scatter') return;
    const op = parseFloat(el._node.style.opacity || '1');
    if (!(op > 0.5)) return;
    const r = (el._inner || el._node).getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    out.push({ i, type: el.type, text: String(el.text ?? el.value ?? el.label ?? el.steps?.[0]?.value ?? el.id ?? ''), scene: el.scene, start: el.start, end: el.end,
      x: r.left, y: r.top, w: r.width, h: r.height, op });
  });
  const caps = [...$('captions').querySelectorAll('*')].filter((n) => n.children.length === 0 && parseFloat(getComputedStyle(n).opacity) > 0.5)
    .map((n) => n.getBoundingClientRect()).filter((r) => r.width > 2);
  let cap = null;
  if (caps.length) {
    const x0 = Math.min(...caps.map((r) => r.left)), y0 = Math.min(...caps.map((r) => r.top));
    cap = { x: x0, y: y0, w: Math.max(...caps.map((r) => r.right)) - x0, h: Math.max(...caps.map((r) => r.bottom)) - y0 };
  }
  return { els: out, cap, scenes: state.tl.scenes.map((s) => [s.start, s.end]) };
}

window.GG = { init, frame, probe, fast: (on) => { state.layoutOnly = !!on; } };
