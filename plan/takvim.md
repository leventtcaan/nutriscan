---
title: NutriScan — Takvim (yalnız "en geç" tarihleri, bağımlılık sırasıyla)
updated: 2026-09-27
durum: v1.5 (27 Eyl: PBI kırılımı sonrası yük dengesi — A0.9 öne, A1.1/A1.11 tarih, A1.7/A1.10 kapsam) · v1.4 (ADR-011 → A1.12, A2.16, A3.7) — ekip incelemesi bekliyor · önceki v1.3: görüşmeler her Cuma, Teams MR teslimleri sabitlendi
dayanak: arastirma/07-tez-v5.md §8 · arastirma/06-v4-kirmizi-takim.md §6 · plan/kararlar.md (ADR-001…011) · kaynak/CSE-BitirmeProjesiEsaslari-2024-07-08.pdf
---
# Takvim

## 0. Nasıl okunur
- Her işin **tek bir tarihi** var: **en geç**. Daha erken bitmesi serbest, en geç tarihini geçmesi arkasındaki işleri geciktirir.
- Her iş **neye bağlı olduğunu** yazar; sıra bu bağımlılıklara göre dizildi. Bir iş, bağlı olduğu işler bitmeden "bitti" sayılmaz.
- Her işin bir **"kaçarsa"** satırı var: en geç tarih geçerse devreye giren önceden kararlaştırılmış yol. Böylece gecikme panik değil, plan değişikliği olur.
- **Sahip** = ADR-004'teki bileşen sahibi (L: Levent · H: Hilal · O: Ozan · E: ekip). Diğer ikisi vekil/gözden geçirici.
- Pano durumu: en geç tarihine 1 hafta kala **sarı**, geçince **kırmızı**.
- **Azure Boards'a dönüşüm (sonra):** Aşama = Epic · İş paketi (A1.3 gibi) = Feature · PBI'lar ayrı çalışmada kırılacak.

## 1. Sabit dış tarihler (pazarlıksız)
| Tarih | Ne | Kaynak |
|---|---|---|
| **2 · 16 · 30 Ekim, 13 · 27 Kasım 2026** | Teams: Meeting Record 1–5 teslimleri (görüşmeler her Cuma) | Teams |
| **18 Ekim 2026 (Pazar)** | CSE 491 Project Proposal — MS Teams (danışman onaylı) | Teams ödevi |
| **1 Kasım 2026** | EVREN ücretsiz dönemi biter (LLM çağrıları kredisiz) | evren.ssyz.org.tr |
| **~6 Kasım 2026** ⚠️ teyit | CSE 491 ara rapor + ara sunum ("vize haftası öncesi", OBS 8. hafta) | Bitirme Esasları m.8, OBS |
| **~18–20 Aralık 2026** ⚠️ teyit | CSE 491 final raporu + çalışan ilk prototip (ders bitimi) | Bitirme Esasları m.8 |
| **~8–11 Mart 2027** | Ramazan Bayramı (çalışma arası) | Takvim |
| **~26 Mart 2027** ⚠️ teyit | CSE 492 "vize öncesi kodlama tamam" → özellik dondurma | Bitirme Esasları m.9 |
| **~14 Mayıs 2027** ⚠️ teyit | CSE 492 rapor + demo videosu jüriye (sınavdan ≥10 gün önce) | Bitirme Esasları m.9 |
| **~15–19 Mayıs 2027** ⚠️ teyit | Kurban Bayramı | Takvim |
| **24 Mayıs – 4 Haziran 2027** ⚠️ teyit | Jüri sunumu (≤20 dk, İngilizce) | Akademik takvim |

