# Katkı kuralları (NutriScan ekibi)

Ayrıntı: [docs/tasarim/13-is-plani.md](docs/tasarim/13-is-plani.md) (kim, neyi, hangi sırayla) ve
[docs/tasarim/10-calisma-duzeni.md](docs/tasarim/10-calisma-duzeni.md) (hazır/bitti tanımı, kod standartları).

## Bir iş nasıl yapılır

1. **Issue** seç ya da sana atanmışı al. Her issue'da plan kimliği (ör. `M1-L2`), kabul ölçütü ve bağlı işler yazar.
   Bağlı işler kapanmadan başlama.
2. **Dal aç:** `<isim>/<issue-no>-<kisa-konu>` (ör. `hilal/7-kural-semasi`). Gün başında `git pull --rebase origin main`.
3. **Yalnız sahibi olduğun dosyalara dokun** (`.github/CODEOWNERS`). Başkasının dosyasında değişiklik gerekiyorsa issue
   aç ve ona ata.
4. **Commit:** Conventional Commits, İngilizce başlık (`fix(rules): …`). AI imzası ve araç adı yok.
5. **PR:** şablonu doldur, `Closes #n` yaz. CI yeşil olmadan inceleme isteme. PR'ı küçük tut (bir issue = bir PR).
6. **İnceleme:** en geç 48 saat. Kod PR'ı 1 kişi; kural ya da takma ad satırı 2 kişi (yazan inceleyemez);
   sözleşme dosyası (`sozlesme` etiketi) 3 kişi.
7. **Merge:** sahibi yapar (squash), dal silinir.

## Asla

- Kural ya da takma ad satırını tek kişi onayıyla `etkin` yapmak (K6).
- `data/config/esikler.yaml` ya da `eval/splits/` dosyalarını sözleşme PR'ı olmadan değiştirmek.
- Değişmez testlerini (D1–D10) silmek ya da atlamak.
- Etiket metnini, sağlık profilini ya da sırları loglamak veya depoya koymak.
- Kaynağı, sayıyı, sürümü uydurmak: doğrulanamıyorsa `[..]` yaz ve PR'da söyle.

## Agent'larla çalışırken

Agent'a issue numarasını ve ilgili tasarım bölümünü ver. Agent [AGENTS.md](AGENTS.md)'yi okur, kendi sahibi olmadığın
dosyalara dokunmaz, veri satırını etkinleştirmez, eşik ve ayrım dosyalarını değiştirmez.
