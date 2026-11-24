# NutriScan iş planı

**Nasıl okunur:** her hafta, her kişinin işleri **sırayla** yazılı. Kutusu boş ilk iş sıradaki iştir.
Bir işin yanında **"önce #n"** yazıyorsa, o iş bitmeden başlama. İş PR'la birleşince issue kendiliğinden kapanır ve kutu `[x]` olur.

**İlerleme:** haftalık ilerleme çubuğu GitHub'da → [Milestones](https://github.com/leventtcaan/nutriscan/milestones).

Bütün işler: https://github.com/leventtcaan/nutriscan/issues (her issue kime atandıysa onun işi)

---

## Kim neyle ilgileniyor

| Kişi | Alanı | Dokunduğu klasörler |
|---|---|---|
| **Levent** | Servis ve API, kural motoru, veritabanı araçları, ölçüm kodu, raporlar | `service/` (aşağıdaki iki dosya hariç), `infra/`, `eval/kod/`, `docs/` |
| **Ozan** | Mobil uygulama, metni bölme ve eşleme, anlamsal arama (Qdrant) | `app/`, `service/nutriscan/text.py`, `service/nutriscan/matching/`, `data/sozluk/` |
| **Hilal** | Kural tablosu ve kaynaklar, test senaryoları, etiketleme kılavuzu, mağaza toplama | `data/kurallar/`, `data/kaynaklar.*`, `data/kanit/`, `eval/senaryolar/`, `eval/kilavuz.md`, `eval/saha.md` |

Herkes kendi klasöründe çalıştığı için birbirimizin dosyasını bozmayız. Başkasının klasöründe bir şey gerekiyorsa
ona söyle (issue aç ya da gruptan yaz).

---

## Hafta 1 · 21–25 Kasım

