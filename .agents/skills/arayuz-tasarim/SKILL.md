---
name: arayuz-tasarim
description: NutriScan'in mobil (Expo/React Native), web ve admin (Vite/React) arayüzlerinde ekran, bileşen ya da tasarım token'ı yazarken veya incelerken HER ZAMAN kullan. Ürüne özgü kuralları (4 durumlu hüküm rozeti, kısıt çipleri, "Neden?", sağlık dili, erişilebilirlik, Türkçe metin) ve AI-slop'tan kaçınma kontrol listesini verir; genel tasarım için frontend-design, Expo için expo-design-system ve expo-native-ui skill'lerini sıraya koyar.
---
# NutriScan arayüz kuralları

## Hangi skill ne zaman
1. **Her zaman bu dosya** (ürün kuralları ve kontrol listesi).
2. Mobil: `expo-design-system` (token'lar nerede yaşar, bileşen sözleşmesi, "native slop" listesi) + `expo-native-ui` (HIG/Material, kontroller, gölge, renk).
3. Web/admin ya da yeni görsel yön: `frontend-design` (önce 4–6 renkli token planı, sonra kod; jenerik varsayılanları ele).

## Görsel kaynak ve tasarım dili
- Ekran akışlarının kaynağı prototip: `plan/prototip-kaynak/*.dc.html` (M01–M22, W01–W05, A01–A04). **Akış, içerik ve durumlar bağlayıcıdır; renk ve yazı tipi taslaktır.**
- Taslak palet (krem zemin + serif başlık + büyük harfli küçük etiketler) `frontend-design`'ın saydığı AI izleriyle örtüşüyor. Kalıcı tasarım dili A1.7-a'da bilinçli seçilir: `frontend-design` iki geçişli planı → ekip onayı → ADR → `packages/ui` token'ları. O zamana kadar yeni ekran prototip taslağını izler.
- Token'lar tek yerde: `packages/ui` (renk, aralık, yazı ölçeği, yarıçap, gölge, hareket). Ekranda ham hex/px/yazı tipi adı yok; kural lint'e bağlanır.

## Ürün kuralları (anayasa'nın arayüz karşılığı)
1. **Hüküm rozeti** yalnız `packages/ui`'deki bileşenle çizilir: Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı. Her biri ikon + metin + renk (S22). "Güvenli", "sağlıklı", yeşil tik tek başına yok.
2. Rozet **yalnız karar kaydı verisinden** gelir (API'nin karar alanı); LLM/asistan metninden türetilmez (K01).
3. Her karardan **"Neden?"** bir dokunuşla açılır: eşleşen içerik, kural + sürüm, kaynak, tarih, güven, profil sürümü (S1). Sağlık kuralında besin eşiği + kaynak alıntısı (M22).
4. **Kesin kısıt / sağlık durumu / hedef** çipleri görsel olarak ayrışır (kilit · durum · kesikli); sağlık durumu isteğe bağlıdır, teşhis sorulmaz.
5. **Her ekran 4+ durumla** tasarlanır: yükleniyor · hata · boş · içerik; ürüne özgü: "katalogda yok" (Doğrulanamadı + etiket okuma), "plan çıkmadı" (gevşetilebilir yumuşak sınırlar; kesin kısıt asla), "LLM kapalı" (butonlarla devam) (S6, S21).
6. **Mahremiyet:** bildirim, paylaşım kartı ve seste üye adı + kısıt birlikte yok (S7, S18). Ekran görüntüsü alınan demo verisi sentetik.
7. **Kontrol kullanıcıda:** plan/liste/takas değişikliği onay ister; geri al her zaman görünür (S4).

## Metin
- Türkçe, cümle düzeni (Title Case yok), etken çatı: "Listeye ekle", "Takası kabul et". Aynı eylem akış boyunca aynı adı taşır.
- Kişiyi değil sepeti konuş; "kötü/zararlı/riskli" yok (S3, anayasa §3). Hata mesajı ne olduğunu ve ne yapılacağını söyler, özür dilemez.
- Sayı biçimi Türkçe: `6.500 TL`, `22,5 g`, `%25`. Tarih: `12 Eylül 2026`.
- Tüm metinler çeviri/metin dosyasından gelir (hardcode yok); İ/ı büyük-küçük harf dönüşümü `tr-TR` yereliyle.

## Erişilebilirlik tabanı
Dokunma alanı ≥ 44 pt · metin kontrastı ≥ 4.5:1 · dinamik yazı boyutu kırılmaz · her ikon butonunda erişilebilirlik etiketi · azaltılmış hareket ayarı dikkate alınır · web'de klavye odağı görünür (NFR-11).

## AI-slop kontrol listesi (PR'dan önce)
- [ ] Emoji ikon yok; ikonlar tek bir set (platform sembolleri ya da seçilen set).
- [ ] Her şey kart değil; aynı yarıçap/gölge her yere basılmamış; gradyan süs yok.
- [ ] Her başlığın üstünde büyük harfli etiket, `A · B · C` meta satırları, butonlarda `→` yok (bilgi taşımıyorsa).
- [ ] Mobilde web tarzı ortalanmış modal yerine platformun sheet/navigasyon kalıbı.
- [ ] Her bölüme giriş animasyonu yok; hareket yalnız kullanıcının eylemine cevap.
- [ ] Lorem ipsum, uydurma istatistik, sahte marka yok; eksik veri `[..]` yer tutucu.
- [ ] iOS ve Android (web ise dar/geniş) ekran görüntüleri PR'da; 4 durumun hepsi görünüyor.
