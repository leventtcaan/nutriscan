*NutriScan — İş bölümü ve stack raporu (25 Eylül)*

Araştırmaların sonucunda iş bölümü ve teknoloji seçimleri için ulaşılan öneriler aşağıda. İtiraz ve eklemeler için açık.

*1) İş bölümü: görev değil, bileşen sahipliği*
Ekipte üç farklı AI aracı kullanılacak (Claude Code, Codex, Antigravity). Araştırmalara göre farklı agent'ların aynı repoya açtığı PR'larda çakışma oranı %40'ın üzerinde. Bu yüzden iş, görevlere değil uygulamanın *bileşenlerine* göre bölündü: her bileşenin bir sahibi var, o klasörlerdeki kod onun sorumluluğunda; başka bir bileşene ihtiyaç duyulursa önce aradaki "sözleşme" (API tanımı) konuşulup güncelleniyor. Her bileşenin bir yedek sorumlusu da var. Efor üç kişiye eşit dağıtılmaya çalışıldı.

• *Mimari, planlama ve AI katmanı (Levent):* repo ve CI altyapısı, ortak kurallar, Hane Planlama Motoru (optimizasyon), asistan (LLM orkestrasyonu), Gizlilik Kapısı, karar kaydı ve izleme (log/metrik), E1–E2 deneyleri
• *Güvenlik ve veri çekirdeği (Hilal):* kural motoru (alerjen kararları), alerjen verisi ve test seti, hane/üye/rıza (KVKK akışları), katalog ve fiyat, kiler, öneri sistemi, admin backend
• *Arayüz ve içerik (Ozan):* mobil uygulama, web uygulaması, admin arayüzü, tarif içeriklerinin hazırlanması, kamera/etiket okuma demo özellikleri

Yük dağılımı Aralık ortasında (CSE 491 prototipinden sonra) yeniden değerlendirilecek.

*2) Stack önerisi ve gerekçeleri*
*Backend:* Java 25 + Spring Boot 4.1 + Spring Modulith, veritabanı PostgreSQL.
→ Ekibin ortak dili Java/Spring. Boot 4.1, Haziran 2027'ye kadar güvenlik güncellemesi alan tek sürüm (3.5'in desteği bitti, 4.0'ınki Aralık 2026'da bitiyor). Modulith bileşen sınırlarını otomatik test ediyor; bir bileşen yanlışlıkla diğerine bağımlılık eklerse CI kırmızı yanıyor.

*Arayüz:* React ailesi → mobil *Expo (React Native)*, web ve admin *Vite + React*.
Angular da ciddi şekilde değerlendirildi (konvansiyonları güçlü, resmi AI araç desteği var). React'i öne çıkaran nedenler:
• Barkod okuma, sesli soru, bildirim ve App Store yayını için en olgun yol Expo. Angular tarafında mobil (Ionic) WebView içinde çalışıyor, Ionic'in ticari servisleri kapanıyor, bazı bileşen kütüphaneleri kapalı kaynağa geçti.
• AI agent'larla kod üretiminde tek karşılaştırmalı ölçümde React önde; Gemini'nin (Antigravity'nin modeli) Angular'da eski yazım kalıplarına kaydığı gözlenmiş.
• Ekip geçen yıl web'i React (Next.js), mobili Expo ile yazdı; herkes biraz tanıyor, gerektiğinde birbirine yardım edebilir.
• Web ve mobil aynı dili (TypeScript) ve aynı paylaşılan paketleri kullanıyor; API istemcisi backend sözleşmesinden otomatik üretiliyor, elle yazılmıyor.

*3) "Veri herkeste farklı oluyor" sorunu (Firebase gibi bir çözüm?)*
Sorunun kökü verinin tek bir kaynaktan gelmemesi. Çözüm: veritabanı şeması ve başlangıç verisi (tarifler, katalog, örnek haneler) Git'te tutulacak; herkes tek komutla aynı veritabanını kendi bilgisayarında kurabilecek. Ayrıca herkesin aynı veriyi gördüğü ortak bir test sunucusu (staging) olacak. Firebase gerekmiyor: verileri yurt dışında tutuyor (sağlık verisi nedeniyle KVKK sorunu) ve Spring + PostgreSQL yapısına uymuyor.

*4) Sunucu ve maliyet*
Tüm ortamlar (geliştirme, ortak test sunucusu, jüri demosu ve beta) ekibin yıllık kiralı Contabo VPS'inde çalışacak; ek barındırma masrafı yok. Contabo'nun Türkiye'de sunucusu olmadığı için KVKK tarafı beta öncesinde şu adımlarla ele alınacak: gereğinden fazla kişisel veri toplanmaması, sağlık bilgilerinin şifreli tutulması ve loglara hiç yazılmaması, kesin kısıtların mümkün olduğunca cihazda kalması, Contabo ile KVKK standart sözleşmesi ve danışman aracılığıyla bir uzman görüşü. Hane bilgisi içeren yapay zekâ işlemleri zaten Türkiye'de (EVREN) yapılacak.

*5) Yapay zekâ modelleri*
Hane bilgisi içeren asistan konuşmaları SSB'nin *EVREN* platformunda (Türkiye'de çalışan açık modeller, 1 Kasım'a kadar ücretsiz) işlenecek. Kişisel veri içermeyen işler (tarif düzenleme, ürün etiketi okuma) için DeepSeek gibi düşük maliyetli modeller kullanılabilir. Uygunluk ve plan kararlarını zaten AI değil, kural ve optimizasyon motorları veriyor.

*6) Fiyat verisi planı*
marketfiyati.org.tr'den veri izni istendi. Olumlu dönerse o veri kullanılacak. Dönmezse B planı: Migros ve A101'de planlamada kullanılacak ~300 ürünün fiyatı iki haftada bir elle güncellenecek (üç kişiye bölününce kişi başı bir saatten az), beta'da kullanıcı fişlerinden gelen fiyatlar eklenecek, her fiyatın yanında ne kadar eski olduğu gösterilecek.

*7) Araçlar*
Kod GitHub'da (private repo), planlama geçen yılki gibi Azure Boards'ta (PBI, sprint). Kurulum Ekim'de.

Sıradaki adımlar: takvim, ürün tanımı + gereksinimler, ardından proposal (teslim 18 Ekim).
