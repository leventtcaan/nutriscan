---
title: NutriScan backlog özeti (üretildi — elle düzenleme)
updated: 2026-09-28
kaynak: plan/board/pbi.yaml + plan/takvim.md
---
# Backlog özeti

8 epic · 65 feature · 66 PBI (54 promptlu). PBI'a bölünmemiş feature'lar sırası gelince bölünür (sprint planlamadan önce).

## Hazırlık
| PBI | İş | Sahip | Agent | Effort | Bağlı | En geç |
|---|---|---|---|---|---|---|
| A0.1-a | Takvim v1.5 + çalışma akışı + vekil tablosu ekip onayı | Ekip | insan | 1 | — | 30 Eylül |
| A0.2-a | Ekip hanelerinde fiş + "bitti/attım" kaydı başlasın | Ekip | insan | 1 | — | 5 Ekim |
| A0.4-a | EVREN hesabı + API anahtarı (kasaya) | Levent | insan | 1 | — | 10 Ekim |
| A0.5-a | Proposal eksikleri + ekip okuması | Ekip | insan | 2 | — | 9 Ekim |
| A0.6-a | Tarif şeması v0 (JSON Schema) + 3 örnek tarif | Ozan | antigravity | 3 | A0.9-a | 16 Ekim |
| A0.6-b | Malzeme sözlüğü v0 (~150) + alerjen ontolojisi taslağı | Ozan | antigravity | 5 | A0.6-a | 16 Ekim |
| A0.9-a | GitHub private repo (Pro) + koruma + collaborator'lar | Levent | insan | 1 | — | 10 Ekim |
| A0.9-b | Azure Boards (Scrum) + GitHub bağlantısı + backlog içe aktarımı | Levent | insan | 2 | A0.9-a | 12 Ekim |
| A1.1-a | Kök AGENTS.md v1 + docs/anayasa.md | Levent | claude-code | 3 | A0.9-a | 18 Ekim |
| A1.2-d | Board senkronu — dal/PR olaylarıyla Azure Boards durum geçişleri + yapılandırma yoksa PR'a aksiyon listesi | Hilal | codex | 2 | A0.9-b | 29 Ekim |
| A1.3-a | Backend iskeleti — Gradle 9 + Boot 4.1 + Modulith, boş modüller, verify yeşil | Levent | claude-code | 3 | A0.9-a | 18 Ekim |
| A1.6-a | OpenAPI sözleşme iskeleti + sözleşme testi | Levent | claude-code | 2 | A1.3-a | 18 Ekim |

Yük (Effort): Hilal 5 · Levent 15 · Ozan 11

## Sprint 0
| PBI | İş | Sahip | Agent | Effort | Bağlı | En geç |
|---|---|---|---|---|---|---|
| A1.1-b | Modül AGENTS.md/CLAUDE.md iskeletleri + CODEOWNERS | Levent | claude-code | 2 | A1.1-a, A1.3-a | 29 Ekim |
| A1.1-c | ci-guard — talimat dosyası ve skill yapısı denetimi | Levent | claude-code | 2 | A1.1-b | 29 Ekim |
| A1.2-a | CI — backend (build/test, Modulith verify, ArchUnit, Spotless, coverage) | Hilal | codex | 3 | A1.3-a | 29 Ekim |
| A1.2-b | CI — apps + contracts + gizli bilgi (ESLint/Prettier, oasdiff, istemci güncel mi, gitleaks) | Levent | claude-code | 2 | A1.6-a, A1.6-b | 29 Ekim |
| A1.2-c | CI — veri doğrulayıcıları (şema, sözlük üyeliği, alerjen kapanışı, sağlık kuralı kaynağı) | Hilal | codex | 3 | A0.6-b, A1.12-a | 29 Ekim |
| A1.3-b | Veritabanı — PostgreSQL 18 + pgvector, Flyway (modül başına klasör), Testcontainers, compose dev | Hilal | codex | 3 | A1.3-a | 29 Ekim |
| A1.4-a | Karar kaydı (Decision Record) şeması + audit modülü (append-only) | Levent | claude-code | 5 | A1.3-b | 1 Kasım |
| A1.5-a | Sentetik hane üreteci (alerjen + sağlık durumu + bütçe) | Hilal | codex | 3 | A0.6-b | 1 Kasım |
| A1.5-b | Git'te seed verisi + tek komutla yerel DB + ortak staging DB (sentetik) | Hilal | codex | 2 | A1.3-b, A1.5-a | 1 Kasım |
| A1.6-b | Orval ile üretilmiş TS istemcisi + pnpm workspace | Ozan | antigravity | 2 | A1.6-a | 25 Ekim |
| A1.7-a | Mobil iskelet — Expo, 5 sekme, tasarım token'ları | Ozan | antigravity | 3 | A1.6-b | 1 Kasım |
| A1.7-b | ui-core — hüküm rozeti + kesin kısıt / sağlık durumu / hedef çipleri (ortak paket) | Ozan | antigravity | 2 | A1.6-b | 1 Kasım |
| A1.8-a | Walking skeleton — backend ping (sürüm + DB), yerelde; staging hazır olunca orada | Levent | claude-code | 1 | A1.3-b, A1.6-a | 1 Kasım |
| A1.8-b | Walking skeleton — mobil ekranda sunucu durumu + uçtan uca smoke testi | Ozan | antigravity | 2 | A1.7-a, A1.8-a | 1 Kasım |
| A1.9-a | EVREN denemesi — Türkçe tool-call, p95, gömme, şartlar (rapor) | Levent | claude-code | 3 | A0.4-a | 30 Ekim (ücretsiz dönem) |
| A1.10-a | OR-Tools CP-SAT (Java) Docker imajında + küçük MSM örneği | Levent | claude-code | 2 | A1.3-a | 1 Kasım |
| A1.10-b | Test araçları uyumu — JUnit 6, jqwik (property), PIT (mutation) | Hilal | codex | 1 | A1.3-a | 1 Kasım |
| A1.12-a | Sağlık durumu kuralı şeması (data/schemas/health-rule.schema.json) | Hilal | codex | 2 | A0.6-b | 25 Ekim |
| A1.12-b | Eşik tablosu v0 — kaynak derleme (4 durum) | Ozan | antigravity | 5 | A1.12-a | 1 Kasım |

