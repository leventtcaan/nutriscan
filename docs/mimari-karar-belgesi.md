# NutriScan — Mimari Karar Belgesi (v1)

**Durum:** TASLAK — 17 Ekim 2026 ekip toplantısında onaylanacak · **Editör:** Levent
**Dayanak:** MR1 (2 Ekim), MR2 (9 Ekim), 16 Ekim görüşmesi · Ozan'ın normalizasyon dokümanları · Hilal'in araştırma dosyaları

> **Bu belge nasıl kullanılır?**
> Projenin **tek doğruluk kaynağıdır**. Bir soru "nasıl yapacağız?" ise cevabı buradadır. Cevap yoksa ya da yanlışsa
> grup mesajı değil, bu belgeye öneri gelir: *"X kararını şuna değiştirmeyi öneriyorum, çünkü …"* (en fazla 3 cümle).
> Kararlar yalnız Çarşamba ekip senkronunda ya da Cuma danışman görüşmesinde değişir. Her agent bu belgeyi okur.
> Durum sütunu: **ÖNERİ** (bu akşam konuşulacak) → **KARAR** (ekip onayladı, tarih).

---

## 1. Ürün

**Tek cümle:** NutriScan, paketli gıdanın içindekiler listesini ve besin tablosunu okur, kullanıcının sağlık durumu için
kaynaklı kurallarla değerlendirir ve **aynı kategorideki ürünler arasında daha iyi seçeneği** gerekçesi ve belirsizliğiyle gösterir.

**Neden bir LLM sohbetinden farklı:** tek ürünü yorumlamak bir LLM'le de yapılabilir. Bizim farkımız
(1) normalize edilmiş bir ürün kütüphanesi üzerinden **karşılaştırma**, (2) aynı ürün + aynı profil → **her zaman aynı sonuç**
(sürümlü kurallar), (3) her sonucun **kaynağı ve kapsamı** görünür. LLM karar vermez.

| Kapsamda (v1) | Kapsam dışı (v1) |
|---|---|
| Etiket fotoğrafı → OCR → içerik + besin değerleri | Barkod, Open Food Facts ürün kayıtları |
| 3 sağlık durumu: çölyak · diyabet · kronik böbrek hastalığı | Diğer hastalıklar, ilaç etkileşimi, çoklu hastalık uzlaştırma |
| 3 ürün kategorisi (bu akşam seçilecek) | Bütün market |
| Ürün kartı + "daha iyi seçenekler" | Günlük tüketim takibi, porsiyon kaydı, menü/diyet planı |
| Sonuç: **Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı** (+ "kısmi değerlendirme" notu) | "Güvenli / zararlı", teşhis, tedavi dili |

## 2. Uçtan uca akış (örnek: Selin — çölyak + diyabet, bisküvi)

```
[1] Fotoğraf → OCR → "buğday unu, şeker, glikoz şurubu, renklendirici (E102)" + besin tablosu (100 g: karb. 72 g, şekerler 48 g)
[2] Böl + türle → buğday unu: gıda hammaddesi · şeker: gıda kavramı · glikoz şurubu: karışım · E102: tekil kimyasal · 48 g: besin değeri
[3] Eşle → (a) birebir sözlük → (b) bulanık eşleşme → (c) Qdrant aday → eşik altıysa "Doğrulanamadı"
         E102 → Tartrazin (SAME_AS) · buğday unu → Buğday (CONTAINS gluten)
[4] Kurala bak → çölyak × buğday → Uygun değil (kaynak: Gıda Kodeksi gluten tanımı)
                 diyabet × karbonhidrat 72 g/100 g → kılavuz profiline göre değerlendirme + bilgi
[5] Kanıt (yalnız bilgi) → E102 için CTD ilişkileri ve JECFA değerlendirmesi, kaynak linkiyle
[6] Göster → ürün kartı + aynı kategoride profile daha uygun 3 ürün, gerekçesiyle
```

## 3. Kararlar

