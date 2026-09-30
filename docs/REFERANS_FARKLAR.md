# Referans kanal ile bizim videoların farkları

Kaynak: `reference/` içindeki 22 video (Darién, İspanya sınırları, Tibet uçakları, Brezilya, iki İrlanda,
27 yıl yürüyüş, Diomede, Monowi, North Sentinel, saat dilimleri, Kiribati, UK/GB/İngiltere, ABD doğu-batı,
NYC, Baarle, Kanada gölleri, ABD'nin büyümesi…). Hepsi 2 kare/sn ile kare kare izlendi (56 kare tablosu),
ayrıca hareket ölçümü yapıldı (`motion.py`: sert kesim, kare değişimi, hareketli süre payı).
Bizim tarafta 50 videonun son sürümü ve motor kodu (`page/main.js`, `src/timeline.mjs`) incelendi.
Ses (müzik / efekt) bu turda analiz edilmedi.

## Ölçülen sayılar

| ölçüt | referans (16 farklı video) | bizim videolar (8 örnek) |
|---|---|---|
| süre | 30–102 sn, çoğu 60–100 | 34–65 sn, ortalama ≈ 44 sn (21 videonun ölçümü) |
| ortalama kare değişimi | 5.3–13.3 (çoğu 8–12) | 2.4–5.4 |
| hareket eden süre payı | %71–98 (çoğu %90+) | %28–55 |
| tamamen durağan kare payı | %0–3 (İrlanda hariç %16) | %7–14 |
| kamera kayma hızı | 4–29 birim/sn | 0.8–6 birim/sn |
| sert kesim / dakika | 3–88 (çoğu 13–42) | 4–26 |

Kısaca: referans yaklaşık **2,5 kat daha hareketli**, hiç durmuyor ve **%50 daha uzun**. Bizim videolar
CLAUDE.md'deki "60–100 sn" kuralının bile altında.

Aşağıdaki liste 125 fark. Etki: ★★★ büyük · ★★ orta · ★ küçük. "Yok" = motorda hiç yok, "kısmen" = var ama zayıf.

## Kapatma durumu (güncel)

Aşağıdaki tablolardaki "bizde" sütunu analiz anının durumunu gösterir; kapatılanlar burada özetlenir.

| grup | kapatıldı | kalan / kısmi |
|---|---|---|
| A. Kamera | sürekli drift + kayma, sahne içi ikinci hamle (`camera.then`, otomatik itme), rotayı takip eden kamera, eğimli kamera + gökyüzü, hareket bulanıklığı, kamera sarsıntısı | split-screen / ikinci pencere (inset) |
| B. Harita çizimi | sınır çizerek açılış (`trace`), neon kenar, eğri yazı, dev kabartmalı ad, kalabalık, kutu/ışın/bulut, yeni paletler (light, blueprint, pastel, bw, kraft), bayrak dalgası, lazer/ateş/düğümlü rota | 3B ölçüm kutusu |
| C. Anlatım / karakter | gemiye binip karaya çıkan karakter, yürüyen karakter, tepki yüzleri (8 ifade), avatar, el damgası, çene düşme yerine tepki emojisi | ülke yüzü yalnız temel ifadeler |
| D. Efekt / geçiş | wipe/zoom/slide/glitch/blast/ice/rewind/ink, renk ayarları, parçacıklar, mercek parlaması, büyüteç | uçak süpürme ile fotoğraf açılışı |
| E. B-roll | kendi ürettiğimiz (FLUX) B-roll kartları ve tam ekran; telifli hiçbir görüntü yok | — |
| F. Zamanlama | her kesimde geçiş, tepki yüzü, itme; süre 58–100 sn hedefi (≥160 kelime) | metrik: `pan` düz vektör haritada faz korelasyonuyla zayıf ölçülür, eşik 1,5'e çekildi |
| G. Konu | her videoya kaynaklı ek sahneler (Wikipedia alıntısıyla) | — |
| H. Hat | Kokoro yerel TTS, Sentinel-2, kalite kapısı, storyboard üretici, skill'ler | ses analizi (Whisper) eklenmedi |

## A. Kamera (1–16)

| # | referansta | bizde | etki |
|---|---|---|---|
| 1 | Kamera hiç durmaz; sahne boyunca sürekli zoom/kayma | Sahne başında hareket, sonra çoğunlukla sabit | ★★★ |
| 2 | 45–60° eğimli 3B harita, ufukta mavi gökyüzü (Brezilya, saat dilimleri, 27 yıl) | Yok; `tilt` kodda kapalı (üstte boş bant kalıyordu) | ★★★ |
| 3 | Yolcuyu/rota ucunu takip eden kamera, sürekli zoom ayarı (27 yıl videosu) | Kısmen: `follow` var ama az sahnede kullanılıyor | ★★★ |
| 4 | Dünyadan küçücük adaya "dalış" zoom'u, kenarda koyu vinyet (Sentinel 30–36 sn) | Zoom var, dalış hissi ve vinyet yok | ★★ |
| 5 | Dönen kamera (bearing 30–90°) — UK, Kiribati | En fazla ±6° | ★★ |
| 6 | Planlar arası hareket bulanıklığı (motion blur) | Yalnızca geçiş anında blur | ★★ |
| 7 | Alan derinliği bulanıklığı / kenar blur | Yok | ★ |
| 8 | Whip-pan: nesne bir sahneden ötekine taşınır | Yok | ★★ |
| 9 | Bir sahnede 2–3 farklı zoom seviyesi (NYC: eyalet → şehir → mahalle) | Sahne başına tek kamera | ★★★ |
| 10 | Bölünmüş ekran 2'li / 4'lü karşılaştırma (NYC 2.5–7 sn) | Yok | ★★ |
| 11 | Ülkeye yaklaşırken ekran kararır, sadece ülke aydınlık (Zaman dilimleri 4 sn, Kiribati 23 sn) | `dim` var ama sadece diğer ülkeleri soluklaştırıyor, ekranı kararttırmıyor | ★★ |
| 12 | "Daha yakından bakalım" büyüteci (senin gördüğün) | Yok | ★★ |
| 13 | Uzaya çıkış, atmosfer parıltısı, gün doğumu ve lens flare finali (Kiribati) | Yok (globe stili sade) | ★ |
| 14 | Sınır çizilirken kamera çizgiyi izler, kenardan başlayıp dolaşır (senin gördüğün) | Yok | ★★★ |
| 15 | Dünyadan sokak seviyesi uyduya kesintisiz iniş (Monowi 3 bina, Baarle sokak) | Yakın plan var ama Sentinel kutusu sınırlı, geçiş sert | ★★ |
| 16 | Ani zoom-out ile "büyük resim" vurgusu (Baarle 8 sn, NYC şehir → ışık noktası) | Yok | ★★ |

## B. Harita çizimi ve sınırlar (17–46)

| # | referansta | bizde | etki |
|---|---|---|---|
| 17 | Sınır bir uçtan başlayıp çizilerek görünür, sonra dolar (senin gördüğün) | Alan tek seferde belirir (yalnız `reveal` daire açılışı var) | ★★★ |
| 18 | Neon (camgöbeği/yeşil/sarı) dış çizgi + parlama | Beyaz çizgi + glow, "soft rim" kısmen | ★★ |
| 19 | Dolgu, arazi dokusunu koruyor (multiply + tarama) | Düz dolgu | ★★ |
| 20 | Dev, 3B kontürlü ülke adı büyükten küçüğe iner (UK, İrlanda) | Yok | ★★★ |
| 21 | Ülke adı poligonun arkasında dev, yarı saydam (Kiribati) | Yok | ★★ |
| 22 | Yazı rota/kıyı/nehir boyunca eğri akar ("Pan-American Highway", "Mississippi", "-50°C", "2 years") | Etiket düz, ±12° | ★★★ |
| 23 | Poligonun asal eksenine dönük yazı (5-140?, ok ölçüsü) | Bilerek yatay (senin isteğin) | ★ |
| 24 | Sarı etiket + iki çizgi ile iki adaya ok (çoklu çıkıntı) | Tek çizgi | ★ |
| 25 | Elle çizilmiş sarı elips + 4 ok içe akar + "Unique" eğri ok | `ring` ve `arrow` var, ok yağmuru ve animasyonlu çizim yok | ★★ |
| 26 | Hareketli diyagonal tarama (bölünmüş şehir) | Statik tarama | ★ |
| 27 | Bölge fethi dalgası: kırmızı taramalı alan Kelt/İngiliz yayılır | `ghost`/`morph` var, yayılan dalga yok | ★★★ |
| 28 | Harita stili değişimi: açık vektör, koyu düz, mavi plan ızgarası, pastel, kraft kâğıt, B/S, turuncu-mor renk derecesi | Yalnız uydu + parşömen | ★★★ |
| 29 | Kıtalar açık gri düz vektör haritada açılıp uyduya çapraz geçiş (Kiribati 0–6 sn) | Yok | ★★ |
| 30 | Kraft kâğıt üzerinde bilgi grafiği: dairesel avatarlar + noktalı oklar (Monowi 41–52 sn) | Yok | ★★★ |
| 31 | Mavi plan ızgarası düzlemi, eğik (Baarle 13–19 sn) | Yok | ★★ |
| 32 | Tarihî sahnelerde krallık dolguları + kıvrık serif adlar (İrlanda 37 sn) | Tarihî sınır var, iç krallıklar yok | ★★ |
| 33 | Bölünme çizgisi "tutuşur" (ateşli sınır, İrlanda 74 sn) | Yok | ★ |
| 34 | Rota kalınlığı zoom ile ölçeklenir, spline dalgalanma, düğüm noktaları + nabız halkası ("her 90 gün") | Sabit kalınlık, düz | ★★ |
| 35 | Sürüklenen buz gibi kıvrımlı rota (yol dışına çıkma) | Yok | ★ |
| 36 | Yapı sınır kutuları: uyduda sarı çerçeveli binalar (Monowi) | Yok | ★★ |
| 37 | Işık sütunu / parlayan noktalar (Fransa denizaşırı toprakları) | Yok | ★★ |
| 38 | Ülke uzaklaşınca ışık noktasına dönüşür (NYC) | Yok | ★★ |
| 39 | Damla pin + içinde kırmızı simge (Darién) | Pin ve art var, simge pinin içinde değil | ★ |
| 40 | Nüfus: insan simgesi sıraları dolar, küçülür, kırmızıya döner (bulaşma) | Yalnız sayaç | ★★★ |
| 41 | Sıralama katmanı: en büyük ülkeler sarı ısı haritası, #1…#5 (Brezilya) | Yok | ★★ |
| 42 | Boyut karşılaştırma: başka ülke silueti üst üste / 5 kez döşenir (Fransa × 5 Tibet'te) | `ghost` yalnız taşır, döşemez | ★★ |
| 43 | Yüzdeye göre dolan siluet (%21→%48 Güney Amerika) | Yok | ★★ |
| 44 | Zaman çubuğu "100 years" + eğik çizgide yıl düğmesi | `year` var, çubuk yok | ★★ |
| 45 | 3B perspektifli ölçü kutusu ("5 km", eğik dörtgen) | 2B ok | ★★ |
| 46 | Ülke dışı noktalara giden dağınık mesafe çizgileri, uçlarda kırmızı halka (Brezilya 26–30 sn) | Tek ölçü çizgisi | ★★ |

## C. Anlatım ve karakter (47–66)

| # | referansta | bizde | etki |
|---|---|---|---|
| 47 | Ülke bir karakter: gözler, ağız, kaşlar, ifadeler kelimeyle senkron (İrlanda 51–95 sn) | Yok | ★★★ |
| 48 | Karakterler haritanın üstünde oynar (Vikingler, kral, lordlar, haritacı kedisi) | Karakter köşede duran kesit | ★★★ |
| 49 | Harita dışı çizim sahne: haritacılar odası, market kasası, monitörlü kedi (5–10 sn) | Yok | ★★★ |
| 50 | Şaşırınca çene yere düşer, ağız açılır (senin gördüğün) | Yok, karakterler durağan | ★★★ |
| 51 | Karakter gemiye biner, varınca atlar (senin gördüğün) | `character` mover motorda var ama NVIDIA çizimiyle kullanılmıyor | ★★★ |
| 52 | Zamanı geri sarma (senin gördüğün) | Yok (`film` geçişi tek yönlü) | ★★ |
| 53 | Konuşma stilleri: sarı kontürlü düz yazı, beyaz balon, düşünce balonu "…", "???" yağmuru | Tek balon tipi | ★★ |
| 54 | Emoji tepki yüzü (gülen → ölü) espri | Emoji kaldırıldı; NVIDIA çizimi tepki yüzü yok | ★★ |
| 55 | Kişi fotoğrafı altıgen rozet içinde haritada, rotayı izler | Yok | ★★ |
| 56 | Aynı mekânda iki karakter aksiyonu senkron (ID kontrolü) | İki karakter yalnız konuşuyor | ★★ |
| 57 | Rota üzerinde yürüyen küçük figürler | Yok | ★★ |
| 58 | Farklı bölgelere yerleştirilmiş kişiler + balon (Phoenix'te kahve) | Yok | ★★ |
| 59 | Aynı maskot/karakter video boyunca tekrar eder | Her sahnede farklı karakter | ★★ |
| 60 | Zaman kayması: film şeridi + mor renk derecesi | `film` var, renk derecesi yok | ★ |
| 61 | Hikâye akışı: bir insanın yolculuğu, bir kasabanın tek sakini | Çoğu "bu sınır neden garip" listesi | ★★★ |
| 62 | Yarım videoda merak boşluğu ("ama bir sorun var") | Zayıf | ★★ |
| 63 | Tanıdık ölçütle kıyas (Fransa'nın 5 katı, NYC, 11 kat) | Kısmen | ★★ |
| 64 | Her 10–15 sn'de bir mizah anı | Yok | ★★★ |
| 65 | Terimlere sabit renk kodu (Büyük Britanya mavi, UK kırmızı, İngiltere yeşil…) | Sahneye göre değişiyor | ★★ |
| 66 | Başa dönen bitiş (Monowi zoom-out, Brezilya komşular) | Çoğunda var | ★ |

## D. Efekt ve geçişler (67–92)

| # | referansta | bizde | etki |
|---|---|---|---|
| 67 | Nükleer sekans: beyaz patlama → turuncu → mor → karanlık B/S | Yalnız beyaz flash | ★★ |
| 68 | Temalı geçişler: buz lekeli silme, kâğıt, mürekkep | Genel `wipe`, `glitch`, `slide` | ★★ |
| 69 | 3B hacimli bulut ve yağmur (Darién 29 sn), kıtadan sürüklenen bulutlar (ABD) | 2B simge | ★★ |
| 70 | Parçacık sistemleri: kar, yağmur, rüzgâr çizgileri | Yok | ★★ |
| 71 | Lens flare + atmosfer (Kiribati finali) | Yok | ★ |
| 72 | Tehlike anlarında kırmızı vinyet nabzı + sarsıntı | `shake` var, vinyet nabzı kısmen | ★ |
| 73 | Karanlık vinyet + sis ruh hali (Darién 17–19 sn) | Yalnız `stamp` vinyeti | ★★ |
| 74 | Her arayüz öğesinde bloom/neon | Bazı öğelerde glow | ★★ |
| 75 | Dalgalanan bez bayrak dokusu (Diomede, ABD bayrağı dolgu) | Düz bayrak dolgu | ★★ |
| 76 | Diklenen bayraklar: gölge + dalga (13 koloni) | `flag pin` var, gölge/dalga yok | ★ |
| 77 | Elle "FAILED" damgası: gerçek el eski haritaya basar (Darién 36 sn) | Damga elsiz | ★★ |
| 78 | Kâğıt dokuları: buruşuk, kraft, tomar simgesi (Paris Antlaşması) | Sadece parşömen | ★ |
| 79 | Işık ışını/lazer: iki ülke arası (Diomede), başlangıç meridyeni | Yok | ★★ |
| 80 | Uçağın süpürdüğü dikdörtgende fotoğraf açılır (Kanada 14–16 sn) | Yok | ★★ |
| 81 | Altıgen simge rozetleri parlak (turuncu adli simge, mavi ulaşım) | Simge düz art | ★★ |
| 82 | Sayı sayacı + birimli sondan "…" ("+2,000,000 lakes…") | Sayaç var, kuyruk yok | ★ |
| 83 | Yazı animasyonları: dev bulanık "nightmare", harf harf titreyen soru, el yazısı "ti=S" | `slam`, `typewriter` var; titreşim ve el yazısı yok | ★★ |
| 84 | Altyazı: küçük düz beyaz, kutusuz | Bizde büyük siyah kutu + sarı kelime | ★★ |
| 85 | Sahneler arası bağlayıcı hareket: öğe ekrandan sahneyi dolaşıp yeni sahneye girer | Yok | ★★ |
| 86 | Öğeler ekran kenarından uçarak girer ("Pan-American Highway" sahne dışından) | Yerinde belirme / ölçek | ★★ |
| 87 | Nesne haritaya "çakılır" (yol tabelası 3B, Monowi) | Yok | ★ |
| 88 | Hedef uçarken iz bırakır (ok süpürme, yörünge halkası) | Kısmen | ★ |
| 89 | Etkileşimli sayaç: hapishane simgesine bağlı "0 → 18 days" | Sayaç ayrı duruyor | ★★ |
| 90 | Öğeler sırayla kısa gecikmeyle (stagger) belirir | Kısmen (`stagger`) | ★ |
| 91 | Sahne başında öğe girişi sözcükten 0.1–0.2 sn önce | Sözcükle aynı anda | ★ |
| 92 | Renk derecesi anlatıya göre değişir (kırmızı tehlike, mor geçmiş, sepya) | Kit başına sabit | ★★ |

## E. Gerçek medya ve B-roll (93–102)

| # | referansta | bizde | etki |
|---|---|---|---|
| 93 | Anlatımdaki isimler için gerçek video/foto (orman, bataklık, taverna, sokak) — sürenin %10–25'i | Hiç yok | ★★★ |
| 94 | Google Earth tarzı 3B uçuş (Tibet 17–29 sn) | Yok | ★★ |
| 95 | Ekran kaydı (Flightradar) | Yok (telif) | ★ |
| 96 | Sokak fotoğrafı üzerinde AR sınır çizgisi + bayraklar (Baarle) | Yok | ★★ |
| 97 | Kartpostal fotoğraf kayarak girer, beyaz çerçeve + eğim + blur (Kanada 27 sn) | Yok | ★★ |
| 98 | Ekrandaki fotoğraf üzerine sarı kontürlü yazı ("Lake Louise") | Yok | ★★ |
| 99 | Karakter arka planı olarak çizim oda/sahne | Yok | ★★★ |
| 100 | Arşiv görüntüsü + film renk derecesi (Sentinel) | Yok | ★ |
| 101 | Haritayla çapraz geçen "ekran" (monitör içinde harita, kedi geçer) | Yok | ★ |
| 102 | Kişi fotoğrafı kesiti + beyaz kontur + isim oku (Karl Bushby) | Yok | ★ |

## F. Zamanlama ve ritim (103–112)

| # | referansta | bizde | etki |
|---|---|---|---|
| 103 | Her ~1–1,5 sn'de ekranda yeni bir şey oluyor | ~2–4 sn'de bir | ★★★ |
| 104 | İlk kareden itibaren hareket; konu 0,5–1 sn'de görünür | Önce başlık şeridi + geniş plan (Darién 0–2 sn) | ★★ |
| 105 | Her isim/olay için bir görsel (isim → resim kuralı) | Bazı sahnelerde yalnız sayaç + etiket | ★★★ |
| 106 | Durağan kare payı %0–3 | %7–14 | ★★ |
| 107 | 60–100 sn | ≈ 44 sn ortalama | ★★★ |
| 108 | Bir videoda 12–20 farklı sahne/görsel dil | 7–11 | ★★ |
| 109 | Vurgu sözcüğüne senkron hareket (kamera + öğe + sayaç birlikte) | Kısmen | ★★ |
| 110 | Hızlı kesim sekansları (Kanada 75 kesim/dk, saat dilimleri 88) belirli anlarda | Her yerde yavaş | ★ |
| 111 | Yavaş nefes anı: İrlanda %16 durağan, gerilimden sonra | Rastgele durağanlık | ★ |
| 112 | Videonun ortasında büyük "olay" (nükleer flaş, gerçek sahne) | Yok | ★★ |

## G. Konu ve dramaturji (113–118)

| # | referansta | bizde | etki |
|---|---|---|---|
| 113 | Kişi/olay hikâyesi (yürüyen adam, 90 yaşındaki barmen, saklı kabile) | Çoğu tek gerçek listesi | ★★★ |
| 114 | Anlatıya dayalı tarihçe (Vikingler → krallar → bağımsızlık) sahneleri | Tarih sahnesi kısa | ★★ |
| 115 | Karşılaştırmalı rakamlar (220 milyon / 144 milyon) görsel karşılaştırma | Sayaç | ★★ |
| 116 | Alt-başlık soruları ekranda ("Why not stay here?") | Yok | ★ |
| 117 | Tanıdık kişi/nesne referansı (Geleceğe Dönüş çıkartması) | Yok | ★ |
| 118 | Bölüm içi "aha" (şaşırtıcı ölçüm: "Afrika'ya daha yakın") çizgisi | Kısmen | ★★ |

## H. Üretim hattı / teknik eksikler (119–125)

| # | eksik | etki |
|---|---|---|
| 119 | Sahne başına **storyboard** aşaması yok (kamera, harita stili, medya, karakter, espri) — referansta her sahne planlı | ★★★ |
| 120 | **Kalite kapısı yok**: hareket, durağan pay, öğe yoğunluğu ölçülmüyor (bu analizin `motion.py`'si otomatikleşebilir) | ★★★ |
| 121 | **Stil hazır ayarları** yok (açık vektör, koyu düz, plan ızgarası, kraft, parşömen, uydu, B/S) | ★★★ |
| 122 | **Öğe kütüphanesi** dar: altıgen rozet, damla pin, el, damga, yıldız/nabız halkası, yön okları | ★★ |
| 123 | **3B arazi** (yükseklik verisi) yok; eğik kamera için gerekli | ★★ |
| 124 | **Parçacık ve hacimli bulut** katmanı yok | ★★ |
| 125 | Referans karşılaştırma **kontrol listesi** yok: her video render sonrası ölçülüp bu tabloyla kıyaslanmıyor | ★★ |

## Araç, skill, repo ve API anahtarı araştırması (hepsi ücretsiz)

Şu an videoyu ben izleyebiliyorum (kare tablosu + ölçüm). Eksik olan, bunu **hızlı ve tekrarlanabilir** yapmak.

| seçenek | ne işe yarar | durum |
|---|---|---|
| OpenCV (`opencv-python-headless`) | kamera zoom/kayma tahmini, optik akış | pip'ten indirilebiliyor, kurulu değil (onayına bağlı) |
| PySceneDetect 0.7.1 | otomatik kesim/sahne listesi | pip'te var, kurulu değil |
| `motion.py` (bu analiz için yazdım, numpy) | kare değişimi, hareketli süre payı, kesim/dk | çalışıyor, ek kurulum gerekmiyor; şimdilik repoda değil, onayınla `tools/ref/` altına koyarım |
| `refsheet.py` (bu analiz için yazdım) | 2 kare/sn zaman damgalı kare tablosu | çalışıyor, aynı durum |
| Whisper (yerel, ücretsiz) | referans anlatımın kelime zamanları → sözcük/görsel senkron ölçümü | kurulu değil, CPU'da yavaş ama olur |
| Tesseract OCR | ekrandaki yazıların zaman çizelgesi | kurulu değil |
| NVIDIA vision modelleri (mevcut anahtar) | otomatik video betimleme | **Denedim, işe yaramıyor**: `cosmos-reason2-8b`, `gemma-3-12b-it`, `phi-3-vision` 404 döndü, `llama-3.2-90b-vision` 180 sn'de zaman aşımı |
| Google Gemini API (ücretsiz katman) | tüm videoyu yükleyip zaman damgalı sahne dökümü | **Google AI Studio'dan ücretsiz anahtar gerekir**; buradan test edemedim |
| Pexels/Pixabay/Wikimedia | telifsiz B-roll fotoğraf/video | ücretsiz; Pexels anahtar ister, Wikimedia istemez |
| NVIDIA FLUX (mevcut anahtar) | B-roll foto, çizim oda arka planı, tepki yüzleri | zaten çalışıyor |
| Yükseklik verisi (AWS Terrain / Copernicus DEM) | 3B eğik kamera için | ücretsiz, anahtarsız |

**Gerekli mi?** Hayır, zorunlu bir anahtar veya repo yok. En çok işe yarayacak ek: OpenCV + PySceneDetect
(kalite kapısı için) ve bir proje skill'i (`.claude/skills/referans-analiz`: kare tablosu → ölçüm → not → kıyas
iş akışı). Gemini anahtarı isteğe bağlı: sadece bunu istersen toplu ve daha hızlı analiz sağlar.
