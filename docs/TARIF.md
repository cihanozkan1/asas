# Referans kanalın ölçülmüş tarifi (84 video, `tools/ref/deep.py`)

Her satır: videolar arası dağılım (p10 / p25 / **medyan** / p75 / p90).

| ölçü | p10 | p25 | medyan | p75 | p90 | birim |
|---|---|---|---|---|---|---|
| süre | 60.20 | 60.27 | **60.40** | 60.80 | 62.98 | s |
| konuşma hızı | 2.83 | 2.97 | **3.09** | 3.15 | 3.29 | kelime/sn |
| ilk kelime | 0.00 | 0.00 | **0.00** | 0.00 | 0.00 | s |
| ilk soru bitişi | 2.02 | 2.60 | **3.40** | 4.92 | 10.35 | s |
| kesme | 1.00 | 2.98 | **4.95** | 8.90 | 12.97 | adet/dk |
| yeni öğe (olay) | 11.90 | 14.90 | **17.25** | 19.90 | 21.84 | adet/dk |
| kamera: static | 7.74 | 12.85 | **19.40** | 25.35 | 35.44 | % süre |
| kamera: zoom_in | 1.70 | 2.17 | **3.30** | 4.70 | 9.10 | % süre |
| kamera: zoom_out | 2.43 | 3.30 | **4.35** | 5.80 | 7.90 | % süre |
| kamera: pan | 4.10 | 6.50 | **10.40** | 12.88 | 14.90 | % süre |
| kamera: mixed | 41.29 | 49.35 | **56.90** | 63.00 | 69.24 | % süre |
| kamera: cut_or_unknown | 1.32 | 2.10 | **3.30** | 5.08 | 8.18 | % süre |
| zoom-in hızı | 2.10 | 2.40 | **2.80** | 3.20 | 3.98 | %/sn |
| zoom-out hızı | 2.10 | 2.30 | **2.75** | 3.12 | 3.70 | %/sn |
| pan hızı | 0.09 | 0.11 | **0.12** | 0.15 | 0.19 | kare genişliği/sn |
| olay → kelime ön süresi (tüm olaylar) | -0.27 | -0.22 | **-0.13** | 0.01 | 0.22 | s |
| sahne uzunluğu (sert kesmeler arası) | 1.25 | 2.25 | **5.50** | 13.00 | 25.25 | s |


## Bulgular (84 video) → kurallarımız

1. **Süre sabit ~60 sn** (p10–p90: 60,2–63). Bizimkiler 60–82 sn; hedef 58–66 sn.
2. **Konuşma hızı 3,1 kelime/sn** (186 wpm). Bizimkiler 2,6–2,9. Ses hızı +%18'e, sahneler arası boşluk 0,08 sn'ye çekildi (nefes boşluğu yok).
3. **Kanca = soru, ilk saniyede**: açılış cümlelerinin 56/84'ü (%67) soru; 24 tanesi "Did you know…", 7 "Have you ever…", 4 "Can you imagine…". İlk soru medyan 3,4 sn'de biter. Bizim açılışlar düz cümleydi → hepsi soruya çevrildi + 1. saniyede büyük yazı kancası.
4. **Yeni öğe 17/dk (≈3,5 sn'de bir)**, sert kesme 5/dk, sahne (kesmeler arası) medyan 5,5 sn. Yani referans bizden daha az öğeyle daha sakin; tempo öğe sayısından değil **her öğenin anlatıyla eşzamanlı ve anlamlı** olmasından geliyor. Bizim videolarda 30–50 öğe/dk vardı → çeşitlilik ve seyreltme.
5. **Kamera**: %19 durağan, %57 "karışık" (yavaş eş zamanlı zoom+kayma), zoom ~%2,8/sn, kayma ~0,12 kare-genişliği/sn. Ani sıçrama yok; yani **sürekli ama çok yavaş** hareket. Bulanıklık/sarsıntı ölçülmedi (bizde kaldırıldı).
6. **Olay → kelime**: yeni öğe medyan kelimeden 0,13 sn **sonra** (−0,13; p25 −0,22, p75 +0,01) ortaya çıkıyor: öğeler söylenen kelimeyle birlikte/hemen sonra, öncesinde değil. Bizde `timing.lead` 0,12 ön süre vardı; kelimeyle aynı ana yakın tutulmalı.
7. **Bitiş**: referansın bitişleri döngüye değil, vurucu gerçeğe/soruya gider ("What citizenship would they have?", "It's not a bad deal, right?"); tam cümle bitirirler. Bizim kural (kullanıcı): son cümle açılışa bağlansın. İkisini birleştiriyoruz: son sahne = soru kalıbıyla biten yarım cümle + ilk karenin aynısı.

## Açılış kalıpları (sayım)

"Did you know…" 24 · "Have you ever…" 7 · "Can you imagine…" 4 · "Can you believe…" 2 · diğer soru kalıpları 19 · düz cümle 28. Ortalama açılış cümlesi ~15 kelime.
Ham deşifre tutulmaz; `tools/ref/deep.py` çıktısı yalnız sayı ve zaman içerir.
