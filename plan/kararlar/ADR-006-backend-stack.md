# ADR-006 · Backend stack

**Tarih / onay:** 2026-09-25, ekip

- **Ne:** Java 25 LTS · Spring Boot 4.1 · Spring Modulith 2.1 · Gradle 9 (Kotlin DSL) · Spring AI 2.0 · OR-Tools CP-SAT (Java içinde; Python yalnız E1 araştırması, parite testiyle) · PostgreSQL 18 + pgvector · Keycloak (self-host) · JUnit 6 + Testcontainers + ArchUnit + PIT + OpenAPI sözleşme testleri.
- **Neden:** Boot 4.1'in açık kaynak desteği Temmuz 2027'ye kadar (Haziran 2027 kapanışını kapsayan tek sürüm; 3.5 Haz 2026'da, 4.0 Ara 2026'da bitiyor); Spring AI 2.0 Boot 4 istiyor; CP-SAT optimallik boşluğu verir (E1'in sorusu). Ayrıntı `arastirma/10-stack-backend-ai.md`.
- **Alternatif:** Boot 3.5 + Spring AI 1.x · Timefold · ayrı Python servisi · Maven. **Neden değil:** destek süresi · optimallik kanıtı yok · ek servis/ops yükü · Gradle'ın test ayrımı (Maven de kabul edilebilir, kritik değil).
