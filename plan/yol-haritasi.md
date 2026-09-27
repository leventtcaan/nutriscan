---
title: NutriScan — Ana Yol Haritası
updated: 2026-09-27
---
# NutriScan — Ana Yol Haritası

> ⏰ **SERT TARİH: CSE 491 Project Proposal — 18 Ekim 2026 (Pazar) — MS Teams** (Hafta 5 = 12–16 Eki; Levent doğruladı).
> Şablon: `kaynak/CSE491_Project_Proposal_Template.docx` (4–6 sayfa, danışmanla birlikte hazırlanır, onay imzası var).
> Proposal = Faz 1+2+3'ün ürünü: problem/motivasyon, hedef+kapsam dışı+ölçülebilir başarı kriteri, benzer sistemler tablosu,
> FR/NFR (must/should/could), teknoloji tablosu + gerekçe + mimari diyagram, üye bazlı iş paketleri (WP1–6), risk tablosu, IEEE/APA kaynakça.
> → Faz 1–3 proposal'a kadar sıkıştırılır; UX ve ekip standartları paralel yürür.

> Sıra kuralı: araştır → netleştir (Levent) → karar (`kararlar.md`) → yaz. Faz atlanmaz.
> Her faz sonunda: DURUM.md güncelle · Apple Notes/NutriScan'e not · LeventOS daily'ye tek satır.

| Faz | Ne | Çıktı | Durum |
|---|---|---|---|
| 0 | Kontekst aktarımı + eski repo (sadece fikir için) okuma | Levent'in anlatımı hafızada | ✅ 2026-09-24 |
| 1 | Problem & fizibilite araştırması → tez v5 (v5.1: 27 Eyl) | `arastirma/07-tez-v5.md`, ADR-001, ADR-011 | ✅ 2026-09-24 · v5.1 2026-09-27 |
| 2 | Ürün tanımı: problem cümlesi, persona, değer önerisi, özgünlük iddiası, feature listesi (MoSCoW), MVP sınırı, optimizasyon modülü | `plan/urun-tanimi.md` · danışman sunumu #1 | 🟡 taslak v5.1 (27 Eyl) + proposal v0 → 2 Ekim görüşmesi |
| 3 | Tech stack & mimari: Spring Boot 4.1, React (Expo + Vite), Contabo, EVREN, logging/observability/admin | `plan/kararlar.md` (ADR-006…010) · mimari diyagram | ✅ 2026-09-25 (mimari diyagram proposal sonrası) |
| 4 | UX: kullanıcı akışları, wireframe, tıklanabilir prototip, mini kullanıcı testi | prototip linki | 🟡 prototip v1 + v5.1 güncellemesi (Version 9, 27 Eyl); kullanıcı testi yok |
| 5 | Ekip & AI çalışma standardı: repo yapısı, ortak agent talimatları (Claude Code/Codex/Antigravity), kod standartları, branch/PR/CI kuralları | kök `AGENTS.md` + `.claude/rules` (kökte CLAUDE.md yok) · board: Azure Boards (ADR-005) | — (takvim A1.1–A1.2, ayrı oturum) |
| 6 | Backlog + sprint planı + iş bölümü + danışman raporlama ritmi | board dolu, sprint 1 hazır | — |
| 7 | Implementasyon sprintleri → test → canlıya alma → gözlem | çalışan ürün | — |
| 8 | Final rapor, sunum, demo | teslim | — |
