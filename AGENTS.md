# AGENTS.md — NutriScan (CSE 491/492 bitirme projesi)

Bu dosya üç agent'ın **ortak** kuralıdır: Codex ve Antigravity doğrudan okur, Claude Code `CLAUDE.md` içindeki
`@AGENTS.md` ile. Kural bir kez burada yazılır; ayrıntı aşağıdaki dosyalardadır, oradan varsayma.
Ders: CSE 491/492 Senior Design · Akdeniz Üniversitesi Bilgisayar Müh. · Danışman: Arş. Gör. Dr. Taha Yiğit Alkan.

## Ekip ve kişisel katman
Levent (Claude Code) · Hilal (Codex) · Ozan (Antigravity). Kiminle çalıştığını kişisel katmandan anla:
Levent `CLAUDE.local.md` (gitignore) · Hilal `~/.codex/AGENTS.md` · Ozan `~/.gemini/GEMINI.md`. Anlaşılmıyorsa **sor**.
Kişisel katman yalnız kişiye özgü tercihleri taşır; proje kuralı her zaman buradadır.

## Proje tek cümlede
Hangi zincirden alışveriş yapılırsa yapılsın hanenin haftalık yemek + alışveriş planını kuran asistan: önce her üyenin
kesin kısıtını ve sağlık durumu kurallarını doğrular, kilerdekini önce kullanır, bütçe sınırında iki markete kadar
optimize eder, her kararını kanıtıyla gösterir. **Kararı motorlar verir (kural motoru, Hane Planlama Motoru); LLM
yalnız anlatır ve araç çağırır.** Tez: `arastirma/07-tez-v5.md` (v5.1).

## Nerede ne var, ne zaman okunur
Hepsini baştan okuma; ihtiyaç olduğunda aç.
| Ne | Nerede | Ne zaman |
|---|---|---|
| Şu an: aşama, bu haftanın öncelikleri, riskler | `DURUM.md` | Her oturum başı |
| Kendi son oturumların | `oturumlar/<kişi>.md` (son 3 girdi) | Her oturum başı |
| Üzerinde çalışılan iş (prompt + kabul) | `plan/board/promptlar/<ID>.md` · AB# eşlemesi `plan/board/azure-idler.yaml` · board: Azure Boards | Her oturum başı |
| Tüm iş listesi (tek kaynak) | `plan/board/pbi.yaml` → özet `plan/board/backlog.md` | İş seçerken |
| Tarihler ("en geç") ve bağımlılık | `plan/takvim.md` | Plan sorusunda |
| Süreç: akış, DoR/DoD, sprint, PR, sahip/vekil | `plan/calisma-akisi.md` | Süreç sorusunda |
| Değişmez kurallar (S1–S22, K01–K20, sağlık dili) | `docs/anayasa.md` | Kod ya da metin yazarken |
| Kararlar | `plan/kararlar.md` (dizin) → `plan/kararlar/ADR-0NN-*.md` | Bir karara dokunurken |
| Ürün: persona, ekranlar, FR/NFR | `plan/urun-tanimi.md` | Kapsam sorusunda |
| Ekran akışları (prototip) | `plan/prototip-kaynak/*.dc.html` | Arayüz işinde |
| Önceki araştırma | `arastirma/NN-*.md` | Konu daha önce araştırıldıysa |
| Ders kuralları, şablonlar | `kaynak/` (**değiştirme**) | Teslim sorusunda |

## Oturum protokolü (skill: `pbi-baslat`, `pbi-kapat`)
**Başlarken:** `DURUM.md` + `oturumlar/<kişi>.md` son 3 girdi → `git pull` → çalışılacak PBI'ın promptu ve kabul
kriterleri. PBI yoksa ya da kabul kriteri boşsa **dur ve iste.** Bağımlı olduğu iş bitmemişse ve sözleşme/fixture
yoksa dur.
**Biterken:** kontrol komutlarının çıktısı görünür · `oturumlar/<kişi>.md` sonuna 5 satır (yaptım · karar · takıldım ·
sıradaki · AI) · karar alındıysa **o anda** ADR (skill: `karar-yaz`) · aşama/öncelik değiştiyse `DURUM.md`.

## Yöntem
Yeni bir konuda ilk hamle kod değildir: **araştır → planla → karar ver → yaz.** Araştırma `arastirma/NN-konu.md`'ye,
her iddia kaynak linki ve doğrulama notuyla. Büyük işte önce 5–10 maddelik plan, insan onayı, sonra kod.

## Dizin haritası
- Planlama ve hafıza (Türkçe): `DURUM.md`, `oturumlar/`, `plan/`, `arastirma/`, `docs/`, `kaynak/`, `toplanti/`
- Kod (İngilizce; A1.3/A1.6/A1.7 ile gelir): `backend/` (Spring Boot + Modulith; modüller household, identity,
  consent, safety, catalog, planning, recommendation, pantry, vision, assistant, privacy, audit, shared) ·
  `apps/mobile` (Expo) · `apps/web`, `apps/admin` (Vite + React) · `packages/ui`, `packages/api-client` (üretilir) ·
  `contracts/` (OpenAPI, olay, motor, LLM araç şemaları) · `data/` (tarif, sözlük, alerjen, sağlık kuralı, katalog, seed) ·
  `research/` (E1/E2 deney kodu; `arastirma/` ile karıştırma) · `infra/` · `tools/`
