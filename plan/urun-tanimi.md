---
title: NutriScan — Ürün Tanımı v5.2 + Gereksinimler (FR/NFR)
updated: 2026-09-29
durum: TASLAK — ekip incelemesi, 2 Ekim görüşmesine götürülecek (takvim A0.3)
dayanak: arastirma/07-tez-v5.md · plan/kararlar.md (ADR-001…011) · plan/takvim.md · arastirma/06-tez-v4.md §7–8 + docs/anayasa.md (S1–S22, K01–K21) · arastirma/05-akislar-edge-case.md · prototip v1
v5.2 (29 Eylül, ADR-015 ÖNERİ): fiyat ve ürün içeriği toplayıcıdan (pilot ŞOK + Tarım Kredi, K21); fiş çıktı (FR-8, FR-17, FR-23, M13–M14, E3)
v5.1 (27 Eylül, ADR-011): sağlık durumu profili (FR-2 yeniden, FR-28 yeni), RAG içerik eşleme (FR-29), önce güvenlik sırası
önceki sürüm: v3 (24 Eylül) — liste optimizasyonu odaklıydı; v5 tezine göre yeniden yazıldı
---
# NutriScan — Ürün Tanımı v5.1

## 1. Tek cümle
NutriScan, hangi zincirden alışveriş yapılırsa yapılsın hanenin **haftalık yemek ve alışveriş planını** kuran bir asistandır: önce her üyenin kesin kısıtını ve sağlık durumu kurallarını doğrular, kilerdekini önce kullanır, bütçe sınırı içinde fiyatı iki markete kadar optimize eder ve **her kararını kanıtıyla gösterir**.

## 2. Kimin için
| Persona | Durum | Beklentisi |
|---|---|---|
| **Planlayan ebeveyn** (birincil) | 4 kişilik hane; çocukta fındık alerjisi, eşte çölyak, anneannede diyabet ya da tansiyon; indirim marketi + semt pazarı; bütçe sıkışık | "Bu hafta ne pişirip ne alayım ki kimse zarar görmesin, bütçe tutsun, evdekiler çürümesin?" |
| **Hane üyesi** | Kendi kısıtı var; listeye ekler, rafta tarar | Kendi kısıtının hanede görülmesi, rafta hızlı ve açıklamalı karar |
| **Diyetisyen** (misafir, salt okunur — could) | Danışanının sepetini görmek | Süreli bağlantıyla 4 haftalık özet |
| **Moderatör / admin** (iç) | Katalog, eşleştirme, kural, KVKK talepleri | Her kararın izini sürmek, veriyi gerekçeyle düzeltmek |

**Öncelik sırası (önce güvenlik):** (1) kesin kısıtlar → (2) sağlık durumu kuralları ve hedefler → (3) hane tercihi ve kiler → (4) fiyat. Bütçe amaç değil sınırdır.

**Kitle kesişimi:** (1) indirim zinciri ve pazar hanesi, (2) evinde kesin kısıt ya da sağlık durumu (diyabet, hipertansiyon, hamilelik) olan hane, (3) birden çok marketten alan hane. Migros'tan online alan ve kesin kısıtı olmayan hane için MAYA yeterli; NutriScan ona tamamlayıcı ("sepeti hane için doğrular").

## 3. Çözdüğü işler (Jobs to be done)
1. **Planlarken:** "Bu haftanın menüsünü ve listesini evdeki herkesin kısıtına, bütçeme ve kilerime göre, alışkanlıklarımızı fazla bozmadan kur."
2. **Raftayken:** "Bu ürün evde kimin için sorun, neden, planımı nasıl etkiler, yerine ne alırım?"
3. **Mutfakta:** "Evde ne var, ne bitmek üzere, neyin son kullanma tarihi yaklaşıyor?"
4. **Hafta sonunda:** "Planladığımla aldığım ne kadar tuttu; neyi değiştirmeye devam ettik?"

