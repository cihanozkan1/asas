# Coğrafya/Tarih Shorts için "Video-as-Code" Araç Seti: Doğrulanmış Repolar, Dokümanlar ve Efekt Bazlı Seçim Rehberi (Ekim 2026)

GeoGlobeTales/Mapology/RealLifeLore tarzı otomatik harita videoları için şu an en sağlam ve en aktif kombinasyon **Remotion (~59k ⭐) + MapLibre GL JS (~11.6k ⭐) + Turf.js (~10.5k ⭐)**, gerekirse buna **deck.gl (~14.6k ⭐)** ekleniyor. Bu üçlü, Remotion ekibinin kendi resmi MapLibre/Mapbox örnek repolarında zaten birlikte kullanılıyor ve her üç efekti (zamanlı emoji/patlama overlay, parlayan sınır, büyüyen ordu oku + takip eden kamera) frame-doğru şekilde çözüyor. Python tarafı (MoviePy + FFmpeg + GeoPandas/Matplotlib) toplu üretim ve statik/2D haritalar için güçlü, ancak 3D kamera hareketlerinde JS/WebGL ekosisteminin gerisinde kalıyor.

## TL;DR

- **Ana öneri:** Remotion + MapLibre GL JS + Turf.js. Başlangıç noktası olarak resmi `remotion-dev/maplibre-example` (token gerektirmez) veya `remotion-dev/mapbox-example` reposunu klonlayın; ikisi de rota çizgisinin zamana göre açılmasını, kameranın rotayı takip etmesini ve Turf ile nokta hareketini hazır gösteriyor.
- **Efekt eşleştirmesi:** Emoji/patlama → `@remotion/animated-emoji` + `@remotion/lottie` + `<AnimatedImage>` (koordinatı `map.project()` ile piksele çevirerek); parlayan sınır → MapLibre'de üst üste bindirilmiş `line` katmanları (bulanık geniş çizgi + keskin ince çizgi) + yarı saydam `fill`; ordu oku → Turf `lineSliceAlong`/`along` + MapLibre/Mapbox `line-gradient`/`line-progress` veya deck.gl `TripsLayer`.
- **Python alternatifi:** GeoPandas + Matplotlib `patheffects` (glow) + `FuncAnimation` ile kare üretip MoviePy v2 / FFmpeg `overlay=...:enable='between(t,a,b)'` ile emoji/PNG bindirin; 3D/dünya küresi sahneleri için Manim veya BlenderGIS. Python yolu ucuz ve toplu üretime uygun ama sinematik kamera için daha fazla el emeği ister.

## Key Findings

1. **Remotion, bu niş için fiilî standart.** star-history verisine göre `remotion-dev/remotion` Eylül 2026 itibarıyla ~59.1k yıldız, 422 katkıcıya sahip ve haftada ~665 yeni yıldız alıyor; Ocak 2026'da GitHub Trending'de 1 numaraya çıktı.\[1\] Remotion'ın resmi Agent Skills listesinde ayrı bir `/remotion-maps` becerisi var ve bu beceri "statik haritalar, animasyonlu rotalar ve işaretçiler, coğrafi açıklayıcılar, Mapbox, MapLibre, MapTiler, GeoJSON ve CesiumJS ile 3D coğrafi uçuşlar" için tanımlanmış.\[2\] Yani Remotion ekibi coğrafi açıklayıcı videoları açıkça hedef kullanım senaryosu olarak görüyor.
2. **Resmi şablonlar küçük ama yetkili.** `remotion-dev/mapbox-example` yalnızca ~38 yıldızlı, `remotion-dev/maplibre-example` ise ~2 yıldızlı (çok yeni).\[3\]\[4\] Normalde "küçük proje" eşiğinin altında kalırlar, ancak bunlar doğrudan Remotion çekirdek ekibinin resmi referans uygulamaları; yıldız sayısı popülerliği değil, yeniliği yansıtıyor. Bu yüzden listeye alındılar.
3. **MapLibre, Mapbox'a karşı pratik avantajlı.** MapLibre örneği token gerektirmiyor (OpenFreeMap stili kullanıyor).\[3\] Mapbox örneği ise "render birden fazla çekirdekte yapıldığı için Mapbox hesabınıza daha fazla harita başlatma ücreti yansıyabilir" uyarısı veriyor.\[4\] Stadia Maps'in Aralık 2020 tarihli yazısına göre Mapbox GL JS, 8 Aralık 2020'deki v2 sürümüyle birlikte "Mapbox ile aktif bir ticari lisans ve abonelik sözleşmesi" gerektirecek şekilde yeniden lisanslandı; MapTiler'a göre MapLibre, BSD lisanslı son sürüm olan Mapbox GL JS 1.13 tabanlıdır ve maplibre-gl-js README'sine göre 3-Clause BSD lisanslıdır.
4. **Deterministik render kuralları kritik.** Her iki resmi örnek de aynı kuralları uyguluyor: `angle` OpenGL renderer, `--concurrency=1`, `interactive: false` ve `fadeDuration: 0` ile harita içi animasyonların kapatılması, ayrıca `delayRender()`/`continueRender()` ile kare başına yüklemenin beklenmesi.\[3\]\[4\] Bunlar uygulanmazsa karelerde titreme/eksik tile görülür.
5. **Python tarafında MoviePy yavaşladı.** MoviePy (~14.9k ⭐) v2.0 ile büyük kırıcı API değişikliği yaptı (`set_position` → `with_position` vb.) ve README'si numpy dönüşümü nedeniyle "doğrudan ffmpeg kullanmaktan daha yavaş" olduğunu kabul ediyor.\[5\] `ffmpeg-python` (~11k ⭐; Libraries.io'ya göre 10.7K yıldız, 22 katkıcı) ise PyPI'daki son sürümü 0.2.0'ın 6 Temmuz 2019 tarihli olmasıyla 7 yılı aşkın süredir yeni sürüm almadı; çalışır ama "aktif bakım" kriterini zayıf karşılıyor.

