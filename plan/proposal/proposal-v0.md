---
title: CSE 491 Project Proposal — draft v0 (content source for the .docx)
updated: 2026-09-27 (v5.1: health-condition profile, safety-first order, RAG placement — ADR-011)
durum: TASLAK — ekip + danışman incelemesi (takvim A0.5, en geç 9 Ekim; teslim 18 Ekim)
dayanak: arastirma/07-tez-v5.md · plan/urun-tanimi.md · plan/kararlar.md · plan/takvim.md
eksik: grup no, öğrenci numaraları, teslim tarihi → [..] ile işaretli
---

# NutriScan — A Verifiable Household Food Planning Assistant

| | |
|---|---|
| Project title | NutriScan: A Verifiable, Constraint-Aware Household Food Planning Assistant |
| Group no. | [GROUP NO] |
| Project supervisor | Res. Asst. Dr. Taha Yiğit Alkan |
| Submission date | [DATE] |

| # | Name and surname | Student no. | Role / responsibility in the project |
|---|---|---|---|
| 1 | Levent Can Ceylan | [NO] | Architecture and project infrastructure; Household Planning Engine (optimisation); assistant orchestration; Privacy Gateway; decision record and observability; experiments E1–E2 |
| 2 | Şükran Hilal Hocaoğlu | [NO] | Safety rule engine (allergens, health rules); allergen data and gold set; household, identity and consent; catalogue and prices; pantry; recommendation; admin backend |
| 3 | Ozan Karadaş | [NO] | Mobile, web and admin clients; recipe content and health-rule sources; label-reading demo |

## 1. Summary
Households in Türkiye make the same tiring decision every week: what to cook, what to buy, where to buy it, what is already at home and what is suitable for whom. They do it under high food inflation (33.79% year-on-year, August 2026) and with different hard constraints inside the same home, such as a child's nut allergy, a parent's coeliac disease or a grandparent's diabetes. Existing tools solve one dimension at a time: product scores (Yuka, local label scanners), prices (marketfiyati.org.tr) or a single retailer's basket (Migros MAYA AI). NutriScan is a chain-independent assistant that plans a household's week with a safety-first order: hard constraints first, then health-condition rules and goals, then household preferences and pantry, and cost last, with the budget as a limit rather than the goal. Its core is the Household Planning Engine, a single integer optimisation model that jointly selects weekday dinners, the shopping list and at most two chains while using pantry items before expiry, respecting the budget and never violating any member's hard constraint. A deterministic rule engine decides product suitability per member for allergens and for self-declared health conditions (diabetes, hypertension, coeliac disease, pregnancy) using source-cited, versioned nutrient and ingredient rules, with four honest outcomes including "could not verify". Retrieval-augmented generation (RAG) only proposes ingredient mappings and quotes rule sources; an LLM-based assistant only interprets requests and explains results, and every decision is traceable. This semester we deliver a working mobile, web and admin prototype with the verified core, the planning engine on real data and first experiment results.

## 2. Problem Definition and Motivation
**Problem.** Planning a week of meals and groceries for a household is a combinatorial decision with many interacting constraints: each member's allergens, health conditions such as diabetes or hypertension, and diet, nutrition goals (e.g., less sugar or salt), a tight budget, items at home that are about to expire, package sizes, and different prices in different chains. People solve it by habit and by reading labels one product at a time, which does not scale to a whole week or a whole household.
**Why it matters.** Food inflation is the largest contributor to consumer inflation in Türkiye (33.79% in August 2026 [1]); a healthy diet for a family of four costs about 133% of the net minimum wage [2]; average salt intake is about twice the national recommendation [3]; and allergen precautionary labelling ("may contain") is voluntary, so its absence does not mean a product is suitable [4]. Mistakes are costly: an unsuitable product for an allergic child is a safety issue, not an inconvenience.
**Gap.** Consumer apps (Yuka, Fig, Turkish label scanners) score a single product; price comparators ignore health; retailer assistants such as Migros MAYA AI plan meals but only for their own chain and treat dietary needs as filters [5]. Discount chains, which have far more stores, have no such assistant. No tool plans the week for the whole household across chains with verifiable decisions.
**Target users.** Households with at least one hard dietary constraint (allergy, coeliac disease) or a health condition that calls for nutrient limits (diabetes, hypertension, pregnancy), households shopping at discount chains and local markets, and households buying from more than one chain.

