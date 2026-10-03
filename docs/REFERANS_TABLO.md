# Referans kanal: teknik envanteri ve bizdeki durum (110 video incelendi)

Kaynak: `docs/REFERANS_ENVANTER.md` (video başına not). "Sıklık" = yaklaşık kaç videoda geçtiği. Durum: VAR / KISMEN / YOK.
Telif kuralı: gerçek fotoğraf, Google Earth, ekran görüntüsü, gerçek kişi portresi alınmaz; yerine kendi çizim/üretim.

| # | Teknik | Sıklık | Durum | Not / karar |
|---|---|---|---|---|
| 1 | Ülke bayrak dokulu dolgu, rota sınıra varınca belirir | ~15 | VAR (bu tur: `onRoute`) | Pan-Amerikan'da uygulandı |
| 2 | Rotayı izleyen kamera, bölgeye göre zoom | ~12 | VAR (bu tur: `follow` listesi + `zoomAlong`) | |
| 3 | 3B duran figürler + eğik kamera (kısa süre) | ~6 | VAR (bu tur: derinlik ölçeği, ayak noktası, yukarıdan düşme, ufka sabitli gökyüzü) | sadece figür anlarında |
| 4 | Numaralı sebep iskeleti (sarı "1." + başlık + leader) | ~12 | YOK | Aday: ortak şablon |
| 5 | Şekil kopyalayıp başka yere koyarak boyut kıyası (×N) | ~14 | YOK | En yüksek değer |
| 6 | Vektör kesit sahnesi (güneş, kaya, su, yapı, derinlik ölçüsü) | ~10 | YOK | Köprü/kanyon/tünel videoları |
| 7 | Hatch (çapraz çizgili) bölge dolgusu | ~15 | KISMEN | Eksik: genel `hatch` dolgu |
| 8 | Koyu "veri haritası" tabanı + koroplet/ısı noktaları | ~10 | KISMEN | koroplet YOK |
| 9 | Çok seviyeli renk kodlu alt bölgeler (ilçe/eyalet) | ~10 | KISMEN | Renkli parça + etiket |
| 10 | Zaman çubuğu + yıl sayacı, bölge devralma (renk yayılır) | ~10 | KISMEN | `timebar` var, devralma yok |
| 11 | Yol/rota üstü eğik sayaç yazısı (path text) | ~6 | VAR (`pathtext`) | rotaya bağlanmadı |
| 12 | Rota rengi bölgeye göre değişir, olay ikonları, durma halkası | ~5 | KISMEN | |
| 13 | Ölçekli halka (ses/radar/şok dalgası yarıçapı) | ~5 | YOK | |
| 14 | Hayvan/obje sürüsü sprite + yayılma okları | ~8 | KISMEN | `scatter` var, ok yok |
| 15 | Yasak/onay/STOP ikon seti, çarpı çizilme animasyonu | ~12 | KISMEN | |
| 16 | Konuşma balonu diyaloğu, ülke = karakter | ~6 | KISMEN | |
| 17 | Protesto silüet kalabalığı, tabela+yumruk | ~4 | YOK | |
| 18 | Küre sahnesi (yarıçap çizgileri, elips dönüşümü, enlem şeridi) | ~10 | KISMEN | Chimborazo için gerekli |
| 19 | Kâğıt harita kartı / page-curl / bölünmüş ekran geçişi | ~8 | YOK | |
| 20 | Kesme-kâğıt (paper cut-out) sahne stili | ~3 | YOK | düşük öncelik |
| 21 | Harf harf / eşittir-üstü-çizili / Deutsch→Dutch yazı animasyonları | ~8 | KISMEN | |
| 22 | OSM yol ağı wipe + renk kodu, enklav parça kümeleri | ~4 | YOK | |
| 23 | Deniz seviyesi/taşkın maskesi (relief eşiği) | ~3 | YOK | verimiz var |
| 24 | Parçacık: kar, toz, sinek bulutu, serpinti | ~10 | KISMEN | |
| 25 | Tarih sahnesi: sepya kabartma harita + banner + savaş mini animasyonu | ~8 | KISMEN | |

## Bizde olan ama yanlış/riskli bulunanlar
- Referansın eğik+bulanık kamerası (Jefferson, Superior): bizde "blur yok" kuralı → alınmaz.
- Radyal zoom blur geçişleri → alınmaz.
- Dolgulu etiket/kutu/kapsül her yerde → bizde düz yazı + kontur kuralı korunur.
- Konfeti/havai fişek → kural gereği yalnız hikâye isterse.
- Tilt, `helpers.save()` içinde tümden siliniyordu → artık `keep=True` ile bilinçli kullanılabilir.

## Öncelik (çorba olmaması için videoya 2–3 teknik)
1. Şekil kopyalama ile boyut kıyası (#5)
2. Hatch dolgu + bölge devralma (#7, #10)
3. Numaralı sebep iskeleti (#4)
4. Vektör kesit sahnesi (#6)
5. Ölçekli halka (#13), STOP/onay ikon seti (#15)
