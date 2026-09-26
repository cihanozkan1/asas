import puppeteer from 'puppeteer-core';
const id = process.argv[2];
const b = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: true, args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required', '--lang=en-US', `--proxy-server=${process.env.HTTPS_PROXY}`, '--ignore-certificate-errors'] });
const p = await b.newPage();
await p.setViewport({ width: 540, height: 960 });
await p.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36');
await p.goto(`https://www.youtube.com/shorts/${id}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
for (let i = 0; i < 12; i++) {
  await new Promise(r => setTimeout(r, 2500));
  const st = await p.evaluate(() => { const v = document.querySelector('video'); return v ? { t: v.currentTime, rs: v.readyState, d: v.duration, src: (v.src||'').slice(0,40), err: v.error && v.error.code } : null; });
  console.log(i, JSON.stringify(st), (await p.title()).slice(0, 60));
}
await p.screenshot({ path: '/tmp/claude-0/-home-user-asas/0cbc0fa6-80ff-51e1-af1e-99f106a26abb/scratchpad/yt.png' });
await b.close();
