# ADR-001 · Ürün yönü: Tez v5 "hanenin haftalık planlama asistanı"

**Tarih / onay:** 2026-09-24, Levent onayı

- **Ne:** NutriScan, zincirden bağımsız, hanenin haftalık yemek + alışveriş planını kuran asistan. Omurga: Hane Planlama Motoru (birleşik Menü–Sepet–Market optimizasyonu); güvenceler: doğrulanabilir asistan (LLM orkestra eder, motorlar karar verir) + gizlilik-koruyan asistan (hane bağlamı taşıyan LLM turları Türkiye'de — ADR-008/009); veri katkısı: 200 lisansı temiz Türk ev yemeği + alerjen ontolojisi; zemin: S1–S22 sözleşme, K01–K20 anayasa. Başarı kriterleri E1/E2/E3 deneyleri. Detay: `arastirma/07-tez-v5.md`.
- **Neden:** v1 (alerjen tarayıcı) sığ ve rakiplerle aynı; v2 (fiş merkezli) dağınık ve zayıf girdiye bağlı; v3 (liste optimizasyonu) derin ama dar, AI görünmüyor; v4 kapsamı doğru ama iddiaları kalibresiz ve takvimi akademik takvime oturmuyordu. v5 = v4 kapsamı + kırmızı takımın 5 düzeltmesi. Bölüm yönergesinin "karmaşık mühendislik problemi" şartını, danışmanın alanını (öneri + optimizasyon, exact vs GA) ve Levent'in "görünür AI, kapsamı sınırlama" isteğini birlikte karşılıyor.
- **Alternatifler:** v1–v4 (yukarıda); kırmızı takım v2'deki "Fiş-merkezli gıda gözlemevi" (Çerçeve B).
- **Neden onlar değil:** özgünlük (MAYA, Yuka, Ürün Dedektörü vb. ile çakışma), derinlik eksikliği ya da girdi/veri riski; ayrıntı `arastirma/02-v2-kirmizi-takim.md`, `06-v4-kirmizi-takim.md`.
- **Açık:** beta kitlesi (işe alım kanalı). Kapananlar: pilot zincirler → ADR-003 · hat sahipliği → ADR-004 · EVREN sorumlusu → Levent (A0.4) · menü kapsamı → hafta içi 5 akşam. **v5.1 güncellemesi: ADR-011.**
