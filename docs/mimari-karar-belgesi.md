# NutriScan — Mimari Karar Belgesi (v1)

**Durum:** v1.3 — 25 Ekim 2026; 23 Ekim 4. toplantı kararları ve açık işleri işlendi · **Editör:** Levent
**Dayanak:** MR1 (2 Ekim), MR2 (9 Ekim), 16 Ekim görüşmesi, 23 Ekim 4. toplantı kaydı · Ozan'ın normalizasyon dokümanları · Hilal'in araştırma dosyaları

> **Bu belge nasıl kullanılır?**
> Projenin **tek doğruluk kaynağıdır**. Bir soru "nasıl yapacağız?" ise cevabı buradadır. Cevap yoksa ya da yanlışsa
> grup mesajı değil, bu belgeye öneri gelir: *"X kararını şuna değiştirmeyi öneriyorum, çünkü …"* (en fazla 3 cümle).
> Kararlar yalnız Çarşamba ekip senkronunda ya da Cuma danışman görüşmesinde değişir. Her agent bu belgeyi okur.
> Durum sütunu: **ÖNERİ** (bu akşam konuşulacak) → **KARAR** (ekip onayladı, tarih).

---

## 1. Ürün

**Tek cümle:** NutriScan, kullanıcının gönderdiği paketli gıda etiketinin içindekiler listesini ve besin tablosunu okur;
kullanıcının seçtiği sağlık durumlarını kaynaklı, onaylı kurallarla değerlendirir ve sonucu gerekçesi, kapsamı ve
belirsizliğiyle gösterir. **Ürün kataloğu ve aynı kategoride alternatif önerisi v1 kapsamında değildir.**

**Neden genel bir LLM sohbetinden farklı:** her sonuç onaylı kural tablosuna, sürümlü kaynağa ve görünür veri kapsamına dayanır.
AI araçları kaynaklardan kural satırı taslağı çıkarmaya yardımcı olabilir; tabloya giriş ve kullanıcı sonucu insan onayı
olmaksızın gerçekleşmez. Aynı girdi ve kural sürümü aynı sonucu üretir.

| Kapsamda (v1) | Kapsam dışı (v1) |
|---|---|
| Tek etiket başvurusu: fotoğraf → OCR → kullanıcı düzeltmesi → istek içinde analiz | Barkod, Open Food Facts ürün kayıtları ve ürün kütüphanesi |
| Etiketten kaynaklı kuralla kontrol edilebilen sağlık durumları; veri yoksa/kuralsızsa "Doğrulanamadı" | İlaç etkileşimi, çoklu hastalıklar arasında otomatik uzlaştırma |
| Mevcut veri kapsamı: 7 sağlık durumu ve 17 kural satırı; kapsam doğrulanmış kurallarla genişletilir | Aynı kategoride alternatif ürün önerileri (sonraki kapsam değerlendirmesi) |
| Sonuç: **Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı**; kaynak ve kapsama ilişkin açıklama | Günlük tüketim takibi, porsiyon kaydı, menü/diyet planı |
| Tarama metni ve sağlık profili istek kapsamında işlenir; sunucuda saklanmaz | "Güvenli / zararlı", teşhis ve tedavi iddiaları |

## 2. Uçtan uca akış (örnek: Selin — çölyak + diyabet, bisküvi)

```
[1] Fotoğraf → OCR → "buğday unu, şeker, glikoz şurubu, renklendirici (E102)" + besin tablosu (100 g: karb. 72 g, şekerler 48 g)
[2] Böl + türle → buğday unu: gıda hammaddesi · şeker: gıda kavramı · glikoz şurubu: karışım · E102: tekil kimyasal · 48 g: besin değeri
[3] Eşle → birebir/bulanık eşleşme; OFF taksonomisinde olmayan Türkçe terimler embedding edilip Qdrant'ta aranır
         Qdrant aday eşleşme üretir; kanonik kavrama bağlama/doğrulama adımı netleşene dek belirsizse "Doğrulanamadı"
         E102 → Tartrazin (SAME_AS) · buğday unu → Buğday (CONTAINS gluten)
[4] Kurala bak → çölyak × buğday → Uygun değil (kaynak: Gıda Kodeksi gluten tanımı)
                 diyabet × karbonhidrat 72 g/100 g → kılavuz profiline göre değerlendirme + bilgi
[5] Kanıt (yalnız bilgi) → E102 için CTD ilişkileri ve JECFA değerlendirmesi, kaynak linkiyle
[6] Göster → her sağlık durumu için sonuç, gerekçe, kaynak, kapsama dair not ve belirsizlik
```

