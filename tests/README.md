# tests/ — iki sınav

Karar belgesi §7. Ayrı bir deney fazı değil; kodun testleridir.

- `eslesme/` — gerçek etiketlerden 100 ifade + doğru cevap (biri yazar, öbürü kontrol eder; bazılarının cevabı "Doğrulanamadı").
  Aynı kod iki ayarla çalışır: yalnız sözlük · sözlük + Qdrant. Ölçüt: doğru sayısı, cevap verme oranı, isabet, yanlış uydurma.
- `kurallar/` — 20 ürün × durum senaryosu; beklenen sonuç kılavuza göre yazılır. Ölçüt: kaçırılan uyarı (en kritik), gereksiz uyarı, "Doğrulanamadı" oranı.

## Etiket nasıl eklenir (`eslesme/etiketler.csv`)
Mutfaktaki bir paketin arkasını **olduğu gibi** yaz; düzeltme yapma (yazım hatası da gerçek veridir).

| Sütun | Ne yazılır |
|---|---|
| `urun` | Ürün adı (marka yazmak zorunlu değil) |
| `kategori` | bisküvi, içecek, kraker… |
| `sivi` | `evet` / `hayir` |
| `icindekiler` | "İçindekiler:" ile başlayan metnin tamamı, "içerebilir" cümlesi ve "glutensiz" gibi beyanlar dahil; tırnak içinde |
| `sekerler_g_100` | Besin tablosundaki "şekerler" (100 g ya da 100 ml); yoksa boş |
| `tuz_g_100` | Besin tablosundaki "tuz"; yoksa boş |
| `ornek_mi` | Gerçek paketse boş bırak |

Çalıştır: `python3 service/run_labels.py` → `eslesme/rapor.md`. Testler: `python3 -m unittest discover -s tests -v`.
