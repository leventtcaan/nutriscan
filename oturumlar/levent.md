# Oturum günlüğü — Levent (Claude Code)

> Her oturumun sonunda en alta bir girdi eklenir; yalnız sona eklenir, eski girdi düzenlenmez.
> Oturum başında son 3 girdi okunur (AGENTS.md › Oturum protokolü).

<!-- Girdi biçimi:
## YYYY-AA-GG · AB#<no> kısa başlık
- yaptım:     …
- karar:      … (ADR-0NN) | yok
- takıldım:   …
- sıradaki:   …
- AI:         araç · ne için · hangi kısmı insan yazdı/karar verdi
-->

## 2026-09-24 → 2026-09-27 · depo öncesi tarihçe (komuta merkezi; eski DURUM.md'den taşındı)
- yaptım:     Faz 0 kontekst; 4 tur araştırma (arastirma/01, 02, 05, 06, 08, 09, 10) · tez v1→v5 (onaylı), v5.1 (ADR-011:
              sağlık durumu profili, önce güvenlik, RAG yalnız eşleme/alıntı) · ürün tanımı v5.1 (29 FR + 12 NFR) ·
              proposal v0 (6 sayfa, docx/PDF betikle) · prototip v1 → Version 9 · ADR-001…012 · takvim v1.1 → v1.5 ·
              çalışma akışı standardı · 65 PBI + 53 prompt · Azure Boards kurulumu (159 öğe, doğrulama 0 fark) · ekip mesajları
- karar:      ADR-001…012
- takıldım:   Scrum süreç geçişi organizasyon yetkisi istedi (Hilal yaptı)
- sıradaki:   ortak depo altyapısı (ADR-013), GitHub repo + Azure bağlantısı
- AI:         Claude Code (komuta merkezi): araştırma ajanları, taslaklar, betikler, board yüklemesi; kararlar Levent'in

## 2026-09-28 · AB#140 Backend iskeleti (A1.3-a)
- yaptım:     backend/ iskeleti (Java 25, Boot 4.1.1, Modulith 2.1.1, Gradle 9.8.0 wrapper SHA-256 pinli), 13 modül + açık
              allowedDependencies, 3 test (verify, modül listesi, sürüm kataloğu); negatif kanıt (sınır bozulunca build kırmızı);
              PR #2 (vekil Hilal). Proje aktarımı + Apple Notes: 00 · Oryantasyon (O·1–3), 05 · Kod (U·1).
- karar:      ADR-014 modül sınırları (ÖNERİ) · kişisel katman: TODO(human) kalktı, aktarım protokolü geldi (CLAUDE.local.md)
- takıldım:   ado MCP 401 (PAT) · §8'de shared satırı yoktu (eklendi) · Gradle yalnız Homebrew'la (OpenJDK 27 de geldi)
- sıradaki:   PR #2 incelemesi (Hilal) → merge sonrası kök AGENTS.md › Komutlar'a `cd backend && ./gradlew build`; PAT yenile
- AI:         Claude Code · sürüm doğrulama, bütün kod/test, aktarım ve notlar · Levent: kök paket, tek proje, kurulum, onay

## 2026-09-28 · AB#140 kapanış ve board düzeni (aynı oturumun devamı)
- yaptım:     PR #2 squash merge → AB#140 Done (Fixes ile otomatik) · A1.2-d board senkronu PBI'ı (AB#261) + A1.2-a (AB#136) → Hilal ·
              AB#139, AB#129 In Progress · pbi-baslat/kapat'a tıklanabilir board bağlantıları · PR inceleyen kuralı (iki ekip üyesi) · ekip mesajı
- karar:      yok (iş ataması; ADR-014 ÖNERİ bekliyor)
- takıldım:   Azure'a yazma ilk denemede izin engeline takıldı (sonra izin verildi) · etiket güncellemesinde `add` ekliyor, `replace` gerekli
- sıradaki:   AZURE_BOARDS_PAT secret + repo değişkenleri (A1.2-d için, Levent) · 30 Eyl takvim onayı · 2 Eki danışman + MR1
- AI:         Claude Code · board REST (validateOnly → yazma), betik, mesaj taslakları · Levent: atama ve dağıtım kararları

## 2026-09-28 · AB#109 fiş ve kiler kaydı klasörü (aynı oturum)
- yaptım:     Drive klasörü (kişi başı fiş klasörleri + Bitti-Attım tablosu + kullanım notu), Hilal'le paylaşıldı; DURUM › Bağlantılar; ekip mesajı
- karar:      yok (erişim yalnız ekip, link paylaşımı kapalı — KVKK)
- takıldım:   Ozan'ın Azure adresi Google hesabı değil → Drive paylaşımı olmadı
- sıradaki:   Ozan'ın Gmail adresiyle paylaşım · AZURE_BOARDS_PAT secret (AB#261 gelince) · 30 Eyl takvim onayı · 2 Eki danışman + MR1
- AI:         Claude Code · klasör/tablo/not oluşturma, mesaj taslağı · Levent: klasörün açılması ve paylaşım kararı

## 2026-09-28 · komuta merkezi (ortak altyapı, board, repo) — oturum devri
- yaptım:     ADR-013 ortak altyapı (depo = planlama klasörü, AGENTS.md, anayasa, 9 skill, oturum günlükleri) · ADR'ler ayrı dosyalara ·
              GitHub repo + koruma (yönetici istisnası) + davetler · Azure Boards ↔ GitHub App (AB#128 ile doğrulandı) · board sütunları
              Scrum durumlarına bağlandı · 21 kişi payı · commit geçmişinden Claude izi temizlendi, PR/commit'te araç adı yok kuralı ·
              AB#161 Sprint 1'e, Hilal kapasitesi S0 16 / S1 14 · AB#140 sonrası doğrulama (3 test yeşil, PR #2 metni temizlendi)
- karar:      ADR-013; öğrenme protokolü (kodu agent yazar, üç aşamalı referanslı aktarım — CLAUDE.local.md); MR1 Levent başlatınca
- takıldım:   Azure süreç geçişi organizasyon yetkisi istedi (Hilal yaptı) · board sütunları geçişte bozuk kalmıştı
- sıradaki:   yeni komuta merkezi oturumu: sıradaki işin seçimi (DURUM › Sıradaki) · AB#149 yeni uygulama oturumunda
- AI:         AI agent · araştırma, betikler, board/GitHub yapılandırması, dokümanlar · Levent: tüm kararlar ve onaylar


## 2026-09-29 · komuta merkezi (iş sırası, referans kuralı, ado PAT)
- yaptım:     sıradaki iş sırası (DURUM › Sıradaki, bağlantılı) · iş öğesi referans kuralı (AGENTS.md + kişisel katman) ·
              ado MCP 401 kök nedeni: PAT hiç yoktu → salt-okuma PAT (Work Items + Project/Team Read, 27 Ara) Anahtar Zinciri'nde, ~/.zshenv; API 200
- karar:      yok (referans biçimi süreç kuralı olarak AGENTS.md'de; PAT yalnız okuma, en az yetki)
- takıldım:   `!` ile başlatılan etkileşimli `security -w` istemine yapıştırma ilk iki denemede ulaşmadı
- sıradaki:   yeni oturumda ado MCP doğrulaması → A1.6-a (AB#149) uygulama oturumu · A1.1-a kapanışı (K→PBI eşleme)
- AI:         AI agent · kök neden, PAT formu, kasa/ortam ayarı, doğrulama · Levent: Create, token'ı kasaya koyma, onaylar
