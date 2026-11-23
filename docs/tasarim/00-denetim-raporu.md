# 00 · Denetim raporu (18 Kasım 2026)

> Uygulamaya başlamadan önce depo, veri, kod, belgeler ve agent ayarları tarandı. Amaç üç soruya cevap vermekti:
> (1) Şimdiye kadar nerede yanlış yaptık? (2) Kodda sabitlenmiş (hardcode) ne var? (3) Proje bu noktadan başka bir
> yöne kaymasın diye neyi kilitlemeliyiz?
>
> Yöntem: iki bağımsız tarama (kod/veri ve belge/süreç) yapıldı. Kritik bulguların her biri ayrıca elle yeniden
> çalıştırılarak doğrulandı. Bu gece **kodun davranışı değiştirilmedi**. Düzeltmeler sahiplik ve iki kişilik inceleme
> kuralına tabi olduğu için [11-yol-haritasi.md](11-yol-haritasi.md) M0'a iş olarak yazıldı.
> Önem: **KRİTİK** = yanlış sağlık sonucu ya da kırmızı çizgi ihlali · **ORTA** = tutarsızlık, bakım riski ·
> **DÜŞÜK** = temizlik.

> **Not (23 Kasım):** bu rapordaki dosya ve satır numaraları 18 Kasım halidir. #7 ile `matcher.py` → `matching/lexical.py`,
> `rules.py` → `rules/engine.py` taşındı ve bulanık eşik `data/config/esikler.toml`'a alındı (C1 kapandı).

## A. Yanlış sonuç ya da yanlış ara karar üreten hatalar (hepsi yeniden üretildi)

A1–A5 ve A7 kullanıcıya görünen **sağlık sonucunu** yanlış yöne çeviriyor (KRİTİK). A6, A8 ve A11 bugün nihai sonucu
değiştirmiyor ama ara kararı yanlış veriyor; başka bir girdide sonucu bozabilir (ORTA). A9–A10 güvenli yönde ama tutarsız (DÜŞÜK).

| # | Girdi | Beklenen | Şu an | Neden | Düzeltme (M0) |
|---|---|---|---|---|---|
| A1 | Boş metin ya da "İçindekiler: 12, 6" | Her durum Doğrulanamadı | Laktoz, sülfit: **Engel bulunmadı** | "Varsayılan" satırı tanınan içerik olmadan da çalışıyor; tanınmayan koruması yalnız `unknown` varsa devreye giriyor (`rules.py:87`) | Tanınan içerik sayısı 0 ise "Engel bulunmadı" yasak; motor seviyesinde değişmez kural |
| A2 | "şeker. Eser miktarda süt içerebilir." | Laktoz: en az Dikkat | **Engel bulunmadı** | Laktoz ve sülfit için `icerebilir` satırı yok | Her durum için "içerebilir" ya da açık "uygulanmaz" kararı; yoksa motor "Engel bulunmadı" vermez |
| A3 | "tereyağı, şeker" (ayrıca peynir, kazein, kefir, dondurma) | Laktoz: Dikkat | **Engel bulunmadı** | LAK-01 hedefleri dar; süt ürünü zinciri kapsanmıyor | Hedefleri OFF zinciriyle genişlet (Hilal + 2. inceleyici); kapsama testi: "süt kökenli her kavram bir kurala bağlı" |
| A4 | "sülfit" ifadesi | Sülfit: Dikkat | **Engel bulunmadı** | SUL-01 yalnız E220–E228 | `en:sulfite` hedefe eklenir |
| A5 | "buğday unu, şeker, süt içerebilir" (nokta yok) | Çölyak: Uygun değil | **Dikkat** | "içerebilir" ayrımı cümle bazlı; OCR noktayı kaçırınca bütün liste "içerebilir"e kayıyor (`text.py:83-90`) | Yalnız "içerebilir"in hemen önündeki öğe; belirsizse Doğrulanamadı |
| A6 | "tuz. Glutensiz değildir." | Beyan sayılmaz | CEL-03 "glutensiz beyanı" diye tetikleniyor; nihai sonuç yalnız "glutensiz değildir" tanınmayan ifade sayıldığı için Doğrulanamadı | Beyan, metinde düz alt dize aramasıyla bulunuyor | Beyanlar C3'te yapılandırılmış `Claim` olarak ayrıştırılır, olumsuzluk işaretlenir; test `fired` listesine bakar |
| A7 | tuz = 0,301 g/100 g | HT: Dikkat (sodyum 0,1204 > 0,12) | Engel bulunmadı | `round(…, 3)` eşik yakınında aşağı yuvarlıyor (`rules.py:42`) | Yuvarlama yok, karşılaştırma ham değerle |
| A8 | "e9999" | Eşleşmez | Bulanık eşleşmeyle E999'a bağlanıyor (eşleşme hatası) | Bulanık adım E-kodu biçimindeki metne de uygulanıyor | E-kodu kalıbındaki ifade bulanık adıma girmez; test `match` nesnesine bakar |
| A9 | "I\u0307ÇİNDEKİLER: …" (ayrışık İ) | Başlık atılır | `ı̇çindekiler` oluyor, başlık tanınmıyor | NFC normalizasyonu yok (`text.py:14`) | Önce `unicodedata.normalize("NFC")` |
| A10 | "ICINDEKILER: …" (ASCII) | Başlık atılır | Tanınmıyor (`text.py:81`) | Başlık kalıbı yalnız Türkçe yazım | Kalıp `dil_kaliplari.toml`'da ASCII biçimleri de içerir |
| A11 | "glikoz şurubu (buğday), şeker" | Çölyak: Engel bulunmadı yönünde muafiyet (1169/2011 Ek II) | **Uygun değil** (alt bileşen "buğday" ayrıca tetikliyor) | Muafiyet yalnız ifadenin kendi zincirine bakıyor (`rules.py:19-21`) | Muafiyet alt bileşenlere miras kalır (06 D9) |

