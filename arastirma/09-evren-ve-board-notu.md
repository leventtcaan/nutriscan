---
title: EVREN LLM katmanı + proje takip aracı — doğrulanmış notlar
updated: 2026-09-28
kaynak: evren.ssyz.org.tr/llm-inference (25 Eyl 2026 Chrome oturumu; 28 Eyl 2026 yeniden okundu) · evren.ssyz.org.tr/pricing (28 Eyl 2026) · Microsoft/GitHub dokümanları
---
# EVREN (SSB) — LLM çıkarım katmanı (25 Eylül 2026 itibarıyla sayfada yazanlar)
- OpenAI uyumlu tek API; `model="auto"` yönlendirici. OpenAI SDK, Codex CLI, Vercel AI SDK uyumlu.
- **Veri egemenliği:** istem, yanıt ve kullanım kayıtları Türkiye'de bare-metal altyapıda; "yurt dışına veri aktarımı yapılmaz" (sayfa beyanı).
- **Kota:** 10M token/gün, 500K TPM (burst), 32 paralel istek. **1 Kasım 2026'ya kadar 0 kredi (ücretsiz test).** Sonrası kredi — ücret/şartlar okunmadı.
- **Modeller (13/13 çevrimiçi):** glm-5.3 (amiral, 512K bağlam, araç kullanımı), deepseek-v4.1-flash (kod/ajan, 1M, görsel), deepseek-v4-flash (1 Kas'ta kalkıyor), qwen3.8-flash-next, gemma-4-31b (görsel, bbox, belge okuma), qwen3-vl-30b (video), **qwen3-embedding-8b (TR-TEB'de 1.)**, qwen3-vl-reranker-8b, **qwen3-guard-4b (içerik güvenliği)**, **dots-ocr / deepseek-ocr-2 (OCR)**, **qwen3-asr-1.7b (Türkçe konuşma tanıma)**.
- Sayfada "tahmini bekleme: uzun" göstergesi → gecikme riski ölçülmeli.
- **NutriScan'e etkisi:** asistan orkestrasyonu, etiket/fiş OCR, Türkçe gömme (katalog/tarif arama), ses tanıma ve güvenlik sınıflandırıcısı Türkiye'de çalışabilir → 05-agent-mimarisi'ndeki "tamamen TR" (B) mimarisi artık gerçekçi; hibrit bulut yolu yedek. **Açık:** ticari/üretim kullanım şartları, 1 Kasım sonrası kredi fiyatı, Türkçe tool-calling doğruluğu (ölçülecek).

## Şartlar ve fiyat — 28 Eylül 2026 kontrolü (A0.4-a, kabul kriteri 2)
Yöntem: site JavaScript ile çizildiği için sayfalar gerçek tarayıcıda açılıp metni okundu (düz HTTP isteği yalnız
başlık döndürüyor). Aşağıdaki her satır, yanında yazan sayfada 28 Eyl 2026'da görüldü.