## 3. Objectives, Scope and Success Criteria
**Objectives**
1. Build a deterministic, explainable suitability engine for Turkish food products that covers allergens and health-condition rules (source-cited nutrient thresholds and ingredient rules), with four outcomes and a full decision record.
2. Formulate and implement the Household Planning Engine: a joint menu–basket–market integer model (weekday dinners, pack-size integrality, pantry and expiry, ≤2 chains, limited number of swaps) solved with an exact solver under a time limit.
3. Build a verifiable assistant in which an LLM orchestrates tools but can never change a decision, a RAG component that suggests ingredient mappings and cites rule sources without deciding, and a privacy layer that keeps household-context LLM processing in Türkiye (application data hosted in the EU, minimised and encrypted).
4. Create a clean-licensed dataset of Turkish home recipes with an allergen ontology, a product catalogue for two pilot chains (ŞOK and Tarım Kredi), and an allergen gold test set.
5. Deliver mobile, web and admin clients and evaluate the system in a beta with real households.

**Out of scope**
Calorie estimation from plate photos, continuous glucose monitoring, placing orders in retailers' carts, a full dietitian portal, medical advice or diagnosis, kidney-disease and drug–food interaction rules, and an Android store release in this academic year.

**Success criteria**
- Safety gate: zero false negatives on the allergen gold set (n ≥ 300), 100% agreement of health-condition decisions with the threshold table on their test set, and no hard-constraint violation in any generated plan or swap (property tests over ≥10,000 random households).
- Planning (E1): the joint model is compared with sequential "menu first, then list" baselines and with a metaheuristic (NSGA-II [15]) over 20 scenarios × 30 seeds; we report optimality gap, hypervolume and runtime.
- Assistant (E2): compared with an LLM-only planner on 50–100 household scenarios; we report constraint violations, budget violations, invented prices, tool-call accuracy and prompt-injection robustness; RAG ingredient mapping is compared with exact/fuzzy matching on the gold set (precision, recall).
- Beta (E3, spring): 20–40 households (≥10 with a hard constraint); plan/swap acceptance, price freshness, use of expiring pantry items, week-4 retention.
- Performance: shelf decision p95 ≤ 1.5 s; swap suggestion p95 ≤ 1 s.

## 4. Similar Systems and Background
| System / work | What it does | Limitation or gap our project addresses |
|---|---|---|
| Yuka, Fig, Ürün Dedektörü [6][7][8] | Scan a product; score it or warn for personal diet/allergen filters | Single product; no multi-member weekly plan, budget or pantry |
| Migros MAYA AI / meal planner [5] | Conversational meal planning and cart filling for Migros | Single chain; dietary needs as filters; no member-level verification or pantry; no cross-chain optimisation |
| marketfiyati.org.tr [9] | Price comparison across chains | No health, allergen or household model |
| Diet optimisation (Stigler; Maillot et al.) [10][11] | LP models of cheapest adequate diet; minimal departure from observed diet | Population or individual diets, not a real household basket with pack sizes, pantry and chains |
| Meal planning with pantry (van Rooijen et al.) [12] | Menu and purchase optimisation to reduce waste | Single store; no allergen verification or assistant |
| LLM benchmarks (NutriBench, FoodGuardBench) [13][14] | LLMs unreliable for food-safety decisions | Motivates our design: engines decide, LLM explains |

