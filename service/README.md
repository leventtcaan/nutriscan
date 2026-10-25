# service/ — Python prototipi

Etiket işleme ve kural değerlendirme prototipi burada bulunur:

- `nutriscan/text.py`: etiket metnini normalize eder ve içerik ifadelerini ayırır.
- `nutriscan/matcher.py`: E-kodu, birebir eşanlamlı, Türkçe çoğul ve bulanık eşleşme uygular.
- `nutriscan/rules.py`: `data/kurallar/kurallar_v0.csv` satırlarını çalıştırır.
- `run_labels.py`: CSV etiketlerini işler ve Markdown raporu yazar.

Çalıştırma: `python3 service/run_labels.py [etiketler.csv rapor.md]`

**Durum:** Bu, komut satırından çalışan bir prototiptir. FastAPI HTTP uç noktası, Qdrant eşlemesi ve LLM mesaj katmanı henüz repoda uygulanmamıştır. Mimari hedef ve sonraki kararlar için [karar belgesine](../docs/mimari-karar-belgesi.md) bakın.
