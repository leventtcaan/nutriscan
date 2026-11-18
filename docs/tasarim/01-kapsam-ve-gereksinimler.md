# 01 · Kapsam ve gereksinimler

> **Durum:** ÖNERİ (18 Kasım 2026). Dayanak: karar belgesi v1.3 (K1–K13), TÜBİTAK 2209-A son metni
> (`plan/tubitak/2209a-basvuru-metni.md`), proposal v1 ve ara rapor (`plan/midterm/midterm-report.md`).
> Bu belge yeni karar vermez; kararları uygulanabilir gereksinimlere çevirir. Karar değişikliği gerektiren her
> nokta [12-karar-onerileri.md](12-karar-onerileri.md) dosyasında ayrı öneri olarak durur.

## 1. Ürün tek cümlede

Kullanıcı paketli gıdanın etiketini telefonla okutur, metni düzeltir. Sistem içindekiler listesindeki her ifadeyi
standart bir kavrama bağlar ve kullanıcının seçtiği her sağlık durumu için, gözden geçirilmiş kaynaklı kural tablosuna
dayanarak dört sonuçtan birini verir: **Uygun değil · Dikkat · Engel bulunmadı · Doğrulanamadı**. Her sonuç gerekçesi,
kaynağı ve kapsamıyla birlikte gösterilir.

## 2. Kapsam sınırları (v1 = CSE 491 finali + CSE 492)

| Kapsamda | Kapsam dışı | Dayanak |
|---|---|---|
| Tek etiket: fotoğraf → cihazda OCR → kullanıcı düzeltmesi → istek içinde analiz | Barkod, ürün kataloğu, tarama geçmişi | K1 |
| Etiketten kaynaklı kuralla kontrol edilebilen sağlık durumları (bugün 7 durum, 17 taslak satır) | İlaç etkileşimi, durumlar arası otomatik uzlaştırma | K2 |
| Sözlük + bulanık eşleşme; eşleşmeyenler için Qdrant'ta anlamsal aday arama | Adayı LLM'e onaylatma | K5; K7'nin açık işi için öneri Ö-02 |
| Kural tablosundan deterministik sonuç | LLM ya da benzerlik puanının sonuç vermesi | K5, K13 |
| LLM ile sade Türkçe açıklama (sonucu değiştirmeden), şablon yedeği | Sohbet asistanı, diyet planı | K11 |
| 14 alerjen grubunu bilgi alanı olarak gösterme | Alerjen gruplarını ana hedef yapma | K2 (26 Eki) |
| Mobil uygulama (Expo) | Web arayüzü, admin paneli | K10 |

## 3. Paydaşlar ve kullanıcı

- **Birincil kullanıcı:** Türkiye'de beslenmeyle ilgili bir durumu kendi yöneten ve satın almadan önce etiket okuyan yetişkin.
- **Ekip (küratör rolü):** sözlük ve kural satırlarını yazan, iki kişilik bağımsız incelemeyle etkinleştiren üç üye.
- **Danışman ve jüri:** sonuçların kaynağa dayandığını ve ölçümün tekrarlanabildiğini görmek ister.
- **TÜBİTAK hakemi:** H1/H2'nin önceden tanımlı protokolle sınandığını görmek ister.

## 4. Fonksiyonel gereksinimler

Kimlikler ara rapordaki numaralandırmayı izler. "Bileşen" sütunu [02-mimari.md](02-mimari.md) §3'teki C-kodlarıdır.

