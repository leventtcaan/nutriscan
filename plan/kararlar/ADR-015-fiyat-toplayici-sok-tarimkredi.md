# ADR-015 · Fiyat ve ürün verisi: web kataloglarından sözlükle sınırlı toplayıcı (pilot ŞOK + Tarım Kredi); fiş çıkar; K21

**Tarih / onay:** 2026-09-29, ÖNERİ (yazan: Levent; yön kararı Levent 29 Eyl; Hilal görüşü 29 Eyl işlendi — teyit bekleniyor; ekip onayı bekliyor)
**Yerine geçtiği:** ADR-002'nin B planı (ekip fiyat turu + hane fişi) ve ADR-003 (pilot Migros + A101). Dayanak: `arastirma/12-fiyat-verisi-edinim.md`.

- **Ne:**
  1. **Ürün ve Fiyat Toplayıcı:** zincir başına küçük bir okuyucu (adapter). Yalnız **tarif sözlüğündeki malzemelere karşılık gelen**
     ürünlerin zincirin herkese açık web kataloğundaki fiyatını, indirimsiz fiyatını, marka ve gramajını, içindekiler metnini ve
     kaynak URL + tarihi okur. Katalog aynalanmaz. Çalışma kuralları K21'dir.
  2. **Pilot zincirler: ŞOK + Tarım Kredi Koop Market**, ikisi birden Kasım'da. Yeni zincir = yeni adapter (mimari zincirden bağımsız).
  3. **İki kullanım katmanı:**
     - **Geliştirme, deney (E1–E3) ve jüri demosu:** K21 kurallarıyla toplanan, sözlükle sınırlı, kaynağı kaydedilmiş, yayımlanmayan
       veri; arayüzde kaynak ve tarihle gösterilir. (Hilal görüşü m.4: "kapsamı belli ve kaynağı kaydedilmiş sınırlı veri".)
     - **Kamuya açık canlı ürün:** ancak kaynağın **yazılı izni ya da lisanslı bir veri kaynağıyla**. Uygulama olgunlaşınca (canlı
       öncesi) ŞOK, Tarım Kredi ve Migros'a ayrı ayrı yazılı izin talebi; CimriMarket / MarketTamam'a kullanım hakkı veren API ya da iş
       ortaklığı sorusu; Bakanlık/TÜBİTAK'a meta veri talebi. TÜBİTAK'ın o uygulamalarla paylaşması NutriScan'e hak doğurmaz.
  4. **Eşleme malzeme → ürün:** "yoğurt 1 kg" → her zincirde uygun aday ürünler. LLM eşleme önerebilir; kabul kural ya da insan
     onayıyla (K01). Barkod gerekmez (iki zincirin sayfasında da yok).
  5. **İçindekiler metni aday veridir:** güvenilmeyen içerik olarak karantina çıkarıcıdan geçer (K04); "katalogda doğrulandı" ancak
     moderasyonla; riski azaltan değişiklik tek kaynaktan kabul edilmez (K12).
  6. **Tazelik ve sağlık:** her fiyat kaynak + tarih taşır; bir zincirin çekimi başarısız olur ya da TTL aşılırsa o zincirin fiyatları
     `COULD_NOT_VERIFY`, optimizasyona girmez (S8, K11). Çekim işi heartbeat yayar (K18). TTL ve hız sınırı yapılandırmadadır.
  7. **Fiş ürünün tamamından çıkar** (fiyat, kiler, eşleştirme). Kiler: barkod + "bitti" + alışveriş listesinde "aldım" işareti.
     E3'ün fiyat ölçütü fiyat tazeliğidir (medyan fiyat yaşı, `COULD_NOT_VERIFY` oranı). Mağaza raf fiyatı doğrulaması yapılmaz (Levent kararı
     29 Eyl: efor/değer); fiyat arayüzde "online katalog fiyatı · tarih" olarak etiketlenir.
  8. **Taze meyve-sebze boşluğu:** online kataloglarda zayıf; eksik kalemde hal / WFP fiyatı yalnız "tahmini" referans, karar girdisi değil.
  9. **Anayasaya K21** (metin aşağıda; anayasada ÖNERİ işaretiyle).
- **K21 metni:** Dış kaynaktan otomatik veri toplama yalnız robots.txt'in izin verdiği yollardan, kendini tanıtan bot adı ve iletişimle,
  yapılandırmadaki hız sınırıyla yapılır; giriş, CAPTCHA, bot koruması ya da IP döndürmeyle hiçbir erişim engeli aşılmaz; kapsam tarif
  sözlüğüyle sınırlıdır, katalog aynalanmaz; her kayıt kaynak URL + tarih taşır; toplanan ham veri yeniden yayımlanmaz. Kamuya açık canlı
  ürün ancak kaynağın yazılı izni ya da lisansla; o zamana kadar veri yalnız geliştirme, deney ve demoda kullanılır. Açık ret ya da itiraz
  gelen kaynakta toplama durur (ADR-002 emsali).