Yük (Effort): Hilal 17 · Levent 17 · Ozan 14

## Sprint 2
| PBI | İş | Sahip | Agent | Effort | Bağlı | En geç |
|---|---|---|---|---|---|---|
| A1.1-d | sprint-report betiği (board → Meeting Record taslağı) | Levent | claude-code | 2 | A0.9-b | 27 Kasım |
| A2.2-c | Rıza — aydınlatma + açık rıza ayrı, geri alma, veri indir, hesap silme (anahtar imhası) | Hilal | codex | 3 | A2.2-b | 20 Kasım |
| A2.2-d | Mobil — hane kurma + rıza ekranları (M02, M03) | Ozan | antigravity | 3 | A2.2-b, A1.7-b | 20 Kasım |
| A2.3-a | Kural motoru çekirdeği — 4 durum, alerjen eşleme, Doğrulanamadı ilkesi | Hilal | codex | 5 | A0.6-b, A1.4-a, A2.2-b | 27 Kasım |
| A2.3-b | Alerjen altın set v1 (n ≥ 200) + CI regresyonu (FN = 0) | Hilal | codex | 3 | A2.3-a | 27 Kasım |
| A2.5-b | Tarif 31–60 + Migros fiyatlı SKU kapsaması ≥ %90 | Ozan | antigravity | 5 | A2.5-a, A2.4-a | 27 Kasım |
| A2.5-c | Tarif ve sözlük çift onayı (60 tarif) | Hilal | insan | 2 | A2.5-a | 27 Kasım |
| A2.7-b | MSM çözücü v0 — CP-SAT modeli sentetik veriyle (önce güvenlik sıralı amaç) | Levent | claude-code | 5 | A2.7-a, A1.10-a, A1.5-a | 4 Aralık |
| A2.8-c | Mobil raf ekranı — hane şeridi + Neden? (M09, M10, M22) | Ozan | antigravity | 5 | A2.8-a, A1.7-b | 9 Aralık |
| A2.10-a | Gizlilik Kapısı v0 — tek çıkış, hassaslık sözlüğü, tipli yer tutucu, Türkçe ek uyumlu geri doldurma | Levent | claude-code | 5 | A1.4-a | 9 Aralık |

Yük (Effort): Hilal 13 · Levent 12 · Ozan 13