## B. Kırmızı çizgi ve karar ihlalleri

| # | Bulgu | Önem | Kural | Düzeltme |
|---|---|---|---|---|
| B1 | 17 kural satırının 17'sinde `kontrol_eden_1/2` boş, ama motor hepsini çalıştırıyor | KRİTİK | K6, kırmızı çizgi 1 | Motor yalnız `durum=etkin` ve iki farklı inceleyicili satırı yükler; deney için `--include-drafts` bayrağı, ürün yanıtında asla |
| B2 | CKD-02'nin kaynağı yer tutucu ("[kaynak doğrulanacak]"), yine de "Dikkat" üretiyor | KRİTİK | Kırmızı çizgi 5 | B1 ile otomatik kapanır; kaynak bulunana kadar taslak |
| B3 | 81 ekip çevirisinin 81'i "taslak — 2 kişi onayı bekliyor", eşleyici koşulsuz yüklüyor | KRİTİK | K6/K8 | Onaysız takma ad üretimde yüklenmez |
| B4 | Ekip çevirilerinin 65'i ölçümün yapıldığı 60 etiketten türetildi; eşik yorumu "test setinde ayarlandı" diyor | KRİTİK (metodoloji) | NFR-8 | Öneri Ö-12: bu 60 etiket ve 894 ifade **yalnız geliştirme kümesine** girer, test kümesi yalnız saha fotoğraflarından kurulur. Bu, TÜBİTAK 2.2'deki tek küme planından bir sapmadır ve danışman onayı ister. %57 → %25 sonucu "aynı kümede kapsam iyileşmesi" olarak anılır. Kod yorumu düzeltilir |
| B5 | OFF taksonomilerinin lisans alanı `[..]`; `additives_classes.txt` ve OFF ürün kayıtları (`tests/eslesme/off_etiketler.csv`, 60 barkod) envanterde yok | KRİTİK | Kırmızı çizgi 7 | `data/kaynaklar.md` satırları eklenir; lisans netleşene kadar `lisans_durumu = arastirma_kullanimi` ara durumu (doğrulayıcı uyarır, kilitlemez; [04 §4](04-veri-modeli.md)); OFF'a soru maili (Levent onayıyla) |
| B6 | Kural kaynakları (WHO 2012, KDIGO 2024, EFSA 2010, ADA 2026, Reg. 1333/2008) envanterde yok | ORTA | Kırmızı çizgi 7 | Envantere satır (TÜBİTAK kaynakçasında hepsi doğrulanmış künyeyle var) |

