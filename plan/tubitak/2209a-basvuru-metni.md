# TÜBİTAK 2209-A 2026-1 — başvuru metni (TYBS alanlarına göre)

> **Başvuru No:** 1919B012605960 (TASLAK, yürütücü Levent Can Ceylan) · **Son gün:** 11 Kasım 2026 17.30 ·
> **Danışman onayı için hedef gönderim:** 30 Ekim 2026 (danışman 2 Kasım'dan sonra yok).
> Dayanak: Hilal'in 25 Ekim taslağı (yöntem titizliği, risk, bütçe, ÜYZ beyanı korundu) + tek araştırma sorusuna odak +
> ön çalışma bulguları. Bütün künyeler 25 Ekim 2026'da Crossref / resmî sayfadan doğrulandı (bkz. en alttaki doğrulama notu).
> Formdaki her başlık aşağıda aynı adla var; metin doğrudan kutuya yapıştırılır.

---

## Araştırma Projesi Bilgileri

**Proje Başlığı** (en fazla 495 karakter)

Türkçe Paketli Gıda Etiketlerinde İçerik İfadelerinin Kanonik Kavramlara Eşlenmesi: Sözlük Tabanlı ve Vektör Aramasıyla Desteklenen Yöntemlerin Karşılaştırılması ve Sağlık Durumuna Göre Kaynaklı Değerlendirme

**Anahtar Kelimeler** (3–5, virgülle)

Türkçe gıda etiketi, kavram normalizasyonu, vektör araması, kaynak izlenebilirliği, sağlık durumu değerlendirmesi

**Bilimsel ve Teknolojik Alan:** Mühendislik → Bilgisayar Bilimleri ve Mühendisliği → (sistemdeki listeden) Yapay Zekâ / Doğal Dil İşleme

**Öncelikli Alanlar:** Evet — TÜBİTAK 2026–2028 Öncelikli Ar-Ge ve Yenilik Konuları, Yapay Zeka ve Veri Bilimi → "Yapay Zekâda Güvenilirlik Çözümleri" (s. 201).

**Proje Özeti** (25–450 kelime)

Çölyak, diyabet ve kronik böbrek hastalığı gibi diyet kısıtı gerektiren sağlık durumlarına sahip tüketiciler, paketli bir gıdanın kendileri için uygun olup olmadığına Türkçe etiketteki içindekiler listesinden ve besin tablosundan karar vermek zorundadır. Etiket aynı bileşeni farklı biçimlerde gösterebilir (eş anlamlı, E-kodu, yazım ya da okuma hatası) ve sağlıkla ilgili bağlantı çoğu zaman etikette yazmaz: "buğday unu" ifadesinde "gluten" kelimesi geçmez. Bu nedenle değerlendirmenin ilk ve en kritik adımı, etiket ifadesinin standart (kanonik) bir kavrama doğru bağlanmasıdır. Ön çalışmamızda 60 gerçek Türk ürününden alınan 894 içerik ifadesinin, açık lisanslı Open Food Facts taksonomisine dayalı düz bir sözlükle %57'si hiçbir kavrama bağlanamamış; Türkçe çoğul eki, gürültü temizliği ve 81 ekip çevirisiyle bu oran %25'e inmiştir. Aynı çalışmada yazım hatalarını yakalayan bulanık eşleşmenin 28 kararından 6'sı yanlış kavrama bağlanmıştır ("askorbik asit" → sorbik asit gibi). Bu bulgu, tanınma oranının doğruluk anlamına gelmediğini ve yöntemlerin cevap anahtarı olan bir veri kümesinde karşılaştırılması gerektiğini göstermektedir.

Araştırmanın sorusu şudur: sözlük ve bulanık eşleşmeden oluşan tabana, taksonomide karşılığı bulunmayan ifadeler için çok dilli gömme vektörleriyle Qdrant aday araması eklemek; doğru kavrama bağlanma, yanlış kabul ve çekimser kalma oranlarını nasıl değiştirir? Gerçek ambalajlardan en az 400 ifadelik, iki ekip üyesinin bağımsız etiketlediği bir altın küme hazırlanacak; iki yöntem aynı ifadeler üzerinde eşleştirilmiş tasarımla karşılaştırılacak, farklar McNemar testiyle, oranlar Wilson güven aralıklarıyla raporlanacaktır. Eşlenen kavramlar, kaynakları mevzuat ve klinik kılavuzlara dayanan ve iki ekip üyesince bağımsız kontrol edilen deterministik bir kural tablosuyla değerlendirilecek; sonuç "Uygun değil", "Dikkat", "Engel bulunmadı" ya da "Doğrulanamadı" olacaktır. Vektör araması ve büyük dil modelleri sağlık sonucunu belirlemeyecek; emin olunmayan her durumda sonuç "Doğrulanamadı" kalacaktır. Kural değerlendirmesinde kaçırılan uyarı en kritik hata olarak ayrıca ölçülecektir.

Proje on iki ayda beş iş paketiyle yürütülecektir: protokol, altın küme, vektör araması deneyi, kaynaklı kural tablosu ve bütünleşik değerlendirme. Beklenen çıktılar Türkçe etiket ifadeleri için çift etiketli bir değerlendirme kümesi, iki eşleme yönteminin karşılaştırmalı sonuçları, kaynak izi tutulan bir kural kayıt modeli ve çalışan bir araştırma prototipidir. Çalışma, TÜBİTAK 2026–2028 Öncelikli Ar-Ge ve Yenilik Konuları'ndaki "Yapay Zekâda Güvenilirlik Çözümleri" başlığının izlenebilirlik, tekrarlanabilirlik ve veri soyağacı maddeleriyle doğrudan ilişkilidir. Proje klinik doğrulama, tanı ya da tedavi iddiası taşımaz.

---

## Araştırma Önerisi

### 1.1. Konunun Önemi ve Araştırma Önerisinin Bilimsel Niteliği

**Konunun önemi.** Çölyak hastalığı, glutene karşı gelişen ve ince bağırsağa zarar veren bağışıklık kaynaklı bir hastalıktır; bilinen tek tedavisi ömür boyu glutensiz diyettir [6]. Küresel meta-analizde biyopsiyle doğrulanmış yaygınlık %0,7, serolojik taramada %1,4 bulunmuştur [5]. Diyabet, kronik böbrek hastalığı ve hipertansiyonda ise sorun bir bileşenin varlığından çok miktarıdır: klinik kılavuzlar eklenmiş şekerin sınırlanmasını ve günlük sodyumun 2 g'ın altında tutulmasını önerir [7–9]. Bu kişiler için market rafında tek bilgi kaynağı ambalaj etiketidir. Etiketin içeriği mevzuatla belirlenmiştir: AB 1169/2011 sayılı Tüzük ve onunla uyumlu Türk Gıda Kodeksi Etiketleme Yönetmeliği içindekiler listesini, 14 alerjen grubunun vurgulanmasını ve 100 g ya da 100 ml başına beslenme bildirimini zorunlu kılar [1,2]; "içerebilir" uyarısı ise gönüllüdür. Etiket bu nedenle yarı yapılandırılmış bir veridir: biçim kurallıdır, ancak kelimeler serbesttir.

**Bilimsel problem.** Bir etiketi sağlık durumuna göre değerlendirmek iki ayrı soruya cevap gerektirir: (1) etikette yazan ifade hangi bileşeni ya da besin kavramını gösteriyor ve (2) bu kavram seçilen durum için hangi kaynaklı kurala takılıyor. Birinci soru doğru cevaplanmadan ikincisi anlamsızdır. Türkçe etiketlerde aynı bileşen eş anlamlıyla ("sakaroz", "şeker"), E-koduyla ("E330", "sitrik asit"), bileşik ifadeyle ("renklendirici (E102)") ve yazım ya da optik karakter tanıma (OCR) hatasıyla ("karbondiokst") görünür. Sağlıkla ilgili bağ çoğu zaman etikette yazmaz: "buğday unu", "bulgur" ya da "malt" ifadelerinde "gluten" geçmez. Tersine, buğdaydan elde edilen glikoz şurubu mevzuatta gluten kaynağı sayılmaz [2]; kelime düzeyinde arama burada yanlış alarm üretir. Serbest metindeki ifadeyi standart bir kavrama bağlama problemi biyomedikal alanda "varlık normalizasyonu" (entity normalization) olarak çalışılmıştır; eş anlamlı kümeleri ve öğrenilmiş temsiller kullanan yöntemler İngilizce biyomedikal veri kümelerinde yüksek başarı göstermiştir [12,13]. Çok dilli cümle gömme modelleri farklı dillerdeki anlamca yakın ifadeleri aynı vektör uzayında yakınlaştırır [14]. Ancak bu sonuçlar İngilizce biyomedikal testlere dayanır; Türkçe gıda etiketi ifadeleri için cevap anahtarlı bir değerlendirme kümesi ve yöntem karşılaştırması bulunmamaktadır.

**Ön bulgular ve araştırma boşluğu.** Açık lisanslı Open Food Facts içerik taksonomisi çok dilli bir başlangıç sözlüğü sunar [11]. Ekibimizin ön çalışmasında 60 gerçek Türk ürününden 894 ifade bu sözlükle eşlendiğinde %57'si hiçbir kavrama bağlanamamış, Türkçe çoğul eki, gürültü temizliği ve 81 ekip çevirisiyle tanınmayan oranı %25'e inmiştir. Aynı çalışmada yazım hatalarını yakalayan bulanık eşleşmenin [16] 28 kararından 6'sı yanlış kavrama bağlanmıştır ("askorbik asit" → sorbik asit, "sodyum sitrat" → sodyum nitrat). Bu iki gözlem, kapsamayı artıran her yöntemin yanlış kabul riskini de taşıdığını ve yöntemlerin yalnız tanınma oranıyla değil, cevap anahtarı olan bir altın kümede doğruluk ve çekimser kalma ile birlikte ölçülmesi gerektiğini gösterir. Piyasadaki etiket tarama uygulamaları genellikle genel bir puan verir ya da barkod veritabanına dayanır; bu çalışma "hastalığa göre ürün tarama ilk kez yapılıyor" iddiasında bulunmaz. Katkısı, Türkçe etiket ifadesini kanonik kavrama bağlayan hattın ölçülebilir biçimde karşılaştırılması ve sonucun her zaman bir mevzuat ya da kılavuz maddesine izlenebilmesidir. Kimyasal–hastalık ilişkisi veritabanları (CTD) ve katkı maddesi değerlendirmeleri (JECFA) araştırma bilgisi sağlar, ancak bir ilişki kaydı tek başına kişiye yönelik kural değildir [20,21]; bu nedenle karar yalnız kaynaklı kural tablosundan üretilir.

**Araştırma sorusu ve hipotezler.** Sözlük ve bulanık eşleşmeden oluşan tabana, taksonomide karşılığı bulunmayan ifadeler için çok dilli gömme vektörleriyle Qdrant aday araması eklemek, Türkçe etiket ifadelerinde doğru kavrama bağlanma, yanlış kabul ve çekimser kalma oranlarını nasıl değiştirir? H1: Hibrit yöntem, aynı ifadelerde doğru kavrama bağlanma oranını taban yönteme göre artırır. H2: Benzerlik eşiği ve aday doğrulama kuralı uygulandığında hibrit yöntemin yanlış kabul oranı taban yöntemden yüksek değildir. Sıfır hipotezleri iki yöntem arasında fark olmadığını öngörür; başarı artışı varsayılmaz.

**Öncelikli alanlarla ilişki.** Proje, TÜBİTAK 2026–2028 Öncelikli Ar-Ge ve Yenilik Konuları'nda Yapay Zeka ve Veri Bilimi alanındaki "Yapay Zekâda Güvenilirlik Çözümleri" başlığıyla ilişkilidir [22]. Bu başlıktaki geriye dönük izlenebilirlik, işlemlerin tekrarlanabilirliği, tutarlılık metrikleri ve verinin soyağacıyla kayıt altına alınması maddeleri; projede her sonucun kural ve kaynak satırına izlenmesi, aynı girdinin aynı kural sürümüyle her zaman aynı sonucu üretmesi, sözlük ve kural kayıtlarında kaynak ve sürüm tutulması ve yöntemlerin sabit bir test kümesinde ölçülmesiyle doğrudan karşılanır.

### 1.2. Amaç ve Hedefler

**Genel amaç.** Türkçe paketli gıda etiketi ifadelerinin kanonik kavramlara bağlanmasında, sözlük tabanlı yönteme taksonomi dışı ifadeler için vektör araması eklemenin doğruluk, yanlış kabul ve çekimser kalma üzerindeki etkisini cevap anahtarlı bir veri kümesinde ölçmek ve eşlenen kavramları kaynaklı, denetlenebilir bir kural tablosuyla sağlık durumuna göre değerlendiren bir araştırma prototipi geliştirmek.

**Ölçülebilir hedefler.**

1. **Altın küme:** Gerçek ambalajlardan en az 400 Türkçe içerik ifadesini iki ekip üyesiyle bağımsız etiketlemek (kanonik kavram, "taksonomide yok" ya da "belirsiz"); etiketleyiciler arası uyumu Cohen kappa ile raporlamak (hedef κ ≥ 0,80) ve uyuşmazlıkları gerekçeli uzlaştırmayla kapatmak.
2. **Yöntem karşılaştırması:** Taban (sözlük + bulanık eşleşme) ve hibrit (taban + Qdrant aday araması) yöntemleri aynı test ifadelerinde çalıştırıp ilk aday doğruluğu, kabul edilen eşleşmelerde isabet, yanlış kabul oranı, çekimser kalma oranı ve ilk 5 adayda doğru kavramı bulma oranını (Recall@5) %95 güven aralıklarıyla raporlamak; farkı McNemar testiyle sınamak.
3. **Hata analizi:** Yanlış ve çekimser sonuçları ifade türüne (Türkçe ad, E-kodu, bileşik ifade, İngilizce, OCR gürültüsü) göre sınıflandırmak ve her sınıf için örnek sayısını raporlamak.
4. **Kaynaklı kural tablosu:** Danışmanla netleştirilecek sağlık durumu listesinin her satırını bir mevzuat ya da klinik kılavuz maddesine bağlamak; her satırın iki ekip üyesince bağımsız kontrol edilmesi ve kontrol edilmemiş satır sayısının sıfır olması.
5. **Kural sınavı:** En az 40 ürün × durum senaryosunda beklenen sonucu kaynaktan önceden yazmak; sistemin kaçırdığı uyarı sayısını (hedef 0), gereksiz uyarı sayısını ve "Doğrulanamadı" oranını raporlamak.

### 2. Yöntem

**Araştırma tasarımı.** Eşleştirilmiş, karşılaştırmalı bir yazılım değerlendirmesi yapılacaktır. Bağımsız değişken eşleme yöntemidir: (A) taban yöntem; (B) hibrit yöntem. Her iki yöntem aynı test ifadelerine uygulanır; böylece fark ifade zorluğundan değil yöntemden kaynaklanır. Bağımlı değişkenler; ilk aday doğruluğu, kabul edilen eşleşmelerde isabet, yanlış kabul oranı, çekimser kalma oranı, kapsama ve Recall@5'tir.

**Ön çalışma ve fizibilite.** Ekip, Python ile çalışan bir prototip geliştirmiştir: etiket metnini Türkçe kurallarla normalleştiren ve parantez, "sınıf: madde" ve "içerebilir" kalıplarını ayıran bir ayrıştırıcı; E-kodu, birebir eş anlamlı, Türkçe çoğul ve bulanık eşleşme adımlarından oluşan bir eşleyici; 7 sağlık durumu için 17 kaynaklı satırdan oluşan taslak bir kural tablosu ve bunları doğrulayan 12 otomatik test. Sözlük, Open Food Facts taksonomisinden üretilmiş 5.459 kavram ve 10.465 yazılıştan oluşur [11]. 60 gerçek ürünün 894 ifadesinde tanınmayan oran %57'den %25'e inmiş; bulanık eşleşmenin 28 kararından 6'sı yanlış bulunmuştur. Ayrıca "irmik" ve "arpa maltı" gibi gluten kaynağı Türkçe ifadelerin sözlükte bulunmadığı ve "glikoz şurubu (buğday)" kalıbında köken bilgisinin ayrı içerik sayılarak gereksiz uyarı ürettiği tespit edilmiştir. Bu bulgular hem yöntemin uygulanabilir olduğunu hem de ölçümün neden gerekli olduğunu göstermektedir.

**Veri ve altın küme (İP2).** İfadeler iki kaynaktan gelecektir: ön çalışmadaki 894 ifadeden tabakalı örneklem ve Antalya'da 10 satış noktasında ürün satın alınmadan fotoğraflanan ambalajlar. Örneklem; Türkçe ad, E-kodu, bileşik ifade, İngilizce ifade ve OCR gürültüsü içeren ifade gruplarını kapsayacak şekilde tabakalanır ve en az 400 ifadeye ulaşır. Her ifadeyi iki ekip üyesi birbirini görmeden etiketler: kanonik kavram kimliği, "taksonomide karşılığı yok" ya da "belirsiz". Uyum Cohen kappa ile ölçülür [18]; uyuşmazlıklar gerekçesi kaydedilerek uzlaştırılır. Küme %30 geliştirme, %70 test olarak bölünür. Eşik ve model seçimi yalnız geliştirme kümesinde yapılır; test ifadelerinin yazılışları sözlüğe ya da vektör veritabanına eklenmez, böylece veri sızıntısı önlenir.

**Taban yöntem (A).** İfade Türkçe küçük harf kuralı, yüzde ve işaret temizliğiyle normalleştirilir; ardından sırasıyla E-kodu, birebir eş anlamlı, Türkçe çoğul eki ayıklanmış biçim ve bulanık eşleşme denenir. Bulanık eşleşmede Ratcliff–Obershelp benzerlik ölçüsü kullanılır [16]; eşik geliştirme kümesinde seçilir. Hiçbiri tutmazsa sonuç çekimserdir ("tanınmayan").

**Hibrit yöntem (B).** Taban yöntemin çekimser kaldığı ifadeler çok dilli bir cümle gömme modeliyle vektöre çevrilir ve sözlükteki bütün yazılışların vektörlerini tutan Qdrant koleksiyonunda en yakın 5 aday aranır [15]. Aday model LaBSE'dir [14]; ilk iki ayda geliştirme kümesinde en az bir alternatifle karşılaştırılarak seçilir ve sürümü sabitlenir. En yakın adayın benzerliği eşik değerin altındaysa ya da ilk iki aday farklı kavramlara ait olup aralarındaki fark küçükse sonuç çekimser kalır. Qdrant yalnız aday üretir; sağlık sonucunu belirlemez.

**İstatistiksel analiz (İP3).** İki yöntemin her test ifadesindeki doğru/yanlış sonuçları eşleştirilmiş 2×2 tabloda karşılaştırılır ve fark tam (exact) McNemar testiyle sınanır [17]. Oranlar Wilson %95 güven aralıklarıyla verilir [19]. Sonuçlar ifade türüne göre alt gruplarda raporlanır; örnek sayısı yetersiz alt gruplar için yalnız betimleyici sonuç verilir.

**Kaynaklı kural tablosu ve kural sınavı (İP4).** Eşlenen kavramlar bir kural tablosuyla değerlendirilir. Kurala yalnız mevzuat (AB 1169/2011, 1924/2006, 828/2014 ve Türk Gıda Kodeksi [1–4]) ve klinik kılavuzlar [7–9] girer; EFSA görüşleri destekleyici kaynaktır [10]. Kurallar beş türdedir: varlık ("bu madde varsa"), miktar ("bu besin 100 g'da şu sınırı aşıyorsa"), beyan ("glutensiz" ifadesi), içerebilir uyarısı ve varsayılan sonuç. Miktar gerektiren durumda besin değeri yoksa kullanıcıdan besin tablosu istenir; gelmezse sonuç "Doğrulanamadı" olur. Tanınmayan bir ifade varsa "Engel bulunmadı" sonucu verilmez. Her satır kaynak belgesi, bölümü ve sürümüyle kaydedilir ve iki ekip üyesince bağımsız kontrol edilmeden etkinleştirilmez. Büyük dil modelleri kaynak bulma ve kural alanlarını taslaklamada yardımcı olabilir, ancak onaylanmamış satır kullanılmaz ve model kullanıcı sonucunu belirlemez. Kural sınavında en az 40 ürün × durum senaryosu için beklenen sonuç kaynaktan önceden yazılır; kaçırılan uyarı, gereksiz uyarı ve "Doğrulanamadı" sayıları raporlanır. Bu sınav klinik doğrulama değil, kurala uygunluk testidir.

**Bütünleşik prototip (İP5).** Telefonda OCR ile okunan ve kullanıcı tarafından düzeltilen etiket metni bir sunucu servisine gönderilir; servis eşleme ve kural adımlarını çalıştırıp her durum için sonucu, gerekçeyi ve kaynağı döndürür. Ürün ve sağlık bilgisi sunucuda saklanmaz. Yöntemlerin iş paketleriyle ilişkisi çalışma takviminde verilmiştir.

### 3.1. Çalışma Takvimi

| Proje Süresi (Ay) | Faaliyetler | Kim(ler) Tarafından Gerçekleştirileceği | Başarı Ölçütü ve Araştırmanın Başarısına Katkısı |
|---|---|---|---|
| 1–2 | İP1 · Kapsam ve deney protokolü: sağlık durumu listesinin danışmanla netleştirilmesi, kaynak ve lisans envanteri, etiketleme kılavuzu, gömme modeli ve eşik seçim planı | Levent Can Ceylan (protokol), Şükran Hilal Hocaoğlu (kaynak ve lisans), Ozan Karadaş (model seçimi) | Yazılı protokol, lisans envanteri ve etiketleme kılavuzu tamamlanır. Katkı: %15 |
| 2–4 | İP2 · Altın küme: ambalaj fotoğraflama, transkripsiyon, en az 400 ifadenin çift bağımsız etiketlenmesi, uzlaştırma, geliştirme/test bölmesi | Tüm ekip | 400/400 ifade çift etiketli; Cohen kappa raporlanır (hedef ≥ 0,80). Katkı: %20 |
| 4–7 | İP3 · Hibrit eşleme deneyi: Qdrant koleksiyonu, model ve eşiğin geliştirme kümesinde sabitlenmesi, iki yöntemin test kümesinde karşılaştırılması, hata analizi | Ozan Karadaş (vektör araması), Levent Can Ceylan (deney ve analiz) | İki yöntem için metrik tablosu, McNemar testi ve hata sınıfları raporlanır. Katkı: %25 |
| 5–9 | İP4 · Kaynaklı kural tablosu ve kural sınavı: kural satırlarının yazılması, iki bağımsız kontrol, en az 40 senaryonun hazırlanması ve çalıştırılması | Şükran Hilal Hocaoğlu (kurallar ve kaynaklar), Levent Can Ceylan (kural motoru) | Kontrol edilmemiş satır sayısı 0; kaçırılan uyarı, gereksiz uyarı ve "Doğrulanamadı" oranları raporlanır. Katkı: %25 |
| 9–12 | İP5 · Bütünleşik prototip ve sonuç: OCR ve kullanıcı düzeltmesiyle uçtan uca akış, sonuç raporu, bildiri taslağı | Tüm ekip | Uçtan uca çalışan prototip, final raporu ve bildiri taslağı. Katkı: %15 |

### 3.2. Risk Yönetimi

| En Önemli Riskler | Alınacak Tedbirler (B Planı) |
|---|---|
| Altın küme için yeterli ve çeşitli gerçek etiket toplanamaması | Ön çalışmadaki 894 ifadeden tabakalı örneklem başlangıç kümesi olarak kullanılır; fotoğraflama ilk iki ayda başlar. Alt grup sayısı yetmezse o alt grup için yalnız betimleyici sonuç verilir; sentetik ifade gerçek etiket gibi sayılmaz. |
| Vektör aramasının yanlış kabulü artırması | Aday yalnız eşik üstündeyse ve ilk iki aday ayrışıyorsa kabul edilir; aksi halde çekimser kalınır. Yanlış kabul ayrı metrik olarak raporlanır; hibrit yöntem kötü sonuç verirse bu da araştırma bulgusu olarak sunulur ve prototipte taban yöntem kullanılır. |
| İki etiketleyici arasında düşük uyum | Etiketleme kılavuzu geliştirme kümesinde denenip güncellenir; uyuşmazlıklar gerekçesiyle kaydedilir ve uzlaştırılır; kappa değeri olduğu gibi raporlanır. |
| Kural eşiklerinde mevzuattaki beyan sınırı ile klinik önerinin karıştırılması | Her kural satırında kaynak türü (mevzuat, klinik kılavuz, EFSA görüşü) ayrı tutulur; kaynağı bulunmayan durum için kural yazılmaz ve sonuç "Doğrulanamadı" olur. |
| OCR ya da mobil arayüzün takvimi aşması | Araştırmanın ana çıktısı metin tabanlı deney ve altın kümedir; OCR son iş paketindeki gösterim katmanına daraltılır, deney tasarımı değişmez. |

### 3.3. Araştırma Olanakları

| Kuruluşta Bulunan Altyapı/Ekipman Türü - Modeli | Projede Kullanım Amacı |
|---|---|
| Ekip üyelerinin kişisel bilgisayarları | Prototip geliştirme, eşleme deneylerinin ve istatistiksel analizin yürütülmesi |
| Açık kaynak yazılımlar: Python, Qdrant (yerel kurulum), PostgreSQL | Eşleme hattı, vektör araması ve bilgi tabanı; lisans ücreti gerektirmez |
| Ekibin mevcut prototipi ve ön çalışma verisi (5.459 kavramlık sözlük, 894 ifadelik ön örneklem, 17 satırlık taslak kural tablosu) | Taban yöntemin çalıştırılması ve altın kümenin başlangıç örneklemi |

### 4. Araştırma Önerisinin Yaygın Etkisi

| Çıktı, Etki ve Kazanımlar | Öngörülen Çıktı(lar), Etki(ler) ve Kazanım(lar) |
|---|---|
| Bilimsel/Akademik Çıktılar | Türkçe gıda etiketi ifadelerinde sözlük tabanlı ve vektör aramasıyla desteklenen eşleme yöntemlerinin karşılaştırmasını sunan bir ulusal kongre bildirisi; yöntem, altın küme protokolü ve hata analizini içeren proje sonuç raporu. |
| Ekonomik/Ticari/Sosyal Çıktılar | En az 400 ifadelik, çift etiketli Türkçe etiket ifadesi değerlendirme kümesi (veri kaynaklarının lisansı uygunsa açık paylaşım); kaynak ve sürüm tutan kural kayıt modeli; diyet kısıtı olan tüketicilere kaynağı gösterilmiş sonuç veren, çalışan bir araştırma prototipi. |
| Yeni Proje(ler) Oluşturmasına Yönelik Çıktılar | Sonuçlara göre kapsamın yeni sağlık durumlarına ve gıda alerjilerine genişletildiği bir devam projesi; sanayi işbirliğiyle 2209-B ya da benzeri bir programa başvuru. |

### 5. Belirtmek İstediğiniz Diğer Konular

Proje, CSE 491/492 bitirme projesi kapsamında başlatılmış ve danışman görüşmelerinde bu araştırma sorusuna odaklanmıştır. Ön çalışmadaki prototip, sözlük ve ölçüm raporları ekibin sürüm kontrollü deposunda tutulmaktadır. Başvuru metninin hazırlanmasında üretken yapay zekâ araçlarından yararlanılmış; bu kullanım ÜYZ beyan bölümünde ayrıntılı olarak bildirilmiştir. Bütün kaynaklar özgün yayın ya da resmî sayfa üzerinden ekipçe doğrulanmış, sayısal değerler ekibin kendi ölçümlerinden alınmıştır. Proje gerçek kişilerden sağlık verisi toplamaz; değerlendirmeler ürün etiketleri ve önceden yazılmış senaryolar üzerinde yapılır.

### 6. Ekler

(Boş bırakılacak.)

---

## Kaynaklar (Kaynakça kutusu, en fazla 32.000 karakter)

[1] T.C. Tarım ve Orman Bakanlığı. Türk Gıda Kodeksi Gıda Etiketleme ve Tüketicileri Bilgilendirme Yönetmeliği. Resmî Gazete, 26.01.2017, Sayı: 29960 (Mükerrer).

[2] European Parliament and Council. Regulation (EU) No 1169/2011 on the provision of food information to consumers. Official Journal of the European Union, L 304, 22.11.2011, s. 18–63. https://eur-lex.europa.eu/eli/reg/2011/1169/oj

[3] European Parliament and Council. Regulation (EC) No 1924/2006 on nutrition and health claims made on foods. Official Journal of the European Union, L 404, 30.12.2006, s. 9–25. https://eur-lex.europa.eu/eli/reg/2006/1924/oj

[4] European Commission. Commission Implementing Regulation (EU) No 828/2014 on the requirements for the provision of information to consumers on the absence or reduced presence of gluten in food. Official Journal of the European Union, L 228, 31.7.2014, s. 5–8. https://eur-lex.europa.eu/eli/reg_impl/2014/828/oj

[5] Singh, P., Arora, A., Strand, T. A., Leffler, D. A., Catassi, C., Green, P. H., Kelly, C. P., Ahuja, V., & Makharia, G. K. (2018). Global prevalence of celiac disease: Systematic review and meta-analysis. Clinical Gastroenterology and Hepatology, 16(6), 823–836.e2. https://doi.org/10.1016/j.cgh.2017.06.037

[6] National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK). Celiac Disease. Erişim: 25.10.2026. https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease

