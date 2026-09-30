#!/usr/bin/env node
// One command from script.json to finished Short:
//   node scripts/pipeline.mjs videos/<id> [--style geo|globe|both] [options]
// Options:
//   --style geo|globe|both  visual preset (default: script.style or geo)
//   --mock-tts              silent narration with estimated timings (no network)
//   --stills [n]            only render n preview stills + contact sheet (default 15)
//   --check-only            validate the script and exit
//   --from S --to S         render only part of the video (seconds)
//   --fps N --scale F       faster previews (e.g. --fps 15 --scale 0.5)
//   --guides                draw the YouTube UI safe zones
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT, readJson, writeJson, deepMerge, log } from '../src/util.mjs';
import { validateScript } from '../src/validate.mjs';
import { buildNarration, mux } from '../src/audio.mjs';
import { buildSfxTrack } from '../src/sfx.mjs';
import { buildTimeline } from '../src/timeline.mjs';
import { renderVideo, renderStills, contactSheet } from '../src/render.mjs';
import { writeUploadText, writeSources } from '../src/meta.mjs';
import { ensureDetail, autoDetailBoxes, byCoarseness, S2_CREDIT, BLUE_MARBLE_CREDIT, NE_CREDIT } from '../src/imagery.mjs';
import { ensureEarth, ensureNight } from '../tools/fetch-data.mjs';
import { buildPage } from '../tools/build-page.mjs';

const BOOLEAN = new Set(['check-only', 'mock-tts', 'guides', 'timeline-only']);

