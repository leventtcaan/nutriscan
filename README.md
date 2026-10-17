# NutriScan

Paketli gıdanın içindekiler listesini ve besin tablosunu fotoğraftan okuyup kullanıcının sağlık durumu için
kaynaklı kurallarla değerlendiren, sonucu gerekçesi ve belirsizliğiyle gösteren mobil uygulama.
CSE 491/492 bitirme projesi · Akdeniz Üniversitesi Bilgisayar Mühendisliği · Grup 9 · Danışman: Dr. Taha Yiğit Alkan

**Tek doğruluk kaynağı:** [docs/mimari-karar-belgesi.md](docs/mimari-karar-belgesi.md). "Nasıl yapacağız?" sorusunun cevabı oradadır.

## Akış
```
etiket fotoğrafı → OCR → böl + türle → eşle (sözlük → bulanık → Qdrant) → kural tablosu → sonuç + kaynak + kapsam → LLM mesajı
```
Kararı yalnız kural tablosu verir. CTD/JECFA araştırma bilgisidir, Qdrant yalnız kelimeyi tanır, LLM yalnız son mesajı yazar.

## Klasörler
| Klasör | İçerik | Sahibi |
|---|---|---|
| `docs/` | Karar belgesi, araştırma notları | Levent (editör) |
| `data/sozluk/` | Kavramlar ve eşanlamlılar | Ozan |
| `data/kurallar/` | Kural tablosu | Hilal |
| `data/kanit/` | CTD/JECFA çıkarımları | Hilal |
| `tests/` | Eşleme testi (100 ifade), kural testi (20 senaryo) | Hep birlikte |
| `service/` | Python + FastAPI servisi | Levent |
| `app/` | Expo mobil uygulama | Ozan |
| `toplanti/` | Meeting Record'lar ve ekip mesajları | — |
| `plan/proposal/` | Proposal kaynağı (`python3 plan/proposal/build_docx.py`) | — |
| `kaynak/` | Ders şablonları (değiştirilmez) | — |

## Çalışma şekli
Kısa dal açılır, sahibi merge eder; haftalık ortak inceleme yapılır. Karar değişikliği grup mesajıyla değil, karar belgesine öneriyle gelir.

Önceki yönün (hane planlama) tüm dosyaları `arsiv/eski-yon-2026-10` etiketinde durur: `git checkout arsiv/eski-yon-2026-10`.
