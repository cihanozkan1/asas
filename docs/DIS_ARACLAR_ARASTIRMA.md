# Dışarıdan temin edilecek araçlar (araştırma, 1 Ekim)

Hedef: patlama / yanardağ / kuşatma gibi efektlerde ve rota mantığında "kalitesi kanıtlanmış" dış kaynak kullanmak. Hiçbiri henüz kurulmadı.

## A. Rota mantığı (yol denizden, gemi karadan geçmesin)
Elle yazılmış nokta yerine gerçek geometri kullan:
| Kaynak | Ne verir | Lisans | Not |
|---|---|---|---|
| [Natural Earth roads / railroads 10m](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/roads/) | büyük karayolları, demiryolları | kamu malı | Pan-Amerikan gibi uzun yollar için yaklaşık; ayrıntı sınırlı |
| [Valhalla](https://github.com/valhalla/valhalla) (MIT) / [OSRM](https://en.wikipedia.org/wiki/Open_Source_Routing_Machine) (BSD) | OSM üstünde gerçek yol rotası (iki şehir arası) | motor MIT/BSD, veri ODbL | OSM verisi "© OpenStreetMap contributors" atfı ister; ürettiğimiz videoyu "produced work" sayar (hukuki görüş değil). Önceki turda OSM'yi reddetmiştin: karar senin |
| [searoute-py](https://github.com/genthalili/searoute-py) (Apache-2.0) | iki liman arası kara dışından geçen deniz yolu | Apache-2.0 | görselleştirme için üretilmiş |
| `tools/validate_routes.mjs` (bizde) | gemi suda, araba karada mı denetler; render öncesi kapı | — | 5 videoda 11 sorun buldu |

## B. Gerçekçi patlama, kuşatma, yanardağ
Blender denemesi (bpy + Mantaflow) bu sunucuda iyi sonuç vermedi: GPU yok, simülasyon duman topu verdi. Önerilen dış kaynaklar:
| Kaynak | İçerik | Lisans / not |
|---|---|---|
| [ActionVFX free](https://www.actionvfx.com/blog/450-free-vfx-stock-footage-assets-ready-for-download) | profesyonel patlama, ateş, duman, toz, enkaz, namlu alevi; 2K | ücretsiz hesap, günlük indirme sınırı; ticari kullanım lisansını indirmeden önce okuyup `docs/LISANSLAR.md`'ye yazmak gerek (sayfa 429 verdi, doğrulayamadım) |
| [FX Elements free](https://www.fxelements.com/free) | 130+ ücretsiz VFX | siyah zemin = screen blend |
| [MyCreativeFX](https://mycreativefx.com/) | patlama, ateş, muzzle flash, alfa kanallı 4K | ticari+kişisel kullanım iddiası |
| [PremiumBeat Detonate](https://www.premiumbeat.com/blog/free-explosion-sfx-vfx-elements/) | 40 ücretsiz patlama elementi | serbest kullanım iddiası |
| [USGS HVO Kīlauea videoları](https://www.usgs.gov/observatories/hvo/multimedia/videos) | gerçek lav fışkırması, zaman atlamalı | kamu malı (USGS); NASA videoları da kamu malı, atıf istenir |
| AI video: [fal.ai](https://www.edenai.co/post/best-ai-video-generation-apis) (Wan 2.2 ≈ $0.02/sn, Veo 3.1 ≈ $0.09/sn, Kling) | stok görüntüsü olmayan sahneler: top atışı, sur yıkılması, tarihi kuşatma | ticari kullanım model başına değişir; Kling ücretsiz katmanda ticari yok; API anahtarı gerekir (ücretli) |
Kullanım: elementler siyah zeminde → screen blend ile haritanın üstüne; zamanlama bizim motorda kelimeye bağlı.

## C. Ajan beceri / repo
- [Remotion agent skills](https://www.remotion.dev/docs/ai/skills) (`npx skills add remotion-dev/skills`): React tabanlı video. Motoru değiştirmek büyük iş; şu an gerekmiyor. Remotion şirket kullanımında lisans ister.
- Blender MCP: GPU yokken işe yaramaz.

## Gerekenler (senden)
1. VFX için hangi yol: ücretsiz paketler mi, ücretli abonelik mi? Hesap açıp indirmeyi sen yapacaksan klasör: `assets/vfx/` (+ lisans metni).
2. AI video istersen fal.ai hesabı ve API anahtarı.
3. OSM atfını kabul ediyor musun? (rota için)