[7] American Diabetes Association Professional Practice Committee. (2026). 5. Facilitating positive health behaviors and well-being to improve health outcomes: Standards of Care in Diabetes—2026. Diabetes Care, 49(Supplement 1), S89–S131. https://doi.org/10.2337/dc26-S005

[8] Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. (2024). KDIGO 2024 clinical practice guideline for the evaluation and management of chronic kidney disease. Kidney International, 105(4S), S117–S314. https://doi.org/10.1016/j.kint.2023.10.018

[9] World Health Organization. (2012). Guideline: Sodium intake for adults and children. Geneva: World Health Organization. https://www.who.int/publications/i/item/9789241504836

[10] EFSA Panel on Dietetic Products, Nutrition and Allergies (NDA). (2010). Scientific opinion on lactose thresholds in lactose intolerance and galactosaemia. EFSA Journal, 8(9), 1777. https://doi.org/10.2903/j.efsa.2010.1777

[11] Open Food Facts. Ingredients taxonomy (taxonomies/food/ingredients.txt), Open Database License (ODbL). Erişim: 22.10.2026. https://github.com/openfoodfacts/openfoodfacts-server/blob/main/taxonomies/food/ingredients.txt

[12] Sung, M., Jeon, H., Lee, J., & Kang, J. (2020). Biomedical entity representations with synonym marginalization. Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL), 3641–3650. https://doi.org/10.18653/v1/2020.acl-main.335

