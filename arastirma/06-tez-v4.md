---
title: NutriScan Tez v4 — Evin gıda asistanı
updated: 2026-09-24
durum: ÖNERİ — Levent onayı bekliyor
dayanak: 04-vizyon-v4-tohum.md · 05-ai-native-rakip.md · 05-agent-mimarisi.md · 05-menu-kiler-oneri.md (+ bench) · 05-akislar-edge-case.md · 05-sistem-fmea.md · önceki 01–03
---
# NutriScan Tez v4

## 0. Evrim
v1 sığ (ürün tek başına) → v2 dağınık (fiş merkezli) → v3 derin ama dar ve AI'sız (liste optimizasyonu) → **v4: hanenin tüm gıda döngüsünü yöneten, görünür bir asistan; kararları doğrulanabilir motorlarda.** v3'ün bütün derinliği korunur; üstüne menü, kiler, asistan, gizlilik ve öneri katmanları gelir.

## 1. Pazar gerçeği (Eylül 2026)
- "Sohbetle menü → liste → sepet" artık sıradan: **Migros MAYA AI** (Temmuz 2026, OpenAI; menü, tarif, sepete ekleme, bitmek üzere hatırlatma, ChatGPT içinde), CarrefourSA Alista, Getir Hazır Sepet; dünyada Walmart Sparky, Instacart Clementine, Kroger/Gemini, Amazon Alexa for Shopping, Ollie, Samsung Food.
- Buzdolabı fotoğrafı, "evdeki malzemeyle tarif", liste fotoğrafı standartlaştı → veri girişi olabilir, **wow değil**.
- Bu aramada bulunamayan üç şey (= bizim alanımız):
  1. Kısıtları **hane üyesi bazında kural motoruyla doğrulayan** ve kararın izini gösteren asistan (rakiplerde kısıt = filtre/tercih).
  2. **Zincirden bağımsız hane grafiği** (kiler + çok zincirli alım + üye kısıtları tek yerde; büyük oyuncular yalnız kendi kasasını görür).
  3. Planı gerçekleşenle karşılaştırıp **optimizasyonla öğrenen** döngü.
- Görünür AI kanıtı: akıl yürütmeyi göstermek güveni artırır ama aşırı güven de doğurur; "yapay zekâ" etiketi satın alma niyetini düşürebilir; seyrek ve onay isteyen proaktiflik çalışır. → **Görünür yüz = asistan + doğrulanabilir karar izi**, "AI" etiketi değil.

## 2. Problem
Türkiye'de haneler her hafta aynı yorucu kararı sıfırdan veriyor: **ne pişireceğiz, ne alacağız, nereden, evde ne var, kime uygun?** Bunu yıllık %33,8 gıda enflasyonu (TÜİK, Ağu 2026), evdeki farklı sağlık kısıtları (çocukta alerji, çölyak, şeker/tuz hedefi) ve kişi başı yüksek israf (UNEP 2024 tahmini ~102 kg/yıl, düşük güvenli) altında yapıyor. Marketlerin asistanları **satıcının tarafında**: kendi zincirinin sepetini doldurur; basın metinlerinde üye bazlı kısıt doğrulaması geçmiyor; verinin nerede işlendiği açıklanmıyor (MAYA OpenAI ile geliştirildi).

## 3. Tez
> **NutriScan, hanenin tarafında duran, zincirden bağımsız bir gıda asistanıdır: haftalık menüyü, listeyi ve market seçimini evdeki herkesin kısıtlarıyla, bütçeyle ve kilerle birlikte tek bir optimizasyonla planlar; rafta ve mutfakta her kararını kanıtlarıyla gösterir; hanenin sağlık verisini Türkiye'den çıkarmaz.**

Konumlanma cümlesi: *"Migros'un asistanı Migros sepetini doldurur. NutriScan hanenin tarafındadır."*

## 4. Döngü: MENÜ → LİSTE → MARKET → MUTFAK → ÖĞREN
| Adım | Kullanıcı deneyimi | Motor | Görünür AI |
|---|---|---|---|
| **Menü** | Pazar sabahı "Haftalık planın hazır: 5 akşam yemeği, 1.850 TL, Ela için fındıksız, kilerdeki yoğurt ve ıspanak kullanıldı — onaylar mısın?" | **Birleşik Menü–Sepet–Market (MSM) optimizasyonu** + öneri sistemi (beğeni puanı) | Proaktif plan kartı; doğal dille değişiklik ("misafir var, 7.000 TL") |
| **Liste** | Menüden + alışkanlıktan otomatik liste; takas kaydırıcısı 1·3·5 | Akıllı Takas (MSM içinde) | "Neden bu takas?" anlatımı |
| **Market** | ≤2 market bölme; rafta barkod → hane şeridi; sesle "Bunu Ela yiyebilir mi?" | Güvenlik kural motoru, market seçimi | Ses; raf fotoğrafı (deneysel, yalnız kırmızı/gri) |
| **Mutfak** | Kiler: barkod "eve girdi", fiş, e-Arşiv; "bitmek üzere"; "evde ne var, ne pişirsem" | Kiler modeli (Gamma–Poisson tükenme, SKT), tarif doğrulayıcı | Buzdolabı fotoğrafı = "hâlâ duruyor mu?" onayı |
| **Öğren** | Plan ve gerçek; kalıcı takaslar; tarif değişikliği radarı; sepet göstergesi; (could) mutfak enflasyonu | Kabul modeli, eşleştirme, bildirim | Haftalık özet, radar bildirimi |

