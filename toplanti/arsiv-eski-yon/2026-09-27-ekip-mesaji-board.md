*NutriScan — Azure Boards hazır*

Board sıfırdan kuruldu: https://dev.azure.com/hilalhocaoglu20/NutriScan
Geçen yılın 92 kaydı arşivlenip board'dan kaldırıldı (çöp kutusunda, gerekirse geri alınabilir). Proje, Hilal'in yaptığı geçişle Scrum sürecinde.

*Yapı*
• *Epic* = aşama (A0–A7) · *Feature* = takvimdeki iş paketi (A1.3 gibi) · *PBI* = 0,5–2 günlük, tek modüllük, tek PR'lık iş
• 8 Epic · 65 Feature · 65 PBI, hepsi sahibine atanmış; ekip işlerinde her birimize ayrı Task var
• Sprintler 2 haftalık: Hazırlık (28 Eyl–18 Eki) → Sprint 0 (19 Eki–1 Kas) → Sprint 1–4 (27 Aralık'a kadar). Sprint sonu Cuması = Meeting Record teslimi
• Aşama 3 ve sonrası şimdilik yalnız Feature; sırası gelince PBI'lara bölünecek

*Bir PBI nasıl işlenir*
1. Board'da kendi PBI'ını aç; açıklamada o işin *agent promptu* hazır (bağlam dosyaları, kapsam, adımlar, kabul kriterleri)
2. Promptu kendi agent'ına ver (Claude Code / Codex / Antigravity); önce plan, sonra kod + test
3. Dal: `<modül>/AB<numara>-<kısa-ad>` · PR başlığı `feat(<modül>): … AB#<numara>` · PR açıklamasında `Fixes AB#<numara>` → merge olunca PBI kendiliğinden kapanır
4. Bir PR = bir modül, en fazla ~400 satır; CI yeşil + modül sahibi ya da vekil onayı
5. Cuma: staging'de 5 dakikalık demo + agent'ın yazdığı bir parçayı anlatma

Ayrıntılar ekteki "Çalışma akışı" PDF'inde (hazır/bitti tanımı, sprint ritmi, vekiller).

*Hazırlık sprintinde (18 Ekim'e kadar) kimde ne var*
Ekip
• AB#104 Takvim + çalışma akışı onayı ⏰ 30 Eylül
• AB#109 Fiş + "bitti/attım" kaydı ⏰ 5 Ekim
• AB#117 Proposal eksikleri (öğrenci no, grup no) + okuma ⏰ 9 Ekim
Levent
• AB#115 EVREN hesabı ⏰ 10 Ekim
• AB#127 GitHub repo ⏰ 10 Ekim · AB#128 board–GitHub bağlantısı ⏰ 12 Ekim
• AB#131 AGENTS.md + anayasa · AB#140 backend iskeleti · AB#149 OpenAPI iskeleti ⏰ 18 Ekim
Ozan
• AB#122 Tarif şeması + 3 örnek tarif · AB#123 Malzeme sözlüğü (~150) + alerjen ontolojisi taslağı ⏰ 16 Ekim
Hilal
• AB#123'te alerjen eşlemelerinin onayı; Sprint 0 işleri 19 Ekim'de başlıyor (veritabanı, sentetik hane üreteci, seed verisi, veri doğrulayıcıları, sağlık kuralı şeması)

Sprint 0'da kişi başı iş: Levent 10, Hilal 6, Ozan 5 PBI; yük sınırı gözetilerek dağıtıldı.

*Ekipçe bakılacaklar (en geç 30 Eylül)*
• Kendi PBI'larınızı açıp atama, tarih ve kapsamı kontrol edin; itiraz ya da eksik varsa PBI'a yorum olarak yazın
• Agent'ınıza Azure DevOps MCP erişimi (salt okunur) kurulumu repo açılınca yapılacak
