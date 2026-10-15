*NutriScan — neredeyiz, yarın ne sunuyoruz (16 Ekim görüşmesi)*

*1) Proje tek cümlede*
Paketli gıdanın içindekiler listesini ve besin tablosunu okuyup kullanıcının hastalığına göre değerlendiren, sonucu kaynağı ve belirsizliğiyle gösteren bir uygulama. Emin olmadığımızda "Doğrulanamadı" diyoruz; "güvenli/zararlı" demiyoruz.

*2) Neredeyiz*
• Yön netleşti: barkod yok, girdi etiketin kendisi. Önerimiz: OCR ile okunur, kontrol edilip sistemde saklanır, analiz saklanan liste üzerinden yapılır.
• Eşleme katmanı tasarlandı (Ozan'ın normalizasyon dokümanı): etiketteki ifade önce türüne ayrılır (tekil kimyasal · kimyasal sınıf · karışım · gıda hammaddesi · besin değeri), sonra sözlükle standart kimliğe bağlanır. Kimyasala yalnız etiket tek bir maddeyi adıyla söylüyorsa iniyoruz (E102 → tartrazin); "doymuş yağ" sınıf olarak kalır, miktarı besin tablosundan gelir.
• Kural, deney ve altyapı tarafı araştırıldı (Hilal'in araştırma dosyaları): hastalık türüne göre kural (çölyak → var/yok, diyabet ve böbrek → besin miktarı), kaynak/lisans kontrolü, ölçüm planı.
• Kaynakların rolü belli: OFF içerik taksonomisi, E-kodu listesi, CTD kimyasal sözlüğü, PubChem → eşleme · klinik kılavuzlar (ADA/TEMD, KDIGO, Gıda Kodeksi) → kural · CTD ilişkileri ve JECFA → kanıt (ilişki ≠ neden; miktar yoksa ADI hesabı yok) · FooDB opsiyonel (lisansı ticari kullanıma kapalı).
• Doğrulamayı kendimiz yapıyoruz: kurallar kılavuzdan kaynağıyla çıkarılıyor, her kuralı iki kişi bağımsız kontrol ediyor. Tezde iddiamız "kılavuza uygunluk", klinik doğrulama değil.

*3) Yarın hocanın iki görevine cevabımız*
*a) Literatür — vektör / graf / hibrit:*
Biyomedikal terim eşlemede literatür hibrit aramayı destekliyor: sözlük/harf eşleşmesi + anlam yakınlığı birlikte (BioSyn 2020, SapBERT 2021). Önerimiz: kayıt ve kurallar için PostgreSQL; eşleme için önce sözlük + bulanık eşleşme, üstüne deney olarak vektör arama (pgvector ya da Qdrant — ölçüme göre). Graf yalnız çok adımlı kanıt zincirleri gerekirse; kural sorgularımız 1–2 adımlı.
*b) Deney — ayrı bir iş değil, yaptığımız işi test etmek:*
Bunu bir sınav gibi düşünün.
• *Eşleme sınavı:* Marketteki paketlerden 100 gerçek içerik ifadesi toplarız ("E102", "buğday unu", "sarı renklendirici", "aroma verici"…). Her birinin doğru cevabını yazarız (E102 → tartrazin). Bazılarının doğru cevabı "bilinmiyor"dur; "aroma verici" hangi madde, belli değil. Sonra sistemimiz bu 100 ifadeyi iki şekilde çözer: *sadece sözlükle* ve *sözlük + vektör aramayla (hibrit)*. İkisinin kaçını doğru bildiğine, kaçında uydurduğuna bakarız. Böylece "vektör arama gerçekten işe yarıyor mu?" sorusunu sayıyla cevaplarız.
• *Kural sınavı:* 20 ürün × hastalık örneği hazırlarız (ör. buğday unlu bisküvi × çölyak). Her biri için kılavuza bakıp beklenen sonucu yazarız ("Uygun değil"), sonra sistemin aynı sonucu verip vermediğine bakarız. En önemli hata: sistemin uyarması gereken yerde uyarmaması.
• Finalde bunu tek tabloyla gösteririz. Ayrı bir deney fazı açmıyoruz; zaten yazdığımız kodun testi.

*4) Görüşme akışı (~15 dk)*
• Proje ve üç katman (eşleme · kural · şeffaflık) → Levent
• Eşleme katmanı ve "doymuş yağ" örneği → Ozan
• Kural, deney ve kaynak/lisans kontrolü → Hilal
• Sorular → hep birlikte

*5) Hocaya soracaklarımız*
1. Girdi: OCR + saklanan liste yaklaşımı uygun mu?
2. Pilot hastalıklar: çölyak, diyabet, kronik böbrek hastalığı ile başlamak uygun mu?
3. TÜBİTAK 2209-A (son gün 11 Kasım): başvurmamızı önerir mi, danışmanlık yapar mı?
4. Proposal (teslim 18 Ekim): yeni yönle güncelleyeceğimiz taslağı nasıl onaylatalım?
5. Ara rapor ve final tarihleri (bizdeki not: ~6 Kasım, ~18 Aralık) doğru mu?

*6) Sonrası — teslimlere göre*
• *18 Ekim · Proposal:* yeni yön, üç katman, değerlendirme planı
• *~6 Kasım · Ara rapor:* çalışan eşleme hattı v0 (böl → türle → sözlük + bulanık) · 100 ifadelik test seti ve ilk skor · çölyak kuralı
• *~18 Aralık · Final + demo:* vektör katmanı eklenmiş hibrit · iki ayarın karşılaştırma tablosu · diyabet ve böbrek kuralları · 20 senaryo · mobilde OCR ile uçtan uca demo
