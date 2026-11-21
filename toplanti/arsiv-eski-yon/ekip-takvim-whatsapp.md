*NutriScan — Takvim* (plan/takvim.md'den üretildi, 28.09.2026)

Her iş: *ne* · 👤 kim · 🔗 neye bağlı · ⏰ en geç. Daha erken bitmesi serbest; en geç tarihi kaçarsa önceden yazılı "kaçarsa" planı uygulanır (tam liste PDF'te).
Kısaltma: işler ID ile (A2.4 gibi) birbirine bağlanıyor; bir iş, bağlı olduğu işler bitmeden bitmiş sayılmaz.

*📌 Sabit tarihler*
• *2 · 16 · 30 Ekim, 13 · 27 Kasım 2026* — Teams: Meeting Record 1–5 teslimleri (görüşmeler her Cuma)
• *18 Ekim 2026 (Pazar)* — CSE 491 Project Proposal — MS Teams (danışman onaylı)
• *1 Kasım 2026* — EVREN ücretsiz dönemi biter (LLM çağrıları kredisiz)
• *~6 Kasım 2026 ⚠️ teyit* — CSE 491 ara rapor + ara sunum ("vize haftası öncesi", OBS 8. hafta)
• *~18–20 Aralık 2026 ⚠️ teyit* — CSE 491 final raporu + çalışan ilk prototip (ders bitimi)
• *~8–11 Mart 2027* — Ramazan Bayramı (çalışma arası)
• *~26 Mart 2027 ⚠️ teyit* — CSE 492 "vize öncesi kodlama tamam" → özellik dondurma
• *~14 Mayıs 2027 ⚠️ teyit* — CSE 492 rapor + demo videosu jüriye (sınavdan ≥10 gün önce)
• *~15–19 Mayıs 2027 ⚠️ teyit* — Kurban Bayramı
• *24 Mayıs – 4 Haziran 2027 ⚠️ teyit* — Jüri sunumu (≤20 dk, İngilizce)

*Aşama 0 — Karar ve proposal (bugün → 18 Ekim)*
*A0.1* Takvimin ekipçe onayı
   👤 Ekip · 🔗 ADR-001…011 · ⏰ 30 Eylül
*A0.2* Ekip hanelerinin fiş + "bitti/attım" kaydına başlaması
   👤 Ekip · 🔗 — · ⏰ 5 Ekim
*A0.3* Ürün tanımı v5.1 + FR/NFR (proposal §5) — 2 Ekim görüşmesine
   👤 Levent · 🔗 Tez v5.1 · ⏰ 1 Ekim
*A0.4* EVREN hesabı + API anahtarı
   👤 Levent · 🔗 — · ⏰ 10 Ekim
*A0.5* Proposal taslağı (şablon: kaynak/CSE491_Project_Proposal_Template.docx) — danışmana e-postayla
   👤 Levent (+Hilal, Ozan bölümleri) · 🔗 A0.3, 2 Ekim görüşmesi · ⏰ 9 Ekim
*A0.6* Tarif şeması + malzeme sözlüğü v0 + alerjen ontolojisi taslağı
   👤 Ozan (şema: Hilal) · 🔗 Tez v5.1 §7 · ⏰ 16 Ekim
*A0.7* Proposal son hali danışmana
   👤 Levent · 🔗 A0.5 geri bildirimi · ⏰ 14 Ekim
*A0.8* Proposal Teams'e
   👤 Levent · 🔗 Danışman onayı (16 Ekim) · ⏰ 18 Ekim
*A0.9* GitHub private repo (Pro) + Azure Boards (Scrum) + erişimler + backlog içe aktarımı
   👤 Levent · 🔗 ADR-005, plan/board/ · ⏰ 10 Ekim

*Aşama 1 — Temel (19 Ekim → 1 Kasım)*
*A1.1* Kök AGENTS.md + docs/anayasa.md (kök kısmı 18 Ekim'e kadar) + modül AGENTS.md'ler + .claude/rules, Codex, Antigravity ayarları
   👤 Levent · 🔗 A0.9 · ⏰ 29 Ekim
*A1.2* CI kapıları: build/test, Modulith verify, ArchUnit, lint, gitleaks, oasdiff, veri doğrulayıcıları
   👤 Levent · 🔗 A1.1 · ⏰ 29 Ekim
*A1.3* Backend iskeleti: Boot 4.1 + Modulith modülleri (boş; 18 Ekim'e kadar) + Flyway + Testcontainers
   👤 Levent (iskelet) · Hilal (veritabanı) · 🔗 A0.9 · ⏰ 29 Ekim
*A1.4* Karar kaydı (Decision Record) + audit (log/metrik şeması + kanarya testi en geç 13 Kasım)
   👤 Levent · 🔗 A1.3 · ⏰ 1 Kasım
*A1.5* Sentetik hane üreteci + Git'te seed verisi + ortak staging DB (Contabo)
   👤 Hilal · 🔗 A1.3 · ⏰ 1 Kasım
*A1.6* OpenAPI sözleşme iskeleti + üretilmiş TS istemcisi (Orval)
   👤 Levent (sözleşme) · Ozan (istemci) · 🔗 A1.3 · ⏰ 1 Kasım
*A1.7* Mobil iskeleti (Expo), tasarım token'ları, ui-core (hüküm rozeti + kısıt çipleri); web/admin iskeleti A2.12'de
   👤 Ozan · 🔗 A1.6 · ⏰ 1 Kasım
*A1.8* Walking skeleton: mobil → API → DB → cevap (tek ekran, uçtan uca; yerelde, staging A1.11 ile)
   👤 Ekip · 🔗 A1.3, A1.6, A1.7 · ⏰ 1 Kasım
*A1.9* EVREN denemesi: Türkçe tool-call doğruluğu, p95, gömme boyutu, kullanım şartları
   👤 Levent · 🔗 A0.4 · ⏰ 30 Ekim (ücretsiz dönem)
*A1.10* Teknoloji denemeleri: OR-Tools native Docker imajı, JUnit 6 + jqwik/PIT uyumu (test araçları Sprint 1'de, en geç 13 Kasım; Expo barkod + Türkçe STT denemesi A2.8'in ilk işi)
   👤 Levent (OR-Tools) · Hilal (test) · 🔗 A1.3 · ⏰ 1 Kasım
*A1.11* Contabo sunucu kurulumu: Docker Compose, Caddy (TLS), yedek, SOPS
   👤 Levent · 🔗 A0.9 · ⏰ 13 Kasım
*A1.12* Sağlık durumu eşik tablosu v0 (diyabet, hipertansiyon, çölyak, hamilelik; her satır kaynaklı: TGK beyan eşikleri, WHO, TÜBER)
   👤 Ozan (derleme) · Hilal (şema, onay) · 🔗 A0.6, ADR-011 · ⏰ 1 Kasım

*Aşama 2 — Güvenilir çekirdek → CSE 491 prototipi (2 Kasım → 18 Aralık)*
*A2.1* CSE 491 ara rapor + ara sunum
   👤 Ekip (derleyen Levent) · 🔗 A0.8, Aşama 1 · ⏰ ~6 Kasım ⚠️ teyit
*A2.2* Hane + üye + rıza akışları (davet, veli onayı, profil sürümü)
   👤 Hilal · 🔗 A1.4, A1.5 · ⏰ 20 Kasım
*A2.3* Kural motoru + alerjen ontolojisi + altın set v1 (n ≥ 200, FN = 0)
   👤 Hilal · 🔗 A0.6, A1.4 · ⏰ 27 Kasım
*A2.16* Sağlık durumu kuralları kural motorunda (besin eşiği → Dikkat / Doğrulanamadı) + test seti (%100 tablo uyumu)
   👤 Hilal · 🔗 A1.12, A2.3 · ⏰ 9 Aralık
*A2.4* Katalog v0: Migros (SKU, paket, fiyat, fiyat yaşı)
   👤 Hilal · 🔗 A0.6, A1.5 · ⏰ 20 Kasım
*A2.5* 60 tarif + bu tariflerin malzemelerinde Migros fiyatlı SKU kapsaması ≥ %90
   👤 Ozan (içerik) · Hilal (onay) · 🔗 A0.6, A2.4 · ⏰ 27 Kasım
*A2.6* TR model karar kapısı (EVREN birincil mi)
   👤 Levent · 🔗 A1.9 · ⏰ 15 Kasım
*A2.7* Planlama motoru (MSM) — sentetik veriyle geliştirme, 60 tarif gelince gerçek veriyle ilk sürüm + E1 v0 ölçümü
   👤 Levent · 🔗 A2.3, A2.4, A2.5 · ⏰ 4 Aralık
*A2.8* Raf: barkod → hane şeridi + "Neden?" (mobil; önce Expo barkod gecikmesi + Türkçe STT denemesi)
   👤 Ozan (arayüz) · Hilal (API) · 🔗 A2.2, A2.3, A2.4, A1.7 · ⏰ 9 Aralık
*A2.9* Liste + Akıllı Takas (mobil + API)
   👤 Levent (motor) · Ozan (arayüz) · 🔗 A2.7 · ⏰ 9 Aralık
*A2.10* Gizlilik Kapısı v0 (sözlük, yer tutucu, eksiz şablon)
   👤 Levent · 🔗 A1.4 · ⏰ 9 Aralık
*A2.11* Asistan v1: 3–5 iş akışı niyeti ("X yiyebilir mi", listeye ekle, takas öner, neden)
   👤 Levent · 🔗 A2.8, A2.9, A2.10 · ⏰ 16 Aralık
*A2.12* Web/admin iskeleti (Vite + React) + Admin v0: karar izi + audit + katalog onayı + Sözleşme panosu
   👤 Hilal (backend) · Ozan (arayüz) · 🔗 A1.4, A2.3, A2.4 · ⏰ 16 Aralık
*A2.13* E2 ilk koşu ("neden LLM yetmez", 50 senaryo)
   👤 Levent · 🔗 A2.7, A2.11 · ⏰ 18 Aralık
*A2.14* CSE 491 final raporu + çalışan prototip demosu
   👤 Ekip (derleyen Levent) · 🔗 A2.7–A2.12 · ⏰ ~18 Aralık ⚠️ teyit
*A2.15* Yük dengesi değerlendirmesi (bileşen sahipliği)
   👤 Ekip · 🔗 A2.14 · ⏰ 18 Aralık

*Aşama 3 — Kış kampı (4 Ocak → 31 Ocak)*
*A3.1* 120 tarif + A101 fiyatları (2. zincir)
   👤 Ozan · Hilal · 🔗 A2.5 · ⏰ 15 Ocak
*A3.2* Menü planlayıcı üründe: 5 akşam, ≤2 market, zaman sınırlı exact + boşluk rozeti
   👤 Levent · 🔗 A2.7, A3.1 · ⏰ 29 Ocak
*A3.3* Kiler: barkod "eve girdi", e-Arşiv/fiş, "bitti", tükenme modeli v0
   👤 Hilal · 🔗 A2.4, A0.2 · ⏰ 29 Ocak
*A3.4* Beta protokolü + rıza/aydınlatma metinleri + (gerekirse) etik kurul başvurusu
   👤 Ekip (derleyen Levent) · 🔗 Güz görüşmelerinin cevapları · ⏰ 15 Ocak
*A3.5* KVKK: uzman görüşü + Contabo standart sözleşme denemesi + yerel-öncelikli kısıt tasarım kararı
   👤 Levent · Hilal · 🔗 ADR-008 · ⏰ 31 Ocak
*A3.6* Raf fotoğrafı denemesi (en fazla 1 hafta, zaman kutulu)
   👤 Ozan · 🔗 A2.8 · ⏰ 31 Ocak
*A3.7* RAG içerik eşleme önerisi (pgvector) + "Neden?"te kaynak alıntısı; altın sette tam/bulanık eşlemeye karşı ölçüm
   👤 Levent (· Hilal onay akışı) · 🔗 A1.9, A2.16 · ⏰ 29 Ocak

*Aşama 4 — Döngü + wow (1 Şubat → 5 Mart)*
*A4.1* 200 tarif
   👤 Ozan · Hilal · 🔗 A3.1 · ⏰ 1 Mart
*A4.2* Gizlilik Kapısı v1 + TR rotası (kanarya/sızıntı testleri)
   👤 Levent · 🔗 A2.10, A2.6 · ⏰ 1 Mart
*A4.3* Proaktif Pazar planı + onay akışı
   👤 Levent (motor) · Ozan (arayüz) · 🔗 A3.2, A3.3 · ⏰ 26 Şubat
*A4.4* Market bölme (≤2 zincir)
   👤 Levent · 🔗 A3.2, A3.1 · ⏰ 26 Şubat
*A4.5* Doğal dille kısıt ("anladığım şu")
   👤 Levent · 🔗 A4.2 · ⏰ 5 Mart
*A4.6* Web Planlama Stüdyosu + sağlığın/israfın fiyatı + "Bu plan neden böyle?"
   👤 Ozan (arayüz) · Levent (API) · 🔗 A3.2 · ⏰ 5 Mart
*A4.7* Öneri sistemi v1 (kısıt-farkında, beğeni puanı → motor)
   👤 Hilal · 🔗 A3.2 · ⏰ 5 Mart
*A4.8* Fiş eşleştirme v1 + moderasyon kuyruğu
   👤 Hilal (backend) · Ozan (admin arayüz) · 🔗 A3.3 · ⏰ 5 Mart
*A4.9* Röntgen modu
   👤 Ozan · Levent · 🔗 A1.4 · ⏰ 5 Mart
*A4.10* Beta işe alımı (20–40 hane, ≥10'unda kesin kısıt) + TestFlight dağıtımı
   👤 Ekip · 🔗 A3.4 · ⏰ 5 Mart

*Aşama 5 — Sertleştirme + demo şeridi (8 Mart → 26 Mart; 8–11 Mart bayram)*
*A5.1* Red-team (prompt injection, fiziksel etiket), chaos, yük testi ("Pazar 09:00")
   👤 Levent · Hilal · 🔗 Aşama 4 · ⏰ 24 Mart
*A5.2* App Store gönderimi (TestFlight → yayın)
   👤 Ozan · 🔗 A4.10 · ⏰ 24 Mart
*A5.3* Demo şeridi (zaman kutulu): ses, içerik değişikliği radarı, raf fotoğrafı, buzdolabı onayı
   👤 Ozan · Levent · 🔗 A3.6 · ⏰ 26 Mart
*A5.4* Özellik dondurma + danışmana çalışan proje
   👤 Ekip · 🔗 Aşama 4 · ⏰ ~26 Mart ⚠️ teyit

*Aşama 6 — Beta (29 Mart → 9 Mayıs)*
*A6.1* Taban dönemi (1–2 hafta)
   👤 Ekip · 🔗 A5.4 · ⏰ 11 Nisan
*A6.2* Müdahale dönemi (4–5 hafta) + E3 ölçümleri
   👤 Ekip · 🔗 A6.1 · ⏰ 9 Mayıs
*A6.3* E1 final koşusu (20 senaryo × 30 tohum)
   👤 Levent · 🔗 A3.2 · ⏰ 9 Mayıs

*Aşama 7 — Kapanış (10 Mayıs → jüri)*
*A7.1* Final rapor + demo videosu → jüri
   👤 Ekip · 🔗 Aşama 6 · ⏰ ~14 Mayıs ⚠️ teyit
*A7.2* Poster + proje web sitesi + kullanım kılavuzu
   👤 Ozan (site) · Ekip · 🔗 A7.1 · ⏰ 21 Mayıs
*A7.3* İngilizce sunum provası (en az 2)
   👤 Ekip · 🔗 A7.1 · ⏰ Jüriden 3 gün önce
*A7.4* Düzeltilmiş rapor
   👤 Ekip · 🔗 Jüri · ⏰ Sunumdan sonra 3 gün
