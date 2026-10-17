# 3. Ingredient semantic matching ve veri kaynakları

**Kısa özet:** Etiketteki her ifade tek bir kimyasal değildir; bu yüzden doğrudan `ingredient -> disease` eşleştirmesi bilimsel olarak fazla basitleştirir. Daha sağlam tasarım, ham etiketi türlendirip önce kavram kimliği ve belirsizliğini, sonra ölçülebilir ürün niteliğini, sonra da condition kuralı ve kanıtı ayrı ayrı çözer. OFF Ingredients Taxonomy, FoodOn, FooDB, CTD ve JECFA farklı görevler için olası girdilerdir; hiçbiri tek başına tüm bu hattı sağlamaz. FooDB’nin açıkça **NC / non-commercial** lisansı, ileride pazara çıkma hedefi için kullanım kapısıdır.

## Araştırma sorusu

**Türkçe/İngilizce ürün etiketi terimlerini hangi adımlar ve kaynaklarla doğru kavramsal kimliğe bağlayabilir, hangi içeriklerin kimyasal kimliğe indirgenemeyeceğini nasıl koruyabiliriz?**

Burada “semantic matching” sadece vektör similarity değildir. Hedef; girdi türünü anlamak, adayları üretmek, kimlik ve bağlamı doğrulamak, belirsizliği saklamak ve bundan sonra uygun evidence/rule kaydına bağlamaktır.

## Kavram katmanları

```text
Ham etiket ifadesi
  -> dil/yazım normalizasyonu
  -> mention türü (ingredient, food/composite, additive, allergen, nutrient, unknown)
  -> canonical food/chemical concept + alias evidence + confidence/ambiguity
  -> ürün verisi (etiket, beyan, besin miktarı, porsiyon, tarih, kaynak)
  -> condition rule (kullanıcıya uygulanabilir ve uzman onaylı)
  -> açıklamalı sonuç veya abstain
```

Bu katmanlar arasındaki fark:

- **Label normalization:** “E102” ve doğrulanmış eş anlamlı terimlerini bir kimliğe yaklaştırma.
- **Food concept linking:** “buğday unu” gibi gıda/kompozit kavramı tanımlama; bu terim tek molekül demek değildir.
- **Chemical identity linking:** ancak açıkça tanımlanabilen katkı/kimyasal için standard identifier bulma.
- **Nutrient data:** karbonhidrat, sodyum vb. sayısal değer ve birim; ingredient listesinde bulunması beklenmez.
- **Disease evidence linking:** kimyasal/food/nutrient ile condition arasında hangi tür yayın veya kılavuz iddiası olduğunu bağlama.
- **Clinical rule evaluation:** sadece uygulanabilir veri ve uzman onayı olan kuralı çalıştırma.

Kişisel beslenme hedefi de bu ingredient eşleşmesinden ayrı tutulmalı. Örneğin “şeker” sözcüğünün kavram eşleşmesi, ürünün toplam karbonhidrat miktarını vermez; ürünün nutrient observation kaydı ile kullanıcının kendi hedef kaydı ayrı kaynaklardan gelir. Porsiyon hesaplanacaksa ürün etiketi değeri ve tüketilen miktar birlikte bulunmalı. Etiket verisinin olmadığı potasyum/fosfor gibi alanlar ingredient embedding’iyle tamamlanmamalı.

## Aday veri kaynaklarının uygunluğu

