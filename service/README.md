# service/ — analiz servisi (Python paketi `nutriscan`)

| Dosya | Ne yapar | Sahibi |
|---|---|---|
| `nutriscan/text.py` | Etiket metnini normalize eder, içerik ifadelerine böler, "içerebilir" ve beyanları ayırır (C3) | Ozan |
| `nutriscan/matching/lexical.py` | E-kodu, birebir eşanlamlı, Türkçe çoğul ve bulanık eşleşme (C4) | Ozan |
| `nutriscan/rules/engine.py` | Kural tablosu satırlarını çalıştırır, durum başına sonuç üretir (C6) | Levent |
| `nutriscan/pipeline.py` | Bir etiketi sırayla böl → eşle → değerlendir; API ve ölçüm betikleri bunu çağırır | Levent |
| `nutriscan/config.py` | Veri klasörü, kural dosyası ve eşikler (`data/config/esikler.toml`); başka hiçbir yerde yol ya da eşik yazılmaz | Levent |
| `nutriscan/types.py` | Ortak sözlük: dört sonuç (`Outcome`) ve önem sırası. Değişmeden önce gruba haber verilir | Levent |
| `nutriscan/codes.py` | Türkçe veri değerleri ↔ İngilizce API kodları; bilinmeyen değer hata verir | Levent |
| `run_labels.py` | CSV etiketlerini işler, Markdown rapor yazar | Levent |

**Kurulum ve çalıştırma:** kök README'deki kurulumdan sonra `.venv/bin/python service/run_labels.py [etiketler.csv rapor.md]`.

**Ortam değişkenleri:** `NUTRISCAN_DATA_DIR` (varsayılan: depodaki `data/`), `NUTRISCAN_RULES_FILE` (varsayılan: `kurallar_v0.csv`).

**Durum:** FastAPI uç noktası (#17), anlamsal arama (#26) ve açıklama katmanı (#32) henüz yok. Tasarım: `docs/tasarim/02-mimari.md`.
