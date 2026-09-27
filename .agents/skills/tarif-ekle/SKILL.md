---
name: tarif-ekle
description: NutriScan veri fabrikasında tarif, malzeme sözlüğü, alerjen ontolojisi ya da sağlık eşik tablosu satırı eklerken/düzenlerken kullan. Şemaya uyumu, sözlük üyeliğini, lisans temizliğini ve kaynak zorunluluğunu denetler. "Tarif ekle", "sözlüğe malzeme ekle", "eşik satırı yaz" dendiğinde.
---
# Tarif ve veri ekle

Kaynak: `arastirma/07-tez-v5.md` §7 (veri fabrikası), §3.1 (sağlık kuralları) · `docs/anayasa.md` §3 · şemalar `data/schemas/`.

## Kurallar
1. **Lisans:** tarifi ekip kendi cümleleriyle yazar. Siteden, kitaptan, videodan metin kopyalanmaz; agent başka tarif metnini yeniden üretmez. Her tarifte `yazar` ve `lisans: ekip-yazimi`.
2. **Sözlük önce:** tarifteki her malzeme `data/dictionary/` içinde olmalı. Yoksa önce sözlük satırı (ayrı commit): kimlik, Türkçe ad, eş anlamlılar, varsayılan birimin gram karşılığı, alerjenler, gluten, eklenmiş şeker.
3. **Alerjeni elle yazma:** tarifin alerjenleri malzemeden türetilir. Sözlükte emin olmadığın eşleme "belirsiz" işaretlenir (S8); tahmin yok.
4. **Sayı ve kaynak uydurma yok:** eşik, madde numarası, besin değeri yalnız kaynağın kendisinden okunur; bulunamazsa `[KAYNAK BULUNAMADI]` kalır. Her eşik satırında belge · madde/sayfa · erişim tarihi · bağlantı · doğrulayan.
5. **Dil:** kullanıcıya gidecek metinlerde "zararlı / riskli / tedavi / önler / güvenli" yok (anayasa §3).
6. **Doğrula:** veri doğrulayıcısını çalıştır (`data/validators/`; komut kök `AGENTS.md` › Komutlar). Kırmızıysa PR açma.
7. **Çift onay:** veri PR'ı sahibin yanında ikinci kişinin onayını ister (Hilal: alerjen/sağlık eşlemeleri).
