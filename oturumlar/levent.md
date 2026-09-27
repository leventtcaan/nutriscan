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