## 4. Döngü ve ekranlar
**Menü → Liste → Market → Mutfak → Öğren.** Mobil sekmeler: Bu hafta · Menü · Tara · Mutfak · Asistan (hane ve gizlilik avatar üzerinden).

| Ekran (prototip v1) | Ne gösterir | Dalga |
|---|---|---|
| M01–M04 Karşılama, hane kurma, rıza, ilk liste (M02: kesin kısıt · sağlık durumu · hedef) | 4 giriş kapısı; kesin kısıt · sağlık durumu (isteğe bağlı) · hedef ayrı; aydınlatma ve açık rıza ayrı | D1 |
| M05 Bu hafta | Bütçe, uyarı kartı, proaktif plan kartı, sepet göstergesi, hane ritmi | D1 (plan kartı D2) |
| M06–M08 Takas, "Neden bu takas?", plan çıkmadı | 1·3·5 takas seçici; zorunlu değişiklik ayrı; olursuzlukta "şunu gevşet" | D1 |
| M09–M10 Rafta hane şeridi, karar "Neden?"; M22 sağlık durumu "Neden dikkat?" | 4 durumlu karar üye başına; içerik, kural, kaynak, tarih, güven, profil sürümü; M22'de besin eşiği + kaynak alıntısı | D1 |
| M11 Doğrulanamadı → etiket okuma | Tahmin yok; etiket okunur, kullanıcı onaylar, moderasyona düşer | D2 |
| M12 Market bölme | ≤2 market, tasarruf, fiyat yaşı | D2 |
| M13–M14 Alışveriş kapanışı, plan ve gerçek (v5.2: fiş yerine) | Listede "aldım" işaretleri kilere düşer; planlanan fiyat ile kaynak/tarihli fiyat özeti, yargılamayan dil | D2 |
| M15 Hane ve gizlilik | Rıza durumu, profil sürümleri, veri indir/sil | D1 |
| M16 Asistan (yazı + ses) | Adımlar görünür; hüküm rozeti karar kaydından | D1 (iş akışları) / D2 (ses: demo şeridi) |
| M17 Pazar planı | Proaktif plan + "nasıl hazırladım" + onay | D2 |
| M18 Menü | Hafta içi 5 akşam; kilerden gelenler; hane içi bölme | Ocak |
| M19 Mutfak | Yakında bitecek, SKT, "hâlâ var mı?" | Ocak |
| M20 İçerik değişikliği radarı | Önce/şimdi; eski paket uyarısı | Demo şeridi |
| M21 Tıbbi sınır | Sabit güvenlik yanıtı; acil belirtide 112 | D1 |
| W01–W05 Web | Planlama Stüdyosu, sağlığın fiyatı, hane paneli, "Nasıl karar veriyoruz", "Bu plan neden böyle?" | D2 (W04 D1) |
| A01–A04 Admin | Karar izi, katalog moderasyonu, audit log, operasyon + deneyler | D1 (A01–A03) / D2 (A04) |

Prototip: https://claude.ai/artifact/T1NAJd4949veMC6Rx5rLUK

## 5. Ürün kuralları (özet — tam liste `arastirma/06-tez-v4.md` §7)
Her karar "Neden?" taşır · dört sonuç (Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı), "güvenli" kelimesi yok · bilinmiyor ≠ yok · kesin kısıtı yalnız sahibi, yalnız profilden gevşetir · görüntüden asla "uygun" çıkmaz · araç (motor) kazanır, LLM hüküm üretemez · tıbbi sınır sabit kurallarla (doz sorusu yok, acil belirtide 112) · sağlık durumu kuralları kaynaklı ve sürümlüdür, bilgilendirme dili kullanır ("Dikkat" + besin bilgisi; "zararlı/riskli" yok), teşhis sorulmaz · karar yolunda benzerlik araması yok: RAG yalnız eşleme önerir ve kaynak alıntılar · karar sürümlere bağlı, değişince yeniden değerlendirilir ve etkilenen haneye düzeltme bildirimi gider · bildirim/ses/paylaşım üye adı + kısıtı birlikte taşımaz · herkes kendi verisini verir · asistan çökse de ürün çalışır, onaysız işlem yok · karar yalnız renkle verilmez.