## C. Kodda sabitlenmiş değerler (hardcode)

| # | Yer | Ne | Nereye taşınır |
|---|---|---|---|
| C1 | `service/nutriscan/matcher.py:12` | `FUZZY_CUTOFF = 0.88` | `data/config/esikler.toml` (geliştirme kümesinde sabitlenir) |
| C2 | `service/run_labels.py:18-19` | 7 durumun adı ve listesi | `data/kurallar/durumlar.csv` (`condition` tablosu) |
| C3 | `service/nutriscan/rules.py:6,85-90` | Dört sonuç metni ve önem sırası | Tek `Outcome` enum; CSV değerleri yüklemede doğrulanır |
| C4 | `rules.py:7,41-42` | Tuz → sodyum dönüşümü (2,5) | `data/kurallar/turetilen_alanlar.csv` (kaynak: 1169/2011 Ek I) |
| C5 | `rules.py:48-54` | `parametre` içinde mini dil: `yalniz_…`, `muaf=…`, bantlar | Ayrı sütunlar: `bagimlilik`, `muaf`, `bantlar` (şema [04](04-veri-modeli.md)) |
| C6 | `service/nutriscan/text.py:8,9,81,90` | Türkçe kalıp listeleri (beyanlar, "içerebilir", "içindekiler") | `data/sozluk/dil_kaliplari.toml` |
| C7 | `matcher.py:60` | Türkçe çoğul eki regex'i | Aynı dosya; ünlü uyumu testleriyle |
| C8 | `matcher.py:11`, `rules.py:5,10`, `run_labels.py:17` | Dosya yolları ve `kurallar_v0.csv` adı | Tek yapılandırma (`NUTRISCAN_DATA_DIR`) |
| C9 | `docs/diyagram/uret.py:105,122-131` | Elle yazılmış sayılar ve "2 onay" iddiası (gerçekte 0 onay) | Sayılar CSV'den hesaplanır; "taslak" diye düzeltilir |

## D. Veri kalitesi

- 50 takma ad birden çok kavrama gidiyor; eşleyici sessizce ilkini seçiyor (ör. "karoten" → E160A / en:carotene). → Belirsiz eşleşme `ambiguous` olarak işaretlenir, sonuç belirsizlik kuralına girer.
- `kavram.csv`'de 58 üst kavram kimliği yok (74 başvuru) ve 23 kimlik iki kez geçiyor; IS_A zinciri sessizce kısalıyor. → `kb validate` bunları hata sayar.
- `tests/eslesme/etiketler.csv` 3 satır, `tests/kurallar/` boş: planlanan 100 ifade ve 20 senaryo yok.
- Testler yalnız çölyak, diyabet ve KBH'yi çalıştırıyor; laktoz, sülfit, PKU, HT, "içerebilir", boş girdi için test yok. A1–A8'in hiçbiri testle yakalanmıyordu.

## E. Belge ve karar tutarsızlıkları

| # | Çelişki | Kazanan | Düzeltme |
|---|---|---|---|
| E1 | K9 "100 ifade + 20 senaryo" ↔ TÜBİTAK "≥ 400 + ≥ 40, 30/70, McNemar" | İkisi de, iki katman | Ö-01 ([12](12-karar-onerileri.md)) |
| E2 | Karar belgesi §4 kural türü 3 değer ↔ CSV 6 tür ↔ TÜBİTAK 5 tür | CSV'nin 6 türü | Ö-03, şema [04](04-veri-modeli.md) |
| E3 | K7 Qdrant "embedding edilip aranır" (belirsiz) ↔ TÜBİTAK: indeks = sözlük yazılışları, sorgu = eşleşmeyen ifade, top-5, eşik + fark | TÜBİTAK netliği | Ö-02 |
| E4 | K2 "liste 30 Ekim'de netleşecek": kayıt yok. 30 Ekim, 6 Kasım ve 13 Kasım toplantılarının kaydı depoda yok | — | Liste kararı Ö-05; eksik toplantı kayıtları ekip tarafından eklenir |
| E5 | `origin/hilal/meeting4-scope-docs` dalı K2'yi "14 alerjen grubunun tamamı" yapıyor; main'deki 26 Ekim ekip kararı bunun tersi | main (26 Eki) | Dal birleştirilmez; Hilal kapatır ya da günceller |
| E6 | §8 sahiplik tablosunda mobil/OCR, kural motoru ve LLM sahibi yok; TÜBİTAK iş paketleri bunları adlandırıyor | TÜBİTAK | Ö-06 |
| E7 | Bayat durumlar: AGENTS.md "K1–K12" (K13 var), README "4. toplantı sonrası", karar belgesi §9 "~6 Kasım ara rapor [teyit edilmedi]", TÜBİTAK durum satırı, ara rapor "being resubmitted" | — | Bu gece düzeltilenler §G'de; kalanlar ekip toplantısında |

