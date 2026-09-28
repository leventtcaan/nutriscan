# Oturum günlüğü — Levent (Claude Code)

> Her oturumun sonunda en alta bir girdi eklenir; yalnız sona eklenir, eski girdi düzenlenmez.
> Oturum başında son 3 girdi okunur (AGENTS.md › Oturum protokolü).

<!-- Girdi biçimi:
## YYYY-AA-GG · AB#<no> kısa başlık
- yaptım:     …
- karar:      … (ADR-0NN) | yok
- takıldım:   …
- sıradaki:   …
- AI:         araç · ne için · hangi kısmı insan yazdı/karar verdi
-->

## 2026-09-24 → 2026-09-27 · depo öncesi tarihçe (komuta merkezi; eski DURUM.md'den taşındı)
- yaptım:     Faz 0 kontekst; 4 tur araştırma (arastirma/01, 02, 05, 06, 08, 09, 10) · tez v1→v5 (onaylı), v5.1 (ADR-011:
              sağlık durumu profili, önce güvenlik, RAG yalnız eşleme/alıntı) · ürün tanımı v5.1 (29 FR + 12 NFR) ·
              proposal v0 (6 sayfa, docx/PDF betikle) · prototip v1 → Version 9 · ADR-001…012 · takvim v1.1 → v1.5 ·
              çalışma akışı standardı · 65 PBI + 53 prompt · Azure Boards kurulumu (159 öğe, doğrulama 0 fark) · ekip mesajları
- karar:      ADR-001…012
- takıldım:   Scrum süreç geçişi organizasyon yetkisi istedi (Hilal yaptı)
- sıradaki:   ortak depo altyapısı (ADR-013), GitHub repo + Azure bağlantısı
- AI:         Claude Code (komuta merkezi): araştırma ajanları, taslaklar, betikler, board yüklemesi; kararlar Levent'in

## 2026-09-28 · AB#140 Backend iskeleti (A1.3-a)
- yaptım:     backend/ iskeleti (Java 25, Boot 4.1.1, Modulith 2.1.1, Gradle 9.8.0 wrapper SHA-256 pinli), 13 modül + açık
              allowedDependencies, 3 test (verify, modül listesi, sürüm kataloğu); negatif kanıt (sınır bozulunca build kırmızı);
              PR #2 (vekil Hilal). Proje aktarımı + Apple Notes: 00 · Oryantasyon (O·1–3), 05 · Kod (U·1).
- karar:      ADR-014 modül sınırları (ÖNERİ) · kişisel katman: TODO(human) kalktı, aktarım protokolü geldi (CLAUDE.local.md)
- takıldım:   ado MCP 401 (PAT) · §8'de shared satırı yoktu (eklendi) · Gradle yalnız Homebrew'la (OpenJDK 27 de geldi)
- sıradaki:   PR #2 incelemesi (Hilal) → merge sonrası kök AGENTS.md › Komutlar'a `cd backend && ./gradlew build`; PAT yenile
- AI:         Claude Code · sürüm doğrulama, bütün kod/test, aktarım ve notlar · Levent: kök paket, tek proje, kurulum, onay
