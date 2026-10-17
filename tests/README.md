# tests/ — iki sınav

Karar belgesi §7. Ayrı bir deney fazı değil; kodun testleridir.

- `eslesme/` — gerçek etiketlerden 100 ifade + doğru cevap (biri yazar, öbürü kontrol eder; bazılarının cevabı "Doğrulanamadı").
  Aynı kod iki ayarla çalışır: yalnız sözlük · sözlük + Qdrant. Ölçüt: doğru sayısı, cevap verme oranı, isabet, yanlış uydurma.
- `kurallar/` — 20 ürün × durum senaryosu; beklenen sonuç kılavuza göre yazılır. Ölçüt: kaçırılan uyarı (en kritik), gereksiz uyarı, "Doğrulanamadı" oranı.