## F. Sapma riski: projeyi bu noktaya kilitleyen önlemler

Sapma iki yoldan gelir: insanların ve agent'ların **eski bilgiyi güncel sanması** ve **kararların kodda sessizce
değişmesi**. Önlemler:

1. **Agent ayarları temizlendi (bu gece).** `.claude/settings.local.json` hâlâ Azure DevOps'ta iş kaydı açma/kapatma
   izni veriyordu; kaldırıldı (izin daraltma, geri dönüşlü).
2. **Hafıza temizlendi (bu gece).** Dört kayıt eski yönü (Java/Spring, Keycloak, Contabo, Azure, "mobil + web + admin
   zorunlu", hane planlama) güncel gibi anlatıyordu; "GEÇERSİZ / tarihsel" diye işaretlendi, güncel stack (K10) başa
   yazıldı.
3. **Tek doğruluk zinciri:** karar belgesi (ne) → `docs/tasarim/` (nasıl) → kod. Tasarımda karar belgesine aykırı bir
   şey yoksa ve olursa Ö-numarasıyla öneri olarak duruyorsa sapma görünür olur.
4. **Kodla zorlanan değişmezler** ([06 §2](06-kural-motoru.md)): taslak satır sonuç vermez, tanınmayan ya da boş girdi
   "Engel bulunmadı" vermez, LLM sonucu değiştiremez. Bunlar belge maddesi değil, CI'da koşan testlerdir.
5. **Değerlendirme bütünlüğü:** geliştirme/test ayrımı dosya karmasıyla kilitlenir; test ifadesi sözlüğe girerse
   değerlendirme betiği çalışmayı reddeder.
6. **Eski yön artıkları:** yerel `platform/AB131-*`, `platform/AB149-*`, `platform/mockito-agent-wip` dalları ve
   `.claude/worktrees/brave-taussig-5962df` worktree'si eski yönden kalma. Bir agent bunları güncel sözleşme
   sanabilir. **Silinmedi** (geri dönüşsüz işlem); öneri: `git tag arsiv/<dal>` ile etiketleyip silmek. Karar Levent'in.
   `plan/board/` (Azure dışa aktarımı, kişisel e-postalar) diskte duruyor; gitignore'da, silinmesi önerilir.

## G. Bu gece yapılanlar

- `.claude/settings.local.json`: iki Azure DevOps izin satırı kaldırıldı.
- Hafıza: `project_nutriscan_ekip_stack`, `project_nutriscan_vizyon`, `project_nutriscan_teslimler`,
  `reference_nutriscan_prototip`, `feedback_model_ve_tarayici` (Haiku → Sonnet), `project_tubitak_2209a`,
  `project_midterm_raporu` dizin satırları güncellendi.
- `docs/tasarim/` tasarım paketi yazıldı (bu dosya dahil). Kod ve veri davranışı **değişmedi**.
- `AGENTS.md`'deki "K1–K12" yazımı "K1–K13" yapıldı ve tasarım paketine bağlantı eklendi.

## H. Senin kararını bekleyenler

1. Eski dalların ve worktree'nin arşiv etiketiyle silinmesi (F6).
2. `plan/midterm/` git'e girsin mi? Depo herkese açık; raporda öğrenci numaraları var (proposal'da da var).
   Ara raporun teslim edildiği bilgisi depoda yok.
3. 30 Ekim, 6 Kasım ve 13 Kasım danışman görüşmelerinde ne karar verildiği; kayıtları `toplanti/` altına girmeli.
4. [12-karar-onerileri.md](12-karar-onerileri.md)'deki Ö-01…Ö-13'ün ekip toplantısında oylanması.
