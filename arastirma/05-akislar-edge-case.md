---
title: 05 — Kullanıcı akışları ve edge case'ler (v4 "Evin gıda asistanı")
updated: 2026-09-24
durum: TASLAK
dayanak: arastirma/04-vizyon-v4-tohum.md, plan/urun-tanimi.md, arastirma/01-mevzuat-risk.md, arastirma/02-v2-urun-deneyimi.md, arastirma/02-v2-fis-veri.md, arastirma/02-v2-kirmizi-takim.md
---

> **Taslak — Levent'le netleştirilmedi, 2026-09-24.**
> v4 vizyonunun (menü → liste → market → mutfak → öğren; görünür asistan; "LLM orkestra eder, motorlar karar verir") üzerine yazıldı. v3 ürün tanımında kapsam dışı olan **yemek planı ve kiler burada kapsama alındı**.
> "(yorum)" etiketli hukuki notlar hukukçu görüşü değildir. Tarihler "≈" ile verildiyse teyit edilmelidir.

---

## 0. Nasıl okunur

**Yapı:** Her akışta sırasıyla aktörler, happy path ve edge case tablosu var. Tablo sütunları şunlar: durum → ürünün tepkisi (ekranda ne olur, metin tonu) → önem → çözen katman.

**Önem**
- **Kritik:** fiziksel zarar ihtimali (alerjen), hukuki ihlal (KVKK, tıbbi cihaz sınırı) ya da geri dönüşsüz ifşa/veri kaybı.
- **Yüksek:** yanlış karar, güven kaybı ya da ciddi terk.
- **Orta:** sürtünme ya da geçici yanlışlık.
- **Düşük:** kozmetik veya nadir.

**Katmanlar**
- **UI:** istemci ekranı, metin, cihaz-içi barkod çözme.
- **Kural:** deterministik güvenlik kural motoru, alerjen taksonomisi, türev içerik sözlüğü.
- **Opt:** menü, sepet ve market optimizasyonu.
- **Agent:** LLM orkestrasyonu, vision/OCR, sohbet guardrail'leri.
- **Admin:** moderasyon, karar izi, KVKK talepleri, destek.
- **Altyapı:** veri modeli, senkron, kimlik, bildirim, barındırma, güvenlik.

**Kısaltmalar**
- Dört durum: `Uygun değil` · `Dikkat` · `Engel bulunmadı` · `Doğrulanamadı`.
- DR = Decision Record. P0–P3 = bildirim öncelikleri (§7).

**Metin tonu:** urun-tanimi §5 ve 02-v2 §8 geçerli. Sepet konuşulur, kişi değil. "Güvenli" kelimesi ve tıbbi fiil yok. Sen dili, kısa cümle. Tırnak içindeki cümleler ekran metni önerisidir.

### 0.1 Tablolarda tekrar edilmeyen çapraz kavramlar
| Kavram | Tanım |
|---|---|
| **Üç değerli kısıt durumu** | Bir üyenin bir alerjen için durumu `tanımlı`, `yok` (üye beyan etti) ya da `bilinmiyor` (girilmedi, rıza yok, davet bekliyor) olabilir. `bilinmiyor` durumunda şerit hüküm vermez, **"Kısıt eklenmemiş"** yazar. |
| **Asimetri ilkesi** | Belirsizlik her zaman daha katı hükme doğru çözülür. Katılaştıran değişiklik ucuzdur. Gevşeten değişiklik daha fazla kanıt ve onay ister. |
| **Sürüm zinciri** | Her hüküm = f(ürün kaydı sürümü, profil sürümü, kural sürümü). Biri değişince ona bağlı canlı nesneler (plan, liste, kiler hükmü, cihaz önbelleği) yeniden değerlendirilir. Geçmiş DR'ler değişmez ve yeniden üretilebilir kalır. |
| **Genel mod** | Sağlık rızası olmadan çalışan mod. İçerik ve 14 alerjen vurgusu herkese aynı gösterilir, kişiye hüküm verilmez. Liste, bütçe planı, fiş ve kiler çalışır. |
| **Hane kuralı** (öneri, yorum) | Kişiye bağlanmayan, hesap sahibinin kendi tercihi olarak girdiği dışlama. Örnek: "evimize fındık girmesin". Başkası adına sağlık verisi girmeden koruma sağlar. **Sağlık verisi sayılıp sayılmadığını bir KVKK uzmanı teyit etmeli.** |
| **Olay kısıtı** | Misafir veya etkinlik kısıtı kişiye değil **yemeğe** bağlanır ("Cumartesi yemeği glutensiz"). Ad sorulmaz, etkinlikten sonra silinir. |
| **Kısıt kartı** | Veli, seçtiği kısıtları tarihli, yazdırılabilir bir PDF'e dökebilir (okul, büyükanne, restoran için). Kartı kimin göreceğine kullanıcı karar verir. |

---

## 1. İlk kurulum ve onboarding

**Aktörler:** kurucu yetişkin (planlayıcı ebeveyn), davet edilen yetişkin, çocuk profili (veli yönetir), genç (13–17; açık soru), yardımcı/bakıcı.

