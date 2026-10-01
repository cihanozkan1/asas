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

## Retention rules from the user (saved verbatim, 2nd round)
"Bir video üreticisi/içerik stratejisti gibi düşünmeni istiyorum. Hazırlayacağın dikey videoların (Shorts/Reels/TikTok) izleyiciye en etkili, sürükleyici ve profesyonel şekilde aktarılması için şu kurallara kesinlikle uyman gerekiyor:
1. İlk 3 Saniye Kuralı (The Hook): Video başlar başlamaz (ilk 1 saniyede) merak, şok veya yüksek değer algısı yaratan bir cümleyle başla. Asla 'Merhaba', 'Kanalıma hoş geldiniz' gibi zaman kaybettiren girişler yapma. Ekranda ilk saniyede büyük, okunması kolay ve merak uyandırıcı bir başlık (Text Hook) bulunmalı.
2. Yüksek Tempo ve Dinamik Kurgu: Konuşmalar arasındaki tüm nefes boşluklarını sil. Görsel, açı veya odak her 2-3 saniyede bir değişmeli; sabit görüntü yok, aralara konuyla ilgili destekleyici görüntüler (B-Roll) ekle.
3. Altyazı ve Görsel Destek: Söylenen her kelime dinamik, renkli, hareketli altyazı olarak gelsin. Önemli kelimeleri sarı, kırmızı veya yeşil gibi renklerle vurgula. Altyazılarla eş zamanlı hafif ses efektleri (pop, woosh, dın) ve uygun emojiler kullan.
4. Bilgi Yoğunluğu ve Netlik: En kısa, en vurucu haliyle anlat; gereksiz detayı kırp; video 'hap bilgi' kıvamında olsun.
5. Kusursuz Döngü: Son cümleyi öyle ayarla ki video başa döndüğünde anlamlı bir cümle tamamlansın; izleyici bittiğini anlamadan ikinci kez izlemeye başlasın."
Money matters: these videos must earn, so retention beats novelty. Research notes: `docs/SHORTS_TAKTIKLERI.md`.

## Quality rules from the user (3rd round)
- No confetti/sparkle text effects; effects must suit the calm map style.
- No blur on zoom-out. To emphasise something: dim the surroundings slightly and keep the subject bright (spotlight).
- A country made of several parts: put the flag/fill on EVERY part, never only the largest.
- Stamp scene: the stamp comes straight down from above, same size as the text, presses, lifts.
- Do not repeat the same texts/effects/sounds in every video: per-video variety, fewer effects.

## Quality rules from the user (4th round, after reviewing the five videos)
- The reference channel was given to judge variety and success, NOT to copy it: make our own, varied, successful videos.
- No filled/framed text (no pills, boxes, plates behind text): plain text with outline + soft shadow only.
- A label must never cover the subject (marked point, highlighted town/area): small highlighted areas count as obstacles.
- No logic leftovers: a ship route/stamp/character from one scene must not stay into a scene of another era/view;
  ships sail on water; no person standing on top of a ship; flags must not overlap or reappear when zoomed in.
- Sound effects quiet and soft (not disturbing). Every video must be reviewed frame by frame by me before delivery.
- Effects must match the story and be reusable in any video: `eruption` (lava, ash, glow), siege (`wall` with `siege`: cannons fire,
  balls hit, walls crumble). Add more such effects when a video's story calls for one (earthquake, flood, fire...).
- Close zoom needs matching imagery: keep follow-camera zooms high enough for the fine Sentinel box; no blurry base showing.

## Toolbox rules (5th round: build tools so we do not fix errors video by video)
- Routes: never hand-type road/ship coordinates. Use `road()` / `sea_points()` / `sea_lane()` (helpers.py); `tools/validate_routes.mjs` is a render gate.
- Real VFX (explosion, fire, volcano, dust, debris): use `clip()` with footage ingested by `tools/vfx_ingest.py` (see `docs/ARAC_KUTUSU.md`); only free/PD/CC0 or licence-checked free packs, licence logged in `docs/LISANSLAR.md`; no logos/watermarks.
- The user does not want to check every video by hand: run the automatic gates (routes, labels, overlaps) and fix before showing.
