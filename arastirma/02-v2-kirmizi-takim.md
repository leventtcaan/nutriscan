Kırmızı takım değerlendirmesi — 2026-09-24

---
title: 02 — v2 konsepti kırmızı takım değerlendirmesi (NutriScan)
tarih: 2026-09-24
durum: HAM — Levent'le netleştirilmedi. Karar değil; kararlar `plan/kararlar.md`'ye Levent onayıyla girer.
girdi: `00-sentez.md`, `01-*.md` (5 rapor), `kaynak/CSE491_Project_Proposal_Template.docx`, web taraması (kaynaklar en altta)
---

> Etiketler: **[kaynak]** = dış kaynağa dayanıyor (link en altta). **[değerlendirme]** = kırmızı takımın yargısı, kanıt değil.
> "v2" = hanenin gıda kararları için kapalı döngü (PLAN → AL → ÖĞREN) karar destek sistemi: fiş/fatura + raf barkodu girdisi; sepet karnesi, kişisel gıda enflasyonu, Akıllı Takas MILP (Pareto, exact vs NSGA-II, gölge fiyat), rafta hane kararı, tağşiş uyarısı, doğal dil → kısıt, haftalık liste + market seçimi, tercih öğrenme, Sepet Wrapped; admin: eşleştirme moderasyonu, karar izi, audit log, LLM izleme.

## 0. Tek paragraf hüküm

v2, ilk tezin "sığ" sorununu çözüyor ama yerine **"geniş ve dağınık"** sorununu getiriyor: 4 alan (beslenme analitiği, fiyat/enflasyon, optimizasyon, gıda güvenliği) × 12+ özellik. Jüri ilk 5 dakikada "hangisi derin?" diye sorar ve cevap hiçbir yerde yazılı değil. Asıl kırılma noktası **girdi**: v2 bütün döngüyü kullanıcının ödülsüz fiş çekmesine bağlıyor. Oysa Türkiye'de fiş yükleyen 3,2 milyon kişi bunu **para karşılığı** yapıyor (Qumpara). ÖKC fişinde barkod yok, eşleştirme bulanık. Satın alma tüketim değil. Fiyat verisinin yasal kaynağı yok. Optimizasyon çekirdeği sağlam, danışmana da tam uyuyor. Ama tek sepet boyutunda problem küçük, bu yüzden "exact vs NSGA-II" kıyası saman adama dönebilir. Ayrıca MILP'te "LP gölge fiyatı" tanımsız. **Onarım:** Döngü korunsun ama omurga tersine çevrilsin. **PLAN (haftalık liste) birincil girdi** olsun, fiş ikincil ve opsiyonel olsun. Derinlik tek yerde toplansın: **hane sepeti + market seçimi çok amaçlı MILP'i**, onu besleyen **doğrulanmış katalog** ve **fiş satırı eşleştirme**. Tağşiş, Wrapped ve Gmail/online fatura kesilsin; kişisel enflasyon ve NL→kısıt "could" olsun. Bu haliyle v2 proposal'a **girmez**; 3 değişiklikle girer (§5).

---

## 1. Dört (+1) persona: en sert 24 soru

Sütunlar: **v2 cevaplıyor mu?** (Evet / Kısmen / Hayır) · **En iyi cevap** · **Cevap yoksa konseptte ne değişmeli**.

### (a) Optimizasyon/OR hocası — Arş. Gör. Dr. T. Y. Alkan

