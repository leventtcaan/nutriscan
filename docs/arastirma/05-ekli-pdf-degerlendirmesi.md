# 5. Ekip arkadaşının kısa PDF’i: eleştirel inceleme

**İncelenen dosya:** [NutriScan_Veri_Kaynaklari_Kisa_Ozet.pdf](/Users/hilalhocaoglu/Downloads/NutriScan_Veri_Kaynaklari_Kisa_Ozet.pdf)  
**Kısa özet:** PDF anlaşılır bir aday akış öneriyor ve vector retrieval’ı karar motorundan ayırması doğru yönde. Ancak OCR→OFF taxonomy→SapBERT/Qdrant→CTD/JECFA akışını proje kararı veya “optimal çözüm” diye almamak gerekir. Türkçe performans, ambiguity, precision/abstention, gerçek ürün verisi, source versions ve özellikle FooDB’nin NC lisansı PDF’deki ana eksiklerdir. Önceki toplantı formunda OCR/barkodun çıkarıldığı yazdığı için ilk adım aynı kararın hâlâ geçerli olup olmadığını ekipçe netleştirmektir.

## PDF’nin önerdiği akışın parçaları

Belge şu varsayımları ortaya koyuyor: ürün içindekiler bölümü OCR ile alınır; OFF Ingredients Taxonomy dilsel normalizasyon için kullanılır; FooDB chemical name/synonym eşleştirmeye yardımcı olur; CTD chemical–disease ilişkileri ve JECFA toksikoloji verisi sağlar; SapBERT+Qdrant belirsiz terimler için aday arar; eşleşme sonrasında CTD/JECFA ile uyarı hazırlanır. PDF ayrıca food/composite terimlerin tek moleküle indirgenemeyebileceğini ve benzerlik aramasının tek başına sağlık hükmü olmadığını belirtiyor.

Bunlar değerlendirmeye alınacak **hipotezlerdir**. Özellikle Qdrant, FooDB ve OCR’nin kullanılıp kullanılmayacağı araştırma sonunda karar verilecek.

## Görsel düzen notu

PDF tek sayfada okunabiliyor; ancak JECFA bölümünün alt çizgisi, hemen sonraki “SapBERT + Qdrant” başlığına çok yaklaşıp başlıkla çakışıyor gibi görünüyor. Yeni sürüm hazırlanırsa JECFA kutusundan sonra biraz daha dikey boşluk bırakılmalı. Bu görsel not, içerik önerilerinin doğruluğundan ayrı bir düzenleme maddesidir.

## İyi başlangıç noktaları

1. **Semantic retrieval ile sağlık kararı arasına sınır koyuyor.** SapBERT/Qdrant yalnızca aday arama olarak gösterilmiş; son kararı kaynağa/kimliğe bağlamak gerektiği söylenmiş.
2. **Food concept ile chemical identity farkını fark ediyor.** Buğday unu veya glikoz şurubu tek molecule değildir; bunları CTD’ye tek chemical gibi bağlamak yanıltıcı olur.
3. **CTD ilişkisini otomatik olarak “zararlı” saymıyor.** Bu önemli; CTD bilimsel hipotez ve yayın bulma kaynağı olabilir, ürün düzeyinde risk ispatı değildir.
4. **Miktar bilinmeden ADI hesabı yapılmayacağını söylüyor.** JECFA değerini porsiyon/maruziyet bilgisi olmadan uygulamamak doğru bir kısıttır.
5. **OFF ürün/barkod kayıtları ile OFF taxonomy dosyasını kavramsal olarak ayırıyor.** Önceki ekip notu OFF ürün/barkod verisini kullanmama kararı almıştı; salt `ingredients.txt` taxonomy’si ayrı kaynak adayıdır.

## Düzeltilmesi veya sınanması gereken noktalar

### 1. OCR ve veri giriş yöntemi kesin değil

PDF’nin ilk adımı etiketi OCR ile almak; ancak 9 Ekim tarihli toplantı formunda OCR kapsam dışı bırakılmış ve ürün ingredient listelerinin sistemde tutulacağı yazılmıştı. Bu eski karar hâlâ geçerliyse PDF akışı doğrudan uyumlu değil. Ekip OCR’ye tekrar dönecekse ayrı bir feasibility deneyi gerekir: doğru ingredient extraction oranı, tablo/çok dilli ambalaj, insan düzeltme yükü ve yanlış ingredient’in sağlık uyarısına etkisi ölçülmeli. OCR’yi geri alma kararı bu PDF’de geçtiği için otomatik alınmamalı.

