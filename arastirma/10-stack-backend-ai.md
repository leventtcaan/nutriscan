> **Ham araştırma — ekiple netleştirilmedi, 2026-09-25**
> Dayanak: `07-tez-v5.md` (omurga, E1/E2/E3), `05-agent-mimarisi.md` (§0, §6, §7), `09-evren-ve-board-notu.md` (EVREN), `08-ekip-calisma-modeli.md` §3 (monorepo, Modulith, ArchUnit, contract-first), `plan/kararlar.md` (ADR-001…005).
> Sürüm numaraları 25 Eylül 2026'da resmi sayfa / GitHub release API'sinden okundu. Doğrulayamadığım her şey **(doğrulanmadı)** diye işaretli. Buradaki ADR'ler **öneri**; `plan/kararlar.md`'ye ancak ekip onayıyla girer.

# 10 — Backend + AI stack'i (Java/Spring, LLM, optimizasyon, kimlik, veri, test)

## 0. Kısa sonuç (öneri)

1. **Java 25 LTS + Spring Boot 4.1.x + Spring AI 2.0.x + Spring Modulith 2.1.x, Gradle 9.x (Kotlin DSL + version catalog).** Boot 3.5'in açık kaynak desteği **30 Haziran 2026'da bitti**; proje Haziran 2027'ye kadar canlı kalacağı için 3.5 + Spring AI 1.x seçeneği fiilen yok. Boot 4.1'in OSS desteği **31 Temmuz 2027**'ye kadar, yani kapanışı kapsıyor.
2. **Spring AI 2.0 başlatıcıları (starter) Boot 4.1 bağımlılıklarını çekiyor** (issue #6465). Bu yüzden 4.0 değil, **4.1** seçilmeli.
3. **LLM: Model Gateway uygulamanın içinde, ayrı bir servis değil.** Her sağlayıcı için bir Spring AI `ChatModel`. EVREN **birincil ve Türkiye'de**, bulut **yedek**: yalnız yer tutuculu metin gider ve tek bayrakla kapanır. LiteLLM gibi ayrı bir proxy eklenmez: Mart 2026'daki tedarik zinciri saldırısı bunun somut bir riskini gösterdi.
4. **"Tamamen TR" (05 §7 B) EVREN'le artık gerçekçi, ama henüz kanıtlanmadı.** Öneri: **varsayılanı TR'ye çevir (TR-öncelikli hibrit)**, bulut yalnız ölçülmüş açıklar için yedek kalsın. 15 Kasım karar kapısında üç şey ölçülecek: Türkçe tool-calling doğruluğu, p95 gecikme ve 1 Kasım sonrası kredi şartları.
5. **Optimizasyon: OR-Tools 9.15 CP-SAT, üretimde Java içinde** (`planning` modülü). Ayrı bir Python servisi kurulmaz. Python yalnız **araştırma ortamı** (E1: OR-Tools Python + pymoo NSGA-II). Formülasyon üç yolla paylaşılır: **ortak örnek (instance) JSON şeması**, Java'dan **CpModelProto/MPS export'u** ve **bağımsız Python fizibilite/amaç denetleyicisi** (parite testleri). Timefold yedek bile değil: E1'in istediği optimallik boşluğunu (gap) vermiyor.
6. **Kimlik: Keycloak 26.7, Türkiye'deki sunucuda self-host.** Mobilde Authorization Code + PKCE (S256) kullanılır. **Hane yetkisi IdP'de değil, uygulamada** (`household` modülü). Personel rolleri Keycloak'ta tutulur (admin/moderatör/auditor, MFA zorunlu). Bu taramada Türkiye'de barındırılan yönetilen bir IdP bulamadım.
7. **Veri: PostgreSQL 18.6 + pgvector 0.8.6.** qwen3-embedding-8b **4096 boyutlu**, pgvector ise HNSW'de `vector` için en fazla 2000, `halfvec` için en fazla 4000 boyut indeksliyor. Bizim katalog/tarif ölçeğimizde indekse gerek yok: `halfvec(4096)` + tam tarama yeterli. Büyürse MRL ile 2048 boyuta indirilir.
8. **Hane izolasyonu iki katmanlı:** uygulama katmanı (her sorguda `household_id`, ArchUnit + test) ve **hane bağlamı taşıyan tablolarda RLS** (derinlemesine savunma). Olaylar Spring Modulith Event Publication Registry (JDBC) üzerinden yürür; bu, bedava bir transactional outbox demek. Audit append-only ve hash zincirli.
9. **Test:** JUnit 6 (Boot 4 ile geliyor), Testcontainers 2.0, ArchUnit 1.5, Spring Modulith test, PIT 1.30, OpenAPI tabanlı sözleşme testi (openapi-generator + oasdiff + Schemathesis). Spring Cloud Contract kullanılmaz. **jqwik riskli:** bakım modunda ve hâlâ JUnit Platform 1.x üzerinde. D0'da spike yapılacak, yedek plan hazır.
10. **LLM eval: kendi JUnit harness'ımız** asıl kapı (E2 metrikleri motorla karşılaştırılarak deterministik ölçülür). promptfoo (Mart 2026'dan beri OpenAI'ın) yalnız prompt matrisi ve red-team için, isteğe bağlı.

---

## 1. Stack tablosu (proposal §6 için)

"Doğrulandı" = 2026-09-25'te resmi release sayfası / GitHub release API'sinden okundu. Proposal'a **ana sürüm hattı** yazılmalı (ör. "Spring Boot 4.1.x"). Yama numarası CI'daki version catalog'da tutulur.

| Katman | Seçim | Sürüm (hat · en son yama) | Tarih / destek | Durum |
|---|---|---|---|---|
| Dil / runtime | Java (Eclipse Temurin JRE) | **25 LTS** · 25.0.x | GA 16 Eyl 2025; Oracle Premier 2030-09 | Doğrulandı ([endoflife](https://endoflife.date/oracle-jdk)) |
| Framework | Spring Boot | **4.1.x** · 4.1.1 | GA 10 Haz 2026; OSS 31 Tem 2027 | Doğrulandı ([blog](https://spring.io/blog/2026/06/10/spring-boot-4/), [endoflife](https://endoflife.date/spring-boot)) |
| | Spring Framework | 7.0.x · 7.0.9 (Boot 4.1.1 ≥7.0.9 istiyor) | OSS 31 Tem 2027 | Doğrulandı ([sys-req](https://docs.spring.io/spring-boot/system-requirements.html)) |
| | Jakarta EE | 11 (Servlet 6.1; Tomcat 11.0.x) | — | Doğrulandı (sys-req) |
| | Spring Security | 7.1.x · 7.1.1 | — | Doğrulandı (GitHub release) |
| Modülerlik | Spring Modulith | **2.1.x** · 2.1.1 | 2.1 GA 11 Haz 2026 | Doğrulandı ([blog](https://spring.io/blog/2026/06/11/spring-modulith-2-1-ga-2-0-7-and-1-4-12-released/)) |
| AI | Spring AI | **2.0.x** · 2.0.1 | GA 12 Haz 2026; 2.0.1 21 Ağu 2026 | Doğrulandı ([blog](https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now/)) |
| | MCP Java SDK | 2.0.0 (spec 2025-11-25) | Spring AI 2.0 ile | Doğrulandı (aynı blog) |
| | LangChain4j (yedek) | 1.20.x | 1.20.0: 4 Eyl 2026 | Doğrulandı (GitHub) |
| LLM (TR) | EVREN | `glm-5.3`, `qwen3-embedding-8b` (4096-d), `qwen3-asr-1.7b`, `dots-ocr`… | 1 Kas 2026'ya kadar ücretsiz | Kısmen (bkz. §3) |
| Optimizasyon | Google OR-Tools (Java + Python) | **9.15** (CP-SAT; SCIP 10.0, HiGHS 1.12 gömülü) | 12 Oca 2026 | Doğrulandı ([release](https://github.com/google/or-tools/releases/tag/v9.15)); v10 RC haberi var **(doğrulanmadı)** |
| Araştırma | pymoo (NSGA-II) | 0.6.2 | 28 Haz 2026 | Doğrulandı (GitHub) |
| | jMetal (Java, isteğe bağlı) | 7.5 (Java 21) | aktif (Eyl 2026 commit) | Doğrulandı (tag) |
| Kimlik | Keycloak | **26.7.x** · 26.7.4 | 16 Eyl 2026 | Doğrulandı ([26.7](https://www.keycloak.org/2026/07/keycloak-2670-released)) |
| Veritabanı | PostgreSQL | **18.x** · 18.6 | 13 Ağu 2026; PG19 hâlâ beta 4 | Doğrulandı ([duyuru](https://www.postgresql.org/about/news/postgresql-186-1711-1615-1519-1424-and-19-beta-3-released-3365/)) |
| | pgvector | 0.8.x · 0.8.6 | — | Doğrulandı (tag) |
| | Flyway | Boot 4.1'in yönettiği 12.4.x (en son 13.8.0) | — | Doğrulandı ([4.1 notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.1-Release-Notes)) |
| | Hibernate ORM | 7.4 (Boot 4.1) | — | Doğrulandı (4.1 notes) |
| Build | Gradle (Kotlin DSL) | **9.x** · 9.8.0 | Java 25 için ≥9.1 | Doğrulandı ([uyumluluk](https://docs.gradle.org/current/userguide/compatibility.html)) |
| Test | JUnit | 6.x (Boot 4 yönetir; en son 6.1.3) | — | Doğrulandı (GitHub) |
| | Testcontainers | 2.0.x · 2.0.5 | — | Doğrulandı |
| | ArchUnit | 1.5.0 (Java 27'ye kadar) | 4 Ağu 2026 | Doğrulandı |
| | PIT | 1.30.0 | 27 Ağu 2026 | Doğrulandı; JUnit 6 ile çalıştığı **doğrulanmadı** |
| | jqwik | 1.10.1 (JUnit Platform 1.14) | bakım modu | Doğrulandı; Boot 4 ile uyumu **risk** |
| | JaCoCo | 0.8.15 (Java 26 resmi) | 5 Haz 2026 | Doğrulandı |
| Sözleşme | openapi-generator · oasdiff · Schemathesis | 7.25.0 · 1.32.1 · 4.28.0 | Eyl 2026 | Doğrulandı |
| | springdoc-openapi | 3.1.x (Boot 4 hattı olduğu **çıkarım**) | 6 Eyl 2026 | Kısmen |
| LLM eval | kendi JUnit harness + promptfoo (isteğe bağlı) | promptfoo 0.123.1 | 18 Eyl 2026 | Doğrulandı |
| Gözlem | Micrometer + OpenTelemetry (Boot 4.1 OTel 1.62) | — | — | Doğrulandı (4.1 notes) |

---

## 2. ADR önerileri

Format: **Ne · Neden · Alternatif · Neden o değil**. Numaralar geçici (`S-xx`). Onaylanınca `plan/kararlar.md`'de ADR-006'dan itibaren sıralanır.

### S-01 — Java 25 LTS
- **Ne:** Derleme ve çalışma Java 25 (Temurin, glibc tabanlı imaj: `eclipse-temurin:25-jre`). Gradle toolchain ile sabitlenir.
- **Neden:** LTS; Oracle Premier desteği 2030'a kadar. Boot 4.1 Java 17–26 arasında resmi destekli. Timefold 2 ve jMetal 7 zaten ≥21 istiyor. Boot 4.1 notlarına göre jOOQ 3.20 de ≥21 istiyor. Java 21'e göre kazanç: sanal thread'lerde `synchronized` pinning'in kalkması (JDK 24), compact object headers ve AOT cache. 3 GB'lık bir VPS'te bellek ve açılış süresi için anlamlı **(kazanç ölçülmedi)**.
- **Alternatif:** Java 21 LTS.
- **Neden o değil:** 21 de çalışır ve Premier desteği 2028'e kadar sürüyor, ama yeni başlayan bir projede bir LTS geriden başlamanın getirisi yok. Kütüphane uyumu kontrol edildi: ArchUnit 1.4.2+ ve JaCoCo 0.8.14+ Java 25'i destekliyor. **Tek risk JNI:** JDK 24'ten beri native kütüphane yüklemek uyarı üretiyor ([JEP 472](https://openjdk.org/jeps/472)). OR-Tools için JVM'e `--enable-native-access=ALL-UNNAMED` bayrağı verilmeli.

### S-02 — Spring Boot 4.1.x (Framework 7, Jakarta EE 11)
- **Ne:** Boot 4.1.x'e pinlenir, aylık yama PR'ı açılır. Boot 4.2'ye geçiş Ocak kış kampında **yalnız gerekirse** yapılır (4.2 şu an M2; GA tarihi **doğrulanmadı**, takvime göre Kasım 2026 beklenir).
- **Neden:** Boot 3.5'in OSS desteği 30 Haz 2026'da bitti; son OSS yaması 3.5.16 ([Dan Vega](https://www.danvega.dev/blog/spring-boot-end-of-life)). 4.0'ın OSS desteği 31 Ara 2026'da bitiyor, yani beta'dan önce. 4.1'inki 31 Tem 2027'de bitiyor, kapanışı (Haz 2027) kapsıyor. Spring AI 2.0 ve Timefold 2 Boot 4 şartı koyuyor. 4.1 ayrıca yerleşik resilience (Framework 7'de `@Retryable`, `@ConcurrencyLimit`), OTel iyileştirmeleri ve HTTP client SSRF koruması (`InetAddressFilter`) getiriyor ([InfoQ](https://www.infoq.com/news/2026/06/spring-boot-4-1/)).
- **Alternatif:** Boot 3.5 + Spring AI 1.1.x.
- **Neden o değil:** 3.5 için OSS güvenlik yaması yok. Ticari destek (Tanzu, HeroDevs) öğrenci bütçesine uymaz. Spring AI 2.0'ın advisor tabanlı tool loop'u (05 §1.2) 1.x'te yok. Canlı ürünü bir yıl boyunca yamasız bir hatta tutmak jüride "güvenlik zemini" iddiasını çürütür.
- **Risk:** Jackson 3'e geçiş ve bazı kütüphanelerin Boot 4 desteğinin gecikmesi. **Azaltma:** D0'da iskelet + tüm bağımlılıklarla "boş ama derlenen" bir uygulama; OpenRewrite `rewrite-spring` tarifleri (6.40.0) mevcut.

### S-03 — Build: Gradle 9 (Kotlin DSL, version catalog)
- **Ne:** `backend/` Gradle çok-projeli yapı (ya da tek proje + Modulith paketleri), `gradle/libs.versions.toml`, wrapper pinli, build cache ve configuration cache açık. Ayrı test source set'leri: `test` (unit), `integrationTest` (Testcontainers), `propertyTest` (jqwik — bkz. S-11), `archTest`.
- **Neden:** 08 §3'teki monorepo bunu varsayıyor. Kök build dosyası bir "hotspot" ve version catalog tüm sürümleri **tek dosyada** topluyor (agent'ların sürüm kaymasını önler). Görev bazlı yapı, CI dakikası sınırlıyken (GitHub Pro, private repo) işe yarıyor: değişen modül testi, test türüne göre ayrı task ve build cache. PIT, jqwik ve Testcontainers'ı ayrı task'larda koşturmak Gradle'da doğal.
- **Alternatif:** Maven 3.9.16 (Maven 4 hâlâ RC).
- **Neden o değil:** Maven agent'lar için daha öngörülebilir, çünkü eğitim verisinde baskın; bir kaynak agent'ların Gradle projesinde bile `pom.xml` üretmeye meyilli olduğunu yazıyor ([codenote](https://codenote.net/en/posts/java-spring-boot-ai-coding-agents-acceleration/)). **Azaltma:** kök `AGENTS.md`'ye "Gradle Kotlin DSL; `pom.xml` yasak" kuralı, `ci-guard`'da `pom.xml` bulunursa kırmızı. Ekip Gradle'dan rahatsız olursa Maven de kabul edilebilir; kritik bir karar değil.

### S-04 — Spring Modulith 2.1 (modüller, olaylar, modül bazlı Flyway)
- **Ne:** `@ApplicationModule` paketleri (08 §3.a haritası), `ApplicationModules.verify()` CI'da, olay tabanlı modüller arası iletişim (`@ApplicationModuleListener`), **JDBC Event Publication Registry**, `spring.modulith.runtime.flyway-enabled=true` ile modül bazlı migration (`db/migration/<modül>`, her modüle ayrı `flyway_schema_history_<modül>`).
- **Neden:** 2.0 ile gelen olay yayın kaydı, olayı iş transaction'ıyla aynı anda yazıyor, çökmede yeniden gönderiyor (`republish-outstanding-events-on-restart`) ve `staleness` izleyicisi takılan olayı `FAILED` yapıyor. Yani broker kurmadan transactional outbox elde ediliyor ([docs](https://docs.spring.io/spring-modulith/reference/events.html)). Modül bazlı Flyway, 08'deki "hotspot: Flyway sürüm numaraları" sorununu çözüyor ([runtime docs](https://docs.spring.io/spring-modulith/reference/runtime.html)). 2.1 ayrıca Boot slice testleriyle modül testi getiriyor.
- **Alternatif:** Tek Flyway klasörü + zaman damgalı sürüm; Kafka/RabbitMQ ile outbox; mikroservisler.
- **Neden o değil:** Tek klasör işe yarar ama modül sahipliğini dosya sisteminde göstermez. 3 kişi ve tek düğüm için broker gereksiz ops yükü; dış tüketici çıkarsa Modulith 2.1'in outbox externalization'ı (Namastack / JobRunr) sonradan eklenir. Mikroservis 3 kişiye ağır.
- **Dikkat:** Modül bazlı Flyway'de `FlywayValidateException` bildirimi var ([issue #1440](https://github.com/spring-projects/spring-modulith/issues/1440)). Durumu **doğrulanmadı**, D0 spike'ında denenmeli. Sorun çıkarsa yedek: tek klasör + modül önekli dosya adı + CODEOWNERS.

### S-05 — LLM çerçevesi: Spring AI 2.0.x
- **Ne:** `ChatClient` + advisor zinciri (`PrivacyAdvisor`, `ToolPolicyAdvisor`, `DecisionTraceAdvisor`, `OutputGuardAdvisor` — 05 §1.2). Tool loop'u biz sürüyoruz (`ToolCallingAdvisor` auto-register kapalı → onay kapısı + SSE "adımlar"). `StructuredOutputValidationAdvisor` kullanılıyor. MCP v1'de yok (iç araçlar `@Tool` bean).
- **Neden:** Boot yerliliği (auto-config, Actuator, Micrometer gözlem adları `gen_ai.client.*`). 2.0'da tool loop advisor zincirine taşındı, bu da "LLM orkestra eder, motor karar verir" ilkesini kod düzeyinde uygulamayı kolaylaştırıyor. OpenAI modülü 2.0.0-M5'ten beri **resmi `openai-java` SDK** üzerinde. OpenAI uyumlu uçlar `spring.ai.openai.base-url` ile bağlanıyor, sunucuya özel alanlar `extraBody` ile geçiliyor ([OpenAI chat docs](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html)).
- **Alternatif:** LangChain4j 1.20 (`langchain4j-open-ai-spring-boot4-starter`, guardrail API'si) · Embabel.
- **Neden o değil:** LangChain4j güçlü ve Boot 4 starter'ı var ([docs](https://docs.langchain4j.dev/tutorials/spring-boot-integration/)), ama iki çerçeveyi birden taşımak agent'lar için bağlam kirliliği yaratır. Spring AI'da bir engel çıkarsa (ör. EVREN tool-calling ayrıştırma hatası) **yalnız `privacy.gateway` arkasındaki model adaptörü** LangChain4j'ye geçirilebilir. ArchUnit kuralı (dış LLM SDK'sını yalnız `privacy.gateway` import eder) bu değişimi tek pakete hapsediyor. Embabel v1 için ek risk (05).
- **Risk:** Spring AI minor sürümlerinde kırıcı değişiklik (05 §8 R7). **Azaltma:** pin + yükseltme ayrı PR + eval kapısı.

### S-06 — Model Gateway: uygulama içi yönlendirme, EVREN birincil, bulut yedek
- **Ne:** `privacy.gateway` içinde bir `ModelRouter`. Her sağlayıcı için ayrı ve elle kurulan `OpenAiChatModel` / `AnthropicChatModel` bean'i; auto-config'e güvenilmez, her birine ayrı bir `base-url` ve anahtar verilir. Yönlendirme kuralları:
  - Tur **hassas** ise (Gizlilik Kapısı kararı) → **yalnız TR** (EVREN). Hata olursa bulut'a **düşmez**, "şu an yanıt veremiyorum" + LLM'siz akış (butonlar) devreye girer.
  - Tur **temiz/yer tutuculu** ise → varsayılan TR. Zaman aşımı, 5xx ya da circuit açıksa bulut (bayrak açıksa).
  - Bayraklar: `llm.cloud.enabled` (global), `llm.enabled` (tam kapatma — demo §9 adım 7), hane başına bütçe.
  - Resilience: Framework 7 `@ConcurrencyLimit` (EVREN'in 32 paralel isteğine karşı ≤ ~16 eşzamanlı çağrı), `@Retryable` (yalnız idempotent tek çağrı, tool loop'un tamamı değil), circuit breaker için Resilience4j 2.4.0. Circuit breaker Framework 7'de yok ([Spring resilience](https://docs.spring.io/spring-framework/reference/core/resilience.html)).
  - Her çağrı `gen_ai.*` span'i + `egress_log` (yer tutuculu gövde, sağlayıcı, model, token, gecikme).
- **Neden:** Tek çıkış kapısı KVKK anlatısının mühendislik karşılığı (K kuralı + ArchUnit). Fallback politikası "hassas tur asla buluta düşmez" kuralını kodda zorluyor. Uygulama içi olduğu için ek servis, ek kimlik bilgisi ya da ek tedarik zinciri yok.
- **Alternatif:** LiteLLM proxy (Python) · Spring Cloud Gateway · ticari AI gateway.
- **Neden o değil:** LiteLLM'in PyPI paketi 24 Mart 2026'da ~40 dakika boyunca kimlik bilgisi çalan zararlı sürümlerle (1.82.7/1.82.8) yayında kaldı ([LiteLLM](https://docs.litellm.ai/blog/security-update-march-2026), [NHS](https://digital.nhs.uk/cyber-alerts/2026/cc-4761)). Bütün API anahtarlarını tutan ayrı bir proxy tam da bu saldırının hedefi. Spring Cloud Gateway HTTP düzeyinde çalışıyor ve "hassas tur" bilgisini görmüyor. Ticari gateway'ler yurt dışında.

### S-07 — "Tamamen TR" mimarisinin (05 §7 B) EVREN ile yeniden değerlendirmesi
**Değişen:** 05'te B'nin zayıf yanları üçtü: ops yükü, maliyet ve tool-calling belirsizliği. EVREN ilk ikisini büyük ölçüde kaldırıyor: yönetilen bir OpenAI uyumlu uç, 1 Kasım'a kadar ücretsiz, 10M token/gün, 32 paralel istek. Aynı API'de gömme, rerank, ASR ve OCR da var. Tek bir TR sağlayıcıyla asistan, etiket/fiş OCR, Türkçe gömme ve ses tanıma işlenebilir (09).

**Hâlâ bilinmeyen / risk:**
| Risk | Kanıt | Azaltma |
|---|---|---|
| Tool-calling desteği / kalitesi | 09: `glm-5.3` "araç kullanımı" diyor. Üçüncü taraf LLMTR geçidi EVREN satırlarında **tool calling, JSON mode ve gerçek streaming'in kapalı** olduğunu yazıyor ([LLMTR](https://llmtr.com/docs/en/gateway/evren/)); bu onların proxy'sine ait olabilir. Doğrudan EVREN uç noktasıyla **doğrulanmadı**. | D0 spike: Spring AI + `glm-5.3` / `qwen3.8-flash-next` ile 20 Türkçe araç senaryosu (AST eşleşme, pass^k). Tool-calling yoksa: **Action-Selector** (05 §1.1). LLM yalnız `intent + slot` JSON'u üretir, akışı kod sürer. Bu zaten sık akışların %80'i için önerilen desen. |
| SLA yok, kapanabilir, kota değişebilir | Sayfada SLA yok; "tahmini bekleme: uzun" göstergesi (09) | Bulut yedek (yalnız yer tutuculu) + LLM'siz çalışma modu (demo §9/7) + ikinci TR sağlayıcı araştırması (Huawei MaaS TR, Bulutistan — 05 §2.5). |
| 1 Kasım sonrası kredi fiyatı | Kayıtta 1.000 CR veriliyor, ücret tablosu okunmadı ([yapayzekaokulum](https://www.yapayzekaokulum.com/blog/evren-yapay-zeka-platformu-nedir)) | Ekim sonuna kadar token ölçümü → aylık tahmin. Kredi yetmezse bulut payı artar (maliyet 05 §4.3: ~$40–90/ay). |
| Kullanım şartları (ticari/üretim, üçüncü kişi verisi) | Anahtar üretmeden önce şartlar onaylanıyor, API `/terms/status` ile denetliyor ([EvrenLLM-Kullanim](https://github.com/drdoof2019/EvrenLLM-Kullanim)); içerik okunmadı | **Şart metni okunup `kaynak/`'a arşivlenmeli.** Beta'da gerçek hane verisi göndermeden önce SSB/SAYZEK'e yazılı soru: "öğrenci bitirme projesi, gerçek kullanıcı, sağlık verisi". |
| Hesap e-Devlet'le kişiye bağlı | Giriş e-Devlet ile | Anahtar tek kişide (bus factor). Ekip hesabı mümkün mü sorulmalı; anahtar sır yöneticisinde tutulmalı, döndürme prosedürü yazılmalı. |
| Gecikme | Ölçülmedi | D0'dan itibaren sentetik prob: her 15 dk'da 1 kısa istek, p50/p95 panoda. Etkileşimli p95 bütçesi (05 §4.4) tutmazsa ilgili akış bulut yoluna ya da LLM'siz şablona. |
| Guard modeli | Üçüncü taraf rehber `qwen3-guard-4b`'nin 404 döndüğünü yazıyor | Guard'a güvenme: kapalı sözlük + kural tabanlı Output Guard birincil. |
| Streaming uç durumu | Son SSE paketinde `choices` boş gelebiliyor (aynı rehber) | Spring AI streaming testi D0 spike'ında. |

**Öneri:** 05'teki C (hibrit) korunuyor ama **varsayılan yön tersine dönüyor**: TR birincil, bulut yedek ("TR-öncelikli hibrit"). Bu, tez §3 "Güvence 2"yi güçlendiriyor ("hane bağlamı taşıyan her tur Türkiye'de" iddiası, bulut kapalıyken de ayakta kalıyor). E2 de iki modu ölçmeye devam ediyor (bulut vs TR). **15 Kasım karar kapısı ölçütleri (öneri):** Türkçe tool-call doğruluğu ≥ bulut modelinin %90'ı, etkileşimli p95 ≤ 05 §4.4 bütçesi, kredi fiyatı ≤ bulut maliyeti. Üçü de tutarsa bulut yolu varsayılan olarak **kapalı** başlar.

### S-08 — Optimizasyon çalışma zamanı: OR-Tools CP-SAT, Java içinde
- **Ne:** `planning` modülü OR-Tools 9.15 Java (`ortools-java` + platform jar'ı) ile MSM modelini kurar ve CP-SAT ile çözer. Tek sepet / Akıllı Takas için MPSolver (SCIP ya da CP-SAT) kullanılır. Çalışma kuralları:
  - **Zaman sınırı:** `getParameters().setMaxTimeInSeconds(3.0)` etkileşimli, proaktif Pazar planında 30–60 sn. Rozet için `objectiveValue()` ve `bestObjectiveBound()`'dan boşluk hesaplanır (tez §5 "en iyiye en fazla %X uzak"). `relative_gap_limit` ile erken durulur.
  - **İptal:** `CpSolver.stopSearch()` thread-safe (`synchronized`). İstek iptal edilince ya da yeni plan eskisini geçersiz kılınca başka bir thread'den çağrılır. MPSolver'da `setTimeLimit` var.
  - **Eşzamanlılık:** `num_workers` **açıkça** ayarlanır; varsayılan 0 = tüm çekirdekler ([sat_parameters.proto](https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto)). Öneri: 4 vCPU'lu sunucuda çözüm başına 4 worker + `@ConcurrencyLimit(2)` + kuyruk. Pazar 09:00 tepesi (D3 yük testi) için proaktif planlar önceden (gece) bir iş kuyruğunda çözülür.
  - **Bellek:** CP-SAT native bellek kullanıyor, JVM heap'ine sayılmıyor. Konteyner limiti = heap + native payı (ör. `-XX:MaxRAMPercentage=50`). **Değer ölçülmedi**, E1 v0 ile ölçülecek.
  - **İmaj:** glibc tabanlı (`eclipse-temurin:25-jre`, Ubuntu). **Alpine (musl) kullanılmaz**, native kütüphane yüklenmez. Platform jar'ları Maven Central'da linux-x86-64, linux-aarch64, darwin-aarch64 vb. olarak var (ekipte Apple Silicon Mac'ler için önemli).
  - **Tekrarlanabilirlik (E1):** `random_seed` sabit. Çok thread'li CP-SAT duvar saatinde deterministik değil. E1 raporunda worker sayısı ve deterministik zaman (`max_deterministic_time`) ayrıca yazılır.
- **Neden:** Tez §5 "zaman sınırlı exact + boşluk rozeti" istiyor ve bunu CP-SAT doğrudan veriyor. Aynı kütüphane Python'da da var, yani araştırma ve üretim **aynı çözücüyü, aynı sürümü** kullanıyor. Süreç içi çalıştığı için ağ sıçraması, ikinci runtime ve ikinci deploy yok. 05-ek-menu_bench ölçümleri de zaten CP-SAT/SCIP ile.
- **Alternatif 1 — Ayrı Python servisi (FastAPI + OR-Tools):** tek formülasyon, araştırmacı dostu. **Neden değil:** ikinci runtime, ikinci CI hattı, ikinci güvenlik yüzeyi, servisler arası sözleşme ve gecikme. 3 kişilik ekipte ops yükü. Güvenlik filtresinin (alerjenli aday çözücüye hiç gitmez — 08 §3.a sözleşmesi) süreç sınırını aşması ArchUnit'le denetlenemez.
- **Alternatif 2 — Timefold Solver 2.7 (Spring Boot 4 starter, `SolverManager`, `termination.spent-limit`):** Spring entegrasyonu çok iyi ([docs](https://docs.timefold.ai/timefold-solver/latest/quickstart/spring-boot/spring-boot-quickstart)). **Neden değil:** yerel arama/metasezgisel. **Alt sınır (bound) ve optimallik kanıtı vermiyor**, E1'in ana sorusu (exact nerede kopar, boşluk ne) cevapsız kalır. Timefold 2 Java 21 + Boot 4 + Jackson 3 istiyor, yani uyumlu. E1'de "endüstriyel metasezgisel tabanı" olarak eklenebilir, bu isteğe bağlı.
- **Alternatif 3 — jMetal 7.5 (Java NSGA-II):** matsezgisel (GA menüyü seçer, CP-SAT sepeti çözer) ürüne girerse. **Şimdilik değil:** tez üründe yalnız zaman sınırlı exact istiyor. NSGA-II E1'de Python'da (pymoo) koşar.

**Formülasyon paylaşımı ve parite (öneri):**
1. **Tek doğruluk kaynağı = örnek şeması:** `contracts/engine/plan-instance.schema.json` (tarifler, SKU'lar, fiyatlar, kiler, kısıtlar, ağırlıklar) + `contracts/engine/fixtures/` (altın örnekler). Java ve Python aynı örnek dosyasını okur.
2. **Model üreticisi Java'da (kanonik).** `CpModel.exportToFile("x.pb.txt")` → Python `CpModel` proto'yu yükleyip **aynı modeli** çözer (E1'in exact kolu). MPSolver tarafında `exportModelAsMpsFormat` / `exportModelToProto` Java API'sinde mevcut (SWIG kaynağında doğrulandı), bu da SCIP/HiGHS kıyası için MPS dosyası demek.
3. **Bağımsız denetleyici Python'da:** `research/e1/checker.py` bir çözümün fizibilitesini (her kesin kısıt, paket tamsayılığı, ≤2 market) ve amaç değerini modelden **bağımsız** hesaplar. pymoo NSGA-II'nin amaç fonksiyonu da bu denetleyicidir. N-sürüm doğrulama: çözücü hata yapsa bile denetleyici yakalar.
4. **Parite testleri (CI, `planning` değişince):** her altın örnek için (a) Java CP-SAT çözümü → Python denetleyici "fizibil" demeli ve amaç farkı ≤ 1e-6 olmalı; (b) proto export → Python CP-SAT aynı optimal amaç değerini bulmalı (küçük örneklerde kanıtlı optimum); (c) OR-Tools sürümü Java `libs.versions.toml` ve Python `uv.lock`'ta **aynı** olmalı (ci-guard kuralı).

### S-09 — Kimlik ve yetki: Keycloak 26.7 (self-host, TR)
- **Ne:**
  - **Keycloak 26.7.x**, Türkiye'deki sunucuda, aynı PostgreSQL üzerinde ayrı bir veritabanında. Tek realm `nutriscan`.
  - İstemciler: `mobile` (public, Authorization Code + **PKCE S256**, sistem tarayıcısı, RFC 8252), `web` (public + PKCE ya da BFF — Faz 3 web ADR'si), `admin` (public + PKCE, **MFA zorunlu**).
  - Backend: Spring Security 7 **resource server** (JWT).
  - Refresh token rotation açık. RFC 9700 implicit ve password grant'ı kaldırıyor, PKCE'yi zorunlu kılıyor ([RFC 9700](https://datatracker.ietf.org/doc/rfc9700/)).
  - **Hane yetkisi uygulamada:** token yalnız `sub` + personel rolleri taşır. `household` modülü `membership(user, household, role: OWNER|ADULT|VIEWER)` tutar. Her istekte aktif hane `X-Household-Id` başlığıyla gelir, sunucu üyeliği doğrular ve hane bağlamını transaction'a koyar (S-10 RLS). Asistan araçlarında `householdId` asla argüman değildir (05 §6.3).
  - **Personel RBAC (Keycloak realm rolleri):** `admin` (katalog, kullanıcı yönetimi), `moderator` (topluluk/katalog düzeltme kuyruğu), `auditor` (salt okuma: karar kaydı, audit, eval panosu; hane içeriğini görmez, yalnız yer tutuculu/aggregate veri görür).
  - **Break-glass:** ayrı bir `breakglass` hesabı (donanım anahtarı/TOTP; kimlik bilgisi iki kişinin bildiği bir yerde mühürlü). Kullanımı zaman sınırlı bir rol verir, **gerekçe alanı zorunlu**, her erişim audit'e (S-10 hash zinciri) yazılır ve üç kişiye bildirim gider. DB düzeyinde `BYPASSRLS` yetkili rol yalnız bu yolda ve yalnız betikle kullanılır. Her kullanım sonrası sprint notuna düşülür.
- **Neden:** Hazır gelen login/kayıt/şifre sıfırlama, e-posta doğrulama, MFA, brute-force koruması, sosyal giriş, oturum yönetimi ve admin konsolu 3 kişilik ekibin sıfırdan yazmayacağı şeyler. Veri Türkiye'deki sunucuda kalıyor (KVKK). Keycloak Organizations özelliği 26'da tam destekli ([duyuru](https://www.keycloak.org/2024/06/announcement-keycloak-organizations)), ama hane için **kullanılmıyor** (aşağıya bakın).
- **Alternatif 1 — Spring Authorization Server** (artık Spring Security 7'nin parçası, [duyuru](https://spring.io/blog/2025/09/11/spring-authorization-server-moving-to-spring-security-7-0/)): daha az RAM, tek deploy. **Neden değil:** yalnız OAuth2/OIDC protokolünü veriyor. Login UI, kayıt, e-posta doğrulama, şifre sıfırlama, MFA ve hesap kurtarma bizim kodumuz olur. Güvenlik açısından en riskli kodu en az zamanı olan ekip yazmış olur.
- **Alternatif 2 — Yönetilen IdP** (Auth0, Clerk, Cognito, Firebase Auth, Zitadel Cloud): **Neden değil:** bu taramada **Türkiye bölgeli** bir yönetilen IdP bulamadım. Kimlik verisi (e-posta, ad) yurt dışına aktarılır, bu da 05'teki KVKK m.9 sorusunu yeniden açar.
- **Alternatif 3 — Haneleri Keycloak Organizations ile modellemek:** **Neden değil:** hane üyeliği, rıza ve kesin kısıtlar domain verisi. Değişince S16 yeniden değerlendirme olayları tetiklenmeli (08 §3.a). IdP'ye taşınırsa olay akışı ve audit bölünür.
- **Maliyet:** Keycloak'ın taban belleği 10.000 önbellekli oturumla ~1.250 MB; konteyner belleğinin %70'i heap'e gidiyor ([sizing](https://www.keycloak.org/high-availability/single-cluster/concepts-memory-and-cpu-sizing)). Tek VPS'te bütçelenmeli (§4).

### S-10 — Veri katmanı: PostgreSQL 18 + pgvector + modül bazlı Flyway + JSONB karar kaydı + hash zincirli audit + RLS
- **PostgreSQL 18.6.** PG19 hâlâ beta 4 (GA Ekim 2026 bekleniyor, [beta 4](https://www.postgresql.org/about/news/postgresql-19-beta-4-released-3386/)). Yeni ana sürümde eklenti (pgvector) ve barındırma desteği gecikir; 18 yeterli. Yükseltme kapanıştan sonra.
- **pgvector 0.8.6 + qwen3-embedding-8b:** Model en fazla **4096** boyut veriyor, **MRL ile 32–4096** arası kullanıcı tanımlı boyut destekliyor, Türkçe dahil 100+ dil, Apache 2.0 ([model kartı](https://huggingface.co/Qwen/Qwen3-Embedding-8B)). EVREN'in 4096 boyut döndürdüğü üçüncü taraf rehberde yazıyor. pgvector'da HNSW/IVFFlat sınırları: `vector` 2.000, `halfvec` 4.000, `bit` 64.000 ([README](https://github.com/pgvector/pgvector)). **4096 doğrudan indekslenemiyor.**
  - **Öneri:** `embedding halfvec(4096)` sakla, **indeks koyma, tam tarama** kullan. Katalog + tarif ölçeğinde (onbinler) tam tarama milisaniyeler mertebesinde **(tahmin, ölçülmedi)** ve recall %100. Satır sayısı ~100k'yı aşarsa: MRL ile ilk 2048 boyutu al, L2-normalize et, `halfvec(2048)` üzerine ifade indeksi (HNSW) kur, `qwen3-reranker-8b` ile yeniden sırala. EVREN `dimensions` parametresini destekliyor mu, **doğrulanmadı**; desteklemiyorsa kesme istemci tarafında yapılır.
  - Gömme sürümü kolonda tutulur (`embedding_model`, `embedding_dim`). Model değişirse yeniden gömme bir batch iş olur.
  - Spring AI `PgVectorStore` yerine **kendi tablo + native sorgu** öneriyorum. Aramada hane filtresi ve güvenlik filtresi (alerjenli tarif hiç dönmez) SQL'de, `safety.api` üzerinden birleşiyor. Genel amaçlı VectorStore soyutlaması bu kuralı gizler.
- **Flyway:** Boot 4.1'in yönettiği sürüm (12.4.x) + Modulith modül klasörleri (S-04).
- **JSONB karar kaydı (Decision Record):** `decision_record(id, household_ref, kind, engine, engine_version, rule_version, input_hash, payload jsonb, schema_version, created_at, trace_id)`. `payload` şeması `contracts/decision-record.schema.json`'da; uygulama yazmadan önce doğrular. Sık sorgulanan alanlar (hüküm, ürün, kural) ayrı kolon + indeks; geri kalanı JSONB (GIN yalnız ihtiyaç olursa). Röntgen modu ve "Neden?" yalnız buradan okur.
- **Append-only audit + hash zinciri:** `audit_event(seq bigserial, at, actor, action, target, payload jsonb, prev_hash bytea, row_hash bytea)`.
  - `row_hash = SHA-256(kanonik_serileştirme(satır) || prev_hash)`.
  - Uygulama rolüne yalnız `INSERT` + `SELECT`; `UPDATE/DELETE/TRUNCATE` REVOKE + trigger ile reddedilir.
  - **Sınır:** tablo sahibi trigger'ı kapatabilir; append-only tek başına kurcalamayı kanıtlamaz ([analiz](https://appmaster.io/blog/tamper-evident-audit-trails-postgresql)). Azaltma: uygulama rolü tablo sahibi değil. Zincir başı (son `row_hash`) günde bir kez DB dışına yazılır (Git'e imzalı commit ya da ayrı depolama). Gece job'ı zinciri doğrular, kırılmayı alarm olarak bildirir.
  - **KVKK silme ile çelişki:** audit'te hane içeriği değil, **referans** tutulur. Kişisel içerik hane başına anahtarla şifrelenir ("anahtar imhası" — 08 §3.a), silmede anahtar yok edilir ve zincir bozulmaz.
- **Hane izolasyonu — RLS mi, uygulama katmanı mı? İkisi birden, kademeli:**
  - **Uygulama katmanı (birincil):** her hane tablosunda `household_id NOT NULL` + indeks. Repository'ler hane bağlamını `HouseholdContext`'ten alır. ArchUnit kuralı: `household_id` taşıyan tabloya dokunan native SQL yalnız işaretli sınıflarda olabilir. Hibernate `@TenantId` bir seçenek, ama native SQL'i yeniden yazmıyor ([kaynak](https://dev.to/software_mvp-factory/row-level-security-in-postgresql-multi-tenant-data-isolation-for-your-saas-without-a-query-change-57bb)).
  - **RLS (derinlemesine savunma):** yalnız hane bağlamı taşıyan tablolarda (üyeler, kısıtlar, rıza, kiler, liste, plan, sohbet olayları, karar kaydı). Politika `household_id = current_setting('app.household_id')::uuid`. Her transaction başında `set_config('app.household_id', ?, true)` çağrılır. Üçüncü parametre `true` = transaction-local, HikariCP havuzunda sızıntıyı önlüyor. Uygulama rolü tablo sahibi olmaz ve `FORCE ROW LEVEL SECURITY` açılır.
  - **Dikkat:** `@ApplicationModuleListener` yeni bir transaction'da (`REQUIRES_NEW`) ve async çalışıyor. Hane bağlamı olayın içinde taşınıp listener'da yeniden kurulmalı. Proaktif Pazar işi haneler arasında döner; her hane ayrı bir transaction'da işlenir.
  - **Test:** Testcontainers'ta iki haneli fikstür. Her repository metodu B hanesi bağlamında çağrılır ve A'nın verisi dönerse test kırmızı olur ("çapraz hane sızıntısı = 0" kapısı; 08 §3.c'deki CI kontrollerine eklenir).
  - **Neden ikisi:** agent'ların yazdığı bir native sorguda filtrenin unutulması en olası hata ve RLS bunu DB'de yakalıyor. Sadece RLS olsaydı hata "boş sonuç" olarak sessiz kalırdı; uygulama katmanı ve test bunu görünür yapıyor. **Bedel:** bağlam kurulumu ve async listener'larda ek kod. D0'da tek tabloyla spike yapılır; zorlaşırsa RLS yalnız `household`/`consent`/`safety` tablolarında kalır.
- **Olay yayını:** Spring Modulith JDBC Event Publication Registry (S-04), `completion-mode=ARCHIVE` (tamamlanan olaylar denetim için kalır), `staleness.processing` ayarlı. Dış broker yok.

### S-11 — Test stack'i
| Katman | Araç | Not |
|---|---|---|
| Unit | JUnit 6 (Boot 4 yönetiyor), AssertJ, Mockito | JUnit 6 Jupiter ile Platform'un sürüm hattını birleştirdi ([rieckpil](https://rieckpil.de/whats-new-for-testing-in-spring-boot-4-0-and-spring-framework-7/)) |
| Entegrasyon | **Testcontainers 2.0** + `@ServiceConnection` (PostgreSQL + pgvector imajı, Keycloak) | 2.0'da artefakt adları `testcontainers-` önekiyle değişti, JUnit 4 desteği kalktı |
| Mimari | Spring Modulith `verify()` + **ArchUnit 1.5** (K-kuralları: tek LLM çıkışı, `safety.api` üzerinden aday, native SQL sınırı) | 08 §3.c |
| Modül | Modulith `@ApplicationModuleTest` + 2.1'in slice test desteği | Modül tek başına boot edilir |
| Property | **jqwik 1.10.1 — RİSK** | jqwik "saf bakım modunda"; 1.10.1 JUnit Platform 1.14 kullanıyor ve JUnit Platform 6 sürümü "belki hiç" ([jqwik](https://github.com/jqwik-team/jqwik)). Boot 4 Platform 6 getiriyor. **D0 spike:** ayrı `propertyTest` source set'i + Platform 1.14'e pinli ayrı Gradle konfigürasyonu. Çalışmazsa **yedek:** JUnit 6 `@ParameterizedTest` + tohumlu rastgele üreteç (sentetik hane üreteci zaten var — tez §8 D0) ve MSM/kural motoru özellikleri için Python tarafında Hypothesis (denetleyici üzerinden). |
| Mutation | **PIT 1.30** + pitest-junit5-plugin | Yalnız `safety` ve `planning` için, gece çalışır (CI dakikası). JUnit 6 uyumu **doğrulanmadı** → D0 spike. |
| Kapsam | JaCoCo 0.8.15 | 08 §3.c eşikleri |
| Sözleşme | OpenAPI-first: `contracts/openapi/*.yaml` → openapi-generator 7.25 (TS istemci + Java arayüzleri) · **oasdiff** kırıcı değişiklik · springdoc 3.x ile çalışan uygulamanın ürettiği spec ↔ repo'daki spec farkı · **Schemathesis 4.28** ile çalışan backend'e karşı şema tabanlı fuzz (Testcontainers ortamında) | Aşağıda neden |
| Motor | Altın örnek + parite testleri (S-08), alerjen altın set FN=0 kapısı (tez §5) | |
| LLM | S-12 | |

**Neden Spring Cloud Contract değil:** SCC (5.0.3, Boot 4 hattı) sağlayıcı güdümlü, Groovy/YAML DSL'le JVM tüketicilere WireMock stub'ı üretiyor. Bizim tüketicilerimiz TS (mobil/web/admin) ve istemci OpenAPI'den **üretiliyor** (08 §3.a). OpenAPI'nin kendisini sözleşme yapmak tek kaynak ilkesine uyuyor. SCC ikinci bir sözleşme dili ekler.

### S-12 — LLM eval: kendi JUnit harness'ımız (asıl), promptfoo (isteğe bağlı)
- **Ne:** `backend/src/evalTest` (ayrı Gradle task, gece + asistan/privacy değişince). Senaryolar `data/eval/assistant/*.yaml` (girdi, beklenen araç çağrısı AST'si, beklenen hüküm/sayı kaynağı). Metrikler:
  - tool-call doğruluğu (AST eşleşme, pass^k)
  - grounding (her sayı bir araç çıktısına bağlı mı; claim checker)
  - **karar değişmezliği %100**
  - kanarya sızıntısı (egress log taraması)
  - enjeksiyon ASR'si
  - E2 metrikleri: yalnız-LLM planlayıcının kısıt/bütçe ihlali — **motor/denetleyiciyle** ölçülür, LLM-hakem değil.

  Sonuçlar JSON olarak `research/e2/`'ye yazılır; aynı dosya jüri grafiğini besler. Spring AI'ın `Evaluator` arayüzü (relevancy/fact-checking) yalnız anlatım kalitesi için, yardımcı.
- **Neden:** Asıl metrikler **deterministik ve domain'e özel**: hüküm motordan gelir, sayı karar kaydından. Bunlar gerçek Spring bean'leriyle (Privacy Gateway, Output Guard, motorlar) koşmalı, yani eval de JVM içinde. Model Gateway'in iki modunu (TR / bulut) aynı harness ölçüyor; E2'nin "bulut + TR modeli" kolu da bu.
- **Alternatif:** promptfoo 0.123 (YAML test matrisi, red-team eklentileri, OpenAI uyumlu sağlayıcıyı `apiBaseUrl` ile destekliyor).
- **Neden asıl o değil:** uygulamayı dışarıdan HTTP ile ya da prompt düzeyinde test ediyor. Advisor zincirini ve motor doğrulamasını içeriden görmüyor. Node bağımlılığı ekliyor. OpenAI tarafından satın alındı (9 Mar 2026). Açık kaynak lisansın süreceği söyleniyor ([promptfoo](https://www.promptfoo.dev/blog/promptfoo-joining-openai/)), ama yön belirsiz. **Kullanım alanı:** prompt varyant kıyası ve hazır red-team saldırı üreticisi (D3 red-team haftası). Kişisel veri içermeyen sentetik hanelerle, yerel olarak.

---

## 3. EVREN ↔ Spring AI entegrasyonu (teknik not)

- **Taban URL:** `https://evren-llmapi.ssyz.org.tr/v1`; `Authorization: Bearer evren_llm_…` ya da `X-API-Key` ([EvrenLLM-Kullanim](https://github.com/drdoof2019/EvrenLLM-Kullanim) — üçüncü taraf, resmi dokümana göre **doğrulanmadı**; resmi sayfa WebFetch'te içerik döndürmedi, 09 Levent'in oturumundan okundu).
- **Spring AI:** `spring.ai.openai.chat.base-url=https://evren-llmapi.ssyz.org.tr` (sonuna `/v1` gerekip gerekmediği spike'ta görülecek; Spring AI dokümanı bazı sunucular için `/v1` eklemeyi öneriyor), `model=glm-5.3`. Sunucuya özel parametreler için `extraBody`. Gömme ve ses için Spring AI'ın OpenAI embedding / transcription modelleri aynı base-url ile. **Rerank ve OCR uç noktaları OpenAI şemasında yok** → `RestClient` ile ince adaptör (`/rerank`, OCR).
- **İki sağlayıcı aynı anda:** auto-config tek `OpenAiChatModel` kurar. EVREN + bulut için **elle bean** (builder) tanımlanır, `spring.ai.model.chat=none` ile auto-config kapatılır ([docs](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html)).
- **D0 spike listesi (EVREN, ~1 gün):** (1) basit sohbet + streaming (son boş `choices` paketi), (2) tool calling: tek araç, paralel araç, Türkçe argüman, (3) `response_format: json_schema` / strict, (4) gömme 4096-d + `dimensions` parametresi, (5) ASR Türkçe, (6) p50/p95 gecikme, 32 paralel istek davranışı, (7) şart metni ve kota uç noktası (`/quota`).

---

## 4. Barındırma bütçesi (kaba, ölçülmedi)

Tek TR VPS (D1–beta):

| Bileşen | Bellek |
|---|---|
| Backend JVM | 1–1,5 GB heap + CP-SAT native payı |
| Keycloak | ~1,25 GB |
| PostgreSQL | 1–2 GB |
| Gözlem | Tempo/Prometheus ~1 GB (Langfuse self-host ClickHouse ister, ağır — 05 §4.2) |

→ **8 GB RAM / 4 vCPU asgari tahmin.** LLM TR'de EVREN'de koşuyor, GPU yok. VPS seçimi Faz 3 infra ADR'sine bırakıldı; bu tahmin oraya girdi.

---

## 5. Riskler ve yedek planlar

| # | Risk | Olasılık / etki | Önlem | Yedek plan |
|---|---|---|---|---|
| 1 | EVREN'de tool-calling yok ya da Türkçe kalitesi düşük | Orta / Yüksek | D0 spike, 20 senaryo | Action-Selector (LLM yalnız intent/slot) · bulut yolu yer tutuculu |
| 2 | EVREN 1 Kasım sonrası pahalı, kapanıyor ya da şartlar üretimi yasaklıyor | Orta / Yüksek | Şart metnini oku, SAYZEK'e yaz, token ölç | Bulut (yer tutuculu) + TR MaaS (Huawei/Bulutistan) + LLM'siz mod |
| 3 | Spring AI 2.0.x kırıcı değişiklik / hata | Orta / Orta | Pin, yükseltme PR'ı + eval kapısı | Adaptör LangChain4j'ye (tek paket, ArchUnit ile sınırlı) |
| 4 | Boot 4 ekosistem gecikmesi (bir kütüphane Boot 4 desteklemiyor) | Düşük–orta / Orta | D0 "tüm bağımlılıklar" iskeleti | Kütüphaneyi çıkar / alternatif |
| 5 | jqwik / PIT JUnit 6 ile çalışmaz | Orta / Düşük | D0 spike | Parameterized + tohumlu üreteç · Hypothesis · PIT'i ertele |
| 6 | Modulith modül bazlı Flyway hatası | Düşük / Orta | D0 spike | Tek klasör + modül önekli dosya adı |
| 7 | CP-SAT native bellek / thread taşması üretimde | Orta / Orta | `num_workers` açık, `@ConcurrencyLimit`, konteyner limiti | Proaktif planı gece kuyruğunda çöz · zaman sınırını düşür · boşluk rozeti |
| 8 | Java ↔ Python formülasyon ayrışması (E1 sonuçları üretimi temsil etmez) | Orta / Yüksek (akademik) | Proto export + bağımsız denetleyici + parite CI + aynı OR-Tools sürümü | E1 exact kolu yalnız Java export'u çözer |
| 9 | RLS bağlamı async listener'da kaybolur → boş sonuç / hata | Orta / Orta | Olayda hane bağlamı taşı, iki haneli sızıntı testi | RLS'yi çekirdek tablolara daralt |
| 10 | Keycloak bellek/ops yükü, yanlış yapılandırma | Orta / Orta | Realm'i kod olarak (export JSON, repo'da), Testcontainers Keycloak | Spring Security 7 Authorization Server (login UI'ı biz yazarız) |
| 11 | Audit zinciri DBA/owner tarafından kurcalanır | Düşük / Orta | Rol ayrımı, günlük zincir başı DB dışına | — (kabul edilen kalan risk, raporda dürüstçe) |
| 12 | 4096-d gömme depolama/performans | Düşük / Düşük | Tam tarama, ölçüm | MRL 2048 + HNSW + rerank |
| 13 | Agent'lar yanlış build aracı/sürüm üretir | Orta / Düşük | AGENTS.md + version catalog + ci-guard | — |
| 14 | EVREN hesabı tek kişiye bağlı (e-Devlet) | Yüksek / Orta | Sır yöneticisi, döndürme prosedürü | İkinci üye hesabı (şartlar izin verirse) |

---

## 6. D0'a düşen spike'lar (19 Eki – 1 Kas, öneri)

1. Boot 4.1.1 + Java 25 + Spring AI 2.0.1 + Modulith 2.1.1 + OR-Tools 9.15 + Testcontainers 2.0 + Keycloak — "boş ama derlenen" iskelet, Docker imajı (x86-64 + Apple Silicon'da yerel).
2. EVREN spike (§3 listesi) → sonuçlar `arastirma/`'ya.
3. jqwik + PIT + JUnit 6 uyumu (yarım gün).
4. RLS + `set_config` + async listener (tek tablo).
5. CP-SAT: MSM v0 modeli, proto export → Python yükleme, parite testi iskeleti.
6. Keycloak realm export + mobil PKCE akışı (mobil stack ADR'sine bağlı).

---

## 7. Doğrulanamayanlar / açık

- **EVREN:** resmi sayfa WebFetch'te içerik vermedi. Tool calling, `dimensions` parametresi, SLA, 1 Kasım sonrası fiyat, ticari/üretim kullanım şartları, ekip hesabı → **doğrulanmadı**. Üçüncü taraf kaynaklar birbiriyle çelişiyor (LLMTR "tool calling yok", 09 notu "araç kullanımı var").
- Spring AI 2.0 GA tarihi: resmi blog **12 Haziran 2026**. Bazı ikincil kaynaklar 28 Mayıs diyor, resmi olan esas alındı.
- Spring Boot 4.2 GA tarihi (şu an 4.2.0-M2) **doğrulanmadı**.
- OR-Tools v10 RC1 (23 Eyl 2026) yalnız arama özetinde geçti, release sayfasında görmedim.
- springdoc 3.x'in Boot 4 hattı olduğu, 2.9/3.1 çift yayın desenine dayanan **çıkarım**.
- jqwik 1.10.1 ve pitest-junit5-plugin'in JUnit Platform 6 ile çalışması **denenmedi**.
- Modulith modül bazlı Flyway'deki `FlywayValidateException` issue'sunun durumu okunmadı.
- Türkiye bölgeli yönetilen IdP: bulamadım (yokluğun kanıtı değil).
- Bellek ve gecikme sayıları (§4, pgvector tam tarama) **tahmin**.

---

## Kaynaklar

**Java / Spring**
- Java sürümleri: https://endoflife.date/oracle-jdk · JEP 472: https://openjdk.org/jeps/472
- Spring Boot 4.1: https://spring.io/blog/2026/06/10/spring-boot-4/ · https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.1-Release-Notes · https://docs.spring.io/spring-boot/system-requirements.html · https://www.infoq.com/news/2026/06/spring-boot-4-1/
- EOL: https://endoflife.date/spring-boot · https://endoflife.date/spring-framework · https://www.danvega.dev/blog/spring-boot-end-of-life · https://spring.io/support-policy/
- Spring AI 2.0: https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now/ · https://github.com/spring-projects/spring-ai/issues/6465 · https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html
- Spring Modulith: https://spring.io/blog/2025/11/21/spring-modulith-2-0-ga-1-4-5-and-1-3-11-released/ · https://spring.io/blog/2026/06/11/spring-modulith-2-1-ga-2-0-7-and-1-4-12-released/ · https://docs.spring.io/spring-modulith/reference/events.html · https://docs.spring.io/spring-modulith/reference/runtime.html · https://github.com/spring-projects/spring-modulith/issues/1440
- Framework 7 resilience: https://docs.spring.io/spring-framework/reference/core/resilience.html · https://spring.io/blog/2025/09/09/core-spring-resilience-features/
- Gradle: https://docs.gradle.org/current/userguide/compatibility.html · agent/build notu: https://codenote.net/en/posts/java-spring-boot-ai-coding-agents-acceleration/
- LangChain4j: https://docs.langchain4j.dev/tutorials/spring-boot-integration/ · https://docs.langchain4j.dev/integrations/language-models/openai-compatible/

**LLM / EVREN**
- EVREN: https://evren.ssyz.org.tr/llm-inference/ · https://github.com/drdoof2019/EvrenLLM-Kullanim · https://llmtr.com/docs/en/gateway/evren/ · https://www.yapayzekaokulum.com/blog/evren-yapay-zeka-platformu-nedir · https://github.com/bykemalh/evren-llm-opencode
- LiteLLM olayı: https://docs.litellm.ai/blog/security-update-march-2026 · https://digital.nhs.uk/cyber-alerts/2026/cc-4761
- promptfoo: https://www.promptfoo.dev/blog/promptfoo-joining-openai/ · https://openai.com/index/openai-to-acquire-promptfoo/
- Qwen3-Embedding-8B: https://huggingface.co/Qwen/Qwen3-Embedding-8B

**Optimizasyon**
- OR-Tools: https://github.com/google/or-tools/releases/tag/v9.15 · https://developers.google.com/optimization/cp/cp_tasks · https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto · https://github.com/google/or-tools/blob/stable/ortools/java/com/google/ortools/sat/CpSolver.java · https://github.com/google/or-tools/blob/stable/ortools/linear_solver/java/linear_solver.swig · https://github.com/google/or-tools/blob/stable/ortools/sat/docs/model.md
- Timefold: https://docs.timefold.ai/timefold-solver/latest/quickstart/spring-boot/spring-boot-quickstart · https://docs.timefold.ai/timefold-solver/latest/upgrading-timefold-solver/upgrade-from-v1
- pymoo: https://github.com/anyoptimization/pymoo · jMetal: https://github.com/jMetal/jMetal

**Kimlik**
- Keycloak: https://www.keycloak.org/2026/07/keycloak-2670-released · https://www.keycloak.org/high-availability/single-cluster/concepts-memory-and-cpu-sizing · https://www.keycloak.org/2024/06/announcement-keycloak-organizations
- Spring Authorization Server → Spring Security 7: https://spring.io/blog/2025/09/11/spring-authorization-server-moving-to-spring-security-7-0/
- RFC 9700: https://datatracker.ietf.org/doc/rfc9700/ · RFC 8252: https://datatracker.ietf.org/doc/html/rfc8252

**Veri**
- PostgreSQL: https://www.postgresql.org/about/news/postgresql-186-1711-1615-1519-1424-and-19-beta-3-released-3365/ · https://www.postgresql.org/about/news/postgresql-19-beta-4-released-3386/ · RLS: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- pgvector: https://github.com/pgvector/pgvector
- RLS + Spring: https://dev.to/software_mvp-factory/row-level-security-in-postgresql-multi-tenant-data-isolation-for-your-saas-without-a-query-change-57bb · https://www.bytefish.de/blog/spring_boot_multitenancy_using_rls.html
- Hash zinciri: https://appmaster.io/blog/tamper-evident-audit-trails-postgresql

**Test**
- Boot 4 test: https://rieckpil.de/whats-new-for-testing-in-spring-boot-4-0-and-spring-framework-7/ · Testcontainers: https://java.testcontainers.org/
- jqwik: https://github.com/jqwik-team/jqwik · https://jqwik.net/release-notes.html
- ArchUnit / PIT / JaCoCo / Schemathesis / oasdiff / openapi-generator: GitHub release sayfaları (2026-09-25 okundu)
- Spring Cloud Contract: https://docs.spring.io/spring-cloud-contract/docs/current/reference/htmlsingle/