| # | Soru (onun ağzından) | v2? | En iyi cevap | Değişiklik |
|---|---|---|---|---|
| 1 | "Modeli tahtaya yazın. Karar değişkeni, amaç, kısıt. Bu Stigler'in diet problemi artı Maillot/Darmon'un 'gözlenen diyetten minimum sapma' LP'si değil mi? Yenilik nerede?" | **Kısmen** (MILP adı var, formülasyon yok) | "Evet, temel literatür bu, kaynakçada var. Bizim farkımız dört yerde: (i) jenerik gıda değil **SKU + tamsayı paket + zincirin ürün yelpazesi**, (ii) **hane üyesi bazlı hard alerjen** kısıtı (kalem–üye tüketim matrisi), (iii) **≤k takas kardinalite kısıtı** (davranışsal kabul edilebilirlik), (iv) **market seçimi**, yani Uncapacitated Facility Location (UFL) alt yapısı. UFL genel halde NP-zor." | Proposal'a formülasyon yazılı girsin (taslak aşağıda, §1-ek). Maillot 2010 ve Stigler 1945 "Similar Systems" tablosunda yer alsın. |
| 2 | "Örnek boyutu ne? 40 kalem × 10 aday = 400 binary. CP-SAT bunu milisaniyede optimal çözer. NSGA-II'yi neden koşuyorsunuz, saman adam mı?" | **Hayır** | "Tek amaçlı küçük örnekte GA'yı kıyaslamıyoruz. Kıyas iki rejimde: (1) **3 amaçlı tam Pareto cephesi**: ε-constraint her ızgara noktası için bir MILP demek, nokta sayısı karesel büyür. Etkileşimli kullanımda **gecikme bütçesi** var (p95 ≤ 1 s); aynı süre bütçesinde hypervolume'e bakıyoruz. (2) **Ölçek**: 20–200 kalem, 3–30 şube, çok haftalık ufuk, sentetik örnek üreteci. Exact'in koptuğu yeri arıyoruz. Exact her yerde kazanırsa bunu dürüstçe raporlarız." | Deney tasarımı proposal'da yazılı olsun: örnek üreteci, parametre ızgarası, ≥30 seed, eşit süre bütçesi, hypervolume + IGD + optimalite açığı. GA'da hard kısıtlar için **onarım (repair) operatörü** tasarlansın. **[değerlendirme]** Gerçek Antalya örnekleri küçük kalacak (fiyatlar çoğunlukla zincir bazında aynı, yani etkin mağaza sayısı ≈ zincir sayısı ≈ 5–7). GA'nın gerekçesi gecikme ve ölçek deneyinden gelmek zorunda. |
| 3 | "MILP'te dual yok. 'Sağlığın fiyatı' dediğiniz gölge fiyat hangi problemin duali?" | **Hayır** (v2 "LP gölge fiyatı" diyor, model MILP) | Üç yol var: (i) LP gevşetmesinin duali (yaklaşık), (ii) tamsayılar sabitlenip yeniden çözülen LP'nin duali (yerel), (iii) **parametrik analiz**: sağlık kısıtının sağ tarafı adım adım sıkılır, her adımda MILP çözülür, ampirik marjinal maliyet eğrisi (basamaklı) çıkar. Üçü kıyaslanır. Kullanıcıya gösterilen: "şekeri %20 azaltmak bu hafta +38 TL". | "LP gölge fiyatı = sağlığın fiyatı" ifadesi **"parametrik marjinal maliyet (LP duali ile karşılaştırmalı)"** olarak değişsin. CSE 413 hafta 4 bağı korunur, iddia dürüstleşir. |
| 4 | "Amaçtaki 'sağlık' ne? Ağırlıkları kim koydu? Nutri-Score mu, kendi uydurduğunuz skor mu?" | **Kısmen** (TÜBER'e göre karne var) | Skor icat edilmez. Sağlık **kısıt** olarak girer (TÜBER 2022 / WHO: serbest şeker enerjinin <%10'u, tuz <5 g/gün; TÜBER'deki kesin değerler doğrulanmalı). Çok amaçlıda ayrı bir amaç olur, **skalarlaştırma yok**, bu yüzden ağırlık keyfiliği de yok. Oran kısıtları doğrusallaştırılır: Σ(şeker_j − ε·kcal_j/1000)·x_j ≤ 0. | Ağırlıklı toplam amaç yasak (tasarım ilkesi). Besin profili için yayımlanmış bir algoritma seçilsin (ör. Nutri-Score 2023 spesifikasyonu). Kapsaması raporlansın (OFF'ta 869-prefix ürünlerin besin tablosu ~%60 dolu). |
| 5 | "Girdi belirsiz. Fiş satırı %70 güvenle eşleşmiş bir ürün alerjen kısıtında nasıl davranıyor?" | **Hayır** | İki katmanlı havuz. **Öneriler** yalnız *doğrulanmış katalogdan* gelir (içindekiler insan onaylı). **Mevcut sepet** (baz) belirsiz olabilir. İçeriği doğrulanmamış ürün, ilgili üye için x_j = 0 olur (konservatif). Belirsizliği şans kısıtıyla (chance constraint) modellemek stretch hedef. | "Doğrulanmış katalog" kavramı tasarımın merkezine konsun (§2, halka 2). |
| 6 | "Tercih öğrenme dediğiniz ne? Kabul/red verisinden amaç ağırlığı mı çıkarıyorsunuz? O inverse optimization; kaç gözlemle?" | **Kısmen** (adı var, yöntemi yok) | MVP'de basit ve konveks bir yöntem: takas çifti ceza terimi d_ij, kabul/red verisiyle L1-düzenlileştirilmiş lojistik modelle güncellenir (SGD, CSE 413 hafta 10). Veri azken popülasyon önceliği kullanılır. Inverse optimization future work. | "Tercih öğrenme" iddiası küçültülsün; "should" önceliğe insin. |

