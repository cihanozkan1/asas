import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: true, args: ['--no-sandbox', '--lang=en-US', `--proxy-server=${process.env.HTTPS_PROXY}`, `--ignore-certificate-errors-spki-list=${process.env.PROXY_SPKI}`] });
const p = await b.newPage();
await p.setViewport({ width: 1400, height: 2000 });
await p.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36');
await p.setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });
await p.goto('https://www.youtube.com/@GeoGlobeTales/shorts', { waitUntil: 'domcontentloaded', timeout: 60000 });
await new Promise(r => setTimeout(r, 5000));
// consent
try { const btn = await p.$('button[aria-label*="Accept"]'); if (btn) { await btn.click(); await new Promise(r => setTimeout(r, 3000)); } } catch {}
// click "Popular"
const clicked = await p.evaluate(() => { const c = [...document.querySelectorAll('chip-shape button, yt-chip-cloud-chip-renderer, button')].find(e => /^\s*Popular\s*$/.test(e.innerText || '')); if (c) { c.click(); return true; } return false; });
await new Promise(r => setTimeout(r, 5000));
const seen = new Map();
for (let i = 0; i < 12; i++) {
  const items = await p.evaluate(() => [...document.querySelectorAll('a[href*="/shorts/"]')].map(a => [a.href, (a.closest('ytm-shorts-lockup-view-model-v2, ytm-shorts-lockup-view-model, ytd-rich-item-renderer')?.innerText || a.innerText || a.title || '').replace(/\n/g, ' | ').slice(0, 160)]));
  for (const [h, t] of items) if (t && !seen.has(h)) seen.set(h, t);
  await p.evaluate(() => window.scrollBy(0, 3000));
  await new Promise(r => setTimeout(r, 1500));
}
console.log('popular clicked:', clicked, 'count', seen.size);
for (const [h, t] of seen) console.log(t);
await b.close();
