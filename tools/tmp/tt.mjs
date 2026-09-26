import puppeteer from 'puppeteer-core';
import fs from 'fs';
const [url, out] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: true, args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required', '--lang=en-US', `--proxy-server=${process.env.HTTPS_PROXY}`, `--ignore-certificate-errors-spki-list=${process.env.PROXY_SPKI}`] });
const p = await b.newPage();
await p.setViewport({ width: 540, height: 960 });
await p.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36');
let mediaUrl = null;
p.on('response', (r) => { const u = r.url(); if (!mediaUrl && /video\/tos|mime_type=video_mp4/.test(u)) mediaUrl = u; });
await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
for (let i = 0; i < 10 && !mediaUrl; i++) {
  await new Promise(r => setTimeout(r, 2000));
  const src = await p.evaluate(() => { const v = document.querySelector('video'); return v ? (v.currentSrc || v.src || (v.querySelector('source')||{}).src) : null; });
  if (src && src.startsWith('http') && !src.includes('playback1')) mediaUrl = src;
}
console.log('title:', (await p.title()).slice(0, 80));
console.log('media:', mediaUrl && mediaUrl.slice(0, 120));
if (mediaUrl) {
  const b64 = await p.evaluate(async (u) => { const r = await fetch(u, { credentials: 'include' }); const buf = new Uint8Array(await r.arrayBuffer()); let s = ''; for (let i = 0; i < buf.length; i += 32768) s += String.fromCharCode(...buf.subarray(i, i + 32768)); return r.status + ':' + btoa(s); }, mediaUrl);
  const [st, data] = [b64.slice(0, b64.indexOf(':')), b64.slice(b64.indexOf(':') + 1)];
  fs.writeFileSync(out, Buffer.from(data, 'base64'));
  console.log('status', st, 'bytes', fs.statSync(out).size);
}
await p.screenshot({ path: out + '.png' });
await b.close();
