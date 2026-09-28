---
title: Durum — NutriScan
updated: 2026-09-28
---
# Durum

> Her oturum başında okunur; **≤ 60 satır**, yalnız "şu an". Tarihçe → `oturumlar/`, kararlar → `plan/kararlar/`,
> işler → Azure Boards + `plan/board/`, bulgular → `arastirma/`. Aşama ya da öncelik değişince güncellenir.

## Şu an
- **Aşama 0 · Karar ve proposal (→ 18 Ekim)**, Hazırlık sprinti (28 Eyl – 18 Eki). Sonra Sprint 0 (19 Eki – 1 Kas): temel + walking skeleton.
- Ürün yönü tez v5.1 (`arastirma/07-tez-v5.md`), ürün tanımı v5.1 (29 FR), proposal v0 hazır (6 sayfa). Prototip: `plan/prototip-kaynak/`.
- Ortak altyapı kuruldu (28 Eyl, ADR-013): bu depo, `AGENTS.md`, `docs/anayasa.md`, skill'ler, oturum günlükleri,
  board ↔ `plan/board/pbi.yaml`. Backend iskeleti AB#140: PR #2 incelemede (vekil Hilal); 13 modül, sınırlar testle korunuyor (ADR-014).
- Board: https://dev.azure.com/hilalhocaoglu20/NutriScan — 8 Epic · 65 Feature · 65 PBI · 21 Task, hepsi atanmış.
- Depo: https://github.com/leventtcaan/nutriscan (private) — Azure Boards'a GitHub App ile bağlı: commit/PR'da `AB#<no>` iş öğesine bağlanır, `Fixes AB#<no>` merge'de kapatır.

## Bu haftanın öncelikleri (tarihler "en geç"; erken bitirmek serbest)
1. **AB#104** takvim + çalışma akışı onayı (ekip, 30 Eyl) · **AB#109** fiş/"bitti" kaydı (ekip, 5 Eki)
2. **2 Ekim Cuma** danışman görüşmesi + **MR1** Teams'e aynı gün
3. **AB#117** proposal eksikleri (öğrenci no, grup no; 9 Eki danışmana) · **AB#122/123** tarif şeması + sözlük (Ozan, 16 Eki)
4. Hilal ve Ozan: GitHub davetini kabul et, depoyu klonla, ilk promptu çalıştır (`plan/ilk-prompt.md`)

## Bekleyen kararlar
- ADR-013 ortak altyapı — ÖNERİ, ekip onayı (A0.1 ile).
- Kalıcı tasarım dili (renk/yazı) — A1.7-a'da `frontend-design` planıyla; prototip paleti taslak.

## Açık riskler
- **Azure DevOps MCP:** organizasyon kişisel Microsoft hesaplı → uzak sunucu desteklenmiyor; yerel sunucu bağlandı ama PAT ile 401 (28 Eyl) → PAT yetkisi/süresi kontrol edilmeli (Levent).
- **marketfiyati izni:** dönüş yok (24 Eyl); en geç ~9 Eki hatırlatma. B planı ekip fiyat turu (AB#186).
- **EVREN ücretsiz dönemi 1 Kasım'da bitiyor:** deneme (AB#158) en geç 30 Ekim.
- Eski projenin sırları (SMTP/DB) iptal edildi mi teyit edilmedi; eski Azure Repos'ta 4 depo duruyor (dokunulmadı).

## Sabit tarihler
Meeting Record: 2 · 16 · 30 Eki, 13 · 27 Kas · Proposal 18 Eki · Ara rapor ~6 Kas · Final ~18 Ara (teyit) · Tam liste `plan/takvim.md` §1.

## Betikler
Board/prompt: `python3 plan/board/board_uret.py` · Takvim mesajı: `python3 plan/takvim_mesaj_uret.py` ·
Proposal: `python3 plan/proposal/build_docx.py` · Ekip paketi: `python3 plan/ekip_paketi_uret.py <klasör>`

## Bağlantılar
Kurallar `AGENTS.md` · Anayasa `docs/anayasa.md` · Süreç `plan/calisma-akisi.md` · Takvim `plan/takvim.md` ·
Kararlar `plan/kararlar.md` · İlk açılış `plan/ilk-prompt.md` · Tez `arastirma/07-tez-v5.md` · Ürün `plan/urun-tanimi.md`