| # | Konu | Karar | Neden | Durum |
|---|---|---|---|---|
| K1 | Girdi | Etiket **OCR** ile okunur, kullanıcı/ekip düzeltebilir, **sistemde saklanır**; analiz saklanan metin üzerinden yapılır | MR2 ("listeler saklanır") ile Ozan'ın akışını (OCR) birleştirir | ÖNERİ |
| K2 | Pilot durumlar | Çölyak (var/yok kuralı) · diyabet (besin miktarı) · kronik böbrek (sodyum; potasyum/fosfor etikette yoksa kısmi) | İki farklı kural mekanizmasını sınar; kılavuzları net | ÖNERİ |
| K3 | Ürün vaadi | Tek ürün kararı + **aynı kategoride daha iyi seçenekler** | LLM sarmalayıcısı olmamak; ürün kütüphanesi gerektirir | ÖNERİ |
| K4 | Kimyasala inme kuralı | Bir ifade **ancak etiket tek bir maddeyi adıyla söylüyorsa** kimyasala bağlanır (E102, askorbik asit). "Doymuş yağ" sınıf, "glikoz şurubu" karışım, "buğday unu" hammadde olarak kalır | Yanlış kimyasal üretmemek; kurallar zaten o seviyede konuşur | ÖNERİ |
| K5 | Kararı kim verir | Yalnız **kural tablosu** (klinik kılavuz + kaynak + sürüm). CTD/JECFA, Qdrant, LLM karar vermez | Savunulabilirlik, tutarlılık | KARAR (MR2) |
| K6 | Doğrulama | Her kural satırını **iki ekip üyesi bağımsız** kontrol eder; iddia "kılavuza uygunluk", klinik doğrulama değil | Uzmana bağımlılık yok; iddia dürüst | ÖNERİ |
| K7 | Qdrant'ın yeri | **Yalnız eşleme hattının 3. adımı** (yedek): alias vektörleri + `concept_id` payload. Ürün, kural, kanıt PostgreSQL'de | Tek görev, ölçülebilir katkı (aç/kapa) | ÖNERİ |
| K8 | Türkçeleştirme | Veritabanları çevrilmez; **alias tablosuna yalnız gereken terimler** eklenir (bkz. §6) | En az iş, izlenebilir | ÖNERİ |
| K9 | Değerlendirme | Eşleme sınavı (100 ifade, sözlük vs hibrit) + kural sınavı (20 senaryo); finalde tek tablo (bkz. §7) | Hocanın deney isteği, ayrı faz açmadan | ÖNERİ |
| K10 | Teknoloji | Python + FastAPI (eşleme/kural servisi) · PostgreSQL · Qdrant · mobil: Expo (React Native) · OCR: cihazda metin tanıma [kütüphane ilk 20 etiketle denenip seçilecek] | Embedding/NLP ekosistemi Python'da; tek servis | ÖNERİ |
| K11 | LLM'in rolü | v1'de **yok**. Yalnız bir kerelik toplu terim çevirisinde yardımcı (insan kontrollü) | "Wrapper" algısı ve tutarsızlık riski | ÖNERİ |
| K12 | Süreç | Sade repo (README + bu belge + kod), Azure ve CI kapıları yok; kısa dallar, sahibi merge eder; haftalık ortak inceleme | Ekibe uymayan ağır süreç bırakıldı | ÖNERİ |

## 4. Veri şeması (PostgreSQL)

```
product            id, ad, marka, kategori, kaynak, tarama_tarihi
label_text         product_id, ham_icindekiler, ham_besin_tablosu, ocr_guveni, duzelten, duzeltme_tarihi
ingredient_mention id, product_id, sira, ham_metin, normalize_metin, tur, ust_mention_id   -- tur: tekil_kimyasal|kimyasal_sinif|karisim|gida_hammaddesi|besin|bilinmeyen
concept            id, tur, ad_tr, ad_en, e_kodu, cas, mesh_id, pubchem_cid
alias              id, concept_id, metin, dil, iliski, kaynak, kaynak_surumu, durum             -- iliski: SAME_AS|CONTEXTUAL|IS_A|CONTAINS|MAY_CONTAIN
mention_match      mention_id, concept_id, yontem, skor, durum                                 -- yontem: birebir|bulanik|vektor · durum: otomatik|onayli|red
nutrient_value     product_id, besin, deger, birim, baz                                        -- baz: 100g|100ml|porsiyon
condition          id, ad_tr, mesh_id
rule               id, condition_id, kural_turu, hedef, kosul, sonuc, kaynak_belge, bolum, surum,
                   kontrol_eden_1, kontrol_eden_2, eksik_veri_sonucu
evidence           concept_id, condition_id, kaynak, iliski_turu, pmid_url, kaynak_surumu         -- yalnız bilgi, karar vermez
result             product_id, condition_id, sonuc, kullanilan_kurallar, kapsam, kural_surumu, tarih
```

**Örnek satırlar:** `concept(42, tekil_kimyasal, "Tartrazin", "Tartrazine", "E102", "1934-21-0", <mesh>)` ·
`alias("sarı renklendirici" → 42, tr, SAME_AS, ekip_ceviri, onayli)` ·
`rule(çölyak, icerik_varligi, hedef: gluten içeren tahıl, sonuc: Uygun değil, kaynak: Gıda Kodeksi …)`

## 5. Veri kaynakları (v1)

