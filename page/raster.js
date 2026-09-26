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
uniform sampler2D uBase;
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
uniform float uDetailMix;
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

vec3 imagery(float lon, float lat) {
  vec3 c = sampleEquirect(uBase, lon, lat);
  if (uDetailCount > 0) {
    vec4 d = sampleBox(uDetail0, uDetailBox0, lon, lat);
    c = mix(c, d.rgb, d.a * uDetailMix);
  }
  if (uDetailCount > 1) {
    vec4 d = sampleBox(uDetail1, uDetailBox1, lon, lat);
    c = mix(c, d.rgb, d.a * uDetailMix);
  }
  if (uDetailCount > 2) {
    vec4 d = sampleBox(uDetail2, uDetailBox2, lon, lat);
    c = mix(c, d.rgb, d.a * uDetailMix);
  }
  if (uDetailCount > 3) {
    vec4 d = sampleBox(uDetail3, uDetailBox3, lon, lat);
    c = mix(c, d.rgb, d.a * uDetailMix);
  }
  return c;
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
    for (const name of ['uAngle', 'uRes', 'uCenter', 'uK', 'uLon0', 'uLat0', 'uMercY0', 'uMode', 'uAlpha', 'uAtmo', 'uBase', 'uBaseSize',
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

  addDetail(img, bboxDeg) {
    if (this.details.length >= MAX_DETAIL) return;
    const unit = 1 + this.details.length;
    const t = this._texture(img, unit, true);
    const r = Math.PI / 180;
    this.details.push({ ...t, unit, box: bboxDeg.map((v) => v * r) });
  }

  draw(view, { alpha = 1, atmo = 1, detailMix = 1 } = {}) {
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
    gl.uniform1i(u.uBase, 0);
    gl.uniform2f(u.uBaseSize, this.base.w, this.base.h);
    gl.uniform1i(u.uDetailCount, this.details.length);
    gl.uniform1f(u.uDetailMix, detailMix);
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
