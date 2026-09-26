// Shared helpers: paths, config merging, ffmpeg/Chrome discovery, WAV/PCM handling.
import fs from 'node:fs';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import os from 'node:os';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const SAMPLE_RATE = 48000;

export function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

export function writeJson(p, data) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(data, null, 2));
}

export function deepMerge(base, over) {
  if (over === undefined) return structuredClone(base);
  if (Array.isArray(over) || typeof over !== 'object' || over === null) return over;
  const out = { ...(base && typeof base === 'object' && !Array.isArray(base) ? structuredClone(base) : {}) };
  for (const [k, v] of Object.entries(over)) out[k] = deepMerge(out[k], v);
  return out;
}

export function log(...args) {
  console.log('[geo]', ...args);
}

// ---------- ffmpeg ----------

let ffmpegPath;
export function findFfmpeg() {
  if (ffmpegPath) return ffmpegPath;
  const candidates = [process.env.FFMPEG_PATH, 'ffmpeg'].filter(Boolean);
  for (const c of candidates) {
    const r = spawnSync(c, ['-version'], { encoding: 'utf8' });
    if (r.status === 0) return (ffmpegPath = c);
  }
  throw new Error('ffmpeg bulunamadı. PATH\'e ekleyin veya FFMPEG_PATH ortam değişkenini ayarlayın.');
}

export function runFfmpeg(args, { input, quiet = true } = {}) {
  return new Promise((resolve, reject) => {
    const proc = spawn(findFfmpeg(), ['-hide_banner', '-loglevel', quiet ? 'error' : 'info', ...args], {
      stdio: [input ? 'pipe' : 'ignore', 'pipe', 'pipe'],
    });
    const out = [];
    let err = '';
    proc.stdout.on('data', (d) => out.push(d));
    proc.stderr.on('data', (d) => (err += d));
    proc.on('error', reject);
    proc.on('close', (code) => {
      if (code === 0) resolve(Buffer.concat(out));
      else reject(new Error(`ffmpeg ${args.join(' ')}\n${err}`));
    });
    if (input) proc.stdin.end(input);
  });
}

// Decode any audio file to mono 48 kHz Float32 samples.
export async function decodeAudio(file) {
  const buf = await runFfmpeg(['-i', file, '-f', 'f32le', '-ac', '1', '-ar', String(SAMPLE_RATE), 'pipe:1']);
  return new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4).slice();
}

// Returns [firstSample, lastSample) of non-silent content.
export function findContent(samples, threshold = 0.01) {
  let a = 0;
  let b = samples.length;
  while (a < b && Math.abs(samples[a]) < threshold) a++;
  while (b > a && Math.abs(samples[b - 1]) < threshold) b--;
  return [a, b];
}

export function writeWav(file, samples, sampleRate = SAMPLE_RATE) {
  const data = Buffer.alloc(samples.length * 2);
  for (let i = 0; i < samples.length; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    data.writeInt16LE(Math.round(s * 32767), i * 2);
  }
  const h = Buffer.alloc(44);
  h.write('RIFF', 0);
  h.writeUInt32LE(36 + data.length, 4);
  h.write('WAVE', 8);
  h.write('fmt ', 12);
  h.writeUInt32LE(16, 16);
  h.writeUInt16LE(1, 20);
  h.writeUInt16LE(1, 22);
  h.writeUInt32LE(sampleRate, 24);
  h.writeUInt32LE(sampleRate * 2, 28);
  h.writeUInt16LE(2, 32);
  h.writeUInt16LE(16, 34);
  h.write('data', 36);
  h.writeUInt32LE(data.length, 40);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, Buffer.concat([h, data]));
}

// ---------- Chrome ----------

export function findChrome() {
  const env = process.env.CHROME_PATH;
  if (env && fs.existsSync(env)) return env;
  const candidates = [];
  if (process.platform === 'win32') {
    const pf = [process.env['PROGRAMFILES'], process.env['PROGRAMFILES(X86)'], process.env.LOCALAPPDATA].filter(Boolean);
    for (const base of pf) {
      candidates.push(path.join(base, 'Google', 'Chrome', 'Application', 'chrome.exe'));
    }
    for (const base of pf) {
      candidates.push(path.join(base, 'Microsoft', 'Edge', 'Application', 'msedge.exe'));
    }
  } else if (process.platform === 'darwin') {
    candidates.push('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
  } else {
    candidates.push('/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser');
    const pw = '/opt/pw-browsers';
    if (fs.existsSync(pw)) {
      for (const d of fs.readdirSync(pw).sort().reverse()) {
        if (d.startsWith('chromium-')) candidates.push(path.join(pw, d, 'chrome-linux', 'chrome'));
      }
    }
  }
  const found = candidates.find((c) => fs.existsSync(c));
  if (!found) throw new Error('Chrome bulunamadı. CHROME_PATH ortam değişkenini chrome.exe yoluna ayarlayın.');
  return found;
}

export function tmpDir(prefix) {
  return fs.mkdtempSync(path.join(os.tmpdir(), prefix));
}

// Normalise a word for matching (lowercase, letters/digits only).
export function normWord(w) {
  return w
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[^a-z0-9]/g, '');
}