[13] Liu, F., Shareghi, E., Meng, Z., Basaldella, M., & Collier, N. (2021). Self-alignment pretraining for biomedical entity representations. Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT), 4228–4238. https://doi.org/10.18653/v1/2021.naacl-main.334

[14] Feng, F., Yang, Y., Cer, D., Arivazhagan, N., & Wang, W. (2022). Language-agnostic BERT sentence embedding. Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 878–891. https://doi.org/10.18653/v1/2022.acl-long.62

[15] Qdrant. Search — Qdrant documentation. Erişim: 25.10.2026. https://qdrant.tech/documentation/search/search/

[16] Python Software Foundation. difflib — Helpers for computing deltas. Python 3 documentation. Erişim: 25.10.2026. https://docs.python.org/3/library/difflib.html

[17] McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika, 12(2), 153–157. https://doi.org/10.1007/BF02295996

[18] Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement, 20(1), 37–46. https://doi.org/10.1177/001316446002000104

[19] Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. Journal of the American Statistical Association, 22(158), 209–212. https://doi.org/10.1080/01621459.1927.10502953

[20] Davis, A. P., Wiegers, T. C., Sciaky, D., Barkalow, F., Strong, M., Wyatt, B., Wiegers, J., McMorran, R., Abrar, S., & Mattingly, C. J. (2025). Comparative Toxicogenomics Database's 20th anniversary: update 2025. Nucleic Acids Research, 53(D1), D1328–D1334. https://doi.org/10.1093/nar/gkae883

