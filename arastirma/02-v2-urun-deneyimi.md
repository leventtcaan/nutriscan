---
title: 02 — v2 ürün deneyimi (ilk 60 saniye, wow anları, retention, IA, demo, ton)
tarih: 2026-09-24
durum: HAM
---

> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24.**
> Konsept v2 (PLAN → AL → ÖĞREN; sağlık × bütçe × güvenlik) üzerine UX araştırması ve fikir üretimi. **Karar değildir.**
> Kaynaklı rakamların linki yanında. `[değerlendirme]` = benim yorumum, kaynağı yok.
> Bağlı raporlar: veri gerçeği `01-veri-fizibilite.md` (fiş OCR 🟡, fiyat verisi izne bağlı), dil ve rıza sınırları `01-mevzuat-risk.md`.

---

## 0. TL;DR

1. **Ürün bir tarayıcı değil, haftalık bir ritüel.** Pazar akşamı planla, hafta içi al, fişi çek, pazartesi karneyi gör. Barkod tarama sadece giriş kapısı. Retention'ı fiş alışkanlığı taşır, tarama taşımaz.
2. **Soğuk başlangıç: ilk 60 saniyede fiş şart olmamalı.** Açılışta üç kapı sun: "Elimde fiş var" / "Mutfaktayım" (Dolap Turu: 3 ürün tara, mini karne al) / "Rafta" (direkt tara). Bir de "Sadece bakıyorum" seçeneği: dolu bir örnek hane. Hesap ve sağlık verisi **ilk değer görüldükten sonra** istenir.
3. **En güçlü 5 wow anı:** (W1) ilk fişten 20 saniyede Sepet Karnesi ve en büyük 3 katkıcı · (W2) Akıllı Takas kaydırıcısı: "3 takasla ayda 340 TL ve %25 daha az şeker" · (W3) rafta hane üyesi bazlı sonuç ve "sepete etkisi" · (W4) mutfak enflasyonun vs TÜİK · (W10) sağlık verisi içermeyen Sepet Wrapped kartı.
4. **Fişin gizli değeri fiyat verisi.** marketfiyati.org.tr yazılı izin istiyor (bkz. `01-veri-fizibilite.md`). Fiş satırları (market, ilçe, tarih, ürün, fiyat) kendi fiyat gözlem tablomuzu kurar. Kişisel enflasyon, "daha ucuz alternatif" ve takas maliyeti buradan beslenir. `[değerlendirme]`
5. **Günlük streak yok.** Sağlık uygulamasında suçluluk üretir, yeme davranışı saplantısına zemin hazırlayabilir. Onun yerine haftalık, affedici bir "hane ritmi" öneriyorum. Ödüllendirilen şey yemek erdemi değil, verinin tamlığı.
6. **Dil kuralı:** kişiyi değil sepeti konuş. "Güvenli", "zararlı", "kötü" kelimeleri yok. Çocuğa skor yok, kalori yok. Her ekranda tek bir büyük sayı ve tek bir aksiyon.

---

## 1. Örnek ürünlerden çıkan dersler