## Details

### Sektör 1: JavaScript / TypeScript & Remotion Ekosistemi

| Araç | ~Yıldız | Rolü | Kaynak kod / doküman |
|---|---|---|---|
| Remotion | ~59k | React ile frame-bazlı video render motoru | https://github.com/remotion-dev/remotion · https://www.remotion.dev/docs/api |
| @remotion/animated-emoji | (monorepo içinde) | Google Noto Animated Emoji'yi Remotion bileşeni olarak sarar | https://www.remotion.dev/docs/animated-emoji/ · https://www.remotion.dev/docs/animated-emoji/animated-emoji · varlıklar: https://github.com/remotion-dev/animated-emoji |
| @remotion/lottie | (monorepo içinde) | Lottie JSON animasyonlarını Remotion zaman çizelgesine kilitler | https://www.npmjs.com/package/@remotion/lottie · https://www.remotion.dev/docs/lottie/lottiefiles · https://www.remotion.dev/docs/lottie/staticfile |
| `<AnimatedImage>` / @remotion/gif | (çekirdek) | GIF/APNG/AVIF/WebP katmanlarını kareye senkron oynatır | https://www.remotion.dev/docs/animatedimage · https://www.remotion.dev/docs/gif |
| Remotion Agent Skills (`/remotion-maps`) | — | AI ajanlar için harita animasyonu en iyi pratikleri | https://www.remotion.dev/docs/ai/skills |
| MapLibre GL JS | ~11.6k | Açık kaynak WebGL vektör harita motoru (globe projeksiyonu dahil) | https://github.com/maplibre/maplibre-gl-js · https://maplibre.org/maplibre-gl-js/docs/examples/ |
| Mapbox GL JS | ~12.4k |\[6\] Ticari lisanslı, FreeCamera API ve 3D terrain'de güçlü | https://github.com/mapbox/mapbox-gl-js |
| deck.gl | ~14.6k | Büyük veri katmanları: TripsLayer, ArcLayer, PathLayer, GeoJsonLayer | https://github.com/visgl/deck.gl · https://deck.gl/docs/api-reference/geo-layers/trips-layer |
| react-map-gl | ~8.5k |\[7\] MapLibre/Mapbox için React sarmalayıcı | https://github.com/visgl/react-map-gl |
| Turf.js | ~10.5k | Coğrafi geometri: along, lineSliceAlong, lineChunk, bezierSpline | https://github.com/Turfjs/turf · https://turfjs.org/docs/api/along |
| globe.gl / react-globe.gl | ~3.1k / ~1.5k | three.js tabanlı 3D dünya küresi: poligon, ark, halka katmanları | https://github.com/vasturiano/globe.gl · https://github.com/vasturiano/react-globe.gl |
| lottie-web | ~30k+ (doğrulanmadı) | Lottie oynatıcı çekirdeği (@remotion/lottie altında) | https://github.com/airbnb/lottie-web |

