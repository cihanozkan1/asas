# `ARASTIRMA_VIDEO_AS_CODE.md` analizi: bizde ne var, ne yok, ne kadar önemli (Ekim 2026)

> **Güncelleme:** bu analizdeki "Yok / Kısmen" olan her şey sonradan eklendi; ayrıntı ve kullanım `docs/ARAC_KUTUSU.md`'de. Aşağıdaki tablolar ekleme öncesi durumu gösterir.

Ölçüt: "Var" = repoda çalışıyor, "Kısmen" = benzeri var ama araştırmadaki kadar iyi değil, "Yok" = hiç yok. Önem: bizim hat için (Node + Chromium sayfası + d3-geo + kendi WebGL uydu katmanı, kare = zamanın saf fonksiyonu).

## 1. JavaScript / Remotion ekosistemi
| Araç | Durum | Önem | Not |
|---|---|---|---|
| Remotion (render motoru) | **Yok** | Orta | Motorumuzun yerine geçmesi büyük iş (50 video senaryosu, Sentinel imagery, kelime senkron altyazı). Değeri "efekt fabrikası" olarak büyük: saydam arka planlı klip üretip `clip()` ile içeri almak. Lisans: ≤3 çalışanlı şirket ücretsiz |
| @remotion/animated-emoji (Noto) | **Yok** | Yüksek | 💥🔥💣⚔️🌋 gibi hazır animasyonlu emoji; bizim stilimize (harita + emoji) uyar. CC BY 4.0: açıklamaya atıf yazmak gerekir |
| @remotion/lottie | **Yok** | Yüksek | Patlama/duman/kılıç Lottie animasyonları; lisansı dosya başına kontrol edilmeli (LottieFiles Simple License) |
| `<AnimatedImage>` / @remotion/gif | **Kısmen** | Orta | GIF/WebP oynatıcımız yok ama `clip` (WebP kare dizisi, alfa destekli) aynı işi görüyor; `vfx_ingest.py` GIF/WebP kabul eder |
| Remotion Agent Skills (`/remotion-maps`) | **Yok** | Düşük–Orta | Yalnız Remotion'a geçersek anlamlı |
| MapLibre GL JS | **Yok** | Düşük–Orta | Vektör harita + globe + 3B kamera verir ama uydu görüntümüz (Sentinel) onda yok; token'sız OpenFreeMap OSM tabanlı (atıf gerekir). Sinematik pitch/terrain gerekirse |
| Mapbox GL JS | **Yok** | Düşük | v2+ ticari lisans; kullanmamalıyız |
| deck.gl (TripsLayer, ArcLayer, GeoJsonLayer) | **Yok** | Orta | Çok ordulu, parlayan izli hareket ve yay (ark) bağlantısı. Bizde tek rota/ok var, iz solması ve ark yok |
| react-map-gl | **Yok** | Düşük | Yalnız MapLibre/Remotion yoluna girersek |
| Turf.js (along, lineSliceAlong, bezierSpline, lineChunk) | **Kısmen** | Düşük–Orta | Eşdeğerleri kendi kodumuzda (rota ilerlemesi, Catmull-Rom). Eklemek ucuz, `lineChunk`/`nearestPointOnLine` işe yarar |
| globe.gl / react-globe.gl | **Kısmen** | Düşük–Orta | Kendi globe modumuz var; ark ve yükselen poligon yok |
| lottie-web | **Yok** | Yüksek | Lottie'nin çekirdeği, sayfaya eklenirse Lottie doğrudan motorumuzda oynar |
| Hazır şablonlar (maplibre-example, mapbox-example, template-three, deck.gl trips) | **Yok** | Orta | Referans kod olarak değerli |

