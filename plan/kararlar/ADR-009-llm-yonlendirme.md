# ADR-009 · LLM yönlendirme

**Tarih / onay:** 2026-09-25, ekip; 15 Kas kapısında kesinleşir

- **Ne:** Hane bağlamı taşıyan her tur **EVREN**'de (TR). Kişisel veri içermeyen işler (tarif yapılandırma, ürün etiketi okuma, katalog zenginleştirme) ucuz bulut modellerine gidebilir (DeepSeek vb.). EVREN 1 Kasım sonrası uygun değilse hane bağlamında asistan şablon + yer tutucu moduna iner (karar motorları LLM'siz çalışmaya devam eder).
- **Neden:** veri egemenliği + maliyet; kararlar zaten LLM'de değil.
- **Deneme:** en geç 1 Kasım (ücretsiz dönem): Türkçe tool-call doğruluğu, p95 gecikme, gömme boyutu, kullanım şartları.
