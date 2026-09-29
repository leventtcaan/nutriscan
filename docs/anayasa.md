---
title: NutriScan anayasası — ürün sözleşmesi (S) + mimari kurallar (K) + sağlık dili
updated: 2026-09-29
durum: KABUL (tez v4/v5.1, ADR-001, ADR-011) — değişiklik yalnız ADR ile
kaynak: arastirma/06-tez-v4.md §7–8 · arastirma/05-sistem-fmea.md §8 · arastirma/05-akislar-edge-case.md · plan/kararlar/ADR-011
---
# Anayasa

Tek ilke: **belirsizlik riski yalnız artırır; emin değilsek "Doğrulanamadı".**
Bu dosya agent'lar için değişmez talimattır; her maddenin yanında onu zorlayan test/kapı yazılıdır (henüz yoksa hangi PBI'da geleceği).
Madde eklemek, kaldırmak ya da gevşetmek = yeni ADR + ekip onayı.

## 1. Ürün sözleşmesi (S1–S22) — kullanıcıya verilen söz
| # | Kural | Nerede zorlanır |
|---|---|---|
| S1 | Her karar ve öneri "Neden?" taşır: eşleşen içerik, kural + sürüm, kaynak, tarih, güven, profil sürümü. | UI–karar kaydı sözleşme testi (A1.4-a, A2.8-b) |
| S2 | Bilmediğini söyler; tahmin yürütmez. | Kural motoru property testleri (A2.3-a) |
| S3 | Yargılamaz: kişiyi değil sepeti konuşur; "kötü/zararlı/riskli" yok; çocuğa skor yok. | Metin şablonu yasaklı kelime testi (A2.16-a) |
| S4 | Kontrol kullanıcıda: onaysız hiçbir şey değişmez (plan, liste, takas). | Asistan onay kartı testi (A2.11-a) |
| S5 | Önce değer: sağlık bilgisi ilk değer görüldükten ve ihtiyaç anında, izinle istenir. | Onboarding akış testi (A2.2-d) |
| S6 | Her durum tasarlanır: boş, hata, yavaş, çevrimdışı, katalogda yok, plan çıkmadı. | Ekran kabul kriterleri |
| S7 | Paylaşım kartında ve bildirimde sağlık verisi yok. | Bildirim şablon testi |
| S8 | **Bilinmiyor, yok değildir:** kısıtı girilmemiş/rızası olmayan üyeye "Engel bulunmadı" gösterilmez. | Property test (A2.3-a) |
| S9 | Katılaştırmak kolay, gevşetmek zor. | Profil API testi (A2.2-b) |
| S10 | Kesin kısıtı yalnız sahibi (çocukta veli), yalnız profil ekranından gevşetir; asistan, optimizasyon, mod gevşetemez. | Property + red-team (A2.2-b, A2.11-a) |
| S11 | "Engel bulunmadı" yalnız kimliği kesin ürüne; görüntüden yalnız "Uygun değil" ya da "barkodu tara". | Raf API testi (A2.8-b) |
| S12 | Türkçeye ve belirsizliğe dürüst çözümleme: İ/ı, türevler, olumsuz cümle ("içermez"), 14 dışı alerjen → "Dikkat". | Altın set (A2.3-b) |
| S13 | Araç kazanır: LLM anlatımı motor kararıyla çelişirse motor geçerli, anlatım düşer. | Claim checker eval'i (A2.11-a) |
| S14 | Tıbbi sınır sabit kurallarla: doz/tolerans sorusuna cevap yok, akut belirtide 112; LLM'e gitmez. | Sabit yanıt testi (A2.11-a) |
| S15 | Sohbet ve ses Türkiye'de maskelenir (Gizlilik Kapısı). | Kanarya testi (A2.10-a) |
| S16 | Her karar ürün/profil/kural sürümüne bağlı; biri değişince açık plan/liste/önbellek yeniden değerlendirilir. | Olay testi (A2.2-b, A1.4-a) |
| S17 | Düzeltme sözü: karar sonradan katılaşırsa etkilenen her haneye bildirim gider. | Admin etki analizi testi (A2.12-b) |
| S18 | Push/ses/paylaşım üye adı + kısıtı birlikte taşımaz. | Bildirim şablon testi |
| S19 | Herkes kendi verisini verir; başkası adına yetişkin sağlık verisi girilmez. | Davet akışı testi (A2.2-b) |
| S20 | Geri alma ve silme gerçektir (anahtar imhası). | Silme testi (A2.2-c) |
| S21 | Asistan çökse de ürün çalışır; LLM'siz mod vardır. | Chaos testi (LLM kapalı) |
| S22 | Karar yalnız renkle verilmez: ikon + metin + renk. | UI bileşen testi (A1.7-b) |