**Hazır şablon/başlangıç repoları (JS):**
- `remotion-dev/maplibre-example` — https://github.com/remotion-dev/maplibre-example — MapLibre haritasını Remotion kompozisyonunda render eder, kamerayı rota boyunca hareket ettirir, GeoJSON rota çizgisini zamanla açar, Turf ile noktayı rotada ilerletir. Token gerekmez.\[3\] **En iyi başlangıç noktası.**
- `remotion-dev/mapbox-example` — https://github.com/remotion-dev/mapbox-example — Aynı yaklaşımın Mapbox sürümü; ücretsiz Mapbox anahtarı gerekir.\[4\] Remotion'ın resmi kaynak listesinde (https://www.remotion.dev/docs/resources) "Mapbox example" olarak yer alır.\[8\] Not: Remotion dokümanlarında ayrı bir "Mapbox" kılavuz sayfası yerine bu repo ve `/remotion-maps` skill'i referans gösteriliyor.
- `remotion-dev/skills` — https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/remotion-maps/REFERENCE.md — Statik harita, Mapbox, MapTiler, CesiumJS seçeneklerini karşılaştıran resmi harita referansı.\[9\]
- deck.gl Trips örneği — https://github.com/visgl/deck.gl/blob/master/examples/website/trips/README.md — TripsLayer'ın bağımsız minimal sürümü.\[10\]

### Sektör 2: Python, FFmpeg & Coğrafi Veri Ekosistemi

| Araç | ~Yıldız | Rolü | Kaynak kod / doküman |
|---|---|---|---|
| MoviePy (v2) | ~14.9k |\[11\] Python video kompozisyonu; zamanlı/konumlu PNG-GIF katmanları | https://github.com/Zulko/moviepy · https://zulko.github.io/moviepy/reference/reference/moviepy.video.VideoClip.VideoClip.html |
| FFmpeg | ~50k+ (doğrulanmadı) | `overlay`, `enable`, `scale`, `fade` filtreleri ile son kompozisyon | https://github.com/FFmpeg/FFmpeg · https://ffmpeg.org/ffmpeg-filters.html#overlay-1 |
| ffmpeg-python | ~11k | FFmpeg filtre grafiklerini Python'dan kurma\[12\] (bakım yavaş) | https://github.com/kkroening/ffmpeg-python |
| Pillow | ~12–13k (doğrulanmadı) | Kare bazlı PNG bindirme/ölçekleme | https://github.com/python-pillow/Pillow |
| Matplotlib | ~20k+ (doğrulanmadı) | `patheffects` (glow/stroke) + `FuncAnimation` | https://github.com/matplotlib/matplotlib · https://matplotlib.org/stable/users/explain/artists/patheffects_guide.html · https://matplotlib.org/stable/api/patheffects_api.html |
| GeoPandas | ~4.5–5k (doğrulanmadı) | Shapefile/GeoJSON okuma, ülke seçme, çizim | https://github.com/geopandas/geopandas |
| Cartopy | ~1.4k+ (doğrulanmadı) | Matplotlib için harita projeksiyonları (ortografik "küre" görünümü) | https://github.com/SciTools/cartopy |
| Plotly | ~16k+ (doğrulanmadı) | Choropleth ve animasyon kareleri | https://github.com/plotly/plotly.py |
| Datashader | ~3.3k (doğrulanmadı) | Milyonlarca noktalık göç/yoğunluk görselleri | https://github.com/holoviz/datashader |
| leafmap | (doğrulanmadı, aktif) | Python'dan MapLibre katmanları; "animate a line" Python portu | https://leafmap.org/maplibre/animate_a_line/ |\[13\]
| Manim (3b1b) / Manim Community | ~93.8k / ~30k (ikincisi doğrulanmadı) | Matematiksel animasyon motoru;\[14\] harita ve ok animasyonları için esnek | https://github.com/3b1b/manim · https://github.com/ManimCommunity/manim |
| BlenderGIS | ~9.4k | Blender'a SRTM/OSM/Shapefile verisi alma;\[15\] sinematik 3D | https://github.com/domlysz/BlenderGIS |

