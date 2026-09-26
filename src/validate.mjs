// Script checks that run before anything is rendered.
import { normWord } from './util.mjs';
const TIME_OF_DAY = /\b(tonight|this (morning|afternoon|evening)|good (morning|evening|night)|last night|tomorrow (morning|night)|yesterday (morning|evening))\b/i;

export function validateScript(script, cfg) {
  const errors = [];
  const warnings = [];
  if (!script.id) errors.push('script.id eksik');
  if (!script.scenes?.length) errors.push('Sahne yok');
  const title = script.meta?.title || '';
  if (!/^(why|how|what|the)\b/i.test(title)) warnings.push(`Başlık "Why/How..." ile başlamıyor: ${title}`);
  let words = 0;
  (script.scenes || []).forEach((s, i) => {
    const n = `Sahne ${i + 1}`;
    if (!s.text?.trim()) errors.push(`${n}: text boş`);
    if (TIME_OF_DAY.test(s.text || '')) errors.push(`${n}: günün saati ifadesi var ("${s.text.match(TIME_OF_DAY)[0]}")`);
    if (!s.noClaim && !(s.sources && s.sources.length)) errors.push(`${n}: kaynak yok (iddia yoksa "noClaim": true)`);
    for (const src of s.sources || []) if (!/^https?:\/\//.test(src.url || '')) errors.push(`${n}: geçersiz kaynak URL`);
    words += (s.text || '').split(/\s+/).filter(Boolean).length;
    // every word-based timing ("at": "Russia") must appear in the narration text
    const tw = (s.text || '').split(/\s+/).map(normWord).filter(Boolean);
    const has = (phrase) => {
      const want = String(phrase).split(/\s+/).map(normWord).filter(Boolean);
      return tw.some((_, i) => want.every((w, j) => tw[i + j] === w || (j === want.length - 1 && tw[i + j]?.startsWith(w))));
    };
    for (const el of s.show || []) {
      const specs = [el.at, el.until, el.moveAt, ...(el.steps || []).map((x) => x.at), ...(el.morph || []).map((x) => x.at)];
      for (const sp of specs) if (typeof sp === 'string' && !has(sp)) errors.push(`${n}: "${sp}" kelimesi metinde yok (${el.type})`);
    }
  });
  const estSec = words / (cfg.voice.estWordsPerMin / 60);
  const [lo, hi] = cfg.video.targetSeconds;
  if (estSec < lo || estSec > hi) warnings.push(`Tahmini süre ${estSec.toFixed(0)} sn (hedef ${lo}-${hi} sn), ${words} kelime`);
  return { errors, warnings, words, estSec };
}
