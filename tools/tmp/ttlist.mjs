import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: true, args: ['--no-sandbox', '--lang=en-US', `--proxy-server=${process.env.HTTPS_PROXY}`, `--ignore-certificate-errors-spki-list=${process.env.PROXY_SPKI}`] });
const p = await b.newPage();
await p.setViewport({ width: 1280, height: 1600 });
await p.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36');
await p.goto('https://www.tiktok.com/@geoglobetales', { waitUntil: 'domcontentloaded', timeout: 60000 });
await new Promise(r => setTimeout(r, 6000));
const seen = new Map();
for (let i = 0; i < 25; i++) {
  const items = await p.evaluate(() => [...document.querySelectorAll('a[href*="/video/"]')].map(a => [a.href, (a.querySelector('img')?.alt || a.innerText || '').slice(0, 110)]));
  for (const [h, t] of items) if (!seen.has(h)) seen.set(h, t);
  await p.evaluate(() => window.scrollBy(0, 2500));
  await new Promise(r => setTimeout(r, 1800));
}
for (const [h, t] of seen) console.log(h, '|', t.replace(/\n/g, ' '));
await p.screenshot({ path: '/tmp/claude-0/-home-user-asas/0cbc0fa6-80ff-51e1-af1e-99f106a26abb/scratchpad/ttlist.png' });
await b.close();
