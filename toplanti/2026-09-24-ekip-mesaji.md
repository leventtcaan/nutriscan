*NutriScan — bitirme projemiz neye dönüştü (24 Eylül)*

Arkadaşlar, geçen seneki NutriScan'i sıfırdan yeniden kurmadan önce 3 tur araştırma yaptık: rakipler, veri, KVKK, danışman, optimizasyon, AI mimarisi ve edge case'ler. Fikir sadece "barkod okut, alerjen var mı bak" olmaktan çıktı; o zaten Yuka, Fig, Ürün Dedektörü gibi uygulamalarda var. Vardığımız yer aşağıda.

*1) Ne yapıyoruz — tek cümle*
Hangi marketten alışveriş yaparsa yapsın hanenin *haftalık yemek ve alışveriş planını* kuran bir asistan. Evdeki herkesin kısıtını (alerji, çölyak vb.) doğrular, kilerdekini önce kullanır, fiyatı en fazla 2 market arasında optimize eder ve her kararının nedenini gösterir.

Kısaca: _"Market asistanı kendi rafını bilir. NutriScan senin evini bilir."_

*2) Kimin için*
• Evinde alerji/çölyak gibi kesin kısıtı olan aileler
• A101, BİM, ŞOK gibi indirim marketlerinden ve pazardan alışveriş yapanlar (Migros'un MAYA AI'ı sadece Migros müşterisine çalışıyor; indirim zincirlerinin böyle bir asistanı yok)
• Birden fazla marketten alışveriş yapanlar

*3) Kullanıcı bir haftayı nasıl yaşıyor (akış)*
① *Pazar sabahı plan gelir:* "Haftalık planın hazır: 5 akşam yemeği, ≈5.900 TL, Ela için fındıksız, kilerdeki yoğurt ve ıspanak kullanıldı. Onaylar mısın?" Onaylamadan hiçbir şey değişmez.
② *Menü:* Hafta içi akşam yemekleri. Kilerden kullanılanlar işaretli, gerekirse "glutensiz taban sadece Selin'e" gibi hane içi bölme yapılıyor.
③ *Liste:* Menüden ve alışkanlıklardan otomatik çıkıyor. "Kaç değişikliğe hazırsın? 1·3·5" seçilince daha sağlıklı/ucuz takaslar öneriliyor.
④ *Market:* "Bunları A101'den, şunları Migros'tan al, 212 TL tasarruf."
⑤ *Rafta:* Barkodu okutunca evdeki herkes için ayrı sonuç çıkıyor (Ela: uygun değil · Selin: uygun değil · Murat: engel yok…). Her sonucun altında "Neden?" var: hangi içerik, hangi kural, veri nereden, ne zaman. Sesle de sorulabiliyor: "Bunu Ela yiyebilir mi?"
⑥ *Mutfak:* Kiler (barkod, fiş, e-Arşiv faturası), bitmek üzere olanlar, son kullanma tarihi yaklaşanlar. Aldığın bir ürünün tarifi değişip Ela'ya uygunsuz hale gelirse bildirim geliyor.
⑦ *Öğren:* Plan ile gerçekte alınan karşılaştırılıyor; tutmayan takaslar daha az öneriliyor.

*4) Kurallar (ürünün sözü)*
• "Güvenli" kelimesini hiç kullanmıyoruz. 4 sonuç var: _Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı._
• Bilgi yoksa tahmin etmiyoruz, "Doğrulanamadı" diyoruz (geçen seneki "boş ürüne SAFE" hatası yok).
• Kesin kısıtı yalnız sahibi, yalnız profilden gevşetebilir; asistan, optimizasyon ya da yazılı istek gevşetemez.
• "Biraz yese olur mu?" gibi tıbbi sorulara sabit cevap; acil belirtide "112'yi ara".

*5) AI nerede, nerede değil*
AI ürünün yüzü: sohbet ve ses asistanı, proaktif Pazar planı, "misafir var, bütçe 7.000 olsun" gibi doğal dille plan değiştirme, etiket/fiş okuma.
Ama *kararı AI vermiyor.* Uygunluk kararını kural motoru, planı optimizasyon motoru veriyor; AI sadece anlıyor ve anlatıyor. Ambalaja "bu ürün alerjensizdir" yazıp AI'ı kandırmaya çalışsan bile karar değişmiyor. Jüriye bunu "Röntgen modu" ile göstereceğiz: ekrandaki her şeyin üstünde "motor karar verdi" ya da "AI anlattı" rozeti.

*6) Teknik kalp: Hane Planlama Motoru*
Menüyü, alışveriş listesini ve market seçimini *tek bir optimizasyon modelinde* birlikte çözüyor (paket boyutları, kiler, son kullanma, 2 market, bütçe, herkesin kısıtı). Bu gerçekten zor bir problem (NP-zor). İlk sentetik ölçümlerde büyüdükçe kesin çözüm bulmak zorlaşıyor; "önce menü, sonra liste" yaklaşımı daha pahalıya geliyor (gerçek veriyle tekrar ölçeceğiz). Danışmanımız Taha Hoca'nın alanına (optimizasyon + öneri sistemleri, kesin çözüm vs genetik algoritma) birebir oturuyor.

*7) Başarıyı nasıl ölçeceğiz (3 deney)*
• *E1:* Planlama motoru — kesin çözücü vs genetik algoritma, farklı ölçeklerde.
• *E2:* "Neden sadece ChatGPT yetmez?" — yalnız-LLM planlayıcı ile bizimkini aynı senaryolarda kıyaslama (kural ihlali, uydurma fiyat vb.).
• *E3:* Gerçek kullanım (beta): Nisan–Mayıs'ta 20–40 aile uygulamayı 5–6 hafta kullanacak, ölçeceğiz.

*8) Gizlilik (KVKK)*
Sağlık bilgisi özel nitelikli veri. Hane verisi Türkiye'de tutulup işlenecek; yurt dışındaki AI'a sadece ürün bilgisi ve maskelenmiş metin gidecek. Türkiye'de açık AI modeli için SSB'nin EVREN platformuna bakıyoruz.

*9) Takvim*
• 18 Ekim: Proposal (Teams)
• 19 Eki – 1 Kas: Temel (repo, CI, veri şeması)
• 2 Kas – 18 Ara: Güvenilir çekirdek → CSE 491 prototipi
• Ocak: kış kampı (menü planlayıcı ürüne girer)
• Şubat – 5 Mart: döngü tamamlanır + wow özellikleri
• ~26 Mart: yeni özellik girişi kapanır
• 29 Mart – 9 Mayıs: beta
• Mayıs: rapor, poster, sunum

*10) Bu hafta kodsuz başlıyoruz*
• Pilot marketler: *Migros + A101*. marketfiyati.org.tr'den veri izni istendi.
• Herkes kendi evinin fişlerini ve "bitti/attım" kayıtlarını tutmaya başlasın (veri setimiz buradan başlayacak).
• 200 Türk ev yemeği tarifini biz yazacağız (hazır setlerin lisansı sorunlu); önce tarif şablonu ve malzeme sözlüğü geliyor.
• İş bölümünü görev bazlı değil, *uygulamanın bileşenleri bazında* yapacağız (herkes AI ile yazacağı için çakışma olmasın diye). Modeli netleştiriyoruz, ayrıca paylaşacağım.

Prototip ekranları (mobil, web, admin) linkte, ayrıca paylaşacağım. Soru ve itirazlarınızı bekliyorum 🙌
