---
title: İlk açılış — depoyu ilk kez açan herkes için
updated: 2026-09-28
okuyan: Levent, Hilal, Ozan (insan). Agent'lar kuralı AGENTS.md'den alır.
---
# İlk açılış

Amaç: üç farklı agent'la (Claude Code, Codex, Antigravity) çalışan üç kişi aynı kurallardan, aynı hafızadan ve aynı
iş listesinden başlasın. Hafıza sohbette değil bu depodadır: `DURUM.md` (şu an), `oturumlar/<kişi>.md` (senin
tarihçen), `plan/` (plan, kararlar, board), `docs/anayasa.md` (değişmez kurallar).

## 1. Bir kere yapılacak kurulum (~15 dk)
1. **Depoyu klonla:** `gh repo clone leventtcaan/nutriscan` (davet e-postasını kabul ettikten sonra).
2. **Kişisel katmanını kur** (depoya girmez; yalnız sana özgü tercihler — proje kuralı yazma):
   | Kişi | Araç | Dosya | İçine yazılacak (öneri) |
   |---|---|---|---|
   | Levent | Claude Code | `CLAUDE.local.md` (depo kökünde, gitignore) | hazır |
   | Hilal | Codex | `~/.codex/AGENTS.md` | "Ben Hilal. NutriScan'de oturum günlüğüm `oturumlar/hilal.md`. Sahip olduğum modüller: safety, household/identity/consent, catalog, pantry, recommendation, admin backend, data/allergens." + kendi dil/açıklama tercihin |
   | Ozan | Antigravity | `~/.gemini/GEMINI.md` | "Ben Ozan. NutriScan'de oturum günlüğüm `oturumlar/ozan.md`. Sahip olduğum modüller: apps/mobile, apps/web, apps/admin, packages/ui, data/recipes, data/dictionary, data/health-rules." + kendi tercihin |
3. **Azure Boards erişimi (MCP, salt okunur)** — *henüz denenmedi; önce Levent dener, sonucu DURUM.md'ye yazar:*
   - Azure DevOps → sağ üst kullanıcı → **Personal access tokens** → New: kapsam yalnız **Work Items: Read** ve
     **Project and Team: Read**, süre dönem sonuna kadar. Anahtar hiçbir dosyaya, sohbete, prompta yazılmaz.
   - Kabuğunda (ör. `~/.zshrc`): `export PERSONAL_ACCESS_TOKEN="$(printf '%s' '<azure-eposta>:<PAT>' | base64)"`
   - Claude Code (`.mcp.json`) ve Codex (`.codex/config.toml`) depodaki ayarı kullanır. Antigravity için aynı sunucuyu
     kendi `~/.gemini/config/mcp_config.json` dosyana ekle (depodaki `.mcp.json` ile aynı `command/args`; `env`'e anahtarı
     yazma, kabuktan gelsin — olmazsa Levent'e yaz).
   - MCP çalışmasa da iş durmaz: PBI'ın promptu depoda `plan/board/promptlar/<ID>.md`.
4. **Commit kancası (bir kez):** depo kökünde `git config core.hooksPath tools/githooks` — AI imzalı commit mesajını reddeder.
5. **Araç sürümü:** Claude Code, Codex ve Antigravity güncel olsun; skill'ler `.agents/skills/` (Claude için `.claude/skills/`).

## 2. İlk prompt (her araçta aynı; `<ad>` yerine adını yaz)
```
Ben <ad>. Bu NutriScan deposunu ilk kez açıyorum. Kod yazma, dosya değiştirme.
1) AGENTS.md, DURUM.md ve oturumlar/<ad>.md dosyalarını oku.
2) Kuralların yüklendiğini göster: AGENTS.md'deki kırmızı çizgilerden 1, 3 ve 7'yi kendi cümlelerinle söyle
   ve .agents/skills altında gördüğün skill'leri listele.
3) plan/board/backlog.md'den bana atanmış Hazırlık ve Sprint 0 PBI'larını AB# numaraları ve en geç tarihleriyle listele.
4) İlk PBI'ım için pbi-baslat skill'ini kuru çalıştır: hazır mı (DoR), eksik ne, plan ne olurdu — ama uygulama.
5) Çıktının sonuna oturumlar/<ad>.md için 5 satırlık ilk girdi taslağını yaz; onaylarsam ekle.
```
Beklenen: agent kuralları doğru anlatır, skill'leri listeler, PBI'larını doğru sayar. Biri eksikse kurulum hatalıdır —
gruba yaz, birlikte bakalım (en sık neden: araç eski sürüm ya da yanlış klasörden açıldı).

## 3. Her gün
- **Başlarken:** "Oturumu aç, AB#<no> üzerinde çalışacağım." (skill: `pbi-baslat`)
- **Biterken:** "Oturumu kapat." (skill: `pbi-kapat` → kontrol çıktısı, PR taslağı, oturum günlüğü)
- **İnceleme:** "PR #<no>'yu incele." (skill: `pr-incele`) — onay düğmesine sen basarsın, agent değil.
- **Arayüz:** her ekran işinde `arayuz-tasarim` otomatik devrede; veri işinde `tarif-ekle`.

## 4. Kısa kurallar (ayrıntı AGENTS.md)
Bir oturum = bir PBI · bir PR = bir modül · önce test · "güvenli" yok, belirsizlik → Doğrulanamadı · sayı/kaynak
uydurma yok · hardcode ve sır yok · karar alındıysa ADR · AI imzası yok, AI kullanımı PR'da beyan edilir ·
agent'ın yazdığını Cuma demosunda anlatabilecek kadar bil.
