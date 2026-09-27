# ADR-010 · Ortak geliştirme verisi: Git'te tek kaynak + ortak staging DB

**Tarih / onay:** 2026-09-25, ekip

- **Ne:** Şema Flyway migration'larıyla, tohum (seed) verisi `data/` altında Git'te; herkes aynı komutla (Docker Compose) aynı yerel veritabanını kurar. Ortak staging PostgreSQL Contabo'da (yalnız sentetik veri).
- **Neden:** "veri herkeste farklılaşıyor" sorununun kökü tek kaynak eksikliği; Firebase gibi bir bulut DB bunu çözmez, üstelik veriyi yurt dışına taşır ve Spring/PostgreSQL mimarisine uymaz.
- **Alternatif:** Firebase/Supabase. **Neden değil:** yurt dışı barındırma (KVKK), satıcı bağımlılığı, iki farklı veri modeli.
- **Not (2026-09-25):** Gayriresmi `github.com/EnesCinr/market-fiyatlari-mcp-server` (marketfiyati iç uç noktaları `/search`, `/searchByIdentity`) değerlendirildi → **izin gelene kadar kullanılmaz** (kullanım koşulları yazılı izin şartı; MIT lisansı kodu kapsar, veriyi değil; bekleyen izin başvurusuyla çelişir). İzin gelirse entegrasyon referansı olarak kullanılır (`searchAlternative` takas için ilgili). İzin maili için hatırlatma: dönüş yoksa en geç ~9 Ekim, danışman bilgili kısa hatırlatma.
