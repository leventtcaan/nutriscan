---
title: 05 — AI-native hane/gıda asistanları: rakip taraması + görünür AI kalıpları (v4 denetimi)
tarih: 2026-09-24
durum: HAM
onceki: 01-rakip-pazar.md (barkod/alerji tarayıcıları), 02-v2-ozgunluk-talep.md (fiş/sepet/enflasyon/Migros SYY), 01-ai-feature-havuzu.md (Instacart Health Tags, Sparky ilk hali, literatür). Orada olanlar burada tekrar edilmedi.
---

> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24.**
> Web araması + doğrudan sayfa çekme. Şirket beyanı olan rakamlar "(şirket beyanı)" diye işaretli. Rakip firmanın yazdığı inceleme "(rakip kaynağı)" diye işaretli.
> "Bulunamadı" = bu aramada çıkmadı, "yok" demek değil. Oturumun web arama kotası iş bitmeden doldu. Son birkaç doğrulama (Pak'nSave, Apple, Amazon Go) Wikipedia üzerinden yapıldı. Samsung Türkiye sayfası zaman aşımına düştü.

Döngü kısaltmaları (tabloda): **Mn** menü · **Ls** liste · **Mk** market/sepet · **Mt** mutfak/kiler · **Ö** öğren (geçmiş, tercih)

---

## 0. TL;DR

- **"Sohbetle menü → liste → sepet" artık standart özellik oldu.** 2025-26'da Walmart (Sparky), Kroger (Gemini, Oca 2026), Amazon (Rufus → Alexa for Shopping, May 2026), Instacart (Clementine, **9 Eyl 2026**), Tesco (beta, Nis 2026) bunu çıkardı. Türkiye'de de **Migros MAYA AI** (Tem 2026, OpenAI ortaklığı, ChatGPT içinde de çalışıyor), **CarrefourSA Alista** (Tem 2026) ve **Getir Hazır Sepet** (Eki 2025) var. v4 bunu yenilik diye sunamaz.
- **Buzdolabı fotoğrafı, "evdeki malzemeyle tarif", el yazısı listeyi fotoğrafla sepete çevirme, sosyal medyadan tarif içe aktarma** da yaygınlaştı. Bunları yapanlar: Samsung Family Hub (Gemini, sınırsız ürün tanıma), Ollie, KitchenPal, Instacart, Getir, Rufus, Honeydew, HelloFresh. Türkçede Nefis Yemek Tarifleri "AI'a Sor", Yemek.com Asistan Şef, Pratik Şef, Üstat var. Bunlar v4'te **giriş kanalı** olabilir, "wow" olamaz.
- **Bulunamayan üç şey:** (1) Hane **üyesi** bazında kısıtı **deterministik olarak doğrulayan**, kararını izlenebilir gösteren bir asistan. Rakiplerde kısıt "tercih/filtre" düzeyinde kalıyor. (2) **Perakendeciden bağımsız** hane grafiği: kiler + çok zincirli alım + üye × kısıt. Büyük oyuncuların hepsi yalnız kendi kasasını görüyor. (3) **Plan ile gerçekleşeni karşılaştırıp** optimizasyonla (takas, gölge fiyat) öğrenen döngü.
- **En yakın 3 rakip:** Migros MAYA AI (+ Migros Sağlıklı Yaşam Yolculuğu), Instacart Clementine, Ollie. Samsung Food + Family Hub dördüncü sırada.
- **Görünür AI üzerine kanıt karışık.** Akıl yürütmeyi ya da kaynağı göstermek güveni artırıyor. Ama güveni **doğru olup olmadığından bağımsız** artırıyor: rastgele kaynak bile güveni yükseltiyor, akıl yürütme göstermek aşırı güvene yol açıyor. Ürün tanıtımında "AI" demek satın alma niyetini düşürüyor. Asistanın ödemeyi kendisinin yaptığı model tutmadı: Walmart'ın ChatGPT Instant Checkout denemesi 3 kat düşük dönüştü. Sonuç: v4'ün "LLM orkestra eder, motorlar karar verir" ilkesi doğru. Ama görünür yüz "AI" etiketi değil, **tıklanıp doğrulanabilen karar izi** olmalı.

---

## 1. Ürün taraması

### 1.1 Global: tarif / menü planlayıcılar

| Ürün | Görünür AI özelliği | Hane/kısıt farkındalığı | Döngü | TR'de? | Şikâyet / zayıf yan |
|---|---|---|---|---|---|
| **Samsung Food** (eski Whisk) + Food+ | Food+ ile 7 günlük AI plan (ücretsizde 3 gün); tarifi "Personalize" ile AI'a değiştirtme; Vision AI (yalnız Galaxy'de kalori tahmini); 240k+ tarif. Food+ 6,99 $/ay. [MealThinker, rakip kaynağı](https://mealthinker.com/blog/samsung-food-alternative), [toolworthy](https://www.toolworthy.ai/tool/samsung-food) | Diyet tercihi filtresi var. Üye bazlı kısıt doğrulaması bulunamadı | Mn, Ls, Mt (Food+ ile manuel kiler) | TR App Store'da var ama **Türkçe desteklenmiyor** (7 dil). 7 puan. [App Store TR](https://apps.apple.com/tr/app/samsung-food-meal-planner/id1133637674) | Plan için tarifleri güne tek tek sürüklemek gerekiyor. Kullanıcılar "AI önerileri diyet tercihimi yansıtmıyor" diyor. Kiler manuel. "Health Score" diyet kültürü dili yüzünden eleştiriliyor (rakip kaynağı) |
| **Samsung Family Hub – AI Vision Inside** (CES 2026 İnovasyon Ödülü, Gemini) | Buzdolabı içi kamera + LLM. Taze, paketli ve işlenmiş gıdada "sınırsız" ürün tanıyor, kullanıcının kaba yazdığı etiketi okuyor, food list'i otomatik güncelliyor. Tarif önerisi, akıllı liste, haftalık gıda raporu. ABD'de 11 Mayıs 2026'dan itibaren OTN güncellemesiyle geliyor. [CES](https://www.ces.tech/ces-innovation-awards/2026/family-hub-with-ai-vision-inside-powered-by-ai-agent/), [Samsung Newsroom](https://news.samsung.com/global/samsung-expands-ai-capabilities-of-bespoke-ai-refrigerator-family-hub-with-major-updates) | Bulunamadı | Mt (güçlü), Mn, Ls | TR'de satış/özellik durumu **doğrulanamadı** (Samsung TR sayfası açılmadı) | Yalnız buzdolabını görüyor, kiler/dolap yok. Pahalı cihaz. "Evde ne var" sorununun yalnız bir kısmını çözüyor. Bu son nokta bir rakip blog yorumu, veri yok. [Recipy blog](https://recipyapp.com/blog/pantry-truth-problem-ai-2026) |
| **Ollie** (ABD; Khosla ve AI2 yatırımlı) | Aileye haftalık otomatik plan, planı sohbetle değiştirme, kiler fotoğrafından malzeme tanıma, Instacart/Walmart/Amazon Fresh'e liste. 9,99 $/ay. [olliemeal.com](https://olliemeal.com/index.html), [Google Play](https://play.google.com/store/apps/details?id=com.confabulation.ollie&hl=en_US) | Rakip incelemesine göre **aile profilleri + üye bazlı alerjen** var. Resmî sitede açık değil | Mn, Ls, Mt (kısmi), Ö (tercih öğrenme) | Hayır (yalnız ABD) | "Tercihleri hatırlamakta zorlanıyor", tarifler tekrar ediyor, fotoğraftan tanınan kiler kalıcı envantere dönmüyor, web sürümü yok, besin takibi tarif düzeyinde kalıyor. [MealThinker, rakip kaynağı](https://mealthinker.com/blog/ollie-meal-planner-review) |
| **Mealime** | AI yok, sabit katalogdan plan | Diyet filtresi | Mn, Ls | — | **21 Ekim 2026'da kapanıyor.** Albertsons kullanıcıları kendi uygulamalarındaki "Meals Hub"a yönlendiriyor, dışa aktarma yok. [Plan to Eat](https://www.plantoeat.com/blog/2026/09/mealime-is-moving-heres-your-best-meal-planning-alternative/), [Pann](https://www.pann-app.com/blog/is-mealime-shutting-down). **Ders:** bağımsız planlayıcıları perakendeciler yutuyor |
| **Plan to Eat** / **Paprika** | AI özelliği bulunamadı. Paprika tamamen manuel, tek seferlik ücret. [FoodiePrep](https://www.foodieprep.ai/blog/mealime-vs-paprika) | Yok | Mn, Ls (Paprika'da kiler var) | Bulunamadı | Kullanıcıların ağır iş yapması gerekiyor. AI'sız kalan eski kuşak |
| **SideChef** | RecipeGen AI: yemek fotoğrafından tarif; Instacart, Walmart, Amazon Fresh'e tek tıkla liste. [BusinessWire](https://www.businesswire.com/news/home/20240806193505/en/SideChef-Announces-RecipeGen-AI) | Diyet tercihi | Mn, Ls | Bulunamadı | Bulunamadı |
| **Honeydew** | TikTok, Instagram ve YouTube videosundan, ekran görüntüsünden AI ile tarif çıkarma; reyon sırasına göre liste; Instacart'a aktarma. [App Store](https://apps.apple.com/us/app/honeydew-capture-recipes/id6714449541) | 6 kişilik hane paylaşımı var, kısıt yok | Mn, Ls | Bulunamadı | Ücretsiz sürümde ayda 10 AI içe aktarma |
| **HelloFresh Cookbook** (May 2026, abonelik gerektirmiyor) | Videodan ya da siteden yapılandırılmış tarif; "Discover" akışı abonelere öneri yapan motoru kullanıyor. 1M+ tarif kaydedilmiş (şirket beyanı). [Chain Store Age](https://chainstoreage.com/hellofresh-offers-free-recipe-services-its-app), [The Grocer](https://www.thegrocer.co.uk/news/hellofresh-launches-ai-powered-social-media-recipe-extraction-tool/720225.article) | Bulunamadı | Mn | Bulunamadı | — |

### 1.2 Global: perakendeci ve platform asistanları

| Ürün | Görünür AI özelliği | Hane/kısıt farkındalığı | Döngü | TR'de? | Şikâyet / zayıf yan |
|---|---|---|---|---|---|
| **Instacart Clementine** (9 Eyl 2026, ABD + Kanada) | Sohbet, liste ya da tarifi saniyeler içinde sepete çeviriyor. "Order my usuals", "restock my pantry staples", fırsatlar, daha ucuz alternatif, el yazısı liste fotoğrafı. [Instacart Newsroom](https://company.instacart.com/pressreleases/meet-clementine-instacart-s-ai-shopping-assistant-that-takes-what-s-for-dinner-off-your-plate), [TechCrunch](https://techcrunch.com/2026/09/09/instacart-launches-an-ai-grocery-shopping-assistant-called-clementine/) | **Var, hane düzeyinde:** tercih merkezi (glutensiz, vejetaryen, **nut-free**, organik) bir kez ayarlanıyor. Üye bazlı olup olmadığı ve nasıl doğrulandığı **belirtilmemiş** | Mn, Ls, Mk (çok perakendeci, tek platform), Mt (geçmişten yeniden stok tahmini), Ö | Hayır | TechCrunch haberinde şeffaflık, adım gösterme ya da sınırlama bilgisi yok. Uber Eats ve DoorDash da benzer asistan çıkardı. Kategori kalabalık |
| **Instacart Cart Assistant** (kurumsal, beyaz etiket) + **ChatGPT app** | Perakendecinin kendi uygulamasına gömülen asistan: diyet filtresi, tariften sepete, fotoğraftan liste, "3 katmanlı içerik moderasyonu", mağazalar arası veri izolasyonu. ChatGPT'de 1.800+ perakendeciden sipariş. [Cart Assistant](https://company.instacart.com/enterprise-blog/cart-assistant-from-instacart), [Instacart IR](https://investors.instacart.com/news-releases/news-release-details/instacart-app-launches-openai-chatgpt-first-company-offer-new) | Diyet filtresi | Mn, Ls, Mk | Hayır | Guardrail'ı pazarlama metninde öne çıkaran tek oyuncu bu. Ayrıntı yok |
| **Walmart Sparky** | Hedefi söylüyorsun ("hafta içi akşam yemekleri"), o planlıyor, akıl yürütüyor ve sepete ekliyor. Kişisel yeniden stoklama, yemek planlama, tekrarlanan ürünleri otomatik yeniden sipariş. İspanyolca. Kullanıcılarda sepet ortalaması %35 yüksek, Sparky'den alınan adet bir çeyrekte 4 katın üstüne çıktı, haftalık aktif kullanıcı %100+ arttı (şirket beyanı, 22 May 2026). [DC360](https://www.digitalcommerce360.com/2026/05/22/walmart-sparky-agent-ai-sales-supply-chain/), [Kellogg vakası](https://www.kellogg.northwestern.edu/academics-research/research/detail/2026/walmarts-sparky-agentic-ai-and-the-future-of-shopping/) | Bulunamadı | Mn, Ls, Mk, Ö | Hayır | "40-50 $ arası" istenince 20 $ altı ürün önermiş, 3. taraf satıcılarda teslimat bilgisini güvenilir çekemiyor. İki senatör "Made in USA" iddiaları için FTC incelemesi istedi. [Retail Media Breakfast Club](https://retailmediabreakfastclub.com/walmarts-sparky-ai-assistant-a-late-mover/), [GuruFocus](https://www.gurufocus.com/news/9090178/walmart-gains-as-sparky-draws-an-ftc-probe-request). **ChatGPT Instant Checkout, siteye yönlendirmeye göre 3 kat düşük dönüştü** (Walmart EVP Daniel Danker, WIRED, 18 Mar 2026). Walmart kendi Sparky'sini ChatGPT ve Gemini'ye gömdü, sepet ve ödeme Walmart'ta kaldı. [PPC Land](https://ppc.land/walmarts-chatgpt-checkout-flopped-heres-what-comes-next/) |
| **Amazon Rufus → Alexa for Shopping** (13 May 2026) + **Alexa+** | Diyet tercihini hatırlıyor, el yazısı listeyi sepete çeviriyor, hedef fiyatta otomatik satın alıyor ("ortalama %20 tasarruf", şirket beyanı), "geçen hafta pumpkin pie için aldıklarımı tekrar sipariş et" diyebiliyorsun. Alexa+ Fresh ve Whole Foods'tan sipariş veriyor, tarif ve diyet tercihini hatırlıyor. [About Amazon](https://www.aboutamazon.com/news/retail/amazon-rufus-ai-assistant-personalized-shopping-features), [GeekWire](https://www.geekwire.com/2026/amazon-unifies-alexa-and-rufus-as-ai-rivals-move-into-online-shopping/), [Grocery Dive](https://www.grocerydive.com/news/amazon-alexa-grocery-technology-digital-whole-foods/741623/) | Hesap düzeyinde diyet tercihi | Mn (kısmi), Ls, Mk, Ö | Amazon.com.tr'de karşılığı **bulunamadı** | Gıda odaklı şikâyet bulunamadı. Amazon Fresh ve Go fiziksel mağazaları Şubat 2026'da kapandı. [Wikipedia](https://en.wikipedia.org/wiki/Amazon_Go) |
| **Kroger alışveriş ajanı** (Oca 2026, Gemini Enterprise) | Tek talimatla yemek fikri, kalabalık sofralar için sepet, geçmişten yeniden sipariş, karşılaştırma. Bütçeye ve "ailenin kendine özgü tercihlerine" göre liste. [Supermarket News](https://www.supermarketnews.com/grocery-technology/kroger-launches-ai-driven-shopping-agent) | "Aile tercihi" var. Doğrulama detayı yok | Mn, Ls, Mk, Ö | Hayır | Bulunamadı (Kroger OptUP için bkz. 02) |
| **Tesco AI asistanı** (Nis 2026'da 280 bin çalışana beta, müşteriye 2026 sonu planlanıyor; Tomoro/OpenAI) | Tercih ve diyete göre tarif, **evde olanı kullanan** yemek, maliyet ya da mutfağa göre arama, malzemeleri sepete ekleme. [Retail Gazette](https://www.retailgazette.co.uk/blog/2026/04/tesco-trials-ai-shopping-assistant-with-280000-colleagues-ahead-of-customer-rollout/), [The Grocer](https://www.thegrocer.co.uk/news/tesco-launches-meal-planning-basket-building-in-app-ai-assistant/717474.article) | Diyet tercihi. Hane ya da üye detayı bulunamadı | Mn, Ls, Mk, Mt (kullanıcı söylerse) | Hayır | Henüz beta |
| **Sainsbury's** / **Ocado** | Müşteriye dönük üretken AI yemek asistanı **bulunamadı** (Sainsbury's'te yalnız genAI arama iyileştirmesi). [Diginomica](https://diginomica.com/ai-and-grocery-uks-leading-supermarkets-put-ai-top-shopping-list-ceos-sainsburys-and-tesco-explain) | — | — | Hayır | — |
| **Picnic** (NL/DE/FR) | Uygulama içi haftalık planlayıcı (Kas 2024): "yalnız sipariş veren kişinin değil, hanedeki herkesin damak tadı". Yazıda AI/LLM geçmiyor. Resmî olmayan bir **MCP sunucusu** Claude ve ChatGPT'yi Picnic sepetine bağlıyor. [Picnic blog](https://jobs.picnic.app/en/blogs/solving-the-most-complex-task-of-grocery-shopping-meal-planning), [mcp-picnic](https://github.com/ivo-toby/mcp-picnic) | **Hane tercihi var** (AI değil) | Mn, Ls, Mk | Hayır | Kiler yok |

### 1.3 Global: beslenme ve tarama uygulamaları

| Ürün | Görünür AI özelliği | Hane/kısıt farkındalığı | Döngü | TR'de? | Şikâyet / zayıf yan |
|---|---|---|---|---|---|
| **MyFitnessPal** AI Coach (Haz 2026) + Meal Planner (Intent) + ChatGPT Health | Coach sekmesi: kayıtlarına bakıp ucuz takas, porsiyon ve menü önerisi. Meal Planner "birey ve aileler için" plan, otomatik liste, sepete ekleme (Premium+ 99,99 $/yıl). Ocak 2026'dan beri ChatGPT Health içinde. Mart 2026'da **Cal AI'ı satın aldı**. [9to5Mac](https://9to5mac.com/2026/06/16/myfitnesspal-adds-ai-powered-coach-for-personalized-nutrition-guidance/), [PR Newswire – Intent](https://www.prnewswire.com/news-releases/myfitnesspal-announces-acquisition-of-intent-revolutionizing-personalized-meal-planning-for-members-302374108.html), [TechCrunch – Cal AI](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens/) | Hedef ve diyet düzeyinde. Alerjen güvenliği yok | Mn, Ls, Ö (öğün kaydı) | MFP TR'de var. **AI Coach yalnız ABD, UK, CA, AU, NZ'de** | Uygulama aşırı şişmiş ("günlük, fitness, GLP-1, koç, planlayıcı…"). [Amy Food Journal](https://www.amyfoodjournal.com/blog/myfitnesspal-review) |
| **Cal AI** | Fotoğraftan kalori. 15M indirme, 40M $+ gelir. [TechCrunch](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens/) | Yok | Ö | Bulunamadı | Aynı yemeği tekrar tarayınca farklı kalori çıkıyor, karışık yemekte ~%20-30 hata. [Calorie Rankings](https://calorierankings.com/reviews/cal-ai/) (bağımsız olduğu doğrulanmadı). Faturalama şikâyetleri var |
| **Fig** | Resmî sayfada **AI özelliği yok.** Gücü 2.000+ diyet ve alerjenlik uzman kural tabanı. Çoklu profil ücretli. [Fig](https://foodisgood.com/app/) | **Güçlü** (kural tabanlı) | Ls (liste), Mk (raf) | Hayır (yalnız ABD) | Bkz. 01 |
| **Yuka** | 2026 basın kitinde **AI özelliği yok.** 80M kullanıcı, 12 ülke. [Yuka press kit](https://yuka.io/wp-content/uploads/presskit/us/yuka-presskit.pdf) | Premium filtre (bkz. 01) | Mk (raf) | Hayır | Bkz. 01. **Ders:** kategorinin en büyük iki tarayıcısı AI diye pazarlamıyor, kural ve veriyle kazanıyor |

### 1.4 Kiler / buzdolabı uygulamaları

| Ürün | Görünür AI özelliği | Hane/kısıt | Döngü | TR'de? | Şikâyet / zayıf yan |
|---|---|---|---|---|---|
| **KitchenPal** | Sitede buzdolabı fotoğrafı, fiş, sesle giriş ve "sen sormadan planlayan" AI iddiası (beta). [kitchenpal.ai](https://kitchenpal.ai/) | Hane paylaşımı. Kısıt detayı yok | Mt, Mn, Ls | Bulunamadı | **Çelişki:** bağımsız bir karşılaştırma "AI fiş taraması yok, her şey barkod, ses ya da elle" diyor. [Foodat](https://www.foodat.co/blog/best-pantry-tracker-apps-in-2026). kitchenpal.ai ile kitchenpalapp.com aynı ürün mü, doğrulanamadı |
| **NoWaste** | Barkod, fiş, fotoğraf ve "AI Assistant" ile giriş, son kullanma tarihine göre sıralama. [App Store](https://apps.apple.com/us/app/nowaste-food-inventory-list/id926211004) | Aile paylaşımı | Mt | Bulunamadı | Barkodla girişte SKT hep yanlış çıkıyor, çoğu ürün "bugün bitiyor" görünüyor. [Fango](https://fango.fi/en/blog/best-pantry-inventory-app/) |
| **Pantry Check** | Barkodla kayıt, SKT görünümü. [pantrycheck.com](https://pantrycheck.com/) | — | Mt | Bulunamadı | Tarif ya da plan entegrasyonu yok |
| **Fridgely** (+ ayrı "Fridgely: AI Recipe Maker") | Barkoddan SKT tahmini, fiş tarama, aile paylaşımı. Ayrı uygulama eldeki malzemeden AI tarifi üretiyor. [fridgelyapp.com](https://fridgelyapp.com/), [App Store](https://apps.apple.com/us/app/fridgely-ai-recipe-maker/id6756694148) | Diyet tercihi (AI Recipe Maker) | Mt, Mn | Bulunamadı | — |
| **Ortak zayıflık: kilerin gerçekten kopması ("pantry drift")** | Elle giriş 1. hafta yapılıyor, 2. hafta unutuluyor, 4. haftada bırakılıyor. Fişle giriş tüketimi ve bozulmayı görmüyor. Fotoğraf opak kabı ve miktarı görmüyor. **Bu bir rakip blog yazısı, veri yok.** [Recipy](https://recipyapp.com/blog/pantry-truth-problem-ai-2026) | | | | v4'ün "Mutfak" adımı için ana risk bu |

### 1.5 Genel asistanlar

| Ürün | Gıda/alışveriş kullanımı | TR'de? | Not |
|---|---|---|---|
| **ChatGPT** | Instacart app: plandan sepete tek sohbet. Instant Checkout Mart 2026'da kaldırıldı, ödeme işi perakendecinin uygulamasına geçti. ChatGPT Health (7 Oca 2026): MyFitnessPal ve Instacart bağlanabiliyor; ayrı hafıza, eğitimde kullanılmıyor; EEA, İsviçre ve UK dışında sunuluyor. [OpenAI](https://openai.com/index/introducing-chatgpt-health/), [PPC Land](https://ppc.land/walmarts-chatgpt-checkout-flopped-heres-what-comes-next/) | **Evet:** Migros app ChatGPT içinde (bkz. 1.6). Health'in TR'de açık olup olmadığı doğrulanamadı | Hane gıda asistanının "yüzü" ChatGPT'ye kayabilir. v4 için hem tehdit hem kanal |
| **Gemini** | Genel plan ve liste promptları, YouTube tarifi + Maps. Kroger ve Walmart (Nis 2026) Gemini üzerinde asistan çalıştırıyor. [Supermarket News](https://www.supermarketnews.com/grocery-technology/kroger-launches-ai-driven-shopping-agent) | Genel Gemini var | Yapılandırılmış kiler ya da hane hafızası yok |

### 1.6 Türkiye

| Ürün | Görünür AI özelliği | Hane/kısıt farkındalığı | Döngü | Şikâyet / zayıf yan |
|---|---|---|---|---|
| **Migros MAYA AI** (Tem 2026, OpenAI iş birliği) | Türkçe sohbetle kişiye özel **menü + tarif + malzemeyi sepete ekleme**, kampanyaları en avantajlı fiyata göre sıralama, **bitmek üzere olan ürünü hatırlatma**, "geçen haftaki siparişimi tekrarla", "protein ağırlıklı kahvaltı sepeti". Sanal Market, Hemen ve Money'de çalışıyor, **ChatGPT içinde "ilk gıda perakendecisi"**. Sesli komut "yakında". "Ürün arayanların %60'ı önerileni sepete ekliyor" (şirket beyanı, Migros One CEO'su Orçun Onat). [Webrazzi](https://webrazzi.com/2026/07/10/migros-yapay-zeka-asistani-maya-ai-ile-alisveris-aliskanliklarini-donusturuyor/), [egirişim](https://egirisim.com/2026/07/23/migrostan-openai-is-birligi-ile-yapay-zeka-alisveris-asistani-maya-ai/), [Karar](https://www.karar.com/ekonomi-haberleri/migros-maya-ai-nedir-chatgpt-ile-migros-siparisi-nasil-verilir-2063440) | Basın metinlerinde **diyet, alerji, hane ya da üye kısıtı bulunamadı** (Habertürk metninde bu terimler hiç geçmiyor). Kişiselleştirme alışveriş geçmişine dayanıyor | Mn, Ls, Mk (tek zincir), Mt (yalnız alımdan "eksilen" tahmini), Ö | Kullanıcı şikâyeti bulunamadı (çok yeni). **TR'deki en güçlü rakip.** Aynı şirkette Sağlıklı Yaşam Yolculuğu (alımdan besin karnesi, bkz. 02) var. İkisini birleştirmesi teknik olarak kolay |
| **CarrefourSA Alista** (24 Tem 2026) | Mağazada QR ile açılıyor: ürün ve stok bulma, kart puanı, alışveriş geçmişi, **eldeki malzemeye ya da diyete göre tarif**. Web sürümü "yakında". [egirişim](https://egirisim.com/2026/07/24/carrefoursa-yapay-zeka-asistani-alista-ile-musterilerine-akilli-alisveris-deneyimi-sunacak/) | Diyet (tarif düzeyinde) | Mn (tarif), Mk | Bulunamadı |
| **Getir** (Eki 2025) | **Hazır Sepet:** alışkanlığa göre hazır sepet; pilotta "%90 değiştirmeden devam etti" (şirket beyanı). **Alışveriş Listem:** el yazısı listenin fotoğrafını sepete çeviriyor ("Türkiye'de ilk"). **GetirYemek Kalori Tahmini:** fotoğraftan kalori. "Ne Yesem" özelliği de var. [Perakende Mühendisi](https://www.perakendemuhendisi.com/getirden-yapay-zeka-destekli-iki-yeni-ozellik-hazir-sepet-ve-alisveris-listem/), [egirişim](https://egirisim.com/2025/10/13/10uncu-yasini-kutlayan-getir-alisverisi-yapay-zeka-ile-daha-da-hizlandirmayi-planliyor/) | Bulunamadı | Ls, Mk, Ö | Bulunamadı |
| **Trendyol** | Shopping Assistant: "bütçe ve tarza göre en uygun sepet" (CTO Cenk Çivici, GITEX AI Türkiye 2026). Gıdada kullanıldığına dair bilgi **bulunamadı**. AITEN (2023) bir Instagram içerik karakteri, ürün değil. [AA](https://www.aa.com.tr/tr/isdunyasi/e-ticaret/trendyol-e-ihracatta-yapay-zeka-teknolojileriyle-buyumesini-hizlandiriyor/704384), [Ajans Dijital](https://ajansdijital.com.tr/trendyol-hizli-marketin-yapay-zeka-asistani-aiten-ise-basladi/) | Bütçe | Mk | — |
| **Hepsiburada, A101, ŞOK, BİM** | Gıdaya yönelik müşteri AI asistanı **bulunamadı** | — | — | — |
| **Yemek.com Asistan Şef** (Ağu 2026) | Tarifi sesle adım adım okuyor, pişirirken soru-cevap yapıyor ("fırın kaç derece?"). Malzeme, süre ve beslenme tercihine göre filtre var. [Webtekno](https://www.webtekno.com/yapay-zeka-yemek-com-asistan-sef-h223093.html) | Beslenme tercihi filtresi | Mt (pişirme anı) | Alışveriş listesi belirtilmemiş |
| **Nefis Yemek Tarifleri "AI'a Sor"** | "Aklındaki malzemelerle ne pişireceğini sor". Site metnine göre alerji ve tercihi dikkate alıyor. [nefisyemektarifleri.com](https://www.nefisyemektarifleri.com/) | Alerji (beyan, nasıl yapıldığı belirsiz) | Mn | Alışveriş listesi bulunamadı |
| **Pratik Şef** (beta, 10k+ ön kayıt, token modeli) | Buzdolabındaki malzemeden Türk mutfağı tarifi; profil (acılık, yağ, tuz, diyet kısıtı); misafir sayısına göre menü modu; eksik malzemeyle alışveriş listesi. [pratiksef.com.tr](https://www.pratiksef.com.tr/) | Diyet kısıtı (profil) | Mn, Ls, Mt | Beta, ölçek küçük |
| **Üstat – AI Yemek Tarifleri** | Malzemeden 3 tarif alternatifi, haftalık menü, eksikleri alışveriş listesine ekleme. [App Store](https://apps.apple.com/tr/app/%C3%BCstat-ai-yemek-tarifleri/id6758657888?l=tr&platform=ipad), [ustatyemek.app](https://ustatyemek.app/) | Bulunamadı | Mn, Ls | — |
| **Refika'nın Mutfağı** | AI ürünü **bulunamadı** | — | — | — |

### 1.7 Raf fotoğrafından çok ürün tanıma

- **Tüketici uygulaması bulunamadı.** Raftaki birden çok paketli ürünü tek fotoğrafta tanıyıp **kişiye göre renklendiren** bir uygulama çıkmadı. Bulunan tarayıcıların hepsi tek etiket ya da tek barkodla çalışıyor (Subfy, Food Allergen Scanner, Checkit AI vb.). [Subfy](https://subfy.app/), [Checkit AI](https://apps.apple.com/app/id6740466800)
- En yakın çok nesneli tanıma: Samsung Family Hub AI Vision (buzdolabı içi, sınırsız ürün), Instacart Caper akıllı arabası (bkz. 01-ai-feature-havuzu).
- **Yorum:** Bu alan boş olabilir ama tekniği en zor olan da bu. TR ambalajları için ürün görsel veritabanı yok (OFF TR'de yalnız ~9,5k ürünün fotoğrafı var, bkz. 01 §2.3).

---

## 2. Döngü kapsamı özeti (kim hangi adımı yapıyor)

| | Mn | Ls | Mk | Mt | Ö | Hane üyesi × kısıt | Kısıtı doğrulama / karar izi | Perakendeciden bağımsız |
|---|---|---|---|---|---|---|---|---|
| Migros MAYA | ✓ | ✓ | ✓ (tek zincir) | ~ (eksilen tahmini) | ✓ | bulunamadı | bulunamadı | ✗ |
| Instacart Clementine | ✓ | ✓ | ✓ (çok perakendeci, tek platform) | ~ (restock) | ✓ | ~ (hane tercihi) | bulunamadı | ~ |
| Walmart Sparky | ✓ | ✓ | ✓ | ~ (replenishment) | ✓ | bulunamadı | bulunamadı | ✗ |
| Ollie | ✓ | ✓ | ~ (dış sepet) | ~ (foto, kalıcı değil) | ~ | ✓ (rakip kaynağı) | bulunamadı | ✓ |
| Samsung Food + Family Hub | ✓ | ✓ | ~ (Instacart) | ✓ (buzdolabı) | ~ | ~ | bulunamadı | ✓ |
| Tesco (beta) | ✓ | ✓ | ✓ | ~ | ✓ | bulunamadı | bulunamadı | ✗ |
| Pratik Şef / Üstat | ✓ | ✓ | ✗ | ~ (elle) | ✗ | ~ (profil) | ✗ | ✓ |
| Fig | ✗ | ✓ | ✓ (raf) | ✗ | ✗ | ✓ (ücretli) | kural tabanı var, iz gösterimi bulunamadı | ✓ |
| **v4 hipotezi** | ✓ | ✓ | ✓ (≤2 market, öneri) | ✓ | ✓ (plan vs gerçek) | ✓ | ✓ | ✓ |

✓ var · ~ kısmi · ✗ yok. v4 satırı **hipotez**, henüz hiçbiri yok.

---

## 3. "Görünür AI" tasarım kalıpları: güven mi, AI yıkaması mı?

### 3.1 Kalıplar ve kanıtları

| Kalıp | Örnek | Kanıt | Hüküm |
|---|---|---|---|
| **Akıl yürütmeyi ya da adımları göstermek** ("thinking", zincirleme akıl yürütme) | ChatGPT/Claude'daki "thinking" alanı, Perplexity'nin hangi terimle aradığını göstermesi | Önceden kayıtlı deney, **N=752**: akıl yürütmeyi (kısa ya da uzun) göstermek güveni ve AI'a uyumu **anlamlı biçimde artırıyor**, ama kullanıcının **yalnız kendisinin bildiği bağlamı** kullanmasını bastırıyor. Sonuç aşırı güven. [Chen, Gao, Liang 2025, arXiv 2511.04050](https://arxiv.org/abs/2511.04050). Başka bir çalışma: kullanıcılar sonuç doğruysa hatalı akıl yürütmeye de güveniyor, **kendinden emin ton hata fark etmeyi azaltıyor**. [Park ve ark. 2025, arXiv 2511.12001](https://arxiv.org/abs/2511.12001) | **Çift taraflı.** Alerjen gibi yüksek riskli kararda akıl yürütme metni ikna aracına dönüşür. Serbest metin yerine **yapılandırılmış iz** göster: hangi kural, hangi veri, hangisi bilinmiyor |
| **Kaynak / atıf göstermek** | Perplexity, derin araştırma ajanları | Canlı deney: kaynak varken güven **anlamlı artıyor, kaynaklar rastgele olsa bile**. Kullanıcı kaynağı açıp bakınca güven düşüyor. Birden fazla kaynak ek güven getirmiyor. [Ding ve ark., AAAI 2025](https://arxiv.org/abs/2501.01303) | Tıklanamayan ya da doğrulanamayan kaynak ikonu **AI yıkaması** riski taşır. v4'te her iddia bir araç çıktısına bağlanmalı ve o çıktı **açılabilir** olmalı. "Kaynak kesinliği" eval metriği olarak ölçülmeli |
| **Adım listesi / izleme kaydı** | "Living breadcrumb", "Dynamic checklist" (Devin), "Thinking toggle", "Audit trail" ("bu fiyat nasıl hesaplandı?") | Uygulayıcı yazısı, **nicel veri yok**. Nitel gözlem: profesyoneller gerçek zamanlı adımları çoğunlukla okumuyor, nihai sonuca göre yargılıyor. Kişiselleştirmenin iz bırakmaması (ChatGPT'nin kapalı kutu hafızası) güveni aşındırıyor. [Smashing Magazine, May 2026](https://www.smashingmagazine.com/2026/05/practical-interface-patterns-ai-transparency/) | Canlı adım animasyonu demo için iyi ama güveni tek başına artırmıyor. **Varsayılan kapalı, açılabilen iz + kalıcı karar kaydı** daha savunulabilir |
| **Güveni kalibre etmek** | Google PAIR, Microsoft HAX | PAIR: açıklamayı **kullanıcının eylemine yanıt olarak** göster. Kısmi açıklama yeterli. Yüzdelik güven skoru kafa karıştırır ("%85,8 mi %87 mi?"), Yüksek/Orta/Düşük gibi kategoriler daha iyi. **Veri eksikse kullanıcıya kendi yargısını kullanmasını söyle.** [PAIR Guidebook](https://pair.withgoogle.com/chapter/explainability-trust/). HAX: 20+ yıllık araştırmadan çıkan 18 yönerge. Sistemin ne yapabildiğini, ne kadar iyi yapabildiğini ve neden öyle yaptığını açık et. [Microsoft HAX](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/) | v4'ün dört durumlu kararı (güvenli / riskli / bilinmiyor / etiketi kontrol et) PAIR'in "veri eksikse kullanıcıya devret" ilkesiyle birebir örtüşüyor. **Güçlü gerekçe** |
| **Proaktif öneri kartı** | Getir Hazır Sepet, MAYA'nın "bitmek üzere" hatırlatması, v4'ün "Pazar sabahı planın hazır" fikri | Saha: Getir'de %90 sepeti değiştirmeden devam etti, MAYA'da %60 öneriyi sepete ekledi (ikisi de **şirket beyanı**, düşük riskli yeniden stoklama). Laboratuvar: kesintisiz öneri gösteren koşulda katılımcılar asistanı **"dikkat dağıtıcı, sinir bozucu"** buldu. Doğru an, iş yükünün düşük olduğu ya da bir sorunun ortaya çıktığı an. [CHI 2025, Assistance or Disruption?](https://dl.acm.org/doi/10.1145/3706598.3713357). Proaktif başlatma, kişisel bağlamın nasıl kullanıldığı konusunda **mahremiyet kaygısı** doğuruyor. [CHI 2026 EA, "Proactive, But Not Creepy"](https://dl.acm.org/doi/10.1145/3772363.3798894) (yalnız özet görüldü) | **Seyrek, zamanı belli, onay bekleyen** kart işe yarar (haftada bir plan). Sürekli dürten asistan geri teper. "Bunu neden gösterdim" bağlantısı mahremiyet kaygısını azaltır |
| **Asistanın kendisinin satın alması** | Instant Checkout, otomatik satın alma | Walmart: sohbet içinden ödeme, siteye yönlendirmeden **3 kat düşük dönüştü**. Danker deneyimi "tatmin edici değil" diye niteledi. Kullanıcılar "beş ayrı koli" gelmesinden çekindi. [PPC Land, WIRED'a atıfla](https://ppc.land/walmarts-chatgpt-checkout-flopped-heres-what-comes-next/). ABD'de alışveriş yapanların yalnız **%22'si** alışverişi bir ajana bırakmaya güveniyor, %48'i veri kullanımından endişeli. [Acosta, Eyl 2026](https://www.bakeryandsnacks.com/Article/2026/09/17/grocery-shoppers-use-ai-but-trust-in-ai-buying-agents-lags/). Tüketiciler ajan için harcama limiti (%30), anında yetki geri alma (%29) ve kolay iptal (%28) istiyor. [Checkout.com, Haz 2026](https://www.checkout.com/newsroom/consumer-demand-for-ai-shopping-is-forming-fast-but-trust-for-agentic-commerce-is-still-catching-up) | v4 **satın almamalı.** Öneri + onay + dışa aktarma yeterli. Bu kanıt v4'ün kapsam sınırını güçlendiriyor |

### 3.2 "AI yıkaması" gibi algılanan ya da güveni kıran örnekler

- **"AI" kelimesinin kendisi:** Aynı ürün tanıtımına "yapay zekâ" eklenince satın alma niyeti düştü. Aracı değişken duygusal güven, algılanan risk yüksekse etki büyüyor. [Cicek, Gursoy, Lu 2024, WSU](https://news.wsu.edu/press-release/2024/07/30/using-the-term-artificial-intelligence-in-product-descriptions-reduces-purchase-intentions/). Müşterilerin %64'ü şirketlerin müşteri hizmetinde AI kullanmamasını tercih ediyor (Gartner, n=5.728, Ara 2023). [Gartner](https://www.gartner.com/en/newsroom/press-releases/2024-07-09-gartner-survey-finds-64-percent-of-customers-would-prefer-that-companies-didnt-use-ai-for-customer-service). **Sağlık ve gıda güvenliği yüksek riskli algılanır.** "AI destekli" etiketi burada artı değil, eksi olabilir.
- **Gizli insan emeği:** Amazon'un "Just Walk Out" sistemi, Nisan 2024'te ortaya çıktığı üzere işlemleri doğrulayan ~1.000 kişilik Hindistan ekibine dayanıyordu. [Wikipedia – Amazon Go](https://en.wikipedia.org/wiki/Amazon_Go)
- **Düzenleyici baskı:** FTC "Operation AI Comply" (Eyl 2024) kapsamında yalnız 2025'te en az 12 AI yıkaması davası açıldı. Örnek: Air AI (Ağu 2025). [NatLawReview](https://natlawreview.com/press-releases/ftc-brings-dozen-ai-washing-enforcement-cases-2025-targeting-overstated-ai), [Holland & Knight, Ağu 2026](https://www.hklaw.com/en/insights/publications/2026/08/operation-ai-comply-2-years-later-continued-enforcement)
- **Görünür ama hatalı çıktı:** Apple Intelligence'ın haber özetleri BBC adına yanlış haber üretti (Ara 2024 – Oca 2025). Haber özetleri iOS 18.3'te kapatıldı, "hata içerebilir" uyarısı eklendi. iOS 26'da "Summarized by Apple Intelligence" etiketiyle geri geldi. [Wikipedia – Apple Intelligence](https://en.wikipedia.org/wiki/Apple_Intelligence)
- **Gıdada guardrail'siz LLM:** Pak'nSave'in "Savey Meal-bot"u (Haz 2023, GPT-3) eldeki malzemeden tarif üretiyordu. Kullanıcıların girdisiyle **klor gazı tarifi** ve "karınca zehirli sandviç" önerdi. [Wikipedia – Pak'nSave](https://en.wikipedia.org/wiki/Pak%27nSave). v4'ün "LLM üretir, kural motoru doğrular" ilkesinin doğrudan gerekçesi.
- **Vaat ile davranışın uyuşmaması:** Samsung Food kullanıcıları "AI önerileri diyet tercihimi yansıtmıyor" diyor (rakip kaynağı). Ollie kullanıcıları "tercihlerimi unutuyor" diyor. **Hafıza vaadi en sık kırılan vaat.**
- **Tersine örnek:** Yuka (80M kullanıcı) ve Fig AI diye pazarlamıyor, kural ve veriyle güven kazanıyor (bkz. §1.3).

### 3.3 v4 için çıkan tasarım kuralları (araştırma çıkarımı, karar değil)

1. **Etikete değil sonuca "AI" de.** "Ela için fındıksız 5 akşam yemeği, 1.850 TL" de, "AI destekli planlayıcı" deme.
2. **Karar izi yapılandırılmış olmalı, serbest metin olmamalı:** kural kimliği, veri kaynağı, veri tarihi, durum. Varsayılan kapalı, tek dokunuşla açılır. LLM'nin anlatımı bu izin **altında** durur, yerine geçmez.
3. **"Bilinmiyor" birinci sınıf durum olmalı.** Veri eksikse karar kullanıcıya devredilir (PAIR). Kendinden emin ton yalnız doğrulanmış kararda kullanılır (Park 2025).
4. **Her kaynak ikonu tıklanabilir ve doğrulanabilir olmalı.** Eval'de ölçülecekler: kaynak kesinliği ve iddia-araç eşleşme oranı (Ding 2025).
5. **Proaktif olmak haftada bir kart demek.** Onay, erteleme ve kapatma seçeneği olmalı, "neden şimdi" bağlantısı olmalı.
6. **Satın alma yok.** Liste dışa aktarılır. Asistan izin olmadan hiçbir şeyi değiştirmez. İzin geri alınabilir.
7. **Canlı adım animasyonu** ("Katalogda arıyorum → Ela için kontrol ediyorum") demo ve jüri için değerli. Ama güven kanıtı olarak sunulmamalı, kanıt karar kaydıdır.

---

## 4. Hüküm: v4 özgün mü?

### 4.1 Kısa cevap
**Parçalar özgün değil, kombinasyon bu aramada bulunamadı.** Menü → liste → sepet, buzdolabı fotoğrafı, hane tercihi, proaktif sepet ve sohbet asistanının hepsinin 2025-26'da güçlü sahipleri var (Migros, Instacart, Walmart, Samsung, Getir). Bulunamayan şu dört şeyin **birlikte** olması: (a) **üye bazlı** kısıtların **deterministik motorla doğrulanması ve karar izinin gösterilmesi**, (b) **perakendeciden bağımsız** hane grafiği (kiler + çok zincirli alım + üyeler), (c) döngünün **plan ile gerçekleşeni ölçerek** optimizasyonla kapanması, (d) Türkçe ve TR verisi.

### 4.2 En yakın 3 rakip

| # | Rakip | Neden en yakın | v4'te olup onda olmayan (bulunamayan) |
|---|---|---|---|
| 1 | **Migros MAYA AI** + Sağlıklı Yaşam Yolculuğu (TR) | Aynı döngü (menü → tarif → sepet → "eksilen" hatırlatma), Türkçe, OpenAI, ChatGPT kanalı, 9M+ kişilik sağlık karnesi altyapısı aynı şirkette | Üye × kısıt ve alerjen doğrulaması, kiler, çok zincir, karar izi. **Risk:** Migros SYY ile MAYA'yı birleştirirse "hane sağlığı + sepet" söylemini v4'ten önce sahiplenir |
| 2 | **Instacart Clementine** (ABD/CA) | Globalde en eksiksiz hane gıda asistanı: hane tercih merkezi (nut-free dahil), usuals, kiler yeniden stoklama, fırsatlar, fotoğraftan liste, tarif | Kısıtın nasıl doğrulandığı ve üye bazlı olup olmadığı açıklanmamış, karar izi yok, kiler durumu yalnız geçmişten tahmin, satış platformuna bağlı |
| 3 | **Ollie** (ABD) | Aile odaklı: üye bazlı alerjen (rakip kaynağına göre), kiler fotoğrafı, sohbetle plan düzenleme, otomatik haftalık plan | Kalıcı kiler, doğrulanabilir güvenlik kararı, fiyat ve market optimizasyonu, öğrenme ("tercihleri unutuyor"). TR yok |
| (4) | Samsung Food + Family Hub AI Vision | En güçlü "göz" (buzdolabında sınırsız ürün tanıma, Gemini) | Türkçe yok, cihaz bağımlı, kısıt doğrulaması yok |

### 4.3 Bizi ayıran 3 şey (savunulabilir sırayla)

1. **Doğrulanabilir kısıt kararı.** Rakiplerde kısıt bir "tercih/filtre" ve nasıl uygulandığı görünmüyor. v4'te kural motoru dört durumlu karar veriyor, karar izi gösteriliyor, LLM araç sonucunu değiştiremiyor. Gıdada guardrail'siz LLM'nin nereye gidebileceğini Pak'nSave örneği gösteriyor. Literatür de LLM'nin güvenlik kararında tek başına güvenilmez olduğunu söylüyor (bkz. 01-ai-feature-havuzu §2). **Bu, jüriye "neden LLM yetmez?" sorusunun cevabı.**
2. **Perakendeciden bağımsız hane grafiği.** Migros, Instacart, Walmart, Kroger ve Tesco yalnız kendi kasasını görüyor. v4 fiş ve fatura üzerinden çok zincirli alımı, kileri ve üye kısıtlarını tek grafikte birleştiriyor (fiş verisi ve Migros tekelinin kırılması için bkz. 02 §2).
3. **Ölçülen ve optimize edilen döngü.** Rakiplerin "öğren" adımı "usuals / tekrar sipariş" düzeyinde. Plan ile gerçekleşenin karşılaştırılması, en az değişiklikle takas (MILP) ve "sağlığın TL fiyatı" tüketici ürününde bulunamadı (bkz. 02 §1.2 c).

**Dürüst uyarılar:**
- 1 ve 3 **kullanıcıya kendiliğinden görünmez.** Görünür AI yüzü tam olarak bunları göstermeli: "Ela için 14 kural kontrol edildi, 1 ürün bilinmiyor, etiketi kontrol et." Aksi halde ürün dışarıdan "MAYA'nın küçük kopyası" gibi görünür.
- 2'nin bedeli **ödeme yapamamak.** v4 sepeti Migros'a ya da Getir'e aktaramaz (herkese açık sepet API'si bulunamadı). Walmart verisi bunun ters yüzünü gösteriyor: kullanıcı ödemeyi perakendecinin kendi uygulamasında yapmayı tercih ediyor. Liste dışa aktarma + "hangi markette" önerisi mantıklı bir sınır.
- 1'in değeri **ürün içerik verisine** bağlı. OFF TR'de içindekiler bilgisi tamam olan ürün ~%25 (bkz. 01 §2.3). "Bilinmiyor" oranı yüksek çıkarsa asistan sürekli "bilmiyorum" diyen bir yüze dönüşür.

### 4.4 v4'e ekle / çıkar / değiştir (öneri, karar değil)

**Ekle**
- **Kiler güven modeli:** Her kiler kaleminde güven skoru olsun, zamanla azalsın. "Pişirdim" dokunuşuyla tarifteki malzemeler düşülsün. Fişten gelen alımla artsın. Sistem yalnız belirsizlik yüksek olduğunda sorsun. Gerekçe: pantry drift, bütün kiler uygulamalarının ortak zayıflığı. Aynı zamanda akademik açıdan tanımlı bir problem (belirsizlik altında envanter durumu tahmini).
- **Karar kaydı ekranı** ("Bu plan neden böyle?"): kural, veri, tarih, alternatifler. Görünür AI'ın ana kanıtı bu ekran.
- **Eval'de "güven kalibrasyonu" metrikleri:** iddia-araç eşleşme oranı, kaynak kesinliği, "bilinmiyor" oranı. Gerekçe: Ding 2025 ve Chen 2025.
- **(Opsiyonel, ileride) MCP / ChatGPT app olarak "hane doğrulayıcı" aracı:** Migros ve Instacart ChatGPT'de zaten var. NutriScan'in kısıt motoru orada çağrılabilen bir **doğrulama aracı** olabilir. Konumlanma "ben de sepet yaparım" değil, **"sepeti hane için doğrularım"** olur. Kapsamı büyütür, o yüzden "ileride" diye işaretli.

**Çıkar ya da "wow" listesinden indir (giriş kanalı olarak kalabilir)**
- **"Buzdolabı fotoğrafı → evde ne var + 3 tarif":** Samsung, Ollie, KitchenPal, Tesco, CarrefourSA, Nefis Yemek Tarifleri, Pratik Şef ve Üstat bunu yapıyor. Wow değil, standart özellik.
- **El yazısı liste fotoğrafı → sepet / liste:** Getir, Instacart, Rufus'ta var. Gerekmiyorsa hiç yapma.
- **Sosyal medyadan tarif içe aktarma, fotoğraftan kalori:** Honeydew, HelloFresh ve SideChef'te var. Cal AI'ın doğruluk şikâyetleri ortada. Kapsam dışı.
- **Canlı adım izleme** wow olarak kalabilir ama "güven" iddiasıyla sunulmamalı (§3.1).

**Riskli ama boş görünen (araştırma spike'ı olarak tut)**
- **Raf fotoğrafıyla çok ürün tarama:** tüketici ürünü bulunamadı. Ama TR ambalaj görsel veritabanı yok. Başarısız olma ihtimali yüksek, en fazla 1 haftalık zaman kutusuyla denenmeli.
- **Tarif değişikliği radarı:** tüketici ürününde bulunamadı. Barkod aynı kalıp içeriğin değiştiğini tespit etmek için içerik geçmişi lazım (bkz. 01-mevzuat-risk.md, "Sürüm/tarif değişikliği" maddesi).
- **Kısıt-farkında işbirlikçi öneri** ("fındık alerjili hanelerin sevdiği"): bulunamadı. Ama soğuk başlangıç sorunu var, kullanıcı olmadan veri yok. Danışmanın alanı olduğu için yöntem katkısı olabilir. Başlangıçta sentetik ya da tohum veri gerekir.

**Değiştir**
- **Proaktiflik:** "Pazar sabahı planın hazır" haftada bir, onay bekleyen tek kart olsun. Anlık dürtme olmasın.
- **Konumlanma dili:** Ürün metinlerinde "yapay zekâ destekli" yerine sonuç ve güvence dili kullanılsın ("kontrol edildi", "neden?"). Gerekçe: Cicek 2024, Gartner.

---

## 5. Levent'e açık sorular (bu araştırmadan doğan)
1. **Migros MAYA'ya karşı konum:** Rakip mi (kendi asistanımız), tamamlayıcı mı (doğrulayıcı katman)? Bu karar "Market" adımının kapsamını belirliyor.
2. **Sepet aktarımı:** Hedef marketlerde (Migros, Getir, A101) sepete dışarıdan ekleme yolu var mı? Herkese açık bir yol **bulunamadı**. Yalnız liste dışa aktarmakla yetinmek kabul mü?
3. **"Wow" demo seçimi:** Buzdolabı fotoğrafı standart hale geldi. Jüriye gösterilecek ana an "karar izi" mi olsun ("Ela için neden?"), yoksa "raf fotoğrafı" riski mi alınsın?
4. **Hafıza vaadi:** Rakiplerin en sık kırılan vaadi "tercihlerimi hatırla". Hane grafiğinin hangi kısmı kullanıcıya **düzenlenebilir** olarak gösterilecek?

---

### Kaynak notu
- Şirket beyanları (Migros %60, Getir %90, Walmart AOV %35, HelloFresh 1M) bağımsız doğrulanmadı.
- Rakip kaynakları (MealThinker, Recipy, Foodat, Fango, FoodiePrep, Calorie Rankings) çıkar çatışmalı, veri olarak değil "şikâyet teması" olarak kullanıldı.
- CHI 2026 "Proactive, But Not Creepy" makalesinin yalnız arama özeti görüldü, tam metne erişilemedi.
- Samsung Family Hub AI Vision'ın TR'de satış durumu ve Amazon.com.tr'de Rufus / Alexa for Shopping durumu **doğrulanamadı**.
