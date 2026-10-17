# NutriScan için kaynak, telif ve lisans kontrolü

**Kısa özet:** Yayımlanmış bilimsel çalışmaları okuyup kaynak göstererek kendi kural şemanızı oluşturmanız tek başına “telif ihlali” anlamına gelmez. Risk; makale veya kılavuz metnini, tablolarını, görsellerini ya da bir veri tabanının kayıtlarını lisansını incelemeden yazılıma, eğitim verisine, uygulama arayüzüne veya herkese açık depoya kopyalamakla artar. Kaynak belirtmek gerekir; ancak kaynak belirtmek, her türlü kopyalama için izin yerine geçmez.

**Durum:** İlk lisans taraması; hukuki görüş değildir. Aşağıdaki kaynak ve lisans bilgileri 15 Ekim 2026 tarihinde kontrol edildi. Veri kaynağı, sürüm ve kullanım biçimi değiştikçe yeniden kontrol edilmelidir.

## 1. NutriScan'in hangi kullanımı ne anlama geliyor?

| Kullanım | İlk değerlendirme | NutriScan için dikkat |
|---|---|---|
| Makaleyi/kılavuzu okuyup tezde kendi cümlelerinizle özetlemek | Genellikle olağan bilimsel çalışma; doğru atıf gerekir | Kaynağın sürümünü, bölüm/sayfasını ve erişim tarihini saklayın. Uzun alıntı, tablo veya görsel eklemeden önce yayıncının koşullarına bakın. |
| Kılavuzdaki bir öneriyi kendi veri şemanızda yapılandırmak | Metni veya tablonun düzenini kopyalamaktan farklıdır; yine de kaynağın ve kullanım koşullarının kaydı gerekir | Örneğin kurum, kılavuz sürümü, yıl, hedef nüfus, öneri, koşul/istisna, kanıt gücü ve ilgili bölüm alanlarını kaydedin. Öneriyi kendi ifadelerinizle yazın. |
| Bir kılavuzdaki tabloyu veya şekli uygulama/tez içine aynen almak | Daha yüksek telif riski; atıf tek başına izin olmayabilir | Açık lisans koşulunu veya yayıncıdan yazılı izni kontrol edin. Tezdeki akademik alıntı istisnası, tabloyu ticari uygulamaya koyma izni gibi varsayılmamalı. |
| Açık veri tabanından kayıtları indirip kendi DB'nize taşımak | Lisansın kapsamı, türev veri tabanı, atıf ve yeniden dağıtım koşulları incelenmeli | Yalnızca API'ye erişilebiliyor olması, verinin her amaçla kopyalanıp yeniden dağıtılabileceği anlamına gelmez. |
| Veri kaynağından embedding üretmek veya veriyi normalize etmek | Lisans incelemesini atlatma yöntemi sayılmamalı | Türetilmiş kayıtların, vektörlerin veya indeksin lisans etkisi kullanım biçimine bağlı olabilir; bunu kaynağın lisansı özelinde değerlendirin. |
| Ürün fotoğrafı veya başka bir kurumun görselini kullanmak | Görselin hakkı, veri tabanı lisansından ayrı olabilir | Görseli ayrıca lisanslayın; fotoğrafta üçüncü taraf marka/logo veya başka haklar da bulunabilir. |