- Her kod modülünde kısa bir `AGENTS.md` (+ Claude için `CLAUDE.md` = `@AGENTS.md`) bulunur; modülün kuralı oradadır.
- Ortak skill'ler: `.agents/skills/` (Codex, Antigravity okur; Claude için `.claude/skills/` symlink).

## Kırmızı çizgiler (her zaman)
1. **"Güvenli" yok.** Karar dört durumdan biridir: Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı.
2. **Belirsizlik riski yalnız artırır:** eksik, eski, çelişkili ya da tanınmayan veri → Doğrulanamadı. Tahmin yok (S8).
3. **LLM karar vermez ve değer uydurmaz:** uygunluk, kısıt, fiyat, eşik, optimizasyon sonucu yalnız motordan/veriden gelir (K01, K02).
4. **Sağlık verisi:** logda/izde yok; dışarı maskesiz çıkmaz (tek egress: `privacy`); prod verisi yerelde ve agent'ta yok — yalnız sentetik hane (K06, K18, K19).
5. **Tıbbi dil yok:** "zararlı, riskli, tedavi, önler, hastalığına iyi gelir" yok; teşhis sorulmaz (anayasa §3).
6. **Kesin kısıt hiçbir yoldan gevşemez** (asistan, optimizasyon, yazılı istek); yalnız sahibi profil ekranından (S10).
7. **Hardcode yok:** eşik, tarih, pencere, kimlik (AB#, org, proje), parametre ve kullanıcıya görünen metin koda
   gömülmez; yapılandırma, veri dosyası, metin dosyası ya da plan dosyasından okunur. Sihirli sayı ve geçici yama yok.
8. **Sır yok:** anahtar, parola, token repoya, prompta, loga girmez; ortam değişkeni ya da kasa (K15).
9. **Kaynak/sürüm/API uydurma yok:** kurulu sürümde ya da resmî dokümanda doğrula; doğrulayamazsan `[..]` bırak ve söyle.

## Kod kuralları
10. Önce test: her kabul kriterine en az bir test; testi koddan sonra kodun davranışına uydurma.
11. **Bir PR = bir modül**, ≤ ~400 satır (üretilmiş kod, lockfile, veri hariç). Görevin modülü dışına dokunman
    gerekirse **dur**; `contracts/` değişikliği önce ayrı "contract-change" PR'ı ister (`plan/calisma-akisi.md` §6).
12. Sözleşme önce: API `contracts/openapi`'den, TS istemcisi üretilir (elle düzenlenmez); isim uydurma — sözleşme, sözlük ya da şemada yoksa sor.
13. Yeni bağımlılık, şema/migration değişikliği, enum sıra numarası, test silme → **sorulmadan yapılmaz**.
14. İkinci kullanımı yoksa soyutlama kurma; basit ve okunur kod.
15. Dil: kod, tanımlayıcılar, commit başlığı, API ve rapor İngilizce; planlama dosyaları ve arayüz metni Türkçe.
16. Arayüz işinde `arayuz-tasarim` skill'i zorunlu; veri işinde `tarif-ekle`.

## Her değişiklikten sonra (en fazla 5 satır)
Ne değişti · neden · alternatif neydi · hangi test neyi kanıtlıyor · insanın kontrol etmesi gereken satır.

## Git ve PR
- Kod değişikliği `main`'e doğrudan girmez (planlama/altyapı dosyalarında depo yöneticisi istisnası: ADR-013). Dal: `<modül>/AB<no>-kisa-ad`. Commit: Conventional + iş öğesi, ör. `feat(safety): gluten kuralı AB#179`.
- PR gövdesinde `Fixes AB#<no>`; şablon eksiksiz; "AI kullanımı" bölümü zorunlu.
- PR'ı modülün sahibi ya da vekili onaylar (`plan/calisma-akisi.md` §8); sahip kendi PR'ını onaylamaz. **Agent onay vermez.**
- **Commit ve PR'da AI imzası yok** (`Co-Authored-By`, "Generated with…"): yazar insandır; AI kullanımı PR'da beyan edilir.
- AI kullanımı serbest ve açıktır; şart: her satır ve karar sahibi tarafından **anlatılabilir ve savunulabilir** olmalı
  (Cuma demosunda agent'ın yazdığı bir parça anlatılır).

## Karar dosyası
`plan/kararlar/ADR-0NN-kisa-ad.md`: ne · neden · alternatif · neden o değil · geri dönmenin maliyeti · etkilenen ·
durum (ÖNERİ/KABUL). ÖNERİ'yi KABUL'e yalnız insan çevirir. Dizine (`plan/kararlar.md`) satır eklenir.

## Sorulmadan yapılmaz
Bağımlılık ekleme · şema/migration · `kaynak/` altına dokunma · anayasa maddesi değiştirme · başka modülün koduna
dokunma · dal silme/force push · board'da başlık/tarih/atama/kapsam değiştirme (önce `plan/board/pbi.yaml` PR'ı) ·
dışarıya veri gönderen komut (telemetri, geri bildirim, yükleme) çalıştırma.

## Komutlar
Kod iskeleti gelince (A1.3, A1.6, A1.7) buraya ve modül `AGENTS.md`'lerine eklenir. Şimdilik:
- Board ve promptlar: `python3 plan/board/board_uret.py` (pbi.yaml + takvim → CSV, backlog, promptlar)
- Takvim mesajı/PDF: `python3 plan/takvim_mesaj_uret.py` · Proposal: `python3 plan/proposal/build_docx.py`
- "Bitti" demeden önce ilgili komutları çalıştır ve **çıktıyı göster.**
