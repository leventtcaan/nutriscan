> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24**
> Bu dosya karar değil, fikir havuzu. Buradaki hiçbir öneri `plan/kararlar.md`'ye girmeden kesinleşmiş sayılmaz.
> Ekip, stack (mobil tarafı dahil), ders yönergesi, önceki MVP'nin içeriği hâlâ **bilinmiyor** — varsayım olan yerler `[VARSAYIM]` diye işaretli.

# NutriScan — AI Feature Havuzu, Literatür ve Kapsam Taslağı

## 0. TL;DR (3 cümle)

1. 2025-26 pazarı "barkod okut → skor göster"i geçti: kazananlar **(a)** kişiye göre açıklanan karar, **(b)** veri yoksa kamerayla etiketi okuyan fallback, **(c)** hane/aile profili, **(d)** kaynak gösteren asistan yapıyor. Plate-calorie ve market-sepeti agent'ları ise hâlâ doğruluk/entegrasyon sorunu yaşıyor.
2. Literatür net bir mesaj veriyor: **LLM'ler beslenme/güvenlik kararında tek başına güvenilmez** (tehlikeli öneri, porsiyon hatası, halüsinasyon); en iyi sonuç **deterministik kural + kılavuz-RAG + LLM açıklaması** hibritinde. Bu, NutriScan'in mimari tezi ve rapordaki "katkı" olabilir.
3. Önerilen farklılaştırıcılar: **Açıklanabilir Güvenlik Motoru (karar izi)**, **Türkçe etiket fallback + moderasyonlu veri döngüsü**, **Hane modu**, **Kaynaklı asistan + eval harness**. Türkiye'ye özgü bonus: **Tağşiş radarı**.

---

## 1. Pazar taraması — 2025-2026'da öne çıkan AI özellikleri

