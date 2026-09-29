# Ortak brif — NutriScan prototip v5.2 ekran üretimi

Çalışma klasörü: `/private/tmp/claude-501/-Users-leventcanceylan-Documents-Senior-Design-Project/ffa0d232-b07b-48c4-a5e2-68075ec2f3fa/scratchpad/proto/`
- `lib.py` — ZORUNLU bileşen kütüphanesi (CSS, verdict(), chip_*(), price(), banner(), xr(), toggle(), header(), phone(), tabs(),
  states_board(), web(), admin(), write(), check()). Kendi CSS'ini yazma; gerekiyorsa inline style kullan (mevcut ekranlar da öyle).
- `gap_spec.md` — boşluk analizi (A envanter, B düzeltmeler, C eksik ekran spesifikasyonları, D akış haritası). Senin ekranların C'de.
- `project/*.dc.html` — mevcut 31 ekran. Görsel dil için M09-Tarama, M17-PazarPlani, M06-Takas, W01-Studyo, A02-Katalog'u oku ve taklit et.
- Ürün kuralları: `/Users/leventcanceylan/Documents/Senior-Design-Project/.claude/skills/arayuz-tasarim/SKILL.md` (oku).

## Değişmez kurallar
1. Hüküm yalnız `verdict(kind)`: no=Uygun değil, warn=Dikkat, ok=Engel bulunmadı, unk=Doğrulanamadı. "Güvenli", "sağlıklı",
   "zararlı", "riskli", "tedavi", "önler" YOK. Tek başına yeşil tik yok.
2. Her fiyat `price(tutar, zincir, tarih)` ile: zincir ŞOK ya da Tarım Kredi, "online katalog", tarih. Eski fiyat `stale=True`
   (Doğrulanamadı). Migros/A101/marketfiyati fiyat kaynağı DEĞİL; fiş/e-Arşiv YOK (v5.2). Şube adı ve konum YOK (konum sorulmuyor).
3. Barkodun verisi: katalog = toplayıcının ŞOK/Tarım Kredi web kataloğu (içindekiler aday, moderasyonla doğrulanır) + etiket okuma +
   Open Food Facts adayı. Zincir sayfalarında barkod yok: barkod katalogda tanınmazsa "Bu ürün hangisi?" → zincir kataloğundan
   aday ürünler (ad, marka, gramaj) → kullanıcı seçer → o hane için "aday" eşleme, moderasyona (A06) düşer. OFF adayı yalnız riski
   artırır: alerjen eşleşirse "Uygun değil (aday veri)", aksi hâlde "Doğrulanamadı"; asla "Engel bulunmadı".
4. Örnek hane (sentetik): Aydın hanesi — Selin (çölyak, planlayan, av S), Ela 7 (fındık + yer fıstığı, av E), Murat (diyabet +
   hedef şeker azalt, av M), Can 14 (kısıt yok, av C). Bütçe haftalık 6.500 TL. Tarih bağlamı 22–28 Eylül 2026.
   Kaynağı olmayan sayı/eşik: `[..]` ya da `[ölçülecek]`; uydurma istatistik yok.
5. Türkçe, cümle düzeni, etken çatı; sayılar `6.500 TL`, `22,5 g`, `%25`. Emoji yok; ikon yalnız `icon()`.
6. Durumlar: spesifikasyonda sayılan her durumu çiz. Mobilde durumlar `states_board([...])` ile yan yana (2–5 telefon). Tek
   durumlu ekran `phone(...)`. Web/admin tek 1440×900 sayfa; birden çok durum gerekiyorsa sayfanın içinde bölmeler ya da ikinci bir
   dosya (`W08b-...`) kullan.
7. Mahremiyet: bildirim/ses/paylaşımda üye adı + kısıt birlikte yok. Kontrol kullanıcıda: onay + geri al görünür.
8. Erişilebilirlik: gerçek `<a href>` / `<button type="button">` / `<input>` + `<label>`; ikon butonunda `aria-label`; dokunma ≥44px.
9. Bağlantılar dosya adıyla (`<a href="M28-PlanHazirlaniyor.dc.html">`). Kanonik dosya adları aşağıda; başka ad uydurma.
10. HTML iyi biçimli: her etiket kapalı, özellikler çift tırnaklı. Metinde `&` → `&amp;`, `<` → `&lt;`.

## Kanonik dosya adları (yeni)
M23-Giris · M24-UyeEkle · M25-KisitSecici · M26-Davet · M27-DavetKabul · M28-PlanHazirlaniyor · M29-PlanFarki · M30-YemekDetay ·
M31-PlanNedenMobil · M32-DogalDil · M33-Liste · M34-Tarayici · M35-UrunKaynak · M36-EtiketCekim · M37-Enjeksiyon · M38-HataBildir ·
M39-RafFoto · M40-KilereEkle · M41-Kiler · M42-LLMKapali · M43-OnayKarti · M44-Sesli · M45-Rontgen · M46-Bildirim · M47-GelenKutusu ·
M48-Duzeltme · M49-ProfilSurum · M50-Rizalar · M51-VeriIndir · M52-HesapSil · M53-Ayarlar · M54-SistemDurumlari · M55-BosDurumlar ·
M56-Erisilebilirlik · W06-GirisWeb · W07-HaneWeb · W08-StudyoDurumlar · W09-Diyetisyen · A05-Toplayici · A06-Esleme ·
A07-SozlesmePanosu · A08-Kurallar · A09-KVKK · A10-AdminGiris
Mevcut: Main (M01) · M02-Hane · M03-Riza · M04-Liste · M05-BuHafta · M06-Takas · M07-TakasNeden · M08-Olursuz · M09-Tarama ·
M10-Neden · M11-Dogrulanamadi · M12-Market · M13-Fis (v5.2'de "Markette · aldım" olarak yeniden yazılır, dosya adı aynı) ·
M14-PlanGercek · M15-Hane · M16-Asistan · M17-PazarPlani · M18-Menu · M19-Mutfak · M20-Radar · M21-TibbiSinir · M22-NedenSaglik ·
W01-Studyo · W02-SaglikFiyati · W03-Panel · W04-Seffaflik · W05-PlanNeden · A01-KararIzi · A02-Katalog · A03-Audit · A04-Operasyon

## Nasıl
`gen_<grup>.py` yaz (from lib import *), her ekran için `write(stem, "M23 · Başlık — MUST/SHOULD/COULD (v5.2)", board, kind, group="<grup>")`.
Başlıkta öncelik: MUST (D1/Ocak) · SHOULD (D2) · COULD (demo şeridi) — ürün tanımı ve spesifikasyona göre. Çalıştır; her dosyada
`check(path)` boş liste dönmeli. Repo'ya (`/Users/leventcanceylan/Documents/Senior-Design-Project`) DOKUNMA. Başka grubun dosyalarına dokunma.
Bitince kısa rapor: yazdığın dosyalar (ad, başlık, w×h, durum sayısı), verdiğin tasarım kararları, spesifikasyondan saptığın yer.