**Levent**
1. [x] [#7](https://github.com/leventtcaan/nutriscan/issues/7) Depo iskeletini kur: kodu yeni klasör düzenine taşı, ayarları dosyaya al. *(Ozan'ın 2. işi bunu bekliyor; ilk iş bu.)*
2. [ ] [#8](https://github.com/leventtcaan/nutriscan/issues/8) Bulunan hatalar için testler yaz (şu an kırmızı yanacaklar). *önce #7*
3. [ ] [#9](https://github.com/leventtcaan/nutriscan/issues/9) Kural motorunu düzelt: belirsizlikte asla "Engel bulunmadı" demesin. *önce #8*

**Ozan**
1. [ ] [#11](https://github.com/leventtcaan/nutriscan/issues/11) Expo uygulamasını kur (şimdilik sahte API ile).
2. [ ] [#10](https://github.com/leventtcaan/nutriscan/issues/10) Metin bölmedeki hataları düzelt ("içerebilir", "glutensiz değil", büyük İ). *önce #7*

**Hilal**
1. [x] [#12](https://github.com/leventtcaan/nutriscan/issues/12) Kural tablosunu yeni biçime taşı (17 satır, hepsi "taslak").
2. [ ] [#13](https://github.com/leventtcaan/nutriscan/issues/13) Kaynak listesini tamamla (eksik kaynaklar ve lisanslar).
3. [ ] [#14](https://github.com/leventtcaan/nutriscan/issues/14) Laktoz ve sülfit kurallarındaki eksikleri ekle. *önce #12*

**Hep birlikte:**
1. [ ] [#15](https://github.com/leventtcaan/nutriscan/issues/15) Çarşamba toplantısında önerileri konuş ve karar ver (`docs/tasarim/12-karar-onerileri.md`).

## Hafta 2 · 26 Kasım – 2 Aralık  ·  Cuma 27 Kasım: MR5

**Levent**
1. [ ] [#23](https://github.com/leventtcaan/nutriscan/issues/23) MR5 formu ve kısa demo (27 Kasım).
2. [ ] [#16](https://github.com/leventtcaan/nutriscan/issues/16) Kural ve sözlük dosyalarını kontrol eden betik. *önce #12*
3. [ ] [#17](https://github.com/leventtcaan/nutriscan/issues/17) API'yi yaz (uygulamanın konuşacağı servis). *önce #9*
4. [ ] [#18](https://github.com/leventtcaan/nutriscan/issues/18) Her şeyi tek komutla kuran docker düzeni. *önce #16*

**Ozan**
1. [ ] [#19](https://github.com/leventtcaan/nutriscan/issues/19) Eşleme ayarlarını koddan dosyaya al. *önce #10*
2. [ ] [#20](https://github.com/leventtcaan/nutriscan/issues/20) Profil, metin girişi ve sonuç ekranları (sahte API ile).

**Hilal**
1. [ ] [#21](https://github.com/leventtcaan/nutriscan/issues/21) Mağazada etiket fotoğrafı yönergesi + mağaza izni.
2. [ ] [#22](https://github.com/leventtcaan/nutriscan/issues/22) Etiketleme kılavuzu (bir ifadeye nasıl doğru cevap yazılır).

## Hafta 3 · 3–9 Aralık

**Hep birlikte**
1. [ ] [#24](https://github.com/leventtcaan/nutriscan/issues/24) Mağazalardan etiket topla (her kişi en az 1 mağaza). *önce #21*
2. [ ] [#25](https://github.com/leventtcaan/nutriscan/issues/25) 100 ifadeyi etiketle: her ifadeyi iki kişi ayrı ayrı. *önce #22, #24*

**Levent**
1. [ ] [#31](https://github.com/leventtcaan/nutriscan/issues/31) Ölçüm kodu (doğruluk, McNemar testi). *önce #16*
2. [ ] [#32](https://github.com/leventtcaan/nutriscan/issues/32) Sonucu sade Türkçeyle anlatan şablon metinler. *önce #17*

**Ozan**
1. [ ] [#26](https://github.com/leventtcaan/nutriscan/issues/26) Qdrant ve anlamsal arama. *önce #18, #19*
2. [ ] [#28](https://github.com/leventtcaan/nutriscan/issues/28) OCR denemesi: 20 etiketle kütüphane seç.
3. [ ] [#27](https://github.com/leventtcaan/nutriscan/issues/27) Anlamsal arama eşiğini ve modelini seç. *önce #26, #25*

**Hilal**
1. [ ] [#29](https://github.com/leventtcaan/nutriscan/issues/29) 20 test senaryosu yaz (ürün + durum + beklenen sonuç). *önce #12*
2. [ ] [#30](https://github.com/leventtcaan/nutriscan/issues/30) Senaryoların ihtiyaç duyduğu kuralları kontrol et ve etkinleştir. *önce #29, #16*

## Hafta 4 · 10–15 Aralık

**Levent**
1. [ ] [#33](https://github.com/leventtcaan/nutriscan/issues/33) Eşleme sınavı: sözlük tek başına vs sözlük + anlamsal arama. *önce #25, #27, #31*
2. [ ] [#34](https://github.com/leventtcaan/nutriscan/issues/34) Kural sınavı: 20 senaryoyu çalıştır (Hilal ile). *önce #30*
3. [ ] [#38](https://github.com/leventtcaan/nutriscan/issues/38) LLM ile açıklama (zaman kalırsa). *önce #32*

**Ozan**
1. [ ] [#35](https://github.com/leventtcaan/nutriscan/issues/35) Uygulamayı gerçek servise bağla, sonuç ve "Neden?" ekranı. *önce #17, #20*
2. [ ] [#36](https://github.com/leventtcaan/nutriscan/issues/36) OCR'ı uygulamaya ekle (deneme olumluysa). *önce #28*

**Hilal**
1. [ ] [#37](https://github.com/leventtcaan/nutriscan/issues/37) Katkı maddeleri için araştırma bilgisi (CTD/JECFA). *önce #16*

## Hafta 5 · 16–18 Aralık  ·  CSE 491 teslimi

1. [ ] [#39](https://github.com/leventtcaan/nutriscan/issues/39) Hata düzeltme (yeni özellik yok) · **hepsi**
2. [ ] [#40](https://github.com/leventtcaan/nutriscan/issues/40) Final raporu · **Levent** toparlar, herkes kendi bölümünü yazar
3. [ ] [#41](https://github.com/leventtcaan/nutriscan/issues/41) Demo provası · **hepsi**

## Bahar dönemi (CSE 492, tarihler sonra kesinleşecek)

- [ ] [#42](https://github.com/leventtcaan/nutriscan/issues/42) Şubat · deney protokolünü kesinleştir · Levent, Hilal
- [ ] [#43](https://github.com/leventtcaan/nutriscan/issues/43) Mart · 400 ifadeyi etiketle · hepsi
- [ ] [#44](https://github.com/leventtcaan/nutriscan/issues/44) Nisan · tam deney ve model karşılaştırması · Ozan, Levent
- [ ] [#45](https://github.com/leventtcaan/nutriscan/issues/45) Mayıs · 40 senaryo, OCR'lı tam akış · Hilal, Levent, Ozan
- [ ] [#46](https://github.com/leventtcaan/nutriscan/issues/46) Haziran · poster, web sitesi, video, final raporu · hepsi

---

## Çalışma kuralları (5 madde)

1. İşe başlarken GitHub'da issue'yu üstüne al.
2. Kendi dalında çalış (`isim/issue-no-kisa-konu`). Bitince **PR aç** (`Closes #n`) ve aynı PR'da bu sayfadaki kutuyu `[x]` yap.
   CI yeşilse PR'ı oku ve **kendin birleştir; başkasının onayı gerekmez.**
3. Kendi klasörünün dışına dokunma; gerekirse sahibine söyle.
4. API'nin ya da bir veri dosyasının biçimi değişecekse önce gruba haber ver.
5. Yarım kalırsa issue'ya kısa bir durum yorumu yaz.

**Tek istisna:** bir kural ya da çeviri satırını "etkin" yapmak için satıra iki kişinin adı yazılır (projenin kuralı, K6).
Bu bir PR onayı değil, satırdaki iki isim alanıdır.

**Ayrıntı lazım olursa:** her işin "nasıl"ı `docs/tasarim/` klasöründe. Başlamak için bu sayfa yeterli.