## 3. Kararlar

| # | Konu | Karar | Neden | Durum |
|---|---|---|---|---|
| K1 | Girdi | Etiket **OCR** ile okunur, kullanıcı düzeltir; analiz anında yapılır. **Ürün/tarama geçmişi saklanmaz**, ürün kütüphanesi yok | V1 etiketi başına değerlendirme ve kural kapsamı; karşılaştırma v1 dışında | KARAR (17 Eki, değişti) |
| K2 | Hastalık kapsamı | Hedef: etiketten kılavuz/mevzuatla kontrol edilebilen durumları kapsamak. Kural/veri yoksa "Doğrulanamadı". **Mevcut depodaki kapsam: 7 sağlık durumu, 17 kural satırı**; kaynaklı kural tablosu için ilk hastalık listesi 30 Ekim toplantısında netleştirilecek | Hedef kapsamı mevcut veri kapsamıymış gibi göstermemek; her durumda kapsamı açıkça göstermek | Hedef KARAR (17 Eki, değişti); liste AÇIK İŞ (23 Eki) |
| K3 | Odak | V1 odağı içerik × hastalık eşleşmesi ve doğru anlatımdır. Aynı kategoride alternatif önerisi **sonraki kapsam değerlendirmesine** bırakılmıştır | Hoca odağı tek yerde istiyor | KARAR (17 Eki, değişti) |
| K4 | Kimyasala inme kuralı | Bir ifade **ancak etiket tek bir maddeyi adıyla söylüyorsa** kimyasala bağlanır (E102, askorbik asit). "Doymuş yağ" sınıf, "glikoz şurubu" karışım, "buğday unu" hammadde olarak kalır | Yanlış kimyasal üretmemek; kurallar zaten o seviyede konuşur | KARAR (17 Eki) |
| K5 | Kararı kim verir | Sağlık sonucu yalnız **gözden geçirilmiş kural tablosundan** üretilir. Qdrant aday eşlemesi yapar; CTD/JECFA araştırma bilgisi sağlar; AI/LLM sonucu bağımsız belirlemez | Kaynak izi ve tekrarlanabilir karar | KARAR (17 Eki; 23 Eki teyit) |
| K6 | Doğrulama | Her kural satırını **iki ekip üyesi bağımsız** kontrol eder; iddia "kılavuza uygunluk", klinik doğrulama değil. Doğrulanmamış satır etkinleştirilmez | Uzmana bağımlılık yok; iddia dürüst | KARAR (17 Eki; 23 Eki teyit) |
| K7 | Qdrant'ın yeri | OFF taksonomisinde olmayan Türkçe eşanlamlılar, gıda ve kimyasal terimler embedding edilerek Qdrant'ta vektör aramasına verilir; Qdrant eşleşme adayı üretir. Kanonik kavrama bağlama/doğrulama ve belirsiz aday işleme yöntemi açık iştir | OFF'ta olmayan terimler için aday bulma; sağlık sonucunu yalnız kural tablosu verir | Qdrant kullanımı KARAR (23 Eki); aday doğrulama AÇIK İŞ |
| K8 | Türkçeleştirme | Veritabanları çevrilmez; **alias tablosuna yalnız gereken terimler** eklenir (bkz. §6) | En az iş, izlenebilir | KARAR (17 Eki) |
| K9 | Değerlendirme | Eşleme sınavı (100 ifade, sözlük vs hibrit) + kural sınavı (20 senaryo); finalde tek tablo (bkz. §7) | Hocanın deney isteği, ayrı faz açmadan | KARAR (17 Eki) |
| K10 | Teknoloji | Python + FastAPI (eşleme/kural servisi) · PostgreSQL · Qdrant · mobil: Expo (React Native) · OCR: cihazda metin tanıma [kütüphane ilk 20 etiketle denenip seçilecek] | Embedding/NLP ekosistemi Python'da; tek servis | KARAR (17 Eki) |
| K11 | LLM'in rolü | LLM, K13 sınırları içinde kaynaklı kural araştırması/taslağına destek verebilir; doğrulanmamış satır etkinleştirilmez. Kullanıcı mesajında yalnız gözden geçirilmiş tablonun yapılandırılmış sonucunu sadeleştirir; sonucu değiştiremez, yeni sağlık iddiası ekleyemez. LLM çalışmazsa şablon metin | Araştırma desteği ile kullanıcı kararını ayırmak | KARAR (17 Eki; kapsamı 23 Eki'de netleşti) |
| K12 | Süreç | Sade repo (README + bu belge + kod), Azure ve CI kapıları yok; kısa dallar, sahibi merge eder; haftalık ortak inceleme | Ekibe uymayan ağır süreç bırakıldı | KARAR (17 Eki) |
| K13 | Kural kaynağı ve AI/araç desteği | Her sağlık durumu için kaynaklı kural kayıtları hazırlanır. LLM/araçlar araştırma ve taslak hazırlığına yardım edebilir; **doğrulanmamış kural etkinleştirilmez**. Qdrant, CTD, JECFA ve LLM sağlık sonucunu bağımsız belirleyemez; sonucu yalnız gözden geçirilmiş kural tablosu üretir. Kural şeması ve dosya prototipi/PostgreSQL arasındaki saklama-onay akışı açık iştir | Kaynak izi, insan incelemesi ve deterministik sonuç | KARAR (4. toplantı, 23 Eki); şema ve saklama akışı açık |

