Bu oturumda NutriScan (CSE 491/492 bitirme projesi, Akdeniz Üniv. Bilgisayar Müh.; ekip: Levent, Hilal, Ozan; danışman
Arş. Gör. Dr. Taha Yiğit Alkan) için **rakip analizi ve ayrışma (differentiation) araştırması** yapacaksın. Sonuç yarın
(9 Ekim) danışmana sunulacak. Kod yazmıyorsun; araştırıp yazıyorsun.

## 1. Önce bunu bil: proje yönü 2 Ekim'de değişti
- Danışman, eski önerimizi (hanenin haftalık yemek + alışveriş planı, fiyat, barkod) yeterince farklı bulmadı: "sonunda ürün
  okutup sonucu görmeye indirgenir, piyasada benzeri var" dedi.
- **Yeni çekirdek:** paketli gıdanın **içindekiler kısmı OCR ile okunur** → içerikler (katkı maddeleri/E-kodları dahil)
  standart kavramlara eşlenir → kullanıcının **sağlık durumlarıyla kanıta dayalı hastalık–içerik eşleşmesi** yapılır → sonuç
  kullanıcıya **doğru ve belirsizliğiyle** anlatılır. **Barkod okuma iptal.**
- Danışmanın açık talepleri: (1) en yakın **5 rakibi** bul, (2) bizim özelliklerimizin onlarda olmadığından emin ol / farkımızı
  netleştir, (3) yaklaşım **literatürle savunulabilir** ve **piyasada olmayan** bir yaklaşım olsun.
- Ekipteki ön çalışma (Ozan): FooDB (gıda bileşikleri), JECFA ve EFSA OpenFoodTox (katkı maddesi kimliği, ADI, toksikoloji),
  CTD (kimyasal–hastalık ilişkisi, MeSH), SapBERT / mSapBERT / MedCPT / BGE-M3 (biyomedikal entity linking ve gömme),
  Qdrant (vektör arama + metadata filtresi). Dokümanlar: `toplanti/2026-10-02-ozan-veri-vektor-analizi.pdf`,
  `toplanti/2026-10-02-ozan-mimari-ozet.pdf`. Görüşme kaydı: `toplanti/2026-10-02-MR1-taslak-duzeltilmis.pdf`.

## 2. Repodaki dosyalar hakkında uyarı
- `DURUM.md` başındaki "YÖN DEĞİŞTİ" notunu oku. `arastirma/07-tez-v5.md`, `plan/urun-tanimi.md`, `plan/kararlar/ADR-015*`,
  `plan/board/*` ve prototip **eski yöndür**: ürün tanımı olarak kullanma.
- `AGENTS.md`'deki **kırmızı çizgiler ve Git kuralları geçerli** (uydurma yok, sır yok, tıbbi dil yok, commit/PR'da AI imzası
  ve araç adı yok).
- Faydalı ama **24 Eylül tarihli ve ham** önceki araştırma: `arastirma/01-rakip-pazar.md` (Yuka, Fig, Fooducate, CodeCheck,
  Spoon Guru, Open Food Facts, Ürün Dedektörü, ÇabukBak, İçerik Tara, Gluten Tarayıcı vb.), `arastirma/05-ai-native-rakip.md`,
  `arastirma/02-v2-ozgunluk-talep.md`, `arastirma/02-v2-yontem-literatur.md`, `arastirma/01-mevzuat-risk.md`. Bunları başlangıç
  listesi olarak kullan, **her iddiayı bugün yeniden doğrula** (özellik eski olabilir, uygulama kapanmış olabilir).

## 3. Görev
1. **Karşılaştırma eksenlerini kur** (önce bunu yaz, sonra ara): girdi yolu (barkod / etiket fotoğrafı-OCR / elle) ·
   kişiselleştirme türü (alerjen / diyet / **sağlık durumu**; hangi durumlar, kaç tane) · içerik → standart kavram eşlemesi
   (E-kodu, eşanlamlı, Türkçe) · **eşlemenin kanıtı**: kaynak gösteriyor mu, kanıt derecesi var mı · belirsizliği nasıl
   söylüyor ("bilinmiyor/doğrulanamadı" var mı, yoksa sessizce "uygun" mu) · açıklama ("neden") · Türkçe / Türkiye pazarı ·
   tıbbi iddia ve mevzuat duruşu · iş modeli.
