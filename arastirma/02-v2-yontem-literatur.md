# 02 — v2 Yöntem ve Literatür: "Akıllı Takas" ve kapalı döngü (PLAN → AL → ÖĞREN)

> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24**
> Web + Europe PMC + Crossref ile tarandı. DOI'lerin hepsi Crossref'te ya da yayıncı sayfasında görüldü. Birincil metni açılamayan yerlerde not var.
> Kısaltmalar: **DOĞRULANMADI** = künye ya da sayı birincil kaynaktan teyit edilemedi. **[yorum]** = bizim çıkarımımız. **[sentetik]** = bizim ürettiğimiz deney verisi, gerçek veri değil.
> Önceki rapor `01-danisman-bitirme.md` §4'te P1–P7 problem havuzu ve Java çözücü tablosu vardı. Burada tekrar edilmedi, yalnızca v2 bağlamında derinleştirildi. **Akıllı Takas = P2 ile P3'ün birleşimi, P6'nın kapalı döngüsü ve P5'in uzantısı.**

---

## 0. Beş cümlelik özet

1. Beslenme bilimi "mevcut diyetten en az sapmayla yeterliliğe ulaşma" problemini 2010'dan beri doğrusal programlamayla çözüyor (Maillot/Darmon ekolü). Bizim yaptığımız, bunu **bireysel tüketim anketinden hanenin gerçek fişine** ve **gıda grubundan barkodlu ürüne** taşımak.
2. Swap RCT'lerinde önerilen takasların yalnız **%13–33'ü kabul ediliyor**. Besin kazancı büyüdükçe kabul **düşüyor** (OR 0,81 / SD). Benzer ürün önerildiğinde kabul **2,2–2,8 kat** artıyor. Bu yüzden "en fazla k takas" ve "kabul olasılığı" modelin çekirdeği olmalı; süs değil.
3. Satın alma verisinden hane düzeyinde hesaplanabilen, doğrulanmış skorlar var: GPQI, Healthy Trolley Index (fişten), HPI/r-HPI (yalnız harcama payıyla) ve FSAm-NPS DI (Nutri-Score tabanlı). **Optimize ettiğimiz skorla değerlendirdiğimiz skor farklı olmalı.**
4. LLM'in serbestçe optimizasyon modeli yazması hâlâ güvenilir değil: benchmark'ların kendisinde bile %8–54 hata var, temizlenmiş setlerde en iyi yöntemler %60–94 doğrulukta. Bizim problemimiz daha dar. Doğru mimari şu: **LLM → şema-sınırlı ara temsil (IR) → deterministik doğrulayıcı → derleyici → çözücü**. Sert güvenlik kısıtları **LLM'den değil profilden** gelir.
5. Formülasyon **kardinalite kısıtlı, çok boyutlu, çoktan seçmeli sırt çantası (MMKP) tipi bir 0-1 MILP**. Tipik boyutta (60 satır × 20 aday) sentetik testte SCIP ~0,01 s, CP-SAT ~0,08 s sürdü. Yani **exact çözüm çekirdekte yetiyor**. Sezgiselin anlamlı olduğu yerler 3-amaçlı cephe ve market seçimi uzantısı. Deney tasarımı bunu dürüstçe göstermeli.

---

## 1. Bireysel diyet modelleme: "gözlenen diyetten minimum sapma"

