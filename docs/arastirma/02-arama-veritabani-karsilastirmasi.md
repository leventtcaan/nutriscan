# 2. Arama ve veritabanı seçeneklerini karşılaştırma

**Kısa özet:** “Vector DB gerekli mi?” sorusunun cevabı veri hacminden çok, eşleştirme görevinde vector retrieval’in exact/fuzzy/lexical yöntemlere ölçülebilir katkısına bağlı. NutriScan için relational kaynak ve kural kayıtları ana sistemde kalmalı. İlk deneyde PostgreSQL + exact alias + full-text/fuzzy arama ve pgvector hibrit seçenek olarak karşılaştırılmalı. Qdrant ancak filtreli arama, ingestion veya ölçek koşullarında ölçülen kazanım ayrı servis maliyetini haklı çıkarırsa; graph DB ise çok adımlı ilişki sorguları gerçek ihtiyaç olursa seçilmeli.

## Karşılaştırılacak görev

Vector database ürünün sağlıklı/zararlı kararını vermez. Test edeceğimiz görev: **Türkçe veya İngilizce etiket parçasını, kontrollü ingredient/chemical sözlüğündeki doğru kanonik adaya sıralamak ve çözümlenemeyen girdide abstain etmektir.** Hastalık kuralı ve kanıt değerlendirmesi ayrı katmandır.

## Yöntem karşılaştırması

| Yöntem | Güçlü yanı | Zayıf yanı | Bu projedeki rolü |
|---|---|---|---|
| Exact alias / identifier | E-numarası, CAS veya bilinen eşanlamlı için deterministik ve denetlenebilir | Yeni yazım, OCR hatası veya eksik alias yakalamaz | İlk aşamada her zaman çalıştır |
| Normalizasyon + fuzzy | Büyük/küçük harf, noktalama, Türkçe karakter ve küçük yazım farklarını yakalar | Benzer yazılıp farklı olan kavramları karıştırabilir | Ucuz ve güçlü baseline; eşik gold setle seçilir |
| Lexical full-text / BM25 benzeri | Terim eşleşmesi ve identifier için açıklanabilir | “badem unu” ile eş anlamlı açıklama gibi parafrazı kaçırabilir | Alias ve açıklamalı kayıt araması |
| Dense vector | Semantik paraphrase ve farklı ad biçimleri için aday üretir | Benzer anlam yanlış kimliğe gidebilir; Türkçe model ve alan dağılımı belirsiz | Yalnızca candidate generation, confidence/abstention ile |
| Hybrid lexical + dense | Lexical kesinliği ile semantik kapsama alanını birleştirebilir | Birden fazla indeks, score fusion ve bakım gerekir | Beklenen ana deney kolu; BioSyn literatürü sparse+dense temsillerini birlikte kullanır |
| İlişkisel DB | Ürün, condition, kaynak, kural ve provenance ilişkilerinde bütünlük ve transaction | Çok derin, değişken graf geçişleri sorgusu karmaşıklaşabilir | Uygulama kayıtlarının source of truth’u |
| Knowledge graph / graph DB | Chemical→gene→phenotype→disease gibi çok-adımlı yolları gezmek ve görselleştirmek doğal | Başlangıçta ek öğrenme, işletim ve eşzamanlama maliyeti | CTD mekanizma ağı araştırma sorguları ürün özelliği olacaksa değerlendir |
| Tamamen sözlük/kural tabanlı | Güvenli, açıklanabilir, kolay audit | Bilinmeyen yazımda kapsam düşer, elle bakım gerekir | Sağlık kuralı için kalıcı deterministik katman; giriş eşleştirmesinde baseline |

