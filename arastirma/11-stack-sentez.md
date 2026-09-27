---
title: Stack sentezi — ekiple tartışma için öneri
updated: 2026-09-25
durum: ÖNERİ — ekip onayı bekliyor (onaylananlar plan/kararlar.md'ye ADR-006+ olarak girer)
dayanak: 10-stack-arayuz.md · 10-stack-backend-ai.md · 10-stack-hosting-ops.md · 09-evren-ve-board-notu.md
---
# Stack sentezi

## Tek bakışta
| Katman | Öneri | Güçlü alternatif | Karar tipi |
|---|---|---|---|
| Dil / çatı | Java 25 LTS · Spring Boot 4.1 · Spring Modulith 2.1 · Gradle 9 (Kotlin DSL) | Maven 3.9 | Net |
| Planlama motoru | OR-Tools 9.15 CP-SAT, **Java içinde**; Python yalnız E1 araştırması (parite testiyle) | Ayrı Python servisi · Timefold | Net |
| LLM | Spring AI 2.0 · uygulama içi Model Gateway · **EVREN birincil**, bulut yedek (yalnız yer tutuculu metin, tek bayrakla kapanır) | Bulut birincil | D0 denemesine bağlı (15 Kas kapısı) |
| Veri | PostgreSQL 18 + pgvector · modül bazlı Flyway · JSONB karar kaydı · hash zincirli append-only audit · uygulama filtresi + RLS | — | Net |
| Kimlik | Keycloak 26 (self-host, TR) · mobilde PKCE · hane yetkisi uygulamada | Spring Authorization Server | Net |
| Mobil | Expo (React Native) + EAS · expo-camera (EAN/UPC) · expo-speech-recognition (cihazda) · expo-notifications · expo-sqlite · expo-secure-store | Angular + Ionic/Capacitor | **Tartışmalı → 2 günlük deneme** |
| Web + Admin | Vite + React · TanStack Router/Query/Table · shadcn/ui · Recharts | Angular 22 | **Tartışmalı → aynı deneme** |
| Ortak TS | OpenAPI → Orval (hook + Zod) · tasarım token'ları · `ui-core` (hüküm rozeti mantığı) | — | Net |
| Barındırma | Prod: **Radore İstanbul** (4 vCPU/8 GB/300 GB, ~29,5 USD+KDV) · DR/yedek: **Netinternet Denizli** · Docker Compose · Caddy (TLS) · SOPS+age · pgBackRest | Huawei Cloud İstanbul (yönetilen PG; fiyat doğrulanmadı) | Net (beta öncesi kurulur) |
| Geliştirme/staging | Contabo VPS + Azure for Students kredisi — **yalnız sentetik veri** | — | Net |
| Gözlem | OpenTelemetry → Grafana/Prometheus/Loki/Tempo · GlitchTip · Langfuse — beta'da ayrı 16 GB TR sunucusu | Minimum: izleme sunucusu yok | Net |
| Push / e-posta | FCM/APNs, içerik jenerik (S18) · işlem e-postası SenderTR (TR) | Kurumsal SMTP | Net |
| Test | JUnit 6 · Testcontainers 2 · ArchUnit · PIT (safety, planning) · OpenAPI sözleşme testleri (oasdiff, Schemathesis) · kendi LLM eval harness'ı | Spring Cloud Contract | Net; jqwik uyumu D0'da denenir |

## Tartışılacak noktalar
1. **Arayüz: React (Expo + Vite) mı, Angular (+ Ionic/Capacitor) mı?** Kanıt React'i hafifçe öne koyuyor (Web-Bench React %44 / Angular %40; Gemini'nin Angular'da eski idiomlara kaydığı gözlemi; Expo'nun barkod/STT/push/store olgunluğu; Ionic ticari servislerinin kapanması, PrimeNG'nin kapalı kaynağa geçmesi; ekipte React/Expo geçmişi → vekil olabilecek kişi). Angular'ın artısı: resmi MCP sunucusu, AI kural dosyası, güçlü konvansiyon, arayüz sahibinin tercihi. **Öneri:** arayüz sahibi proposal'dan önce (en erken hemen, en geç ~10 Ekim; proposal'ın teknoloji tablosu buna bağlı) 2 gün, aynı iki ekranı (barkod → ürün kartı + hüküm rozeti; Pareto grafiği + kaydırıcı) iki stack'te Antigravity ile yazar, sonuç ölçülür; veri Angular'ı gösterirse alternatif ADR hazır. Antigravity'de kritik ekranlar için Claude Opus modeline geçilebiliyorsa bu, stack'ten bağımsız en ucuz risk azaltma.
2. **EVREN birincil mi?** Resmi sayfada (Chrome, 25 Eyl) model filosunda "araç kullanımı" etiketi var (glm-5.3, deepseek-v4.1-flash, gemma-4-31b, qwen3.8) ama Türkçe doğruluğu ölçülmedi; SLA yok, 1 Kasım sonrası fiyat ve kullanım şartları bilinmiyor, hesap e-Devlet ile tek kişiye bağlı. **Öneri:** 1 Kasım'dan önce ~1 günlük deneme (tool-call doğruluğu, p95, gömme boyutu, şartlar); 15 Kasım kapısında kesinleşir.
3. **Beta bütçesi:** tam kurulum ≈ 3.650 TL/ay, minimum ≈ 2.430 TL/ay (Nisan–Haziran 2027). Kim öder, fatura kimin adına (veri sorumlusu sorusuyla bağlantılı)?
4. **Google Play hesabı:** kişisel (12 test kullanıcısı × 14 gün kapalı test şartı) mı, organizasyon (muaf; D-U-N-S gerekir, doğrulanmadı) mı?
5. **Contabo VPS'in bölgesi:** Türkiye'de değil (Contabo'nun TR lokasyonu yok) → yalnız sentetik veriyle staging/demo.

## D0'da (en erken 19 Eki, en geç 1 Kas) yapılacak denemeler
EVREN (tool calling, streaming, gömme, gecikme, şartlar; en geç 1 Kas — ücretsiz dönem) · Boot 4.1 + Spring AI 2.0 + Modulith iskeleti · OR-Tools native Docker imajı · jqwik/PIT + JUnit 6 uyumu · Expo barkod gecikmesi + cihazda Türkçe STT.
