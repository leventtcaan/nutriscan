---
title: 01 — Rakip ve pazar araştırması (NutriScan)
tarih: 2026-09-24
durum: HAM
---

> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24.**
> Web araması + birkaç doğrudan API sorgusu. Rakamlar kaynağıyla birlikte; bulunamayan her şey "bulunamadı" olarak işaretli.
> Reddit bu ortamdan erişilemedi (crawler engeli); şikâyet analizi App Store listeleri, inceleme toplayıcıları ve bağımsız testlerle yapıldı.

---

## 0. TL;DR

- **Çekirdek fikir (barkod + alerji/diyet profili + güvenli/riskli dönüt) özgün değil.** Dünyada Fig, Yuka Premium, CodeCheck, Fooducate bunu yapıyor. **Türkiye'de de artık yapılıyor:** Ürün Dedektörü (alerji, hamilelik, helal, çölyak profili), ÇabukBak (vegan/helal/glutensiz tercihleri, ~80k barkod), Gluten Tarayıcı (2015'ten beri, ~100k ürün).
- **Asıl boşluk özellik değil, veri.** Open Food Facts'te (OFF) Türkiye'de **11.411 ürün var, ingredients'ı tamamlanmış olan yalnızca 2.832 (~%25).** Karşılaştırma için Fransa 1.269.160, Almanya 427.235. Yalnızca OFF'a dayanan bir uygulama Türkiye'de ürünlerin çoğunda "bulunamadı / içerik yok" der. (Kendi API sorgumuz, 2026-09-24.)
- **Savunulabilir özgünlük** şu kesişimde: Türkçe etiket OCR ile veri boşluğunu kapatma (ve OFF'a geri besleme) + "may contain"/eksik veri için dürüst **"bilinmiyor"** durumu + hane (aile) profilleri + hastalığa özgü kurallar (diyabet, hipertansiyon) + alışveriş geçmişinden hane düzeyinde analiz + marketfiyati.org.tr fiyatlarıyla bütçe-duyarlı alternatif.
- **Doymuş alanlar:** genel sağlık puanı (Nutri-Score/katkı maddesi puanı), E-kod/helal sorgulama, kalori takibi, "AI ile etiket fotoğrafı analiz" eden jenerik uygulamalar (2025-26'da çok sayıda yeni uygulama çıktı).

---

## 1. Global rakipler

| Uygulama | Ne yapıyor | Kişiselleştirme (alerji/hastalık) | İş modeli | Kullanıcı / rating | Türkiye'de? | Zayıf yanı |
|---|---|---|---|---|---|---|
| **Yuka** (FR) | Gıda + kozmetik barkod, 0-100 puan (beslenme, katkı, organik) | **Premium'da** gluten, laktoz, sülfit, soya, palm yağı + vejetaryen/vegan/domuzsuz uyarıları. **"Traces"/"may contain" dikkate alınmıyor** | Freemium, yıllık ~10-20 $/€ | 80-85M kullanıcı, App Store 4,8 (100K rating), 6M ürün (4M gıda) | **Hayır** (15 ülke listesinde yok) | Alerji listesi dar ve paywall arkasında; puanlama yöntemi bilimsel olarak eleştiriliyor; mükerrer/eksik ürün kayıtları |
| **Fig** (US) | Alerji/diyet odaklı barkod tarayıcı | **Var, en güçlüsü:** 2.800+ kısıt/alerji, çoklu profil ("Multiple Figs"), restoran | Freemium, Fig+ 5,99-69,99 $ | 1M+ üye, App Store 4,7 (16K+ rating) | **Hayır** (esas olarak ABD) | Bağımsız testte shared-line/cross-contact bilgisini kaçırdı; çoklu profil ve sınırsız tarama ücretli |
| **Open Food Facts app** | Açık, crowdsourced veritabanı; Nutri-Score, NOVA, Eco-Score | Temel tercihler (alerjen filtresi) var, hastalık profili yok | Kâr amacı gütmeyen, ücretsiz | ~4M ürün, 150+ ülke; justuseapp 4,4 | Evet, ama TR verisi çok zayıf (bkz. §2.3) | Tarayıcı hataları, yavaşlık, Fransa dışında eksik veri |
| **Fooducate** (US) | Harf notu, kalori/besin takibi | Premium'da gluten/alerjen, diyabet, hamilelik, kolesterol, IBS vb. | Freemium, lifetime ~34,97 $ (2026) | Bulunamadı | Resmi olarak hayır | ABD odaklı veri; tracker ağırlıklı |
| **CodeCheck** (CH/DE) | Gıda + kozmetik; DAAB, Greenpeace gibi uzman kaynaklı değerlendirme | Vegan, vejetaryen, glutensiz, laktozsuz uyarıları | Freemium + reklam | 2019'da 5M+ indirme; güncel rakam bulunamadı | Hayır (DE, AT, CH, UK, US, NL) | DACH dışında veri zayıf |
| **Spoon Guru** (UK) | **B2B**: perakendecilere diyet/alerji arama-filtre motoru (Tesco vb.) | 1000+ diyet etiketi (perakendeci katalogunda) | B2B lisans; ~9,2M $ yatırım | Tesco'da bazı aramalarda dönüşümde %500'e varan artış (şirket iddiası) | Hayır | Tüketici uygulaması değil; perakendeciye bağımlı |
| **Foodvisor** (FR) | AI fotoğrafla kalori, barkod | Diyet hedefi; alerji odaklı değil | Freemium abonelik | 15M+ kullanıcı (3. taraf inceleme) | Store'da var, TR verisi bulunamadı | Kalori tracker; alerji güvenliği yok |
| **MyFitnessPal** (US) | Kalori/makro takibi, 20M girdi | Alerji yok | Premium ~80-100 $/yıl | Çok büyük | Evet (genel) | Barkod 2022'de paywall'a alındı; 2026'daki durum kaynaklar arasında çelişkili |
| **Bobby Approved** (US) | Influencer kaynaklı "temiz içerik" onayı | Sınırlı | Freemium | Google Play 4,8 (19,4K review) | Hayır | ABD ürünleri, influencer kriterleri |
| **Spokin** (US) | Alerji topluluğu: güvenli ürün, restoran, seyahat | Alerji + çölyak profili | Ücretsiz/topluluk | Bulunamadı | Hayır | Tarayıcı değil, keşif/topluluk |
| **El CoCo / GoCoCo** (ES) | Nutri-Score + NOVA, crowdsourced | Bulunamadı | Ücretsiz | 2019'da 15K+ ürün; güncel rakam bulunamadı | Hayır | İspanya'ya özgü |
| **Kroger OptUP** (US) | **Sadakat kartı ile hane sepetinin sağlık puanı** | Genel sağlık; alerji yok | Perakendeci uygulaması | Bulunamadı | Hayır | Tek zincire bağlı. *Önemli:* "alışveriş takibi" fikri ABD'de perakendeci düzeyinde var |
| **HelloCheck** | Fiş fotoğrafından ürün çıkarma + A-E sağlık puanı | Bulunamadı | Bulunamadı | Bulunamadı | Bulunamadı | Fiş OCR fikri var |
| **Jenerik "AI allergen scanner"lar** (Food Allergen Scanner, WellValet, Subfy, ScanGredients, VegVisor, WhatsVegan…) | Etiket fotoğrafı → OCR/LLM → alerjen | Var (çoğu) | Çoğu abonelik | Küçük | App Store'da erişilebilir, TR odaklı değil | Barkod DB'si yok, doğrulama yok, kalıcı veri birikimi yok |
| **ScanAvert / Allergy Scanner / Picky / Veganly** | — | — | — | — | — | **Bu adlarla kesin eşleşme bulunamadı.** "Picky?" alerji paylaşım uygulaması (tarayıcı değil); "Veganly" yerine çok sayıda vegan tarayıcı var |

Kaynaklar: Yuka [Play](https://play.google.com/store/apps/details?id=io.yuka.android&hl=en_US), [App Store](https://apps.apple.com/us/app/yuka-food-cosmetic-scanner/id1092799236), [Yardım: food preferences](https://help.yuka.io/l/en/article/qzr8gkygvp-food-preferences), [Yardım: ülkeler](https://help.yuka.io/l/en/article/v7vndx8ivc-availability-countries), [Fiyat](https://help.yuka.io/l/en/article/hkzw2hkj5w-cost-membership), [Scandit vaka](https://www.scandit.com/resources/case-studies/yuka/) · Fig [App Store](https://apps.apple.com/us/app/fig-food-scanner-guide/id1564434726), [foodisgood.com](https://foodisgood.com/app/), [SnackSafely testi](https://snacksafely.com/2023/09/advisory-dont-use-the-fig-scanner-app-if-the-potential-for-allergen-cross-contact-concerns-you/) · OFF [Wikipedia](https://en.wikipedia.org/wiki/Open_Food_Facts), [justuseapp](https://justuseapp.com/en/app/588797948/open-food-facts/reviews) · Fooducate [Zendesk](https://fooducate.zendesk.com/hc/en-us/articles/8287618975131-Fooducate-Premium-Features), [MWM](https://mwm.ai/apps/fooducate-nutrition-coach/398436747) · CodeCheck [Wikipedia](https://en.wikipedia.org/wiki/CodeCheck) · Spoon Guru [The Grocer](https://www.thegrocer.co.uk/news/tesco-signs-up-spoon-guru-to-help-with-special-diet-searches/552795.article), [Retail Insight](https://www.retail-insight-network.com/news/newstesco-spoon-guru-partner-to-help-customers-with-specific-dietary-needs-5814760/), [Tracxn](https://tracxn.com/d/companies/spoon-guru/__XXiSpXQrrREsi2rTsBCR7LL9lS0IFCKhNLlnpQCP8OI/funding-and-investors) · Foodvisor [Garage Gym Reviews](https://www.garagegymreviews.com/foodvisor-review) · MyFitnessPal [XDA](https://www.xda-developers.com/myfitnesspals-barcode-scanner-behind-a-paywall/), [Nutrola timeline](https://nutrola.app/en/blog/why-did-myfitnesspal-remove-barcode-scanning) · Bobby Approved [Play](https://play.google.com/store/apps/details?id=com.bobbyapproved&hl=en_US) · Spokin [spokin.com](https://www.spokin.com/about-the-spokin-app) · El CoCo [indisa.es](https://www.indisa.es/al-dia/coco-nueva-app-gratuita-detecta-ultraprocesados-ayuda-encontrar) · Kroger OptUP [kroger.com](https://www.kroger.com/health/nutrition/optup) · HelloCheck [hellocheck.app](https://www.hellocheck.app/) · 2026 sıralama [nutrifyai](https://www.nutrifyai.app/blog/best-food-scanner-apps-2026) · AI tarayıcılar [Food Allergen Scanner](https://apps.apple.com/us/app/food-allergen-scanner/id6738454688), [WellValet](https://www.wellvalet.com/allergen-scanner-app.html), [Subfy](https://subfy.app/) · Picky [alittlepicky.com](https://www.alittlepicky.com)

**Çıkarım:** En yakın global muadil **Fig**'dir (çoklu profil + 2.800 kısıt). Fig ve Yuka Türkiye'de yok; bu "Türkiye'de boşluk var" demek değil, "global devler buraya veri olmadığı için gelmemiş" demek olabilir.

---

## 2. Türkiye

### 2.1 Doğrudan rakipler (Türkiye'de, Türkçe)

| Uygulama | Ne yapıyor | Kişiselleştirme | Veri | İş modeli | Ölçek | Zayıf yanı |
|---|---|---|---|---|---|---|
| **Ürün Dedektörü** | Barkod veya etiket fotoğrafı → katkı, risk, kişisel uyarı (gıda + kozmetik) | **Alerji, hamilelik, helal, çölyak, cilt tipi** | EFSA/AB mevzuatına dayalı 500+ katkı/INCI kaydı | Ücretsiz + Pro abonelik (kişisel profil analizi Pro'da) | Kullanıcı sayısı bulunamadı | Barkod ürün DB büyüklüğü belirsiz; aile profili/alışveriş takibi yok |
| **ÇabukBak** | Barkod → AI ile içerik analizi, puan | Vegan, vejetaryen, helal, glutensiz, alkolsüz vb. | ~80.000 barkod, ~23.000 içerik tanımı | Tamamen ücretsiz | "Günde yüzlerce" yeni kullanıcı (şirket beyanı) | Hastalık profili yok; aile/alışveriş takibi yok |
| **İçerik Tara** (gidakontrol.com) | Kamera + OCR ile etiket analizi, E-kod DB | Genel alerjen uyarısı; kişisel profil belirtilmemiş | OCR + E-kod DB | Bulunamadı | Bulunamadı | Barkod DB belirsiz |
| **Besin App** | Barkod/isimle arama, besin skoru, 5 ürüne kadar karşılaştırma | Kişisel profil yok (sitede belirtilmemiş) | TR marketlerinden 12.000+ ürün (site; bir haberde 3.000+) | Ücretsiz, reklamsız | Bulunamadı | Kişiselleştirme yok |
| **FoodCheck** | Barkod → içerik/etiket görüntüleme, offline cache | Yok | "Açık kaynaklar" (büyük ihtimalle OFF) | Ücretsiz + reklam | Henüz rating yok | Bireysel geliştirici, profil yok |
| **Gıda Analizi: İçerik Tara (Labelscan)** | Trafik ışığı, gizli şeker/tuz, alternatif öneri | Yok | Bulunamadı | Haftalık ₺199,99 / yıllık ₺1.999,99 | 1 değerlendirme (Kasım 2025 çıkış) | Pahalı, profil yok |
| **Gluten Tarayıcı** | Barkod → glutensiz mi | Sadece gluten | ~100.000 ürün, ~15.000 üye, ~2M sorgu, ~300 mağaza | Ücretsiz; Ankara Çölyak Derneği ile | 2015'ten beri aktif | Tek alerjen; UI/altyapı eski olabilir (doğrulanmadı) |
| **Glutensiz Nokta** | Çölyak aile girişimi; glutensiz online market + uygulama | Gluten | Sertifikalı yüzlerce ürün | E-ticaret | Bulunamadı | Tarayıcı değil, market |
| **Helal Tarayıcı / HalalFoodScan / Helal Gıda: Katkı Maddeleri** | Barkod/E-kod → helal/şüpheli/haram | Helal | E-kod DB | Freemium (Helal Tarayıcı ₺99,99/hafta – ₺1.299,99/yıl) | Çok az rating | Tek boyut |
| **Diyetkolik** | Kalori takibi, barkodla besin değeri, **online diyetisyen** | Diyet hedefi; alerji güvenliği odaklı değil | Kendi DB | Freemium + diyetisyen ücretli | "Türkiye'nin en çok kullanılan diyet platformu" iddiası; rakam bulunamadı | "Diyetisyen paneli" fikri burada kısmen var |

Kaynaklar: [urundedektoru.com](https://urundedektoru.com/) · [cabukbak.com](https://cabukbak.com/), [ÇabukBak App Store](https://apps.apple.com/us/app/-/id6756517558) · [gidakontrol.com](https://www.gidakontrol.com/) · [besin.app](https://besin.app/) · [FoodCheck App Store](https://apps.apple.com/tr/app/foodcheck-g%C4%B1da-analiz/id6757622854?l=tr) · [Gıda Analizi App Store](https://apps.apple.com/tr/app/g%C4%B1da-analizi-i-%C3%A7erik-tara/id6755642006?l=tr) · [glutentarayici.com](https://glutentarayici.com/), [Yeni Ankara](https://www.yeniankara.com.tr/guncel/colyaklilar-gluten-tarayici-ile-alisverise-hazir-67670) · [Glutensiz Nokta](https://apps.apple.com/tr/app/glutensiz-nokta/id1465466345) · [Helal Tarayıcı](https://apps.apple.com/tr/app/helal-taray%C4%B1c%C4%B1-barkod/id6747710371?l=tr), [HalalFoodScan](https://apps.apple.com/tr/app/halalfoodscan-helal-taray%C4%B1c%C4%B1/id1473427574?l=tr), [Helal Gıda](https://play.google.com/store/apps/details?id=com.gmsapp.halalfood&hl=tr&gl=US) · [Diyetkolik](https://apps.apple.com/tr/app/diyetkolik-online-diyet/id558076089?l=tr)

**Çıkarım:** 2025-26'da Türkiye'de "barkod/etiket + AI analiz" uygulaması patlaması olmuş; çoğu tek geliştirici, küçük ölçekli, rating'i neredeyse yok. **Kimse pazarı domine etmiyor**, ama "ilk ve tek" iddiası artık yapılamaz. Ürün Dedektörü özellik seti olarak NutriScan'in onboarding fikrine en yakın olanı.

### 2.2 Dolaylı oyuncular / veri kaynakları

| Kaynak | Ne sunuyor | NutriScan için anlamı |
|---|---|---|
| **Migros Sanal Market** (ve benzeri market uygulamaları) | Glutensiz/laktozsuz kategori sayfaları; ürün sayfalarında "içindekiler" ve "iz miktarda … içerebilir" metni | Kişisel profil ve tarayıcı yok; ama etiket metninin dijital olarak bir yerde var olduğunu gösteriyor. Scraping ToS/hukuk riski taşır |
| **marketfiyati.org.tr** (TÜBİTAK + Sanayi ve Teknoloji / Ticaret Bakanlığı + TCMB) | 7 zincirde (A101, BİM, CarrefourSA, Hakmar, Migros, Tarım Kredi, ŞOK) ~50.000 ürün fiyatı, mobilde barkodla fiyat karşılaştırma | **Resmî public API yok.** GitHub'da `api.marketfiyati.org.tr/api/v2` kullanan gayriresmî MCP projeleri var (eğitim amaçlı). Kullanıcılar kategorizasyonun zayıf olduğunu söylüyor |
| **Güvenilir Gıda – taklit/tağşiş listesi** (Tarım ve Orman Bakanlığı) | Taklit/tağşiş tespit edilen ürünlerin marka + parti listesi; 2025 sonunda toplam 2.345 ürün | Liste **parti (lot) düzeyinde**, barkod düzeyinde değil → otomatik eşleşme zor; ama "bu marka/ürün tipi listede" uyarısı Türkiye'ye özgü, rakiplerde görülmedi |
| **GS1 Türkiye – Verified by GS1** | Barkod → firma/ürün kimliği doğrulama; kurumsal API | İçerik/alerjen vermez, ama barkodun gerçek sahibini/ürün adını doğrulamak için kullanılabilir. API şartları için GS1 TR'ye başvuru gerekiyor |

Kaynaklar: [Migros glutensiz](https://www.migros.com.tr/glutensiz-urunler-c-462), [Migros Schar ürün sayfası](https://www.migros.com.tr/schar-pan-multigrano-glutensiz-ekmek-250g-p-8b0a53) · [TÜBİTAK duyurusu](https://tubitak.gov.tr/tr/haber/zincir-market-fiyatlarina-aninda-erisimin-onu-acildi), [Webrazzi](https://webrazzi.com/2025/02/11/sanayi-ve-teknoloji-bakanligi-ndan-market-fiyatlarini-karsilastiran-platform-market-fiyati/), [TRT Haber](https://www.trthaber.com/haber/ekonomi/tek-tikla-market-fiyati-donemi-50-bin-urun-karsilastiriliyor-934814.html), [yibudak/marketfiyati_mcp](https://github.com/yibudak/marketfiyati_mcp), [aigile-era/market-mcp-serkan](https://github.com/aigile-era/market-mcp-serkan), [X – API eksikliği yorumu](https://x.com/uygunbodur/status/1889568880693006698) · [Güvenilir Gıda listesi](https://guvenilirgida.tarimorman.gov.tr/GuvenilirGida/gkd/TaklitVeyaTagsis), [Dünya – 2.345 ürün](https://www.dunya.com/gundem/taklit-ve-tagsiste-rekor-liste-2-bin-345-urun-ifsa-edildi-haberi-822226) · [Verified by GS1 TR](https://gs1tr.org/view/verified/search.php), [TOBB haberi](https://tobb.org.tr/Sayfalar/Detay.php?rid=10738&lst=Haberler)

### 2.3 Veri gerçeği: Open Food Facts Türkiye kapsamı (kendi sorgumuz)

OFF Search API v2, `countries_tags=en:<ülke>`, 2026-09-24:

| Sorgu | Ürün sayısı |
|---|---|
| Türkiye, toplam | **11.411** |
| Türkiye, `ingredients-completed` | **2.832 (~%24,8)** |
| Türkiye, `ingredients-to-be-completed` | 8.579 |
| Türkiye, `nutrition-facts-completed` | 5.937 (~%52) |
| Türkiye, fotoğraf yüklenmiş | 9.479 |
| Türkiye, `traces_tags=en:gluten` | 271 |
| Fransa, toplam | 1.269.160 |
| Almanya, toplam | 427.235 |

Endpoint: `https://world.openfoodfacts.org/api/v2/search?countries_tags=en:turkey&page_size=1&fields=code` (+ `states_tags=...`). API ara sıra 503 döndü; rakamlar tek anlık görüntüdür.

**Anlamı:** Türkiye'de OFF, yerli rakiplerin kendi DB'lerinden (Gluten Tarayıcı ~100k, ÇabukBak ~80k, marketfiyati ~50k fiyat kaydı) küçük. **İçerik listesi olmadan alerji kararı verilemez**; yani OFF'u tek kaynak olarak alan bir NutriScan, Türkiye'de taranan ürünlerin büyük kısmında güvenilir karar veremez. Bu hem en büyük risk hem de en savunulabilir özgünlük fırsatı (bkz. §4).

### 2.4 Mevzuat notları (ürün tasarımını doğrudan etkiliyor)

- **"İz miktarda … içerebilir" (precautionary allergen labelling, PAL) Türkiye'de zorunlu değil**; içerikteki alerjenlerin vurgulanarak yazılması zorunlu. Yani PAL'in yokluğu "güvenli" demek değil. [Besin Alerjisi Derneği](https://besinalerjisi.org.tr/alerjen-etiketleme-kurallari/), [Türk Gıda Kodeksi Etiketleme Yönetmeliği – Resmî Gazete 2017](https://www.resmigazete.gov.tr/eskiler/2017/01/20170126M1-6.htm), [Alerji ve Astım Derneği](https://alerjiastim.org.tr/alerjen-etiketleme-kurallari-ve-bilinmesi-gerekenler/)
- **KVKK md. 6:** sağlık verisi (alerji, diyabet, hamilelik) özel nitelikli kişisel veri; açık rıza + erişim kısıtı + loglama gerekir. Canlıya çıkacak bir ürün için bu bir mimari gereksinim. [KVKK – Özel Nitelikli Kişisel Veriler](https://www.kvkk.gov.tr/Icerik/2051/Ozel-Nitelikli-Kisisel-Veriler)

### 2.5 Hedef kitle büyüklüğü (kaynaklı)

| Durum | Rakam | Kaynak / not |
|---|---|---|
| **Diyabet** | 20-79 yaş yetişkinlerin %16'sından fazlası, **~9,6 milyon kişi**; Avrupa'da en yüksek | IDF Diabetes Atlas 2025 (11. baskı), [Turkish Minute haberi](https://turkishminute.com/2025/12/19/turkey-tops-europe-in-diabetes-rates-as-one-in-six-adults-is-affected/), [IDF Türkiye sayfası](https://diabetesatlas.org/data-by-location/country/trkiye/) (doğrudan açılamadı) |
| Diyabet (öz-bildirim) | 2008'de %6,6 → 2022'de **%13,2** (Türkiye Sağlık Araştırması, n=120.044) | [Endocrine 2026, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13046645/) |
| Diyabet (TURDEP-II, 2010) | %16,5 (%7,5 yeni tanı), ~6,5 milyon | [Eur J Epidemiol 2013](https://link.springer.com/article/10.1007/s10654-013-9771-5) |
| **Hipertansiyon** | %31,8 (kadın %36,1, erkek %27,5) — **2012 verisi**, güncel ulusal çalışma bulunamadı | [PatenT2 – Türk Hipertansiyon Derneği](https://www.turkhipertansiyon.org/prevelans_calismasi_2.php) |
| **Çölyak** | Çocuklarda biyopsi doğrulamalı **%0,47** (20.190 öğrenci, 62 il, 2006-08) | [Dalgıç ve ark., Am J Gastroenterol 2011](https://pubmed.ncbi.nlm.nih.gov/21691340/) |
| Çölyak (tahmin) | 250.000-750.000 hasta, **yalnızca ~%10'u tanılı** (25-75 bin) | [CNN Türk, 2023, İl Sağlık Müdürü beyanı](https://www.cnnturk.com/saglik/turkiyede-25-bin-ile-75-bin-arasinda-tani-almis-hasta-beklenmektedir-2005228) — resmî istatistik değil |
| **Gıda alerjisi (IgE, doğrulanmış)** | Ergenlerde %0,15 (Ankara); 6-9 yaş %0,80 (Doğu Karadeniz). Sık alerjenler: yumurta, inek sütü, **fındık**, yer fıstığı, ceviz, **mercimek** | [Kaya 2013, PAI](https://ncbi.nlm.nih.gov/pubmed/23772635), [Orhan 2009](https://pubmed.ncbi.nlm.nih.gov/19400894/), [Turk J Pediatr](https://turkjpediatr.org/article/view/333) |
| Yetişkin gıda alerjisi | Ulusal temsilî rakam **bulunamadı** (%14 rakamı yalnızca mevsimsel rinitli 774 hastalık alt grupta) | [ResearchGate](https://www.researchgate.net/publication/235660004_Adults_Food_Allergies_in_Mediterranean_region_of_Turkey) |
| **Laktoz intoleransı** | "%70-80" sık dolaşan rakam; ancak bu **laktaz yetmezliği (genetik)**, semptomatik intolerans değil. Güvenilir ulusal çalışma **bulunamadı** — sunumda kullanma | [Cumhuriyet](https://www.cumhuriyet.com.tr/is-dunyasi/turkiyenin-en-az-70inde-laktoz-intoleransi-var-2172601), [ResearchGate derleme](https://www.researchgate.net/publication/335859159_Laktoz_Intoleransin_Prevalansi_Teshisi_ve_Laktozsuz_Beslenme_Tavsiyeleri) |
| **Hamilelik** (vekil) | 2025'te 895.374 canlı doğum → yılda ~0,9M gebelik (düşükler hariç, alt sınır) | [TÜİK 2025 haberi](https://www.haberler.com/ekonomi/dogum-istatistikleri-19867339-haberi/) |
| **Vegan/vejetaryen** | Güvenilir sayı **bulunamadı** | — |

Kullanıcı davranışı: Türkiye'de etiketi okuyup satın alma kararını değiştirme oranı %21,8 (Ankara Üniv. tezi); tüketiciyi en çok karıştıran bileşen E-kodlar; fiyat, içerikten önce geliyor. [Gıda Teknolojisi 2022](https://www.gidateknolojisi.com.tr/haber/2022/09/turkiyede-tuketicilerde-etiket-okuma-aliskanliklari)

**Çıkarım:** Pazar büyüklüğü argümanı **diyabet** üzerinden çok güçlü (9,6M, Avrupa'nın en yükseği). Çölyak küçük ama tanı oranı düşük ve topluluğu örgütlü (dernekler, pilot kullanıcı kaynağı). "Fiyat önce gelir" bulgusu bütçe-duyarlı öneri fikrini destekliyor.

---

## 3. Kullanıcı şikâyetleri (tekrar eden temalar)

Reddit erişilemedi; kaynaklar App Store/Play listeleri, justuseapp toplamaları, bağımsız testler ve basın.

1. **Ürün bulunamıyor / eksik veri.** OFF: "Fransız ürünlerinde iyi, ABD'de değil"; tarama sonuç vermiyor. Yuka: özel/sağlık ürünleri indekslenmemiş, kullanıcı veri girmek zorunda kalıyor, ücretli kullanıcılar bile bunu yapmak zorunda. [OFF justuseapp](https://justuseapp.com/en/app/588797948/open-food-facts/reviews), [Yuka justuseapp](https://justuseapp.com/en/app/1092799236/yuka-food-cosmetic-scanner/reviews)
2. **Yanlış/çelişkili veri.** Yuka'da mükerrer ürünler farklı puanlarla; puanlar zamanla değişiyor. [Yuka justuseapp](https://justuseapp.com/en/app/1092799236/yuka-food-cosmetic-scanner/reviews)
3. **"May contain" / cross-contact eksikliği (alerji için en kritik).** Yuka traces'i resmen dikkate almıyor. SnackSafely bağımsız testinde Fig, üreticinin shared-line alerjen bildirdiği 3 üründe risk göstermedi. Kök neden: PAL gönüllü, etiket DB'si üretim hattını bilmez. [Yuka yardım](https://help.yuka.io/l/en/article/qzr8gkygvp-food-preferences), [SnackSafely](https://snacksafely.com/2023/09/advisory-dont-use-the-fig-scanner-app-if-the-potential-for-allergen-cross-contact-concerns-you/), [SnackSafely 2014](https://snacksafely.com/2014/12/barcode-scanning-apps-what-they-dont-know-can-hurt-you/). Alerjik tüketicilerin %43'ü ürün bilgisine telefonla tarayarak ulaşmayı tercih ettiğini söylüyor. [PMC – PAL çalışması](https://pmc.ncbi.nlm.nih.gov/articles/PMC5628481/)
4. **Paywall.** Yuka'da alerji uyarıları Premium'da; Fig'de çoklu profil/sınırsız tarama Fig+'da; MyFitnessPal barkodu 2022'de ücretliye aldı. [XDA](https://www.xda-developers.com/myfitnesspals-barcode-scanner-behind-a-paywall/)
5. **Puanlama bilimsel değil / aşırı basit.** Kalori ve yağ üzerinden cezalandırma, porsiyon bilgisi yok, "pseudoscience" eleştirisi. [Substack – Unbiased Science](https://theunbiasedscipod.substack.com/p/that-app-scoring-your-groceries-we), [NPR 2025](https://www.npr.org/2025/05/26/nx-s1-5391915/phone-apps-food-nutrition-health)
6. **Allerjiye değil intoleransa uymuyor / aşırı kısıtlama.** Fig incelemeleri: tercihlere rağmen çok ürün uygunsuz işaretleniyor. [Olive – Fig reviews](https://www.oliveapp.com/blogs/fig-app-reviews)
7. **Dil / ülke desteği.** Yuka 6 dil, 15 ülke; Türkçe ve Türkiye yok. Fig esasen ABD. [Yuka dil](https://help.yuka.io/l/en/article/d3rc6ysi03-yuka-languages)
8. **UX:** OFF'ta tarama geçmişinden detaya gitme zahmetli, yavaşlık; Yuka'da geçmiş/favori entegrasyonu zayıf, mağaza bazlı filtre yok.

---

## 4. Boşluk analizi

### 4.1 Doymuş (özgünlük iddiası kurma)
- Genel sağlık puanı (Nutri-Score, NOVA, katkı maddesi puanı) — Yuka, OFF, El CoCo, Besin App, ÇabukBak.
- E-kod / helal sorgulama — en az 3 TR uygulaması.
- Kalori/makro takibi — MyFitnessPal, Foodvisor, Diyetkolik.
- "Etiket fotoğrafı çek, AI anlatsın" — 2025-26'da onlarca jenerik uygulama; TR'de İçerik Tara, Ürün Dedektörü, Labelscan.
- Tek alerjen (gluten) tarayıcı — Gluten Tarayıcı 2015'ten beri.
- Basit alerji/diyet profili — Ürün Dedektörü (TR), Fig/Yuka (global).

### 4.2 Gerçekten zayıf veya boş alanlar (Türkiye + kişisel sağlık profili + alışveriş takibi kesişimi)

| Açı | Durum (bulunan) | Neden savunulabilir | Risk |
|---|---|---|---|
| **A. Türkçe etiket OCR → yapılandırılmış veri → OFF'a geri besleme** | TR rakiplerinin kendi kapalı DB'leri var; OFF TR'de ingredients'ı tamam ürün ~2.8k. Açık veriye katkı yapan bir TR uygulaması **bulunamadı** | Veri boşluğu ölçülebilir (%25 → hedef X). Akademik olarak güçlü: Türkçe ingredients parsing, alerjen taksonomisi eşleme, "iz" cümlesi çıkarımı. Proje çıktısı kamusal değer üretir | OCR/LLM hata oranı; moderasyon; OFF katkı kurallarına uyum |
| **B. Belirsizlik-bilinçli karar ("güvenli / riskli / bilinmiyor")** | Rakipler ikili dönüt veriyor; Fig/Yuka traces'i kaçırıyor | TR'de PAL zorunlu değil → "iz uyarısı yok ≠ güvenli". Veri kalitesi skoru + kaynak gösterimi + "etiketi kontrol et" durumu. Güvenlik mühendisliği argümanı | UX'te "bilinmiyor" oranı yüksek çıkarsa kullanıcı sıkılır |
| **C. Hastalığa özgü kural motoru (diyabet, hipertansiyon, hamilelik, çölyak)** | Fooducate'te kısmen var (ABD); TR'de Ürün Dedektörü hamilelik/çölyak var, **diyabet/hipertansiyon kural seti bulunamadı** | TR diyabette Avrupa 1.'si (9,6M). Porsiyon başına şeker/karbonhidrat, sodyum eşikleri, hamilelikte riskli içerikler (ör. çiğ süt peyniri, yüksek kafein) — klinik kaynaklı, açıklanabilir kurallar | Tıbbi tavsiye sınırı; bir diyetisyen/hekimle kural doğrulama şart |
| **D. Hane/aile profilleri + ortak sepet** | Fig'de var (ücretli, ABD). TR'de **bulunamadı** | "Bu ürün evde kimin için riskli?" tek taramada; çocukta fındık/yumurta alerjisi + ebeveynde diyabet senaryosu | Özellik tek başına özgün değil; A-C ile birleşince anlamlı |
| **E. Alışveriş geçmişinden hane düzeyinde analiz** | ABD'de Kroger OptUP (sadakat kartı), HelloCheck (fiş OCR). TR'de **bulunamadı** | Tarama + (opsiyonel) fiş OCR ile aylık "şeker/sodyum trendi", tekrar eden riskli alımlar. Proje adındaki "alışkanlık takibi"ni somutlaştırır | Fiş formatları heterojen; KVKK; kullanıcı her şeyi taramaz → veri eksik |
| **F. Bütçe-duyarlı güvenli alternatif** | marketfiyati.org.tr fiyat verir ama sağlık/alerji bilmez; sağlık uygulamaları fiyat bilmez. İkisini birleştiren **bulunamadı** | "Bu ürün senin için riskli; aynı kategoride güvenli ve en ucuz 3 alternatif şu marketlerde." TR'de fiyat içerikten önce geliyor (%21,8 bulgusu) | Resmî API yok; gayriresmî endpoint kırılabilir, ToS belirsiz → izin/yazışma gerekir |
| **G. Taklit/tağşiş uyarısı** | TR rakiplerinde **bulunamadı** | Türkiye'ye özgü, resmî veri. "Bu marka + ürün tipi Bakanlık listesinde" uyarısı | Liste parti bazlı; barkodla birebir eşleşmez → yanlış pozitif ve marka itibarı riski, dikkatli dil |
| **H. Diyetisyen paneli** | Diyetkolik diyetisyen + kalori sunuyor; alerji/tarama odaklı değil | Diyetisyen danışanının profilini/kural setini yönetir, alışveriş raporunu görür | Canlıya çıkışta iki taraflı pazar (diyetisyen edinme) zor; bitirme projesi kapsamını şişirir |

---

## 5. Dürüst hüküm

**"Bu uygulama özgün mü?" — Mevcut haliyle hayır.** "Onboarding'de alerji/hastalık gir, barkod tara, güvenli/riskli gör" hem globalde (Fig, Yuka, CodeCheck, Fooducate) hem Türkiye'de (Ürün Dedektörü, ÇabukBak, Gluten Tarayıcı) var. Danışmana "piyasada yok" denirse ilk Google aramasıyla çürür.

**Ama problem çözülmüş değil.** Türkiye'de problemin asıl darboğazı **veri**: OFF'ta içerik bilgisi tamam ürün ~2.800. Yerli rakipler küçük, kapalı DB'li, çoğu tek geliştirici; hiçbiri pazarı domine etmiyor. Global devler Türkiye'de yok. Özgünlük özellik listesinden değil, **veri boşluğunu nasıl kapattığından ve kararı ne kadar dürüst verdiğinden** gelir.

**Özgünlüğü artırmak için 5 somut yön (öncelik sırasıyla):**

1. **Türkçe etiket OCR + LLM ile ingredients/alerjen/"iz" çıkarımı → doğrulanmış kayıtları OFF'a geri yaz.** Ölçülebilir hedef: TR'de ingredients-completed oranını artırmak. Bitirme raporu için en güçlü teknik katkı. (A)
2. **Üç durumlu, açıklanabilir karar motoru:** güvenli / riskli / bilinmiyor + gerekçe + veri kaynağı + güven skoru; PAL yokluğunu "güvenli" saymama. (B)
3. **Diyabet ve hipertansiyon için klinik kaynaklı kural seti** (porsiyon başı şeker/sodyum eşikleri), bir diyetisyen/hekimle doğrulanmış. Türkiye'de diyabetin Avrupa'da 1. olması pazar argümanını taşır. (C)
4. **Hane profilleri + hane alışveriş raporu** (tarama geçmişi, opsiyonel fiş OCR): "evdeki kim için riskli" ve aylık trend. (D+E)
5. **Güvenli + ucuz alternatif:** marketfiyati.org.tr fiyatıyla birleştirme. Önce TÜBİTAK/Bakanlık'tan veri kullanım izni istenmeli. (F)

Taklit/tağşiş uyarısı (G) ucuz bir "Türkiye'ye özgü" artı olarak eklenebilir; diyetisyen paneli (H) kapsamı büyütür, ertelenmesi mantıklı.

**Levent'e açık sorular (bu araştırmadan doğan):**
- Eski MVP hangi veri kaynağını kullanıyordu, TR ürünlerinde bulunma oranı neydi?
- Ekip OCR/LLM tarafını üstlenebilir mi, yoksa odak mobil + backend mi?
- Çölyak/alerji dernekleriyle (Ankara Çölyak Derneği, Besin Alerjisi Derneği) pilot kullanıcı bağlantısı kurulabilir mi?
- "Canlıya almak" için KVKK tarafında (açık rıza metni, veri sorumlusu) kim sorumlu olacak?
