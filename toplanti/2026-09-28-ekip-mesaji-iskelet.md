*NutriScan — ilk kod main'de: backend iskeleti (28 Eylül)*

*1) Ne yapıldı*
• Backend iskeleti `main`'e girdi (AB#140 Done, PR #2 — Hilal onayladı): Java 25 + Spring Boot 4.1 + Spring Modulith 2.1, Gradle 9.
• Backend 13 modüle bölündü (safety, planning, privacy, audit, household, catalog, pantry…). Her modül hangi modüllere dokunabileceğini kendi `package-info.java` dosyasında yazıyor; kural bozulursa build kırmızıya dönüyor. Örnek: planning, catalog'a doğrudan erişemiyor → alerjen kontrolünden geçmemiş ürün plana giremiyor.
• Karar kaydı: `plan/kararlar/ADR-014-modul-sinirlari.md` (ÖNERİ — okuyup itirazınız varsa yazın).
• Denemek için: `cd backend && ./gradlew build` (Gradle kurmaya gerek yok, Java 25 yeterli).

*2) Board ve süreç güncellemeleri*
• Yeni PBI: *A1.2-d · Board senkronu* (AB#261) — dal/PR açılınca board durumları kendiliğinden ilerleyecek; elle sürükleme azalacak.
• CI işleri tek elde toplandı: A1.2-a (CI backend, AB#136) ve A1.2-d → Hilal. `.github/` incelemesi Levent'te.
• A1.3-b (veritabanı, AB#141) artık başlayabilir: bağlı olduğu iskelet bitti.
• PR kuralı hatırlatma: modül sahibi kendi PR'ını açtıysa diğer iki kişi inceleyen olarak atanır, biri onaylar.
• `pbi-baslat` / `pbi-kapat` skill'leri artık iş öğesi, sprint backlog ve PR bağlantılarını otomatik veriyor.

*3) Agent'la nasıl çalışıyoruz (kısa)*
• İlk kez: `plan/ilk-prompt.md` §2'deki prompt (her araçta aynı; kuralları yüklediğini ve size atanan PBI'ları gösterir).
• Her iş: agent'a *"Oturumu aç, AB#<no> üzerinde çalışacağım."* → agent PBI'ın promptunu `plan/board/promptlar/<ID>.md`'den okur, hazır mı bakar, önce plan çıkarır; onaydan sonra test + kod.
• Bitince: *"Oturumu kapat."* → kontrol çıktısı, PR taslağı, oturum günlüğü.
• Prompt yapısını görmek için örnek: `plan/board/promptlar/A1.3-a.md` (Bağlam · Görev · Kapsam · Kabul kriterleri · Teslim). Her PBI'ınki aynı kalıpta.

*4) Yakındaki işler*
• *30 Eylül* — Takvim + çalışma akışı onayı (AB#104, herkes)
• *2 Ekim Cuma* — danışman görüşmesi + MR1 aynı gün Teams'e
• *5 Ekim* — hanelerde fiş + "bitti/attım" kaydı (AB#109, herkes)
• *9 Ekim* — proposal eksikleri: öğrenci no, grup no (AB#117)
• *16 Ekim* — tarif şeması + malzeme sözlüğü v0 (AB#122/123)
• Sprint 0 (19 Ekim) öncesi: CI (AB#136), board senkronu (AB#261), veritabanı (AB#141)

Board: https://dev.azure.com/hilalhocaoglu20/NutriScan · Depo: https://github.com/leventtcaan/nutriscan