## 4. Hedef veri şeması (PostgreSQL — yalnız bilgi tabanı)

Bu şema hedef taslaktır; depodaki prototip CSV dosyası kullanır. 4. toplantı, kaynak kural kayıtlarının tek doğruluk kaynağı ve onay akışının dosya prototipi ile hedef PostgreSQL arasında netleştirilmesini takip işi yaptı. Ürün saklanmaz (K1); taranan etiket istek içinde işlenir, yanıt döner, kayıt tutulmaz.

```
concept     id, tur, ad_tr, ad_en, e_kodu, cas, mesh_id, pubchem_cid
alias       id, concept_id, metin, dil, iliski, kaynak, kaynak_surumu, durum      -- iliski: SAME_AS|CONTEXTUAL|IS_A|CONTAINS|MAY_CONTAIN · OFF'ta bulunmayan içerik/kimyasal terimlerin embedding adayları Qdrant'ta aranır
condition   id, ad_tr, mesh_id, kapsam_notu
rule        id, condition_id, kural_turu (varlik|miktar|beyan), hedef, kosul, sonuc, eksik_veri_sonucu,
            kaynak_belge, bolum, surum, kontrol_eden_1, kontrol_eden_2
evidence    concept_id, condition_id, kaynak (CTD|JECFA), iliski_turu, calisma_sayisi, pmid_url, kaynak_surumu   -- yalnız bilgi
source      id, ad, url, surum_tarihi, lisans, alinan_alanlar

istek (saklanmaz):  ham_icindekiler, besin_degerleri, profil
yanıt (saklanmaz):  mention listesi, eşleşmeler, kural sonuçları, araştırma bilgisi, LLM mesajı
```

## 5. Veri kaynakları (v1)

| Görev | Kaynak | Kullanım | Lisans notu |
|---|---|---|---|
| E-kodu → Türkçe resmî ad | Türk Gıda Kodeksi Katkı Maddeleri Yönetmeliği | alias + concept | Resmî mevzuat; atıf |
| Türkçe ↔ İngilizce gıda adı | OFF Ingredients Taxonomy (`ingredients.txt`) | mevcut sözlük ve eşanlamlılar; taksonomide olmayan terimler için Qdrant aday araması | ODbL — atıf, türev şartı incelenecek |
| Kimyasal kimlik | CTD Chemical Vocabulary · PubChem (eksikler, ön hazırlıkta) | concept | CTD kullanım şartları; PubChem açık |
| Kanıt (bilgi) | CTD Chemical–Disease · WHO JECFA | evidence | Atıf; yalnız listemizdeki maddeler |
| Kural | ADA 2026 / TEMD · KDIGO 2024 · Gıda Kodeksi (gluten) | rule | Kendi cümlelerimizle, bölüm atfıyla |
| Test verisi | Gerçek etiketlerden 100 ifade + 20 senaryo (dosya) | tests/ | Kendi verimiz |
| **v1'de yok** | FooDB (CC BY-NC), ChEBI, FoodOn, UMLS | — | Kapsam ve lisans |

