// Camera path: each scene flies from wherever the camera is to its target, with a
// log-space zoom "dip" on long moves so both ends stay in view, then drifts in slowly.
import { geoInterpolate, geoDistance, geoOrthographic, geoMercator } from 'd3-geo';

export const ease = {
  inOutCubic: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  outCubic: (t) => 1 - Math.pow(1 - t, 3),
  outBack: (t) => {
    const c1 = 1.70158, c3 = c1 + 1;
    return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
  },
  inOutSine: (t) => -(Math.cos(Math.PI * t) - 1) / 2,
};

export const clamp01 = (x) => Math.max(0, Math.min(1, x));

export function makeProjection(view) {
  if (view.mode === 'globe') {
    return geoOrthographic()
      .rotate([-view.lon, -view.lat])
      .scale(view.k)
      .translate([view.cx, view.cy])
      .clipAngle(90)
      .precision(0.3);
  }
  return geoMercator()
    .rotate([-view.lon, 0])
    .center([0, view.lat])
    .scale(view.k)
    .translate([view.cx, view.cy])
    .precision(0.3);
}

export class CameraPath {
  // shots: [{start, end, target:{lat,lon,zoom}|null, duration, lead}]
  constructor(shots, intro, opts) {
    this.opts = opts; // {W, baseK, drift}
    this.segs = [];
    let prev = null;
    for (const s of shots) {
      if (!s.target) {
        if (prev) this.segs.push({ ...prev, keep: true, start: s.start });
        continue;
      }
      const t0 = Math.max(0, s.start - (s.lead ?? 0.1));
      const from = prev ? this._evalSeg(prev, t0) : intro;
      const seg = { t0, dur: s.duration, from, to: s.target, start: s.start };
      seg.dip = this._dip(from, s.target);
      this.segs.push(seg);
      prev = seg;
    }
    this.intro = intro;
  }

  _dip(a, b) {
    const d = geoDistance([a.lon, a.lat], [b.lon, b.lat]);
    const { W, baseK } = this.opts;
    const need = W / (baseK * Math.max(d * 1.5, 1e-4));
    const gm = Math.sqrt(a.zoom * b.zoom);
    if (need >= gm) return null;
    return Math.log(need);
  }

  _evalSeg(seg, t) {
    const u = clamp01((t - seg.t0) / seg.dur);
    const drift = this.opts.drift;
    if (u >= 1) {
      const dt = t - (seg.t0 + seg.dur);
      return { lat: seg.to.lat, lon: seg.to.lon, zoom: seg.to.zoom * Math.exp(drift * dt) };
    }
    const e = ease.inOutCubic(u);
    const interp = geoInterpolate([seg.from.lon, seg.from.lat], [seg.to.lon, seg.to.lat]);
    const [lon, lat] = interp(e);
    const l0 = Math.log(seg.from.zoom), l1 = Math.log(seg.to.zoom);
    let lz;
    if (seg.dip != null) {
      // quadratic bezier in log space whose midpoint equals the dip
      const c = 2 * seg.dip - 0.5 * (l0 + l1);
      lz = (1 - e) * (1 - e) * l0 + 2 * e * (1 - e) * c + e * e * l1;
    } else {
      lz = l0 + (l1 - l0) * e;
    }
    return { lat, lon, zoom: Math.exp(lz) };
  }

  at(t) {
    let seg = null;
    for (const s of this.segs) if (s.t0 <= t) seg = s;
    if (!seg) return this.intro;
    return this._evalSeg(seg, t);
  }
}
