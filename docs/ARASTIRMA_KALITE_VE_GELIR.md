# Araştırma: Kalite kontrolü, izleyici tutma ve gelir (harita/coğrafya Shorts)

Tarih: 2026-10-02. Amaç: "her videoda mantık hatası" sorununu kökünden çözmek ve videoların gerçekten para kazanmasını sağlamak.
Kaynak güvenilirliği notu: **[R]** = resmi (YouTube Help, Anthropic dokümanı, arXiv), **[B]** = blog/ikincil, yaklaşık değer.

## 1. Kısa sonuç
1. Tek başına "videoya bakıp hata bul" yöntemi güvenilir değil: görsel modeller bu işte insanın yaklaşık yarısı kadar hata yakalıyor [R: Spotlight]. Çözüm: **önce hesapla (kesin), sonra dar sorularla çok geçişli görsel kontrol, sonra bağımsız gözden geçirici**.
2. Benim önceki incelemem teknik olarak yetersizdi: Claude görselleri 1568 px uzun kenara (standart katman) indiriyor; 46 küçük kareli sayfalar bayrak tarzı, emoji, çakışma gibi ayrıntıyı göstermiyordu [R: Anthropic vision dokümanı].
3. Gelir: YouTube 15 Temmuz 2025'ten beri "inauthentic content" (kalıp/seri üretim) politikasıyla gelirini kesiyor. Bizim boru hattımız tam bu riski taşıyor; videolar arası **gerçek** çeşitlilik hem kullanıcının kuralı hem politika gereği [R].
4. Shorts tek başına düşük gelir: ortalama 1000 izlenme başına yaklaşık $0,03–0,07 [B]. Ortaklık eşiği 10 milyon Shorts izlenmesi/90 gün + 1000 abone [R]. Uzun video (4000 genel izlenme saati) ikinci yol; Shorts akışındaki saatler sayılmıyor [R].
5. Ölçüm olmadan kalite iddiası tahmindir: Studio'daki "viewed vs swiped away" ve tutma eğrisi gerçek geri bildirim [R/B]. vidIQ sonra.

## 2. Gelir ve politika (kritik)
- **Inauthentic content** (eski adı repetitious content, 15 Temmuz 2025): toplu üretilmiş, kalıp, az varyasyonlu içerik gelir dışı. Örnekler: "genel/özgün olmayan şablonlarla yapılmış yapay zekâ içeriği", "az eğitici değerli/az anlatılı benzer içerik", aynı durumun tekrarı. İzin verilen: aynı giriş/çıkış, ama gövdesi farklı; her videonun ayrı hikâye/odak/kavramı olan seriler [R: support.google.com/youtube/answer/1311392]. Yapay zekâ anlatıcı yasak değil; araştırılmış senaryo + özgün görsel + değer katan içerik geçiyor [B].
- **Bizim için çıkarım:** (a) her videoda farklı kurgu iskeleti, farklı görsel dil/efekt seti, farklı ritim; (b) kaynaklı, özgün anlatı (zaten var); (c) katalog düzeyinde "şablon benzerliği" ölçümü: yeni video önceki videolarla sahne dizilimi/efekt/ses seti açısından çok benziyorsa uyar.
- **Yapay zekâ etiketi:** Gerçekçi değiştirilmiş/sentetik içerik etiketi gerekir; yapay zekâ çizim/animasyon/anlatıcı ve açıkça gerçek dışı görseller için gerekmez [B, birden çok kaynak]. Gerçek kişi sesi/yüzü taklidi yok; haber görüntüsü gibi gösterilen uydurma olay yok.
- **YPP eşikleri [R: answer/72851]:** 1000 abone + 4000 genel izlenme saati (12 ay) VEYA 1000 abone + 10 milyon Shorts izlenmesi (90 gün). Shorts akışı saatleri 4000 saate sayılmaz. 2FA, AdSense, ihlal (strike) yok.
- **Gelir payı [B]:** Shorts havuzunun %45'i izlenme payına göre dağıtılıyor; RPM çoğunlukla $0,01–0,07/1000. 10M izlenme ≈ birkaç yüz dolar. Yani Shorts bir **büyüme/huni** aracı; esas gelir uzun video, abone ve (sonra) sponsor/ürün.
- **İzlenme sayımı [R/B]:** Ağustos 2026'dan itibaren izlenme oynatma başlar başlamaz sayılıyor; gelir/uygunluk "engaged views" üzerinden, yani izlenme sayısı tek başına anlamsız.

