# NutriScan — ortak tanım (taslak, 8 Ekim)
Dayanak: 2 Ekim görüşmesi (MR1) · Ozan'ın veri/vektör analizi ve özeti · Hilal'in bilimsel değerlendirme yol haritası.

## Tek cümle
NutriScan, paketli bir gıdanın etiketini fotoğraftan okur, içindekileri ve besin değerlerini tanır, kullanıcının sağlık
durumu için **uzman onaylı ve kaynaklı kurallarla** karşılaştırır ve sonucu **neden ve ne kadar emin olduğuyla** birlikte gösterir.

## Ne yapar / ne yapmaz
| Yapar | Yapmaz |
|---|---|
| Etiket fotoğrafını okur (OCR): içindekiler + varsa besin tablosu | Barkod okumaz (danışman kararı) |
| "E102", "sarı renklendirici", "tartrazin"i aynı madde olarak tanır (Türkçe) | Etikette yazmayan miktarı tahmin etmez |
| Sağlık durumuna göre dört sonuçtan birini verir: Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı | "Zararlı / güvenli / hastalığınızı tetikler" demez, teşhis koymaz |
| Her sonucun kuralını, kaynağını ve kanıt düzeyini gösterir | Günlük tüketim takibi yapmaz (ilk sürümde yok) |
| Emin olmadığında "Doğrulanamadı" der | Kuralı yapay zekâya yorumlatmaz |

## Akış (örnek: astımı olan kullanıcı, sarı şekerleme)
1. **Oku:** fotoğraf → `şeker, glikoz şurubu, sitrik asit, renklendirici (E102)`
2. **Tanı:** E102 → Tartrazin (Türk Gıda Kodeksi E-kodu listesi, FooDB eşanlamlıları; bulunamazsa SapBERT aday önerir, aday kesin sayılmaz)
3. **Kurala bak:** astım × tartrazin satırı var mı? Satır kılavuz dayanaklı ve uzman onaylıysa sonuç oradan gelir; değilse "Doğrulanamadı".
4. **Göster:** "Dikkat — E102 (tartrazin) · dayanak · kanıt düzeyi · kaynaklar ▸ · bilgilendirmedir, teşhis değildir"

## Kaynakların rolü
- **Kural kütüphanesi (kararı veren):** hastalığa özgü kılavuzlar (ör. diyabet TEMD/ADA, böbrek KDIGO), uzman (diyetisyen) onayı, sürüm.
  WHO yalnız genel çerçeve; nüfus önerisi ürün eşiği yapılmaz.
- **FooDB:** madde adlarını ve eşanlamlılarını eşlemek (adım 2).
- **CTD:** kimyasal–hastalık ilişkisi bulan yayınları kural yazana getirmek. İlişki ≠ nedensellik; kendi başına uyarı üretmez.
- **JECFA / EFSA:** katkı maddesinin değerlendirmesi ve ADI; miktar bilinmiyorsa yalnız bilgi olarak.
- **SapBERT / vektör arama:** eşleme adayı önermek. Karar vermez.

## İlk pilotun kapsamı (öneri)
Çölyak (gluten içerikleri, kesin kural) · diyabet (eklenmiş şeker içerikleri + 100 g'daki şeker/karbonhidrat) ·
kronik böbrek hastalığı (fosfat katkıları + sodyum) · astım (sülfit ve bazı renklendiriciler). Her durum için "hangi soruyu
cevaplıyoruz" tablosu yazılır; cevaplayamadığımız soru açıkça "kapsam dışı".

## Bilimsel katkı ve ölçüm
1. **Türkçe etiket tanıma doğruluğu:** gerçek etiketlerde terimlerin yüzde kaçı doğru maddeye bağlanıyor.
2. **Uzmanla uyum:** ürün × sağlık durumu senaryolarında NutriScan'in sonucu ile bağımsız uzman değerlendirmesi karşılaştırılır;
   kaçırılan uyarı, gereksiz uyarı ve "Doğrulanamadı" oranı ayrı raporlanır.
3. **Kaynakların katkısı:** FooDB, CTD, JECFA'nın her biri senaryoların yüzde kaçında işe yarar bilgi sağladı.

## Ekipçe karar verilecek 3 nokta
1. **Barkod / kendi kataloğumuz:** Hilal'in yol haritasında var, danışman barkodu iptal etti. Öneri: ilk sürümde yok; taranan etiketler kayıt olarak saklanır.
2. **Porsiyon ve günlük takip:** Hilal'in yol haritasında var (sodyum hedefi). Öneri: ilk sürümde yok; 100 g başına bilgi + kural. Danışmana "sonraki adım" diye sorulur.
3. **Pilot durumları:** yukarıdaki dört durum mu, yoksa üç mü (çölyak, diyabet, böbrek)?
