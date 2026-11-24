# AGENTS.md — NutriScan

Bu dosyayı ekibin üç agent'ı (Claude Code, Codex, Antigravity) okur. Kısa tutulur; ayrıntı karar belgesindedir.

## Önce oku
- **[docs/mimari-karar-belgesi.md](docs/mimari-karar-belgesi.md)** — projenin tek doğruluk kaynağı. Akış, kararlar (K1–K13),
  veri şeması, kaynaklar, test planı, sahiplik. Burada yazmayan bir mimari karar verme; kullanıcıya sor.
- **[docs/tasarim/](docs/tasarim/README.md)** — uygulama tasarım paketi (gereksinim, mimari, API, veri, eşleme, kural motoru,
  değerlendirme, çalışma düzeni, yol haritası). Karar belgesi *ne*, tasarım paketi *nasıl* sorusunu cevaplar; çelişirse karar
  belgesi kazanır ve tasarım güncellenir. Koda başlamadan ilgili bölümü ve kural motoru değişmezlerini (06 §2) oku.
- **[PLAN.md](PLAN.md)** — kim neyi hangi sırayla yapıyor, hangi klasörler kimin. Agent yalnız kendi kişisinin klasörlerine dokunur.
- Araştırma notları: `docs/arastirma/`. Toplantı kayıtları: `toplanti/`. `toplanti/arsiv-eski-yon/` ve `docs/arsiv/` karar kaynağı değildir.

## Ekip
Levent (Claude Code) · Hilal (Codex) · Ozan (Antigravity). Alan sahipliği karar belgesi §8'de.

## Bir issue nasıl yapılır (her agent, her iş, aynı sırayla)
1. **Sıradaki işi bul:** `PLAN.md`'de kişinin adı altındaki ilk kutusu boş işi al. `gh issue view <n>` ile aç; "Önce bitmesi
   gereken" issue'lardan biri açıksa **başlama**, kullanıcıya hangisini beklediğini söyle.
2. **Oku:** issue'daki "Uygulama notu" yorumunu ve bağlı tasarım bölümünü oku. Dokunacağın dosyalar kişinin klasörlerinde
   değilse dur ve sor.
3. **Dal aç:** güncel `main`'den `git switch -c <isim>/<n>-<kisa-konu>`.
4. **Önce test:** kabul ölçütünü teste çevir, kırmızı yandığını gör; sonra kodu yaz, yeşile getir. Sonuç değiştiren bir
   düzeltmede `tests/golden/` altın kaydı aynı commit'te, nedeni mesajda yazılarak güncellenir.
5. **Kontrol et:** `.venv/bin/python -m unittest discover -s tests` yeşil olmalı.
6. **PR aç:** `gh pr create --base main`. Başlık Conventional Commits + `(#<n>)`. Gövdede dört başlık: **Ne** · **Neden**
   (`Closes #<n>`) · **Nasıl doğrulandı** (komut ve çıktı) · **Dikkat** (varsa). Aynı PR'da `PLAN.md`'deki işin kutusunu
   `[x]` yap.
7. **Birleştirme kişinin işidir:** CI yeşilse kişi PR'ı okur ve kendisi birleştirir; başka birinin onayı gerekmez. Agent,
   kullanıcı "birleştir" demeden merge etmez.
8. **Yarım kalırsa:** issue'ya kısa durum yorumu yaz (ne bitti, ne kaldı, ne bekleniyor).

### Ekip aynı hızda çalışmaz: erken ya da yanlış adım atmamak için
- **Başlamadan:** `git switch main && git pull`. Sonra kontrol et: (a) bağımlı issue'lar **kapalı** mı (açık PR'ı olması yetmez,
  birleşmiş olmalı) · (b) bu issue için açık bir PR ya da başkasının dalı var mı (`gh pr list --search "<n>"`) · (c) issue sana
  ya da kullanıcına mı atanmış. Biri tutmuyorsa **başlama**, kullanıcıya durumu söyle.
- **Bekleyen bir şey varsa** başkasının klasörüne geçici kod, sahte dosya ya da "şimdilik" düzeltme koyma. Kendi tarafını
  sözleşmeye (`docs/tasarim/openapi.yaml`, `04-veri-modeli.md` biçimleri) göre yaz, eksik kısmı issue'ya yorum olarak bildir.
- **PR açmadan önce** `git fetch && git merge origin/main` yap ve testleri yeniden çalıştır; başkasının birleşen işiyle
  çakışma varsa yalnız kendi dosyalarında çöz, başkasının dosyasındaki çakışmayı ona sor.
- **Bilmediğin bir durumla karşılaşırsan** (beklenmedik test, eksik veri, belgeyle çelişen kod) tahmin edip ilerleme; dur ve sor.
- Bir iş bitmeden PLAN'daki sıradaki işe geçme; bir PR birleşmeden ona bağlı işe başlama.

## Kırmızı çizgiler
1. **Sağlık durumuna ilişkin sonucu yalnız gözden geçirilmiş kural tablosu belirler.** Qdrant yalnız eşleşme
   adayı üretir; CTD/JECFA araştırma bilgisidir. LLM ve diğer araçlar kaynaklı kural araştırması/taslağına
   yardımcı olabilir; iki ekip üyesi bağımsız doğrulamadan satır etkinleştirilmez. Qdrant, CTD, JECFA ve LLM
   sonucu bağımsız belirleyemez. LLM yapılandırılmış sonucu anlatabilir; sonucu değiştiremez.
2. Sonuç dört durumdan biridir: **Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı.** "Güvenli", "zararlı",
   "tetikler", "tedavi", "önler" yok; teşhis yok.
3. **Belirsizlik riski yalnız artırır:** eşleşme eşik altı, veri eksik ya da kural yoksa sonuç "Doğrulanamadı". Tahmin yok.
4. **Kimyasala inme kuralı:** bir ifade ancak etiket tek bir maddeyi adıyla söylüyorsa kimyasala bağlanır. Sınıf, karışım ve
   hammadde olduğu seviyede kalır. Etikette yazmayan miktar uydurulmaz.
5. **Kaynak, sayı, sürüm, API uydurma yok.** Resmî kaynaktan doğrula; doğrulayamazsan `[..]` bırak ve söyle.
6. Ürün ve sağlık profili sunucuda saklanmaz. Sır (anahtar, parola, token) repoya, koda, loga girmez.
7. Lisans: her veri kaynağının lisansı `data/kaynaklar.md`'de kayıtlı olmadan veri repoya girmez. FooDB kullanılmaz (CC BY-NC).

## Çalışma
- Kısa dal (`<isim>/<issue-no>-<kisa-konu>`), her iş bir PR; sahibi okur ve birleştirir; haftalık ortak inceleme.
- Commit: Conventional Commits, İngilizce başlık. **Commit ve PR'da AI imzası ve araç adı yok.**
- Dil: kod ve tanımlayıcılar İngilizce; dokümanlar ve arayüz metni Türkçe.
- Öneri, gruba ham agent çıktısı olarak değil, karar belgesine en fazla 3 cümlelik değişiklik önerisi olarak gelir.
- Büyük bir işe başlamadan önce kısa bir plan yaz ve insan onayı al.