## 2. Python / FFmpeg / coğrafi veri
| Araç | Durum | Önem | Not |
|---|---|---|---|
| FFmpeg | **Var** (mux, kodlama, ses) | Yüksek | `overlay=enable='between(t,a,b)'` ile son aşama emoji/GIF bindirme **kullanmıyoruz** |
| Pillow | **Var** | Orta | Kare işleme (vfx_ingest) |
| OpenCV | **Var** | Orta | Analiz araçları (araştırmada yok, bizde var) |
| MoviePy v2 | **Yok** | Düşük | Kendi README'si FFmpeg'den yavaş diyor; üretimde gerekmez |
| ffmpeg-python | **Yok** | Düşük | 2019'dan beri sürümsüz; gerek yok |
| Matplotlib (patheffects glow, FuncAnimation) | **Yok** | Orta | Veri/diyagram odaklı videolar için; bizde glow zaten canvas'ta var |
| GeoPandas, Cartopy, Shapely | **Yok** | Orta | Veri işleme ve ortografik projeksiyon; Shapely rota/geometri için faydalı |
| Plotly, Datashader | **Yok** | Düşük–Orta | Göç/yoğunluk gibi veri videoları için |
| leafmap | **Yok** | Düşük | Notebook odaklı |
| Manim | **Yok** | Düşük–Orta | Temiz diyagram/ok animasyonu |
| BlenderGIS + Blender | **Yok** (Blender 4.2 geçici denendi) | Düşük (bu sunucuda) | GPU yok, sinematik arazi için ancak yerel makinede |
| Natural Earth (vektör + yollar) | **Var** | Yüksek | `world-atlas`, NE yolları, admin-1 |
| world-atlas / topojson | **Var** | Yüksek | |
| Tarihî sınırlar | **Var** | Yüksek | aourednik (GPL-3.0 notu `docs/LISANSLAR.md`'de) |

## 3. Efekt bazında: bizde ne kadar iyi?
| Efekt (araştırmadaki) | Bizdeki karşılığı | Kalite (dürüst) |
|---|---|---|
| Koordinata bağlı emoji/patlama | `icon`, `art:*` (FLUX çizimler), `react`, `scatter` | Çizimler iyi; **hareketli patlama/ateş yok**. Kendi `eruption` ve `siege` yaptığım efektler zayıf, videolardan çıkarıldı |
| Parlayan sınır | `highlight` + `neon`, `trace`, glow, bayrak dolgusu, spot karartma | **İyi** (parça başına bayrak, glow, spot çalışıyor) |
| Büyüyen ordu oku / rota + takip kamerası | `route` (`drawDur`, `laser`, `follow` kamera, `mover`), `arrow`, `wall`, gerçek yol/deniz geometrisi (yeni) | **İyi**; çok ordulu iz solması ve ark katmanı yok |
| Deterministik kare | `GG.frame(t)` saf fonksiyon | **Çok iyi** (Remotion'un ana kuralı bizde baştan var) |
| Sinematik 3B/arazi | Yok (kamera kuş bakışı, hafif sway) | **Zayıf**, ayrı bir yetenek |
| Gerçek patlama klibi | `clip` elemanı + `vfx_ingest.py` hazır, kütüphane **boş** | Altyapı hazır, içerik yok |

## 4. Önem sırası (ekleme planı)
1. **Lottie + Noto animasyonlu emoji** → `clip` kütüphanesine saydam dizi olarak (patlama, ateş, bomba, kılıç). Hızlı ve stilimize uygun.
2. **Remotion'ı yalnız efekt fabrikası** olarak kur (saydam klip render → `vfx_ingest`), maplibre-example ve skill'leri referans olarak al.
3. **deck.gl TripsLayer/ArcLayer** mantığını kendi motorumuza: iz solması ve ark elemanı (veya Remotion içinde render edip klip yap).
4. **Turf.js** ve **Shapely**: rota yardımcıları, `nearestPointOnLine`, `lineChunk`.
5. Python yığını (Matplotlib, GeoPandas, Cartopy, Plotly, Datashader, MoviePy, ffmpeg-python, leafmap, Manim): veri videoları için kur; üretim yolu FFmpeg + kendi motorumuz kalır.
6. MapLibre/globe.gl/react-map-gl/Mapbox örnekleri: referans repo olarak `reference-code/` altına (gitignore), motor değişikliği yok.
7. BlenderGIS: yerel makine notu; bu sunucuda çalışmaz.

## 5. Lisans uyarıları (araştırmadan)
Remotion: ≤3 çalışanlı kâr amaçlı şirket ücretsiz, 4+ için ücretli. Mapbox GL v2+: ticari. Noto animasyonlu emoji: CC BY 4.0 (atıf). MapLibre: BSD. OpenFreeMap/OSM verisi: atıf.