- **Neden:**
  - Fiş hanenin sabit alışkanlığını gösterir, seyrek ve geç gelir; ekip fiyat turu 2 haftada ~300 ürünle sınırlı. İkisi de sunumdaki
    kenar durumu sorularını karşılamaz ve ürün canlıya çıkamaz.
  - Hazır, ürün düzeyinde, zincir bazında yasal bir kaynak yok; Open Prices TR'de 28 fiyat (arastirma/12 §2).
  - ŞOK ve Tarım Kredi, 13 zincir içinde robots.txt'i ürün sayfalarına açık ve herkese açık koşullarında otomatik erişim yasağı
    bulunmayan iki zincir; fiyat ve içindekiler HTML'de, koruma aşmak gerekmiyor (arastirma/12 §4). Migros, A101 ve diğerleri koşullarla
    ya da bot korumasıyla kapalı; onlara dokunulmaz.
  - Sözlükle sınırlı kapsam FSEK Ek m.8'in "önemli kısım" riskini küçültür; yayım yok TTK m.55 riskini küçültür; koruma aşılmaması TCK
    m.243 riskini dışarıda bırakır (arastirma/12 §6).
  - ŞOK indirim zinciri, Tarım Kredi uygun fiyatlı kooperatif: tezdeki kitleyle Migros'tan daha tutarlı.
  - İçindekiler metni alerjen motoruna da girdi sağlar (OFF TR kapsamı zayıf). İkinci zincir Ocak yerine Kasım'da gelir; E1 baştan iki zincirli.
- **Alternatif:** (a) ekip fiyat turu + fiş (ADR-002 B planı) · (b) Open Prices'ı ekiple tohumlamak · (c) demo dahil her şeyden önce
  yazılı izin beklemek · (d) zincir adı gizlenmiş ("Market A/B") gösterim · (e) korunan zincirleri (Migros, A101, CarrefourSA) kazımak ·
  (f) yalnız Bakanlık/TÜBİTAK protokolü.
- **Neden değil:** (a) ölçeklenmez, kenar durumu kapsamaz · (b) yine elle toplama, TR'de boş, ODbL share-alike · (c) cevap belirsiz ve
  uygulama olgunlaşmadan istenen izin zayıf kalır; kritik yol (27 Kas MSM gerçek veri) bekler — canlı öncesi yapılır · (d) risk
  verinin çekilme biçiminden doğar, gösterimden değil; kullanıcı "Market A"da ne yapacağını bilemez · (e) koşullarda açık yasak ve bot
  koruması; aşmak TCK m.243 riski · (f) süresi ve sonucu belirsiz; paralel başvuru, kritik yola konmaz.
- **Geri dönmenin maliyeti:** orta. Adapter katmanı fiyat kaynağını soyutlar: bir zincir kapanırsa ya da izinli/lisanslı bir kaynak
  gelirse yalnız adapter değişir; MSM ve katalog şeması aynı kalır. Metin revizyonu tek seferlik.
- **Açık risk:** (1) online fiyat mağaza raf fiyatından farklı olabilir — **kabul edilen risk**; etiket dürüst ("online katalog fiyatı · tarih").
  (2) Canlı öncesi izin/lisans gelmezse fiyat karşılaştırma canlıda kapalı kalır; demo ve deneyler etkilenmez. (3) Site yapısı
  değişirse adapter kırılır → sağlık kontrolü + `COULD_NOT_VERIFY`. (4) FSEK Ek m.8 gri alanı kapsam sınırıyla küçülür, sıfırlanmaz.
- **Etkilenen:**
  - Kararlar: ADR-002 (B planı yerine geçildi) · ADR-003 (yerine geçildi) · ADR-010 (marketfiyati satırları).
  - Metinler: `arastirma/07-tez-v5.md` (v5.2) · `plan/urun-tanimi.md` · `plan/proposal/proposal-v0.md` · `plan/takvim.md` · `DURUM.md`.
  - Board (`plan/board/pbi.yaml`): A2.4-a katalog v0 (ŞOK + Tarım Kredi) · A2.4-b fiyat turu → toplayıcı · A2.5-b kapsama hedefi ·
    A0.2-a fiş kaydı → yalnız "bitti/attım" · A3.1 (A101) → canlı öncesi izin/lisans · A4.8 (fiş eşleştirme) düşer ·
    A2.7-c, A2.13-a girdileri.
  - Anayasa: yeni K21; ilgili S8, K01, K04, K11, K12, K18.
  - Modül: `catalog` (Hilal): adapter'lar, zamanlayıcı, sağlık kontrolü.
