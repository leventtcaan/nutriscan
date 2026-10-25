# NutriScan araştırma dosyaları

**Kısa özet:** Bu klasör, hastalık kuralı kaynakları, içerik normalizasyonu, eşleme altyapısı, lisans ve TÜBİTAK araştırması için hazırlanmış araştırma notlarını içerir. Bunlar araştırma dayanağıdır; güncel ürün kapsamı ve bağlayıcı mimari kararlar [mimari karar belgesindedir](../mimari-karar-belgesi.md).

**Araştırma notları:** 15 Ekim 2026 · **Dizin güncellemesi:** 25 Ekim 2026
**Proje bağlamı:** NutriScan bir etiket başvurusunu kaynaklı kurallarla değerlendirir. V1'de ürün kataloğu, saklanan tarama geçmişi ve aynı kategoride alternatif önerisi yoktur. 9 Ekim toplantı formundaki ürün listesini saklama yönü daha sonraki K1 kararıyla geçersiz kılınmıştır. Repodaki mevcut kural dosyası 7 sağlık durumu ve 17 satır içerir; kapsam kaynaklı kurallar doğrulandıkça genişler.

## Dosyalar ve sıra

1. [Hastalığa göre değerlendirme literatürü](01-hastalik-entegrasyonu.md) — “Hastalık–her içerik” eşleştirmesi yerine hangi tür klinik/beslenme kuralının hangi ürün verisiyle çalışabildiği.
2. [Arama ve veritabanı seçenekleri](02-arama-veritabani-karsilastirmasi.md) — exact/fuzzy, lexical, vector, hybrid, relational ve graph seçeneklerini aynı ölçütlerle sınama.
3. [Ingredient semantic matching tasarımı](03-ingredient-semantic-matching.md) — etiket ifadesinden doğrulanabilir kavrama, oradan kaynaklı kanıta giden katmanlı eşleştirme.
4. [TÜBİTAK 2209-A başvuru planı](04-tubitak-2209a.md) — güncel 2026 çağrısı, araştırma sorusu, yöntem, iş paketi, risk ve başvuru kontrolü.
5. [Ekip arkadaşının PDF değerlendirmesi](05-ekli-pdf-degerlendirmesi.md) — PDF’deki iddialar, iyi başlangıçlar, açık varsayımlar ve ticari kullanım açısından riskler.
6. [Lisans ve telif kontrolü](06-lisans-ve-telif-kontrolu.md) — yayımlanmış araştırma, klinik kılavuz, veri tabanı ve uygulama varlıklarını kullanırken tutulacak izin/atıf envanteri.

## Şu anki çalışma ilkeleri

- **PDF öneri, kanıt değil.** OFF Ingredients Taxonomy, CTD ve JECFA'nın kullanım amacı ile lisans koşulları ayrı kaydedilir. 4. toplantıda Qdrant'ın OFF'ta olmayan terimler için embedding ve vektör aramasıyla aday eşleşme üretmesi kararlaştırılmıştır; aday eşleşmenin doğruluğu ayrıca sınanır.
- **Benzerlik skoru sağlık kanıtı değildir.** Vector search en fazla olası eşleşme adayları üretir. Kanonik kimlik, kanıt türü ve klinik kural ayrıca doğrulanır.
- **Alerjen ve hastalık mantığı aynı değildir.** Bazı içerik-varlığı kuralları örtüşebilir; besin öğesi miktarı veya kişiye özgü hedef gerektiren değerlendirmeler için farklı veri gerekir.
- **“Bilinmiyor” geçerli sonuçtur.** Bilgi eksikse, eşleşme muğlaksa veya kural uygulanabilir değilse sistem bunu açıkça söyler ve sağlık hükmü üretmez.
- **Qdrant kullanımı kararlaştırıldı; katkı ve doğrulama ölçülecek.** OFF taksonomisinde olmayan terimlerde Qdrant aday araması kullanılacak. Aday doğruluğu, kapsamı ve belirsiz eşleşmeler için abstention davranışı ölçülecek; kanonik kavrama bağlama yöntemi ve doğrulama akışı açık iştir.
- **AI/araç desteği yalnız araştırma ve taslak hazırlığıdır.** 4. toplantı kararına göre her sağlık durumu için kaynaklı kural kayıtları hazırlanır; LLM/araçlar araştırmaya ve taslağa yardım edebilir, doğrulanmamış satır etkinleştirilmez. K6 uyarınca iki ekip üyesi bağımsız kontrol eder. Araç seçimi henüz kaydedilmemiştir; AI sağlık sonucunu belirlemez.
- **TÜBİTAK metinleri taslak kalacak.** Kaynaklar, araştırma çıktıları ve üretken yapay zekâ kullanımı ekipçe/doğruluk ve özgünlük açısından kontrol edilecek; danışman son sorumluluğu üstlenecek.
- **Atıf lisans izni değildir.** Her veri, model ve görselin lisansı ve hedef kullanım (tez, açık depo, servis, ticari ürün) ayrı kaydedilecek; FooDB ve OFF kullanımı ürünleşme öncesi yeniden incelenecek.