Her kaynak için `kaynak, sürüm/indirme tarihi, lisans, alınan alanlar` bir envanter dosyasında tutulur (Hilal).

## 6. Türkçeleştirme

1. **E-kodu köprüsü:** Türkçe ad → E-kodu → CAS → CTD. Çeviri gerekmez.
2. **OFF taksonomisi:** Türkçe girdileri doğrudan alias olur ("şeker → en:sugar").
3. **Taksonomide olmayan terimler:** Türkçe eşanlamlı, gıda veya kimyasal içerik terimleri embedding edilip Qdrant'ta aranır; Qdrant yalnız eşleşme adayı verir.
4. **Doğrulama:** adayın kanonik kavrama bağlanması, doğrulanması ve belirsiz eşleşmenin ele alınması yöntemi toplantı 4'te açık iş bırakıldı. Bu adım netleşene kadar belirsiz terim tahminle eşlenmez.
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

## 9. Yol haritası ve tarih durumu

> Aşağıdaki teslim tarihleri tarihli notlardaki hedeflerdir; resmi takvim olarak teyit edilmemiştir.
> 18 Ekim hedef tarihi geçti. Proposal'ın teslim edilip edilmediği bu repoda kayıtlı değildir.

| Teslim | Son kayıt / hedeflenen içerik |
|---|---|
| **18 Ekim · Proposal v1** | Hedef tarihi geçti; teslim durumu bilinmiyor. `plan/proposal/proposal-v1.md` tarihsel taslak olarak işaretlenmiştir. |
| **~6 Kasım · Ara rapor** [tarih teyit edilmedi] | 4. toplantıdaki aksiyon: sağlık durumu kapsamını, doğrulama ölçütlerini ve CTD/JECFA/Qdrant rollerini kaynak bağlantılarıyla rapora yazmak; kaynaklı kural tablosu hazırlığını başlatmak. |
| **~18 Aralık · Final + demo** [tarih teyit edilmedi] | Etiketten sonuç üretme, kaynak/kapsam açıklaması, eşleme ve kural değerlendirmesi; mobil OCR ancak uygulama geliştirilirse. Aynı kategoride alternatif önerisi v1 teslim kapsamı değildir. |

## 10. Kayıtlı uygulama durumu ve 4. toplantı takip işleri

- Depodaki kural tablosu `data/kurallar/kurallar_v0.csv` şu anda 17 satır ve 7 sağlık durumu içerir. Bu mevcut veri kapsamıdır; K2'nin hedef kapsamıyla aynı değildir.
- Servis prototipinde metin işleme, sözlük tabanlı eşleme, bulanık eşleme, kural değerlendirme ve CSV'den rapor üretme vardır. Qdrant kullanımı mimari karardır, ancak Qdrant adımı, FastAPI uç noktası, mobil uygulama ve LLM mesaj katmanı depodaki kodda henüz uygulanmamıştır.
- 23 Ekim 4. toplantı kaydı: [resmî toplantı kaydı](../toplanti/2026-10-23-toplanti-4-kaydi.pdf). Qdrant ile OFF'ta olmayan terimlere aday arama kararlaştırılmıştır; adayların kanonik kavrama bağlanması ve doğrulama yöntemi açık iştir.
- 4. toplantıdaki takip işleri: TÜBİTAK raporuna sağlık durumu kapsamı, kanıt doğrulama yaklaşımı ve CTD/JECFA/Qdrant rollerini kaynaklarla yazmak; bir sonraki hafta hastalık listesini ve kural kayıt şemasını netleştirip kaynaklı kural tablosunu hazırlamaya başlamak; Qdrant aday doğrulama/kanonik eşleme ile kural kayıtlarının dosya prototipi/PostgreSQL saklama ve onay akışını kararlaştırmak. Toplantı kaydında sorumlu kişi veya ara teslim tarihi belirtilmiyor.
- Sonraki görüşme tarihi kayıtta 30 Ekim 2026 olarak geçer. Daha sonraki sonuç kaydı yoksa bu takip işleri tamamlanmış kabul edilmemelidir.
- TÜBİTAK 2209-A ve diğer ara/final rapor tarihleri için son resmi takvim bu belgede doğrulanmış değildir.
