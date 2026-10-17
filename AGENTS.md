# AGENTS.md — NutriScan

Bu dosyayı ekibin üç agent'ı (Claude Code, Codex, Antigravity) okur. Kısa tutulur; ayrıntı karar belgesindedir.

## Önce oku
- **[docs/mimari-karar-belgesi.md](docs/mimari-karar-belgesi.md)** — projenin tek doğruluk kaynağı. Akış, kararlar (K1–K12),
  veri şeması, kaynaklar, test planı, sahiplik. Burada yazmayan bir mimari karar verme; kullanıcıya sor.
- Araştırma notları: `docs/arastirma/`. Toplantı kayıtları: `toplanti/`.

## Ekip
Levent (Claude Code) · Hilal (Codex) · Ozan (Antigravity). Alan sahipliği karar belgesi §8'de.

## Kırmızı çizgiler
1. **Kararı yalnız kural tablosu verir.** Qdrant/vektör arama yalnız kelimeyi tanır; CTD/JECFA yalnız araştırma bilgisidir;
   LLM yalnız son mesajı yazar ve sonucu değiştiremez.
2. Sonuç dört durumdan biridir: **Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı.** "Güvenli", "zararlı",
   "tetikler", "tedavi", "önler" yok; teşhis yok.
3. **Belirsizlik riski yalnız artırır:** eşleşme eşik altı, veri eksik ya da kural yoksa sonuç "Doğrulanamadı". Tahmin yok.
4. **Kimyasala inme kuralı:** bir ifade ancak etiket tek bir maddeyi adıyla söylüyorsa kimyasala bağlanır. Sınıf, karışım ve
   hammadde olduğu seviyede kalır. Etikette yazmayan miktar uydurulmaz.
5. **Kaynak, sayı, sürüm, API uydurma yok.** Resmî kaynaktan doğrula; doğrulayamazsan `[..]` bırak ve söyle.
6. Ürün ve sağlık profili sunucuda saklanmaz. Sır (anahtar, parola, token) repoya, koda, loga girmez.
7. Lisans: her veri kaynağının lisansı `data/kaynaklar.md`'de kayıtlı olmadan veri repoya girmez. FooDB kullanılmaz (CC BY-NC).

## Çalışma
- Kısa dal (`<isim>/<kisa-konu>`), sahibi merge eder; haftalık ortak inceleme.
- Commit: Conventional Commits, İngilizce başlık. **Commit ve PR'da AI imzası ve araç adı yok.**
- Dil: kod ve tanımlayıcılar İngilizce; dokümanlar ve arayüz metni Türkçe.
- Öneri, gruba ham agent çıktısı olarak değil, karar belgesine en fazla 3 cümlelik değişiklik önerisi olarak gelir.
- Büyük bir işe başlamadan önce kısa bir plan yaz ve insan onayı al.