### Happy path
1. **Karşılama.** Tek cümle ve bir "Sadece bakıyorum" seçeneği (dolu örnek hane) var. Hesap istenmez.
2. **Önce değer.** Asistan tek bir soru sorar: "Bu hafta evde kaç kişi yemek yiyecek?" 30 saniyede kısıtsız bir haftalık plan ve liste çıkar (varsayılan bütçeyle).
3. **Hesap.** Planı saklamak için Apple, Google ya da e-postayla kaydolunur.
4. **Hane kurma.** Hane adı ve üyeler girilir: takma ad, yaş aralığı, rol. Her üyenin kısıt durumu **`bilinmiyor`** olarak başlar.
5. **Kendi kısıtını ekleme.** O anda iki ayrı bölüm açılır: aydınlatma ("Okudum" butonu, onay değil) ve açık rıza (işaretlenmemiş kutu). Ardından kısıt çipleri seçilir; belirsiz terimlerde görselli netleştirme gelir.
6. **Çocuk ekleme.** Veli beyanı ve veli rızası alınır. Takma ad ya da emoji önerilir.
7. **Yetişkin daveti.** WhatsApp linki gönderilir. Davetli kendi hesabıyla katılır ve kısıtını kendisi girer. Kurucu katılımı onaylar.
8. **Bütçe ve konum.** Bütçe, tercih edilen zincir(ler) ve il/ilçe girilir. Konum izni istenmez.
9. **Şiddetli alerji satırı.** Bir kez gösterilir, sonra her zaman erişilebilir kalır: "NutriScan etikette beyan edileni karşılaştırır. Etiketi her zaman sen kontrol et; doktorunun eylem planı önce gelir."
10. **İlk kısıtlı plan.** "Ela için fındıksız, ≈ 1.850 TL. Onaylıyor musun?"

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 1.1 | **Sağlık bilgisi vermeden devam** | Genel mod açılır. Şeritte her üye için gri **"Kısıt eklenmemiş"** yazar; `Engel bulunmadı` asla gösterilmez. Plan bütçe ve tercihle çalışır. Hatırlatma en fazla 2 haftada bir, bağlam içinde gelir (ör. taramadan sonra): "Bu üründe fındık beyan edilmiş. Evde kaçınan biri varsa kısıt ekleyebilirsin." | Kritik | UI · Kural |
| 1.2 | **Açık rıza reddedildi ama kullanıcı kısıt girmeye çalışıyor** | Kısıt kaydedilmez. "Kısıtını kaydetmek için izin gerekiyor. İzin vermeden de listeni ve bütçeni planlayabilirsin." Soru tekrar tekrar sorulmaz, dark pattern yok. Red zaman damgasıyla rıza kaydına yazılır. | Kritik | UI · Altyapı |
| 1.3 | **Kurucu, eşinin kısıtını kendisi girmek istiyor** | Engellenir, iki yol sunulur: davet et ya da hane kuralı ekle. "Murat'ın bilgisini Murat girmeli. İstersen şimdi 'evde fındık istemiyoruz' diye bir hane kuralı ekleyebiliriz." Hane kuralı hard kısıt gibi uygulanır ama kimseye atfedilmez. | Kritik | UI · Kural |
| 1.4 | **Davet kabul edilmiyor / hiç açılmıyor** | Üye "Davet bekliyor" durumunda, kısıtı `bilinmiyor` kalır. Link 7 gün sonra geçersiz olur. Tek bir hatırlatma teklif edilir. Plan kartında "Murat'ın kısıtları henüz yok" satırı görünür. | Yüksek | UI · Altyapı |
| 1.5 | **Davet linki yanlış kişiye iletildi ya da grupta paylaşıldı** | Link tek kullanımlıktır. Katılım isteği kurucunun onayına düşer: "Ayşe K. haneye katılmak istiyor. Tanıyor musun?" Onaydan önce davetli hiçbir hane verisini göremez. | Kritik | Altyapı · UI |
| 1.6 | **Alerjen adı belirsiz:** "fıstık" (yer fıstığı = TGK #5, Antep fıstığı = sert kabuklu #8, çam fıstığı = listede yok), "kuruyemiş", süt alerjisi mi laktoz intoleransı mı, çölyak mı gluten hassasiyeti mi | Görselli netleştirme kartı açılır. Şemsiye terim alt türlere ayrılır: "Sert kabukluların hepsi mi, yalnız fındık mı?" Laktoz seçilince uyarı çıkar: "Süt alerjisi farklıdır: laktozsuz süt süt alerjisine uygun değildir." Kullanıcı emin değilse geniş olan seçenek önerilir. | Kritik | UI · Kural |
| 1.7 | **TGK 14 dışında alerji** (kivi, nohut/mercimek, çam fıstığı, domates, mısır) | "Özel kısıt" olarak eklenir, ama hüküm tavanı düşüktür. Etikette kelime eşleşirse `Uygun değil`. Eşleşmezse en iyi hüküm `Dikkat` olur, `Engel bulunmadı` değil. "Kivi zorunlu alerjen listesinde yok, etiketlerde gizli kalabilir. Bulursam söylerim; bulamazsam 'engel yok' demem." | Kritik | Kural · UI |
| 1.8 | **Çocuk için gerçek ad, doğum tarihi ya da fotoğraf girilmek isteniyor** | Takma ad veya emoji önerilir. Yaş yerine aralık tutulur (0–3 · 4–12 · 13–17). 18 yaş geçişi için yalnız doğum yılı ve ayı tutulabilir (açık soru, §8.5). Fotoğraf alanı yok. Veli beyanı ("Bu çocuğun velisiyim") kaydedilir. | Yüksek | UI · Altyapı |
| 1.9 | **Genç (13–17) kendi telefonunda kullanmak istiyor** | *(Açık soru)* Önerilen: veli davetiyle "genç hesabı". Genç listeye ekleyebilir, tarama yapabilir, kendi kısıtını görebilir. Bütçeyi ve başkalarının kısıt nedenlerini göremez. Asimetri gereği kısıt **ekleyebilir** ama **kaldıramaz**; kaldırmayı veli yapar. | Yüksek | UI · Altyapı |
| 1.10 | **İki ebeveyn davetten önce ayrı haneler kurmuş, ikisi de "Ela"yı eklemiş** | Hane birleştirme sihirbazı açılır: hangi hane kalacak; liste, bütçe ve kiler hangi taraftan alınacak. İki "Ela" profili velinin onayıyla birleştirilir, hard kısıtların **birleşimi** alınır ve fark gösterilir: "Selin fındık, Murat fındık + susam girmiş. İkisi de uygulanacak." | Yüksek | Altyapı · UI |
| 1.11 | **Hesap birleştirme:** iPhone'da Apple (gizli e-posta), web'de Google hesabı ya da anonim oturumdan hesaba geçiş | Ayarlar > "Hesapları bağla": kullanıcı iki hesapta da oturum açarak sahipliği kanıtlar. Birleştirme önizlemesi gösterilir, sağlık verili iki profil birleşirken kısıtların birleşimi alınır ve kullanıcı onaylar. Anonim oturum verisi hesap açılınca taşınır, açılmazsa 30 gün cihazda kalır. Gizlilik gereği otomatik "başka hesabın var" tespiti yapılmaz. | Orta | Altyapı |
| 1.12 | **Bir kişi iki hanede** (üniversiteli: yurt + aile evi; ev arkadaşları; yazlık) | Kişinin tek hesabı ve birden fazla hane üyeliği olur. Kısıtlar kişiye bağlıdır; her haneyle paylaşım için ayrı onay gerekir ("Kısıtların 'Yurt' hanesinde de görünsün mü?"). Üst barda aktif hane gösterilir, tarama aktif hanenin üyelerini kullanır. Bildirim başlığında hane adı yazar. | Yüksek | Altyapı · UI |
| 1.13 | **Boşanmış ebeveynler / iki ev** (Ela hafta içi annede, hafta sonu babada) | Çocuk profili haneden bağımsız bir "kişi" kaydıdır. Oluşturan veli diğerini **ortak veli** olarak davet eder; kabul edilirse profil iki haneye bağlanır. Kısıtlar ortaktır; liste, bütçe, fiş ve kiler paylaşılmaz. Kısıt eklemek için tek veli yeter, kaldırmak için iki veli (ya da velayet sahibi; hukuk teyidi) gerekir. Diğer veli uygulamada değilse sistem "aynı çocuk mu" eşleştirmesi **yapmaz**. Varlık takvimi ("Ela hafta sonu bizde değil") porsiyonu değiştirir, hard kısıtı değiştirmez (bkz. 3.6). | Kritik | Altyapı · Kural · UI |
| 1.14 | **Bakıcı / büyükanne / yardımcı** | "Yardımcı" rolü: yalnız velinin seçtiği çocukların hard kısıtlarını ve hükümlerini görür; tarama yapabilir, listeye ekleyebilir. Bütçe, fiş ve yetişkin kısıtları görünmez. Rol süreli (ör. 30 gün, yenilenebilir) ve velinin açık paylaşım onayına bağlıdır. Akıllı telefonu olmayan büyükanne için **Kısıt kartı** (PDF) basılabilir. | Yüksek | UI · Altyapı |
| 1.15 | **Yaşlı ebeveynin alışverişini uzaktan yapan yetişkin evlat** (anne ayrı yaşıyor, şeker hedefi var, akıllı telefonu yok) | Başkası adına veri girilemez. İki yol var: (a) anne kendi numarasına gelen SMS koduyla, yüz yüze kurulumda kendi rızasını verir; (b) evlat kendi hesabında "annemin listesi" için hane kuralı tanımlar. (yorum; hukukçu teyidi gerekli) | Yüksek | Altyapı · UI |
| 1.16 | **Şiddetli alerji / anafilaksi geçmişi beyan edildi** | Uyarı bir kez tam ekran gösterilir, sonra her hükmün altında küçük ve kalıcı bir satır olarak durur. Uygulama "önler" ya da "korur" demez. "Doktorunun eylem planı her zaman önce gelir. Etiketi sen de kontrol et." | Kritik | UI |
| 1.17 | **Onboarding yarıda kesildi** (uygulama kapandı, telefon çaldı) | Adımlar taslak olarak saklanır ve "Kaldığın yerden devam" sunulur. Rıza verilmeden girilen kısıtlar kalıcı kaydedilmez. Yarım kalmış rıza, rıza sayılmaz. | Orta | UI · Altyapı |
| 1.18 | **Çok kalabalık / çok kuşaklı hane (8 kişi) ya da ev arkadaşı hanesi** | Şerit özetlenir: "6 kişi için engel bulunmadı · 1 kişi Dikkat · 1 kişide kısıt eklenmemiş". Dokununca açılır. Ev arkadaşı tipinde bütçe kişi başınadır, ortak kalemler ayrı tutulur. | Orta | UI · Opt |
| 1.19 | **Erişilebilirlik:** az gören, yaşlı ya da okuma güçlüğü olan kullanıcı | Onboarding sesli asistanla tamamlanabilir. Dinamik yazı boyutu desteklenir. Rıza metni sesli okunabilir, ama **kutuyu kullanıcı kendisi işaretler**; asistan sesli komutla rıza veremez. | Orta | UI · Agent |

---

## 2. Asistanla sohbet (yazılı ve sesli)

**Aktörler:** her yetişkin üye, genç ya da çocuk (ebeveynin telefonunda), markette sesli kullanan kişi.

### Happy path
1. Kullanıcı yazar ya da söyler: "Bu akşam 30 dakikada ne pişirsem, evde ıspanak var."
2. Türkiye'deki sunucu kimliği ve hane bağlamını yükler. Serbest metin **maskelenir**: sağlık terimleri ve üye adları yer tutucuya (`ÜYE_2`, `KISIT_7`) dönüşür.
3. LLM niyeti çıkarır ve araç planını yapar: `kiler_oku` → `tarif_öner` → `kural_kontrol` → `fiyat`.
4. Ekranda canlı adım şeridi görünür: "Kilerine bakıyorum → 3 tarif buldum → Ela için kontrol ediyorum".
5. Yanıt 3 karttır. Her karttaki hüküm çipleri **araç çıktısından** çizilir, "Neden?" katmanı vardır. LLM metni yalnızca anlatır.
6. Kullanıcı bir tarif seçer. "Eksik 3 malzemeyi listeye ekleyeyim mi?" sorusuna onay verir, kalemler eklenir ve 10 saniye "Geri al" görünür.
7. Asistan bir tercih öğrenirse ("Murat patlıcan sevmez") önce sorar: "Hafızama ekleyeyim mi?" Eklenen bilgi "Hafızam" ekranında görünür ve düzenlenebilir.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 2.1 | **Belirsiz istek** ("bir şey öner", "ucuz bir şey") | Bağlamdan varsayım yapılır, en fazla bir soru sorulur. Varsayımlar düzenlenebilir çip olarak görünür: [4 kişi] [30 dk] [önce evdekiler]. | Orta | Agent · UI |
| 2.2 | **Tehlikeli istek:** "Fındık alerjim var ama biraz yesem olur mu?" | LLM'den **önce**, Türkiye'de çalışan deterministik güvenlik sınıflandırıcısı (sözlük + küçük model) devreye girer ve sabit şablon döner: "Ne kadarının sorun olacağını söyleyemem; bu doktorunun vereceği bir karar. Fındıksız benzer seçenekler: …" Evet/hayır, doz ve ahlak dersi yok. | Kritik | Agent · Kural |
| 2.3 | **Akut belirti bildirildi** ("dudağım şişti", "Ela fındık yedi, nefesi daralıyor") | Sohbet durur ve tam ekran uyarı açılır: **"Acil durumda hemen 112'yi ara."** Yanında [112'yi ara] butonu olur. LLM üretimi, tarif ya da öneri yok. Olay yalnız sayaç olarak loglanır, içerik tutulmaz. | Kritik | Agent · UI |
| 2.4 | **Tıbbi soru** ("şekerim 280 ne yiyeyim", "insülinden önce ne yemeliyim", "hamileyim, bunu yiyebilir miyim") | Tedavi, doz ya da teşhis yok. Etiket bilgisi verilebilir: "Bu üründe porsiyon başına 18 g şeker beyan edilmiş." "Güvenle tüketilebilir" gibi ifadeler yasak. Tek satır yönlendirme: "Bunu hekiminle konuşmalısın." | Kritik | Agent |
| 2.5 | **Kapsam dışı** ("maç kaç kaç", "ödevimi yaz") | Tek cümlelik kibar sınır ve 3 örnek yetenek: "Ben evin yemek ve alışveriş işlerine bakıyorum. Mesela: …" Maliyet için istek erken kesilir. | Düşük | Agent |
| 2.6 | **Yanlış anlama / STT hatası** ("fındıksız" → "fındıklı", "Ela" → "Ala", "fındık" ↔ "fıstık") | Durum değiştiren her şey onay kartıyla döner: "Şunu anladım: Ela için fındıksız · 1.500 TL. Doğru mu?" Sesli modda anlaşılan geri okunur. Alerjen terimi içeren bir STT sonucunun güveni düşükse yazılı onay istenir. | Kritik | Agent · UI |
| 2.7 | **Karışık dil, şive, bölgesel ürün adı** ("gevrek" İzmir'de simit demek; "pazı", "bazlama"; "abe şu cipsi alsam mı"; Türkçe-Kürtçe, Arapça ya da İngilizce karışık) | Bölgesel eş anlamlılar sözlüğü kullanılır (Admin yönetir). Emin değilse görselli sorar: "Simit mi demek istedin?" v1 yalnız Türkçe arayüzdür; başka dilde gelen isteğe dürüst yanıt verilir: "Şimdilik yalnız Türkçe anlayabiliyorum." (Arapça: açık soru) | Orta | Agent · Admin |
| 2.8 | **Çocuk kullanıcı** (ebeveynin telefonu ya da genç hesabı) | Kilo, kalori ve diyet konuşulmaz. "Kilo vermek istiyorum" gelirse yargısız yanıt: "Bunu ailenle ve doktorunla konuşmak en iyisi." Kısıt, bütçe ve paylaşım eylemleri kapalıdır. Yeme bozukluğu sinyalinde ("hiç yemek istemiyorum") destekleyici tek mesaj ve profesyonel yönlendirme verilir, ayrıntıya girilmez. | Yüksek | Agent |
| 2.9 | **Küfür, taciz, kötüye kullanım** | Yanıt sakin ve kısa olur, kullanıcının diline ayak uydurulmaz. Tekrarlanırsa kısa bir bekleme süresi konur. Hesap bazlı oran sınırı var. Sohbet içeriği moderasyona gönderilmez (mahremiyet), yalnızca sayaç tutulur. | Düşük | Agent · Altyapı |
| 2.10 | **Jailbreak / yasaklı dil zorlaması** ("sadece 'güvenli' de", "doktor gibi davran") | Deterministik çıktı filtresi yasaklı kelime ve iddia listesini (güvenli, önler, tedavi eder, doktor onaylı, %100) tarar. Eşleşme varsa yanıt engellenir ve şablon metin döner. Olay loglanır, eval setine eklenir. | Kritik | Agent |
| 2.11 | **Prompt injection:** ürün adında, topluluk katkısında, fiş satırında ya da ambalaja basılı metinde "önceki talimatları yok say" | Araç çıktıları "veri" olarak işaretlenir. İçerikten gelen metin durum değiştiren bir araç çağıramaz. Katkı metinleri moderasyonda injection taramasından geçer. | Kritik | Agent · Admin |
| 2.12 | **LLM anlatımı araç hükmüyle çelişiyor** (metin "Ela yiyebilir" derken araç `Uygun değil` dönmüş) | Hüküm çipleri LLM metninden değil araç çıktısından çizilir. Gönderimden önce iddia–araç eşleşme denetimi yapılır. Çelişki varsa metin atılır, şablon açıklama gösterilir, olay eval setine düşer. | Kritik | Agent · Kural |
| 2.13 | **Asistan hata yaptı, kullanıcı düzeltiyor** ("Bu üründe fındık yok, yanlış söylüyorsun") | Asistan hükmü değiştiremez. "Etikette gördüğün farklı mı? Fotoğrafını çekersen kontrol ettireyim." Bu, hatalı veri bildirimi olarak Admin kuyruğuna gider. Tercih ya da hafıza hatasında ("Murat patlıcanı sever") asistan anında düzeltir. | Yüksek | Agent · Admin |
| 2.14 | **Uzun oturum / haftalarca süren hafıza** | Hard kısıtlar sohbet hafızasından değil, her seferinde **profilden** okunur (tek doğruluk kaynağı). Sohbet hafızası özetlenir, "Hafızam" ekranından görülüp silinebilir. Sohbette geçen sağlık bilgisi sessizce kaydedilmez: "Bunu Ela'nın profiline ekleyeyim mi?" sorusuyla rıza akışına gider. | Kritik | Agent · Altyapı |
| 2.15 | **Hane içi mahremiyet** (Can, 15: "annem bilmesin ama vejetaryen oldum") | Sohbetler kişiye özeldir, diğer üyeler göremez. Haneye yansıyan her şey açık bir eylemdir: "Bunu hane planına ekleyeyim mi? Diğerleri planda 'vejetaryen seçenek' görecek." | Yüksek | Altyapı · Agent |
| 2.16 | **Serbest metin ya da ses sağlık verisi içeriyor** ve yurt dışı LLM/STT'ye gidebilir | Türkiye'deki sunucuda maskeleme yapılır (sözlük + NER): "fındığa dokunuyor", "şekerim var" gibi ifadeler yer tutucuya döner. Maskeleme güveni düşükse istek Türkiye'de barındırılan açık ağırlıklı modele yönlendirilir. STT de Türkiye'de ya da cihazda çalışır. *(Hipotez; teknik spike gerekli)* | Kritik | Agent · Altyapı |
| 2.17 | **Markette sesli yanıt:** kalabalıkta sağlık ayrıntısı yüksek sesle söyleniyor | Varsayılan olarak sesli yanıtta hüküm söylenir, neden söylenmez: "Ela için uygun değil, ayrıntı ekranda." Kullanıcı ayardan değiştirebilir. | Yüksek | UI · Agent |
| 2.18 | **LLM yavaş ya da erişilemiyor** (sağlayıcı kesintisi, kota) | 3 saniyede adım şeridi görünür. 8 saniyede: "Asistan şu an yavaş; butonlarla devam edebilirsin." Tarama, liste, plan onayı ve kısıt kontrolü LLM olmadan çalışır. | Yüksek | Altyapı · UI |
| 2.19 | **Asistan durum değiştiren bir eylem yapacak** (davet, diyetisyen paylaşımı, plan onayı, silme) | Her biri için tek dokunuşlu onay kartı gösterilir. Geri alınabilir eylemlerde "Geri al" çıkar, geri alınamazlarda açık uyarı verilir. | Yüksek | Agent · UI |
| 2.20 | **"Komşu aşure getirdi, Ela yiyebilir mi?"** (ev yapımı, etiketsiz) | Hüküm `Doğrulanamadı`. Genel bilgi verilir: "Aşurede sık fındık, ceviz ve Antep fıstığı olur. Yapan kişiye sormak en iyisi." Tahminle hüküm verilmez. | Kritik | Kural · Agent |
| 2.21 | **Marka karalama sorusu** ("X markası zehir mi?") | Yanıt etiket bilgisine döner, kanaat bildirilmez. Resmî bir liste kaydı varsa kaynağıyla birlikte "olası eşleşme" diliyle verilir. | Orta | Agent |
| 2.22 | **Kullanıcı asistanı insan ya da doktor sanıyor** ("sen doktor musun?") | "Ben bir yapay zekâ asistanıyım, doktor değilim." Asistan ilk kullanımda kendini bu şekilde tanıtır. | Orta | Agent |

---

## 3. Haftalık menü ve liste planlama

**Aktörler:** planlayıcı ebeveyn, diğer yetişkinler, asistan (proaktif).

### Happy path
1. **Proaktif plan.** Pazar sabahı, öğrenilmiş saatte asistan yazar: "Haftalık planın hazır: 5 akşam yemeği ≈ 1.850 TL, kilerdeki yoğurt ve ıspanak kullanıldı. Bakar mısın?"
2. **Plan ekranı.** Gün kartları, her yemekte üye bazlı durum çipleri, bütçe çubuğu ve "Neden bu yemek?" katmanı görünür.
3. **Değişiklik.** Kullanıcı bir yemeği değiştirir ("Çarşamba balık olmasın"). Plan en az sapmayla yeniden hesaplanır.
4. **Liste.** Onaydan sonra liste üretilir: menü malzemeleri − kiler + alışkanlık kalemleri. Akıllı Takas önerileri en fazla k tanedir.
5. **Market seçimi.** Tek durak / En ucuz / Dengeli.
6. **Paylaşım.** Liste haneyle canlı paylaşılır.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 3.1 | **Olursuz plan** (kısıtlarla bütçe tutmuyor; glutensiz ürünler pahalı) | "Bu kısıtlarla en düşük ≈ 2.140 TL. Şunlardan biri işe yarar: bütçe +290 TL · 2 akşam bakliyat · iki market." Gevşetme önerilerinde hard kısıt **hiçbir zaman** yer almaz. | Kritik | Opt · Kural |
| 3.2 | **Misafir** ("Cumartesi 6 kişiyiz, biri vegan, biri çölyak") | Olay kısıtı olarak işlenir: kısıt yemeğe bağlanır, misafirin adı sorulmaz, etkinlikten sonra silinir. Şiddetli alerji söylenirse ek satır: "Etiketleri misafirinle birlikte kontrol edin." | Kritik | Opt · UI · Altyapı |
| 3.3 | **Ramazan** (≈ 8 Şubat – 9 Mart 2027; Diyanet takvimiyle teyit): iftar/sahur, oruç tutan ve tutmayan üyeler | Ramazan modu öğün yapısını iftar + sahur olarak değiştirir. Pide ve hurma şablonları gelir. Bildirimler iftar ±1 saatte ve sahurda susturulur. Şeker hedefli üye için "oruç tutmalı mı" tavsiyesi verilmez; soru gelirse hekime yönlendirilir. | Yüksek | Opt · UI · Agent |
| 3.4 | **Bayram** (Kurban ≈ 16–19 Mayıs 2027, beta dönemine denk geliyor): kurban eti, bayram ziyaretleri, ikramlık | Kilere çok miktarda et ve dondurucu kalemi eklenir; plan eti önceliklendirir ama her gün et zorlamaz. Ziyaret günlerinde evde daha az öğün planlanır. İkramlık fındıklı çikolata "misafir ikramlığı" etiketiyle kilere girer; Ela'nın öğünlerine girmez, şerit uyarısı sürer. | Yüksek | Opt · Kural |
| 3.5 | **Bütçe hafta ortasında değişti** (maaş gecikti, −1.000 TL) | Yalnız henüz alınmamış kalemler en az sapmayla yeniden optimize edilir. Alınmış ya da pişmiş olana dokunulmaz. "3 değişiklikle 1.000 TL düşer: …" | Yüksek | Opt |
| 3.6 | **Üye yok, tatilde ya da diğer evde** | Porsiyon ve tercih ağırlığı düşer. **Hard kısıt varsayılan olarak aktif kalır**, çünkü raf ömrü uzun ürünler üye döndüğünde hâlâ evde olur. Kullanıcı açıkça "Ela yokken fındıklı alınabilir" derse bu yalnızca o haftanın taze öğünleri için geçerli olur; kilerde kalacak kalemler işaretlenir. | Kritik | Opt · Kural · UI |
| 3.7 | **Tercih çatışması** (Murat et istiyor, Can vejetaryen, küçük çocuk seçici) | Ortak taban + varyant önerilir ("etli ve etsiz ayrı tencere"). Adalet kısıtı: aynı kişinin tercihi arka arkaya feda edilmez. Kimse adıyla suçlanmaz. | Orta | Opt |
| 3.8 | **Aynı yemek tekrarı / çeşitlilik** | Çeşitlilik kısıtı: aynı ana yemek 7 günde en fazla bir kez. Hanenin sabit günleri öğrenilir ve korunur (Cuma balık, Pazartesi kuru fasulye). | Düşük | Opt |
| 3.9 | **Planlanan ürün rafta yok** | Kullanıcı "Yoktu" der. Aynı kısıtlarla, kural kontrolünden geçmiş alternatif gelir; yalnız etkilenen yemek yeniden hesaplanır. "Yoktu" bilgisi zincir-şube-gün olarak kaydedilir. | Yüksek | Opt · Kural · UI |
| 3.10 | **LLM'in önerdiği tarifte gizli alerjen ya da bileşik içerik** (pesto = çam fıstığı + peynir, tahin = susam, Worcestershire = balık, hazır çorba, bulyon) | Tarif motoru LLM'den yapılandırılmış malzeme listesi alır ve her malzemeyi taksonomiye çözer. Çözülemeyen bileşik içerik varsa yemek `Doğrulanamadı` olur: ya plana girmez ya da "hazır sos yerine evde yap" varyantıyla girer. | Kritik | Kural · Agent |
| 3.11 | **Kiler varsayımı yanlış** (plan "evdeki yoğurt"u kullanıyor ama yoğurt bitmiş ya da bozulmuş) | Onaydan önce en fazla 3 kiler kalemi için hızlı teyit sorulur: "Hâlâ var mı?" Yoksa kalem listeye eklenir. | Orta | UI · Opt |
| 3.12 | **Fiyat bilinmiyor ya da eski** | Bütçe aralık olarak gösterilir: "≈ 1.750–1.950 TL · 4 ürünün fiyatı 20 günden eski." Fiyat uydurulmaz. Bütçe hard kısıtsa hesap üst sınırla yapılır. | Yüksek | Opt |
| 3.13 | **Birim/porsiyon dönüşüm hatası** ("2 su bardağı un", "1 demet maydanoz", paket boyu) | Dönüşüm tablosu ve paket yuvarlaması kullanılır ("500 g'lık paket"). Miktar düzenlenebilir. Artan miktar kilere geçer. | Orta | Opt · Kural |
| 3.14 | **Mutfak kısıtları** (fırın yok, hafta içi ≤30 dk, tek ocak, yurt) | Profil ayarı olarak girilir ve zamanla öğrenilir, tarif filtrelerine yansır. | Düşük | Opt |
| 3.15 | **Proaktif plan görmezden gelindi ya da reddedildi** | Plan "taslak" olarak kalır, arkasından hatırlatma gitmez. "Bu hafta plan istemiyorum" tek dokunuştur, neden sorulmaz. Üç hafta üst üste reddedilirse öneri sıklığı ayda bire iner ve bu kullanıcıya söylenir. | Orta | Agent · UI |
| 3.16 | **İki evde yaşayan çocuk ve okul beslenme çantası** (okulda fındık yasağı) | Varlık takvimi kullanılır. "Beslenme çantası" ayrı bir öğün tipidir. Okulun kuralı hane kuralı olarak girilir. | Orta | Opt · UI |
| 3.17 | **Sağlık hedefi (şeker azalt) bütçeyle çatışıyor** | Hedef soft kısıttır, bütçe önceliklidir; öneriler varsayılan olarak "daha pahalı" olamaz. Kullanıcı "sağlığın fiyatı" eğrisinden kendi seçer. Tıbbi dil kullanılmaz. | Orta | Opt |
| 3.18 | **Plan onaylandıktan sonra bir üyeye yeni hard kısıt eklendi** | Plan ve liste anında yeniden doğrulanır. Etkilenen yemekler `Uygun değil` olarak işaretlenir, "onaylı" rozeti düşer ve alternatif teklif edilir. | Kritik | Kural · Altyapı |

---

## 4. Rafta tarama

**Aktörler:** markette alışveriş yapan üye, yardımcı; sesli mod.

### Happy path
1. Tara sekmesi açılır. Kamera izni bağlam içinde istenir. Barkod cihazda 300 ms'nin altında çözülür.
2. Ürün kimliği doğrulanmış katalog kaydına eşlenir (kayıt sürümü ve doğrulama tarihiyle).
3. Kural motoru her üye × içerik için dört durumlu hüküm üretir ve bir DR yazar.
4. Ekranda: ürün, hane şeridi (Ela: `Uygun değil` · fındık), "Etiketi kontrol et" satırı, "Neden?" katmanı, planına etkisi ve bir alternatif (aynı zincir, kısıtlara uygun, fiyat farkıyla).
5. Ürün listeye ya da sepete eklenir, liste kalemi işaretlenir.
6. Sesli mod: "Bunu Ela yiyebilir mi?" sorusuna aynı hüküm sesli döner.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 4.1 | **Barkod okunmuyor** (buruşuk, kavisli, parlama, küçük) | 3. saniyede ipucu: "Biraz uzaklaştır · feneri aç." 6. saniyede iki seçenek: "Numarayı yaz" (13 hane, kontrol basamağı doğrulanır) ya da "Etiketi çek". | Orta | UI |
| 4.2 | **Ürün katalogda yok** (BİM/A101/ŞOK aktüel ürünü, yerel üretici) | Hüküm `Doğrulanamadı`: "Etiketi çekersen 10 saniyede okurum." Sonra: OCR → içindekiler bölümü tespiti → alerjenler vurgulanır → kullanıcı onaylar. Hüküm yalnız bu kullanıcıya, "Etiketten okundu · doğrulama bekliyor" rozetiyle gösterilir. `Engel bulunmadı` için içindekiler bölümü eksiksiz okunmuş ve OCR güveni eşiğin üstünde olmalı. Kayıt moderasyona düşer. | Kritik | Agent · Kural · Admin |
| 4.3 | **Farklı ülke barkodu / ithal ürün** (GS1 öneki 869 değil; Türkçe ithalatçı etiketi yapıştırılmış) | OFF'taki yabancı sürüm Türkiye sürümünden farklı olabilir: "Bu kayıt başka bir ülke sürümüne ait olabilir; Türkçe etiketle karşılaştır." Hüküm `Doğrulanamadı` ya da Türkçe etiket okuması olur. GS1 öneki üretim ülkesini kanıtlamaz, yalnız GS1 üyeliğini gösterir. | Yüksek | Kural · Agent |
| 4.4 | **Aynı barkod, değişmiş tarif** (ya da küçük üreticinin barkodu başka ürüne yeniden kullanması) | Her katalog kaydında "son doğrulama" tarihi var. Ör. 180 günden eski kayıtlar "eski olabilir" rozeti taşır. Kullanıcının etiket fotoğrafı kayıttan farklıysa diff moderasyona gider. Onaylanan değişiklik hükmü katılaştırıyorsa ürünü kilerinde tutan hanelere tarif radarı bildirimi gider. Ürün adı tamamen farklıysa: "Bu barkod başka bir ürüne ait görünüyor." | Kritik | Kural · Admin · Altyapı |
| 4.5 | **Çoklu paket** (koli barkodu, 3'lü paket, her aroması farklı alerjen içeren karışık paket) | Dış paket barkodu tekil ürüne eşlenmez. Karışık pakette hüküm, içindeki **en katı** ürünün hükmüdür. "İçindeki ürünleri tek tek tarayabilirsin." | Kritik | Kural · UI |
| 4.6 | **Dökme ürün / semt pazarı / tezgâh** (kuruyemişçi, peynir tezgâhı, fırın, kasap; barkod yok) | Barkod yoksa hüküm `Doğrulanamadı`. Kuruyemiş ve unlu mamul tezgâhlarında sert kabuklu ya da gluten kısıtı olan üye için hüküm en iyi hâlde `Dikkat` olur (çapraz bulaşma). "Satıcıya sor; açıkta satılan gıdada da alerjen bildirimi zorunlu." | Kritik | Kural · UI |
| 4.7 | **Mağaza içi tartı/raf barkodu** (20–29 önekli, içinde fiyat gömülü) | Bu barkod global bir kimlik taşımaz: "Bu mağaza içi tartı etiketi; ürünün kendi ambalajını ya da etiketini tara." Etiketten kilogram fiyatı okunabilir. | Orta | UI · Kural |
| 4.8 | **İnternet yok** (bodrum kattaki market) | Cihazda şifreli olarak hanenin kısıtları, pilot zincirin katalog alt kümesi ve kural sürümü bulunur. Çevrimdışı hüküm rozetle verilir: "Çevrimdışı · katalog 3 gün önce güncellendi". Ürün önbellekte yoksa `Doğrulanamadı`. Profil önbelleği eskiyse (başka bir cihazda yeni kısıt eklenmiş olabilir): "Son eşitleme 2 gün önce; yeni eklenen kısıtlar burada görünmeyebilir." Bekleyen işlemler bağlantı gelince senkronlanır. | Kritik | Altyapı · Kural |
| 4.9 | **Işık kötü, el titriyor, eski Android** | Otomatik fener önerisi ve dokunarak odaklama. Düşük uçlu cihazlarda cihaz-içi ML Kit, olmazsa ZXing yedeği. Çekim kalitesi kontrol edilir. | Orta | UI |
| 4.10 | **Rafın tek fotoğrafında çok ürün** (aynı markanın fındıklı ve sade çeşidi yan yana) | Görüntüden ürün tahmini yalnızca **triyaj** içindir. Yüksek güvenle tanınan ve kısıtla çakışan ürün kırmızıya (`Uygun değil`) boyanır. Geri kalan her şey gri kalır: "Tara ve emin ol." Görüntü tanımadan **asla yeşil / `Engel bulunmadı`** çıkmaz. | Kritik | Agent · Kural · UI |
| 4.11 | **Fiyat etiketi farkı** (raf 64,90 · katalog 59,90 · kasada farklı; "2 al 1 öde") | Fiyat kaynağıyla birlikte gösterilir: "raf etiketi, bugün" ya da "fiş, 12 gün önce". Kampanya birim fiyata çevrilir. Bilgi satırı: "Raf ve kasa fiyatı farklıysa tüketici lehine olan uygulanır." (Fiyat Etiketi Yönetmeliği; teyit edilecek) | Orta | UI · Opt |
| 4.12 | **Gıda olmayan barkod** (şampuan, 978 önekli kitap) | "Bu bir gıda ürünü değil gibi görünüyor." Hata sayılmaz. | Düşük | UI |
| 4.13 | **Kamera izni reddedildi** | Sistem ayarına götüren tek bir satır gösterilir. Barkod numarası yazılabilir ya da galeriden fotoğraf seçilebilir. İzin tekrar tekrar istenmez. | Orta | UI |
| 4.14 | **Katalogda kayıt var ama içindekiler eksik** (yalnız alerjen özeti var) | Üyenin kısıtı için kayıtta açık bir "içermez" bilgisi yoksa hüküm `Doğrulanamadı`. "İçerebilir" beyanı `Dikkat` üretir. Bu beyanın yokluğu kanıt sayılmaz. | Kritik | Kural |
| 4.15 | **Olumsuzlama ve Türkçe metin** ("fındık içermez", "glutensiz", büyük harfle "FINDIK", "peynir altı suyu tozu (süt)", "E322 (soya lesitini)", "irmik", "malt") | Normalizasyon Türkçe locale ile yapılır (İ/ı). Türev içerik sözlüğü ve olumsuzlama kalıpları kullanılır. "İçermez" beyanı `Engel bulunmadı` için tek başına yetmez; içindekiler de kontrol edilir. Bunlar her kural sürümünde koşan test setinin parçasıdır (bkz. X.1). | Kritik | Kural |
| 4.16 | **Görme engeli / renk körlüğü** | Hüküm yalnız renkle verilmez: ikon, metin ve her durum için farklı titreşim deseni kullanılır. Ekran okuyucu önce hükmü okur: "Ela için uygun değil: fındık." Butonlar tek elle ulaşılabilir alt yarıdadır. | Yüksek | UI |
| 4.17 | **Hane dışından biri için tarama** ("arkadaşımın çocuğu için") | "Geçici kontrol" açılır: kısıt çipi seçilir, kaydedilmez, oturum sonunda silinir. Hükmü aynı motor verir. | Orta | UI · Kural |
| 4.18 | **Üyeler arasında farklı hükümler** (Ela `Uygun değil`, Murat `Engel bulunmadı`) | Şerit üye bazlıdır. Özet satırında en katı hüküm üstte durur: "1 kişi için uygun değil." Listeye eklenirse "yalnız Murat için" notu düşülür. | Orta | UI |

---

## 5. Fiş, e-Arşiv ve buzdolabı fotoğrafıyla öğrenme

**Aktörler:** alışverişi yapan üye; fişi yükleyen herhangi bir üye.

### Happy path
1. Tara > Fiş seçilir ya da e-Arşiv PDF/XML'i sistemin "Paylaş" menüsüyle gönderilir.
2. Cihazda kalite kontrolü yapılır: bulanıklık, kırpma, uzun fişte parçaların birleştirilmesi.
3. Türkiye'deki sunucuda kişisel veri **redaksiyonu** yapılır (kart, TCKN, telefon, ad, adres). Vision modeline yalnızca redakte görüntü gider.
4. Satırlar çıkarılır. Aritmetik ve KDV denetimi kodda yapılır. Fiş anahtarının hash'iyle mükerrer kontrolü yapılır.
5. Eşleştirme sırası: zincir sözlüğü → aday listesi → emin olunamayan satırlar için "Bu mu?" kartı (en fazla 3 tane).
6. Sonuç: kiler güncellenir, kimliksiz fiyat gözlemleri kaydedilir, plan-gerçek özeti ve tek bir içgörü gösterilir.
7. Ham görsel çıkarımdan sonra silinir.
8. **Buzdolabı fotoğrafında:** "Gördüklerim" listesi güven rozetleriyle çıkar. Kullanıcı onaylar, kiler güncellenir ve "Bu akşam için 3 tarif" gelir.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 5.1 | **Bulanık ya da solmuş termal fiş** | Cihazda kalite skoru hesaplanır. Eşiğin altındaysa: "Biraz bulanık, bir daha çekelim mi?" Yine düşükse yalnız okunabilen satırlar alınır: "4 satır okunamadı." Toplamı tutturmak için satır **uydurulmaz** (vision modellerinin bilinen eğilimi). | Yüksek | Agent · UI |
| 5.2 | **60 cm'lik uzun fiş** | Rehberli parça parça çekim yapılır (üst, orta, alt). Parçalar örtüşmeden birleştirilir. | Orta | UI · Agent |
| 5.3 | **İade/iptal satırı** ("İPTAL", eksi tutar) | Eşleşen pozitif satırla birlikte nötrlenir. Kilere girmez, fiyat gözlemi üretmez. | Orta | Agent · Kural |
| 5.4 | **İndirim satırları** (satır indirimi, "2. ürün %50", sepet sonunda Money/puan) | Standart fiyat, satır indirimi düşülmüş birim fiyattır. Sepet düzeyindeki indirim ayrı alanda tutulur ve fiyat endeksine girmez. Bütçe gerçekte ödenen tutarla hesaplanır. | Orta | Altyapı · Opt |
| 5.5 | **Başkasının fişi** (arkadaşın, yerde bulunan, iş yemeği) | Güvenilir biçimde tespit edilemez. Sinyaller: hanenin alışılmış il ve zinciri dışında olması, hane profiliyle uyumsuzluk. Sinyal varsa sorulur: "Bu alışveriş hanene mi ait?" [Evet] [Hayır, yalnız fiyat için kullan] [Sil]. Başkasının kişisel verisi zaten redaksiyonla atılır. | Orta | Agent · UI |
| 5.6 | **Çok eski fiş** (3 aydan eski) | Fiyat gözlemi yükleme tarihine değil **fiş tarihine** yazılır. Kilere otomatik eklenmez: "Muhtemelen tüketildi. Kilere ekleyeyim mi?" Plan-gerçek karşılaştırması ilgili geçmiş haftaya işlenir. | Orta | Altyapı |
| 5.7 | **Sahte ya da düzenlenmiş fiş** (fiyat zehirleme amaçlı) | Kontroller: aritmetik ve KDV tutarlılığı, cihaz sicil no ile mağaza tutarlılığı, MAD ile aykırı değer, hesap yaşı ve itibarı, oran sınırı. Şüpheli fiş hanenin kendi kullanımında kalır ama topluluk fiyatına girmez. Bir fiyat hücresi en az 3 katkıcı olmadan yayımlanmaz. | Yüksek | Admin · Altyapı |
| 5.8 | **Fişte kişisel veri** (maskeli kart, sadakat kartı telefonu, e-Arşiv'de TCKN ve ad-adres, online siparişte teslimat adresi) | Türkiye'deki sunucuda, vision modelinden **önce** regex ve görsel bölge redaksiyonu yapılır. Ham görsel silinir; redakte sürüm tutulacaksa en fazla 30 gün tutulur. Fiş başkasına ait olsa da aynı kural uygulanır. | Kritik | Altyapı · Agent |
| 5.9 | **Mükerrer yükleme** (aynı fiş iki kez; Selin fotoğrafını, Murat e-Arşiv PDF'ini yüklüyor) | Fiş anahtarının hash'i karşılaştırılır (sicil no + Z no + fiş no + tarih). Farklı formatlar arasında zincir + tarih (± birkaç dakika) + toplam eşleşmesine bakılır. "Bu fişi Selin 2 saat önce eklemiş. Yine de ekleyeyim mi?" | Orta | Altyapı |
| 5.10 | **Online siparişte ikame ürün** (Migros Sanal ya da Getir'de "X yerine Y gönderildi") | Faturadaki satırlar siparişle karşılaştırılır ve yeni ürün kural motorundan geçer. Hüküm katılaşıyorsa P0 bildirimi: "Siparişinde bir ürün değiştirilmiş. Yeni ürün Ela için uygun değil. Bak →" | Kritik | Kural · Altyapı |
| 5.11 | **e-Arşiv yalnız görüntü PDF'i, şifreli PDF ya da XML (UBL-TR)** | XML varsa satırlar doğrudan okunur (`InvoiceLine/Item/Name`). Görüntü PDF'inde vision kullanılır. Şifreli PDF için: "Şifresini açıp tekrar paylaşır mısın?" Alıcının TCKN'si redakte edilir. | Orta | Agent |
| 5.12 | **Gıda dışı satırlar** (deterjan, poşet) | KDV oranı ve sözlükle ayrılır, beslenme hesabına girmez. Varsayılan olarak gıda bütçesine de sayılmaz; kullanıcı bunu değiştirebilir. | Düşük | Kural · Opt |
| 5.13 | **Tartılı ürün** (0,742 kg × 89,90) **ya da adet belirsiz** | Kilogram ve birim fiyat ayrıştırılır. Adet yoksa paket boyu varsayılır ve "≈" ile gösterilir. | Orta | Agent |
| 5.14 | **Buzdolabı fotoğrafı: kapalı kaplar, arka sıra, ev yemeği** | "Gördüklerim" listesi güven rozetleriyle çıkar. "Kaplardakini göremiyorum, eklemek ister misin?" Fotoğraftan alerjen hükmü verilmez. Tarifler yalnız onaylanan kalemlerle üretilir. | Yüksek | Agent · UI |
| 5.15 | **Buzdolabı fotoğrafında yüz, aile fotoğrafı ya da telefon numarası yazılı not** | Fotoğraf cihazda yalnız raf bölgesine kırpılır ya da yüzler bulanıklaştırılır. LLM'e redaksiyondan önce hiçbir şey gitmez. Ham görsel saklanmaz. | Yüksek | Altyapı · Agent |
| 5.16 | **Eşleştirme soğuk başlangıcı** (20 satırın 12'si belirsiz) | En fazla 3 "Bu mu?" kartı gösterilir; gerisi kategori düzeyinde tutulur ("süt ürünü"). Kullanıcı yorulmaz. Ekip kendi fişleriyle sözlüğü önceden tohumlar. | Yüksek | Agent · Admin |
| 5.17 | **Hane hiç fiş yüklemiyor** | Ürün fişsiz de tam çalışır (girdi sırası: liste > barkod > fiş). "Plan-gerçek" yerine "planlandığı gibi" varsayımı ve kapsama yüzdesi gösterilir. | Orta | UI · Opt |

---

## 6. Kiler ve son kullanma

**Aktörler:** hane üyeleri; ev arkadaşı hanesinde her kişi.

### Happy path
1. Kalemler kaynaklarıyla birlikte kilere girer: fiş, barkod, buzdolabı fotoğrafı, elle giriş, plandan artan.
2. Her kalemde yaklaşık miktar ("≈"), tarih ve açılış durumu tutulur. Tarih etiketten okunur; okunamazsa kategori varsayılanı "tahmini" etiketiyle kullanılır. SKT ve TETT ayrı tutulur.
3. "Bitmek üzere" tahmini listeye öneri olarak düşer.
4. Plan "önce evdekini kullan" ilkesiyle kiler kalemlerini önceliklendirir.
5. Tüketim iki yoldan düşülür: "pişirildi" işaretlenince plan malzemeleri düşer ya da sonraki fişten çıkarım yapılır.
6. Haftada bir kısa "kiler turu" yapılır: 3 kalem teyidi.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 6.1 | **Yanlış miktar** (fişte 2 yazıyor, 1 alınmış; kg ile adet karışmış) | Satırda tek dokunuşla düzeltilir. Düzeltme ilgili fiyat gözlemini de düzeltir. | Orta | UI |
| 6.2 | **Tüketilmiş ama işaretlenmemiş** | Her kalemin güveni kategori ömrüne göre zamanla azalır. Güveni düşük kalem planda kullanılmadan önce teyit sorulur. Aynı ürünün yeni fişi gelirse önceki stok "muhtemelen bitti" sayılır. | Yüksek | Opt · Altyapı |
| 6.3 | **SKT gelmeden bozulan ürün** (küf) | "Bozuldu" işaretlenince kilerden düşer. İsraf istatistiği yargısız verilir: "Bu ay 2 ürün bozuldu, ≈ 85 TL." O hanede bu kategorinin varsayılan ömrü kısalır. Tariflerde kullanılmaz. "Küflü kısmı kesip kullan" gibi gıda güvenliği tavsiyesi verilmez. | Yüksek | UI · Opt |
| 6.4 | **SKT ile TETT karışıklığı** (son tüketim tarihi / tavsiye edilen tüketim tarihi) | SKT'si geçmiş kalem hiçbir tarife ya da plana girmez, gri olarak "Son tüketim tarihi geçti" yazar. TETT'si geçmiş kalemde yalnız bilgi verilir: "Tavsiye edilen tarih geçti." Tüketip tüketmeme konusunda tavsiye verilmez. | Kritik | Kural · UI |
| 6.5 | **Açılmış paket** ("açıldıktan sonra 3 gün içinde tüketin") | Açılış tarihi bilinmez. Plan kalemi kullanacağı zaman "Açık mı?" diye sorar. Ambalajdaki "açıldıktan sonra X gün" bilgisi etiketten okunursa uygulanır. | Orta | UI · Kural |
| 6.6 | **Tahmini tarih kesin gibi algılanıyor** | "≈" ve "tahmini" rozeti kullanılır. Bildirim de kesin tarih vermez: "Ispanağı bu hafta kullanmak iyi olur." | Orta | UI |
| 6.7 | **Paylaşılan kiler** (ev arkadaşları, "benim yoğurdum") | Kalemde isteğe bağlı sahip etiketi tutulur. Ev arkadaşı hanesinde plan başkasının kalemini kullanmaz. Aile hanesinde kiler ortaktır. | Orta | Opt · UI |
| 6.8 | **Kilerde bir üyeye uygun olmayan ürün var** (misafir ikramlığı, Murat'ın fındıklı gofreti) | Kiler görünümünde üye hükmü gösterilir. "Ela için ne pişirsem" önerileri bu kalemleri dışarıda bırakır. Suçlayıcı dil kullanılmaz. | Kritik | Kural · Opt |
| 6.9 | **Kiler kaleminin hükmü sonradan değişti** (tarif radarı, katalog düzeltmesi, yeni kısıt) | Kalem işaretlenir ve hüküm katılaştıysa P0 bildirimi gider (bkz. 7.4, 10.1). | Kritik | Kural · Altyapı |
| 6.10 | **Toplu stok** (enflasyon nedeniyle 10 kg un, 15 kg kurban eti) | Büyük miktar ve dondurucu alanı desteklenir. Dondurucu kalemlerinde "bitmek üzere" tahmini yapılmaz. Plan çeşitliliği korur, her gün et zorlamaz. | Orta | Opt |
| 6.11 | **Geri çağırma / resmî liste eşleşmesi** (parti numarası bilinmiyor) | Admin onayından sonra "olası eşleşme" diliyle ve kaynak linkiyle bildirilir. Kesin hüküm verilmez. | Yüksek | Admin · UI |
| 6.12 | **Kiler hiç girilmemiş ya da terk edilmiş** | Özellik sessizce kapanmaz; durum söylenir: "Kilerin 3 haftadır güncellenmedi. Plan yaparken evdekileri hesaba katmıyorum." Kiler opsiyoneldir. | Orta | UI · Opt |
| 6.13 | **İki ev** (yazlık, çocuğun ikinci evi) | Kiler hane başına tutulur. Kalemler "Yazlığa götürdüm" toplu aksiyonuyla taşınır. | Düşük | UI |

---

## 7. Bildirimler ve proaktif asistan

**Öncelik sınıfları**
- **P0 Güvenlik:** kısıt ihlaline dönüşen tarif değişikliği, ikame ürün, hatalı hükmün düzeltilmesi, geri çağırmada olası eşleşme.
- **P1 Plan:** Pazar planı, eksik liste.
- **P2 İçgörü:** haftalık özet, fiyat değişimi.
- **P3 Hatırlatma:** tarih, fiş.

### Happy path
1. P1–P3 bildirimlerinin toplamı **haftada en fazla 3**'tür ve kullanıcı bu sınırı değiştirebilir. P0 bu bütçeye dahil değildir.
2. Zamanlama hanenin öğrenilmiş ritmine göre yapılır. Sessiz saatler varsayılan olarak 22:00–08:00'dir.
3. Push içeriğinde sağlık verisi olmaz; ayrıntı uygulama açılınca sunucudan çekilir.
4. Her bildirim tek aksiyonludur ve en fazla ≈ 90 karakterdir.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 7.1 | **Bildirim yorgunluğu** | Bir sınıf üç kez üst üste görmezden gelinirse otomatik seyrekleşir ve bu kullanıcıya söylenir: "Fiyat bildirimlerini ayda bire indirdim. Geri açmak için →" Haftalık tek özet seçeneği de sunulur. | Yüksek | Altyapı · UI |
| 7.2 | **Yanlış zaman** (iftar, okula hazırlık saati, gece vardiyası) | Kullanıcının etkileşim saatleri öğrenilir. Ramazan modunda iftar ±1 saat ve sahur susturulur. Saat dilimi cihazdan alınır. | Orta | Altyapı |
| 7.3 | **Sessiz saatlerde P0** | P0 gece 03:00'te push ile uyandırmaz. Sessiz saat bitince ilk sırada gönderilir ve uygulama açılınca, onaylanana kadar kapatılamayan bir banner olarak durur. Kullanıcı "Güvenlik uyarıları her zaman" seçtiyse istisna uygulanır. *(Açık soru: hangi P0 gece de gönderilmeli?)* | Kritik | Altyapı · UI |
| 7.4 | **Yanlış pozitif tarif değişikliği uyarısı** (OCR "fındık içermez"i "fındık" okudu; "aynı tesiste fındık işlenmektedir" ifadesi `Uygun değil` sanıldı) | P0 **yalnız moderasyonun onayladığı** katalog değişikliğiyle tetiklenir, tek bir kullanıcının OCR'ıyla tetiklenmez. Uyarı hatalı çıkarsa düzeltme gider: "Dün X için gönderdiğimiz uyarı hatalıydı; ürün önceki durumuna döndü. Özür dileriz." | Yüksek | Admin · Kural |
| 7.5 | **Yanlış negatif** (tarif değişti ama yakalanmadı) | Tarif radarı katalogdaki kayıtları yaşına göre periyodik yeniden doğrulamaya sokar; en çok kilerde bulunan ürünler önce gelir. Kullanıcının etiket fotoğrafındaki fark da tetikleyici olur. | Kritik | Admin · Altyapı |
| 7.6 | **Kilit ekranında sağlık verisi** ("Ela'nın fındık alerjisi için…") | Push metni jeneriktir: "Kilerindeki bir ürünle ilgili önemli bir güncelleme var." Üye adı ve kısıt push'ta asla birlikte yer almaz. APNs/FCM (yurt dışı) payload'ında kişisel veri bulunmaz; içerik uygulama açılınca Türkiye'deki sunucudan çekilir. | Kritik | Altyapı |
| 7.7 | **P0 hane içinde kime gidecek** | Çocuğun kısıtıyla ilgili P0 velilere gider; izin verilmişse yardımcılara da. Yetişkinin kendi kısıtıyla ilgili P0 yalnız ona gider (paylaşım ayarı açıksa haneye de). Biri onayladığında diğerlerinde "Selin gördü" yazar ve bildirim sessizleşir. | Yüksek | Altyapı |
| 7.8 | **Bildirim izni yok** | Uygulama içi gelen kutusu kullanılır ve P0 açılışta banner olarak çıkar. E-posta yalnız P0 için, jenerik metinle ve ayar açıksa gönderilir. | Yüksek | UI · Altyapı |
| 7.9 | **Proaktif asistan yanlış bağlamda** ("Pazar planın hazır" ama aile tatilde, hastanede ya da yasta) | "Bu hafta ara ver" tek dokunuştur (1–4 hafta), neden sorulmaz. Tatil ihtimali (fiş yok + plan reddi) yalnızca soru olarak sorulur, varsayılmaz. | Orta | Agent · UI |
| 7.10 | **Suçluluk ya da şantaj dili** | Bildirim metinleri onaylı şablon kütüphanesinden gelir. LLM'in ürettiği metin yasaklı kelime filtresinden geçer. "Kaçırdın" ya da "başarısız" gibi ifadeler yoktur. | Orta | Agent · Admin |
| 7.11 | **Birden fazla cihaz / birden fazla hane** | Bir cihazda okunan bildirim diğerlerinden de temizlenir. Başlıkta hane adı yazar. | Düşük | Altyapı |
| 7.12 | **Bildirime tıklandığında içerik değişmiş** (ürün kaydı düzeltilmiş) | "Bu uyarı güncellendi" ara ekranı çıkar ve eski hükümle yeni hüküm yan yana gösterilir. | Orta | UI |
| 7.13 | **Fiş hatırlatması hane içi suçlamaya dönüşüyor** | Yalnız hane düzeyinde ilerleme gösterilir: "Bu haftanın fişleri: 4/5." Kimin eksik olduğu gösterilmez. | Orta | UI |
| 7.14 | **Acil uyarı önceliği:** aynı anda P0, P1 ve P2 var | Önce P0 gider. Diğerleri tek bir özette birleştirilir ya da ertelenir. P0 açılmadan içgörü bildirimi gönderilmez. | Yüksek | Altyapı |

---

## 8. Hesap, gizlilik ve KVKK talepleri

**Aktörler:** her üye, veli, hane yöneticisi, Admin'deki KVKK sorumlusu.

### Happy path
1. **Rıza listesi.** Hane > Gizlilik ekranında amaç bazlı rızalar tarih ve sürümleriyle görünür; her biri geri alınabilir.
2. **Geri alma.** Önce "Neler değişir" önizlemesi gösterilir, kullanıcı onaylar, işlem uygulanır ve makbuz verilir.
3. **Veri indirme.** İki format hazırlanır: JSON (makine okunur) ve okunur PDF/HTML. Hazır olunca uygulama içi bildirim gelir. Yasal süre 30 gündür (KVKK m.13), hedef ise dakikalardır.
4. **Hesap silme.** Önizlemede hane, çocuk profilleri ve katkılara ne olacağı gösterilir. Geri alma penceresi (ör. 14 gün; açık soru) sonunda kalıcı silme yapılır ve makbuz verilir.
5. **m.11 başvurusu.** Uygulama içi form ya da e-posta ile yapılır, Admin'deki KVKK kuyruğuna düşer. SLA 30 gündür.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 8.1 | **Sağlık rızası geri alındı: ne çalışmaya devam eder** | **Çalışanlar:** liste, bütçe planı, tarama (genel mod), fiş, kiler. **Kapananlar:** kişisel hüküm şeridi, kısıtlı plan, tarif radarı, "sağlığın fiyatı". Mevcut plan korunur ama kısıt rozetleri kalkar ve "Bu plan artık kısıt kontrolünden geçmiyor" etiketi eklenir. Kısıt verisi silinir. Tüm bunlar geri almadan **önce** tek ekranda gösterilir. | Kritik | Altyapı · Kural · UI |
| 8.2 | **Silme talebi ile değişmez karar kaydı/audit çatışıyor** | DR ve audit içindeki sağlık verisi kişi başına ayrı anahtarla şifrelenir. Silmede anahtar imha edilir (kripto-silme): kaydın yapısı ve sayaçlar kalır, içerik okunamaz. Audit'e yalnız içeriksiz bir "silme yapıldı" olayı düşer. Yedeklerden rotasyonla düşer (ör. 35 gün) ve bu süre aydınlatma metninde yazar. | Kritik | Altyapı · Admin |
| 8.3 | **Topluluk katkıları** (etiket fotoğrafı, OFF'a giden içerik, fiyat gözlemi) | Katkı anında açıkça söylenir: "Katkın anonim olarak kataloğa ve Open Food Facts'e eklenir; hesabını silsen de kalır." Hesapla bağ koparılır. Kişisel iz içeren fotoğraf katkı olarak kabul edilmez. | Yüksek | Admin · UI |
| 8.4 | **Hane yöneticisi ayrılıyor** (boşanma, taşınma) | Hanede başka yetişkin varsa ayrılmadan önce yöneticiliği devretmesi zorunludur. Kişisel kısıtlar kişiyle gider; liste, kiler ve fişler hanede kalır. Ayrılan kişi kendi yüklediği fişler için seçim yapar: götür, sil ya da anonim "eski üye" olarak hanede bırak. Çocuk profili ortak veliliyse kalır. Ortak veli yoksa ayrılan veliyle gider ve kalan haneye açık uyarı gösterilir: "Ela'nın kısıtları artık bu hanenin planında yok." | Kritik | Altyapı · UI |
| 8.5 | **Çocuk 18 yaşına giriyor** | Veli rızasının dayanağı sona erer (yorum). 18'e 30 gün kala veliye ve (hesabı varsa) gence bildirim gider. 18'de profil "yetişkin, kendi onayı bekleniyor" durumuna geçer. 30 günlük geçiş süresinde genç kendi hesabıyla onay vermezse kısıtlar silinir. Veliye bilgi verilir: "Can artık kendi profilini yönetiyor." Doğum yılı ve ayı tutulmuyorsa veliye yılda bir sorulur. | Yüksek | Altyapı · UI |
| 8.6 | **Ölüm / hesap devri** | Hesap devri yapılmaz (kişisel veri devredilmez). Hanedeki diğer yetişkin yöneticilik talep eder; talep 14 günlük itiraz penceresinden sonra kabul edilir. Vefat eden kişinin kısıtları, hane ya da mirasçı talebiyle silinir. Vefat eden tek veliyse çocuk profili için diğer veliden yeni rıza alınır. Ton sade ve taziyelidir, bürokratik dil kullanılmaz. | Yüksek | Admin · Altyapı |
| 8.7 | **Veri indirme formatı ve kapsamı** | JSON şemalıdır ve sürüm taşır; yanında okunur bir PDF gelir. İçerik: profil, kısıt geçmişi, rıza kayıtları, listeler, fiş satırları, DR'lerin insan cümlesi hâli. Başka yetişkinlerin kısıtları dahil edilmez; onlar yalnız "hane üyesi 2" olarak görünür. Çocuğun verisi veliye verilir. İndirme linki tek kullanımlıktır, 24 saat geçerlidir ve uygulama içinde açılır; e-posta eki olarak gönderilmez. | Yüksek | Altyapı |
| 8.8 | **Başvuran gerçekten o kişi mi?** | Uygulama içi talep oturumla doğrulanır. E-posta başvurusu hesap e-postasıyla eşleştirilir ve uygulama içinden onay istenir. TCKN istenmez. | Orta | Admin |
| 8.9 | **Hesap ele geçirme** (SIM swap, çalınan telefon) | Yeni cihazdan giriş olunca diğer cihazlara bildirim gider. Oturum listesi ve uzaktan çıkış var. Çevrimdışı önbellek cihaz anahtarlığıyla şifrelidir ve oturum iptal edilince silinir. Paylaşım, silme ve yönetici devri gibi hassas işlemlerde yeniden kimlik doğrulama istenir. | Kritik | Altyapı |
| 8.10 | **Rıza metninin sürümü değişti** | Etkilenen amaç için yeniden rıza istenir. Rıza verilene kadar o amaç eski ve daha dar kapsamla çalışır. Kapsam genişliyorsa sessiz geçiş yapılmaz. | Yüksek | Altyapı · UI |
| 8.11 | **Hane içi görünürlük** (Murat, şeker hedefinin hanede nedeniyle birlikte görünmesini istemiyor) | Üye ayarı: "Hanede yalnız hüküm görünsün." Şeritte "Murat için Dikkat · kişisel tercih" yazar; nedeni yalnız Murat görür. | Yüksek | UI · Kural |
| 8.12 | **Uygulama silindi ama hesap duruyor** | Hesap ve veri kalır. 12 ay hareketsizlikten sonra "hesabın silinecek" e-postası gider; saklama süresi dolunca veri imha edilir. Süre aydınlatma metninde yazar. | Orta | Altyapı |
| 8.13 | **Veri ihlali** | 72 saat içinde Kurul'a bildirim planı hazırdır. Kullanıcılara uygulama içinden ve e-postayla ne sızdığı ve ne yapmaları gerektiği bildirilir; şablon önceden yazılıdır. | Kritik | Admin · Altyapı |
| 8.14 | **Yalnız analitik rızası reddedildi** | Ürün tamamen çalışır. Analitik yalnız rızayla, kimliksiz ve Türkiye'de işlenir. | Orta | Altyapı |

---

## 9. Web Planlama Stüdyosu ve paylaşım

**Aktörler:** iki ebeveyn (aynı anda), diyetisyen (misafir, salt okunur), ortak bilgisayar kullanan kişi.

### Happy path
1. Web'e telefondan QR ile (şifresiz) ya da Apple/Google ile girilir.
2. Stüdyoda bu haftanın planı, liste, kısıt çipleri, bütçe kaydırıcısı, sağlığın fiyatı ve market bölme görünür.
3. Web'deki değişiklikler mobile canlı yansır ("Liste telefonunda").
4. **Diyetisyen paylaşımı:** kapsam seçilir (hangi üye, hangi dönem, hangi metrikler) → süre seçilir (7/14/30 gün) → link oluşur, 6 haneli erişim kodu ayrı kanaldan gider → erişim logu tutulur → kullanıcı istediği an iptal edebilir.
5. WhatsApp'a gönder / yazdır: liste metni sağlık nedeni içermez.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 9.1 | **Diyetisyen linkinin süresi doldu** | Link açılınca: "Bu paylaşımın süresi doldu; paylaşan kişiden yenisini isteyebilirsin." Paylaşanın kim olduğu söylenmez. Paylaşana 2 gün önce "Uzatayım mı?" diye sorulur; uzatma yeni bir onaydır. | Orta | Altyapı · UI |
| 9.2 | **Link sızdı** (grupta paylaşıldı, e-posta iletildi) | Link tek başına yetmez; ayrı kanaldan gelen erişim kodu gerekir. İlk açan cihaz linke bağlanır, başka cihaz yeni kod ister. Erişim logu paylaşana görünür: "3 farklı cihazdan açılma denemesi." Tek dokunuşla iptal edilir. Sayfa arama motorlarına kapalıdır (noindex), ekranda filigran vardır, ad yerine takma ad kullanılır. Çocuğun verisi varsayılan olarak dışarıdadır. | Kritik | Altyapı · UI |
| 9.3 | **Diyetisyene paylaşım, sağlık verisinin üçüncü kişiye aktarımıdır** | Paylaşım anında ayrı bir açık rıza ekranı gelir: kim görecek, ne görecek, ne kadar süre. Başka bir yetişkinin verisi ancak o yetişkinin kendi onayıyla eklenir. | Kritik | UI · Altyapı |
| 9.4 | **İki ebeveyn listeyi aynı anda düzenliyor** | Kalem düzeyinde CRDT ya da işlem günlüğü kullanılır. Aynı kalemde çakışma olursa son değişiklik uygulanır ama geri alınabilir: "Murat miktarı 2 yaptı, sen sildin. Geri alayım mı?" Silinen kalem 7 gün "Son silinenler"de durur. | Yüksek | Altyapı · UI |
| 9.5 | **Biri planı onaylarken diğeri listeyi değiştirdi** | Plan belirli bir liste sürümüne bağlıdır. Sürüm değişmişse onay butonu şuna dönüşür: "Liste değişti, planı yeniden hesaplayayım mı?" | Yüksek | Opt · Altyapı |
| 9.6 | **Bir veli yeni hard kısıt ekledi; diğerinin ekranında eski plan açık** | Sunucu profil sürümünü artırır ve açık tüm istemcilere geçersizleme olayı gönderir. Eski sürümle gelen "onayla" isteği sunucuda reddedilir. Ekranda: "Ela'nın kısıtları güncellendi; 2 yemek artık uygun değil." | Kritik | Altyapı · Kural |
| 9.7 | **Ortak bilgisayar** (iş yeri, kütüphane) | "Bu cihazı hatırla" varsayılan olarak kapalıdır. 30 dakika hareketsizlikte oturum kapanır. Tek tıkla "ekran paylaşımı modu" açılır: adlar ve kısıt nedenleri maskelenir. | Yüksek | UI · Altyapı |
| 9.8 | **Diyetisyenle Zoom'da ekran paylaşımı** | Sunum modunda yalnız paylaşım kapsamındaki veri görünür. | Orta | UI |
| 9.9 | **Listeyi WhatsApp'a gönderme ya da yazdırma** | Metinde yalnız ürün ve miktar olur; "Ela için" gibi sağlık nedenleri yer almaz. Kullanıcı bunu uyarıyla açabilir. | Yüksek | UI |
| 9.10 | **Pareto / sağlığın fiyatı grafiği ekran okuyucuda** | Grafiğin tablo alternatifi vardır ve noktalar arasında klavyeyle gezinilebilir. | Orta | UI |
| 9.11 | **Stüdyo mobil tarayıcıdan açıldı** | "Masaüstünde daha rahat" bilgisi gösterilir; temel işlevler yine çalışır. | Düşük | UI |
| 9.12 | **Çevrimdışı çatışma** (telefon bodrumda kalemi "alındı" yaptı, bu arada web'de aynı kalem silindi) | Bağlantı gelince birleştirme kuralı uygulanır: fiziksel gerçek öncelikli olduğu için "alındı" silmeye üstün gelir. Kullanıcıya birleştirme özeti gösterilir. | Orta | Altyapı |
| 9.13 | **Diyetisyen düzenleme yapmak istiyor** | Görünüm salt okunurdur. Diyetisyene hesap açtırılmaz. Not bırakma özelliği ileride düşünülebilir (C önceliği). | Düşük | UI |

---

## 10. Admin ve moderasyon

**Aktörler:** moderatör, destek, KVKK sorumlusu, geliştirici (rolleri ayrı).

### Happy path
1. Katkı (ör. etiket fotoğrafı) gelir → OCR → mevcut kayıtla diff alınır (alerjen alanları vurgulu) → injection ve kalite taraması yapılır.
2. Moderatör fotoğrafı ve çıkarımı yan yana görür, alan alan onaylar ve gerekçe yazar.
3. Alerjeni kaldıran (gevşeten) değişiklik ikinci bir onay ister (4 göz ilkesi).
4. Yayında katalog sürümü artar. Etki analizi yapılır: ürün kaç hanenin kilerinde ya da listesinde? Hükmü katılaşan hanelere P0 gider.
5. Her adım audit'e yazılır: kim, ne, ne zaman, önce-sonra, gerekçe. Audit silinemez.
6. Karar izi araması: scanId ile aranır, sonuç takma adlı olarak hem insan cümlesi hem ham kayıt şeklinde görünür.

### Edge case'ler
| # | Durum | Ürünün tepkisi (ekran · metin) | Önem | Katman |
|---|---|---|---|---|
| 10.1 | **Yanlış onay** (moderatör "fındık yok"u onayladı, üründe fındık var) | Geri alma yeni bir sürüm olarak yapılır, eski sürüm silinmez. DR'ler üzerinden bu sürümü kullanan tüm hükümler bulunur. Ürünü kilerinde, listesinde ya da son 30 günlük taramasında bulunduran hanelere düzeltme P0'ı gider: "Daha önce X için 'Engel bulunmadı' göstermiştik; hatalıydı. Ela için uygun değil." Moderatöre geri bildirim verilir, kök neden kaydedilir. | Kritik | Admin · Altyapı |
| 10.2 | **Kötü niyetli katkıcı** (yanlış içerik, rakip markayı karalama, trol) | Yeni hesapların katkıları gölge kuyruğa düşer. İtibar puanı ve oran sınırı uygulanır. Onaylanmamış katkı başka hiçbir kullanıcıya görünmez. Tek tıkla "bu hesabın tüm katkılarını geri al" yapılabilir ve bu da audit'e yazılır. | Yüksek | Admin |
| 10.3 | **Toplu veri zehirleme** (koordineli hesaplar, sahte fiyatlar, aynı cihaz parmak izi) | Anomali panosu hesap yaşı, patlama ve coğrafya sinyallerini izler. Fiyat hücrelerinde k≥3 katkıcı ve MAD kontrolü var. Karantina modu şüpheli zaman penceresindeki katkıları topluca askıya alır. Geri alma sonrası etkilenen hesaplar yeniden yapılır. | Yüksek | Admin · Altyapı |
| 10.4 | **Kural değişikliğinin geçmiş kararlara etkisi** (v1.3 → v1.4; ör. yulaf çölyakta `Dikkat` olacak) | Yayından önce iki şey zorunludur: altın test setinin geçmesi ve bir etki raporu ("312 ürünün hükmü değişir: 40'ı katılaşır, 3'ü gevşer"). Gevşeten değişiklik 2 onay ister. Geçmiş DR'ler değişmez ve eski sürümle yeniden üretilebilir. Canlı nesneler (kiler, liste, plan) yeniden değerlendirilir. Bildirim yalnızca hükmü katılaşan **ve** kilerde ya da listede bulunan ürünler için gider. | Kritik | Admin · Kural |
| 10.5 | **Destek erişimi** (kullanıcı "neden uygun değil dedi" diye yazdı) | Varsayılan görünüm takma adlıdır (`ÜYE_2`, `KISIT_7`). Gerçek değeri görmek için break-glass gerekir: gerekçe, talep numarası, 60 dakika süre. Kullanıcı bunu görür: "Destek ekibi #123 numaralı talebin için karar kaydına baktı." "Kullanıcı yerine giriş" yapılamaz. | Kritik | Admin · Altyapı |
| 10.6 | **Admin hesabının ele geçirilmesi / iç tehdit** | 2FA zorunludur (donanım anahtarı tercih edilir). Roller ayrıdır: moderatör, destek, KVKK sorumlusu, geliştirici. En az yetki ilkesi ve IP kısıtı uygulanır. Toplu dışa aktarım yoktur. Audit yalnız eklemeye açıktır (append-only). | Kritik | Altyapı |
| 10.7 | **Moderasyon kuyruğu tıkandı** (3 kişilik ekip) | Önceliklendirme: alerjenle ilgili katkılar ve etkilenen hane sayısı önce gelir. Bekleyen ürün kullanıcıya dürüstçe `Doğrulanamadı` olarak görünür. SLA panosu vardır. | Yüksek | Admin |
| 10.8 | **OFF'taki kaynak veri değişti** (upstream düzenleme) | OFF katmanı ayrı ve değiştirilmeden tutulur; doğrulanmış katman önceliklidir. OFF'taki değişiklik otomatik uygulanmaz, diff olarak kuyruğa düşer. | Orta | Admin · Altyapı |
| 10.9 | **Resmî liste içe aktarma** (geri çağırma, taklit/tağşiş) | Bulanık eşleşmeler Admin onayından geçer. Kullanıcı "olası eşleşme" ve kaynak linki görür. Marka itibarı nedeniyle kesin dil kullanılmaz. | Yüksek | Admin |
| 10.10 | **Marka ya da üretici itirazı** ("içerik bilginiz yanlış") | İtiraz formu vardır ve etiket kanıtıyla incelenir. Düzeltme ya da ret gerekçeli olur ve audit'e yazılır. Üreticinin gönderdiği bilgi de katkı gibi moderasyondan geçer. | Orta | Admin |
| 10.11 | **Sözlük değişikliği** (fiş kısaltması, "gevrek = simit" gibi bölgesel eş anlamlı) | Sözlük sürümlüdür ve değişiklikten önce etki önizlemesi gösterilir. Alerjen taksonomisine dokunan bir sözlük değişikliği kural değişikliği sayılır (bkz. 10.4). | Yüksek | Admin · Kural |
| 10.12 | **LLM modeli sağlayıcı tarafında güncellendi** | Model sürümü sabitlenir. Yükseltmeden önce NL→kısıt ve guardrail eval setleri koşar; eşik "alerjen gevşetme = 0" ve "yasaklı kelime = 0"dır. Geçmezse yayın yapılmaz. | Kritik | Admin · Agent |
| 10.13 | **Ekip üyesi karar izinde merakla sağlık verisine bakıyor** | Her arama audit'e yazılır ve anormal arama örüntüsünde uyarı çıkar. Görünüm takma adlıdır. | Yüksek | Admin |

---

## 11. Çapraz kesen edge case'ler (tüm akışlar)
| # | Durum | Tepki | Önem | Katman |
|---|---|---|---|---|
| X.1 | **Türkçe İ/ı sorunu:** `"FINDIK".toLowerCase()` İngilizce locale'de `"findik"` döner ve sözlükteki "fındık" ile eşleşmez; alerjen kaçar | Kural motorunda sabit Türkçe locale ile normalizasyon (İ→i, I→ı) ve aksan duyarlı eşleştirme yapılır. Büyük harfli etiket metni için test seti tutulur ve her kural sürümünde koşar. | Kritik | Kural |
| X.2 | **Eski istemci, eski kural paketiyle çevrimdışı hüküm veriyor** | Kural paketi sürüm taşır ve bir minimum sürüm vardır. Kritik kural güncellemesinde cihaz önbelleği geçersiz sayılır, gerekirse zorunlu güncelleme ekranı çıkar. | Kritik | Altyapı |
| X.3 | **Cihaz saati yanlış** | SKT, fiş tarihi ve link süreleri sunucu saatiyle hesaplanır. | Orta | Altyapı |
| X.4 | **Mobil veri kotası az, bağlantı yavaş** | Görsel cihazda sıkıştırılır. Fiş yüklemesi Wi-Fi'ye ertelenebilir. | Orta | UI · Altyapı |
| X.5 | **Para ve sayı formatı** (1.850,00 TL; ondalık virgül) | OCR ve giriş Türkçe locale ile yapılır. `12,50` ile `1250` karışmasına karşı aritmetik kontrol uygulanır. | Orta | Agent · Altyapı |
| X.6 | **Mağaza incelemesi** (Apple 1.4.1 ve 5.1.2(i), Google Health declaration) | Uygulama içi bütün metinler yasaklı iddia listesine karşı bir linter'dan geçer. Mağaza açıklaması da aynı listeye tabidir. | Yüksek | Admin · UI |
| X.7 | **Yalnız Türkçe arayüz** | Kapsam dürüstçe söylenir. Arapça konuşan kullanıcılar için karar Levent'te (açık soru). | Orta | — |

---

## 12. En kritik 15 edge case

Seçim ölçütü: (1) fiziksel zarar ya da hukuki ihlal, (2) sessiz başarısızlık (kullanıcı hatayı fark etmez), (3) jürinin "bunu nasıl düşünmediniz" diyeceği alan bilgisi.

| K | Edge case | Neden kritik | Tablodaki yeri | Karşılayan madde |
|---|---|---|---|---|
| K1 | **Bilinmiyor ≠ yok.** Kısıtı girilmemiş, rızası olmayan ya da daveti bekleyen üyeye `Engel bulunmadı` gösterilmesi | Sessiz ve yanıltıcı "yeşil" | 1.1 · 1.4 · 4.18 | S8 |
| K2 | **Alerjen kavram karışıklığı:** fındık / fıstık / Antep / çam fıstığı; süt alerjisi / laktoz; çölyak / gluten hassasiyeti; TGK dışı alerjen | Yanlış kısıtla doğru çalışan motor yine zarar verir | 1.6 · 1.7 | S9 · S12 |
| K3 | **İçerik çözümleme hatası:** Türkçe İ/ı, türev içerik ("peynir altı suyu"), olumsuzlama ("içermez"), LLM tarifindeki bileşik içerik ("pesto", "tahin") | Kural motoru "doğru" çalışırken alerjeni kaçırır | 4.14 · 4.15 · 3.10 · X.1 | S12 |
| K4 | **Akut reaksiyon ve doz/tolerans sorusu** ("biraz yesem?", "dudağım şişti") | Hayati risk ve tıbbi cihaz sınırı | 2.2 · 2.3 · 2.4 | S14 |
| K5 | **LLM'in araç hükmünü bozması:** "güvenli" demesi, çelişen anlatım, prompt injection | Mimari ilkenin ("LLM karar vermez") delinmesi | 2.10 · 2.11 · 2.12 | S13 |
| K6 | **Serbest metin ya da sesle sağlık verisinin yurt dışına çıkması** | KVKK m.9: sistematik aktarıma rıza yetmez | 2.16 · 2.14 | S15 |
| K7 | **Hard kısıtın dolaylı gevşemesi:** olursuzluk önerisi, asistan ("Ela artık yiyebiliyor"), tatil/misafir modu, tek velinin kaldırması | "Alerjen gevşetme = 0" hedefinin arka kapısı | 3.1 · 3.6 · 1.13 · 2.6 | S9 · S10 |
| K8 | **Görsel tanımadan olumlu hüküm** (raf fotoğrafı, buzdolabı; fındıklı ve sade çeşidin ambalajı neredeyse aynı) | Wow özelliği aynı zamanda en riskli özellik | 4.10 · 5.14 | S11 |
| K9 | **Ürün kimliği kayması:** aynı barkodda yeni tarif, ithal sürüm, karışık çoklu paket, dökme ürün, mağaza içi barkod | Doğru ürün sanılan yanlış kayıt | 4.3–4.7 | S11 · S16 |
| K10 | **Online siparişte ikame ürün** | Kullanıcı hiç taramadığı ürünü yer | 5.10 | S17 |
| K11 | **Yanlış moderasyon onayı / toplu zehirleme** ve geçmişte "Engel bulunmadı" görmüş kullanıcılar | Hata düzelir ama zarar görebilecek kişiye ulaşmaz | 10.1–10.3 · 7.4 | S9 · S17 |
| K12 | **Sürüm değişikliği canlı nesnelere yayılmıyor:** yeni kısıt eklendi ama diğer velinin açık planı, çevrimdışı telefon ya da eski istemci eski hükümle çalışıyor | Dağıtık sistemde sessiz tutarsızlık | 3.18 · 4.8 · 9.6 · X.2 | S16 |
| K13 | **İfşa kanalları:** push ve kilit ekranı, sesli yanıt, WhatsApp listesi, diyetisyen linkinin sızması | Çocuğun alerjisi ya da yetişkinin hedefi yanlış göze ulaşır | 7.6 · 2.17 · 9.2 · 9.9 | S18 |
| K14 | **Rıza zinciri:** başkası adına veri girilmesi, iki evde yaşayan çocuk, bakıcı, misafir, hane içi mahremiyet (genç) | Özel nitelikli veride tek hukuki dayanak açık rızadır | 1.3 · 1.13 · 1.14 · 3.2 · 2.15 | S19 |
| K15 | **Veri yaşam döngüsü:** rıza geri alma ve silme ile değişmez DR/audit çatışması; 18 yaş; yöneticinin ayrılması; ölüm | "Silindi" dendiği hâlde veri kalır ya da çocuk korumasız kalır | 8.1 · 8.2 · 8.4–8.6 | S20 |

---

## 13. Ürün sözleşmesine eklenecek maddeler (urun-tanimi §5, 8'den devam)

> Mevcut 7 madde korunur. Aşağıdaki maddeler taslaktır. Her maddenin altında nasıl doğrulanacağı yazılı (property test, eval ya da inceleme).

**S8 — Bilinmiyor, yok değildir.**
Kısıtı girilmemiş, rızası olmayan ya da daveti bekleyen bir üye için hüküm verilmez; şerit "Kısıt eklenmemiş" der. `Engel bulunmadı` yalnız tanımlı kısıt ve doğrulanmış içerik varsa verilir.
*Doğrulama:* property test: kısıt = bilinmiyor ⇒ hüküm ∉ {Engel bulunmadı}. **(K1)**

**S9 — Asimetri: katılaştırmak ucuz, gevşetmek pahalı.**
Belirsizlik her zaman daha katı hükme çözülür. Kısıt ekleme, alerjen ekleme ve kuralı sıkılaştırma tek adımdır. Kısıt kaldırma, alerjen silme ve kuralı gevşetme; kısıtın sahibinin (çocukta ortak velilerin) ya da iki moderatörün onayını ister.
*Doğrulama:* Admin iş akışında 4 göz kontrolü; etki raporunda "gevşeyen" sayısı. **(K2, K7, K11)**

**S10 — Hard kısıtı yalnız sahibi, yalnız profil ekranında gevşetir.**
Asistan, olursuzluk önerileri, misafir/tatil modu ve optimizasyon hard kısıtı hiçbir zaman gevşetmez ve gevşetmeyi önermez. Varlık takvimi porsiyonu değiştirir, kısıtı değiştirmez.
*Doğrulama:* NL→kısıt eval'inde alerjen gevşetme = 0; olursuzluk öneri üreticisinde property test. **(K7)**

**S11 — Hüküm yalnız kimliği kesin ürüne verilir.**
`Engel bulunmadı` yalnız iki durumda verilir: barkoddan tarihli doğrulanmış katalog kaydına ulaşıldıysa ya da etiket eksiksiz ve eşiğin üstünde bir güvenle okunduysa. Görüntü tanıma, dökme ürün, ev yemeği, çoklu paketin dış barkodu ve yabancı sürüm kaydı için en iyi hüküm `Dikkat` ya da `Doğrulanamadı`dır. Görüntüden yalnız `Uygun değil` ya da "tara" çıkabilir.
*Doğrulama:* hüküm kaynağı alanı zorunludur; kaynak ∈ {görüntü, dökme, ev yemeği} ⇒ hüküm ≠ Engel bulunmadı. **(K8, K9)**

**S12 — İçerik çözümlemesi Türkçe'ye ve belirsizliğe dürüsttür.**
Etiketten ya da LLM tarifinden gelen her içerik adı Türkçe locale normalizasyonundan ve türev/bileşik içerik sözlüğünden geçer. Çözülemeyen bileşik içerik `Doğrulanamadı`dır. "İçermez" beyanı ve "içerebilir" beyanının yokluğu tek başına kanıt sayılmaz. TGK 14 dışındaki özel alerjenlerde en iyi hüküm `Dikkat`tir. Belirsiz alerjen adları (fıstık, kuruyemiş, laktoz/süt, gluten/çölyak) girişte netleştirilir.
*Doğrulama:* büyük harf, olumsuzlama ve türev içerik altın seti her kural sürümünde koşar. **(K2, K3)**

**S13 — Araç kazanır.**
Kullanıcının gördüğü her hüküm, rakam ve uyarı bir araç çıktısından çizilir. LLM metni hükmü değiştiremez. Her metin yasaklı kelime/iddia filtresinden ve iddia–araç eşleşme denetiminden geçer. Araç çıktıları ve topluluk metinleri talimat değil veridir.
*Doğrulama:* red-team ve injection eval seti; yasaklı kelime = 0; çelişki oranı panoda izlenir. **(K5)**

**S14 — Tıbbi sınır deterministiktir.**
Doz, tolerans ve tedavi sorularına evet ya da hayır denmez. Akut belirti algılanınca sohbet durur ve 112 yönlendirmesi gösterilir. Bu yollar LLM'e bırakılmaz.
*Doğrulama:* güvenlik sınıflandırıcısı için duyarlılık eşiği; sesli giriş dahil test seti. **(K4)**

**S15 — Sağlık verisi sınırı sohbette de geçerlidir.**
Serbest metin ve ses, yurt dışında işlenmeden önce Türkiye'de maskelenir. Maskeleme güveni düşükse istek Türkiye'deki modele gider ya da işlenmez. Sohbette geçen sağlık bilgisi profile yalnız rıza akışıyla girer.
*Doğrulama:* maskeleme sızıntı oranı eval'i (şive ve yazım hatası dahil). *Hipotez; Faz 3 ADR.* **(K6)**

**S16 — Sürüm zinciri.**
Her hüküm (ürün, profil, kural) sürüm üçlüsüne bağlıdır. Biri değişince ona bağlı canlı plan, liste, kiler ve cihaz önbelleği yeniden değerlendirilir. Eski sürümle gelen onay sunucuda reddedilir. Çevrimdışı hüküm son eşitleme tarihini gösterir. Geçmiş DR'ler değişmez.
*Doğrulama:* eşzamanlılık testleri (iki istemci + çevrimdışı); DR yeniden üretim testi. **(K9, K12)**

**S17 — Düzeltme sözü.**
Kullanıcıya gösterilmiş bir hüküm sonradan katılaşırsa (moderasyon düzeltmesi, kural değişikliği, ikame, tarif değişikliği), o ürünü kilerinde, listesinde ya da son 30 günlük taramasında bulunduran her haneye düzeltme bildirimi gider. Bildirim hatayı açıkça söyler.
*Doğrulama:* DR'den etkilenen hane sorgusu; bildirim teslim oranı. **(K10, K11)**

**S18 — İfşa kanalları sağlık verisi taşımaz.**
Push ve kilit ekranı, e-posta, varsayılan sesli yanıt, WhatsApp/yazdırma listesi ve paylaşım kartları üye adıyla kısıtı birlikte içermez. Paylaşım linkleri süreli, ayrı erişim kodlu, loglu ve iptal edilebilirdir. Çocuk verisi varsayılan olarak dışarıdadır.
*Doğrulama:* push payload ve paylaşım çıktısı için otomatik PII/sağlık terimi taraması. **(K13)**

**S19 — Herkes kendi verisini verir; üçüncü kişinin kısıtı yemeğe bağlanır.**
Başka bir yetişkin adına sağlık verisi girilmez. Misafirin ya da etkinliğin kısıtı yemeğe bağlanır ve süresi dolunca silinir. Çocuk profili velilere bağlıdır; iki haneye ancak ortak veli onayıyla bağlanır. Yardımcı rolü süreli ve kapsamlıdır. Her yetişkin hanede "yalnız hüküm" görünürlüğünü seçebilir. Sohbet kişiye özeldir; haneye kaydetmek açık bir eylemdir.
*Doğrulama:* rıza kaydı denetimi: her kısıt kaydının bir rıza kaydı ve bir veri sahibi vardır. **(K14)**

**S20 — Geri alma ve silme gerçektir.**
Rıza geri alınınca işleme durur, ürün genel modda çalışmaya devam eder ve neyin kapanacağı önceden gösterilir. Silme kripto-silmedir; DR ve audit yalnız içeriksiz kalıntı tutar. Anonim katkıların geri alınamayacağı katkı anında söylenir. 18 yaş, yöneticinin ayrılması ve ölüm için tanımlı geçiş akışları vardır.
*Doğrulama:* silme sonrası DR'lerden içeriğin okunamadığını gösteren test; geçiş akışı senaryo testleri. **(K15)**

**S21 — Asistan yoksa ürün çalışır; asistan onaysız iş yapmaz.**
LLM kesintisi tarama, liste, plan onayı ve kısıt kontrolünü durdurmaz. Asistan paylaşan, durum değiştiren ya da geri alınamaz eylemleri tek dokunuşlu onay olmadan yapmaz. *(destekleyici)*

**S22 — Hüküm yalnız renkle verilmez.**
Hüküm ikon, metin ve haptikle birlikte verilir. Ekran okuyucu önce hükmü okur. *(destekleyici)*

---

## 14. Ekran ve özellik envanterine etkisi (v3 envanterinde olmayanlar)

**Mobil**
- Kısıt netleştirme kartı (fıstık/laktoz/gluten)
- Özel kısıt ve hüküm tavanı açıklaması
- Hane birleştirme sihirbazı
- Ortak veli daveti
- Yardımcı rolü
- Kısıt kartı (PDF)
- "Hafızam"
- Acil durum ekranı (112)
- "Neler değişir" (rıza geri alma önizlemesi)
- Genel mod göstergesi
- Düzeltme bildirimi ara ekranı
- "Bu hafta ara ver"
- Geçici kontrol (hane dışı kişi)

**Web**
- Paylaşım erişim logu ve iptal
- Ekran paylaşımı modu
- Birleştirme ve çakışma özeti

**Admin**
- Etki raporu (kural ve katalog değişikliği)
- 4 göz onayı
- Karantina modu
- Katkıcı toplu geri alma
- Break-glass erişimi
- Anomali panosu
- Eval kapısı (model yükseltme)

---

## 15. Açık sorular — Levent'e
1. **Genç hesabı:** 13–17 yaşa kendi hesabı açılsın mı? Alt yaş sınırı ne olsun? (1.9)
2. **Doğum tarihi:** Çocuk profilinde doğum yılı ve ayı tutulsun mu (18 yaş geçişi için), yoksa veliye yılda bir mi sorulsun? (8.5)
3. **Boşanmış veliler:** Kısıt kaldırmak için iki velinin onayı mı gereksin, yoksa velayet sahibinin mi? Hukukçuya sorulmalı. (1.13)
4. **Hane kuralı:** Kişiye bağlanmayan dışlama ("evde fındık yok") KVKK açısından sağlık verisi mi? KVKK uzmanına sorulmalı. (0.1)
5. **Gece P0:** Hangi P0 uyarıları sessiz saatte bile gönderilmeli? (7.3)
6. **Silme penceresi:** Hesap silmede 14 günlük geri alma penceresi olsun mu? (§8)
7. **Dil kapsamı:** Arapça ya da başka bir dil v1'de olacak mı? (X.7)
8. **Sohbette sağlık verisi:** Maskeleme mi, Türkiye'de barındırılan model mi? Teknik spike ve Faz 3 ADR gerekiyor. (2.16)
9. **Ürün tanımı:** v4 menü ve kileri kapsama aldı. `plan/urun-tanimi.md` v4'e göre güncellensin mi?
