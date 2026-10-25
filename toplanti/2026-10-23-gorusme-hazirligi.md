# 23 Ekim 2026 danışman görüşmesi — hazırlık

> **Tarihsel hazırlık notu.** Bu dosya görüşme öncesi hazırlanmıştır; içindeki “açık işler” toplantı sonucu değildir. Gerçekleşen 23 Ekim 4. toplantısının [resmî kaydını](2026-10-23-toplanti-4-kaydi.pdf), güncel kapsam/kararları için [mimari karar belgesini](../docs/mimari-karar-belgesi.md) kullanın.

**Açılacaklar (Ozan'ın PC'si, `git pull` sonrası):** `docs/toplanti-paketi.html` · `docs/akis-diyagrami.html`
Artifact sürümleri: paket https://claude.ai/artifact/LwT8iRcrjLBCMtFCSSmC4X · diyagram https://claude.ai/artifact/3b2jpcUmTmh5YtmPSbEVYN

## Konuşma sırası
1. **Ne yapıyoruz (30 sn):** içindekiler + besin tablosu okunur → her ifade standart kavrama bağlanır → kullanıcının hastalığı için resmî kaynaklı kural → Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı. Emin değilsek tahmin yok.
2. **Hocanın 4 sorusu (paketten):**
   - Veri: OFF taksonomileri → 5.459 kavram, 10.465 eşanlamlı (lisans `data/kaynaklar.md`); eşikler AB 1169/2011, 1924/2006, 828/2014, 1333/2008, WHO 2012, EFSA 2010, KDIGO 2024, ADA 2026. FooDB yok (CC BY-NC).
   - Türkçeleştirme: 60 gerçek Türk etiketi, 894 ifade; tanınmayan %57 → %52 (Türkçe çoğul, OFF işaretleri, gürültü) → %25 (81 ekip çevirisi, 2 kişi onayı bekliyor).
   - Şema + Qdrant: kavram · eşanlamlı · ekip_eşanlamlı · kurallar · kanıt haritası; ürün/sağlık verisi saklanmaz; Qdrant yalnız eşlemede, kalan %25 üzerinde aç/kapa ölçülecek.
   - Kural nereden: mevzuat > klinik kılavuz; "kaçın" → varlık, "sınır" → miktar, kaynak yoksa kural yok (astım × E102 → Doğrulanamadı + CTD bilgisi). `data/kurallar/kanit_haritasi.csv` (10 satır).
3. **Kanıt (bisküvi):** çölyak Uygun değil (buğday unu → buğday, IS_A); glikoz şurubu gluten sayılmaz (AB 1169/2011 Ek II muafiyeti); diyabet Dikkat (48 g > 5 g "düşük şeker"); 12 test geçiyor.
4. **Sorular:** (1) Türkçeleştirme ölçümü yeterli mi? (2) Qdrant'ı kalan %25'te aç/kapa ölçmek uygun mu? (3) TÜBİTAK araştırma sorusu "sözlük vs hibrit eşleme" olabilir mi?

## Olası sorular
- *CRUD yetmez mi?* Karar CRUD; ama düz eşleşmede ifadelerin %57'si hiçbir kurala ulaşmadı. Fark ve araştırma eşleme katmanında.
- *Laktoz neden Dikkat?* EFSA: çoğunluk tek seferde ≤ 12 g tolere eder, tek eşik yok; etikette miktar yok.
- *PKU'da 59 Doğrulanamadı?* Fenilalanin doğal proteinlerde de var, etiketten hesaplanamaz; bilinçli.
- *Eksikler?* TR yönetmelik ekleri AB metinleriyle karşılaştırılıyor (katkı yönetmeliği ekleri taranmış PDF); kurallar ve ekip çevirileri ikinci onay bekliyor; Qdrant adımı sıradaki iş; böbrek × fosfat katkısı için kaynak aranıyor.

## Açık işler (görüşme sonrası)
- Hilal: `data/kurallar/kurallar_v0.csv` eşik/kaynak kontrolü, TR Ek-1 teyidi, 2. onay
- Ozan: `data/sozluk/ekip_esanlamli.csv` 81 karşılığa göz atma, Türkçeleştirme listesinin devamı (`tests/eslesme/off_rapor.md`), Qdrant adımı
- Levent: servis (FastAPI) iskeleti, "yalnız içindekiler bölümünü ayıkla" adımı, TÜBİTAK 2209-A metni (2 Kasım'dan önce, 5–6 sayfa, kaynaklar doğrulanmış)
- Hep birlikte: ekipten 30 gerçek etiket (`tests/eslesme/etiketler.csv`, talimat `tests/README.md`)

## Komutlar
`python3 data/uret_sozluk.py <indirilenler> <off_commit>` · `python3 service/run_labels.py [etiketler.csv rapor.md]` ·
`python3 -m unittest discover -s tests -v` · `python3 docs/diyagram/uret.py`
