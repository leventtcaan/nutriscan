---
title: NutriScan — Çalışma akışı standardı (board → agent → PR → danışman)
updated: 2026-09-27
durum: v1 — Levent onayı 2026-09-27 (kapasite, vekiller, takvim v1.5); ekip okuması A0.1 ile
dayanak: arastirma/08-ekip-calisma-modeli.md §3 (araştırma) · ADR-004 (sahiplik), ADR-005 (GitHub + Azure Boards), ADR-011 · plan/takvim.md v1.5
not: 08 raporundaki A/B/C hatları, GitHub Projects ve "Closes #N" bu belgeyle geçersiz; yerine isimler, Azure Boards ve AB# geçer.
---
# Çalışma akışı standardı

**Tek cümle:** Her iş board'da bir PBI olarak doğar, sahibinin agent'ına standart bir promptla verilir, tek modüllük bir PR olarak döner, CI kapılarından ve sahibin onayından geçer, Cuma günü staging'de gösterilir ve iki haftada bir Meeting Record'a otomatik olarak yazılır.

## 1. Akış (uçtan uca)
```
plan/takvim.md ──► Azure Boards
  Aşama = Epic · iş paketi (A1.3) = Feature · PBI (A1.3-a, 0,5–2 gün) · Task (gerekirse)
        │ sprint planlama (Pazartesi, 2 haftada bir)
        ▼
PBI "Approved" (DoR §4 sağlandı, promptu hazır)
        │ sahip PBI'ı "Committed" yapar, dalı açar:  <modül>/AB<id>-<kısa-ad>
        ▼
Sahibin agent'ı (Claude Code · Codex · Antigravity) — prompt: plan/board/promptlar/<ID>.md
        │ önce plan → sonra kod + test → yerelde CI komutları
        ▼
PR (tek modül, ≤400 satır, şablon dolu, "Fixes AB#<id>")
        │ CI kapıları (§6) yeşil  +  CODEOWNERS: sahip ya da vekil onayı
        ▼
squash merge → PBI otomatik "Done" → staging'e deploy (Cuma)
        │
        ▼
Cuma: danışman görüşmesi + 5 dk modül demosu ("agent'ın yazdığı kritik parçayı anlat")
        │ sprint sonu Cuması = Meeting Record teslimi
        ▼
MR formu board'dan üretilir: kapanan PBI'lar = "yapılanlar", sıradaki sprint = "yapılacaklar"
```

## 2. Board yapısı (Azure Boards, "NutriScan Scrum" süreci — `dev.azure.com/hilalhocaoglu20/NutriScan`; kuruldu 2026-09-27, ADR-012)
| Seviye | Ne | Kaynak | Örnek başlık |
|---|---|---|---|
| **Epic** | Aşama | takvim §3 başlıkları | `A1 · Temel (19 Ekim → 1 Kasım)` |
| **Feature** | İş paketi | takvim satırı (ID aynen) | `[A1.3] Backend iskeleti` |
| **PBI** | 0,5–2 günlük tek modül işi, tek PR | `plan/board/pbi.yaml` | `[A1.3-a] Gradle + Boot 4.1 + Modulith iskeleti` |
| **Task** | Yalnız insan alt işi gerekirse (hesap açma, fotoğraf çekme) | PBI içinde | `Contabo'da SSH anahtarı` |
| **Bug** | Hata; PBI gibi akar, önceliği sprint içinde en üst | — | `[BUG] …` |

- **Durumlar ve kim değiştirir (PBI/Bug):**
  | Geçiş | Ne zaman | Kim / nasıl |
  |---|---|---|
  | New → Approved | Sprint planlamada, DoR (§4) tamam | Sahip, board'da sürükler |
  | Approved → Committed | İşe başlarken (dal açılınca) | Sahip, board'da sürükler (`pbi-baslat` hatırlatır) |
  | Committed → Done | PR `main`'e girince | **Otomatik:** PR/commit gövdesinde `Fixes AB#<no>` (GitHub App bağlantısı) |
  | → Removed | Vazgeçilince (silme yok) | Sahip + gerekçe yorumu; `pbi.yaml`'da da işaretlenir |
