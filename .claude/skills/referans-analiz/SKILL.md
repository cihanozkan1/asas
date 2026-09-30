---
name: referans-analiz
description: Bir referans kısa videoyu (yalnız fikir/teknik çıkarmak için) kare kare inceler, hareketi ölçer ve bizim videolarla farklarını çıkarır. "Referansı incele", "bizde eksik ne var", "kalite karşılaştır" denince kullan.
---

# Referans analizi

Amaç fikir ve teknik öğrenmek. **Referanstan hiçbir kare, ses, çizim veya metin videolarımıza girmez** (telif sıfır riski).
Referanslar `reference/` içinde durur, git'e girmez.

## Adımlar
1. Kare tablosu (2 kare/sn, süre etiketli, 30 sn'lik parçalar):
   `REF_OUT=/tmp/rs python3 tools/ref/refsheet.py reference/<video>.mp4 2 0 30` (30, 60, 90 için tekrarla) ve görüntüleri oku.
2. Ölçüm: `python3 tools/ref/quality.py reference/<video>.mp4` (kare değişimi, hareket payı, durağan pay, kamera hızı, kesim/dk).
3. Not al: kamera hamlesi, harita stili, her grafik öğe ve nasıl girip çıktığı, karakter/espri, geçiş, B-roll türü, sözcük-görsel eşzamanı.
4. Bizim aynı konulu videomuzla yan yana kıyasla (`output/_teslim2/<id>.mp4`), farkları `docs/REFERANS_FARKLAR.md` biçiminde tabloya ekle.
5. Fark = ("referansta X", "bizde Y", etki ★). Ölçülebilenleri sayıyla yaz.

## Sınırlar
- Ses analiz edilmedi; gerekirse yerel Whisper eklenebilir.
- Yeni bir teknik aldığında telifsiz karşılığını tasarla (kendi çizimimiz, kendi render'ımız) ve `docs/LISANSLAR.md`'yi güncelle.
