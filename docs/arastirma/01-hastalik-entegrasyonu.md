# 1. Hastalıkların NutriScan’e entegrasyonu: literatür ve karar çerçevesi

**Kısa özet:** Hastalıkları, alerjenlerdeki gibi yalnızca “üründe var/yok” kontrolüne indirgemek mümkün değildir. Diyabet veya kronik böbrek hastalığında ürünün porsiyon verilerine dayanan, uzmanlarca hazırlanıp doğrulanan bir başlangıç profili skoru ana özelliği açık tutabilir; kullanıcının kişisel hedefi varsa bu skoru daha da uyarlayabilir. Skor klinik güvenlik hükmü değildir. CTD gibi kimyasal-hastalık veri tabanları araştırma hipotezi ve yayın bulmaya yarar; tek başına tüketici uyarısı kuralı oluşturmaz.

## Araştırma sorusu

**Ürün etiketi ve beyan edilen besin değerleri sınırlı olduğunda, hangi hastalık–ürün senaryoları kaynaklı, ölçülebilir ve güvenli karar desteği olarak modellenebilir; sistem hangi koşulda değerlendirme yapmayı reddetmelidir?**

Buradaki temel tasarım sorusu her ingredient’i her hastalıkla eşleştirmek değil; hastalıkla ilgili klinik öneriyi, onu etkileyen **ürün niteliği** ve gerekli **kullanıcı girdisi** üzerinden uygulamaktır.

## Literatürden çıkan temel ayrım

