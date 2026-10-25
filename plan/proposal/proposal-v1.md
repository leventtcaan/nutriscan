---
title: CSE 491 Project Proposal — v1 (content source for the .docx)
updated: 2026-10-17 (re-scoped after advisor meetings of 2, 9 and 16 October; decisions in docs/mimari-karar-belgesi.md)
durum: TARİHSEL V1 TASLAĞI — 18 Ekim hedefi geçti; teslim durumu repoda kayıtlı değil
eksik: yok
---

> **Tarihsel anlık görüntü.** Bu kaynak 17 Ekim'de 18 Ekim teslim hedefi için hazırlandı. Repoda teslim edilip edilmediği kayıtlı değildir. V1 kapsamını ve aynı kategoride alternatif önerisi gibi artık güncel olmayan taslak maddelerini içerir; güncel kapsam için [mimari karar belgesini](../../docs/mimari-karar-belgesi.md) esas alın. AI/araçlarla taslak kural çıkarımı yönlendirmesi bu sürümde henüz yer almıyor.

# NutriScan — Evidence-Based Food Ingredient and Health-Condition Matching

| | |
|---|---|
| Project title | NutriScan: Evidence-Based Food Ingredient and Health-Condition Matching |
| Group no. | 9 |
| Project supervisor | Dr. Taha Yiğit Alkan |
| Submission date | 18.10.2026 |

| # | Name and surname | Student no. | Role / responsibility in the project |
|---|---|---|---|
| 1 | Levent Can Ceylan | 20220808045 | Knowledge-base schema and backend integration; LLM message layer; evaluation coordination; decision record editor |
| 2 | Şükran Hilal Hocaoğlu | 20210808005 | Health-condition list, guideline sources and rule table; evidence sources (CTD, JECFA); licence inventory; test sets |
| 3 | Ozan Karadaş | 20220808007 | Ingredient dictionary and matching pipeline (incl. vector search); Turkish terminology; mobile app and OCR |

## 1. Summary
People with a health condition such as coeliac disease, diabetes, chronic kidney disease or asthma read food labels to decide whether a product suits them. The ingredient list is written in varying words ("E102", "tartrazin", "sarı renklendirici"), some terms are mixtures or classes rather than single substances, and the scientific sources that link substances to conditions are in English and rarely say how much matters. NutriScan is a mobile application that reads a packaged food's ingredient list and nutrition table with OCR, links each Turkish label phrase to a standard concept, and evaluates the product for the user's own conditions with a versioned, source-cited rule table. The result is one of four outcomes (not suitable, caution, no issue found, could not verify) shown with its rule, source and coverage; scientific associations (CTD, JECFA) are shown as research information and never turn into warnings by themselves. Matching runs in three steps: exact dictionary lookup, fuzzy matching, and vector search (Qdrant) as a fallback with an acceptance threshold. An LLM writes the final message from the structured result but cannot change it. By the end of the semester we deliver a working mobile prototype covering diet-relevant conditions with guideline-based rules, and a measured comparison of dictionary-only and hybrid matching on real Turkish labels.

## 2. Problem Definition and Motivation
**Problem.** Deciding whether a packaged food suits a person with a health condition requires three steps that are hard for a person and for software: recognising what each label phrase means, knowing which of those substances or nutrient amounts matter for the condition, and knowing how strong the evidence behind that link is. Label wording is inconsistent, Turkish terms rarely appear in international scientific databases, and associations in the literature do not state dose or causality.
**Why it matters.** Mistakes have a cost in both directions: missing a gluten source is a health issue for a person with coeliac disease, while warning about every ingredient that appears somewhere in the literature makes an application useless and scientifically wrong. Turkish labelling law makes the ingredient list and the main nutrition values mandatory [1], so the information needed for many decisions is on the package, but it is not machine-readable for the consumer.
**Gap.** Existing scanners score a product or apply diet filters, usually through barcodes and without showing why a warning was produced or how certain it is (Section 4). Large language models can describe a label photo, but they are not consistent across runs and do not separate a documented association from a guideline-based recommendation.
**Target users.** Adults in Türkiye managing a diet-relevant condition themselves (e.g., coeliac disease, diabetes, chronic kidney disease, hypertension, asthma with sulphite sensitivity) who read labels before buying.

