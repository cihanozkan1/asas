# script.json biçimi

```jsonc
{
  "id": "kaliningrad",                 // çıktı klasörü adı
  "style": "geo",                      // varsayılan stil: geo | globe
  "voice": { "name": "en-US-AndrewNeural", "rate": "+12%" },   // opsiyonel, config'i ezer
  "music": "assets/music/x.mp3",       // opsiyonel
  "config": { ... },                   // opsiyonel: config/default.json üzerine birleşir
  "intro": { "dLat": -8, "dLon": 40, "zoom": 0.6 },            // açılış kamerası (hedefe göre)
  "imagery": [{ "bbox": [W, S, E, N], "width": 4096 }],         // yakın plan Sentinel-2 görüntüsü
  "meta": { "title", "description", "pinnedComment": [..], "tags": [..], "hashtags"?: [..], "credits"?: [..] },
  "scenes": [ Scene, ... ]
}
```

## Scene

| alan | açıklama |
|---|---|
| `text` | Anlatım cümlesi (İngilizce). Altyazı buradan kelime kelime üretilir. |
| `era` | `now` (uydu) veya `history` (geo stilinde parşömen harita) |
| `camera` | `{ "fit": [hedefler], "pad": 0.85, "zoomMul": 0.5 }` veya `{ "lat", "lon", "zoom" }`. Yoksa kamera yerinde kalır. `fit: "highlights"` sahnedeki vurguları sığdırır. `duration`, `lead` ayarlanabilir. |
| `transition` | `film` (film şeridi zaman geçişi), `flash`, `fade` |
| `show` | Öğe listesi (aşağıda) |
| `sources` | `[{ "claim", "url", "quote"?, "title"? }]` — iddia varsa zorunlu |
| `noClaim` | `true` → kaynak gerekmez (ör. "But look closer...") |
| `pauseAfter` | Sahne sonrası sessizlik (sn) |

## Hedefler (highlight / fit)

- `"RUS"`, `"RU"`, `"643"`, `"Russia"` — ülke (Natural Earth 1:10m)
- `{ "country": "FRA", "part": { "lat": 4, "lon": -53 } }` — ülkenin o noktayı içeren parçası (ör. Fransız Guyanası)
- `{ "admin1": "Kaliningrad", "country": "RUS" }` — eyalet/bölge (Natural Earth admin-1)
- `{ "countries": ["POL", "LTU"] }` veya `[hedef, hedef]` — birlikte tek şekil gibi çizilir
- `{ "circle": { "lat", "lon", "km" } }` — küçük yerler için daire
- `{ "geojson": "bolge.geojson" }` — video klasöründeki özel sınır

## Öğeler (`show`)

Ortak alanlar: `at` (sahne başından saniye **veya anlatımdaki kelime**, ör. `"at": "Poland"`),
`until` (saniye veya kelime), `hold` (kaç sahne daha kalsın, ya da `"end"`), `id`.
Aynı öğe ardışık sahnelerde tekrar yazılırsa kesintisiz devam eder (yeniden animasyon yapmaz).

| type | alanlar |
|---|---|
| `highlight` | `target`, `fill` (`"#e8742a"` veya `"flag:pl"` bayrak dolgusu), `fillOpacity`, `stroke`, `pattern: "hatch"` |
| `label` | `text`, `lat`/`lon` veya `screen: [x,y]` (0–1), `size`, `style` (`""` kalın beyaz, `serif`, `tag`, `yellow`), `dx`, `dy` |
| `flag` | `code` (flag-icons kodu, `eu` dahil), `lat`/`lon` veya `screen`, `size`, `pin` (direkli bayrak) |
| `icon` | `icon` (`"art:<ad>"` = `assets/art/<ad>.png`, bizim ürettiğimiz çizim; emoji yalnız `EMOJI_ART` eşlemesi varsa), konum, `size`. Eşlemesiz emoji derlemede hata verir (Twemoji kaldırıldı) |
| `ring` | `lat`, `lon`, `r` — elle çizilmiş sarı daire |
| `arrow` | `from`, `to` (`[lat, lon]`), `color`, `curve`, `width` |
| `line` | `from`, `to`, `label` (ör. `"65 km"`), kesikli mesafe çizgisi |
| `badge` | `text` (`"1"`), konum, `color` — numaralı bölge |
| `question` | konum — üç soru işareti |
| `year` | `value` (`"1945"`), `light: true` uydu üstünde beyaz — dev serif yıl |
| `stat` | `value` (`"1,000,000"`, `"$7.2M"` sayılar sayarak artar), `caption`, `size` |
| `stamp` | `text` (`"COLONIALISM"`) — kırmızı damga + karartma |
| `title` | `text` — üstte büyük başlık |

## Kurallar (validate ile denetlenir)

- Günün saati ifadesi yok (tonight, this morning, ...).
- İddia içeren her sahnede kaynak var.
- Hedef süre `video.targetSeconds` (varsayılan 55–95 sn); yaklaşık 165 kelime/dk (Kokoro). Kalite kapısı `tools/ref/quality.py` her render sonunda çalışır.

## Referans araç kutusu (page/extras.js; `tools/authoring/helpers.py` kısayolları)

| type | açıklama |
|---|---|
| `highlight` + `trace: true` (`trace()`) | Ülke/bölge sınırı bir noktadan başlayıp etrafı çizilerek açılır, sonra dolgu gelir. `neon` ile parlak kenar |
| `label` `style:'extrude'`, `anim:'giant'` (`giant()`) | Dev kabartmalı ad, haritaya küçülerek oturur |
| `pathtext` | Yazı bir yol/kıyı boyunca eğri akar |
| `crowd`, `pin`, `box` (`area()`), `beam`, `cloud`, `particles`, `flare`, `lens` | Kalabalık, iğne, kutu, ışın, bulut, parçacık (snow/rain/dust/embers/confetti), mercek parlaması, büyüteç |
| `photo`, `avatar`, `react`, `link` | Üretilmiş B-roll kartı/tam ekran, sohbet avatarı, tepki yüzü (`art:emote_*`), bağlantı çizgisi |
| `timebar`, `orbit`, `handstamp`, `grade` | Zaman çubuğu, yörünge ikonları, el ile damga, renk ayarı (bw/thermal/sepia/danger/cold/dusk) |
| `route` (+`rider`, `mover`, `laser`, `nodes`, `follow` kamera) | Gemiye binen karakter (`rider_ship`), yürüyen karakter (`walker`), lazer/ateş/düğümlü rota |
| `tilt` | Eğimli kamera + gökyüzü |
| `camera.then` | Sahne içinde ikinci/üçüncü kamera hamlesi; yoksa uzun sahnelere otomatik itme eklenir (`camera.noPush`) |
| `transition` | `film`, `flash`, `fade`, `wipe`, `zoom`, `slide`, `glitch`, `blast`, `ice`, `rewind`, `ink`; belirtilmeyen her kesime döngüyle zoom/slide/wipe |
| palet | `dark atlas neon chalk light blueprint pastel bw kraft` |

Otomatik: `enrich()` (helpers.save) cümleden tepki yüzü seçer (think/laugh/cry/angry/shock/cool); `tools/storyboard.py <id>` `videos/<id>/storyboard.md` üretir.