**Doğrulanan**
| Konu | Sayfada yazan | Kaynak |
|---|---|---|
| Ücretsiz dönem | 1 Kasım 2026'ya kadar tüm çıkarım istekleri kredi bakiyesinden bağımsız, ücretsiz | /llm-inference/ |
| Kota | 10M token/gün (hesap başına, her gece 00:00 yenilenir) · 500K TPM · 32 eşzamanlı istek; kalan kota `x-ratelimit-*` başlıklarında | /llm-inference/ |
| Önbellek indirimi | Önbellekten (prefix-cache) karşılanan istem token'ı kotaya **%3 ağırlıkla** yazılır | /llm-inference/ |
| Model değişikliği | 14/14 model (25 Eyl'de 13): `mimo-v2.6-pro` eklendi · `deepseek-v4-flash` 1 Kas'ta kalkıyor → `deepseek-v4.1-flash` | /llm-inference/ |
| Kredi ekonomisi | e-Devlet ile kayıt → **1000 CR başlangıç**; kredi katkıyla kazanılır (günlük giriş +10 CR, etiketleme, veri/model paylaşımı); kazanım tavanı günde 100 CR (giriş hariç); harcama HOLD → SETTLE → RELEASE | /pricing/ |
| Kredinin kullanıldığı yer | Model eğitimi, **çıkarım istekleri**, veri seti dışa aktarımı, ön etiketleme, veri işleme | /pricing/ |
| Hesap kuralı | **Her TCKN için tek hesap**; sosyal kazanımlar için min. 7 gün hesap yaşı | /pricing/ (Adil Kullanım) |
| Veri konumu | İstem, yanıt ve kullanım kayıtları Türkiye'de bare-metal altyapıda; "yurt dışına veri aktarımı yapılmaz" (sayfa beyanı) | /llm-inference/ |
| Kimlik | API anahtarı Keycloak tabanlı; kapsam, rol, organizasyon izolasyonu; kullanıcı/organizasyon düzeyinde kredi izolasyonu | /llm-inference/ |
| GPU eğitim fiyatı | 1× H200 = 10 CR/saat … 48× H200 = 1680 CR/saat (NutriScan'de model eğitimi yok, bilgi için) | /pricing/ |

**Oturum içinden (Levent'in hesabı, 28 Eyl 2026; Claude in Chrome ile okundu)**
| Konu | Ekranda yazan | Kaynak |
|---|---|---|
| Kayıt sözleşmeleri | İlk kayıtta **KVKK Aydınlatma Metni** ve **Üyelik Sözleşmesi** onaylanır (platform geneli) | /guide › Başlarken |
| LLM kullanım şartları | Ayrı bir belge: `LLM_TERMS_OF_SERVICE_v1` (`current_version: 1`, `is_material: true`). Metin web'de değil, API'de: `GET /v1/terms/text`; onay `POST /v1/terms/accept {"version": 1}`; hesap başına bir kez, onaysız çağrı `403 terms_not_accepted` | /llm/models |
| Şartlardan alıntı | "Kullanım Şartları Madde 3: 1 Kasım 2026 tarihine kadar tüm çıkarım modelleri test ve entegrasyon amaçlı tamamen ücretsizdir (0.00 CR)." | /llm/models |
| Fiyatın yeri | `GET /v1/models` her model için `pricing: {prompt_token_price, completion_token_price, currency: "CR", free_until: "2026-11-01"}` döndürür; bugün değerler 0.0. **1 Kasım sonrası fiyat burada ilan edilecek** | /llm/models (örnek yanıt) |
| Uç nokta | `https://evren-llmapi.ssyz.org.tr/v1` · `Authorization: Bearer` ya da `X-API-Key` · anahtar biçimi `evren_llm_...` · uçlar: chat/completions, responses, embeddings, rerank, ocr, audio/transcriptions, models | /llm/models |
| Kota birimi | "Her **API anahtarına** günlük 10.000.000 token ücretsiz" (herkese açık sayfa "hesap başına" diyor) · 429 = hesap kotası, 503 = anlık doluluk | /llm/models |
| Akıl yürüten modeller | DeepSeek/Qwen'de düşünme ve yanıt aynı `max_tokens` bütçesini paylaşır → en az 2048, önerilen 4096 | /llm/models |
| Kredi talebi | Kredi Merkezi › Talep: miktar (CR) + amaç + gerekçe (min. 20 karakter) → yönetici inceler ve onaylar | /billing?tab=request |
| Hesap durumu | Bakiye 1.020 CR (1000 başlangıç + 2 günlük giriş) · API anahtarı henüz yok | /billing, /api-keys |

**Kaynaklar arası çelişki (rakamlar oynak, tek kaynağa bağlanmaz)**
- Günlük kazanım tavanı: herkese açık /pricing/ **100 CR**, oturum içi /billing **50 CR**.
- 1× H200: /pricing/ **10 CR/saat**, /guide **15 CR/saat**.
- Kılavuz 13 model, herkese açık sayfa 14 model sayıyor.
→ Karar gerektiren rakam API'nin kendi yanıtından (`/v1/models`, `x-ratelimit-*`, `X-Evren-Credits-*`) okunur, sayfadan değil.

**LLM Kullanım Şartları v1 — özet** (`GET /v1/terms/text`, 28 Eyl 2026, Levent'in anahtarıyla; `accepted: false`)
Belge kendini "hukuk ekibince nihai gözden geçirilmemiş, ilk yayın öncesi taslak" diye niteliyor; v1 esaslı
(`is_material=true`), yani ilk çağrıdan önce açık onay şart.
| Madde | Özet | NutriScan için |
|---|---|---|
| 1 Kapsam | Gateway'in tüm uçları; anahtar oluşturan ya da Chat Portal kullanan her hesap | Backend'in her EVREN çağrısı bu şartlara tabi |
| 2 Kabul edilebilir kullanım | Yasadışı/zararlı içerik, kritik altyapı saldırısı, reşit olmayana zarar, model lisansı ihlali ve **kota/kimlik atlatma yasak: "anahtar paylaşımı" ve otomatik hesap açma dahil**. `content_guard` ve `content_policy` katmanları kısmen uygular, "nihai sorumluluk kullanıcıda" | **Levent'in anahtarı ekiple paylaşılamaz** (kişisel tercih değil, şart ihlali). Her üye kendi hesabı/anahtarı ya da organizasyon |
| 3 Faturalama | HOLD → SETTLE ile CR; "kesin tutarlar `/v1/models` ve admin fiyatlandırma panelinde" yayımlanır | Fiyat `/v1/models`'tan okunur. **Not:** /llm/models sayfası "Madde 3" diye 1 Kasım'a kadar 0.00 CR diyor, ama v1 metninin 3. maddesinde bu cümle yok → ücretsiz dönemin dayanağı sayfa beyanı ve `free_until` alanı |
| 4 Veri ve KVKK | İstem ve yanıt metni KVKK kapsamında işlenir; **organizasyon düzeyinde korpus rızası (`llm_corpus_consent`)** ve kullanıcı düzeyinde unutulma hakkı (`llm_privacy_tombstone`) var; ayrıntı ayrı KVKK belgelerinde (bize açık değil) | **Saklama süresi yazılı değil → Doğrulanamadı.** Korpus rızası, istemlerin bir derlemde kullanılabileceğini ima ediyor → yalnız maskeli/sentetik veri (K06, K18, K19) ve rızanın kapalı olduğu teyit edilmeli |
| 5 Hizmet seviyesi | "Olduğu gibi"; çıktı doğruluğu garanti değil; kesintide en iyi çaba kredi iadesi; SLA yok | Model çıktısı karar değildir (K01, K02 zaten böyle); kesintide asistan düşer, motor kararları etkilenmez |
| 6 Fesih | İhlalde hesap/anahtar askıya alınabilir; kullanıcı anahtarı panelden kapatabilir | Tek anahtara bağımlılık riski → yedek sağlayıcı yolu yapılandırmada durmalı |
| 7 Değişiklik | Fiyat modeli, veri işleme ya da sorumluluk değişirse yeni esaslı sürüm → herkes yeniden onaylayana kadar gateway kapalı | 1 Kasım fiyatı esaslı değişiklikse **yeniden onay gerekir**; backend `403 terms_not_accepted`'ı ayrı hata olarak göstermeli |

**Onay ve fiyat** (28 Eyl 2026)
- Şartlar v1 Levent'in kararıyla onaylandı: `accepted_version: 1`, `accepted_at: 2026-09-28T14:33:57Z`; `terms/status` → `accepted: true`.
- `GET /v1/models` → hesaba tanımlı **13 model**, hepsinde `prompt_token_price: 0.0`, `completion_token_price: 0.0`,
  `currency: "CR"`, `free_until: "2026-11-01"`. **1 Kasım sonrası fiyat henüz ilan edilmemiş** → Doğrulanamadı.
- Görevler: chat (glm-5.3, deepseek-v4.1-flash, deepseek-v4-flash, mimo-v2.6-pro, qwen3.8-flash-next, gemma-4-31b, auto) ·
  vision_chat (qwen3-vl-30b) · embedding (qwen3-embedding-8b) · rerank (qwen3-reranker-8b) · ocr (dots-ocr, deepseek-ocr-2) ·
  audio_transcription (qwen3-asr-1.7b).
- **`qwen3-guard-4b` hesabın kataloğunda yok** (herkese açık sayfada listeleniyor). İçerik güvenliği sınıflandırıcısına
  dayanan bir tasarım yapılmadan önce erişim teyit edilmeli.
- Model kaydında ayrıca `capabilities`, `context_length`, `default_max_output_tokens`, `precision` alanları var →
  bağlam ve çıktı sınırı da koda gömülmez, buradan okunur.

**Hâlâ açık**
- **Saklama süresi ve korpus rızasının varsayılanı:** v1'de yok; `docs/compliance/` KVKK belgeleri bize açık değil.
- **1 Kasım sonrası token fiyatı:** `/v1/models` `pricing` alanı deneme sırasında (AB#158, en geç 30 Eki) tekrar okunur.
- Haberler (ör. [GZT, 28 Eyl 2026](https://www.gzt.com/teknoloji/milli-yapay-zeka-platformu-evren-kullanima-acildi-1-kasima-kadar-sinirsiz-ve-ucretsiz-4264937))
  ücretsiz dönemi doğruluyor, sonrası için bilgi vermiyor. İkincil kaynak, fiyat için kullanılmaz.

**Sıradaki adımlar**
1. ✓ Anahtar oluşturuldu (ad "NutriScan dev (Levent)", sınıf LLM Çıkarım, son kullanma 31.12.2026) ve Anahtar
   Zinciri'nde `nutriscan-evren-api-key` kaydında; değeri hiçbir sohbete ya da dosyaya girmedi.
2. ✓ Şartlar onaylandı, `pricing` okundu (yukarıda).
3. `ssyz@ssb.gov.tr` adresine soru: (a) istem/yanıt saklama süresi, (b) `llm_corpus_consent` varsayılanı ve nasıl
   kapatılır, (c) 1 Kasım sonrası çıkarım CR oranı, (d) üç kişilik öğrenci projesi için organizasyon kurulumu.

**NutriScan'e etkisi**
- **Bütçe:** 1 Kasım sonrası maliyet hesaplanamıyor → Doğrulanamadı. Ücretsiz dönemde asistan akışlarının token
  tüketimi ölçülür (EVREN denemesi, en geç 30 Eki); fiyat `/v1/models` üzerinden ilan edilince bu ölçümle çarpılır.
  Önbellek %3 kuralı, sabit sistem istemini ve araç tanımlarını başta tutmayı ödüllendirir. Bakiye yetmezse
  Kredi Merkezi › Talep ile gerekçeli kredi istenebilir (onay yöneticide, garanti değil).
- **Fiyat ve kota koddan okunur:** sayfalardaki rakamlar birbiriyle çelişiyor. Eşik ve fiyat koda gömülmez; istemci
  `pricing` ve `x-ratelimit-*` / `X-Evren-Credits-*` başlıklarını okur (kırmızı çizgi 7).
- **Sağlayıcı bağımsızlığı:** istemci OpenAI uyumlu ve temel adresi yapılandırmadan okuyor olmalı (kırmızı çizgi 7);
  EVREN şartları uygun çıkmazsa ya da ücretli olursa hibrit bulut yolu yalnız yapılandırma değişikliğiyle açılır.
- **Sağlık verisi:** veri yurt içinde kalsa da saklama süresi ve şartlar yazılı değil. EVREN'e de Gizlilik Kapısı
  (`privacy`) üzerinden maskeli veri gider, prod verisi yok (K06, K18, K19). "Türkiye'de" beyanı bu kuralı gevşetmez.
- **Anahtar ve hesap:** her TCKN tek hesap ve anahtar kişiye bağlı; şartlar md. 2 anahtar paylaşımını açıkça yasaklıyor.
  Levent'in anahtarı ekiple hiçbir biçimde paylaşılmaz (kabul kriteri 1 + şart). Hilal ve Ozan'ın kendi hesabını mı
  açacağı, yoksa organizasyon altında mı çalışılacağı **açık soru** (e-posta sorusu (d)).

# Proje takip aracı
- **Azure DevOps (Boards):** ilk 5 kullanıcı ücretsiz (Basic: Boards, Repos, Pipelines, Artifacts). Scrum süreç şablonu: PBI, Task, Bug, Sprint, backlog, capacity, burndown. Resmi Microsoft MCP sunucusu (uzak sunucu GA, 2026) → work item okuma/yazma, WIQL. GitHub entegrasyonu: Azure Boards GitHub App; commit/PR'da `AB#<id>` ile iş öğesine bağlanır.
  Kaynaklar: https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/ · https://github.com/microsoft/azure-devops-mcp · https://learn.microsoft.com/en-us/azure/devops/release-notes/2026/sprint-278-update · https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops
- **GitHub Projects:** iteration alanı (sprint), board/table/roadmap, sub-issue; ama yerleşik backlog/PBI kavramı yok, sprint düzeni elle kurulur. https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields
- **Self-host (Contabo VPS: Plane/Taiga/OpenProject):** mümkün ama bakım, yedek, güvenlik yükü; Azure Boards ücretsiz ve yönetilen olduğu için gereksiz.
