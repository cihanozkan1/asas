# Bağımsız gözden geçirici (render sonrası, yayından önce)

Videoyu yazan kişi kendi hatasını görmez. Bu yüzden her video, **yazandan bağımsız** bir ajan tarafından, yalnızca inceleme paketiyle ve aşağıdaki kontrol listesiyle incelenir. Kapılar (`tools/gates`) hesapla yakalanabilenleri yakalar; gözden geçirici hesapla yakalanamayanları arar.

## Paket
`python3 tools/gates/review_pack.py <id>` → `output/<id>/review/` (sahne başına 3 kare + her efekt/damga/bayrak/karakter girişinden 0,6 sn sonra kare; kare başına 520 px, sayfa 1560×924: Claude küçültmesin diye). `index.md` her sahnenin anlatımını ve öğe listesini verir.

## Kullanım kuralları (araştırmadan: docs/ARASTIRMA_KALITE_VE_GELIR.md)
- Her sayfaya **tam boyutta** bak; "hata var mı?" diye değil, aşağıdaki **dar sorularla**, geçiş türüne göre ayrı geçiş yap.
- Her sayfa için her geçişte "sorun yok" ya da bulgu yaz; atlamak yasak.
- Şüphe varsa kırp ve büyüt (PIL ile), tahmin etme.
- Ajan, yazım bağlamını bilmez: sadece `review/` klasörü, `index.md` ve bu dosya verilir.

## Geçişler ve sorular
1. **Örtme/kalabalık:** İki yazı, yazı–ikon, bayrak–bayrak, efekt–damga üst üste mi? Etiket işaretlenen noktayı/bölgeyi kapatıyor mu? Bayrak, bayrak dolgusunun üstünde mi? Aynı yerde gereksiz iki efekt var mı?
2. **Mantık/dönem artığı:** Önceki sahnenin gemisi, damgası, karakteri, rotası, efekti bu sahnede duruyor mu? Tarih sahnesinde modern öğe, modern sahnede tarih öğesi var mı? Gemi suda, araç karada mı? Kişi geminin üstünde mi?
3. **Coğrafya/ölçek:** İşaretlenen şekil (poligon, ülke, ada) gerçek kara parçasıyla örtüşüyor mu, taşıyor mu? Etiket doğru yerde mi? Harita yüzeyinde bariz bozukluk (siyah leke, düz mavi dikdörtgen, bulanık taban) var mı?
4. **Efekt–anlatım uyumu:** Her efekt o an söylenen kelimeyle ilgili mi? Hikâyeyle ilgisiz süs (roket, baloncuk…) var mı? Efekt kelimeden önce/sonra gereksiz uzun mu duruyor?
5. **Okunabilirlik:** Yazı kenarda kesiliyor mu? Alt %17 ve sağ düğme sütununda önemli yazı var mı? Altyazı örtülüyor mu? Kontrast yeterli mi?
6. **Süreklilik/hareket:** Üç sahne arası kare değişimi var mı, sabit/donuk kare var mı? Efekt son karede donup kalıyor mu? İlk karede kanca yazısı var mı?
7. **Doğruluk:** Ekrandaki sayı/yıl/isim anlatımla ve `sources` ile uyuşuyor mu? Yazım hatası?

## Çıktı biçimi
Her bulgu: `{"sahne": n, "zaman": "12.3s", "gecis": 1-7, "ciddiyet": "hata|uyari", "aciklama": "...", "sayfa": "scene05_1.jpg"}`; bulgu yoksa `[]`. Ardından sayfa başına "sorun yok" listesi.

## Yazan kişinin yükümlülüğü
Bulguların hepsi düzeltilir, kapılar yeniden koşulur, paket yeniden üretilir ve **yeni** bir gözden geçirici başlatılır; temiz çıkana kadar tekrarlanır. Yeni hata sınıfı bulunursa `tools/gates/golden/`a eklenir ve ilgili kapı yazılır.