## 3. Objectives, Scope and Success Criteria
**Objectives**
1. Read Turkish ingredient lists and nutrition tables from label photos (OCR), with user correction.
2. Split and type each label phrase (single chemical, chemical class, mixture, food raw material, nutrient value) and link it to a standard concept (E-number, CAS, MeSH) without inventing chemical identities.
3. Build a versioned rule table for diet-relevant conditions from clinical guidelines and food regulation, with three rule types: presence, amount, declaration.
4. Show each result with its rule, source, coverage and research evidence; say "could not verify" when data or rules are missing.
5. Measure the contribution of vector search over dictionary matching on real Turkish labels.

**Out of scope**
Barcode scanning and product databases; storing scanned products; product recommendations or alternatives (possible later feature); dose or exposure calculations; diagnosis, treatment advice or clinical validation; drug interactions and reconciliation of multiple conditions.

**Success criteria**
- Matching test (100 real label phrases with reference answers): dictionary-only and hybrid settings reported on accuracy, answer rate, precision of answered items and wrong-match count; hybrid kept only if it improves accuracy without raising wrong matches.
- Rule test (20 product × condition scenarios): zero missed "not suitable" outcomes; every rule row has a source, section, version and two independent reviewers.
- Same input and same rule version always give the same outcome.
- End-to-end demo on real Turkish labels on a phone, including the LLM message with template fallback.

## 4. Similar Systems and Background
| System / work | What it does | Limitation or gap our project addresses |
|---|---|---|
| Yuka [2] | Barcode scan; 0–100 product score; premium diet filters | Single score, no health-condition rules; not available in Türkiye |
| Fig [3] | Barcode scan with thousands of diet and allergen filters | Filters without visible evidence or uncertainty; US market |
| Fooducate [4] | Product grades and tracking; premium modes for some conditions | US data; grades do not show rule source or coverage |
| Ürün Dedektörü [5] | Turkish barcode/label analysis with personal filters (allergy, pregnancy, coeliac) | Limited condition coverage (diabetes, kidney disease, asthma); no evidence level |
| CTD [6], WHO JECFA [7] | Curated chemical–disease associations; additive safety evaluations | Associations without dose or causality; English; not consumer rules |
| Biomedical entity linking (BioSyn [8], SapBERT [9]) | Map free-text terms to standard concepts with lexical and dense retrieval | Evaluated on English biomedical text, not Turkish food labels |

Our contribution is the combination: Turkish label-phrase linking with typed concepts, a rule table that separates guideline-based decisions from literature associations, and transparent results with coverage and uncertainty.

## 5. Preliminary Requirements
**Functional requirements**
| ID | Requirement | Priority (must / should / could) |
|---|---|---|
| FR-1 | The system shall let the user select one or more health conditions in a profile kept on the device. | must |
| FR-2 | The system shall capture a label photo, extract the ingredient list and nutrition values with OCR, and let the user correct the text. | must |
| FR-3 | The system shall split the ingredient list and assign each phrase a type (single chemical, chemical class, mixture, food raw material, nutrient, unknown). | must |
| FR-4 | The system shall link phrases to canonical concepts by exact dictionary lookup, then fuzzy matching, then vector search with a threshold; unresolved phrases shall be marked "could not verify". | must |
| FR-5 | The system shall evaluate the product for each selected condition with the versioned rule table and return one of four outcomes. | must |
| FR-6 | The system shall show for each outcome the rule, its source and section, the data used and the coverage; CTD/JECFA evidence shall be shown as information only. | must |
| FR-7 | The system shall generate the final user message with an LLM from the structured result, with a template fallback. | should |
| FR-8 | The team shall be able to add aliases and rule rows through a reviewed data file, without code changes. | should |
| FR-9 | The system could suggest products of the same category that better fit the profile. | could |