- **Task'lar** (ekip işlerindeki kişi payları): To Do → In Progress → Done, herkes kendi payını sürükler. Tüm paylar Done olunca PBI'ın sahibi PBI'ı Done yapar.
- **Otomatik bağlantı:** commit, dal ya da PR'da `AB#<no>` geçmesi iş öğesine GitHub bağlantısı ekler; durum yalnız `Fixes` ile değişir.
- Board sütunları durumlarla birebir: Backlog items `New → Approved → Committed (WIP ≤ 6: kişi başı 2) → Done`; Feature/Epic `New → In Progress → Done`. Feature/Epic durumu elle (ilk PBI başlayınca In Progress, son PBI bitince Done).
- **Alanlar:** Area Path = modül (`NutriScan\backend\safety`, `NutriScan\apps\mobile`, `NutriScan\data` …) · Iteration = sprint (§3) · Effort = 1/2/3/5/8 · **Etiketler:** `sahip:levent|hilal|ozan`, `agent:claude-code|codex|antigravity|insan`, `omurga:motor|guvence1|guvence2|veri|zemin`, `deney:E1|E2|E3`, gerekirse `contract-change`.
- **Assigned To:** PBI'ın sahibi. Vekil yalnız sahip yokken üstlenir (board'da not düşülür).
- **Yeni PBI ekleme:** önce `pbi.yaml` → `board_uret.py` → yalnız yeni öğeler yüklenir (`azure-idler.yaml`'da olanlar atlanır); AB# numarası yaml'a değil `azure-idler.yaml`'a yazılır.
- **Kaynak kural:** tarih ve bağımlılığın tek kaynağı `plan/takvim.md`; PBI metinlerinin tek kaynağı `plan/board/pbi.yaml`. Board bunlardan üretilir (`python3 plan/board/board_uret.py` → CSV içe aktarım). Board'da elle yapılan değişiklik (durum, atama, yorum) serbest; kapsam değişikliği önce yaml'a.

## 3. Sprint ritmi
**2 haftalık sprint, Pazartesi–Pazar; sprint sonu Cuması = Meeting Record teslimi.** Görüşmeler her hafta Cuma.

| Sprint | Tarih | Aşama | Sprint sonu Cuması |
|---|---|---|---|
| Hazırlık | 28 Eyl – 18 Eki | A0 (kodsuz) | MR1 2 Eki · MR2 16 Eki |
| **Sprint 0** | 19 Eki – 1 Kas | A1 Temel | MR3 **30 Eki** |
| Sprint 1 | 2 – 15 Kas | A2 | MR4 **13 Kas** (ara rapor ~6 Kas bu sprintte) |
| Sprint 2 | 16 – 29 Kas | A2 | MR5 **27 Kas** |
| Sprint 3 | 30 Kas – 13 Ara | A2 | — (görüşme 11 Ara) |
| Sprint 4 | 14 – 27 Ara | A2 kapanış | CSE 491 final ~18 Ara |
| Kış kampı | 4 – 31 Oca | A3 | 2 sprint (S5, S6) |

| Ne | Ne zaman | Süre | Çıktı |
|---|---|---|---|
| Sprint planlama | sprint başı Pazartesi | 30 dk | Her sahip kendi modülünden PBI seçer (takvimdeki "en geç"e göre); çapraz ihtiyaçlar `contract-change` PBI'ı olur |
| Async durum | her gün | 3 satır | Grup mesajı: dün / bugün / engel. Board'daki durum güncel |
| Sözleşme günü | Çarşamba | 15–30 dk | Açık `contract-change` PR'ları karara bağlanır |
| Danışman + entegrasyon | her Cuma | görüşme + 30 dk | `main` staging'e; her sahip 5 dk demo + agent kodundan bir parçayı anlatır |
| Sprint review + retro | sprint sonu Cuma | 45 dk | Hız: PR lead time, review süresi, tamamlanan Effort; retro'dan en çok 2 aksiyon |
| Meeting Record | sprint sonu Cuma | 15 dk | `sprint-report` betiği board'dan taslak üretir; görüşmede imza, aynı gün Teams |

**Erken bitirme (çekme) kuralı:** tarihler "en geç"tir; hedef daha erken bitirmek. Sprint'teki PBI'ların bitince sonraki sprintin Approved PBI'larından (önce kritik yol, sonra kendi modülün) çekilir; board'da sprint alanı güncellenir, takvim değişmez.

**Kapasite kuralı:** sprint başına kişi başı en çok ~13 Effort; sınav haftalarında yarısı. Taşan PBI sonraki sprintin başına geçer, takvimdeki "kaçarsa" planı tetiklenir mi diye bakılır.

## 4. Hazır tanımı (DoR) — PBI "Approved" olabilmesi için
1. Tek modül, tek PR ile bitebilir; ≤2 gün.
2. Bağlı olduğu PBI'lar Done **ya da** sözleşme/fixture/mock hazır (beklemeden çalışılabilir).
3. Kabul kriterleri test edilebilir (her biri bir test ya da gözle doğrulanabilir bir çıktı).
4. Sahip ve agent belli; **prompt hazır** (`plan/board/promptlar/<ID>.md`, §7 şablonu).
5. Sözleşme etkisi yazılı: yok / eklemeli / kırıcı.
6. İlgili kurallar (S/K maddeleri) PBI'da anılmış.

## 5. Bitti tanımı (DoD) — PBI "Done"
1. Kabul kriterlerinin hepsi otomatik testle (ya da PR'da ekran görüntüsü/çıktıyla) karşılandı.
2. CI kapılarının hepsi yeşil (§6).
3. Sahip ya da vekil onayladı; sahip kendi PR'ını açtıysa diğer iki kişiden biri.
4. PR şablonu dolu; "agent'ın yazdığını okudum ve açıklayabilirim" işaretli.
5. Modülün `AGENTS.md`'si, sözleşmesi ve gerekiyorsa ADR güncel.
6. `main`'e squash merge; PBI otomatik Done; sonraki Cuma staging'de görünür.

## 6. Kod akışı kuralları (özet; ayrıntı 08 §3.c)
- **Trunk-based:** tek uzun ömürlü dal `main`. Dal adı `<modül>/AB<id>-<kısa-ad>` (ör. `safety/AB42-gluten-kurali`), ömrü ≤2 gün, her gün `main`'e rebase.
- **Commit:** Conventional Commits + iş öğesi: `feat(safety): gluten kuralı AB#42`. PR gövdesinde `Fixes AB#42` → merge'de PBI Done.
- **Bir PR = bir modül.** İki modüle dokunan PR yalnız `contract-change` etiketiyle ve iki sahibin onayıyla (08 §3.e protokolü: önce sözleşme PR'ı, sonra uygulama PR'ları).
- **Boyut:** ≤400 satır insan/agent yazımı (üretilmiş kod, lockfile, veri YAML'ı hariç); aşarsa PBI bölünür.
- **Review SLA:** 24 saat; 48 saati geçen ve sözleşmeye dokunmayan, CI'ı yeşil PR'ı herhangi bir üye onaylayabilir.
- **CI kapıları (main koruması):** build + test · Modulith `verify()` + ArchUnit (K kuralları) · lint/format · `oasdiff` + üretilmiş istemci güncel · gitleaks · veri doğrulayıcıları · değişen kodda coverage (%70; safety/privacy %90) · ci-guard (kök `CLAUDE.md` = `@AGENTS.md`, `CLAUDE.local.md`/`AGENTS.override.md` depoda yok, her modülde AGENTS.md + CLAUDE.md + CODEOWNERS, skill symlink'leri tam) · alerjen + sağlık kuralı altın set regresyonu (safety/data değişince).
- **Yasaklar:** prod verisi yerelde/agent'ta yok (K kuralı) · sır repoda yok · `CLAUDE.local.md`, `AGENTS.override.md` yok · agent'a hesap/parola verilmez.

## 7. Agent prompt standardı
Her PBI'ın promptu repoda `plan/board/promptlar/<ID>.md` dosyasıdır; board'daki PBI açıklaması bu dosyaya link verir. Prompt kuralları **tekrar etmez, işaret eder** (tek kaynak `AGENTS.md`, `docs/anayasa.md`, modül `AGENTS.md`, `contracts/`).

```
# <ID> · <başlık>                      (AB#<id> — board'a alınınca doldurulur)
Sahip: <kişi> · Agent: <araç> · Modül/klasör: <yol> · Effort: <n> · En geç: <tarih>

## Bağlam (önce oku)
- AGENTS.md (kök) · <modül>/AGENTS.md · docs/anayasa.md: <ilgili S/K maddeleri>
- <sözleşme / fixture / ADR / tez bölümü yolları>

## Görev
<2–5 cümle: ne yapılacak, neden (hangi omurga parçası / deney)>

## Kapsam
- Değiştirebileceğin yer: <klasör(ler)>
- Dokunma: <klasör(ler)>. Başka modüle ya da contracts/'a dokunman gerekirse DUR, PR açıklamasına "contract-change gerekli" yaz.

## Adımlar
1. Önce planı yaz (dosya listesi + test listesi), sonra uygula.   ← Claude Code: plan modu; Codex/Antigravity: ilk mesajda plan
2. …
n. Yerelde: <build/test/lint komutları>

## Kabul kriterleri (her biri test ya da görünür çıktı)
- [ ] …

## Teslim
- Dal: <modül>/AB<id>-<kısa-ad> · Commit/PR başlığı: <tip>(<modül>): … AB#<id>
- PR şablonunu doldur; kabul kriterlerini PR'da işaretle; ekran görüntüsü (UI ise).
```

**Araç notları (ADR-013):** Claude Code → `CLAUDE.md` = `@AGENTS.md` (2.1.183'te AGENTS.md doğrudan okunmuyor; import tüm sürümlerde çalışır), skill'ler `.claude/skills` symlink'i, büyük işte önce plan modu · Codex → `AGENTS.md` + nested, `.agents/skills`; toplam talimat ≤32 KiB · Antigravity → `AGENTS.md` (dosya başına ≤24 KB) + `.agents/skills`; `.agents/rules/` kullanılmaz (kopya kayması). Ortak: agent bir hatayı iki kez yaparsa kural önce **teste**, sonra gerekirse `AGENTS.md`'ye.

## 8. Sahiplik ve vekiller (ADR-004 + ADR-011)
| Modül / klasör | Sahip | Vekil |
|---|---|---|
| Kök dosyalar, `.github/`, `infra/`, `AGENTS.md`, `docs/anayasa.md`, CI | Levent | Hilal |
| `backend/…/planning` (Hane Planlama Motoru), `research/` (E1/E2) | Levent | Hilal |
| `backend/…/assistant`, `backend/…/privacy` (Gizlilik Kapısı) | Levent | Hilal |
| `backend/…/audit` + karar kaydı, gözlemlenebilirlik | Levent | Hilal |
| `backend/…/safety` (kural motoru: alerjen + sağlık durumu), `data/allergens`, altın setler | Hilal | Levent |
| `backend/…/household` + `identity` + `consent` | Hilal | Levent |
| `backend/…/shared` (ortak küçük tipler, `@Modulithic` shared module) | Levent | Hilal |
| `backend/…/catalog` (+ fiyat), `backend/…/pantry`, `backend/…/recommendation` | Hilal | Levent |
| Admin backend uçları | Hilal | Ozan |
| `apps/mobile`, `apps/web`, `apps/admin`, `packages/ui`, `packages/api-client` (üretilir) | Ozan | Hilal (mobil) · Levent (web/admin) |
| `data/recipes`, `data/dictionary`, `data/health-rules` (kaynak derleme) | Ozan | Hilal (şema + onay) |
| `backend/…/vision` (demo şeridi) | Ozan | Levent |
| `contracts/` | ilgili sağlayıcı modülün sahibi | tüketici onayı zorunlu |

Vekil tablosu Levent onayıyla kesinleşti (2026-09-27); ekip itirazı olursa A0.1'de güncellenir. Yük ~18 Aralık'ta yeniden dengelenir (A2.15).

## 9. Açık
- Repo: Levent'in GitHub Pro (Student Pack) kişisel hesabında private + iki collaborator (A0.9) — varsayılan.
- Azure Boards CSV içe aktarımında "Assigned To" e-postayla eşleşir; ekip e-postaları board kurulunca eklenecek.
- `sprint-report` betiği (board → MR taslağı) Azure DevOps MCP ya da REST ile Sprint 0'da yazılır (PBI A1.1-d).