[21] Joint FAO/WHO Expert Committee on Food Additives (JECFA). Evaluations of the Joint FAO/WHO Expert Committee on Food Additives database. Erişim: 25.10.2026. https://apps.who.int/food-additives-contaminants-jecfa-database/

[22] TÜBİTAK. (2026). TÜBİTAK 2026–2028 Öncelikli Ar-Ge ve Yenilik Konuları, v01.07.2026, s. 201. https://tubitak.gov.tr/sites/default/files/2026-08/TUBITAK_2026-2028_Ar-Ge_ve_Yenilik_Konulari-v01.07.2026.pdf

---

## Bütçe

| Kalem | Tutar (TL) | Gerekçe |
|---|---|---|
| Makine-Teçhizat | 0 | Mevcut bilgisayarlar yeterli |
| Hizmet Alımı | 0 | Ücretli API, bulut ya da hizmet gerekmiyor |
| Sarf Malzemesi | 0 | Ambalajlar satın alınmadan fotoğraflanır |
| Ulaşım | 1.200 | 10 satış noktası ziyareti × 3 öğrenci × 2 biniş × 20 TL (Antalyakart öğrenci binişi, 25.10.2026'da antalyakart.com.tr/Page/Faqs sayfasından doğrulandı) |

---

## Doğrulama notu (forma girmez)

- Crossref ile doğrulanan künyeler (25.10.2026): [5], [7] (başlık ve sayfa), [8], [10], [12], [13], [14], [17], [18], [19], [20].
- EUR-Lex: [2], [3], [4] (OJ numarası, tarih, sayfa). [22]: PDF indirildi, "Yapay Zekâda Güvenilirlik Çözümleri" s. 201'de.
- Sayılar `tests/eslesme/off_rapor.md` ve `data/` dosyalarından: 894 ifade, 223 tanınmayan (%25), 28 bulanık kararın 6'sı yanlış
  (askorbik asit → sorbik asit ×3, sodyum sitrat → sodyum nitrat ×2, yağlı süt tozu → yağsız süt tozu ×1).
- Hilal'in taslağından fark: tek araştırma sorusu (S2 "AI ile kural taslağı" araştırma sorusu değil, yöntem içinde yardımcı adım);
  14 alerjen grubu ana hedef değil (ekip kararı bekliyor); altın küme 120 → 400; 42 kurgu senaryo yerine ≥ 40 ürün × durum senaryosu.
- Formda doldurulmayacak, Levent'in gireceği alanlar: danışman ve proje ortaklarının TC kimlik numaraları, fotoğraf, adres (ARBİS),
  banka bilgileri, taahhüt ve onay kutuları.
