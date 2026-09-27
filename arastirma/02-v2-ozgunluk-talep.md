---
title: 02 — v2 konsepti: özgünlük denetimi + talep kanıtı
tarih: 2026-09-24
durum: HAM
onceki: 01-rakip-pazar.md (barkod/alerji rakipleri orada, burada tekrar edilmedi)
---

> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24.**
> Web araması + doğrudan veri çekme (OWID CSV, COSI-TUR ve TÜBER PDF'leri). Her iddianın yanında kaynak var.
> Bulunamayan ya da doğrulanamayan her şey açıkça öyle işaretlendi. "Bulunamadı" demek "yok" demek değil, "bu aramada çıkmadı" demek.

v2 bileşen kısaltmaları (tabloda bunlar kullanılıyor):
**a** sepet karnesi (TÜBER'e göre) · **b** kişisel gıda enflasyonu vs TÜİK · **c** akıllı takas MILP + Pareto + gölge fiyat · **d** rafta hane üyesi kararı + sepete etki + alternatif · **e** geriye dönük taklit/tağşiş/geri çağırma uyarısı · **f** doğal dil → kısıt → solver · **g** haftalık liste + hangi market · **h** "Sepet Wrapped"

---

## 0. TL;DR

- **v2'nin tek tek bileşenlerinin hepsi bir yerde var.** Alımdan sepet sağlık skoru (a): Kroger OptUP, Albert Heijn, Summo+, HelloCheck, **Türkiye'de Migros Sağlıklı Yaşam Yolculuğu (~9,4M kişiye ulaşmış)**. Fişten kişisel enflasyon (b): Grocery Tracker, Ghostflation, Yomio. En ucuz market sepeti (g): marketfiyati.org.tr, Cimri, Akakçe. Sağlıklı alternatif (d): FoodSwitch, Tesco, TR barkod uygulamaları. Doğal dil kısıtla sepet (f): Cooklist (ABD, B2B). Alıma göre geri çağırma (e): ABD zincirleri (Costco vb.).
- **Bulunamayan kombinasyon:** zincirden bağımsız (fiş/fatura) toplanan **hane sepeti** üzerinde, **sağlık + kişisel enflasyon + bütçe** tek defterde, ve bunun üstünde **"mevcut sepetten en az sapmayla, bütçeyi aşmadan, alerjen/çölyak hard kısıtlarıyla sağlığı iyileştir" optimizasyonu + "sağlığın TL fiyatı" (gölge fiyat)**. Bunu yapan tüketici ürünü ne globalde ne TR'de bulunamadı. Özgünlüğün ağırlık merkezi **(c)**. (a) ve (b) bunun veri motoru, kendi başına özgün değil.
- **Matematik yeni değil.** Diyet LP'si 1940'lardan, USDA Thrifty Food Plan 1975'ten beri var. Yeni olan, bunu **gözlenmiş gerçek hane sepetine**, **TR'nin çok marketli gerçek fiyatlarına** ve **güvenlik kısıtlarına** uygulamak. Hocaya "yeni algoritma" diye değil, **"bilinen yöntemin yeni veri ve kısıt ortamına uygulanması"** diye sunulmalı.
- **Yeni tehdit:** Sağlık Bakanlığı **27 Ağustos 2026'da Nutri-Score V2 tabanlı "Beslenme Skoru Hesaplayıcı"yı açtı.** Paketli gıdada zorunlu olması planlanıyor. Ürün düzeyinde A–E puanı kamusal mal oluyor, o yüzden bununla rekabet edilmemeli, üstüne inşa edilmeli.
- **Talep kanıtı güçlü, ama bir nüans var:** Gıda enflasyonu yıllık %33,79 (Ağu 2026), gıda hane bütçesinin %17,3'ü (en yoksul %20'de %29,2), obezite %21,8, çocuk fazla kilo+obezite %22,4, enerjinin ~%31'i ultra-işlenmiş gıdadan. **Ancak FAO'ya göre TR'de en ucuz sağlıklı diyeti karşılayamayanların oranı düşük (%4-7).** Yani problem "sağlıklı beslenmeyi karşılayamamak" değil, **"bütçe baskısı altında, bilgi eksikliğiyle, sağlıklı sepeti kuramamak"**. Problem cümlesi buna göre kurulmalı (§4).

---

## 1. v2'ye benzeyen ürünler

### 1.1 Ürün tablosu

| # | Ürün (ülke) | Ne yapıyor | v2 bileşenleri | TR'de? | v2'ye göre eksik |
|---|---|---|---|---|---|
| 1 | **Kroger OptUP** (ABD) | Shopper's Card alımlarından hane düzeyinde "OptUP Score"; "Better for You" benzer ama daha sağlıklı ürün önerisi. Bağımsız uygulama kaldırıldı, özellik Kroger uygulamasında sürüyor. [FAQ](https://www.kroger.com/hc/help/faqs/health-and-wellness/optup), [OptUP sayfası](https://www.kroger.com/health/pharmacy/optup) | a, d (kısmi) | Hayır | Tek zincir. Bütçe/fiyat optimizasyonu, alerjen hard kısıtı ve enflasyon yok |
| 2 | **Albert Heijn – Mijn Voedingswaarden** (NL, 2018) | Bonus kart alımlarının şeker, lif, tuz, protein, doymuş yağ, kalori dökümü; **hangi alımların en çok şeker vb. içerdiği**; seçilen besin öğesine göre alternatif. [AH duyurusu](https://nieuws.ah.nl/albert-heijn-lanceert-mijn-voedingswaarden-op-ahnl/). 2025'te NL'de "slimme swaps / eetwissels" başladı. [Foodpersonality](https://www.foodpersonality.nl/nieuws/nieuws/19099/albert-heijn-slimme-swaps-en-nutri-score-op-alle-producten) | a (en büyük katkı yapan ürünler dahil), d | Hayır | Tek zincir, fiyat boyutu yok. Güncel durumu doğrulanamadı |
| 3 | **Tesco** (UK) | "Helpful Little Swaps": **daha sağlıklı ve aynı fiyatta ya da daha ucuz** ürünü yan yana gösteriyor. [Marketing Week](https://www.marketingweek.com/tesco-clubcard-data-to-help-people-eat-healthier/), [Tesco PLC](https://www.tescoplc.com/helpful-little-swaps-increases-health-profile-of-baskets/). Spoon Guru ile "Smart Swaps" [vaka](https://www.spoon.guru/resources/case-studies/tesco-helpful-little-swaps/). Clubcard ile her sepete sağlık skoru hesaplıyor ama **bu skor dahili, müşteriye gösterilmiyor** [IAB UK](https://www.iabuk.com/news-article/tesco-creating-health-scores-baskets-using-clubcard-data) | c'nin tek ürünlük, kural tabanlı hali (bütçeyi artırmayan swap) | Hayır | Sepet düzeyinde optimizasyon yok, kişisel kısıt yok |
| 4 | **Sainsbury's / Nectar** (UK) | Alım verisine göre kişisel meyve-sebze hedefi (2020-21 kampanyası) [NutritionInsight](https://www.nutritioninsight.com/news/sainsburys-helps-shoppers-set-personalized-fruit-and-veg-intake-goals-with-nectar-app.html). Yıllık alışveriş özeti "Check you out" (Wrapped tarzı) [Grocery Gazette](https://www.grocerygazette.co.uk/2024/01/09/sainsburys-nectar-round-up/) | a (kısmi), h | Hayır | Kampanya bazlı; yıllık özet sağlık odaklı değil |
| 5 | **Migros – Sağlıklı Yaşam Yolculuğu** (TR) | Money kart alımlarından **3 aylık besin grubu dağılımını önerilen tüketim oranlarıyla** karşılaştırıyor ("Dengeli Beslenme Endeksi", DBE); ihmal edilen besin grubunu gösteriyor, o gruptan **indirimli ürün** öneriyor; vegan/vejetaryen seçeneği var. **~9,4M kişiye ulaştığı**, ~%20 olumlu davranış değişikliği sağladığı söyleniyor (şirket beyanı); DBE 2019'da 70,5'ten 75,7'ye çıkmış. [Migros Kurumsal](https://www.migroskurumsal.com/surdurulebilirlik/calismalarimiz), [Migros Sürdürülebilirlik – SYY](https://surdurulebilirlik.migroskurumsal.com/saglikli-yasam-yolculugu.html) | a (besin grubu düzeyinde), d/c (kısmi: indirimli öneri) | **EVET** | Yalnız Migros alımları. Şeker/tuz/doymuş yağ/NOVA değil besin grubu düzeyinde. Hane üyesi, alerjen kısıtı, bütçe optimizasyonu, enflasyon yok |
| 6 | **Summo+** (UK, Şub 2026) | AI ile fiş tarama (ürün, fiyat, adet, indirim); alışverişe Yeşil/Amber/Kırmızı sağlık skoru; vitamin-mineral tahmini; "fazla işlenmiş gıda / az sebze" örüntüsü; 30-90 günlük harcama trendi; hane karşılaştırma; kiler; ortak liste; 35+ dil; £4,99–74,99 abonelik; henüz yeterli puan yok. [App Store](https://apps.apple.com/gb/app/summo/id6756615656) | a, b (kısmi: harcama trendi var, resmî enflasyonla kıyas yok), g (kısmi) | TR fişi desteği belirtilmemiş | **v2'ye en yakın global ürün.** Optimizasyon, hard alerjen kısıtı, ulusal rehber (TÜBER) ve resmî enflasyon kıyası yok |
| 7 | **HelloCheck** (Telegram botu, 2023) | Fiş fotoğrafı → kalori, şeker, yağ, A–E Health Score, "basket profile", öneri. Dil EN/RU. Toplam geliri 16 $ (TrustMRR, 24.09.2026). [hellocheck.app](https://www.hellocheck.app/), [TrustMRR](https://trustmrr.com/startup/hellocheck-ai-receipt-scanner) | a | Hayır | Ölçek yok. Fikir var, ürün tutmamış |
| 8 | **haul** (ABD) | Fiş → kiler + besin verisi; öğün fotoğrafını alınan ürünlerle eşleştiriyor. [gethaul.app](https://gethaul.app/) | a (kısmi) | Hayır | Kalori tracker ağırlıklı |
| 9 | **Grocery Tracker: Receipt Scan** | Fiş → kategori, bütçe, hane paylaşımı, **"kişisel gıda enflasyonun vs resmî gıda enflasyonu"**, fiyat karşılaştırma, fırsat uyarısı; 6 puan. [App Store](https://apps.apple.com/us/app/grocery-tracker-receipt-scan/id6753721422) | **b (tam)**, g (kısmi) | Dil listesinde Türkçe yok | Sağlık yok |
| 10 | **Ghostflation** | Fiş → kişisel enflasyon oranı, barkodla shrinkflation tespiti, en ucuz market listesi. [ghostflation.app](https://ghostflation.app/how-it-works) | b, g | Belirtilmemiş | Sağlık yok |
| 11 | **Yomio** | Fiş → harcama; "hane enflasyon takibi" rehberi; 5 kişilik hane paylaşımı; 50+ ülke, 10+ dil (Türkçe desteği arama özetinde geçiyor, **doğrulanmadı**). [Yomio blog](https://yomio.app/en/blog/household-inflation-tracker-with-receipts) | b | Belirsiz | Sağlık yok |
| 12 | **InflataCart** (ABD) | Alışveriş listesi + BLS ulusal ortalama fiyatlarla enflasyon. [site](https://inflatacart.pitchinteractive.com/), [SF Chronicle](https://www.sfchronicle.com/personal-finance/article/inflatacart-grocery-inflation-price-tracker-20070212.php) | b (kısmi) | Hayır | Kişisel fiyat değil, ulusal ortalama |
| 13 | **FoodSwitch / GlutenSwitch** (AU, George Institute, 2012) | Barkod → Health Star / trafik ışığı + "switch" önerisi; kullanıcı fotoğrafıyla DB büyütme; GlutenSwitch ile glutensiz tahmin. [George Institute](https://www.georgeinstitute.org/our-research/research-projects/the-foodswitch-app), [healthdirect](https://www.healthdirect.gov.au/foodswitch-app) | d | Hayır | Fiyat, hane, sepet yok |
| 14 | **SwapSHOP** (UK, akademik RCT, 2024) | Barkod + kişisel swap + hedef + geri bildirim; şeker ve doymuş yağda azalma yönünde bulgu var ama tuzda yok; kesin deneme gerektiği söyleniyor. [JMIR mHealth](https://doi.org/10.2196/45854) | d, c (kural tabanlı) | Hayır | Ürün değil. **Akademik referans olarak değerli** |
| 15 | **Sifter – Scan by Diet** (ABD, B2B) | Yüzlerce diyet filtresi, alternatif, ilaç-gıda etkileşimi; perakendeciye beyaz etiket. [siftersolutions](https://www.siftersolutions.com/scan-by-diet) | d | Hayır | Fiş, sepet, bütçe yok |
| 16 | **Instacart Smart Shop + Health Tags** (ABD, 2025) | 30 sağlık etiketi, ~500k ürün, 14 beslenme tercihiyle kişiselleştirilmiş arama. [Instacart IR](https://investors.instacart.com/news-releases/news-release-details/instacart-launches-ai-powered-smart-shop-technology-and-new) | d (kısmi), f (kısmi) | Hayır | Optimizasyon yok |
| 17 | **Cooklist** (ABD, B2B) | Perakendeciye gömülü AI asistan; "Plan 5 dinners under $120. Gluten-free. 2 kid meals." gibi **doğal dil kısıtlarını** sepete çeviriyor. Bu bilgi arama özetinden, sayfa içeriği doğrulanamadı. [cooklist.com](https://cooklist.com/) | **f**, g | Hayır | Geçmiş sepet, sağlık optimizasyonu ve gölge fiyat görülmedi |
| 18 | **ABD zincirlerinin geri çağırma bildirimi** | Walmart, Kroger, Costco, Target, Whole Foods sadakat/üyelik geçmişine göre geri çağırma bildirimi gönderiyor; Costco öncü sayılıyor. [Food Poisoning News, 2025](https://www.foodpoisoningnews.com/do-loyalty-apps-know-about-recalls-on-products-youve-bought/) | **e** | Hayır | Tek zincir, perakendeci içi |
| 19 | **marketfiyati.org.tr** (TR, kamu) | ~50k ürün, 7 zincir, barkodla fiyat; **"sepet oluşturabilir, toplam tutarı görebilir, en uygun marketi seçebilirsiniz."** [Dijipedya](https://dijipedya.com/market-fiyatlari-karsilastirma-uygulamasi/), [AA](https://www.aa.com.tr/tr/podcast/-marketfiyatiorgtr-nedir-nasil-calisir-/3485380) | **g** | **EVET** | Sağlık, hane profili ve geçmiş yok |
| 20 | **Cimri Market / Akakçe Market** (TR) | Liste toplamında en ucuz market, fiyat geçmişi grafiği, fiyat alarmı, barkodla karşılaştırma. [Akakçe Market](https://www.akakce.com/market/), [Herm.io](https://www.herm.io/tr/alisveris-onerileri/turkiyede-online-alisveriste-fiyat-karsilastirma-rehberi-akakce-cimri-epey-ve-pratik-fiyat-takibi/) | g, b (ürün bazlı fiyat geçmişi) | **EVET** | Sağlık yok, kişisel sepet endeksi yok |
| 21 | **Akıllı Fiş / Harcamalar / Harcama Takip & Akıllı Fiş** (TR) | Türk market fişlerini (Şok, BİM, Migros, A101…) okuyan gider takibi. [Akıllı Fiş](https://apps.apple.com/tr/app/ak%C4%B1ll%C4%B1-fi%C5%9F-b%C3%BCt%C3%A7e-takibi/id6761904988?l=tr), [Harcamalar](https://apps.apple.com/hn/app/harcamalar/id6762603210?l=en-GB), [Harcama Takip](https://play.google.com/store/apps/details?id=com.mehmetcetin.harcamatakip&hl=tr) | Fiş OCR altyapısı | **EVET** | Beslenme ve enflasyon yok. **Türk fişi OCR'ının yapılabildiğinin kanıtı** |
| 22 | **Qumpara** (TR) | Fiş fotoğrafı gönder, puan kazan; 9.300+ yorum, 4,5 puan. [App Store](https://apps.apple.com/tr/app/qumpara-fi%C5%9Fini-g%C3%B6nder-kazan/id1179401931?l=tr) | Fiş toplama kanalı | **EVET** | Analiz yok. TR'de "fiş karşılığı ödül" davranışının oturduğunu gösteriyor |
| 23 | **BBC Türkçe kişisel enflasyon hesaplayıcı** (2023) | 6 harcama kategorisine elle girilen tutarlarla TÜİK ve ENAG'a göre kişisel enflasyon. [Cumhuriyet](https://www.cumhuriyet.com.tr/ekonomi/hissedilen-enflasyon-kisisel-enflasyonunuzu-hesaplayin-2066383) | b (kaba, elle girişli) | **EVET** | Ürün/fiş düzeyi yok |
| 24 | **TÜİK / TCMB hesaplayıcıları** | **TÜİK'in resmî "kişisel enflasyon hesaplayıcısı" bulunamadı.** TÜİK'te "TÜFE & Yİ-ÜFE Hesaplama" (tutar dönüştürücü) var [biruni.tuik.gov.tr](https://biruni.tuik.gov.tr/medas/donusum_hesap.zul); TCMB'nin "Enflasyon Hesaplayıcı"sı genel TÜFE ile çalışıyor [TCMB](https://herkesicin.tcmb.gov.tr/wps/wcm/connect/ekonomi/hie/icerik/enflasyon+hesaplayici) | — | — | Kişisel sepet yok |
| 25 | **e-Devlet taklit/tağşiş sorgusu + ÜDTS** (TR) | Marka/parti/üretici sorgusu; 7 ürün grubunda (çay, takviye, alkol, enerji içeceği, bebek maması, bal, bitkisel yağ) SMS/barkodla orijinallik doğrulama. [Dünya](https://www.dunya.com/gundem/taklit-ve-tagsis-urun-listesi-artik-e-devletten-de-goruntulenebilecek-haberi-788763), [Güvenilir Gıda](https://guvenilirgida.tarimorman.gov.tr/GuvenilirGida/gkd/TaklitVeyaTagsisListe1?siteYayinDurumu=True) | e'nin veri kaynağı | **EVET** | Geçmiş alımla kişisel eşleştirme yapan ürün bulunamadı |
| 26 | **Sağlık Bakanlığı "Beslenme Skoru Hesaplayıcı"** (TR, 27 Ağu 2026) | Nutri-Score V2-2023 tabanlı A–E. Paketli gıdada **zorunlu olması planlanıyor**, başlangıç tarihi belli değil. [Gıda Bülteni](https://www.gidabulteni.com/gida/marketteki-gidalarda-beslenme-skoru-donemi-saglikli-gidaya-a-sagliksiz-gidaya-e-harfi/3852) | Ürün puanı (d'nin girdisi) | **EVET** | Ürün düzeyinde. Sepet, hane ve bütçe yok |

**Bulunamayan / doğrulanamayanlar:**
- **"Healthy Basket"** adıyla bir tüketici uygulaması bulunamadı.
- **Fetch, Receipt Hog:** fiş karşılığı ödül uygulamaları. Beslenme özelliği **bulunamadı**. [Fetch](https://fetch.com/blog/smart-shopping/best-apps-for-scanning-digital-receipts), [Receipt Hog vs Fetch](https://visionvix.com/receipt-hog-vs-fetch/)
- **Shopwell / Innit:** 2017'de Innit satın aldı, 2018'de alerji + diyabet/hipertansiyon profilli sürüm çıktı (800k ürün, 2,5M indirme). **Bugün aktif olup olmadığı doğrulanamadı.** [Business Wire 2018](https://www.businesswire.com/news/home/20181008005181/en/Innit-Launches-Upgraded-Shopwell-to-Help-People-Know-Their-Food), [eWeek](https://www.eweek.com/cloud/startup-innit-acquires-food-resource-app-maker-shopwell/)
- **"Sift":** bu adla ürün yok; en yakın eşleşme Sifter (#15).
- **"Nutrify":** aynı adla birden çok kalori uygulaması var. Fiş analizi yapan bir sürüm arama özetinde geçti ama **doğrulanamadı**. [nutrify.app](https://nutrify.app/)
- **Foodvisor, Yuka, Fig vb.:** 01-rakip-pazar.md'de işlendi. Fiş/sepet özellikleri yok.
- **A101, BİM, ŞOK (Cepte ŞOK), CarrefourSA:** uygulamalarında **dijital fiş dökümü ya da sağlık/beslenme özelliği bulunamadı** (arama sonuçları şikâyet ve kampanya sayfalarıydı). Migros Money'de alışveriş geçmişi var. [Migros Money SSS](https://www.money.com.tr/mc/iletisim/sikca-sorulan-sorular/69), [Cepte ŞOK](https://play.google.com/store/apps/details?id=com.positive.ceptesok&hl=en_US)
- **Online sipariş faturası (Getir, Trendyol Go, Migros Hemen vb.):** tüketiciye ürün kalemli e-Arşiv faturası verildiği ve bunun makinece okunabilir indirilebildiği **doğrulanamadı**. v2'nin ikinci girdi kanalı için açık risk.
- **Türkiye'de fişten beslenme analizi yapan bir uygulama bulunamadı.**

### 1.2 Bileşen × piyasa matrisi

| Bileşen | Globalde yapan | TR'de yapan | Doygunluk |
|---|---|---|---|
| **a** Alımdan sepet sağlık karnesi | Kroger, AH, Summo+, HelloCheck, haul | **Migros** (tek zincir, besin grubu düzeyinde) | **Orta-yüksek.** "Çok zincirli + fiş tabanlı + TÜBER eşikli + kişi başı + NOVA" versiyonu TR'de yok |
| **b** Kişisel gıda enflasyonu | Grocery Tracker, Ghostflation, Yomio | Yalnız kaba, elle girişli hesaplayıcı (BBC Türkçe) | Globalde **doymuş**, TR'de fiş tabanlısı yok. Teknik olarak kolay, özgünlük iddiası taşımaz |
| **c** MILP takas + Pareto + gölge fiyat | Tek ürünlük ve kural tabanlı swap var (Tesco, AH, FoodSwitch, SwapSHOP). Sepet düzeyinde kısıtlı optimizasyon **tüketici ürünü olarak bulunamadı**. Akademide LP diyet optimizasyonu çok yaygın | Yok | **Ürün olarak boş, akademik olarak olgun yöntem** |
| **d** Rafta hane üyesi kararı + alternatif | Fig, Yuka, FoodSwitch, Sifter | Ürün Dedektörü, ÇabukBak vb. (bkz. 01) + Bakanlık Beslenme Skoru | **Doymuş.** Yalnız "bu ürün sepet karneni şu kadar değiştirir" kısmı yeni |
| **e** Geriye dönük taklit/tağşiş/geri çağırma | ABD zincirleri (perakendeci içi) | Veri var (e-Devlet, ÜDTS), kişisel eşleştirme yok | TR'de **boş** ama liste parti bazlı olduğu için eşleştirme zor (bkz. 01 §2.2) |
| **f** Doğal dil → kısıt → solver | Cooklist (B2B), LLM yemek planlayıcıları | Bulunamadı | Doğal dilden sepet kurma **doygunlaşıyor**. "LLM kısıtı çıkarır, **deterministik solver** çözer ve sonuç doğrulanabilir" ayrımı savunulabilir |
| **g** Haftalık liste + hangi market | Ghostflation, Summo+ | **marketfiyati, Cimri, Akakçe** | **Doymuş**, TR'de devlet destekli ücretsiz araç var |
| **h** Sepet Wrapped | Nectar "Check you out" | Bulunamadı | Özellik, özgünlük değil |

---

## 2. Hüküm: ne gerçekten özgün, ne doymuş

**Doymuş (özgünlük iddiası kurma):**
- **g** en ucuz market sepeti: TR'de kamu (marketfiyati) + 2 büyük özel oyuncu yapıyor.
- **b** tek başına: fişten kişisel enflasyon globalde en az 3 uygulamada var.
- **d** rafta karar + alternatif: 01'deki tüm barkod rakipleri; artı Bakanlık Beslenme Skoru ürün puanını ücretsiz kamusal mala çeviriyor.
- **a** tek başına: Migros aynı fikri TR'de 2019'dan beri 9M+ kişiye uyguluyor. **Hocaya "TR'de alımdan beslenme analizi yok" denirse Migros örneğiyle çürür.**
- **h**: pazarlama özelliği.

**Gerçekten boş görünen kombinasyon:**
1. **Zincirden bağımsız hane defteri:** fiş + fatura ile birden çok marketten gelen alımlar tek hane sepetinde birleşiyor. Migros'un yapamayacağı şey bu, çünkü Migros yalnız kendi kasasını görüyor.
2. **Sağlık × fiyat aynı defterde:** aynı sepet kalemlerinden hem TÜBER sapması (serbest şeker, tuz, doymuş yağ, NOVA 4 payı) hem Laspeyres tipi kişisel fiyat endeksi hesaplanıyor. Summo+ ikisine yaklaşıyor (sağlık skoru + harcama trendi) ama resmî enflasyon kıyası ve ulusal rehber yok. Grocery Tracker'da enflasyon var, sağlık yok.
3. **Gözlenmiş sepet üzerinde kısıtlı optimizasyon (c):** "en az sapma + bütçe ≤ B + alerjen/çölyak hard + en fazla k değişiklik → sağlık maksimum", Pareto cephesi ve LP ikili değişkeninden **"şekeri 10 g azaltmanın aylık TL maliyeti"**. **Tüketici ürünü olarak bulunamadı.** Tesco ve AH swap'ları tek ürünlük ve sezgisel; akademik LP çalışmaları ise gerçek hane sepetinden değil, temsili sepetten başlıyor ([PLOS One 2016](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0163411), [Frontiers 2018 derleme](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full), [Wiley 2023 sistematik derleme](https://onlinelibrary.wiley.com/doi/10.1155/2023/1271115)).

**Dürüst uyarılar:**
- (c)'nin **matematiği yeni değil**. USDA Thrifty Food Plan 1975'ten beri LP'yle maliyeti minimize edilmiş sağlıklı sepet üretiyor (aynı Frontiers derlemesi). Katkı: yöntemin *gözlenmiş hane sepeti + TR çok marketli fiyat + güvenlik kısıtı* ortamına taşınması ve gölge fiyatın tüketiciye anlaşılır dille sunulması.
- "Bulunamadı" ≠ "yok". Summo+ gibi 2026'da çıkmış, puanı olmayan ürünler bu aramada zor görünüyor. Aynı fikirde sessiz bir uygulama çıkabilir.
- Özgünlüğün değeri **veri kalitesine** bağlı. Fiş satırı → ürün eşleştirmesi (kısaltılmış fiş adları, tartılı ürünler) çözülmezse (a), (b) ve (c) çöker. Türk fişinden **tutar** okuyan uygulamalar var (#21). **Satırı ürün kimliğine ve besin verisine bağlayan** bir TR örneği bulunamadı, asıl teknik risk burada.
- **Migros asıl tehdit ve aynı zamanda referans.** DBE çıktılarını (70,5 → 75,7) "fikrin davranış değiştirdiğinin yerli kanıtı" olarak kullanmak mümkün. Ama Migros verisinin kamuya açık olmadığı, rakamların şirket beyanı olduğu unutulmamalı.

**Öneri (araştırma çıkarımı, karar değil):** Çekirdek = **(a+b) çok zincirli hane defteri** (veri motoru) + **(c) optimizasyon ve gölge fiyat** (entelektüel çekirdek). (e) ucuz ve TR'ye özgü bir artı. (d), (g), (h) ince özellik olarak kalmalı. (f) opsiyonel: LLM yalnız kısıt çıkarımında kullanılmalı, çözümü deterministik solver üretmeli. Ürün puanında kendi skorunu icat etmek yerine **Bakanlık Beslenme Skoru / Nutri-Score V2** kullanılmalı.

---

## 3. Talep kanıtı (kaynaklı, en güncel bulunan)

### 3.1 Fiyat baskısı

| Gösterge | Değer | Kaynak |
|---|---|---|
| TÜİK gıda ve alkolsüz içecekler, **yıllık** | **%33,79 (Ağustos 2026)**; aylık %0,22; yıllık TÜFE'ye **en yüksek katkı: 8,12 puan**. Genel TÜFE yıllık %31,51 | [Capital](https://www.capital.com.tr/haberler/tum-haberler/tuik-2026-yili-agustos-ayi-enflasyon-rakamlarini-acikladi), [SBB](https://www.sbb.gov.tr/2026-yili-agustos-ayi-tuketici-ve-uretici-fiyat-gelismeleri-aciklandi/) |
| TÜİK gıda, 2025 yıl sonu | **%28,31 (Aralık 2025)**; genel TÜFE %30,89 | [Alomaliye](https://www.alomaliye.com/2026/01/05/aralik-2025-tufe-enflasyon-rakamlari/), [TÜİK bülteni](https://data.tuik.gov.tr/Bulten/Index?p=Tuketici-Fiyat-Endeksi-Aralik-2025-58294&dil=1) |
| Alternatif gıda enflasyonu ölçümleri | Türk-İş mutfak enflasyonu (Ankara) 12 ay **%37,90** (Ağu 2026). Birleşik Kamu-İş (64 temel gıda, zincir market) yıllık **%59,5** (Haz 2026). ENAG 2025 genel **%56,14** (TÜİK %30,89) | [Türk-İş](https://www.turkis.org.tr/turk-is-agustos-2026-aclik-ve-yoksulluk-siniri), [Birleşik Kamu-İş](https://birlesikkamuis.org.tr/haber/kamu-is-halkin-enflasyonu-arastirmasi-haziran-2026/gez9be4jwru96q0j4b4u2ifb), [Euronews](https://tr.euronews.com/2026/01/05/2025-enflasyonu-tuik-yuzde-3089-enag-ise-yuzde-5614-acikladi) |
| → Çıkarım | Farklı sepetler için ölçülen gıda enflasyonu %34 ile %60 arasında değişiyor. **"Benim sepetimin enflasyonu ne?" sorusunun cevabı gerçekten haneye göre değişiyor.** (b)'nin gerekçesi bu. | — |
| Türk-İş açlık sınırı | 4 kişilik ailenin sağlıklı, dengeli, yeterli beslenmesi için aylık gıda harcaması **37.388 TL (Ağu 2026)** | [Türk-İş](https://www.turkis.org.tr/turk-is-agustos-2026-aclik-ve-yoksulluk-siniri) |
| Net asgari ücret 2026 | **28.075,50 TL** → açlık sınırı asgari ücretin **~%133'ü** (kendi hesabımız) | [EY](https://www.ey.com/tr_tr/insights/tax/2026-asgari-ucret), [Kolay İK](https://kolayik.com/blog/2026-asgari-ucret-net-hesabi-ve-kesintiler) |

### 3.2 Hane bütçesinde gıda

| Gösterge | Değer | Kaynak |
|---|---|---|
| TÜİK Hanehalkı Bütçe Araştırması 2025: gıda + alkolsüz içecek payı | **%17,3** (konut %29,3 ve ulaştırma %20,5'ten sonra 3.) | [Dünya, 2 Haz 2026](https://www.dunya.com/ekonomik-veriler/tuik-hanehalki-tuketim-verilerini-acikladi-konut-ve-kira-harcamalari-ilk-sirada-haberi-827063) |
| Gelir grubuna göre | En düşük gelirli %20: **%29,2**; en yüksek %20: **%12,4** | aynı kaynak |
| Ipsos Panel Postası (Tem 2026) | Katılımcıların %24'ü gıda-içecek harcamasını kısmış; "gıda harcamamı kıstım" diyenlerin oranı bir yılda %35 artmış. Örneklem büyüklüğü haberde yok | [Gıdatarım](https://gidatarim.com/en-zoru-gidadan-tasarruf-yapmak/) |

### 3.3 Sağlıklı diyetin maliyeti (FAO/Dünya Bankası)

| Gösterge | Değer | Kaynak |
|---|---|---|
| Sağlıklı diyetin günlük maliyeti, TR | **4,77 PPP$ (2024)**. Dünya 4,46, Avrupa ve Orta Asya 4,01. 2017: 3,45 (2021 fiyatları, FAO ve Dünya Bankası 2025 serisi) | [OWID – cost-healthy-diet](https://ourworldindata.org/grapher/cost-healthy-diet) (CSV'den çekildi) |
| Karşılayamayan nüfus, TR | **%6,6 ≈ 5,8 milyon kişi (2024)**. 2019'da %14,4 (12,3M) idi | [OWID – share](https://ourworldindata.org/grapher/share-healthy-diet-unaffordable), [OWID – number](https://ourworldindata.org/grapher/number-healthy-diet-unaffordable) |
| SOFI 2026 (21 Tem 2026 raporu, haber aktarımı) | TR maliyet **4,58 $ (2025)**, dünya 4,28 $. Karşılayamayanlar 2017'de ~%15'ten 2025'te **~%4**'e inmiş. **Ana rapordan doğrulanmadı.** Seriler farklı PPP bazında olduğu için OWID rakamlarıyla doğrudan karşılaştırılamaz | [Bloomberg HT, 22 Tem 2026](https://www.bloomberght.com/fao-saglikli-beslenme-luks-oldu-3783430) |
| Akdeniz diyeti sepeti, TR62 bölgesi (hakemli, 2025) | Aylık 20.930 TL = bölgesel eşdeğer medyan gelirin **%98'i**; en düşük gelir grubunda **%214**, orta gelirde %91,9, yüksek gelirde %37,3; ulusal medyanla (çocuklu çift) %75. Ulusal ortalama gıda harcama payı %18,1 | [MDPI Sustainability 17(24):11254](https://www.mdpi.com/2071-1050/17/24/11254), [ResearchGate](https://www.researchgate.net/publication/398742764_Is_the_Mediterranean_Diet_Affordable_in_Turkiye_A_Household-Level_Cost_Analysis) |
| → **Nüans** | FAO metriği *en ucuz* sağlıklı sepeti ölçüyor ve TR'de karşılayamayan oranı düşük. Gerçekçi ve kültüre uygun (Akdeniz) sepet ise düşük gelirde erişilemez. **Problem "sağlıklı beslenmek imkânsız" değil, "bütçe içinde sağlıklı sepeti kurmak bilgi ve hesap gerektiriyor"**. Bu tam olarak (c)'nin çözdüğü şey | — |

### 3.4 Sağlık yükü

| Gösterge | Değer | Kaynak |
|---|---|---|
| Yetişkin obezite (15+) | **%21,8 (2025)**, 2022'de %20,2. Kadın %24,8, erkek %18,7. Fazla kilolu: erkek %43,1, kadın %32,2 (TÜİK Türkiye Sağlık Araştırması 2025) | [Gazete Oksijen](https://gazeteoksijen.com/saglik/turkiyenin-saglik-karnesi-turkiyede-her-bes-kisiden-biri-obez-277558), [CNN Türk](https://www.cnnturk.com/video/turkiye/tuik-acikladi-turkiyede-obezite-orani-yukseldi-3426755) |
| Çocuk (7-8 yaş, COSI-TUR 2022) | Fazla kilolu **%12,5**, obez **%9,9**, toplam **%22,4**. En yüksek Ege (%25,3) | [Sağlık Bakanlığı COSI-TUR 2022 PDF](https://hsgm.saglik.gov.tr/depo/birimler/saglikli-beslenme-ve-hareketli-hayat-db/Dokumanlar/Kitaplar/Turkiye_Cocukluk_Cagi_Obezite_Arastirmasi_2022.pdf) (s. 104, PDF'ten okundu) |
| Diyabet | 20-79 yaş **%16+, ~9,6M kişi**, Avrupa'da en yüksek (IDF 2025) | 01-rakip-pazar.md §2.5, [Turkish Minute](https://turkishminute.com/2025/12/19/turkey-tops-europe-in-diabetes-rates-as-one-in-six-adults-is-affected/) |
| Hipertansiyon (öz-bildirim) | En sık sağlık sorunları arasında **%16,9** (TÜİK TSA 2025) | [Gazete Oksijen](https://gazeteoksijen.com/saglik/turkiyenin-saglik-karnesi-turkiyede-her-bes-kisiden-biri-obez-277558) |

### 3.5 Ne yeniyor: ultra-işlenmiş gıda, tuz, şeker

| Gösterge | Değer | Kaynak |
|---|---|---|
| Ultra-işlenmiş gıdadan (NOVA 4) enerji, TR | **%30,64** (günlük 1.912 kcal'nin 605 kcal'si). TBSA 2017 verisi, n=12.609, 15+ yaş | [Hacettepe YL tezi, 2022](https://openaccess.hacettepe.edu.tr/items/ef380af4-b32f-4f44-89c4-793feefe987b), atıf: [Food Sci Nutr 2025 / PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12464447/) |
| UPF enerjisinin kaynağı | **Ultra-işlenmiş ekmek: UPF enerjisinin %62,87'si**, ardından yağlar ve hamur işleri. UPF tüketimi kiracılarda, öğrencilerde ve gıda güvencesizliği olanlarda daha yüksek | aynı tez |
| → Tasarım çıkarımı | TR'de NOVA 4 payını **ekmek sınıflaması belirliyor**. Fırın ekmeği ile paketli ekmeğin NOVA'da nasıl sınıflanacağı karnenin sonucunu doğrudan değiştirir. Bir diyetisyenle netleştirilmeli | — |
| Tuz | TBSA 2017: **10,2 g/gün**; SALTürk-II 2012: 15 g/gün. TÜBER üst sınırı: **<5 g/gün** (sodyum <2 g) | [HSGM Tuz Programı](https://hsgm.saglik.gov.tr/depo/birimler/saglikli-beslenme-ve-hareketli-hayat-db/Dokumanlar/Programlar/turkiyede-tuz-tuketiminin-azaltilmasi-programi-2017-2021.pdf), [AA](https://www.aa.com.tr/tr/saglik/turkiyedeki-gunluk-tuz-tuketimi-orani-onerilenden-iki-kat-fazla-/1766556) |
| TÜBER 2022 eşikleri ("sepet karnesi" için) | Serbest/eklenmiş şeker **enerjinin <%10'u** (2000 kcal'de ~50 g), tercihen <%5. Doymuş yağ **<%10** (ideal %7-8). Tuz <5 g. NOVA sınıflaması rehberde anlatılıyor | [TÜBER 2022 tam metin PDF](https://ekutuphane.saglik.gov.tr/Ekutuphane/kitaplar/Turkiye_Beslenme_Rehber_TUBER_2022_min.pdf) (PDF'ten okundu) |

### 3.6 "Sağlıklı beslenme pahalı" algısı

- **Doğrudan, ülke temsili bir TR anketi ("sağlıklı gıda pahalı diyenler %X") bulunamadı.**
- En yakın kanıtlar:
  - TR yetişkinleri (n=5.285, 2023): Food Choice Questionnaire'de **fiyat, lezzetten sonra 2. en önemli seçim motivasyonu** (2,8/4). Hane gıda güvencesizliği seçim motivasyonlarını anlamlı düzeyde düşürüyor. [PMC11660712](https://pmc.ncbi.nlm.nih.gov/articles/PMC11660712/)
  - NIQ 2025 Küresel Sağlık ve Refah Anketi: TR'de **%68** sağlıklı beslenmenin 5 yıl öncesine göre "çok daha önemli" olduğunu söylüyor. [Dünya, 7 Tem 2026](https://www.dunya.com/ekonomi/tuketicinin-saglik-talebi-gidayi-donusturuyor-haberi-831233)
  - PwC "Tüketicinin Sesi 2026" (27 ülke, n=21.808): katılımcıların **yaklaşık dörtte üçü için fiyat-fayda dengesi en önemli kriter**. TR alt kırılımı doğrulanmadı. [Gıda Hattı](https://www.gidahatti.com/haber/28501876/tuketicinin-tercihine-saglik-yon-veriyor)
  - 01'den: TR'de etiketi okuyup kararını değiştirenler %21,8; **fiyat içerikten önce geliyor**. [Gıda Teknolojisi](https://www.gidateknolojisi.com.tr/haber/2022/09/turkiyede-tuketicilerde-etiket-okuma-aliskanliklari)
  - Uzman görüşü, anket değil: enflasyonla beslenme çantasında peynir, yoğurt, yumurta ve meyvenin yerini ucuz ultra-işlenmiş kek, bisküvi ve krakerin aldığı söyleniyor. [Euronews, 7 Eyl 2026](https://tr.euronews.com/2026/09/07/enflasyon-ve-ultra-islenmis-urun-kiskacinda-cocuklar-ogrencinin-beslenme-cantasinda-ne-olm)
- **Kullanılmaması gerekenler:** Gıda Bülteni'ndeki "TR'de sağlıklı gıda 2 kattan fazla pahalı" iddiası kaynaksız; 2 kat rakamı UK Food Foundation "Broken Plate 2025"ten geliyor [Gıda Bülteni](https://www.gidabulteni.com/beslenme/saglikli-beslenmek-2-kat-daha-pahali/3139). Arama özetlerinde geçen "Ekim 2025 anketi, %81,9 harcama kıstı" rakamının kaynağı bulunamadı.
- **Boşluk:** Bu algı TR'de ölçülmemiş. Proje kendi kısa kullanıcı anketini yaparsa (ör. n≥100 hane) hem talep kanıtı hem gereksinim toplama sağlar.

### 3.7 Müdahale etkisine dair kanıt (hocaya "işe yarar mı?" sorusu için)

- Migros SYY: DBE 70,5 → 75,7 (2019), ~%20 olumlu davranış değişikliği. Şirket beyanı. [Migros](https://surdurulebilirlik.migroskurumsal.com/saglikli-yasam-yolculugu.html)
- SwapSHOP fizibilite RCT'si: şeker ve doymuş yağda azalma yönünde bulgu, tuzda yok. [JMIR mHealth 2024](https://doi.org/10.2196/45854)
- Sadakat kartı verisiyle yapılan 15 diyet müdahalesinin derlemesi: sonuçlar karışık; ikame etkisi ve eksik veri sorunları var. [IJPDS derlemesi](https://pmc.ncbi.nlm.nih.gov/articles/PMC13064808/)
- Swap önerisinin çevrim içi mağazada etkisini ölçen randomize deneme: [PLOS Medicine](https://journals.plos.org/plosmedicine/article?id=10.1371%2Fjournal.pmed.1004847). Rakamları okunmadı, sadece varlığı not edildi.

---

## 4. Problem cümlesi önerisi (taslak)

> Türkiye'de haneler tüketim harcamalarının %17,3'ünü, en düşük gelirli %20'lik dilimde ise %29,2'sini gıdaya ayırıyor. Gıda fiyatları Ağustos 2026 itibarıyla yıllık %33,79 artıyor ve enflasyona en büyük katkıyı yapıyor. Farklı sepetlerle yapılan ölçümler (%34–60) her hanenin gıda enflasyonunun farklı olduğunu gösteriyor. Aynı dönemde 15 yaş üstü nüfusun %21,8'i obez, 7-8 yaş çocukların %22,4'ü fazla kilolu ya da obez, yetişkinlerin yaklaşık altıda biri diyabetli. Alınan enerjinin yaklaşık %31'i ultra-işlenmiş gıdalardan geliyor ve tuz tüketimi Türkiye Beslenme Rehberi'nin önerdiği üst sınırın iki katı. Sorun, sağlıklı beslenmenin çoğu hane için imkânsız olması değil: FAO'ya göre en ucuz sağlıklı diyeti karşılayamayanlar nüfusun küçük bir kısmı. Sorun, hanelerin bütçe baskısı altında gıda kararlarını ürün ürün ve fiyat öncelikli vermesi, sepetlerinin bütünü hakkında ölçülebilir bir geri bildirim almaması. Mevcut araçlar bu kararı ya tek ürün düzeyinde sağlık puanıyla (barkod uygulamaları, Sağlık Bakanlığı Beslenme Skoru), ya tek bir zincirin sadakat verisiyle (Migros), ya da sağlıktan bağımsız fiyat karşılaştırmasıyla (marketfiyati.org.tr, Cimri, Akakçe) destekliyor. Hiçbiri hanenin farklı marketlerden gerçekte aldığı sepeti birleştirip şu soruyu cevaplamıyor: **"Bu bütçeyle ve bu güvenlik kısıtlarıyla (alerji, çölyak) sepetimi en az değişiklikle ne kadar sağlıklı yapabilirim ve bunun bana aylık maliyeti kaç TL?"**

(Kısa versiyon, tek cümle: *Türk haneleri, yıllık %30'u aşan gıda enflasyonu altında, çok marketten yaptıkları alışverişin bütününün sağlık ve maliyet etkisini göremiyor; bu yüzden bütçelerini aşmadan ve güvenlik kısıtlarını çiğnemeden sepetlerini iyileştirecek somut, ölçülebilir bir yol bulamıyor.*)

---

## 5. Levent'e açık sorular (bu araştırmadan doğan)

1. **Migros ile konumlanma:** "Migros'un tek zincirle yaptığını zincirden bağımsız ve optimizasyonlu yapıyoruz" çerçevesi ekibe uygun mu? Hoca Migros'u biliyor mu?
2. **Veri motoru riski:** Fiş satırını ürüne eşleştirme TR'de kanıtlanmamış. İlk sprintte bunun için bir fizibilite prototipi (ör. 50 gerçek fiş, eşleşme oranı) yapılabilir mi?
3. **Online sipariş faturası kanalı:** Ekipte Getir, Trendyol Go ya da Migros Hemen faturasının ürün kalemli indirilip indirilemediğini kendi hesabından kontrol edebilecek biri var mı?
4. **Ürün puanı:** Kendi skorumuz yerine Bakanlık Beslenme Skoru / Nutri-Score V2 kullanmak kabul mü?
5. **Talep anketi:** "Sağlıklı beslenme pahalı" algısı TR'de ölçülmemiş. Küçük bir ekip anketi yapılabilir mi, kapsama alınsın mı?
6. **NOVA ve ekmek:** TR'de UPF enerjisinin ~%63'ü ekmekten geliyor. Karnenin NOVA hesabını bir diyetisyen/akademisyenle doğrulama imkânı var mı?