| ID | Gereksinim | Öncelik | Bileşen | Kabul ölçütü (test edilebilir) |
|---|---|---|---|---|
| FR-1 | Kullanıcı bir ya da birden çok sağlık durumu seçer. Profil telefonda tutulur, her analiz isteğiyle gönderilir, sunucuda saklanmaz. | must | C1 | Sunucu veritabanında ve loglarında profil alanı bulunmaz (şema + log incelemesi). |
| FR-2 | Etiket fotoğrafı cihazda OCR'dan geçer, kullanıcı içindekiler metnini ve besin değerlerini düzeltir. | must | C1 | 20 gerçek etikette OCR denemesi raporu; düzeltme ekranı her alanı düzenlenebilir sunar. |
| FR-3 | Metin ifadelere bölünür: parantezli alt bileşen, "sınıf: madde", "içerebilir" cümlesi ve beyanlar ("glutensiz") ayrılır; her ifadeye tür atanır. | must | C3 | `tests/` altında her kalıp için birim testi; beyanlarda olumsuzluk ("glutensiz değil") beyan sayılmaz. |
| FR-4 | Her ifade sırayla E-kodu → birebir → çoğul eki → bulanık eşleşmeyle bir kavrama bağlanır. | must | C4 | Sıra ve yöntem adı yanıtta görünür; eşik yapılandırmadan okunur. |
| FR-5 | FR-4'ün bağlayamadığı ifade için anlamsal aramadan en yakın 5 aday alınır; aday ancak eşik ve fark kuralını geçerse kabul edilir, yoksa sistem çekimser kalır. | must | C5 | Eşik altı adayda `method=abstain`; yanıt adayları ve puanları içerir. |
| FR-6 | Seçilen her durum yalnız **etkin** (iki bağımsız incelemeden geçmiş) kural satırlarıyla değerlendirilir ve dört sonuçtan biri döner. | must | C6 | Taslak satır üretim modunda hiçbir sonucu etkilemez (birim testi). |
| FR-7 | Miktar kuralı için gereken besin değeri yoksa uygulama kullanıcıdan ister, verilmezse sonuç "Doğrulanamadı" olur. | must | C6, C1 | `missing_inputs` alanı yanıtta döner; uygulama ilgili alanı vurgular. |
| FR-8 | Her sonuç için kural, kaynak belge ve bölüm, kullanılan veri ve kapsam gösterilir; CTD/JECFA kayıtları yalnız "araştırma bilgisi" başlığında görünür. | must | C6, C7, C1 | Yanıt şemasında `reasons[].source` zorunlu; `evidence` ayrı alan. |
| FR-9 | Kullanıcı mesajı yapılandırılmış sonuçtan LLM ile üretilir; denetim geçmezse ya da LLM yanıt vermezse şablon mesaj kullanılır. | should | C8 | Denetim kuralları testleri; LLM kapalıyken uçtan uca akış çalışır. |
| FR-10 | Ekip, sözlük ve kural satırlarını kod değiştirmeden, incelenmiş veri dosyalarıyla ekler; her satır inceleme durumunu taşır. | should | C9, C10 | Veri doğrulayıcı betik eksik alanlı ya da tek incelemeli etkin satırı reddeder. |
| FR-11 | Eşleşen ifadenin Türk Gıda Kodeksi alerjen grubu bilgi olarak gösterilir. | should | C4, C1 | Alerjen grubu sonucu değiştirmez (birim testi). |
| FR-12 | Yanıt, kullanılan sözlük, kural, eşik ve model sürümlerini taşır. | must | C2 | `versions` alanı her yanıtta dolu; aynı sürümle aynı girdi aynı yanıtı verir. |
| FR-13 | Kural tablosunda satırı bulunmayan durum için sonuç "Doğrulanamadı" ve kapsam notu döner. | must | C6 | Astım gibi kuralsız durumda test. |

## 5. Fonksiyonel olmayan gereksinimler

