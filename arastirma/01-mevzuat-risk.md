> **Ham araştırma — hukuki tavsiye değildir, Levent'le netleştirilmedi, 2026-09-24**
> Web araştırmasıyla derlendi. "(yorum)" etiketli yerler hukukçu görüşü değil, araştırmacının çıkarımıdır. "Belirsiz" denilen yerler bir avukat / KVKK uzmanı / danışmanla doğrulanmalı. Kaynak linkleri her iddianın yanında.

# NutriScan — Mevzuat ve Risk Araştırması

## 0. Tek paragraf özet

NutriScan'in topladığı veri (alerji, diyabet, çölyak, hipertansiyon, böbrek hastalığı, hamilelik) KVKK'da **özel nitelikli kişisel veri (sağlık verisi)**. En ağır rejime giriyor. Öğrenci projesi olmak bir istisna sağlamıyor. En tehlikeli üç mimari karar şunlar: (1) sağlık profilini **yurt dışındaki bir LLM'e veya buluta** göndermek, (2) uygulamayı **"alerjik reaksiyonu önler / hastalığı yönetir"** diye konumlandırıp tıbbi cihaz sınırına girmek, (3) **"güvenli" etiketini** doğrulanmamış veriyle vermek. Üçü de tasarımda çözülebilir: sağlık profili Türkiye'de kalır, LLM'e gönderilmez; kural motoru deterministik olur; dil "bilgilendirme" düzeyinde tutulur; "güvenli" yerine "listelenen içerikte alerjen bulunamadı + etiketi kontrol et" denir.

---

## 1. KVKK (6698 sayılı Kanun)