**Sınır verisi kaynakları (her iki sektör için):**
- Natural Earth — https://github.com/nvkelso/natural-earth-vector — 1:10m/50m/110m ülke ve idari sınırlar (Shapefile/GeoJSON), kamu malı.
- world-atlas (TopoJSON) — https://github.com/topojson/world-atlas — Natural Earth'ten türetilmiş hafif `countries-50m.json` / `countries-110m.json`; web için ideal.
- Uyarı: Tarihî sınırlar (ör. 1914 Avrupası, Osmanlı dönemleri) bu setlerde yok; modern sınırlar üzerinden elle düzenleme veya ayrı tarihî veri setleri gerekir.

### Efekt 1 — Dinamik Emoji / Overlay (💥 ⚔️ 💣) Koordinata Bağlı

**Sektör 1 (en iyi):**
- `@remotion/animated-emoji` — Google Fonts Animated Emoji'yi sarar; v4.0.187'den beri mevcut. Varlıklar pakete dahil değil; `remotion-dev/animated-emoji` reposunun `public/` klasöründen kendi projenize kopyalamanız gerekiyor.\[16\]\[17\] Mevcut emoji listesi `getAvailableEmoji()` ile alınır (https://www.remotion.dev/docs/animated-emoji/get-available-emoji). \[18\]
- `@remotion/lottie` — LottieFiles'tan indirilen patlama/kılıç/duman animasyonları; Remotion zaman çizelgesiyle senkron, scrub edilebilir.\[19\]\[20\] After Effects'ten içe aktarma kılavuzu: https://www.remotion.dev/docs/after-effects \[21\]
- `<AnimatedImage>` — GIF/APNG/AVIF/WebP; ImageDecoder API kullandığı için Chrome/Firefox'ta çalışır. Safari gerekiyorsa `@remotion/gif` `<Gif>` bileşeni.\[22\]\[23\]
- **Koordinat → piksel yöntemi:** Her karede `map.project([lon, lat])` ile piksel konumunu alın, emoji bileşenini `position: absolute` ile oraya yerleştirin; boyut için Remotion'ın `interpolate()`/`spring()` fonksiyonlarını `useCurrentFrame()` ile kullanın, görünme zamanı için `<Sequence from={...}>`. Alternatif olarak emojiyi doğrudan harita içine koymak için MapLibre "Add an animated icon to the map" örneği (https://maplibre.org/maplibre-gl-js/docs/examples/) \[24\] veya deck.gl `IconLayer` kullanılabilir.

**Sektör 2:**
- MoviePy v2: `ImageClip("boom.png").with_position((x, y)).with_start(t).with_duration(d)` ve konum için `with_position(lambda t: ...)` ile hareket; `CompositeVideoClip` ile birleştirme. `layer` özelliği üst üste gelme sırasını belirler.\[25\]
- FFmpeg: `overlay=x:y:enable='between(t,5,10)'` ile saniye-doğru görünme; birden fazla zaman penceresi `between(t,2,5)+between(t,10,15)` ile; animasyonlu GIF için `-stream_loop -1 -i boom.gif ... overlay=...:shortest=1`; ölçek için `scale`, solma için `fade=...:alpha=1`.\[26\]\[27\]
- Lat/Lon → piksel: Matplotlib/Cartopy'de `ax.transData.transform()` (Cartopy'de önce projeksiyon dönüşümü) ile hesaplayıp FFmpeg/MoviePy'ye aktarın.
- Emoji kaynağı: Google Noto Animated Emoji (https://googlefonts.github.io/noto-emoji-animation/) — Lottie/GIF/WebP biçimlerinde, CC BY 4.0 lisanslı.\[28\]

### Efekt 2 — Parlayan Ülke/Bölge Sınırları (Glow)

**Sektör 1 (en iyi):**
- **MapLibre/Mapbox katman yığını:** Aynı GeoJSON kaynağından (world-atlas'tan dönüştürülmüş veya Natural Earth) üç katman: (1) `fill` + `fill-opacity: 0.25–0.4` yarı saydam dolgu, (2) geniş `line` + yüksek `line-blur` + düşük `line-opacity` (dış hale), (3) ince keskin `line` (çekirdek). `filter` ile yalnızca hedef ülke(ler) seçilir; parlamayı titretmek/nabız etkisi için `line-width`/`line-opacity` değerini `useCurrentFrame()` ile her karede `setPaintProperty` üzerinden güncelleyin.
- **deck.gl `GeoJsonLayer`** ile benzer çok-katmanlı yaklaşım; daha güçlü bloom için deck.gl üzerinde post-processing efektleri.
- **globe.gl** `polygonsData` + `polygonAltitude` ile ülkeyi küreden "yükselterek" vurgular; `polygonCapColor`/`polygonSideColor` ile yarı saydam renklendirme.\[29\]\[30\] Remotion içinde three.js tabanlı sahneler için `@remotion/three` (https://github.com/remotion-dev/template-three) kullanılabilir.\[31\]

**Sektör 2:**
- **Matplotlib patheffects:** `withStroke(linewidth=..., foreground=..., alpha=...)` katmanlarını kalından inceye, alfası artarak üst üste yığarak glow taklidi; `GeoPandas.plot(facecolor=..., alpha=0.3, edgecolor=...)` ile dolgu.\[32\]\[33\] Bu yaklaşım Text, Line2D ve Patch nesnelerinde çalışır.\[34\]\[35\]
- Plotly `choropleth` + `marker.line` hızlı alternatif; ancak gerçek "bulanık hale" yok.
- Gerçek bloom için: Matplotlib karesini Pillow `GaussianBlur` ile bulanıklaştırıp orijinalle `screen`/toplama modunda birleştirin (veya FFmpeg `gblur` + `blend`).

### Efekt 3 — Büyüyen Ordu Oku / Göç Rotası + Takip Eden Kamera

**Sektör 1 (en iyi):**
- **Turf.js:** `along` (https://turfjs.org/docs/api/along) çizgi boyunca belirli mesafede nokta verir\[36\] → ok başı/kamera hedefi; `lineSliceAlong` (https://turfjs.org/docs/api/lineSliceAlong) 0'dan `ilerleme × toplam uzunluk` mesafesine kadar alt çizgi verir\[37\] → büyüyen çizgi; `bezierSpline` (https://turfjs.org/docs/api/bezierSpline) köşeli rotayı yumuşak eğriye çevirir;\[38\] `lineChunk` (https://turfjs.org/docs/api/lineChunk) rotayı eşit parçalara böler\[39\] (aşamalı ilerleme).
- **MapLibre "Animate a line":** https://maplibre.org/maplibre-gl-js/docs/examples/animate-a-line/ — GeoJSON kaynağını her karede güncelleyerek çizgi uzatır.\[40\] Turf ile nokta hareketi: https://maplibre.org/maplibre-gl-js/docs/examples/animate-a-point-along-a-route/ \[41\]
- **`line-gradient` + `line-progress`:** https://docs.mapbox.com/mapbox-gl-js/example/line-gradient/ — Kaynakta `lineMetrics: true` zorunlu;\[42\]\[43\] `step` ifadesi ile `line-progress < ilerleme` bölümü renkli, kalanı saydam yapılarak çizgi tek GeoJSON ile "açılır". Mapbox'ın resmi blog yazısı (https://www.mapbox.com/blog/building-cinematic-route-animations-with-mapboxgl) bu tekniği `turf.along` ve FreeCamera API ile kamera takibiyle birleştiriyor.\[44\] Bilinen sınırlama: `line-gradient` yalnızca GeoJSON kaynaklarında çalışır ve çok yakın duraklarda hassasiyet sorunları raporlanmıştır.\[45\]\[46\]
- **Kamera:** Mapbox FreeCamera — https://docs.mapbox.com/mapbox-gl-js/example/free-camera-path/ ("Animate the camera along a path") ve https://docs.mapbox.com/mapbox-gl-js/example/free-camera-point/; `getFreeCameraOptions()`, `lookAtPoint()`, `setFreeCameraOptions()`.\[47\]\[48\]\[49\] MapLibre'de eşdeğeri `jumpTo({center, zoom, bearing, pitch})` çağrısını her karede yapmak (resmi maplibre-example'ın yaptığı budur). Remotion'da `flyTo`/`easeTo` gibi zamana bağlı geçişler yerine her karede `jumpTo` kullanın; aksi halde render deterministik olmaz.
- **deck.gl `TripsLayer`:** https://deck.gl/docs/api-reference/geo-layers/trips-layer — `getPath` + `getTimestamps` + `currentTime` + `trailLength`;\[50\]\[51\] `currentTime`'ı Remotion karesine bağlayınca çok sayıda ordunun aynı anda ilerlemesi için ideal. `ArcLayer` (https://deck.gl/docs/api-reference/layers/arc-layer) iki nokta arası kavisli bağlantılar\[52\] (ticaret/göç) için. Animasyon kılavuzu: https://deck.gl/docs/developer-guide/animations-and-transitions \[53\]
- **globe.gl ark katmanı:** `arcsData`, `arcDashLength`, `arcDashAnimateTime` ile küre üzerinde uçan oklar ("Emit Arcs on Click" örneği).\[54\]\[55\]

**Sektör 2:**
- Matplotlib/Cartopy + `FuncAnimation` (https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html): her karede `line.set_data(x[:i], y[:i])`; kamera takibi için `ax.set_extent()` değerini karede kaydırın. Rota yumuşatma için Shapely `interpolate()` (Turf `along` eşdeğeri).
- leafmap MapLibre portu (https://leafmap.org/maplibre/animate_a_line/) Python'dan MapLibre çizgi animasyonu yapar,\[13\] ancak etkileşimli/notebook odaklıdır; video render için ekran kaydı veya ek araç gerekir.
- Manim: `Create()`/`MoveAlongPath` ve kamera `frame.animate` ile çok temiz ok animasyonları; harita arka planını görüntü veya SVG olarak alır.
- BlenderGIS: gerçek arazi (SRTM) üzerinde Blender kamerası ile sinematik uçuş; en yüksek görsel kalite, en dik öğrenme eğrisi.

## Recommendations

1. **Yeni başlıyorsanız:** `remotion-dev/maplibre-example`'ı klonlayın → world-atlas'tan `countries-50m.json`'u GeoJSON'a çevirip glow katman yığınını ekleyin → `@remotion/animated-emoji` ve `@remotion/lottie` ile patlama/kılıç katmanlarını `map.project()` ile koordinata bağlayın. Bu tek repo üç efektin iskeletini zaten sağlıyor.
2. **Çok ordulu savaş sahneleri için:** MapLibre üzerine deck.gl `TripsLayer` ekleyin (`MapboxOverlay` interleaved modu); her ordu bir trip, `currentTime = frame`.\[56\]
3. **Sinematik 3D/arazi gerekiyorsa:** Mapbox GL JS + FreeCamera + terrain kullanın, ama Mapbox kullanım ücretini ve Remotion çoklu çekirdek render'ında artan harita yüklemelerini hesaba katın;\[4\] `--concurrency=1` ile render edin.\[4\]
4. **Toplu/ucuz üretim (günde onlarca Short):** Python hattı — GeoPandas + Matplotlib glow + FuncAnimation kareleri → FFmpeg `overlay`/`enable` ile emoji bindirme. MoviePy'yi prototip için kullanın, üretimde doğrudan FFmpeg komutlarına geçin (MoviePy kendi README'sinde daha yavaş olduğunu kabul ediyor).
5. **Lisans kontrolü:** Remotion'ın LICENSE.md dosyasına göre ücretsiz lisans bireyleri, en fazla 3 çalışanlı kâr amaçlı şirketleri ve kâr amacı gütmeyen kuruluşları kapsar; 4 ve daha fazla çalışanlı şirketler Company License almalıdır (remotion.pro/license: "Remotion for Automators için minimum aylık 100 $"). Stadia Maps'e göre Mapbox GL JS v2'yi kullanmak "Mapbox ile aktif bir ticari lisans ve abonelik sözleşmesi" gerektirir; Geoapify'a göre v2 Mapbox hesabı ve API token'ı olmadan çalışmaz. Noto animasyonlu emojiler CC BY 4.0 (atıf gerekli). Ticari kanal açmadan önce üçünü de kontrol edin.

## Caveats

- **Yıldız sayıları:** Remotion, MapLibre, deck.gl, Turf, globe.gl, react-globe.gl, MoviePy, ffmpeg-python, 3b1b/manim, BlenderGIS, Mapbox GL JS ve react-map-gl sayıları Ağustos–Eylül 2026 GitHub/star-history verilerinden doğrulandı. Tabloda "(doğrulanmadı)" olarak işaretlenen sayılar (FFmpeg, ManimCommunity, lottie-web, Pillow, Matplotlib, GeoPandas, Cartopy, Plotly, Datashader, Natural Earth, world-atlas) tahmini değerlerdir; repo URL'leri bilinen kanonik adreslerdir ama bu çalışmada tek tek açılmadı.
- **Doğrulanmayan iki doküman bağlantısı:** `ffmpeg.org/ffmpeg-filters.html#overlay-1` ve Matplotlib `FuncAnimation` API sayfası uzun süredir kullanılan standart adreslerdir, ancak bu araştırmada doğrudan açılmadı.
- **"Gerçek stüdyolar ne kullanıyor" sorusu:** GeoGlobeTales, Mapology veya RealLifeLore'un iş akışlarını kamuya açık şekilde belgeleyen bir kaynak bulunamadı; bu kanalların büyük olasılıkla After Effects/GEOlayers gibi ticari araçlar kullandığı varsayılabilir ama doğrulanmış değildir. Buradaki öneriler, bu görsel dili kodla yeniden üretmenin en sağlam açık kaynak yoludur.
- **Küçük ama resmi repolar:** `remotion-dev/mapbox-example` (~38 ⭐) ve `remotion-dev/maplibre-example` (~2 ⭐) yıldız eşiğinin altında olsa da Remotion çekirdek ekibinin resmi örnekleri olduğu için listeye alındı. ml-line-animation, mpl_visual_context gibi küçük topluluk paketleri bilinçli olarak dışarıda bırakıldı.
- **Tarihî sınırlar:** Natural Earth ve world-atlas modern sınırları içerir; tarihî imparatorluk/cephe hatları için ayrı veri veya elle çizim gerekir.

## Sources

1. [remotion-dev/remotion - 59.1k Stars · Global Rank #380](https://www.star-history.com/remotion-dev/remotion/)
2. [Agent Skills](https://www.remotion.dev/docs/ai/skills)
3. [GitHub - remotion-dev/maplibre-example](https://github.com/remotion-dev/maplibre-example)
4. [GitHub - remotion-dev/mapbox-example: Remotion Mapbox example](https://github.com/remotion-dev/mapbox-example)
5. [github.com](https://github.com/Zulko/moviepy)
6. [mapbox/mapbox-gl-js - 12.4k Stars · Global Rank #4218](https://www.star-history.com/mapbox/mapbox-gl-js/)
7. [visgl/react-map-gl - 8.5k Stars · Global Rank #6662](https://www.star-history.com/visgl/react-map-gl/)
8. [List of resources](https://www.remotion.dev/docs/resources)
9. [skills/skills/remotion-best-practices/remotion-maps/REFERENCE.md at main · remotion-dev/skills](https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/remotion-maps/REFERENCE.md)
10. [deck.gl/examples/website/trips/README.md at master · visgl/deck.gl](https://github.com/visgl/deck.gl/blob/master/examples/website/trips/README.md)
11. [Zulko/moviepy - 14.9k Stars · Global Rank #3319](https://www.star-history.com/zulko/moviepy/)
12. [kkroening/ffmpeg-python - 11k Stars · Global Rank #4873](https://www.star-history.com/kkroening/ffmpeg-python/)
13. [Animate a line - leafmap](https://leafmap.org/maplibre/animate_a_line/)
14. [3b1b/manim - 93.8k Stars · Global Rank #145](https://www.star-history.com/3b1b/manim/)
15. [domlysz/BlenderGIS - 9.4k Stars · Global Rank #5903](https://www.star-history.com/domlysz/blendergis/)
16. [@remotion/animated-emoji](https://www.remotion.dev/docs/animated-emoji/)
17. [\<AnimatedEmoji\>](https://www.remotion.dev/docs/animated-emoji/animated-emoji)
18. [getAvailableEmoji()](https://www.remotion.dev/docs/animated-emoji/get-available-emoji)
19. [Finding Lottie files to use](https://www.remotion.dev/docs/lottie/lottiefiles)
20. [Lottie Animations](https://deepwiki.com/remotion-dev/skills/5.4-lottie-animations)
21. [Import from After Effects](https://www.remotion.dev/docs/after-effects)
22. [\<AnimatedImage\>](https://www.remotion.dev/docs/animatedimage)
23. [\<Gif\>](https://www.remotion.dev/docs/gif/gif)
24. [Animate a marker](https://docs.maptiler.com/sdk-js/examples/animate-marker/)
25. [moviepy.video.VideoClip.VideoClip — MoviePy documentation](https://zulko.github.io/moviepy/reference/reference/moviepy.video.VideoClip.VideoClip.html)
26. [ffmpeg-engineering-handbook/docs/advanced/overlays.md at main · endcycles/ffmpeg-engineering-handbook](https://github.com/endcycles/ffmpeg-engineering-handbook/blob/main/docs/advanced/overlays.md)
27. [How to Add a Transparent Overlay on a Video using FFmpeg - Creatomate](https://creatomate.com/blog/how-to-add-a-transparent-overlay-on-a-video-using-ffmpeg)
28. [Noto Emoji](https://googlefonts.github.io/noto-emoji-files/)
29. [GitHub - vasturiano/globe.gl: UI component for Globe Data Visualization using ThreeJS/WebGL · GitHub](https://github.com/vasturiano/globe.gl)
30. [GitHub - mrienstra/vasturiano-globe.gl: UI component for Globe Data Visualization using ThreeJS/WebGL · GitHub](https://github.com/mrienstra/vasturiano-globe.gl)
31. [template three](https://github.com/remotion-dev/template-three)
32. [Path effects guide — Matplotlib 3.11.1 documentation](https://matplotlib.org/stable/users/explain/artists/patheffects_guide.html)
33. [Matplotlib - Path Effects](https://www.tutorialspoint.com/matplotlib/matplotlib_path_effects.htm)
34. [patheffects — Matplotlib 2.0.2 documentation](https://matplotlib.org/2.0.2/api/patheffects_api.html)
35. [matplotlib.patheffects — Matplotlib 3.11.1 documentation](https://matplotlib.org/stable/api/patheffects_api.html)
36. [along](https://turfjs.org/docs/api/along)
37. [lineSliceAlong](https://turfjs.org/docs/api/lineSliceAlong)
38. [bezierSpline](https://turfjs.org/docs/api/bezierSpline)
39. [lineChunk](https://turfjs.org/docs/api/lineChunk)
40. [Animate a line - MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/examples/animate-a-line/)
41. [Animate a point along a route - MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/examples/animate-a-point-along-a-route/)
42. [Create a gradient line using an expression](https://docs.mapbox.com/mapbox-gl-js/example/line-gradient/)
43. [Unable to use line-gradient paints styles for lines · Issue #858 · mapbox/mapbox-gl-draw](https://github.com/mapbox/mapbox-gl-draw/issues/858)
44. [How to create animated route tracking scenes - Mapbox Blog](https://www.mapbox.com/blog/building-cinematic-route-animations-with-mapboxgl)
45. [Limited Precision with line-gradient and line-progress linear interpolation · Issue #9728 · mapbox/mapbox-gl-js](https://github.com/mapbox/mapbox-gl-js/issues/9728)
46. [line-gradient for vector tile sources · Issue #8974 · mapbox/mapbox-gl-js](https://github.com/mapbox/mapbox-gl-js/issues/8974)
47. [Animate the camera around a point with 3D terrain](https://docs.mapbox.com/mapbox-gl-js/example/free-camera-point/)
48. [Animate the camera along a path](https://docs.mapbox.com/mapbox-gl-js/example/free-camera-path/)
49. [Properties and options](https://docs.mapbox.com/mapbox-gl-js/api/properties/)
50. [TripsLayer](https://deck.gl/docs/api-reference/geo-layers/trips-layer)
51. [deck.gl/docs/api-reference/geo-layers/trips-layer.md at 8.7-release · visgl/deck.gl](https://github.com/visgl/deck.gl/blob/8.7-release/docs/api-reference/geo-layers/trips-layer.md)
52. [ArcLayer](https://deck.gl/docs/api-reference/layers/arc-layer)
53. [Animations and Transitions](https://deck.gl/docs/developer-guide/animations-and-transitions)
54. [globe.gl/example/emit-arcs-on-click/index.html at master · vasturiano/globe.gl](https://github.com/vasturiano/globe.gl/blob/master/example/emit-arcs-on-click/index.html)
55. [globe.gl/example/random-arcs/index.html at master · vasturiano/globe.gl](https://github.com/vasturiano/globe.gl/blob/master/example/random-arcs/index.html)
56. [github.com](https://github.com/visgl/deck.gl/commit/fd1c1bbe7997dfba5c75e0cefdb4ca152a8ea764)