| Görev | Kaynak | Kullanım | Lisans notu |
|---|---|---|---|
| E-kodu → Türkçe resmî ad | Türk Gıda Kodeksi Katkı Maddeleri Yönetmeliği | alias + concept | Resmî mevzuat; atıf |
| Türkçe ↔ İngilizce gıda adı | OFF Ingredients Taxonomy (`ingredients.txt`) | alias | ODbL — atıf, türev şartı incelenecek |
| Kimyasal kimlik | CTD Chemical Vocabulary · PubChem (eksikler, ön hazırlıkta) | concept | CTD kullanım şartları; PubChem açık |
| Kanıt (bilgi) | CTD Chemical–Disease · WHO JECFA | evidence | Atıf; yalnız listemizdeki maddeler |
| Kural | ADA 2026 / TEMD · KDIGO 2024 · Gıda Kodeksi (gluten) | rule | Kendi cümlelerimizle, bölüm atfıyla |
| Ürünler | Ekibin OCR taraması (3 kategori × ~70) | product, label_text | Kendi verimiz |
| **v1'de yok** | FooDB (CC BY-NC), ChEBI, FoodOn, UMLS | — | Kapsam ve lisans |

Her kaynak için `kaynak, sürüm/indirme tarihi, lisans, alınan alanlar` bir envanter dosyasında tutulur (Hilal).

## 6. Türkçeleştirme

1. **E-kodu köprüsü:** Türkçe ad → E-kodu → CAS → CTD. Çeviri gerekmez.
2. **OFF taksonomisi:** Türkçe girdileri doğrudan alias olur ("şeker → en:sugar").
3. **Ekip çevirisi:** ürün kütüphanesinde geçip hâlâ eşleşmeyen terimler **bir kez** toplu çevrilir, iki kişi kontrol eder,
   alias'a `kaynak: ekip_ceviri, durum: onayli` diye yazılır.
4. **Kalanlar:** çok dilli embedding ile Qdrant adımı; eşik altıysa "Doğrulanamadı".
Kullanıcıya görünen bütün metinler ekip tarafından Türkçe yazılır.

## 7. Değerlendirme

- **Eşleme sınavı:** gerçek etiketlerden 100 ifade + doğru cevap (biri yazar, öbürü kontrol eder; bazılarının cevabı "Doğrulanamadı").
  Aynı kod iki ayarla: *yalnız sözlük* ve *sözlük + Qdrant (hibrit)*. Ölçüt: doğru sayısı · cevap verme oranı · verdiği cevaplarda isabet · yanlış uydurma.
- **Kural sınavı:** 20 ürün × durum senaryosu; beklenen sonuç kılavuza göre yazılır, sistemle karşılaştırılır.
  Ölçüt: kaçırılan uyarı (en kritik) · gereksiz uyarı · "Doğrulanamadı" oranı.
- Finalde tek tablo. Ayrı deney fazı yok; bunlar kodun testleridir.

## 8. Sahiplik ve çalışma kuralları

| Kişi | Alan (son söz) |
|---|---|
| Ozan | Sözlük, eşleme hattı, Qdrant, Türkçeleştirme |
| Hilal | Kurallar, kanıt kaynakları, lisans envanteri, test setleri |
| Levent | Veri şeması, uçtan uca entegrasyon, bu belgenin editörlüğü |
| Hep birlikte | OCR ile ürün taraması (kategori başına paylaşılır) |

1. Bu belge tek doğruluk kaynağıdır; grup mesajı değil.
2. Ham agent çıktısı gruba atılmaz; öneri belgeye 3 cümleyle gelir.
3. Herkesin agent'ı bu belgeyi okur.
4. Ritim: Çarşamba ekip senkronu (30 dk) · Cuma danışman. Kararlar yalnız bu iki noktada değişir.

## 9. Teslimlere göre sıra

| Teslim | O güne kadar |
|---|---|
| **18 Ekim · Proposal** | Bu belgenin §1–§7'si proposal'a dönüşür |
| **~6 Kasım · Ara rapor** [tarih teyit] | Repo sıfırlandı · ilk 3 kategoride ürün taraması başladı · sözlük v0 · eşleme hattı (birebir + bulanık) · 100 ifadelik test ve ilk skor · çölyak kuralı |
| **~18 Aralık · Final + demo** [tarih teyit] | Qdrant adımı + karşılaştırma tablosu · diyabet ve böbrek kuralları · 20 senaryo · "daha iyi seçenekler" · mobilde OCR ile uçtan uca demo |

## 10. Bu akşam karar verilecekler

1. K1–K12: onay ya da değişiklik
2. **3 ürün kategorisi** (öneri: bisküvi/kraker · kahvaltılık gevrek · atıştırmalık)
3. TÜBİTAK 2209-A (son gün 11 Kasım): başvuruyor muyuz?
4. Proposal: kim, hangi bölüm, ne zamana?
