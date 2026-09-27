---
title: NutriScan Tez v3 — proposal adayı
updated: 2026-09-24
durum: ÖNERİ — Levent onayı bekliyor
dayanak: 01-*.md (ilk tur), 02-v2-*.md (ikinci tur: özgünlük/talep, fiş/veri, yöntem/literatür, ürün deneyimi, kırmızı takım)
---
# NutriScan — Tez v3

## 0. Nasıl buraya geldik
- **v1** (alerjen karar motoru + etiket OCR + yan optimizasyon): tek ürün seviyesinde; "kullanıcı etiketi kendi okur" sorusuna cevabı yok → Levent: sığ.
- **v2** (fiş merkezli kapalı döngü, 12+ özellik): kırmızı takım: sığ değil ama dağınık; girdi en zayıf halkaya (kâğıt fiş: barkod/gram/adet yok) bağlı; 8 aya sığmıyor (27/45).
- **v3** = v2'nin döngü anlatısı + **plan-önce optimizasyon omurgası** (kırmızı takım Çerçeve A, 35/45) + fişten ince, ölçülü bir veri dilimi.

## 1. Problem (tek paragraf)
Türkiye'de haneler yıllık **%33,8 gıda enflasyonu** (TÜİK, Ağu 2026) altında, evdeki **farklı sağlık kısıtlarını** (çocukta alerji, çölyak, şeker/tuz hedefi) aynı anda gözeterek haftalık alışveriş kararı veriyor. Tuz tüketimi önerinin 2 katı (10,2 g), enerjinin %30,6'sı ultra-işlenmiş gıdadan; 4 kişilik ailenin sağlıklı beslenme tutarı net asgari ücretin ~%133'ü (Türk-İş). Mevcut araçlar tek boyutu çözüyor: **ürün puanı** (Yuka, ÇabukBak, Sağlık Bakanlığı Nutri-Score hesaplayıcısı — 27 Ağu 2026), **fiyat** (marketfiyati, Cimri, Akakçe) ya da **tek zincirin sadakat verisi** (Migros Sağlıklı Yaşam Yolculuğu). Hiçbiri şu soruyu cevaplamıyor:
> **"Bu bütçe ve bu hanenin kısıtlarıyla, alışkanlıklarımızı en az bozarak sepetimizi ne kadar sağlıklı yapabiliriz — ve bunun bedeli kaç TL?"**

## 2. Tez (tek cümle)
NutriScan, hanenin haftalık alışveriş planını her üyenin sağlık/alerji kısıtları ve bütçeyle birlikte **en az değişiklikle** iyileştiren, bu iyileştirmenin **bedelini TL olarak** gösteren ve raf taraması ile fiş verisinden gerçekleşeni öğrenerek kendini düzelten bir **karar destek sistemidir**.

## 3. Döngü: PLANLA → AL → ÖĞREN
| Adım | Kullanıcı ne yapar | Sistem ne yapar | Derinlik |
|---|---|---|---|
| **PLANLA** (web + mobil) | Haftalık listeyi girer (şablon/geçen hafta/yazı; ses could) | Kabul-farkında minimum-sapma MILP: ≤k takas, bütçe, üye bazlı alerjen hard kısıtı, TÜBER oranları, gerekirse hane içi bölme ("glutensiz ekmek Ela'ya"); Pareto (TL × sağlık × değişiklik); ≤2 market seçimi | OR çekirdeği |
| **AL** (mobil) | Rafta barkod okutur | Hane şeridi: her üye için 4 durumlu karar ("güvenli" kelimesi yok) + plana etkisi + katalogdan uygun alternatif | Kural motoru, property test |
| **ÖĞREN** (mobil, opsiyonel) | Fişi çeker / e-Arşiv PDF'ini paylaşır | Satır → ürün eşleştirme (retrieve → rerank → çekimser kal → kullanıcı/admin onayı → zincir sözlüğü); plan vs gerçek; takas kabul modeli güncellenir; fiyatlar kataloğa akar | ML/veri |