## 2. Mimari kurallar (K01–K21)
| # | Kural | Kapattığı FM | Kanıt |
|---|---|---|---|
| **K01** | **LLM hiçbir uygunluk kararını, kısıtı, fiyatı, kiler miktarını ve optimizasyon sonucunu üretemez ya da değiştiremez.** Kullanıcıya görünen her hüküm rozeti yalnız Decision Record'dan çizilir. | LLM-01, 02, 05, 06, 07 | ArchUnit (LLM modülünden karar yazma API'sine bağımlılık yok); UI bileşen testi (rozet yalnız DR alır) |
| **K02** | Asistanın her olgusal iddiası (ürün, sayı, üye–hüküm) bir araç çıktısı ID'sine bağlanır; bağlanamayan cümle claim checker'da düşer. "Güvenli" kelimesi hiçbir yüzeyde yok. | LLM-01, 02, 16 | Eval'de sadakat %100; prod blok oranı SLI |
| **K03** | **Güvenlik monotonluğu:** eksik, eski, çelişkili ya da tanınmayan veri riski yalnız artırır. LLM, NL derleyici, topluluk, önbellek ve görsel tanıma sert kısıtı gevşetemez, güvence veremez. Gevşetme yalnız kısıt sahibinin (çocukta velinin) yeniden kimlik doğrulamalı profil ekranından yapılır. | KUR-01, 02, 07, LLM-09, GOR-06, VER-08 | Property testleri (10k–100k örnek); red-team gevşetme = 0 |
| **K04** | Güvenilmeyen içerik (etiket, fiş, OFF kaydı, topluluk katkısı, tarif, ürün/üye adı, görsel içi metin) talimat kanalına girmez; yalnız araçsız, şema-kısıtlı karantina çıkarıcıdan yapısal veri olarak geçer. | LLM-05–08 | Red-team injection korpusu; şema sözleşme testi |
| **K05** | Asistanın dışarıya iletişim yolu yok: URL getirme, mesaj/e-posta gönderme, dış link ve görsel render yok. Yazma araçları onay kartı + geri al ister. | LLM-03, 05, 17 | Araç envanteri testi (yasaklı araç tanımlı değil); CSP testi |
| **K06** | **Tek egress kapısı:** LLM, VLM, push, e-posta, crash/log/trace, analitik — yurt dışına çıkan her payload TR'deki maskeleme + DLP kapısından geçer; kapı kararsızsa istek düşer (fail-closed). Sağlık verisi ve kimlik yurt dışına çıkmaz. | LLM-10, GOR-03, ALT-11, 12, 15, OPS-02 | Nightly kanarya testi; maskeleme eval'i; ağ düzeyinde egress allowlist |
| **K07** | **Kiracı ayrımı:** householdId yalnız token'dan türetilir; her veri erişimi tenant-scoped repository + Postgres RLS'ten geçer; önbellek, vektör deposu ve nesne deposu anahtarları householdId taşır; haneye katılım sahip onayıyla olur. | ALT-02, 03, 04, LLM-11 | PR'da yetki matrisi; iki-hane kanarya testi; RLS testi |
| **K08** | Her görünen karar/öneri **değişmez bir Decision Record** üretir: girdi hash'i, veri kaynağı + yaşı, kural paketi hash'i, profil sürümü, model + prompt sürümü, çözücü sürümü + parametreleri. Düzeltme yeni DR + `supersedes`. | KUR-04, 05, OPT-03, OPS-01 | DR kapsama SLI = %100 |
| **K09** | Kural paketi, sözlük, prompt, model ID ve çözücü parametreleri **sürümlü config**'tir: golden set + replay + eval kapısından geçmeden yayına çıkamaz, tek komutla geri alınır. Model alias'ı yasak. | KUR-04, 05, LLM-14 | CI kapısı; rollback provası |
| **K10** | Optimizasyon çıktısı **bağımsız doğrulayıcıdan** (ayrı kod, tamsayı aritmetik, alerjen motoruyla çift kontrol) geçmeden gösterilmez. Alerjenli adaylar çözücüden önce domain'den çıkar. Metaheuristic sonucunda `isFeasible` kontrolü zorunlu. | OPT-03, 07, 08 | Doğrulayıcı ihlal sayacı = 0; CI'da FULL_ASSERT |
| **K11** | **Veri kalitesi kapısı:** fiyat > 0 ve kategori bandında; besin ≥ 0 ve fiziksel olarak tutarlı (Atwater); birim normalize. Her değer kaynak + yaş taşır. Kapıdan geçmeyen ya da TTL'i aşan veri karara ve optimizasyona girmez. | OPT-04, 05, VER-01, 09 | Fuzz testleri; tazelik SLO'su |
| **K12** | **Asimetrik moderasyon:** riski azaltan her değişiklik (alerjen/iz kaldırma, negatif sözlüğe ekleme, kural gevşetme) tek kaynaktan otomatik kabul edilmez; kanıt + iki kişi onayı gerekir. Riski artıran değişiklik hızlı yoldan geçer. | VER-03, KUR-03, 05 | Birim test; audit raporu |
| **K13** | OFF verisi ayrı ve değiştirilmemiş şemada durur; katkılarımız ayrı katmanda ve ODbL ile dışa aktarılabilir; mirror ithalatı atomiktir (staging → doğrula → swap); kişisel veri ürün DB'sine girmez. | VER-01, 02, 10 | Şema/rol testi; import doğrulama testi |
| **K14** | Her yüklenen dosya: boyut/piksel/sayfa sınırı, magic-byte doğrulama, ağsız sandbox'ta decode + yeniden encode, EXIF temizliği, XML'de DTD kapalı. Ham görsel TTL ile silinir; cihazda yüz/kart redaksiyonu yapılır. | GOR-03, 04, 05 | CI'da kötü dosya korpusu; TTL alarmı |
| **K15** | **Sırlar repoda ve istemcide yok:** pre-commit + CI + push protection sır taraması; sırlar gizli yöneticide, ortam başına ayrı, rotasyonlu. Eski projenin tüm sırları geçersiz sayılır ve rotasyon yazılı teyit edilir. | ALT-07 | gitleaks kapısı; rotasyon envanteri |
| **K16** | Audit log **append-only** (UPDATE/DELETE yetkisi yok), hash zincirli, günlük kök hash dış depoya imzalı yazılır; audit yazılamazsa işlem de olmaz; admin'in kullanıcı verisini görmesi gerekçeli ve süreli (break-glass). | ALT-08, 13 | Gece zincir doğrulaması; ArchUnit `@Audited` |
| **K17** | Her pahalı kaynak (LLM token, VLM, çözücü CPU, SMS, push) kullanıcı/hane/global kotalıdır; global bütçe devre kesicisi ve "LLM'siz mod" flag'i vardır; **çekirdek akışlar (tarama, liste, takas) LLM olmadan çalışır.** | LLM-04, 12, 13, ALT-05, OPT-02, 06 | Chaos (LLM kapalı) + yük testi |
| **K18** | **Gözlemlenebilirlik sözleşmesi:** W3C traceparent mobil → backend → LLM → çözücü uçtan uca; üç katmanlı log (teknik / domain olayı / audit) şemalı; logda sağlık verisi ve ham kişisel veri yok (allowlist + scrubbing); her zamanlanmış iş heartbeat yayar. | OPS-01, 02, 07 | Log kanarya testi; açıklama tatbikatı; dead-man's switch |
| **K19** | **Prod verisi prod dışına çıkmaz:** test/staging/demo yalnız sentetik hane üreteciyle çalışır; geliştiricilerin ve AI kodlama ajanlarının prod DB/sır erişimi yok; prod erişimi break-glass ve loglu. | OPS-06, ALT-07 | Erişim logu denetimi; ajan talimat dosyası kuralı |
| **K20** | **Her değişiklik geri alınabilir, her kurtarma kanıtlanır:** göçler expand/contract, enum'lar STRING; API N-1 mobil sürümü destekler + uzaktan min-version; deploy otomatik rollback'li; aylık restore tatbikatı; dönemde bir KVKK 72 saat tatbikatı. | OPS-04, 05, ALT-06, 09 | Tatbikat raporları; göç testleri |
| **K21** | **Dış veri toplama** *(ÖNERİ — ADR-015, ekip onayı bekliyor)*: otomatik toplama yalnız robots.txt'in izin verdiği yollardan, kendini tanıtan bot adı ve iletişimle, yapılandırmadaki hız sınırıyla; giriş, CAPTCHA, bot koruması ya da IP döndürmeyle hiçbir engel aşılmaz; kapsam tarif sözlüğüyle sınırlı, katalog aynalanmaz; her kayıt kaynak URL + tarih taşır; ham veri yeniden yayımlanmaz. **Kamuya açık canlı ürün ancak kaynağın yazılı izni ya da lisansla**; o zamana kadar veri yalnız geliştirme, deney ve demoda. Açık ret ya da itiraz gelen kaynakta toplama durur. | Veri lisansı (01-mevzuat-risk §6, arastirma/12 §6) | Adapter testleri: bot adı, robots.txt uyumu, hız sınırı, sözlük kapsamı (toplayıcı PBI'ı, A2.4) |

## 3. Sağlık durumu dili ve RAG sınırı (ADR-011)
1. Hastalık kuralları **bilgilendirme** dilindedir: "100 g'da 58 g şeker; kaynaklı 'yüksek' eşiği 22,5 g". Yasak: "zararlı", "riskli", "hastalığına iyi gelir", "tedavi", "önler", "güvenli", "doktor onaylı".
2. Teşhis sorulmaz; üye durumu kendisi seçer. Çölyak kesin kısıttır (Uygun değil); diyabet/hipertansiyon/hamilelik "Dikkat" + besin bilgisi + kaynak üretir; besin tablosu yoksa "Doğrulanamadı".
3. Her eşik satırı kaynaklı ve sürümlüdür (belge, madde, tarih, doğrulayan); kaynaksız eşik yayına çıkmaz (CI, A1.2-c).
4. **Anlamsal arama (RAG) karar yolunda yoktur:** yalnız sözlüğe eşleme **önerir** (moderatör onaylar) ve açıklamada kaynak pasajını alıntılar. Karar yalnız onaylı sözlük + sürümlü kurallarla verilir.
5. Uygulama "tıbbi cihaz değildir, teşhis/tedavi etmez" uyarısını taşır.