## Sprint 1
| PBI | İş | Sahip | Agent | Effort | Bağlı | En geç |
|---|---|---|---|---|---|---|
| A1.4-b | Log/metrik/iz şeması + "sağlık verisi logda yok" kanarya testi | Levent | claude-code | 3 | A1.3-a | 13 Kasım |
| A1.11-a | Contabo sunucu — Docker Compose staging, Caddy TLS, SOPS sırlar, yedek | Levent | claude-code | 3 | A0.9-a | 13 Kasım |
| A2.8-a | Expo barkod gecikmesi + cihazda Türkçe konuşma tanıma denemesi | Ozan | antigravity | 2 | A1.7-a | 9 Aralık |
| A2.12-a | Web + admin iskeleti (Vite + React, TanStack Router/Query, shadcn/ui) | Ozan | antigravity | 3 | A1.6-b, A1.7-b | 16 Aralık |
| A2.1-a | CSE 491 ara rapor + ara sunum | Ekip | insan | 2 | — | 6 Kasım |
| A2.2-a | Kimlik — Keycloak realm + Spring Security resource server (OAuth2 PKCE, roller) | Hilal | codex | 3 | A1.3-b | 20 Kasım |
| A2.2-b | Hane + üye + davet + veli onayı + profil sürümü (API + tablolar) | Hilal | codex | 5 | A2.2-a, A1.4-a | 20 Kasım |
| A2.4-a | Katalog v0 — ürün/SKU/paket/fiyat + fiyat yaşı, Migros içe aktarma | Hilal | codex | 3 | A0.6-b, A1.5-b | 20 Kasım |
| A2.4-b | Migros fiyat turu #1 (~300 ürün, üç kişiye bölünür) | Ekip | insan | 1 | — | 20 Kasım |
| A2.5-a | İlk 30 tarif (şemaya uygun, malzemeler sözlükte) | Ozan | antigravity | 5 | A0.6-a, A0.6-b | 15 Kasım |
| A2.6-a | TR model karar kapısı — EVREN birincil mi (ADR-009 kesinleşir) | Levent | insan | 1 | A1.9-a | 15 Kasım |
| A2.7-a | Motor sözleşmesi — PlanRequest/PlanResult şeması + golden fixture'lar | Levent | claude-code | 2 | A1.6-a | 4 Aralık |

Yük (Effort): Hilal 13 · Levent 11 · Ozan 12

## Sprint 3
| PBI | İş | Sahip | Agent | Effort | Bağlı | En geç |
|---|---|---|---|---|---|---|
| A2.3-c | safety.api — EligibilityService (planlamaya uygun aday kümesi) | Hilal | codex | 2 | A2.3-a | 2 Aralık |
| A2.16-a | Sağlık durumu kuralları kural motorunda + test seti (%100 tablo uyumu) | Hilal | codex | 3 | A1.12-b, A2.3-a | 9 Aralık |
| A2.7-c | MSM gerçek veriyle (60 tarif + Migros) + E1 v0 ölçümü | Levent | claude-code | 3 | A2.7-b, A2.5-b, A2.3-c, A2.4-a | 4 Aralık |
| A2.8-b | Raf API — barkod → üye başına karar + alternatif (p95 ≤ 1,5 sn) | Hilal | codex | 3 | A2.2-b, A2.3-a, A2.4-a | 9 Aralık |
| A2.9-a | Akıllı Takas API — k = 1·3·5, zorunlu değişiklik ayrı, olursuzluk açıklaması | Levent | claude-code | 3 | A2.7-b | 9 Aralık |
| A2.9-b | Mobil liste + takas ekranları (M04, M06–M08) | Ozan | antigravity | 3 | A2.9-a | 9 Aralık |
| A2.11-a | Asistan v1 — araç kataloğu + orkestrasyon (3–5 iş akışı niyeti) | Levent | claude-code | 5 | A2.8-b, A2.9-a, A2.10-a | 16 Aralık |
| A2.12-b | Admin backend — karar izi okuma, katalog onayı (gerekçe + etki analizi), audit görünümü | Hilal | codex | 5 | A1.4-a, A2.3-a, A2.4-a | 16 Aralık |
| A2.12-c | Admin arayüzü — karar izi, katalog moderasyonu, audit, Sözleşme panosu (A01–A03) | Ozan | antigravity | 5 | A2.12-a, A2.12-b | 16 Aralık |

Yük (Effort): Hilal 13 · Levent 11 · Ozan 8

## Sprint 4
| PBI | İş | Sahip | Agent | Effort | Bağlı | En geç |
|---|---|---|---|---|---|---|
| A2.11-b | Mobil asistan ekranı — adımlar görünür, hüküm rozeti karar kaydından (M16, M21) | Ozan | antigravity | 3 | A2.11-a | 16 Aralık |
| A2.13-a | E2 ilk koşu — yalnız-LLM planlayıcı vs NutriScan (50 senaryo) | Levent | claude-code | 3 | A2.7-c, A2.11-a, A1.5-a | 18 Aralık |
| A2.14-a | CSE 491 final raporu + çalışan prototip demosu | Ekip | insan | 3 | — | ~18 Aralık ⚠️ teyit |
| A2.15-a | Yük dengesi ve bileşen sahipliği değerlendirmesi | Ekip | insan | 1 | — | 18 Aralık |

Yük (Effort): Hilal 2 · Levent 5 · Ozan 5

## Henüz PBI'a bölünmemiş feature'lar
A0.3, A0.7, A0.8, A3.1, A3.2, A3.3, A3.4, A3.5, A3.6, A3.7, A4.1, A4.2, A4.3, A4.4, A4.5, A4.6, A4.7, A4.8, A4.9, A4.10, A5.1, A5.2, A5.3, A5.4, A6.1, A6.2, A6.3, A7.1, A7.2, A7.3, A7.4

## Kontrol uyarıları
- Sprint 0 · Hilal: 17 Effort > 14