**Non-functional requirements**
| ID | Requirement | How it will be checked |
|---|---|---|
| NFR-1 | Same input and same rule version produce the same outcome. | Repeated runs on the rule test set |
| NFR-2 | The LLM message never changes the outcome or adds facts; no "safe/harmful" wording. | Automated check of messages on the test set; banned-word list |
| NFR-3 | No scanned product or health profile is stored on the server. | Schema review; request/log inspection |
| NFR-4 | A result is shown within 3 s (p95) for a typical label after OCR. | Timing on the test set |
| NFR-5 | Every rule row carries source, section, version and two reviewers. | Data validation script |

## 6. Method and Technology Plan
**Approach.** Small, decision-first increments: one shared decision record defines the architecture; each component has one owner; results are measured on fixed test sets. Rules are data, so adding a condition adds rows, not code.
**Architecture outline.** Mobile app (Expo) captures the label and runs on-device OCR → Python service (FastAPI) splits and types phrases → matching pipeline: exact lookup and fuzzy matching on the alias table, then Qdrant nearest-neighbour search over alias embeddings with an acceptance threshold → rule engine evaluates presence, amount and declaration rules per condition (amounts come from the nutrition table, not from ingredient names) → evidence lookup adds CTD/JECFA information → an LLM turns the structured result into a short Turkish message; a checker rejects messages that change the outcome or use banned words, falling back to a template.
**Data.** A knowledge base only: concepts (E-number, CAS, MeSH, PubChem CID), aliases with relation types (same as, contextual, is-a, contains, may contain), conditions with coverage notes, rules (type, condition, outcome, missing-data outcome, source, section, version, two reviewers), evidence (CTD, JECFA, with study counts) and a source/licence inventory. Sources: Turkish Food Codex additive and labelling regulations [1][10], Open Food Facts ingredients taxonomy [11], CTD vocabulary and associations [6], PubChem [12], WHO JECFA [7], clinical guidelines such as ADA 2026 and KDIGO 2024 [13][14]. Only needed Turkish terms are added to the alias table, reviewed by two members; FooDB is excluded for licence reasons (CC BY-NC) [15].
| Layer / component | Technology or tool | Reason for the choice |
|---|---|---|
| Mobile client and OCR | Expo (React Native), on-device text recognition (library chosen on 20 real labels) | One code base for iOS and Android; no photo upload |
| Matching and rule service | Python, FastAPI, rapidfuzz, multilingual embedding model | Text matching and embedding tools are Python-native |
| Knowledge base | PostgreSQL | Relational rules, sources and versions |
| Vector search | Qdrant (alias embeddings only) | Fallback matching step; contribution measured by switching it off |
| Final message | LLM with structured input and output checker | Readable explanations without letting the model decide |

## 7. Work Plan
Week 1 = 14 September 2026; interim report around week 8, final report and demo around week 14.
| WP | Work package and its output | Responsible member(s) | Weeks |
|---|---|---|---|
| WP1 | Decision record, repository, knowledge-base schema, service skeleton | Levent | 6–7 |
| WP2 | Ingredient dictionary v0: E-numbers, OFF taxonomy (Turkish), CTD vocabulary; reviewed Turkish aliases | Ozan | 6–9 |
| WP3 | Condition list, guideline sources, rule table with two-person review; licence inventory | Hilal (review: Levent, Ozan) | 6–12 |
| WP4 | Matching pipeline (split, type, exact, fuzzy, Qdrant) and the 100-phrase matching test | Ozan, Levent | 7–13 |
| WP5 | Mobile app: OCR capture and correction, profile, result screen with sources and coverage; LLM message layer | Ozan (app), Levent (LLM, integration) | 8–14 |
| WP6 | Rule test (20 scenarios), measurements, interim and final reports, TÜBİTAK 2209-A application | All (coordination: Levent) | 8–14 |

