// WebGL2 satellite renderer. For every screen pixel it inverts the SAME projection
// d3 uses for the vector overlay (orthographic globe or Mercator), so imagery and
// borders line up exactly at any zoom.

// Up to this many Sentinel-2 detail textures (texture units 1..MAX_DETAIL).
const MAX_DETAIL = 4;

const VS = `#version 300 es
in vec2 aPos;
void main() { gl_Position = vec4(aPos, 0.0, 1.0); }`;

const FS = `#version 300 es
precision highp float;
uniform vec2 uRes;
uniform vec2 uCenter;      // projection translate, px, top-left origin
uniform float uK;          // projection scale (px per radian)
uniform float uLon0;       // radians
uniform float uLat0;       // radians
uniform float uMercY0;     // mercator y of lat0
uniform int uMode;         // 0 globe, 1 flat mercator
uniform float uAngle;      // post-projection rotation (radians, d3 projection.angle)
uniform float uAlpha;      // overall opacity of the imagery
uniform float uAtmo;       // atmosphere glow strength (globe)
uniform float uSepia;      // 0..1: flat-map tint for close-up shots (old map, dark map...)
uniform vec3 uTintLand;
uniform vec3 uTintSea;
uniform sampler2D uBase;
uniform sampler2D uLand;     // land polygons rasterised (white = land), for open-sea detection
uniform float uHasLand;
uniform float uNoGrade;    // night-lights base: keep it as it is
uniform vec2 uBaseSize;
uniform int uDetailCount;
uniform sampler2D uDetail0;
uniform sampler2D uDetail1;
uniform sampler2D uDetail2;
uniform sampler2D uDetail3;
uniform vec4 uDetailBox0;  // west, south, east, north (radians)
uniform vec4 uDetailBox1;
uniform vec4 uDetailBox2;
uniform vec4 uDetailBox3;
uniform vec4 uDetailMix;  // per box
out vec4 outColor;

const float PI = 3.141592653589793;

vec3 sampleEquirect(sampler2D tex, float lon, float lat) {
  vec2 uv = vec2((lon + PI) / (2.0 * PI), (PI * 0.5 - lat) / PI);
  vec2 dx = dFdx(uv), dy = dFdy(uv);
  dx.x -= round(dx.x); dy.x -= round(dy.x);   // seam at the antimeridian
  uv.x = fract(uv.x);
  return textureGrad(tex, uv, dx, dy).rgb;
}

vec4 sampleBox(sampler2D tex, vec4 box, float lon, float lat) {
  float u = (lon - box.x) / (box.z - box.x);
  float v = (box.w - lat) / (box.w - box.y);
  if (u < 0.0 || u > 1.0 || v < 0.0 || v > 1.0) return vec4(0.0);
  float edge = min(min(u, 1.0 - u), min(v, 1.0 - v));
  float w = smoothstep(0.0, 0.18, edge);
  vec4 t = texture(tex, vec2(u, v));
  return vec4(t.rgb, w * t.a);
}

// Map-like grade (reference channels use a bright, soft satellite look, not a dark photo):
// water becomes a clear teal that keeps its bathymetry, land is lifted and slightly softened.
float gMag = 1.0;

vec3 grade(vec3 c, vec3 cs, float openSea, vec3 cw, float flatSea) {
  // cs: a blurrier sample, used for the sea tone so JPEG blocks in the ocean don't show
  // cw: the colour water is detected on (the soft sample when the base is magnified, so rivers
  // and coasts don't turn into blue JPEG squares)
  float l = dot(cw, vec3(0.299, 0.587, 0.114));
  float ls = dot(cs, vec3(0.299, 0.587, 0.114));
  float water = smoothstep(0.015, 0.08, cw.b - max(cw.r, cw.g * 0.92)) * (1.0 - smoothstep(0.3, 0.5, l));
  // sharp close-up imagery: deep river / lake water is almost black, not blue; count it as water
  // unless it is green (forest), so it doesn't break up into dark squares
  water = max(water, flatSea * smoothstep(0.16, 0.08, l) * smoothstep(-0.015, 0.01, cw.b - cw.g * 0.95));
  // dark bluish pixels of sharp imagery (shaded sea, mosaic seams) are sea as well, never black patches
  water = max(water, flatSea * smoothstep(0.34, 0.22, l) * smoothstep(0.0, 0.02, cw.b - max(cw.r, cw.g * 0.97)));
  water = max(water, smoothstep(0.075, 0.04, l));   // black inland lakes in the base texture are water too
  water = max(water, openSea);
  // depth ramp: deep water dark teal, continental shelves bright turquoise (the bathymetry carries the map's character)
  vec3 sea = mix(vec3(0.06, 0.28, 0.38), vec3(0.30, 0.68, 0.74), pow(smoothstep(0.035, 0.3, ls), 1.3));
  vec3 land = pow(max(c, vec3(0.0)), vec3(0.8)) * 1.06;
  float ll = dot(land, vec3(0.299, 0.587, 0.114));
  // relief: local contrast from the difference to a blurred sample, a touch more saturation, gentle s-curve
  float coast = smoothstep(0.0, 0.05, cs.b - max(cs.r, cs.g * 0.92));   // no relief halo where the blur sees water
  land = max(land + (c - cs) * 1.1 * (1.0 - coast), vec3(0.0));
  ll = dot(land, vec3(0.299, 0.587, 0.114));
  land = mix(vec3(ll), land, 1.08);
  land = mix(land, land * land * (3.0 - 2.0 * min(land, vec3(1.0))), 0.35);
  // magnified far beyond the base image: bathymetry turns into JPEG blocks, so the sea goes flat
  // (the same for sharp close-up imagery, whose dark river water is full of JPEG blocks)
  sea = mix(sea, vec3(0.2, 0.47, 0.57), max(0.25 * smoothstep(0.7, 0.2, gMag), flatSea));
  return mix(land, sea, water);
}

// water the masked detail imagery knows about: inside the box, where the land mask left the pixel empty
float boxSea(sampler2D tex, vec4 box, float lon, float lat) {
  float u = (lon - box.x) / (box.z - box.x);
  float v = (box.w - lat) / (box.w - box.y);
  if (u < 0.0 || u > 1.0 || v < 0.0 || v > 1.0) return 0.0;
  float edge = min(min(u, 1.0 - u), min(v, 1.0 - v));
  return smoothstep(0.0, 0.18, edge) * (1.0 - texture(tex, vec2(u, v)).a);
}

vec3 sampleSoft(sampler2D tex, float lon, float lat) {
  vec2 uv = vec2((lon + PI) / (2.0 * PI), (PI * 0.5 - lat) / PI);
  vec2 dx = dFdx(uv), dy = dFdy(uv);
  dx.x -= round(dx.x); dy.x -= round(dy.x);
  uv.x = fract(uv.x);
  float m = max(length(dx), length(dy));
  vec2 k = vec2(max(m * 16.0, 24.0 / 12288.0));
  gMag = m * uBaseSize.x;   // base texels per screen pixel (< 1: magnified)
  return textureGrad(tex, uv, vec2(k.x, 0.0), vec2(0.0, k.y)).rgb;
}

float openSeaAt(float lon, float lat) {
  if (uHasLand < 0.5) return 0.0;
  vec2 uv = vec2(fract((lon + PI) / (2.0 * PI)), (PI * 0.5 - lat) / PI);
  float landv = textureLod(uLand, uv, 1.5).r;   // blurred: coasts stay on colour detection
  return 1.0 - smoothstep(0.0, 0.03, landv);
}

vec3 imagery(float lon, float lat) {
  float openSea = openSeaAt(lon, lat);
  vec3 cs = sampleSoft(uBase, lon, lat);
  vec3 c = sampleEquirect(uBase, lon, lat);
  float dW = 0.0;   // sharp detail imagery knows its own small islands: trust its colours there
  if (uDetailCount > 0) {
    vec4 d = sampleBox(uDetail0, uDetailBox0, lon, lat);
    c = mix(c, d.rgb, d.a * uDetailMix[0]);
    dW = max(dW, d.a * uDetailMix[0]);
  }
  if (uDetailCount > 1) {
    vec4 d = sampleBox(uDetail1, uDetailBox1, lon, lat);
    c = mix(c, d.rgb, d.a * uDetailMix[1]);
    dW = max(dW, d.a * uDetailMix[1]);
  }
  if (uDetailCount > 2) {
    vec4 d = sampleBox(uDetail2, uDetailBox2, lon, lat);
    c = mix(c, d.rgb, d.a * uDetailMix[2]);
    dW = max(dW, d.a * uDetailMix[2]);
  }
  if (uDetailCount > 3) {
    vec4 d = sampleBox(uDetail3, uDetailBox3, lon, lat);
    c = mix(c, d.rgb, d.a * uDetailMix[3]);
    dW = max(dW, d.a * uDetailMix[3]);
  }
  float kSea = 0.0;   // the land mask of a close-up box says where its water is: no dark coastal patches from the base
  if (uDetailCount > 0) kSea = max(kSea, boxSea(uDetail0, uDetailBox0, lon, lat) * uDetailMix[0]);
  if (uDetailCount > 1) kSea = max(kSea, boxSea(uDetail1, uDetailBox1, lon, lat) * uDetailMix[1]);
  if (uDetailCount > 2) kSea = max(kSea, boxSea(uDetail2, uDetailBox2, lon, lat) * uDetailMix[2]);
  if (uDetailCount > 3) kSea = max(kSea, boxSea(uDetail3, uDetailBox3, lon, lat) * uDetailMix[3]);
  openSea = max(openSea, kSea);
  openSea *= 1.0 - dW;
  vec3 cw = mix(c, cs, smoothstep(0.7, 0.2, gMag) * (1.0 - dW));
  vec3 g = uNoGrade > 0.5 ? c : grade(c, cs, openSea, cw, dW);
  if (uSepia > 0.0) {
    float l = dot(c, vec3(0.299, 0.587, 0.114));
    float water = smoothstep(0.015, 0.08, c.b - max(c.r, c.g * 0.92)) * (1.0 - smoothstep(0.3, 0.5, l));
    water = max(water, dW * smoothstep(0.34, 0.22, l) * smoothstep(0.0, 0.02, c.b - max(c.r, c.g * 0.97)));
    vec3 land = uTintLand * (0.62 + 0.6 * pow(l, 0.8));
    vec3 sea = uTintSea * (0.9 + 0.2 * l);
    g = mix(g, mix(land, sea, water), uSepia);
  }
  return g;
}

void main() {
  vec2 p = vec2(gl_FragCoord.x, uRes.y - gl_FragCoord.y);
  vec2 d = p - uCenter;
  float ca = cos(uAngle), sa = sin(uAngle);
  d = vec2(d.x * ca - d.y * sa, d.x * sa + d.y * ca);
  vec2 q = d / uK;
  q.y = -q.y;
  if (uMode == 0) {
    float r2 = dot(q, q);
    if (r2 > 1.0) {
      float r = sqrt(r2);
      float px = (r - 1.0) * uK;                   // distance outside the limb in px
      float g = exp(-px / (18.0 + uK * 0.035)) * uAtmo;
      outColor = vec4(vec3(0.35, 0.62, 1.0) * g, g) * uAlpha;
      return;
    }
    float z = sqrt(1.0 - r2);
    // inverse of d3.geoRotation([-lon0, -lat0]) applied to (lambda', phi')
    float X = z, Y = q.x, Z = q.y;
    float cp = cos(-uLat0), sp = sin(-uLat0);
    float lon = atan(Y, X * cp + Z * sp) + uLon0;
    float lat = asin(clamp(Z * cp - X * sp, -1.0, 1.0));
    lon = mod(lon + PI, 2.0 * PI) - PI;
    vec3 c = imagery(lon, lat);
    // soft light from the upper left + limb haze
    vec3 n = vec3(q.x, q.y, z);
    float diff = 0.78 + 0.32 * max(dot(n, normalize(vec3(-0.45, 0.55, 0.75))), 0.0);
    c *= diff;
    float rim = pow(1.0 - z, 2.5);
    c = mix(c, vec3(0.45, 0.7, 1.0), rim * 0.55 * uAtmo);
    outColor = vec4(c, 1.0) * uAlpha;
  } else {
    float lon = uLon0 + q.x;
    float my = uMercY0 + q.y;
    float lat = 2.0 * atan(exp(my)) - PI * 0.5;
    lon = mod(lon + PI, 2.0 * PI) - PI;
    vec3 c = imagery(lon, lat);
    outColor = vec4(c, 1.0) * uAlpha;
  }
}`;