| Özellik | Gerçek örnek (2025-26) | Ne öğreniyoruz | NutriScan için yorum |
|---|---|---|---|
| **Vision LLM ile etiket okuma** | Open Food Facts: OCR'dan gelen içindekiler listesini fine-tune edilmiş açık kaynak LLM ile düzeltiyor (Ingredients Spellcheck); besin tablosu için LayoutLMv3 tabanlı çıkarım ([Robotoff](https://openfoodfacts.github.io/robotoff/), [TDS yazısı](https://towardsdatascience.com/how-did-open-food-facts-use-open-source-llms-to-enhance-ingredients-extraction-d74dfe02e0e4/)). Türkiye'de ÇabukBak, Ürün Dedektörü, İçerik Tara etiket fotoğrafı analiz ediyor ([ÇabukBak](https://cabukbak.com/), [Ürün Dedektörü](https://urundedektoru.com/), [İçerik Tara](https://www.gidakontrol.com/)). | Ambalaj OCR'ı zor: HalalBench'te klasik OCR motorlarının en iyisi F1 ≈ 0.19 ([arXiv 2604.22754](https://arxiv.org/abs/2604.22754)). Vision LLM'ler daha iyi ama hata yapıyor → **kullanıcı onayı şart**. | **Farklılaştırıcı.** OFF'ta Türk ürün kapsamı zayıf [doğrulanmalı]; fallback olmadan uygulama ilk haftada "ürün bulunamadı" ekranına döner. |
| **Menü / tabak okuma** | Menü: FoodPickAI, Allergy Lens, MenuBuddy ([Allergy Lens](https://play.google.com/store/apps/details?id=com.emisa.allergylens&hl=en_US), [MenuBuddy](https://menubuddy.app/)). Tabak: Cal AI, MyFitnessPal Meal Scan ([MFP](https://www.prnewswire.com/news-releases/myfitnesspal-announces-its-2025-summer-release-302536319.html)), Dexcom Stelo photo meal logging ([Dexcom](https://investors.dexcom.com/news/news-details/2025/Dexcom-Launches-Revolutionary-AI-Powered-Meal-Logging-Feature-Across-Glucose-Biosensing-Portfolio/default.aspx)). | Tabakta **tanıma iyi, porsiyon kötü**: genel LLM'lerde enerji/ağırlıkta ~%40 ortalama hata raporlanıyor ([özet](https://kcalm.app/blog/chatgpt-calorie-counting-accuracy/)); OmniFood-Bench porsiyon ve riskli hasta önerilerinde ciddi açık buluyor ([arXiv 2607.08423](https://arxiv.org/abs/2607.08423)). | Menü tarama = wow-demo adayı (alerjen odaklı, kalori değil). Tabak kalorisi = **Sonraya**; jüri önünde yanlış sayı vermek riskli. |
| **Conversational shopping assistant** | Instacart Cart Assistant (Kasım 2025, Caper smart cart'lara gömülü) ([Instacart](https://investors.instacart.com/news-releases/news-release-details/instacart-announces-new-enterprise-ai-solutions-democratize-ai)); MyFitnessPal AI Coach (Haziran 2026) ([MFP](https://news.myfitnesspal.com/twenty-years-of-nutrition-data-and-one-ai-coach-that-puts-it-all-to-work-for-you/)). | Asistanın değeri **kişisel veriye bağlanınca** ortaya çıkıyor (geçmiş, hedef). Genel sohbet botu tek başına fark yaratmıyor. | Asistanı "ChatGPT klonu" değil, **ürün + profil + geçmiş bağlamlı ve kaynaklı** yap. |
| **Kişiselleştirilmiş açıklanabilir skor** | Yuka kişisel filtreler (gluten, laktoz...) ([App Store](https://apps.apple.com/us/app/yuka-food-cosmetic-scanner/id1092799236)); Fig 2.800+ diyet, diyetisyenlerle 50.000+ diyet-içerik ilişkisi ([Fig](https://foodisgood.com/), [Fig clinicians](https://foodisgood.com/clinicians/)). | Fig'in gücü AI değil, **uzman onaylı kural tabanı**. Yuka eser miktar (trace) alerjeni hesaba katmıyor → boşluk. | Kural tabanı (TGK 14 alerjen + Türkçe eş anlamlılar) + "neden" açıklaması = çekirdek. "Eser miktarda içerebilir" ayrı seviye = kolay fark. |
| **RAG ile klinik kılavuza dayalı açıklama** | Akademide: KBH (böbrek) diyeti için NKF 2020 kılavuzuyla RAG; RAG en yüksek doğruluk ama yine de zararlı yanlışlar ([J Ren Nutr 2025, PubMed 39864474](https://pubmed.ncbi.nlm.nih.gov/39864474/)). Diyabet tarif analizi: kılavuz verilince LLM'ler iyileşiyor ([arXiv 2609.03967](https://arxiv.org/abs/2609.03967)). | RAG **gerekli ama yeterli değil** → çıktıya guardrail + eval gerekiyor. | Türkçe kaynak: **TÜBER 2022** ([Sağlık Bakanlığı PDF](https://hsgm.saglik.gov.tr/media/attachments/2025/05/12/turkiye-beslenme-rehberi-2022.pdf)), **TGK Etiketleme Yönetmeliği** ([Tarım Bak.](https://www.tarimorman.gov.tr/Konu/2088/TGK_Etiketleme_Tuketici_Bilgilendirme_Yonetmelik_Kilavuz)). Hastalık kılavuzları (çölyak, diyabet, KBH) lisans kontrolü gerekir. |
| **Agentic: plan → liste → sepet** | Walmart Sparky: "akşama ne yesek" → haftalık plan → sepete ekleme; Mart 2026'da ChatGPT Instant Checkout'tan çekildi (doğruluk/entegrasyon) ([Grocery Dive](https://www.grocerydive.com/news/walmart-sparky-chatgpt-instant-checkout/815961/), [DC360](https://www.digitalcommerce360.com/2026/03/19/ecommerce-trends-walmart-agentic-commerce-evolving/)); Instacart ChatGPT app ([Barchart](https://www.barchart.com/story/news/36507554/instacart-app-launches-in-openai-chatgpt-first-company-to-offer-new-instant-checkout-app-experience)). | Walmart bile sepet otomasyonunda geri adım attı. Türkiye'de Migros/Getir/Trendyol için **public API yok** [doğrulanmalı]. | "Profilime uygun alışveriş listesi" = yapılabilir. "Markete sepet at" = **Sonraya** (entegrasyon yok, scraping riskli). |
| **CGM / giyilebilir** | Dexcom Stelo GenAI haftalık içgörü + 2026'da günlük 3 öneri ([Dexcom 2026](https://investors.dexcom.com/news/news-details/2026/Stelo-Adds-Enhanced-Smart-Meal-Logging-Features-as-Dexcom-Continues-to-Transform-Personal-Glucose-Management/default.aspx)); January AI: sensörsüz glukoz tahmini, barkod/foto/ses ile ([January](https://january.ai/consumers)). Health Connect 50+ veri tipi, Mart 2025'ten beri FHIR medical records ([Wikipedia](https://en.wikipedia.org/wiki/Health_Connect)); RN kütüphaneleri: `react-native-health-connect`, `@kingstinct/react-native-healthkit` ([GitHub](https://github.com/matinzd/react-native-health-connect)). | Okuma teknik olarak kolay; **anlamlı korelasyon** için gerçek CGM'li kullanıcı ve haftalar süren veri lazım. Ekipte CGM kullanan yoksa demo boş kalır. | **Sonraya** (ya da sadece kilo/adım okuyan "light" entegrasyon). |
| **Sesli asistan** | MyFitnessPal Voice Log (Aralık 2024) ([PR](https://www.prnewswire.com/news-releases/say-it-log-it-myfitnesspal-unveils-voice-log-302329040.html)); January sesli kayıt. | Ses = yeni bir input kanalı, pipeline aynı. Türkçe STT artık yeterince iyi. | Wow-demo: markette "bunu kızım yiyebilir mi?" → aynı karar motoru. Düşük maliyet, yüksek şov. |
| **Family / household modu** | Fig "Multiple Figs": tek hesapta 5 profil, ortak uyumlu ürün bulma ([Fig destek](https://foodisgood.com/support/multiple-figs/)); Yuko Scan aile profilleri. Yuka'da yok. | Rakiplerde bile kaba (paylaşımlı şifre!). Gerçek hane modeli (davet, rol, çocuk profili) nadir. | **Farklılaştırıcı.** Veri modeli işi, AI değil → öğrenciler için güvenli. |
| **Diyetisyen/klinisyen paneli (B2B2C)** | Fig klinisyenlere ücretsiz Fig+ ve hasta materyali veriyor ([Fig clinicians](https://foodisgood.com/clinicians/)); January AI EHR entegrasyonu ([Nutrition Insight](https://www.nutritioninsight.com/news/january-ai-health-app-medical-records-glucose.html)). | B2B2C büyük bir ikinci ürün (rol, izin, KVKK, ayrı UI). | Tam panel = **Sonraya**. "Diyetisyenle paylaşılabilir salt-okunur rapor linki" = v1'de ucuz versiyon. |

**Türkiye rakip notu:** ÇabukBak, Ürün Dedektörü, İçerik Tara, AllergicApp zaten "barkod + AI analiz + kişisel uyarı" yapıyor. Yani **"barkod okut, AI yorumlasın" tek başına özgün değil.** Özgünlük; karar şeffaflığı, veri kalitesi döngüsü, hane modu ve ölçülmüş doğrulukta aranmalı.

**Türkiye'ye özgü fırsat — Tağşiş radarı:** Tarım ve Orman Bakanlığı "Taklit veya Tağşiş Yapılan Gıdalar" listesini firma/marka/ürün/parti no ile yayınlıyor ([Güvenilir Gıda](https://guvenilirgida.tarimorman.gov.tr/GuvenilirGida/gkd/TaklitVeyaTagsis)). API yok; sayfa periyodik çekilip marka+kategori eşleştirilebilir. Hukuki risk: "bu ürün sahte" deme, "bu markanın şu partisi listede, kaynak: ..." de.

---

## 2. Literatür taraması temeli (12 kaynak)

**A. Kişiselleştirilmiş / sağlık-farkındalıklı öneri**
1. Zhang ve ark., **MOPI-HFRS** — tercih + kişisel sağlık + çeşitlilik için çok amaçlı (Pareto) graph öneri, LLM ile açıklama. arXiv 2412.08847, 2024 (KDD 2025). https://arxiv.org/abs/2412.08847
2. Yang ve ark., **ChatDiet** — kişisel + popülasyon modeli, causal inference, LLM ile açıklamalı öneri chatbot'u. Smart Health 32, 2024. https://arxiv.org/abs/2403.00781
3. Mohbat & Zaki, **KERL** — food knowledge graph + LLM ile kişisel tarif önerisi ve besin analizi. ACL 2025. https://arxiv.org/abs/2505.14629
4. Yang & Rahmani, **Personalized Causal Graph Reasoning for LLMs** — kişisel causal graph üzerinde LLM akıl yürütmesi, glukoz odaklı öneri. arXiv 2503.00134, 2025. https://arxiv.org/abs/2503.00134
5. Zhang ve ark., **NGQA** — NHANES/FNDDS ile kişiye özel "bu gıda bana sağlıklı mı" graph QA benchmark'ı. arXiv 2412.15547, 2024. https://arxiv.org/abs/2412.15547
6. **Explanation interface for healthy food recommendations** — iş yeri dağıtımında açıklama arayüzü; açıklamalar anlamayı ve kontrol hissini artırıyor. JMIR mHealth uHealth 2025. https://mhealth.jmir.org/2025/1/e51271

**B. Etiket / içerik metninden bilgi çıkarımı (alerjen tespitinin temeli)**
7. Arief, **HalalBench** — 14 dilde 1.043 ambalaj görseli; klasik OCR'ın ambalajda çöktüğünü gösteriyor (en iyi F1 ≈ 0.19). arXiv 2604.22754, 2026. https://arxiv.org/abs/2604.22754
8. Coburn ve ark., **ACETADA** — 8 büyük multimodal modelin beslenme analizi; bağlam metadata'sı ve CoT hatayı düşürüyor. arXiv 2507.07048, 2025. https://arxiv.org/abs/2507.07048
9. Open Food Facts / Robotoff — üretimde çalışan ingredient detection + LLM spellcheck + nutrition extraction (gri literatür ama gerçek sistem). https://openfoodfacts.github.io/robotoff/

**C. LLM beslenme güvenliği, halüsinasyon ve değerlendirme**
10. Hua ve ark., **NutriBench** — 11.857 insan-doğrulamalı öğün açıklaması, 12 LLM; CoT/RAG karşılaştırması. arXiv 2407.12843. https://arxiv.org/abs/2407.12843
11. Luo ve ark., **Cooking Up Risks / FoodGuardBench** — FDA kılavuzlu 3.339 sorgu; LLM'ler gıda güvenliğinde zayıf ve jailbreak'e açık; FoodGuard-4B guardrail modeli. arXiv 2604.01444, 2026. https://arxiv.org/abs/2604.01444
12. Mao ve ark., **FAM-Bench** — 13 hastalık için 2.500 uzman-doğrulamalı örnek; "bu yemek bu hastalığa uygun mu" multimodal akıl yürütme. arXiv 2605.31410, 2026. https://arxiv.org/abs/2605.31410

**Yedek / destekleyici:** OmniFood-Bench (VLM'ler yemeği tanıyor, porsiyonda ve riskli hastada tehlikeli) https://arxiv.org/abs/2607.08423 · Azimi ve ark., LLM'ler Registered Dietitian sınavında, RAG ve prompt etkisi https://arxiv.org/abs/2408.02964 · KBH diyetinde LLM vs RAG, J Ren Nutr 2025 https://pubmed.ncbi.nlm.nih.gov/39864474/ · Venkataramanan ve ark., LLM'ler diyabet için tarif analizi (2026) https://arxiv.org/abs/2609.03967 · Pucci ve ark., yeme bozukluğu sorgularında LLM'lerin "false safety"si (2026) https://arxiv.org/abs/2606.02444

**Literatürden çıkan tez (raporda "motivasyon" olabilir):**
LLM'ler tanıma ve açıklamada güçlü; **karar verme** (bu ürün bu kişi için güvenli mi?) ve **sayısal tahminde** güvenilmez. Bu yüzden: *karar = deterministik ve denetlenebilir, açıklama = LLM + kaynak, her ikisi = ölçülür.*

---

## 3. Feature fikir havuzu

Zorluk: 1 (kolay) – 5 (çok zor), 3 deneyimsiz kişi + AI coding agent varsayımıyla.

| # | Fikir | Kullanıcı değeri | Şov değeri | Zorluk | Veri bağımlılığı | Risk |
|---|---|---|---|---|---|---|
| 1 | Sağlık/alerji profili (TGK 14 alerjen + diyet + durum: çölyak, diyabet, laktoz, vegan, helal) | Temel | Düşük | 1 | Yok | KVKK: sağlık verisi = özel nitelikli |
| 2 | Barkod tarama + OFF lookup + yerel cache/mirror | Temel | Düşük | 2 | OFF (15 okuma/dk/IP limiti) | Rate limit, eksik TR veri |
| 3 | **Deterministik uygunluk motoru** (kural + Türkçe eş anlamlı sözlük + E-kodu eşleme: "peynir altı suyu tozu" → süt) | Çok yüksek | Orta | 3 | Kendi sözlüğümüz | Sözlük eksikse yanlış "güvenli" |
| 4 | **Açıklanabilir verdict** (Yeşil/Sarı/Kırmızı + "neden" + hangi içerik + kaynak) | Çok yüksek | Yüksek | 2 | #3 | Aşırı basitleştirme |
| 5 | "Eser miktarda içerebilir" ayrı seviye (precautionary labeling) | Yüksek (ağır alerjikler) | Orta | 1 | OFF `traces` alanı | Veri eksik |
| 6 | Tarama geçmişi + alışveriş günlüğü | Orta | Düşük | 1 | Yok | — |
| 7 | **Etiket fotoğrafı fallback** (vision LLM → structured JSON → kullanıcı onayı) | Çok yüksek (TR kapsama açığı) | Yüksek | 3 | LLM API | OCR hatası, maliyet |
| 8 | Kullanıcı düzeltmesi + **moderasyon kuyruğu** | Yüksek (veri kalitesi) | Orta (admin demosunda yüksek) | 3 | Kullanıcılar | Spam/yanlış veri |
| 9 | **Hane modu**: tek tarama → tüm aile profilleri matrisi (çocuk fıstık, baba diyabet, anne çölyak) | Çok yüksek | Yüksek | 2 | Yok | Davet/rol karmaşası |
| 10 | **Kaynaklı asistan** (RAG: TÜBER 2022, TGK, seçili hastalık kılavuzları; ürün + profil bağlamı; cevapta kaynak) | Yüksek | Çok yüksek | 4 | Kılavuz PDF'leri, lisans | Halüsinasyon, tıbbi tavsiye algısı |
| 11 | **Eval harness + golden set** (etiketlenmiş 150-300 TR ürün; kural vs LLM vs hibrit precision/recall) | Dolaylı | Çok yüksek (jüri/rapor) | 3 | Manuel etiketleme emeği | Zaman |
| 12 | Daha iyi alternatif önerisi (aynı kategori, profile uygun, Nutri-Score/NOVA daha iyi) | Yüksek | Yüksek | 3 | OFF kategori verisi (TR'de zayıf) | Önerilecek aday az |
| 13 | Haftalık alışveriş içgörüsü (NOVA-4 oranı, şeker/tuz trendi + LLM özet) | Orta-yüksek | Yüksek | 3 | #6 geçmişi | Az veriyle anlamsız |
| 14 | Raf karşılaştırma: 2-3 ürünü arka arkaya tara → sana göre sırala | Yüksek | Yüksek | 2 | #3, #4 | — |
| 15 | Menü fotoğrafı tarama (restoran, alerjen odaklı) | Orta-yüksek | Çok yüksek | 3 | Vision LLM | Yanlış güven hissi; restoran tarifi bilinmez |
| 16 | Sesli soru ("bunu kızım yiyebilir mi?") STT → aynı pipeline | Orta | Yüksek | 2 | STT API | Türkçe STT, gürültü |
| 17 | Tabak fotoğrafı kalori tahmini | Orta | Yüksek | 3 | Vision LLM | ~%40 hata, jüri önünde yanlış sayı |
| 18 | Profile uygun alışveriş listesi / haftalık plan (agentic: tool calling ile ürün DB'den seç) | Yüksek | Yüksek | 4 | Ürün DB kapsamı | Önerilen ürün bulunamaz |
| 19 | Market sepetine aktarma (Migros/Getir/Trendyol) | Yüksek | Çok yüksek | 5 | Public API yok | Scraping, ToS ihlali |
| 20 | Health Connect / HealthKit okuma (kilo, adım, glukoz) | Orta | Orta | 3 | Native modül | İki platform ayrı iş |
| 21 | CGM korelasyonu ("bu ürün sende glukoz zıplatıyor") | Yüksek (diyabetik) | Çok yüksek | 5 | Gerçek CGM kullanıcısı | Test edecek kullanıcı yok |
| 22 | Diyetisyen paneli (danışan yönetimi, hedef atama) | Yüksek (B2B2C) | Yüksek | 4 | Gerçek diyetisyen | Kapsamı ikiye katlar |
| 23 | Diyetisyenle paylaşılabilir salt-okunur rapor (süreli link / PDF) | Orta | Orta | 2 | #6 | Link sızıntısı |
| 24 | **Tağşiş radarı**: taranan markanın Bakanlık listesinde kaydı varsa uyar + geçmişte aldıysan push | Yüksek (TR'ye özgü) | Çok yüksek | 3 | Bakanlık sayfası (API yok) | Yanlış eşleşme → hukuki risk |
| 25 | Offline mod (son taramalar + alerjen sözlüğü cihazda) | Orta (markette çekim yok) | Düşük | 3 | — | Senkron karmaşası |
| 26 | OFF'a geri katkı (onaylanan düzeltmeleri write API ile gönder) | Dolaylı (topluluk) | Orta-yüksek | 2 | OFF write API, ODbL | Kalitesiz veri göndermek |
| 27 | Admin **karar izi (decision trace) görüntüleyici** | Dolaylı | Çok yüksek (hoca eleştirisine cevap) | 2 | #3 | — |
| 28 | LLM monitoring paneli (trace, maliyet, latency, 👎 geri bildirim, prompt versiyonu) | Dolaylı | Yüksek | 3 | Langfuse/OTel | Ek altyapı |
| 29 | Gamification / streak | Düşük | Düşük | 2 | — | Sağlık uygulamasında ters etki |
| 30 | Çocuk/yaşlı için sadeleştirilmiş görünüm | Orta | Düşük | 2 | — | — |

### Gruplama

**Çekirdek (olmazsa olmaz)** — bunlar olmadan ürün yok:
#1 profil · #2 barkod + OFF + cache · #3 deterministik uygunluk motoru · #4 açıklanabilir verdict · #5 eser miktar seviyesi · #6 geçmiş · #8 düzeltme + moderasyon · #27 karar izi (admin) · structured logging + audit log (bkz. §4)

**Farklılaştırıcı (bizi özgün yapan 4 şey)**
1. **Açıklanabilir Güvenlik Motoru** (#3+#4+#27+#11): "Karar LLM'e bırakılmaz." Kural motoru karar verir, her karar bir *Decision Record* üretir (hangi içerik, hangi kural, hangi veri kaynağı/versiyonu), LLM sadece bunu insan diliyle anlatır. Golden set ile **ölçülmüş** doğruluk (kural vs LLM-only vs hibrit). Hem jüri hem rapor için "mühendislik + araştırma" katkısı.
2. **Türkçe etiket fallback + veri kalitesi döngüsü** (#7+#8+#26): OFF'ta yoksa fotoğraf → vision LLM → yapılandırılmış öneri → kullanıcı onayı → moderasyon → (opsiyonel) OFF'a katkı. Türkiye kapsama açığını çözen gerçek bir data flywheel.
3. **Hane modu** (#9): tek tarama, tüm aile için matris. AI değil ama kullanıcı değeri çok yüksek, rakiplerde kaba.
4. **Kaynaklı asistan** (#10): sadece TÜBER/TGK/seçili kılavuzlardan cevap, her cümlede kaynak, emin değilse "bilmiyorum/diyetisyene danış". Eval harness'ten geçer.
   - *Alternatif 4. madde:* **Tağşiş radarı** (#24) — Türkiye'ye özgü, jüride çok akılda kalır, teknik olarak asistandan kolay; ama hukuki dil dikkat ister.

**Wow-demo (sunumda 30 saniyede etki)**
#14 raf karşılaştırma · #16 sesli soru · #15 menü tarama · #24 tağşiş radarı · admin'de canlı karar izi + eval dashboard'u (#27, #28, #11)
Demo senaryosu önerisi: *"Annesi çölyak, çocuğu fıstık alerjik bir aile markette"* → ürün OFF'ta yok → etiket fotoğrafı → matris kararı → sesli soru → admin'de o taramanın karar izi.

**Sonraya (v2 / "future work" bölümü)**
#17 tabak kalorisi · #18 haftalık plan agent'ı (v1 sonu mümkünse) · #19 market sepeti · #20-21 Health Connect/CGM · #22 tam diyetisyen paneli · #25 offline · #29 gamification · #30 sade görünüm

---

## 4. Admin / operasyon ve observability

Hocaların "loglar daha açıklayıcı olmalı" eleştirisinin kökü genelde şu: loglar **teknik gürültü** (`INFO Controller called`), **iş olayı** ve **denetim kaydı** ayrılmamış. Üç katmanı ayır:

| Katman | Amaç | Nerede | Örnek |
|---|---|---|---|
| **Technical log** | Hata ayıklama | stdout JSON → Loki/ELK | `ERROR off.client timeout after 3000ms` |
| **Domain event log** | "Sistemde ne oldu?" | JSON log + metrik | `scan.completed`, `label.extracted`, `verdict.issued` |
| **Audit log** | "Kim neyi değiştirdi?" (yasal, değişmez) | Append-only DB tablosu | Admin X, ürün 869... alerjenini `süt` ekledi, gerekçe, önce/sonra |

### 4.1 Structured logging — somut kurallar
- Her request'e `traceId` (OpenTelemetry) ve MDC'ye `userIdHash`, `scanId`, `profileVersion`. Kullanıcı ID'si **hash'li**, sağlık verisi logda **asla düz metin değil**.
- Log mesajı değil **olay adı + alanlar**: `event=verdict.issued` gibi sabit bir event taxonomy (`plan/`'da belgelenir).
- Her tarama bir **Decision Record** üretir (DB'de saklanır, admin'de okunur). Örnek:

```json
{
  "event": "verdict.issued",
  "traceId": "4bf92f...",
  "scanId": "scn_01J...",
  "userIdHash": "a3f9...",
  "profileVersion": 4,
  "barcode": "8690504012345",
  "dataSource": {"type": "OFF_CACHE", "fetchedAt": "2026-09-12T10:02:11Z", "offRevision": 37},
  "rulesFired": [
    {"ruleId": "ALG-GLUTEN-03", "version": 2, "matched": "buğday unu", "severity": "BLOCK"},
    {"ruleId": "TRACE-NUT-01", "version": 1, "matched": "fındık izi içerebilir", "severity": "WARN"}
  ],
  "verdict": "RED",
  "householdVerdicts": {"member_1": "RED", "member_2": "YELLOW"},
  "explanation": {"llmCallId": "gen_...", "model": "...", "promptVersion": "explain-v3", "latencyMs": 820, "tokens": 412, "cached": false},
  "totalLatencyMs": 1130
}
```
- Admin'de bu kayıt **insan cümlesine** çevrilerek gösterilir: *"Profil v4 (çölyak, fındık) 8690504012345'i taradı → OFF cache (12 gün önce) → ALG-GLUTEN-03 'buğday unu' ile tetiklendi → KIRMIZI → açıklama 820 ms."* Hocaya gösterilecek ekran bu.

### 4.2 Admin panel modülleri
1. **Dashboard:** günlük tarama, aktif kullanıcı, OFF hit/miss oranı, fallback (etiket foto) oranı, verdict dağılımı, p95 latency, LLM maliyeti/gün, hata oranı.
2. **Karar izi arama:** barkod / scanId / traceId ile tek taramanın tüm hikâyesi (§4.1).
3. **Ürün verisi moderasyonu:** kullanıcı düzeltmeleri kuyruğu; **diff görünümü** (OFF vs önerilen), onay/red + gerekçe, katkıcı güven puanı, "OFF'a gönder" butonu.
4. **Kural & sözlük yönetimi:** alerjen eş anlamlıları, E-kodları, kural versiyonlama; değişiklik → audit log + golden set otomatik tekrar koşar ("bu değişiklik 3 testi kırdı").
5. **LLM izleme:** trace listesi (prompt versiyonu, model, token, maliyet, latency), 👎 alan cevaplar kuyruğu, guardrail'e takılanlar, eval koşularının zaman serisi.
6. **Audit log görüntüleyici:** kim / ne / ne zaman / önce-sonra JSON / gerekçe; filtrelenebilir, silinemez.
7. **KVKK işlemleri:** veri dışa aktarma ve silme talepleri; destek için kullanıcı verisine bakmak "gerekçe yaz + logla" (break-glass) ile.
8. **Feature flags:** LLM özelliklerini canlıda kapatabilme (maliyet/kalite olayında).

### 4.3 LLM evals — minimum ciddi kurulum
- **Golden set:** 150-300 Türk ürünü, alerjenleri elle etiketlenmiş (3 kişi × ~70 ürün, çapraz kontrol). Karar motorunun precision/recall'u; **false negative (yanlış "güvenli")** ayrıca raporlanır — sağlıkta asıl metrik bu.
- **Açıklama/asistan evals:** 50-100 soru; LLM-as-a-judge ikili rubrik (kaynağa sadık mı? profil ile çelişiyor mu? tıbbi tavsiye sınırını aşıyor mu?), judge modeli sabitlenmiş ([Langfuse regression testing](https://langfuse.com/resources/engineering/llm-regression-testing), [Evidently rehberi](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)).
- **CI kapısı:** prompt veya kural değişince eval'ler koşar, eşik altındaysa merge engellenir (promptfoo veya basit JUnit parametrik testler).
- **Red-team seti:** jailbreak ve riskli sorular ("fıstık alerjim var ama azıcık yesem?"). FoodGuardBench bunun literatür karşılığı ([arXiv 2604.01444](https://arxiv.org/abs/2604.01444)).

### 4.4 Araç önerisi (öğrenci bütçesi) `[VARSAYIM: backend Spring Boot]`
- Spring Boot Actuator + Micrometer → Prometheus + Grafana (metrik).
- Logback JSON encoder → Loki (log) — ya da başlangıçta sadece Grafana Cloud free tier.
- OpenTelemetry Java agent (trace). GenAI semantic conventions hâlâ experimental ama Langfuse OTLP endpoint'i kabul ediyor ([Langfuse OTel](https://langfuse.com/integrations/native/opentelemetry)).
- Spring AI 1.0 (Mayıs 2025 GA): ChatClient, structured output, tool calling, pgvector RAG, Micrometer observability hazır ([awesome-spring-ai](https://github.com/spring-ai-community/awesome-spring-ai)).
- Sentry (hata takibi, mobil + backend).
- Admin UI: hazır admin şablonu (React-Admin / Refine) — sıfırdan tablo yazmak zaman kaybı.

---

## 5. Yapılabilirlik filtresi

### 5.1 Gerçekçi kapasite `[VARSAYIM]`
3 kişi × haftada ~12-15 saat × ~32 hafta ≈ **1.200-1.400 kişi-saat** (Ocak final dönemi ve bayramlar düşülmeli). AI coding agent'lar CRUD ve boilerplate'i hızlandırır, ama **entegrasyon, debug, veri etiketleme, deploy** hızlanmaz. Kabaca: 1 çekirdek + 3-4 farklılaştırıcı + 2-3 wow-demo + sağlam admin sığar; daha fazlası sığmaz.

### 5.2 Scope'u öldüren tuzaklar
1. **Kendi ML modelini eğitmek** (OCR, alerjen NER, kalori). → API'li vision LLM kullan; katkıyı model değil **sistem + ölçüm** yap.
2. **Tabak kalorisi / CGM / market sepeti** — demo'da parlak, doğrulukta veya entegrasyonda ölür.
3. **Her şeyi chatbot'a çevirmek.** Chat bir kanal; karar motoru olmadan boş.
4. **Mikroservis, Kubernetes, event bus** — 3 kişi için modüler monolit yeter. Mimari "temizlik" = sınırları net modüller, deploy karmaşası değil.
5. **İki native uygulama** (Swift + Kotlin). Tek cross-platform (React Native/Expo ya da Flutter) — `[Levent'e sor: ekip mobilde ne biliyor?]`
6. **OFF'a canlı bağımlılık:** 15 okuma/dk/IP, 10 arama/dk; "birkaç yüzden fazla ürün için dump indirin" diyorlar ([OFF API](https://openfoodfacts.github.io/openfoodfacts-server/api/)). → Türkiye alt kümesini JSONL dump'tan yerel Postgres'e al, gece senkronu.
7. **KVKK:** alerji/hastalık bilgisi **özel nitelikli kişisel veri**; açık rıza + aydınlatma metni + VERBİS değerlendirmesi. LLM API'si yurt dışındaysa bu **yurt dışına aktarım** (7499 sayılı Kanun, 1 Eylül 2024'ten beri yeni rejim) ([KVKK rehberi](https://www.kvkk.gov.tr/Icerik/8142/Kisisel-Verilerin-Yurt-Disina-Aktarilmasi-Rehberi)). Azaltma: LLM'e kimlik göndermeme, sadece "kısıt listesi + ürün" gönderme (veri minimizasyonu) — hukuken yeterli mi, danışmana sorulmalı.
8. **"Tıbbi tavsiye" algısı / mağaza politikası:** "teşhis/tedavi" dili kullanma; her ekranda "bilgilendirme amaçlıdır" ve alerjide nihai kontrol etiketindir uyarısı.
9. **Canlıda kullanıcı yok:** "canlıya alındı" ≠ "kullanılıyor". Şubat'tan itibaren 20-50 kişilik beta (aileler, alerji dernekleri, kampüs) planlanmazsa dashboard boş kalır.
10. **Admin'i sona bırakmak:** logging ve audit **ilk sprintte** kurulmalı; sonradan eklenen log hep yüzeysel kalır (geçen seferki hata).
11. **Türkçe sözlük emeğini küçümsemek:** "süt tozu, kazein, laktoz, peynir altı suyu, tereyağı..." — kural motorunun kalitesi bu sözlük kadar.
12. **LLM maliyeti ve gecikmesi:** açıklamaları (ürün × profil-kısıt kombinasyonu) cache'le; ucuz model varsayılan, pahalısı sadece fallback'te.

### 5.3 İdeal kapsam taslağı `[VARSAYIM: akademik takvim Ekim–Haziran]`

**MVP (Ekim → Ocak başı, ~12 hafta) — "güvenilir ve açıklanabilir tarayıcı"**
- Auth, profil (#1), hane modu veri modeli baştan (#9 — sonradan eklemek pahalı).
- OFF TR dump → yerel DB + canlı fallback + cache (#2).
- Kural motoru v1 + Türkçe sözlük v1 + eser miktar seviyesi (#3, #5).
- Verdict ekranı + şablon açıklama (LLM'siz de çalışsın) (#4), geçmiş (#6).
- Structured logging, Decision Record, audit log, basit admin (dashboard + karar izi) (#27).
- CI/CD + staging + prod deploy; golden set'in ilk 100 ürünü.
- **Çıkış kriteri:** 100 ürünlük golden set'te false negative oranı ölçülmüş ve raporlanmış.

**v1 (Şubat → Mayıs, ~14 hafta) — "farklılaştırıcılar + gerçek kullanıcı"**
- Etiket fotoğrafı fallback + moderasyon kuyruğu + (opsiyonel) OFF'a katkı (#7, #8, #26).
- Hane modu UI + davet (#9).
- LLM açıklama + kaynaklı asistan (TÜBER + TGK ile başla) + guardrail (#10).
- Eval harness CI'da, LLM izleme paneli (#11, #28).
- Wow: raf karşılaştırma (#14), sesli soru (#16); zaman kalırsa tağşiş radarı (#24) veya menü tarama (#15).
- 20-50 kişilik beta + kısa kullanıcı çalışması (SUS anketi + güven ölçümü) → rapora veri.

**Haziran:** bug bash, demo senaryosu provası, rapor. **Yeni özellik yok.**

---

## 6. Levent'e açık sorular (bu dosyadaki varsayımları kapatmak için)
1. Ders yönergesi "canlıya alma", kullanıcı sayısı, rapor formatı için ne istiyor? (`kaynak/`'a konacak)
2. Ekip mobilde ne biliyor? (React Native / Flutter / native / web-PWA)
3. Önceki MVP'de ne vardı, hangi hocalar ne eleştirdi? (sadece admin/log mu?)
4. LLM API bütçesi var mı? (aylık ~X TL; öğrenci kredileri?)
5. Hedef kullanıcı: genel sağlık bilinçli tüketici mi, alerjik/çölyak aileler mi? (farklılaştırıcı seçimini değiştirir)
6. Danışmandan KVKK / etik kurul (kullanıcı çalışması için) görüşü alınacak mı?

---

## Kaynaklar (toplu)
- Open Food Facts: [API & limitler](https://openfoodfacts.github.io/openfoodfacts-server/api/) · [Robotoff](https://openfoodfacts.github.io/robotoff/) · [LLM spellcheck yazısı](https://towardsdatascience.com/how-did-open-food-facts-use-open-source-llms-to-enhance-ingredients-extraction-d74dfe02e0e4/) · [openfoodfacts-ai](https://github.com/openfoodfacts/openfoodfacts-ai)
- Ürünler: [Yuka](https://apps.apple.com/us/app/yuka-food-cosmetic-scanner/id1092799236) · [Fig](https://foodisgood.com/) · [Fig clinicians](https://foodisgood.com/clinicians/) · [Fig multiple profiles](https://foodisgood.com/support/multiple-figs/) · [Instacart AI Solutions](https://investors.instacart.com/news-releases/news-release-details/instacart-announces-new-enterprise-ai-solutions-democratize-ai) · [Walmart Sparky / ChatGPT](https://www.grocerydive.com/news/walmart-sparky-chatgpt-instant-checkout/815961/) · [Walmart agentic commerce](https://www.digitalcommerce360.com/2026/03/19/ecommerce-trends-walmart-agentic-commerce-evolving/) · [Dexcom Stelo 2025](https://investors.dexcom.com/news/news-details/2025/Dexcom-Launches-Revolutionary-AI-Powered-Meal-Logging-Feature-Across-Glucose-Biosensing-Portfolio/default.aspx) · [Dexcom Stelo 2026](https://investors.dexcom.com/news/news-details/2026/Stelo-Adds-Enhanced-Smart-Meal-Logging-Features-as-Dexcom-Continues-to-Transform-Personal-Glucose-Management/default.aspx) · [January AI](https://january.ai/consumers) · [MFP Voice Log](https://www.prnewswire.com/news-releases/say-it-log-it-myfitnesspal-unveils-voice-log-302329040.html) · [MFP AI Coach](https://news.myfitnesspal.com/twenty-years-of-nutrition-data-and-one-ai-coach-that-puts-it-all-to-work-for-you/) · [Allergy Lens](https://play.google.com/store/apps/details?id=com.emisa.allergylens&hl=en_US) · [MenuBuddy](https://menubuddy.app/)
- Türkiye: [ÇabukBak](https://cabukbak.com/) · [Ürün Dedektörü](https://urundedektoru.com/) · [İçerik Tara](https://www.gidakontrol.com/) · [TÜBER 2022](https://hsgm.saglik.gov.tr/media/attachments/2025/05/12/turkiye-beslenme-rehberi-2022.pdf) · [TGK Etiketleme Kılavuzu](https://www.tarimorman.gov.tr/Konu/2088/TGK_Etiketleme_Tuketici_Bilgilendirme_Yonetmelik_Kilavuz) · [Alerjen etiketleme (Alerji ve Astım Derneği)](https://alerjiastim.org.tr/alerjen-etiketleme-kurallari-ve-bilinmesi-gerekenler/) · [Taklit/Tağşiş listesi](https://guvenilirgida.tarimorman.gov.tr/GuvenilirGida/gkd/TaklitVeyaTagsis) · [KVKK yurt dışı aktarım rehberi](https://www.kvkk.gov.tr/Icerik/8142/Kisisel-Verilerin-Yurt-Disina-Aktarilmasi-Rehberi) · [KVKK 2024 değişiklikleri](https://www.erdem-erdem.av.tr/bilgi-bankasi/kisisel-verilerin-korunmasi-kanununda-neler-degisti)
- Health: [Health Connect](https://en.wikipedia.org/wiki/Health_Connect) · [react-native-health-connect](https://github.com/matinzd/react-native-health-connect) · [react-native-healthkit](https://github.com/kingstinct/react-native-healthkit)
- Observability/eval: [OTel GenAI semconv rehberi](https://openobserve.ai/blog/opentelemetry-genai-semantic-conventions/) · [Langfuse OTel](https://langfuse.com/integrations/native/opentelemetry) · [Langfuse regression testing](https://langfuse.com/resources/engineering/llm-regression-testing) · [LLM-as-a-judge](https://www.evidentlyai.com/llm-guide/llm-as-a-judge) · [Spring AI kaynakları](https://github.com/spring-ai-community/awesome-spring-ai)
- Akademik: §2'deki 12 + 5 yedek kaynak.

> Not: Kalori-doğruluğu için alıntılanan "~%40 hata" rakamı ikincil kaynaktan (kcalm.app blog, Fridolfsson ve ark. 2025'e atıf yapıyor); rapora girmeden önce birincil makale bulunmalı. OFF'taki Türk ürün sayısı sorgulanamadı (sunucu 503) — `world.openfoodfacts.org/facets/countries/turkey` tekrar kontrol edilecek.