Türkiye Kültür ve Turizm Bakanlığı, telif korumasının eser meydana getirildiğinde başladığını ve fikirlerin soyut halde değil somutlaşmış eserler olarak korunduğunu açıklıyor. Bakanlığın FSEK 35 açıklamasında bilimsel eserlerde alıntının belli olması, eser ve eser sahibinin yanında alıntı yerinin de belirtilmesi gerektiği yazıyor. Bu kurallar sınırsız kopyalama izni değildir; istisnanın somut kullanımınıza uygulanıp uygulanmadığı ayrıca değerlendirilmelidir. [Telif Hakkı Nasıl Korunur?](https://telifhaklari.ktb.gov.tr/TR-332374/telif-hakki-nasil-korunur.html), [Genel Sorular — alıntı ve FSEK 35](https://telifhaklari.ktb.gov.tr/TR-332449/genel-sorular.html)

## 2. Projede adı geçen veri kaynakları için ilk bulgular

### FooDB

FooDB, verileri ve metaverileri için **CC BY-NC 4.0** lisansını belirtiyor. Lisans, ticari olmayan kullanımlar için atıf koşullu ve telif ücreti istemeyen bir kullanım izni verir; ticari kullanıma izin vermez. FooDB'nin About sayfası da verinin tamamının veya bir bölümünün ticari amaçla kullanılması/yeniden dağıtılması için açık izin gerektiğini söylüyor. Yalnızca akademik bitirme projesi kapsamında kalan, ticari kazanç/avantaj amacı taşımayan bir prototip bu lisansla kullanılabilir bir senaryo olabilir; ancak “uygulama kullanıcıya ücretsiz” tek başına yeterli ölçüt değildir. CC BY-NC tanımı kullanımın öncelikli amacına bakar. Bu nedenle amaç, tanıtım, fonlama ve dağıtım biçimi belirsizse bunu kesin hukuki sınıflandırma gibi sunmayın. [FooDB Compliance](https://foodb.ca/compliance), [FooDB About](https://foodb.ca/about), [CC BY-NC 4.0 lisans metni](https://creativecommons.org/licenses/by-nc/4.0/legalcode)

Bitirme projesi için uygun lisans koşullarıyla kullanımın kendisi genellikle veri sahibine ayrı lisans ücreti ödemek anlamına gelmez; atıf, lisans bağlantısı, değişiklikleri belirtme ve ticari olmayan amaç koşullarına uymak gerekir. Ancak NutriScan daha sonra ticari avantaja yönelirse aynı veri kullanımını sürdürmeden önce izin alınmalı veya uygun lisanslı başka veri kaynağı seçilmelidir. Akademik prototip, herkese açık depo/demo ve ileride ürünleşme ayrı kullanım aşamaları olarak envanterde izlenmeli.

### Open Food Facts (OFF)

OFF, veri tabanını **ODbL**, tek tek içerikleri **Database Contents License**, ürün görsellerini ise **CC BY-SA** kapsamında tanımlıyor; görsellerde ek haklar da bulunabileceğini belirtiyor. ODbL, kamuya sunulan türev veri tabanları için atıf ve paylaşım koşulları içeriyor. Buna karşılık bir koleksiyon veri tabanında OFF verisinin yanına bağımsız başka veri tabanları konması ile OFF kayıtlarından türev veri tabanı oluşturulması aynı durum değildir. Ürün DB'nizin hangi kategoriye gireceği ve uygulamanın nasıl dağıtıldığı netleşince lisans metni üzerinden uzman incelemesi yapılmalı. Bu yüzden “OFF kullanırsak bütün uygulama açık kaynak olmak zorunda” gibi genellemeler yapmayın; ODbL'nin veri tabanı kapsamı ile uygulamanın kaynak kodu ve ürün çıktıları birbirinden ayrıştırılmalı. [OFF lisans açıklaması](https://openfoodfacts.github.io/openfoodfacts-server/api/tutorials/license-be-on-the-legal-side/), [ODbL 1.0 tam lisans metni](https://opendatacommons.org/licenses/odbl/1-0/)

NutriScan ürün fotoğraflarını kullanmayacaksa görsel lisansı konusu kapsam dışı kalabilir; yine de OFF'tan alınan diğer alanların lisans/atıf şartları devam eder. Uygulama yalnızca API'yi çağırsa dahi API'nin güncel kullanım ve yeniden kullanım koşulları kontrol edilmelidir.

### Klinik kılavuzlar ve makaleler

Bir kılavuzdaki sağlık önerisini kaynak göstererek kendi alanlarınızda yapılandırmak, kılavuzun tam metnini veya tablosunu kopyalamaktan ayrıdır. NutriScan'in kural kaydı şunları tutabilir: yayın/kılavuz adı, yayımlayan kurum, sürüm/yıl, bölüm veya sayfa, hedef nüfus, önerinin kendi kısa ifadesi, varsa açık sayı ve birim, istisna/koşul, kanıt derecesi ve kaynak URL'si. Sayısal değerleri kaynağın kapsamı ve bağlamıyla birlikte aktarın; kılavuzdaki tüm tabloyu veri tabanına aynen geçirmek, özellikle dağıtılan yazılım için ayrıca izin/lisans incelemesi gerektirebilir.

Bu lisans değerlendirmesi, önerinin klinik olarak doğru olduğu anlamına gelmez. Sağlık kuralının bilimsel geçerliliği, güncelliği, hedef nüfusa uygulanabilirliği ve güvenlik değerlendirmesi ayrı iş paketidir.

## 3. Şimdiden kaydetmemiz gereken kaynak envanteri

Her veri veya model kaynağı için bu alanları bir `data_sources`/kaynak envanterinde (veya en azından CSV/Markdown kaydında) tutun:

| Alan | Örnek içerik |
|---|---|
| Kaynak kimliği | `off-ingredients-taxonomy` |
| Kaynağın adı ve sahibi | Open Food Facts Ingredients Taxonomy |
| Tam URL ve sürüm/commit/snapshot tarihi | Erişilen sürüm ve indirme tarihi |
| Lisans ve lisans URL'si | ODbL 1.0; gerekiyorsa içerik lisansı ayrıca |
| Alınan alanlar | Terim, eş anlamlı, ID, kategori vb. |
| Dönüşüm | Türkçe normalizasyon, eşleştirme, çıkarılan alanlar vb. |
| Dağıtım biçimi | Yalnızca kurum içi; tez eki; herkese açık depo; çalışan servis; ticari ürün |
| Atıf biçimi | Lisansın gerektirdiği görünür atıf ve değişiklik bildirimi |
| Yeniden dağıtım / share-alike / NC durumu | Koşul ve çözümlenmemiş sorular |
| Sorumlu ve inceleme tarihi | Ekip üyesi, sonraki kontrol tarihi |

Model ağırlıkları, embedding modelleri, kod kütüphaneleri, ontology/vocabulary dosyaları, benchmark veri setleri ve demo ürün görselleri için de ayrı lisans kaydı açın. Her birinin lisansı farklı olabilir.

## 4. NutriScan için önerilen güvenli iş akışı

1. **Kaynağı tam olarak sabitleyin.** Ad, URL, lisans, sürüm/commit ve erişim tarihini kaydedin. “İnternetten bulundu” kaynak envanteri için yeterli değildir.
2. **Kullanım senaryosunu belirtin.** Sadece kendi cihazınızda deney, tez/metin, herkese açık GitHub deposu, TÜBİTAK başvurusu/demo ve ticari ürün dağıtımı aynı varsayılmamalı.
3. **Kılavuzu okuyup kuralı bağımsız biçimde yazın.** Kısa ve kendi ifadelerinizle yapılandırın; kaynağı, ilgili yeri, popülasyonu, koşul/istisnayı ve belirsizliği saklayın. Tam paragraf, şekil veya tabloyu uygulamaya kopyalamayın.
4. **Veri lisansını kayıt bazında inceleyin.** “Açık”, “ücretsiz”, “API var” ve “atıf yaptık” ifadelerini yeniden dağıtım/ticari izin yerine koymayın.
5. **Ticari uyumluluğu baştan kontrol edin.** Özellikle NC lisanslı veri ve share-alike koşullu veri için veri modeline bağlamadan önce izin/uyumluluk kararı alın. İzin alınamıyorsa ticari kullanıma uygun kaynak seçin veya bağımsız, izinli veri oluşturun.
6. **Kod ile veri lisanslarını ayırın.** Uygulama kodunun açık kaynak lisansı, üçüncü taraf veri kayıtlarının lisans koşullarını otomatik olarak değiştirmez.
7. **Yayın/ürünleşme öncesi gözden geçirin.** Üniversitenin teknoloji transfer/ofis veya hukuk birimi ya da fikri mülkiyet alanında çalışan bir hukukçuya, kaynak envanteri ile gerçek dağıtım akışını birlikte gösterin. Özellikle ODbL türev/collection ayrımı ve FooDB'nin olası ürünleşmede kullanımı netleştirilmelidir.

## 5. Kısa karar

- Kaynakları okuyup **doğru atıfla kendi kural modelinizi yazmanız** makul başlangıç yaklaşımıdır; kaynak metinlerini ve tablolarını aynen taşımayın.
- **Atıf, lisans izninin yerine geçmez.** Açık erişim de otomatik olarak ticari yeniden kullanım hakkı vermez.
- FooDB'nin mevcut lisans açıklaması ticari kullanım açısından engel/izin gereksinimi oluşturuyor. OFF'un veritabanı, içerik ve görsel katmanlarını ayrı değerlendirin.
- Her kaynağın sürümü ile lisans şartı dosyada kayıtlı değilse o veriyi uygulama deposuna veya ürün veri tabanına eklemeyin.
- Bu belge ön taramadır; dağıtım ve ürünleşme kararları için kesin hukuki görüş yerine geçmez.

## Kaynaklar

- [T.C. Kültür ve Turizm Bakanlığı — Telif Hakkı Nasıl Korunur?](https://telifhaklari.ktb.gov.tr/TR-332374/telif-hakki-nasil-korunur.html)
- [T.C. Kültür ve Turizm Bakanlığı — Genel Sorular (FSEK 35 alıntı açıklaması)](https://telifhaklari.ktb.gov.tr/TR-332449/genel-sorular.html)
- [FooDB — Compliance](https://foodb.ca/compliance)
- [FooDB — About](https://foodb.ca/about)
- [Creative Commons — CC BY-NC 4.0 Deed](https://creativecommons.org/licenses/by-nc/4.0/deed.en)
- [Open Food Facts — License and reuse documentation](https://openfoodfacts.github.io/openfoodfacts-server/api/tutorials/license-be-on-the-legal-side/)
- [Open Data Commons — ODbL 1.0 legal text](https://opendatacommons.org/licenses/odbl/1-0/)
