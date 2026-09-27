---
title: 08 — Ekip çalışma modeli (AI agent'lı 3 kişilik ekip, bileşen sahipliği)
updated: 2026-09-24
durum: HAM ARAŞTIRMA — Levent'le netleştirilmedi, 2026-09-24
dayanak: 07-tez-v5.md (§3 omurga, §7 veri fabrikası, §8 takvim, §12 açık kararlar) · 05-agent-mimarisi.md · toplanti/2026-09-24-ekip-mesaji.md
---
> **Not (27 Eyl 2026):** Bu rapor araştırmadır; uygulanan standart `plan/calisma-akisi.md` (ADR-004/005/012). A/B/C hatları, GitHub Projects ve "Closes #N" orada isimler, Azure Boards ve AB# ile değiştirildi.

# 08 — Ekip çalışma modeli

> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24.** Stack kararları (web framework, mobil, DB, hosting) Faz 3 ADR'lerinde; burada stack'ten bağımsız yazıldı. "(doğrulanmadı)" ve "(ikincil kaynak)" etiketlerine dikkat.

## 0. Kısa sonuç
1. **Model:** bileşen/modül sahipliği + contract-first + mekanik kapılar. Sahiplik bir kişiye "kod yazma tekeli" değil, **son söz ve review yükümlülüğü** verir; sınırları insanlar değil **CI** korur (Spring Modulith `verify()`, ArchUnit, CODEOWNERS, `oasdiff`, şema doğrulayıcıları).
2. **Neden şart:** farklı agent'ların aynı repoda eşzamanlı PR'larında textual conflict oranı **%41,7**, aynı agent'ın kendi PR çiftlerinde **%19,8** (arXiv 2607.04697, Temmuz 2026). Ekipte üç farklı agent olacak → çakışma "kişi" değil **bölümleme (partition)** problemi. Ajan PR'larının genelinde %27,67 conflict (AgenticFlict, 142k PR).
3. **Repo:** tek monorepo; backend **modüler monolit** (Spring Modulith), frontend'ler ayrı app klasörleri, **veri de bir modül** (`data/`), sözleşmeler ayrı klasörde (`contracts/`).
4. **Agent talimatları:** tek kaynak **kök `AGENTS.md`** (~100–150 satır, "içindekiler") + modül başına kısa `AGENTS.md` + araç-özel **ince** dosyalar. Önemli ayrıntı: Claude Code artık `AGENTS.md`'yi doğrudan okuyor (v2.1.277+), ama **kökte `CLAUDE.md` varsa `AGENTS.md`'leri okumuyor** → kökte `CLAUDE.md` koymuyoruz; Claude'a özel kurallar `.claude/rules/`'ta.
5. **Araç:** **GitHub Projects** (ücretsiz, PR/issue ile yerli bağ, `gh` CLI + GitHub MCP "projects" araçları her agent'tan erişilebilir). Linear'ın ücretsiz planında 250 aktif issue sınırı var; Jira Free'de AI yok ve GitHub'la bağ zayıf; Plane iyi ama ikinci sistem.
6. **Kritik altyapı notu:** private repoda **CODEOWNERS, protected branch ve rulesets GitHub Free'de yok**. Çözüm: repoyu GitHub Pro'lu (Student Developer Pack) kişisel hesapta aç **ya da** public repo; sır taraması için private'ta `gitleaks` (GitHub push protection private'ta ücretli).

---

## 1. Güncel çalışma modelleri (2025–2026) — ne buldum

### 1.1 Sorun: agent'lar kod üretimini ucuzlattı, review ve tutarlılık darboğaz oldu
- **Çakışma verisi (birincil):**
  - *AgenticFlict* (Ogenrwot & Businge, Nisan 2026): 142k+ agent PR'ı, 59k+ repo; merge simülasyonunda **%27,67 conflict**, 336k+ conflict bölgesi; agent'lar arasında belirgin fark ([arXiv 2604.03551](https://arxiv.org/abs/2604.03551)).
  - *AI Agent Pull Requests on GitHub* (Temmuz 2026): **farklı agent çiftleri %41,7, aynı agent çiftleri %19,8 textual conflict**; conflict'li dosyaların %84,4'ü kaynak kod; ~%42'si yapısal (modify/delete, add/add); öneri: paylaşılan repoda **koordinasyon mekanizması** ([arXiv 2607.04697](https://arxiv.org/abs/2607.04697)).
  - Bizim için anlamı: üç üye farklı agent kullanacağı için en kötü senaryodayız (cross-agent). Aynı dosyayı iki agent'ın açmaması gerekir → dosya/klasör sahipliği.
- **Review darboğazı (ikincil kaynaklar, rakamları doğrulamadım):** LinearB 2026 raporu agent PR'larının "pickup time"ını 5,3× uzun, Faros AI medyan review süresini +%441 veriyor ([FlowVerify](https://www.flowverify.co/blog/ai-code-review-bottleneck-2026-data), [Codacy](https://blog.codacy.com/ai-breaking-code-review-how-engineering-teams-survive-pr-bottleneck)). Yön tutarlı: **küçük PR + otomatik kapı + odaklı insan review'u**.
- **Thoughtworks Radar Vol. 34 (15 Nisan 2026):** "cognitive debt" uyarısı — AI çok kod üretince geliştirici sistemden uzaklaşıyor; **feedforward** (Agent Skills, spec-driven) + **feedback** (mutation testing vb.) kontrolleriyle "harness"; temel mühendislik disiplinleri geçerliliğini koruyor ([Thoughtworks](https://www.thoughtworks.com/about-us/news/2026/combat-ai-cognitive-debt-radar-v34)).

### 1.2 Modül / bounded-context sahipliği
- **CODEOWNERS:** yol desenine göre sahip; branch protection'da "Require review from Code Owners" ile zorunlu onay. Private repoda **Pro/Team** gerekir; Free'de yalnız public repoda ([GitHub Docs — code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).
- **Required reviewer rule (rulesets, GA 17 Şubat 2026):** dosya desenine göre "şu klasöre dokunan PR şu kişiden N onay almalı"; CODEOWNERS'ı **tamamlar, yerini almaz** ([Changelog](https://github.blog/changelog/2026-02-17-required-reviewer-rule-is-now-generally-available/)). Hangi planda olduğu sayfada yazmıyor (doğrulanmadı).
- **Modüler monolit — Spring Modulith:** kök paketin her doğrudan alt paketi bir modül; alt paketleri otomatik "internal"; `ApplicationModules.of(App.class).verify()` üç şey denetler: **döngü yok**, **yalnız API paketine erişim**, `allowedDependencies` ile **izinli bağımlılıklar**; altında ArchUnit ([Spring Modulith 2.1 docs](https://docs.spring.io/spring-modulith/reference/verification.html)). 2026 rehberleri bunu "AI agent'ın sınır ihlalini mekanik olarak yakalayan emniyet kemeri" olarak konumluyor ([DEV 2026 rehberi](https://dev.to/x4nent/the-modular-monolith-2026-complete-guide-spring-modulith-archunit-fitness-functions-and-lessons-878), [Java Code Geeks, Tem 2026](https://www.javacodegeeks.com/2026/07/spring-modulith-2-0-enforcing-module-boundaries-before-microservices.html)).
- **Thoughtworks "architecture drift reduction with LLMs":** deterministik araçlar (ArchUnit, Spring Modulith, Spectral) + LLM değerlendirmesi birlikte; kuralı deterministik araç koyar, LLM düzeltir ([Radar](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms)).
- **Gerçek örnek — OpenAI "Harness engineering" (2026 başı):** küçük ekip, agent-first repo; `AGENTS.md` ~100 satırlık **içindekiler** (tasarım dokümanları, mimari harita, yürütme planlarına işaretçi); **mimari lint ve yapısal testlerle mekanik olarak** zorlanıyor, dokümana güvenilmiyor ([OpenAI](https://openai.com/index/harness-engineering/)). *Not:* orijinal sayfa 403 verdi; içerik özetleri ikincil kaynaklardan ([özet 1](https://alexlavaee.me/blog/openai-agent-first-codebase-learnings/), [özet 2](https://madplay.github.io/en/post/harness-engineering)).
- **Gerçek örnek — Shopify:** Rails monolitini "componentization" + Packwerk ile sınırlı bileşenlere böldü (2019–2020, AI öncesi ama modüler monolit örneğinin klasiği) ([Shopify Engineering](https://shopify.engineering/shopify-monolith)).

### 1.3 Contract-first
- **OpenAPI** tek doğruluk kaynağı; backend interface'leri (`openapi-generator` spring `interfaceOnly`) ve TS istemcisi (`openapi-typescript` / Orval) **üretilir**; CI'da `oasdiff` ile main'e göre breaking change varsa PR kırmızı ([Orval](https://orval.dev/docs/), [karşılaştırma 2026](https://www.pkgpulse.com/guides/orval-vs-openapi-typescript-vs-kubb-openapi-client-2026), [contract-first rehberi](https://dev.to/wallaceespindola/contract-first-integration-a-practical-guide-for-developers-49nf)).
- **Consumer-driven (Pact):** mikroservislerde değerli; monolit + tek backend'de **OpenAPI şeması + şema-tabanlı test yeterli**, Pact sonraya ([Speakeasy](https://www.speakeasy.com/blog/pact-vs-openapi/), [Pact FAQ](https://docs.pact.io/faq/convinceme)). NutriScan için karar: Pact yok; bunun yerine **tüketici fixture'ları** (golden JSON) + Schemathesis tarzı şema testi (opsiyonel).
- **Modül içi sözleşme:** Spring Modulith'te modüller arası çağrı API paketi ya da **domain event** üzerinden; event sınıfı da sözleşmedir.

### 1.4 Spec-driven development (SDD)
- **GitHub Spec Kit:** `constitution.md` (değişmez ilkeler) → spec → plan → tasks → implement; 30+ agent entegrasyonu, MIT ([repo](https://github.com/github/spec-kit), [MS Dev Blog](https://developer.microsoft.com/blog/spec-driven-development-spec-kit/)).
- **AWS Kiro:** `requirements.md` (EARS) · `design.md` · `tasks.md` + "steering" (`product.md`, `tech.md`, `structure.md`); Temmuz 2025 preview, 2026'da GA (ikincil) ([Kiro docs](https://kiro.dev/docs/specs/)).
- **Eleştiri (önemli):** Thoughtworks SDD'yi **Assess** halkasında tutuyor: uzun, review'u zor spec dosyaları; "AI için elle ayrıntılı kural yazmak ölçeklenmiyor" ([Radar](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development)). Böckeler (martinfowler.com, Eki 2025): Kiro küçük bug'ı dört user story'ye çeviriyor ("balyozla ceviz kırmak"), Spec Kit markdown'ları "review'u sıkıcı", agent'lar talimatı yine atlıyor; üç seviye: spec-first / spec-anchored / spec-as-source ([Fowler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)).
- **NutriScan için çıkarım:** tam Spec Kit değil, **hafif spec-anchored**: `constitution` = bizim **K01–K20 + S1–S22** (zaten var); her özellik için 1 sayfalık `spec.md` (kabul kriteri + hangi sözleşme + hangi omurga/deney) — issue'nun gövdesi olabilir.

### 1.5 AGENTS.md ve çok-agent talimat dosyaları
| Araç | Okuduğu | Nested | Not / kaynak |
|---|---|---|---|
| **Codex (CLI/IDE/cloud)** | `AGENTS.override.md` > `AGENTS.md` (+ fallback adları) | Evet; git kökünden cwd'ye iner | Birleşik boyut sınırı `project_doc_max_bytes` (32 KiB varsayılan; yeni sürümde 64 KiB diyen ikincil kaynak var) ([OpenAI docs](https://developers.openai.com/codex/guides/agents-md)) |
| **Claude Code** | `CLAUDE.md`; **v2.1.277+ `AGENTS.md`'yi doğrudan okur — ama yalnız cwd ve üstünde `CLAUDE.md`/`CLAUDE.local.md` yoksa** | Alt klasör `AGENTS.md`'si o klasörde dosya okununca yüklenir | `.claude/rules/*.md` sayılmaz, `AGENTS.md` ile birlikte yüklenir; `paths:` frontmatter ile yola özel kural; `@path` import (4 hop); `.agents/` altını okumaz; CLAUDE.md hedefi <200 satır ([resmi docs](https://code.claude.com/docs/en/memory)) |
| **Gemini CLI** | `GEMINI.md`; `settings.json` → `context.fileName: ["AGENTS.md","GEMINI.md"]` | Evet, genelden özele birleştirir | ([gemini-cli docs](https://geminicli.com/docs/cli/gemini-md/)) |
| **Antigravity** | Proje kökünde `GEMINI.md` veya `AGENTS.md`; workspace kuralları `.agents/rules/`; skills + workflows | ? | Kural dosyası ≤12.000 karakter; `~/.gemini/AGENTS.md` global desteği v1.20.3 (ikincil, doğrulanmadı) ([Antigravity docs](https://antigravity.google/docs/rules-workflows/), [Codelab](https://codelabs.developers.google.com/autonomous-ai-developer-pipelines-antigravity)) |
| **Cursor** | `.cursor/rules/*.mdc` + `AGENTS.md` | Evet, alt klasör kazanır | ([Cursor docs](https://cursor.com/docs/rules)) |
| **GitHub Copilot** | `.github/copilot-instructions.md`, `.github/instructions/**.instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Coding agent'ta evet (Ağu 2025); IDE'de ayarla açılıyor (Mar 2026); code review `AGENTS.md` okuyor (Haz 2026) | ([Changelog 2025-08](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/), [2026-03](https://github.blog/changelog/2026-03-11-major-agentic-capabilities-improvements-in-github-copilot-for-jetbrains-ides/), [2026-06](https://github.blog/changelog/2026-06-18-copilot-code-review-agents-md-support-and-ui-improvements/)); Copilot CLI'da nested desteği için açık issue'lar var ([#3051](https://github.com/github/copilot-cli/issues/3051)) |

- `AGENTS.md` Linux Foundation altındaki Agentic AI Foundation'a devredildi, 20–30+ araç destekliyor (ikincil, [morphllm](https://www.morphllm.com/agents-md-guide)). *Dikkat:* aynı kaynak "Claude Code AGENTS.md okumaz" diyor — **resmi doküman bunu yalanlıyor** (v2.1.277+). İkincil kaynaklar hızla eskiyor.
- Thoughtworks: talimat dosyaları **ekip varlığı**, kişisel ayar değil ("curated shared instructions") ([Radar — AGENTS.md](https://www.thoughtworks.com/radar/techniques/agents-md)).
- İkincil bir özet, "geliştiricinin yazdığı AGENTS.md başarıyı artırıyor, LLM'in ürettiği AGENTS.md maliyeti %20+ artırıyor" diyor — kaynağını doğrulamadım ([danielvaughan](https://codex.danielvaughan.com/2026/05/27/agent-instruction-files-agents-md-claude-md-cross-tool-portability-codex-cli/)). Yine de pratik ders makul: **talimat dosyasını agent'a baştan yazdırma, insan küratörlüğünde kısa tut.**

### 1.6 Paylaşılan skill / prompt kütüphanesi, MCP
- **Agent Skills (SKILL.md):** Anthropic'in Aralık 2025'te açık standart yaptığı klasör+`SKILL.md` formatı; ad+açıklama başta yüklenir, gövde gerekince (progressive disclosure). Claude Code, Codex, Gemini CLI, Copilot, Cursor ve Antigravity destekliyor ([agentskills.io](https://agentskills.io/home), [Codex skills](https://developers.openai.com/codex/skills), [Cursor skills](https://cursor.com/docs/skills)). **Her aracın skill klasör yolu farklı** (`.claude/skills/`, `.agents/skills/`, `.cursor/skills/`…) — tam yollar araç araç doğrulanmadı; öneri: tek kaynak `tools/skills/` + symlink.
- **MCP:** her agent destekliyor ama **yapılandırma formatları farklı** (Claude `.mcp.json`, Cursor `.cursor/mcp.json`, Codex `config.toml`, Gemini `settings.json` — format ayrıntıları doğrulanmadı). Öneri: MCP listesini minimal tut (GitHub MCP; lokal dev DB salt-okunur; doküman MCP'si opsiyonel) ve `tools/mcp/servers.yaml`'dan küçük bir betikle üret.
- **K kuralı hatırlatması:** "prod verisi prod dışına çıkmaz — AI kodlama agent'ları dahil" (tez v4 §8). MCP ile hiçbir agent prod DB'ye bağlanmaz.

### 1.7 Trunk-based, küçük PR, stacked PR, worktree
- **Stacked PR'lar GitHub'da yerli:** özel önizleme 13 Nisan 2026, **public preview 30 Temmuz 2026**; `gh extension install github/gh-stack`; mevcut review/check/merge kuralları çalışıyor; GA tarihi yok, davranış değişebilir ([Changelog](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/), [Docs](https://docs.github.com/en/pull-requests/how-tos/stacked-pull-requests)). NutriScan'de "sözleşme PR'ı → uygulama PR'ı" zinciri için kullanışlı; zorunlu değil.
- **Git worktree ile paralel agent:** Claude Code ekibinin en çok verdiği ipucu "3–5 worktree, her birinde ayrı oturum" (Boris Cherny, Şubat 2026, ikincil); pratik tavan review kapasitesi. Güvenli paralellik tarifi: **her işçi sınırlı bir bölgeye sahip, kendi worktree'sinde, lokal test, bağımlılık sırasıyla merge** ([özet](https://blog.vibecoder.me/multi-claude-parallel-agents-anthropic-workflow), [aakashx](https://www.aakashx.com/blog/parallel-claude-code-agents/)). Bu, bizim modül modelinin kişi-içi versiyonu.

### 1.8 CI kapıları
- **Mimari:** Spring Modulith `verify()` + ArchUnit kuralları (K01–K20'den türeyen: "alerjenli seçenek çözücüye gitmez", "maskelenmemiş veri dış LLM istemcisine gitmez" → paket bağımlılık testleri).
- **Stil:** Spotless/Checkstyle (Java), ESLint + Prettier (TS), Ruff (Python veri doğrulayıcıları).
- **Test/coverage:** JaCoCo / Vitest; eşik değişen kod üzerinde (toplam değil). Mutation testing (PIT) — Thoughtworks feedback kontrolü; yalnız `safety` ve `planning` için, D1 sonrası.
- **Sır:** private repoda GitHub secret scanning/push protection **ücretli (GitHub Secret Protection, Team/Enterprise)**, public'te ücretsiz ([GitHub Docs](https://docs.github.com/code-security/secret-scanning/about-secret-scanning), [Changelog 2023](https://github.blog/changelog/2023-05-09-secret-scannings-push-protection-is-available-on-public-repositories-for-free/)) → **gitleaks** pre-commit + CI. (Eski repoda commit'li SMTP/DB sırları sorunu hâlâ açık — DURUM.md.)
- **Sözleşme:** `oasdiff breaking`; üretilmiş istemci diff'i (üretilen kod elle düzenlenmişse kırmızı).
- **Veri:** JSON Schema + sözlük üyeliği + alerjen kapanışı + "her malzemenin fiyatlı SKU'su" (tez §7).

---

## 2. Proje yönetimi aracı

| | GitHub Projects | Linear | Jira (Free) | Plane |
|---|---|---|---|---|
| Ücret (3 kişi) | Ücretsiz | Ücretsiz: sınırsız üye, **250 aktif issue, 2 takım**; sınırda yeni issue açılmıyor | Ücretsiz ≤10 kullanıcı; **Rovo AI yok (Premium+)**; 100 otomasyon/ay | Cloud ücretsiz ≤12 üye; CE self-host AGPL, sınırsız |
| GitHub bağı | Yerli (issue=kart, PR "closes #") | Resmî entegrasyon | Uygulama ile | Entegrasyon |
| Agent erişimi | `gh` CLI (her agent terminalde çalıştırır) + **GitHub MCP `projects_list/get/write`** (Oca 2026) | Resmî MCP `mcp.linear.app/mcp` | Atlassian MCP (plan durumu doğrulanmadı) | Resmî MCP (`mcp.plane.so`, 30+ araç) |
| Danışman raporu | Iteration alanı, roadmap/tablo görünümü, grafikler; issue'lardan otomatik rapor | Cycles, iyi raporlar | Güçlü ama ağır | Cycles/modules |
| Risk | Scrum ergonomisi Linear'dan zayıf | 250 aktif issue sınırı 7–8 aylık projede sıkıştırır (arşivleme disiplini gerekir) | Öğrenci ekibe ağır, AI yok | İkinci sistem, senkron yükü |

Kaynaklar: [Linear fiyat](https://t0ggles.com/blog/linear-free-plan-limits) (ikincil), [Linear MCP](https://aidenapp.org/linear-claude-code) (ikincil), [Jira pricing](https://www.atlassian.com/software/jira/pricing), [Plane MCP](https://developers.plane.so/dev-tools/mcp-server), [Plane free](https://freealternatives.to/plane/free-plan) (ikincil), [GitHub MCP projects](https://github.blog/changelog/2026-01-28-github-mcp-server-new-projects-tools-oauth-scope-filtering-and-new-features/).

**Öneri: GitHub Projects.** Gerekçe: (1) ücretsiz ve sınırsız; (2) kod, PR, CI, CODEOWNERS ve kart **aynı yerde** → "kart → branch → PR → merge → kart kapanır" otomatik; (3) üç farklı agent'ın ortak paydası `gh` CLI ve GitHub MCP — Linear/Plane MCP'sini herkesin aracında ayrıca kurmak gerekmez; (4) danışman raporu (`SDP Meeting Record Form`) kapanan issue'lardan agent'la üretilebilir. Linear daha iyi UX sunar ama 250 issue sınırı ve ikinci sistem maliyeti bu ekip için gereksiz. *Linear'ın öğrenci/eğitim programı var mı — doğrulamadım.*

**Kurulum:** tek org-level Project "NutriScan"; alanlar: `Status` (Backlog/Ready/In progress/In review/Done), `Iteration` (2 haftalık), `Module` (tek seçim: aşağıdaki modül listesi), `Omurga` (Motor/Güvence1/Güvence2/Veri/Zemin/Demo şeridi — tez §3 önceliklendirme kuralı), `Deney` (E1/E2/E3/—), `Dalga` (D0/D1/Kış/D2/D3). Etiketler: `mod:<ad>`, `contract-change`, `cross-module`, `agent:<araç>` (hız ölçümü için).

---

## 3. ÖNERİ — NutriScan çalışma modeli

### 3.a Bileşen/modül haritası ve sahipler
Tez §12'deki hat önerisi korunuyor: **A** optimizasyon/öneri/deneyler · **B** backend çekirdek/kural motoru/Gizlilik Kapısı/admin · **C** mobil/web/vision. Buna iki açık yük eklendi: **asistan** ve **veri fabrikası**. Her modülün bir **sahibi** ve bir **vekili** var (vekil: sahip yokken onay verebilir).

| # | Modül (klasör) | Omurga | İçerik | Sahip | Vekil |
|---|---|---|---|---|---|
| 1 | `backend/…/planning` | Motor | MSM (menü + paket + kiler/SKT + ≤2 market + Akıllı Takas), zaman sınırlı exact, boşluk rozeti | **A** | B |
| 2 | `backend/…/recommendation` | Motor | kısıt-farkında öneri, beğeni | **A** | C |
| 3 | `research/` (E1/E2/E3) | Deneyler | benchmark, sentetik hane üreteci, analiz notebook'ları | **A** | B |
| 4 | `backend/…/household` + `identity` + `consent` | Zemin | hane, üyeler, kesin kısıtlar, rıza, silme/anahtar imhası | **B** | A |
| 5 | `backend/…/safety` | Güvence (kural motoru) | 4 hüküm, "Doğrulanamadı" ilkesi, alerjen doğrulama | **B** | A |
| 6 | `backend/…/audit` + `decisionlog` | Zemin / Güvence 1 | karar kaydı (DR#), silinemez audit, Röntgen verisi | **B** | C |
| 7 | `backend/…/privacy` | Güvence 2 | Gizlilik Kapısı: hassaslık dedektörü, yer tutucu, TR/bulut yönlendirme bayrağı | **B** | A |
| 8 | `backend/…/assistant` | Güvence 1 | LLM orkestrasyonu, araç kataloğu, claim checker | **B** *(öneri; alternatif A — bkz. not)* | A |
| 9 | `backend/…/catalog` | Zemin | ürün, SKU, zincir, fiyat + yaş etiketi, OFF girdisi güvenilmeyen metin | **B** | C |
| 10 | `backend/…/pantry` | Döngü | kiler, SKT, "bitti", e-Arşiv/fiş eşleştirme, tükenme v0 | **C** | A |
| 11 | `backend/…/vision` (+ model adaptörleri) | Görünür AI | etiket/fiş okuma, raf/buzdolabı (demo şeridi) | **C** | B |
| 12 | `apps/mobile` | UX | 5 sekme, barkod, ses | **C** | B |
| 13 | `apps/web` | UX | Stüdyo, "Bu plan neden böyle?", sağlığın fiyatı | **C** | A |
| 14 | `apps/admin` | Zemin | katalog düzeltme, Sözleşme panosu, audit görünümü | **B** (tez §12) | C |
| 15 | `data/recipes`, `data/dictionary`, `data/catalog`, `data/substitutions` | **Veri katkısı** | 200 tarif, malzeme sözlüğü, fiyat CSV, ikame tablosu | **Veri sahibi (tek kişi, açık karar)** | diğer ikisi çift onay |
| 16 | `data/allergens` + `data/eval/allergen-gold` | Güvence (veri) | alerjen ontolojisi, çapraz reaksiyon, altın set (n≥300, FN=0 kapısı) | **B** | A |
| 17 | `contracts/` | Zemin | OpenAPI, event şemaları, motor I/O şeması, LLM araç kataloğu | ilgili **sağlayıcı** modülün sahibi | tüketici onayı zorunlu |
| 18 | Kök dosyalar, `.github/`, `infra/`, `docs/anayasa.md`, `AGENTS.md` | Zemin | CI, deploy (TR hosting), talimat dosyaları, K/S | **Platform rolü** (ekip lideri) | herhangi biri |

**Yük notları (karar Levent'in, kişileri bilmeden öneremem):**
- **Asistan kimde?** B önerisi: Gizlilik Kapısı asistanın ön kapısı; "yurt dışına ne çıkar" sınırının tek sahibi olması K kuralı açısından temiz. Bedeli: B en yüklü hat olur. Alternatif A: E2 ("neden LLM yetmez") A'nın deneyi ve asistan motor araçlarını çağırıyor. Hangisi olursa olsun `assistant` modülü **karar vermez** (tez §3), yalnız araç çağırır → sözleşme LLM araç kataloğudur.
- **Veri fabrikası kimde?** Tez §7 "tek sahip" diyor. İş **öne yüklü** (60 tarif 15 Kas, 120 tarif 15 Oca, 200 tarif 1 Mar; ≥12 tarif/hafta + 60–110 saat etiketleme), UI işi ise D2'de zirve yapıyor. Bu zaman tamamlayıcılığıyla **C** mantıklı aday; alternatif **A** (verinin ana tüketicisi — üretici ve tüketici aynı kişi, sözleşme sürtünmesi az, ama A'nın E1 + MSM yükü ağır ve kritik yol tek kişiye toplanır). Alerjen verisi her iki durumda **B**'de kalır (güvenlik kapısıyla aynı sahip).
- **Platform rolü:** zemin dosyalarını (AGENTS.md, CI, ArchUnit kuralları, sözleşme iskeleti) tek bir kişinin yazıp bakımını yapması tutarlılığı artırır. Bu rol modül sahipliğine **ek**, ağırlığı D0'da.

**Modüller arası sözleşmeler (kim kime ne verir):**
| Sağlayıcı → Tüketici | Sözleşme | Biçim |
|---|---|---|
| backend → mobile/web/admin | REST API | `contracts/openapi/<modül>.yaml` → üretilmiş TS istemcisi `packages/api-client` (elle düzenlenmez) |
| safety → planning | "uygun aday kümesi" (alerjenli tarif/ürün çözücüye hiç gitmez) | Modulith API paketi `safety.api.EligibilityService` + ArchUnit: `planning` aday tarif/ürün kümesini yalnız `safety.api` üzerinden alır (catalog'un ham ürün listesine doğrudan erişim yok) |
| planning → assistant, web | `PlanRequest` / `PlanResult` (+ optimallik boşluğu, DR#) | `contracts/engine/*.schema.json` + `contracts/engine/fixtures/` (golden örnekler → C ve asistan motor bitmeden stub'la çalışır) |
| catalog/pantry/household → planning | domain event'ler (`PriceUpdated`, `PantryChanged`, `ConstraintChanged`) → S16 yeniden değerlendirme | `contracts/events/*.md` + event sınıfları modülün `events` named interface'inde |
| tüm karar veren modüller → audit | karar kaydı şeması | `contracts/decision-record.schema.json` (B) |
| modüller → assistant | LLM araç kataloğu (05-agent-mimarisi §6.3) | `contracts/llm-tools/*.json` — araç tanımı asistan sahibinde, uygulaması ilgili modülde |
| privacy → assistant, vision | "maskelenmiş metin" tipi; dışa giden tek istemci | ArchUnit: dış LLM SDK'sını yalnız `privacy.gateway` import edebilir (tek çıkış kapısı, K kuralı) |
| data → catalog, planning, safety | tarif/sözlük/fiyat/alerjen dosyaları | `data/schemas/*.schema.json`; backend veriyi build/seed adımında okur, elle kopyalamaz |

### 3.b Repo yapısı — monorepo
**Neden monorepo:** agent'lar bütün bağlamı tek yerde görür; sözleşme değişikliği + üretilmiş istemci tek PR'da atomik; tek `AGENTS.md`, tek CI, tek Project. 3 kişilik ekipte polyrepo'nun sürüm/senkron yükü gereksiz. **Nx/Turborepo şimdilik yok** (pnpm workspaces 2–10 paket için yeterli — [karşılaştırma](https://dev.to/yobox/how-to-pick-a-monorepo-tool-in-2026-kko)); ihtiyaç doğarsa Nx'in Gradle eklentisi var ([Nx blog](https://nx.dev/blog/spring-boot-with-nx)). *Mobil Expo seçilirse EAS'ın pnpm ile sorun çıkarabildiği bildiriliyor (ikincil, doğrulanmadı; Faz 3 mobil ADR'sinde test edilecek).*

```
nutriscan/
├── AGENTS.md                      # tek kaynak, ~120 satır, "içindekiler"
├── .github/
│   ├── CODEOWNERS
│   ├── pull_request_template.md   # agent/model, spec linki, sözleşme etkisi, öz-kontrol
│   ├── ISSUE_TEMPLATE/            # feature(spec), bug, contract-change, data
│   └── workflows/                 # ci-backend, ci-apps, ci-data, ci-contracts, ci-guard
├── docs/
│   ├── anayasa.md                 # K01–K20 + S1–S22 (constitution)
│   ├── adr/                       # plan/kararlar.md'nin repo kopyası/devamı
│   ├── architecture/module-map.md # bu tablonun canlı hali (+ Modulith Documenter çıktısı)
│   └── specs/<issue-no>-<ad>.md   # yalnız büyük özellikler için
├── contracts/
│   ├── openapi/  events/  engine/{schema,fixtures}/  llm-tools/
│   └── decision-record.schema.json
├── backend/                       # Gradle, Spring Boot + Spring Modulith
│   └── src/main/java/…/nutriscan/
│       ├── household/ safety/ catalog/ planning/ recommendation/
│       ├── pantry/ vision/ assistant/ privacy/ audit/ shared/
│       └── (her modülde AGENTS.md + package-info.java @ApplicationModule)
│   └── src/test/…/architecture/   # ModularityTests (verify), ArchUnit K-kuralları
│   └── src/main/resources/db/migration/<modül>/   # Flyway, modül başına klasör
├── apps/ mobile/ web/ admin/      # her birinde AGENTS.md
├── packages/ api-client/ (üretilmiş) ui/ (tasarım token'ları, C)
├── data/
│   ├── recipes/ dictionary/ catalog/ substitutions/ allergens/
│   ├── schemas/ validators/ (Python, uv)
│   └── eval/ (altın set METADATA; fiş/etiket görselleri repoda DEĞİL — KVKK, marka görseli)
├── research/ e1/ e2/ e3/          # notebook + benchmark (tez 05-ek-menu_bench taşınır)
├── infra/ compose/ deploy/        # TR hosting (Faz 3)
├── tools/
│   ├── skills/                    # tek kaynak SKILL.md'ler → araç klasörlerine symlink
│   ├── mcp/servers.yaml           # tek kaynak → araç formatlarına üretim betiği
│   └── scripts/                   # sync-agent-files, sprint-report, new-module
├── .claude/rules/                 # Claude'a özel, ince (paths: frontmatter)
├── .cursor/rules/                 # Cursor'a özel, ince (.mdc, glob)
├── .gemini/settings.json          # context.fileName: ["AGENTS.md"]
└── .agents/rules/                 # Antigravity workspace kuralları (ince)
```

### 3.c Branch / PR / CI kuralları
**Hosting ön koşulu:** repo **GitHub Pro'lu (Student Developer Pack) bir kişisel hesapta private**, diğer ikisi collaborator → protected branch + CODEOWNERS çalışır ([Student Pack](https://education.github.com/pack)). Alternatif: org + public repo (her şey ücretsiz, secret push protection dahil) — ama kod ve veri erkenden açılır; veri lisansı/KVKK açısından `data/eval` zaten repoda olmayacak. Karar Levent'in.

- **Trunk-based:** tek uzun ömürlü dal `main`; kısa dallar `<mod>/<issue-no>-<kısa-ad>`; dal ömrü **≤2 gün**; günde en az bir kez `main`'e rebase.
- **PR boyutu:** hedef ≤400 satır insan-yazımı değişiklik (üretilmiş kod, lockfile, veri YAML'ı hariç); aşarsa böl (stacked PR opsiyonel).
- **Bir PR = bir modül.** İki modüle dokunan PR ancak `contract-change` etiketiyle ve iki sahibin onayıyla (bkz. 3.e).
- **Merge:** squash; Conventional Commits başlık (`feat(planning): …`); PR gövdesinde `Closes #N`.
- **Zorunlu onay:** CODEOWNERS'taki sahip ya da vekil; sahip kendi PR'ını açtıysa diğer iki kişiden biri. Veri PR'larında tez §7'deki **çift onay**.
- **Review SLA:** 24 saat. 48 saati geçerse ve PR tüm kontrolleri geçiyor + sözleşmeye dokunmuyorsa herhangi bir üye onaylayabilir (darboğaz önleyici).
- **PR şablonu (agent'lı çağ için):** hangi agent/model; hangi issue/spec; sözleşme etkisi (yok/eklemeli/kırıcı); "agent'ın yazdığını okudum ve açıklayabilirim" onay kutusu (cognitive debt önlemi); ekran görüntüsü (UI).
- **Zorunlu CI kontrolleri (`main` koruması):**
  1. build + unit test (değişen modüller)
  2. `ModularityTests` (Spring Modulith `verify()`) + ArchUnit K-kuralları
  3. lint/format (Spotless, ESLint/Prettier, Ruff)
  4. `oasdiff breaking` + üretilmiş istemci güncel mi
  5. `gitleaks`
  6. veri doğrulayıcıları (şema, sözlük üyeliği, alerjen kapanışı, fiyatlı SKU kapsaması)
  7. değişen kodda coverage eşiği (başlangıç %70, `safety` ve `privacy` için %90)
  8. **ci-guard:** talimat dosyası kuralları (kök `CLAUDE.md` yok, `CLAUDE.local.md` commit'lenmemiş, her modül klasöründe `AGENTS.md` var ve CODEOWNERS'ta sahibi var, AGENTS.md ≤150 satır)
  9. alerjen altın set regresyonu (FN=0) — `safety` veya `data/allergens` değişince
- **Hotspot dosyalar** (çakışma kaynakları): `build.gradle(.kts)` kök, `settings.gradle`, `pnpm-lock.yaml`, `application.yml`, Flyway sürüm numaraları. Kurallar: Flyway **modül başına klasör + zaman damgalı sürüm** (`V20261104_1530__…`); lockfile yalnız bağımlılık PR'ında; kök build dosyaları platform rolünde.
- **Lokal:** her üye kendi içinde paralel agent çalıştıracaksa `git worktree` (modül içi alt görevler için).

### 3.d Agent talimat dosyası mimarisi
**İlke:** tek kaynak, kısa, mekanik olarak doğrulanan. Kurallar dosyada **ve** testte; dosya "neden"i ve haritayı söyler, CI "ne"yi zorlar.

1. **Kök `AGENTS.md` (~100–150 satır, içindekiler):**
   - Proje tek paragraf + omurga (tez §3) + "karar LLM'de değil motorda".
   - Modül haritası (tablo: klasör → sahip rolü → modülün AGENTS.md linki).
   - **Altın kurallar** (10 madde, K01–K20'nin en kritikleri; tam liste `docs/anayasa.md`): Doğrulanamadı ilkesi · tek çıkış kapısı · prod verisi yok · sır yok · enum ordinal yok · alerjenli seçenek çözücüye gitmez…
   - **Sınır kuralı:** "Sana verilen görev hangi modüldeyse yalnız o klasörü değiştir. Başka modüle ya da `contracts/`a dokunman gerekiyorsa DUR, `contract-change` issue'su aç."
   - Komutlar: build, test, lint, üretim (`./gradlew generateApi`, `pnpm gen:api`), veri doğrulama.
   - PR kuralları (3.c özet) ve PR şablonunu doldurma zorunluluğu.
2. **Modül `AGENTS.md` (≤60 satır):** modülün sorumluluğu, public API'si, izinli bağımlılıkları, kendine özgü kurallar (ör. `planning`: "çözücüye zaman sınırı zorunlu; exact başarısızsa sezgisel + boşluk rozeti"; `safety`: "belirsizlikte her zaman Doğrulanamadı; test olmadan kural ekleme"), modül testlerinin nasıl çalıştığı.
3. **Araç-özel ince dosyalar:**
   | Araç | Ne yapıyoruz |
   |---|---|
   | Claude Code | **Kökte `CLAUDE.md` yok** (varsa AGENTS.md'ler okunmaz). Claude v2.1.277+ zorunlu. Claude'a özel şeyler `.claude/rules/*.md` (`paths:` ile). Eski sürüm/`AGENTS.md` okuyamayan oturum için yedek: tek satırlık `CLAUDE.md` = `@AGENTS.md` — ama bu durumda alt klasör `AGENTS.md`'leri yüklenmez, onlar da import edilmeli. `CLAUDE.local.md` yasak (AGENTS.md'yi kapatır). |
   | Codex | Doğrudan `AGENTS.md` + nested; toplam boyut sınırı (32 KiB) → kök + modül dosyaları kısa kalmalı. `AGENTS.override.md` repoda yasak. |
   | Gemini CLI | `.gemini/settings.json` → `"context": {"fileName": ["AGENTS.md"]}` repoda commit'li; `GEMINI.md` yok. |
   | Antigravity | Kökte `AGENTS.md` okunuyor; ek kural gerekirse `.agents/rules/` (≤12k karakter). |
   | Cursor | `AGENTS.md` nested okunuyor; `.cursor/rules/*.mdc` yalnız glob'a bağlı küçük ekler için. |
   | Copilot | `AGENTS.md` coding agent + code review'da okunuyor; IDE'de nested için ayar açılmalı; `.github/copilot-instructions.md` = "AGENTS.md'yi oku" tek satır. |
4. **Skill kütüphanesi (`tools/skills/`)** — tekrar eden işler için SKILL.md: `new-endpoint` (OpenAPI'den başla → generate → implement → test), `new-recipe` (şema, sözlük kontrolü, alerjen etiketi), `contract-change` (3.e protokolü), `write-migration` (Flyway modül klasörü), `sprint-report` (Meeting Record taslağı). Symlink: `.claude/skills`, `.agents/skills`, `.cursor/skills` → `tools/skills` *(her aracın yolu kurulumda doğrulanacak)*.
5. **Bakım:** talimat dosyası değişikliği = platform rolünün onayı gereken PR; iki haftada bir "talimat bahçıvanlığı" (eskiyen kuralı sil, çelişkiyi gider); agent bir hatayı iki kez tekrarlarsa kural **önce teste**, sonra gerekirse dosyaya.

### 3.e Çapraz modül değişikliği protokolü
Senaryo: C'nin mobil ekranı `planning`'den yeni bir alan istiyor.
1. **Issue:** `contract-change` etiketiyle, tüketici açar: ne lazım, neden, hangi özellik/omurga.
2. **Sözleşme PR'ı (önce):** yalnız `contracts/` + üretilmiş kod değişir. Yazan tüketici olabilir. **Sağlayıcı sahibin onayı zorunlu**, tüketicinin onayı zorunlu. `oasdiff`:
   - **Eklemeli (non-breaking):** hızlı yol — sağlayıcı onayı yeter, aynı gün.
   - **Kırıcı:** sürümleme ya da tüm tüketicilerin onayı + geçiş planı; D3 freeze'den sonra yasak.
3. **Uygulama PR'ları (sonra, ayrı):** sağlayıcı kendi modülünde uygular; tüketici bu arada `contracts/engine/fixtures` veya mock sunucuyla çalışır. İstenirse stacked PR.
4. **Acil/küçük istisna:** sağlayıcı müsait değilse tüketici sağlayıcı modülünde değişiklik yapabilir, ama PR sahibin ya da vekilin onayı olmadan merge olmaz (CODEOWNERS bunu zaten zorlar).
5. **Modül sınırı değişikliği** (yeni modül, bağımlılık izni, modül devri): ADR + üç kişinin onayı.

### 3.f Haftalık ritim
Danışman resmi ritmi ~2 hafta ve Meeting Record dönemde ≥5 → **2 haftalık sprint, danışman görüşmesine hizalı.**

| Ne | Ne zaman | Süre | Çıktı |
|---|---|---|---|
| Sprint planlama | sprint başı Pazartesi | 30 dk | her sahip kendi modül kolonundan kart seçer; çapraz ihtiyaçlar `contract-change` olarak açılır |
| Async stand-up | her gün | 3 satır | Project'te kart durumu + grup mesajı: dün / bugün / engel |
| **Sözleşme günü** | her Çarşamba | 30 dk | açık `contract-change` PR'ları karara bağlanır (hafta sonuna kadar uygulama yapılabilsin) |
| Entegrasyon + demo | her Cuma | 30 dk | `main` staging'e deploy; her sahip modülünü 5 dk gösterir ve **agent'ın yazdığı kritik bir parçayı açıklar** (cognitive debt önlemi) |
| Veri panosu | her Cuma | otomatik | tez §7 metrikleri (tarif/hafta ≥12, sözlük ve SKU kapsaması, fiyat yaşı, çift onay oranı) |
| Sprint review + retro | sprint sonu | 45 dk | hız metrikleri (tez §8: PR lead time, review süresi, tamamlanan iş; `agent:` etiketine göre kırılım) |
| Danışman raporu | görüşmeden 1 gün önce | agent + 15 dk insan | `sprint-report` skill'i kapanan issue'lardan **SDP Meeting Record** taslağı: "yapılanlar / yapılacaklar" + roadmap görünümü ekran görüntüsü |

D0 (19 Eki – 1 Kas) = **Sprint 0**: repo iskeleti, AGENTS.md v1, CI kapıları, Modulith iskeleti (boş modüller + `verify()` yeşil), OpenAPI iskeleti, veri şeması + sözlük v0, **walking skeleton** (mobil → API → DB → cevap, tek ekran). Kapı: 18 Aralık D1 çıkışı ölçülür (tez §8).

### 3.g Riskler ve önlemler
| Risk | Belirti | Önlem |
|---|---|---|
| **Sahip darboğazı / bus factor** (sınav haftası, hastalık) | PR'lar onay bekliyor | Her modülde vekil; 24/48 saat SLA kuralı; modül AGENTS.md'si ve testler bilgi taşır |
| **Silo, geç entegrasyon** | Her modül tek başına çalışıyor, birlikte değil | Sprint 0 walking skeleton; her Cuma `main`'den staging; uçtan uca smoke test CI'da |
| **Yük dengesizliği** | Bir hat sürekli geride | Modül devri protokolü (ADR + 3 onay); D1 sonunda (18 Ara) yeniden dengeleme |
| **Araç davranış farkı** (üç farklı agent aynı kuralı farklı yorumlar) | Bir modülde sürekli lint/mimari ihlal, büyük PR | Kalite dosyada değil **kapıda**: aynı CI herkese; ortak skill'ler her aracı aynı akışa sokar; PR boyut sınırı; kritik modüllerde (safety, privacy, planning) daha yüksek coverage + mutation testing |
| **Cross-agent conflict** (%41,7) | Sık rebase çakışması | Klasör sahipliği, bir PR = bir modül, kısa dallar, günlük rebase, hotspot kuralları |
| **Mimari kayma / agent drift** | Modüller arası gizli bağımlılık, kopyalanmış mantık | `verify()` + ArchUnit her PR'da; Modulith Documenter ile modül diyagramı her sprint güncellenir; 2 haftada bir drift incelemesi |
| **Talimat dosyası şişmesi / çelişkisi** | Agent kuralları atlıyor | ≤150 satır sınırı CI'da; tek kaynak; kural önce teste |
| **Sözleşme trafiği** (her şey `contract-change`) | Çarşamba toplantısı uzuyor | Eklemeli değişiklikler hızlı yol; motor/ekran için fixture ile erken çalışma |
| **Claude Code AGENTS.md tuzağı** | Claude Code kuralları görmüyor | *(27 Eyl düzeltmesi, ADR-013)* Kökte `CLAUDE.md` = `@AGENTS.md` importu (resmî desen, tüm sürümlerde çalışır); ci-guard bunu denetler |
| **Private repo özellik sınırı** | CODEOWNERS/koruma çalışmıyor | Pro'lu kişisel hesap veya public repo (3.c) |
| **Sır ve kişisel veri sızıntısı** | Eski repodaki SMTP/DB sırrı hatası | gitleaks pre-commit + CI; `.env` şablonu; `data/eval` görselleri repoda değil; MCP yalnız lokal/sentetik DB |
| **Cognitive debt** (kimse agent kodunu anlamıyor) | Jüri sorusuna cevap verilemiyor | PR şablonunda "açıklayabilirim" kutusu; Cuma "kritik parçayı anlat"; ADR'ler |
| **Bireysel katkının görünürlüğü** (not) | Jüri "kim ne yaptı" sorar | Modül sahipliği bunu doğal olarak gösterir; git istatistiği + modül haritası rapora girer |
| **SDD bürokrasisi** | Spec yazmak koddan uzun | Yalnız çapraz modül/büyük özelliklerde `docs/specs`; küçük işte issue gövdesi yeter |

---

## 4. Doğrulanamayanlar / açık
- OpenAI "Harness engineering" sayfası 403 → ikincil özetlerden.
- LinearB/Faros review rakamları, Linear fiyat ayrıntıları, Plane ücretsiz plan, Antigravity `AGENTS.md` sürüm notu: ikincil kaynak.
- Her aracın skill klasör yolu ve MCP yapılandırma formatı araç araç doğrulanmadı — kurulumda (Sprint 0) denenmeli.
- Required reviewer rule'un hangi planda olduğu, GitHub Projects'in tüm özelliklerinin Free'de olup olmadığı (grafik/insights) kurulumda teyit edilmeli.
- Linear eğitim programı araştırılmadı.

## 5. Levent'e sorulacaklar (karar)
1. Asistan modülü B'de mi A'da mı?
2. Veri fabrikasının tek sahibi kim (öneri C, alternatif A)?
3. Repo: Pro'lu kişisel hesapta private mı, org + public mi?
4. Ekip üyeleri hangi agent'ları kesin kullanacak (Codex / Antigravity / Cursor / Copilot)? Talimat dosyası kurulumu buna göre daraltılır.
5. Sprint uzunluğu: danışmana hizalı 2 hafta uygun mu?
