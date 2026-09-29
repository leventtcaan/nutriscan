# Prototip kaynakları (yedek)
Canlı tuval: https://claude.ai/artifact/T1NAJd4949veMC6Rx5rLUK (Design canvas). Bu klasör 2026-09-29 itibarıyla yayınlanan sürümün (**Version 11 — v5.2 / ADR-015**) yerel yedeğidir.
- `*.dc.html` = artboard'lar (76), `canvas.json` = tuval dizini.
- v5.2 (29 Eyl, ADR-015): 45 yeni ekran (M23–M56, W06–W09, A05–A10), her biri durumlarıyla (yükleniyor · hata · boş · içerik + ürüne özgü);
  31 mevcut ekranda fiş kaldırıldı, fiyatlar ŞOK + Tarım Kredi online kataloğu + tarih, konum/şube yok, "Tara" sekmesi M34'e.
  Barkodun verisi M35'te; toplayıcı sağlığı A05; eşleme kuyruğu A06; sözleşme panosu A07. Boşluk analizi (özellik × ekran): `v52-bosluk-analizi.md`.
- `uretec/`: v5.2 ekranlarının üreticisi — `lib.py` (ortak bileşenler, ürün kuralları: 4 hüküm rozeti, fiyat kaynağı/tarihi) +
  `gen_*.py` + `layout.py`; bir `project/` klasörü yanında çalışır (tuvalden indirilen düzen).
- v5.1 (27 Eyl): M02 sağlık durumu seçimi (kesin kısıt · sağlık durumu · hedef), M22 yeni "Neden dikkat?" (diyabet, besin eşiği, kaynak alıntısı), M09 Murat satırı "Dikkat", A01 karar izine HLT-SUGAR-01, A02 kuyruğa RAG eşleme önerisi; M01/M03/M15/M16/W04'te veri konumu ADR-008'e göre düzeltildi (uygulama verisi AB, hane bağlamlı yapay zekâ Türkiye), W04'e önce güvenlik sırası.
- `gen_v4.py` + `tabs.py` = M16–M21 ekranlarını ve v4 sekme çubuğunu üreten betikler (tuval klasörünün içinde çalıştırılır; v5.1 elle düzenlemelerini içermez — yeniden çalıştırmadan önce karşılaştır).
- Tuvali güncellerken önce Artifact `read` ile güncel dosyaları çek (sayfa içinden kaydedilen sürümler olabilir), bu yedeği değil.