## 3. Algoritma ve izleyici tutma
- Ana sinyaller [B, vidIQ ve çok sayıda blog]: swipe-away oranı (ilk 2–3 sn), ortalama izlenen yüzde, tekrar izleme (döngü), paylaşım. Eşikler (yaklaşık): swipe-away <%30 iyi, >%50 öldürücü; ortalama izlenen >%70 iyi; "viewed vs swiped away" >%70 viral bölge, <%30 ölü.
- Studio'da Content → Shorts → "Viewed vs swiped away" ve tutma eğrisi [R/B].
- **Analytics API:** `audienceWatchRatio` / `elapsedVideoTimeRatio` ile tutma raporu var; Shorts desteği belgelenmemiş, swipe-away metriği API'de yok [R]. Pratik: Studio'dan dışa aktarma veya vidIQ.
- Çıkarım: ilk 2 sn = hook yazısı + soru + hareket; döngü cümlesi (zaten var); düşüş noktaları eğriden okunup sahne kopyalama/kısaltma kararına bağlanmalı (ölçüm döngüsü).

## 4. Kalite kontrol: literatürden bulgular
- **Spotlight [R, arXiv 2511.18102]:** Üretilmiş videolarda 1604 hata, 6 tür (fizik, beliriş/kayboluş, mantık, hareket, anatomi, uyum). En iyi görsel model hataların %12,6'sını yakaladı, insan %26,8. Hata türünü ayrı ayrı inceleyen çok ajanlı ayrıştırma küçük modelleri yükseltti. Ders: tek bakış yerine hata türüne göre ayrı geçişler.
- **UI görsel hata araştırmaları (OwlEyes/Nighthawk) [R]:** metin çakışması, bileşen örtmesi, kayıp görsel, bulanık ekran kategorileri; görselden öğrenilen dedektörler.
- **Self-QA döngüsü [B]:** render → ekran görüntüsü → görsel model eleştirisi → düzelt/geç/insana bırak.
- **OpenMontage reviewer [B/GitHub]:** render sonrası ffprobe, 4 konumdan kare (siyah kare, bozuk bindirme), ses seviyesi (sessizlik/kırpma), "slideshow risk" puanı (tekrar, süs görsel, zayıf hareket, çekim niyeti, tipografiye aşırı yaslanma, desteksiz sinematik iddia).
- **skill-motion-graphic [B/GitHub]:** her vuruş için still + iletişim sayfası (tam düzen ve **telefon genişliği**), 7 eksende puan, "en kötü 3 sorun" düzelt, tüm puanlar ≥8 olana ve en az 3 tur. `seek(t)` ile deterministik render (bizde `GG.frame(t)` zaten böyle).
- **Remotion "ajan geri bildirim boşluğu" [B]:** "TSX derleniyor ve render 0 ile bitiyor = boru hattı çalıştı, hareket brife uyuyor demek değil." Öneri: still'i ucuz doğrulama aracı olarak kullan, geçişlerde/vuruşlarda **bilinçli örnekle**, benzer öğeleri kopyalamak yerine bileşen yap.
- **Hakem (LLM-judge) kalibrasyonu [B]:** altın küme (elle etiketli), Cohen kappa ≥0,6, %75–90 uyum; prompt/model değişince altın kümeyi yeniden koş.

## 5. Claude görme sınırları (resmi, [R] platform.claude.com/docs/en/build-with-claude/vision)
- Görseller 28×28 piksellik yamalarla işleniyor. Standart katman: en fazla 1568 px uzun kenar, 1568 görsel token. Yüksek çözünürlük (Claude 4.7 ve sonrası): 2576 px, 4784 token. Büyük görsel küçültülür; küçük yazı okunmaz hâle gelebilir.
- Sınırlamalar: konum/koordinat çıktıları yaklaşık, sayma yaklaşık, çok küçük görsellerde (<200 px) halüsinasyon; "yapay zekâ üretimi mi" sorusuna güvenilmez.
- **Çıkarım:** (a) tek görselde en fazla 4 kare ve kare başına ≥540×960; (b) şüpheli bölgeler kırpılıp ayrı verilmeli; (c) "hata var mı?" yerine dar sorular ("bu iki öğe çakışıyor mu?"); (d) kesin ölçülebilen her şey hesapla yapılmalı.

