> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24**
> Bu dosya bir fizibilite taramasıdır; karar değildir. Kararlar `plan/kararlar.md`'ye Levent onayıyla girer.
> Kendi ölçümlerimin yöntemi en altta ("Ek: Metodoloji"). Kaynağı olmayan her cümle **[değerlendirme]** etiketlidir.

# NutriScan — Veri ve Teknik Fizibilite

## 0. Özet hüküm tablosu

| Alt başlık | Hüküm | Tek cümle |
|---|---|---|
| Barkod → ürün verisi (OFF) | 🟡 Sarı | API ve lisans uygun; ama Türkiye ürünlerinde içindekiler alanı yaklaşık %15–25 dolu. |
| OFF'u kendi DB'ye mirror etmek | 🟢 Yeşil | Nightly JSONL/CSV + 14 günlük delta export resmi olarak var; backend'den canlı API'ye yüklenmek yerine önerilen yol bu. |
| Alternatif kaynaklar (GS1, FatSecret, Edamam, USDA, TürKomp, marketfiyati) | 🔴 Kırmızı / 🟡 | Türkiye barkodlu **içindekiler/alerjen** verisini ücretsiz ve yasal veren ikinci bir kaynak bulamadım. |
| Veri boşluğu: etiket fotoğrafı → vision LLM | 🟡 Sarı | Teknik olarak yapılabilir ve ucuz (çağrı başına ~0,5–1,5 cent); Türkçe etiket doğruluğu için yayınlanmış ölçüm yok, kendimiz ölçmek zorundayız. |
| Alerjen tespiti (Türkçe) | 🔴 Kırmızı (OFF'a güvenirsek) / 🟡 (kendi katmanımızla) | OFF'un Türkçe alerjen/taxonomy desteği zayıf; alerjen çıkarımını kendimiz yapmalıyız. |
| Barkod tarama | 🟢 Yeşil | Native/cross-platform'da çözülmüş problem; PWA'da iOS için WASM gerekiyor ama yapılabilir. |
| Alışveriş alışkanlığı takibi | 🟢 (tarama geçmişi + manuel) / 🟡 (fiş OCR) / 🔴 (sadakat programı) | Gerçekçi kaynak tarama geçmişi; fiş OCR opsiyonel; market sadakat entegrasyonu için açık API bulamadım. |
| Hukuk (KVKK) | 🟡 Sarı | Alerji/sağlık profili özel nitelikli kişisel veri; yurt dışı LLM API'sine veri gönderimi ayrıca düşünülmeli. |

---

## 1. Open Food Facts (OFF)

### 1.1 API, sürümler, rate limit, User-Agent
- **v3 önerilen sürüm, v2 deprecated ama destekleniyor** ([OFF API intro](https://openfoodfacts.github.io/openfoodfacts-server/api/)).
- **Rate limit (resmi):** ürün okuma **15 istek/dk/IP**, arama **10 istek/dk/IP** ([OFF API intro](https://openfoodfacts.github.io/openfoodfacts-server/api/)). Aynı sayfa, isteklerin kullanıcı uygulamasından gelmesi durumunda limitin kullanıcı başına uygulandığını söylüyor.
  - **Sonuç [değerlendirme]:** Mobil istemci OFF'u doğrudan çağırırsa limit kullanıcı başına işler, sorun olmaz. **Spring Boot backend tek IP'den proxy yaparsa tüm kullanıcılar 15/dk'yı paylaşır** → canlı ürün için kırılma noktası. Bu yüzden ya mirror ya da istemciden doğrudan çağrı.
- OFF ayrıca "birkaç yüz üründen fazlasını çekecekseniz CSV/JSONL indirin" diyor ([OFF API intro](https://openfoodfacts.github.io/openfoodfacts-server/api/)).
- **User-Agent zorunlu:** `AppName/Version (ContactEmail)` formatında ([OFF API intro](https://openfoodfacts.github.io/openfoodfacts-server/api/)).
- Staging ortamı: `world.openfoodfacts.net` (HTTP basic auth `off/off`) ([OFF API intro](https://openfoodfacts.github.io/openfoodfacts-server/api/)). Write testleri buraya yapılmalı.
- Okuma endpoint'i: `GET /api/v2/product/{barcode}?fields=...` ([OFF API tutorial](https://openfoodfacts.github.io/openfoodfacts-server/api/tutorial-off-api/)); v3 karşılığı `GET /api/v3/product/{barcode}` 2026-09-24'te canlıda çalıştı (kendi testim, Ek).
- Gözlem: 2026-09-24 akşamı arka arkaya sorgularda birkaç kez "Page temporarily unavailable" HTML sayfası döndü (retry ile düzeldi). **[değerlendirme]** İstemci JSON bekleyip HTML alırsa çökmemeli; retry + timeout + cache şart.

### 1.2 Lisans ve share-alike
- Veritabanı **ODbL**, tekil içerik **DbCL**, ürün görselleri **CC BY-SA** ([OFF data](https://world.openfoodfacts.org/data), [OFF terms](https://world.openfoodfacts.org/terms-of-use)).
- Ticari kullanım serbest, **atıf zorunlu** (lisansı belirt + OFF'a link) ([OFF terms](https://world.openfoodfacts.org/terms-of-use)).
- **Share-alike:** OFF verisini kendi verinizle birleştirip oluşan uyarlanmış veritabanını kamuya açarsanız o da ODbL ile sunulmalı ([ODbL özeti](https://opendatacommons.org/licenses/odbl/summary/), [OFF terms](https://world.openfoodfacts.org/terms-of-use)). ODbL "adapted database" ile "produced work" (ör. uygulama ekranı) arasında ayrım yapar ([ODbL özeti](https://opendatacommons.org/licenses/odbl/summary/)).
- Görsellerde ambalaj tasarımı/marka hakları gibi üçüncü taraf hakları ayrıca geçerli olabilir ([OFF terms](https://world.openfoodfacts.org/terms-of-use)).
- Uyum soruları: `reuse@openfoodfacts.org` ([OFF lisans rehberi](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/tutorials/license-be-on-the-legal-side/)).
- **Pratik yorum [değerlendirme, hukuki görüş değil]:**
  - Ürün tablosunu (OFF mirror + kullanıcıların eklediği ürünler) ODbL altında tutmayı baştan kabul et; eklenenleri zaten OFF'a geri yaz (bkz. 1.5). Böylece share-alike yükü pratikte sıfırlanır.
  - Kullanıcı profili, alerji listesi, tarama geçmişi **ürün veritabanının parçası değil**; ayrı şemada tut. Bu hem ODbL hem KVKK açısından temiz ayrım.
  - Arayüzde "Veri: Open Food Facts (ODbL)" + ürün sayfası linki.

### 1.3 Toplu veri: dump, Parquet, delta → mirror mantığı
- **MongoDB dump** ve **JSONL** (nightly), **CSV** (nightly; food ~0,9 GB sıkıştırılmış / ~9 GB açık), **Parquet** (Hugging Face), **delta export** (son 14 gün, günlük) ([OFF data](https://world.openfoodfacts.org/data)). 2026-09-24'te CSV dosyası 1,27 GB idi, `Last-Modified: 23 Sep 2026` (kendi HEAD isteğim).
- Parquet: Hugging Face `openfoodfacts/product-database`, ~4,83 M satır (food + beauty) ([HF dataset](https://huggingface.co/datasets/openfoodfacts/product-database)). Uzaktan DuckDB ile sorgulamayı denedim; HF **HTTP 429** ile kesti → Parquet'i tek seferde indirip yerelde sorgulamak gerekiyor.
- **Önerilen mirror deseni [değerlendirme]:**
  1. İlk yükleme: JSONL/CSV'den **Türkiye alt kümesi** (`code LIKE '869%' OR countries_tags ∋ en:turkey`) + istenirse tüm dünya → PostgreSQL.
  2. Günlük job: delta export'u uygula (14 gün penceresi var, bir gün kaçarsa tolere eder).
  3. Barkod mirror'da yoksa → OFF canlı API (istemci veya backend, rate-limit bütçesiyle) → sonucu cache'le.
  4. Hâlâ yoksa → "ürün bulunamadı" akışı (bölüm 3).
  - Faydası: rate-limit'ten bağımsız, düşük gecikme, offline test edilebilir, kendi alerjen katmanını (bölüm 4) önceden hesaplayabilirsin.

### 1.4 Taxonomy ve skor alanları
- Taxonomy'ler `openfoodfacts-server/taxonomies` altında düz metin DAG dosyaları ([OFF taxonomies](https://wiki.openfoodfacts.org/Global_taxonomies), [GitHub repo](https://github.com/openfoodfacts/openfoodfacts-server)).
- Alerjen tespiti: `allergens.txt` eş anlamlıları + `ingredients.txt` içindeki `allergens:en:` özelliği/ebeveyn zinciri ([OFF issue #3297](https://github.com/openfoodfacts/openfoodfacts-server/issues/3297)). Örn. `casein` girdisinin `tr: Kazein` çevirisi ve `milk proteins → dairy` ebeveyni var ([ingredients.txt](https://raw.githubusercontent.com/openfoodfacts/openfoodfacts-server/main/taxonomies/food/ingredients.txt)).
- Ürün alanları: `allergens_tags`, `traces_tags`, `ingredients_text_<lc>`, `ingredients` (parse edilmiş, `is_in_taxonomy` ile), `unknown_ingredients_n`, `nutriscore_grade/score`, `nova_group`, `states_tags` (tamlık durumları). Parquet şemasında Eco-Score alanı `environmental_score_*` adını taşıyor; API cevabı hâlâ `ecoscore_grade` döndürdü (kendi testim). Eco-Score 2024 sonunda **Green-Score** adını aldı ([OFF Green-Score](https://us.openfoodfacts.org/green-score)).
- **Türkçe destek ölçümü (kendi analizim, `main` dalı, 2026-09-24):**
  - `allergens.txt`: **0 adet `tr:` satırı**; karşılaştırma: AB dillerinin çoğunda ~15 satır ([allergens.txt](https://raw.githubusercontent.com/openfoodfacts/openfoodfacts-server/main/taxonomies/allergens.txt)).
  - `ingredients.txt`: ~5.600 girdiden **~502'sinde Türkçe** karşılık var; Fransızca ~4.000, Almanca ~3.150 ([ingredients.txt](https://raw.githubusercontent.com/openfoodfacts/openfoodfacts-server/main/taxonomies/food/ingredients.txt)). Temel alerjen kelimeleri (fındık, yer fıstığı, buğday, soya, susam, kazein) mevcut.
  - Parser'daki "may contain" (içerebilir) regex listesinde **Türkçe yok** ([IngredientsStrings.pm](https://raw.githubusercontent.com/openfoodfacts/openfoodfacts-server/main/lib/ProductOpener/IngredientsStrings.pm)). Yani "eser miktarda X içerebilir" cümlesinden `traces_tags` otomatik çıkmıyor; mevcut traces verisi büyük ihtimalle kullanıcıların elle girdiği değerler **[değerlendirme]**.
  - Bu sorun Türkçeye özel değil: OFF, ABD'de yaygın ifadeler tanınmadığı için **12.419 ABD ürününde alerjen uyarısının eksik** olduğunu kendi issue'sunda raporluyor ([OFF issue #14657](https://github.com/openfoodfacts/openfoodfacts-server/issues/14657)).

### 1.5 Write API ve kullanıcı katkısı
- Yazma işlemleri kimlik doğrulaması istiyor; `POST /cgi/product_jqm2.pl` + `user_id`/`password` ([OFF API tutorial](https://openfoodfacts.github.io/openfoodfacts-server/api/tutorial-off-api/)).
- Uygulamalar için **tek global hesap** + her yazmada `app_name`, `app_version`, `app_uuid` (kullanıcı başına salt'lı UUID; moderatörler sorunlu kullanıcıyı uygulamanın tamamını banlamadan engelleyebilsin diye) ([OFF API intro](https://openfoodfacts.github.io/openfoodfacts-server/api/)).
- OFF, Keycloak/OIDC'ye geçiyor; kullanıcı adı/şifre yöntemi geriye dönük uyum için kalacak ([OFF API intro](https://openfoodfacts.github.io/openfoodfacts-server/api/)).
- Görsel yükleme sonrası OFF'un kendi hattı çalışıyor: Google Cloud Vision OCR → Robotoff tahminleri (insights) → topluluk doğrulaması ([Robotoff mimari](https://openfoodfacts.github.io/robotoff/introduction/architecture/)).
- OFF, kullanıcı katkısı alan uygulamalardan bu katkıları geri göndermesini bekliyor ([OFF data/SDK sayfası](https://world.openfoodfacts.org/data)).
- **[değerlendirme]** Crowdsourcing döngüsü: kullanıcı ürün bulamazsa 2 foto çeker (ön + içindekiler/besin tablosu) → bizim LLM çıkarımımız anında sonuç verir → aynı fotoğraflar + (kullanıcı onaylı) metin staging'de test edilip production OFF'a yazılır. Güvenlik: yazma yalnızca backend'den, global hesabın şifresi istemcide asla durmamalı.

### 1.6 Türkiye kapsaması — ölçülen rakamlar (2026-09-24)

**Kaynak A — OFF canlı API facet sayımları** (`countries_tags=en:turkey`, v2 search, [OFF Turkey sayfası](https://world.openfoodfacts.org/country/turkey)):

| Metrik | Sayı | Oran |
|---|---|---|
| Türkiye etiketli ürün | **11.411** | — |
| `ingredients-completed` | 2.832 | **%24,8** |
| `nutrition-facts-completed` | 5.937 | %52,0 |
| Nutri-Score bilinen (a–e) | ≤ 2.990 (unknown: 8.421) | ≤ %26,2 |
| `product-name-completed` | 7.121 | %62,4 |
| `photos-uploaded` | 9.479 | %83,1 |
| `complete` (her şey tam) | 14 | %0,1 |

**Kaynak B — OFF nightly CSV export (23 Eyl 2026) üzerinde kendi filtrem** ([CSV linki](https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz)):

| Alt küme | Ürün | İçindekiler metni dolu | Besin tablosu tam | Nutri-Score a–e | NOVA | İçindekiler fotoğrafı |
|---|---|---|---|---|---|---|
| Barkod `869…` (Türkiye GS1 öneki) | **19.375** | 2.808 (**%14,5**) | 11.546 (%59,6) | 3.300 (%17,0) | 1.896 (%9,8) | 4.685 (%24,2) |
| `countries_tags ∋ en:turkey` | 7.882 | 1.377 (%17,5) | 4.896 (%62,1) | 1.597 (%20,3) | 842 (%10,7) | 2.014 (%25,6) |
| Birleşim | 22.322 | 3.309 (%14,8) | 13.082 (%58,6) | 3.821 (%17,1) | 2.205 (%9,9) | — |

- `869` önekli ürünlerin 14.440'ı Türkiye etiketi taşımıyor; en çok Fransa (5.292), Almanya (1.493), Irak (880) etiketli → bunlar büyük ölçüde **ihraç ürünleri** ve içindekiler başka dilde olabilir.
- Yıllık yeni `869` kayıtları: 2024'te 3.090, 2025'te 3.956, 2026'da (23 Eyl'e kadar) 1.948 → veri tabanı büyüyor ama yavaş.
- **Tutarsızlık notu:** API "Türkiye" için 11.411 derken CSV'de 7.882 satır çıktı. Nedenini çözemedim (export'un kapsam farkı olabilir). İki kaynak da **içindekiler doluluğunu %15–25 aralığında** gösteriyor; kararı bu aralık üzerinden vermek güvenli.
- **Bağlam:** TÜBİTAK'ın marketfiyati.org.tr'si zincir marketlerde **~50.000 ürün** listeliyor ([TÜBİTAK duyurusu](https://tubitak.gov.tr/tr/haber/zincir-market-fiyatlarina-aninda-erisimin-onu-acildi)). OFF'ta içindekiler metni dolu ~3.300 Türkiye ürünü var; ikisinin kesişimini ölçemedim, ama **[değerlendirme]** markette rastgele okutulan bir üründe içindekilerin hazır gelme ihtimali düşük.

**Alerjen etiketleme kalitesi — API örneklemi** (Türkiye + ingredients-completed; API varsayılan sıralamasıyla ilk 600 ürün, 380'inde `ingredients_lc=tr`; basit anahtar kelime eşleştirmesi, sonuçlar yaklaşık):

| İçindekilerde geçen | Ürün | `allergens_tags` içinde ilgili tag yok |
|---|---|---|
| Süt/peynir/tereyağı/peyniraltı… | 145 | 29 (~%20) |
| Fındık/badem/ceviz/kaju | 58 | 14 (~%24) |
| Yumurta | 35 | 5 |
| "içerebilir / eser miktar / iz miktar" ifadesi | 49 | `traces_tags` boş: 12 (~%24) |

- Parse edilemeyen içindekiler oranı (`unknown_ingredients_n / ingredients_n`): **medyan %67**; ürünlerin %93'ünde >%20 bilinmeyen; yalnız %6'sında sıfır.
- Somut örnekler (canlı API, 2026-09-24):
  - [8682615108467](https://world.openfoodfacts.org/product/8682615108467): "Hurma, **süt proteini** konsantresi, **yer fıstığı %17**, **peyniraltı suyu** proteini…" → `allergens_tags: []`. 8 bileşenden 7'si bilinmiyor; `yer fıstığı %17` → `tr:yer-fıstığı-17` diye parse edilmiş. **[değerlendirme]** Türkçedeki "%17" (yüzde işareti önde) biçimi ya parser'da desteklenmiyor ya da ürün yeniden işlenmemiş.
  - [8719200750593](https://world.openfoodfacts.org/product/8719200750593): alerjen `tr:Yağsız Pastörize Süt` olarak girilmiş, `en:milk`'e bağlanmamış. `en:milk` ile filtreleyen bir uygulama bunu kaçırır.
  - [8691381000486](https://world.openfoodfacts.org/product/8691381000486) (doğal maden suyu + karbondioksit) → `nova_group: 4`. Türetilmiş skorlarda da hata var.
- **Sonuç:** OFF'un `allergens_tags` alanı Türk ürünleri için **"güvenli" kararının tek dayanağı olamaz**. Ham `ingredients_text_tr` + kendi alerjen motorumuz gerekir (bölüm 4).

---

## 2. Alternatif / tamamlayıcı kaynaklar

| Kaynak | Ne veriyor | Erişim / maliyet | Türkiye barkodu + içindekiler? | Hüküm |
|---|---|---|---|---|
| **USDA FoodData Central** | Branded Foods, Foundation, SR Legacy… | Ücretsiz key, 1.000 istek/saat/IP; **CC0** ([FDC API guide](https://fdc.nal.usda.gov/api-guide/)) | "ulker" araması 2 sonuç verdi, ikisi de `marketCountry: United States` (kendi testim). ABD pazarı. | 🔴 barkod için / 🟢 jenerik besin değeri için |
| **GS1 Türkiye / Verified by GS1** | 7 temel alan: GTIN, marka, açıklama, görsel, GPC, net miktar, satış ülkesi ([GS1 UK VbG](https://www.gs1uk.org/standards-services/data-services/verified-by-gs1), [özet](https://www.barcode.graphics/verified-by-gs1/)) | API yalnız anahtar verilen üyelere/partnerlere ([GS1 UK](https://www.gs1uk.org/standards-services/data-services/verified-by-gs1)); GS1TR ürün doğrulama perakendeci/e-pazaryeri odaklı ve giriş istiyor; TOBBsenkron GDSN veri havuzu B2B ([GS1TR ürün doğrulama](https://urunkimlikkarti.gs1tr.org/)) | İçindekiler/alerjen **yok** (7 alan). Ürün adı/marka doğrulaması için faydalı olabilir. | 🔴 (öğrenci projesi erişimi belirsiz) |
| **TürKomp** | 645 gıda × 100 bileşen, ~63.000 değer; ulusal ve resmi ([TÜBİTAK MAM](https://mam.tubitak.gov.tr/en/turkeys-national-food-composition-database/), [TürKomp hakkında](https://turkomp.tarimorman.gov.tr/about)) | Ücretsiz web, kişisel kullanım ([TürKomp veri kullanımı](https://turkomp.tarimorman.gov.tr/useofdata)); sayfa fetch'te redirect döngüsüne girdi, uygulamada kullanım koşullarını doğrulayamadım | **Barkodsuz**, jenerik gıda (ekmek, beyaz peynir…). Paketli ürün değil. | 🟡 manuel "jenerik gıda" girişi için; izin yazılı teyit edilmeli |
| **FatSecret Platform** | Global besin DB, barkod | Basic 5.000 çağrı/gün ücretsiz; **Premier Free öğrencilere açık ama yalnız ABD verisi**; 62+ ülke yalnız ücretli Premier ([FatSecret editions](https://platform.fatsecret.com/api-editions)) | Türkiye veri seti ücretli Premier'de bile açıkça listelenmemiş | 🔴 |
| **Edamam Food DB** | 700k+ UPC/EAN | Ücretsiz tier yok; $14/ay'dan başlıyor; atıf zorunlu ([Edamam](https://developer.edamam.com/food-database-api)) | Coğrafi kapsam belirtilmemiş | 🔴 (maliyet + belirsiz TR kapsamı) |
| **Nutritionix** | ~1,9M kalem, ABD market/restoran | Kurumsal plan $1.850/ay'dan ([Suggestic listesi](https://blog.suggestic.com/food-api-ultimate-list)); resmi sayfa fetch'te 402 döndü | ABD odaklı | 🔴 |
| **marketfiyati.org.tr** (TÜBİTAK BİLGEM) | ~50k ürün, 7 zincir (BİM, A101, ŞOK, Migros, CarrefourSA, Hakmar, "Tarım Kooperatif"), barkodla fiyat ([TÜBİTAK](https://tubitak.gov.tr/tr/haber/zincir-market-fiyatlarina-aninda-erisimin-onu-acildi), [haber](https://www.trthaber.com/haber/ekonomi/tek-tikla-market-fiyati-donemi-50-bin-urun-karsilastiriliyor-934814.html)) | Frontend `api.marketfiyati.org.tr/api/v1–v3`'e çağrı yapıyor (JS bundle'da gördüm); topluluk projeleri bunu anahtarsız kullanıyor ([örnek](https://github.com/realkq/foca-kantin-fiyat)). **Kullanım Koşulları:** içeriğin TÜBİTAK BİLGEM'in **yazılı izni olmadan** kopyalanması, işlenmesi ya da herhangi bir amaçla kullanılması yasak ([Kullanım Koşulları](https://marketfiyati.org.tr/kullanim-kosullari)) | Fiyat + ad + görsel; içindekiler yok (gördüğüm kadarıyla) | 🔴 izinsiz / 🟡 **yazılı izin istenirse** (TÜBİTAK projesi olarak başvurmaya değer) |
| **Market e-ticaret siteleri (scraping)** | İçindekiler çoğu zaman ürün sayfasında var | [değerlendirme] Site ToS'ları, bot korumaları, sayfa yapısı değişince kırılma; üstüne 5846 FSEK/veri tabanı hakları. LLM ile çıkarım teknik olarak kolay: ürün sayfasından içindekiler/besin tablosu çıkarımında %95–98 doğruluk raporlanmış ([arXiv 2506.21585](https://arxiv.org/html/2506.21585v1)) | Var ama hukuken riskli | 🔴 canlı ürün için |

**Bölüm sonucu:** Türkiye'de paketli ürün içindekiler/alerjen verisi için **OFF dışında açık ve yasal bir kaynak bulamadım**. Boşluğu kullanıcı fotoğrafı + LLM + OFF'a geri besleme kapatacak.

---

## 3. Veri boşluğu: etiket fotoğrafından çıkarım

### 3.1 Güncel yaklaşımlar
- **OFF'un kendi hattı:** Google Cloud Vision OCR → Robotoff ([mimari](https://openfoodfacts.github.io/robotoff/introduction/architecture/)).
  - İçindekiler tespiti: xlm-roberta-large'dan fine-tune edilmiş sequence tagging, ~5.000 metin ([ingredient detection](https://openfoodfacts.github.io/robotoff/references/predictions/ingredient-detection/)).
  - Besin tablosu: LayoutLMv3, 3.500+ etiketli görsel, 60+ besin sınıfı ([nutrient extraction](https://openfoodfacts.github.io/robotoff/references/predictions/nutrient-extraction/)).
  - OCR hatalarını düzeltmek için fine-tune edilmiş Mistral-7B: F1 0,65, veri tabanındaki tanınmayan içerik sayısında -%11 ([TDS yazısı, Eki 2024](https://towardsdatascience.com/how-did-open-food-facts-use-open-source-llms-to-enhance-ingredients-extraction-d74dfe02e0e4/)).
  - İki modelin sayfasında da Türkçe performansı belirtilmemiş.
- **Klasik OCR, Türkçe etikette zayıf:** HalalBench (1.043 görsel, 14 dil, Türkçe dahil; 993'ü sentetik) üzerinde en iyi motor docTR, genel F1 0,193; **Türkçe en iyi F1 0,035**. ML Kit v2 de test edilenler arasında ([HalalBench, arXiv 2604.22754](https://arxiv.org/html/2604.22754)). Hata türleri: küçük punto (%30,6), çok dilli panel karışması (%22,2), silindirik ambalaj bozulması (%19,4).
- **Vision LLM:** İki dilli (Arapça/İngilizce) 294 etiketlik bir çalışmada GPT-4o, GPT-4V ve Gemini'yi geçti; post-processing sonrası Jaccard GPT-4o için %17,8 → %71,6, Gemini için %11,2 → %64,8 ([J. Imaging 2025, PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12387780/)). İngilizce, Arapçadan iyi çıktı.
- **Türkçe paketli ürün etiketi için yayınlanmış vision-LLM doğruluk ölçümü bulamadım.** Bu bir risk, ama aynı zamanda proje için ölçülebilir bir katkı: 100–200 Türkçe etiketlik küçük bir eval seti.

### 3.2 Maliyet (çağrı başına, yaklaşık)
- Claude'da görsel maliyeti: `⌈w/28⌉ × ⌈h/28⌉` görsel token. 1000×1000 px ≈ 1.296 token. Standart tier en fazla 1.568 token; yüksek çözünürlük tier (Claude 4.7+) en fazla 4.784 token ([Claude vision docs](https://platform.claude.com/docs/en/build-with-claude/vision)).
- Fiyatlar: Haiku 4.5 $1 / $5, Sonnet 5 $2 / $10 (1M token başına, giriş/çıkış) (Claude API model tablosu, 2026-06 önbelleği; [pricing](https://platform.claude.com/docs/en/about-claude/pricing)).
- **Hesap [değerlendirme, varsayım: 1 fotoğraf + ~700 token prompt + ~500 token JSON çıktı]:**
  - Haiku 4.5, 1000×1000 foto: ~2.000 giriş → $0,002 + 500 çıkış → $0,0025 ≈ **$0,005/çağrı**.
  - Sonnet 5, 2000×1500 foto (3.888 token): ~4.600 giriş → $0,009 + 500 çıkış → $0,005 ≈ **$0,015/çağrı**.
  - Ayda 1.000 "ürün bulunamadı" çağrısı ≈ **$5–15**. Maliyet belirleyici değil; asıl mesele doğruluk.
- Google Gemini: 3.5 Flash-Lite $0,30 / $2,50, 3.5 Flash $1,50 / $9,00; ücretsiz tier var ([Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)). Görsel başına token sayısını bu kaynakta doğrulamadım.

### 3.3 Önerilen desen [değerlendirme]
1. Kullanıcı ön yüz + içindekiler + besin tablosu fotoğraflarını çeker. İstemci kırpmayı ve netliği kontrol eder; bulanıksa tekrar ister.
2. Vision LLM structured output (JSON schema) üretir: `ingredients_text_tr`, `allergens_declared` (etikette kalın/altı çizili olanlar), `may_contain`, besin tablosu (100 g başına), ve her alan için "okunabildi mi".
3. Çıktı kural motorundan (bölüm 4) geçer. LLM çıktısına **doğrudan "güvenli" kararı verdirilmez**.
4. Kullanıcı metni onaylar/düzeltir. Onaylanan veri ürün tablomuza girer ve OFF'a geri yazılır (1.5).
5. Aynı barkod sonraki kullanıcılarda artık "bulundu" olur. Crowdsourcing bu şekilde ağ etkisi yaratır.

---

## 4. Alerjen tespiti doğruluğu

### 4.1 Zorluklar (Türkçe)
- **Yasal zemin:** Türk Gıda Kodeksi Etiketleme Yönetmeliği'ne göre alerjenler içindekiler listesinde kalın, altı çizili ya da farklı renkle vurgulanmalı ([Besin Alerjisi Derneği](https://besinalerjisi.org.tr/alerjen-etiketleme-kurallari/), [Yönetmelik, RG 26.01.2017](https://www.resmigazete.gov.tr/eskiler/2017/01/20170126M1-6.htm)). **"Eser miktarda … içerebilir" beyanı isteğe bağlı**; kapsamlı risk değerlendirmesi sonucu bulaşma kaçınılmazsa yapılabilir ([Besin Alerjisi Derneği](https://besinalerjisi.org.tr/alerjen-etiketleme-kurallari/), [Lexpera – kılavuz](https://www.lexpera.com.tr/resmi-gazete-disindaki-kaynak/metin/turk-gida-kodeksi-gida-etiketleme-ve-tuketicileri-bilgilendirme-yonetmeligi-kilavuzu)).
  - **Kritik sonuç:** Etikette "içerebilir" yazmaması ürünün iz miktarda alerjen içermediği anlamına **gelmez**.
- **Uluslararası kanıt:** Uyarı (PAL) ile gerçek bulaşma arasında korelasyon yok. PAL'lı ürünlerin çoğunda alerjen çıkmıyor, PAL'sız ürünlerde ise klinik düzeyde alerjen bulunabiliyor. Alerjik tüketicilerin %8'e kadarı PAL'lı ürünle reaksiyon bildirmiş ([WAO Journal 2024 – ACT-UP](https://www.worldallergyorganizationjournal.org/article/S1939-4551(24)00104-2/fulltext), [PMC anket](https://pmc.ncbi.nlm.nih.gov/articles/PMC12073677/)).
- **Dil zorlukları (örnekler bölüm 1.6'daki verilerden):**
  - Türev adlar: kazein/kazeinat, peyniraltı suyu (tozu), laktoz, süt proteini konsantresi, tereyağı altı suyu → süt.
  - Yazım varyantları: "peynir alti sw", "seker", "i̇çerir" (noktalı İ Unicode sorunu), "sütyağı / süt yağı".
  - Tuzak eşleşmeler: "hindistan cevizi" ≠ ağaç yemişi (AB listesinde değil), "karabuğday" ≠ gluten, "glutensiz yulaf", "kakao yağı" ≠ süt.
  - Bileşik ifadeler: "fındık püresi (%13)", "yer fıstığı %17".
  - Tek etikette çok dil (TR/EN/AR).
  - E-kodları: E322 lesitin (soya kaynaklı olabilir), E1105 lizozim (yumurta). Kaynak belirtilmezse belirsizlik var. **[değerlendirme]** E-kodu→alerjen eşlemesi "olası" seviyesinde işaretlenmeli.
- **Literatür:** Türkçe alerjen çıkarımı için yayınlanmış bir benchmark bulamadım.
  - Genel alanda false negative, false positive'ten daha kritik sayılıyor; bir çalışma FN'yi FP'nin 3 katı ağırlıklandırıyor ([OCR+NLP Allergen Notifying System](https://www.researchgate.net/publication/389057385_OCR_and_NLP_based_Personalized_Allergen_Notifying_System)).
  - Gıda metni sınıflandırmada en iyi sistemler bile macro-F1 ~0,82 civarında ([SemEval-2025 Task 9](https://food-hazard-detection-semeval-2025.github.io/), [özet](https://arxiv.org/pdf/2503.19800)).
  - LLM'lerle bileşik malzeme ayrıştırması (GPT-4o, Llama-3, Mixtral) üzerine çalışmalar var ([arXiv 2411.05892](https://arxiv.org/pdf/2411.05892)).

### 4.2 Önerilen hibrit mimari [değerlendirme]
1. **Normalizasyon:** Türkçe küçük harf (İ/ı doğru), diakritik varyantları, yüzde/parantez temizliği, "(süt ürünü)" gibi açıklamaları koruma.
2. **Kural + sözlük katmanı (deterministik, birincil):** 14 AB/TR alerjen grubu × Türkçe eş anlamlı/türev sözlüğü (OFF `ingredients.txt`'deki `tr:` girdilerinden başla, genişlet), negatif listeler (hindistan cevizi, karabuğday, glutensiz…), "içerebilir/eser/iz miktarda/aynı hatta" kalıpları → traces.
3. **LLM katmanı (ikincil):** Yalnızca sözlüğün tanımadığı token'lar için "bu bileşen şu alerjen gruplarından birini içerebilir mi?" sorusu. Cevap kaynak cümleyle birlikte döner. LLM tek başına "güvenli" diyemez; en fazla **ek risk** ekleyebilir (monoton: risk sadece artar).
4. **Karar durumları (3 değil 4 durum):**
   - 🔴 **İçeriyor**: alerjen içindekilerde açıkça var.
   - 🟠 **İz / çapraz bulaşma riski**: "içerebilir" var ya da E-kodu belirsiz.
   - ⚪ **Emin değilim**: bilinmeyen bileşen oranı eşik üstünde, OCR güveni düşük, veri OFF'tan ve doğrulanmamış, ya da içindekiler yok.
   - 🟢 **Tespit edilmedi**: asla "güvenli" kelimesi değil. Metin "Etikette X bulunamadı, paketi kontrol edin" olmalı.
5. **Kaynak gösterme:** Her kararda tetikleyen kelime vurgulanır, veri kaynağı (OFF / kullanıcı fotoğrafı / LLM), son güncelleme tarihi ve "etiketi kontrol et" çağrısı gösterilir.
6. **Eşikler FN'yi minimize edecek şekilde:** Belirsizlikte "Emin değilim"e düş. Değerlendirmede recall (duyarlılık) birincil metrik olmalı. Bunu `plan/kararlar.md`'ye bir tasarım ilkesi olarak yazmayı öner.
7. **Test seti:** OFF Türkiye alt kümesinden 200–300 ürünü elle etiketle (altın standart) ve regresyon testi olarak CI'da çalıştır.

---

## 5. Barkod tarama

| Platform | Seçenek | Durum |
|---|---|---|
| Android native / cross-platform | **Google ML Kit Barcode**: EAN-8/13, UPC-A/E dahil; tamamen on-device, offline ([ML Kit](https://developers.google.com/ml-kit/vision/barcode-scanning)). **Google Code Scanner**: kamera izni gerektirmez ([ML Kit](https://developers.google.com/ml-kit/vision/barcode-scanning)) | 🟢 |
| iOS native | **VisionKit DataScannerViewController**: iOS 16+, A12 Bionic+ ([WWDC22](https://developer.apple.com/videos/play/wwdc2022/10025/), [Apple docs](https://developer.apple.com/documentation/visionkit/scanning-data-with-the-camera)); ML Kit iOS'ta da var | 🟢 |
| React Native / Flutter | ML Kit/VisionKit sarmalayan kütüphaneler ([Margelo RN rehberi 2026](https://margelo.com/blog/react-native-barcode-scanner)) | 🟢 |
| Web — BarcodeDetector API | Chrome Android 83+ tam; masaüstü Chrome yalnız macOS/ChromeOS; **Safari (iOS dahil) yalnız flag arkasında, Firefox yok**; deneysel ([MDN BCD verisi](https://github.com/mdn/browser-compat-data/blob/main/api/BarcodeDetector.json), [MDN](https://developer.mozilla.org/en-US/docs/Web/API/BarcodeDetector)) | 🟡 |
| Web — WASM | **zxing-wasm** (ZXing-C++), **barcode-detector** polyfill (aynı API'yi WASM ile sağlar) ([zxing-wasm](https://github.com/Sec-ant/zxing-wasm), [iOS WASM yazısı](https://dev.to/ilhannegis/barcode-scanning-on-ios-the-missing-web-api-and-a-webassembly-solution-2in2)) | 🟢 (iOS için zorunlu yol) |
| Web — ticari SDK | Scanbot, Dynamsoft vb. (lisans ücretli; fiyatlarına bakmadım) | — |

**PWA mı, native mi? [değerlendirme]**
- PWA ile yapılabilir: `getUserMedia` + barcode-detector polyfill her iki platformda çalışır. Ancak iOS'ta PWA kamera deneyimi, arka plan ve bildirim davranışı native'den zayıf.
- Market koridorunda hızlı ve tekrarlı tarama, offline cache ve fotoğraf çekimi (bölüm 3) ağırlıklı bir akış olduğu için **cross-platform mobil (React Native veya Flutter) + Spring Boot backend** daha az sürprizli.
- Bu bir ekip/yetkinlik kararı. Levent'e sorulacak (bölüm 8).

---

## 6. "Alışveriş alışkanlığı" için veri kaynakları

| Kaynak | Gerçekçilik | Not |
|---|---|---|
| **Tarama geçmişi** (+ "bunu aldım" butonu) | 🟢 | Sıfır dış bağımlılık; kategori, Nutri-Score ve alerjen trendleri buradan üretilir. Tarama ≠ satın alma; ayrımı kullanıcıya sordurmak gerekir [değerlendirme]. |
| **Manuel alışveriş listesi** | 🟢 | Basit, düşük değerli ama güvenilir. |
| **Fiş (ÖKC) fotoğrafı OCR** | 🟡 | 2026'da aynı gün 12.000 TL'ye kadar satışta ÖKC fişi düzenlenebiliyor ([birfatura](https://birfatura.com/fatura-kesme-siniri-kac-tl/), [Paraşüt](https://www.parasut.com/blog/e-fatura-ve-e-arsiv-zorunlulugu)), yani market alışverişlerinin büyük çoğunluğu fiş. [değerlendirme] Fiş satırları kısaltmalı ("ULKR CIK GOFRET") ve barkod içermez; ürün eşleştirmesi bulanık kalır. Vision LLM ile satır çıkarımı mümkün, eşleşme güveni düşük. "Stretch goal" seviyesi. |
| **e-Arşiv / e-Fatura** | 🔴 | e-Arşiv faturayı görmek için düzenleyenin alıcıya e-posta göndermesi gerekiyor; portal, adınıza düzenlenen faturaların yalnız listesini gösteriyor, içeriğini göstermiyor ([MDP Group](https://mdpgroup.com/blog/tarafiniza-duzenlenen-e-arsiv-faturalar-nasil-goruntulenir/)). Market fişlerinin çoğu zaten e-Arşiv değil. Programatik tüketici erişimi bulamadım. |
| **Market sadakat programı entegrasyonu** (Migros Money vb.) | 🔴 | Harcama geçmişi uygulama içinde görülüyor, ama **herkese açık geliştirici API'si bulamadım** ([Money SSS](https://www.money.com.tr/mc/iletisim/sikca-sorulan-sorular/69)). Yalnız kurumsal anlaşmayla mümkün olabilir; bitirme projesi takvimine sığmaz [değerlendirme]. |
| **marketfiyati.org.tr fiyat verisi** | 🟡 (izinle) | "Aldığın ürünün daha ucuzu" gibi özellikler için cazip, ancak Kullanım Koşulları yazılı izin istiyor ([Kullanım Koşulları](https://marketfiyati.org.tr/kullanim-kosullari)). |

---

## 7. Sonuç

### 7.1 Genel hüküm: **🟡 SARI — teknik olarak mümkün, ama veri tarafı "hazır" değil.**
Barkod okuma ve backend çözülmüş problemler. Projenin gerçek mühendislik değeri ve riski iki yerde:
1. Türkçe içindekiler verisinin eksikliği (%75–85 ürün içindekilersiz).
2. Türkçe alerjen çıkarımının güvenilirliği.

Bu iki konu projenin **ana katkısı** olarak konumlandırılırsa bitirme projesi için güçlü bir hikâye olur [değerlendirme].

### 7.2 En büyük 5 teknik risk ve azaltma yolları

| # | Risk | Neden kırılır | Azaltma |
|---|---|---|---|
| 1 | **Alerjik kullanıcıya yanlış "güvenli" (false negative)** | OFF `allergens_tags` Türk ürünlerinde eksik (~%20–24 örneklemde); parser Türkçe "içerebilir"i tanımıyor; TR'de PAL isteğe bağlı | Kendi kural+sözlük motoru; LLM yalnız risk ekler; 4 durumlu karar ("Emin değilim" dahil); "güvenli" kelimesi yok; kaynak + vurgu gösterimi; recall odaklı altın test seti |
| 2 | **Kapsama boşluğu: ürün yok ya da içindekiler yok** | OFF'ta Türkiye ürünlerinin yalnız %15–25'inde içindekiler var | Foto → vision LLM → kullanıcı onayı → kendi DB + OFF'a geri yazma; ilk demo için ekip olarak 1–2 market rafını önceden doldurma [değerlendirme] |
| 3 | **Rate limit / dış servis kesintisi** | Backend tek IP'den 15/dk; OFF zaman zaman HTML hata sayfası dönüyor | Nightly JSONL + günlük delta mirror; canlı API sadece miss'te; cache; circuit breaker; istemci tarafı fallback |
| 4 | **Türkçe etiket OCR/LLM doğruluğu bilinmiyor** | Klasik OCR Türkçede F1 0,035 (HalalBench); vision LLM'in Türkçe ölçümü yok | Proje içinde 100–200 etiketlik eval seti; çekim yönlendirmesi (kırp, netlik kontrolü); alan bazlı güven skoru; kullanıcı onayı zorunlu |
| 5 | **Hukuk: KVKK + lisanslar** | Alerji/sağlık bilgisi özel nitelikli kişisel veri; 7499 sayılı Kanun'la md. 6 ve yurt dışı aktarım (md. 9) 1 Haziran 2024'te değişti ([KVKK değişiklik metni](https://kvkk.gov.tr/SharedFolderServer/CMSFiles/4eba766b-7425-4cd4-97f5-cb09c4cf4ef9.pdf), [Erdem & Erdem](https://www.erdem-erdem.av.tr/bilgi-bankasi/kisisel-verilerin-korunmasi-kanununda-neler-degisti)); yurt dışı LLM API'sine veri gitmesi; ODbL share-alike; marketfiyati izni | Profil verisini LLM'e **göndermemek** (LLM'e yalnız etiket fotoğrafı gider, karar backend'de verilir); açık rıza + aydınlatma metni; veri minimizasyonu; ODbL ürün tablosunu ayrı tutmak; marketfiyati için yazılı izin ya da o özellikten vazgeçmek |

### 7.3 Sıradaki tek adım (öneri)
Levent'le 15 dakika: aşağıdaki açık soruları netleştir. Ardından `plan/kararlar.md`'ye ilk iki karar: (a) OFF mirror + delta; (b) "güvenli" demeyen 4 durumlu alerjen kararı.

---

## 8. Levent'e açık sorular (varsayım yapmadım)
1. MVP'de hedef platform: yalnız mobil mi, PWA mı, ikisi mi? Ekibin RN/Flutter/Kotlin/Swift deneyimi var mı?
2. Eski MVP hangi veri kaynağını kullanıyordu, ne kadar ürün kapsıyordu? Eski DB'de elle girilmiş Türk ürünü verisi var mı?
3. "Canlıya almak" tanımı: mağaza yayını (App Store/Play) mı, sınırlı beta mı? Gerçek alerjik kullanıcıyla test planlanıyor mu? (Etik/sorumluluk metni gerekir.)
4. LLM API'si için bütçe veya kurum hesabı var mı?
5. Danışman (Taha Yiğit Alkan) ürünün "sağlık tavsiyesi" sınırı ve KVKK konusunda bir beklenti belirtti mi?
6. marketfiyati.org.tr ya da GS1 Türkiye'ye üniversite üzerinden resmi başvuru yapmak ekip için gerçekçi mi?

---

## Ek: Metodoloji (kendi ölçümlerim, 2026-09-24)
- **OFF API facet sayımları:** `GET https://world.openfoodfacts.org/api/v2/search?countries_tags=en:turkey&states_tags=<state>&fields=code&page_size=1` → `count`. User-Agent: `NutriScanResearch/0.1 (...)`. Arama limitine uyuldu (istekler arası 8–20 sn).
- **CSV analizi:** `en.openfoodfacts.org.products.csv.gz` (1,27 GB, Last-Modified 23 Eyl 2026) diske yazılmadan stream edildi; `code ^869` veya `countries_tags ~ en:turkey` satırları (22.322) DuckDB ile sayıldı.
  - "İçindekiler dolu" = `ingredients_text` boş değil.
  - **Uyarı:** CSV'nin `allergens` sütunu API'deki `allergens_tags` ile tutarsız çıktı (8 ürünlük kontrolde 5'i API'de `en:milk` içeriyordu). Bu yüzden alerjen boşluğu oranlarını **yalnız API örnekleminden** raporladım.
- **Alerjen örneklemi:** API'den Türkiye + `ingredients-completed` ilk 6 sayfa × 100 = 600 ürün; `ingredients_lc=tr` olan 380'inde Türkçe anahtar kelime regex'i (süt/peynir/tereyağı/kazein/laktoz…; fındık/badem/ceviz (hindistan cevizi hariç)/kaju; yumurta) ile "içerikte geçiyor ama tag yok" sayıldı. Örnekler elle bakıldı. Regex'in yanlış pozitifleri var (ör. karabuğday, glutensiz, İngilizce metinler); oranları **yaklaşık** okuyun.
- **Taxonomy sayımları:** GitHub `main` dalından raw dosyalar; `allergens.txt` satır başı dil kodu sayımı; `ingredients.txt` boş satırla ayrılmış bloklarda `tr:` satırı olanlar; `IngredientsStrings.pm` içinde `%may_contain_regexps` dil anahtarları.
- **Hugging Face Parquet** uzaktan sorgusu HTTP 429 ile başarısız oldu. Bu dosyadan rakam kullanmadım (yalnız satır sayısı ve şema).