function parseArgs(argv) {
  const a = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (!k.startsWith('--')) {
      a._.push(k);
      continue;
    }
    const name = k.slice(2);
    const next = argv[i + 1];
    const takesValue = !BOOLEAN.has(name) && !(name === 'stills' && !/^\d+$/.test(next ?? ''));
    if (takesValue && next != null && !next.startsWith('--')) {
      a[name] = next;
      i++;
    } else a[name] = true;
  }
  return a;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const target = args._[0];
  if (!target) {
    console.log('Kullanım: node scripts/pipeline.mjs videos/<id> [--style geo|globe|both] [--mock-tts] [--stills] [--check-only]');
    process.exit(1);
  }
  const videoDir = path.resolve(target.endsWith('.json') ? path.dirname(target) : target);
  const script = readJson(target.endsWith('.json') ? target : path.join(videoDir, 'script.json'));
  const cfg = deepMerge(readJson(path.join(ROOT, 'config/default.json')), script.config);

  const v = validateScript(script, cfg);
  v.warnings.forEach((w) => log('UYARI:', w));
  if (v.errors.length) {
    v.errors.forEach((e) => log('HATA:', e));
    process.exit(2);
  }
  log(`senaryo OK: ${script.scenes.length} sahne, ${v.words} kelime, ~${v.estSec.toFixed(0)} sn`);
  if (args['check-only']) return;

  const styleArg = args.style || script.style || 'geo';
  const styles = styleArg === 'both' ? ['geo', 'globe'] : [styleArg];
  const outDir = path.join(ROOT, 'output', script.id);
  fs.mkdirSync(outDir, { recursive: true });

  await buildPage();
  const night = script.earth === 'night';
  const earthFile = night ? await ensureNight() : await ensureEarth();
  const assets = { earth: '/' + path.relative(ROOT, earthFile).split(path.sep).join('/'), detail: [] };
  // day-time Sentinel close-ups would clash with the night lights texture
  const auto = night ? [] : autoDetailBoxes(script, cfg);
  const details = night ? [] : [...auto, ...(script.imagery || [])].sort(byCoarseness);
  for (const d of details) assets.detail.push(await ensureDetail(d));

  const provider = args['mock-tts'] ? 'mock' : (args.tts || cfg.voice.provider);
  const narrationWav = path.join(outDir, `narration${provider === 'mock' ? '.mock' : ''}.wav`);
  const narration = await buildNarration(script, cfg, provider, narrationWav);
  log(`anlatım: ${narration.duration.toFixed(1)} sn (${provider}, ${narration.voice.name} ${narration.voice.rate})`);

  const hasChars = script.scenes.some((sc) => (sc.show || []).some((e) => e.type === 'character' && e.image));
  const hasArt = JSON.stringify(script.scenes).includes('art:');
  const hasHist = script.scenes.some((sc) => sc.era === 'history');
  const credits = [night ? 'Earth at night: NASA Black Marble (NASA Earth Observatory)' : BLUE_MARBLE_CREDIT, NE_CREDIT, ...(assets.detail.length ? [S2_CREDIT] : []), ...(hasChars || hasArt ? ['Illustrations: AI-generated artwork'] : []), ...(hasHist ? ['Historical borders: aourednik/historical-basemaps (GPL-3.0)'] : [])];
  writeUploadText(script, path.join(outDir, `${script.id}.txt`), credits);
  writeSources(script, path.join(outDir, 'sources.md'));

  for (const style of styles) {
    const preset = cfg.presets[style];
    if (!preset) throw new Error('Bilinmeyen stil: ' + style);
    const tl = await buildTimeline({ script, cfg, preset, narration, videoDir, assets, guides: !!args.guides });
    writeJson(path.join(outDir, `timeline.${style}.json`), tl);
    if (args['timeline-only']) continue;

    if (args.stills) {
      const n = Number(args.stills) > 1 ? Number(args.stills) : 15;
      const times = args.times
        ? String(args.times).split(',').map(Number)
        : Array.from({ length: n }, (_, i) => Math.min(tl.duration - 0.05, 0.3 + (i * (tl.duration - 0.6)) / (n - 1)));
      const files = await renderStills(tl, times, path.join(outDir, `stills_${style}`), { scale: Number(args.scale || 0.5) });
      const sheet = await contactSheet(files, path.join(outDir, `contact_${style}.jpg`));
      log('önizleme:', path.relative(ROOT, sheet));
      continue;
    }

    const silent = path.join(outDir, `video.${style}.mp4`);
    await renderVideo(tl, silent, {
      from: Number(args.from || 0),
      to: args.to != null ? Number(args.to) : null,
      fps: args.fps ? Number(args.fps) : null,
      scale: Number(args.scale || 1),
      crf: cfg.video.crf,
      workers: args.workers ? Number(args.workers) : cfg.video.workers,
    });
    const final = path.join(outDir, `${script.id}_${style}${provider === 'mock' ? '_mock' : ''}.mp4`);
    const from = Number(args.from || 0);
    const to = args.to != null ? Number(args.to) : tl.duration;
    if (from > 0) {
      log('--from kullanıldı: ses eklenmedi, sadece görüntü:', path.relative(ROOT, silent));
      continue;
    }
    let sfxWav = null;
    if (cfg.sfx?.enabled !== false) {
      sfxWav = path.join(outDir, `sfx.${style}.wav`);
      const n = await buildSfxTrack(tl, sfxWav, cfg.sfx?.volume ?? 0.5);
      log(`ses efektleri: ${n} olay`);
    }
    await mux({
      video: silent,
      narration: narrationWav,
      sfx: sfxWav,
      music: script.music ?? cfg.audio.music,
      musicVolume: cfg.audio.musicVolume,
      duration: to,
      out: final,
      loudness: cfg.audio.loudness,
    });
    fs.rmSync(silent);
    log('HAZIR:', path.relative(ROOT, final));
    if (!args['no-quality']) {
      // quality gate: measured against the reference channel (tools/ref/quality.py)
      const q = spawnSync('python3', [path.join(ROOT, 'tools/ref/quality.py'), final, '--json', path.join(outDir, `quality.${style}.json`)], { encoding: 'utf8' });
      log('kalite kapısı:\n' + (q.stdout || q.stderr).trim());
    }
  }
}

main().catch((e) => {
  console.error('\n[geo] HATA:', e.stack || e.message);
  process.exit(1);
});
