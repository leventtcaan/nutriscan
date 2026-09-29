---
title: Fiyat verisi edinim yolu — marketfiyati reddi sonrası tarama ve fizibilite denemesi
updated: 2026-09-29
dayanak: ADR-002 (red sonucu) · 01-mevzuat-risk §6 · 02-v2-fis-veri §5 · 05-menu-kiler-oneri §3 (MSM)
yöntem: üç paralel masa başı araştırma (yasal kaynaklar · zincir zincir kazıma · emsaller) + robots.txt'e uyan küçük deneme (28–29 Eyl 2026)
etiketler: [F] kaynak açıldı ve okundu · [C] veriden hesaplandı · [S] yalnız arama özeti · [U] doğrulanamadı
---
# Fiyat verisi edinim yolu

> Bu bir masa başı araştırmadır, hukuki görüş değildir. Karar: ADR-015 (ÖNERİ).

## 0. Soru ve sonuç
**Soru:** marketfiyati.org.tr yazılı olarak reddettikten sonra (ADR-002), MSM'nin ihtiyacı olan zincir bazında, ürün düzeyinde,
haftalık fiyat verisi yasal ve sürdürülebilir biçimde nereden gelir? Hane fişi ve ekip fiyat turu ölçeklenmiyor: fiş hanenin sabit
alışkanlığını gösterir, kenar durumları kapsamaz; fiyat turu 2 haftada ~300 ürün.

**Sonuç:**
1. Ürün düzeyinde, zincir bazında, haftalık ve **hazır** yasal bir kaynak yok (§2).
2. Veri resmî olarak toplanıyor: 200+ şubeli zincirler fiyatı Bakanlık sistemine göndermekle yükümlü; TÜBİTAK bunu CimriMarket ve
   MarketTamam'la paylaşıyor (§3). Bu, başvurulabilecek bir lisans kanalı olduğunu gösterir; NutriScan'in kullanım hakkı buradan
   çıkmaz, ayrıca başvurulmalıdır.
3. Zincirlerin kendi web katalogları: 13 zincirden **ŞOK ve Tarım Kredi Koop** robots.txt ve herkese açık koşullar bakımından
   savunulabilir; fiyat, marka, gramaj ve **içindekiler** HTML'de (§4, §5). Diğerleri koşullarla ya da bot korumasıyla kapalı.
4. Hukuki gri alan FSEK Ek m.8'in "önemli kısım" ölçütünde; tasarımla küçültülür: kapsam tarif sözlüğüyle sınırlı, katalog
   aynalanmaz, veri yeniden yayımlanmaz, koruma aşılmaz. **robots.txt ve koşulların sessizliği yazılı izin değildir:** bu kurallarla
   toplanan veri yalnız geliştirme, deney ve demoda; kamuya açık canlı ürün ancak yazılı izin ya da lisansla (ADR-015, K21; Hilal
   görüşü 29 Eyl m.4).

## 1. Gereken veri
- Zincir × ürün: ad, marka, gramaj/paket, raf fiyatı, indirimsiz fiyat, tarih, kaynak URL. Tercihen içindekiler (alerjen motoru).
- Ölçek: tarif sözlüğündeki malzemeler (birkaç yüz) × zincir başına aday ürünler; haftalık tazelik; MSM için ≥ 2 zincir.
- Eşleme ürünle ürün değil, **malzemeyle ürün**: "yoğurt 1 kg" → her zincirde uygun en ucuz ürün. Barkod gerekmez.

