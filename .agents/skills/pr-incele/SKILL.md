---
name: pr-incele
description: NutriScan'de başka bir ekip üyesinin PR'ını incelerken kullan. PR'ı checkout eder, kontrolleri koşar, değişikliği anayasa ve PBI kabul kriterlerine göre denetler, satır satır açıklar ve sahibe sorulacak 3 "neden" sorusu üretir. Onay vermez; onay insanın düğmesidir. "PR #12'yi incele" dendiğinde.
---
# PR incele

1. `gh pr checkout <no>`; PR gövdesindeki `AB#` numarasından PBI'ı ve promptunu bul (`plan/board/azure-idler.yaml`, `plan/board/promptlar/`).
2. Kontrolleri kendin koş; CI sonucuna güvenip geçme. Çıktıyı göster.
3. Denetim listesi:
   - Kabul kriterlerinin her biri gerçekten test ediliyor mu (testi okuyup, kodu değiştirince kırılır mı diye düşün)?
   - Değişiklik tek modülde mi; `contracts/` değiştiyse `contract-change` etiketi ve iki sahip onayı var mı?
   - Anayasa: "güvenli" kelimesi, belirsizlikte Doğrulanamadı, LLM'in karar yazması, logda sağlık verisi, dışarı maskesiz veri, hardcode eşik/tarih/kimlik, sır.
   - Arayüzse: `arayuz-tasarim` skill'inin kontrol listesi.
   - Yeni bağımlılık, şema/migration, enum ordinal, silinen test var mı?
4. Değişikliği bölüm bölüm açıkla (inceleyen agent'sız anlayabilsin diye kısa).
5. Sahibe sorulacak 3 "neden" sorusu (sahip agent'a sormadan cevaplayabilmeli).
6. Sonuç: "onaya hazır / değişiklik gerekli" önerisi + gerekçe. **Onay düğmesine insan basar.**