**§1-ek — Proposal'a girecek formülasyon taslağı [değerlendirme]**
- Kümeler: I liste kalemleri, J aday ürünler (doğrulanmış katalog + mevcut ürünler), S mağazalar, H hane üyeleri.
- Değişkenler: y_ij∈{0,1} (kalem i, ürün j ile karşılanır), x_js∈ℤ≥0 (j'den s'de alınan paket), z_s∈{0,1} (s'ye gidilir).
- Amaçlar:
  - f₁ = Σ d_ij·y_ij (sapma; d_i,cur(i) = 0)
  - f₂ = Σ p_js·x_js + Σ c_s·z_s (fiyat + mağaza gitme maliyeti, UFL yapısı)
  - f₃ = sağlık yoğunluğu (ε-kısıt olarak)
- Kısıtlar:
  - Σ_j y_ij = 1
  - Σ_i Σ_{j≠cur(i)} y_ij ≤ k
  - y_ij = 0, eğer ∃h∈tüketen(i) ve j∈Alerjen(h)
  - Σ_s x_js ≥ ihtiyaç_i·y_ij
  - x_js ≤ M·a_js·z_s (a_js: zincir yelpazesinde var mı)
  - Σ_s z_s ≤ m
  - bütçe
  - TÜBER oran kısıtları
- Sınıf: çok amaçlı MILP, UFL alt yapısı. Exact: OR-Tools CP-SAT/SCIP + ε-constraint. Sezgisel: NSGA-II (jMetal) + onarım operatörü. Doktora bağı: kapsama/konum problemi ↔ market seçimi.

### (b) Yazılım mühendisliği hocası

| # | Soru | v2? | En iyi cevap | Değişiklik |
|---|---|---|---|---|
| 7 | "Geçen yıl admin ve loglar yetersizdi. Bu sefer 'yeterli'nin ölçütü ne?" | **Kısmen** (karar izi, audit, LLM izleme listelenmiş) | Üç katmanlı log var: teknik, domain event, append-only audit. Her tarama ve **her optimizasyon çağrısı** bir Decision Record üretir: girdi özeti, çözücü durumu (OPTIMAL/FEASIBLE), gap, süre, bağlayıcı kısıtlar. Admin'de "bu takas neden önerildi" sorusu **yeniden oynatılabilir** (replay). Kabul testi: kullanıcıya gösterilen her çıktıdan 3 tıkta veri kaynağına inilebilmeli. | NFR olarak yazılsın. Logging ve audit 1. sprintte kurulsun, sona bırakılmasın. |
| 8 | "Mobil + web + admin + backend + solver + OCR/LLM hattı. 3 kişi, Java biliyorsunuz. Frontend deneyiminiz? Mimari ne?" | **Hayır** | Modüler monolit: Spring Boot, modül sınırları Spring Modulith veya ArchUnit ile korunur. Solver için ya Java OR-Tools içeride (Python yalnız araştırma notebook'u) ya da ayrı Python servisi: ADR ile karar verilir. Mobil tek kod tabanı (RN/Expo veya Flutter, ekip kararı). Web = admin (hazır şablon: React-Admin/Refine) + tanıtım sitesi + salt-okunur hane paneli. | **Web kapsamı proposal'da daraltılsın.** "Web" şartının tam bir kullanıcı uygulaması isteyip istemediği danışmana sorulsun. **[değerlendirme]** 3 tam istemci yazmak bu ekibin en büyük zaman deliği. |
| 9 | "Optimizasyonun doğru çalıştığını nasıl test ediyorsunuz?" | **Hayır** | Property-based ve metamorfik testler: (i) hiçbir çıktı üye alerjeni içermez (binlerce rastgele örnekte invariant), (ii) bütçe artınca amaç kötüleşmez, (iii) k artınca sapma-amaç cephesi kötüleşmez, (iv) küçük örneklerde brute force ile eşitlik, (v) Java ve Python modeli aynı örnekte aynı optimumu verir. Eşleştirme ve OCR için golden set regresyonu CI'da koşar. | Test stratejisi proposal'ın 6. bölümüne girsin. |
| 10 | "Kodu AI agent'lar yazıyor. Kod kalitesini nasıl garanti ediyorsunuz, kodu siz anlıyor musunuz?" | **Hayır** | Ortak AGENTS.md/CLAUDE.md standardı var. Her PR'da insan review zorunlu (yazan ≠ onaylayan). CI kapıları: test, lint, coverage eşiği, mimari kurallar. ADR'ler tutulur. **AI kullanım beyanı** yapılır (Alkan'ın izlence politikası beyanı zorunlu tutuyor). Sunumda her üye kendi modülünü savunur. | Proposal'da "süreç ve kalite güvencesi" alt başlığı olsun (yol haritası Faz 5). |
| 11 | "'Canlıya alındı' diyorsunuz. Kaç kullanıcı, hangi SLA, veri nerede, KVKK?" | **Hayır** | Sunucu Türkiye'de barındırılır; alışveriş geçmişi de özel nitelikli veri gibi korunur (glutensiz alım çölyak bilgisini ele verir). LLM'e yalnız **maskelenmiş** fiş satırı ve ürün metni gider; kart son haneleri, şube, saat gitmez. Rıza metinleri ayrı olur (2026/347). Şubat–Mayıs arası 20–40 hanelik Antalya betası yapılır. p95 ve uptime hedefi konur, yedekleme yapılır. | NFR'lere ve risk tablosuna eklensin. |

### (c) Veri/ML hocası

| # | Soru | v2? | En iyi cevap | Değişiklik |
|---|---|---|---|---|
| 12 | "Fiş satırı → ürün eşleştirmenin doğruluğu ne? Veri seti nerede, nasıl ölçüyorsunuz?" | **Hayır** | Kendi etiketli setimizi kurarız: ≥300 fiş / ~3.000 satır, 3–4 zincir. Test seti **zincir bazında ayrılır** (görülmemiş zincire genelleme). Metrikler: top-1/top-5, **kapsama @ %95 hassasiyet** (otomatik kabul oranı), kalibrasyon (ECE). Yöntem: aday getirme (trigram/BM25 + embedding) → yeniden sıralama (cross-encoder veya LLM) → eşik altı kullanıcıya "bu mu?" ya da admin kuyruğu → onaylar zincir sözlüğüne girer (active learning). Endüstride aynı desen var: %98 hassasiyet eşiğinde otomatik kabul, kapsama %68 → %77 [kaynak: arXiv 2608.25037]. | Eşleştirme, v2'nin **ML çekirdeği** olarak açıkça tanımlansın. Başarı kriteri sayısal olsun. Türkçe fiş satırı veri seti bu taramada bulunamadı (derin arama yapılmadı). Açık veri seti olarak yayımlanırsa katkı olur (KVKK maskelemesiyle). |
| 13 | "Satın alma tüketim değil. 'Kişi başı şeker' metriğiniz tam olarak neyi ölçüyor?" | **Hayır** | Kişi başı değil, **satın alınan 1000 kcal başına** yoğunluk, 4 haftalık kayan pencerede. Literatür: fiş tabanlı HEI ile 24 saatlik hatırlama arasında orta uyum var (Appelhans ve ark. 2017, ρc = 0,57). Ama bu ölçüm hane düzeyinde; dışarıda yeme, israf ve üyeler arası paylaşım hariç [kaynak]. Türkiye'de evde kişi başı ~93 kg/yıl gıda israfı var (UNEP 2021) [kaynak]. | Metrik tanımı değişsin. Arayüzde "tüketim" veya "yediğin" dili olmasın; "sepetin" denir. |
| 14 | "Topluluk fiyat verisi kaç haneden gelecek, hangi yoğunlukta? Kişisel enflasyonu nasıl hesaplıyorsunuz: ürün değişimi, paket küçülmesi, seyrek tekrar?" | **Hayır** | Eşleşmiş model (matched-model) zincirleme endeks (Jevons/Törnqvist) kullanılır. Birim fiyat (TL/kg) paket küçülmesini yakalar. Sonuç TÜİK gıda TÜFE ile kıyaslanır (Ağustos 2026 yıllık %33,79) [kaynak]. Güven aralığı raporlanır. **Ama** 20–40 haneyle "topluluk fiyatı" istatistiksel olarak ince kalır. | "Topluluk fiyat verisi" iddiası küçülsün: hanenin kendi fiyat geçmişi + ekip katalog fiyatı (+ izin gelirse marketfiyati). Kişisel enflasyon **could** olsun. Kategori ağırlıklı kişisel enflasyon hesaplayıcıları zaten var [kaynak]; bizim farkımız ürün düzeyi, onu da veri seyrekliği sınırlar. |
| 15 | "Doğal dilden kısıt: doğruluk nasıl ölçülüyor, yanlışsa ne oluyor?" | **Kısmen** ("karar LLM'e bırakılmaz" ilkesi var) | Kapalı bir DSL var (10–12 kısıt tipi, JSON şema). Şema doğrulanır, "Anladığım: …" diye geri okunur, kullanıcı onaylar. 150–200 Türkçe ifadelik test setinde tam eşleşme doğruluğu ölçülür. LLM modeli kurmuyor, **yalnız parametre dolduruyor**. Genel NL→optimizasyon modeli hâlâ zayıf (OptiMUS-0.3, IndustryOR'da %37) [kaynak]; biz bu yüzden kasıtlı olarak dar tutuyoruz. | Form her zaman var. NL → **could** (demo parlatıcısı). |
| 16 | "İşe yaradığını nasıl kanıtlayacaksınız? Kontrol grubu, etik kurul?" | **Hayır** | 491'de offline değerlendirme: sentetik örnekler + ekip haneleri. 492'de beta: 2 hafta baz + 4 hafta müdahale (SaltSwitch deseni: n = 66, 6 hafta, tuz alımında 0,7 g/gün/kişi azalma) [kaynak]. Birincil metrikler: **takas kabul oranı** ve 1000 kcal başına şeker/tuz değişimi. Sanal market RCT'si (n = 947): takas sunmak sepet tuzunu %4–13 düşürdü; büyük farklı takaslar kabulü düşürmedi [kaynak: Payne Riches 2019]. | Başarı kriterleri bölümüne girsin. Etik kurul gereği danışmana sorulsun. |

### (d) Kuşkucu gerçek kullanıcı: Antalya'da çalışan anne

| # | Soru | v2? | En iyi cevap | Değişiklik |
|---|---|---|---|---|
| 17 | "Her alışverişten sonra fişin fotoğrafını mı çekeceğim? Fiş 60 cm, yarısı silik, iki çocukla kasadayım." | **Hayır** (v2 pasif takibe yaslanıyor) | "Hayır. Zaten yazdığın listeyi uygulamaya yaz ya da söyle; uygulama listeyi senin marketine göre düzeltir. Fiş isteğe bağlı: 'bu ay ne kadar gitti' merakın için." Uzun fiş parça parça çekilir, otomatik birleştirilir. | **Girdi hiyerarşisi ters dönsün: liste > raf barkodu > fiş.** Türkiye'de insanlar fiş yüklüyor ama para karşılığı (Qumpara, 3,2M kullanıcı) [kaynak]. |
| 18 | "Ben BİM'e gidiyorum. Önerdiğin ürün BİM'de yoksa ne işime yarar?" | **Kısmen** (market seçimi var) | Takas havuzu kullanıcının zincirinin yelpazesiyle sınırlanır (a_js kısıtı). İndirim zincirlerinde özel marka payı yüksek (A101 ~%50, ŞOK ~%35) [kaynak], yani zincirler arası birebir ürün eşleşmesi zayıf. | Model kısıtı olsun. Pilot zincir sayısı 1–2 ile sınırlansın (Levent karar verir). |
| 19 | "'Sepet karnesi' verip çocuğuma ne yedirdiğimi mi yargılayacaksın?" | **Hayır** | Harf notu yok, yargı yok, seçenek var: "1 değişiklikle bu hafta şeker %18 azalır, sepet 12 TL ucuzlar." | "Karne" adı ve not sistemi kalksın. UX ilkesi: her metrik bir eylemle gelir. |
| 20 | "Bana ayda kaç lira kazandırır? Verimi kime satıyorsunuz?" | **Kısmen** | Ana ekranda somut TL tasarruf (önerilen vs gerçek). Veri satışı yok, veri Türkiye'de, tek dokunuşla silinir. | Değer önerisinde **TL birinci**, sağlık ikinci. Gizlilik taahhüdü onboarding'de. |

### (e) Health-tech yatırımcısı

| # | Soru | v2? | En iyi cevap | Değişiklik |
|---|---|---|---|---|
| 21 | "Qumpara 3,2M kişiden ürün düzeyinde fiş verisi toplayıp markalara satıyor; Migros Money geçmiş alışverişleri zaten gösteriyor. Hendeğiniz ne?" | **Hayır** | Dürüst cevap: fiş okuma hendek değil. Hendek adayları: (i) doğrulanmış Türkçe içerik + alerjen kataloğu (OFF'a geri besleniyor), (ii) hane kısıt modeli + alışveriş **öncesi** optimizasyon, (iii) güven (veri satmıyoruz). Qumpara'nın müşterisi marka; bizim müşterimiz hane. | "Similar Systems" tablosuna Qumpara, Migros Money ve Kroger OptUP eklensin. OptUP ayrı uygulama olarak 2021'de kapandı, özellikleri ana uygulamaya gömüldü [kaynak]. |
| 22 | "Kim para öder? Türkiye'de tüketici gıda uygulamasına abonelik ödemez." | **Hayır** | Bitirme için şart değil. Rapordaki "ekonomik kısıt/sürdürülebilirlik" paragrafına: B2C freemium zor. Olası yollar: zincire white-label "sağlıklı + ucuz sepet" motoru (Kroger dersi: özellik perakendecinin uygulamasında yaşar), işveren wellness, diyetisyen B2B2C. | Bir paragraf yeter, kapsamı büyütmesin. |
| 23 | "Haftalık aktif kullanım nedeni ne? Sağlık uygulamaları 30 günde kullanıcı kaybeder." | **Kısmen** (haftalık liste var) | Tutundurucu "Wrapped" değil, **haftalık liste**. Tetik: hafta başı "listen hazır, 3 takasla 85 TL tasarruf". | Beta'da W4 retention ölçülsün. Wrapped kesilsin. |
| 24 | "Regülasyon: sağlık iddiası, tıbbi cihaz sınırı, tağşiş uyarısıyla marka itibarı?" | **Kısmen** | Wellness dili kullanılır, "güvenli" kelimesi yok, LLM'e profil gitmez. Tağşiş listesi **parti/seri** bazlı [kaynak]; fişte parti numarası yok. Marka düzeyinde geriye dönük uyarı yanlış pozitif üretir, haksız rekabet/itibar riski doğurur. | Tağşiş geriye dönük uyarısı **kesilsin** (future work, ya da ürün sayfasında yalnız kaynaklı bilgi linki). |

**Skor:** 24 sorunun 0'ında "Evet", 9'unda "Kısmen", 15'inde "Hayır". **[değerlendirme]** Bu kavram için normal; proposal henüz yazılmadı. Ama "Hayır"ların çoğu **tek cümlelik tasarım kararıyla** kapanıyor. Pahalı olanlar sadece 3: girdi (#17), eşleştirme (#12), GA gerekçesi (#2).

---

## 2. En zayıf 5 halka ve onarımları

### Halka 1 — Girdi: kullanıcı fiş çekmez
- **Kanıt:** Türkiye'de fiş yükleme davranışı var ama **ödülle** besleniyor: Qumpara 3,2M kullanıcıya puan/nakit veriyor, veriyi markalara "shopper insight" diye satıyor [kaynak]. Kroger'in sepet sağlık puanı uygulaması OptUP ayrı uygulama olarak yaşamadı (2021) [kaynak]. Online sipariş faturalarını otomatik çekmek için Gmail okuma izni "restricted scope" sayılıyor: yıllık CASA güvenlik denetimi gerekiyor, ~500–4.500 $ ve üstü, en ağır seviyede pentest [kaynak].
- **Onarım:**
  1. Birincil girdi **haftalık liste** olsun (yazı, ses, geçen haftanın kopyası).
  2. Rafta barkod ikincil olsun (liste kalemini SKU'ya bağlar).
  3. Fiş üçüncül ve opsiyonel olsun: planlananla alınanı karşılaştırır, ÖĞREN adımını besler.
  4. Online fatura için Gmail entegrasyonu olmasın; kullanıcı PDF'i "paylaş" menüsüyle uygulamaya gönderir (could).
  5. Demo verisi ekip haneleri + beta'dan gelir, 491'den itibaren her hafta fiş biriktirilir.

### Halka 2 — Eşleştirme doğruluğu ve doğrulanmış katalog darboğazı
- **Kanıt:** GİB taslak kılavuzuna göre ÖKC fişinde zorunlu satır içeriği yalnız "mal cinsi, KDV oranı, KDV dahil tutar"; **barkod/GTIN alanı yok** [kaynak]. Satırlar kısaltılmış ve zincire özgü. Alerjen hard kısıtı içindekiler verisi istiyor, oysa OFF'ta Türkiye ürünlerinin yalnız %15–25'inde içindekiler var (`01-veri-fizibilite.md`).
- **Onarım:**
  1. **Doğrulanmış katalog v0:** pilot zincir(ler)de en çok alınan ~300 SKU. Ekip fotoğraflar, vision LLM çıkarır, insan onaylar. Kaba hesap: ~2 dk/ürün, yani 10–15 saat. Takas önerileri **yalnız** bu katalogdan gelir.
  2. **Eşleştirme hattı:** retrieve → rerank → eşik → kullanıcıya tek dokunuşla "bu mu?" / admin kuyruğu → zincir sözlüğü.
  3. **Geri düşüş:** SKU bulunamazsa satır kategori düzeyinde tutulur ("süt 1 L", TürKomp değeri). Sepet metriği yine hesaplanır, takas önerilmez.
  4. **Ölçüm:** kapsama @ %95 hassasiyet, zincir bazında.
  5. **İzlenecek gelişme:** aynı taslak kılavuz, ÖKC'den düzenlenen e-Belge'lerde QR'ın belgeye erişim/doğrulama bağlantısı içereceğini söylüyor. Yürürlüğe girerse e-Arşiv faturalı alışverişlerde yapılandırılmış satır verisine yol açabilir. Taslak, dayanak yapma.

### Halka 3 — Satın alma ≠ tüketim
- **Kanıt:** Fiş tabanlı diyet kalitesi ile gerçek alım arasındaki uyum orta düzeyde (ρc = 0,57), ölçüm hane düzeyinde; dışarıda yeme ve israf dahil değil [kaynak]. Türkiye'de evde kişi başı ~93 kg/yıl israf var [kaynak]. Yüksek enflasyonda **stoklama** da bir ayın sepetini bozar. **[değerlendirme]**
- **Onarım:**
  1. Metrik = satın alınan 1000 kcal başına şeker/tuz/ultra-işlenmiş payı, 4 haftalık kayan pencerede.
  2. Kişi başı gösterim yok; kişi hedefleri yalnız **plan** tarafında kısıt olarak kullanılır.
  3. Dil "sepetin", "yediğin" değil.
  4. Raporda bu sınırlılık bir paragrafla açıkça yazılır. MÜDEK "gerçekçi kısıt" + dürüstlük puanı getirir.

### Halka 4 — Fiyat verisi
- **Kanıt:** marketfiyati.org.tr kullanım koşulları yazılı izin istiyor (`01-veri-fizibilite.md`). Topluluk fişleri 20–40 haneyle seyrek ve gecikmeli. Kategori ağırlıklı kişisel enflasyon hesaplayıcıları zaten var [kaynak].
- **Onarım:**
  1. **Ekim'de** TÜBİTAK BİLGEM'e akademik kullanım izni başvurusu yapılsın (danışman imzasıyla).
  2. İzin gelene kadar fiyat = hanenin kendi fiş geçmişi + katalog v0 fiyatları. Katalog fiyatları ekipçe 2 haftada bir güncellenir, eskime tarihi gösterilir.
  3. Model fiyat belirsizliğine karşı sağlam olsun: fiyat aralığı ve "fiyat X gün önce" etiketi.
  4. Kişisel enflasyon **could**: veri yeterse 492'de bir ekran.

### Halka 5 — Kapsam patlaması ve derinliğin dağılması
- **Kanıt:** 12+ özellik × 3 istemci. CSE 492'de **kodlama vize haftasından önce bitmek zorunda** (`01-danisman-bitirme.md`). Bu da bahar döneminde gerçek geliştirme penceresinin ~8–9 hafta olduğu anlamına geliyor. **[değerlendirme]**
- **Onarım:** **Tek omurga kuralı.** Omurga = "hane sepeti karar motoru" (Akıllı Takas + market seçimi). Her özellik ya bu motoru **besler** (liste, barkod, fiş, katalog) ya da motorun sonucunu **gösterir/açıklar** (takas ekranı, sağlığın fiyatı, karar izi). İkisini de yapmayan özellik kesilir ya da future work'e gider (§3 tablosu).

---

## 3. Kapsam gerçekçiliği

### 3.1 Kapasite
- 3 kişi × 12–15 saat/hafta × ~32 hafta ≈ **1.150–1.450 kişi-saat**. Buradan düşülecekler: Ocak finalleri, Mart ve Mayıs bayramları, 491/492 raporları, sunumlar, form ve toplantı yükü (~%20). **Net ~950–1.150 saat.** **[değerlendirme]**
- AI agent'lar CRUD ve boilerplate'i hızlandırır. Entegrasyonu, veri etiketlemeyi, deploy'u, debug'ı ve deney koşmayı hızlandırmaz.
- **Sert takvim gerçeği:** 492'de vize öncesi "kodlama tamam", rapor ve demo videosu sınavdan ≥10 gün önce. Pratikte **Nisan başı feature freeze**.

### 3.2 Özellik sınıflandırması ve karar

| Özellik | Sınıf | Karar | Not |
|---|---|---|---|
| Akıllı Takas MILP (tek amaç: sapma; bütçe, ≤k, üye alerjeni, zincir yelpazesi) | **Derinlik** | **491 çekirdek** | OR-Tools; formülasyon + testler |
| Çok amaçlı Pareto: ε-constraint vs NSGA-II, gecikme bütçesi, ölçek deneyi | **Derinlik** | 491: notebook + deney v0 · 492: üründe | Ara rapor ve final raporunun bel kemiği |
| "Sağlığın fiyatı" (parametrik marjinal maliyet + LP duali) | Derinlik + albeni | 491 notebook · 492 ekran | Demo anı: kaydırıcı → TL |
| Market seçimi (UFL-lite, ≤2 market) | **Derinlik** (danışmanın alanı) | 492 | Fiyat verisine bağlı; izin yoksa zincir düzeyinde |
| Haftalık liste (yazı; ses could) | Albeni + **girdi omurgası** | **491** | Bütün döngü buradan başlar |
| Rafta barkod → hane üyesi bazlı karar + listeye/sepete etkisi + alternatif | Albeni (SWE mirası, yeniden yazılır) | **491** | Deterministik; "güvenli" kelimesi yok |
| Doğrulanmış katalog v0 (~300 SKU) | Derinlik (veri) | **491** | Her şeyin önkoşulu |
| Fiş → satır → eşleştirme | **Derinlik (ML)** | 491: veri seti ≥100 fiş + baseline ölçüm · 492: üretim hattı + moderasyon | Opsiyonel girdi |
| Admin: karar izi + audit log + eşleştirme moderasyonu | **Derinlik (SWE)** | **491'den itibaren** | Geçen yılki eleştiriye doğrudan cevap |
| LLM izleme | SWE (hafif) | 492, minimal | LLM yalnız 2 yerde (fiş çıkarımı, açıklama); abartma |
| Sepet göstergesi (1000 kcal başına, "karne" değil) | Albeni + analiz | 492 | 491'de metodoloji yazılır |
| Tercih öğrenme (takas cezası güncelleme) | Derinlik iddiası, veri az | 492 should, basit | Inverse opt. future work |
| Topluluk fiyat verisi | Girdi | 492 should | İddia küçük tutulur |
| Kişisel gıda enflasyonu | Albeni | 492 **could** | Veri yeterse |
| Doğal dil → kısıt | Albeni (demo) | 492 **could** | Form her zaman var |
| Online sipariş faturası (Gmail) | Gürültü (şimdilik) | **Kes** → PDF paylaşımı could | CASA maliyeti |
| Taklit/tağşiş geriye dönük uyarı | Gürültü + hukuki risk | **Kes** (future work) | Parti bazlı liste, fişte parti yok |
| Sepet Wrapped | Gürültü | **Kes** | Haziran'da boş vakit olmaz |

### 3.3 CSE 491 sonu (Ocak 2027) — "çalışan prototip" sınırı
**Var:**
- Spring Boot modüler monolit, auth, hane (davetli rıza), structured logging, Decision Record, audit log.
- CI/CD + staging (Türkiye'de).
- Mobil: liste oluştur → "Takas öner" (tek amaçlı MILP, açıklamalı) → rafta barkodla hane üyesi kararı.
- Doğrulanmış katalog v0 (~300 SKU, 1 pilot zincir).
- Admin v0: karar izi görüntüleyici + audit log + katalog onay ekranı.
- Araştırma paketi: yazılı formülasyon, Python notebook'ta ε-constraint vs NSGA-II ilk deney (sentetik), parametrik "sağlığın fiyatı" eğrisi.
- Fiş veri seti v0 (≥100 fiş, etiketli) + baseline eşleştirme ölçümü (ör. top-1, kapsama@%95).

**Yok:** fiş üretim hattı, market seçimi, Pareto ekranı, web kullanıcı paneli, NL.

**Demo senaryosu (Ocak):** "Çocuk fındık alerjik, bütçe 1.200 TL. Liste gir, 3 takas öner, 64 TL tasarruf + şeker −%15, rafta bir ürünü okut, admin'de o önerinin karar izi."

### 3.4 CSE 492 sonu (Haziran 2027) — "canlı ürün" sınırı
**Nisan başı feature freeze'e kadar:**
- Çok amaçlı Pareto üründe (gecikme bütçeli).
- Sağlığın fiyatı ekranı.
- Market seçimi (≤2 market).
- Fiş hattı v1 (maskeleme → çıkarım → eşleştirme → kullanıcı onayı / admin kuyruğu).
- Sepet göstergesi.
- Takas cezası güncelleme.
- Web: admin + tanıtım sitesi + salt-okunur hane paneli.

**Nisan–Mayıs:**
- 20–40 hanelik Antalya betası (2 hafta baz + 4 hafta müdahale).
- Final deneyler: ölçek, 30 seed, istatistik testi.
- Bug bash.

**Haziran:** rapor, poster, demo videosu, İngilizce prova. **Yeni özellik yok.**

---

## 4. Alternatif çerçeveler (aynı çekirdek alan)

### Çerçeve A — "Plan-önce hane sepeti optimizasyonu" (Liste → Optimize → Market → Raf)
- **Ne:** Hane haftalık listesini girer. Sistem, hanedeki herkesin kısıtları (alerjen hard, TÜBER oranları), bütçe ve seçilen zincir(ler)in yelpazesi altında **en az sapmayla** takasları, paket boyutlarını ve gidilecek market(ler)i önerir. Rafta barkod son kontroldür. Fiş yalnız "plan vs gerçek" karşılaştırması ve öğrenme için vardır.
- **Derinlik:** çok amaçlı MILP + UFL alt yapısı, exact vs NSGA-II (gecikme ve ölçek), parametrik sağlığın fiyatı, metamorfik test.
- **Neden güçlü:**
  - Karar **alışverişten önce** veriliyor; takas müdahalesinin işe yaradığı an bu [kaynak: Payne Riches 2019].
  - Kullanıcının girdi yükü düşük: liste zaten var olan bir alışkanlık.
  - Danışmanın doktorası (kapsama/konum) ve CSE 413 ile birebir örtüşüyor.
- **Zayıf yanı:**
  - Fiyat ve yelpaze verisi problemi aynen duruyor.
  - "Liste yazan hane" varsayımı doğrulanmalı.
  - v2 kadar "pasif sihir" hissi yok.

### Çerçeve B — "Fiş-merkezli hane gıda gözlemevi"
- **Ne:** Türk market fişleri için etiketli satır→ürün veri seti ve kalibre edilmiş eşleştirme modeli (çekimser kalabilen, active learning). Üstüne hane satın alma kalitesi (1000 kcal başına) ve ürün düzeyinde kişisel/semt gıda enflasyonu endeksi. Optimizasyon yalnız basit takas önerisi düzeyinde.
- **Derinlik:** varlık çözümleme (entity resolution) ML'i, endeks teorisi, istatistik; muhtemelen ilk açık Türkçe fiş satırı veri seti (bu taramada rastlanmadı).
- **Neden güçlü:** Veri katkısı gerçek ve ölçülebilir. Pasif çalışıyor. Enflasyon gündemiyle "why now" çok güçlü (gıda yıllık %33,79).
- **Zayıf yanı:**
  - Danışman uyumu orta (veri madenciliği evet, OR zayıf).
  - Girdi yükü en yüksek; Qumpara ödüllü rakip olarak orada.
  - Fiş görüntüleri KVKK açısından hassas.
  - "Karmaşık mühendislik problemi" argümanı optimizasyondan daha zor savunulur.

### Dürüst kıyas (1 = zayıf, 5 = güçlü) [değerlendirme]

| Kriter | v2 (şu hali) | A: Plan-önce | B: Gözlemevi |
|---|---|---|---|
| Jüri "complexity" (derinlik yoğunluğu) | 3 (var ama dağınık) | **5** | 4 |
| Danışman uyumu (OR + öneri) | 4 | **5** | 3 |
| Kullanıcı girdi yükü (düşük = iyi) | 2 | **4** | 2 |
| Veri riski (fiyat, eşleştirme, katalog) | 2 | 3 | 2 |
| 8 ay × 3 kişiye sığma | 1 | **4** | 3 |
| Demo gücü | **5** | 4 | 3 |
| "SWE dersinin üstüne ne eklediniz?" | **5** | 4 | 4 |
| Özgünlük (TR'de) | 3 | 3 | **4** |
| Canlıda gerçekten kullanılma olasılığı | 2 | **3** | 2 |
| **Toplam** | 27 | **35** | 27 |

**Hüküm:**
- **v2 kaybediyor.** Nedeni fikrin kötülüğü değil, **iki çerçevenin birleşimi** olması: A'nın optimizasyon omurgası ile B'nin veri omurgasını aynı 8 aya sığdırmaya çalışıyor, girdiyi de B'nin en zayıf halkasına (fiş) bağlıyor.
- **v2'nin kazandığı yer** anlatı ve demo: kapalı döngü, "SWE dersinden fark" sorusunun en iyi cevabı.
- **Öneri:** v2'nin döngü anlatısı korunur, **omurga A olur**, B'den ince bir dilim alınır: fiş opsiyonel, eşleştirme ölçülü ML modülü olarak kalır.
- Önerilen tek cümle: *"NutriScan, hanenin haftalık alışveriş listesini, her üyenin sağlık ve alerji kısıtlarıyla bütçeyi aynı anda gözeterek en az değişiklikle iyileştiren ve bu iyileştirmenin bedelini TL olarak gösteren, raf ve fiş verisiyle kendini düzelten bir karar destek sistemidir."*

---

## 5. Son hüküm

**v2 bu haliyle proposal'a girmez.** Girerse jüri ve danışman ilk turda "odak yok, derinlik nerede, girdi nereden" diye parçalar. Proposal'ın 4–6 sayfalık formatı da 12 özelliği taşıyamaz.

### Girmeden önce 3 değişiklik
1. **Omurgayı ve girdiyi ters çevir (Çerçeve A).**
   - Problem tanımı "hanenin haftalık sepet kararı" olsun.
   - Birincil girdi liste olsun, sonra barkod, en son (opsiyonel) fiş.
   - Proposal'daki özellik listesi yerine tek problem cümlesi + tek sistem diyagramı konsun.
   - Tağşiş, Wrapped ve Gmail/online fatura çıkarılıp "Out of scope" bölümüne yazılsın. Kişisel enflasyon ve NL→kısıt "could" olsun.
2. **Derinliği yazılı ve ölçülebilir yap.**
   - §1-ek'teki formülasyon proposal'a girsin.
   - Deney tasarımı yazılsın: ε-constraint vs NSGA-II, gecikme bütçesi, ölçek ızgarası, 30 seed, hypervolume/IGD/gap.
   - "LP gölge fiyatı" yerine "parametrik marjinal maliyet" denilsin.
   - Sayısal başarı kriterleri: eşleştirmede kapsama @ %95 hassasiyet · 0 alerjen ihlali (property test) · p95 öneri süresi ≤ 1 s · beta'da takas kabul oranı ve 1000 kcal başına şeker/tuz değişimi.
3. **Veri gerçeğini proposal'dan önce bağla.**
   - Pilot zincir(ler) seçilsin (1–2, **Levent karar verir**).
   - Doğrulanmış katalog v0 planı yazılsın (~300 SKU, kim, kaç saat).
   - TÜBİTAK BİLGEM'e fiyat verisi izin başvurusu danışmanla Ekim'de gönderilsin.
   - Metrik tanımı "1000 kcal başına sepet" olsun.
   - "Similar Systems" tablosuna Qumpara, Migros Money, Kroger OptUP, FoodSwitch/SaltSwitch ve Maillot/Darmon eklensin.

### Danışmana (cuma) sorulacak 3 soru
- "Web" şartı tam kullanıcı uygulaması mı istiyor, yoksa admin + tanıtım sitesi + salt-okunur panel yeter mi?
- Solver Java OR-Tools'ta mı olsun, yoksa Python mikroservis mi (CSE 413 dili Python)?
- Beta kullanıcı çalışması etik kurul gerektiriyor mu?

### Levent'e açık sorular (varsayım yapılmadı)
- Pilot zincir hangisi? Ekip haneleri hangi zincirlerden alışveriş yapıyor?
- Hedef hane "herhangi bir aile" mi, yoksa "en az bir üyesinde alerji/diyet kısıtı olan aile" mi? (A çerçevesinde ikisi de çalışır; demo ve beta işe alımı değişir.)
- Ekip bu dönem CSE 413 alıyor mu? (Deneyin ödevle çakışması ve çift kullanım politikası.)

> Not (koordinatöre): Bu dosya karar değil. `DURUM.md` ve `plan/kararlar.md` güncellemesi Levent onayından sonra yapılmalı.

---

## Kaynaklar
- Appelhans ve ark. 2017 / satın alma verisinin diyet kalitesi göstergesi olarak geçerliliği: [Supreme Nudge, BJN (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11646671/) · [r-HPI, Eur J Nutr](https://link.springer.com/article/10.1007/s00394-022-02962-4) · [SHoPPER (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6390355/)
- Minimum sapmalı diyet optimizasyonu (Maillot/Darmon): [Frontiers in Nutrition 2018 derlemesi](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full) · [Donkor 2023 sistematik derleme](https://onlinelibrary.wiley.com/doi/10.1155/2023/1271115)
- SaltSwitch RCT (Eyles 2017): [Eur J Prev Cardiol / PubMed](https://pubmed.ncbi.nlm.nih.gov/28631933/) · Payne Riches ve ark. 2019, sanal markette takas RCT: [Appetite (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6335438)
- Kişisel enflasyon araçları: [TCMB Enflasyon Hesaplayıcı](https://herkesicin.tcmb.gov.tr/wps/wcm/connect/ekonomi/hie/icerik/enflasyon+hesaplayici) · [Cumhuriyet kişisel enflasyon hesaplayıcı](https://www.cumhuriyet.com.tr/ekonomi/hissedilen-enflasyon-kisisel-enflasyonunuzu-hesaplayin-2066383)
- TÜİK Ağustos 2026 gıda enflasyonu (%33,79): [Capital](https://www.capital.com.tr/haberler/tum-haberler/tuik-2026-yili-agustos-ayi-enflasyon-rakamlarini-acikladi) · [SBB](https://www.sbb.gov.tr/2026-yili-agustos-ayi-tuketici-ve-uretici-fiyat-gelismeleri-aciklandi/)
- Gmail restricted scope ve CASA: [Google — restricted scope verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification) · [DeepStrike CASA 2026](https://deepstrike.io/blog/google-casa-security-assessment-2025)
- Taklit/tağşiş listesi (parti/seri bazlı, Eylül 2026 güncellemesi): [CNN Türk](https://www.cnnturk.com/turkiye/galeri/tarim-ve-orman-bakanligi-taklit-tagsis-listesi-2026-sahte-hileli-urunler-sorgulama-ekrani-guvenilirgida-tarimorman-gov-tr-2161082) · [gzt](https://www.gzt.com/gundem/tarim-bakanligi-taklit-tagsis-listesi-2026-bakanlik-ifsa-listesi-yeni-markalar-gundem-haberleri-4228723)
- Gıda israfı Türkiye (UNEP 2021, 93 kg/kişi/yıl evde): [Tarım ve Orman Bakanlığı](https://www.tarimorman.gov.tr/Sayfalar/Detay.aspx?SayfaId=77) · [UNEP Food Waste Index 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024)
- Özel marka payları (A101 ~%50, ŞOK ~%35): [USDA FAS Turkey Retail Foods](https://apps.fas.usda.gov/newgainapi/api/report/downloadreportbyfilename?filename=Retail+Foods_Ankara_Turkey_6-10-2019.pdf) (2019 raporu, güncelliği doğrulanmalı) · [ESM Magazine](https://www.esmmagazine.com/retail/top-5-supermarket-retail-chains-in-turkiye-238806)
- Ürün eşleştirme / fiş satırı: [Retrieve, Match, Escalate — arXiv 2608.25037](https://arxiv.org/pdf/2608.25037) · [Philippine receipt item names (Springer)](https://link.springer.com/chapter/10.1007/978-3-031-62281-6_26) · [ReceiptSense](https://arxiv.org/html/2406.04493v2)
- NL → optimizasyon: [OptiMUS-0.3](https://arxiv.org/pdf/2407.19633) · [LM4OPT](https://arxiv.org/pdf/2403.01342)
- Qumpara (3,2M kullanıcı; markalara fiş verisi): [App Store](https://apps.apple.com/tr/app/qumpara-fi%C5%9Fini-g%C3%B6nder-kazan/id1179401931?l=tr) · [Markalar için Qumpara](https://qumpara.com/markalar-icin-qumpara) · [Fiş yükleyerek kazanma rehberi](https://qumpara.com/rehber/fis-yukleyerek-para-kazanma)
- Migros Money (geçmiş alışveriş detayları): [App Store](https://apps.apple.com/us/app/money-migros-kampanya-finans/id1541353571)
- Kroger OptUP (2021'de ayrı uygulama olarak kapatıldı): [AppBrain](https://www.appbrain.com/app/optup/com.kroger.mobile.healthyshopper) · [Kroger](https://www.kroger.com/health/nutrition/optup)
- GİB YN ÖKC Fiş ve e-Belge Formatları Teknik Kılavuzu (taslak, 16.12.2025): [PDF](https://ynokc.gib.gov.tr/UploadedFiles/Files/yn-okc-fis-ve-e-belge-formatlari-kilavuz_taslak_16122025.pdf)
- İç kaynaklar: `arastirma/00-sentez.md`, `01-danisman-bitirme.md` (CSE 491/492 takvimi, CSE 413, P1–P7), `01-veri-fizibilite.md` (OFF TR kapsamı, marketfiyati ToS, fiş OCR), `01-mevzuat-risk.md` (KVKK, tıbbi cihaz), `01-rakip-pazar.md`, `01-ai-feature-havuzu.md`, `kaynak/CSE491_Project_Proposal_Template.docx`
