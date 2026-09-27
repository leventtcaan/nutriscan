*NutriScan — ortak repo hazır*

Repo açıldı: https://github.com/leventtcaan/nutriscan (private). Hilal (HilalHocaoglu) ve Ozan'a (ozankrds) yazma yetkisiyle davet gitti; e-postadaki daveti kabul etmeniz yeterli.
Repo, Azure Boards'a bağlı: commit ya da PR'da `AB#<numara>` yazınca iş öğesine bağlanıyor, `Fixes AB#<numara>` merge olunca PBI'ı kendiliğinden kapatıyor (denendi, çalışıyor).

*Neden böyle kurduk*
Üçümüz üç farklı agent'la çalışıyoruz (Claude Code, Codex, Antigravity). Birbirimizden kopmamak için kural, hafıza ve iş listesi sohbette değil repoda duruyor; her agent aynı dosyalardan başlıyor:
• `AGENTS.md` — ortak kurallar. Codex ve Antigravity doğrudan okuyor, Claude Code `CLAUDE.md` üzerinden
• `DURUM.md` — projenin "şu an"ı (aşama, bu haftanın öncelikleri, riskler)
• `oturumlar/<ad>.md` — herkesin kendi oturum günlüğü; her oturum sonunda 5 satır eklenir
• `docs/anayasa.md` — değişmez ürün ve mimari kurallar ("güvenli" yok, belirsizlik → Doğrulanamadı, LLM karar vermez, sağlık dili…)
• `plan/kararlar/` — her karar ayrı dosya (ADR-001…013)
• `plan/board/` — iş listesinin tek kaynağı; board buradan üretiliyor. Her PBI'ın agent promptu `plan/board/promptlar/` altında
• `.agents/skills/` — üç agent'ın da kullandığı ortak skill'ler: PBI başlat/kapat, PR incele, karar yaz, tarif ekle ve arayüz için AI-slop'u önleyen tasarım skill'leri (NutriScan kuralları + Anthropic frontend-design + Expo'nun resmî tasarım skill'leri)

*İlk kurulum (~15 dk)*
1. Daveti kabul et → `gh repo clone leventtcaan/nutriscan`
2. Kişisel katmanını kur (repoya girmez, yalnız sana özgü):
   Hilal → `~/.codex/AGENTS.md` · Ozan → `~/.gemini/GEMINI.md`
   İçine: adın, oturum günlüğün (`oturumlar/<ad>.md`), sahip olduğun modüller. Örnek metin `plan/ilk-prompt.md`'de.
3. Agent'ını repo klasöründe aç ve `plan/ilk-prompt.md`'deki *ilk promptu* aynen ver (adını yazarak). Agent kod yazmıyor; kuralları anlatıyor, skill'leri listeliyor ve sana atanmış PBI'ları çıkarıyor. Biri eksik çıkarsa kurulumda sorun var demektir; gruba yazın, birlikte bakalım.

*Her gün*
• Başlarken: "Oturumu aç, AB#<numara> üzerinde çalışacağım."
• Biterken: "Oturumu kapat." → kontrol çıktısı, PR taslağı, oturum günlüğü
• İnceleme: "PR #<numara>'yı incele." → onay düğmesine biz basıyoruz, agent değil

*Kurallar (kısa)*
Bir oturum = bir PBI · bir PR = bir modül · önce test · sayı, kaynak, sürüm uydurma yok · hardcode ve sır yok · karar alındıysa ADR · commit ve PR'da AI imzası yok (Co-Authored-By vb.) · `main` korumalı: kod PR + bir onayla giriyor · agent'ın yazdığını Cuma demosunda anlatabilecek kadar bilmek

*Sonra*
Azure Boards'u agent'lara doğrudan bağlama (MCP) önce Levent'te denenecek; sonuç gelince kurulum adımı paylaşılacak. O zamana kadar her PBI'ın promptu zaten repoda.
