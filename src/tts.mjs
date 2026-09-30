// Text-to-speech with word timings.
//  - edge: Microsoft Edge neural voices (msedge-tts), word boundaries from the service
//  - kokoro: local Kokoro-82M (Apache-2.0), python helper tools/kokoro_tts.py; no third-party service
//  - mock: silent audio with estimated timings (for layout tests without network)
// Results are cached per (provider, voice, rate, pitch, text).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { ROOT, SAMPLE_RATE, decodeAudio, findContent, normWord, tmpDir, log } from './util.mjs';

const CACHE = path.join(ROOT, 'cache/tts');

export function tokenize(text) {
  return text.split(/\s+/).filter(Boolean);
}

function cacheKey(obj) {
  return crypto.createHash('sha1').update(JSON.stringify(obj)).digest('hex').slice(0, 16);
}

// Map service word boundaries onto our whitespace tokens (which keep punctuation).
export function alignWords(tokens, bounds, totalSec) {
  const out = tokens.map((text) => ({ text, start: null, end: null }));
  let bi = 0;
  for (let ti = 0; ti < tokens.length; ti++) {
    const target = normWord(tokens[ti]);
    if (!target) continue;
    let acc = '';
    let first = null;
    let last = null;
    let guard = bi;
    while (guard < bounds.length && acc.length < target.length) {
      const nb = normWord(bounds[guard].text);
      if (!nb) { guard++; continue; }
      if (target.startsWith(acc + nb) || (acc === '' && nb.startsWith(target))) {
        acc += nb;
        first = first ?? bounds[guard];
        last = bounds[guard];
        guard++;
        if (nb.startsWith(target) && acc.length >= target.length) break;
      } else break;
    }
    if (first) {
      out[ti].start = first.start;
      out[ti].end = last.end;
      bi = guard;
    } else {
      // try to resync: look ahead a few boundaries for this token
      for (let j = bi; j < Math.min(bounds.length, bi + 4); j++) {
        if (normWord(bounds[j].text) === target) {
          out[ti].start = bounds[j].start;
          out[ti].end = bounds[j].end;
          bi = j + 1;
          break;
        }
      }
    }
  }
  // Fill gaps by interpolation between known neighbours.
  const known = out.map((w, i) => (w.start != null ? i : -1)).filter((i) => i >= 0);
  if (known.length < tokens.length * 0.6) return estimateWords(tokens, 0, totalSec);
  for (let i = 0; i < out.length; i++) {
    if (out[i].start != null) continue;
    const prev = [...known].reverse().find((k) => k < i);
    const next = known.find((k) => k > i);
    const a = prev != null ? out[prev].end : 0;
    const b = next != null ? out[next].start : totalSec;
    const span = (next ?? out.length) - (prev ?? -1);
    const pos = i - (prev ?? -1);
    out[i].start = a + ((b - a) * (pos - 1)) / span;
    out[i].end = a + ((b - a) * pos) / span;
  }
  return out;
}

export function estimateWords(tokens, t0, t1) {
  const weights = tokens.map((w) => normWord(w).length + 2 + (/[,.;:!?]$/.test(w) ? 3 : 0));
  const sum = weights.reduce((a, b) => a + b, 0);
  let t = t0;
  return tokens.map((text, i) => {
    const d = ((t1 - t0) * weights[i]) / sum;
    const w = { text, start: t, end: t + d * 0.9 };
    t += d;
    return w;
  });
}

async function edgeSynth(text, voice) {
  const { MsEdgeTTS, OUTPUT_FORMAT } = await import('msedge-tts');
  const opts = {};
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  if (proxy) {
    const { HttpsProxyAgent } = await import('https-proxy-agent');
    opts.agent = new HttpsProxyAgent(proxy);
  }
  const tts = new MsEdgeTTS(opts);
  await tts.setMetadata(voice.name, OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3, { wordBoundaryEnabled: true });
  const dir = tmpDir('tts-');
  const { audioFilePath, metadataFilePath } = await tts.toFile(dir, text, { rate: voice.rate, pitch: voice.pitch });
  tts.close();
  const meta = metadataFilePath ? JSON.parse(fs.readFileSync(metadataFilePath, 'utf8')) : { Metadata: [] };
  const bounds = meta.Metadata.filter((m) => m.Type === 'WordBoundary').map((m) => ({
    text: m.Data.text.Text,
    start: m.Data.Offset / 1e7,
    end: (m.Data.Offset + m.Data.Duration) / 1e7,
  }));
  return { audioFile: audioFilePath, bounds, dir };
}

