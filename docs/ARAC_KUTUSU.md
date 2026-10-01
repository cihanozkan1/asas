# Araç kutusu (Ekim 2026) — `ARASTIRMA_VIDEO_AS_CODE.md` içindeki her şey eklendi

Kaynak liste: `docs/ARASTIRMA_VIDEO_AS_CODE.md` (kullanıcının araştırması). Durum/önem analizi: `docs/ANALIZ_ARASTIRMA.md`.
Hat: ana video motoru (Node + Chromium sayfası, `scripts/pipeline.mjs`) aynen kalır; yeni araçlar **efekt fabrikası** olarak saydam klip üretir
ve `clip()` elemanıyla videoya girer (`assets/vfx/<ad>/`, WebP kare dizisi + alfa).

## A. Rota mantığı
| Araç | Kullanım |
|---|---|
| `road([(lat,lon),...], at)` | Natural Earth yol ağında gerçek yol rotası (`tools/roadroute.py`) |
| `sea_points(a,b)`, `sea_lane(a,b,at)`, `ship(sea_points(a,b),...)` | searoute ile karadan geçmeyen deniz yolu |
| `npm run routes:check` / `tools/validate_routes.mjs` | gemi suda, araç karada mı; render kapısı (`--skip-route-check` ile atlanır) |
| `node tools/turf_route.mjs smooth|chunk|along|slice|length|nearest ...` | Turf.js: bezierSpline, lineChunk, along, lineSliceAlong, nearestPointOnLine |

