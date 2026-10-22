# Kaynak ve lisans envanteri

Her satır bir kaynak. Veri repoya girmeden önce satırı doldurulur (bkz. `docs/arastirma/06-lisans-ve-telif-kontrolu.md`).

| Kaynak | URL | Sürüm / indirme | Lisans | Alınan alanlar | Kullanım | Kontrol eden |
|---|---|---|---|---|---|---|
| Open Food Facts — ingredients taxonomy | github.com/openfoodfacts/openfoodfacts-server · `taxonomies/food/ingredients.txt` | commit 14cbdc68, 22.10.2026 | ODbL 1.0 (atıf; türev veri tabanı paylaşım şartı incelenecek) | İngilizce/Türkçe adlar, üst kavram (IS_A), wikidata | `data/sozluk/` (kavram, eşanlamlı) | Levent · [2. kişi] |
| Open Food Facts — additives taxonomy | aynı depo · `taxonomies/additives.txt` | commit 14cbdc68, 22.10.2026 | ODbL 1.0 | E-kodu, İngilizce/Türkçe ad, wikidata | `data/sozluk/` | Levent · [2. kişi] |
| Reg. (EC) No 1924/2006, konsolide 13.12.2014 — Ek | eur-lex.europa.eu · CELEX 02006R1924-20141213 | 22.10.2026'da okundu | AB mevzuatı (atıfla serbest) | şeker içermez / düşük şeker / düşük–çok düşük sodyum eşikleri | `data/kurallar/` DM-01, CKD-01 | Levent · [Hilal] |
| Reg. (EU) No 1169/2011 — Ek I, Ek II | eur-lex.europa.eu · CELEX 32011R1169 | 22.10.2026'da okundu | AB mevzuatı | gluten içeren tahıllar ve muafiyetler; tuz = sodyum × 2,5 | `data/kurallar/` CEL-01/02, CKD-01 | Levent · [Hilal] |
| Reg. (EU) No 828/2014 | eur-lex.europa.eu · CELEX 32014R0828 | 22.10.2026'da okundu | AB mevzuatı | "glutensiz" ≤ 20 mg/kg | `data/kurallar/` CEL-03 | Levent · [Hilal] |
| TGK Beslenme ve Sağlık Beyanları Yönetmeliği | RG 29960 (mükerrer), 26.01.2017 (FAOLEX nüshası tur171238) | 22.10.2026'da okundu | Resmî mevzuat | 1924/2006 ile uyum beyanı (madde metni); **Ek-1 eşikleri teyit bekliyor** | `data/kurallar/` dayanak | [Hilal] |
| TGK Gıda Katkı Maddeleri Yönetmeliği | RG 32338 (mükerrer), 13.10.2023 | 22.10.2026'da indirildi | Resmî mevzuat | **Ekler taranmış PDF; E-kodu Türkçe adları henüz karşılaştırılmadı** | ileride `data/sozluk/` doğrulaması | [atanacak] |