## 2. Danışman görüşmeleri ve Meeting Record teslimleri
- **Görüşmeler her hafta Cuma** (danışmanla). Her görüşmenin çıktısı bir sonraki haftanın işlerine girer.
- **Teams'te 5 Meeting Record teslim tarihi (sabit):** her formu, o tarihten önceki bir Cuma görüşmesi doldurur (`kaynak/SDP Meeting Record Form.docx`: "yapılanlar / yapılacaklar", üyeler + danışman imzası). Form, görüşmeden 1 gün önce taslak olarak hazırlanır.
| Form | Teams son tarihi | Hangi görüşme(ler) | O dönemin ana konusu |
|---|---|---|---|
| MR1 | **2 Ekim** | 2 Ekim Cuma görüşmesi (25 Eylül iptal oldu) ⚠️ aynı gün yükleme | Tez v5.1 (sağlık durumu profili, ADR-011), stack kararları, takvim, ürün tanımı + gereksinim taslağı, prototip; etik kurul sorusu; KVKK uzman yönlendirmesi |
| MR2 | **16 Ekim** | 9 Ekim ve/veya 16 Ekim | Proposal taslağı ve son hali → **danışman onayı** → 18 Ekim teslim |
| MR3 | **30 Ekim** | 23 Ekim ve/veya 30 Ekim | Temel aşama (repo, CI, iskelet), EVREN denemesi, ara rapor planı |
| MR4 | **13 Kasım** | 6 Kasım ve/veya 13 Kasım | Ara rapor/sunum; güvenlik çekirdeği ve veri fabrikası; TR model karar kapısı (15 Kasım) |
| MR5 | **27 Kasım** | 20 Kasım ve/veya 27 Kasım | Kural motoru + altın set, katalog v0, 60 tarif; motorun gerçek veriyle ilk koşusu; final rapor planı |

## 3. Aşamalar ve iş paketleri (bağımlılık sırasıyla)

### Aşama 0 — Karar ve proposal (bugün → 18 Ekim)
| ID | İş | Sahip | Bağlı olduğu | En geç | Kaçarsa |
|---|---|---|---|---|---|
| A0.1 | Takvimin ekipçe onayı | E | ADR-001…011 | 30 Eylül | Taslak haliyle 2 Ekim görüşmesine götürülür |
| A0.2 | Ekip hanelerinin fiş + "bitti/attım" kaydına başlaması | E | — | 5 Ekim | Veri seti Kasım'a kayar, kiler modeli sentetikle başlar |
| A0.3 | Ürün tanımı v5.1 + FR/NFR (proposal §5) — 2 Ekim görüşmesine | L | Tez v5.1 | 1 Ekim | Görüşmeye tez v5 + FR/NFR iskeletiyle gidilir |
| A0.4 | EVREN hesabı + API anahtarı | L | — | 10 Ekim | Deneme için süre daralır (1 Kasım sınırı) |
| A0.5 | Proposal taslağı (şablon: `kaynak/CSE491_Project_Proposal_Template.docx`) — danışmana e-postayla | L (+H, O bölümleri) | A0.3, 2 Ekim görüşmesi | 9 Ekim | Taslak en geç 12 Ekim'de gider |
| A0.6 | Tarif şeması + malzeme sözlüğü v0 + alerjen ontolojisi taslağı | O (şema: H) | Tez v5.1 §7 | 16 Ekim | Tarif yazımı sözlüksüz başlar, sonra normalize edilir |
| A0.7 | Proposal son hali danışmana | L | A0.5 geri bildirimi | 14 Ekim | 16 Ekim görüşmesinde yüz yüze son düzeltme |
| A0.8 | **Proposal Teams'e** | L | Danışman onayı (16 Ekim) | **18 Ekim** | — (sabit) |
| A0.9 | GitHub private repo (Pro) + Azure Boards (Scrum) + erişimler + backlog içe aktarımı | L | ADR-005, `plan/board/` | 10 Ekim | A0.6 verisi geçici klasörde başlar, repo açılınca taşınır |