## 5. Mimari ilke
- **LLM orkestra eder, motorlar karar verir.** Sık niyetler ("X yiyebilir mi", listeye ekle, haftalık plan) sabit iş akışı, kritik yolda LLM yok; serbest araç döngüsü yalnız uzun kuyrukta. Her kalıcı değişiklik bir **Öneri (Proposal)**, onay UI'dan gelir.
- **Hüküm rozeti yalnız karar kaydından çizilir**; LLM hüküm kelimesi üretemez; karar değişmezliği %100 ölçülür.
- **Gizlilik Kapısı (Türkiye):** hassaslık dedektörü → tipli yer tutucu (Ü2, K7) → bulut LLM → **Türkçe ek uyumlu geri doldurma**; hassas/belirsiz tur ve buzdolabı → **Türkiye'de barındırılan açık model** (EVREN / TR MaaS / kendi GPU). Bulut yolu flag ile kapatılabilir.
- **Güvenilmeyen metin** (etiket, fiş, tarif, topluluk) karantinadaki araçsız çıkarıcılardan geçer; ham hâli yetkili LLM'e gitmez. Yetki seviyeleri L0–L5; profil/rıza/paylaşım/silme LLM'e kapalı.
- Çerçeve adayı: **Spring Boot 4 + Spring AI 2.0** (stack ADR'de kesinleşecek).

## 6. Derinlik — ölçülebilir katkılar
| # | Katkı | Kanıt / ölçüm |
|---|---|---|
| C1 | **Birleşik Menü–Sepet–Market optimizasyonu** (atama + tamsayı örtü + tesis seçimi + MMKP; güçlü NP-zor) | [sentetik] 60 sn'de optimallik boşluğu %5–40; "önce menü sonra liste" %2–42 daha pahalı → exact vs NSGA-II için dürüst sahne (20 senaryo × 30 tohum) |
| C2 | Kabul-farkında minimum-sapma takas + **sağlığın fiyatı** + **hane içi alerjinin maliyeti** + israfın fiyatı | Parametrik maliyet eğrileri |
| C3 | **Doğrulanabilir agent**: araç çağrısı doğruluğu, grounding, karar değişmezliği, fiziksel etiketle prompt injection red-team | Eval harness CI'da |
| C4 | **Gizlilik-koruyan agent**: Gizlilik Kapısı + Türkçe ek uyumlu geri doldurma + bulut vs TR model kıyası | Sızıntı (kanarya) testi, ek uyumu doğruluğu, kalite farkı |
| C5 | **Türkçe veri katkısı**: alerjen/içerik çözümleme, fiş satırı eşleştirme, etiket okuma setleri (muhtemelen ilk açık Türkçe setler) | Kapsama @ %95 hassasiyet; alerjen yanlış negatifi = 0 |
| C6 | **Kısıt-farkında öneri sistemi → optimizasyona girdi** (danışmanın iki alanı tek akışta) | Önce güvensizleri ele, sonra sırala; kohort popülerliği + keşif |
| C7 | **Kiler modeli**: kategori önselli Gamma–Poisson tükenme + SKT-farkında menü | Tahmin hatası, israf değişimi |
| SWE | 20 mimari kural (K01–K20), 22 ürün sözleşmesi maddesi (S1–S22), FMEA (75 mod), SLO'lar, audit, karar izi | Otomatik kanıtlar (test/CI) |

## 7. Ürün sözleşmesi (özet — S1–S22)
S1–S7 v3'ten (Neden? her yerde, bilmediğini söyler, yargılamaz, kontrol kullanıcıda, önce değer, her durum tasarlanır, paylaşım kartında sağlık verisi yok). Yeni:
- **S8** Bilinmiyor, yok değildir. **S9** Katılaştırmak kolay, gevşetmek zor. **S10** Kesin kısıtı yalnız sahibi, yalnız profilden gevşetir (asistan/optimizasyon/mod gevşetemez).
- **S11** "Engel bulunmadı" yalnız kimliği kesin ürüne; görüntüden yalnız "Uygun değil" ya da "tara". **S12** Türkçeye ve belirsizliğe dürüst çözümleme (İ/ı, türevler, olumsuz cümle, 14 dışı alerjen → "Dikkat").
- **S13** Araç kazanır. **S14** Tıbbi sınır sabit kurallarla (doz sorusuna cevap yok, acil belirtide 112). **S15** Sohbet ve ses Türkiye'de maskelenir.
- **S16** Her karar ürün/profil/kural sürümüne bağlı; biri değişince açık plan/liste/önbellek yeniden değerlendirilir. **S17** Düzeltme sözü: karar sonradan katılaşırsa etkilenen her haneye bildirim.
- **S18** Push/ses/paylaşım üye adı + kısıtı birlikte taşımaz. **S19** Herkes kendi verisini verir. **S20** Geri alma ve silme gerçek (anahtar imhası). **S21** Asistan çökse de ürün çalışır; onaysız işlem yok. **S22** Karar yalnız renkle verilmez.

## 8. Mimari anayasa (özet — K01–K20, `05-sistem-fmea.md`)
Tek ilke: **belirsizlik riski yalnız artırır; emin değilsek "Doğrulanamadı".** Tek çıkış kapısı (maskelenmemiş veri dışarı çıkmaz), prod verisi prod dışına çıkmaz (AI kodlama ajanları dahil), hane verisi DB düzeyinde ayrık, sır repoda yok, audit silinemez, alerjenli seçenek çözücüye hiç verilmez, enum sıra numarasıyla saklanmaz, mağaza içi barkod global anahtar değil, OFF girdisi güvenilmeyen metin sayılır… Bu maddeler **ekibin agent'ları için değişmez talimat dosyalarına** ve CI testlerine dönüşecek.

## 9. Görünür AI yüzeyleri
1. **Asistan sekmesi** (yazı + ses): çalışırken adımlarını gösterir ("Katalogda arıyorum → Ela için kontrol ediyorum → 3 plan hesapladım"), her iddiası tıklanabilir karar kaydına bağlı.
2. **Pazar sabahı proaktif plan** kartı.
3. **Kamera**: etiket, fiş, raf (deneysel), buzdolabı onayı.
4. **Doğal dille plan değişikliği** ("anladığım şu, doğru mu?").
5. **Tarif değişikliği radarı** bildirimi.
6. Web'de **karar izi / "Bu plan neden böyle?"** ekranı.

## 10. Yayın dalgaları (kesme yok, sıralama var)
| Dalga | Zaman | İçerik |
|---|---|---|
| **D1 — Güvenilir çekirdek** | Ekim → Ocak (CSE 491 prototipi) | Hane + rıza; güvenlik motoru + katalog v0; raf barkodu + Neden?; liste + Akıllı Takas; asistan v1 (iş akışı niyetleri); Gizlilik Kapısı v0; admin v0 (karar izi, audit, katalog); eval harness v0; MSM modeli + benchmark (notebook); 200 tarif küratörlüğü başlar |
| **D2 — Döngü tamamlanır** | Şubat → Mart | Menü planlayıcı + birleşik MSM üründe; kiler (barkod/fiş/e-Arşiv) + tükenme modeli; proaktif Pazar planı; market bölme; web Stüdyo + sağlığın fiyatı; fiş eşleştirme; ses; tarif değişikliği radarı; öneri sistemi v1 |
| **D3 — Wow + kanıt** | Mart → Nisan başı (feature freeze) | Raf fotoğrafı (deneysel), buzdolabı onayı, NL → kısıt, TR model yolu tam, red-team, mutfak enflasyonu (could), diyetisyen linki (could) |
| **Beta** | Nisan → Mayıs | 20–40 hane Antalya (2 hafta baz + 4 hafta müdahale), final deneyler |
| **Sonrası** | — | Sepete aktarma (API yok), CGM/Health Connect, ChatGPT/MCP "hane doğrulayıcı" |

Risk (tek satır): en büyük risk kapasite; agent + harness mimarisi ve sözleşme/anayasa dosyalarıyla karşılanacak, dalgalar ölçülerek ilerleyecek.

## 11. Levent'in soruları → cevap
| Soru | Cevap |
|---|---|
| "Kendi okur zaten" | Tek ürünü değil, **haftayı** çözüyoruz: 4 kişinin kısıtı × bütçe × kiler × 100 tarif × 2 market — birleşik problem 60 sn'de bile kanıtlanamıyor. |
| "Complexity zayıf" | C1–C7 + SWE; NP-zor birleşik optimizasyon, gizlilik-koruyan agent, Türkçe veri setleri. |
| "SWE dersinin üstüne ne eklediniz" | Tarama + aile + liste → tüm gıda döngüsü + asistan + optimizasyon + gizlilik + kanıtlı karar. |
| "AI görünür değil" | Asistan ürünün yüzü: sohbet, ses, kamera, proaktif plan, radar; ama her iddiası kanıtlı. |
| "Migros MAYA varken neden?" | MAYA satıcının tarafında ve tek zincirli; basın metinlerinde üye bazlı kısıt doğrulaması yok; OpenAI ile geliştirildi, veri işleme yeri açıklanmamış. NutriScan hanenin tarafında, zincirden bağımsız, kanıtlı ve verisi Türkiye'de. |