export class Raster {
  constructor(canvas) {
    this.canvas = canvas;
    const gl = canvas.getContext('webgl2', { preserveDrawingBuffer: true, premultipliedAlpha: true, antialias: false });
    if (!gl) throw new Error('WebGL2 not available');
    this.gl = gl;
    const prog = gl.createProgram();
    for (const [type, src] of [[gl.VERTEX_SHADER, VS], [gl.FRAGMENT_SHADER, FS]]) {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      gl.attachShader(prog, s);
    }
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
    this.prog = prog;
    gl.useProgram(prog);
    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'aPos');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    this.u = {};
    for (const name of ['uAngle', 'uRes', 'uCenter', 'uK', 'uLon0', 'uLat0', 'uMercY0', 'uMode', 'uAlpha', 'uAtmo', 'uSepia', 'uTintLand', 'uTintSea', 'uBase', 'uBaseSize', 'uLand', 'uHasLand', 'uNoGrade',
      'uDetailCount', 'uDetail0', 'uDetail1', 'uDetail2', 'uDetail3', 'uDetailBox0', 'uDetailBox1', 'uDetailBox2', 'uDetailBox3', 'uDetailMix']) {
      this.u[name] = gl.getUniformLocation(prog, name);
    }
    this.details = [];
    this.maxTex = gl.getParameter(gl.MAX_TEXTURE_SIZE);
    const dbg = gl.getExtension('WEBGL_debug_renderer_info');
    this.renderer = dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : 'unknown';
    this.software = /swiftshader|llvmpipe|software/i.test(this.renderer);
  }

  _texture(img, unit, mip) {
    const gl = this.gl;
    let src = img;
    const max = this.maxTex;
    if (img.width > max || img.height > max) {
      const s = Math.min(max / img.width, max / img.height);
      const c = document.createElement('canvas');
      c.width = Math.floor(img.width * s);
      c.height = Math.floor(img.height * s);
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      src = c;
    }
    const tex = gl.createTexture();
    gl.activeTexture(gl.TEXTURE0 + unit);
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
    if (mip) gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, mip ? gl.LINEAR_MIPMAP_LINEAR : gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, mip ? gl.REPEAT : gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    return { tex, w: src.width, h: src.height };
  }

  // Render the imagery at a fraction of the output size (CSS scales it back up).
  setScale(cssW, cssH, scale) {
    this.cssWidth = cssW;
    this.canvas.width = Math.round(cssW * scale);
    this.canvas.height = Math.round(cssH * scale);
  }

  setBase(img) {
    this.base = this._texture(img, 0, true);
  }

  setLand(canvas) {
    this.land = this._texture(canvas, 6, true);
  }

  addDetail(img, bboxDeg) {
    if (this.details.length >= MAX_DETAIL) return;
    const unit = 1 + this.details.length;
    const t = this._texture(img, unit, true);
    const r = Math.PI / 180;
    this.details.push({ ...t, unit, box: bboxDeg.map((v) => v * r) });
  }

  draw(view, { alpha = 1, atmo = 1, detailMix = 1, sepia = 0, tintLand = null, tintSea = null } = {}) {
    const gl = this.gl;
    const { width, height } = this.canvas;
    gl.viewport(0, 0, width, height);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    if (alpha <= 0.001) return;
    gl.useProgram(this.prog);
    const u = this.u;
    const r = Math.PI / 180;
    gl.uniform2f(u.uRes, width, height);
    const f = width / this.cssWidth;
    gl.uniform2f(u.uCenter, view.cx * f, view.cy * f);
    gl.uniform1f(u.uK, view.k * f);
    gl.uniform1f(u.uAngle, ((view.angle || 0) * Math.PI) / 180);
    gl.uniform1f(u.uLon0, view.lon * r);
    gl.uniform1f(u.uLat0, view.lat * r);
    gl.uniform1f(u.uMercY0, Math.log(Math.tan(Math.PI / 4 + (view.lat * r) / 2)));
    gl.uniform1i(u.uMode, view.mode === 'globe' ? 0 : 1);
    gl.uniform1f(u.uAlpha, alpha);
    gl.uniform1f(u.uAtmo, atmo);
    gl.uniform1f(u.uSepia, sepia || 0);
    gl.uniform3f(u.uTintLand, ...(tintLand || [0.86, 0.79, 0.62]));
    gl.uniform3f(u.uTintSea, ...(tintSea || [0.56, 0.69, 0.67]));
    gl.uniform1i(u.uBase, 0);
    gl.uniform1i(u.uLand, this.land ? 6 : 0);
    gl.uniform1f(u.uHasLand, this.land ? 1 : 0);
    gl.uniform1f(u.uNoGrade, this.noGrade ? 1 : 0);
    gl.uniform2f(u.uBaseSize, this.base.w, this.base.h);
    gl.uniform1i(u.uDetailCount, this.details.length);
    // detailMix: one number, or one per box
    const m = [0, 1, 2, 3].map((i) => (Array.isArray(detailMix) ? detailMix[i] ?? 0 : detailMix));
    gl.uniform4f(u.uDetailMix, m[0], m[1], m[2], m[3]);
    this.details.forEach((d, i) => {
      gl.uniform1i(u[`uDetail${i}`], d.unit);
      gl.uniform4f(u[`uDetailBox${i}`], ...d.box);
    });
    // Unused detail samplers still need a valid unit.
    for (let i = this.details.length; i < MAX_DETAIL; i++) gl.uniform1i(u[`uDetail${i}`], 0);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
}