| Kaynak | İşe yarayabileceği aşama | Sağlamadığı şey | Lisans/uygulama notu |
|---|---|---|---|
| Kendi doğrulanmış etiket kataloğu | Türkiye’deki gerçek ürün adları, içerik, alerjen beyanı, besin tablosu ve kontrol tarihi | Evrensel synonym sözlüğü; etiket miktarından fazlasını | Her alan için label görseli/üretici kaynağı, doğrulayan ve tarih saklayın |
| Open Food Facts `ingredients.txt` | Dil varyantı, alias, kategori ve taxonomy tabanlı aday normalizasyon | Her yerel Türkçe terim veya kimyasal doğruluğu; kullanıcıya özel ürün doğrulaması | Önceki toplantı formunda OFF ürün/barkod kayıtları kapsam dışındaydı. Taxonomy dosyası ayrı bir sözlük adayıdır; ayrı dataset olsa da kullanım ve türev veri koşullarını ayrıca denetleyin. [Dosya](https://github.com/openfoodfacts/openfoodfacts-server/blob/main/taxonomies/food/ingredients.txt), [OFF API/data lisans açıklaması](https://github.com/openfoodfacts/openfoodfacts-server/blob/main/docs/api/index.md) |
| FoodOn | Gıda, kaynak organizma, ham/işlenmiş ürün ve bileşen ilişkileri için kavram/ontology | Türkçe etiket kapsamını, ürünün gerçek formulation’ını veya miktarını | Ontology kavram ağıdır, kimyasal risk kuralı değildir. Core repo CC BY 4.0 belirtir; atıf ve kullandığınız sürümü kaydedin. [FoodOn makalesi](https://www.nature.com/articles/s41538-018-0032-6), [FoodOn repo](https://github.com/FoodOntology/foodon) |
| FooDB `Compound` / `CompoundSynonym` | Bazı tanımlanabilir compound’lar için alternatif ad/kimlik ve gıdalarda bulunan kimyasallar | Etiketten görülmeyen bileşik miktarı veya hastalık kuralı | FooDB compliance sayfası bütün metadata/veriyi CC BY-NC 4.0 altında yayımladığını söylüyor. Bu, ticari uygulamaya gömmek/yeniden dağıtmakla uyumlu olmayabilir. İzin/lisans değişmeden üretim ve ticari modelde kullanmayın; araştırma prototipindeki izin kapsamını da kurumla teyit edin. [FooDB downloads](https://foodb.ca/downloads), [FooDB compliance](https://foodb.ca/compliance) |
| CTD Chemical Vocabulary + Chemical–Disease | Chemical ID, alias, hastalık ilişkisi, ilişki türü ve dayanak yayın keşfi | Gıda etiketindeki terimin kesin kimliği, doz, ürün maruziyeti veya klinik beslenme planı | Doğrudan curation ile inferred relation’ı ayrı tutun; tür/organism, kanıt/predicate ve PMID kaydını koruyun. [CTD 2025 update](https://academic.oup.com/nar/article/53/D1/D1328/7816860) |
| WHO JECFA Evaluations | Gıda katkısı için değerlendirme özeti, kimyasal bilgi, değerlendirme/ADI geçmişi | Condition’a özel kullanıcı beslenme kuralı; miktar yoksa porsiyon maruziyeti | Katkı maddesi risk değerlendirme kolunda değerlendir; disease evidence ile aynı graph edge olarak kullanma. [JECFA database](https://apps.who.int/food-additives-contaminants-jecfa-database/Home) |
| USDA FoodData Central | Nutrient reference/branded data modeli ve API örneği | Türk pazarındaki ürünlerin tam kapsaması ve kullanıcının seçtiği paketin doğruluğu | Branded Food kayıtları ABD marka/GTIN bağlamındadır; NutriScan ürünü için ancak exact product match ve lisans/coverage incelemesi varsa destekleyici olur. Kaynağı ürün etiketinden ayır. [FoodData Central data dictionary](https://fdc.nal.usda.gov/portal-data/external/dataDictionary) |
| Hastalık klinik kılavuzları / MeSH-MEDIC gibi terminolojiler | Condition adını kimliklendirme ve clinical rule’ın dayanağını yazma | Ingredient alias sözlüğü | Condition ID, tercih edilen ad, eş anlamlı, kaynağı ve sürümü ayrı kaydet; UMLS içeriği kullanılırsa vocabulary-specific terms of use’u incele. [NLM UMLS conditions](https://www.ncbi.nlm.nih.gov/books/NBK9675/) |

### Önemli ticari lisans sonucu

FooDB web sitesindeki compliance metni **CC BY-NC 4.0** der. “Açık erişim/indirilebilir” ile “ticari üründe serbest kullanım” aynı şey değildir. NutriScan pazara çıkma hedefini koruyorsa FooDB’den kopyalanan synonym, record, embedding veya türetilmiş lookup tablosunun ne ölçüde NC kapsamına girdiğini varsaymayın. Proje sunumunda FooDB’yi araştırma aday kaynağı diye anmakla, üretim veritabanında dağıtmak farklı kararlardır. Ekip, lisans açısından izinli alternatifler ve veri kaynağı sözleşmesini netleştirmeli.

## Neden bire bir ingredient–disease tablosu yeterli değil?

- **“Şeker” tek başına `sucrose` değildir.** Genel/etiket kavramı, bir veya birkaç kimyasalın miktarını göstermeyebilir. “Şeker” ifadesini otomatik olarak tek molecule map etmeyin.
- **“Buğday unu” tek compound değildir.** FoodOn gibi food ontology bunu gıda/kompozit kavramı olarak temsil edebilir; gluten/alerjen anlamı ise ayrıca mevzuat ve klinik rule alanıdır.
- **Katkı kodu ile formülasyon bilgisi aynı değil.** Bir E-code exact alias üzerinden belirli additive kimliğine ulaşabilir; ürünün gerçek konsantrasyonunu veya porsiyonda tüketilen miktarı vermez.
- **“Aynı substance–disease pair” farklı bağlamlarda geçebilir.** Hücre deneyi, hayvan modeli, çevresel maruziyet, gözlemsel insan çalışması ve clinical guideline aynı kanıt türü değildir.
- **Besin tablosu ayrı ölçümdür.** Etiket besin öğesini 100 g/100 ml veya porsiyon bazında bildirebilir; sistem bu değer, birim, kaynak ve porsiyonu saklamadan hesap yapamaz.

## Önerilen eşleştirme hattı

1. **Raw record:** Orijinal metni, mümkünse etiket alanını, ürün sürümünü, giriş yapan kaynağı ve kontrol tarihini sakla. Normalized text raw metnin yerine geçmesin.
2. **Text normalization:** Unicode, baş/son boşluk, punctuation, case-fold, Türkçe `ı/i`, diacritics ve yaygın yazım varyantlarını test et. Dönüşümün reversible/original text’e bağlı olmasını sağla.
3. **Mention segmentation + type:** Çok bileşenli ingredient satırını alt öğelere ayır; `food`, `composite`, `additive/code`, `chemical`, `allergen statement`, `nutrient`, `unknown` sınıfları kullan. Split sonucu da kaynak metniyle ilişkilendir.
4. **Deterministic lookup:** E-code, CAS veya onaylı exact alias. Kod eşleşmesini kaynağın code table version’ı ve jurisdiction’ıyla birlikte sakla.
5. **Candidate generation:** Lexical/fuzzy ve gerektiğinde dense vector araması aday döndürsün. Her adayın canonical ID’si, alias kaynağı, eşleşme yöntemi, similarity rank/score, model sürümü ve dil desteği ayrı kaydedilsin.
6. **Rerank + decision:** Type compatibility, identifier, context, source, lexical hit ve expert-curated alias sinyalini puanla. Confidence threshold yalnızca validation set ve hata maliyetleriyle kalibre edilsin. Ambiguous veya unknown ifadede otomatik karar verme.
7. **Human curation loop:** Ekipçe doğrulanan yeni aliasları kendi source-traceable lexicon’ına ekle; dış taxonomy’ye katkı yapılacaksa lisans ve bakım şartını incele.
8. **Clinical evidence lookup:** Canonical concept ID üzerinden CTD veya başka literatür kaynağına bağlan; direct/inferred, species, route/dose/context, source article ve evidence grade’i koru.
9. **Rule evaluation:** Kullanıcının condition’ı için onaylanmış rule ve gerekli product/user data varsa çalıştır. Aksi halde “eşleşme adayı bulundu; hastalık değerlendirmesi yapılmadı” gibi ayrık durum döndür.

## Örnekler

| Etiket girdisi | Uygun yorum | Otomatik çıkmaması gereken sonuç |
|---|---|---|
| `E102` | Code → jurisdiction/source-verified additive concept (alias map) | “Bu üründeki doz X” veya “disease risk” |
| `şeker` | Food/ingredient class veya belirsiz gıda terimi; context ve taxonomy adayları | Her zaman sucrose kimliği veya diabetes warning |
| `buğday unu` | Food/composite concept; allergen/gluten rule ayrı | Tek chemical entity veya kimyasal doz |
| `sodyum 320 mg / 100 g` | Nutrient value + unit + basis, label provenance | Porsiyon/toplam tüketim bilinmeden gün hedefi sonucu |
| `aroma verici` | Generic/underspecified ingredient mention | Tahmin edilen tek bileşik ve ona bağlı disease relation |

## Kanıt ilişkisi veri şeması

Klinik claim’i “ingredient disease listesi” içinde kaybetmeyin. Asgari bağlantı modeli:

```text
Product
  -> has_label_mention -> IngredientMention(raw_text, position, source, observed_at)
IngredientMention
  -> candidate_match -> Concept(id, concept_type, preferred_label, source_vocab)
Concept
  -> supported_by -> EvidenceStatement(predicate, evidence_type, species/population,
                                          route/context/dose_if_reported, PMID/URI,
                                          source_version, curated_at)
Condition
  -> evaluated_by -> Rule(rule_id, target_attribute, required_inputs, applicability,
                           source_guideline, reviewer_status, version)
Product + user-declared profile + portion
  -> evaluated_under -> Result(status, rationale, data_gaps, provenance)
```

`candidate_match` ile `supported_by` farklı predicate olmalı. Dış kaynakta “chemical is associated with disease” kaydı varsa, bu kimlik ve yayın bulma adımıdır; `Rule` tablosuna ancak ayrı klinik kaynak/uzman onayıyla dönüşebilir.

Kişisel besin hesabı için ayrıca `PersonalNutritionTarget`, `ProductNutrientObservation` ve `ConsumptionEvent` kayıtlarını kullanın; bunlar ingredient alias graph’ına gömülmesin. Etiket değeri 100 g bazındaysa, tüketim miktarına göre dönüşüm yapılabilir:

```text
consumed_nutrient = label_value_per_100g * consumed_grams / 100
```

Karşılaştırma için hedefin aynı besin öğesi, birim ve dönem (`meal`, `day` vb.) için tanımlanmış olması gerekir. Kullanıcının diğer öğünleri güvenilir biçimde kaydedilmediyse toplam günlük kalan miktar hesaplanamaz. NutriScan yalnızca ölçebildiği porsiyon katkısını raporlamalı; kişisel tedavi veya sağlık uygunluğu kararı çıkarmamalıdır. Türkiye’de temel zorunlu beslenme bildiriminde potasyum/fosfor her zaman yer almadığından, bu alanlar ürün etiketinde yoksa ingredient adı üzerinden sayısal tahmin üretmek yerine `unknown`/`not available` tutulmalıdır. [Türk Gıda Kodeksi, Madde 35](https://resmigazete.gov.tr/eskiler/2017/01/20170126M1-6.htm)

Kullanıcının kişisel hedefi yoksa ürün ingredient-linking hattı yine çalışır ve uzmanlarca onaylanmış bir başlangıç profili varsa `guideline_profile_score` üretebilir. Kişisel hedef girilmişse ayrıca `personal_target_comparison` yapılır. Bir nutrient etikette yoksa ölçülebilen boyutlarda `partial_score` gösterilir; profil kuralı/uygulanabilirlik yoksa `not_assessed` döner. Genel nüfus rehberi kullanılıyorsa bu ayrı `general_reference` kaynağı ve kullanıcı kapsamıyla sunulur, `PersonalNutritionTarget` olarak kopyalanmaz. Sonuç üretimi bu yolları karıştırmamalıdır: `label_information`, `general_reference`, `guideline_profile_score`, `personal_target_comparison`, `partial_score`, `not_assessed`.

## Eşleştirme değerlendirmesi

- Annotated set’i `raw phrase / language / context / expected type / canonical ID / ambiguity / annotator agreement` alanlarıyla kurun.
- Exact alias, fuzzy, lexical, dense ve hybrid yöntemlerini aynı split ve gold labels üzerinde çalıştırın.
- `top-1`, `Recall@k`, MRR yanında otomatik kabul edilen eşleşmelerin precision’ını, abstention oranını ve **coverage’e karşı selective accuracy** grafiğini raporlayın.
- Yanlış canonical mapping kaynaklı hastalık uyarısını; “doğrulanamadı” ile aynı hata sınıfına koymayın. Yanlış uyarı, kaçırılan uyarı, eksik veri ve expert disagreement ayrı kodlansın.
- Türkçe yerel adlar/çekimler, spelling, E-code, composite food, alias collision ve unknown input ayrı test katmanı olsun.

## Önerilen karar ve açık sorular

1. **İlk sözlükte kendi curated alias tablosu + OFF taxonomy/FoodOn’dan izinli ve kontrollü aday kayıtları** kullanın; otomatik kopyalanan her entry’ye source/version/license metadata ekleyin.
2. Chemical identity için CTD vocabulary ve uygun açık kimyasal registry seçeneklerini karşılaştırın. Her iki yolla aynı alias/ID kapsamını sağlıyor mu ölçün.
3. FooDB için ürün içine veri yerleştirme kararı vermeden license review tamamlayın.
4. Nutrient value’ları ingredient database’den değil, doğrulanmış label field’larından tutun.
5. SapBERT ve multilingual alternatifleri Türkçe ve İngilizce gold set üzerinde karşılaştırın; modelin eğitim verisi ve UMLS terim kullanımını deployment öncesi inceleyin.
6. Nihai eşleştirme mimarisini `02-arama-veritabani-karsilastirmasi.md` deney sonuçlarıyla seçin.

## Kaynakça

- [OFF Ingredients Taxonomy](https://github.com/openfoodfacts/openfoodfacts-server/blob/main/taxonomies/food/ingredients.txt)
- [Open Food Facts API / data / license notes](https://github.com/openfoodfacts/openfoodfacts-server/blob/main/docs/api/index.md)
- [FoodOn: a harmonized food ontology](https://www.nature.com/articles/s41538-018-0032-6)
- [FoodOn repository and CC BY 4.0](https://github.com/FoodOntology/foodon)
- [FooDB download files](https://foodb.ca/downloads)
- [FooDB data compliance / license](https://foodb.ca/compliance)
- [CTD 2025 update](https://academic.oup.com/nar/article/53/D1/D1328/7816860)
- [WHO JECFA Evaluations Database](https://apps.who.int/food-additives-contaminants-jecfa-database/Home)
- [USDA FoodData Central dictionary](https://fdc.nal.usda.gov/portal-data/external/dataDictionary)
- [NLM UMLS conditions of use](https://www.ncbi.nlm.nih.gov/books/NBK9675/)
- [T.C. Tarım ve Orman Bakanlığı — Türk Gıda Kodeksi](https://www.tarimorman.gov.tr/Konular/Gida-Ve-Yem-Hizmetleri/Gida-Hizmetleri/Kodeks)
