---
title: NutriScan — Karar kayıtları (dizin)
updated: 2026-09-29
---
# Karar kayıtları

Her karar ayrı dosyada: `plan/kararlar/ADR-0NN-kisa-ad.md` (iki kişi aynı anda karar yazsa da çakışma olmaz).
Biçim: **ne seçtik · neden · alternatif · neden o değil** (+ açık kalanlar). Yeni numara, en büyük numaradan devam eder.
Geri alınan karar silinmez; yeni ADR yazılır ve eskisinin başına "yerine geçen: ADR-0NN" notu düşülür.
Durum: **ÖNERİ** (ekip onayı bekliyor) · **KABUL** (ekip ya da ürün sahibi onayı, tarihiyle).

| ADR | Karar | Tarih / onay |
|---|---|---|
| [ADR-001](kararlar/ADR-001-urun-yonu-tez-v5.md) | Ürün yönü: Tez v5 "hanenin haftalık planlama asistanı" | 2026-09-24, Levent onayı |
| [ADR-002](kararlar/ADR-002-fiyat-verisi.md) | Fiyat verisi: marketfiyati.org.tr izni + yedek | 2026-09-24 |
| [ADR-003](kararlar/ADR-003-pilot-zincirler-migros-a101.md) | Pilot zincirler: Migros + A101 | 2026-09-24, Levent |
| [ADR-004](kararlar/ADR-004-bilesen-sahipligi.md) | İş bölümü modeli: görev değil bileşen/modül sahipliği | 2026-09-24; eşleme 2026-09-25 ekip onayı |
| [ADR-005](kararlar/ADR-005-github-azure-boards.md) | Araçlar: GitHub | kod) + Azure Boards (planlama) (2026-09-25, ekip |
| [ADR-006](kararlar/ADR-006-backend-stack.md) | Backend stack | 2026-09-25, ekip |
| [ADR-007](kararlar/ADR-007-arayuz-stack-react.md) | Arayüz stack'i: React ailesi | 2026-09-25, ekip |
| [ADR-008](kararlar/ADR-008-barindirma-contabo-kvkk.md) | Barındırma: tüm ortamlar ekibin Contabo VPS'inde | 2026-09-25, ekip — son karar |
| [ADR-009](kararlar/ADR-009-llm-yonlendirme.md) | LLM yönlendirme | 2026-09-25, ekip; 15 Kas kapısında kesinleşir |
| [ADR-010](kararlar/ADR-010-ortak-veri-git-seed.md) | Ortak geliştirme verisi: Git'te tek kaynak + ortak staging DB | 2026-09-25, ekip |
| [ADR-011](kararlar/ADR-011-saglik-durumu-once-guvenlik.md) | Sağlık durumu profili + önce güvenlik sırası + RAG'ın yeri | 2026-09-27, Levent onayı; tez v5.1 |
| [ADR-012](kararlar/ADR-012-calisma-akisi-board.md) | Çalışma akışı + board'un tek kaynaktan üretilmesi | 2026-09-27, taslak — ekip onayı A0.1 ile |
| [ADR-013](kararlar/ADR-013-ortak-altyapi.md) | Ortak altyapı: depo = planlama klasörü, tek talimat dosyası, ortak skill'ler, dosyada hafıza | 2026-09-28, ÖNERİ |
| [ADR-014](kararlar/ADR-014-modul-sinirlari.md) | Backend modül sınırları: açık izin listesi, en dar başlangıç | 2026-09-28, ÖNERİ (AB#140, PR #2) |
| [ADR-015](kararlar/ADR-015-fiyat-toplayici-sok-tarimkredi.md) | Fiyat ve ürün verisi: web kataloglarından sözlükle sınırlı toplayıcı (demo/deney; canlı ürün yazılı izin/lisansla); pilot ŞOK + Tarım Kredi; fiş çıkar; K21 | 2026-09-29, ÖNERİ (Levent yön kararı; ekip onayı bekliyor) |