**Tek omurga kuralı:** Her özellik ya motoru **besler** (liste, barkod, fiş, katalog, NL kısıt) ya da sonucunu **gösterir/açıklar** (takas ekranı, sağlığın fiyatı, karar izi). İkisini de yapmayan kesilir.

## 4. Derinlik — ölçülebilir katkılar
| # | Katkı | Nasıl ölçülür |
|---|---|---|
| K1 | **Çok üyeli hane için kabul-farkında minimum-sapma sepet modeli** (≤k takaslı çok-kaynak kısıtlı multiple-choice knapsack; hane bölme; "takas kimseyi kötüleştirmez") | Formülasyon + metamorfik/property testler; 0 alerjen ihlali |
| K2 | **Sağlığın fiyatı**: parametrik marjinal maliyet eğrileri (ε-taraması), "kullanıcı sabrının fiyatı" (k), "hane içi alerjenin maliyeti" | Kesin eğri; LP gevşetmesiyle karşılaştırma |
| K3 | **Exact vs NSGA-II ölçek çalışması**: tek sepet milisaniyede (SCIP 60×20 ≈ 0,012 s); soru "hangi ölçekte (hafta × market × üye) exact kırılır, GA orada ne kadar iyi?" + ≤2 market seçimi (danışmanın konum problemi alanı) | 20 senaryo × 30 seed, hypervolume/IGD+, Wilcoxon, Friedman+Holm, A12 |
| K4 | **Güvenli NL → kısıt derleyicisi** (LLM şemaya bağlı ara temsil üretir → deterministik doğrulayıcı → şablonla geri okuma → derleyici → solver; alerjen yalnız profilden, LLM gevşetemez; sağlık terimleri LLM'e gitmeden maskelenir) | Etiketli test setinde doğruluk; red-team seti |
| K5 | **Türk fiş satırı eşleştirme**: muhtemelen ilk etiketli Türkçe fiş satırı veri seti + çekimser kalabilen eşleştirici | Kapsama @ %95 hassasiyet, zincir bazında |
| K6 | **Kabul-farkında döngü**: öneri → gerçekleşen alım → hiyerarşik Bayesçi kabul modeli | Beta: takas kabul oranı, 1000 kcal başına şeker/tuz değişimi |
| SWE | Modüler monolit, Decision Record + audit log + structured logging (ilk sprintten), CI'da property/metamorfik test ve eval | Geçen yılki "admin/log" eleştirisine doğrudan cevap |

Dürüstlük ilkeleri (rapora girer): matematik yeni değil (diyet LP 1945/USDA TFP) → katkı "gerçek hane sepetine, Türkiye fiyatlarına ve kabul davranışına uyarlama"; satın alma ≠ tüketim → metrik "satın alınan 1000 kcal başına", dil "sepetin", "yediğin" değil; en yakın akademik emsal CHI 2026 "Food Information System" proposal'da anılır.

## 5. Kullanıcı tarafı — wow anları
1. **30 saniyede ilk plan**: fiş yok; Türk hane sepeti şablonundan çip seç → ilk öneri.
2. **Takas kaydırıcısı** 1 · 3 · 5: kaydırdıkça TL ve şeker canlı değişir ("3 takasla ayda 340 TL, %25 daha az şeker, Ela'nın listesiyle çakışma yok").
3. **Sağlığın fiyatı**: "Tuzu yarıya indirmek ayda 85 TL" eğrisi.
4. **Rafta hane şeridi**: tek tarama, 4 kişi, plana etkisi, daha ucuz uygun alternatif.
5. **Market bölme**: "Bunları A101'den, şunları Migros'tan — 212 TL tasarruf."
6. **Doğal dil**: "Ela için fındıksız, haftalık 6.500 TL" → kısıt çipleri (could/should).
7. **Plan vs gerçek**: "3 takastan 2'si kalıcı oldu."
8. *(could)* Mutfak enflasyonun vs TÜİK — sağlık verisi içermeyen paylaşılabilir kart.

Ton: suçlayıcı dil yok, günlük streak yok (yeme bozukluğu riski), haftalık "hane ritmi".

## 6. Platform rolleri
- **Mobil**: liste, raf taraması, fiş, bildirim.
- **Web (tam kullanıcı uygulaması)**: Planlama Stüdyosu — Pareto, kısıtlar, sağlığın fiyatı, market bölme, hane yönetimi, raporlar, diyetisyene süreli salt-okunur link.
- **Admin**: karar izi arama, audit log, katalog moderasyonu, eşleştirme kuyruğu, deney/eval paneli, KVKK talepleri.

## 7. Veri gerçeği
- **Doğrulanmış katalog v0**: pilot zincir(ler)de en çok alınan ~300 SKU; ekip fotoğraflar → vision LLM çıkarır → insan onaylar (~10–15 saat). Takaslar **yalnız** bu katalogdan.
- Ürün puanı için Bakanlık Nutri-Score'u **kullan** (yarışma).
- Fiyat: hanenin kendi fişleri + katalog fiyatları (2 haftada bir, eskime etiketi); marketfiyati için **TÜBİTAK BİLGEM'e danışman imzalı izin başvurusu (Ekim)**.
- Kategori fallback: Ciqual/USDA (TürKomp ücretli).
- Fiş: kâğıt fiş zayıf (barkod/gram/adet yok) → opsiyonel; A101/Migros e-Arşiv XML/PDF güçlü kanal.
- KVKK: profil ve geçmiş Türkiye'de; LLM'e yalnız ürün/fiş verisi, sağlık terimleri maskeli.

## 8. Kapsam dışı
Taklit/tağşiş uyarısı (parti bazlı liste, fişte parti yok → yanlış alarm), Sepet Wrapped, Gmail entegrasyonu (CASA denetimi), tabak kalorisi, CGM/Health Connect, markete sepet aktarma, tam diyetisyen paneli, yemek planı.

## 9. Kilometre taşları
- **Ocak (CSE 491 sonu)**: liste → tek amaçlı takas (açıklamalı) → rafta hane kararı; katalog v0; admin v0 (karar izi + audit + katalog onayı); formülasyon + notebook'ta ilk exact vs NSGA-II; ≥100 etiketli fiş + baseline eşleştirme ölçümü.
- **Nisan başı (feature freeze)**: Pareto + sağlığın fiyatı + market seçimi + fiş hattı v1 + web Planlama Stüdyosu + NL kısıt.
- **Nisan–Mayıs**: 20–40 hanelik Antalya betası (2 hafta baz + 4 hafta müdahale), final deneyler.
- **Haziran**: rapor, poster, web sitesi, demo videosu, İngilizce prova — yeni özellik yok.

## 10. Levent'in 4 sorusuna cevap
| Soru | Cevap |
|---|---|
| "İçindekileri kendi okur zaten" | Ürünü değil **haftalık sepeti** çözüyoruz: 4 kişinin kısıtı × bütçe × 40 kalem × alternatifler arasında en az değişiklikli optimumu kimse elle bulamaz. |
| "Complexity zayıf" | K1–K6: çok kısıtlı MILP, parametrik maliyet eğrileri, exact vs GA ölçek çalışması, güvenli NL derleyici, Türkçe fiş eşleştirme, kabul modeli. |
| "SWE dersinin üstüne ne eklediniz" | Geçen yıl ürün seviyesi (tara → güvenli/riskli) + sahte haftalık rapor. Bu yıl hane sepeti seviyesi: sahte rapor gerçek bir öğrenme döngüsüne, liste optimizasyona, aile profili çok üyeli kısıta dönüştü. |
| "Nasıl bu kadar sığ" | Tek omurga + 4 ölçülebilir derinlik + 7 wow anı; ama kapsam 8 aya sığacak şekilde kesilmiş. |
