---
title: Durum — NutriScan
updated: 2026-09-29
---
# Durum

> Her oturum başında okunur; **≤ 60 satır**, yalnız "şu an". Tarihçe → `oturumlar/`, kararlar → `plan/kararlar/`,
> işler → Azure Boards + `plan/board/`, bulgular → `arastirma/`. Aşama ya da öncelik değişince güncellenir.

## Şu an
- **Aşama 0 · Karar ve proposal (→ 18 Ekim)**, Hazırlık sprinti (28 Eyl – 18 Eki). Sonra Sprint 0 (19 Eki – 1 Kas): temel + walking skeleton.
- Ürün yönü tez v5.1 (`arastirma/07-tez-v5.md`), ürün tanımı v5.1 (29 FR), proposal v0 hazır (6 sayfa). Prototip: `plan/prototip-kaynak/`.
- Ortak altyapı kuruldu (28 Eyl, ADR-013): bu depo, `AGENTS.md`, `docs/anayasa.md`, skill'ler, oturum günlükleri,
  board ↔ `plan/board/pbi.yaml`. Backend iskeleti AB#140 Done (PR #2 merge, 28 Eyl): 13 modül, sınırlar testle korunuyor (ADR-014). Board senkronu AB#261 (Hilal).
- Board: https://dev.azure.com/hilalhocaoglu20/NutriScan — 8 Epic · 65 Feature · 66 PBI · 21 Task, hepsi atanmış. Kapasite (Effort/sprint): varsayılan 13 · Sprint 0 Levent 20, Hilal 16 · Sprint 1 Hilal 14.
- Depo: https://github.com/leventtcaan/nutriscan (private) — Azure Boards'a GitHub App ile bağlı: commit/PR'da `AB#<no>` iş öğesine bağlanır, `Fixes AB#<no>` merge'de kapatır.

## Bu haftanın öncelikleri (tarihler "en geç"; erken bitirmek serbest)
1. **AB#104** takvim + çalışma akışı onayı (ekip, 30 Eyl) · **AB#109** "bitti/attım" kaydı (ekip, 5 Eki; fiş v5.2 ile çıktı)
2. **2 Ekim Cuma** danışman görüşmesi + **MR1** Teams'e aynı gün (hazırlık Levent başlatınca; önceden gündeme getirilmez)
3. **AB#117** proposal eksikleri (öğrenci no, grup no; 9 Eki danışmana; PDF eski — teslimden önce `.docx` Pages'te açılıp Dosya → Dışa Aktar → PDF) · **AB#122/123** tarif şeması + sözlük (Ozan, 16 Eki)
4. ✅ Hilal ve Ozan depoyu kurdu, ilk prompt sorunsuz (28 Eyl)

## Sıradaki (Levent) — yeni komuta merkezi oturumu buradan başlar
Sıra (29 Eyl): ✅ A0.4-a Done · ✅ [A1.6-a · OpenAPI iskeleti](https://dev.azure.com/hilalhocaoglu20/NutriScan/_workitems/edit/149) Done (PR #3 + #4; A1.6-b Ozan'a açıldı) ·
1) **v5.2 fiyat revizyonu** (ADR-015 ÖNERİ) → ekip bildirimi ·
2) [A1.1-a · AGENTS.md doğrulaması](https://dev.azure.com/hilalhocaoglu20/NutriScan/_workitems/edit/131) — eksik: anayasa K sütununa test adı/PBI, üç araç kanıtı ·
3) ekip Task'ları: [A0.1-a-L](https://dev.azure.com/hilalhocaoglu20/NutriScan/_workitems/edit/105) (30 Eyl) ·
[A0.2-a-L](https://dev.azure.com/hilalhocaoglu20/NutriScan/_workitems/edit/110) · [A0.5-a-L](https://dev.azure.com/hilalhocaoglu20/NutriScan/_workitems/edit/118) (9 Eki).

## Bekleyen kararlar
- ADR-013 ortak altyapı — ÖNERİ, ekip onayı (A0.1 ile).
- Kalıcı tasarım dili (renk/yazı) — A1.7-a'da `frontend-design` planıyla; prototip paleti taslak.

## Açık riskler
- **Azure DevOps MCP — çözüldü, yalnız yenileme riski:** masaüstü uygulaması `~/.zshenv` okumadığı için `.mcp.json` artık `tools/ado-mcp.sh` başlatıcısını kullanıyor (PAT'i env'den ya da Anahtar Zinciri `nutriscan-ado-pat` kaydından alır, base64(`:PAT`) yapar). MCP ile AB#115 get + list_comments doğrulandı (401 yok). Salt-okuma PAT 27 Ara'da biter → öncesinde yenile, Anahtar Zinciri kaydını değiştirmek yeter.
- **Fiyat verisi (29 Eyl, ADR-015 ÖNERİ):** marketfiyati reddetti (ADR-002) → Ürün ve Fiyat Toplayıcı, pilot **ŞOK + Tarım Kredi**, fiş çıktı, K21.
  Toplayıcı çekirdeği + ŞOK [A2.4-b · toplayıcı](https://dev.azure.com/hilalhocaoglu20/NutriScan/_workitems/edit/186) Levent (Sprint 0) → Tarım Kredi A2.4-c → katalog A2.4-a (20 Kas). Açık risk: online fiyat = raf fiyatı
  doğrulanmadı (tek mağazada 10–20 ürün) · kamuya açık sürüm için yazılı izin/lisans D3 öncesi (A4.8) · Hilal teyidi + ekip onayı bekliyor.
- **EVREN ücretsiz dönemi 1 Kasım'da bitiyor:** deneme (AB#158) en geç 30 Ekim. Levent'in anahtarı Anahtar Zinciri'nde
  (`nutriscan-evren-api-key`, son kullanma 31.12.2026 → öncesinde yenile). LLM şartları v1 onaylandı (28 Eyl); fiyat hâlâ 0 CR, 1 Kasım sonrası ilan edilmedi;
  şartlar anahtar paylaşımını yasaklıyor, saklama süresi yazılı değil (`arastirma/09-evren-ve-board-notu.md`).
- Eski projenin sırları (SMTP/DB) iptal edildi mi teyit edilmedi; eski Azure Repos'ta 4 depo duruyor (dokunulmadı).

## Sabit tarihler
Meeting Record: 2 · 16 · 30 Eki, 13 · 27 Kas · Proposal 18 Eki · Ara rapor ~6 Kas · Final ~18 Ara (teyit) · Tam liste `plan/takvim.md` §1.

## Betikler
Board/prompt: `python3 plan/board/board_uret.py` · Takvim mesajı: `python3 plan/takvim_mesaj_uret.py` ·
Proposal: `python3 plan/proposal/build_docx.py` · Ekip paketi: `python3 plan/ekip_paketi_uret.py <klasör>`

## Bağlantılar
Kiler kayıtları (Drive, yalnız ekip; fiş klasörleri v5.2 ile kullanılmıyor): https://drive.google.com/drive/folders/1epph-aHH7v28m11WbxFwLXEksCyVMCEi
Kurallar `AGENTS.md` · Anayasa `docs/anayasa.md` · Süreç `plan/calisma-akisi.md` · Takvim `plan/takvim.md` ·
Kararlar `plan/kararlar.md` · İlk açılış `plan/ilk-prompt.md` · Tez `arastirma/07-tez-v5.md` · Ürün `plan/urun-tanimi.md`