## 2. Hazır yasal kaynaklar
| Kaynak | Ürün düzeyi | Durum | Not |
|---|---|---|---|
| Open Food Facts Open Prices (ODbL) | Evet | **TR'de 28 fiyat, 16 konum** [C] (HF dökümü 318.187 satır, 27 Eyl 2026; API `currency=TRY` 28 kayıt [F]) | Pratikte boş; API bugün 504 verdi. [HF](https://huggingface.co/datasets/openfoodfacts/open-prices) · [API](https://prices.openfoodfacts.org/api/v1/prices?currency=TRY) |
| WFP Türkiye gıda fiyatları (CC BY-IGO) | Hayır, 44 emtia, ulusal ortalama, aylık | Kullanılabilir [F] | Yalnız "tahmini" referans. [HDX](https://data.humdata.org/dataset/wfp-food-prices-for-turkiye) |
| İzmir BB hal fiyatları | Hayır, günlük toptan | Kullanılabilir; 28 Eyl'de 97 ürün [F] | [Açık veri](https://acikveri.bizizmir.com/en/dataset/sebze-ve-meyve-hal-fiyatlari) |
| İBB hal fiyatları web servisi | Hayır, günlük | Lisans doğrulandı, uç noktalar [U] | [İBB](https://data.ibb.gov.tr/dataset/hal-urunleri-ve-fiyatlari-web-servisi) |
| TÜİK | Hayır (Mayıs 2022'den beri yalnız endeks) | Kullanılamaz [F] | [Duyuru 14](https://www.tuik.gov.tr/media/announcements/Tufe_duyuru_tr.pdf) |
| Cimri / Akakçe API | — | Yalnız satıcı entegrasyonu [S] | Cimri robots.txt `/api/` kapalı [F] |
| Apify aktörleri (Migros, A101, Getir) | — | İzin yerine geçmez | Migros koşulları robotu yasaklıyor (§4) |
| NielsenIQ / Circana / GfK / Measurable AI | — | Gerçekçi değil | Panel/satış ölçümü, raf fiyatı değil; kurumsal fiyat |
| Kaggle / HF / GitHub setleri | — | Kullanılamaz | GitHub setleri lisanssız ve izinsiz kazıma (market-indirim-data, migros-scraper, cimri_market_api) [F] |

## 3. Resmî kanal: veri var, lisanslanıyor
- **Perakende Yönetmeliği m.12/Ç** (RG 7 Ara 2022, 32036): 200+ şubeli gıda perakendecileri ürün ve şube verisini Bakanlığın
  belirlediği sisteme aktarır; "kamuoyuyla paylaşılabilir" (takdir). [F] [mevzuat.gov.tr](https://www.mevzuat.gov.tr/File/GeneratePdf?mevzuatNo=22722&mevzuatTur=KurumVeKurulusYonetmeligi&mevzuatTertip=5)
- **TÜBİTAK:** A101, BİM, CarrefourSA, Hakmar, Migros, Tarım Kredi, ŞOK verisi temizlenip **CimriMarket ve MarketTamam**'a
  veriliyor (11 Şub 2025). [F] [TÜBİTAK](https://tubitak.gov.tr/tr/haber/zincir-market-fiyatlarina-aninda-erisimin-onu-acildi)
  → marketfiyati'nin "üçüncü taraflara vermiyoruz" cevabı ticari lisans kanalını dışlamıyor; kriterler yayımlanmamış [U].
- **4982 bilgi edinme:** veri almak gerçekçi değil (m.7 özel çalışma, m.8 yayımlanmış bilgi, m.23 ticari sır) [F]; ama
  **meta veri** istenebilir: m.12/Ç usul ve esasları, üçüncü taraf erişim kriterleri.
- **TÜİK emsali:** barkod verisi ikili protokollerle (2026'da fiyatların %43,29'u); web kazıma TÜBİTAK projesiyle ve
  "şirketlerden gerekli izinler alınarak", gıda dışı kalemlerde (%5,57). [F] [TÜFE yöntem belgesi 2026 §7.2–7.3](https://veriportali.tuik.gov.tr/api/en/data/downloads?t=r&p=MIuxEHQMO0LGQb15J78DA%2FsGg%2FNV1pc6o%2BLILgK8hFQqDeIpWxTRir%2Fdy7%2FS%2FLONi009sk1BfocOWe5Kqcz2OP0XGGHIg8JZQdpaZ0iaAOU%3D)

## 4. Zincir zincir web kataloğu (28 Eyl 2026)
Kural: tanımlı bot adı (`NutriScan-research/0.1 …`), zincir başına birkaç istek, koruma aşılmadı, giriş yapılmadı. Engellenen
zincirlerin yasal sayfaları tarayıcıda normal ziyaretçi olarak okundu; fiyat toplanmadı.

| Zincir | robots.txt | Kullanım koşulları | Teknik | Sonuç |
|---|---|---|---|---|
| Migros | Ürün sayfaları açık | Robot, spider, "page-scrape" yasak [F] [işlem rehberi](https://www.migros.com.tr/islem-rehberi?id=10) | SSR, JSON-LD fiyat | 🔴 (yazılı izinle açılır) |
| Macrocenter | Ürün açık | "screen scraping" yazılı izinsiz yasak [F] [üyelik](https://www.macrocenter.com.tr/uyelik-sozlesmesi) | Migros altyapısı | 🔴 |
| A101 / Kapıda | Ürün açık | Otomatik program ile içerik edinme yasak (§4.12, §4.18) [F] [üyelik](https://www.a101.com.tr/sozlesmeler/uyelik-sozlesmesi) | Cloudflare challenge | 🔴 |
| **ŞOK** | Ürün açık, yalnız `/arama` kapalı [F] | Herkese açık sayfalarda yasak bulunamadı [F] ([yasal uyarı](https://www.sokmarket.com.tr/hesabim/yardim-ve-destek/yardim/yasal-uyari)); üye sözleşmesi [U] | Next.js SSR; fiyat, indirimsiz fiyat, marka, içindekiler HTML'de; site haritası 20.910 ürün (28 Eyl) [C] | 🟢 şartlı |
| **Tarım Kredi Koop** | `Disallow:` boş (hepsi açık) [F] | Bulunamadı; yalnız KVKK ve çerez [F] | Laravel SSR; kategori sayfası 18 ürün/sayfa, fiyat HTML'de; ürün sayfasında içindekiler [C] | 🟢 şartlı |
| BİM | robots.txt yok | Koşul sayfası yok | Yalnız haftalık aktüel | 🟢 ama kapsam yok |
| Hakmar Express | Açık | Kopyalama yasak [F] | JSON API | 🟡 |
| CarrefourSA | Tanımlı bot'a 403 | İzinsiz kopyalama yasak [F] | Cloudflare | 🔴 |
| Getir | Ürün kapalı | Katalog/veritabanı kopyalama yasak §7.3 [F] | CloudFront 403 | 🔴 |
| Trendyol Go | `Disallow: /` [F] | İzinsiz kopyalama yasak [F] | App | 🔴 |
| Yemeksepeti | Kısmen açık | [U] (PerimeterX CAPTCHA; çözülmedi) | Korumalı | 🔴 |
| Metro | Fiyat alt alanı `Disallow: /` [F] | — | Akamai | 🔴 |
| File | — | — | Yalnız app | Uygulanamaz |

**Tarım Kredi gıda kataloğu ölçümü** (12 gıda kategorisinin ilk sayfası + sayfa sayısı × 18) [C]: ~1.900–2.100 ürün.
Temel gıda ~580 · atıştırmalık ~490 · içecek ~290 · et ~200 · şarküteri-kahvaltılık ~130 · peynir ~55–70 · yoğurt ve dondurulmuş
~40–55 · süt, sıvı yağ, meyve-sebze, sütlü tatlı ~20–36 · tereyağı-krema 8. **Taze meyve-sebze zayıf.**
**Barkod:** ŞOK ve Tarım Kredi ürün sayfalarında bulunamadı → eşleme malzeme → ürün (§1).

## 5. Emsaller
- **Tüketici uygulamaları:** Market Fiyatı, CimriMarket, MarketTamam aynı TÜBİTAK verisi [F]; Sepetix Market Fiyatı servisi [S];
  uyguno "otomatik" günlük, kaynak açıklanmıyor [F]; Fiyatbu POS verisi (çıkarım) [F]. Açık Sepet (GitHub) marketfiyati
  arayüzünün servisini kullanıyor [F] — kapsam dışı yol.
- **Akademi:** Soybilgen, Yazgan, Kaya (2023) zincir sitelerinden 5,9 M günlük gıda fiyatı [F özet]; Yalçın ve Baysal (2024,
  TÜİK'in dergisi) kazıma, hukuk/etik tartışması yok, veri yayımı yok [F]. Emsal var ama gerekçe olarak zayıf.
- **Uluslararası:** Hırvatistan 15 May 2025'ten beri perakendeciye günlük makinece okunur fiyat yükümlülüğü [F]; Kroger resmî
  ürün API'si [S]; Tesco API kapandı [S]; Avusturya Heisse Preise kazımayla çalışıyor, SPAR API değişince 5 ay veri kaybı [F].
- **e-Arşiv:** Migros online müşteri son 1 yılın faturalarını indirebiliyor [F]; UBL-TR satır kalemli [S]. Fiş kanalı ADR-015
  ile kapsam dışı; bilgi olarak tutuldu.

## 6. Hukuki çerçeve (masa başı)
- **FSEK Ek m.8:** esaslı yatırımla oluşturulmuş veritabanının "önemli bir kısmının" aktarımı izne bağlı; araştırma ya da TDM
  istisnası yok (2026 itibarıyla). Veri ve materyalin kendisi korunmaz (FSEK m.6/11). Rekabet Kurulu Nadirkitap kararında
  esaslı yatırım yokluğundan koruma tanımadı ([22-57/886-366](https://www.rekabet.gov.tr/Karar?kararId=4645c49c-a4bb-490c-8c00-42c7c60d0a35)) [F].
  **Tasarım sonucu:** katalog aynalanmaz; sözlükle sınırlı birkaç yüz ürün.
- **TTK m.55/1-c-3:** başkasının iş ürününü teknik yolla aktarma; piyasa ilişkisini etkilemesi gerekir. Kapalı, ticari olmayan
  demoda zayıf; veri yeniden yayımlanır ya da rakip fiyat servisi görünümü alırsa artar.
- **TCK m.243/244:** giriş, CAPTCHA, bot koruması ya da IP döndürme ile aşma "hukuka aykırı giriş" tartışması doğurur; aşırı yük
  m.244. **Tek gerçek ceza riski; korunan zincirler bu yüzden kapalı kalır.**
- **robots.txt ≠ koşullar:** robots teknik işaret, koşullar sözleşme katmanı. Migros, Macrocenter, A101 robots'ta ürünü açıp
  koşullarda botu yasaklıyor. Tıklanmamış (browsewrap) koşulların bağlayıcılığı TBK m.21'e göre zayıf, ama yok saymak kötü niyet
  delili olur.
- **KVKK:** fiyat ve ürün için ilgisiz (kişi verisi toplanmıyor).

## 7. Açık sorular
1. **Online fiyat = mağaza raf fiyatı mı?** (ŞOK, Tarım Kredi) — doğrulanmayacak (29 Eyl, efor/değer); kabul edilen risk, arayüz etiketi "online katalog fiyatı · tarih" (ADR-015).
2. Tarım Kredi'nin Antalya'da şubesi ve online kataloğun bölgeye göre değişip değişmediği.
3. ŞOK üye sözleşmesinin tam metni.
4. BİM aktüel sayfasının yapısı (deneme adresi yanlıştı).
5. TÜBİTAK/Bakanlık üçüncü taraf erişim kriterleri (4982 meta veri talebi).

## 8. Deneme kaydı (ham çıktı yeri)
28–29 Eyl 2026 toplam ~18 istek (ŞOK, Tarım Kredi) + BİM'e 1 yanlış adres; hepsi robots.txt izinli, 5 sn aralıklı. Ajanların
robots.txt kopyaları ve indirilen sayfalar oturum geçici klasöründeydi; depoya alınmadı (üçüncü taraf içerik).