## 6. Kısıtlar (ürün gözüyle)
| Alan | Durum | Ürüne etkisi / çözüm |
|---|---|---|
| Ürün içeriği | OFF'ta TR içerik kapsamı %15–25, Türkçe alerjen taksonomisi yok | Doğrulanmış katalog: toplayıcının içindekiler metni (ŞOK + Tarım Kredi) aday veri, etiket okuma + moderasyonla doğrulanır; katalog dışı ürün "Doğrulanamadı" |
| Sağlık kuralları | Kişiye özel klinik eşik yok; kılavuzlar popülasyon düzeyinde | Kaynaklı, sürümlü eşik tablosu (TGK beyan eşikleri, WHO, TÜBER 2022), diyetisyen incelemesi; besin tablosu yoksa "Doğrulanamadı"; böbrek hastalığı kapsam dışı (etikette potasyum/fosfor yok) |
| Tarif | Temiz lisanslı Türkçe set yok | Ekibin yazdığı 200 ev yemeği (60 → 120 → 200) |
| Fiyat | marketfiyati reddetti (28 Eyl); ürün düzeyinde hazır yasal kaynak yok (arastirma/12) | Ürün ve Fiyat Toplayıcı: ŞOK + Tarım Kredi web kataloğu, sözlükle sınırlı, kaynak + tarih, K21; eski fiyat "Doğrulanamadı"; kamuya açık sürüm yazılı izin/lisansla (ADR-015) |
| Barındırma | Tüm ortamlar Contabo (TR lokasyonu yok) | KVKK yolu ADR-008: minimizasyon, alan şifreleme, loglarda sağlık alanı yok, yerel-öncelikli kısıt seçeneği, standart sözleşme, uzman görüşü |
| LLM | Hane bağlamı EVREN (TR); ücretsiz dönem 1 Kasım'da biter | Kişisel olmayan işler ucuz bulut; EVREN uygun değilse asistan şablon moduna iner |
| Mağaza | Apple Developer hesabı var; Google Play şimdilik yok | Beta TestFlight üzerinden |
| Takvim | Özellik dondurma ~26 Mart | Dalga kademeleri: taahhüt / planlı / hedef |

## 7. Kapsam kademeleri (proposal'daki öncelik)
- **MUST (taahhüt):** D1 güvenilir çekirdek (alerjen + sağlık durumu kuralları dahil) + Ocak menü planlayıcı + beta.
- **SHOULD (planlı):** RAG içerik eşleme önerisi + kaynak alıntısı (Ocak); D2 döngü + wow (proaktif plan, market bölme, doğal dille kısıt, web Stüdyo, öneri v1, Gizlilik Kapısı v1, Röntgen modu).
- **COULD (hedef / demo şeridi):** ses, içerik değişikliği radarı, raf fotoğrafı, buzdolabı onayı, mutfak enflasyonu, diyetisyen bağlantısı.
- **Out of scope:** tabak fotoğrafıyla kalori, CGM/Health Connect, markete sepet aktarma, tam diyetisyen paneli, gamification, Android mağaza yayını (şimdilik), taklit/tağşiş uyarısı.

