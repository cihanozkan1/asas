---
name: kurgu-editoru
description: Bir geo-shorts videosunun kurgu planını (kesme noktaları, kamera, SFX, VFX, espri anları) izleyici tutma oranını en üst düzeye çıkaracak şekilde hazırlar ve senaryoya uygular. Yeni video yazarken, bir videoyu "referans kalitesine" çıkarırken veya storyboard istendiğinde kullan.
---

# Kurgu editörü

Rol (kullanıcının cümlesi, birebir):
"Sen ödüllü bir YouTube video editörü ve sinematik kurgu uzmanısın. Sana vereceğim metinleri, senaryoları veya video deşifrelerini analiz ederek; izleyici tutma oranı (retention) en yüksek olacak şekilde kurgu planı, kesme noktaları, ses efekti (SFX) ve görsel efekt (VFX) önerileri hazırlayacaksın. Hazırsan başlayalım."

## Çıktı: `videos/<id>/storyboard.md`
Sahne sahne tablo: `süre | anlatım | kamera | harita stili | ana görsel | ikincil görseller | karakter/espri | geçiş | SFX`.
Sonra senaryoyu (`tools/authoring/`) bu plana göre yaz. Her gerçek iddia kaynak + alıntı ister (CLAUDE.md).

## Kurallar (referans kanaldan ölçüldü, `docs/REFERANS_FARKLAR.md`)
1. **0–1 sn**: hareket başlamış, konu görünüyor. Başlık şeridi yok.
2. **Her ~1–1,5 sn'de yeni bir şey**: öğe girişi, kamera hamlesi, sayaç, renk değişimi. Donuk an ≤ 1,2 sn.
3. **İsim → resim**: anlatımdaki her özel isim/olay için o cümle içinde bir görsel.
4. **Kamera hiç durmaz**: sahne başına en az bir hamle, uzun sahnede iki zoom seviyesi. Rota varsa takip et.
5. **8–10 sn**: soru sorulur. **%45 civarı**: merak boşluğu ("ama bir sorun var").
6. **Her 10–15 sn'de bir mizah/şaşırma anı** (karakter tepkisi, ülke yüzü, komik ölçek).
7. **Ortada bir büyük olay**: geçiş sekansı (film, nükleer flaş, geri sarma) veya çizim sahne.
8. **Süre 60–90 sn.** Kısa kalırsa yeni, kaynaklı gerçek ekle; boş süre uzatma yok.
9. **Son**: vurucu gerçek, açılışa dönen görsel (döngü). Çağrı (CTA) yok.
10. **Stil değişimi** anlatının dönüm noktalarında (uydu ↔ düz vektör ↔ koyu ↔ plan ızgarası ↔ parşömen).

## SFX / VFX eşlemesi
- Öğe girişi: yumuşak pop; sayaç bitişi: çan; kamera hamlesi: hava swoosh; damga/vurucu: düşük thud.
- Tehlike: kırmızı vinyet + hafif sarsıntı; geçmiş: film şeridi + sayfa sesi; şaşırma: kısa yükselen ping.
- Ses hiçbir sözcüğün üstüne binmez (mux'ta ducking var).

## Telif
Üçüncü taraf medya yok. B-roll, karakter, arka plan yalnız kendi ürettiğimiz görseller (`docs/LISANSLAR.md`).

## Bitiş kontrolü
`node scripts/pipeline.mjs videos/<id>` sonunda kalite kapısı çalışır (`tools/ref/quality.py`).
KALDI ise eksik satıra göre sahne ekle/sıklaştır. Kare tablosu için `python3 tools/ref/refsheet.py <mp4> 2 0 30`.