| ID | Gereksinim | Doğrulama |
|---|---|---|
| NFR-1 | **Determinizm:** aynı girdi + aynı sürümler → aynı sonuç. Anlamsal arama dahil (sabit model, sabit koleksiyon). | Senaryo testlerini iki kez çalıştırıp bayt düzeyinde karşılaştırma. |
| NFR-2 | **Belirsizlik riski yalnız artırır:** tanınmayan ifade, eksik veri ya da kuralsız durum asla "Engel bulunmadı" üretmez. | Özellik testi (property test): rastgele tanınmayan ifade eklenince sonuç hiç "daha güvenli" yöne gitmez. |
| NFR-3 | **Kural kökeni:** etkin her satır kaynak belge, bölüm, sürüm ve iki farklı inceleyici taşır. | `kb validate` betiği CI'da. |
| NFR-4 | **Gizlilik:** etiket metni ve sağlık profili sunucuda saklanmaz, loglara yazılmaz. | Log biçimi testi (yasaklı alan adı listesi), istek gövdesini loglamayan middleware. |
| NFR-5 | **Dil güvenliği:** LLM mesajı sonucu değiştirmez; "güvenli", "zararlı", "tetikler", "tedavi", "önler" ve teşhis dili yoktur. | Yasaklı kelime denetimi + sonuç sözcüğü eşleşme denetimi; test kümesindeki tüm mesajlarda. |
| NFR-6 | **Veri lisansı:** `data/kaynaklar.md` envanterinde kaydı olmayan veri depoya girmez. | Veri değişikliği PR'ında kontrol listesi + doğrulayıcı. |
| NFR-7 | **Gecikme:** OCR sonrası tipik etikette sonuç ≤ 3 sn (p95). | Test kümesinde zamanlama raporu. |
| NFR-8 | **Deney bütünlüğü:** test ifadeleri sözlüğe ve Qdrant koleksiyonuna girmez; eşik ve model geliştirme kümesinde sabitlenir. | Ayrım dosyalarının karması (hash) kayıtlı; değerlendirme betiği çakışmayı reddeder. |
| NFR-9 | **Yapılandırma:** eşik, dosya yolu, model adı, durum listesi kodda sabit yazılmaz. | Kod incelemesi kontrol listesi + `rg` ile sayısal sabit taraması. |
| NFR-10 | **Erişilebilirlik:** sonuç rengiyle değil ikon + metinle anlaşılır; dokunma alanı ≥ 44 pt; dinamik yazı boyutu kırılmaz. | Uygulama ekran görüntüleri + erişilebilirlik denetimi. |

## 6. İzlenebilirlik: hedef → gereksinim → test

| Hedef (TÜBİTAK 1.2) | Gereksinimler | Kanıt |
|---|---|---|
| 1. İnsan etiketli referans kümesi | NFR-8 | `eval/` veri kümesi, kappa raporu ([09](09-degerlendirme-protokolu.md)) |
| 2. Taban ve hibrit yöntemi karşılaştırma | FR-4, FR-5, NFR-1 | Eşleme deneyi raporu: doğruluk, yanlış kabul, çekimserlik, Recall@5, McNemar |
| 3. Hata analizi | FR-3, FR-4, FR-5 | Hata sınıfı tablosu |
| 4. Kaynaklı kural tablosu | FR-6, FR-10, FR-13, NFR-3 | `kb validate` çıktısı, iki inceleyicili satırlar |
| 5. Bütünleşik sınama | FR-1…FR-9, NFR-2, NFR-4 | Kural sınavı senaryoları, uçtan uca demo |

## 7. Değerlendirme hedefleri: iki katman

TÜBİTAK son metni ile karar belgesi K9 farklı ölçekler veriyor. Çelişki değil, aşamalı plan olarak okunur
(öneri [12 · Ö-01](12-karar-onerileri.md)):

| Aşama | Eşleme sınavı | Kural sınavı | Ne zaman |
|---|---|---|---|
| CSE 491 finali (K9) | 100 ifade, iki kişi etiketler | 20 ürün × durum senaryosu | ~18 Aralık 2026 |
| TÜBİTAK / CSE 492 | ≥ 400 ifade, Cohen kappa ≥ 0,80 hedefi, 30/70 geliştirme/test | ≥ 40 senaryo | 12 aylık İP1–İP5 |

İlk 100 ifade ve 20 senaryo, ikinci aşamanın geliştirme kümesinin çekirdeği olur. Bu yüzden ilk günden aynı biçim
(şema, kılavuz) kullanılır ve iş iki kez yapılmaz.
