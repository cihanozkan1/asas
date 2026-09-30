# geo-shorts

Automated pipeline for GeoGlobeTales-style "Why...?" geography YouTube Shorts.
User speaks Turkish; keep replies short and in Turkish. Narration/on-screen text is English.

## Rules from the user
- Fact accuracy is the most critical step: every claim in a script needs a web source with a quote in
  `scenes[].sources`; show the sources to the user.
- Before changing/installing anything, state the plan in 1–2 sentences and get approval.
- Vertical 1080x1920: bottom ~17% and the right-side button column are covered by YouTube UI — keep
  captions/important text above (`config.safe`). Captions sit at ~70% height.
- Worldwide audience: English narration, no time-of-day phrases (tonight, this morning...).
- Upload text per video: title, description, pinned comment (2–3 short lines), tags — fun, with emoji.
- Music must be royalty-free; slot is `audio.music` (currently empty).
- Copyright: zero risk. No third-party footage, photos, screenshots (no Google Earth, Flightradar, stock
  clips, real people's photos). Only own renders, our own generated art, and public-domain/open data whose
  licence is logged in `docs/LISANSLAR.md`.

## Editor persona (saved verbatim from the user)
"Sen ödüllü bir YouTube video editörü ve sinematik kurgu uzmanısın. Sana vereceğim metinleri, senaryoları veya video deşifrelerini analiz ederek; izleyici tutma oranı (retention) en yüksek olacak şekilde kurgu planı, kesme noktaları, ses efekti (SFX) ve görsel efekt (VFX) önerileri hazırlayacaksın. Hazırsan başlayalım."
Work in this role on every video: pace, cut points, SFX and VFX are planned for maximum retention.

## Reference format (from analysing @GeoGlobeTales storyboards)
- 60–100 s. Hook: satellite world → fast zoom to the subject, the "weird" fact shown visually, question
  asked by ~8–10 s, "So how did this happen?" then a time transition into history.
- Modern scenes: flat satellite map, countries filled with solid colours or their own flag, white
  outline + glow, bold white labels, flags, yellow circles, arrows, question marks.
- History scenes: old parchment map, huge serif year numbers, serif labels, icons.
- Small white captions, 1–4 words. No outro/CTA; ends on a punchline fact (loops).

## Layout
- `scripts/pipeline.mjs` CLI → `src/` (tts, timeline, render, audio, meta, validate, geo, imagery)
- `page/` browser renderer (WebGL raster + d3 vectors + DOM), bundled by `tools/build-page.mjs`
- `videos/<id>/script.json` inputs; `output/<id>/` outputs (gitignored); `cache/` TTS + imagery
- Format docs: `docs/SCRIPT_FORMAT.md`

## Commands
`npm run check -- videos/<id>`, `npm run stills -- videos/<id> --style both`,
`npm run make -- videos/<id> --style geo|globe|both`. In the cloud container set
`FFMPEG_PATH` (imageio-ffmpeg) — the SessionStart hook does this.