## 6. Kesin (deterministik) araçlar
- **ffmpeg:** `blackdetect`, `freezedetect`, `silencedetect`, `scdet` (sahne değişimi) tek geçişte; kural katmanı pass/warn/fail üretir [B/R]. "Her 2–3 sn'de görsel değişim" kuralını `scdet`/kare farkıyla sayıya dökebiliriz; donmuş efekt karesi `freezedetect` ile yakalanır.
- **OCR (PaddleOCR, Apache-2.0) [B]:** render edilmiş karelerde metni oku; yazım/kesilme/güvenli alan dışı taşma kontrolü (ör. "DARIÉN GAP" kenarda kırpıldı). Tesseract bu tür karmaşık videoda zayıf.
- **Altın kare karşılaştırma (Playwright/pixelmatch mantığı) [B]:** onaylanmış kareyle fark; animasyonu dondurarak deterministik. Bizde uygun: render zaten zamanın saf fonksiyonu.
- **Göreli konum doğrulaması (Galen: `inside`, `above`, `near`, `aligned`) [B]:** öğe kutuları üzerinde "A, B'nin içinde / C'yi kapatmıyor" gibi iddialar. Biz bunu kendi sahne verimizde (öğe kutuları) yazarız; DOM'dan `getBoundingClientRect` + kanvas çizim kutuları.
- **Otomatik etiket yerleştirme [B]:** benzetimli tavlama (D3-Labeler, avoid-overlap) enerji fonksiyonu: etiket-etiket örtmesi, etiket-nokta örtmesi, uzaklık, yön tercihi. Etiketleri elle koymak yerine bu çözücüye bırakmak çakışmaları kökten azaltır.
- **Coğrafi doğruluk:** shapely/geopandas ile nokta-çokgen testi (karada mı), poligonu Sentinel/Natural Earth'ten türetme (elle poligon yasak), `validate_routes` genişletilmesi.

## 7. Harita anlatımı ve üretim pratiği [B]
- Yaygın üretim zinciri: QGIS/Mapbox taban + After Effects/Blender hareket. Bizde Sentinel + web render + Remotion/MapLibre aynı işi yapıyor.
- "Belgesel harita" tarzı (ör. Mappi): yavaş kamera itişi, çizilen rota, parlayan ülke sınırı, temiz etiket.
- Harita odaklı anlatı iskeleti: coğrafyayı açıkla → oyuncuları tanıt → zaman içinde hareketi göster → stratejik sonucu açıkla → bugünkü ayak izi ile bitir. (Bizim "Neden…?" iskeletine ek varyasyon kaynağı: videolara farklı iskelet ata.)
- Ses: YouTube Audio Library ses efektleri (≈1072 adet) telifsiz ve gelir getiren videolarda güvenli, atıf gerekmez [R/B]. Freesound lisansları karışık (CC0/CC-BY/NC) — tek tek kontrol gerekir.
- Piyasada hazır "harita animasyon" servisleri var (Mapimator, Animaps, Mappi); bunlar şablonlu olduğu için inauthentic riski yüksek ve kendi sistemimizle çeşitlilik avantajı kaybolur; kullanmamayı öneriyorum.

## 8. Bizim sistemde neyi yanlış yaptık (özet eşleştirme)
| Sorun | Kök neden | Araştırmadaki karşılığı |
|---|---|---|
| Efekt başka sahneye taşıyor, son karede donuyor | motor süreleri otomatik uzatıyor; kapı yok | `freezedetect` + öğe-ömrü kapısı |
| Bayraklar çakışıyor, biçim karışık | yerleşim tahmini + çakışma kapısı yok | Galen tipi göreli konum + etiket çözücü |
| Poligon kara şekline uymuyor | elle poligon | veriden türetme + kara-uyum kapısı |
| İnceleme kaçırıyor | küçük kontakt sayfa | vision çözünürlük sınırı, dar sorular, kırpma |
| Alakasız efekt (roket, baloncuk) | efekt seçimi serbest | efekt başına "anlatım gerekçesi" alanı |
| Aynı hata başka videoda | tek tek düzeltme | altın "hata hayvanat bahçesi" + regresyon |
| Kalıp riski | tüm videolar aynı iskelet | inauthentic politikası: şablon benzerlik ölçümü |

