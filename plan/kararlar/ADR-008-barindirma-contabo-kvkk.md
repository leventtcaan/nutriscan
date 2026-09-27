# ADR-008 · Barındırma: tüm ortamlar ekibin Contabo VPS'inde

**Tarih / onay:** 2026-09-25, ekip — son karar

- **Ne:** Geliştirme, ortak staging, jüri demosu **ve beta** ekibin yıllık kiralı Contabo VPS'inde (Docker Compose). Ek barındırma maliyeti yok.
- **Neden:** Kullanıcı sayısı küçük (beta 20–40 hane); yıllık ödeme yapılmış; ekip daha önce VPS üzerinden canlıya çıktı.
- **KVKK yolu (Contabo'nun TR lokasyonu yok → yurt dışı aktarım):** beta öncesi (en geç Mart 2027) şu katmanlar birlikte uygulanır:
  1. **Veri minimizasyonu:** hesap için yalnız gerekli alanlar; üye adı yerine takma ad; doğum tarihi yerine yaş aralığı; fiş görselleri işlendikten sonra silinir.
  2. **Sağlık kısıtlarının korunması:** alan düzeyinde şifreleme (anahtarlar sunucu diskinde değil); loglarda/izlemede sağlık alanı yok (gece testi).
  3. **Yerel-öncelikli tasarım seçeneği (değerlendirilecek):** kesin kısıtlar cihazda tutulur, sunucu kararları ürün düzeyinde üretir, eşleştirme cihazda yapılır → sağlık verisinin sunucuya sistematik gidişi azalır. Planlama motoru için gereken kısıt vektörü kimliksiz ve kalıcı olmayan istekle gönderilir.
  4. **Hukuki dayanak:** Contabo ile KVKK standart sözleşmesi (değiştirilmeden, 5 iş günü içinde Kurum'a bildirim) denenir; aydınlatma metninde verinin AB'de (Almanya/bölge teyit edilecek) işlendiği açıkça yazılır; beta öncesi bir KVKK uzmanından kısa görüş (danışman aracılığıyla).
  - Bu katmanlar riski azaltır; takma adlı/şifreli veri KVKK'da kişisel veri sayılmaya devam eder. Standart sözleşme sağlanamazsa beta için geri dönüş yolu: aynı Docker kurulumunun küçük bir TR sunucusuna taşınması.
- **LLM:** hane bağlamı taşıyan turlar EVREN'de (TR) kalır (ADR-009).
- **Tez etkisi:** 07-tez-v5'teki "hane bağlamı taşıyan veriyi Türkiye'de işler" cümlesi proposal'da "hane bağlamı taşıyan LLM işlemleri Türkiye'de; uygulama verisi KVKK standart sözleşmesiyle AB'de, minimize ve şifreli" olarak güncellenecek. *(✅ 27 Eyl: tez v5.1 + proposal güncellendi.)*
- **Alternatif:** beta için TR VPS · Radore/Netinternet tam kurulum. **Neden değil (şimdilik):** mevcut kaynak kullanılacak; yukarıdaki yol sağlanamazsa yeniden açılır.