Dijital sağlık rehberlerinin yazılı klinik önerilerden veri öğeleri, iş akışı ve açık karar mantığı çıkarması gerekir. WHO SMART Guidelines / Digital Adaptation Kits, bir önerinin yazılımda kullanılabilmesi için hedef kullanıcıyı, veri alanlarını, karar adımlarını ve test edilebilir mantığı açık hale getirir. NutriScan için kullanılabilecek fikir bu süreçtir; WHO DAK örnekleri doğrudan NutriScan’in gıda kuralları değildir. [WHO SMART Guidelines](https://www.who.int/teams/digital-health-and-innovation/smart-guidelines), [WHO DAK bileşenleri](https://smart.who.int/dak-pnc/v0.9.9/decision-logic.html)

| Değerlendirme sınıfı | Örnek mantık | Uygun ürün verisi | Gerekli kullanıcı verisi | Başlıca sınır |
|---|---|---|---|---|
| İçerik veya beyan varlığı | Etikette açıkça bildirilen tetikleyici/alerjen var mı? | İçindekiler, alerjen beyanı, iz miktar uyarısı ve kaynak/güncellik | İlgili alerjen veya durum profili | Etiketin eksik veya eski olması; çapraz bulaşma bilgisinin belirsizliği |
| Hastalığa özgü içerik kısıtı | Belirli içerik, seçilmiş hastalık kuralının kapsamına giriyor mu? | Güvenilir ingredient kimliği ve varsa ürünün ilgili beyanı | Hastalığın türü/alt türü ve kişisel plan gerekebilir | Her hastada aynı kural geçerli olmayabilir |
| Porsiyon ve besin öğesi hesabı | Seçilen porsiyonun profile katkısını ve varsa kişisel hedefle farkını hesapla | Besin değerleri, birim, referans miktar, porsiyon ve kaynak | Başlangıçta uzman onaylı guideline profile; kişisel hedef isteğe bağlı | Ingredient adları besin miktarını vermez; etiket verisi yanlış/eksik olabilir |
| Kimyasal–hastalık literatür ilişkisi | Bir kimyasal hakkında hastalıkla ilişkili çalışma/yayın bulunuyor mu? | Kimyasal kimliği, ilişki türü, tür/organizma, yayın ve bağlam | Uygulama profiline bağlı değil; önce uzman yorumu gerekir | İlişki; nedensellik, gıda maruziyeti veya ürünün zararı anlamına gelmez |
| Toksikolojik katkı maddesi değerlendirmesi | Madde için bir değerlendirme/rehber değer var mı? | Kesin madde ve gerekiyorsa üründeki miktar/tüketim verisi | Toplam maruziyet ve ilgili değerlendirme koşulları | Hastalık tedavisi veya bireysel klinik tavsiye değildir |

### Alerji, çölyak ve diğer hastalıklar aynı kategori değil

Çölyak hastalığı ile buğday alerjisi farklı klinik durumlardır. NIDDK, çölyak hastalığını gluteni tetikleyici alan kronik sindirim/bağışıklık bozukluğu olarak tanımlar ve buğday alerjisinden ayrı tutar. Bu nedenle arayüzde ikisini “alerji” olarak toplamayın; içerik eşleşmesi teknik olarak benzer bir var/yok kontrolü kullanabilir ama kuralın adı, dayanağı ve sonuç metni farklı olmalı. [NIDDK — celiac disease facts](https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease/definition-facts)

Besin öğesine dayalı hastalık desteğinde, tek bir “şeker”, “tuz” veya “potasyum” eşiği herkese uygulanacak bir hastalık hükmü gibi sunulmamalı. ADA 2026 rehberi diyabette beslenme planlamasını kişiye göre bireyselleştiriyor; KDIGO 2024 de CKD için sodyum, fosfor, potasyum ve protein ayarlamalarının kişisel gereksinim ve hastalık şiddetine göre renal diyetisyen/uzman desteğiyle yapılmasını belirtiyor. Bunlar ürün uyarı kuralı için gerekli bağlamı gösterir; doğrudan koda gömülecek NutriScan eşikleri değildir. [ADA Standards of Care 2026, bölüm 5](https://diabetesjournals.org/care/article/49/Supplement_1/S89/163932), [KDIGO 2024 CKD Guideline](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

## Kişiye göre miktar değerlendirmesi nasıl kurulur?

Kişiselleştirme iki ayrı parçayı bir araya getirir; bu parçaları tek bir hastalık tablosunda eritmeyin:

1. **Kişisel hedef:** Kullanıcının bakım ekibiyle belirlediği besin öğesi hedefi ve bunun öğünlük/günlük gibi zaman kapsamı. Hastalık adı bu değeri otomatik üretmez. İlk sürümde kullanıcı hedefi kendi planından girebilir; uygulama bunu `user_reported` olarak işaretler ve klinik olarak doğrulanmış gibi sunmaz. İleride uzman tarafından doğrulanan hedefler `clinician_confirmed` gibi ayrı bir durumla saklanabilir.
2. **Ürünün ölçülebilir katkısı:** Ürün etiketindeki besin miktarı, etiketin referans bazı (100 g, 100 ml veya porsiyon), seçilen tüketim miktarı, birim ve kaynak tarihi.

Hesaplama yalnızca ikisi de mevcut ve birimleri uyumlu olduğunda yapılır:

```text
consumed_nutrient = label_nutrient_per_100g * consumed_grams / 100
remaining_target = personal_target_for_period - reliably_logged_intake_for_period
```

Bu hesap, yalnızca ürünün ölçülen katkısını veya kullanıcının güvenilir biçimde kaydettiği dönemin kalan miktarını gösterir. Günün başka yerlerinde yenilenler kaydedilmediyse “günlük hedefin içinde kaldı” denemez. Hedef, porsiyon veya ürün değeri yoksa `Not assessed` / `Insufficient data` döndürülür. Sonuç metni “kişisel planında belirttiğin hedefe göre bu porsiyonun hesaplanan katkısı…” diye sınırını belirtmeli; “bu ürün güvenli/zararlı” hükmüne çevrilmemeli.

| Hastalık senaryosu | Değerlendirilebilecek ürün verisi | Kişiselleştirme girdisi | Sistem sınırı |
|---|---|---|---|
| Diyabet ve karbonhidrat takibi | Ürünün toplam karbonhidrat miktarı, beslenme bildiriminin bazı ve tüketilen porsiyon | Kullanıcının kendi öğün planında belirttiği hedef veya takip tercihi | Şeker miktarı toplam karbonhidratla aynı alan değildir. NutriScan insülin dozu, karbonhidrat/insülin oranı veya tedavi değişikliği hesaplamamalı. ADA 2026, beslenme tedavisini kişiselleştirilmiş planla ve beslenme uzmanı desteğiyle ele alır. |
| Kronik böbrek hastalığı | Etikette gerçekten beyan edilmiş tuz/sodyum, protein ve varsa potasyum/fosfor; tüketim porsiyonu | Uzmanla belirlenmiş ilgili besin hedefleri; gerekiyorsa zaman kapsamı | Hastalık evresi, diyaliz, laboratuvar sonuçları, ilaçlar ve eşlik eden durumlar gereksinimi değiştirebilir. Ingredient adından potasyum/fosfor miktarı türetilmez. NIDDK kişiye uygun potasyum/protein/sodyum miktarı için sağlık uzmanı/diyetisyenle çalışmayı önerir. |

Türkiye’de zorunlu beslenme bildiriminin temel alanları enerji, yağ, doymuş yağ, karbonhidrat, şekerler, protein ve tuzdur; potasyum ve fosfor bu genel zorunlu listenin içinde değildir. Bu yüzden böbrek hastalığı senaryolarında bu değerler etikette yoksa, sadece içerik adlarına bakarak miktar hesabı yapılamaz. Tuz ve sodyum da ayrı birimlerdir; karşılaştırmadan önce etiket tanımına göre dönüştürülmeli, hedefle aynı birimde tutulmalıdır. [Türk Gıda Kodeksi Gıda Etiketleme ve Tüketicileri Bilgilendirme Yönetmeliği, Madde 35](https://resmigazete.gov.tr/eskiler/2017/01/20170126M1-6.htm), [NIDDK — CKD’de sağlıklı beslenme](https://www.niddk.nih.gov/health-information/kidney-disease/chronic-kidney-disease-ckd/healthy-eating-adults-chronic-kidney-disease?dkrd=nkdep.nih.gov%2Fresources%2Feating-right.shtml)

## Kullanıcı kişisel hedefini bilmiyorsa skor nasıl çalışır?

Kişisel hedefi bilmeyen kullanıcı için ana uygunluk özelliğini kapatmamalıyız. Bunun yerine skorun **kişisel tedavi uygunluğu** değil, açıkça tanımlanmış bir **kılavuz temelli başlangıç profiline uyum** olduğunu belirtmeliyiz. Kullanıcı kişisel hedefini eklediğinde aynı ürün, bu hedefe göre ikinci kez değerlendirilebilir. Bunun için eşikleri baştan icat etmek gerekmez: ilgili hastalık için güncel profesyonel kılavuzlardaki açık sayısal öneriler, kapsamı ve kanıt gücü korunarak başlangıç profile aktarılabilir. Bir kılavuzun yalnızca nitel öneri verdiği yerde ekip bunu keyfî gram sınırına çevirmemeli; nitel öneriyi açıklanabilir bir özellik olarak tutmalı veya bileşik skor ağırlığını araştırma hipotezi diye ayrıca test etmelidir.

### 1. Kişisel hedef olmadan: başlangıç profili skoru

Kullanıcı hastalığını seçince, uygulama ilgili hastalık için uzmanlarca hazırlanmış, kaynak ve kapsamı belli bir başlangıç profili uygular. Skor, etikette gözlenen ürün özelliklerinin bu profile ne kadar uyduğunu özetler. Her skor ekranında porsiyon, kullanılan besin alanları, profil sürümü ve eksik veriler gösterilir. Skor “tıbben güvenlidir” anlamına gelmez; ürünler arasında seçim yapmaya yarayan, kanıta dayalı ama NutriScan’in ayrıca tanımlayıp doğrulaması gereken bir tarama puanıdır.

- **Diyabet örneği:** Tek tip günlük karbonhidrat limiti uydurmayın. ADA’nın önerdiği genel beslenme örüntüsü ve etiketin gerçekten sağladığı alanlar (toplam karbonhidrat, şeker, varsa lif, seçilen porsiyon) üzerinden çok bileşenli bir profil oluşturulabilir. Ürün kategorisine göre göreli sıralama da kullanıcıya yardımcı olur. Ancak hangi alanın skoru ne kadar değiştireceği ve puan bantları ADA kılavuzunun kendisi değil, uzmanlarla geliştirilip karşılaştırmalı test edilecek NutriScan modelidir. ADA tek tip makrobesin dağılımı önermiyor; beslenme planının kişiselleştirilmesini vurguluyor. [ADA Standards of Care 2026](https://doi.org/10.2337/dc26-S005)
- **Kronik böbrek hastalığı örneği:** Etiketteki tuz/sodyumdan, seçilen porsiyonun rehberdeki günlük referansa katkısı hesaplanabilir. KDIGO 2024, CKD’de sodyum alımı için <2 g/gün önerisini 2C kanıt düzeyinde veriyor; sodyum kaybettiren nefropatide bu kısıtlamanın genellikle uygun olmadığını ve çocuklar için ayrı yaklaşım gerektiğini de belirtiyor. Bu nedenle başlangıç profili “yetişkin CKD için rehber taraması” diye etiketlenmeli; istisnalar görünür olmalı. Potasyum/fosfor etikette yoksa skora varmış gibi katılmaz. [KDIGO 2024 CKD Guideline](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

Bu puan için etiket ve klinik kaynakla desteklenmeyen attribute’a ceza/ödül vermeyin. Örneğin içerik listesinde fosfat katkısı varsa “fosfat katkısı bildiriliyor, miktar etiketten hesaplanamıyor” şeklinde açıklama yapılabilir; toplam fosfor miktarı varmış gibi sayısal puanlama yapılamaz. Tüm hastalıklar için tek ortak ağırlık ve eşik tablosu da kullanılmamalı.

### 2. Kişisel hedef eklendiğinde: kişiye göre uyarlama

Kullanıcı hedefini uzman planından eklerse veya bir uzman onaylı profile bağlanırsa, başlangıç profilinin üstüne kişisel hedef karşılaştırması çalışır. Hedefin birimi, öğün/gün kapsamı, kaynağı ve geçerlilik tarihi saklanır. Kullanıcıya “bu porsiyon hedefinin X kadarını kullanıyor” denebilir; ama diğer öğünler kaydedilmediyse günün kalanı için toplam sonuç verilmez.

Bu başlangıç profili **ürün seçim desteğidir; otomatik kişisel diyet planı değildir**. Rehberden türetilmiş genel örnek öğün veya eğitim içeriği ayrı bir özellik olarak geliştirilebilir. Kişinin enerji ve besin gereksinimlerine göre tam menü üretimi ise yaş, eşlik eden hastalıklar, tedavi/ilaç, böbrek hastalığının bağlamı ve kişinin tercihleri gibi ek bağlam ister; bu kapsamı bitirme projesindeki ürün skoruna karıştırmayın. ADA kişiselleştirilmiş tıbbi beslenme tedavisini sağlık ekibiyle geliştirmeyi öneriyor; NIDDK de CKD’de uygun besin miktarlarını sağlık uzmanı/diyetisyenle belirlemeyi vurguluyor. [ADA 2026](https://doi.org/10.2337/dc26-S005), [NIDDK — CKD’de beslenme](https://www.niddk.nih.gov/health-information/kidney-disease/chronic-kidney-disease-ckd/healthy-eating-adults-chronic-kidney-disease?dkrd=nkdep.nih.gov%2Fresources%2Feating-right.shtml)

### Skor ve güven düzeyini ayrı gösterin

Bir ürün için `profile_score` ile `data_coverage` ayrı alanlar olmalı. Skor, ölçülebilen niteliklerin başlangıç/kişisel profile uyumunu anlatır; coverage ise hesapta kaç gerekli alanın mevcut ve güvenilir olduğunu belirtir. Etikette potasyum/fosfor yoksa sistem böbrek profili için “tam puan” vermemeli; örneğin tuz/sodyum boyutundaki sonucu gösterip genel değerlendirmenin **kısmi** olduğunu söylemeli. Bir kritik alan eksikse tek genel puan üretmek yerine bileşen puanları ve “eksik verili” statüsü gösterilebilir.

Önerilen statüler: `guideline_profile_score` (başlangıç profili), `personal_target_comparison` (kişisel hedef), `partial_score` (bazı alanlar ölçülebiliyor), `not_assessed` (kural kapsamı yok veya temel veri eksik). Skor; gerekçe, profil/kural sürümü ve kullanılan etiket alanlarıyla açıklanmalı. “Daha uygun / dikkat / veri eksik” gibi sonuç etiketleri, uzman değerlendirmesiyle belirlenecek bantlara bağlanmalı; `safe / harmful` gibi tıbbi hüküm olmamalı.

**TÜBİTAK için araştırma sorusu:** Uzmanların bağımsız ürün değerlendirmeleriyle, kılavuz temelli başlangıç profilinden çıkan skor ne kadar uyuşuyor; eksik etiket verisi ve belirsiz hastalık bağlamı skora ne yapmalı? Klinik etki iddiası kurmadan uzmanlar arası uyum, false-positive/false-negative, veri coverage’ı ve kullanıcıların skor anlamını doğru kavrayıp kavramadığını ölçün.

## Diyetisyen ekibimizde yoksa uygulanabilir doğrulama yolu

Bilgisayar mühendisliği ekibi yazılımın ve ölçüm hattının doğruluğunu kendi başına test edebilir; ürün skorunun klinik/beslenme açısından uygunluğunu tek başına doğrulayamaz. Uzman katkısı, ekibin yerine sistemi kurmak değildir: ekip kaynağı kurala çevirir; uzman bu yorumun kapsamını, istisnalarını ve kullanıcıya gösterilen dilini gözden geçirir.

### Uzman görüşmesini küçük ve somut tutun

1. Önce kapsamı daraltın: örneğin yalnızca **yetişkinlerde diyabet için paketli ürünün karbonhidrat bilgisi** veya **yetişkin CKD için etiketteki tuz/sodyum**. “Tüm hastalıklar için beslenme puanı” istemeyin.
2. İlgili üniversitenin Beslenme ve Diyetetik bölümüne, üniversite hastanesine veya danışmanınızın klinik ağına ulaşın. CKD için renal beslenmede deneyimli diyetisyen; diyabet için diyabet beslenme tedavisinde deneyimli diyetisyen uygun ilk görüşme kişisidir. Gerekirse danışmandan ilgili bölüm öğretim üyesine kısa bir tanıştırma rica edin.
3. Görüşmeye bir sayfalık materyal götürün: kılavuzdan aldığınız cümle ve bölüm; düşündüğünüz kural; kullandığınız etiket alanları; kapsam/istisna; 5–10 sentetik örnek ürün; şu anki açıklama metni. Uzmandan “uygulamayı tasarlamasını” değil, bu dönüşümde hata/tehlikeli genelleme olup olmadığını incelemesini isteyin.
4. Görüş ve değişiklikleri tarih, uzmanlık alanı, kaynak sürümü ve hangi kuralı etkilediğiyle kaydedin. Mümkünse ikinci bir bağımsız uzmanla kritik kuralları çapraz kontrol edin; erişilemiyorsa bu sınırlılığı raporlayın, doğrulanmış gibi yazmayın.

### Puan ağırlıklarını nereden alacağız?

İlk adım, kılavuzun **açıkça belirttiği ölçütleri** kaynaklı alt kurallara çevirmek. Kılavuz sayısal ağırlık/ürün puanı vermiyorsa mühendislik ekibi klinik ağırlıkları kendiliğinden icat etmemeli. Önce `portion_carb`, `sugars`, `fiber_if_available` veya `labeled_sodium` gibi boyutları ayrı gösterin. Bileşik skor için iki yol var:

- Uzmanlar ve danışmanla, nedenleri yazılmış ağırlık/bant taslağı belirleyip bunu “araştırma modelinin varsayımları” diye tanımlayın; bağımsız uzman puanlarıyla uyumu ölçmeden klinik olarak doğrulanmış saymayın.
- Uzman veya savunulabilir kaynak ağırlıkları bulunamazsa, bileşen puanları ve açıklanabilir göreli sıralama verin; birleşik klinik uygunluk puanı iddiasını sonraki çalışmaya bırakın.

Kılavuzdan aktarılabilen **sayısal bir hedef**, ürün başına doğrudan “uygunluk eşiği” olmayabilir. Günlük toplam sınır ile tek ürün porsiyonunu ayırın; porsiyonun referansın ne kadarını kullandığını gösterin, tüm günün nasıl geçeceğini öngörmeyin. Başlangıçta gerekli olmayan laboratuvar veya ilaç verisini toplamadan ilerleyin; gerçek hasta verisi toplamayı düşünürseniz üniversitenin etik ve veri koruma süreçlerini danışmanla netleştirin.

### Uzman bulunamazsa kapsamı nasıl dürüstçe koruruz?

- Teknik doğrulama devam eder: birim/porsiyon hesaplarının testleri; etiket alanı doğruluğu; tekrar üretilebilir skor; eksik veride `partial_score`; kaynak/versiyon izlenebilirliği.
- Klinik doğrulama iddiası kurulmaz. Sonuç, “uzman onaylı hastalık puanı” değil, **kılavuzlardan türetilmiş deneysel profile-alignment prototipi** diye raporlanır.
- Araştırmanın ana iddiası eşleştirme doğruluğu, etiket verisi coverage’ı ve kural provenance’ına daraltılabilir. Skorun klinik uygunluğu açık sınırlılık ve gelecek iş olur.
- Gold set klinik görüş olmadan kurulamazsa, yalnızca teknik test senaryoları ve sentetik ürün/profil kullanılır; bunlar gerçek hasta senaryosunda etkinlik kanıtı diye sunulmaz.

Bu ayrım TÜBİTAK başvurusunda da işe yarar: ekibin gerçek yapabileceği teknik ölçütleri ana teslimat yapın; uzman görüşmesini teyit edilmemiş söz gibi değil, doğrulama iş adımı ve erişim riski olarak plana yazın. Uzman bulunamama riski için B planı hazır olsun.

### Kişisel hedef veri modeli

Klinik kuralı ile kullanıcıya ait hedef ayrı nesneler olmalı. Örneğin:

```text
PersonalNutritionTarget(
  target_id, user_id, nutrient_concept_id, value, unit,
  period_type, comparator, valid_from, valid_until,
  entry_source, verification_status, source_note, updated_at
)

ProductNutrientObservation(
  product_id, nutrient_concept_id, value, unit, basis_value,
  basis_unit, label_source, label_version, observed_at
)

ConsumptionEvent(
  user_id, product_id, consumed_amount, consumed_unit,
  event_time, product_match_status
)
```

`entry_source` ve `verification_status` kişisel hedefin nereden geldiğini gösterir; `source_note` hassas doktor belgesini saklamak zorunda değildir. İlk prototipte gereksiz klinik kayıt, laboratuvar sonucu veya ilaç listesi toplamadan çalışın. Kullanıcıya hedefi silme/düzeltme imkânı ve ayrı rıza vermeden kaydı tutmama seçeneği sunun. Birden fazla hastalık hedefi çakışıyorsa uygulama bunları kendi başına uzlaştırmaz; ayrı katkıları gösterir ve değerlendirmeyi uzmana bırakır.

## Kaynakların hastalık entegrasyonundaki olası rolü

- **WHO SMART Guidelines / klinik kılavuzlar:** Hedef kullanıcıyı, önerinin koşullarını, gerekli verileri ve karar mantığını şeffaf bir kural tablosuna dönüştürmek için yöntemsel örnek. Hastalığa özel klinik kaynağın yerine geçmez.
- **Hastalık kılavuzları ve ulusal profesyonel rehberler:** Gerçek kuralın ana bilimsel dayanağı. Her çıkarım kaynak yılı, bölüm, hasta grubu, öneri türü ve uzman yorumu ile saklanmalı.
- **CTD:** Kimyasal–disease literatür ilişkilerini ve dayanak yayınlarını keşfetmeye yarayabilir. CTD 2025 makalesi, curated doğrudan etkileşimlerin ve kimyasal/gen/phenotype üzerinden türetilmiş ilişkilerin ayrı tutulduğunu; kayıtların tür ve PubMed ID ile izlenebildiğini açıklar. CTD bir klinik beslenme kılavuzu veya market ürünü maruziyet ölçümü değildir. [CTD 2025 update](https://academic.oup.com/nar/article/53/D1/D1328/7816860)
- **JECFA:** Katkı maddesi, kirletici ve benzeri maddeler için toksikolojik değerlendirme özeti ve ADI/TDI geçmişi sağlar. Miktar/maruziyet bilinmeden bireysel ürün tüketim hesabı kurulamaz; hastalık temelli beslenme hedefi yerine geçmez. Veri tabanı Haziran 2026’daki 102. toplantı güncellemesine kadar değerlendirmeleri kapsadığını bildiriyor. [WHO JECFA Evaluations Database](https://apps.who.int/food-additives-contaminants-jecfa-database/Home)
- **FooDB:** Gıda bileşik/kimyasal verileri araştırma ve kimlik zenginleştirme için aday olabilir; ancak lisansı ticari kullanım açısından ciddi bir kapı oluşturur. Ayrıca etikette yazmayan bileşen miktarını üretmez. Ayrıntı için [ingredient mapping dosyasına](03-ingredient-semantic-matching.md) bakın.
- **Etiket taksonomileri ve ontolojiler:** Etiket terimlerini standardize etmeye yardımcı olur. Terim eşleştirme, klinik kuralı doğrulamaz.

## Önerilen karar modeli

Her hastalık kuralı kaynaklı ve sürümlü kayıt olsun. Bir kural en az şu alanları taşısın:

```text
rule_id, condition_concept_id, rule_type, target_product_attribute,
operator_or_logic, required_product_fields, required_user_fields,
applicable_population, exclusions, source_id, source_version,
source_section, evidence_type, reviewer_status, reviewed_at,
rule_version, uncertainty_message, output_template
```

`rule_type` sınırlı sözlükten seçilebilir: `ingredient_presence`, `allergen_declaration`, `nutrient_amount`, `portion_calculation`, `chemical_evidence_review`, `toxicological_exposure_review`. Hastalık adı ile içerik arasına gerekçe alanı koyun; arada “chemical–disease association” varsa bunu tek başına karar kuralı saymayın.

### Uygulama akışı

1. Kullanıcının seçtiği condition terimini kanonik bir kimlikle sakla; serbest metni ayrı tut.
2. Üründeki her ifadeyi önce türlendir: gıda/kompozit bileşen, kimyasal/additive, alerjen, besin öğesi veya çözümlenemeyen ifade.
3. Uygun ürün niteliği ve kullanıcı verisi var mı kontrol et. Etiketteki ingredient listesi ile besin değer tablosunu aynı veri gibi kullanma.
4. Geçerli kaynak ve uzman incelemesi bulunan başlangıç profili skorunu çalıştır; kullanıcı hedefi varsa ayrıca kişisel karşılaştırma yap. Veri eksikse tüm özelliği kapatmak yerine ölçülebilen bileşen skorunu ve coverage’ı göster.
5. Sonuçta karşılaştırılan veriyi, kaynak ve kural sürümünü, porsiyonu, sınırlılığı göster.
6. Kural kapsamı yoksa `Not assessed` / `Unverified` döndür; bazı etiket nitelikleri eksikse `Partial score` üret. Hiçbir profil sonucunu “güvenli”, “zararlı” veya kişiye özel klinik karar diye sunma.

## İlk pilot kapsamı için öneri

Hastalıkların “en yaygın ilk beşi” olmak, etiketlerden doğru değerlendirme yapabileceğimiz anlamına gelmez. Önceliği yaygınlığa ek olarak veri gözlemlenebilirliği, uzman kuralının bulunabilirliği, yanlış uyarının etkisi, örnek senaryo üretilebilirliği ve ekip/uzman erişimi ile belirleyin.

- **Aday 1 — çölyak/gluten:** İçerik/alerjen benzeri eşleşme katmanını ve belirsizlik durumlarını denemeye elverişli. Buğday alerjisiyle ayrı condition tipi olmalı; “glutensiz” etiketi veya çapraz bulaşma iddiası varsa yerel mevzuat ve doğru etiket kaynakları ayrıca incelenmeli.
- **Aday 2 — diyabet / karbonhidrat bilgisi:** Ingredient semantics’ten farklı ikinci mekanizmayı sınar. Ürün besin tablosu ve porsiyon hesabı olmadan sadece “şeker” adına bakarak değerlendirme yapılamaz. Kullanıcı hedef bilmese de ADA temelli başlangıç profili skorlanabilir; skor tek tip karbonhidrat limiti gibi sunulmaz. Kullanıcı hedef eklerse ayrı kişisel değerlendirme yapılır.
- **Aday 3 — kronik böbrek hastalığı:** Ürünlerde etiketle doğrulanabilen tuz/sodyum üzerinden başlangıç profile screening yapılabilir; KDIGO 2024 kapsamı, kanıt derecesi ve istisnalar skorda görünür olmalı. Potasyum/fosfor etikette yoksa değerlendirme kısmi kalır; tek bir fosfat katkısı toplam fosfor miktarı değildir.

Bunlar tıbbi tavsiye değil, **teknik pilot adayıdır**. Danışman ve uygun beslenme/sağlık uzmanı kapsamı onaylamalıdır.

## Araştırma ve doğrulama planı

1. Bir sayfalık condition coverage matrix hazırla: condition → kural türü → etiket/veri alanı → gereken kullanıcı girdisi → kaynak → hangi durumda abstain edilir.
2. Her pilot için en az bir güncel profesyonel kılavuz ve yerel etiket mevzuatı kaynağı seç; bölüm ve sürümü kaydet.
3. Uzmanla kuralları değerlendirecek senaryo formatını kararlaştır; ekip kendi yorumunu referans sonuç gibi kabul etmesin.
4. Ürün/condition/porsiyon senaryoları için bağımsız uzman altın standardı oluştur. Klinik katılımcı verisi toplanacaksa üniversitenin etik kurul ve veri koruma gerekliliklerini baştan belirle.
5. Hesaplama doğruluğu, eşleşme doğruluğu, false-positive/false-negative, değerlendirilebilir senaryo oranı ve uzmanlar arası uyumu ayrı raporla.

## Riskler ve kontrol

- **Korelasyonu klinik kural sanmak:** CTD ilişkisi veya vektör benzerliği, uyarı kuralına otomatik taşınmaz.
- **Etiket bileşeninden miktar çıkarmak:** Ingredient varlığı doz/maruziyet değildir.
- **Genel eşiği kişisel kural sanmak:** Klinik rehberlerin hedef/önerilerini “kesin zarar sınırı” diye sunma.
- **Hastalık ve alerji kavramlarını karıştırmak:** UI, veri sözlüğü ve test setinde ayrı tipler.
- **Eksik veriyle kesin sonuç:** Abstention kapsamını ve nedenini ölç; “doğrulanamadı” kullanıcıya açıklanmalı.
- **Birden fazla hastalık/ilaç durumu:** İlk pilotta kapsam dışı bırak veya uzmana yönlendir; etkileşimleri otomatik genelleme.

## Karar özeti

**Araştırma hipotezi:** NutriScan’de tek bir genel `ingredient -> disease` ilişki tablosu yerine, condition’a göre türü belli, kaynaklı kural ve ürünün ölçülen niteliklerini ayıran bir karar modeli daha doğrulanabilir olur. Bu hipotez; pilot gold seti, uzman incelemesi ve veri yeterliliği ile test edilmelidir.

**Sonraki çıktı:** Hastalık kapsam matrisi ve danışmana götürülecek 5–10 temsilî senaryo. Klinik eşik sayısı bu araştırma notunda kesinleştirilmemiştir.

## Kaynakça

- [WHO SMART Guidelines](https://www.who.int/teams/digital-health-and-innovation/smart-guidelines)
- [WHO SMART DAK — decision-support logic](https://smart.who.int/dak-pnc/v0.9.9/decision-logic.html)
- [NIDDK — Definition & Facts for Celiac Disease](https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease/definition-facts)
- [ADA Standards of Care in Diabetes—2026, Section 5](https://diabetesjournals.org/care/article/49/Supplement_1/S89/163932)
- [KDIGO 2024 CKD Guideline](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)
- [CTD 2025 update, Nucleic Acids Research](https://academic.oup.com/nar/article/53/D1/D1328/7816860)
- [WHO JECFA Evaluations Database](https://apps.who.int/food-additives-contaminants-jecfa-database/Home)
- [Türkiye Tarım ve Orman Bakanlığı — Türk Gıda Kodeksi](https://www.tarimorman.gov.tr/Konular/Gida-Ve-Yem-Hizmetleri/Gida-Hizmetleri/Kodeks)
