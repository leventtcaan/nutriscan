---
name: karar-yaz
description: NutriScan'de mimari, ürün ya da süreç kararı alındığında ADR dosyası yazmak için kullan. Yeni numarayı bulur, şablonu doldurur, dizine ekler; durum ÖNERİ olarak başlar. "Bunu karar olarak yaz", "ADR aç" dendiğinde ya da oturumda bir seçim yapıldığında.
---
# Karar yaz (ADR)

1. Numara: `plan/kararlar/` altındaki en büyük `ADR-0NN` + 1.
2. Dosya: `plan/kararlar/ADR-0NN-kisa-ad.md` (küçük harf, Türkçe karakter yok).
3. İçerik:
   ```
   # ADR-0NN · <başlık>
   **Tarih / onay:** YYYY-AA-GG, ÖNERİ (yazan: <kişi>)
   - **Ne:** …
   - **Neden:** …
   - **Alternatif:** … **Neden değil:** …
   - **Geri dönmenin maliyeti:** düşük/orta/yüksek + neden
   - **Etkilenen:** dosyalar, PBI'lar, anayasa maddeleri
   ```
4. `plan/kararlar.md` dizin tablosuna satır ekle.
5. Eski bir kararı değiştiriyorsa eskisini silme; başına "yerine geçen: ADR-0NN" notu düş.
6. ÖNERİ → KABUL yalnız insan (ürün sahibi ya da ekip) onayıyla, tarihiyle.