| Ürün | Ne yapıyor (kanıt) | NutriScan'e ders |
|---|---|---|
| **Spotify Wrapped** | 2025'te ilk 24 saatte 200M+ kullanıcı, 500M+ paylaşım (paylaşımda yıllık %41 artış) ([TechCrunch](https://techcrunch.com/2025/12/04/spotify-says-wrapped-2025-is-its-biggest-yet-with-200m-users-in-its-first-day), [MBW](https://www.musicbusinessworldwide.com/spotify-wrapped-campaign-hit-200m-engaged-users-in-24-hours-a-19-yoy-increase/)). İşleyen mekanizmalar: kesin sayılar, sosyal karşılaştırma, merak, nostalji ve kimlik ("Alchemist" gibi arketipler) ([Irrational Labs](https://irrationallabs.com/blog/spotify-wrapped-behavioral-science/)) | Sepet Wrapped'ı **kimlik** etrafında kur ("Bakliyat Ustaları" gibi hane arketipleri). Ham sağlık rakamını paylaştırma. Dikey 9:16 story formatı kullan. |
| **Year in Monzo** | Başta ton seçimi soruluyor: "nice" ya da "savage". 3 kişilik ekip 2.000+ satır metin yazmış; 150 mağazaya özel espri ve yaklaşık 80 "mood" var. Bulunan çözüm: veri noktalarını birleştirip bir hikâye kurmak ([Monzo — Writing Year in Monzo 2024](https://monzo.com/blog/writing-year-in-monzo-2024), [How we built](https://monzo.com/blog/how-we-built-year-in-monzo-unlocking-the-data-magic)) | Ton seçimi fikri iyi, ama sağlıkta "savage" mod olmamalı. Önerim "Sade / Esprili" seçeneği. Espriyi mağazaya değil ürüne ve alışkanlığa bağla ("Yılın ürünü: Ayran, 48 kez"). |
| **Yemeksepeti 2025 Keyif Özeti** | Kullanıcıya kişisel sipariş özeti sunuluyor ([DHA](https://www.dha.com.tr/gundem/yemeksepeti-2025-siparis-ozetini-acikladi-2787626)) | TR kullanıcısı Wrapped formatını gıda bağlamında zaten tanıyor. |
| **Monzo Trends** | "Left to spend" (faturalar düşüldükten sonra kalan), kategori hedefleri ve hedefe yaklaşınca bildirim ([Monzo Trends](https://monzo.com/us/blog/monzo-us-blog/trends), [kategori hedefleri](https://monzo.com/us/blog/monzo-us-blog/trends-category-targets)) | Ana ekranda tek sayı: **"Bu ay kalan market bütçen"**. Ay sonu tahmini: "Bu hızla 1.200 TL aşacaksın; 2 takas bunu kapatır." |
| **Papara** | Aylık Özet, kategori grafikleri, en çok harcanan marka. "Yuvarla" özelliği küsuratı birikim hesabına atıyor ([Aylık Özet](https://blog.papara.com/aylik-ozet-ile-gercek-patron-sensin/), [Yuvarla](https://www.papara.com/faq/birikim-hesabi/birikim-hesabimdaki-yuvarla-ozelligi-nedir)) | Aylık özet TR'de alışılmış bir format. Yuvarla'dan esinle **"Takas Kumbarası"**: kabul edilen takasların tasarrufu görünür biçimde birikir. |
| **Acorns Round-Ups** | Kullanıcı karar vermeden arka planda birikim yapıyor; ilk 4 ayda ortalama 150$+ ([Acorns](https://www.acorns.com/round-ups/)) | Pasif değeri görünür yap: "Hiçbir şey yapmadan bu ay 3 fiyat farkı yakaladık." |
| **Yuka** | 0–100 puan ve 4 renk; düşük puanlı ürüne aynı kategoriden alternatif ([GreenChoice](https://about.greenchoicenow.com/resources/yuka-app)). Eleştiri: korku, utanç ve kaygı yaratabiliyor ([Abby Langer](https://abbylangernutrition.com/yuka-app-review-scan-or-scam/), [NPR](https://www.npr.org/2025/05/26/nx-s1-5391915/phone-apps-food-nutrition-health)) | Sadeliği al: tek bakışta karar ve tek alternatif. Yargılayan dili alma. |
| **Fig** | "Multiple Figs": hane üyeleri için ayrı profiller, 2.800+ kısıt ([App Store](https://apps.apple.com/us/app/fig-food-scanner-guide/id1564434726)) | Rafta **kişi bazlı sonuç şeridi**. Fig'de olmayan şey: sonucun haftalık sepete etkisi. |
| **Kroger OptUP** | Hanenin son 8 haftalık alımlarından 0–1000 skor; önerilen hedef 600+; sepetin ≥%50'si yeşil, ≤%10'u kırmızı olmalı ([Kroger FAQ](https://www.kroger.com/hc/help/faqs/health-and-wellness/optup), [Kroger blog](https://www.kroger.com/blog/health/opt-up)). Ayrı OptUP uygulaması artık desteklenmiyor, özellikleri ana Kroger uygulamasına taşınmış ([Kroger OptUP sayfası](https://www.kroger.com/health/nutrition/optup), arama özeti; sayfa bu oturumda zaman aşımına uğradı, tarih doğrulanmadı) | **Sepet skoru tek başına bir uygulamayı ayakta tutmuyor.** Skorun yanına para ve aksiyon (takas) konmalı. Ayrıca OptUP tek zincirin sadakat kartına bağlı; biz fişle zincirden bağımsız çalışıyoruz. |
| **Instacart** | AI ile çıkarılan 30 Health Tag (~500 bin ürün), Smart Shop, ADA ile diyabet sayfası ([Instacart](https://company.instacart.com/pressreleases/instacart-launches-ai-powered-smart-shop-and-new-features-that-make-healthy-choices-easy)). Family Carts: hane üyeleri ortak sepet dolduruyor, sipariş verilince herkese bildirim gidiyor ([Help](https://www.instacart.com/help/section/4179348463), [RetailWire](https://retailwire.com/discussion/instacart-has-a-family-plan-to-build-shopping-carts/)) | **Ortak canlı liste** hane modunun görünen yüzü. Etiket çıkarımı LLM'le yapılabilir ama karar kuralda kalmalı. |
| **Fetch** | Her fiş bir puan kazandırıyor. eReceipt için e-posta ya da market hesabı bağlanıyor, otomatik taranıyor ([Fetch eReceipts](https://fetch.com/blog/fetch-tips-tricks/fetch-and-ereceipts-earn-rewards-when-online-shopping)). "%70 haftalık retention" iddiası ikincil bir blogdan geliyor, doğrulanmadı ([RaftLabs](https://www.raftlabs.com/blog/how-to-create-an-app-like-fetch-rewards)) | **Her fiş anında bir karşılık vermeli.** Bizde bu para değil, içgörü. Online siparişler için pasif giriş kanalı gerekli. |
| **Expensify** | Faturayı `receipts@expensify.com` adresine yönlendirmek yeterli, SmartScan işliyor ([Expensify](https://use.expensify.com/receipt-scanning-app)) | "fis@…" yönlendirme adresi: Getir, Migros Sanal Market ve Trendyol Go faturaları için OAuth'suz, düşük sürtünmeli pasif giriş `[değerlendirme; fatura formatları doğrulanmadı]`. |
| **Copilot Money** | Düzeltmelerden öğrenen otomatik kategorizasyon; 2–3 hafta sonra manuel iş neredeyse bitiyor. iPad/Mac uygulaması büyütülmüş iPhone ekranı değil ([Penny Hoarder](https://www.thepennyhoarder.com/budgeting/budgeting-copilot-money-review/), [Finny](https://getfinny.app/blog/copilot-money-review-2026)) | Fiş satırı eşleştirmesi düzeltmelerden öğrenmeli. Web, mobilin kopyası olmamalı. |
| **Duolingo** | Streak en etkili retention kolu. 7+ günlük seri 3,6 kat bağlılık, Streak Freeze riskli kullanıcıda churn'ü %21 düşürüyor, Friend Streak +%22 (ikincil kaynaklar: [Deconstructor of Fun](https://duolingo.deconstructoroffun.com/mechanics/streaks), [Lenny's Podcast özeti](https://www.recall.it/summary/business/behind-the-product-duolingo-streaks-or-jackson-shuttleworth-group-pm-retention-team)). Eleştiri: suçluluk bildirimleri, "goal displacement" ([The Decision Lab](https://thedecisionlab.com/insights/consumer-insights/streak-creep-the-perils-of-too-much-gamification), [Web Designer Depot](https://webdesignerdepot.com/the-art-of-duolingo-notifications-the-subtle-manipulation-of-language-learners/)) | Mekanizmanın kendisini değil ilkesini al: affedici ve sosyal (hane) olsun. **Günlük değil haftalık.** |
| **Noom** | Yeşil / sarı / turuncu. Kırmızı yok, "iyi/kötü" etiketi yok ([Noom](https://www.noom.com/support/faqs/using-the-app/logging-and-tracking/food-and-water/2025/10/how-nooms-food-color-system-works/)) | Besin kalitesinde kırmızı kullanma. Kırmızı sadece alerjen/kısıt çakışmasına ayrılsın. |
| **Too Good To Go** | Kişisel etki gerçek dünya eşdeğerleriyle anlatılıyor (CO2 → telefon şarjı) ([App Store](https://apps.apple.com/us/app/too-good-to-go-end-food-waste/id1060683933)) | Tasarrufu somut eşdeğere çevir: "340 TL ≈ 1 haftalık ekmek + süt". |
| **Cal AI** | 25+ kartlık uzun quiz onboarding, sonunda kişisel plan ve paywall ([ScreensDesign](https://screensdesign.com/showcase/cal-ai-calorie-tracker)) | Uzun onboarding yatırım hissi yaratıyor, ama bizde değer bir fotoğraftan anında üretilebiliyor. **Tersini yap:** 1 soru sor, değeri göster, gerisini zamanla iste. |
| **GetirFinans** | Onboarding saniyeler sürüyor; küçük harfli, samimi mikro metin; "yoğurt sipariş etmek kadar kolay" hedefi ([UX Design Awards 2026](https://ux-design-awards.com/winners/2026-1-getirfinans-digital-onboarding)) | Hassas bir alanda (finans) bile samimi ve sade ton TR'de ödül alıyor. |
| **Spotify taste onboarding** | Seçilen sanatçı ve türler ilk gün kişiselleştirmeyi besliyor; davranış verisi geldikçe devrediyor ([Spotify Research](https://research.atspotify.com/2025/9/generalized-user-representations-for-large-scale-recommendations)) | **"Sepetini seç" ızgarası:** en sık aldığın 8 ürünü görsellerden seç, tahmini karneyi gör. |
| **Apple HealthKit / just-in-time izin** | İzni bağlam içinde ve yalnızca gereken veri için iste ([Apple](https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data), [Sage Bionetworks](https://sage-bionetworks.github.io/DesignSystem/just-in-time-permission.html)) | Sağlık rızası alerji eklendiği anda istenmeli, açılışta değil. |
| **Kişisel enflasyon araçları** | BBC/Cumhuriyet hesaplayıcısı, açık kaynak "enflasyonum" (Laspeyres, 13 ECOICOP, TÜİK'le yan yana) ([Cumhuriyet](https://www.cumhuriyet.com.tr/ekonomi/hissedilen-enflasyon-kisisel-enflasyonunuzu-hesaplayin-2066383), [GitHub](https://github.com/umutseve4/enflasyonum)) | Merak var ama araçların hepsi **manuel veri giriyor**. Biz fişten otomatik hesaplıyoruz. |

---

## 2. İlk 60 saniye ve soğuk başlangıç

### 2.1 Problem
Konseptin değeri geçmiş alışverişe (fişe) bağlı, ama kullanıcı ilk açılışta elinde fiş olmadan geliyor. Boş bir karne ekranı erken churn'ün en sık nedeni. Örnek veri ve dolu demo durumları "aha" anını öne çekiyor ([Appcues](https://www.appcues.com/blog/mobile-onboarding), [Appcues aha](https://www.appcues.com/blog/aha-moment-examples)).

### 2.2 Açılış: "Nereden başlayalım?" (4 kapı)

| Kapı | Kim için | İlk değer | Süre |
|---|---|---|---|
| **A. Elimde fiş var** | Alışverişten yeni dönen | Fiş Karnesi (W1) | ~25 sn |
| **B. Mutfaktayım** (Dolap Turu) | Evde, fişi yok | Dolaptan 3 ürün taranır, mini karne çıkar: "3 üründen 2'sinde şeker ilk 3 içerikte" + "hanende tahminen…" | ~40 sn |
| **C. Rafta / markette** | Tam karar anında | Profil sorulmadan genel sonuç ve alternatif, ardından tek soru: "Bunu kimin için alıyorsun?" | ~10 sn |
| **D. Sadece bakıyorum** | Meraklı | Örnek hane (sentetik "Aydın ailesi" ayı). Bütün ekranlar dolu, üstte "örnek veri" şeridi ve "Kendi haneni kur" butonu | 0 sn |

Kapı B'ye ek olarak **"Sepetini seç"** (Spotify modeli): TR'de sık alınan 24 ürün kategorisinden görsel ızgara (ekmek, ayran, kola, gofret, zeytinyağı…). Kullanıcı 8 tanesini seçer, "tahmini karne"yi görür. Kesinlik iddiası taşımaz, üzerinde "ilk fişinle netleşir" yazar.

### 2.3 Saniye saniye (Kapı A)

| Zaman | Ekranda | Not |
|---|---|---|
| 0–5 sn | Splash yok. Tek cümle: **"Fişini çek, hanenin sepetini 20 saniyede gör."** Altında 4 kapı | Hesap yok, anonim yerel oturum |
| 5–10 sn | Kamera izni. Sistem penceresinden önce tek satır: "Fişi okumak için kamera lazım; fotoğraf sende kalır, sadece metni işleriz." | Metin, gerçek mimari kararla tutarlı olmalı |
| 10–25 sn | Fiş çekiliyor. Satırlar iskelet olarak belirip tek tek doluyor ("ekmek ✓, ayran ✓, ULKR CIK GOF… ?") | Algılanan hız: bekleme animasyonu aynı zamanda ne yapıldığını gösteriyor |
| 25–40 sn | **Karne:** tek büyük sayı + en büyük 3 katkıcı + "bu fişte ~X TL'lik fırsat" | Eşleşmeyen satırlar için "3 satırı onayla" kaydırmalı kartları |
| 40–55 sn | Tek soru: **"Kaç kişisiniz?"** (stepper). Kişi başı rakamlar canlı güncellenir | Rakamın gözün önünde değişmesi mini bir wow |
| 55–60 sn | "Hanene özel olsun mu? Alerji ya da hedef ekle" · belirgin bir **"Sonra"** butonu | Kaydetmek için Apple/Google ile giriş burada istenir, daha önce değil |

### 2.4 Onboarding ilkeleri (sağlık rızası dahil, sürtünmesiz)
1. **Önce değer, sonra hesap, en son sağlık verisi.** Sıra: fiş → karne → kişi sayısı → (isteğe bağlı) hedef/alerji → hesap.
2. **Teşhis değil hedef sor:** "Evde neyi değiştirmek istersiniz? □ Şekeri azaltmak □ Tuzu azaltmak □ Bütçeyi korumak □ Belirli içeriklerden kaçınmak". "Prediyabet" gibi bir tanı alanı yok. Bu hem tıbbi cihaz riskini (bkz. `01-mevzuat-risk.md` §3) hem rıza sürtünmesini azaltır. `[değerlendirme: "şeker azaltma hedefi" seçiminin sağlık verisi sayılıp sayılmadığı hukuken teyit edilmeli; alışveriş geçmişi dolaylı sağlık verisine dönüşebiliyor, §1.1]`
3. **Just-in-time rıza:** Alerji/intolerans eklendiği anda tek ekranda iki ayrı bölüm gösterilir: aydınlatma metni ("okudum", onay değil) ve **işaretlenmemiş** bir açık rıza kutusu. Bu, 18.02.2026 tarihli ve 2026/347 sayılı İlke Kararı'na uygun (`01-mevzuat-risk.md` §1.3). Üstte 3 maddelik özet, altta "tam metin" linki.
4. **Çocuk profili:** Veli ekler. Gerçek isim yerine takma ad veya emoji önerilir (veri minimizasyonu). Yaş yerine sadece "çocuk" etiketi.
5. **Başka yetişkin:** WhatsApp davet linki gönderilir. Davet edilen kişi kendi alerji ve hedefini **kendisi** girer; başkası adına sağlık verisi girilmez (`01-mevzuat-risk.md` §1.6).
6. **Ciddi alerji satırı:** Alerji eklendiğinde bir kez ve kalıcı olarak gösterilir: "Etiketi her zaman sen kontrol et; NutriScan etikette beyan edilenleri karşılaştırır." (Yuka modeli)
7. **Bildirim izni** açılışta değil, "Haftalık karnen hazır olunca haber vereyim mi?" dendiği anda istenir.
8. **Konum izni yok.** Market seçimi için il/ilçe seçmek yeterli.

### 2.5 Soğuk başlangıç veri stratejisi `[değerlendirme]`
- **Fiş satırı eşleşmezse:** "'ULKR CIK GOFRET' → Ülker Çikolatalı Gofret mi? Evet / Hayır / Barkodu okut". Her düzeltme eşleştirme sözlüğüne girer (Copilot modeli) ve admin moderasyon kuyruğuna düşer.
- **Fiyat:** Her fiş satırı (market, ilçe, tarih, ürün, birim fiyat) bir fiyat gözlemi olur. Fiyat bilgisi olmayan ürünlerde "fiyat bilinmiyor" yazar, uydurulmaz.
- **Kişisel enflasyon en az 2 ay veri ister.** İlk gün bunun yerine "Bu fişteki ürünlerin TÜİK kategorilerinde yıllık artış" gösterilir. Kişisel rakam 2. ayda açılır ve bu bir **kilit açılma** anı olarak sunulur (retention).
- **Besin verisi eksikse:** OFF → etiket OCR → kategori ortalaması (TürKomp/OFF kategori medyanı) sırası izlenir. Her sayının yanında kaynak rozeti: "etiket" / "tahmini".

---

## 3. Wow anları (12)

★ = en güçlü 5. Her maddede sırasıyla: **Tetik** · **Ekranda** · **Neden etkiler** · **Teknik bağımlılık** · **Paylaşım** · **Risk**.

### W1 ★ İlk Fiş Karnesi (20 saniye)
- **Tetik:** İlk fiş fotoğrafı.
- **Ekranda:** "Bu fiş: 23 ürün, 1.184 TL. Kişi başı haftalık eklenmiş şeker ≈ 180 g." Altında **en büyük 3 katkıcı** yatay çubuklarla: Kola 2,5 L (%38) · Gofret ×3 (%21) · Meyve suyu 1 L (%14). En altta: "Bu 3 üründe küçük bir değişiklik → ayda ~X TL ve %Y daha az şeker · **Takasları gör**".
- **Neden etkiler:** Kullanıcının kendi kağıdı saniyeler içinde anlamlı bir veriye dönüşüyor. Pareto görünümü karmaşayı tek aksiyona indiriyor. Meyve suyunun listede çıkması gibi sürprizler akılda kalıyor.
- **Teknik:** Vision LLM fişi satırlara çevirir (JSON). Bulanık eşleştirme fiş kısaltmasını ürüne bağlar. Besin verisi OFF + fallback'ten gelir. Güven skoru tutulur. Hesap backend'de yapılır; LLM'e profil gitmez.
- **Paylaşım:** Yok (kişisel).
- **Risk:** Yanlış eşleşme. Önlem: "≈" işareti, "%82 eşleşti" rozeti, tanınmayan ürün için kategori ortalaması.

### W2 ★ Akıllı Takas: "3 takasla ayda 340 TL ve %25 daha az şeker"
- **Tetik:** Karnedeki "Takasları gör" butonu ya da pazartesi karnesi.
- **Ekranda:** Kaydırıcı: **"Kaç değişikliğe hazırsın? 1 · 3 · 5"**. Kaydırdıkça TL ve şeker rakamları canlı değişir. Altında 3 takas kartı ("Kola 2,5 L → sade soda + limon: −62 TL/ay, −… g şeker"). Her kartta "Ela'nın listesiyle çakışma yok" rozeti. Kart başına "Listeye ekle" ve "Bize göre değil".
- **Neden etkiler:** Para ve sağlık aynı cümlede, kayıp değil kazanç olarak. En az değişiklikle sonuç sunulduğu için davranış maliyeti düşük. Kontrol kullanıcıda (kaydırıcı).
- **Teknik:** Optimizasyon (P2/P3 · ILP): en fazla k değişiklik, bütçe ≤ B, alerjen kısıtı hard constraint, amaç şeker/tuz/UPF azaltımı. İkame adayları aynı OFF kategorisinden gelir. Fiyatlar fiş gözlemlerinden. "Bize göre değil" geri bildirimi kabul olasılığını öğrenir (P6). **Danışman açısı:** exact vs sezgisel ve aradaki gap.
- **Paylaşım:** Kısmen. "Bu ay takaslarla 340 TL biriktirdik" kartında sağlık verisi olmaz. Takas Kumbarası burada birikir.
- **Risk:** Kabul edilmeyecek ikameler ("kola → su" gibi). Önlem: aynı ürün tipinde kal (kola → şekersiz kola da bir seçenek), kabul oranını ölç.

### W3 ★ Rafta hane kararı + sepete etkisi
- **Tetik:** Barkod tarama.
- **Ekranda:** Üstte ürün. Altında **hane şeridi**: 👧 Ela: "Fındık içerir, listeyle çakışıyor" (kırmızı) · 👨 Murat: "Porsiyon başına 18 g şeker, haftalık hedefin %…'i" (turuncu) · 👩 Selin, 👦 Can: "Çakışma yok, etiket beyanına göre". Alt kart: **"Sepete eklersen bu haftanın şekeri 180 → 205 g"**. En altta: "Daha iyi: [X] · 4 TL ucuz · fındık beyanı yok · %40 daha az şeker".
- **Neden etkiler:** Tek taramada dört kişi. Ürün kararı haftanın bağlamına oturuyor; rakiplerde bu "sepete etkisi" yok. Önerilen alternatif hem daha uygun hem daha ucuz.
- **Teknik:** Deterministik alerjen motoru, 4 durumlu sonuç, hane profilleri, haftalık sepet durumu, fiyat gözlemi, Decision Record.
- **Paylaşım:** Yok.
- **Risk:** Veri yoksa **"Doğrulanamadı: etiketi çek, 10 saniyede okuyalım"** (bkz. W11). Yanlış "çakışma yok" en ağır risk; dil ve kaynak rozeti burada kritik.

### W4 ★ Mutfak enflasyonun vs TÜİK
- **Tetik:** 2. ayın ilk fişi (kilit açılır) ve her ay başı.
- **Ekranda:** **"Senin mutfak enflasyonun: %41 · TÜİK gıda: %33,79 (Ağustos 2026)"** ([Alomaliye/TÜİK](https://www.alomaliye.com/2026/09/03/enflasyon-rakamlari-tufe-agustos-2026/)). Altında "Farkı yaratan 3 ürün: zeytinyağı +%72, …". Bir de "Aynı ürünü geçen ay A101 Konyaaltı'nda %12 daha ucuza almıştın" gibi bir satır.
- **Neden etkiler:** TR'de her gün konuşulan bir konu. "Resmi rakam vs benim hissettiğim" sorusuna kişisel veriyle cevap veriyor. Mevcut araçlar manuel giriş istiyor, bu otomatik.
- **Teknik:** Aynı ürünün zaman serisi, hane sepet ağırlıklarıyla Laspeyres, ürün kimliği normalizasyonu, birim fiyat (gramaj değişimi), TÜİK alt endeks tablosu (aylık bülten, elle ya da script'le içe aktarma).
- **Paylaşım:** **Evet, en güvenli kart.** Sağlık verisi içermiyor. Örnek: "Benim mutfak enflasyonum %41. Seninki?"
- **Risk:** Siyasi hassasiyet. Önlem: nötr dil ("senin sepetin TÜİK sepetinden farklı"), yöntem linki. Az veride geniş belirsizlik aralığı gösterilir.

### W5 Gizli zam dedektörü (paket küçülmesi)
- **Tetik:** Aynı ürünün gramajı düşmüş, fiyatı değişmemiş ya da artmış.
- **Ekranda:** "Bu gofret 40 g'dan 36 g'a indi. Birim fiyatı %11 arttı." Yanında "Birim fiyatı en düşük 3 alternatif".
- **Neden etkiler:** Görünmeyen bir şey görünür oluyor. Paylaşılabilir ve öfke/merak uyandırıyor.
- **Teknik:** Ürün gramaj geçmişi (OFF + etiket OCR + fiş satırındaki gramaj). Veri bağımlılığı yüksek; demo'da seed veriyle gösterilir. **Kapsam: "could"**.
- **Paylaşım:** Evet (ürün düzeyinde, kişisel veri yok).
- **Risk:** Yanlış eşleşme sonucu haksız "gizli zam" iddiası (marka itibarı). Önlem: yalnızca barkod + gramaj kesin eşleştiğinde göster.

### W6 "Sağlığın fiyatı"
- **Tetik:** Kullanıcı bir hedef seçmiş ("şekeri azalt") ve karneyi açıyor.
- **Ekranda:** Eğri: x ekseni haftalık şeker azaltımı, y ekseni aylık maliyet farkı. Eğri üzerindeki noktalar tıklanabilir ("burada kola→soda, burada…"). Tek cümlelik özet: **"İlk 10 g bedava, hatta 30 TL kazandırıyor. Sonraki 10 g ayda +45 TL."**
- **Neden etkiler:** Sağlık "yapmalısın" olmaktan çıkıp pazarlığı yapılabilir bir fiyata dönüşüyor. İlk adımların çoğunlukla bedava olması şaşırtıyor. Jüri için optimizasyonun en görsel hali bu.
- **Teknik:** P1/P3 LP; ε-constraint ile Pareto eğrisi; dual değişken (gölge fiyat) = marjinal maliyet (CSE 413'ün dili).
- **Paylaşım:** Hayır. İleride anonim toplu içgörü olabilir ("Antalya'da medyan…").
- **Risk:** Kullanıcı "fiyat"ı tıbbi bir reçete gibi algılayabilir. Önlem: "sepet önerisi, tıbbi tavsiye değil" satırı.

### W7 Doğal dille plan: "Çölyaklı kızım için 700 TL"
- **Tetik:** Web'deki Planlama Stüdyosu ya da mobilde serbest metin/ses.
- **Ekranda:** Metin anında **kısıt çiplerine** dönüşür: [👧 Ela · glütensiz · zorunlu] [Bütçe ≤ 700 TL] [1 hafta] [Market: yakınımdakiler]. Çipler düzenlenebilir. Ardından liste çıkar: 14 ürün, 687 TL, her satırda "neden bu". Başlık: "Kısıtları böyle anladım".
- **Neden etkiler:** Konuşur gibi kullanılıyor. Çipler güven veriyor, çünkü LLM karar vermiyor, sadece anlıyor. Mimari ilke doğrudan UX'e yansıyor.
- **Teknik:** LLM metni JSON kısıta çevirir. "Kızım" ifadesi profile backend'de eşlenir; LLM'e profil gitmez (KVKK). Sonra optimizasyon ve fiyat verisi devreye girer.
- **Paylaşım:** Hayır.
- **Risk:** Yanlış anlama. Önlem: çip onayı olmadan hesap yapılmaz.

### W8 Haftalık liste + market seçimi
- **Ekranda:** "Listeyi A101 + Migros'a bölersen 86 TL ucuz. Sadece BİM'den alırsan 42 TL pahalı ama tek durak." Seçenekler: **Tek durak / En ucuz / Dengeli**.
- **Neden etkiler:** Zaman ile para arasındaki takas görünür oluyor.
- **Teknik:** P5 (Traveling Purchaser'ın hafif hali / set cover). Zayıf halka fiyat kapsaması, bu yüzden "fiyatı bilinmeyen 3 ürün" açıkça yazılır.
- **Risk:** Fiyatı eskimiş gözlemler. Önlem: "son görülme: 12 gün önce" etiketi.

### W9 Geriye dönük taklit/tağşiş uyarısı
- **Tetik:** Tarım ve Orman Bakanlığı listesine yeni eklenen bir kayıt, kullanıcının geçmiş fişleriyle eşleşiyor. Bakanlık "Taklit veya Tağşiş Yapılan Gıdalar" ve "Sağlığı Tehlikeye Düşürecek Gıdalar" adlı iki liste yayımlıyor ([Güvenilir Gıda](https://guvenilirgida.tarimorman.gov.tr/GuvenilirGida/gkd/TaklitVeyaTagsis), [Bakanlık duyurusu](https://www.tarimorman.gov.tr/Haber/6409/Taklit-Ve-Hileli-Gida-Listeleri-Artik-Anlik-Paylasilacak)).
- **Ekranda (bildirim):** "Nisan'da aldığınız bir ürüne **benzer isimli** bir ürün bakanlık listesine eklendi. Parti numarasını kontrol etmek için →" Sakin ton, kaynağın linki.
- **Neden etkiler:** Pasif takibin koruyucu değeri. Kullanıcı hiçbir şey yapmadan fayda görüyor ve güven kazanılıyor.
- **Teknik:** Listeyi içe aktarma (erişim yolu ve formatı **doğrulanmadı**: HTML tablo olabilir, API olmayabilir). Firma/marka/ürün adıyla bulanık eşleştirme. Liste parti/seri numarasına göre, fişte bu bilgi yok. O yüzden sonuç her zaman "olası eşleşme"dir. Admin'de onay kuyruğundan geçer.
- **Paylaşım:** Hayır.
- **Risk:** Yanlış pozitif (itibar/iftira riski). Kesin dil kullanılmaz, kaynak her zaman gösterilir.

### W10 ★ Sepet Wrapped (aylık "Sepet Özeti" + yıllık "Sepet Wrapped")
- **Tetik:** Ay sonu (aylık) ve Aralık (yıllık).
- **Ekranda (6–8 dikey story kartı):** ① "Bu yıl 212 fiş, 3.140 ürün" ② **Hane arketipi: "Bakliyat Ustaları 🫘"** ③ "Yılın ürünü: Ayran (48 kez)" ④ "Takas Kumbarası: 4.120 TL" ⑤ "Mutfak enflasyonun %38 · TÜİK %33,8" ⑥ "En sadık marketin: …" ⑦ "Hanenin şeker yolculuğu: Ocak→Aralık −%22" (sadece uygulama içinde, varsayılan paylaşım kartında yok) ⑧ Paylaşım kartı seçici.
- **Neden etkiler:** Kimlik, nostalji ve sosyal karşılaştırma ([Irrational Labs](https://irrationallabs.com/blog/spotify-wrapped-behavioral-science/)). TR'de Yemeksepeti Keyif Özeti sayesinde tanıdık bir format. Spotify ölçeğinde bir paylaşım davranışı zaten var.
- **Teknik:** Toplama job'u, 12–15 arketip kuralı (Monzo'da yaklaşık 80 mood var, bize daha azı yeter), sunucuda görsel üretimi (1080×1920 PNG), paylaşım linki ve web landing sayfası.
- **Paylaşım:** **Evet, ana edinim kanalı.**
- **Risk:** İstemeden sağlık bilgisi ifşa etmek (aşağıdaki kurallara bakın). Proje takvimi yıllık Wrapped'a yetişmez; demo'da aylık özet ve seed veri kullanılır.

### W11 "Veri yoksa ben okurum" + katkı anı
- **Tetik:** Ürün DB'de yok ya da içindekiler alanı boş. TR'de bu sık görülüyor; OFF'ta içindekiler dolu oranı ~%15–25 (`01-veri-fizibilite.md`).
- **Ekranda:** Etiket fotoğrafı çekilir, içindekiler ~8 saniyede metne döner, alerjenler vurgulanır, kullanıcı onaylar. Ardından: **"Bu ürünü ilk sen okudun. Senin sayende 38 hane artık içeriğini görüyor."**
- **Neden etkiler:** Hayal kırıklığı anı bir katkı anına dönüşüyor (Wikipedia/OFF hissi). Dürüst "bilmiyorum" + çözüm = güven.
- **Teknik:** Vision OCR, kullanıcı onayı, moderasyon, OFF'a geri yazma (ODbL).
- **Paylaşım:** Opsiyonel katkı kartı.
- **Risk:** OCR hatası. Önlem: onay adımı zorunlu, düşük güvende "doğrulanamadı".

### W12 Canlı ortak liste (hane anı)
- **Tetik:** Selin markette listeyi açık tutuyor, Murat evden "yoğurt" ekliyor.
- **Ekranda:** Selin'in ekranında satır anında beliriyor: "Murat ekledi · 1 dk önce". Satır otomatik kontrolden geçer: "Ela'nın listesiyle çakışma yok".
- **Neden etkiler:** Hane modu somut ve canlı bir şeye dönüşüyor. Instacart Family Carts'ın TR'deki karşılığı.
- **Teknik:** Gerçek zamanlı senkron (WebSocket/SSE), çakışma çözümü.
- **Risk:** Kişi bazlı suçlama ("Can cips ekledi"). **Ekleyene yönelik yargı içeren bir öneri gösterilmez.** Takas önerisi yalnızca listenin sahibine, isim vermeden sunulur.

### Paylaşım kartı kuralları (Wrapped benzeri)
1. **Varsayılan kartta** sağlık, alerji, çocuk, kişi adı ya da tanı yok. Yer alabilecekler: para, arketip, eğlenceli istatistik, enflasyon, katkı.
2. Kullanıcı hangi kartı paylaşacağını kendisi seçer. "Hepsini paylaş" butonu yok.
3. Dört kart tipi: **Enflasyon** ("Mutfak enflasyonum %41. Seninki?") · **Takas** ("3 takasla ayda 340 TL") · **Arketip** ("Bakliyat Ustaları") · **Katkı** ("Bu yıl 27 ürünün içeriğini ilk ben okudum").
4. 1080×1920, büyük tipografi, tek renk arka plan, marka filigranı, QR/kısa link. Link açılınca web'de "kendi karneni çıkar" sayfası gelir (edinim).
5. Kişisel karşılaştırma ("seninki?") var, ama başka hanelerle sıralama/liderlik tablosu **yok** (utanç ve sınıf riski).

---

## 4. Retention döngüleri

### 4.1 Çekirdek döngü: haftalık hane ritmi
```
Pazar akşamı ─ PLAN ─▶ "Haftalık liste hazır: 14 ürün ≈ 2.350 TL, 2 takas önerisi" (web/mobil)
Hafta içi   ─ AL   ─▶ Ortak liste + rafta tarama (mobil)
Alışveriş sonrası ─▶ Fiş çek → 20 sn fiş karnesi (değişken ödül: "bu fiş haftanı nasıl etkiledi?")
Pazartesi sabahı ─ ÖĞREN ─▶ Haftalık karne bildirimi (tek sayı + 1 aksiyon)
Ay başı ─▶ Sepet Özeti + mutfak enflasyonu · Aralık ─▶ Sepet Wrapped
```
**Yatırım (Hook modelinin son adımı):** Her fiş, kişisel enflasyonu, takas kalitesini ve fiyat karşılaştırmasını iyileştirir. Bunu görünür kıl: **"Hane haritası %68 tamam: 4 fiş daha girersen enflasyonun kesinleşir."**

### 4.2 Fiş çekme alışkanlığı nasıl kurulur
- **Her fişe anında bir karşılık:** En az 1 yeni içgörü garanti edilir ("Bu fişte 2 ürüne başka bir markete göre fazla ödedin"). Fetch'teki "her fişe puan" ilkesinin para yerine bilgiyle karşılığı.
- **Öğrenilmiş zamanlama:** Fiş tarih ve saatlerinden hanenin alışveriş günü çıkarılır ("Cumartesi 11:00–13:00"). Hatırlatma o saatten 2 saat sonra gelir. Konum izni gerekmez.
- **Tek dokunuş:** Ana ekran widget'ı ("Fiş çek"), iOS kilit ekranı ve Android Quick Settings kısayolu.
- **Toplu ve geç giriş:** "Cüzdandaki 5 fişi art arda çek" (çoklu çekim), galeriden seçim ("dünkü fiş").
- **Pasif giriş:** Online siparişler için e-posta yönlendirme adresi (Expensify modeli). Gmail OAuth daha ağır bir izin ve KVKK yükü getirir; v2 sonrasına bırakılır. `[değerlendirme]`
- **Hane paylaşımı:** Fişi kim çekerse çeksin haneye düşer. İlerleme hane düzeyinde gösterilir ("Bu haftanın fişleri: 4/5"), **kim çekmediği gösterilmez**.
- **Tamamlanma çekimi, kayıp korkusu değil:** "Karnenin kesinleşmesi için 1 fiş kaldı" (Zeigarnik). "Serini kaybedeceksin" gibi bir mesaj asla kullanılmaz.

### 4.3 Ödül sistemi (para yerine)
| Ödül | Örnek | Neden güvenli |
|---|---|---|
| Tasarrufun görünürlüğü | Takas Kumbarası: "Bu ay 340 TL" | Para kişisel ve pozitif |
| İçgörü kilidi | 2. ay enflasyon, 3. ay trend, 12. ay Wrapped | İlerleme veriye bağlı, yemeğe değil |
| Katkı statüsü | "27 ürünün içeriğini ilk sen okudun" | Topluluk değeri |
| Hane başarısı | "Bu ay hanece şeker −%8" (sadece uygulama içinde) | Hane düzeyinde, kişi hedef alınmıyor |

Rozetler sadece **veri ve katkı davranışına** verilir ("İlk 10 fiş", "İlk ürün katkısı"). "Şekersiz hafta" gibi **yeme davranışına rozet yok**.

### 4.4 Streak'in sağlık uygulamasındaki riskleri ve öneri
- **Kanıt (iki yönlü):** Duolingo'da streak çok güçlü (yukarıdaki tablo). Ama sağlık/diyet uygulamalarında streak, rozet ve iyi/kötü renk kodlaması iç açlık-tokluk sinyallerinden kopmayı ve kompulsif takibi besleyebilir ([National Alliance for Eating Disorders](https://www.allianceforeatingdisorders.com/health-tracking-apps-and-disordered-eating/), [BJPsych Open nitel çalışma](https://www.cambridge.org/core/journals/bjpsych-open/article/effects-of-diet-and-fitness-apps-on-eating-disorder-behaviours-qualitative-study/2D1EE739D97AB3EFC6573835E4C527BD)). Bir boylamsal çalışmada genel bozuk yeme davranışı riski takibin 1. ayında arttı ([PMC11556259](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11556259/)). Nedensellik tartışmalı: semptomu olanlar bu uygulamaları daha çok kullanıyor olabilir ([NCHR](https://www.center4research.org/fitness-tracking-apps-eating-disorders/)).
- **Öneri:**
  1. **Günlük streak yok.** Yerine "Hane ritmi": son 8 haftanın ısı haritası. Kırılan bir sayı yok, sadece dolu ve boş kareler var. Tatil haftası otomatik işaretlenir.
  2. Metrik veri davranışını ölçer, yemeği değil.
  3. **Bildirim bütçesi haftada en fazla 3:** karne, plan ve bir olay bildirimi (tağşiş ya da fiyat). Kullanıcı ayarlayabilir. Duygusal şantaj yok ("Duo üzgün" tarzı mesajlar kullanılmaz).
  4. **"Sadece bütçe ve alerji" modu:** Şeker/tuz/UPF metrikleri tamamen gizlenir. Yeme bozukluğu geçmişi olanlar ya da bu metrikleri görmek istemeyenler için. Ayarlarda tek anahtar.
  5. Kişi bazlı tüketim takibi yok. Ölçülen şey hanenin **satın aldığı**, kimin ne yediği değil. Bu tasarım kararı riski yapısal olarak düşürür.

### 4.5 Ölçülecekler (final raporu için)
D1/W1/W4 retention · hane başına haftalık fiş · fiş→karne süresi (p50/p95) · fiş satırı eşleşme oranı · takas kabul oranı · 2. ay enflasyon kilidinin açılma oranı · paylaşım kartı üretim/paylaşım oranı. Faz 4'teki mini kullanıcı testinde 5–8 hane.

---

## 5. Web'in anlamlı rolü (mobilin kopyası değil)

Mobil **yakalama ve anlık karar** içindir: 5 saniyelik etkileşimler. Web **düşünme, planlama ve paylaşma** içindir: büyük ekranda, klavyeyle 5–20 dakikalık oturumlar.

| Web modülü | Ne yapılır | Neden web'de |
|---|---|---|
| **Hane Paneli** | Haftalık/aylık karne, trendler, sıralanabilir katkıcılar tablosu (market, kategori ve üye filtresiyle; üye filtresi sadece alerji/hedef çakışmaları için) | Çok boyutlu keşif küçük ekrana sığmaz |
| **Planlama Stüdyosu** | Doğal dille plan, kısıt çipleri, kaydırıcılar (bütçe, şeker hedefi, değişiklik sayısı), interaktif "sağlığın fiyatı" Pareto grafiği, market bölme; ardından "listeyi telefona gönder" | Optimizasyonun görünür yüzü. **Jüri için en güçlü ekran** |
| **Fiş Arşivi ve düzeltme** | Satır satır eşleştirme düzeltme, toplu onay, e-posta ile gelen faturalar | Klavyeyle 10 kat hızlı. Düzeltmeler veri kalitesine gider |
| **Fiyat ve Enflasyon** | Kişisel enflasyon ayrıntısı, ürün fiyat geçmişi, marketler arası karşılaştırma, gizli zam listesi | Tablo ve grafik yoğun |
| **Diyetisyenle paylaşım** | Süreli, salt-okunur link ya da PDF: "Son 8 hafta hane sepeti: şeker/tuz/UPF trendi, en büyük katkıcılar". Paylaşan her şeyi kontrol eder, süre dolunca link ölür, erişim loglanır | Ucuz ama değerli bir B2B2C tohumu (`01-ai-feature-havuzu.md` #23) |
| **Hane yönetimi** | Üyeler, davet, roller (yönetici / üye / çocuk profili), rızalar, veri indirme ve silme | KVKK hakları self-servis, okunaklı |
| **Wrapped landing** | Paylaşılan kart linki web'de açılır: "Kendi karneni çıkar" | Edinim hunisi |

**Admin** ayrı bir uygulamadır (moderasyon, karar izi, veri kalitesi); ayrıntısı `01-ai-feature-havuzu.md` §4'te.

---

## 6. Ana ekran haritası (bilgi mimarisi)

### Mobil (5 sekme)
| Sekme | İçerik |
|---|---|
| **1. Bugün** | Haftalık karnenin tek sayısı · kalan market bütçesi · önerilen tek aksiyon · liste kısayolu · bildirimler |
| **2. Tara** (ortada, büyük buton) | Tek kamera, üç mod: **Barkod · Fiş · Etiket** (hedef: otomatik algılama) · galeriden seç · çoklu fiş |
| **3. Liste** | Ortak haftalık liste · market modu · satır içi takas önerisi · "planı web'de aç" |
| **4. Sepet** | Haftalık/aylık karne · katkıcılar · takaslar ve kumbara · enflasyon · fiş arşivi · özetler/Wrapped |
| **5. Hane** | Üyeler ve profiller · hedefler · bütçe · mod ("sadece bütçe ve alerji") · bildirim bütçesi · rıza ve veri |

### Web (ana sayfalar)
`/panel` Hane Paneli · `/plan` Planlama Stüdyosu · `/fisler` Fiş Arşivi · `/fiyat` Fiyat ve Enflasyon · `/raporlar` Aylık özet, Wrapped, diyetisyen paylaşımı · `/hane` Üyeler, rıza, veri · `/r/{token}` salt-okunur paylaşım · `/w/{id}` Wrapped kartı landing

### Admin
`/admin/moderasyon` (ürün katkıları, etiket OCR onayı, fiş eşleştirme kuyruğu) · `/admin/karar-izi` (Decision Record arama) · `/admin/veri-kalitesi` (TR içindekiler kapsamı, eşleşme oranı, fiyat kapsaması, OCR güven dağılımı) · `/admin/kurallar` (alerjen sözlüğü, sürümler) · `/admin/llm` (maliyet, hata, eval) · `/admin/resmi-listeler` (tağşiş listesi içe aktarma ve eşleşme onayı)

---

## 7. Demo senaryosu (jüri önünde 5 dakika)

**Hikâye (kurgusal):** Aydın ailesi, Antalya Konyaaltı. **Selin** (39, öğretmen, alışverişi o yapıyor) · **Murat** (43; doktoru "şekere dikkat" demiş, uygulamada "şekeri azaltma hedefi" olarak var, tanı olarak değil) · **Ela** (9, fındık alerjisi) · **Can** (15). **Aylık market bütçesi 28.000 TL.** Karşılaştırma için: TÜRK-İŞ'in Ağustos 2026 açlık sınırı Ankara'da 4 kişilik aile için 37.388 TL ([TÜRK-İŞ](https://www.turkis.org.tr/turk-is-agustos-2026-aclik-ve-yoksulluk-siniri)). Yani aile gerçekten sıkışık. Rakam demo'da tek cümleyle geçer, üzerinde durulmaz.

**Hazırlık:** Ekip üyelerinin **gerçek fişleri** · 8 haftalık seed geçmiş · masada 3 gerçek ürün (biri fındıklı gofret, biri DB'de olmayan yerel bir ürün, biri alternatif) · iki telefon (Selin ve Murat) · projeksiyonda web · yedek video · mobil hotspot.

| Zaman | Ekran | Olay | Jüri anı |
|---|---|---|---|
| 0:00–0:30 | Telefon (slayt yok) | Problem tek cümle: "Selin'in her hafta üç sorusu var: Ela'ya dokunur mu, Murat'ın şekeri ne olur, ay sonu gelir mi?" | — |
| 0:30–1:15 | Mobil · **W1** | Selin fişi jüriye gösterir ve çeker. 20 saniyede karne: kişi başı şeker ve en büyük 3 katkıcı. Tanınmayan bir satır kaydırarak onaylanır. | ★1: Kağıt fişin 20 saniyede analize dönüşmesi, üstelik tanıyamadığını söyleyen dürüst bir sistem |
| 1:15–2:00 | Mobil · **W2** | Kaydırıcı 1 → 3 takas: "ayda 340 TL, %25 daha az şeker, Ela'nın listesiyle çakışma yok". Tek cümle teknik: "Bu bir ILP; en fazla 3 değişiklik, bütçe ve alerjen kısıtları." | ★2: Para ve sağlık aynı cümlede |
| 2:00–2:50 | Mobil (Murat) · **W3 + W11** | Fındıklı gofret taranır. Ela: çakışma. Murat: şekere etkisi. "Sepete eklersen 180 → 205 g". 4 TL ucuz bir alternatif çıkar. Sonra yerel ürün: "Doğrulanamadı" → etiket çekilir → 8 saniyede içindekiler ve vurgulu alerjenler. | ★3: "Bilmiyorum" diyebilen ve veriyi kendisi üreten sistem |
| 2:50–3:40 | Web (projeksiyon) · **W7 + W6 + W8 + W12** | Selin yazar: "Ela için fındıksız, Murat için şekeri azaltılmış, haftalık 6.500 TL". Kısıt çipleri belirir, liste oluşur. Pareto grafiği: "10 g daha az şeker = ayda +45 TL". Market bölme: A101 + Migros 86 TL ucuz. Murat'ın telefonunda liste canlı güncellenir. | ★4: Optimizasyon görünür (danışmanın alanı). LLM sadece anlıyor, karar vermiyor |
| 3:40–4:20 | Mobil · **W4 + W9** | Aylık özet: "Mutfak enflasyonunuz %41, TÜİK gıda %33,79", en büyük katkı zeytinyağı. Seed'den tetiklenen sakin bir bildirim: "Mart'ta aldığınız ürüne benzer isimli bir ürün bakanlık listesinde." | TR'nin gündelik gündemine dokunuyor |
| 4:20–4:45 | Mobil + QR · **W10** | Sepet Özeti kartı: "Bakliyat Ustaları · 3 takasla 4.120 TL". Ekrandaki QR'ı jüri kendi telefonuyla açar ve web landing'i görür. | ★5: Paylaşılabilir, "gerçek ürün" hissi |
| 4:45–5:00 | Admin | Murat'ın taramasının karar izi: kural v1.3, kaynak "etiket OCR", güven 0,92, zaman damgası. Kapanış: **"Tahmin etmiyoruz: bilmediğimizde söylüyoruz, bildiğimizde hesaplıyoruz."** | Hocaların geçen yılki eleştirisine (izlenebilirlik) doğrudan cevap |

**Demo riskleri ve önlemler:** OCR/LLM gecikmesi → demo fişleri için sıcak cache ve deterministik fallback · internet → hotspot, gerekirse yedek video · eşleşme hatası → demo ürünleri önceden DB'de · canlı senkron → iki cihaz aynı ağda, önceden test edilir.

---

## 8. Albeni riskleri, ton ve dil ilkeleri

### 8.1 Riskler
| # | Risk | Belirti | Önlem |
|---|---|---|---|
| R1 | **Diyet polisi hissi** | Her tarama bir yargı olur, kullanıcı uygulamayı açmaktan kaçınır (Yuka eleştirisi) | Seçenek dili, kırmızı sadece çakışmaya, ekranda tek alternatif |
| R2 | **Hane içi suçlama** | "Can'ın cipsleri şekerin %40'ı" → aile içi kavga aracı | Tüketim kişiye atfedilmez; sepet hanenin. Kişi bazlı sonuç yalnızca rafta alerji/hedef çakışması için |
| R3 | **Çocuk** | Çocuğa skor, "kötü yiyor" dili | Çocuk profili yalnızca kısıt taşır. Skor, kilo ve kişisel trend yok |
| R4 | **Yeme bozukluğu / ortoreksiya** | Kompulsif kontrol, "temiz" saplantısı | Kalori yok, streak yok, "sadece bütçe ve alerji" modu, "temiz beslenme" dili yok |
| R5 | **Bilgi yükü** | Nutri-Score, NOVA, şeker, tuz, UPF, fiyat, enflasyon aynı anda | Her ekranda bir kahraman sayı. Detay bir dokunuş ötede (progressive disclosure) |
| R6 | **Yanlış kesinlik** | Bulanık eşleşmeyi kesin rakam gibi sunmak | "≈", güven rozeti, kaynak rozeti ("etiket" / "tahmini") |
| R7 | **Tıbbi iddia** | "Prediyabetini yönet" | "Şeker azaltma hedefi", "bilgilendirme amaçlı" (`01-mevzuat-risk.md` §3) |
| R8 | **Paylaşımda ifşa** | Kartta çocuğun alerjisi görünür | Varsayılan kartta sağlık verisi yok (§3 kuralları) |
| R9 | **Siyasi hassasiyet** | TÜİK kıyası kavga konusuna dönüşür | Nötr dil, yöntem linki, "senin sepetin farklı" çerçevesi |
| R10 | **Sınıf ve utanç** | "Ucuz = sağlıksız" imaları, bütçeyi aşan "sağlıklı" öneriler | Bütçe hard kısıt. Önerilerde varsayılan "daha pahalı" olamaz. Liderlik tablosu yok |

### 8.2 Ton ilkeleri (Türkçe)
1. **Sepeti konuş, kişiyi değil.** ✗ "Çok fazla şeker tüketiyorsun." → ✓ "Bu haftaki sepette şekerin yarısı 2 üründen geliyor."
2. **Yargı değil seçenek.** ✗ "Bu ürün zararlı." → ✓ "Aynı rafta %40 daha az şekerli bir seçenek var, 3 TL de ucuz."
3. **"Güvenli" kelimesi yok, çakışma var.** ✗ "Ela için güvenli." → ✓ "Ela'nın listesiyle çakışma yok · etiket beyanına göre."
4. **Bilmediğini söyle ve yolu göster.** ✓ "Bu ürünün içeriğini doğrulayamadık. Etiketi çekersen 10 saniyede okuruz."
5. **Kayıp değil tamamlanma.** ✗ "Serini kaybetme!" → ✓ "Bu haftanın karnesi 1 fiş bekliyor."
6. **Somut, yerel, ölçülü sayı.** "340 TL", "%33,79" (Türkçe ondalık virgül), yaklaşık değerlerde "≈". En fazla bir ondalık basamak; TÜİK rakamı kaynağındaki gibi yazılır.
7. **Samimi ama laubali değil.** "Sen" dili (Papara/GetirFinans çizgisi), ölçülü emoji. Espri sadece özet/Wrapped'da ve kullanıcı "Esprili" seçerse. Sağlıkta "savage" mod yok.
8. **Renk dili.** Kırmızı = yalnızca alerjen/kısıt çakışması (bir gerçek bildiriyor). Besin kalitesi yeşil-sarı-turuncu ile gösterilir (Noom), kırmızı kullanılmaz. Gri = doğrulanamadı.
9. **Tıbbi fiil yok.** Yasak: *önler, tedavi eder, yönetir, güvenli, doktor onaylı, %100*. Kullanılır: *hedef, tercih, bilgi, beyan edilen*.
10. **Kısa.** Bildirim en fazla ~90 karakter ve tek aksiyon. Ekran başlığı en fazla 6 kelime.

### 8.3 Kelime tablosu
| Kullanma | Yerine |
|---|---|
| zararlı, kötü, sağlıksız | "daha yüksek şekerli/tuzlu", "sık alındığında dikkat" ya da sadece sayı |
| güvenli / güvenle tüketilebilir | "çakışma yok · etiket beyanına göre" |
| yasak, yememeli | (yok; seçenek sun) |
| temiz beslenme, hile, kaçamak, suçlu zevk | (yok) |
| diyet | hedef |
| hastalığını yönet | "şeker azaltma hedefi" |
| Serini kaybedeceksin! | "Karnen 1 fiş bekliyor." |
| Başarısız oldun / hedefi aştın | "Bu hafta hedefin biraz üstündeyiz, 1 takas farkı kapatır." |

### 8.4 Bildirim örnekleri
- ✓ "Haftalık karnen hazır: bu hafta sepette şeker %8 azaldı."
- ✓ "Cumartesi alışverişinin fişini atmak ister misin? 20 saniye sürer."
- ✓ "Zeytinyağı bu ay senin sepetinde %9 arttı. Daha uygun 2 seçenek var."
- ✗ "Ela'nın fındık alerjisi için 3 riskli ürün aldınız!" (suçlayıcı, korkutucu; kilit ekranında sağlık verisi ifşa ediyor)
- ✗ "Bu hafta çok şeker aldınız 😟"

---

## 9. Levent'e açık sorular

1. **Fiş v2'nin çekirdeği mi?** Veri raporunda fiş OCR "stretch" (🟡) olarak işaretlenmişti. Bu UX fişi merkeze koyuyor. Önerim: karar vermeden önce **20 gerçek TR fişiyle** eşleştirme doğruluğunu ölçen bir spike.
2. **Fiyat verisini fişten crowdsource etmek** kabul mü? (marketfiyati yazılı izni başvurusu paralel yürüyebilir.)
3. Persona olarak **"hanenin alışverişini yapan kişi"** uygun mu?
4. **Günlük streak olmaması** kararı onaylanıyor mu? Oyunlaştırma kapsamı nerede duracak?
5. Proje takvimi yıllık Wrapped'a yetişmiyor. Demo'da aylık "Sepet Özeti" + seed veri yeterli mi?
6. **Demo şehri:** Antalya örneği senden geldi. Ekip hangi şehirde, gerçek fişler nereden gelecek?
7. **Tağşiş listesi:** erişim ve format spike'ı yapılsın mı?
8. **Online sipariş girişi:** e-posta yönlendirme (hafif) mi, OAuth (ağır) mı, yoksa kapsam dışı mı?
9. **Ton seçimi** ("Sade / Esprili") olsun mu? Metin yükü ekibe ek iş getirir (Monzo'da 3 kişi 2.000+ satır yazmış).

---

## Kaynaklar (toplu)

**Wrapped ve özetler:** [TechCrunch — Wrapped 2025](https://techcrunch.com/2025/12/04/spotify-says-wrapped-2025-is-its-biggest-yet-with-200m-users-in-its-first-day) · [MBW](https://www.musicbusinessworldwide.com/spotify-wrapped-campaign-hit-200m-engaged-users-in-24-hours-a-19-yoy-increase/) · [Music Ally](https://musically.com/2025/12/05/spotify-wrapped-2025-attracted-over-200m-users-in-first-day/) · [Irrational Labs](https://irrationallabs.com/blog/spotify-wrapped-behavioral-science/) · [Monzo — Writing Year in Monzo 2024](https://monzo.com/blog/writing-year-in-monzo-2024) · [Monzo — How we built](https://monzo.com/blog/how-we-built-year-in-monzo-unlocking-the-data-magic) · [Monzo — 5 million Years](https://monzo.com/blog/how-we-wrote-5-million-years-in-monzo) · [Yemeksepeti 2025 özeti — DHA](https://www.dha.com.tr/gundem/yemeksepeti-2025-siparis-ozetini-acikladi-2787626) · [Strava Year in Sport](https://support.strava.com/en-us/articles/15401959-your-year-in-sport) · [road.cc — Year in Sport paywall](https://road.cc/content/news/strava-year-sport-now-only-subscribers-317425)

**Fintech / bütçe:** [Monzo Trends](https://monzo.com/us/blog/monzo-us-blog/trends) · [Monzo kategori hedefleri](https://monzo.com/us/blog/monzo-us-blog/trends-category-targets) · [Revolut analytics](https://help.revolut.com/en-US/help/accounts/budget-and-analytics/how-can-i-see-my-spending-and-income-analytics/) · [Papara Aylık Özet](https://blog.papara.com/aylik-ozet-ile-gercek-patron-sensin/) · [Papara harcama grafikleri](https://blog.papara.com/harcama-grafikleri-nasil-takip-edilir/) · [Papara Yuvarla](https://www.papara.com/faq/birikim-hesabi/birikim-hesabimdaki-yuvarla-ozelligi-nedir) · [Acorns Round-Ups](https://www.acorns.com/round-ups/) · [Copilot Money](https://www.copilot.money/) · [Penny Hoarder — Copilot](https://www.thepennyhoarder.com/budgeting/budgeting-copilot-money-review/) · [Finny — Copilot](https://getfinny.app/blog/copilot-money-review-2026) · [GetirFinans — UX Design Awards 2026](https://ux-design-awards.com/winners/2026-1-getirfinans-digital-onboarding)

**Gıda / market:** [Kroger OptUP](https://www.kroger.com/health/nutrition/optup) · [OptUP FAQ](https://www.kroger.com/hc/help/faqs/health-and-wellness/optup) · [Kroger blog](https://www.kroger.com/blog/health/opt-up) · [Grocery Dive — Kroger Health](https://www.grocerydive.com/news/kroger-health-healthcare-grocery-food-medicine/725196/) · [Instacart Smart Shop / Health Tags](https://company.instacart.com/pressreleases/instacart-launches-ai-powered-smart-shop-and-new-features-that-make-healthy-choices-easy) · [Instacart Family carts](https://www.instacart.com/help/section/4179348463) · [Yuka — GreenChoice](https://about.greenchoicenow.com/resources/yuka-app) · [Yuka neden kayıt](https://help.yuka.io/l/en/article/knm8htuqdh-why-register) · [Fig App Store](https://apps.apple.com/us/app/fig-food-scanner-guide/id1564434726) · [Fetch eReceipts](https://fetch.com/blog/fetch-tips-tricks/fetch-and-ereceipts-earn-rewards-when-online-shopping) · [RaftLabs — Fetch](https://www.raftlabs.com/blog/how-to-create-an-app-like-fetch-rewards) · [Expensify](https://use.expensify.com/receipt-scanning-app) · [GroceryTrack](https://grocerytrack.food/blog/best-grocery-tracking-apps-2026) · [Too Good To Go](https://apps.apple.com/us/app/too-good-to-go-end-food-waste/id1060683933) · [Noom renk sistemi](https://www.noom.com/support/faqs/using-the-app/logging-and-tracking/food-and-water/2025/10/how-nooms-food-color-system-works/) · [Nutri-Score RCT (loyalty card)](https://link.springer.com/article/10.1007/s11747-020-00723-5) · [Nutri-Score sosyal norm müdahalesi](https://www.sciencedirect.com/science/article/abs/pii/S0306919224000575)

**Retention / oyunlaştırma / riskler:** [Deconstructor of Fun — Duolingo streaks](https://duolingo.deconstructoroffun.com/mechanics/streaks) · [Lenny's — Duolingo streaks özeti](https://www.recall.it/summary/business/behind-the-product-duolingo-streaks-or-jackson-shuttleworth-group-pm-retention-team) · [Duolingo Friend Streak](https://blog.duolingo.com/friend-streak/) · [The Decision Lab — Streak Creep](https://thedecisionlab.com/insights/consumer-insights/streak-creep-the-perils-of-too-much-gamification) · [Web Designer Depot — Duolingo bildirimleri](https://webdesignerdepot.com/the-art-of-duolingo-notifications-the-subtle-manipulation-of-language-learners/) · [National Alliance for Eating Disorders](https://www.allianceforeatingdisorders.com/health-tracking-apps-and-disordered-eating/) · [BJPsych Open](https://www.cambridge.org/core/journals/bjpsych-open/article/effects-of-diet-and-fitness-apps-on-eating-disorder-behaviours-qualitative-study/2D1EE739D97AB3EFC6573835E4C527BD) · [PMC11556259 — boylamsal çalışma](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11556259/) · [NCHR](https://www.center4research.org/fitness-tracking-apps-eating-disorders/) · [NPR — food scanner apps](https://www.npr.org/2025/05/26/nx-s1-5391915/phone-apps-food-nutrition-health) · [Abby Langer — Yuka](https://abbylangernutrition.com/yuka-app-review-scan-or-scam/)

**Onboarding / izin:** [Appcues — mobile onboarding](https://www.appcues.com/blog/mobile-onboarding) · [Appcues — aha moment](https://www.appcues.com/blog/aha-moment-examples) · [Cal AI — ScreensDesign](https://screensdesign.com/showcase/cal-ai-calorie-tracker) · [Spotify Research — cold start](https://research.atspotify.com/2025/9/generalized-user-representations-for-large-scale-recommendations) · [Apple — HealthKit yetkilendirme](https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data) · [Sage Bionetworks — just-in-time permission](https://sage-bionetworks.github.io/DesignSystem/just-in-time-permission.html)

**TR verisi:** [TÜİK Ağustos 2026 — Alomaliye](https://www.alomaliye.com/2026/09/03/enflasyon-rakamlari-tufe-agustos-2026/) · [TÜRK-İŞ Ağustos 2026](https://www.turkis.org.tr/turk-is-agustos-2026-aclik-ve-yoksulluk-siniri) · [Cumhuriyet — kişisel enflasyon](https://www.cumhuriyet.com.tr/ekonomi/hissedilen-enflasyon-kisisel-enflasyonunuzu-hesaplayin-2066383) · [enflasyonum (GitHub)](https://github.com/umutseve4/enflasyonum) · [TCMB enflasyon hesaplayıcı](https://herkesicin.tcmb.gov.tr/wps/wcm/connect/ekonomi/hie/icerik/enflasyon+hesaplayici) · [Güvenilir Gıda — Taklit/Tağşiş](https://guvenilirgida.tarimorman.gov.tr/GuvenilirGida/gkd/TaklitVeyaTagsis) · [Tarım ve Orman — anlık paylaşım duyurusu](https://www.tarimorman.gov.tr/Haber/6409/Taklit-Ve-Hileli-Gida-Listeleri-Artik-Anlik-Paylasilacak)