## 5. Preliminary Requirements
**Functional requirements**
Baseline below; the full list (29 items) is kept in the repository.
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | The system shall let a user create a household, invite adult members who give their own consent, and add child profiles under guardian consent. | Must |
| FR-2 | The system shall store, per member, hard constraints (14 regulated allergens, coeliac/gluten, diet choices), optional self-declared health conditions (diabetes, hypertension, pregnancy) and soft goals separately; it shall never diagnose. | Must |
| FR-3 | The system shall decide product suitability per member with a deterministic rule engine and return one of four outcomes: Not suitable, Caution, No conflict found, Could not verify; it shall never label a product as "safe". | Must |
| FR-4 | The system shall apply versioned, source-cited health-condition rules (nutrient thresholds per 100 g, ingredient rules), report "Caution" with the nutrient fact and source, and use informational wording only. | Must |
| FR-5 | The system shall scan EAN/UPC barcodes on mobile and explain each decision (matched ingredient, rule and version, data source and date, confidence). | Must |
| FR-6 | The system shall plan weekday dinners, the shopping list and the chain choice in a single optimisation model in safety-first order (hard constraints, health rules and goals, preferences and pantry, then cost within budget) and report the optimality gap. | Must |
| FR-7 | The system shall propose at most k swaps (k = 1, 3, 5) for a list and, when a plan is infeasible, suggest which soft limits could be relaxed (never hard constraints). | Must |
| FR-8 | The system shall provide a text assistant that answers common intents by calling the decision engines, shows its steps and never changes a decision; medical/dose questions get a fixed safety response. | Must |
| FR-9 | The system shall record every decision in an append-only decision record, keep a tamper-evident audit log, and let moderators approve catalogue corrections with a reason. | Must |
| FR-10 | The system shall keep a catalogue for two pilot chains (ŞOK, Tarım Kredi) with pack sizes, ingredients, prices, source and price age, and track the pantry (barcode, "bought", "finished"). | Must |
| FR-11 | The system shall suggest mappings from unseen label ingredient names to the dictionary with semantic search (RAG), apply them only after moderator approval, and quote rule sources in explanations. | Should |
| FR-12 | The system shall generate a proactive weekly plan that changes nothing until approved, split the list across at most two chains, and accept natural-language constraints that are read back for confirmation. | Should |
| FR-13 | The web app shall provide a Planning Studio with cost–health trade-offs and a "why is the plan like this" view. | Should |

**Non-functional requirements**
| ID | Requirement | How it will be checked |
|---|---|---|
| NFR-1 | Zero allergen false negatives on the gold set; health rules agree with the threshold table; no hard-constraint violation. | CI regression on the gold sets; property-based tests |
| NFR-2 | Shelf decision p95 ≤ 1.5 s; swap p95 ≤ 1 s; re-plan ≤ 3 s with gap badge. | Load tests; OpenTelemetry metrics |
| NFR-3 | No health data in logs/traces/crash reports; household-context LLM calls processed in Türkiye; minimised and encrypted health fields. | Nightly canary test; egress review |
| NFR-4 | 100% of user-visible decisions have a decision record; the assistant cannot alter a decision. | UI–record contract test; LLM eval harness in CI |
| NFR-5 | Module boundaries and architecture rules enforced automatically. | Spring Modulith verify + ArchUnit in CI |
| NFR-6 | OAuth2/PKCE, household-level isolation, admin MFA, no secrets in the repository. | IDOR tests, gitleaks, dependency scanning |

## 6. Method and Technology Plan
**Approach.** Research-first, contract-first development in two-week sprints. The system is a modular monolith (household, safety, catalogue, planning, recommendation, pantry, assistant, privacy, audit) whose module boundaries and architecture rules (e.g., "the LLM cannot change a decision") are verified in CI; every module has one owner.

**Architecture outline.** Mobile (Expo) and web/admin (React) clients use a TypeScript client generated from the OpenAPI contract → Spring Boot modular monolith → PostgreSQL (with pgvector). Inside: the safety rule engine (allergens and health-condition rules) filters and scores candidates before the Household Planning Engine (OR-Tools CP-SAT [16]) solves the joint model; the assistant (Spring AI) calls the engines as tools through a privacy gateway that routes household-context requests to EVREN (open models hosted in Türkiye); a RAG component over pgvector suggests ingredient mappings for moderators and retrieves rule sources for explanations, but is never on the decision path; every decision is written to the decision record and shown in the admin trace view.

