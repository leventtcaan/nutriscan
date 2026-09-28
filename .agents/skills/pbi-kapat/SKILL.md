---
name: pbi-kapat
description: NutriScan'de bir PBI üzerindeki çalışmayı bitirirken ya da oturumu kapatırken kullan. Kontrol komutlarını çalıştırıp çıktıyı gösterir, kabul kriterlerini işaretler, PR açıklamasını ve oturum günlüğü girdisini taslak olarak yazar, karar varsa ADR açtırır. "Oturumu kapat", "PR hazırla", "AB#143 bitti" dendiğinde.
---
# PBI kapat

## Adımlar
1. **Kontroller:** modülün build/test/lint komutlarını çalıştır (modül `AGENTS.md`'sinde ya da kök `AGENTS.md` › Komutlar). Çıktıyı **göster**; kırmızıysa "bitti" deme.
2. **Kabul kriterleri:** promptun (`plan/board/promptlar/<ID>.md`) her maddesi için kanıtı eşle: test adı, komut çıktısı ya da ekran görüntüsü. Karşılanmayan madde varsa açıkça yaz.
3. **Sınır kontrolü:** `git diff --stat main` — yalnız izinli klasörler mi? ≤400 satır mı (üretilmiş kod, lockfile, veri YAML hariç)? Değilse bölmeyi öner.
4. **PR taslağı** (`.github/pull_request_template.md` biçiminde): ne · neden · alternatif · nasıl doğrulanır · AI kullanımı · sürprizler · inceleyene 3 soru. Başlık `<tip>(<modül>): … AB#<no>`, gövdede `Fixes AB#<no>`. Commit/PR'a AI imzası (Co-Authored-By, "Generated with") ekleme; commit mesajında ve PR metninde araç adı (Claude, Codex, Antigravity…) geçmez — "AI agent" yaz.
5. **Karar:** oturumda mimari/ürün kararı alındıysa `karar-yaz` skill'iyle ADR taslağı (durum ÖNERİ).
6. **Oturum günlüğü:** `oturumlar/<kişi>.md` sonuna 5 satır (yaptım · karar · takıldım · sıradaki · AI). Eski girdiye dokunma.
7. **DURUM.md:** yalnız aşama/öncelik/risk değiştiyse; ≤60 satır kuralı.
8. İnsana hatırlat: PR'ı aç, inceleyeni ata (modül sahibi ya da vekil — `plan/calisma-akisi.md` §8; **sahip kendi PR'ını açtıysa diğer iki ekip üyesinin ikisi de inceleyen olarak atanır**, biri onaylar — §5), Cuma demosunda anlatılacak kısmı seç. Her hatırlatma tıklanabilir bağlantıyla verilir (iş öğesi, PR, sprint backlog; biçim `pbi-baslat` › Çıktı).
