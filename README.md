# geo-shorts — "Why...?" coğrafya Shorts üretim hattı

Senaryo JSON'undan tek komutla 1080×1920, 30 fps, anlatımlı ve altyazılı YouTube Short üretir:
harita/küre animasyonu + Edge TTS seslendirme + kelime zamanlamalı altyazı + (isteğe bağlı) müzik
+ yükleme metni (`.txt`) + kaynak raporu (`sources.md`).

İki görsel stil var (aynı senaryo ile ikisi de üretilebilir):

| Stil | Görünüm |
|---|---|
| `geo` | GeoGlobeTales tarzı: düz uydu haritası (günümüz sahneleri) + eski parşömen harita (`"era": "history"` sahneleri) |
| `globe` | Uzayda 3D dünya küresi, tüm sahneler uydu görüntüsü |

## Windows kurulumu (bir kez)

Gerekenler: Node.js 20+, Google Chrome, ffmpeg (PATH'te), git.

```powershell
git clone https://github.com/cihanozkan1/asas.git
cd asas
git checkout claude/sa-098kyg
npm install
npm run setup        # NASA Blue Marble + Natural Earth verisini indirir (~60 MB)
```

Chrome veya ffmpeg bulunamazsa yollarını verin:

```powershell
$env:CHROME_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$env:FFMPEG_PATH = "C:\ffmpeg\bin\ffmpeg.exe"
```

## Kullanım

```powershell
npm run check  -- videos/kaliningrad                 # senaryo kontrolü (kaynak, süre, yasak ifadeler)
npm run stills -- videos/kaliningrad --style both    # hızlı önizleme: 15 kare + kontakt sayfası
npm run make   -- videos/kaliningrad --style geo     # tam video
npm run make   -- videos/kaliningrad --style both    # iki stil birden
npm run voices                                       # İngilizce Edge seslerini listele
```

Çıktılar `output/<id>/` altında:

- `<id>_geo.mp4` / `<id>_globe.mp4` — yüklenecek video
- `<id>.txt` — başlık, açıklama, hashtag, kaynak satırları, sabit yorum, etiketler
- `sources.md` — senaryodaki her iddia + alıntı + kaynak linki
- `contact_<stil>.jpg` — önizleme kareleri (`--stills` ile)

Faydalı seçenekler: `--mock-tts` (internetsiz sessiz test), `--guides` (YouTube arayüz güvenli alanlarını
çizer), `--fps 15 --scale 0.5` (hızlı taslak render), `--from 20 --to 35` (kısmi render),
`--stills 20 --times 3,9,12` (belirli saniyeler).

## Yeni video eklemek

1. `videos/<id>/script.json` oluştur (biçim: [docs/SCRIPT_FORMAT.md](docs/SCRIPT_FORMAT.md)).
2. Her sahnedeki iddiaları kaynakla ve `sources` alanına alıntıyla yaz.
3. `npm run check` → `npm run stills` → gözle kontrol → `npm run make`.

## Müzik

Telifsiz bir parça seçildiğinde `assets/music/` içine koyup `config/default.json` → `audio.music`
alanına (veya senaryoya `"music": "assets/music/parca.mp3"`) yazın. Ses seviyesi `audio.musicVolume`;
anlatım sırasında müzik otomatik kısılır (ducking). Son miks −14 LUFS'e normalize edilir.

## Görüntü ve veri lisansları

- NASA Blue Marble Next Generation — kamu malı
- Sentinel-2 cloudless 2016, EOX — CC BY 4.0 (kaynak satırı `.txt` içine otomatik eklenir)
- Natural Earth — kamu malı; world-atlas (ISC)
- flag-icons (MIT), Twemoji grafikleri (CC BY 4.0), Montserrat / Playfair Display (OFL)
- Seslendirme: Microsoft Edge "Read Aloud" nöral sesleri (msedge-tts). Resmi olmayan bir uç noktadır;
  seri üretimde sorun çıkarsa Azure Speech (aynı sesler, ücretsiz katman) sağlayıcısı eklenebilir.

## Nasıl çalışır

```
script.json ──► validate ──► Edge TTS (sahne sahne, kelime zamanları, önbellek)
                                  │
                                  ▼
                        timeline (kamera, öğe zamanları, altyazılar)
                                  │
     page/ (WebGL uydu + d3 vektör + DOM öğeler) ◄── headless Chrome, GG.frame(t) kare kare
                                  │
                                  ▼
                 JPEG kareler ──► ffmpeg H.264 ──► + anlatım (+ müzik) ──► mp4
```

Her kare yalnızca `t` zamanının fonksiyonudur; bu yüzden render deterministiktir ve sesle birebir senkron kalır.