Spring semester (CSE 492): wider condition coverage, curation tools, same-category alternatives, user study.

## 8. Expected Outputs and Risks
**Expected outputs**
A working mobile prototype that reads real Turkish labels and returns explained, source-cited results for diet-relevant conditions; the knowledge base (dictionary, rule table, evidence links, source inventory); the matching and rule test sets with measured results; the repository with documentation; interim and final reports; a TÜBİTAK 2209-A application.

**Risks**

| Risk | Likelihood | Impact | Mitigation plan |
|---|---|---|---|
| OCR errors on curved or glossy packages | High | Medium | User correction step; fuzzy matching; library chosen on real labels |
| Turkish terms missing from dictionaries | High | Medium | E-number bridge; reviewed team aliases; vector fallback with threshold; "could not verify" |
| Guideline misread without a clinician | Medium | High | Two independent reviewers per rule; source section stored; claim limited to guideline conformity |
| LLM message adds or changes facts | Medium | High | Structured input only; output checker; template fallback |
| Vector search adds little over dictionary | Medium | Low | Measured result is reported either way; component can be removed |
| Data licences (FooDB, OFF) | Medium | Medium | FooDB excluded; OFF used with attribution; source inventory |
| Medical-device boundary [16] | Low | High | Informational wording, no diagnosis or treatment claims, in-app disclaimer |

## 9. References
[1] Türk Gıda Kodeksi Gıda Etiketleme ve Tüketicileri Bilgilendirme Yönetmeliği, Resmî Gazete 29960 (mükerrer), 26.01.2017.
[2] Yuka, help centre, https://help.yuka.io
[3] Fig, https://foodisgood.com/
[4] Fooducate, https://www.fooducate.com/
[5] Ürün Dedektörü, https://urundedektoru.com/
[6] A. P. Davis et al., "Comparative Toxicogenomics Database's 20th anniversary: update 2025," Nucleic Acids Research, vol. 53, no. D1, pp. D1328–D1334, 2025.
[7] WHO, JECFA evaluations database, https://apps.who.int/food-additives-contaminants-jecfa-database/
[8] M. Sung, H. Jeon, J. Lee and J. Kang, "Biomedical Entity Representations with Synonym Marginalization," in Proc. 58th Annual Meeting of the ACL, 2020, pp. 3641–3650.
[9] F. Liu, E. Shareghi, Z. Meng, M. Basaldella and N. Collier, "Self-Alignment Pretraining for Biomedical Entity Representations," in Proc. NAACL-HLT, 2021, pp. 4228–4238.
[10] Türk Gıda Kodeksi Gıda Katkı Maddeleri Yönetmeliği, Resmî Gazete 28693, 30.06.2013 (with later amendments).
[11] Open Food Facts, ingredients taxonomy (taxonomies/food/ingredients.txt), github.com/openfoodfacts/openfoodfacts-server
[12] NCBI PubChem, https://pubchem.ncbi.nlm.nih.gov/
[13] American Diabetes Association Professional Practice Committee, "5. Facilitating Positive Health Behaviors and Well-being to Improve Health Outcomes: Standards of Care in Diabetes—2026," Diabetes Care, vol. 49, suppl. 1, pp. S89–S131, 2026, doi:10.2337/dc26-S005.
[14] KDIGO CKD Work Group, "KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease," Kidney International, vol. 105, no. 4S, pp. S117–S314, 2024, doi:10.1016/j.kint.2023.10.018.
[15] FooDB Version 1.0, licence statement (CC BY-NC 4.0), https://foodb.ca/
[16] Tıbbi Cihaz Yönetmeliği, Resmî Gazete 31499 (mükerrer), 02.06.2021; Regulation (EU) 2017/745.
