# ADR-013 · Ortak altyapı: depo = planlama klasörü, tek talimat dosyası, ortak skill'ler, dosyada hafıza

**Tarih / onay:** 2026-09-28, Levent (ürün sahibi) onayıyla kuruldu; ekip onayı A0.1 ile — ÖNERİ

- **Ne:**
  1. **Tek klasör = tek depo:** planlama klasörü (`plan/`, `arastirma/`, `docs/`, `kaynak/`, `toplanti/`) ve ileride kod aynı private GitHub deposunda. Hafıza depoda: `DURUM.md` (ortak "şu an", ≤60 satır), `oturumlar/<kişi>.md` (kişi başı, yalnız sona eklenir), kararlar `plan/kararlar/ADR-0NN-*.md` (her karar ayrı dosya), işler `plan/board/pbi.yaml` → Azure Boards.
  2. **Tek talimat dosyası:** `AGENTS.md` (yönlendirici, ≤150 satır, <24 KB). Codex ve Antigravity doğrudan okur; Claude Code `CLAUDE.md` = `@AGENTS.md` importuyla. Değişmez kurallar `docs/anayasa.md`'de. Kişisel katman depo dışında: `CLAUDE.local.md` (gitignore), `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`.
  3. **Ortak skill'ler** `.agents/skills/` (Codex ve Antigravity okur), Claude için `.claude/skills/` symlink: `pbi-baslat`, `pbi-kapat`, `pr-incele`, `karar-yaz`, `tarif-ekle`, `arayuz-tasarim` + dışarıdan alınan `frontend-design` (Anthropic, Apache-2.0), `expo-design-system`, `expo-native-ui` (Expo, MIT; dışarı geri bildirim gönderen bölüm çıkarıldı — `VENDOR.md`).
  4. **Azure Boards MCP:** yerel `@azure-devops/mcp` (sürüm sabit) + kişisel PAT (yalnız okuma); `.mcp.json` (Claude), `.codex/config.toml` (Codex), Antigravity kişisel config. Board değişikliği yalnız `pbi.yaml` PR'ı + betik.
  5. **Git:** `main` korumalı, PR + sahip/vekil onayı; commit/PR'da AI imzası yok, AI kullanımı PR'da beyan edilir (`.claude/settings.json` attribution kapalı).
- **Neden:** üç kişi, üç farklı agent, çok sayıda oturum: kural bir kez yazılmazsa ve hafıza dosyada durmazsa ekip kopar, agent'lar farklı gerçeklerle çalışır. Bu desen ekipteki başka bir projede (CSE 481) denendi. Claude Code 2.1.183 AGENTS.md'yi doğrudan okumuyor → import şart (ADR-004'teki "kökte CLAUDE.md yok" varsayımı bununla düzeltildi). Antigravity'nin `AGENTS.md` ve `.agents/skills` okuduğu resmî dokümanda doğrulandı (28 Eyl).
- **Alternatif:** (a) kod için ayrı depo, planlama Levent'in klasöründe · (b) araç başına ayrı talimat dosyaları (`GEMINI.md`, `.agents/rules`, `CLAUDE.md` içerikli) · (c) Azure uzak MCP sunucusu. **Neden değil:** (a) planlama ve hafıza ekipten kopar, iki gerçek oluşur · (b) kopyalar kayar, hangisinin doğru olduğu belirsizleşir · (c) kişisel Microsoft hesaplı organizasyonları desteklemiyor (Microsoft Learn, 21 Eyl 2026).
- **Geri dönmenin maliyeti:** düşük–orta: dosya yapısı taşınabilir; talimat/skill yapısı araç sürümleri değiştikçe güncellenir.
- **Açık:** Azure MCP + PAT kişisel hesapla denenmedi (AB#128) · üç araçta yüklemenin denenerek doğrulanması (AB#131) · ci-guard (AB#133).