### 1.1 Temel çalışmalar
| Çalışma | Ne yaptı | Bize ne veriyor |
|---|---|---|
| **Maillot, Vieux, Amiot, Darmon (2010)** AJCN 91(2):421–430 · [doi:10.3945/ajcn.2009.28426](https://doi.org/10.3945/ajcn.2009.28426) | INCA anketindeki her yetişkin (n=1171) için izo-kalorik bir LP kuruldu. Model 32 besin önerisini karşılarken **gözlenen diyetten en az sapıyor**. Özetteki ifade: "In half the modeled diets, <5 of the foods usually consumed were replaced." | **k ≈ 5** için ampirik dayanak. Bireysel modelleme paradigmasının kurucu makalesi. |
| **Maillot ve ark. (2017)** PLOS ONE 12:e0174679 · [doi:10.1371/journal.pone.0174679](https://doi.org/10.1371/journal.pone.0174679) | "İzo-maliyet" modelleri: diyetin maliyeti gözlenen maliyete sabitlendi. Her başlangıç maliyetinde yeterli diyet bulunabildi. Serbest maliyetli modelde maliyet ort. +0,22 €/gün arttı ve günlük maliyeti 3,85 €'nun altında olanlarda sistematik olarak yükseldi. | **"Bütçeyi aşmadan"** kısıtının doğrudan literatür karşılığı. Düşük bütçede zorlaşma → olursuzluk (infeasibility) yönetimi gerekli. |
| **Lluch ve ark. (2017)** Nutrients 9(2):162 · [doi:10.3390/nu9020162](https://doi.org/10.3390/nu9020162) | 1719 yetişkin, 33 besin. Serbest şekeri %10'un üstünde olanlar (%41) ayrıca modellendi. Model repertuvardaki besinleri tercih ediyor ve repertuvar dışı besin eklenmesini kontrol ediyor. | Kişinin "repertuvarı" = bizde **fişten gelen sepet**. Repertuvar dışı ürün eklemeyi sınırlama fikri. |
| **Gazan ve ark. (2018)** Adv Nutr 9(5):602–616 · [doi:10.1093/advances/nmy049](https://doi.org/10.1093/advances/nmy049) · [PMC6140431](https://pmc.ncbi.nlm.nih.gov/articles/PMC6140431/) | Diyet optimizasyonu derlemesi. Karesel sapma küçük değişiklikleri çok sayıda besine yayıyor. Yüzde sapma daha az besinde daha büyük değişiklik üretiyor. Kabul edilebilirlik kısıtları: porsiyon ve sıklık üst sınırları, grup min/max, ilişki kısıtları (ekmek–reçel). | Amaç fonksiyonu seçimi bir **davranış seçimidir**: az ama büyük değişiklik mi, çok ama küçük değişiklik mi? |
| **Schäfer ve ark. (2025)** PLOS ONE 20:e0313347 · [doi:10.1371/journal.pone.0313347](https://doi.org/10.1371/journal.pone.0313347) | Almanya 2024 FBDG. **Dört amaç fonksiyonu karşılaştırıldı.** Değişen grup sayısı: linear-relative 46, linear-absolute 78, squared-relative 167, squared-absolute 248. Kabul sınırı olarak gözlenen alımın P5–P95'i kullanıldı. | Sapma ölçüsünün **seyreklik (sparsity)** etkisini ölçen en net kanıt. L1-göreli az sayıda değişiklik üretiyor, bu da takas mantığına uyuyor. |
| **Okubo ve ark. (2015)** Nutr J 14:57 · [doi:10.1186/s12937-015-0047-7](https://doi.org/10.1186/s12937-015-0047-7) | Japonya. Amaç: $\sum_i \lvert x_i - x_i^{obs}\rvert / x_i^{obs}$. Mutlak değer, pozitif ve negatif sapma değişkenleriyle doğrusallaştırıldı (goal programming). | Formülün açık yazıldığı kaynak. |
| **Tyszler, Kramer, Blonk (2016)** Int J LCA 21:701–709 · [doi:10.1007/s11367-015-0981-9](https://doi.org/10.1007/s11367-015-0981-9) | Ceza skoru = değişen porsiyon sayısı × o besinin önceki tüketim miktarının normalizasyonu. Mantık: çok tüketilen besini değiştirmek daha "pahalı". | Satır bazlı **popülerlik ağırlıklı sapma**. |
| **Gerdessen & de Vries (2015)** EJCN 69:1272–1278 · [doi:10.1038/ejcn.2015.56](https://doi.org/10.1038/ejcn.2015.56) | Goal programming'de başarı fonksiyonunun (achievement function) sonucu nasıl değiştirdiği. | Hedef sapmalarının ağırlıklandırılması. |
| **Optifood** (Daelmans ve ark. 2013 · [doi:10.1111/mcn.12083](https://onlinelibrary.wiley.com/doi/10.1111/mcn.12083)) | LP + goal programming: tüm besin açıklarının toplamını minimize ediyor. 100% RNI'ye ulaşılamayan "problem nutrients" raporlanıyor. | **Olursuzlukta ne raporlanacağı:** "bu bütçe ve bu kısıtlarla şu besin hedefi tutmuyor". |

### 1.2 Formülasyon kalıpları (bizim için özet)
- **Sapma ölçüsü.** Gözlenen miktar $x^{0}_i$, yeni miktar $x_i$ olsun.
  - L1-göreli: $\min \sum_i (u_i^+ + u_i^-)/x_i^0$, $x_i - x_i^0 = u_i^+ - u_i^-$.
  - Karesel: QP.
  - Takas bağlamında sapma ürün değişimi olduğu için ikili (binary) değişkenle ifade edilir: $\sum d_{\ell j} x_{\ell j}$. Burada $d$, "ne kadar farklı bir ürüne geçiliyor" bilgisini taşır. **[yorum]** Bu, L1-göreli ailesinin 0-1 karşılığı ve seyreklik $\sum x \le k$ ile açıkça kontrol ediliyor.
- **Kabul edilebilirlik.** Üç yol var: ürün ve grup başına üst sınır (anket P90/P95 ya da gözlenenin %115'i), grup payı bandı (P5–P95), porsiyon sınırı. **[yorum]** Bizde bunların karşılığı: aday kümesi $J_\ell$ (aynı veya komşu kategori), grup enerji payı bandı ve izo-enerji kısıtı.
- **İzo-enerji.** Enerji sabit tutulur, yoksa model "daha az gıda al" diyerek sağlığı "iyileştirir".
- **Maliyet.** Serbest maliyet, izo-maliyet ya da bütçe üst sınırı.

---

## 2. Healthy swap müdahaleleri: kabul oranları ve k'nin gerekçesi

| Çalışma | Ortam, n | Kabul / kullanım | Etki | Modele ne katıyor |
|---|---|---|---|---|
| **Forwood ve ark. (2015)** IJBNPA 12 · [doi:10.1186/s12966-015-0241-1](https://doi.org/10.1186/s12966-015-0241-1) | Deneysel online market, n=1610 | Ortalama 12,36 üründe 4,1 takas önerildi. Medyan 1 takas kabul edildi (IQR 0–2). Katılımcıların %47,1'i hiç kabul etmedi. Seçim anında öneri, ödemedekinden daha çok kabul gördü (OR 1,22). Kabul kategoriye göre %6 (taze tavuk) ile %36 (makarna/pirinç) arasında değişti. **Enerji yoğunluğu kazancı büyük olan takas daha az kabul gördü: OR 0,81/SD.** | Grup düzeyinde enerji yoğunluğu değişmedi. Kabul edilen her takas enerji yoğunluğunu −24 kJ/100 g düşürdü. | **Kabul olasılığı, besin sıçramasıyla azalır.** Bu, "maksimum sağlık" ile "maksimum kabul" arasında bir trade-off olduğu anlamına gelir. |
| **Koutoukidis ve ark. (2019)** IJBNPA 16 · [doi:10.1186/s12966-019-0810-9](https://doi.org/10.1186/s12966-019-0810-9) | Deneysel online market, 2×2 tasarım, n=1088 | Yalnız takas grubu: %63'ü en az bir takas kabul etti. Kabul oranı medyanı %14,3 (IQR 0–28,6). Takası isteyenler %76. | SFA'da kontrole göre −2,0 (%95 GA −3,3; −0,6). Birim: sepet enerjisinde SFA %'si, kontrol %25,7. | Kabul düşük ama etki anlamlı. Kullanıcı özelliği istiyor. |
| **Payne Riches ve ark. (2019)** Appetite 133:378–386 · [doi:10.1016/j.appet.2018.11.028](https://doi.org/10.1016/j.appet.2018.11.028) | Deneysel online market, hipertansif, n=947 | **Önerilen takasların %33'ü kabul edildi.** Kabul edilen "çok daha az tuzlu" takasların %30'u farklı alt kategoriden geldi. | Tuz: −%4 ve −%13. Gruplar arası fark −%9. | Kategori dışı takas kabul oranını düşürmedi. $J_\ell$ **komşu kategoriye** genişletilebilir. |
| **Bunten ve ark. (2021)** PLOS ONE 16:e0246455 · [doi:10.1371/journal.pone.0246455](https://doi.org/10.1371/journal.pone.0246455) | Simülasyon online market, n=713 | **%12,91 (292/2262).** Sağlık, maliyet ve sosyal norm çerçeveleri arasında fark yok. | — | Mesaj çerçevesi değil, **teklifin kendisi** önemli. |
| **Schruff-Lim ve ark. (2024)** Appetite 194:107158 · [doi:10.1016/j.appet.2023.107158](https://doi.org/10.1016/j.appet.2023.107158) | Simülasyon market, n=428 | Benzer öneri, benzemeyen öneriye göre daha çok kabul gördü: OR 2,24. Karışık öneri: OR 2,78. | Sepet FSA skoru −1,7 (d=−0,48). Nutri-Score etiketine ek fayda sağladı. | **Benzerlik → kabul.** $d_{\ell j}$ ve $\pi_{\ell j}$ için doğrudan parametre kaynağı. |
| **Jansen, van Kleef, Van Loo (2021)** IJBNPA 18 · [doi:10.1186/s12966-021-01222-8](https://doi.org/10.1186/s12966-021-01222-8) | Online market, n=550, 2×2×2 tasarım | Takas teklifi ve Nutri-Score etiketi ayrı ayrı etkili. | — | — |
| **Piernas ve ark. (2024) SwapSHOP** JMIR mHealth 12:e45854 · [doi:10.2196/45854](https://doi.org/10.2196/45854) | Barkod tarayan uygulama, fizibilite RCT, n=112 | Müdahale grubunun %81 (SFA kolu) ve %87'si (şeker kolu) takas özelliğini kullandı. | SFA −0,56 g/100 g, şeker −1 g/100 g (keşif analizi). | **Bize en yakın ürün:** tarama + kişisel takas. Optimizasyon, bütçe ve hane boyutu yok. |
| **Wrieden & Levy (2016)** Change4Life Smart Swaps · PHN 19:2388–2392 · [doi:10.1017/S1368980016000513](https://doi.org/10.1017/S1368980016000513) | Yarı deneysel, 267'ye karşı 135 aile | Daha az şekerli içecek alan %32 (karşılaştırma %19), tahılda %24 (karşılaştırma %12). | Kısa vadeli etki. Kalıcılık belirsiz. | Kampanya düzeyinde kanıt. |
| **Sutherland ve ark. (2021) SWAP IT** JMIR 23:e25256 · [doi:10.2196/25256](https://doi.org/10.2196/25256) | 32 okul, 3022 öğrenci, beslenme çantası | — | Çantadaki ek gıda enerjisi −117 kJ. | "Swap" dilinin çocuk ve aile bağlamında işlediğini gösteriyor. Kabul oranı raporlanmadı. |
| Huang ve ark. (2006) PLoS Clin Trials 1:e22 · [doi:10.1371/journal.pctr.0010022](https://doi.org/10.1371/journal.pctr.0010022) | **Gerçek** online market | Koutoukidis'e göre etki deneysel marketlerden çok daha küçük. | — | **Dış geçerlilik uyarısı:** gerçek hayatta kabul daha düşük olabilir. |

**Modelleme çıkarımları [yorum]:**
- **k kısıtının gerekçesi üç katmanlı:**
  - Diyet modellemesinde yarı bireyde 5'ten az değişiklik yetiyor (Maillot 2010).
  - Swap denemelerinde sepet başına ~4 teklif yapılıyor, medyan 1 kabul geliyor (Forwood 2015).
  - Çok teklif, kabul oranını ve güveni düşürür (bilişsel yük). Bu son nokta **doğrulanmadı**, hipotez olarak test edilmeli.
- **Kabul olasılığı ön dağılımı (prior):**
  - Taban kabul %13–33.
  - Besin sıçraması büyüdükçe azalır: log-OR ≈ ln 0,81 ≈ −0,21 / SD.
  - Benzerlikle artar: log-OR ≈ ln 2,2–2,8 ≈ 0,8–1,0.
  - Kategoriye bağlıdır: %6–36.
  - Bu değerler, hane verisi gelene kadar **popülasyon ön dağılımı (prior)** olur (§5).
- **Sonuç ölçütü önerisi:** "Önerilen takas sayısı" değil, **gerçekleşen sağlık kazancı** = kabul edilen ve bir sonraki fişte **gerçekten satın alınan** takasların $\Delta h$ toplamı. Fiş, beyan edilen kabulü doğrular. Bu bizim kapalı döngünün ayırt edici verisi.

---

## 3. Satın alma verisiyle diyet kalitesi skorları: hane düzeyinde hesaplanabilirlik

| Skor | Girdi | Hesaplama | Doğrulama | Fişle hesaplanır mı? [yorum] |
|---|---|---|---|---|
| **GPQI-2016** (Brewster ve ark. 2017 · [doi:10.1016/j.jfca.2017.07.012](https://doi.org/10.1016/j.jfca.2017.07.012); 2019 JAND · [doi:10.1016/j.jand.2018.08.165](https://doi.org/10.1016/j.jand.2018.08.165)) | Harcama payları. USDA Food Plan'in 29 kategorisi → HEI-2010 tipi 11 bileşen, 0–75 puan. | Gözlenen harcama payı ile standart USDA payı kıyaslanır. | HEI-2015 ile ilişkili. Kısmi (≥%50) veriyle bile HEI ile r=0,41 (Parker ve ark. 2021 · [doi:10.1017/S0007114520004833](https://doi.org/10.1017/S0007114520004833)). | **Evet**, ama ABD kategori ve fiyat normları TR'ye uyarlanmalı. |
| **Healthy Trolley Index (HETI)** (Taylor ve ark. 2015 BJN 114:2129 · [doi:10.1017/S0007114515003827](https://doi.org/10.1017/S0007114515003827)) | **Süpermarket fişleri**, 1 ay, n=836 | Gıda grubu harcama payları Avustralya rehberiyle kıyaslanır, 0–100. | Fizibilite çalışması. | **Evet.** Fişten skor üretmenin doğrudan emsali. |
| **HPI** (Tharrey ve ark. 2019 PHN · [doi:10.1017/S1368980018003154](https://doi.org/10.1017/S1368980018003154)) ve **r-HPI** (Perignon ve ark. 2023 EJN · [doi:10.1007/s00394-022-02962-4](https://doi.org/10.1007/s00394-022-02962-4)) | **Yalnız harcama payları** (miktar ve besin gerekmez) | Çeşitlilik alt skoru: 5 grupta harcama payı P25'in üstündeyse puan. Kalite alt skoru: kesme noktaları, örn. kırmızı et payı >%21 ise −1. | Kantar panelinde, n=4375 + 2188. NRF9.3 ile ρ=0,59, enerji yoğunluğu ile ρ=−0,65. | **Evet, en kolayı.** Ürün–besin eşleşmesi zayıf olsa bile yalnız kategori ve fiyatla çalışıyor. Darmon ekolü (Maillot'yla aynı). |
| **FSAm-NPS DI** (Nutri-Score tabanlı diyet indeksi; örn. Khoury ve ark. 2022 · [doi:10.3389/fnut.2022.897089](https://doi.org/10.3389/fnut.2022.897089)) | Ürün başına FSAm-NPS puanı | Enerji ağırlıklı ortalama: $DI=\sum_i \text{NPS}_i E_i / \sum_i E_i$. | Kohortlarda hastalık riskiyle ilişkili. | **Evet**, OFF'ta Nutri-Score ve besin varsa. Sepete doğrudan uygulanır. |
| Supreme Nudge (Colizzi ve ark. 2024 BJN · [doi:10.1017/S0007114524002630](https://doi.org/10.1017/S0007114524002630)) | Sadakat kartı alımları ile FFQ kıyası | 13 grup, 0–130 puan | Satın alma ve tüketim kalitesi arasında ρ=0,31. Satın alma sistematik olarak daha düşük. | Uyarı: **sepet ≠ tüketim.** |

**Öneri [yorum]:**
- **Optimize edilen sağlık terimi $h$:** Enerji ağırlıklı FSAm-NPS iyileşmesi artı TÜBER/WHO yoğunluk hedeflerinden sapmalar (§7). İkisi de doğrusal.
- **Bağımsız değerlendirme skoru:** r-HPI (TR'ye uyarlanmış) ve besin yeterliliği (MAR/MER). Optimize ettiğimiz metriği rapor metriği yapmak Goodhart tuzağıdır: model kendi hedefini "iyileştirir".
- **İddianın sınırı:** Bulgular "hanenin **satın aldığı sepetin** kalitesi" düzeyinde kalmalı. "Bireyin diyeti" iddia edilmemeli: satın alma ile tüketim arasındaki korelasyon 0,3–0,4.

---

## 4. LLM + optimizasyon: doğal dilden kısıt ve model

### 4.1 Alanın durumu (2022–2026)
| Çalışma | Fikir | Sayılar ve not |
|---|---|---|
| **NL4Opt** (Ramamonjison ve ark., NeurIPS 2022 Competition, PMLR 220:189–203 · [link](https://proceedings.mlr.press/v220/ramamonjison23a.html)) | NL → varlık etiketleme → LP'nin mantıksal formu | İlk ortak benchmark. Kazananlar BiLSTM, CRF ve BERT tabanlıydı. |
| **OptiMUS** (AhmadiTeshnizi, Gao, Udell, ICML 2024 · [PMLR v235](https://proceedings.mlr.press/v235/ahmaditeshnizi24a.html)) | Modüler ajan: model kurar, kod yazar, hata ayıklar, değerlendirir. Uzun tanımlar için. NLP4LP veri seti. | Önceki yöntemlere göre kolay setlerde >%20, zor setlerde >%30 iyileşme. |
| **Chain-of-Experts** (Xiao ve ark., ICLR 2024 · [link](https://proceedings.iclr.cc/paper_files/paper/2024/hash/d45ee77826332c100a1e15f7765b99ff-Abstract-Conference.html)) | Rol atanmış çok ajan, "conductor" ve geri yansıtma. ComplexOR seti. | Temizlenmiş EasyLP'de %94,4 (survey Tablo 2). |
| **ORLM** (Huang, Tang ve ark., Operations Research 73:2986–3009, 2025 · [doi:10.1287/opre.2024.1233](https://doi.org/10.1287/opre.2024.1233)) | OR-Instruct sentetik veriyle 7–8B modelleri ince ayar. IndustryOR benchmark'ı. | Temizlenmiş NL4Opt'ta %73,8, ComplexLP'de %59,5 (survey Tablo 2). |
| **LLMOPT** (Jiang ve ark. · [arXiv 2410.13213](https://arxiv.org/abs/2410.13213)) | Beş elemanlı evrensel formülasyon, çoklu talimat ayarı, öz-düzeltme | Altı sette SOTA'ya göre ort. +%11,08 çözme doğruluğu. Yayın yeri bu oturumda teyit edilmedi. |
| **Autoformulation** (Astorga ve ark., ICML 2025 · [PMLR v267](https://proceedings.mlr.press/v267/astorga25a.html)) | MCTS ile formülasyon uzayında arama. Sembolik araçlarla eşdeğer formülasyonları budama. | "Doğruluk değerlendirmesi" ayrı bir çekirdek zorluk olarak tanımlanıyor. |
| **OptiGuide** (Li, Mellou, Zhang, Pathuri, Menache 2023 · [arXiv 2307.03875](https://arxiv.org/abs/2307.03875)) | LLM çözücünün **yerine geçmiyor, yanında** çalışıyor. What-if soruları sorulur, çözücü cevaplar, LLM açıklar. | Bizim "700 TL olursa?" senaryomuzun endüstri emsali (Microsoft, tedarik zinciri). |
| **Survey: Optimization Modeling Meets LLMs** (Xiao ve ark. 2025 · [arXiv 2508.10047](https://arxiv.org/abs/2508.10047)) | Benchmark kalitesi analizi | **Benchmark hata oranları:** NL4Opt ≥%26,4 · IndustryOR ≥%54 · EasyLP ≥%8,1 · ComplexLP ≥%23,7 · NLP4LP ≥%21,7 · ComplexOR ≥%24,3. Hata türleri: mantık hatası, eksik parametre, yanlış altın cevap. (Tablo özetleyici araçla okundu, sayılar tablodan birincil olarak teyit edilmeli.) |
| **IR2Solve** (Zhu ve ark., 2026-07 · [arXiv 2608.02641](https://arxiv.org/abs/2608.02641)) | **Şema-sınırlı ara temsil (ModelIR)** + iki aşamalı deterministik doğrulama ve derleme | Örnek başına 1 LLM çağrısı. Chain-of-Experts 8 çağrı yapıyor (3,3× token), SAC-Opt 39 çağrı (22,9×). **Bizim önerdiğimiz mimarinin en yakın akademik karşılığı.** |
| **Opt-Verifier** (Liu ve ark., ICML 2026 · [arXiv 2605.29556](https://arxiv.org/abs/2605.29556)) | Yapı tarafı (model tanıma uyuyor mu) ve çözüm tarafı (çözüm mantıklı mı) doğrulaması | Mevcut yöntemlere göre >%20 doğruluk artışı (özet). |
| **VeriSimpl** (Abdul Rahman ve ark., ICML 2026 · [arXiv 2607.20474](https://arxiv.org/abs/2607.20474)) | Çözücüyle sadeleştirilmiş tanı sorguları üretip formülasyonu yerel olarak doğrulama | Ana mesaj: "hatasız çalışması ≠ doğru olması". |
| **Ask Before You Optimize / InterOPT** (Ge ve ark., 2026-09 · [arXiv 2609.05258](https://arxiv.org/abs/2609.05258)) ve **SAILOR** (Sadeghi ve ark., 2026-09 · [arXiv 2609.13945](https://arxiv.org/abs/2609.13945)) | Eksik tanımda **netleştirme sorusu sormak** | SAILOR: 1723 örnek. Birebir amaç değeri uyumu veri setine göre %27–%87,6, örnek başına 1,4–5,7 soru. |
| **Kısıtlı çözümleme (constrained decoding)** (Geng ve ark. EMNLP 2023 · [doi:10.18653/v1/2023.emnlp-main.674](https://doi.org/10.18653/v1/2023.emnlp-main.674); JSONSchemaBench 2025 · [arXiv 2501.10868](https://arxiv.org/abs/2501.10868)) | Çıktıyı dilbilgisi ya da JSON şemasıyla sınırlamak | Sözdizimi hatasını sıfırlar. **Anlam hatasını sıfırlamaz.** |

**Ders [yorum]:** Genel amaçlı "LLM modelci" hâlâ %60–90 bandında ve benchmark'lar kirli. Bizim ihtiyacımız **sabit bir modelin parametrelerini ve seçili kısıt şablonlarını doldurmak**. Bu, semantik ayrıştırma (slot filling) problemidir, açık uçlu formülasyon değildir. Hata yüzeyi çok daha küçük ve **test edilebilir**.

### 4.2 Önerilen güvenli mimari: "kısıt derleyici"
```
Kullanıcı (TR metin/ses)
  → [1] LLM + JSON-şema kısıtlı çıktı  →  IR (ara temsil)
  → [2] Deterministik doğrulayıcı: şema · birim · aralık · varlık çözümleme (kızım → üye m2) · belirsiz ifade sözlüğü
  → [3] Politika birleştirme:  SERT = profil (alerjen, tıbbi)  ∪  IR (yalnız SIKILAŞTIRABİLİR)
  → [4] Geri-çeviri onayı: IR → şablonla (LLM'siz) Türkçe cümle → "Şunu anladım: … Doğru mu?"
  → [5] Derleyici IR → OR-Tools modeli (sabit kısıt şablonları)  → çözücü
  → [6] Olursuzsa: yumuşak hedefleri sırayla gevşet, en küçük gevşetmeyi raporla ("k=3 ile %5 tasarruf mümkün değil; k=5 gerekli")
  → [7] Son doğrulayıcı: çözümdeki tüm kısıtları bağımsız kodla yeniden hesapla + alerjen kural motoruyla çift kontrol
  → [8] LLM açıklar: yalnız çözücünün döndürdüğü sayıları kullanarak
```
**Değiştirilemez kurallar [yorum]:**
- **Alerjen ve tıbbi kısıtlar LLM'den gelmez.** Kaynakları profil ve deterministik sözlüktür (`00-sentez` ile tutarlı: "LLM sadece risk ekleyebilir").
- Metinde profilde olmayan bir alerjen geçerse, sistem **profile ekleme önerir**. Sessizce eklemez, hiçbir zaman kaldırmaz ("alerjiyi boşver" → reddedilir ve açıklanır).
- **Belirsiz ifade sözlüğü sabittir ve versiyonlanır.** Örnek: "şeker az" → serbest şeker enerji payı ≤ %10 (yumuşak). "şekersiz / çok az" → ≤ %5. "tuz az" → sodyum ≤ 2000 mg / 2000 kcal. LLM yalnız sözlükteki anahtarları seçebilir, eşik uyduramaz.
- Sözlükte olmayan ifade için **netleştirme sorusu** sorulur (InterOPT/SAILOR mantığı). Tahmin yapılmaz.

**IR şeması örneği.** Girdi: "çölyaklı kızım için 700 TL, şeker az".
```json
{
  "budget": {"amount": 700, "currency": "TRY", "period": "week", "hardness": "hard"},
  "member_refs": [{"mention": "kızım", "member_id": "m2", "resolved_by": "profile"}],
  "safety_mentions": [{"member_id": "m2", "condition": "celiac", "in_profile": true}],
  "nutrient_goals": [{"scope": "household", "nutrient": "free_sugar", "lexicon_key": "AZ", "hardness": "soft"}],
  "max_swaps": null,
  "clarifications_needed": []
}
```
Not: `safety_mentions` kısıt değildir, yalnızca profille çapraz kontroldür. Gluten kısıtı profilden derlenir.

**Değerlendirme (ölçülebilir iddia):**
- 200–300 cümlelik Türkçe NL→IR test seti. İçinde çok üyeli, belirsiz ve saldırgan örnekler olacak ("alerjiyi boşver", "bu hafta kızım yok").
- Metrikler: slot-F1, IR tam eşleşmesi, netleştirme doğruluğu ve **güvenlik-kritik hata oranı** (sert kısıt düşmesi veya gevşemesi). Hedef: guard sonrası 0.
- Karşılaştırma: düz istem (prompt) vs. şema-kısıtlı çıktı vs. şema + doğrulayıcı + geri-çeviri.
- İkili ayrıştırma (iki farklı istem ya da model) anlaşmazlığı ek bir **belirsizlik sinyali** olarak kullanılır.

**Risk:** "Çölyaklı kızım" metni özel nitelikli sağlık verisidir. Yurt dışındaki bir LLM'e gönderilmesi `01-mevzuat-risk.md`'deki aktarım sorununu doğurur. Çözüm yolu: sağlık terimlerini **cihazda veya sunucuda sözlükle** yakala ve LLM'e maskele ("[ÜYE_2] için [KOŞUL_1]"). LLM'e yalnız bütçe ve hedef slotları kalsın. Karar hukukçu veya danışmanla verilmeli.

---

## 5. Tercih öğrenme: kabul/red verisinden kişisel fayda

| Yaklaşım | Ne öğrenir | Veri ihtiyacı | Bizim hacimde gerçekçi mi? [yorum] |
|---|---|---|---|
| **Hiyerarşik (Bayesçi) lojistik kabul modeli** | $\pi_{\ell j}=\sigma(\beta_0+\beta^\top\phi_{\ell j}+b_H+b_{H,\text{kat}})$. Özellikler: Δfiyat %, ΔNPS (SD), aynı alt kategori, aynı marka, paket değişimi, yenilik. Hane ve hane×kategori rastgele etkileri. | Az. Popülasyon katsayıları §2'deki literatürden prior alır, hane etkileri kısmi havuzlama (partial pooling) ile öğrenilir. | **Evet. Birincil öneri.** |
| **Contextual / combinatorial bandit** (LinUCB: Li ve ark. 2010 · [doi:10.1145/1772690.1772758](https://doi.org/10.1145/1772690.1772758); Thompson sampling: Chapelle & Li 2011 · [NeurIPS](https://proceedings.neurips.cc/paper/2011/hash/e53a0a2978c28872a4505bdb51db06dc-Abstract.html); kombinatoryal TS: Wang & Chen 2018 · [PMLR v80 / arXiv 1803.04623](https://arxiv.org/abs/1803.04623)) | Keşif ve sömürü dengesi: posteriordan $\theta$ örneklenir → $\pi$ hesaplanır → MILP k takaslık bir "slate" seçer | Online. Keşif maliyeti var. | **Evet, lojistik modelin üstüne.** Keşif **yalnız sert kısıtları sağlayan adaylar arasında** yapılır. |
| **Inverse optimization** (Chan, Mahmood, Zhu 2025 OR 73(2) · [doi:10.1287/opre.2022.0382](https://doi.org/10.1287/opre.2022.0382); Keshavarz, Wang, Boyd 2011 · [doi:10.1109/ISIC.2011.6045410](https://doi.org/10.1109/ISIC.2011.6045410); Aswani, Shen, Siddiq 2018 · [doi:10.1287/opre.2017.1705](https://doi.org/10.1287/opre.2017.1705); online: Bärmann, Pokutta, Schneider ICML 2017 · [PMLR v70](https://proceedings.mlr.press/v70/barmann17a.html); diyet uygulaması: Ghobadi & Mahmoudzadeh 2021 EJOR 290:829 · [doi:10.1016/j.ejor.2020.08.048](https://doi.org/10.1016/j.ejor.2020.08.048), Shahmoradi & Lee 2022 OR · [doi:10.1287/opre.2021.2143](https://doi.org/10.1287/opre.2021.2143)) | Gözlenen sepetleri (yaklaşık) optimal kılan amaç ağırlıkları $(\lambda_h,\lambda_d,\lambda_c)$ veya kısıtlar | Az parametre (3–5 ağırlık) ise düşük. Tam amaç vektörü için yüksek. Gürültüye duyarlı. | **Kısmen.** Hane başına 3–5 trade-off ağırlığı, online IO ile ($O(1/\sqrt{T})$) araştırma uzantısı olarak yapılabilir. Ana döngüye konmamalı. |
| Derin öneri modelleri | Gömülü (embedding) tercih | Yüksek | **Hayır** (yalnızca aday üretiminde önceden eğitilmiş gömülüler kullanılabilir). |

**Veri hacmi hesabı [yorum, varsayım]:**
- Pilot: 20–40 hane × 8 hafta × ~1,5 fiş/hafta × k=3–5 teklif.
- Toplam ≈ **1.000–4.000 etiketli karar**, hane başına 40–100.
- Bu hacim ~8 sabit etki ve hane rastgele etkisi için yeterli. Hane başına ayrı model ya da derin model için yetersiz.

**Döngü:**
1. Kabul olasılığı $\pi$ posterior ortalamasından alınır (Thompson'da örnekten).
2. MILP amacı "beklenen gerçekleşen sağlık" olur: $\sum \pi\,\Delta h$.
3. Bir sonraki fiş etiketi düzeltir: "kabul etti ama almadı" = zayıf red.
4. Önerilerin küçük bir payı (örn. %10) güvenli adaylar arasında rastgele sıralanıp loglanır. Bu, **tarafsız çevrimdışı politika değerlendirmesine** (replay; Li ve ark. 2011 · [doi:10.1145/1935826.1935878](https://doi.org/10.1145/1935826.1935878)) izin verir.

**Etik sınır:** Öğrenilen hiçbir parametre alerjen veya tıbbi kısıta dokunamaz (`01` §P6 ile aynı ilke).

---

## 6. Çok üyeli hane: farklı kısıtlar, ortak sepet

**Literatür:**
- **Cost of the Diet** (Deptford ve ark. 2017 BMC Nutr 3 · [doi:10.1186/s40795-017-0136-4](https://doi.org/10.1186/s40795-017-0136-4); WFP deneyimi: Frega ve ark. 2012 · [doi:10.1177/15648265120333S212](https://doi.org/10.1177/15648265120333S212)): Tipik bir hanenin **üyelerinin ihtiyaçlarını toplayarak** en düşük maliyetli yeterli diyeti LP ile hesaplıyor. Hane düzeyi diyet LP'sinin yerleşik emsali. Ancak alerjen ve kişisel ürün ayrımı yok.
- **Yetişkin erkek eşdeğeri (AME)** (Weisell & Dop 2012 · [doi:10.1177/15648265120333S203](https://doi.org/10.1177/15648265120333S203)): Hane alımını üyelere enerji ihtiyacı oranında paylaştırma. Tüketim payı $\omega_{\ell m}$ için varsayılan kural.
- **Grup önerici sistemleri** (Masthoff 2015 · [doi:10.1007/978-1-4899-7637-6_22](https://doi.org/10.1007/978-1-4899-7637-6_22); sağlıklı gıda alanı: Tran ve ark. 2018 JIIS · [doi:10.1007/s10844-017-0469-0](https://doi.org/10.1007/s10844-017-0469-0); aile beslenme önerisi: SWITCHtoHEALTHY, Kalpakoglou ve ark. 2025 · [doi:10.3390/nu17243892](https://doi.org/10.3390/nu17243892)): Toplama stratejileri (ortalama, "least misery", "most pleasure").
- **Adaletin fiyatı** (Bertsimas, Farias, Trichakis 2011 OR · [doi:10.1287/opre.1100.0865](https://doi.org/10.1287/opre.1100.0865)): Adalet kısıtının toplam faydaya maliyetini ölçmek için çerçeve.

**Formülasyon öğeleri [yorum]** (tam hali §7.6'da):
- **Tüketen kümesi $S_\ell$:** Varsayılan kategori sezgiselinden gelir (bebek maması → bebek, kahve → yetişkinler), kullanıcı etiketleyebilir.
- **Alerjen:** Satır $\ell$'ye atanabilecek ürün, **tüketen tüm üyeler için** güvenli olmalı.
- **Satır bölme:** Ortak bir satır, kısıtlı bir üye yüzünden sorunluysa ("ekmek" + çölyaklı çocuk) iki kişisel satıra bölünebilir: çocuğa glutensiz, diğerlerine normal. Bölmenin maliyeti paket yuvarlaması ve fiyat farkıdır. Bu maliyet raporlanabilir bir çıktıdır: **"hane içi alerjenin haftalık maliyeti"**.
- **Üye bazlı besin hedefleri:** Çocuk için WHO sodyum sınırı enerji ihtiyacı oranında aşağı ölçeklenir (WHO 2012 · [NBK133292](https://www.ncbi.nlm.nih.gov/books/NBK133292/)).
- **Adalet:** "Kimse kötüleşmez" kısıtı $\Delta H_m\ge 0\;\forall m$, ya da max-min. Adaletin fiyatı raporlanır.

---

## 7. KENDİ FORMÜLASYONUMUZ: Akıllı Takas (ST — Smart Swap)

### 7.1 Kümeler
- $M$: hane üyeleri, $m\in M$.
- $L$: sepet satırları. Fişten eşlenen ürünler, genelde son 1–2 haftanın birleşik sepeti. $\ell\in L$, $|L|=n$.
- $J_\ell$: satır $\ell$ için seçenekler. $0\in J_\ell$ mevcut ürünü korumak demek. Diğerleri aday takaslardır. Adaylar aynı veya komşu kategoriden gelir (kategori ağacı mesafesi $\le\delta$), benzerlik top-K ile süzülür, fiyatı ve besini bilinir. Tipik $|J_\ell|\le 20$.
- $K$: besin öğeleri {E (kcal), serbest/eklenmiş şeker, Na, SFA, lif, protein}.
- $S_\ell\subseteq M$: satır $\ell$'yi tüketen üyeler.
- $G$: gıda grupları (TÜBER'in 5 grubu + "ekstra" grup).

### 7.2 Parametreler
| Sembol | Anlam | Kaynak |
|---|---|---|
| $c_{\ell j}$ | Seçenek $j$ alınırsa satır maliyeti (TL). Paket boyutu farkı adet düzeltmesiyle girer: $q_{\ell j}=\lceil q_\ell g_\ell/g_j\rceil$. | Fiş fiyatı / marketfiyati / OFF |
| $a_{\ell jk}$ | Satırın toplam besin miktarı ($q_{\ell j}$ paket için) | OFF, etiket OCR |
| $h_{\ell j}$ | Sağlık puanı. Örn. $-\text{NPS}_j\cdot E_{\ell j}/E_0$ (enerji ağırlıklı FSAm-NPS katkısı). | OFF Nutri-Score bileşenleri |
| $d_{\ell j}\ge0$ | Sapma cezası, $d_{\ell0}=0$. Kategori mesafesi + normalize besin farkı L1 + marka/paket değişimi + öğrenilen ceza. | §1, §5 |
| $\pi_{\ell j}\in[0,1]$ | Kabul olasılığı | §2 prior + §5 posterior |
| $\alpha_j$ | Ürün $j$'nin alerjen kümesi ("içerir" + "iz içerebilir"). Beyan yoksa ve profil katıysa "bilinmiyor" = yasak. | Karar motoru (`00-sentez`) |
| $A_m$ | Üye $m$'nin yasaklı alerjen ve bileşen kümesi | Profil |
| $\omega_{\ell m}$ | Tüketim payı ($\sum_m\omega_{\ell m}=1$, varsayılan AME oranı) | Profil + sezgisel |
| $B$ | Bütçe (TL/dönem) | Kullanıcı / IR |
| $k$ | En fazla takas | Kullanıcı / varsayılan 3–5 |
| $\varepsilon_E$ | İzo-enerji toleransı (örn. 0,05) | Tasarım |
| $\bar\sigma,\bar\nu,\bar s,\bar\phi$ | Yoğunluk hedefleri: serbest şeker enerji payı ≤0,10 ([WHO 2015](https://www.ncbi.nlm.nih.gov/books/NBK285525/)); Na ≤1 mg/kcal (2000 mg/2000 kcal, [WHO 2012](https://www.ncbi.nlm.nih.gov/books/NBK133292/)); SFA enerji payı ≤0,10 ([WHO 2023](https://www.ncbi.nlm.nih.gov/books/NBK594769/)); lif ≥12,5 g/1000 kcal (EFSA'nın yetişkin 25 g/gün AI'sından türetildi) | Aşağıdaki TÜBER notu |

> **TÜBER notu:** TÜBER 2022 sunum PDF'inde ([HSGM](https://hsgm.saglik.gov.tr/media/attachments/2025/05/12/turkiye-beslenme-rehberi-2022.pdf)) yetişkin makro dağılımı doğrulandı: **CHO %45–60, yağ %20–35, protein %10–20 enerji**. Posa için "Ek 1.4.1 … posa/lif (AI)" tablosu var ama görüntü olduğu için değeri okunamadı. Tuz ve serbest şeker için TÜBER tam metnindeki birebir ifade **DOĞRULANMADI**: tam metin PDF'i (~10 MB) bu oturumda açılamadı. Yukarıdaki eşikler WHO'dan alındı. Proposal'dan önce TÜBER tam metninden (Ek tablolar) teyit edilip `kaynak/`'a not düşülmeli.

### 7.3 Karar değişkenleri
- $x_{\ell j}\in\{0,1\}$: satır $\ell$'de seçenek $j$ seçilir.
- $s_k^+\ge0$: hane yoğunluk hedefi aşımı. $s_{mk}^+\ge0$: üye hedefi aşımı (goal programming).
- Hane uzantısı: $z_\ell\in\{0,1\}$ satır bölme, $y^{R}_{\ell j},y^{O}_{\ell j}\in\{0,1\}$ bölünen satırın kısıtlı ve diğer parçaları (§7.6).

### 7.4 Amaç (tek amaçlı sürüm: beklenen gerçekleşen fayda)
$$
\max_{x,s}\;\; \underbrace{\sum_{\ell\in L}\sum_{j\in J_\ell\setminus\{0\}} \pi_{\ell j}\,(h_{\ell j}-h_{\ell 0})\,x_{\ell j}}_{\text{beklenen sağlık kazancı}}
\;-\;\lambda_d \underbrace{\sum_{\ell}\sum_{j} d_{\ell j}\,x_{\ell j}}_{\text{sapma}}
\;-\;\sum_{k}\rho_k\, s_k^+ \;-\;\sum_{m,k}\rho_{mk}\, s_{mk}^+
$$
Hedef sapmaları "tüm takaslar kabul edilirse" oluşacak sepet üzerinden hesaplanır. Bu, planın kendisinin hedefe ne kadar yaklaştığıdır.

### 7.5 Kısıtlar
**(C1) Çoktan seçmeli (GUB):**
$$\textstyle\sum_{j\in J_\ell} x_{\ell j}=1 \qquad \forall \ell\in L$$

**(C2) Alerjen, sert ve yapısal:**
$$x_{\ell j}=0 \quad \text{eğer } \alpha_j\cap \textstyle\bigcup_{m\in S_\ell}A_m\neq\emptyset$$
Değişken ön işlemde **modelden silinir**. Güvenlik, çözücü toleransına bırakılmaz. Mevcut ürün ihlal ediyorsa $x_{\ell0}=0$ olur: zorunlu takas ya da satır bölme (§7.6).

**(C3) Kardinalite (davranışsal bütçe):**
$$\textstyle\sum_{\ell}\sum_{j\neq0}x_{\ell j}\le k$$
Opsiyonel: grup başına en fazla 1 takas.

**(C4) Bütçe, kısmi kabule karşı sağlam.** Kullanıcı takasların herhangi bir alt kümesini kabul edebilir. Sepet hiçbir kombinasyonda $B$'yi aşmamalı ($C_0=\sum_\ell c_{\ell0}\le B$ varsayımıyla):
$$C_0+\textstyle\sum_{\ell}\sum_{j\ne0}(c_{\ell j}-c_{\ell0})^{+}\,x_{\ell j}\le B$$
Kullanıcı **tasarruf** istiyorsa ($B<C_0$), kısmi kabulde tasarruf garanti edilemez. Bu durumda nominal kısıt kullanılır ve "hepsini kabul edersen" diye açıkça etiketlenir:
$$\textstyle\sum_{\ell,j}c_{\ell j}x_{\ell j}\le B$$

**(C5) İzo-enerji:**
$$(1-\varepsilon_E)E_0\le \textstyle\sum_{\ell,j}a_{\ell jE}\,x_{\ell j}\le(1+\varepsilon_E)E_0$$

**(C6) Hane yoğunluk hedefleri.** Oranlar paydayla çarpılarak doğrusallaştırılır. Kısmi fiş kapsamına (hanenin tüm alımı görünmeyebilir) karşı sağlam olsunlar diye yoğunluk formunda yazılır:
$$\textstyle\sum_{\ell,j}\big(4a_{\ell j,\text{şkr}}-\bar\sigma\,a_{\ell jE}\big)x_{\ell j}\le s^+_{\text{şkr}}$$
$$\textstyle\sum_{\ell,j}\big(a_{\ell j,\text{Na}}-\bar\nu\,a_{\ell jE}\big)x_{\ell j}\le s^+_{\text{Na}}$$
$$\textstyle\sum_{\ell,j}\big(9a_{\ell j,\text{SFA}}-\bar s\,a_{\ell jE}\big)x_{\ell j}\le s^+_{\text{SFA}}$$
$$\textstyle\sum_{\ell,j}\big(\bar\phi\,a_{\ell jE}-a_{\ell j,\text{lif}}\big)x_{\ell j}\le s^+_{\text{lif}}$$
Kullanıcı bir hedefi "kesin" yaparsa $s^+=0$ olur ve hedef sert kısıta döner.

**(C7) Üye hedefleri:** Aynı yapı, bu kez $\sum_{\ell: m\in S_\ell}\omega_{\ell m}(\cdot)$ ile ve üyeye özgü eşiklerle (çocuk: Na eşiği $\times E_m/E_{\text{yetişkin}}$; diyabetik ebeveyn: şeker ≤ %5).

**(C8) Kabul edilebilirlik ve ikame uyumu:**
- $J_\ell$ aday üretimiyle zaten sınırlıdır.
- Grup enerji payı bandı: $\ell_g E\le\sum_{\ell\in g}\sum_j a_{\ell jE}x_{\ell j}\le u_g E$ (Schäfer 2025'teki P5–P95 mantığı). Doğrusal olsun diye $E$ yerine $E_0$ sabiti alınır, (C5) sayesinde bu yaklaşım makul.

**(C9) Kullanıcı kilitleri ve soğuma:**
- Kullanıcının "dokunma" dediği satır için $x_{\ell0}=1$.
- Son $T$ haftada reddedilen $(\ell,j)$ çiftleri için $x_{\ell j}=0$.

### 7.6 Hane uzantısı: satır bölme
Ortak satır $\ell$ için kısıtlı üyeler $R_\ell=\{m\in S_\ell:\alpha_{\ell0}\cap A_m\ne\emptyset\}$, diğerleri $O_\ell=S_\ell\setminus R_\ell$.
$$
\textstyle\sum_j x_{\ell j}=1-z_\ell,\qquad \sum_j y^R_{\ell j}=z_\ell,\qquad \sum_j y^O_{\ell j}=z_\ell
$$
$$
y^R_{\ell j}=0 \text{ eğer } \alpha_j\cap\textstyle\bigcup_{m\in R_\ell}A_m\ne\emptyset;\qquad x_{\ell j}=0 \text{ eğer } \alpha_j\cap\bigcup_{m\in S_\ell}A_m\ne\emptyset
$$
- Maliyet ve besin: parçalar $\Omega_R=\sum_{m\in R_\ell}\omega_{\ell m}$ ve $\Omega_O$ paylarıyla hesaplanır, paket yuvarlaması **yukarı** yapılır. Bölmenin ek maliyeti buradan doğar.
- Bölme (C3)'te 1 takas sayılır: $\sum_{\ell,j\ne0}x_{\ell j}+\sum_\ell z_\ell\le k$.
- **Adalet:** $\Delta H_m=\sum_{\ell: m\in S_\ell}\omega_{\ell m}\sum_j (h_{\ell j}-h_{\ell0})x_{\ell j}+\dots\ \ge 0\ \ \forall m$. Anlamı: takas kimsenin sepet payını kötüleştirmez.
- **Raporlanan çıktı:** "hane içi alerjenin maliyeti" = (C2) ve bölme varken optimal maliyet − alerjen yokken optimal maliyet.

### 7.7 Sınıf ve karmaşıklık
- **Sınıf:** Saf 0-1 değişkenler ve birkaç sürekli sapma değişkeni içeren bir **MILP**. Yapı: GUB (C1) + $r$ adet yan kısıt (bütçe, $k$, 2 enerji, ~4 hane, ~$|M|\times$birkaç üye). Bu, **çok boyutlu çoktan seçmeli sırt çantası (MMKP)** yapısıdır.
- **Özel durumlar:**
  - Yalnız bütçe: **MCKP** (Sinha & Zoltners 1979 · [doi:10.1287/opre.27.3.503](https://doi.org/10.1287/opre.27.3.503)). Zayıf NP-zor. $O(\sum_\ell|J_\ell|\cdot B)$ sözde polinom DP ile çözülür. LP gevşetmesi baskınlık ve dışbükey zarfla açgözlü biçimde çözülür (Kellerer, Pferschy, Pisinger 2004 · [doi:10.1007/978-3-540-24777-7](https://doi.org/10.1007/978-3-540-24777-7)).
  - Bütçe + $k$: DP durumu $(b,t)$ ile hâlâ sözde polinom, $O(\sum_\ell|J_\ell|\cdot B\cdot k)$. 60×21×700×6 ≈ 5×10⁶ işlem. **[yorum] CSE 413 hafta 13 (DP) bağlantısı:** Çekirdek modeli DP ile bağımsız çözüp MILP'i doğrulamak iyi bir "iki exact yöntem" kontrolüdür. Kardinalite kısıtlı sırt çantası: Caprara ve ark. 2000 · [doi:10.1016/S0377-2217(99)00261-1](https://doi.org/10.1016/S0377-2217(99)00261-1).
  - ≥2 genel kaynak kısıtı: MMKP, $d$-boyutlu sırt çantasını içerdiği için P≠NP altında **FPTAS yoktur** (Magazine & Chern 1984 · [doi:10.1287/moor.9.2.244](https://doi.org/10.1287/moor.9.2.244); $d=2$ için EPTAS da yoktur: Kulik & Shachnai 2010 · [doi:10.1016/j.ipl.2010.05.031](https://doi.org/10.1016/j.ipl.2010.05.031)). Besin kısıtları eklenince DP'nin durum uzayı patlar ve MILP gerekli olur.
- **LP gevşetmesinin yapısı (neden boşluk küçük):** $n$ GUB eşitliği ve $r$ yan kısıtlı bir LP'de temel uygun çözümün en fazla $n+r$ temel değişkeni vardır. Her GUB'ın en az bir pozitif değişkeni olduğundan **en fazla $r$ satır kesirli** olabilir. $r\approx10$ ve $n=60$ iken satırların çoğu zaten tamsayıdır. Bu hem küçük tamsayılılık boşluğunu açıklar hem de bir yuvarlama sezgiseli önerir.

### 7.8 Tipik boyut ve çözüm süresi (sentetik ölçüm)
[sentetik] Ayrıntılar:
- Kod: `arastirma/02-ek-swap_bench.py` (sentetik üreteç + model; `python3 02-ek-swap_bench.py 10`).
- Örnek üreteci: satır başına rastgele enerji, şeker, Na, SFA, lif, fiyat ve NPS. Adaylar ±%15–80 pertürbasyonla üretildi, %20'si 0. üye için alerjenli.
- Model: (C1)–(C7) + sağlam bütçe, $k=5$, $\beta=0$.
- Donanım ve yazılım: Apple M1, OR-Tools 9.15 (MPSolver arayüzü, varsayılan parametreler). Her satır 10 örnek.

| $n\times|J|$ | İkili değişken | SCIP medyan / maks (s) | CP-SAT medyan / maks (s) | LP gevşetmesi boşluğu (medyan) |
|---|---|---|---|---|
| 30×10 | 330 | 0,005 / 0,006 | 0,042 / 0,048 | ≈%0 |
| **60×20** | **1.260** | **0,012 / 0,014** | **0,081 / 0,087** | ≈%0 |
| 120×40 | 4.920 | 0,048 / 0,066 | 0,385 / 0,535 | ≈%0 |
| 300×40 | 12.300 | 0,169 / 0,198 | 1,58 / 1,98 | ≈%0 |

Sıkı varyantlar:
- 60×20, $k=10$, **zorunlu %5 tasarruf** (nominal bütçe): SCIP 0,23 s, CP-SAT 0,17 s. LP boşluğu medyan %3,3, maks %11,5. Gevşetme gevşek kalıyor.
- $k=3$ + %5 tasarruf: 20 örneğin **20'si olursuz.** Olursuzluğun ispatı 60×20'de 0,14 s, 120×40'ta SCIP ile **~5 s** sürdü. Ürün açısından ders şu: olursuzluk hızlı bir ön kontrol ve gevşetme önerisiyle (§4.2-[6]) yönetilmeli.

**Sonuç [yorum]:** Gerçekçi boyutta çekirdek problem **milisaniyeler içinde kesin optimum** veriyor. CP-SAT sürekli sapma değişkenleriyle SCIP'ten yavaş kaldı. Üretimde MPSolver+SCIP (ya da HiGHS) yeterli. Sezgiselin **çekirdekte hız gerekçesi yok**. Gerekçe 3-amaçlı cephede ve market uzantısında aranmalı (§7.10, §7.11).

### 7.9 LP gevşetmesi ve gölge fiyat: "sağlığın fiyatı"
- **Sürüm A** (bütçe altında sağlığı maksimize et): Bütçe kısıtının duali $\mu_B$ = **1 TL ek bütçenin marjinal sağlık kazancı**. Tersi $1/\mu_B$ "sağlık puanının TL fiyatı" olur.
  - [sentetik] 60×20 örnekte $\beta=0$ iken LP = MILP = 5,07 ve $\mu_B=2,80$ puan/TL (normalize birim).
  - Bütçe %3 artırılınca kısıt bağlayıcı olmaktan çıktı ($\mu_B=0$). Darboğaz artık $k$'ydı: $k=3\to5\to8$ için amaç −54,7 → 5,1 → 82,2.
  - **Yorum:** İki gölge fiyat var. **TL'nin fiyatı** ve **kullanıcı sabrının fiyatı** (bir takasın marjinal değeri = (C3)'ün duali). İkincisi v2'ye özgü ve raporda güçlü bir anlatı.
- **Sürüm B** (sağlık hedefi altında maliyeti minimize et): $\min \sum c x$ s.t. $\sum h x\ge H^\ast$. Sağlık kısıtının duali doğrudan **TL/sağlık puanı** olur. Besin kısıtlarının dualleri "sodyum yoğunluğunu 100 mg/1000 kcal düşürmenin haftalık marjinal maliyeti" anlamına gelir.
- **Dürüstlük notu:** MILP'te dualite yoktur. Seçenekler:
  - (i) LP gevşetmesinin duali: sınır verir. Bizde çoğu örnekte LP=MILP olduğu için anlamlı.
  - (ii) Tamsayılar sabitlenerek LP duali (Gomory & Baumol 1960 · [doi:10.2307/1910130](https://doi.org/10.2307/1910130)): yerel.
  - (iii) **Kesin parametrik eğri:** $B$ üzerinde ε-constraint taraması. Parçalı sabit sağlık–bütçe eğrisi çıkar, kırılma noktaları arası eğim ayrık fiyattır. [sentetik] 7 noktalık tarama 1,2 s sürdü.
  - **Öneri:** Uygulamada (iii), raporda CSE 413 bağlantısı için (i).

### 7.10 Çok amaçlı sürüm ve deney tasarımı
**Amaçlar:**
- $f_1$ = maliyet (min).
- $f_2$ = sağlık (max; $\sum(h_{\ell j}-h_{\ell0})x_{\ell j}-\sum\rho s^+$).
- $f_3$ = sapma (min; $\sum d\,x$).
- $k$ ya parametre ($k\in\{1,\dots,5\}$) ya da 4. amaç olur (takas sayısı).

**Exact yöntem:**
- ε-constraint (Haimes, Lasdon, Wismer 1971 · [doi:10.1109/TSMC.1971.4308298](https://doi.org/10.1109/TSMC.1971.4308298)) ve **AUGMECON2** (Mavrotas & Florios 2013 · [doi:10.1016/j.amc.2013.03.002](https://doi.org/10.1016/j.amc.2013.03.002)). AUGMECON2 zayıf baskın noktaları eler.
- Maliyet kuruşa, sağlık ve sapma tamsayı puana ölçeklenirse, ε adımı 1 ile **tam Pareto kümesi** elde edilir (iki amaçlı durumda).
- 3 amaçta bir ızgara taraması yapılır ve süre raporlanır.

**Sezgisel yöntem:** NSGA-II (Deb ve ark. 2002 · [doi:10.1109/4235.996017](https://doi.org/10.1109/4235.996017)), jMetal (Java).
- Tamsayı kodlama: gen $\ell\in J_\ell$. Alerjenli adaylar **alandan çıkarıldığı için** sert kısıt yapı gereği sağlanır.
- (C3) ve (C4) için onarım operatörü: en kötü $\Delta h/\Delta c$ oranlı takası geri al.
- Besin hedefleri için Deb'in kısıtlı baskınlık kuralı.
- Mutasyon: $1/n$ olasılıkla aday değiştir. Çaprazlama: uniform.

**Taban çizgileri (hocanın makalesindeki "rastgele yerleştirme" rolü):**
- (a) Açgözlü: $\Delta h/\Delta c$ sırasıyla $k$ takas.
- (b) "Kategorideki en iyi Nutri-Score": bugünkü uygulamaların naif yaklaşımı.
- (c) Rastgele $k$ takas.

Bu taban çizgileri **sepet düzeyi optimizasyonun değerini** ölçer.

**Metrikler:**
- Hypervolume (Zitzler & Thiele 1999 · [doi:10.1109/4235.797969](https://doi.org/10.1109/4235.797969)). Exact cepheden alınan ideal ve nadir ile normalize edilir, referans noktası nadir×1,1.
- IGD+ (Ishibuchi ve ark. 2015 · [doi:10.1007/978-3-319-15892-1_8](https://doi.org/10.1007/978-3-319-15892-1_8)).
- Exact cephe noktalarının yakalanma oranı.
- HV oranı boşluğu: $1-HV_{\text{NSGA}}/HV_{\text{exact}}$.
- Hedefe ulaşma süresi (time-to-target).

**Protokol:**
- Her örnek × algoritma için **30 tohum**.
- **Eşit değerlendirme bütçesi** (örn. 50k değerlendirme) ve ayrıca eşit duvar saati.
- İstatistik: örnek bazında eşleştirilmiş Wilcoxon işaretli sıra testi; algoritmalar arası Friedman + Holm düzeltmesi; etki büyüklüğü Vargha–Delaney $A_{12}$ (Vargha & Delaney 2000 · [doi:10.3102/10769986025002101](https://doi.org/10.3102/10769986025002101)). Rehber: Derrac ve ark. 2011 · [doi:10.1016/j.swevo.2011.02.002](https://doi.org/10.1016/j.swevo.2011.02.002).

**Senaryolar (20, hocanın WB-MCLP makalesindeki 20 senaryoya paralel):**
- Faktörler: sepet $n\in\{20,60,120\}$ · aday $|J|\in\{10,20,40\}$ · bütçe sıkılığı $\beta\in\{-5\%,0,+5\%\}$ · hane tipi {tek kişi, çift, 4 kişi + çölyaklı çocuk, 3 kişi + diyabetik ebeveyn} · $k\in\{3,5\}$.
- Kesirli faktöriyel tasarımla 18 senaryo + 2 stres senaryosu ($n=300$ ve market uzantısı).
- Veri: pilot hanelerin gerçek fişleri + OFF TR ürünleri + fiyat. Bu verilere kalibre edilmiş bir sentetik üreteç seti büyütür.

**Dürüst hipotez:** Çekirdek 2-amaçlı problemde exact yöntem cepheyi saniyeler içinde çıkarır ve NSGA-II'ye gerek kalmaz. NSGA-II'nin kazandığı yer 3–4 amaçlı yoğun cephe ve market uzantısı olabilir. **Hangisi çıkarsa çıksın, gap ölçülüp raporlanır** (CSE 413'ün ruhu).

**Tercih öğrenme deneyi** (kullanıcısız da yapılabilir):
- Sentetik haneler, §2'deki oranlarla kalibre edilmiş gerçek kabul modeliyle üretilir.
- 12 simüle hafta boyunca üç politika karşılaştırılır:
  - (P0) kabulü yok sayan sağlık maksimizasyonu,
  - (P1) popülasyon $\pi$'li MILP,
  - (P2) hiyerarşik Bayes + Thompson örneklemeli MILP.
- Metrikler: kümülatif gerçekleşen sağlık kazancı, kabul oranı ve kâhine (oracle) göre pişmanlık (regret). 30 tohum.

### 7.11 Uzantı: market seçimi (en fazla 2 market + mesafe)
**Kümeler:**
- $S$: yarıçap $R$ içindeki marketler (OSM).
- $\mathcal T=\{T\subseteq S:1\le|T|\le2\}$. $|S|=10$ için $|\mathcal T|=55$.

**Parametreler:**
- $p_{js}$: ürün $j$'nin market $s$'teki fiyatı. Stokta yoksa $+\infty$.
- $\tau_T$: ev → $T$ → ev turunun maliyeti. Yürüme ise `01` §P5'teki eğim düzeltmeli mesafe (hocanın WB-MCLP'sine atıf). Araçla ise km.
- $\gamma$: TL/km zaman değeri.

**Değişkenler:** $u_T\in\{0,1\}$ (hangi market kümesi), $w_{\ell js}\in\{0,1\}$.

**Model:**
$$
\textstyle\sum_{T}u_T=1,\qquad \sum_{s}w_{\ell js}=x_{\ell j},\qquad w_{\ell js}\le\sum_{T\ni s}u_T,\qquad w_{\ell js}=0\ \text{ eğer } p_{js}=\infty
$$
$$
\text{bütçe: }\textstyle\sum p_{js}q_{\ell j}w_{\ell js}\le B,\qquad \text{amaca ek terim: }-\lambda_\tau\,\gamma\sum_T\tau_T u_T
$$
**Sınıf:** $|T|\le2$ ile sınırlı bir **Traveling Purchaser Problem** (Laporte, Riera-Ledesma, Salazar-González 2003 · [doi:10.1287/opre.51.6.940.24921](https://doi.org/10.1287/opre.51.6.940.24921)). Turlar önceden sayılabildiği için rota alt problemi yoktur. Market = tesis, satır = müşteri olarak düşünülürse p≤2 tesisli tesis yerleşimi ile atama yapısına benzer.

**Kesin ayrışım (decomposition):** $T$ sabitlenince her ürün $T$ içindeki en ucuz markette alınır: $p_{jT}=\min_{s\in T}p_{js}$. Böylece iç problem §7.5'in MMKP'sine döner. **55 × ~12 ms ≈ 0,7 s** ile kesin çözüm elde edilir (tahmin, 60×20 ölçümünden). Tek parça MILP (monolitik) ~12.600 ikili değişkenle ayrıca çözülür. Bu uzantı exact ile GA karşılaştırması için doğal stres senaryosudur.

**Veri riski:** `01` ile aynı: marketfiyati.org.tr'nin API'si ve kullanım koşulları belirsiz.

---

## 8. Rapor için "katkı" cümleleri (öneri)

1. **Modelleme katkısı:**
   - Beslenme epidemiyolojisindeki "gözlenen diyetten en az sapma" paradigması (Maillot ve ark. 2010) anket verisinden **hanenin fişle gözlenen gerçek sepetine** ve gıda grubundan **barkodlu ürün düzeyine** taşındı.
   - Bu problem, kardinalite kısıtlı çok boyutlu çoktan seçmeli sırt çantası (MMKP) tipi bir 0-1 MILP olarak formüle edildi.
   - Formülasyon alerjen kısıtlarını değişken eleme ile **yapısal olarak** garanti ediyor, bütçeyi takasların kısmi kabulüne karşı **sağlam** tutuyor ve farklı kısıtları olan hane üyelerini **satır bölme** ile birlikte çözüyor.
2. **Kabul-farkında karar desteği:**
   - Swap RCT'lerinden kalibre edilen kabul olasılıkları (kabul %13–33; besin sıçraması büyüdükçe kabul düşüyor) amaç fonksiyonuna "beklenen gerçekleşen sağlık kazancı" olarak gömüldü.
   - Kabul olasılıkları hane geri bildirimiyle hiyerarşik Bayesçi olarak kişiselleşiyor. Bir sonraki fiş, beyan edilen kabulü doğruluyor.
   - Keşif Thompson örneklemesiyle, yalnızca güvenli adaylar arasında yapılıyor.
3. **Güvenli doğal dil → kısıt derleyicisi:**
   - LLM açık uçlu model yazmak yerine şema-sınırlı bir ara temsile derleme yapıyor.
   - Sert güvenlik kısıtları yalnızca deterministik profilden geliyor (LLM gevşetemez).
   - Mimari geri-çeviri onayı ve bağımsız çözüm doğrulayıcısıyla güvenceleniyor.
   - Türkçe bir NL→kısıt test seti ve "güvenlik-kritik hata oranı" metriğiyle değerlendiriliyor.
4. **Karar-analitik çıktılar ve deneysel değerlendirme:**
   - LP dualitesi ve kesin ε-constraint taramasıyla hanenin **"sağlığın fiyatı"** (TL/sağlık puanı), **"bir takasın değeri"** ve **"hane içi alerjenin maliyeti"** hesaplanıyor.
   - Exact (ε-constraint/AUGMECON2 ve market ayrışımı) ile NSGA-II, 20 senaryo × 30 tohumda hypervolume ve IGD+ üzerinden parametrik olmayan testlerle karşılaştırılıyor.

---

## 9. Yenilik kontrolü: en yakın komşular (taramada görülenler)
| İş | Benzerlik | Fark |
|---|---|---|
| Szymanski ve ark., **CHI 2026**, "Balancing Goals, Health, and Cost: A Food Information System…" · [doi:10.1145/3772318.3793193](https://doi.org/10.1145/3772318.3793193) | Alışverişi **çok amaçlı optimizasyon** olarak kuruyor: maliyet × besin × kişisel hedef, sepet düzeyinde. 8 hafta, n=55, gıda güvencesiz topluluk. | Tam metin okunamadı (403). Özet ve basın bültenine göre fiş, minimum sapma, k-takas, LLM, hane üyesi alerjeni ve tercih öğrenme **görünmüyor** (DOĞRULANMADI). **Proposal'da mutlaka anılmalı.** |
| SwapSHOP (Piernas 2024) | Barkod tarama + kişisel takas | Optimizasyon, bütçe ve hane yok |
| Jansen & Bennin 2025, IJIM Data Insights · [doi:10.1016/j.jjimei.2024.100303](https://doi.org/10.1016/j.jjimei.2024.100303) | Kişisel sağlıklı ve sürdürülebilir market ürünü önerisi (ML) | İçeriği okunamadı (403) |
| Aguilera Moreno 2026, MIGP öğün optimizasyonu · [arXiv 2605.13849](https://arxiv.org/abs/2605.13849) | Tamsayı porsiyon + goal programming, HiGHS ile <100 ms | Mevcut diyetten sapma, LLM ve sepet yok |
| Opticourses (Dubois, Tharrey, Darmon 2017 · [doi:10.1017/S1368980017002282](https://doi.org/10.1017/S1368980017002282)) | Düşük gelirli hanelerde "ek maliyet olmadan daha sağlıklı alım" müdahalesi (Darmon ekolü) | İnsan danışmanlığıyla yürüyor. Otomatik optimizasyon değil. |

**Hüküm [yorum]:** Parçaların her biri literatürde var. **Birleşimi taramada bulunamadı:** fiş → minimum sapmalı k-takas MILP'i → hane üyeleri ve alerjen → LLM kısıt derleyicisi → kabulden öğrenme. "İlk" iddiası yerine "taramamızda bulunamadı" denmeli.

---

## 10. Açık sorular ve riskler
**Levent'e:**
- Pilot hane sayısı gerçekçi olarak kaç? (§5 hesabı 20–40 varsayıyor.)
- $k$ varsayılanı 3 mü 5 mi?
- "Şeker az" gibi sözlük eşiklerini diyetisyen onaylayacak mı?

**Danışmana:**
- Çekirdekte exact yöntem ms düzeyinde çözüyor. Bu durumda NSGA-II karşılaştırmasının 3-amaç ve market uzantısında yapılması kabul mü?
- DP ile MILP'in karşılıklı doğrulaması CSE 413 projesiyle örtüşebilir mi? Çift kullanım politikası sorulmalı.

**Veri riskleri:**
- Fiş satırından ürüne eşleme (`01-veri-fizibilite`: fişte barkod yok).
- Aday ürünlerin fiyatı (marketfiyati).
- TR'de r-HPI kesme noktaları yok, uyarlama gerekecek.

**Doğrulanacaklar:**
- TÜBER tuz, şeker ve posa sayıları (tam metin).
- Survey Tablo 1'deki hata oranları.
- CHI 2026 makalesinin tam içeriği.

---

## Kaynakça (DOI/link)
**Diyet optimizasyonu:**
- Maillot M, Vieux F, Amiot MJ, Darmon N (2010) AJCN 91:421 — [doi:10.3945/ajcn.2009.28426](https://doi.org/10.3945/ajcn.2009.28426)
- Maillot M ve ark. (2017) PLOS ONE 12:e0174679 — [doi:10.1371/journal.pone.0174679](https://doi.org/10.1371/journal.pone.0174679)
- Lluch A ve ark. (2017) Nutrients 9:162 — [doi:10.3390/nu9020162](https://doi.org/10.3390/nu9020162)
- Gazan R ve ark. (2018) Adv Nutr 9:602 — [doi:10.1093/advances/nmy049](https://doi.org/10.1093/advances/nmy049)
- van Dooren C (2018) Front Nutr, LP derlemesi — [doi:10.3389/fnut.2018.00048](https://doi.org/10.3389/fnut.2018.00048)
- Schäfer AC ve ark. (2025) PLOS ONE 20:e0313347 — [doi:10.1371/journal.pone.0313347](https://doi.org/10.1371/journal.pone.0313347)
- Okubo H ve ark. (2015) Nutr J 14:57 — [doi:10.1186/s12937-015-0047-7](https://doi.org/10.1186/s12937-015-0047-7)
- Tyszler M, Kramer G, Blonk H (2016) Int J LCA 21:701 — [doi:10.1007/s11367-015-0981-9](https://doi.org/10.1007/s11367-015-0981-9)
- Gerdessen JC, de Vries JHM (2015) EJCN 69:1272 — [doi:10.1038/ejcn.2015.56](https://doi.org/10.1038/ejcn.2015.56)
- Daelmans B ve ark. (2013) Matern Child Nutr — [doi:10.1111/mcn.12083](https://doi.org/10.1111/mcn.12083)

**Swap denemeleri:**
- Forwood SE ve ark. (2015) IJBNPA 12 — [doi:10.1186/s12966-015-0241-1](https://doi.org/10.1186/s12966-015-0241-1)
- Koutoukidis DA ve ark. (2019) IJBNPA 16 — [doi:10.1186/s12966-019-0810-9](https://doi.org/10.1186/s12966-019-0810-9)
- Payne Riches S ve ark. (2019) Appetite 133:378 — [doi:10.1016/j.appet.2018.11.028](https://doi.org/10.1016/j.appet.2018.11.028)
- Bunten A ve ark. (2021) PLOS ONE 16:e0246455 — [doi:10.1371/journal.pone.0246455](https://doi.org/10.1371/journal.pone.0246455)
- Schruff-Lim EM ve ark. (2024) Appetite 194:107158 — [doi:10.1016/j.appet.2023.107158](https://doi.org/10.1016/j.appet.2023.107158)
- Jansen L, van Kleef E, Van Loo EJ (2021) IJBNPA 18 — [doi:10.1186/s12966-021-01222-8](https://doi.org/10.1186/s12966-021-01222-8)
- Piernas C ve ark. (2024) JMIR mHealth 12:e45854 — [doi:10.2196/45854](https://doi.org/10.2196/45854)
- Wrieden WL, Levy LB (2016) PHN 19:2388 — [doi:10.1017/S1368980016000513](https://doi.org/10.1017/S1368980016000513)
- Sutherland R ve ark. (2021) JMIR 23:e25256 — [doi:10.2196/25256](https://doi.org/10.2196/25256)
- Huang A ve ark. (2006) PLoS Clin Trials 1:e22 — [doi:10.1371/journal.pctr.0010022](https://doi.org/10.1371/journal.pctr.0010022)

**Satın alma skorları:**
- Brewster PJ ve ark. (2017) J Food Compos Anal — [doi:10.1016/j.jfca.2017.07.012](https://doi.org/10.1016/j.jfca.2017.07.012)
- Brewster PJ ve ark. (2019) JAND — [doi:10.1016/j.jand.2018.08.165](https://doi.org/10.1016/j.jand.2018.08.165)
- Parker HW ve ark. (2021) BJN — [doi:10.1017/S0007114520004833](https://doi.org/10.1017/S0007114520004833)
- Taylor A ve ark. (2015) BJN 114:2129 — [doi:10.1017/S0007114515003827](https://doi.org/10.1017/S0007114515003827)
- Tharrey M ve ark. (2019) PHN 22:765 — [doi:10.1017/S1368980018003154](https://doi.org/10.1017/S1368980018003154)
- Perignon M ve ark. (2023) EJN 62:363 — [doi:10.1007/s00394-022-02962-4](https://doi.org/10.1007/s00394-022-02962-4)
- Khoury N ve ark. (2022) Front Nutr — [doi:10.3389/fnut.2022.897089](https://doi.org/10.3389/fnut.2022.897089)
- Colizzi C ve ark. (2024) BJN — [doi:10.1017/S0007114524002630](https://doi.org/10.1017/S0007114524002630)
- Dubois C, Tharrey M, Darmon N (2017) PHN 20:3051 — [doi:10.1017/S1368980017002282](https://doi.org/10.1017/S1368980017002282)

**LLM + optimizasyon:**
- Ramamonjison R ve ark. (2023) NL4Opt, PMLR 220 — [link](https://proceedings.mlr.press/v220/ramamonjison23a.html)
- AhmadiTeshnizi A, Gao W, Udell M (2024) OptiMUS, ICML — [PMLR v235](https://proceedings.mlr.press/v235/ahmaditeshnizi24a.html)
- Xiao Z ve ark. (2024) Chain-of-Experts, ICLR — [link](https://proceedings.iclr.cc/paper_files/paper/2024/hash/d45ee77826332c100a1e15f7765b99ff-Abstract-Conference.html)
- Huang C, Tang Z ve ark. (2025) ORLM, Operations Research 73:2986 — [doi:10.1287/opre.2024.1233](https://doi.org/10.1287/opre.2024.1233)
- Jiang C ve ark. LLMOPT — [arXiv 2410.13213](https://arxiv.org/abs/2410.13213)
- Astorga N ve ark. (2025) Autoformulation, ICML — [PMLR v267](https://proceedings.mlr.press/v267/astorga25a.html)
- Li B ve ark. (2023) OptiGuide — [arXiv 2307.03875](https://arxiv.org/abs/2307.03875)
- Xiao Z ve ark. (2025) Survey — [arXiv 2508.10047](https://arxiv.org/abs/2508.10047)
- Zhu P ve ark. (2026) IR2Solve — [arXiv 2608.02641](https://arxiv.org/abs/2608.02641)
- Liu H ve ark. (2026) Opt-Verifier — [arXiv 2605.29556](https://arxiv.org/abs/2605.29556)
- Abdul Rahman S ve ark. (2026) VeriSimpl — [arXiv 2607.20474](https://arxiv.org/abs/2607.20474)
- Ge S ve ark. (2026) InterOPT — [arXiv 2609.05258](https://arxiv.org/abs/2609.05258)
- Sadeghi S ve ark. (2026) SAILOR — [arXiv 2609.13945](https://arxiv.org/abs/2609.13945)
- Geng S ve ark. (2023) EMNLP — [doi:10.18653/v1/2023.emnlp-main.674](https://doi.org/10.18653/v1/2023.emnlp-main.674)
- Geng S ve ark. (2025) JSONSchemaBench — [arXiv 2501.10868](https://arxiv.org/abs/2501.10868)

**Tercih öğrenme, bandit ve inverse optimization:**
- Li L ve ark. (2010) WWW — [doi:10.1145/1772690.1772758](https://doi.org/10.1145/1772690.1772758)
- Li L ve ark. (2011) WSDM — [doi:10.1145/1935826.1935878](https://doi.org/10.1145/1935826.1935878)
- Chapelle O, Li L (2011) NeurIPS — [link](https://proceedings.neurips.cc/paper/2011/hash/e53a0a2978c28872a4505bdb51db06dc-Abstract.html)
- Wang S, Chen W (2018) ICML — [arXiv 1803.04623](https://arxiv.org/abs/1803.04623)
- Chan TCY, Mahmood R, Zhu IY (2025) OR 73(2) — [doi:10.1287/opre.2022.0382](https://doi.org/10.1287/opre.2022.0382)
- Keshavarz A, Wang Y, Boyd S (2011) — [doi:10.1109/ISIC.2011.6045410](https://doi.org/10.1109/ISIC.2011.6045410)
- Aswani A ve ark. (2018) OR — [doi:10.1287/opre.2017.1705](https://doi.org/10.1287/opre.2017.1705)
- Bärmann A ve ark. (2017) ICML — [PMLR v70](https://proceedings.mlr.press/v70/barmann17a.html)
- Ghobadi K, Mahmoudzadeh H (2021) EJOR 290:829 — [doi:10.1016/j.ejor.2020.08.048](https://doi.org/10.1016/j.ejor.2020.08.048)
- Shahmoradi Z, Lee T (2022) OR 70:2538 — [doi:10.1287/opre.2021.2143](https://doi.org/10.1287/opre.2021.2143)

**Hane ve grup:**
- Deptford A ve ark. (2017) BMC Nutr 3 — [doi:10.1186/s40795-017-0136-4](https://doi.org/10.1186/s40795-017-0136-4)
- Frega R ve ark. (2012) FNB 33:S228 — [doi:10.1177/15648265120333S212](https://doi.org/10.1177/15648265120333S212)
- Weisell R, Dop MC (2012) FNB 33:S157 — [doi:10.1177/15648265120333S203](https://doi.org/10.1177/15648265120333S203)
- Masthoff J (2015) — [doi:10.1007/978-1-4899-7637-6_22](https://doi.org/10.1007/978-1-4899-7637-6_22)
- Tran TNT ve ark. (2018) JIIS 50:501 — [doi:10.1007/s10844-017-0469-0](https://doi.org/10.1007/s10844-017-0469-0)
- Kalpakoglou K ve ark. (2025) Nutrients 17:3892 — [doi:10.3390/nu17243892](https://doi.org/10.3390/nu17243892)
- Bertsimas D, Farias VF, Trichakis N (2011) OR 59:17 — [doi:10.1287/opre.1100.0865](https://doi.org/10.1287/opre.1100.0865)

**Kombinatoryal optimizasyon ve MOEA:**
- Sinha P, Zoltners AA (1979) OR 27:503 — [doi:10.1287/opre.27.3.503](https://doi.org/10.1287/opre.27.3.503)
- Kellerer H, Pferschy U, Pisinger D (2004) Knapsack Problems — [doi:10.1007/978-3-540-24777-7](https://doi.org/10.1007/978-3-540-24777-7)
- Caprara A ve ark. (2000) EJOR 123:333 — [doi:10.1016/S0377-2217(99)00261-1](https://doi.org/10.1016/S0377-2217(99)00261-1)
- Magazine MJ, Chern MS (1984) MOR 9:244 — [doi:10.1287/moor.9.2.244](https://doi.org/10.1287/moor.9.2.244)
- Kulik A, Shachnai H (2010) IPL 110:707 — [doi:10.1016/j.ipl.2010.05.031](https://doi.org/10.1016/j.ipl.2010.05.031)
- Gomory RE, Baumol WJ (1960) Econometrica 28:521 — [doi:10.2307/1910130](https://doi.org/10.2307/1910130)
- Haimes YY, Lasdon LS, Wismer DA (1971) IEEE TSMC — [doi:10.1109/TSMC.1971.4308298](https://doi.org/10.1109/TSMC.1971.4308298)
- Mavrotas G (2009) AMC 213:455 — [doi:10.1016/j.amc.2009.03.037](https://doi.org/10.1016/j.amc.2009.03.037)
- Mavrotas G, Florios K (2013) AMC 219:9652 — [doi:10.1016/j.amc.2013.03.002](https://doi.org/10.1016/j.amc.2013.03.002)
- Deb K ve ark. (2002) IEEE TEVC 6:182 — [doi:10.1109/4235.996017](https://doi.org/10.1109/4235.996017)
- Zitzler E, Thiele L (1999) IEEE TEVC 3:257 — [doi:10.1109/4235.797969](https://doi.org/10.1109/4235.797969)
- Ishibuchi H ve ark. (2015) EMO, LNCS 9019 — [doi:10.1007/978-3-319-15892-1_8](https://doi.org/10.1007/978-3-319-15892-1_8)
- Derrac J ve ark. (2011) SWEVO 1:3 — [doi:10.1016/j.swevo.2011.02.002](https://doi.org/10.1016/j.swevo.2011.02.002)
- Vargha A, Delaney HD (2000) JEBS 25:101 — [doi:10.3102/10769986025002101](https://doi.org/10.3102/10769986025002101)
- Laporte G, Riera-Ledesma J, Salazar-González JJ (2003) OR 51:940 — [doi:10.1287/opre.51.6.940.24921](https://doi.org/10.1287/opre.51.6.940.24921)

**Yakın ürün ve sistem çalışmaları:**
- Szymanski A ve ark. (2026) CHI — [doi:10.1145/3772318.3793193](https://doi.org/10.1145/3772318.3793193)
- Jansen L, Bennin K (2025) IJIM-DI 5:100303 — [doi:10.1016/j.jjimei.2024.100303](https://doi.org/10.1016/j.jjimei.2024.100303)
- Aguilera Moreno F (2026) — [arXiv 2605.13849](https://arxiv.org/abs/2605.13849)

**Rehberler:**
- WHO (2015) Sugars — [NBK285525](https://www.ncbi.nlm.nih.gov/books/NBK285525/)
- WHO (2012) Sodium — [NBK133292](https://www.ncbi.nlm.nih.gov/books/NBK133292/)
- WHO (2023) SFA/TFA — [NBK594769](https://www.ncbi.nlm.nih.gov/books/NBK594769/)
- TÜBER 2022 sunum — [HSGM PDF](https://hsgm.saglik.gov.tr/media/attachments/2025/05/12/turkiye-beslenme-rehberi-2022.pdf)
- TÜBER 2022 tam metin (açılamadı) — [HSGM depo](https://hsgm.saglik.gov.tr/depo/birimler/saglikli-beslenme-ve-hareketli-hayat-db/Dokumanlar/Rehberler/Turkiye_Beslenme_Rehber_TUBER_2022_min.pdf)