### Aşama 1 — Temel (19 Ekim → 1 Kasım)
Amaç: herkesin aynı standartla, aynı veriyle, çakışmadan çalışabileceği zemin + riskli teknolojilerin erken denenmesi.
| ID | İş | Sahip | Bağlı olduğu | En geç | Kaçarsa |
|---|---|---|---|---|---|
| A1.1 | Kök AGENTS.md + `docs/anayasa.md` (kök kısmı 18 Ekim'e kadar) + modül AGENTS.md'ler + `.claude/rules`, Codex, Antigravity ayarları | L | A0.9 | 29 Ekim | Talimatsız kod yazımı başlamaz |
| A1.2 | CI kapıları: build/test, Modulith verify, ArchUnit, lint, gitleaks, oasdiff, veri doğrulayıcıları | L | A1.1 | 29 Ekim | Kapılar olmadan merge yasak |
| A1.3 | Backend iskeleti: Boot 4.1 + Modulith modülleri (boş; 18 Ekim'e kadar) + Flyway + Testcontainers | L (iskelet) · H (veritabanı) | A0.9 | 29 Ekim | Boot 4.0 + sonra yükseltme (risk notu) |
| A1.4 | Karar kaydı (Decision Record) + audit (log/metrik şeması + kanarya testi en geç 13 Kasım) | L | A1.3 | 1 Kasım | Karar üreten modüller başlayamaz (bekler) |
| A1.5 | Sentetik hane üreteci + Git'te seed verisi + ortak staging DB (Contabo) | H | A1.3 | 1 Kasım | Herkes kendi test verisini üretir (geçici) |
| A1.6 | OpenAPI sözleşme iskeleti + üretilmiş TS istemcisi (Orval) | L (sözleşme) · O (istemci) | A1.3 | 1 Kasım | Arayüz mock veriyle başlar |
| A1.7 | Mobil iskeleti (Expo), tasarım token'ları, `ui-core` (hüküm rozeti + kısıt çipleri); web/admin iskeleti A2.12'de | O | A1.6 | 1 Kasım | Arayüz tek ekranla başlar |
| A1.8 | **Walking skeleton:** mobil → API → DB → cevap (tek ekran, uçtan uca; yerelde, staging A1.11 ile) | E | A1.3, A1.6, A1.7 | 1 Kasım | Aşama 2'ye geçilmez |
| A1.9 | **EVREN denemesi:** Türkçe tool-call doğruluğu, p95, gömme boyutu, kullanım şartları | L | A0.4 | **30 Ekim** (ücretsiz dönem) | Asistan bulut + yer tutucu ile başlar, TR kararı 15 Kasım'a |
| A1.10 | Teknoloji denemeleri: OR-Tools native Docker imajı, JUnit 6 + jqwik/PIT uyumu (Expo barkod + Türkçe STT denemesi A2.8'in ilk işi) | L (OR-Tools) · H (test) | A1.3 | 1 Kasım | Yedek araçlar (raporda listeli) |
| A1.11 | Contabo sunucu kurulumu: Docker Compose, Caddy (TLS), yedek, SOPS | L | A0.9 | 13 Kasım | Staging yerelde |
| A1.12 | Sağlık durumu eşik tablosu v0 (diyabet, hipertansiyon, çölyak, hamilelik; her satır kaynaklı: TGK beyan eşikleri, WHO, TÜBER) | O (derleme) · H (şema, onay) | A0.6, ADR-011 | 1 Kasım | Kural motoru yalnız alerjen + çölyakla başlar, sağlık kuralları Aralık'a |

### Aşama 2 — Güvenilir çekirdek → CSE 491 prototipi (2 Kasım → 18 Aralık)
Sıra mantığı: önce **veri + güvenlik** (her şey onların üstünde), sonra **raf ve plan**, sonra **asistan ve admin**.
| ID | İş | Sahip | Bağlı olduğu | En geç | Kaçarsa |
|---|---|---|---|---|---|
| A2.1 | **CSE 491 ara rapor + ara sunum** | E (derleyen L) | A0.8, Aşama 1 | **~6 Kasım** ⚠️ teyit | — (sabit) |
| A2.2 | Hane + üye + rıza akışları (davet, veli onayı, profil sürümü) | H | A1.4, A1.5 | 20 Kasım | Tek üyeli hane ile devam |
| A2.3 | Kural motoru + alerjen ontolojisi + altın set v1 (n ≥ 200, FN = 0) | H | A0.6, A1.4 | 27 Kasım | Raf kararı yalnız "Doğrulanamadı" + kesin eşleşmelerle çalışır |
| A2.16 | Sağlık durumu kuralları kural motorunda (besin eşiği → Dikkat / Doğrulanamadı) + test seti (%100 tablo uyumu) | H | A1.12, A2.3 | 9 Aralık | Yalnız diyabet + hipertansiyon (şeker, tuz) |
| A2.4 | Katalog v0: Migros (SKU, paket, fiyat, fiyat yaşı) | H | A0.6, A1.5 | 20 Kasım | Katalog 150 SKU ile başlar |
| A2.5 | **60 tarif** + bu tariflerin malzemelerinde Migros fiyatlı SKU kapsaması ≥ %90 | O (içerik) · H (onay) | A0.6, A2.4 | 27 Kasım | Planlama motoru ilk ölçümü 40 tarifle |
| A2.6 | TR model karar kapısı (EVREN birincil mi) | L | A1.9 | 15 Kasım | Bulut + yer tutucu rotası sürer |
| A2.7 | Planlama motoru (MSM) — sentetik veriyle geliştirme, 60 tarif gelince gerçek veriyle ilk sürüm + E1 v0 ölçümü | L | A2.3, A2.4, A2.5 | 4 Aralık | Tek sepet takası (Akıllı Takas) ile prototipe girer |
| A2.8 | Raf: barkod → hane şeridi + "Neden?" (mobil; önce Expo barkod gecikmesi + Türkçe STT denemesi) | O (arayüz) · H (API) | A2.2, A2.3, A2.4, A1.7 | 9 Aralık | Tek üye için karar |
| A2.9 | Liste + Akıllı Takas (mobil + API) | L (motor) · O (arayüz) | A2.7 | 9 Aralık | Takas yalnız web'de gösterilir |
| A2.10 | Gizlilik Kapısı v0 (sözlük, yer tutucu, eksiz şablon) | L | A1.4 | 9 Aralık | Asistan yalnız sentetik hanelerle çalışır |
| A2.11 | Asistan v1: 3–5 iş akışı niyeti ("X yiyebilir mi", listeye ekle, takas öner, neden) | L | A2.8, A2.9, A2.10 | 16 Aralık | Serbest sohbet yok, yalnız iş akışları |
| A2.12 | Web/admin iskeleti (Vite + React) + Admin v0: karar izi + audit + katalog onayı + Sözleşme panosu | H (backend) · O (arayüz) | A1.4, A2.3, A2.4 | 16 Aralık | Admin salt okunur |
| A2.13 | E2 ilk koşu ("neden LLM yetmez", 50 senaryo) | L | A2.7, A2.11 | 18 Aralık | Ocak kampına kayar |
| A2.14 | **CSE 491 final raporu + çalışan prototip demosu** | E (derleyen L) | A2.7–A2.12 | **~18 Aralık** ⚠️ teyit | — (sabit) |
| A2.15 | Yük dengesi değerlendirmesi (bileşen sahipliği) | E | A2.14 | 18 Aralık | Ocak ilk haftasına |

### Aşama 3 — Kış kampı (4 Ocak → 31 Ocak)
| ID | İş | Sahip | Bağlı olduğu | En geç | Kaçarsa |
|---|---|---|---|---|---|
| A3.1 | **120 tarif** + A101 fiyatları (2. zincir) | O · H | A2.5 | 15 Ocak | Menü 60–90 tarifle çıkar |
| A3.2 | Menü planlayıcı üründe: 5 akşam, ≤2 market, zaman sınırlı exact + boşluk rozeti | L | A2.7, A3.1 | 29 Ocak | Tek market ile |
| A3.3 | Kiler: barkod "eve girdi", e-Arşiv/fiş, "bitti", tükenme modeli v0 | H | A2.4, A0.2 | 29 Ocak | Yalnız barkod + "bitti" |
| A3.4 | Beta protokolü + rıza/aydınlatma metinleri + (gerekirse) etik kurul başvurusu | E (derleyen L) | Güz görüşmelerinin cevapları | 15 Ocak | Beta ertelenir → kapanış daralır |
| A3.5 | KVKK: uzman görüşü + Contabo standart sözleşme denemesi + yerel-öncelikli kısıt tasarım kararı | L · H | ADR-008 | 31 Ocak | Beta öncesi TR sunucu geri dönüş yolu (ADR-008) |
| A3.6 | Raf fotoğrafı denemesi (en fazla 1 hafta, zaman kutulu) | O | A2.8 | 31 Ocak | Demo şeridinden düşer |
| A3.7 | RAG içerik eşleme önerisi (pgvector) + "Neden?"te kaynak alıntısı; altın sette tam/bulanık eşlemeye karşı ölçüm | L (· H onay akışı) | A1.9, A2.16 | 29 Ocak | Eşleme sözlük + bulanık eşleme ile; RAG D2'ye |

### Aşama 4 — Döngü + wow (1 Şubat → 5 Mart)
| ID | İş | Sahip | Bağlı olduğu | En geç | Kaçarsa |
|---|---|---|---|---|---|
| A4.1 | **200 tarif** | O · H | A3.1 | 1 Mart | 150 tarifle beta |
| A4.2 | Gizlilik Kapısı v1 + TR rotası (kanarya/sızıntı testleri) | L | A2.10, A2.6 | 1 Mart | Asistan hane bağlamında şablon moduna iner |
| A4.3 | Proaktif Pazar planı + onay akışı | L (motor) · O (arayüz) | A3.2, A3.3 | 26 Şubat | Kullanıcı planı elle tetikler |
| A4.4 | Market bölme (≤2 zincir) | L | A3.2, A3.1 | 26 Şubat | Tek zincir |
| A4.5 | Doğal dille kısıt ("anladığım şu") | L | A4.2 | 5 Mart | Form ile kısıt girişi |
| A4.6 | Web Planlama Stüdyosu + sağlığın/israfın fiyatı + "Bu plan neden böyle?" | O (arayüz) · L (API) | A3.2 | 5 Mart | Stüdyo salt okunur |
| A4.7 | Öneri sistemi v1 (kısıt-farkında, beğeni puanı → motor) | H | A3.2 | 5 Mart | Öneri v0 (popülerlik) |
| A4.8 | Fiş eşleştirme v1 + moderasyon kuyruğu | H (backend) · O (admin arayüz) | A3.3 | 5 Mart | Fiş yalnız kategori düzeyinde |
| A4.9 | Röntgen modu | O · L | A1.4 | 5 Mart | Admin karar izi ile gösterilir |
| A4.10 | Beta işe alımı (20–40 hane, ≥10'unda kesin kısıt) + TestFlight dağıtımı | E | A3.4 | 5 Mart | 15 hane ile beta |

### Aşama 5 — Sertleştirme + demo şeridi (8 Mart → 26 Mart; 8–11 Mart bayram)
| ID | İş | Sahip | Bağlı olduğu | En geç | Kaçarsa |
|---|---|---|---|---|---|
| A5.1 | Red-team (prompt injection, fiziksel etiket), chaos, yük testi ("Pazar 09:00") | L · H | Aşama 4 | 24 Mart | Bulgular betada düzeltilir |
| A5.2 | App Store gönderimi (TestFlight → yayın) | O | A4.10 | 24 Mart | Beta TestFlight üzerinden |
| A5.3 | Demo şeridi (zaman kutulu): ses, içerik değişikliği radarı, raf fotoğrafı, buzdolabı onayı | O · L | A3.6 | 26 Mart | Yalnız demoda, betaya girmez |
| A5.4 | **Özellik dondurma** + danışmana çalışan proje | E | Aşama 4 | **~26 Mart** ⚠️ teyit | — (sabit) |

### Aşama 6 — Beta (29 Mart → 9 Mayıs)
| ID | İş | Sahip | Bağlı olduğu | En geç | Kaçarsa |
|---|---|---|---|---|---|
| A6.1 | Taban dönemi (1–2 hafta) | E | A5.4 | 11 Nisan | Taban 1 haftaya iner |
| A6.2 | Müdahale dönemi (4–5 hafta) + E3 ölçümleri | E | A6.1 | 9 Mayıs | Kısa müdahale, dürüst raporlama |
| A6.3 | E1 final koşusu (20 senaryo × 30 tohum) | L | A3.2 | 9 Mayıs | Daha az senaryo, raporda belirtilir |

### Aşama 7 — Kapanış (10 Mayıs → jüri)
| ID | İş | Sahip | Bağlı olduğu | En geç | Kaçarsa |
|---|---|---|---|---|---|
| A7.1 | Final rapor + demo videosu → jüri | E | Aşama 6 | **~14 Mayıs** ⚠️ teyit | — (sabit) |
| A7.2 | Poster + proje web sitesi + kullanım kılavuzu | O (site) · E | A7.1 | 21 Mayıs | — |
| A7.3 | İngilizce sunum provası (en az 2) | E | A7.1 | Jüriden 3 gün önce | — |
| A7.4 | Düzeltilmiş rapor | E | Jüri | Sunumdan sonra 3 gün | — (sabit) |

## 4. Kritik yol
`A0.6 şema/sözlük` → `A2.4 katalog` + `A2.5 60 tarif` → `A2.7 motor gerçek veriyle` → `A3.1 120 tarif` → `A3.2 menü planlayıcı` → `A4.3 proaktif plan` → `A5.4 dondurma` → `A6 beta` → `A7.1 rapor`.
Yan yollar: güvenlik (`A2.3` → `A2.8` → admin), asistan (`A1.9` → `A2.6` → `A2.10` → `A4.2` → `A4.5`), beta ön koşulları (`A3.4`, `A3.5` → `A4.10`).

## 5. Teyit edilecek tarihler (danışman / bölüm)
CSE 491 ara rapor ve final rapor tarihleri · Mühendislik güz ve bahar vize haftaları · 492 "kodlama tamam" tarihi · jürinin tarihi · bahar dönemi görüşme sayısı ve son tarihi · Kurban Bayramı.
