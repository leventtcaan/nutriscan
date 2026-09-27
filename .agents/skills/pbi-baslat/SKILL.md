---
name: pbi-baslat
description: NutriScan'de bir PBI'a (Azure Boards iş öğesi, AB#numara ya da A1.3-a gibi takvim kimliği) başlarken kullan. Oturum açılışını yapar, PBI'ın promptunu ve kabul kriterlerini okur, kapsamı ve bağımlılıkları doğrular, önce plan + test listesi çıkarır. "AB#143'e başla", "A1.4-a'yı al", "oturumu aç" dendiğinde.
---
# PBI başlat

Amaç: her agent (Claude Code, Codex, Antigravity) bir işe aynı şekilde başlasın; bağlam sohbetten değil dosyadan gelsin.

## Adımlar
1. **Kim olduğunu belirle.** Kişisel katmandan (Levent: `CLAUDE.local.md` · Hilal: `~/.codex/AGENTS.md` · Ozan: `~/.gemini/GEMINI.md`) ya da git kullanıcı adından. Belirsizse sor.
2. **Oturum açılışı:** `DURUM.md` + `oturumlar/<kişi>.md` son 3 girdi. `git pull`.
3. **PBI'ı bul.** Sırayla:
   - `plan/board/azure-idler.yaml` → AB# ↔ takvim kimliği eşlemesi.
   - Prompt: `plan/board/promptlar/<ID>.md` (board'daki PBI açıklamasıyla aynı metin).
   - Kabul kriterleri ve bağımlılıklar: `plan/board/pbi.yaml` içindeki kayıt.
   - Azure DevOps MCP bağlıysa (`ado`), iş öğesini oradan da oku; durum (New/Approved/Committed) ve yorumlar oradadır.
4. **Hazır mı? (DoR, `plan/calisma-akisi.md` §4)** Aşağıdakilerden biri eksikse **dur ve söyle**, kod yazma:
   - Kabul kriteri yok ya da test edilemez.
   - `bagli` listesindeki bir PBI bitmemiş **ve** kullanılabilir sözleşme/fixture/mock yok.
   - İş, promptun "Değiştirebileceğin yer" dışına taşıyor (→ `contract-change` gerekir).
5. **Plan çıkar (kod yok):** değişecek dosyalar, yazılacak testler (her kabul kriterine en az bir test), ilgili anayasa maddeleri (`docs/anayasa.md`), açık sorular. 5–10 madde. İnsan onaylamadan uygulamaya geçme.
6. **Dalı aç:** `<modül>/AB<numara>-<kısa-ad>` (promptun "Teslim" bölümünde yazılı). Board'da PBI'ı Committed yapmayı insana hatırlat.
7. **Uygularken:** önce test, sonra kod. Bilmediğin sürüm/API/eşik/kaynak uydurulmaz; doğrula ya da `[..]` bırak ve söyle. Hardcode yok: eşik, tarih, kimlik ve parametre yapılandırmadan gelir.

## Çıktı (kullanıcıya)
- PBI özeti (1 cümle) · hazır mı (evet/hayır + neden) · plan · ilk komut.