## 9. Önerilen mimari ve öncelik
**Katman 0 – Yazım kısıtları:** (1) elle koordinat/poligon yok; (2) her efekt `why` kelimesine bağlı, anlatımda geçmeyen efekt reddedilir; (3) etiketleri çözücü yerleştirir; (4) videoya iskelet türü atanır (varyasyon).
**Katman 1 – Hesaplı kapılar (render öncesi ve sonrası):** öğe ömrü/sahne sızıntısı, klip kare sayısı≈süre, her karede öğe kutuları (çakışma, konuyu örtme, ekran dışı, güvenli alan), poligon-kara uyumu, biçim karışımı/kutulu yazı, hedef ekranda mı, `freezedetect/blackdetect/silencedetect/scdet`, OCR (yazım/kesilme), "her 3 sn'de değişim".
**Katman 2 – Çok geçişli görsel kontrol:** hata türü başına ayrı geçiş (çakışma, mantık/dönem, ölçek/kara-deniz, efekt-anlatı uyumu, okunabilirlik); tam çözünürlüklü kırpmalar; videoyu yazandan **bağımsız** gözden geçirici; sahne başına ve geçişlerde örnekleme (başlangıç/orta/son + efekt vuruşları).
**Katman 3 – Altın küme:** bu görüşmede senin bulduğun ~30 hata (bayrak çakışması, poligon taşması, yanardağ önünde alev, roket, baloncuk, donmuş patlama, tekrar vuruş…) kare/kırpma olarak saklanır; her kapı/hakem değişikliğinde bunların hepsini yakalaması şart (kappa ≥0,6 hedefi).
**Katman 4 – Ölçüm:** Studio'dan "viewed vs swiped away" + tutma eğrisi dışa aktarımı (veya vidIQ) → düşüş sahneleri → kurgu kararı.

Öncelik: K1 (kapılar) → Altın küme → K2 → K0 → K4. Kurulum gerektirenler: PaddleOCR (pip, Apache-2.0). Üçüncü taraf skill/MCP kurulumu önerilmiyor.

## 10. Doğrulanamayanlar / sınırlar
- Gelir ve algoritma eşiklerinin çoğu blog kaynaklı ve yaklaşık; resmi olan YPP eşikleri ve inauthentic politikası.
- En başarılı coğrafya Shorts kanallarının tutma verisi herkese açık değil; kendi videolarımızın verisi tek gerçek kaynak.
- Görsel hakem doğruluğu ölçülmeden güvenilmemeli; altın kümeyle ölçeceğiz.

## Kaynaklar
- [YouTube Help: YPP monetization policies (inauthentic content)](https://support.google.com/youtube/answer/1311392)
- [YouTube Help: YPP eligibility](https://support.google.com/youtube/answer/72851)
- [YouTube Analytics API channel reports](https://developers.google.com/youtube/analytics/channel_reports)
- [Anthropic: Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- [Spotlight: Identifying and Localizing Video Generation Errors Using VLMs](https://arxiv.org/html/2511.18102)
- [Owl Eyes: Spotting UI Display Issues](https://arxiv.org/pdf/2009.01417) · [Nighthawk](https://arxiv.org/pdf/2205.13945)
- [OpenMontage-Agent](https://github.com/DrHossamAshour/OpenMontage-Agent) · [skill-motion-graphic](https://github.com/hculap/skill-motion-graphic) · [Video as Code: Remotion and the Agent Feedback Gap](https://www.digitalapplied.com/blog/video-as-code-remotion-agentic-generation-2026)
- [Awesome Claude Video Skills](https://github.com/zhuyansen/awesome-claude-video-skills) · [Claude-Code-Video-Toolkit](https://github.com/wilwaldon/Claude-Code-Video-Toolkit)
- [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html) · [Video QC gate (DEV)](https://dev.to/masonwritescode/build-a-video-qc-gate-that-catches-black-frames-before-your-viewers-do)
- [PaddleOCR for video](https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/paddleocr-text-detection-video)
- [Galen spec language](https://galenframework.com/docs/reference-galen-spec-language-guide/) · [D3-Labeler](https://github.com/tinker10/d3-labeler) · [Automatic label placement](https://en.wikipedia.org/wiki/Automatic_label_placement)
- [LLM-as-judge calibration](https://deepchecks.com/llm-judge-calibration-automated-issues/) · [Best practices 2026](https://futureagi.com/blog/llm-as-judge-best-practices-2026/)
- [YouTube Shorts algorithm 2026 (vidIQ)](https://vidiq.com/blog/post/youtube-shorts-algorithm/) · [Shorts retention rate](https://www.shortimize.com/blog/youtube-shorts-retention-rate)
- [Shorts monetization 2026](https://fluxnote.io/guides/youtube-shorts-monetization-2026-updates) · [Engaged views (YouTube Blog)](https://blog.youtube/inside-youtube/engaged-views-youtube-explained/)
- [YouTube AI disclosure rules 2026](https://shortsfast.com/blog/youtube-ai-content-disclosure-rules-2026/) · [AI voice and monetization](https://typecast.ai/learn/youtube-ai-monetization-july-15-ypp-update/)
- [YouTube Audio Library help](https://support.google.com/youtube/answer/3376882)
- [Mappi: documentary map animation](https://mappi.studio/documentary-map-animation)