### 1.1 Veri sınıfı
- Sağlık verisi, KVKK m.6 kapsamında özel nitelikli kişisel veri. [KVKK — Özel Nitelikli Kişisel Veriler](https://www.kvkk.gov.tr/Icerik/2051/Ozel-Nitelikli-Kisisel-Veriler)
- **Alışveriş geçmişi de dolaylı sağlık verisine dönüşebilir.** Örnek: glütensiz ürünler düzenli alınıyorsa bu çölyak olduğunu ele verir. (yorum) Bu yüzden alışveriş geçmişi de sağlık verisi gibi korunmalı.

### 1.2 Hukuki sebep: 7499 sayılı Kanun sonrası (01.06.2024'ten beri)
- 7499 sayılı Kanun 12.03.2024'te Resmî Gazete'de yayımlandı. KVKK değişiklikleri 01.06.2024'te yürürlüğe girdi. Sağlık verisi ile diğer özel nitelikli veriler arasındaki ayrım kalktı ve işleme şartları genişledi. [Erdem & Erdem](https://www.erdem-erdem.av.tr/bilgi-bankasi/kisisel-verilerin-korunmasi-kanununda-neler-degisti) · [KVKK madde gerekçeli metin (PDF)](https://www.kvkk.gov.tr/SharedFolderServer/CMSFiles/062384e3-d18c-4c38-b108-3a7a2a28e849.pdf)
- Yeni m.6/3'teki şartlar: açık rıza · kanunda açıkça öngörülme · fiili imkânsızlıkta hayat/beden bütünlüğü · alenileştirme · hak tesisi · sır saklama yükümlüsü kişilerce sağlık hizmetleri · istihdam/sosyal güvenlik · belirli kâr amacı gütmeyen vakıf/dernekler. [Erdem & Erdem](https://www.erdem-erdem.av.tr/bilgi-bankasi/kisisel-verilerin-korunmasi-kanununda-neler-degisti)
- **(yorum)** NutriScan için pratikte tek uygun şart **açık rıza**. "Sır saklama yükümlülüğü altındaki kişiler" şartı hekim ve sağlık kuruluşları için yazılmış. Özel bir tüketici uygulamasına uyduğunu gösteren bir kaynak bulamadım.
- Özel nitelikli veri için Kurul'un **"yeterli önlemler"** kararı bağlayıcı. Bu karar ayrı politika, eğitim, gizlilik sözleşmesi, erişim yetkisi ve süre kontrolü, şifreli aktarım gibi önlemler istiyor. [Kurul Kararı 2018/10](https://www.kvkk.gov.tr/Icerik/4110/2018-10)

### 1.3 Aydınlatma metni ve açık rıza metni
- Aydınlatma ile açık rıza **ayrı ayrı** yapılmalı. [Aydınlatma Tebliği m.5/1-f](https://kvkk.gov.tr/Icerik/5443/AYDINLATMA-YUKUMLULUGUNUN-YERINE-GETIRILMESINDE-UYULACAK-USUL-VE-ESASLAR-HAKKINDA-TEBLIG) · [Kurul Kararı 2018/90](https://www.kvkk.gov.tr/Icerik/5420/2018-90)
- **Yeni: 18.02.2026 tarihli ve 2026/347 sayılı İlke Kararı.** İki metin farklı başlıklar altında ayrı ayrı sunulmalı. Aynı sayfadaysalar alt alta, iki ayrı bölüm olmalı. Kararın yasakladıkları: metinleri iç içe koymak, aydınlatma için "onay" istemek, başka şirketin metnini kopyalamak, muğlak veya aşırı uzun metin yazmak. Uymamanın yaptırımı m.18. [KVKK duyurusu](https://www.kvkk.gov.tr/Icerik/8710/veri-sorumlulari-tarafindan-acik-riza-ve-aydinlatma-metinlerinin-ayri-ayri-duzenlenmesi-gerektigi-hakkinda-kisisel-verileri-koruma-kurulunun-18-02-2026-tarihli-ve-2026-347-sayili-ilke-kararina-iliskin-kamuoyu-duyurusu)
- **(yorum)** Uygulama içi tasarım: onboarding'de önce aydınlatma metni gösterilir ("okudum" demek yeterli, onay değil). Ardından **her amaç için ayrı, önceden işaretlenmemiş** rıza kutuları gelir: (a) sağlık profilini işleme, (b) yurt dışına aktarım (varsa), (c) LLM ile işleme (varsa), (d) analitik/pazarlama. Çekirdek işlev (a) olmadan çalışmaz; öteki rızalar hizmet şartına bağlanmamalı. Rızanın geri alınabilmesi ve hesap silme uygulama içinde olmalı.

### 1.4 Yurt dışına aktarım: LLM API ve yurt dışı bulut
- Yeni m.9 sırası: önce **yeterlilik kararı**. Yoksa **uygun güvenceler**: standart sözleşme, BCR veya taahhütname. Bunlar da yoksa yalnızca **arızi** aktarım (açık rıza bunlardan biri). [Erdem & Erdem](https://www.erdem-erdem.av.tr/bilgi-bankasi/kisisel-verilerin-korunmasi-kanununda-neler-degisti) · [KVKK Yurt Dışına Aktarım Rehberi](https://www.kvkk.gov.tr/Icerik/8142/Kisisel-Verilerin-Yurt-Disina-Aktarilmasi-Rehberi)
- **Kurul henüz hiçbir ülke için yeterlilik kararı vermedi.** Sayfadaki ifade: "henüz bir belirleme yapılmamıştır". [KVKK — Yurt Dışına Aktarım](https://www.kvkk.gov.tr/Icerik/2053/Yurtdisina-Aktarim)
- Standart sözleşme **değiştirilmeden** kullanılır. İmzadan itibaren **5 iş günü içinde** Kurum'a bildirilir. Usul ve Esaslar Yönetmeliği 10.07.2024'te yürürlüğe girdi. [Paksoy](https://paksoy.av.tr/2024/07/kisisel-verileri-koruma-kurumu-yurt-disina-veri-aktarimlarina-iliskin-yeni-bir-yonetmelik-yayimladi/) · [Ozay Law](https://ozay.av.tr/publication/kisisel-verilerin-yurt-disina-aktarilmasina-iliskin-usul-ve-esaslar-hakkinda-yonetmelik) · [KVKK standart sözleşme duyurusu](https://www.kvkk.gov.tr/Icerik/8170/Yurt-Disina-Kisisel-Veri-Aktariminda-Kullanilacak-Standart-Sozlesmelerde-Dikkat-Edilmesi-Gereken-Hususlara-Iliskin-Kamuoyu-Duyurusu)
- **Arızi aktarımın tanımı:** düzenli olmayan, bir veya birkaç kez gerçekleşen, süreklilik göstermeyen ve olağan faaliyet akışının parçası olmayan aktarım. **Açık rıza artık sistematik aktarımın dayanağı olamaz.** [KVKK Danışman özeti](https://www.kvkkdanisman.com/blog/yurt-disi-veri-aktarimi-yontemleri) · [Yönetmelik PDF](https://kvkk.gov.tr/SharedFolderServer/CMSFiles/aaf0eeec-9599-4c68-8b7a-33039059ca41.pdf)
- **(yorum, kritik)** Her taramada kullanıcının sağlık profilini OpenAI, Anthropic veya Google API'sine göndermek **düzenli ve süreklidir**, yani arızi sayılmaz. Bu durumda sağlayıcıyla **KVKK standart sözleşmesi imzalanıp 5 iş günü içinde bildirilmesi** gerekir. Büyük LLM sağlayıcılarının Türk standart sözleşmesini değiştirilmeden imzalayıp imzalamadığını **doğrulayamadım.** Microsoft'un Azure Türkiye için bunu sağlayıp sağlamadığı forumlarda bile soru olarak duruyor. [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5615914/standard-contract-with-microsoft-azure-turkey-with) Aynı durum Vercel, Supabase, Firebase gibi yurt dışı PaaS'lar için de geçerli.
- **Pratik çıkış yolu (yorum):**
  1. Sağlık profili ve alışveriş geçmişi **Türkiye'de barındırılan** sunucuda/veritabanında tutulur.
  2. Risk kararını **deterministik kural motoru** verir: içindekiler + alerjen taksonomisi + profil.
  3. LLM kullanılacaksa ona yalnızca **ürün verisi** gider (içindekiler metni, etiket OCR'ı). Kimlik veya profil gitmez. Bu durumda bile istek metadatası (IP, cihaz) kişisel veri sayılabilir; sunucu üzerinden proxy'lenmeli.
  4. Anonimleştirilmiş veri KVKK dışındadır, ancak "sağlık profili + ürün" birleşimi genelde anonim değil, en fazla takma adlıdır.

### 1.5 VERBİS kaydı
- Genel istisna: yıllık çalışan sayısı 50'den az **ve** yıllık mali bilanço 100 milyon TL'den az olup **ana faaliyeti özel nitelikli veri işlemek olmayanlar**. [Kurul Kararı 2018/87](https://www.kvkk.gov.tr/Icerik/5271/2018-87) · [2023/1154 değişikliği duyurusu](https://www.kvkk.gov.tr/Icerik/7646/Kamuoyu-Duyurusu-Veri-Sorumlulari-Siciline-Kayit-Yukumlulugune-Iliskin-Istisna-Kriterinde-Degisiklik-Yapilmasi-Hakkinda-)
- NutriScan'in ana faaliyeti sağlık verisi işlemek, dolayısıyla genel istisnaya girmez. **Ancak 04.09.2025 tarihli ve 2025/1572 sayılı Kurul Kararı** ile ana faaliyeti özel nitelikli veri işlemek olup **yıllık çalışan sayısı 10'dan az ve yıllık mali bilançosu 10 milyon TL'den az** olan veri sorumluları da VERBİS'ten muaf tutuldu. [KVKK duyurusu](https://www.kvkk.gov.tr/Icerik/8388/KAMUOYU-DUYURUSU)
- **(yorum)** 3 kişilik öğrenci ekibi bu eşiklerin altında kalır, yani VERBİS kaydı muhtemelen gerekmez. **VERBİS muafiyeti diğer yükümlülüklerden muafiyet değildir**: aydınlatma, rıza, güvenlik ve ihlal bildirimi aynen geçerli.
- **"Öğrenci projesi / kâr amacı yok" istisnası bulamadım.** KVKK m.28'deki istisnalar (ev içi faaliyet, resmi istatistik vb.) kamuya açık bir uygulamaya uymuyor. (yorum)

### 1.6 Çocuk verisi ve hane profilleri
- KVKK'da ve Kurul düzenlemelerinde çocuk rızası için **açık bir yaş sınırı yok.** Uygulamada Medeni Kanun'daki ayırt etme gücü ve kanuni temsilci rızası esas alınıyor. [Eralp Avukatlık](https://www.eralp.av.tr/kvkk-ve-gdpra-gore-cocuk-verilerinin-islenmesi/) · [KVKK — Çocukların Kişisel Verileri](https://www.kvkk.gov.tr/Icerik/6737/Cocuklarin-Kisisel-Verilerinin-Korunmasi-Bakimindan-Dikkat-Edilmesi-Gerekenler) · [Kurul Kararı 2020/255](https://www.kvkk.gov.tr/Icerik/6894/2020-255)
- **(yorum, belirsiz)** Hane profillerinde iki ayrı durum var:
  - **Çocuk:** veli kendi hesabından rıza verir. Metin çocuğun anlayacağı dilde de hazırlanmalı.
  - **Başka bir yetişkin** (eş, anne-baba): rızayı hesabı açan kişi değil, **verinin sahibi** vermeli. Önerilen tasarım, hanedeki yetişkini davetle bağlamak. Rıza sahibi kendi onayını verir. "Başkası adına sağlık verisi girme" akışı olmamalı.

### 1.7 Güvenlik ve ihlal
- İhlal fark edildikten sonra Kurul'a **en geç 72 saat** içinde bildirim yapılır; ilgili kişilere de makul en kısa sürede. [Kurul Kararı 2019/10](https://www.kvkk.gov.tr/Icerik/5362/Veri-Ihlali-Bildirimi) · [2019/271 — ilgili kişiye bildirimin asgari içeriği](https://www.kvkk.gov.tr/Icerik/5547/2019-271)

### 1.8 Cezalar (2026, yeniden değerlemeli)
- Aydınlatma: 85.437 – 1.709.200 TL
- Veri güvenliği: 256.357 – 17.092.242 TL
- VERBİS: 341.809 – 17.092.242 TL
- Standart sözleşmeyi bildirmeme: 90.308 – 1.806.177 TL
- Kaynak: [Köksal Partners](https://www.koksalpartners.com/tr/kvkk-cezalari) · [Mondaq](https://www.mondaq.com/turkey/data-protection/1729106/2026-y%C4%B1l%C4%B1nda-kvkk-kapsam%C4%B1ndaki-%C4%B0dari-para-cezas%C4%B1-tutarlar%C4%B1-g%C3%BCncellendi). Tutarlar ikincil kaynaktan alındı; resmi Kurum duyurusuyla teyit edilmeli.
- **(yorum)** Kimin veri sorumlusu olduğu belirsizse (öğrenci mi, şirket mi, üniversite mi) ceza muhatabı da belirsiz kalır. Bu **en önce netleşmesi gereken soru**.

### 1.9 İlgili olabilecek diğer düzenlemeler
- **Kişisel Sağlık Verileri Hakkında Yönetmelik (2019):** kapsamı Sağlık Bakanlığı süreçlerine bağlı faaliyetlerle sınırlı görünüyor. (yorum) NutriScan'e muhtemelen uygulanmaz; doğrulanmalı. [Resmî Gazete](https://www.resmigazete.gov.tr/eskiler/2019/06/20190621-3.htm)
- **KVKK "Üretken Yapay Zekâ ve Kişisel Verilerin Korunması Rehberi" (24.11.2025):** LLM kullanan veri sorumluları için Kurum'un beklentilerini içeriyor. [KVKK](https://www.kvkk.gov.tr/Icerik/8547/uretken-yapay-zeka-ve-kisisel-verilerin-korunmasi-rehberi-15-soruda) · [Yapay zekâ tavsiyeleri (PDF)](https://www.kvkk.gov.tr/SharedFolderServer/CMSFiles/25a1162f-0e61-4a43-98d0-3e7d057ac31a.pdf)

### 1.10 Minimum KVKK uyum checklist'i
1. **Veri sorumlusunu belirle:** gerçek kişi mi, şirket mi? Aydınlatma metninde unvan ve iletişim bilgisi yer almalı.
2. **Veri envanteri:** hangi alan, hangi amaç, hangi hukuki sebep, saklama süresi. Alışveriş geçmişini de sağlık verisi say.
3. **Aydınlatma metni:** 2026/347'ye uygun, ayrı, kısa, kopya olmayan metin.
4. **Açık rıza metni:** ayrı ekran, amaç başına ayrı ve önceden işaretlenmemiş kutu, kayıt altına alınan zaman damgası, geri alınabilir.
5. **Veri minimizasyonu:** tam teşhis yerine yalnızca gereken bayraklar (ör. "çölyak: evet"). İlaç, doz, tahlil gibi veriler toplanmamalı.
6. **Barındırma yeri:** sağlık verisi Türkiye'de kalsın. Yurt dışı gerekiyorsa standart sözleşme + 5 iş günü içinde bildirim.
7. **LLM'e profil verisi gönderme.**
8. **2018/10 önlemleri:** at-rest ve in-transit şifreleme, rol bazlı erişim, erişim logları, ekip içi gizlilik taahhüdü, yazılı politika.
9. **Silme:** uygulama içi hesap ve veri silme (Apple ve Google bunu zaten şart koşuyor), saklama süresi dolunca otomatik imha.
10. **İlgili kişi başvuru kanalı:** m.11 hakları için e-posta veya form, 30 gün içinde yanıt.
11. **İhlal müdahale planı:** 72 saat içinde bildirim için kim ne yapacak.
12. **Çocuk ve hane:** veli akışı, yetişkinler için davet ile kendi rızası.
13. **VERBİS:** 2025/1572 eşiklerini yıllık kontrol et.

---

## 2. GDPR: AB kullanıcısı gelirse ne değişir (kısa)
- **Kapsam:** AB'deki kişilere mal veya hizmet sunmak (hedefleme) GDPR'ı uygulanabilir kılar (m.3/2). [GDPR — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **Sağlık verisi (m.9/2-a):** açık rıza (explicit consent). KVKK ile büyük ölçüde örtüşür.
- **Çocuk (m.8):** bilgi toplumu hizmetlerinde varsayılan yaş 16. Üye devletler bunu 13'e kadar indirebilir. Bu, KVKK'dan daha net bir kural.
- **AB temsilcisi (m.27):** AB dışındaki bir veri sorumlusu, **büyük ölçekte özel nitelikli veri işliyorsa** AB'de temsilci atamak zorunda. İstisna yalnızca arızi ve küçük ölçekli işlemler için var.
- **DPIA (m.35)** ve olası **DPO (m.37):** büyük ölçekte sağlık verisi işlemek iki yükümlülüğü de tetikleyebilir.
- **Ürün sorumluluğu:** Yeni AB Ürün Sorumluluğu Direktifi 2024/2853 yazılımı açıkça "ürün" sayıyor ve **9 Aralık 2026'dan sonra** piyasaya sürülen ürünlere uygulanıyor. [EUR-Lex 2024/2853](https://eur-lex.europa.eu/eli/dir/2024/2853/oj/eng) · [Reed Smith](https://www.reedsmith.com/articles/eu-product-liability-directive-software-digital-products-cybersecurity/)
- **(yorum)** İlk sürümü **yalnızca Türkiye mağazasında** yayınlamak GDPR, MDR ve AI Act yükünü ilk etapta dışarıda tutar.

---

## 3. Tıbbi cihaz sınırı (MDR 2017/745 ve TİTCK Tıbbi Cihaz Yönetmeliği)
- Türkiye'deki Tıbbi Cihaz Yönetmeliği MDR ile tam uyumlu ve **02.06.2021 tarihli, 31499 (mükerrer) sayılı** Resmî Gazete'de yayımlandı. Yani AB'deki yorum Türkiye'ye de büyük ölçüde taşınır. [TİTCK mevzuat](https://www.titck.gov.tr/faaliyetalanlari/tibbicihaz/tibbi-cihaz-mevzuati) · [TİTCK — MDR Türkçe (PDF)](https://www.titck.gov.tr/Dosyalar/TibbiCihaz/CihazHakkinda/MDR%202018.pdf)
- **Belirleyici olan üreticinin beyan ettiği amaç.** Bu amaç etiket, kullanım talimatı, **tanıtım ve satış materyalleri** ile beyanlardan okunur. Yani App Store açıklaması, web sitesi ve sunum dili de "amaç beyanı" sayılır. [MDCG 2019-11 rev.1 (Haziran 2025)](https://health.ec.europa.eu/document/download/b45335c5-1679-4c71-a91c-fc7a4d37f12b_en?filename=md_mdcg_2019_11_guidance_qualification_classification_software_en.pdf)
- MDR resital 19: yaşam tarzı ve iyi olma (well-being) amaçlı yazılım tıbbi cihaz değildir. MDCG 2019-11 de "wellness or fitness apps" için tıbbi cihaz yazılımı (MDSW) sayılmaz diyor. [MDCG 2019-11 rev.1](https://health.ec.europa.eu/document/download/b45335c5-1679-4c71-a91c-fc7a4d37f12b_en?filename=md_mdcg_2019_11_guidance_qualification_classification_software_en.pdf) · [OpenRegulatory](https://openregulatory.com/mdcg/mdcg-2019-11)
- MDCG karar adımları şöyle: yazılım veri üzerinde saklama, iletme ve "basit arama"nın ötesinde bir işlem yapıyor mu? Bu işlem **tek tek hastaların yararına** mı? Bir de dikkat: **zarar riski, niteleme kriteri değildir.** [MDCG 2019-11 rev.1, s.8–13](https://health.ec.europa.eu/document/download/b45335c5-1679-4c71-a91c-fc7a4d37f12b_en?filename=md_mdcg_2019_11_guidance_qualification_classification_software_en.pdf)
- MDR m.2(1)'deki tıbbi amaçlar: teşhis, **önleme**, izleme, tahmin, prognoz, tedavi veya **hafifletme**. [MDR — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2017/745/oj)
- **(yorum, belirsiz — NutriScan'in asıl gri alanı):**
  - NutriScan veri üzerinde işlem yapıyor (profil × içindekiler eşleştirmesi) ve bunu **tek bir kişi için** yapıyor. Bu iki adımda MDSW'ye yaklaşıyor.
  - "Diyabet/böbrek hastası için bu ürün **risklidir**" veya "alerjik reaksiyonu **önler**" dili hastalığın önlenmesi veya hafifletilmesi amacı olarak okunabilir. Bu durumda Kural 11 uyarınca en az Sınıf IIa olur; onaylanmış kuruluş gerekir ve öğrenci ekibi için pratikte proje biter.
  - "Etikette beyan edilen içerikleri tercihlerinle karşılaştırır, bilgilendirme amaçlıdır" dili ise **yaşam tarzı / bilgi aracı** tarafında kalır.
  - Bu sınırı kesin çizen bir resmi kılavuz örneği (gıda alerjeni tarayıcı) **bulamadım.** Kesin görüş için TİTCK'ya ön danışma veya bir düzenleyici danışman gerekir.
- **Rakiplerin konumlanması:**
  - **Yuka (AB şartları):** Uygulamanın tıbbi tavsiye vermediğini ve analizin doğruluğunu garanti etmediğini söylüyor. Diyet tercihleri özelliğinin **ciddi alerjisi olanlar tarafından kullanılmaması** gerektiğini ve ambalajın kontrol edilmesini yazıyor (m.3.3, 6.3.1, 6.3.4). [Yuka CGU Europe](https://help.yuka.io/l/fr/article/pyaesjv84d-conditions-g-n-rales-d-utilisation-et-de-vente-de-yuka-europe) · [Yuka limitations](https://help.yuka.io/l/en/article/wz3cbbztf3-what-are-yuka-s-limitations)
  - **Fig:** Hizmetin "general wellness" ve bilgilendirme amaçlı olduğunu, tıbbi tavsiye olmadığını söylüyor. Sorumluluğu son 12 aylık ödeme veya 100 USD ile sınırlıyor. [Fig ToS](https://foodisgood.com/terms-of-service)
- **Doğru dil (yorum):** "içerik bilgisi", "tercihlerine göre işaretleme", "etikette beyan edilen", "bilgilendirme amaçlıdır", "etiketi ve doktorunu esas al".
- **Yapılmaması gereken iddialar:** "güvenli", "alerjiden korur / önler", "diyabetini yönet", "doktor onaylı", "tıbbi", "teşhis", "kişiye özel beslenme tedavisi", "%100 doğru", "hamilelikte güvenle tüketilebilir".

---

## 4. Sorumluluk: yanlış "güvenli" dönütü
- **Gerçek bir örnek var:** SnackSafely, Fig'in üç üründe paylaşımlı üretim hattı bilgisini yanlış verdiğini raporladı. Bir örnekte Fig hiçbir alerjen endişesi göstermemiş, üretici ise aynı hatta buğday ve soya işlendiğini doğrulamış. Rapor, gönüllü "içerebilir" beyanına dayanan uygulamaların yapısal olarak kör olduğunu gösteriyor. [SnackSafely](https://snacksafely.com/2023/09/advisory-dont-use-the-fig-scanner-app-if-the-potential-for-allergen-cross-contact-concerns-you/)
- **Feragat metinlerinin sınırı (Türk hukuku):**
  - TBK m.115: ağır kusurdan sorumsuzluk anlaşması **kesin hükümsüz**. Uzmanlık gerektiren ve izne bağlı hizmetlerde hafif kusur için sorumsuzluk anlaşması da hükümsüz. [TBK m.115 — Kanun Yolu](https://kanunyolu.com.tr/kanun-madde/6098/115) · [Erdem & Erdem](https://www.erdem-erdem.av.tr/bilgi-bankasi/borclar-kanunu-hukumleri-uyarinca-sorumsuzluk-anlasmalari)
  - Tüketici sözleşmelerinde müzakere edilmemiş ve dengesizlik yaratan şartlar (haksız şart) **kesin hükümsüz**. [6502 s. TKHK m.5](https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6502&MevzuatTur=1&MevzuatTertip=5)
  - 7223 s. Kanun m.6 güvensiz üründen doğan zarar için imalatçıya sorumluluk yüklüyor. Yazılımın bu kanundaki "ürün" tanımına girip girmediği **belirsiz**. [7223 s. Kanun](https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=7223&MevzuatTur=1&MevzuatTertip=5)
- **(yorum)** Feragat metni tek başına kalkan değildir. Sorumluluk tartışmasında asıl belirleyici, özenin **tasarımda** gösterilip gösterilmediği olur. Ayrıca sözleşme tarafı olmayan kişiler (hane profilindeki çocuk gibi) için haksız fiil hükümleri (TBK m.49 vd.) devreye girer ve kullanıcı sözleşmesi onları bağlamaz.
- **UX önlemleri (sektörde yaygın olanlardan derlendi, yorum):**
  1. **Üç durumlu sonuç, asla ikili değil:**
     - "Profilinle çakışan içerik bulundu" (kırmızı)
     - "Listelenen içerikte çakışma bulunamadı" (nötr; **"güvenli" kelimesi yok**)
     - "**Doğrulanamadı**": veri eksik, eski, OCR güveni düşük veya içindekiler boş (gri)
  2. **"Etiketi kontrol et" uyarısı** her sonuç ekranında olmalı; alerji profili olanlarda daha belirgin.
  3. **Kaynak ve tarih:** "Open Food Facts, son güncelleme …" veya "Etiket fotoğrafından okundu".
  4. **"Eser miktarda içerebilir" ayrı gösterilmeli.** Bu beyanın **yokluğu** kanıt sayılmamalı (bkz. §5).
  5. **Ciddi alerji / anafilaksi uyarısı:** onboarding'de "şiddetli alerjin varsa bu uygulamaya güvenme" (Yuka modeli).
  6. **LLM çıktısı "güvenli" kararı vermemeli.** Karar kural motorunda kalmalı; LLM en fazla açıklama metni üretmeli.
  7. **Yanlış bildir** butonu ve düzeltme süreci.
  8. **Sürüm/tarif değişikliği:** barkod aynı kalıp içerik değişebilir. Eski veriye "eski olabilir" etiketi koy.

---

## 5. Gıda etiketleme (Türk Gıda Kodeksi)
- Yönetmelik **26.01.2017 tarihli ve 29960 (mükerrer) sayılı** Resmî Gazete'de yayımlandı. [Mevzuat](https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=23282&MevzuatTur=7&MevzuatTertip=5) · [Resmî Gazete](https://www.resmigazete.gov.tr/eskiler/2017/01/20170126M1-6.htm)
- **Ek-1'deki 14 zorunlu alerjen:**
  1. Gluten içeren tahıllar (buğday, çavdar, arpa, yulaf, melezleri)
  2. Kabuklular
  3. Yumurta
  4. Balık
  5. Yerfıstığı
  6. Soya
  7. Süt (laktoz dahil)
  8. Sert kabuklu meyveler (badem, fındık, ceviz, kaju, pikan, Brezilya fındığı, antep fıstığı, makadamya)
  9. Kereviz
  10. Hardal
  11. Susam
  12. Kükürt dioksit/sülfitler (≥10 mg/kg veya ≥10 mg/L)
  13. Acı bakla (lupin)
  14. Yumuşakçalar
  - Her birinin kendi istisnaları var (ör. tam rafine soya yağı, glüten içeren tahıllardan elde edilen glikoz şurupları). [Ekler — gumruk.com.tr](https://www.gumruk.com.tr/files/turk_gida_kodeksi_gida_etiketleme_ve_tuketicileri_bilgilendirme_yonetmeligi_ekler.htm)
- Alerjenler içindekiler listesinde **vurgulanarak** (kalın, büyük harf veya renkli) yazılır. Hazır ambalajlı olmayan gıdalarda ve toplu tüketim yerlerinde de bildirim zorunludur. [Tarım ve Orman — Kılavuz](https://www.tarimorman.gov.tr/Konu/2088/TGK_Etiketleme_Tuketici_Bilgilendirme_Yonetmelik_Kilavuz) · [Güvenilir Gıda](https://guvenilirgida.tarimorman.gov.tr/Haber/Detay/17279)
- **"Eser miktarda içerebilir" beyanı:** **zorunlu değil, gönüllü.** Kılavuza göre (m.21, isteğe bağlı alerjen bildirimi) yalnızca kapsamlı bir risk değerlendirmesi sonucunda bulaşma kaçınılmazsa kullanılabilir. [Kılavuz — Lexpera](https://www.lexpera.com.tr/resmi-gazete/metin/turk-gida-kodeksi-gida-etiketleme-ve-tuketicileri-bilgilendirme-yonetmeligi-kilavuzu) · [Besin Alerjisi Derneği](https://besinalerjisi.org.tr/alerjen-etiketleme-kurallari/)
- **(yorum) Uygulamaya etkisi:**
  - 14'lü liste alerjen taksonomisinin **zorunlu çekirdeği** olmalı. Çölyak için gluten ayrı bayrak olmalı (yulaf ve eser gluten nüansı nedeniyle).
  - "İçerebilir" beyanının olmaması, çapraz bulaşma olmadığı anlamına gelmez. Uygulama bunu "çakışma yok" diye okumamalı.
  - Diyabet, hipertansiyon ve böbrek hastalığı için alerjen listesi değil **besin öğesi eşikleri** (şeker, tuz/sodyum, potasyum, fosfor) gerekir. Bu eşiklerin kaynağı (ör. WHO veya bir klinik kılavuz) kararlar dosyasına yazılmalı. Bu uyarılar tıbbi cihaz sınırına en yakın özellik (bkz. §3).

---

## 6. Veri lisansları
### 6.1 Open Food Facts (ODbL)
- Veritabanı ODbL, tekil içerikler Database Contents License, görseller CC BY-SA lisanslı. **Ticari kullanıma izin var.** Atıf zorunlu: "Contains data from Open Food Facts…" gibi, linkle. OFF doğruluğu **garanti etmiyor.** [OFF Terms](https://world.openfoodfacts.org/terms-of-use) · [OFF Data](https://world.openfoodfacts.org/data)
- **ODbL'de share-alike yalnızca veritabanına bulaşır, uygulama koduna bulaşmaz:**
  - **Produced Work** (ekranda gösterilen sonuç): yalnızca atıf/uyarı gerekir (m.4.3).
  - **Derivative Database** (OFF'u kendi düzeltmelerinle veya eklemelerinle birleştirdiğin veritabanı): bunu **Publicly Use** edersen o veritabanını ODbL ile sunman ve makine okunur tam kopyasını ya da **değişiklik dosyasını** vermen gerekir (m.4.4, 4.6).
  - **Collective Database** (OFF değiştirilmeden, kendi bağımsız veritabanlarının yanında): share-alike uygulanmaz (m.4.5).
  - Kaynak: [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)
- OFF'un kendi özeti: uyarlanmış veritabanını kamuya açık kullanırsan onu ODbL ile sunmalı ve değişikliklerini geri paylaşmalısın. **Her API çağrısı gerçek bir kullanıcı taramasına karşılık gelmeli; API ile kazıma (scraping) engellenir.** [OFF Data](https://world.openfoodfacts.org/data)
- **(yorum) Mimari öneri:**
  - OFF verisi **ayrı bir tabloda/katmanda, değiştirilmeden** tutulur.
  - Ekibin eklediği Türk ürünleri ve düzeltmeler OFF'a API ile **geri gönderilir.** Bu hem lisans riskini sıfırlar hem de "katkı" hikâyesi olur.
  - Kapalı kaynak kod sorun değil. Sorun, OFF ile birleştirilmiş ve paylaşılmayan bir **veritabanı** olur.
  - Ürün görsellerinde marka ve tasarım hakları ayrıca var; bunları doğrulamak kullanıcının sorumluluğu. [OFF Terms](https://world.openfoodfacts.org/terms-of-use)

### 6.2 marketfiyati.org.tr ve market siteleri
- marketfiyati.org.tr TÜBİTAK BİLGEM tarafından geliştirildi; zincir marketlerin fiyatlarını gösteriyor. [TÜBİTAK](https://tubitak.gov.tr/tr/haber/zincir-market-fiyatlarina-aninda-erisimin-onu-acildi) · [Bigpara](https://bigpara.hurriyet.com.tr/haberler/ekonomi-haberleri/market-fiyatlari-tek-sitede_ID1607491/)
- Sitenin **kullanım koşullarını ve API iznini doğrulayamadım.** Site tek sayfalık bir uygulama; koşullar metni araç tarafından okunamadı. **Levent tarayıcıda "Kullanım Koşulları" sayfasına bakmalı.**
- Türk hukukunda scraping'i doğrudan düzenleyen bir hüküm yok. Riskler şunlar:
  - **FSEK Ek m.8:** veritabanı yapımcısının sui generis hakkı. Önemli bir kısmın çoğaltılması ve yayılması izne bağlı. [Lexology](https://www.lexology.com/library/detail.aspx?g=cf0ded85-1ada-4062-9a5d-06e57c171818) · [Güleryüz](https://www.guleryuz.av.tr/tr/news-publications/detail/https-wwwguleryuzavtr-tr-news-publications-detail-web-kazima-web-scraping-ve-internet-sitelerine-yonelik-koruma)
  - **TTK m.55/1-c:** başkasının iş ürününden izinsiz yararlanma (haksız rekabet). [Göksu Safi Işık](https://www.goksusafiisik.av.tr/tr/publications/2025-summer-issue/web-scraping-eyleminin-haksiz-rekabet-acisindan-degerlendirilmesi?id=510)
  - Kullanım koşulları ve robots.txt ihlali.
  - **(yorum)** Teknik engelleri aşmak ceza hukuku riski de doğurabilir (TCK m.243–244). Bu konuda kaynaklı bir değerlendirme bulamadım; avukata sorulmalı.
- **(yorum) Öneri:** Fiyat özelliği MVP'nin çekirdeği değilse **ilk sürümde hiç olmasın.** Olacaksa TÜBİTAK BİLGEM'den veya marketlerden **yazılı izin ya da resmi API** istenmeli. İzin yoksa scraping yapılmamalı.

---

## 7. Yapay zekâ ve mağaza politikaları
### 7.1 AB AI Act
- **Risk sınıfı (yorum):**
  - NutriScan Ek III'teki yüksek riskli alanlardan birine girmiyor.
  - **Tıbbi cihaz sayılırsa ve onaylanmış kuruluş gerektirirse** (Sınıf IIa ve üstü) m.6(1) üzerinden **yüksek riskli** olur. Bu da ayrıca MDR ve AI Act birlikte uyum demek. [Legalithm — Ek I](https://www.legalithm.com/en/ai-act-guide/annex-i) · [MDCG 2025-6 / AIB 2025-1](https://health.ec.europa.eu/document/download/b78a17d7-e3cd-4943-851d-e02a2f22bbb4_en)
  - Wellness konumlandırmasında kalırsa: sohbet (chatbot) özelliği varsa **m.50 şeffaflık** yükümlülüğü (kullanıcıya bir yapay zekâyla konuştuğunu söyleme) 2 Ağustos 2026'dan beri uygulanıyor. [AB Komisyonu SSS](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act) · [artificialintelligenceact.eu](https://artificialintelligenceact.eu/transparency-rules-article-50/)
- **Digital Omnibus:** 6–7 Mayıs 2026 geçici uzlaşısına göre yüksek risk takvimi ertelendi: Ek III için 2 Aralık 2027, Ek I için 2 Ağustos 2028. **m.50 ertelenmedi.** Omnibus'un AB Resmî Gazetesi'nde yayımlanıp yayımlanmadığını doğrulayamadım. [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)
- AI Act ancak **AB pazarına çıkılırsa** ilgili hale gelir; yalnızca Türkiye'de yayınlanan bir sürümü doğrudan bağlamaz. (yorum) Tüzük metni: [AI Act — EUR-Lex 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

### 7.2 LLM ile sağlık tavsiyesinin riskleri
- **Anthropic AUP:** sağlık kararları ve tıbbi rehberlik "yüksek riskli kullanım" sayılıyor. Bu kullanımda **nitelikli bir profesyonel içerik yayımlanmadan önce onu gözden geçirmeli** ve kullanıcıya yapay zekâ kullanıldığı söylenmeli. Aynı politika wellness tavsiyelerinin (beslenme, uyku vb.) bu kategoriye girmediğini açıkça belirtiyor. [Anthropic AUP](https://www.anthropic.com/legal/aup)
- **OpenAI kullanım politikaları (29.10.2025):** lisans gerektiren kişiye özel tıbbi tavsiye, lisanslı bir profesyonelin uygun katılımı olmadan yasak. [KJK özeti](https://kjk.com/2025/12/18/openai-bans-personalized-professional-advice-in-2025-update/) · [OpenAI](https://openai.com/policies/usage-policies/) (sayfa araçla açılamadı; ikincil kaynak)
- **(yorum)** "Böbrek hastasısın, bu ürünü yeme" tipi kişiye özel LLM çıktısı hem sağlayıcının politikasını hem tıbbi cihaz sınırını hem de halüsinasyon sorumluluğunu tetikler. **LLM'i yalnızca içerik çıkarma** (etiket OCR'ını yapılandırma, içerik adlarını normalize etme) ve **genel açıklama** için kullanın. Kararı kural motoru versin.

### 7.3 Apple App Store
- **1.4.1:** Hatalı bilgi verebilecek tıbbi uygulamalar **daha sıkı incelenir.** Doğruluk iddiaları için veri ve metodoloji açıklanmalı. Uygulama kullanıcıya **doktora danışmasını** hatırlatmalı.
- **5.1.3(i):** Sağlık verisi reklam veya pazarlama amacıyla üçüncü taraflara verilemez.
- **5.1.3(ii):** Kişisel sağlık bilgisi **iCloud'da saklanamaz.**
- **5.1.1(v):** Hesap açılabiliyorsa **uygulama içinde hesap silme** zorunlu.
- **5.1.2(i):** Kişisel veri **üçüncü taraf yapay zekâyla** paylaşılacaksa bu açıkça söylenmeli ve **açık izin** alınmalı.
- Kaynak: [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)

### 7.4 Google Play
- **Health apps declaration formu** zorunlu; kapalı ve açık test dahil tüm kanallarda doldurulmalı. [Play Console Help](https://support.google.com/googleplay/android-developer/answer/14738291?hl=en)
- Tıbbi cihaz **olmayan** sağlık uygulamaları açıklamalarında şu anlamda bir uyarı taşımalı: uygulama "tıbbi cihaz değildir, herhangi bir tıbbi durumu teşhis etmez, tedavi etmez, iyileştirmez veya önlemez". Kullanıcıya bir sağlık profesyoneline danışması da hatırlatılmalı. Uygulama içi ve Console'da gizlilik politikası linki zorunlu. [Health Content and Services](https://support.google.com/googleplay/android-developer/answer/16679511?hl=en)
- Beslenme, "health and fitness" kategorisinde geçiyor. Sağlık iddiası yapan uygulamalar amaçlarını, iddianın dayanağını ve risklerini açıklamalı. [Health app categories](https://support.google.com/googleplay/android-developer/answer/13996367?hl=en)
- **(yorum)** Google'ın istediği uyarıdaki "önlemez" ifadesi, "alerjik reaksiyonu önler" pazarlamasıyla **doğrudan çelişir.** Bu da §3'teki dil kuralını mağaza tarafından da zorunlu kılıyor.
- **Health Connect:** yalnızca Health Connect verisine (kilo, kan şekeri vb.) erişilirse gerekir. MVP'de gerek yok. [Android — Health Connect publish](https://developer.android.com/health-and-fitness/health-connect/publish)

---

## 8. Sonuç

### 8.1 Projeyi öldürebilecek riskler (en fazla 5)

| # | Risk | Neden öldürür | Somut önlem |
|---|---|---|---|
| 1 | **Sağlık profilinin yurt dışı LLM veya buluta sistematik aktarımı** | Kurul henüz yeterlilik kararı vermedi. Düzenli aktarım arızi sayılmadığı için açık rıza yetmez. Standart sözleşme yoksa aktarım hukuka aykırı olur. Sağlık verisinde güvenlik ihlali cezası 17 milyon TL'ye kadar çıkıyor. | Profil ve geçmiş Türkiye'de barındırılır. LLM'e yalnızca ürün verisi gider. Yurt dışı kaçınılmazsa standart sözleşme imzalanıp 5 iş günü içinde bildirilir. |
| 2 | **Tıbbi cihaz sayılmak** ("önler", "hastalığını yönet", kişiye özel diyabet/böbrek uyarıları) | Sınıf IIa ve üstü onaylanmış kuruluş demek. Öğrenci ekibi bunu yapamaz. Mağazalar da kanıt ister. | Wellness ve bilgilendirme amacı her yerde tutarlı yazılır (mağaza metni, site, sunum). Yasaklı iddia listesi uygulanır. Hastalık bazlı uyarılar "besin öğesi bilgisi" düzeyinde kalır. Gerekirse TİTCK'ya ön danışma yapılır. |
| 3 | **Yanlış "güvenli" dönütü ve anafilaksi** | İtibar, dava ve mağazadan kaldırılma. Feragat metni ağır kusuru ve tüketiciye karşı haksız şartları kurtarmaz. | "Güvenli" kelimesi kullanılmaz. Üç durumlu sonuç, "doğrulanamadı" durumu, kaynak ve tarih gösterimi, her ekranda etiketi kontrol et uyarısı, şiddetli alerjisi olanlara açık uyarı, LLM karar vermez. |
| 4 | **Rıza ve aydınlatma kurgusunun yanlış kurulması** (tek metin, önceden işaretli kutu, başkası adına sağlık verisi) | Özel nitelikli veride işlemenin tek dayanağı geçersiz olur. 2026/347 ile Kurul bu konuya özellikle eğiliyor. | Ayrı metinler ve amaç başına rıza. Hane üyeleri kendi rızasını verir, çocuk için veli. Rıza kaydı tutulur, geri alınabilir, silme uygulama içinde. |
| 5 | **Veri lisansı / scraping** (OFF share-alike ihlali, izinsiz market verisi) | Veri kaynağının kesilmesi, ihtarname, haksız rekabet davası. Canlı üründe veri katmanının yeniden yazılması gerekir. | OFF ayrı ve değiştirilmemiş katmanda tutulur, atıf yapılır, katkılar geri gönderilir. Fiyat özelliği ya kaldırılır ya da yazılı izin alınır. |

### 8.2 Canlıya çıkmadan önce yapılacaklar
1. [ ] **Veri sorumlusunu belirle** (öğrenci / şirket / üniversite); **danışmana sor.**
2. [ ] Veri envanteri ve minimizasyon kararı; `plan/kararlar.md` dosyasına işlenir.
3. [ ] Barındırma yeri kararı (Türkiye). LLM'e ne gideceğinin kararı.
4. [ ] Aydınlatma metni + açık rıza ekranları (2026/347'ye uygun). Kopyala-yapıştır yok.
5. [ ] Gizlilik politikası (web'de, herkese açık URL, coğrafi kısıtsız), kullanım koşulları, tıbbi olmadığına dair uyarı metni.
6. [ ] Yasaklı iddia listesi; mağaza metni ve arayüz metinleri bu listeye göre gözden geçirilir.
7. [ ] Alerjen taksonomisi = TGK Ek-1'deki 14 alerjen (+ istisnalar). Besin öğesi eşiklerinin kaynağı dokümante edilir.
8. [ ] Üç durumlu sonuç arayüzü, "doğrulanamadı" durumu, kaynak ve tarih, yanlış bildir butonu.
9. [ ] Güvenlik: şifreleme, rol bazlı erişim, loglar, yedekleme; 2018/10 önlemlerinin listesi.
10. [ ] Uygulama içi hesap ve veri silme, rıza geri alma, m.11 başvuru kanalı.
11. [ ] İhlal müdahale planı (72 saat).
12. [ ] OFF atfı ve katkı geri gönderme akışı. Fiyat verisi için izin (ya da özellik yok).
13. [ ] Apple: 5.1.2(i) ve 5.1.3 kontrolü, App Privacy etiketi. Google: Health apps declaration, Data safety formu, uyarı metni.
14. [ ] İlk sürüm yalnızca Türkiye mağazası (GDPR, MDR ve AI Act'i sonraya bırakır).
15. [ ] Kullanıcı testlerinde gerçek sağlık verisi toplanacaksa **üniversite etik kurulu** gerekip gerekmediği danışmana sorulur (belirsiz).
16. [ ] Son metinlerin (gizlilik politikası, rıza metni, kullanım koşulları) bir avukata veya KVKK uzmanına bir kez okutulması; üniversite hukuk kliniği ya da barosu seçenek olabilir.

---

## 9. Levent'e açık sorular
- Uygulamayı kim yayınlayacak: bir öğrencinin bireysel geliştirici hesabı mı, şirket mi, üniversite mi? Veri sorumlusu buna göre belirlenir.
- LLM'in rolü tam olarak ne olacak: OCR/normalize mi, sohbet mi, karar mı?
- Hedef pazar yalnızca Türkiye mi?
- Fiyat karşılaştırma MVP'de şart mı?
- Hastalıklar (diyabet, böbrek, hipertansiyon) MVP'de mi, yoksa ilk sürüm yalnızca alerjen/çölyak ile mi çıkacak? İkincisi tıbbi cihaz riskini ciddi biçimde düşürür (yorum).

## 10. Doğrulanamayanlar / sınırlar
- marketfiyati.org.tr kullanım koşulları okunamadı.
- Büyük LLM ve bulut sağlayıcılarının KVKK standart sözleşmesi imzalayıp imzalamadığı bulunamadı.
- Gıda alerjen tarayıcılarına özel resmi bir MDR/TİTCK niteleme örneği bulunamadı.
- 2026 KVKK ceza tutarları ikincil kaynaktan alındı.
- AI Act Digital Omnibus'un AB Resmî Gazetesi'nde yayımlanıp yayımlanmadığı doğrulanamadı.
- OpenAI politika sayfası araçla açılamadı (403); içerik ikincil kaynaktan.
