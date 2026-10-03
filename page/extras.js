// New drawing / effect features (the "reference channel" toolbox). Everything is a pure function of
// time t, like the rest of the renderer. main.js calls into this module at a few fixed hook points:
//   prepare(el)            per element, once, after geometry data exists
//   drawGeo(ctx, t)        map-anchored canvas things (marks layer, tilts with the map)
//   drawUnder(ctx, t)      screen-space canvas below the UI (dotted links...)
//   drawOver(ctx, t)       screen-space canvas above the UI (particles, sun flare, burst lines)
//   html(el)               DOM markup of the new UI element types
//   anim(el, inner, life, t) per-frame DOM animation of the new UI element types (returns tweaks)
//   fxHtml(t)              full-screen transition overlays for the new transitions
//   grade(t)               CSS filter string of active `grade` elements
import { geoPath, geoInterpolate, geoDistance } from 'd3-geo';
import { makeExtras2, TYPES as TYPES2 } from './extras2.js';

const TAU = Math.PI * 2;

export function makeExtras(S) {
  const { state, W, H, ease, clamp01 } = S;
  const hash01 = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const rgba = (hex, a) => {
    const m = /^#?([0-9a-f]{6})$/i.exec(hex || '');
    if (!m) return `rgba(255,255,255,${a})`;
    const n = parseInt(m[1], 16);
    return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
  };
  const lifeOf = (el, t, a, b) => S.lifeOf(el, t, a, b);
  const img = (src) => state.images[src];

  // ------------------------------------------------------------------ geometry prep
  function prepare(el) {
    if (el.type === 'pathtext') el._pts = S.densify(S.catmullRom(el.points), false);
    if (el.type === 'box') el._corners = [[el.from.lon, el.from.lat], [el.to.lon, el.from.lat], [el.to.lon, el.to.lat], [el.from.lon, el.to.lat]];
  }

  // ------------------------------------------------------------------ path text
  // text set along a real line (a road, a coast, a river): each letter rides the curve
  function drawPathText(ctx, el, life) {
    const pts = S.screenPolyline(el._pts);
    if (pts.length < 2) return;
    let path = pts;
    // read left to right
    if (path[path.length - 1][0] < path[0][0]) path = [...path].reverse();
    const cum = [0];
    for (let i = 1; i < path.length; i++) cum.push(cum[i - 1] + Math.hypot(path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]));
    const L = cum[cum.length - 1];
    const size = el.size || 64;
    ctx.save();
    ctx.font = `900 ${size}px Montserrat`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const chars = [...String(el.text)];
    const adv = chars.map((c) => ctx.measureText(c).width + size * 0.04);
    const total = adv.reduce((a, b) => a + b, 0);
    const k = Math.min(1, (L * 0.92) / total);       // shrink to fit the visible path
    const fs = size * k;
    ctx.font = `900 ${fs}px Montserrat`;
    const a2 = adv.map((v) => v * k);
    const T = a2.reduce((a, b) => a + b, 0);
    let d = (L - T) / 2;
    const u = ease.outCubic(clamp01(life.age / (el.revealDur ?? 0.9)));
    const shown = Math.ceil(chars.length * u);
    const at = (dist) => {
      let i = 1;
      while (i < cum.length - 1 && cum[i] < dist) i++;
      const f = clamp01((dist - cum[i - 1]) / (cum[i] - cum[i - 1] || 1));
      return [path[i - 1][0] + (path[i][0] - path[i - 1][0]) * f, path[i - 1][1] + (path[i][1] - path[i - 1][1]) * f];
    };
    const maxA = ((el.maxAngle ?? 50) * Math.PI) / 180;
    ctx.globalAlpha = life.out;
    ctx.lineJoin = 'round';
    const color = el.color || '#ffffff';
    for (let i = 0; i < shown; i++) {
      const mid = d + a2[i] / 2;
      const p = at(mid), p0 = at(Math.max(0, mid - a2[i])), p1 = at(Math.min(L, mid + a2[i]));
      let ang = Math.atan2(p1[1] - p0[1], p1[0] - p0[0]);
      ang = Math.max(-maxA, Math.min(maxA, ang));
      const pop = ease.outBack(clamp01(u * chars.length - i + 1));
      ctx.save();
      ctx.translate(p[0], p[1]);
      ctx.rotate(ang);
      ctx.translate(0, -(el.offset ?? 0.75) * fs);
      ctx.scale(pop, pop);
      ctx.lineWidth = fs * 0.2;
      ctx.strokeStyle = el.stroke || 'rgba(8,10,16,.9)';
      if (el.glow) { ctx.shadowColor = el.glow; ctx.shadowBlur = 22; }
      ctx.strokeText(chars[i], 0, 0);
      ctx.shadowBlur = 0;
      ctx.fillStyle = color;
      ctx.fillText(chars[i], 0, 0);
      ctx.restore();
      d += a2[i];
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ crowd of people pictograms
  function person(ctx, x, y, s, color) {
    ctx.fillStyle = color;
    ctx.beginPath(); ctx.arc(x, y - s * 0.78, s * 0.24, 0, TAU); ctx.fill();
    ctx.beginPath();
    ctx.moveTo(x - s * 0.34, y);
    ctx.lineTo(x - s * 0.34, y - s * 0.4);
    ctx.quadraticCurveTo(x - s * 0.34, y - s * 0.52, x - s * 0.2, y - s * 0.52);
    ctx.lineTo(x + s * 0.2, y - s * 0.52);
    ctx.quadraticCurveTo(x + s * 0.34, y - s * 0.52, x + s * 0.34, y - s * 0.4);
    ctx.lineTo(x + s * 0.34, y);
    ctx.closePath();
    ctx.fill();
  }
  function drawCrowd(ctx, el, life, t) {
    const p = el.screen ? [S.W * el.screen[0], S.H * el.screen[1]] : S.project(el);
    if (!p) return;
    const n = el.count || 24, cols = el.cols || Math.ceil(Math.sqrt(n * 1.6)), s = el.size || 34;
    const rows = Math.ceil(n / cols);
    const grow = clamp01(life.age / (el.growDur ?? 1.0));
    // visible count can also shrink/grow at scripted times: [{t, n}]
    let vis = Math.round(n * grow);
    for (const c of el.counts || []) if (t >= c.t) vis = c.n;
    let redN = 0;
    for (const r of el.red || []) if (t >= r.t) redN = Math.max(redN, r.n);
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.shadowColor = 'rgba(0,0,0,.55)'; ctx.shadowBlur = 6;
    for (let i = 0; i < Math.min(n, vis); i++) {
      const r = Math.floor(i / cols), c = i % cols;
      const x = p[0] + (c - (cols - 1) / 2) * s * 0.95, y = p[1] + (r - (rows - 1) / 2) * s * 1.25 + s * 0.6;
      const pop = ease.outBack(clamp01((life.age - i * 0.02) / 0.25));
      ctx.save();
      ctx.translate(x, y); ctx.scale(pop, pop); ctx.translate(-x, -y);
      person(ctx, x, y, s, i < redN ? (el.redColor || '#ff3b3b') : el.color || '#ffffff');
      ctx.restore();
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ country with a face
  const EXPR = {
    neutral: { brow: 0, browY: 0, curve: 0.1, open: 0, wide: 1 },
    happy: { brow: -8, browY: -0.05, curve: 0.9, open: 0.25, wide: 1 },
    angry: { brow: 26, browY: 0.03, curve: -0.35, open: 0, wide: 0.85 },
    worried: { brow: -22, browY: -0.02, curve: -0.5, open: 0.1, wide: 1.1 },
    surprised: { brow: -12, browY: -0.1, curve: 0, open: 0.95, wide: 1.35 },
    sad: { brow: -18, browY: 0, curve: -0.9, open: 0, wide: 1 },
    smug: { brow: 14, browY: 0, curve: 0.55, open: 0, wide: 0.8 },
    talk: { brow: 0, browY: 0, curve: 0.3, open: 0.5, wide: 1 },
  };
  function faceParams(el, t) {
    let cur = EXPR.neutral, prev = EXPR.neutral, since = -9, name = 'neutral';
    for (const e of el.expr || []) if (t >= e.t) { prev = cur; cur = EXPR[e.e] || EXPR.neutral; since = e.t; name = e.e; }
    const u = ease.inOutSine(clamp01((t - since) / 0.2));
    const o = {};
    for (const k of Object.keys(EXPR.neutral)) o[k] = prev[k] + (cur[k] - prev[k]) * u;
    if (name === 'talk') o.open = 0.15 + 0.4 * Math.abs(Math.sin(t * 11));
    return o;
  }
  function drawFace(ctx, el, life, t) {
    const feat = state.targetMain?.[el.target] || { type: 'FeatureCollection', features: state.targets[el.target] };
    const b = geoPath(state.proj).bounds(feat);
    const bw = b[1][0] - b[0][0], bh = b[1][1] - b[0][1];
    if (!(bw > 4)) return;
    const cx = (b[0][0] + b[1][0]) / 2 + (el.dx || 0), cy = (b[0][1] + b[1][1]) / 2 + (el.dy || 0);
    const s = Math.max(60, Math.min(bw, bh) * (el.scale ?? 0.55)) * ease.outBack(clamp01(life.age / 0.4));
    const P = faceParams(el, t);
    const look = el.look ? S.project(el.look) : null;
    const wob = Math.sin(t * 2.1 + (el.seed || 0)) * 0.03;
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.translate(cx, cy);
    ctx.rotate(wob);
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    const er = s * 0.2 * P.wide, ex = s * 0.24, ey = -s * 0.1;
    const blink = (t + (el.seed || 0) * 0.9) % 3.4 < 0.11;
    for (const side of [-1, 1]) {
      const x = side * ex;
      ctx.fillStyle = '#fff'; ctx.strokeStyle = '#141414'; ctx.lineWidth = s * 0.035;
      ctx.beginPath();
      if (blink) { ctx.moveTo(x - er, ey); ctx.lineTo(x + er, ey); ctx.stroke(); }
      else {
        ctx.ellipse(x, ey, er, er * 1.08, 0, 0, TAU); ctx.fill(); ctx.stroke();
        let px = 0, py = 0;
        if (look) { const dx = look[0] - cx, dy = look[1] - cy, d = Math.hypot(dx, dy) || 1; px = (dx / d) * er * 0.42; py = (dy / d) * er * 0.42; }
        else { px = Math.sin(t * 0.9) * er * 0.25; py = Math.cos(t * 0.7) * er * 0.12; }
        ctx.fillStyle = '#141414';
        ctx.beginPath(); ctx.arc(x + px, ey + py, er * 0.46, 0, TAU); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x + px - er * 0.14, ey + py - er * 0.16, er * 0.14, 0, TAU); ctx.fill();
      }
      // eyebrow
      ctx.strokeStyle = '#141414'; ctx.lineWidth = s * 0.05;
      const by = ey - er * 1.25 + P.browY * s, a = (-side * P.brow * Math.PI) / 180, L = er * 1.15;
      ctx.beginPath();
      ctx.moveTo(x - Math.cos(a) * L, by - Math.sin(a) * L);
      ctx.lineTo(x + Math.cos(a) * L, by + Math.sin(a) * L);
      ctx.stroke();
    }
    // mouth
    const my = s * 0.24, mw = s * 0.26;
    ctx.strokeStyle = '#141414'; ctx.lineWidth = s * 0.05;
    ctx.beginPath();
    if (P.open > 0.3) {
      ctx.fillStyle = '#3a0d12';
      ctx.ellipse(0, my, mw * (0.5 + 0.35 * P.open), s * 0.13 * P.open + 3, 0, 0, TAU);
      ctx.fill(); ctx.stroke();
    } else {
      ctx.moveTo(-mw, my);
      ctx.quadraticCurveTo(0, my + P.curve * s * 0.22, mw, my);
      ctx.stroke();
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ pin with a picture inside
  function drawPin(ctx, el, life) {
    const p = S.project(el);
    if (!p) return;
    const drop = (1 - ease.outBounce(clamp01(life.age / 0.55))) * 90;
    const s = (el.size || 78) * ease.outBack(clamp01(life.age / 0.25));
    const c = el.color || '#e11d2e';
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(p[0], p[1], s * 0.28, s * 0.09, 0, 0, TAU); ctx.fill();
    ctx.translate(p[0], p[1] - drop);
    ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 12; ctx.shadowOffsetY = 4;
    ctx.fillStyle = '#fff'; ctx.strokeStyle = c; ctx.lineWidth = s * 0.06;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.bezierCurveTo(-s * 0.15, -s * 0.5, -s * 0.5, -s * 0.78, -s * 0.5, -s * 1.12);
    ctx.arc(0, -s * 1.12, s * 0.5, Math.PI, 0);
    ctx.bezierCurveTo(s * 0.5, -s * 0.78, s * 0.15, -s * 0.5, 0, 0);
    ctx.fill(); ctx.shadowBlur = 0; ctx.stroke();
    const im = el.src && img(el.src);
    if (im) {
      const iw = s * 0.62, ih = iw * (im.height / im.width);
      const k = Math.min(1, (s * 0.62) / ih);
      ctx.drawImage(im, -iw * k / 2, -s * 1.12 - ih * k / 2, iw * k, ih * k);
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ area box (buildings, parks)
  function drawBox(ctx, el, life) {
    const P = el._corners.map(([lon, lat]) => S.project({ lon, lat }));
    if (P.some((p) => !p)) return;
    const u = ease.inOutCubic(clamp01(life.age / (el.drawDur ?? 0.55)));
    const col = el.color || '#ffe600';
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.lineJoin = 'round';
    // traced outline: total length walked clockwise
    const seg = [];
    let tot = 0;
    for (let i = 0; i < 4; i++) { const a = P[i], b = P[(i + 1) % 4]; const d = Math.hypot(b[0] - a[0], b[1] - a[1]); seg.push(d); tot += d; }
    let want = tot * u;
    ctx.beginPath();
    ctx.moveTo(P[0][0], P[0][1]);
    for (let i = 0; i < 4 && want > 0; i++) {
      const a = P[i], b = P[(i + 1) % 4], f = Math.min(1, want / (seg[i] || 1));
      ctx.lineTo(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f);
      want -= seg[i];
    }
    if (u >= 1) ctx.closePath();
    ctx.shadowColor = col; ctx.shadowBlur = 14;
    ctx.strokeStyle = col; ctx.lineWidth = el.width || 5;
    ctx.stroke();
    if (u >= 0.98) {
      ctx.shadowBlur = 0;
      ctx.beginPath(); P.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.closePath();
      ctx.fillStyle = rgba(col, el.fillAlpha ?? 0.16); ctx.fill();
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ light pillar
  function drawBeam(ctx, el, life, t) {
    const p = S.project(el);
    if (!p) return;
    const h = (el.height || 420) * ease.outCubic(clamp01(life.age / 0.6));
    const w = el.width || 30;
    const col = el.color || '#ffd60a';
    const pulse = 0.8 + 0.2 * Math.sin(t * 4 + p[0]);
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.globalAlpha = life.out * pulse;
    const g = ctx.createLinearGradient(0, p[1], 0, p[1] - h);
    g.addColorStop(0, rgba(col, 0.9)); g.addColorStop(1, rgba(col, 0));
    ctx.fillStyle = g;
    ctx.fillRect(p[0] - w / 2, p[1] - h, w, h);
    const g2 = ctx.createRadialGradient(p[0], p[1], 0, p[0], p[1], w * 2.2);
    g2.addColorStop(0, rgba(col, 0.9)); g2.addColorStop(1, rgba(col, 0));
    ctx.fillStyle = g2;
    ctx.beginPath(); ctx.arc(p[0], p[1], w * 2.2, 0, TAU); ctx.fill();
    ctx.restore();
  }

  // ------------------------------------------------------------------ procedural clouds (drift over the map)
  let cloudSprite = null;
  function sprite() {
    if (cloudSprite) return cloudSprite;
    const c = document.createElement('canvas');
    c.width = 320; c.height = 200;
    const x = c.getContext('2d');
    const blobs = [[100, 120, 70], [170, 96, 84], [240, 122, 66], [140, 128, 62], [205, 132, 60], [60, 136, 44], [275, 138, 40]];
    for (const [bx, by, r] of blobs) {
      const g = x.createRadialGradient(bx, by - r * 0.25, r * 0.1, bx, by, r);
      g.addColorStop(0, 'rgba(255,255,255,0.98)'); g.addColorStop(0.65, 'rgba(250,252,255,0.86)'); g.addColorStop(1, 'rgba(240,246,255,0)');
      x.fillStyle = g; x.beginPath(); x.arc(bx, by, r, 0, TAU); x.fill();
    }
    // soft blue underside
    x.globalCompositeOperation = 'source-atop';
    const u = x.createLinearGradient(0, 60, 0, 200);
    u.addColorStop(0, 'rgba(255,255,255,0)'); u.addColorStop(1, 'rgba(120,150,200,0.55)');
    x.fillStyle = u; x.fillRect(0, 0, 320, 200);
    return (cloudSprite = c);
  }
  function drawClouds(ctx, el, life, t) {
    const p = el.screen ? [S.W * el.screen[0], S.H * el.screen[1]] : S.project(el);
    if (!p) return;
    const n = el.count || 3, size = el.size || 300, sp = sprite();
    ctx.save();
    for (let i = 0; i < n; i++) {
      const h1 = hash01(i * 7 + (el.seed || 3)), h2 = hash01(i * 13 + 5);
      const drift = (life.age * (el.speed ?? 46)) % (size * 3);
      const x = p[0] + (h1 - 0.5) * size * 2.2 + drift - size * 1.2 + (el.dx || 0);
      const y = p[1] + (h2 - 0.5) * size * 0.9 + Math.sin(t * 0.6 + i) * 6;
      const k = size * (0.7 + h2 * 0.6) / 320;
      const a = ease.outCubic(clamp01((life.age - i * 0.15) / 0.6)) * life.out;
      ctx.globalAlpha = a * 0.28; ctx.filter = 'blur(10px)';
      ctx.drawImage(sp, x - 160 * k + 34, y - 100 * k + 60, 320 * k, 200 * k);   // ground shadow
      ctx.filter = 'none';
      ctx.globalAlpha = a * (el.opacity ?? 0.95);
      ctx.drawImage(sp, x - 160 * k, y - 100 * k, 320 * k, 200 * k);
      if (el.rain) {
        ctx.strokeStyle = 'rgba(190,225,255,0.85)'; ctx.lineWidth = 3; ctx.lineCap = 'round';
        for (let r = 0; r < 14; r++) {
          const rx = x - 90 * k + hash01(r + i * 31) * 180 * k, off = ((t * 520 + r * 97) % 260);
          ctx.beginPath(); ctx.moveTo(rx, y + 40 * k + off); ctx.lineTo(rx - 8, y + 40 * k + off + 34); ctx.stroke();
        }
      }
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ links between screen points (dotted, curved)
  function drawLink(ctx, el, life) {
    const a = [S.W * el.from[0], S.H * el.from[1]], b = [S.W * el.to[0], S.H * el.to[1]];
    const dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy) || 1;
    const cv = el.curve ?? 0.22;
    const c = [(a[0] + b[0]) / 2 - (dy / len) * len * cv, (a[1] + b[1]) / 2 + (dx / len) * len * cv];
    const u = ease.inOutCubic(clamp01(life.age / (el.drawDur ?? 0.7)));
    const pt = (v) => [(1 - v) * (1 - v) * a[0] + 2 * v * (1 - v) * c[0] + v * v * b[0], (1 - v) * (1 - v) * a[1] + 2 * v * (1 - v) * c[1] + v * v * b[1]];
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.fillStyle = el.color || '#ffffff';
    ctx.shadowColor = 'rgba(0,0,0,.4)'; ctx.shadowBlur = 4;
    const n = Math.round(len / 22);
    for (let i = 0; i <= n * u; i++) { const q = pt(i / n); ctx.beginPath(); ctx.arc(q[0], q[1], el.dot || 4.2, 0, TAU); ctx.fill(); }
    if (el.arrow !== false && u > 0.95) {
      const q1 = pt(1), q0 = pt(0.96), ang = Math.atan2(q1[1] - q0[1], q1[0] - q0[0]);
      ctx.beginPath();
      ctx.moveTo(q1[0] + Math.cos(ang) * 12, q1[1] + Math.sin(ang) * 12);
      ctx.lineTo(q1[0] + Math.cos(ang + 2.5) * 18, q1[1] + Math.sin(ang + 2.5) * 18);
      ctx.lineTo(q1[0] + Math.cos(ang - 2.5) * 18, q1[1] + Math.sin(ang - 2.5) * 18);
      ctx.fill();
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ particles (screen space, above the UI)
  function drawParticles(ctx, el, life, t) {
    const kind = el.kind || 'snow', dens = el.density ?? 1;
    const a = ease.outCubic(clamp01(life.age / 0.8)) * life.out;
    ctx.save();
    ctx.globalAlpha = a;
    if (kind === 'snow') {
      const n = Math.round(150 * dens);
      for (let i = 0; i < n; i++) {
        const h = hash01(i * 3.7 + 1), h2 = hash01(i * 5.1 + 2), h3 = hash01(i * 9.3 + 3);
        const sp = 90 + h3 * 160, r = 2 + h2 * 5.5;
        const x = ((h * W + Math.sin(t * (0.6 + h2) + i) * 34 + t * 28) % (W + 40) + W + 40) % (W + 40) - 20;
        const y = ((h2 * H + t * sp) % (H + 20)) - 10;
        ctx.fillStyle = `rgba(255,255,255,${0.55 + 0.4 * h3})`;
        ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
      }
    } else if (kind === 'rain') {
      ctx.strokeStyle = 'rgba(200,225,255,.6)'; ctx.lineWidth = 2.6; ctx.lineCap = 'round';
      const n = Math.round(170 * dens);
      for (let i = 0; i < n; i++) {
        const h = hash01(i * 2.3), h2 = hash01(i * 7.9), sp = 900 + h2 * 700;
        const x = ((h * (W + 300) + t * 210) % (W + 300)) - 150, y = ((h2 * H + t * sp) % (H + 120)) - 60;
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - 14, y + 46); ctx.stroke();
      }
    } else if (kind === 'dust') {
      const n = Math.round(90 * dens);
      for (let i = 0; i < n; i++) {
        const h = hash01(i * 4.1), h2 = hash01(i * 8.7), sp = 700 + h2 * 900;
        const x = ((h * (W + 600) + t * sp) % (W + 600)) - 300, y = h2 * H, len = 90 + h * 200;
        const g = ctx.createLinearGradient(x, y, x + len, y);
        g.addColorStop(0, 'rgba(196,150,90,0)'); g.addColorStop(1, `rgba(196,150,90,${0.22 + 0.2 * h2})`);
        ctx.fillStyle = g; ctx.fillRect(x, y, len, 2 + h * 4);
      }
    } else if (kind === 'swarm') {
      // a buzzing cloud (flies, locusts, mosquitoes) drifting over the spot
      const n = Math.round(90 * dens), cx = (el.screen?.[0] ?? 0.5) * W, cy = (el.screen?.[1] ?? 0.45) * H;
      for (let i = 0; i < n; i++) {
        const h = hash01(i * 3.7 + 1), h2 = hash01(i * 5.1 + 2), a = t * (1.2 + h * 2.2) + i;
        const x = cx + Math.cos(a) * (60 + 380 * h2) + Math.sin(t * 0.7 + i) * 60, y = cy + Math.sin(a * 1.3) * (40 + 260 * h);
        ctx.fillStyle = 'rgba(25,25,25,.9)'; ctx.beginPath(); ctx.arc(x, y, 3 + h2 * 2.5, 0, TAU); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.fillRect(x - 5, y - 4, 4, 2); ctx.fillRect(x + 1, y - 4, 4, 2);
      }
    } else if (kind === 'ash') {
      // fallout: grey flakes sinking slowly
      const n = Math.round(110 * dens);
      for (let i = 0; i < n; i++) {
        const h = hash01(i * 3.7 + 1), h2 = hash01(i * 5.1 + 2), h3 = hash01(i * 9.3 + 3);
        const x = ((h * W + Math.sin(t * 0.8 + i) * 26) % W + W) % W, y = ((h2 * H + t * (30 + h3 * 50)) % (H + 20)) - 10;
        ctx.fillStyle = `rgba(${150 + 60 * h3 | 0},${150 + 60 * h3 | 0},${150 + 60 * h3 | 0},${0.45 + 0.4 * h})`;
        ctx.beginPath(); ctx.ellipse(x, y, 2 + h2 * 4, 1.5 + h * 2.5, h * 3, 0, TAU); ctx.fill();
      }
    } else if (kind === 'embers') {
      const n = Math.round(80 * dens);
      for (let i = 0; i < n; i++) {
        const h = hash01(i * 1.9), h2 = hash01(i * 6.1), sp = 60 + h2 * 140;
        const x = (h * W + Math.sin(t * 1.5 + i) * 30 + W) % W, y = H - ((h2 * H + t * sp) % H);
        ctx.fillStyle = `rgba(255,${140 + h2 * 80},40,${0.4 + 0.5 * h})`;
        ctx.shadowColor = '#ff9a2e'; ctx.shadowBlur = 10;
        ctx.beginPath(); ctx.arc(x, y, 2 + h2 * 3, 0, TAU); ctx.fill();
      }
    } else if (kind === 'confetti') {
      const cols = ['#ff3b6b', '#ffd60a', '#4ade80', '#38bdf8', '#a78bfa'];
      const n = Math.round(90 * dens);
      for (let i = 0; i < n; i++) {
        const h = hash01(i * 3.3), h2 = hash01(i * 5.7), sp = 200 + h2 * 260;
        const x = (h * W + Math.sin(t * 2 + i) * 40 + W) % W, y = ((h2 * H + t * sp) % (H + 40)) - 20;
        ctx.save(); ctx.translate(x, y); ctx.rotate(t * (2 + h * 4) + i);
        ctx.fillStyle = cols[i % cols.length]; ctx.fillRect(-7, -4, 14, 8); ctx.restore();
      }
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ sun / lens flare
  function drawFlare(ctx, el, life, t) {
    const p = el.screen ? [W * el.screen[0], H * el.screen[1]] : S.project(el);
    if (!p) return;
    const a = ease.outCubic(clamp01(life.age / 1.0)) * life.out;
    const r = (el.r || 260) * (0.9 + 0.1 * Math.sin(t * 2));
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.globalAlpha = a;
    const g = ctx.createRadialGradient(p[0], p[1], 0, p[0], p[1], r);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.12, 'rgba(255,236,180,.9)'); g.addColorStop(0.4, 'rgba(255,170,80,.28)'); g.addColorStop(1, 'rgba(255,120,40,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p[0], p[1], r, 0, TAU); ctx.fill();
    const s = ctx.createLinearGradient(p[0] - r * 2.2, p[1], p[0] + r * 2.2, p[1]);
    s.addColorStop(0, 'rgba(255,220,160,0)'); s.addColorStop(0.5, 'rgba(255,240,210,.85)'); s.addColorStop(1, 'rgba(255,220,160,0)');
    ctx.fillStyle = s; ctx.fillRect(p[0] - r * 2.2, p[1] - 3, r * 4.4, 6);
    // ghosts toward the frame centre
    const cx = W / 2, cy = H / 2;
    [[0.35, 26, 'rgba(120,200,255,.35)'], [0.6, 46, 'rgba(255,170,90,.28)'], [0.85, 18, 'rgba(160,255,190,.3)'], [1.2, 60, 'rgba(255,120,150,.2)']].forEach(([f, rr, c]) => {
      const gx = p[0] + (cx - p[0]) * f, gy = p[1] + (cy - p[1]) * f;
      ctx.fillStyle = c; ctx.beginPath(); ctx.arc(gx, gy, rr, 0, TAU); ctx.fill();
    });
    ctx.restore();
  }

  // ------------------------------------------------------------------ burst lines around a reaction
  function drawBurst(ctx, el, life) {
    if (!el._scr) return;
    const [x, y] = el._scr;
    const u = clamp01(life.age / 0.5);
    if (u >= 1) return;
    ctx.save();
    ctx.globalAlpha = (1 - u) * life.out;
    ctx.strokeStyle = el.burstColor || '#fff'; ctx.lineWidth = 5; ctx.lineCap = 'round';
    const r0 = (el.size || 150) * (0.6 + ease.outCubic(u) * 0.5), r1 = r0 + 40 + 40 * (1 - u);
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * TAU + 0.2;
      ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * r0, y + Math.sin(a) * r0); ctx.lineTo(x + Math.cos(a) * r1, y + Math.sin(a) * r1); ctx.stroke();
    }
    ctx.restore();
  }


  // ------------------------------------------------------------------ callout / ellipse / glow / crack (from the 40-video review)
  const FONT = "'Montserrat', sans-serif";
  function drawCallout(ctx, el, life) {
    const p = S.project({ lon: el.lon, lat: el.lat });
    if (!p) return;
    const u = ease.outCubic(clamp01(life.age / 0.6));
    const q = [p[0] + (el.dx ?? 130), p[1] + (el.dy ?? -180)];
    const m = [(p[0] + q[0]) / 2 + (el.curve ?? 34), (p[1] + q[1]) / 2 - 24];
    ctx.save();
    ctx.globalAlpha = life.out;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 4; ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 8;
    ctx.beginPath();
    for (let i = 0; i <= 24; i++) {
      const t = (i / 24) * u, x = (1 - t) * (1 - t) * q[0] + 2 * t * (1 - t) * m[0] + t * t * p[0], y = (1 - t) * (1 - t) * q[1] + 2 * t * (1 - t) * m[1] + t * t * p[1];
      if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
    }
    ctx.stroke();
    ctx.beginPath(); ctx.arc(p[0], p[1], 7 * u, 0, TAU); ctx.fillStyle = '#fff'; ctx.fill();
    ctx.translate(q[0], q[1]); ctx.rotate(-0.06);
    ctx.globalAlpha = life.out * clamp01(life.age / 0.25);
    const size = el.size || 54, lines = String(el.text).split('\n');
    ctx.textAlign = 'center'; ctx.lineJoin = 'round';
    lines.forEach((ln, i) => {
      const fs = i === 0 ? size : size * 0.62, y = -lines.length * size * 0.3 + i * size * 0.78;
      ctx.font = `900 ${fs}px ${FONT}`;
      ctx.lineWidth = fs * 0.16; ctx.strokeStyle = '#0b0b0b'; ctx.strokeText(ln, 0, y);
      ctx.fillStyle = i === 0 ? (el.color || '#ffd60a') : '#ffffff'; ctx.fillText(ln, 0, y);
    });
    ctx.restore();
  }
  function drawEllipse(ctx, el, life) {
    const p = S.project({ lon: el.lon, lat: el.lat });
    if (!p) return;
    const prog = ease.outCubic(clamp01(life.age / 0.8));
    const rx = el.rx ?? 200, ry = el.ry ?? 140, rot = (el.rot ?? -0.25);
    ctx.save(); ctx.globalAlpha = life.out; ctx.translate(p[0], p[1]); ctx.rotate(rot);
    ctx.strokeStyle = el.color || '#ffd60a'; ctx.lineWidth = el.width || 6; ctx.lineCap = 'round'; ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 8;
    ctx.beginPath();
    const a0 = -Math.PI * 0.55, a1 = a0 + TAU * 1.06 * prog;
    for (let a = a0; a <= a1; a += 0.04) {
      const k = 1 + 0.03 * Math.sin(a * 2.7) + (a - a0) * 0.006, x = Math.cos(a) * rx * k, y = Math.sin(a) * ry * k;
      if (a === a0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke(); ctx.restore();
  }
  function drawGlow(ctx, el, life, t) {
    const p = S.project({ lon: el.lon, lat: el.lat });
    if (!p) return;
    const k = state.view?.k || 1000;
    const r = el.km ? Math.max(30, (el.km / 6371) * k) : (el.r || 160);
    const pulse = 0.82 + 0.18 * Math.sin((t - el.start) * 4);
    const c = el.color || '#ff3b1f', c2 = el.color2 || 'rgba(255,200,0,0)';
    ctx.save(); ctx.globalCompositeOperation = 'screen'; ctx.globalAlpha = life.out * life.in * (el.alpha ?? 0.85) * pulse;
    const rr = r * (0.6 + 0.4 * ease.outCubic(clamp01(life.age / 0.8)));
    const g = ctx.createRadialGradient(p[0], p[1], 0, p[0], p[1], rr);
    g.addColorStop(0, c); g.addColorStop(0.55, el.mid || 'rgba(255,120,0,.45)'); g.addColorStop(1, c2);
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(p[0], p[1], rr * (el.stretch ?? 1), rr, el.rot ?? 0, 0, TAU); ctx.fill();
    ctx.restore();
  }
  function drawDisc(ctx, el, life, t) {
    const p = S.project({ lon: el.lon, lat: el.lat });
    if (!p) return;
    const k = state.view?.k || 1000;
    const r = (el.km ? Math.max(20, (el.km / 6371) * k) : (el.r || 200)) * ease.outCubic(clamp01(life.age / 0.7));
    ctx.save(); ctx.globalAlpha = life.out;
    const col = el.color || '#5ec8ff';
    ctx.fillStyle = col; ctx.globalAlpha = life.out * (el.alpha ?? 0.22);
    ctx.beginPath(); ctx.arc(p[0], p[1], r, 0, TAU); ctx.fill();
    ctx.globalAlpha = life.out; ctx.strokeStyle = col; ctx.lineWidth = el.width || 5; ctx.shadowColor = col; ctx.shadowBlur = 16;
    ctx.beginPath(); ctx.arc(p[0], p[1], r * (1 + 0.012 * Math.sin((t - el.start) * 5)), 0, TAU); ctx.stroke();
    ctx.restore();
  }
  function drawCrack(ctx, el, life) {
    const y0 = (el.y ?? 0.45) * H, prog = ease.outCubic(clamp01(life.age / 0.5)), grow = clamp01((life.age - 0.4) / 0.8);
    const n = 26, pts = [];
    for (let i = 0; i <= n; i++) { const r = Math.sin((i + (el.seed || 3)) * 91.7) * 43758.5; const j = (r - Math.floor(r) - 0.5); pts.push([(i / n) * W, y0 + j * 90 + (i % 2 ? 18 : -18)]); }
    ctx.save(); ctx.globalAlpha = life.out; ctx.lineJoin = 'miter';
    const upto = Math.floor(n * prog);
    for (const [w, col] of [[10 + 46 * grow, '#ffffff'], [4 + 40 * grow, '#050505']]) {
      ctx.strokeStyle = col; ctx.lineWidth = w; ctx.beginPath();
      for (let i = 0; i <= upto; i++) { if (i) ctx.lineTo(pts[i][0], pts[i][1]); else ctx.moveTo(pts[i][0], pts[i][1]); }
      ctx.stroke();
    }
    ctx.restore();
  }


  // ------------------------------------------------------------------ siege (walls under cannon fire)
  // wall element with `siege: {cannons, shots, delay, dist}`: cannons line up outside the wall, take turns
  // firing; every ball flies in an arc, hits the stone, throws debris and dust, and the hit sections
  // crumble away. Everything is a pure function of time (shot i fires at a fixed moment).
  const stoneCol = ['#d6c7a1', '#c2b184', '#a89868', '#8e7f58'];
  function wallGeom(el) {
    if (el._sg && el._sgT === state.t) return el._sg;
    const pts = S.screenPolyline(el._pts || []);
    const cum = [0];
    for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    const L = cum[cum.length - 1] || 1;
    const side = el.side ?? 1;
    const at = (d) => {
      d = Math.max(0, Math.min(L, d));
      let i = 1;
      while (i < pts.length - 1 && cum[i] < d) i++;
      const a = pts[i - 1], b = pts[i], seg = cum[i] - cum[i - 1] || 1, f = (d - cum[i - 1]) / seg;
      const dx = (b[0] - a[0]) / seg, dy = (b[1] - a[1]) / seg;
      return { x: a[0] + (b[0] - a[0]) * f, y: a[1] + (b[1] - a[1]) * f, nx: -dy * side, ny: dx * side };
    };
    el._sgT = state.t;
    return (el._sg = { pts, cum, L, at });
  }
  function siegeShots(el) {
    if (el._shots) return el._shots;
    const sg = el.siege, n = sg.shots ?? 11, nC = sg.cannons ?? 4, delay = sg.delay ?? 1.4;
    const dur = Math.max(2.5, el.end - el.start);
    const T = Math.max(0.28, (dur * 0.8 - delay) / Math.max(1, n - 1));
    const cs = sg.targets || [0.36, 0.62];
    el._shots = Array.from({ length: n }, (_, i) => ({
      i, t: el.start + delay + i * T, cannon: i % nC, c: cs[i % cs.length] + (hash01(i * 3.7 + 1) - 0.5) * 0.03, fly: 0.45, last: i >= n - 2,
    }));
    return el._shots;
  }
  // stretches of wall (px along it) that have crumbled by time t
  function wallBreaches(el, t) {
    if (!el.siege) return [];
    const g = wallGeom(el), cs = el.siege.targets || [0.36, 0.62];
    const cap = g.L * 0.1;
    return cs.map((c, j) => {
      let w = 0;
      for (const sh of siegeShots(el)) {
        if (Math.abs(sh.c - c) > 0.05) continue;
        const a = (t - (sh.t + sh.fly)) / 0.3;
        if (a > 0) w += g.L * (sh.last ? 0.045 : 0.02) * ease.outCubic(clamp01(a));
      }
      w = Math.min(cap, w);
      return w > 2 ? [c * g.L - w, c * g.L + w] : null;
    }).filter(Boolean);
  }
  function puff(ctx, x, y, r, a, col) {
    if (a <= 0.01) return;
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, rgba(col, a)); g.addColorStop(0.6, rgba(col, a * 0.55)); g.addColorStop(1, rgba(col, 0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
  }
  function drawSiege(ctx, el, life, t) {
    const g = wallGeom(el);
    if (g.pts.length < 2) return;
    const sg = el.siege, nC = sg.cannons ?? 4, D = sg.dist ?? 300, size = sg.size ?? 170;
    const cimg = img('/assets/art/cannon.png');
    // cannon positions: spread along the wall, outside it
    const cannons = Array.from({ length: nC }, (_, i) => {
      const f = 0.2 + 0.6 * ((i + 0.5) / nC), base = g.at(f * g.L);
      const d = D * (0.85 + 0.3 * hash01(i + 5));
      return { x: Math.min(W - 90, Math.max(90, base.x + base.nx * d)), y: Math.min(H * 0.74, Math.max(480, base.y + base.ny * d)), f };
    });
    const shots = siegeShots(el);
    ctx.save();
    ctx.globalAlpha = life.out;
    // cannons (appear one after another, recoil when they fire)
    cannons.forEach((c, i) => {
      const appear = ease.outBack(clamp01((t - el.start - 0.15 * i) / 0.4));
      if (appear <= 0) return;
      const mine = shots.filter((s) => s.cannon === i && t >= s.t);
      const last = mine.length ? mine[mine.length - 1] : null;
      const tgt = g.at(shots.find((s) => s.cannon === i)?.c * g.L || g.L / 2);
      const ang = Math.atan2(tgt.y - c.y, tgt.x - c.x);
      const rc = last ? Math.exp(-(t - last.t) / 0.12) : 0;
      ctx.save();
      ctx.translate(c.x - Math.cos(ang) * 16 * rc, c.y - Math.sin(ang) * 16 * rc);
      ctx.rotate(ang);
      if (Math.cos(ang) < 0) { ctx.rotate(Math.PI); ctx.scale(-1, 1); }
      ctx.scale(appear, appear);
      if (cimg) ctx.drawImage(cimg, -size / 2, -size * 0.34, size, size * (cimg.height / cimg.width));
      ctx.restore();
    });
    // flights, muzzle smoke, impacts
    for (const sh of shots) {
      const c = cannons[sh.cannon], tg = g.at(sh.c * g.L);
      const dt = t - sh.t;
      if (dt < -0.05 || dt > 3.2) continue;
      const ang = Math.atan2(tg.y - c.y, tg.x - c.x);
      const mx = c.x + Math.cos(ang) * size * 0.45, my = c.y + Math.sin(ang) * size * 0.45;
      // muzzle flash + smoke
      if (dt >= 0) {
        if (dt < 0.14) { ctx.save(); ctx.globalCompositeOperation = 'screen'; puff(ctx, mx, my, 70 * (1 - dt / 0.2), 1 - dt / 0.14, '#ffc24a'); ctx.restore(); }
        for (let k = 0; k < 4; k++) puff(ctx, mx - Math.cos(ang) * 10 * k + (hash01(sh.i * 9 + k) - 0.5) * 30, my - dt * (30 + 20 * k) - 6, 24 + 70 * dt + 8 * k, Math.max(0, 0.45 * (1 - dt / 1.6)), '#cfcfcf');
      }
      // ball in the air
      if (dt >= 0 && dt <= sh.fly) {
        const u = dt / sh.fly, bx = mx + (tg.x - mx) * u, by = my + (tg.y - my) * u - 130 * Math.sin(Math.PI * u);
        ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.beginPath(); ctx.ellipse(bx, by + 130 * Math.sin(Math.PI * u) * 0.9, 10, 5, 0, 0, TAU); ctx.fill();
        ctx.fillStyle = '#17120d'; ctx.beginPath(); ctx.arc(bx, by, 9, 0, TAU); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.beginPath(); ctx.arc(bx - 3, by - 3, 3, 0, TAU); ctx.fill();
      }
      // impact: flash, debris, dust (the last hits are bigger)
      const ia = dt - sh.fly;
      if (ia >= 0) {
        const K = sh.last ? 1.9 : 1;
        if (ia < 0.2) { ctx.save(); ctx.globalCompositeOperation = 'screen'; puff(ctx, tg.x, tg.y, 90 * K * (0.5 + ia * 3), 1 - ia / 0.2, '#ffb347'); ctx.restore(); }
        for (let k = 0; k < 9; k++) {
          const ang2 = hash01(sh.i * 13 + k) * TAU, sp = (140 + 220 * hash01(sh.i * 7 + k * 3)) * K;
          const px = tg.x + Math.cos(ang2) * sp * ia, py = tg.y + Math.sin(ang2) * sp * ia * 0.6 - 260 * ia + 900 * ia * ia * 0.5;
          const al = Math.max(0, 1 - ia / 1.1);
          if (al <= 0) continue;
          ctx.save(); ctx.translate(px, py); ctx.rotate(ia * 8 * (k % 2 ? 1 : -1) + k);
          ctx.fillStyle = rgba(stoneCol[k % 4], al); ctx.fillRect(-6 * K, -5 * K, 12 * K, 9 * K); ctx.restore();
        }
        for (let k = 0; k < 4; k++) puff(ctx, tg.x + (hash01(sh.i + k) - 0.5) * 70 * K, tg.y - ia * 40 - k * 6, (26 + 90 * ia) * K * (0.7 + 0.15 * k), Math.max(0, 0.55 * (1 - ia / (sh.last ? 2.4 : 1.3))), '#b9a98a');
      }
    }
    // rubble where the wall has fallen
    for (const [d0, d1] of wallBreaches(el, t)) {
      for (let k = 0; k < 9; k++) {
        const d = d0 + (d1 - d0) * hash01(d0 * 0.13 + k), p = g.at(d);
        ctx.fillStyle = stoneCol[k % 4];
        ctx.save(); ctx.translate(p.x + p.nx * (hash01(k * 5 + d0) * 14), p.y + p.ny * (hash01(k * 5 + d0) * 14 + 4)); ctx.rotate(k * 1.7);
        ctx.fillRect(-7, -5, 14, 10); ctx.strokeStyle = '#3f3524'; ctx.lineWidth = 1.5; ctx.strokeRect(-7, -5, 14, 10); ctx.restore();
      }
    }
    ctx.restore();
  }
  // camera kick on every hit
  function shakeAt(t) {
    let dx = 0, dy = 0;
    for (const el of state.tl.elements) {
      if (el.type !== 'wall' || !el.siege || t < el.start || t > el.end + 0.5) continue;
      for (const sh of siegeShots(el)) {
        const a = t - (sh.t + sh.fly);
        if (a < 0 || a > 0.35) continue;
        const k = 1 - a / 0.35, amp = (sh.last ? 22 : 9) * k * k;
        dx += amp * Math.sin(a * 91 + sh.i); dy += amp * Math.cos(a * 77 + sh.i);
      }
    }
    for (const el of state.tl.elements) {
      if (el.type !== 'eruption' || t < el.start || t > el.end) continue;
      const a = t - el.start;
      const amp = (el.shake ?? 6) * clamp01(a / 0.3) * clamp01((el.end - t) / 0.6);
      dx += amp * Math.sin(t * 61); dy += amp * Math.cos(t * 53);
    }
    return [dx, dy];
  }

  // ------------------------------------------------------------------ volcano eruption
  // lava fountain (ballistic glowing particles), lava streams creeping down the slopes, an ash plume
  // and a pulsing glow at the crater. `size` = on-screen height of the volcano art (the crater is near its top).
  function drawEruption(ctx, el, life, t) {
    const p = S.project({ lon: el.lon, lat: el.lat });
    if (!p) return;
    const size = el.size || 190, age = t - el.start;
    const cx = p[0] + (el.craterDx ?? 0), cy = p[1] - size * (el.craterDy ?? 0.3);
    const ramp = ease.outCubic(clamp01(age / 0.7)) * life.out;
    ctx.save();
    // opening flash
    if (age < 0.35) { ctx.globalCompositeOperation = 'screen'; puff(ctx, cx, cy, size * 1.6 * (0.4 + age * 2), 0.9 * (1 - age / 0.35), '#fff1b0'); ctx.globalCompositeOperation = 'source-over'; }
    // ash plume rising from the crater
    for (let i = 0; i < 12; i++) {
      const per = 2.6 + hash01(i) * 1.2, a = ((age + hash01(i + 9) * per) % per) / per;
      const x = cx + Math.sin(i * 2.1 + a * 3) * size * 0.25 + a * size * 0.5 * (el.wind ?? 1), y = cy - a * size * 2.2 - 10;
      puff(ctx, x, y, size * (0.18 + 0.5 * a), 0.5 * (1 - a) * ramp, i % 3 ? '#3c3835' : '#6b645d');
    }
    // lava streams creeping down the flanks
    ctx.globalCompositeOperation = 'screen';
    for (let i = 0; i < 4; i++) {
      const dir = i % 2 ? 1 : -1, len = size * (0.55 + 0.25 * hash01(i + 3)), u = ease.outCubic(clamp01((age - 0.4 - i * 0.15) / 2.0));
      if (u <= 0) continue;
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      for (const [w, col] of [[14, 'rgba(255,90,20,.35)'], [7, 'rgba(255,150,40,.9)'], [3, 'rgba(255,230,140,.95)']]) {
        ctx.strokeStyle = col; ctx.lineWidth = w * (0.8 + 0.2 * Math.sin(t * 5 + i)); ctx.globalAlpha = ramp;
        ctx.beginPath(); ctx.moveTo(cx, cy + 6);
        const steps = 14;
        for (let k = 1; k <= steps * u; k++) {
          const f = k / steps;
          ctx.lineTo(cx + dir * (f * len * 0.8 + Math.sin(f * 7 + i * 2) * 10), cy + 6 + f * len * (0.9 + 0.15 * hash01(i + 1)));
        }
        ctx.stroke();
      }
    }
    // fountain of glowing lava bombs
    ctx.globalAlpha = 1;
    for (let i = 0; i < 90; i++) {
      const per = 1.1 + hash01(i * 1.7) * 0.9, a = ((age + hash01(i + 40) * per) % per) / per;
      if (age < 0.05) break;
      const ang = -Math.PI / 2 + (hash01(i * 3.1) - 0.5) * 1.5, v = size * (1.3 + 1.1 * hash01(i * 5.3));
      const x = cx + Math.cos(ang) * v * a * per * 0.9, y = cy + Math.sin(ang) * v * a * per * 0.9 + size * 1.6 * (a * per) * (a * per) * 0.9;
      const r = 3 + 6 * hash01(i * 9.1) * (1 - a * 0.5);
      const col = a < 0.35 ? '#ffe28a' : a < 0.7 ? '#ff7a1f' : '#7a1d0d';
      ctx.globalAlpha = ramp * (1 - a * a);
      ctx.shadowColor = '#ff6a00'; ctx.shadowBlur = 14;
      ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
    }
    ctx.shadowBlur = 0; ctx.globalAlpha = 1;
    // glow at the crater
    puff(ctx, cx, cy + 4, size * 0.7, (0.55 + 0.2 * Math.sin(t * 9)) * ramp, '#ff6a1f');
    ctx.restore();
  }

  // ------------------------------------------------------------------ hooks called by main.js
  function drawGeo(ctx, t) {
    for (const el of state.tl.elements) {
      const t0 = el.type;
      if (!['pathtext', 'crowd', 'face', 'pin', 'box', 'beam', 'cloud', 'callout', 'ellipse', 'glow', 'crack', 'disc', 'eruption'].includes(t0) && !(t0 === 'wall' && el.siege)) continue;
      const life = lifeOf(el, t, 0.3, 0.3);
      if (!life) continue;
      if (t0 === 'pathtext') drawPathText(ctx, el, life);
      else if (t0 === 'crowd') drawCrowd(ctx, el, life, t);
      else if (t0 === 'face') drawFace(ctx, el, life, t);
      else if (t0 === 'pin') drawPin(ctx, el, life);
      else if (t0 === 'box') drawBox(ctx, el, life);
      else if (t0 === 'beam') drawBeam(ctx, el, life, t);
      else if (t0 === 'cloud') drawClouds(ctx, el, life, t);
      else if (t0 === 'callout') drawCallout(ctx, el, life);
      else if (t0 === 'ellipse') drawEllipse(ctx, el, life);
      else if (t0 === 'glow') drawGlow(ctx, el, life, t);
      else if (t0 === 'crack') drawCrack(ctx, el, life);
      else if (t0 === 'disc') drawDisc(ctx, el, life, t);
      else if (t0 === 'eruption') drawEruption(ctx, el, life, t);
      else if (t0 === 'wall') drawSiege(ctx, el, life, t);
    }
  }
  function drawUnder(ctx, t) {
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, W, H);
    for (const el of state.tl.elements) {
      if (el.type !== 'link') continue;
      const life = lifeOf(el, t, 0.3, 0.3);
      if (life) drawLink(ctx, el, life);
    }
  }
  function drawOver(ctx, t) {
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, W, H);
    for (const el of state.tl.elements) {
      if (!['particles', 'flare', 'react'].includes(el.type)) continue;
      const life = lifeOf(el, t, 0.3, 0.4);
      if (!life) continue;
      if (el.type === 'particles') drawParticles(ctx, el, life, t);
      else if (el.type === 'flare') drawFlare(ctx, el, life, t);
      else if (el.burst) drawBurst(ctx, el, life);
    }
  }

  // ------------------------------------------------------------------ DOM element markup
  const esc = S.esc;
  function html(el) {
    switch (el.type) {
      case 'photo': {
        const full = el.kind === 'full';
        const s = el.size || 560;
        return `<div class="inner photo ${full ? 'full' : 'card'}" style="${full ? '' : `width:${s}px;height:${s * (el.ratio ?? 0.68)}px`}"><div class="ph"><img src="/assets/broll/${el.image}.jpg"></div>${el.caption ? `<div class="cap-l">${esc(el.caption)}</div>` : ''}</div>`;
      }
      case 'avatar': {
        const s = el.size || 170;
        return `<div class="inner avatar ${el.shape || 'hex'}" style="width:${s}px;height:${s}px"><div class="frame"><img src="/assets/characters/${el.image}.png"></div>${el.name ? `<div class="an">${esc(el.name)}</div>` : ''}</div>`;
      }
      case 'react':
        return `<div class="inner react"><img src="${el.src}" style="width:${el.size || 150}px;height:auto"></div>`;
      case 'timebar': {
        return `<div class="inner timebar" style="width:${el.width || 820}px"><div class="tb-track"><div class="tb-fill"></div><div class="tb-knob"></div></div><div class="tb-y a">${esc(el.from)}</div><div class="tb-y b">${esc(el.to)}</div><div class="tb-l">${esc(el.label || '')}</div><div class="tb-c"></div></div>`;
      }
      case 'orbit': {
        const R = el.radius || 300;
        return `<div class="inner orbit" style="width:${R * 2}px;height:${R * 2}px"><div class="ring"></div><div class="mid">${esc(el.text || '')}</div>${(el.items || []).map((t) => `<div class="it"><i></i><b>${esc(t)}</b></div>`).join('')}</div>`;
      }
      case 'tally':
        return `<div class="inner tally">${(el.items || []).map((it) => `<div class="tr"><img src="/assets/art/${String(it.icon || '').replace('art:', '')}.png"><b data-v="${it.value}" data-p="${esc(it.prefix || '')}" data-s="${esc(it.suffix || '')}">0</b><span>${esc(it.label || '')}</span></div>`).join('')}</div>`;
      case 'handstamp':
        return `<div class="inner handstamp"><div class="hs-text" style="font-size:${el.size || 96}px">${esc(el.text)}</div><div class="hs-tool"><i class="knob"></i><i class="neck"></i><i class="base"></i></div></div>`;
      case 'clip': {
        const w = el.size || 540, h = Math.round(w * (el.ratio ?? 0.5625));
        return `<div class="inner clip ${el.blend === 'screen' ? 'screen' : ''}" style="width:${w}px;height:${h}px;${el.round ? 'border-radius:24px;overflow:hidden;' : ''}${el.blend === 'screen' ? 'mix-blend-mode:screen;' : ''}"><canvas width="${w}" height="${h}"></canvas></div>`;
      }
      case 'lens': {
        const D = (el.r || 300) * 2;
        return `<div class="inner lens" style="width:${D}px;height:${D}px"><canvas width="${D}" height="${D}"></canvas><div class="rim"></div><div class="handle"></div></div>`;
      }
      default:
        return null;
    }
  }

  // per-frame DOM animation: returns tweaks {scale, rot, opacity, dx, dy}
  function anim(el, inner, life, t) {
    const tw = { scale: 1, rot: 0, opacity: 1, dx: 0, dy: 0 };
    switch (el.type) {
      case 'photo': {
        const im = inner.querySelector('img');
        const u = clamp01(life.age / Math.max(0.5, el.end - el.start));
        const pan = el.pan || 'in';
        const z = pan === 'out' ? 1.22 - 0.2 * u : 1.02 + 0.2 * u;
        const off = pan === 'left' ? -60 * u : pan === 'right' ? 60 * u : 0;
        im.style.transform = `scale(${z}) translateX(${off}px)`;
        if (el.kind === 'full') { tw.opacity = ease.outCubic(life.in); tw.scale = 1; }
        else {
          const from = el.from || 'right';
          const a = ease.outCubic(clamp01(life.age / 0.5));
          tw.dx = (from === 'left' ? -1 : from === 'right' ? 1 : 0) * (1 - a) * W * 0.8;
          tw.dy = (from === 'top' ? -1 : from === 'bottom' ? 1 : 0) * (1 - a) * H * 0.6;
          tw.rot = (el.rot ?? -4) + (1 - a) * 10;
          inner.style.filter = a < 1 ? `blur(${(1 - a) * 12}px)` : '';
          tw.scale = 0.9 + 0.1 * a;
        }
        break;
      }
      case 'avatar': {
        tw.scale = ease.outBack(life.in);
        tw.rot = Math.sin(t * 1.4 + (el.seed || 0)) * 2;
        break;
      }
      case 'react': {
        const a = clamp01(life.age / 0.45);
        tw.scale = ease.outBack(a) * (1 + 0.04 * Math.sin(t * 9));
        const shake = el.shake === false ? 0 : Math.max(0, 1 - life.age / 0.8);
        tw.rot = (el.rot || 0) + Math.sin(life.age * 40) * 7 * shake;
        tw.dy = -ease.outCubic(a) * 20;
        break;
      }
      case 'timebar': {
        const u = ease.inOutCubic(clamp01((life.age - 0.25) / (el.dur ?? 1.3)));
        inner.querySelector('.tb-fill').style.width = `${u * 100}%`;
        inner.querySelector('.tb-knob').style.left = `${u * 100}%`;
        const y0 = parseInt(el.from, 10), y1 = parseInt(el.to, 10);
        inner.querySelector('.tb-c').textContent = Number.isFinite(y0) && Number.isFinite(y1) ? String(Math.round(y0 + (y1 - y0) * u)) : '';
        tw.scale = ease.outBack(life.in);
        break;
      }
      case 'tally': {
        inner.querySelectorAll('.tr').forEach((n, i) => {
          const u = ease.outCubic(clamp01((life.age - 0.15 - i * (el.stagger ?? 0.35)) / 0.9));
          const b = n.querySelector('b'), v = Number(b.dataset.v);
          b.textContent = `${b.dataset.p}${Math.round(v * u).toLocaleString('en-US')}${b.dataset.s}`;
          n.style.opacity = String(clamp01(u * 3));
          n.style.transform = `translateX(${(1 - u) * -80}px)`;
        });
        tw.scale = ease.outBack(life.in);
        break;
      }
      case 'orbit': {
        const items = inner.querySelectorAll('.it');
        const R = el.radius || 300, sp = el.speed ?? 0.5;
        items.forEach((n, i) => {
          const a = (i / items.length) * TAU + life.age * sp - Math.PI / 2;
          n.style.transform = `translate(${R + Math.cos(a) * R}px, ${R + Math.sin(a) * R}px) translate(-50%,-50%)`;
          n.style.opacity = String(ease.outCubic(clamp01((life.age - i * 0.1) / 0.4)));
        });
        tw.scale = ease.outBack(life.in);
        break;
      }
      case 'handstamp': {
        // a rubber stamp drops straight down onto the text, exactly as wide as the text, presses, lifts away
        const a = life.age;
        const tool = inner.querySelector('.hs-tool'), tx = inner.querySelector('.hs-text');
        const w = tx.offsetWidth + 24, h = tx.offsetHeight + 16;
        tool.style.width = w + 'px'; tool.style.left = '50%'; tool.style.marginLeft = -(w / 2) + 'px';
        const base = tool.querySelector('.base'); base.style.height = h + 'px'; tool.style.bottom = `calc(50% - ${h / 2}px)`;
        const down = ease.inCubic(clamp01(a / 0.38));
        const up = ease.outCubic(clamp01((a - 0.62) / 0.4));
        const press = clamp01((a - 0.38) / 0.1) * (1 - clamp01((a - 0.5) / 0.12));
        tool.style.transform = `translateY(${(-1 + down) * 900 - up * 900 + press * 6}px) scaleY(${1 - press * 0.04})`;
        tool.style.opacity = String(1 - clamp01((a - 1.0) / 0.15));
        const hit = clamp01((a - 0.38) / 0.06);
        tx.style.opacity = String(hit);
        tx.style.transform = `translate(-50%,-50%) rotate(-3deg) scale(${1 + (1 - hit) * 0.25})`;
        break;
      }
      case 'clip': {
        // frame sequence from assets/vfx/<name>/: shows the frame for the element's own time (looping optional)
        const cv = inner.querySelector('canvas'), cx = cv.getContext('2d');
        const n = el.n || 1, fps = el.fps || 24, sp = el.speed || 1;
        let k = Math.floor(life.age * fps * sp);
        k = el.loop ? k % n : Math.min(n - 1, k);
        const im = img(`/assets/vfx/${el.name}/f${String(k + 1).padStart(4, '0')}.${el.ext || 'webp'}`);
        cx.clearRect(0, 0, cv.width, cv.height);
        if (im) {
          // cover-fit
          const sc = Math.max(cv.width / im.width, cv.height / im.height);
          cx.drawImage(im, (cv.width - im.width * sc) / 2, (cv.height - im.height * sc) / 2, im.width * sc, im.height * sc);
        }
        tw.opacity = ease.outCubic(clamp01(life.age / 0.25)) * life.out;
        tw.scale = 0.96 + 0.04 * ease.outCubic(clamp01(life.age / 0.4));
        break;
      }
      case 'lens': {
        const a = ease.outCubic(clamp01(life.age / 0.55));
        tw.scale = 2.6 - 1.6 * a;
        tw.rot = -14 * (1 - a);
        tw.opacity = clamp01(life.age / 0.15) * life.out;
        drawLensContent(el, inner);
        break;
      }
      default:
        break;
    }
    return tw;
  }

  // the lens shows the current frame magnified around its centre
  function drawLensContent(el, inner) {
    const cv = inner.querySelector('canvas');
    if (!cv || !el._scr) return;
    const cx = cv.getContext('2d');
    const D = cv.width, mag = el.mag || 1.9;
    cx.setTransform(1, 0, 0, 1, 0, 0);
    cx.clearRect(0, 0, D, D);
    const [x, y] = el._scr;
    const sw = D / mag;
    for (const id of ['space', 'raster', 'vector', 'paper', 'marks']) {
      const c = document.getElementById(id);
      if (!c || c.style.display === 'none') continue;
      const k = c.width / W;
      cx.globalCompositeOperation = id === 'paper' ? 'multiply' : 'source-over';
      try { cx.drawImage(c, (x - sw / 2) * k, (y - sw / 2) * k, sw * k, sw * k, 0, 0, D, D); } catch { /* tainted or lost context: skip */ }
    }
  }

  // ------------------------------------------------------------------ transitions (overlay html)
  function fxHtml(t) {
    let out = '';
    let blur = 0;
    for (const s of state.tl.scenes) {
      const tr = s.transition;
      if (!tr) continue;
      const d = t - s.start;
      if (tr === 'blast' && d > -0.1 && d < 1.5) {
        // white bloom -> orange -> purple -> dark
        const u = clamp01((d + 0.1) / 1.6);
        const stops = [[0, [255, 255, 255, 1]], [0.22, [255, 200, 90, 0.9]], [0.5, [255, 90, 40, 0.75]], [0.72, [120, 30, 150, 0.6]], [1, [10, 8, 20, 0]]];
        let c = stops[0][1];
        for (let i = 1; i < stops.length; i++) if (u <= stops[i][0]) { const f = (u - stops[i - 1][0]) / (stops[i][0] - stops[i - 1][0]); c = stops[i - 1][1].map((v, k) => v + (stops[i][1][k] - v) * f); break; }
        out += `<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 45%, rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${c[3]}) 0%, rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${c[3] * 0.85}) 100%)"></div>`;
        blur = Math.max(blur, 12 * Math.sin(Math.PI * Math.min(1, u * 1.4)));
      } else if (tr === 'ice' && d > -0.3 && d < 0.7) {
        const u = clamp01((d + 0.3) / 1.0);
        const grow = ease.inOutCubic(u < 0.5 ? u * 2 : 2 - u * 2);   // frost creeps in, then melts off
        for (let k = 0; k < 46; k++) {
          const x = hash01(k * 5.1) * W, y = hash01(k * 8.3) * H, r = (60 + hash01(k * 3.9) * 260) * grow;
          out += `<div style="position:absolute;left:${x - r}px;top:${y - r}px;width:${r * 2}px;height:${r * 2}px;border-radius:50%;background:radial-gradient(circle, rgba(235,246,255,.95) 0%, rgba(215,236,252,.75) 55%, rgba(215,236,252,0) 100%)"></div>`;
        }
      } else if (tr === 'rewind' && d > -0.2 && d < 0.9) {
        const u = clamp01((d + 0.2) / 1.1), a = Math.sin(Math.PI * u);
        const f = Math.floor(t * 24);
        for (let k = 0; k < 9; k++) {
          const top = hash01(f * 11 + k * 3) * H, hh = 14 + hash01(f + k * 17) * 80, off = (hash01(f * 5 + k) - 0.5) * 160 * a;
          out += `<div style="position:absolute;left:0;right:0;top:${top}px;height:${hh}px;transform:translateX(${off}px);background:rgba(255,255,255,.16);mix-blend-mode:screen"></div>`;
        }
        out += `<div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0 2px, transparent 2px 5px);opacity:${a}"></div>`;
        out += `<div style="position:absolute;inset:0;background:rgba(60,110,255,${0.16 * a})"></div>`;
        // double-triangle rewind glyph
        const gx = 70, gy = 150, s = 46;
        out += `<div style="position:absolute;left:${gx}px;top:${gy}px;opacity:${a};display:flex"><div style="width:0;height:0;border-top:${s / 2}px solid transparent;border-bottom:${s / 2}px solid transparent;border-right:${s}px solid #fff;filter:drop-shadow(0 3px 6px rgba(0,0,0,.6))"></div><div style="width:0;height:0;border-top:${s / 2}px solid transparent;border-bottom:${s / 2}px solid transparent;border-right:${s}px solid #fff;filter:drop-shadow(0 3px 6px rgba(0,0,0,.6))"></div></div>`;
        blur = Math.max(blur, 5 * a);
      } else if (tr === 'ink' && d > -0.25 && d < 0.6) {
        const u = clamp01((d + 0.25) / 0.85), g = ease.inOutCubic(u < 0.5 ? u * 2 : 2 - u * 2);
        for (let k = 0; k < 30; k++) {
          const x = hash01(k * 4.3) * W, y = hash01(k * 6.7) * H, r = (90 + hash01(k * 2.1) * 300) * g;
          out += `<div style="position:absolute;left:${x - r}px;top:${y - r}px;width:${r * 2}px;height:${r * 2}px;border-radius:50%;background:radial-gradient(circle, rgba(8,10,20,.98) 0%, rgba(8,10,20,.9) 65%, rgba(8,10,20,0) 100%)"></div>`;
        }
      }
    }
    return { html: out, blur };
  }

  // ------------------------------------------------------------------ colour grades
  function grade(t) {
    const parts = [];
    for (const el of state.tl.elements) {
      if (el.type !== 'grade') continue;
      const life = lifeOf(el, t, 0.5, 0.5);
      if (!life) continue;
      const a = ease.inOutSine(life.in) * ease.inOutSine(life.out) * (el.amount ?? 1);
      switch (el.mode) {
        case 'bw': parts.push(`grayscale(${a}) contrast(${1 + 0.15 * a}) brightness(${1 - 0.15 * a})`); break;
        case 'thermal': parts.push(`sepia(${0.65 * a}) hue-rotate(${-28 * a}deg) saturate(${1 + 1.1 * a}) contrast(${1 + 0.12 * a})`); break;
        case 'sepia': parts.push(`sepia(${0.8 * a}) contrast(${1 + 0.05 * a})`); break;
        case 'danger': parts.push(`saturate(${1 + 0.35 * a}) hue-rotate(${-10 * a}deg) contrast(${1 + 0.1 * a}) brightness(${1 - 0.1 * a})`); break;
        case 'cold': parts.push(`hue-rotate(${18 * a}deg) saturate(${1 - 0.15 * a}) brightness(${1 + 0.04 * a})`); break;
        case 'dusk': parts.push(`sepia(${0.35 * a}) hue-rotate(${-15 * a}deg) brightness(${1 - 0.3 * a}) saturate(${1 + 0.3 * a})`); break;
        default: break;
      }
    }
    return parts.join(' ');
  }

  // round-9 toolbox (extras2.js): merged in front of the originals
  const X2 = makeExtras2(S);
  const w = (a, b) => (...args) => { a(...args); b(...args); };
  return {
    prepare: w(prepare, X2.prepare), drawGeo: w(drawGeo, X2.drawGeo), drawUnder, drawOver: w(drawOver, X2.drawOver),
    html: (el) => html(el) ?? X2.html(el),
    anim: (el, inner, life, t) => (TYPES2.includes(el.type) ? X2.anim(el, inner, life, t) : anim(el, inner, life, t)),
    fxHtml: (t) => { const a = fxHtml(t), b = X2.fxHtml(t); return { html: a.html + b, blur: a.blur }; },
    grade, wallBreaches, shakeAt };
}