## 8. Functional requirements (proposal §5 — English)
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | The system shall let a user create a household, invite adult members who give their own consent, and add child profiles under guardian consent. | Must |
| FR-2 | The system shall store, per member, hard constraints (the 14 regulated allergens, coeliac/gluten, diet choices), optional self-declared health conditions (diabetes, hypertension, pregnancy; coeliac disease is enforced as a hard constraint) and soft goals (e.g., reduce sugar or salt) as separate profile parts; it shall never diagnose or ask for medical records. | Must |
| FR-3 | The system shall present the privacy notice and the explicit consent as separate screens, with unticked, purpose-specific consent boxes, and allow consent withdrawal, data export and account deletion in the app. | Must |
| FR-4 | The system shall decide product suitability per member with a deterministic rule engine and return one of four outcomes: Not suitable, Caution, No conflict found, Could not verify. | Must |
| FR-5 | The system shall return "Could not verify" whenever product data is missing, stale or ambiguous, and shall never label a product as "safe". | Must |
| FR-28 | The system shall map each health condition to versioned, source-cited rules (nutrient thresholds per 100 g, ingredient rules) and report them as "Caution" with the nutrient fact and the threshold's source, or "Could not verify" when the nutrition table is missing; it shall use informational wording only (no "harmful", "risky" or treatment claims). | Must |
| FR-6 | The system shall scan EAN/UPC barcodes on mobile and show a household strip with one outcome per member within 1.5 s (p95) for catalogued products. | Must |
| FR-7 | The system shall attach an explanation to every decision: matched ingredient, rule and version, data source and date, confidence and profile version ("Why?"). | Must |
| FR-8 | The system shall maintain a product catalogue for two pilot chains (ŞOK and Tarım Kredi) filled by a collector that reads only the products matching the recipe ingredient dictionary from the chains' public web catalogues, storing pack size, price, ingredient text, source URL and date; ingredient text is verified by moderation, and a public release requires the chains' written permission or a licensed source. | Must |
| FR-9 | The system shall let a user build a weekly shopping list and propose at most k swaps (k = 1, 3, 5) that keep the list within budget and never violate any member's hard constraint. | Must |
| FR-10 | The system shall plan weekday dinners, the shopping list and the chain choice in a single optimisation model that uses pantry items before their expiry, respects the budget and all hard constraints, and reports the optimality gap. | Must |
| FR-11 | The system shall explain an infeasible plan by listing which soft limits (budget, number of changes, quantities) could be relaxed; hard constraints shall never be offered for relaxation. | Must |
| FR-12 | The system shall provide an assistant (text) that answers common intents ("can X eat this", add to list, suggest swaps, explain a decision) by calling the decision engines, showing its steps, and never changing a decision. | Must |
| FR-13 | The system shall answer dose or medical questions with a fixed safety response and show an emergency (112) message for acute symptoms, without using an LLM. | Must |
| FR-14 | The system shall record every decision in an append-only decision record and show it to administrators as a human-readable trace. | Must |
| FR-15 | The system shall keep a tamper-evident audit log of all administrative changes (who, what, when, before/after, reason). | Must |
| FR-16 | The system shall let moderators review and approve catalogue corrections with a mandatory reason, and show which past decisions a correction would affect. | Must |
| FR-17 | The system shall track the pantry through barcode "added", "bought" marks on the shopping list and "finished" actions, and estimate items that are about to run out. | Must |
| FR-18 | The system shall generate a proactive weekly plan (e.g., Sunday morning) that changes nothing until the user approves it. | Should |
| FR-19 | The system shall split the list across at most two chains and show the saving and price age. | Should |
| FR-20 | The system shall turn a natural-language request ("guests on Saturday, budget 7,000") into constraint chips, read them back for confirmation and never relax hard constraints from text. | Should |
| FR-21 | The web app shall provide a Planning Studio with cost–health trade-off options, a "price of health" curve and a "why is the plan like this" view. | Should |
| FR-22 | The system shall recommend recipes and substitutes that are pre-filtered for all members' hard constraints and ranked by learned household preference. | Should |
| FR-23 | The system shall read product labels from photos, ask the user to confirm uncertain lines, and send corrections to moderation. | Should |
| FR-24 | The system shall offer an "X-ray mode" that marks every UI element as engine-decided or LLM-narrated. | Should |
| FR-29 | The system shall suggest mappings from unseen label ingredient names to the ingredient dictionary using semantic search (RAG, pgvector), apply a mapping only after moderator approval, and quote the rule's source passage in explanations; similarity search shall never decide suitability. | Should |
| FR-25 | The system shall notify households that bought or keep a product when its ingredients change and it becomes unsuitable for a member. | Could |
| FR-26 | The system shall accept voice questions in the store and answer without reading member names and constraints aloud together. | Could |
| FR-27 | The system shall mark likely unsuitable products on a shelf photo (only "Not suitable" or "scan the barcode", never "suitable"). | Could |