## Önceki sohbetlerden alınan bağlam

- 9 Ekim tarihli toplantı formu, ürün içeriklerini sistemde saklamayı öneren tarihsel kayıttır. Bu saklama yönü 17 Ekim tarihli K1 kararıyla değişmiştir. Güncel politika: tarama ve sağlık profili sunucuda saklanmaz; kural yoksa “Doğrulanamadı”; ürün karşılaştırması v1 dışında.
- 4. toplantıda (23 Ekim) Qdrant kullanımı netleşti: OFF taksonomisinde bulunmayan Türkçe eşanlamlılar ve içerik/kimyasal terimler embedding edilip vektör aramasıyla aday eşleşme bulunacak. Kanonik kavrama bağlama ve doğrulama yöntemi açık iştir.
- Aynı toplantıda her sağlık durumu için kaynaklı kural kayıtları hazırlanması; LLM/araçların araştırma ve taslağa yardım edebilmesi; doğrulanmamış kuralların etkinleştirilmemesi; sonucu yalnız gözden geçirilmiş kural tablosunun belirlemesi kararlaştırıldı.
- Önceki proje konuşmalarında uygulamanın amacı alerjen ve hastalık profiline göre ürün bilgilerini değerlendirmek olarak tanımlanmış. Bu notlar klinik eşik veya kesin sağlık iddiası olarak kullanılmayacak.
- Değerlendirilen sohbetler: “Bitirme projesini analiz et”, “NutriScan’i bilimsel temelde analiz” ve 9 Ekim toplantı formuna ilişkin proje konuşmaları.

## Birlikte ilerleme sırası

Önce 1. dosyada hastalık kapsamı ve kanıt modelini danışmanla tartışılabilir hale getirin. Ardından 2. ve 3. dosyalardaki aday eşleştirme/veritabanı deneyini tanımlayın. Bunlardan çıkan deney sorusunu 4. dosyada TÜBİTAK formatına taşıyın. 5. dosya, takım arkadaşının PDF’inde hangi önerilerin deney planına alınacağını gösterir.

## Değişiklik günlüğü

- 2026-10-15: İlk araştırma dizini ve beş çalışma dosyası oluşturuldu. Kaynak seçimi ve teknik mimariyi önceden kesinleştirmeyen değerlendirme yaklaşımı benimsendi.
- 2026-10-15: Kaynak araştırmaları ve veri entegrasyonu için lisans/telif ön taraması, FooDB/OFF özel notları ve ekip kaynak envanteri şablonu eklendi.
- 2026-10-25: 9 Ekim taslağının K1 ile değiştiği açıklandı; 23 Ekim 4. toplantı kaydındaki Qdrant ve kaynaklı AI/araç destekli kural hazırlama kararları işlendi.
