// Headless Chrome frame capture -> ffmpeg (H.264). Also used for quick still previews.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import os from 'node:os';
import puppeteer from 'puppeteer-core';
import { ROOT, findChrome, findFfmpeg, log, runFfmpeg } from './util.mjs';

const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.woff2': 'font/woff2', '.woff': 'font/woff',
};

// Serves the project root (page, node_modules assets, cache/imagery) on localhost.
export function startServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const url = decodeURIComponent(req.url.split('?')[0]);
      const file = path.normalize(path.join(ROOT, url));
      if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        if (!url.endsWith('favicon.ico')) console.warn('[server] 404', url);
        res.writeHead(404);
        res.end();
        return;
      }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

async function openPage(timeline, scale = 1) {
  const server = await startServer();
  const port = server.address().port;
  const browser = await puppeteer.launch({
    executablePath: findChrome(),
    headless: true,
    args: [
      '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--enable-webgl', '--hide-scrollbars', '--mute-audio',
      '--font-render-hinting=none', '--disable-lcd-text', '--force-color-profile=srgb',
      // Chrome refuses to run as root (containers/CI) without this; harmless on a desktop.
      ...(process.getuid?.() === 0 ? ['--no-sandbox'] : []),
    ],
  });
  const page = await browser.newPage();
  page.on('console', (m) => {
    if (['error', 'warning', 'warn'].includes(m.type())) log('[page]', m.text());
  });
  page.on('pageerror', (e) => log('[page error]', e.message));
  await page.setViewport({ width: timeline.W, height: timeline.H, deviceScaleFactor: scale });
  await page.goto(`http://127.0.0.1:${port}/page/index.html`, { waitUntil: 'load' });
  await page.waitForFunction(() => window.GG, { timeout: 30000 });
  const info = await page.evaluate((tl) => window.GG.init(tl), timeline);
  const close = async () => {
    await browser.close();
    server.close();
  };
  return { page, info, close };
}

export async function renderStills(timeline, times, outDir, { scale = 0.5 } = {}) {
  fs.mkdirSync(outDir, { recursive: true });
  const { page, close } = await openPage(timeline, scale);
  const files = [];
  try {
    for (const t of times) {
      await page.evaluate((tt) => window.GG.frame(tt), t);
      const f = path.join(outDir, `still_${t.toFixed(2).padStart(6, '0')}.jpg`);
      await page.screenshot({ path: f, type: 'jpeg', quality: 88 });
      files.push(f);
    }
  } finally {
    await close();
  }
  return files;
}

export async function contactSheet(files, out, cols = 5) {
  if (!files.length) return null;
  const listDir = path.dirname(files[0]);
  const rows = Math.ceil(files.length / cols);
  const pattern = path.join(listDir, 'sheet_%03d.jpg');
  files.forEach((f, i) => fs.copyFileSync(f, path.join(listDir, `sheet_${String(i).padStart(3, '0')}.jpg`)));
  await runFfmpeg(['-y', '-framerate', '1', '-i', pattern, '-vf', `scale=324:576,tile=${cols}x${rows}:padding=6:color=white`, '-frames:v', '1', '-q:v', '3', out]);
  for (let i = 0; i < files.length; i++) fs.rmSync(path.join(listDir, `sheet_${String(i).padStart(3, '0')}.jpg`));
  return out;
}

async function renderChunk(timeline, out, { from, n, rate, scale, crf, onFrame }) {
  const { page, close, info } = await openPage(timeline, scale);
  if (onFrame.first) { onFrame.first = false; log(`GPU: ${info.renderer}, uydu katmanı ölçeği ${info.rasterScale}`); }
  const ff = spawn(findFfmpeg(), [
    '-hide_banner', '-loglevel', 'error', '-y',
    '-f', 'image2pipe', '-framerate', String(rate), '-c:v', 'mjpeg', '-i', '-',
    '-vf', 'scale=in_range=full:out_range=tv,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', String(crf), '-r', String(rate),
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', out,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((resolve, reject) => ff.on('close', (c) => (c === 0 ? resolve() : reject(new Error('ffmpeg exit ' + c)))));
  try {
    for (let i = 0; i < n; i++) {
      await page.evaluate((tt) => window.GG.frame(tt), from + i / rate);
      const buf = await page.screenshot({ type: 'jpeg', quality: 92, optimizeForSpeed: true, captureBeyondViewport: false });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
      onFrame();
    }
  } finally {
    ff.stdin.end();
    await close();
  }
  await done;
}

// Frames are split into contiguous chunks rendered by parallel Chrome instances,
// then joined losslessly with the concat demuxer.
export async function renderVideo(timeline, out, { from = 0, to = null, fps = null, scale = 1, crf = 18, workers = null } = {}) {
  const rate = fps || timeline.fps;
  const end = to ?? timeline.duration;
  const total = Math.ceil((end - from) * rate);
  const k = Math.max(1, Math.min(workers || os.cpus().length, Math.ceil(total / 60)));
  log(`render: ${total} kare, ${rate} fps, ${k} paralel işçi`);
  const dir = fs.mkdtempSync(path.join(path.dirname(out), '.chunks-'));
  const per = Math.ceil(total / k);
  let doneFrames = 0;
  const t0 = Date.now();
  const tick = () => {
    doneFrames++;
    if (doneFrames % 30 === 0 || doneFrames === total) {
      const el = (Date.now() - t0) / 1000;
      const eta = (el / doneFrames) * (total - doneFrames);
      process.stdout.write(`\r[geo] kare ${doneFrames}/${total}  (${((el / doneFrames) * 1000).toFixed(0)} ms/kare efektif, kalan ~${Math.round(eta)} sn)   `);
    }
  };
  tick.first = true;
  const parts = [];
  const jobs = [];
  for (let w = 0; w < k; w++) {
    const f0 = w * per;
    const n = Math.min(per, total - f0);
    if (n <= 0) break;
    const file = path.join(dir, `part${w}.mp4`);
    parts.push(file);
    jobs.push(renderChunk(timeline, file, { from: from + f0 / rate, n, rate, scale, crf, onFrame: tick }));
  }
  try {
    await Promise.all(jobs);
    process.stdout.write('\n');
    const list = path.join(dir, 'list.txt');
    fs.writeFileSync(list, parts.map((p) => `file '${p.split(path.sep).join('/')}'`).join('\n'));
    await runFfmpeg(['-y', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', '-movflags', '+faststart', out]);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
  log(`render süresi: ${Math.round((Date.now() - t0) / 1000)} sn`);
}
