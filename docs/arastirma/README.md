# NutriScan araştırma dosyaları

**Kısa özet:** Bu klasör, NutriScan'in hastalık eşleştirme, içerik normalizasyonu, arama altyapısı ve TÜBİTAK 2209-A başvurusu için karar vermeye yarayan araştırma notlarını sıraya koyar. Ekli PDF bir tasarım önerisidir; içindeki kaynak ve teknoloji seçimleri kesin karar kabul edilmemiştir.

**Araştırma tarihi:** 15 Ekim 2026  
**Proje bağlamı:** NutriScan; paketli gıda içeriklerini ve ürün bilgilerini kullanıcının paylaştığı alerjen/hastalık profiliyle kaynaklı biçimde değerlendirmeyi hedefliyor. Önceki toplantı formunda barkod ve OCR kapsam dışında, ürün içerik listeleri ise sistemde saklanacak şekilde yazılmıştı. Bu belge bunu 9 Ekim toplantısının geçerli taslağı olarak kaydeder; bilimsel/teknik değerlendirme sonucunda ekip bu kararı tekrar ele alabilir.

## Dosyalar ve sıra

1. [Hastalığa göre değerlendirme literatürü](01-hastalik-entegrasyonu.md) — “Hastalık–her içerik” eşleştirmesi yerine hangi tür klinik/beslenme kuralının hangi ürün verisiyle çalışabildiği.
2. [Arama ve veritabanı seçenekleri](02-arama-veritabani-karsilastirmasi.md) — exact/fuzzy, lexical, vector, hybrid, relational ve graph seçeneklerini aynı ölçütlerle sınama.
3. [Ingredient semantic matching tasarımı](03-ingredient-semantic-matching.md) — etiket ifadesinden doğrulanabilir kavrama, oradan kaynaklı kanıta giden katmanlı eşleştirme.
4. [TÜBİTAK 2209-A başvuru planı](04-tubitak-2209a.md) — güncel 2026 çağrısı, araştırma sorusu, yöntem, iş paketi, risk ve başvuru kontrolü.
5. [Ekip arkadaşının PDF değerlendirmesi](05-ekli-pdf-degerlendirmesi.md) — PDF’deki iddialar, iyi başlangıçlar, açık varsayımlar ve ticari kullanım açısından riskler.
6. [Lisans ve telif kontrolü](06-lisans-ve-telif-kontrolu.md) — yayımlanmış araştırma, klinik kılavuz, veri tabanı ve uygulama varlıklarını kullanırken tutulacak izin/atıf envanteri.

## Şu anki çalışma ilkeleri

- **PDF öneri, kanıt değil.** OFF Ingredients Taxonomy, FooDB, CTD, JECFA, SapBERT ve Qdrant seçenek olarak değerlendirilecek. Her birinin hangi soruya cevap verdiği, lisansı, Türkçe kapsamı ve doğruluk katkısı ayrı ayrı sınanacak.
- **Benzerlik skoru sağlık kanıtı değildir.** Vector search en fazla olası eşleşme adayları üretir. Kanonik kimlik, kanıt türü ve klinik kural ayrıca doğrulanır.
- **Alerjen ve hastalık mantığı aynı değildir.** Bazı içerik-varlığı kuralları örtüşebilir; besin öğesi miktarı veya kişiye özgü hedef gerektiren değerlendirmeler için farklı veri gerekir.
- **“Bilinmiyor” geçerli sonuçtur.** Bilgi eksikse, eşleşme muğlaksa veya kural uygulanabilir değilse sistem bunu açıkça söyler ve sağlık hükmü üretmez.
- **En uygun altyapı ölçülerek seçilecek.** Küçük ve kaynaklı bir gold set üzerinde doğruluk, kapsam, abstention, latency, maliyet ve lisans karşılaştırılmadan ayrı vector database benimsenmeyecek.
- **TÜBİTAK metinleri taslak kalacak.** Kaynaklar, araştırma çıktıları ve üretken yapay zekâ kullanımı ekipçe/doğruluk ve özgünlük açısından kontrol edilecek; danışman son sorumluluğu üstlenecek.
- **Atıf lisans izni değildir.** Her veri, model ve görselin lisansı ve hedef kullanım (tez, açık depo, servis, ticari ürün) ayrı kaydedilecek; FooDB ve OFF kullanımı ürünleşme öncesi yeniden incelenecek.

## Önceki sohbetlerden alınan bağlam

- 9 Ekim tarihli toplantı formu karar/eylem maddeleri: kaynak gösterilen ve uzman onaylı kural tablosu; FooDB/CTD/JECFA/SapBERT/vector search yalnızca destekleyici seçenekler; yetersiz kanıtta “Doğrulanamadı”; ürün içindekilerinin sistemde tutulması; hastalık eşleştirme ve veri mimarisinin ekipçe araştırılması; sistem çıktısının bağımsız uzman değerlendirmesiyle karşılaştırılması.
- Önceki proje konuşmalarında uygulamanın amacı alerjen ve hastalık profiline göre ürün bilgilerini değerlendirmek olarak tanımlanmış. Bu notlar klinik eşik veya kesin sağlık iddiası olarak kullanılmayacak.
- Değerlendirilen sohbetler: “Bitirme projesini analiz et”, “NutriScan’i bilimsel temelde analiz” ve 9 Ekim toplantı formuna ilişkin proje konuşmaları.

## Birlikte ilerleme sırası

Önce 1. dosyada hastalık kapsamı ve kanıt modelini danışmanla tartışılabilir hale getirin. Ardından 2. ve 3. dosyalardaki aday eşleştirme/veritabanı deneyini tanımlayın. Bunlardan çıkan deney sorusunu 4. dosyada TÜBİTAK formatına taşıyın. 5. dosya, takım arkadaşının PDF’inde hangi önerilerin deney planına alınacağını gösterir.

## Değişiklik günlüğü

- 2026-10-15: İlk araştırma dizini ve beş çalışma dosyası oluşturuldu. Kaynak seçimi ve teknik mimariyi önceden kesinleştirmeyen değerlendirme yaklaşımı benimsendi.
- 2026-10-15: Kaynak araştırmaları ve veri entegrasyonu için lisans/telif ön taraması, FooDB/OFF özel notları ve ekip kaynak envanteri şablonu eklendi.
