// Bundles page/main.js (+ d3/topojson) into page/dist/bundle.js for the renderer.
import path from 'node:path';
import { build } from 'esbuild';
import { ROOT } from '../src/util.mjs';

export async function buildPage() {
  await build({
    entryPoints: [path.join(ROOT, 'page/main.js')],
    bundle: true,
    format: 'esm',
    target: 'chrome110',
    outfile: path.join(ROOT, 'page/dist/bundle.js'),
    logLevel: 'warning',
  });
}

if (process.argv[1]?.endsWith('build-page.mjs')) await buildPage();