2. **Uzun liste (≥ 15 aday):** global uygulamalar, Türkiye'deki uygulamalar ve **akademik çalışmalar/prototipler**
   (gıda–hastalık bilgi grafları, gıda etiketinden hastalık uyarısı, gıda alanında biyomedikal entity linking; ör. FoodKG,
   FooDis ve benzerleri — varlıklarını ve içeriklerini doğrula, isim uydurma).
3. **İlk 5'i seç:** seçim ölçütünü açıkça yaz (yeni çekirdekle örtüşme). Özellikle **sağlık durumuna göre içerik tarayan**
   ürünleri atlama (ör. Fig'in sağlık/diyet kısıtları, Fooducate'in hastalık modları, Ürün Dedektörü'nün kişisel uyarıları):
   bunlar en tehlikeli rakiplerdir.
4. **İlk 5'in derin incelemesi:** resmî site, App Store / Google Play sayfası, yardım/SSS, varsa makale. Her eksende ne
   yaptıklarını kaynakla yaz; denemediğin şeyi "denendi" diye yazma.
5. **Boşluk analizi → ayrışma adayları (3–5):** her aday için: hangi rakipte kısmen var · neden yeni · literatürde dayanağı
   (gerçek ve erişilebilir kaynak) · 2 dönemde 3 kişiyle yapılabilir mi · **nasıl ölçülür** (tez deneyi olabilecek metrik).
   Muhtemel yön (doğrulamak senin işin): *kanıt derecesi ve kaynağı görünen hastalık–içerik eşleşmesi + Türkçe etikette
   entity linking + belirsizliği dürüst söyleyen sonuç*. Tek başına "hastalığa göre uyarı" yeni değil olabilir; bunu dürüstçe söyle.
6. **Öneri:** 1 çekirdek ayrışma + 2 destekleyici. Jürinin soracağı 5 soruyu ve kısa cevaplarını yaz
   (ör. "Fig zaten yapıyor, farkınız ne?", "CTD ilişkisi nedensellik mi?", "Neden LLM'e sormuyorsunuz?").

## 4. Kurallar
- Her olgusal iddianın yanında **link + erişim tarihi**. Bulamadığını "bulunamadı" diye yaz; sayı, özellik, makale uydurma.
- **"Kimse yapmıyor" deme.** Doğru ifade: "X tarihinde şu N kaynakta arandı, bulunamadı." Danışman savunulabilirlik istiyor.
- Ozan'ın dokümanındaki güçlü iddiaları (ör. "CTD kesin nedensellik", "tüketimi engeller", "milyar ölçek", "26 kat hız") kendi
  analizine taşıma; değinirsen doğrulanmış haliyle değin.
- Tıbbi dil yok: "zararlı, riskli, tedavi, önler, güvenli" yazma; "bilgilendirme" dilinde kal.

## 5. Çıktı
1. `arastirma/13-rakip-analizi-v6.md` (Türkçe, ≤ ~400 satır): eksenler · uzun liste tablosu · ilk 5 seçim gerekçesi · ilk 5 ×
   eksen tablosu (her hücrede kaynak) · boşluk analizi · ayrışma adayları · öneri · jüri soruları · açık sorular · kaynakça.
   Dosya başında `title / tarih / durum: HAM` frontmatter'ı (diğer `arastirma/` dosyaları gibi).
2. `toplanti/2026-10-09-rakip-ozeti.md`: danışmana gösterilecek **tek sayfalık** özet: ilk 5 × 5–6 kritik eksen tablosu +
   3–4 cümlelik "farkımız" ifadesi + kaynak sayısı ve arama tarihi.
3. Başka dosyaya dokunma (board, plan, AGENTS.md, DURUM.md dahil).
4. Git: `docs/rakip-analizi-v6` dalı, commit `docs(arastirma): competitor analysis for re-scoped direction`, PR aç (gövdede
   kısa özet + "AI kullanımı: AI agent ile araştırma ve taslak; doğrulama ekipte"). Commit/PR'da AI imzası ve araç adı yok.
   `main`'e doğrudan yazma.
5. Bitirince bana 10 satırı geçmeyen bir özet ver: ilk 5, önerilen çekirdek ayrışma, en zayıf nokta, ekibe sorulacak 3 soru.
