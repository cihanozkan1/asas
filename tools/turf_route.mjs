#!/usr/bin/env node
// Turf.js route helpers for the authoring side (JSON in, JSON out). Points are [lat, lon] like the script format.
//   node tools/turf_route.mjs smooth  '[[41,28.9],[38,24],[36,14]]'            -> bezierSpline (smooth curve through the points)
//   node tools/turf_route.mjs chunk   '[[...]]' 50                              -> lineChunk: equal 50 km pieces (stage-by-stage movement)
//   node tools/turf_route.mjs along   '[[...]]' 0.5                             -> point at 50 % of the length
//   node tools/turf_route.mjs slice   '[[...]]' 0.0 0.4                         -> lineSliceAlong between 0 % and 40 %
//   node tools/turf_route.mjs length  '[[...]]'                                  -> km
//   node tools/turf_route.mjs nearest '[[...]]' '[lat,lon]'                      -> nearestPointOnLine
import * as turf from '@turf/turf';
const [cmd, pts, ...rest] = process.argv.slice(2);
const P = JSON.parse(pts).map(([la, lo]) => [lo, la]);
const line = turf.lineString(P);
const back = (g) => g.map(([lo, la]) => [+la.toFixed(5), +lo.toFixed(5)]);
const len = turf.length(line);
let out;
if (cmd === 'smooth') out = back(turf.bezierSpline(line, { resolution: 10000, sharpness: 0.6 }).geometry.coordinates);
else if (cmd === 'chunk') out = turf.lineChunk(line, +rest[0], { units: 'kilometers' }).features.map((f) => back(f.geometry.coordinates));
else if (cmd === 'along') out = back([turf.along(line, +rest[0] * len).geometry.coordinates])[0];
else if (cmd === 'slice') out = back(turf.lineSliceAlong(line, +rest[0] * len, +rest[1] * len).geometry.coordinates);
else if (cmd === 'length') out = Math.round(len * 10) / 10;
else if (cmd === 'nearest') { const q = JSON.parse(rest[0]); out = back([turf.nearestPointOnLine(line, [q[1], q[0]]).geometry.coordinates])[0]; }
else { console.error('unknown command'); process.exit(1); }
console.log(JSON.stringify(out));
