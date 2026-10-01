import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
import http from 'node:http';
const root = '/home/user/asas/remotion/node_modules/maplibre-gl/dist/';
const srv = http.createServer((q, r) => {
  if (q.url === '/') { r.setHeader('content-type', 'text/html'); r.end(`<link rel=stylesheet href=/maplibre-gl.css><div id=m style="width:540px;height:960px"></div><script type=module>
  import * as maplibregl from '/maplibre-gl.mjs';
  const m=new maplibregl.Map({container:'m',style:{version:8,sources:{c:{type:'geojson',data:{type:'Feature',geometry:{type:'Polygon',coordinates:[[[0,0],[10,0],[10,10],[0,10],[0,0]]]}}}},layers:[{id:'f',type:'fill',source:'c',paint:{'fill-color':'#f00'}}]},center:[5,5],zoom:4,interactive:false,fadeDuration:0});
  m.on('load',()=>{document.title='LOADED'});m.on('error',e=>{console.log('ERR',e.error&&e.error.message)});</script>`); return; }
  const f = root + q.url.slice(1);
  if (fs.existsSync(f)) { r.setHeader('content-type', f.endsWith('.mjs') ? 'text/javascript' : f.endsWith('.css') ? 'text/css' : 'application/octet-stream'); r.end(fs.readFileSync(f)); } else { r.statusCode = 404; r.end(); }
}).listen(8765);
const exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await puppeteer.launch({ executablePath: exe, headless: true, args: ['--no-sandbox', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--enable-webgl', '--use-gl=angle', '--use-angle=swiftshader'] });
const p = await b.newPage();
p.on('console', (m) => console.log('PAGE', m.text().slice(0, 200)));
await p.goto('http://localhost:8765/');
await new Promise((r) => setTimeout(r, 6000));
console.log('title', await p.title());
await b.close(); srv.close();
