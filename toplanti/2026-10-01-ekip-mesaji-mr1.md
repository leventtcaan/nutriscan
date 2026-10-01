*NutriScan — yarın danışman görüşmesi + MR1 (2 Ekim Cuma)*

*1) Ne götürüyoruz*
• Ürün yönü v5.2: hanenin haftalık yemek + alışveriş planı; önce kesin kısıt ve sağlık kuralı, sonra kiler, en son fiyat. Kararı motorlar veriyor, LLM yalnız anlatıyor.
• Fiyat verisi: marketfiyati veri talebimizi reddetti → demo ve deney için ŞOK + Tarım Kredi online kataloglarından kurallı, sınırlı toplama (K21); kamuya açık sürüm yalnız yazılı izinle. Fiş okuma çıktı.
• Prototip: 77 ekran, durumlarıyla (mobil, web, admin) — https://claude.ai/artifact/T1NAJd4949veMC6Rx5rLUK · repoda `plan/prototip-kaynak/`
• Takvim + çalışma düzeni: 2 haftalık sprintler, Azure Boards, PR'ı başka bir ekip üyesi onaylıyor, her Cuma kısa modül demosu.
• Kod başladı: 13 modüllü backend iskeleti + OpenAPI sözleşmesi ve sözleşme testleri `main`'de.
• Proposal taslağı (6 sayfa): öğrenci numaraları işlendi (PR #5 merge oldu); 9 Ekim'e kadar hocaya e-postayla gidecek.

*2) Görüşme akışı (~20 dk) — herkes kendi alanını anlatsın*
• Ürün yönü, fiyat verisi kararı, takvim ve kod iskeleti → Levent
• Güvenlik çekirdeği ve prototip incelemesinde yakalananlar (onaysız sağlık kuralı karar vermiyor, eksik okunan etiket "doğrulama bekliyor") → Hilal
• Prototipte demo şeridi: plan → liste → raf tarama → "Neden?" → profil → Ozan
• Agent kullanımını açıkça söylüyoruz: her PR'daki her satırı sahibi anlatabiliyor. Hoca bir parça sorarsa sahibi anlatır.

*3) Hocaya soracaklarımız*
1. Fiyat verisi yaklaşımı uygun mu? ŞOK / Tarım Kredi / Migros'a gidecek izin mektupları bölüm ya da danışman imzasıyla gidebilir mi?
2. Bahar betası (20–40 hane, sağlık verisi) için etik kurul başvurusu gerekli mi, ne zaman?
3. Sağlık eşiklerini onaylayacak diyetisyen (Beslenme ve Diyetetik) ve KVKK için hukuk tarafından bir bağlantı önerebilir mi?
4. Proposal: grup numaramız, 6 sayfa + İngilizce uygun mu, onay 16 Ekim görüşmesinde mi?
Başka sormak istediğiniz varsa bu akşam yazın, listeye ekleyelim.

*4) Görüşmeden önce*
• Prototipe 10 dk göz atın, özellikle kendi anlatacağınız ekranlara.
• A0.1-a (takvim onayı) payı board'da açık olan varsa Done'a çeksin.
• MR1 formunu görüşme notlarıyla birlikte dolduruyoruz; imza ve yoklama görüşmede, Teams'e aynı gün yükleniyor.

*5) Sonraki hafta (9 Ekim'e kadar)*
• Proposal taslağı hocaya · tarif şeması v0 + sözlük taslağı (en geç 16 Ekim) · "bitti/attım" kaydı başlıyor (5 Ekim) · görüşmeden çıkan işler board'a.
