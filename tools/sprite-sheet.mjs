import { build } from 'esbuild';
import puppeteer from 'puppeteer-core';
import fs from 'fs';
import { findChrome, ROOT } from '../src/util.mjs';
// Renders every character preset and ship to one PNG for a quick visual check.
// Usage: node tools/sprite-sheet.mjs [out.png]
await build({ stdin: { contents: `import {characterSvg, shipSvg, CHARACTER_PRESETS} from './page/sprites.js'; window.S={characterSvg, shipSvg, P:Object.keys(CHARACTER_PRESETS)};`, resolveDir: ROOT }, bundle: true, outfile: '/tmp/sp.js', format: 'iife' });
const js = fs.readFileSync('/tmp/sp.js','utf8');
const b = await puppeteer.launch({ executablePath: findChrome(), args: process.getuid?.() === 0 ? ['--no-sandbox'] : [] });
const p = await b.newPage(); await p.setViewport({ width: 1400, height: 900 });
await p.setContent(`<body style="margin:0;background:#8fb1ac;display:flex;flex-wrap:wrap;gap:10px;padding:10px"><script>${js}</script></body>`);
await p.evaluate(() => { for (const k of S.P) { const d=document.createElement('div'); d.style.cssText='width:220px;height:290px;text-align:center;font:bold 16px sans-serif'; d.innerHTML=S.characterSvg({preset:k}).replace('<svg','<svg width="210" height="252"')+k; document.body.appendChild(d);} const s=document.createElement('div'); s.innerHTML=S.shipSvg({}).replace('<svg','<svg width="240" height="220"'); document.body.appendChild(s); const s2=document.createElement('div'); s2.innerHTML=S.shipSvg({emblem:'#c1121f',cross:'saltire',sail:'#fff'}).replace('<svg','<svg width="240" height="220"'); document.body.appendChild(s2);});
await p.screenshot({ path: '' + (process.argv[2] || 'output/sprites.png') + '' });
await b.close();