// ---- kokoro (local) ----
const KOKORO_RAW = path.join(ROOT, 'cache/tts_raw');
const kokoroSpeed = (voice) => {
  if (voice.speed) return voice.speed;
  const m = String(voice.rate || '').match(/([+-]?\d+)%/);
  return 1 + (m ? Number(m[1]) / 100 : 0) * 1.4;   // edge "+12%" (175 wpm) ~ kokoro 1.17
};
const kokoroKey = (text, voice) => cacheKey({ text, v: voice.name, s: kokoroSpeed(voice) });

// Synthesises all texts that are not cached yet in ONE python run (the model loads once).
export function prewarmKokoro(texts, voice) {
  const todo = [...new Set(texts)].filter((t) => !fs.existsSync(path.join(KOKORO_RAW, kokoroKey(t, voice) + '.wav')));
  if (!todo.length) return;
  log(`Kokoro: ${todo.length} sahne seslendiriliyor (yerel model)...`);
  const req = { voice: voice.name, speed: kokoroSpeed(voice), jobs: todo.map((t) => ({ key: kokoroKey(t, voice), text: t })) };
  const r = spawnSync('python3', [path.join(ROOT, 'tools/kokoro_tts.py'), KOKORO_RAW], { input: JSON.stringify(req), encoding: 'utf8', maxBuffer: 1 << 26 });
  if (r.status !== 0) throw new Error('Kokoro hatası: ' + (r.stderr || '').slice(-600));
}

async function kokoroSynth(text, voice) {
  prewarmKokoro([text], voice);
  const k = kokoroKey(text, voice);
  return { audioFile: path.join(KOKORO_RAW, k + '.wav'), bounds: JSON.parse(fs.readFileSync(path.join(KOKORO_RAW, k + '.json'), 'utf8')), dir: null };
}

// Returns { samples: Float32Array (48k mono, trimmed), words: [{text,start,end}] relative to trimmed audio }
export async function synthScene(text, voice, provider) {
  fs.mkdirSync(CACHE, { recursive: true });
  const key = cacheKey({ provider, voice, text, v: 2 });
  const wavCache = path.join(CACHE, key + '.f32');
  const jsonCache = path.join(CACHE, key + '.json');
  if (fs.existsSync(wavCache) && fs.existsSync(jsonCache)) {
    const b = fs.readFileSync(wavCache);
    return { samples: new Float32Array(b.buffer, b.byteOffset, b.byteLength / 4), words: JSON.parse(fs.readFileSync(jsonCache, 'utf8')) };
  }
  const tokens = tokenize(text);
  let samples, words;
  if (provider === 'mock') {
    const wordsPerSec = 2.9;
    const dur = Math.max(1, tokens.length / wordsPerSec);
    samples = new Float32Array(Math.round(dur * SAMPLE_RATE));
    words = estimateWords(tokens, 0.02, dur - 0.05);
  } else {
    let lastErr;
    for (let attempt = 0; attempt < 4; attempt++) {
      try {
        const { audioFile, bounds, dir } = provider === 'kokoro' ? await kokoroSynth(text, voice) : await edgeSynth(text, voice);
        const raw = await decodeAudio(audioFile);
        if (dir) fs.rmSync(dir, { recursive: true, force: true });
        const [a, b] = findContent(raw, 0.008);
        const pad = Math.round(0.03 * SAMPLE_RATE);
        const s0 = Math.max(0, a - pad);
        const s1 = Math.min(raw.length, b + Math.round(0.06 * SAMPLE_RATE));
        samples = raw.slice(s0, s1);
        const shift = s0 / SAMPLE_RATE;
        const dur = samples.length / SAMPLE_RATE;
        words = alignWords(tokens, bounds.map((w) => ({ ...w, start: w.start - shift, end: w.end - shift })), dur);
        break;
      } catch (e) {
        lastErr = e;
        log(`  TTS hatası (deneme ${attempt + 1}/4): ${e.message}`);
        await new Promise((r) => setTimeout(r, 1500 * 2 ** attempt));
      }
    }
    if (!samples) throw lastErr;
  }
  fs.writeFileSync(wavCache, Buffer.from(samples.buffer, samples.byteOffset, samples.byteLength));
  fs.writeFileSync(jsonCache, JSON.stringify(words));
  return { samples, words };
}

export async function listVoices(filter = 'en-') {
  const { MsEdgeTTS } = await import('msedge-tts');
  const tts = new MsEdgeTTS();
  const voices = await tts.getVoices();
  return voices.filter((v) => v.Locale.startsWith(filter));
}
