// Narration assembly (scene clips + pauses) and final audio/video mux.
import fs from 'node:fs';
import path from 'node:path';
import { SAMPLE_RATE, writeWav, runFfmpeg, ROOT, log } from './util.mjs';
import { synthScene } from './tts.mjs';

export async function buildNarration(script, cfg, provider, outWav) {
  const voice = { ...cfg.voice, ...(script.voice || {}) };
  const clips = [];
  for (let i = 0; i < script.scenes.length; i++) {
    const s = script.scenes[i];
    process.stdout.write(`\r[geo] seslendirme ${i + 1}/${script.scenes.length}   `);
    clips.push(await synthScene(s.text, voice, provider));
  }
  process.stdout.write('\n');
  const lead = cfg.voice.leadIn;
  const scenes = [];
  let t = lead;
  const parts = [new Float32Array(Math.round(lead * SAMPLE_RATE))];
  for (let i = 0; i < clips.length; i++) {
    const c = clips[i];
    const dur = c.samples.length / SAMPLE_RATE;
    const gap = script.scenes[i].pauseAfter ?? cfg.voice.sceneGap;
    scenes.push({
      start: i === 0 ? 0 : t,
      audioStart: t,
      words: c.words.map((w) => ({ text: w.text, start: t + Math.max(0, w.start), end: t + Math.min(dur, w.end) })),
    });
    parts.push(c.samples);
    parts.push(new Float32Array(Math.round(gap * SAMPLE_RATE)));
    t += dur + gap;
  }
  const speechEnd = t - (script.scenes.at(-1).pauseAfter ?? cfg.voice.sceneGap);
  const duration = speechEnd + cfg.video.tail;
  for (let i = 0; i < scenes.length; i++) scenes[i].end = i + 1 < scenes.length ? scenes[i + 1].start : duration;
  const total = parts.reduce((a, p) => a + p.length, 0);
  const all = new Float32Array(total);
  let o = 0;
  for (const p of parts) {
    all.set(p, o);
    o += p.length;
  }
  writeWav(outWav, all);
  return { scenes, duration, voice };
}

export async function mux({ video, narration, music, musicVolume, duration, out, loudness }) {
  const args = ['-y', '-i', video, '-i', narration];
  let filter;
  if (music) {
    const m = path.resolve(ROOT, music);
    if (!fs.existsSync(m)) throw new Error('Müzik dosyası yok: ' + m);
    args.push('-stream_loop', '-1', '-i', m);
    const fadeOut = Math.max(0, duration - 1.5).toFixed(2);
    filter =
      `[1:a]aresample=48000,apad,asplit=2[n1][n2];` +
      `[2:a]aresample=48000,volume=${musicVolume},afade=t=in:d=0.8,afade=t=out:st=${fadeOut}:d=1.5[m];` +
      `[m][n2]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=350[md];` +
      `[n1][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=${loudness}:TP=-1.5:LRA=11[a]`;
  } else {
    filter = `[1:a]aresample=48000,apad,loudnorm=I=${loudness}:TP=-1.5:LRA=11[a]`;
  }
  args.push('-filter_complex', filter, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
    '-t', duration.toFixed(3), '-movflags', '+faststart', out);
  log('ses + görüntü birleştiriliyor...');
  await runFfmpeg(args);
}
