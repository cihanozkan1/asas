// Second toolbox (reference-channel study, round 9). Same contract as extras.js: pure functions of time.
//   drawGeo(ctx, t)   map-anchored canvas things: clone (true-size copy), wave (scaled rings), flood (coastal rise)
//   drawOver(ctx, t)  full-screen vector scenes: section (cross-section), radii (planet radii), protest (silhouette crowd)
//   html(el)/anim()   DOM types: ban, reason, retext, banner
//   fxHtml(t)         extra transitions: curl, split
import { geoPath, geoCentroid, geoCircle, geoRotation } from 'd3-geo';

const TAU = Math.PI * 2;
export const TYPES = ['clone', 'wave', 'flood', 'section', 'radii', 'protest', 'ban', 'reason', 'retext', 'banner'];

export function makeExtras2(S) {
  const { state, W, H, ease, clamp01 } = S;
  const lifeOf = (el, t, a, b) => S.lifeOf(el, t, a, b);
  const esc = S.esc;
  const hash01 = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const rgba = (hex, a) => {
    const m = /^#?([0-9a-f]{6})$/i.exec(hex || '');
    if (!m) return `rgba(255,255,255,${a})`;
    const n = parseInt(m[1], 16);
    return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
  };
  const text = (ctx, s, x, y, size, fill = '#fff', align = 'center') => {
    ctx.font = `900 ${size}px Montserrat, sans-serif`;
    ctx.textAlign = align; ctx.textBaseline = 'middle';
    ctx.lineJoin = 'round'; ctx.lineWidth = Math.max(4, size * 0.16);
    ctx.strokeStyle = 'rgba(8,12,24,.92)'; ctx.strokeText(s, x, y);
    ctx.fillStyle = fill; ctx.fillText(s, x, y);
  };

  // ------------------------------------------------------------------ clone: the same shape, true size, somewhere else
  const mapGeom = (g, fn) => {
    const m = (c) => (typeof c[0] === 'number' ? fn(c) : c.map(m));
    return { type: g.type, coordinates: m(g.coordinates) };
  };
  function prepare(el) {
    if (el.type === 'clone') {
      const feats = state.targets[el.target] || [];
      if (!feats.length) return;
      const c = geoCentroid({ type: 'FeatureCollection', features: feats });
      const to = [el.to.lon, el.to.lat];
      const toC = geoRotation([-to[0], -to[1]]);
      const fromC = geoRotation([-c[0], -c[1]]);
      el._geom = feats.map((f) => ({ type: 'Feature', properties: {}, geometry: mapGeom(f.geometry, (p) => toC.invert(fromC(p))) }));
    }
  }
  function drawClone(ctx, el, life, t) {
    if (!el._geom) return;
    const u = ease.outCubic(clamp01(life.age / 0.7));
    const path = geoPath(state.proj, ctx);
    const col = el.color || '#ffd60a';
    ctx.save();
    ctx.globalAlpha = life.out * u;
    ctx.lineJoin = 'round';
    ctx.beginPath(); path({ type: 'FeatureCollection', features: el._geom });
    ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 16; ctx.shadowOffsetY = 8;
    ctx.fillStyle = rgba(col, el.fillAlpha ?? 0.55); ctx.fill();
    ctx.shadowColor = col; ctx.shadowBlur = 10; ctx.shadowOffsetY = 0;
    ctx.strokeStyle = col; ctx.lineWidth = 5; ctx.stroke();
    ctx.restore();
    if (el.label) {
      const b = path.centroid({ type: 'FeatureCollection', features: el._geom });
      if (b && Number.isFinite(b[0])) { ctx.save(); ctx.globalAlpha = life.out * u; text(ctx, el.label, b[0], b[1], el.size || 64); ctx.restore(); }
    }
  }

  // ------------------------------------------------------------------ wave: rings whose radius is a real distance
  function drawWave(ctx, el, life, t) {
    const path = geoPath(state.proj, ctx);
    const R = (el.km / 6371) * (180 / Math.PI);
    const n = el.rings ?? 3, col = el.color || '#5ec8ff';
    ctx.save();
    ctx.lineJoin = 'round';
    const grow = ease.outCubic(clamp01(life.age / 0.9));
    for (let i = 0; i < n; i++) {
      const ph = (life.age * (el.speed ?? 0.45) + i / n) % 1;
      const r = R * ph * grow;
      if (r <= 0) continue;
      ctx.globalAlpha = life.out * (1 - ph) * 0.95;
      ctx.beginPath(); path(geoCircle().center([el.lon, el.lat]).radius(r)());
      ctx.shadowColor = col; ctx.shadowBlur = 12;
      ctx.strokeStyle = col; ctx.lineWidth = 6 * (1 - ph) + 2; ctx.stroke();
    }
    // the full reach stays as a thin dashed edge
    ctx.globalAlpha = life.out * 0.8 * grow; ctx.shadowBlur = 0;
    ctx.setLineDash([16, 12]); ctx.lineWidth = 3; ctx.strokeStyle = '#fff';
    ctx.beginPath(); path(geoCircle().center([el.lon, el.lat]).radius(R * grow)()); ctx.stroke();
    ctx.restore();
  }

  // ------------------------------------------------------------------ flood: a schematic coastal rise (km inland of the shore)
  function drawFlood(ctx, el, life) {
    const feats = state.targets[el.target] || [];
    if (!feats.length) return;
    const p0 = S.project({ lon: el.lon ?? 0, lat: el.lat ?? 0 });
    const p1 = S.project({ lon: (el.lon ?? 0) + 0.1, lat: el.lat ?? 0 });
    const pxPerKm = p0 && p1 ? Math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / (0.1 * 111.32 * Math.cos(((el.lat ?? 0) * Math.PI) / 180)) : 1;
    const band = Math.max(3, (el.km || 20) * pxPerKm * ease.inOutCubic(clamp01(life.age / (el.dur ?? 1.6))));
    const path = geoPath(state.proj, ctx);
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.beginPath(); path({ type: 'FeatureCollection', features: feats }); ctx.clip();
    ctx.beginPath(); path({ type: 'FeatureCollection', features: feats });
    ctx.lineJoin = 'round';
    ctx.strokeStyle = rgba(el.color || '#2f8fe8', 0.62); ctx.lineWidth = band * 2; ctx.stroke();
    ctx.strokeStyle = rgba('#bfe4ff', 0.9); ctx.lineWidth = 3; ctx.stroke();
    ctx.restore();
  }

  function drawGeo(ctx, t) {
    for (const el of state.tl.elements) {
      if (el.type !== 'clone' && el.type !== 'wave' && el.type !== 'flood') continue;
      const life = lifeOf(el, t, 0.3, 0.3);
      if (!life) continue;
      if (el.type === 'clone') drawClone(ctx, el, life, t);
      else if (el.type === 'wave') drawWave(ctx, el, life, t);
      else drawFlood(ctx, el, life);
    }
  }

  // ------------------------------------------------------------------ full-screen vector scenes
  const sky = (ctx, a, b) => { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, a); g.addColorStop(1, b); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); };
  const poly = (ctx, pts) => { ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath(); };

  function arrow2(ctx, x, y0, y1, label, k, col = '#fff') {
    // vertical dimension line with end ticks and a label
    ctx.save();
    ctx.globalAlpha *= k;
    const yy = y0 + (y1 - y0) * k;
    ctx.strokeStyle = col; ctx.lineWidth = 6; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x, yy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x - 20, y0); ctx.lineTo(x + 20, y0); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x - 20, yy); ctx.lineTo(x + 20, yy); ctx.stroke();
    if (label && k > 0.6) text(ctx, label, x + 30, (y0 + yy) / 2, 54, '#fff', 'left');
    ctx.restore();
  }

  function drawSection(ctx, el, life) {
    const k = ease.outCubic(clamp01(life.age / 0.6));
    const waterY = H * (el.waterY ?? 0.42), L = el.land ?? 0.2;
    const floor = el.floor || [[0, 0.62], [0.28, 0.66], [0.5, 0.82], [0.72, 0.66], [1, 0.62]];
    ctx.save();
    ctx.globalAlpha = k * life.out;
    sky(ctx, el.sky?.[0] || '#9bd3f5', el.sky?.[1] || '#e8f5ff');
    // sun
    const sg = ctx.createRadialGradient(W * 0.82, H * 0.12, 10, W * 0.82, H * 0.12, 140);
    sg.addColorStop(0, '#fff6c8'); sg.addColorStop(0.35, 'rgba(255,224,120,.9)'); sg.addColorStop(1, 'rgba(255,224,120,0)');
    ctx.fillStyle = sg; ctx.fillRect(0, 0, W, H * 0.4);
    // water body down to the sea floor
    const fl = floor.map(([x, y]) => [x * W, y * H]);
    poly(ctx, [[0, waterY], [W, waterY], ...fl.slice().reverse()]);
    const wg = ctx.createLinearGradient(0, waterY, 0, H * 0.9); wg.addColorStop(0, el.water?.[0] || '#38a8d8'); wg.addColorStop(1, el.water?.[1] || '#0b3d78');
    ctx.fillStyle = wg; ctx.fill();
    // waves on the surface
    ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.lineWidth = 5; ctx.beginPath();
    for (let x = 0; x <= W; x += 10) { const y = waterY + Math.sin(x / 38 + life.age * 2.2) * 6; x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.stroke();
    // ground strata under the floor, and the two coasts above the water
    const strata = el.strata || ['#7c5a3a', '#5a3e28', '#3d2a1c'];
    strata.forEach((c, i) => {
      poly(ctx, [...fl.map(([x, y]) => [x, y + i * H * 0.07]), [W, H], [0, H]]);
      ctx.fillStyle = c; ctx.fill();
    });
    const coastH = H * (el.coastH ?? 0.14);
    for (const side of [0, 1]) {
      const x0 = side ? W * (1 - L) : 0, x1 = side ? W : W * L;
      const edgeY = fl[side ? fl.length - 1 : 0][1];
      // a bank: grass on top, soil below, going straight down to the sea floor
      ctx.fillStyle = strata[0]; ctx.fillRect(x0, waterY - coastH, x1 - x0, edgeY - (waterY - coastH) + 4);
      ctx.fillStyle = side ? '#5aa34a' : '#6fb257'; ctx.fillRect(x0, waterY - coastH, x1 - x0, coastH + 6);
      ctx.fillStyle = '#41782f'; ctx.fillRect(x0, waterY - coastH, x1 - x0, 12);
      if (el.coastLabels) text(ctx, el.coastLabels[side], (x0 + x1) / 2, waterY - coastH - 38, 40, '#fff');
    }
    // structure
    const s = el.structure || {};
    const sx0 = W * (s.x0 ?? L), sx1 = W * (s.x1 ?? 1 - L);
    if (s.kind === 'tunnel') {
      const ty = H * (s.y ?? 0.78), th = 46 * k;
      const g = Math.max(0, Math.min(1, (life.age - 0.5) / 1.2));
      ctx.lineCap = 'round';
      ctx.strokeStyle = '#2b2f3a'; ctx.lineWidth = th + 14; ctx.beginPath(); ctx.moveTo(sx0, ty); ctx.lineTo(sx0 + (sx1 - sx0) * g, ty); ctx.stroke();
      ctx.strokeStyle = '#f97316'; ctx.lineWidth = th - 6; ctx.beginPath(); ctx.moveTo(sx0, ty); ctx.lineTo(sx0 + (sx1 - sx0) * g, ty); ctx.stroke();
      // a train moving inside
      if (g >= 1) { const tx = sx0 + ((life.age * 260) % (sx1 - sx0)); ctx.fillStyle = '#fff'; ctx.fillRect(tx - 44, ty - 14, 88, 28); }
    } else if (s.kind === 'bridge') {
      const by = waterY - H * (s.h ?? 0.2), g = ease.inOutCubic(clamp01((life.age - 0.4) / 1.4));
      ctx.strokeStyle = '#d33a3a'; ctx.lineWidth = 16;
      ctx.beginPath(); ctx.moveTo(sx0, by); ctx.lineTo(sx0 + (sx1 - sx0) * g, by); ctx.stroke();
      const towers = s.towers || [0.35, 0.65];
      towers.forEach((u) => {
        const tx = sx0 + (sx1 - sx0) * u;
        if (g > u) {
          ctx.lineWidth = 18; ctx.beginPath(); ctx.moveTo(tx, by + H * 0.3); ctx.lineTo(tx, by - H * 0.1); ctx.stroke();
          ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(211,58,58,.9)';
          for (let c = 0; c < 7; c++) { ctx.beginPath(); ctx.moveTo(tx, by - H * 0.1); ctx.lineTo(tx + (c - 3) * 55, by); ctx.stroke(); }
          ctx.strokeStyle = '#d33a3a';
        }
      });
    }
    // a known silhouette to read the size against (drawn from simple shapes)
    if (el.ref) {
      const r = el.ref, rx = W * (r.x ?? 0.5), base = H * (r.base ?? 0.8), h = H * (r.h ?? 0.15) * ease.outBack(clamp01((life.age - 0.9) / 0.6));
      ctx.fillStyle = '#e7ecf5';
      if (r.kind === 'tower') { poly(ctx, [[rx - h * 0.18, base], [rx - h * 0.04, base - h * 0.6], [rx, base - h], [rx + h * 0.04, base - h * 0.6], [rx + h * 0.18, base]]); ctx.fill(); }
      else if (r.kind === 'person') { ctx.fillRect(rx - h * 0.1, base - h * 0.7, h * 0.2, h * 0.7); ctx.beginPath(); ctx.arc(rx, base - h * 0.82, h * 0.12, 0, TAU); ctx.fill(); }
      else ctx.fillRect(rx - h * 0.16, base - h, h * 0.32, h);
      if (r.label) text(ctx, r.label, rx, base + 34, 36);
    }
    for (const d of el.dims || []) arrow2(ctx, W * d.x, H * d.y0, H * d.y1, d.label, ease.outCubic(clamp01((life.age - (d.at ?? 0.8)) / 0.8)));
    if (el.title) text(ctx, el.title, W / 2, H * 0.1, 66);
    ctx.restore();
  }

  function drawRadii(ctx, el, life) {
    const k = ease.outCubic(clamp01(life.age / 0.6));
    ctx.save();
    ctx.globalAlpha = k * life.out;
    sky(ctx, '#071a2e', '#0d3b4f');
    for (let i = 0; i < 70; i++) { ctx.fillStyle = `rgba(255,255,255,${0.25 + 0.6 * hash01(i)})`; ctx.fillRect(hash01(i * 3.1) * W, hash01(i * 5.7) * H, 3, 3); }
    const cx = W / 2, cy = H * (el.cy ?? 0.46), R = el.r ?? 330;
    // the planet flattens at the poles (the shape is exaggerated on purpose)
    const flat = (el.flat ?? 0.16) * ease.inOutCubic(clamp01((life.age - 0.8) / 1.4));
    const rx = R * (1 + flat * 0.5), ry = R * (1 - flat);
    const g = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.3, R * 0.1, cx, cy, R * 1.1);
    g.addColorStop(0, '#5fa8e8'); g.addColorStop(0.6, '#2b6cb8'); g.addColorStop(1, '#0e2f66');
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, TAU); ctx.fill();
    ctx.strokeStyle = 'rgba(160,220,255,.8)'; ctx.lineWidth = 6; ctx.stroke();
    ctx.setLineDash([14, 12]); ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(cx - rx - 40, cy); ctx.lineTo(cx + rx + 40, cy); ctx.stroke(); ctx.setLineDash([]);
    const rad = (ang, col, label, i) => {
      const u = ease.outCubic(clamp01((life.age - 0.4 - i * 0.5) / 0.8));
      const a = (ang * Math.PI) / 180, ex = cx + Math.cos(a) * rx, ey = cy - Math.sin(a) * ry;
      ctx.strokeStyle = col; ctx.lineWidth = 8; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + (ex - cx) * u, cy + (ey - cy) * u); ctx.stroke();
      ctx.fillStyle = col; ctx.beginPath(); ctx.arc(cx, cy, 11, 0, TAU); ctx.fill();
      if (u > 0.7) text(ctx, label, cx + (ex - cx) * 0.55, cy + (ey - cy) * 0.55 - (Math.abs(ang) < 30 ? 38 : 0), 46, col);
    };
    (el.radii || []).forEach((r, i) => rad(r.angle, r.color || '#fff', r.label, i));
    for (const m of el.marks || []) {
      const a = (m.angle * Math.PI) / 180, mx = cx + Math.cos(a) * (rx + (m.out ?? 22)), my = cy - Math.sin(a) * (ry + (m.out ?? 22));
      ctx.fillStyle = m.color || '#ff3b3b'; poly(ctx, [[mx, my - 26], [mx - 20, my + 12], [mx + 20, my + 12]]); ctx.fill();
      text(ctx, m.label, mx + (Math.cos(a) >= 0 ? -34 : 34), my - 44, 36, '#fff', Math.cos(a) >= 0 ? 'right' : 'left');
    }
    if (el.title) text(ctx, el.title, W / 2, H * 0.1, 64);
    ctx.restore();
  }

  function drawProtest(ctx, el, life, t) {
    const n = el.count ?? 16, col = el.color || '#2a3a6a';
    ctx.save();
    ctx.globalAlpha = life.out;
    for (let i = 0; i < n; i++) {
      const h = hash01(i * 7.1), x = (i + 0.5 + (h - 0.5) * 0.6) * (W / n), s = 120 + hash01(i * 3.3) * 70;
      const rise = ease.outBack(clamp01((life.age - i * 0.04) / 0.5));
      const y = H + 40 - rise * (el.height ?? 300) * (0.75 + 0.5 * hash01(i * 5.9));
      const sway = Math.sin(t * 3 + i) * 5;
      ctx.fillStyle = col; ctx.strokeStyle = col; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      // torso with shoulders, round head, both arms up holding a sign above the head
      ctx.beginPath(); ctx.moveTo(x - s * 0.34, y + s * 1.1); ctx.lineTo(x - s * 0.3, y + s * 0.16); ctx.quadraticCurveTo(x, y - s * 0.02, x + s * 0.3, y + s * 0.16); ctx.lineTo(x + s * 0.34, y + s * 1.1); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.arc(x, y - s * 0.16, s * 0.2, 0, TAU); ctx.fill();
      ctx.lineWidth = s * 0.1;
      ctx.beginPath(); ctx.moveTo(x - s * 0.3, y + s * 0.2); ctx.lineTo(x - s * 0.4 + sway, y - s * 0.62); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x + s * 0.3, y + s * 0.2); ctx.lineTo(x + s * 0.4 + sway, y - s * 0.62); ctx.stroke();
      if (h > 0.25) {
        ctx.save(); ctx.translate(x + sway, y - s * 0.66); ctx.rotate(((h - 0.5) * 14 * Math.PI) / 180);
        ctx.fillRect(-s * 0.48, -s * 0.46, s * 0.96, s * 0.46); ctx.restore();
      }
    }
    ctx.restore();
  }

  function drawOver(ctx, t) {
    for (const el of state.tl.elements) {
      if (el.type !== 'section' && el.type !== 'radii' && el.type !== 'protest') continue;
      const life = lifeOf(el, t, 0.3, 0.3);
      if (!life) continue;
      if (el.type === 'section') drawSection(ctx, el, life);
      else if (el.type === 'radii') drawRadii(ctx, el, life);
      else drawProtest(ctx, el, life, t);
    }
  }

  // ------------------------------------------------------------------ DOM types
  function html(el) {
    switch (el.type) {
      case 'ban': {
        const s = el.size || 160;
        return `<div class="inner ban" style="width:${s}px;height:${s}px"><img src="${el.src}"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" pathLength="100"/><line x1="18" y1="82" x2="82" y2="18" pathLength="100"/></svg></div>`;
      }
      case 'reason':
        return `<div class="inner reason"><b class="rn">${esc(el.n)}.</b><span class="rt">${esc(el.text)}</span></div>`;
      case 'retext':
        return `<div class="inner retext" style="font-size:${el.size || 84}px"><span class="ra">${esc(el.from)}<i class="rs"></i></span><span class="rb">${esc(el.to)}</span></div>`;
      case 'banner': {
        const s = el.size || 200;
        return `<div class="inner banner" style="width:${s}px;height:${s * 1.5}px"><i class="pole"></i><div class="cloth"><img src="${el.src}"></div></div>`;
      }
      default:
        return null;
    }
  }
  function anim(el, inner, life, t) {
    const tw = { scale: 1, rot: 0, opacity: 1, dx: 0, dy: 0 };
    switch (el.type) {
      case 'ban': {
        const c = inner.querySelector('circle'), l = inner.querySelector('line');
        const a = clamp01((life.age - 0.1) / 0.45), b = clamp01((life.age - 0.5) / 0.35);
        c.style.strokeDashoffset = String(100 - 100 * ease.outCubic(a));
        l.style.strokeDashoffset = String(100 - 100 * ease.outCubic(b));
        tw.scale = ease.outBack(clamp01(life.age / 0.3));
        break;
      }
      case 'reason':
        tw.scale = ease.outBack(clamp01(life.age / 0.4));
        tw.dy = (1 - ease.outCubic(clamp01(life.age / 0.4))) * 30;
        break;
      case 'retext': {
        const sa = ease.inOutCubic(clamp01((life.age - (el.strikeAt ?? 0.7)) / 0.35));
        inner.querySelector('.rs').style.width = `${sa * 100}%`;
        const showB = ease.outBack(clamp01((life.age - (el.strikeAt ?? 0.7) - 0.3) / 0.4));
        const rb = inner.querySelector('.rb');
        rb.style.opacity = String(clamp01(showB)); rb.style.transform = `scale(${0.8 + 0.2 * showB})`;
        inner.querySelector('.ra').style.opacity = String(1 - 0.35 * sa);
        tw.scale = ease.outBack(clamp01(life.age / 0.35));
        break;
      }
      case 'banner': {
        const cl = inner.querySelector('.cloth');
        const w = ease.outCubic(clamp01(life.age / 0.5));
        cl.style.transform = `scaleX(${w}) skewY(${Math.sin(t * 3.1) * 4}deg)`;
        tw.scale = 1;
        break;
      }
      default:
        break;
    }
    return tw;
  }

  // ------------------------------------------------------------------ transitions: a paper sheet that peels over the screen, a diagonal split
  function fxHtml(t) {
    let out = '';
    for (const s of state.tl.scenes) {
      const tr = s.transition;
      if (tr !== 'curl' && tr !== 'split') continue;
      const d = t - s.start;
      if (d < -0.1 || d > 0.8) continue;
      const u = clamp01((d + 0.1) / 0.9), up = u < 0.5 ? u * 2 : 2 - u * 2, e = ease.inOutCubic(up);
      if (tr === 'curl') {
        // the sheet covers from the bottom-right corner; its folded edge is a lit gradient strip
        const x = W * (1 - e) * 1.0, y = H * (1 - e) * 1.0;
        out += `<div style="position:absolute;inset:0;background:#efe4c8;clip-path:polygon(${W}px ${y * 0.6}px,${W}px ${H}px,${x * 0.6}px ${H}px);opacity:1"></div>`;
        out += `<div style="position:absolute;inset:0;clip-path:polygon(${W}px ${y * 0.6}px,${x * 0.6}px ${H}px,${x * 0.6 - 90}px ${H}px,${W}px ${y * 0.6 - 90}px);background:linear-gradient(135deg,rgba(0,0,0,.28),rgba(255,255,255,.55))"></div>`;
      } else {
        const off = e * W * 0.75;
        out += `<div style="position:absolute;inset:0;background:#0b1120;clip-path:polygon(0 0,${W * 0.5 + off * 0.0}px 0,${W * 0.35}px ${H}px,0 ${H}px);transform:translateX(${-off}px)"></div>`;
        out += `<div style="position:absolute;inset:0;background:#0b1120;clip-path:polygon(${W * 0.5}px 0,${W}px 0,${W}px ${H}px,${W * 0.35}px ${H}px);transform:translateX(${off}px)"></div>`;
      }
    }
    return out;
  }

  return { prepare, drawGeo, drawOver, html, anim, fxHtml };
}