**Data.** Open Food Facts (ODbL) [17] as a mirrored source; prices for two pilot chains (ŞOK, Tarım Kredi) from a weekly collector limited to our ingredient dictionary, within robots.txt and never bypassing access controls, each with source and date (public release only with the chains' permission; the public price platform gives no third-party access); 200 team-written Turkish home recipes with an allergen ontology based on the Turkish Food Codex labelling regulation; a versioned health-rule threshold table with a source for every row (Turkish Food Codex nutrition-claim limits; WHO guidelines [19][20] only for weekly goals), approved by a dietitian before any rule produces a verdict; synthetic households for development.

| Layer / component | Technology or tool | Reason for the choice |
|---|---|---|
| Backend | Java 25, Spring Boot 4.1, Spring Modulith, Gradle | Team's common language; Boot 4.1 is the only line supported through June 2027; Modulith verifies module boundaries |
| Planning engine | Google OR-Tools CP-SAT (Java); Python only for experiments | Exact solver with optimality gap under a time limit (needed for E1); no extra service |
| Database | PostgreSQL 18 + pgvector | Relational core, JSONB decision records, vector search for RAG ingredient mapping and recipe search [21] |
| AI layer | Spring AI 2.0; EVREN (Türkiye) for household context; low-cost cloud models only for non-personal tasks | Data sovereignty and cost; decisions stay in deterministic engines |
| Mobile | Expo (React Native), expo-camera, EAS | Most mature path for barcode, speech, push and App Store release |
| Web + admin | Vite + React, TanStack, shadcn/ui, Recharts | Shared TypeScript and generated API client with mobile |
| Identity | Keycloak (self-hosted), OAuth2 PKCE | Standard, self-hostable, role-based admin |
| Hosting and ops | Contabo VPS, Docker Compose, Caddy, OpenTelemetry + Grafana | Low cost; reproducible deployment; observability from day one |
| Process | GitHub (private), Azure Boards (Scrum), AGENTS.md rules for AI coding agents, CI gates | Component ownership and automated gates prevent conflicts between different coding agents |

## 7. Work Plan
Week 1 = 14 September 2026; each package has a latest date and a fallback in the project calendar.
| WP | Work package and its output | Responsible member(s) | Weeks |
|---|---|---|---|
| WP1 | Requirements, architecture, repository, CI gates, agent rules, walking skeleton | Levent (all review) | 3–7 |
| WP2 | Data factory: recipe schema, ingredient dictionary, allergen ontology, health-rule threshold table, price-and-product collector (ŞOK, Tarım Kredi), 60 recipes with prices | Ozan (content, rule sources), Hilal (schema, catalogue) | 4–11 |
| WP3 | Safety core: household and consent flows, rule engine (allergens + health conditions), gold sets, decision record integration | Hilal | 7–13 |
| WP4 | Household Planning Engine v0 on real data; swaps; first E1 measurement | Levent | 7–13 |
| WP5 | Mobile shelf scan with household strip and "Why?", list/swaps UI, web and admin v0 | Ozan (with Hilal for admin backend) | 6–14 |
| WP6 | Assistant v1 and Privacy Gateway v0; first E2 run; interim and final reports; integration | Levent (all members) | 8–14 |

Spring semester (CSE 492): RAG ingredient mapping and source quoting, menu planner in production, pantry, proactive plan, chain split, natural-language constraints, web Planning Studio, recommendation, beta with 20–40 households, final experiments.

## 8. Expected Outputs and Risks
**Expected outputs**
By the end of this semester: working prototype (mobile + web + admin) with the verified safety core, shelf scan with explanations, list and swaps, the Household Planning Engine on real data, assistant v1; private repository with CI gates and documentation; recipe dataset (≥60) and allergen gold set (≥200); interim and final reports with first E1/E2 results.

**Risks**

| Risk | Likelihood | Impact | Mitigation plan |
|---|---|---|---|
| Missing or wrong product/allergen data | High | High | Verified catalogue; "could not verify" instead of guessing; gold-set release gate |
| Collected prices go stale, a site changes or a chain objects | Medium | Medium | Health check per run; stale → "could not verify"; replaceable adapter per chain; stop on objection (K21); CI priced-SKU coverage ≥ 90% |
| Joint optimisation too slow at scale | Medium | Medium | Time-limited exact solver with gap badge; metaheuristic (E1) |
| LLM unreliable or unavailable | Medium | Medium | LLM never decides; workflow intents; template fallback |
| Medical-device boundary for health-condition features [22] | Medium | High | Informational wording only, no diagnosis or treatment claims, source-cited rules, dietitian review, in-app disclaimer |
| Health data protection (KVKK [18]) | Medium | High | Minimised, encrypted health fields; none in logs; household-context LLM calls in Türkiye; EU hosting under KVKK standard contract; legal review before beta |
| Conflicts between AI coding agents | Medium | Medium | Component ownership, contract-first changes, CI gates |

## 9. References
[1] TÜİK, "Tüketici Fiyat Endeksi, Ağustos 2026" (SBB summary, sbb.gov.tr).
[2] Türk-İş, "Ağustos 2026 Açlık ve Yoksulluk Sınırı," turkis.org.tr.
[3] T.C. Sağlık Bakanlığı, "Türkiye'de Tuz Tüketiminin Azaltılması Programı 2017–2021."
[4] Türk Gıda Kodeksi Gıda Etiketleme ve Tüketicileri Bilgilendirme Yönetmeliği, Resmî Gazete 29960, 26.01.2017.
[5] Webrazzi, "Sofralar artık yapay zekâ destekli MAYA ile kuruluyor," 13.12.2024; LOG, "MAYA AI," 2026.
[6] Yuka, "What are Yuka's limitations," https://help.yuka.io/l/en/article/wz3cbbztf3-what-are-yuka-s-limitations
[7] Fig, https://foodisgood.com/
[8] Ürün Dedektörü, https://urundedektoru.com/
[9] marketfiyati.org.tr, TÜBİTAK BİLGEM, https://marketfiyati.org.tr
[10] G. J. Stigler, "The Cost of Subsistence," J. Farm Econ., vol. 27, no. 2, pp. 303–314, 1945.
[11] M. Maillot et al., "Individual diet modeling translates nutrient recommendations into realistic and individual-specific food choices," Am. J. Clin. Nutr. 91(2):421–430, 2010, doi:10.3945/ajcn.2009.28426.
[12] L. van Rooijen et al., Resources, Conservation & Recycling, vol. 205, 107559, 2024, doi:10.1016/j.resconrec.2024.107559.
[13] A. Hua et al., "NutriBench," arXiv:2407.12843.
[14] "Cooking Up Risks / FoodGuardBench," arXiv:2604.01444, 2026.
[15] K. Deb et al., "A fast and elitist multiobjective genetic algorithm: NSGA-II," IEEE TEVC 6(2), 2002, doi:10.1109/4235.996017.
[16] Google OR-Tools, developers.google.com/optimization; Spring Modulith, spring.io/projects/spring-modulith
[17] Open Food Facts API and data (ODbL), https://openfoodfacts.github.io/openfoodfacts-server/api/
[18] KVKK No. 6698 (amended by No. 7499, 2024); KVKK, "Üretken Yapay Zekâ ve Kişisel Verilerin Korunması Rehberi," 2025.
[19] Türk Gıda Kodeksi Beslenme ve Sağlık Beyanları Yönetmeliği, 2017; T.C. Sağlık Bakanlığı, TÜBER 2022.
[20] WHO, "Guideline: Sugars intake for adults and children," 2015; WHO, "Guideline: Sodium intake…," 2012.
[21] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS 2020, arXiv:2005.11401.
[22] Regulation (EU) 2017/745 (MDR); TİTCK Tıbbi Cihaz Yönetmeliği, RG 31499, 2021; MDCG 2019-11 rev.1.