### 2. OFF taxonomy iyi bir alias kaynağı olabilir ama gerçek doğruluk kaynağı değildir

`ingredients.txt` taxonomy dosyası çeviri/sınıflandırma/alias içerir; fakat yerel Türkçe terim kapsamı, güncellik ve doğru kavrama bağlama performansı gold set üzerinde test edilmeli. Taxonomy’de eşleşme olması ürün etiketinin doğrulandığı anlamına gelmez. OFF product database kullanmama ile OFF vocabulary dosyasını araştırma adayı yapma farklı tercihlerdir. Türev veri, attribution/share-alike ve commercial conditions ayrıca incelenmelidir. [OFF taxonomy](https://github.com/openfoodfacts/openfoodfacts-server/blob/main/taxonomies/food/ingredients.txt), [OFF data/license documentation](https://github.com/openfoodfacts/openfoodfacts-server/blob/main/docs/api/index.md)

### 3. FooDB’nin ticari lisansı proje hedefiyle çatışabilir

FooDB’nin kendi compliance sayfası dataset ve metadata için **CC BY-NC 4.0** bildiriyor. NutriScan’i piyasaya sürme hedefi varsa FooDB verisini uygulamanın lookup tablosuna, embedding index’ine veya dağıtılan ürüne dahil etmek ticari kullanım açısından ciddi belirsizlik oluşturur. Takım kaynak kullanımını lisans incelemesinden önce onaylamamalı; veri ticari ürüne girecekse izin veya uygun lisanslı alternatif bulunmalı. [FooDB compliance](https://foodb.ca/compliance)

### 4. CTD ilişki sınıfı, tür ve yayın bağlamı akışta açık değil

CTD direct-curated Chemical–Disease ilişkileri ile inference ilişki ağları aynı güven seviyesinde/aynı predicate değildir. Veri; source article/PMID, tür (taxon), ilişki türü, evidence context ve doğrudan/türetilmiş olma bilgisiyle saklanmalı. CTD’nin 2025 update’i birden fazla türden araştırma ve çok sayıda inference bulunduğunu açıklıyor. Ürün etiketi ilişkisi kurmak için `ChemicalID` yeterli değildir; ürün maruziyeti, dose ve kullanıcıya uygulanabilir klinik rule ayrı kaynaktan gerekir. [CTD 2025 update](https://academic.oup.com/nar/article/53/D1/D1328/7816860)

### 5. JECFA, hastalık kuralı veritabanı değildir

JECFA katkı maddeleri, contaminant ve bazı diğer bileşenler için toksikolojik değerlendirme/ADI gibi information sunar. Bu, condition’a özel beslenme kuralı değildir. Doz ve toplam tüketim verisi yoksa eşik kıyaslaması yapılamaz; ayrıca söz konusu JECFA değerlendirmesinin maddede/ülkede kullanım durumunu ve sürümünü kaydetmek gerekir. [WHO JECFA database](https://apps.who.int/food-additives-contaminants-jecfa-database/Home)

### 6. “Kullanıcı hastalığına göre risk” ürün içeriğinden tek adımda çıkarılamaz

Ingredient listesi ürünün tüm compound’larını ya da miktarlarını vermez. Hastalık temelli beslenme önerileri kişiye ve eşlik eden durumlara göre değişebilir. ADA 2026 kişiye göre beslenme planlamasını; KDIGO 2024 CKD besin öğesi ayarlamalarının bireyselleştirilmesini vurgular. Bu nedenle PDF’deki son “gerekçeli uyarı” adımından önce condition guideline, applicable population, gerekli product/user data, uzman incelemesi ve abstain logic tanımlanmalı. [ADA 2026](https://diabetesjournals.org/care/article/49/Supplement_1/S89/163932), [KDIGO 2024](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

### 7. SapBERT, Türkçe gıda etiketinde performans kanıtı değildir

SapBERT UMLS terminology’de synonym alignment ile biomedical entity linking için geliştirilmiştir. PDF’deki Türkçe ingredient stringlerinin aynı embedding uzayında doğru chemical identity’ye bağlanacağı gösterilmiyor. Model collation’ı, tokenizer/language support, training corpus, model license ve cross-lingual test seti incelenmeli. UMLS Metathesaurus’un kendisi lisans anlaşması ve vocabulary-level şartlar içeriyor; “açık model” varsayımıyla kaynak kısıtlarını atlamayın. [SapBERT paper](https://aclanthology.org/2021.naacl-main.334/), [NLM UMLS terms](https://www.ncbi.nlm.nih.gov/books/NBK9675/)

### 8. Qdrant erken mimari kararı olabilir

Qdrant dense/sparse hybrid ve payload filter sunar; aynı ihtiyaç PostgreSQL + pgvector + lexical search ile daha az bileşenle sağlanabilir mi, test edilmemiş. Küçük bir ingredient dictionary için vector DB performans kazancı vermeyebilir. Aynı gold set üzerinde accuracy/recall, accepted precision, coverage/abstention, latency, index maliyeti ve operasyonel yük karşılaştırılmalı. [Qdrant hybrid search](https://qdrant.tech/documentation/search/hybrid-queries/), [pgvector](https://github.com/pgvector/pgvector)

## PDF taslağını araştırma deneyine çevirme

PDF’deki akışı başlangıçta `Aday Mimari A` olarak etiketleyin; şu alternatiflerle kıyaslayın:

- **A — PDF akışı:** etiket ifadesi → OFF taxonomy exact/alias → SapBERT/Qdrant adayları → chemical ID → CTD evidence + gerektiğinde JECFA.
- **B — denetlenebilir baseline:** raw label → own curated alias/identifier table + fuzzy/lexical → canonical food/chemical ID → source-linked evidence table → expert rule.
- **C — hibrit arama:** B’deki deterministic/lexical girişe dense candidate retrieval ve reranking ekle; aynı gold setle ölç.
- **D — graph-backed evidence (yalnızca gerekirse):** CTD network path’lerini araştırma amaçlı graph’ta gez; relational rule engine ve product decision path ayrı tut.

**Karar kriteri:** Hangi akış daha yüksek kabul edilmiş precision verir, daha iyi coverage sunar, unknown/ambiguous vakada ne sıklıkla yanlış kesin karar verir, Türkçe terimleri nasıl işler, source/version/lisansı korur ve ne kadar bakım ister? Bu ölçümler olmadan tek bir mimariyi “optimal” ilan etmeyin.

## Ekip arkadaşına geri bildirim için kısa not

PDF; sözlük → aday eşleştirme → evidence → gerekçeli sonuç fikrini tartışmak için iyi bir başlangıç. Kaynak ve bileşen seçimi öneri düzeyinde tutulmalı. En önemli ek: bir **benchmark ve abstention protokolü**; ticari kullanım için FooDB lisans incelemesi; CTD evidence type/taxon/provenance; hastalık ile alerji ve ingredient ile nutrient data ayrımı; OCR’nin mevcut ekip kapsamıyla uyumunun teyidi.

## Kaynakça

- [Takım arkadaşının PDF’i](/Users/hilalhocaoglu/Downloads/NutriScan_Veri_Kaynaklari_Kisa_Ozet.pdf)
- [CSE 491 Meeting Record 2](/Users/hilalhocaoglu/Documents/ChatGPT/bitirme/MeetingRecord2_NutriScan.docx)
- [Open Food Facts Ingredients Taxonomy](https://github.com/openfoodfacts/openfoodfacts-server/blob/main/taxonomies/food/ingredients.txt)
- [Open Food Facts data and license documentation](https://github.com/openfoodfacts/openfoodfacts-server/blob/main/docs/api/index.md)
- [FooDB license/compliance](https://foodb.ca/compliance)
- [CTD 2025 update](https://academic.oup.com/nar/article/53/D1/D1328/7816860)
- [WHO JECFA Evaluations Database](https://apps.who.int/food-additives-contaminants-jecfa-database/Home)
- [SapBERT, NAACL 2021](https://aclanthology.org/2021.naacl-main.334/)
- [NLM UMLS Reference Manual](https://www.ncbi.nlm.nih.gov/books/NBK9675/)
- [Qdrant hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/)
- [pgvector](https://github.com/pgvector/pgvector)
- [ADA Standards 2026](https://diabetesjournals.org/care/article/49/Supplement_1/S89/163932)
- [KDIGO 2024 CKD Guideline](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)
