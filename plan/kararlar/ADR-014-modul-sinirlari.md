# ADR-014 · Backend modül sınırları: açık izin listesi, en dar başlangıç

**Tarih / onay:** 2026-09-28, AB#140 (PR #2) — ÖNERİ; ekip onayı Hilal'in PR incelemesiyle

- **Ne:**
  1. `backend/` tek Gradle projesi; modüller `com.nutriscan` altındaki 13 paket (Spring Modulith), alt proje yok.
  2. Her modülün `package-info.java`'sı `@ApplicationModule(allowedDependencies = …)` ile **açık** izin listesi taşır. İlk harita
     (`arastirma/08-ekip-calisma-modeli.md` §3.a sözleşme tablosundan): planning → safety, audit · assistant → privacy, planning ·
     vision → privacy · safety → audit · recommendation → safety, audit · diğer 7 modül → `{}` (hiçbiri).
  3. `shared`, `@Modulithic(sharedModules = "shared")` ile ortak modül: herkes kullanır, kendisi kimseye bağımlı olmaz.
  4. Olay dinleme bağımlılıkları (catalog/pantry/household → planning) modülün tamamına değil adlandırılmış arayüze verilir:
     `"catalog :: events"`; olaylar yazıldığında eklenir.
  5. Liste genişletmek PR'da görünür bir satırdır; bağımlı modülün sahibi onaylar.
- **Neden:** `allowedDependencies` yazılmazsa Modulith varsayılanı **sınırsız** (spring-modulith-api 2.1.1 `ApplicationModule.java`
  kaynağında doğrulandı). Açık liste, kırmızı çizgileri mimaride zorlar: alerjenli aday çözücüye yalnız safety üzerinden gidebilir
  (S10), dış LLM'e yalnız privacy çıkar (K06, K18). `ModularityTests.verify()` bunu her build'de denetler; AB#140'ta bilerek
  bozulup kırmızıya döndüğü gösterildi.
- **Alternatif:** (a) varsayılanı bırakıp yalnız ArchUnit kuralı yazmak · (b) tahminle geniş başlangıç listesi · (c) modül başına
  Gradle alt projesi · (d) `shared` için `@ApplicationModule(type = OPEN)`.
- **Neden o değil:** (a) her yasak ayrı kural ister, unutulan modül sınırsız kalır · (b) daraltmak mevcut kodu kırar, genişletmek tek
  satır · (c) sınırı iki kez çizer, 3 kişilik ekipte build karmaşası; gerekirse sonra bölünür · (d) OPEN iç paketleri de açar ve
  modülü döngü denetiminden çıkarır.
- **Geri dönmenin maliyeti:** düşük: liste satırları ve bir test; alt projeye bölmek orta (Gradle yeniden yapılandırma).
- **Etkilenen:** bütün backend modül sahipleri (Levent, Hilal, Ozan) · `backend/AGENTS.md` · A1.2 CI kapıları.