[BioSyn’in orijinal makalesi](https://aclanthology.org/2020.acl-main.335.pdf) biomedical entity normalization için sparse lexical ve dense semantic temsilleri birleştirir; bu, hibrit yaklaşımı denemek için literatür dayanağıdır. [SapBERT makalesi](https://aclanthology.org/2021.naacl-main.334/) synonymy odaklı tıbbi entity linking için güçlü bir adaydır. İki makaledeki benchmark başarısı NutriScan’in Türkçe gıda etiketi üzerinde başarı garantisi değildir.

## Altyapı seçenekleri

### PostgreSQL + normal tablolar + `pgvector`

- Ürün, label mention, canonical entity, alias, evidence, source, condition rule ve expert review aynı foreign-key/transaction modelinde tutulabilir.
- pgvector exact nearest-neighbor aramasıyla referans sonucu verir; HNSW veya IVFFlat ile hız/recall değiş tokuşu yapılabilir. PostgreSQL full-text search ve kendi alias tablolarıyla birlikte test edilebilir. [pgvector resmi deposu](https://github.com/pgvector/pgvector)
- Proje kataloğu ve bilimsel kayıtlar zaten ilişkisel yapıda olduğu için ilk prototipte en düşük operasyonel karmaşıklığı sunması beklenir. Bu bir hipotezdir; sorgu ve veri hacmiyle ölçülecek.

### PostgreSQL + Qdrant

- Qdrant vektör araması, payload filtreleme ve dense/sparse hybrid query sunuyor. Qdrant kendi dokümanlarında da hybrid search’e kesin keyword eşleşmesi ve semantic recall rolü veriyor; filtre alanları için payload index planlanmalı. [Qdrant hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/), [Qdrant filtering](https://qdrant.tech/documentation/search/filtering/)
- Ana iş relational kayıtlar, provenance ve onaylanmış kurallar ise ikinci database bu kayıtların kopyasını yaratır. Kaynak verinin sahibi PostgreSQL kalmalı; Qdrant sadece `entity_id`, sözlük sürümü, dil, model sürümü ve alias metadata taşıyan arama indeksi olmalı.
- Bu seçeneği ancak aynı test setinde retrieval iyileşmesi veya operasyon gereksinimi ölçülürse tutun.

### Graph database

- CTD gibi Chemical/Gene/Phenotype/Disease düğüm ve ilişkilerini birden çok adımda yürütme ihtiyacı varsa graph modeli ilişki yolunu görünür kılar. Neo4j’nin property graph yaklaşımı düğüm, ilişki ve ilişki özelliklerini doğrudan temsil eder; resmî dokümanları graph traversal ve vector index imkânlarını da açıklar. [Neo4j graph database](https://neo4j.com/docs/getting-started/graph-database/), [Neo4j vector index](https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/vector-indexes/)
- Bununla birlikte bir hastalık kuralı için 1–2 join yapılması graph DB gerektirmez. Relational tablolarla kanıt zinciri kurulabilir. Graph seçimi “hastalık ve kimyasal sayısı çok” diye değil, tekrar eden çok-adımlı path sorguları ölçüldüğü için yapılmalı.

## Önerilen deney

### Gold set

Ekipçe seçilmiş gerçek etiket örneklerinden kişisel/ürün marka verisini yayımlamadan bir **label mention → doğru concept ID** seti oluşturun. Her kayıt için raw phrase, dil, bağlam, tür (`food`, `composite`, `additive`, `chemical`, `nutrient`, `allergen`), gold ID, kabul edilebilir aliaslar, ambiguity flag ve annotator consensus saklayın.

- Train/dev/test bölmesi aynı entity’nin yakın aliaslarının train ve testte sızıntı yapmasını engellesin; entity-held-out ve surface-form-held-out sonuçları ayrı raporlansın.
- Bilinen maddeler, E-code/CAS, Türkçe imla varyantı, İngilizce ad, composite food, bilinmeyen ifade ve gerçekten belirsiz ifade dengeli örneklensin.
- En az iki kişi örnekleri bağımsız etiketlesin; uyuşmazlıklar altın standarda alınmadan önce çözülsün. Klinik kurallar için ingredient etiketi bilen annotator tek başına yeterli değildir; ilgili beslenme/sağlık uzmanı ayrı onay verir.

### Deney kolları

1. Canonical identifier ve curated exact aliases.
2. Unicode/Türkçe karakter normalizasyonu + fuzzy string.
3. Lexical full-text arama.
4. Dense embedding aday araması.
5. Lexical+dense hybrid fusion (örn. rank fusion).
6. Gerektiğinde aday reranking; `abstain` kararı dahil.

SapBERT bir kol olabilir; ancak Türkçe gıda etiketlerindeki performansı, model ve UMLS kaynak lisansı ve dağıtım şartları kontrol edilmeden varsayılmamalı. SapBERT’in özgün paper’ı UMLS üzerinden öğrenildiğini belirtir; UMLS Metathesaurus’un farklı vocabularies için lisans koşulları bulunur. [SapBERT](https://aclanthology.org/2021.naacl-main.334/), [NLM UMLS conditions of use](https://www.ncbi.nlm.nih.gov/books/NBK9675/)

### Ölçümler

| Ölçü | Ne cevaplar |
|---|---|
| Top-1 accuracy | İlk sıradaki öneri doğru mu? |
| Recall@k | Doğru kavram ilk k aday arasında var mı? |
| MRR | Doğru aday ortalama kaçıncı sırada? |
| Precision among auto-accepted | Otomatik onaylanan eşleşmelerin kaçı doğru? |
| Coverage / abstention rate | Sistem ne kadarında karar veriyor, ne kadarında geri çekiliyor? |
| Selective accuracy vs coverage | Daha az karar verince doğruluk nasıl değişiyor? |
| Per-class / per-language errors | Türkçe, additive, composite gibi sınıflarda nerede hata oluyor? |
| p50/p95 latency, memory, index/build cost | Arama katmanının pratik ve işletim maliyeti |
| Provenance completeness | Her adayın alias, source, version ve model bilgisini açıklayabiliyor muyuz? |

Sağlık kararı değerlendirmesinde retrieval accuracy, clinical rule accuracy ile karıştırılmamalı. Hatalı risk uyarısı ve kaçırılmış uyarı maliyetleri ayrı raporlanmalı; hangi otomasyon eşiğinin kullanılacağı uzman ve test verisi olmadan belirlenmemeli.

## Karar kuralı

- **Başlangıç önerisi:** PostgreSQL’i kayıt/ilişki/kural için ana kaynak yapın; `exact aliases + fuzzy + lexical` baseline kurun. `pgvector` ile semantik retrieval deney kolu ekleyin.
- **Qdrant’a geçiş koşulu:** Gold sette hibrit arama ölçülebilir kalite artışı verir ve payload filtresi/latency/ölçek gibi gereksinimler ek servisi haklı çıkarırsa.
- **Graph DB’ye geçiş koşulu:** Chemical–gene–phenotype–disease gibi çok adımlı kanıt yolları ürünün araştırma/izlenebilirlik ihtiyacına dönüşür, relational sorgular sürdürülemez hale gelir ve graph prototipinde somut fayda gösterilirse.
- **Vector araması kullanılmama sonucu da kabul edilebilir:** Exact+lexical yöntemler eşdeğer kalitede ve daha düşük maliyetliyse vector database eklemeyin.

## Sınırlamalar ve riskler

- Biomedikal embedder’ın Türkçe gıda etiketi üzerinde domain shift’i vardır; çapraz dil eşleştirme test seti oluşturun.
- Vector score’u olasılık olarak yorumlanmamalı; karar eşiğini validation set üzerinde kalibre edin.
- ANN index hız kazandırabilir ama approximate recall/filter davranışı vardır; küçük corpuslarda exact scan daha iyi olabilir.
- Qdrant ürün açıklamasında graph/ontology built-in olmadığı açıkça belirtiliyor; semantik ilişkileri payload’a gömmek kanonik ilişkisel modeli ikame etmez. [Qdrant FAQ](https://qdrant.tech/documentation/faq/)
- Kullandığınız model/dataset lisansı ve yeniden dağıtım şartı ticari hedefle uyumlu olmalı.

## Kaynakça

- [BioSyn — ACL 2020](https://aclanthology.org/2020.acl-main.335.pdf)
- [SapBERT — NAACL 2021](https://aclanthology.org/2021.naacl-main.334/)
- [NLM UMLS Reference Manual: use conditions](https://www.ncbi.nlm.nih.gov/books/NBK9675/)
- [pgvector](https://github.com/pgvector/pgvector)
- [Qdrant hybrid search](https://qdrant.tech/documentation/search/hybrid-queries/)
- [Qdrant filtering](https://qdrant.tech/documentation/search/filtering/)
- [Qdrant FAQ](https://qdrant.tech/documentation/faq/)
- [Neo4j graph basics](https://neo4j.com/docs/getting-started/graph-database/)
- [Neo4j vector indexes](https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/vector-indexes/)
