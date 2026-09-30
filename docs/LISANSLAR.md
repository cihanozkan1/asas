# Lisanslar ve telif denetimi

Kural (CLAUDE.md): telif riski sıfır. Üçüncü taraf video, foto, ekran görüntüsü, gerçek kişi fotoğrafı yok
(Google Earth, Flightradar, stok klip dahil). Yalnız kendi çizimlerimiz, kendi render'ımız ve açık veri.

Son denetim: 2026-09-30.

| parça | kaynak / lisans | ticari kullanım | durum |
|---|---|---|---|
| Ülke sınırları, kıyılar | Natural Earth (kamu malı) | evet | temiz |
| Dünya görüntüsü | NASA Blue Marble / Black Marble (kamu malı) | evet | temiz, kredi videoda |
| Yakın plan uydu | Copernicus Sentinel-2 L2A, AWS açık veri (`tools/s2_fetch.py`) | evet, kredi şartıyla | temiz. Önceki EOX "cloudless" mozaikleri ticari kullanım için ayrı lisans istiyordu, **kaldırıldı** |
| Tarihî sınırlar | aourednik/historical-basemaps, GPL-3.0 (veri) | GPL: veriyi dağıtmıyoruz, yalnız ondan çizim üretiyoruz; kredi videoda | düşük artık risk. İstersen elle çizilmiş sınırlarla değiştirilebilir |
| Bayraklar | flag-icons, MIT | evet | temiz |
| Yazı tipleri | @fontsource (Anton, Bebas Neue, Montserrat, Oswald, Permanent Marker, Playfair), SIL OFL | evet | temiz |
| Emoji | Twemoji (CC-BY 4.0) | atıf ister | **kaldırıldı**: motor artık emoji çizimi göstermiyor, hepsi kendi çizimimiz |
| Karakterler, harita çizimleri | NVIDIA barındırılan FLUX.1-dev ile üretildi, arka plan rembg | FLUX.1-dev lisansı: çıktılar "ticari amaç dahil her amaçla" kullanılabilir (yalnız çıktılarla rakip model eğitilemez) | temiz; prompt ve seed `assets/*/prompts/` içinde |
| Ses efektleri | Kenney (CC0) + ffmpeg ile kendi ürettiklerimiz | evet | temiz (`assets/sfx/LICENSE.md`) |
| Anlatım sesi | **Kokoro-82M** (Apache-2.0), yerel model (`tools/kokoro_tts.py`) | evet | temiz. Önceki `msedge-tts` Microsoft'un resmî olmayan servisiydi, **varsayılan olmaktan çıkarıldı** |
| Konuşma üretimi | espeak-ng (GPL-3.0) yalnız çalışma anında fonem için | çıktı ses etkilenmez | temiz |
| Müzik | yok (`audio.music` boş) | — | müzik eklenirse telifsiz kaynak + buraya kayıt |
| Kod / kütüphaneler | d3-geo (ISC), topojson (ISC), puppeteer (Apache-2.0), esbuild (MIT), rasterio (BSD), OpenCV (Apache-2.0), PySceneDetect (BSD) | evet | temiz |
| Video kodlama | ffmpeg + libx264 | çıktı etkilenmez | standart |
| Referans videolar | yalnız analiz için `reference/` içinde, git'e girmez, hiçbir kare videolara girmez | — | yayınlanmaz |

## Kurallar
- Yeni bir varlık eklemeden önce bu tabloya lisansıyla ekle.
- Yeni B-roll yalnız kendi ürettiğimiz görsellerden.
- Gerçek kişi, marka, logo, ünlü yüz çizimi yok (üretimde adları kullanma, genel tarif).