## B. Klip kütüphanesi ve `clip()`
`clip('<ad>', at, lat=, lon=, size=, screen=[x,y], blend='screen', loop=True, speed=1.0)`. Videoda kullanılan klipler `assets/vfx/MANIFEST.json`'dadır.
| Kaynak | Komut | Not |
|---|---|---|
| Noto animasyonlu emoji (60 seçili: 💥🔥🌋🌪️🎆💀🚀☄️🎯🛸⚡🌧️❄️💧🩸🌊🌍🎉✨🚩🚨…) | `npm run vfx:emoji` (`tools/ingest_emoji.py`), tümü: `npm run emoji:fetch` | **CC BY 4.0: açıklamaya atıf** — pipeline `emoji_*` klip kullanılınca upload metnine "Animated emoji: Google Noto Emoji (CC BY 4.0)" ekler. Adlar: `assets/vfx/emoji_<ad>` |
| Herhangi bir indirilen video (ücretsiz paketler, ProRes/MOV/WebM alfa, siyah zemin, yeşil perde) | `python3 tools/vfx_ingest.py dosya ad --key alpha|black|green|none --license ... --source ...` | siyah zeminli ateş/duman → `--key black` |
| Wikimedia Commons (yalnız kamu malı/CC0) | `tools/commons_search.py "..."`, `tools/vfx_fetch.py "File:..." ad` | logo/zaman damgası olan kayıtları kullanma |
| Remotion kompozisyonları | `npm run vfx:remotion -- <Kompozisyon> <klipAdı> --props '{...}' --frames 0-59` | aşağıda (C) |
| Python / Matplotlib / Cartopy / Manim çıktıları | `tools/py/*` (D) | `vfx_ingest.py` ile içeri |
Ücretsiz profesyonel paketler (hesap açıp elle indirilir → `vfx_ingest.py`): [ActionVFX ücretsiz](https://www.actionvfx.com/blog/450-free-vfx-stock-footage-assets-ready-for-download), [FX Elements](https://www.fxelements.com/free), [MyCreativeFX](https://mycreativefx.com/), [PremiumBeat Detonate](https://www.premiumbeat.com/blog/free-explosion-sfx-vfx-elements/). Lisans metni okunur, `--license` ile kayda geçer.

## C. Remotion çalışma alanı (`remotion/`)
Kurulum: `npm run remotion:setup` (+ `tools/chrome` sarmalayıcı `remotion/chrome-wrapper.sh`: tam Chromium + yazılımsal WebGL2 bayrakları; GPU'suz sunucuda MapLibre/deck.gl/three bununla çalışır). Stüdyo: `npm run remotion:studio`.
| Paket (hepsi `remotion/package.json`'da) | Kullanım |
|---|---|
| `remotion`, `@remotion/cli`, `@remotion/bundler`, `@remotion/renderer` 4.0.532 | render motoru |
| `@remotion/animated-emoji` | `EmojiPop` kompozisyonu (varlıklar `remotion/public/animated-emoji/`, `npm run emoji:fetch`) |
| `@remotion/lottie` + `lottie-web` | `LottieBurst` (herhangi bir Lottie JSON `remotion/public/lottie/`; örnek: `burst.json`) |
| `<AnimatedImage>`, `@remotion/gif` | `GifLayer` (GIF/WebP/APNG/AVIF; `useGif` ile Safari-uyumlu `<Gif>`) |
| `maplibre-gl` 5.x (6.x'in worker'ı Remotion webpack'inde çalışmıyor) | `GlowBorder`: üç katmanlı parlayan sınır (halo + halo + çekirdek) + dolgu, nabız; `ArmyArrow` |
| `@turf/turf` | `ArmyArrow`: bezierSpline + lineSliceAlong büyüyen ok, `along` ile ok başı ve takip kamerası (`jumpTo`) |
| `deck.gl`, `@deck.gl/core|layers|geo-layers|mapbox`, `react-map-gl` | `TripsDemo`: TripsLayer (izli çoklu ordu) + ArcLayer, `currentTime` = kare |
| `globe.gl`, `react-globe.gl`, `three` 0.186, `@react-three/fiber`, `@remotion/three` | `GlobeArcs`: küre üzerinde ark ve halka, kamera kare başına |
| `mapbox-gl`, `@types/mapbox-gl` | yalnız kurulu (ticari lisans/token ister, kullanmıyoruz) |
Resmi şablonlar `reference-code/` içinde (gitignore): `maplibre-example`, `mapbox-example`, `template-three`, `animated-emoji`, `skills`, `deck.gl-trips`, `globe.gl`, `maplibre-gl-js`, `turf`, `BlenderGIS`, `world-atlas`.
Remotion Agent Skills: `.claude/skills/remotion-best-practices/` (içinde `remotion-maps`, `remotion-create`, `remotion-render` …).
Deterministik render kuralları: `interactive:false`, `fadeDuration:0`, `delayRender/continueRender`, `--concurrency=1` (`remotion.config.ts`), her karede `jumpTo` (flyTo yok).
Lisans: Remotion ≤3 çalışanlı kâr amaçlı şirket için ücretsiz; 4+ için Company License.

## D. Python yığını
Kurulu: MoviePy 2, ffmpeg-python, Pillow, Matplotlib, GeoPandas, Shapely, PyProj, Cartopy, Plotly, Datashader, leafmap, Manim Community, searoute, scipy, OpenCV (oturum açılışında `.claude/hooks/session-start.sh` temel paketleri kurar; Manim için `apt install libcairo2-dev libpango1.0-dev pkg-config`).
| Betik | Ne yapar |
|---|---|
| `tools/py/glow_border.py "Turkey" ad` | GeoPandas + `patheffects` glow + Gaussian bloom → saydam klip |
| `tools/py/route_anim.py ad "lat,lon" ...` | Cartopy ortografik küre, Shapely `interpolate` ile büyüyen rota, uç noktayı izleyen kamera → klip |
| `tools/py/ffmpeg_overlay.py in.mp4 out.mp4 emoji.gif --at x,y --t a,b [--moviepy]` | FFmpeg `overlay=…enable='between(t,a,b)'` ve MoviePy v2 ile bitmiş videoya zamanlı emoji/GIF |
| `tools/py/density.py out.png` | Datashader yoğunluk haritası (göç, şehirler) |
| `tools/py/manim_arrow.py` | Manim: büyüyen ok + yazı; `manim -t -ql ...` sonra `vfx_ingest.py` |
| leafmap | kurulu (MapLibre "animate a line" Python portu; notebook odaklı) |
Plotly choropleth ve diğer ek çıktılar için aynı kalıp: kare üret → `vfx_ingest.py`.

## E. Veri
`npm run geodata` → `data/cache/ne/` (Natural Earth 10m/50m/110m ülkeler, admin-1, yollar, demiryolları, nehirler, göller, kıyı, okyanus, yerleşimler, havalimanları, limanlar, buzullar, bölgeler, saat dilimleri, graticule; kamu malı) + `reference-code/world-atlas`. Motor `world-atlas` (npm) ve tarihî sınırlar (aourednik, GPL-3.0 notu `docs/LISANSLAR.md`) kullanır. Tarihî sınırlar Natural Earth'te yok.

## F. Blender
`npm run blender:setup` → Blender 4.2 LTS + BlenderGIS (`tools/vendor/BlenderGIS`, GPL-3.0, yalnız araç) kurar; `tools/blender/blender.sh -b ...`. GPU'suz sunucuda yavaş: sinematik arazi uçuşu için yerel makine.

## G. Eski araçlar (kısa)
`eruption`, `wall`+`siege` (kendi yazdığımız, zayıf; gerçek klip varsa `clip` tercih), Sentinel-2, FLUX çizimleri, Kokoro TTS.