## 9. Non-functional requirements (proposal §5 — English)
| ID | Requirement | How it will be checked |
|---|---|---|
| NFR-1 | Allergen safety: zero false negatives on the gold set (n ≥ 300) as a release gate; health-condition rules agree 100% with the threshold table on their test set. | Automated regression test in CI on every change to rules or allergen data |
| NFR-2 | No hard-constraint violation in any suggestion, plan or swap. | Property-based tests over ≥10,000 random households × baskets |
| NFR-3 | Performance: shelf decision p95 ≤ 1.5 s; swap suggestion p95 ≤ 1 s; interactive re-plan returns within 3 s with an optimality-gap badge. | Load tests and production metrics (OpenTelemetry) |
| NFR-4 | Privacy: no health data in logs, traces or crash reports; household-context LLM calls processed in Turkey (EVREN); data minimised and health fields encrypted at rest. | Nightly canary test with a synthetic "hazelnut" profile; egress log review |
| NFR-5 | Explainability: 100% of user-visible decisions have a decision record. | Contract test between UI badges and decision records |
| NFR-6 | LLM grounding: the assistant cannot alter a decision; narration–decision contradictions are caught by a claim checker. | Eval harness in CI (tool-call accuracy, grounding, prompt-injection red-team) |
| NFR-7 | Modularity: module boundaries and architecture rules are enforced automatically. | Spring Modulith verify + ArchUnit rules in CI |
| NFR-8 | Security: OAuth2/PKCE login, household-level data isolation, role-based admin with MFA, no secrets in the repository. | Automated IDOR tests, gitleaks, dependency scanning |
| NFR-9 | Availability: core scan and planning ≥ 99.5% during the beta; the product keeps working when the LLM is unavailable. | Uptime monitoring; chaos test with the LLM disabled |
| NFR-10 | Recoverability: RPO ≤ 15 min, RTO ≤ 4 h. | Monthly restore drill from backups |
| NFR-11 | Accessibility: outcomes are never conveyed by colour alone; touch targets ≥ 44 px; WCAG 2.2 AA on web. | Automated accessibility checks + manual review |
| NFR-12 | Maintainability: every pull request touches one module, passes all CI gates, and its author can explain the agent-written code. | CODEOWNERS, PR template, weekly code walkthrough |

## 10. Başarı ölçütleri (proposal §3 "Success criteria"a)
- **E1:** Birleşik planlama modelinin kesin çözücü ve sezgisel yöntemlerle kıyası (20 senaryo × 30 tohum; hypervolume, IGD+, optimallik boşluğu); "önce menü sonra liste" tabanına göre fark gerçek veriyle raporlanır.
- **E2:** Yalnız-LLM planlayıcıya karşı kısıt ihlali, bütçe ihlali, uydurma fiyat; asistan tool-call doğruluğu ve enjeksiyon dayanıklılığı.
- **E3:** 20–40 hanelik beta (≥10 hanede kesin kısıt): takas/plan kabulü, fiyat tazeliği (medyan fiyat yaşı, "Doğrulanamadı" oranı), SKT'li kiler kullanımı, 4. hafta tutunma.
- **Sağlık durumu kuralları:** eşik tablosu test setinde %100 uyum; RAG eşleme önerisi, tam/bulanık eşlemeye karşı altın sette recall/precision ile raporlanır.
- **Güvenlik kapısı:** altın sette 0 yanlış negatif; hiçbir öneride kesin kısıt ihlali yok.
