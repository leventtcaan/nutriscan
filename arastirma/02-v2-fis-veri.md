> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24**
> Soru: "Türk market fişinden v2 için gereken veriyi (ürün, miktar, fiyat → sepet karnesi, kişisel enflasyon, akıllı takas) güvenilir çıkarabilir miyiz, nerede kırılır?"
> `01-veri-fizibilite.md` (OFF kapsamı, TürKomp/USDA/marketfiyati ilk tarama, vision-LLM maliyeti) ve `01-mevzuat-risk.md` (KVKK genel, yurt dışı aktarım) **tekrar edilmedi**, gerektiğinde atıf var.
> Etiketler: **[değerlendirme]** = kaynağa dayanmayan kendi yorumum · **[VARSAYIM]** = ölçülmemiş sayı, doğrulanması gerekir · **bulunamadı** = aradım, kaynak yok.

# v2 — Fişten Veri: Fizibilite ve Kırılma Noktaları

## 0. Özet hüküm tablosu

| Alt başlık | Hüküm | Tek cümle |
|---|---|---|
| 1a. Kâğıt ÖKC fişinde yapılandırılmış veri (QR/barkod) | 🔴 | GİB'in fiş formatında QR ya da barkod yok; satırda yalnız "mal cinsi + KDV oranı + tutar" zorunlu. Tüketicinin kâğıt fişi GİB'den doğrulayabileceği bir servis **bulunamadı**. |
| 1b. e-Arşiv / online sipariş faturası | 🟢 (online) / 🟡 (mağaza) | e-Arşiv'in resmî hâli satırlı UBL-TR XML. A101 portalı XML/PDF veriyor, Migros Sanal Market son 1 yılı indirtiyor. Mağaza alışverişinde e-Arşiv ancak kasada istenirse çıkıyor. |
| 2a. Fiş fotoğrafından satır okuma (vision LLM) | 🟡 | Genel fiş benchmark'larında en zor alan satırlar (structure parsing F1 0,30–0,65). Türkçe fiş için yayımlanmış ölçüm ve açık veri seti **bulunamadı**. |
| 2b. Satır → ürün (SKU) eşleştirme | 🔴 soğuk başlangıçta / 🟡 topluluk sözlüğüyle | İsviçre çalışmasında zincirlerin dijital fişinde bile barkod (GTIN) yok. Elle eşlenen 5.950 ürün alımların %69,6'sını kapsamış, yani uzun kuyruk var ama yönetilebilir. |
| 3. Eşleşmeyen satırda kategori düzeyi beslenme tahmini | 🟡 | Ciqual (açık lisans) ve USDA (CC0) hazır. TürKomp ticari kullanımda ücretli, "program içinde kullanım" için sözleşme gerekiyor. Asıl kırılma **kütle bilgisinin yokluğu**. |
| 3b. Satın alma → diyet kalitesi geçerliliği | 🟡 | Literatürde satın alma–tüketim korelasyonu orta düzeyde (ρ 0,31–0,57). Ürün "diyet" değil **"sepet" karnesi** olarak konumlanmalı. |
| 4a. Topluluk fiyat verisi (KVKK + kalite) | 🟡 | Fiyat tek başına kişisel veri değil; "kullanıcı + mağaza + zaman" birleşimi kişisel veri. Anonimleştirme + k-eşiği + sahte veri kontrolüyle yapılabilir. |
| 4b. Kişisel enflasyon metodolojisi | 🟢 (TÜİK alt endeksleri × kişisel ağırlık) / 🟡 (topluluk fiyatlı ürün düzeyi endeks) | Kişisel ağırlık fişten gelir, fiyat değişimi resmî alt endeksten alınır; bu, az veriyle de sağlam çalışır. Ürün düzeyi endeks veri yoğunluğu ister. |
| 5. marketfiyati.org.tr kataloğu | 🔴 izinsiz / 🟢 izinle (değeri çok yüksek) | 7 zincirin ~50 bin ürünü, marka ve kategori içeriyor; eşleştirme hedefi olarak ideal. Kullanım Koşulları yazılı izin şartı koyuyor. İletişim adresleri aşağıda. |

**Tek cümlelik hüküm [değerlendirme]:** Fişten *toplam tutar, tarih, mağaza* güvenilir. *Satırlar* okunur ama doğrulama ister. *Satır → ürün* ancak topluluk sözlüğü büyüdükçe güvenilir olur. *Satır → kütle (gram)* ise sepet karnesinin gerçek darboğazı.

---

## 1. Türk perakende fişinin yapısı ve dijital kanallar

### 1.1 Yeni Nesil ÖKC fişi: zorunlu minimum içerik
GİB'in 16 Aralık 2025'te yayımladığı taslak kılavuzdaki nakit fiş örneğinde şu alanlar zorunlu ([GİB taslak kılavuz, Bölüm 2.1–2.2](https://ynokc.gib.gov.tr/UploadedFiles/Files/yn-okc-fis-ve-e-belge-formatlari-kilavuz_taslak_16122025.pdf), [duyuru](https://ynokc.gib.gov.tr/Home/DuyuruDetay/11136)):
- İşletme adı (tabela), ünvan, adres, vergi dairesi, VKN/TCKN, telefon
- Tarih, saat, **FİŞ NO**
- Satırlar: **"Mal cinsleri, vergi oranları ve vergi dâhil satış tutarları"**. Örnek satır: `EKMEK %1 *12,00`
- TOPKDV, TOPLAM, ödeme türü ve tutarı
- MERSİS no, internet sitesi (varsa)
- **EKÜ NO, Z NO, MF + firma kodu + cihaz sicil numarası**
- Kartlı ödemede POS bilgisiyle birleşik tek belge (bütünleşik fiş).

**Sonuçlar:**
- Fiş formatında **QR/karekod yok, barkod yok**. Metin taraması boyunca "karekod" yalnız e-Belge çıktıları ve ödeme türü raporları (TR Karekod ile ödeme) için geçiyor (aynı kaynak).
- Asgari formatta **adet ve birim fiyat zorunlu değil.** Zincir fişlerinde "adet × birim fiyat" ya da "kg × fiyat" satırları görülüyor, ama bu biçim standart değil **[değerlendirme; sistematik kaynak bulunamadı]**.
- Satırdaki **KDV oranı** gıda/gıda dışı ayrımı için bedava ama zayıf bir sinyal (GİB örneğinde ekmek %1, şampuan %20) **[değerlendirme]**.
- **Tekil fiş anahtarı:** Cihaz sicil no + Z no + fiş no + tarih her fişte zorunlu. Mükerrer yükleme tespiti için doğal bir anahtar **[değerlendirme]**.
- Durum: Kılavuzun 1 Temmuz 2026'da yürürlüğe girmesi planlanmıştı ([PwC özeti](https://www.pwc.com.tr/tr/hizmetlerimiz/vergi/dolayli-vergi/bultenler/e-donusum-bultenleri/2025/yn-okc-lerden-duzenlenecek-fis-e-belge-ve-diger-belgeler-ile-rapor-formatlarina-iliskin-teknik-kilavuz-taslagi-hazirlanmistir.html), arama özeti; sayfa bana 403 verdi). 24 Eylül 2026 itibarıyla ynokc.gib.gov.tr duyurularında **nihai sürümün yayımlandığını bulamadım**. Duyurularda yalnız Taksi Mali Cihaz kılavuzları var.

### 1.2 2026 düzenlemesi: ÖKC'den e-Belge
- **VUK Genel Tebliği Sıra No 593** (RG 8 Mayıs 2026, sayı 33247): YN ÖKC'ler e-Belge (e-Fatura, e-Arşiv vb.) düzenleyebilecek ([Tebliğ PDF](https://ynokc.gib.gov.tr/UploadedFiles/Files/vuk_593_20260508.pdf)).
- Tebliğ TSM'nin görevleri arasında fiş, belge ve raporların **"elektronik ortamda müşteriye iletilmesi"** hizmetini sayıyor (md. 3/ğ). Altyapı dijital fişi öngörüyor. Ancak tüketiciye fişi elektronik iletmeyi **zorunlu kılan** bir hüküm ya da tüketici API'si **bulunamadı**.
- Taslak kılavuza göre ÖKC'den basılan e-Belge çıktısında **erişim/doğrulama bağlantılı QR** ve imza değerinin ilk 20 karakteri zorunlu ([taslak kılavuz, Bölüm 3](https://ynokc.gib.gov.tr/UploadedFiles/Files/yn-okc-fis-ve-e-belge-formatlari-kilavuz_taslak_16122025.pdf)).
- **[değerlendirme]** Orta vadede fırsat: Kullanıcı kasada e-Arşiv isterse, fişte QR → GİB doğrulama → (satıcı e-postası ya da portal üzerinden) satırlı XML akışı mümkün olabilir. Bugün tüketici için bu akışın uçtan uca çalıştığını gösteren kaynak **bulunamadı**.

### 1.3 e-Arşiv faturası: yapılandırılmış veri var, erişim dolaylı
- **Karekod (1 Eylül 2023'ten beri zorunlu)** şu alanları içeriyor: gönderen/alıcı VKN-TCKN, senaryo, tip, tarih, fatura no, ETTN, para birimi, mal/hizmet tutarı, KDV matrahı, hesaplanan KDV, vergiler dahil toplam, ödenecek tutar. **Satır bilgisi yok** ([Gri Portal – GİB Karekod Standardı özeti](https://www.griportal.com/blog/e-belgelerde-karekod-zorunlulugu/)).
- Doğrulama: ETTN + satıcı VKN ile GİB e-Arşiv sorgulama ([ebelge.gib.gov.tr](https://ebelge.gib.gov.tr/earsivsorgula.html)). Bu, faturanın **varlığını ve toplamlarını** doğrular, satırları vermez.
- e-Arşiv Portal'ın "adıma düzenlenen belgeler" ekranı **yalnız liste gösteriyor**, içerik göstermiyor ([MDP Group](https://mdpgroup.com/blog/tarafiniza-duzenlenen-e-arsiv-faturalar-nasil-goruntulenir/); 01 raporunda da tespit edilmişti).
- XML'in kendisi (UBL-TR) satırlı: `InvoiceLine/Item/Name` var. Satıcı, üretici ve alıcı ürün kimliği alanları **opsiyonel** ([UBL-TR Ortak Elemanlar](https://dev.izibiz.com.tr/resource/BELGELER/UBL-TR%20Ortak%20Elemanlar%20-%20V%200.7.pdf)). Zincirlerin bu alana GTIN/barkod yazıp yazmadığı **bulunamadı**; örnek XML ile test edilmeli.

### 1.4 Zincir marketler: dijital fiş / e-Arşiv kanalları

| Zincir | Mağaza alışverişi | Online sipariş | Format | Kaynak |
|---|---|---|---|---|
| **Migros** (mağaza) | Kasada e-Arşiv istenirse **"e-Arşiv bilgi fişi"** verilir; linkte VKN/TCKN + referans no ile faturaya ulaşılır; fatura **7 iş günü içinde** oluşur | — | Link (format belirtilmemiş) | [Migros Kurumsal SSS](https://www.migroskurumsal.com/sikca-sorulan-sorular) |
| **Migros Sanal Market** | — | "Siparişlerim"den **son 1 yılın** e-Arşiv faturaları indirilebilir | İndirilebilir fatura | [Migros Kurumsal SSS](https://www.migroskurumsal.com/sikca-sorulan-sorular) |
| **Migros Money** | Uygulamada "alışveriş geçmişi"yle harcamalar izlenebiliyor | — | **Ürün düzeyinde dijital fiş gösterip göstermediği doğrulanamadı** | [Money SSS](https://www.money.com.tr/mc/iletisim/sikca-sorulan-sorular/69) |
| **A101** | Kasada e-Arşiv istenirse e-posta alınarak düzenleniyor (arama özeti; SSS sayfası bana 403 verdi) | Kapıda: üyelik e-postasına gidiyor; "Sipariş Detayı → Faturayı Gör" | **fatura.a101.com.tr**: Belge No/ETTN/Fatura No + tarih + tutar + captcha → **"Xml İndir" / "Pdf İndir"** (sayfayı kendim kontrol ettim) | [A101 fatura portalı](https://fatura.a101.com.tr/), [A101 Kapıda SSS](https://www.a101.com.tr/kapida/sikca-sorulan-sorular/fatura) |
| **BİM** | Kasada VKN/TCKN + e-posta ile e-Arşiv; "bilgi fişi" + sorgulama sorunlarına dair şikâyetler var | Yok | Resmî kaynak **bulunamadı** | [Şikayetvar (anekdot)](https://www.sikayetvar.com/bim/e-arsiv-fatura) |
| **ŞOK / Cepte ŞOK** | **Bulunamadı** | Cepte ŞOK sipariş faturası formatı **bulunamadı** | — | — |
| **CarrefourSA** | "Fatura bulucu" sayfası fiş bilgisiyle sorgu yapıyor (sayfa bana 403 verdi) | Hesabım → Faturalarım → e-Arşiv | Belirtilmemiş | [Fatura bulucu](https://www.carrefoursa.com/fatura-bulucu) |
| **Trendyol (Go dahil)** | — | Bireysel e-Arşiv **PDF olarak e-postaya** gider, "Siparişlerim"den indirilebilir | PDF | [Yengeç](https://yengec.co/blog/trendyol-e-faturam-rehberi/) (ikincil; Go'ya özel kaynak bulunamadı) |
| **Getir / GetirBüyük** | — | **Bulunamadı** | — | — |

**Bölüm sonucu [değerlendirme]:**
- **En temiz kanal online sipariş faturası.** PDF/XML, satırlı, muhtemelen tam ürün adıyla geliyor (tam ad varsayımı test edilmeli).
- Mağaza alışverişinde yapılandırılmış veri ancak kullanıcı kasada e-Arşiv isterse var. Bu kullanıcıya ek sürtünme; ana kanal kâğıt fiş fotoğrafı olarak kalıyor.
- Hiçbir zincirin tüketiciye açık **API'si** bulunamadı (01 raporundaki sadakat programı bulgusuyla tutarlı).

### 1.5 Kapsama kör noktaları
- **Semt pazarı:** "Pazar takibi suretiyle iş yapanlar" ÖKC kullanma mecburiyeti dışında ([GİB – ÖKC mecburiyeti dışında bırakılanlar](https://ynokc.gib.gov.tr/UploadedFiles/Files/okckullanimindanmuaftutulanlar.pdf)). Yani pazardan alınan sebze-meyvenin çoğu zaman fişi yok. Sepet karnesi sistematik olarak **meyve-sebzeyi eksik sayar** ve sonuç "kötü sepet" yönüne kayar **[değerlendirme]**.
- Termal kâğıt zamanla soluyor. Qumpara aynı gün yüklemeyi öneriyor ([Qumpara rehber](https://qumpara.com/rehber/fis-yukleyerek-para-kazanma)).
- Fırın, bakkal, kasap fiş verse bile kullanıcının yüklemeyi unutması; dışarıda yeme (bkz. 3.3).

### 1.6 Türkiye'de emsal (rakip değil, fizibilite kanıtı)
- **Qumpara:** Fişi otomatik okuyor ("genellikle 24 saat içinde otomatik okuma sistemi"). Aynı fiş ikinci kez yüklenemiyor. e-Arşiv ve online faturalar PDF ya da ekran görüntüsü olarak kabul ediliyor ([Qumpara](https://qumpara.com/rehber/fis-yukleyerek-para-kazanma)). Doğruluk ya da hacim rakamı yayımlanmamış.
- Satır çıkardığını söyleyen uygulamalar: Akıllı Fiş ("Şok, Bim ve Migros için özel fiş okuma"), FişMatik ([App Store](https://apps.apple.com/tr/app/ak%C4%B1ll%C4%B1-fi%C5%9F-b%C3%BCt%C3%A7e-takibi/id6761904988?l=tr), [FişMatik](https://kfsoftware.app/apps/fismatik/)). Doğruluk rakamı yok.
- GitHub'da benzer öğrenci projeleri var: "fiş OCR + AI ile ürün tanıyan" kiler uygulaması, açıkça "bitirme tezi projesi" ([Tazelyx](https://github.com/omer-damar/Tazelyx)); fiş OCR ile erzak takibi ([Optura](https://github.com/Egebo/Optura)). **[değerlendirme]** "Fiş okuma" tek başına özgün katkı değil. Özgünlük eşleştirme, sepet metrikleri ve takas optimizasyonunda olmalı (özgünlük raporuyla birlikte okunmalı).

---

## 2. Fiş satırını okumak ve gerçek ürüne eşlemek

### 2.1 Neden zor
- Satır kısaltmaları kasa yazılımındaki kısa ada bağlı; barkod basılmıyor (1.1).
- Aynı ürün farklı zincirde farklı kısaltılıyor. **[değerlendirme]** Sözlük zincir başına tutulmalı.
- Türk fişlerine özgü kısaltma sözlüğü, kısaltma istatistiği ya da örnek derlemesi **bulunamadı**. "ULK.CIK.GOF 36G" gibi örnekler şimdilik varsayımsal. İlk iş, ekipten 50–100 gerçek fiş toplamak.
- Ek satır türleri: indirim satırları, çoklu alım, tartılı ürün (kg × fiyat), iade, poşet, sepet düzeyinde sadakat indirimi **[değerlendirme]**.

### 2.2 Fiş anlama benchmark'ları ve vision-LLM doğruluğu (2025–2026)

| Kaynak | Veri | Bulgu |
|---|---|---|
| **SROIE** (ICDAR 2019) | 626 eğitim / 347 test fişi; yalnız 4 alan: şirket, tarih, adres, toplam | **Satır içermiyor**; satır okumayı ölçmez ([arXiv 2103.10213](https://arxiv.org/pdf/2103.10213)) |
| **CORD** | 1.000 Endonezya fişi, satır (menü) düzeyi etiket | Satırlı tek klasik set ([CORD](https://scispace.com/pdf/cord-a-consolidated-receipt-dataset-for-post-ocr-parsing-2kln2mk844.pdf)) |
| **ReceiptBench** (Wang vd., 2026) | 10.656 gerçek fiş, %98 İngilizce | En iyi genel F1: Qwen3-VL-8B (SFT+GRPO) 0,795; Gemini-3-Pro 0,737; GPT-5 0,708. **Structure parsing (satırlar) 0,30–0,65**, en zor alan. Kritik hata türü: **"aritmetik tutarlılık için halüsinasyon"**, yani model toplam tutsun diye satır fiyatını değiştiriyor ya da olmayan vergi kalemi uyduruyor ([arXiv 2605.22413](https://arxiv.org/html/2605.22413v1)) |
| **Fatura/fiş LLM karşılaştırması** (2025) | SROIE 1.000 fiş | Görselden doğrudan: Gemini 2.5 Pro %87,46, Gemini 2.5 Flash %82,15, GPT-5 Chat %69,21. Önce metne çevirip parse etmek: %42–47. **Görseli doğrudan vermek belirgin daha iyi** ([arXiv 2509.04469](https://arxiv.org/html/2509.04469)) |
| **Türkçe OCR/VLM benchmark** (Yılmaz vd., IJDAR 2026) | 6.600 sentetik görsel (basılı, el yazısı, sahne) | VLM'ler klasik OCR'ı geçiyor. Türkçe karakterler (ç, ğ, ı, İ, ö, ş, ü) tüm modelleri zorluyor; yalnız GPT-4o kararlı kalmış. Qwen2.5-VL açık kaynakta GPT-4o'ya yakın ([DOI](https://doi.org/10.1007/s10032-026-00613-6), [ön baskı](https://www.researchsquare.com/article/rs-7797886/latest.pdf)) |

- **Türkçe fiş veri seti:** Hugging Face'te "turkish receipt" araması sonuç vermedi. GitHub'da yalnız birkaç örnek görsel içeren depolar var ([ör.](https://github.com/kaptanmajere/azure-receipt-reader)). **Etiketli, kamuya açık Türkçe market fişi veri seti bulunamadı.** Bu hem risk hem katkı fırsatı (ör. 150–300 fişlik anonimleştirilmiş eval seti) **[değerlendirme]**.
- **Uzun fiş sorunu [değerlendirme]:** Vision API'leri görseli bir üst sınıra kadar küçültüyor (01, §3.2). 40+ satırlık uzun fişte küçük punto okunmaz hâle gelebilir. İstemci fişi 2–3 dilime bölüp üst üste binen bölgelerle göndermeli.
- **Aritmetik kontrol şart ama modele bırakılmamalı [değerlendirme]:** Satır toplamı = TOPLAM ve KDV'ler = TOPKDV kontrolü **kod içinde** yapılmalı. Tutmazsa model düzeltmez, kullanıcıya "şu satırı kontrol et" denir. ReceiptBench'teki halüsinasyon türü tam da bu kontrolü modele yaptırınca ortaya çıkıyor.

### 2.3 Satır → ürün eşleştirme (entity resolution) literatürü

| Çalışma | Ne yaptı | Sayı |
|---|---|---|
| **Melz, "Understanding Scanned Receipts"** (arXiv 2020) | Kroger fiş satırı → ürün KB'si, Lucene tabanlı IR (wildcard, "mashed" terimler, PMI n-gram, fuzzy) | 65 fiş, 711 satır; doğruluk **0,47 → 0,79** ([arXiv 2005.01828](https://arxiv.org/abs/2005.01828)) |
| **Tan, Tan, Recario** (Intelligent Computing, 2024) | Filipin market fişi ürün adlarını KNN + LSTM ile açma | KNN ortalama "similarity ratio" %92,63. Metrik doğruluk değil benzerlik oranı, dikkatli okunmalı ([Springer](https://link.springer.com/chapter/10.1007/978-3-031-62281-6_26)) |
| **Wu vd., Nutrients 2021 (İsviçre)** | Migros ve Coop sadakat kartı dijital fişleri; **fişte GTIN yok**, eşleştirme elle | 464 kullanıcıda 65.391 farklı ürün. En sık **5.950 ürün kimliği** elle eşlendi → alımların **%69,6**'sı kapsandı. Yazarlara göre çoğunluğu yakalamak için ürünlerin **%10'undan azını** tanımlamak yetiyor ([DOI](https://doi.org/10.3390/nu14010159)) |
| **USDA Purchase to Plate Crosswalk** | IRI/Circana tarayıcı verisi (UPC) → FNDDS besin kodları; olasılıksal + semantik + elle | 650.592 UPC → 4.390 besin kodu (2013); **eşleme hatası < %5** ([ERS](https://www.ers.usda.gov/data-products/purchase-to-plate), [data.gov özeti](https://resources.data.gov/resources/fdspp-usda-linked-nutrition-data/)) |
| **Peeters, Steiner, Bizer** (EDBT 2025) | LLM ile ürün eşleştirme (WDC Products) | Görülmemiş ürünlerde GPT-4, transfer edilmiş PLM'leri **%40–68 F1** farkla geçiyor. En iyi LLM'ler sıfır ya da az örnekle, binlerce örnekle eğitilmiş PLM'e yaklaşıyor. Prompt model/veri çiftine göre ayarlanmalı ([arXiv 2310.11244](https://arxiv.org/html/2310.11244v4)) |

**Çıkarımlar:**
1. **Uzun kuyruk ama Pareto:** İsviçre verisi, en sık birkaç bin ürünü çözmenin alımların çoğunu kapsadığını gösteriyor. Topluluk sözlüğü stratejisi bu dağılım yüzünden işe yarar **[değerlendirme]**.
2. **Zincir dijital fişi bile GTIN vermiyor** (İsviçre). Türkiye'de de fişte barkod olmayacağını baştan kabul etmek gerek.
3. **LLM eşleştirici güçlü ama aday listesiyle sınırlanmalı [değerlendirme]:** Serbest üretimde model olmayan ürün uydurabilir. Katalogdan getirilen top-k aday + "hiçbiri" seçeneği ile rerank daha güvenli.

### 2.4 Önerilen eşleştirme hattı [değerlendirme]
1. **Ayrıştır:** VLM → JSON (satır metni, adet, birim fiyat, satır tutarı, KDV %, indirim bağlantısı). Aritmetik ve KDV kontrolü kodda yapılır.
2. **Normalize:** Türkçe büyük/küçük harf (İ/ı), nokta ve kısaltma ayrımı, gramaj/hacim çıkarımı (`36G`, `1L`, `0,745 KG`).
3. **Sözlük isabeti:** `(zincir, normalize satır metni)` → onaylı ürün. Topluluk oyu ≥ N ve çelişki yoksa otomatik kabul edilir.
4. **Aday üretimi:** Katalogdan (OFF TR alt kümesi, izin varsa marketfiyati kataloğu, kendi ürün tablomuz) fuzzy + embedding ile top-k aday.
5. **LLM rerank:** Yalnız adaylar arasından seçim veya "hiçbiri"; kalibre güven skoru.
6. **Kategori fallback:** SKU yoksa bile kategori (ör. "gofret", "UHT süt", "domates") atanır. Sepet karnesinin çoğu için yeterli.
7. **Kullanıcı onayı:** Düşük güvenli satır için tek dokunuşlu aday listesi. Onaylar 3. adımdaki sözlüğü besler.
8. **Ölçüm:** Satır okuma F1, SKU top-1, kategori doğruluğu, fiş başına onay süresi. Hedef değerler ekip eval setiyle belirlenir.

---

## 3. Eşleşmeyen satır için beslenme tahmini

### 3.1 Asıl kırılma: kütle (gram) bilinmiyor [değerlendirme]
Kişi başı şeker/tuz/doymuş yağ hesabı için **kaç gram** alındığı gerekir. Fiş bunu:
- **tartılı** üründe veriyor (kg),
- bazen **ad içinde** veriyor (`36G`, `1L`),
- paketli üründe çoğu zaman **vermiyor**. Gramaj ancak SKU eşleşirse ürün kaydından gelir.

Kategori fallback'inde bir de **varsayılan paket boyu** tahmini gerekir; hata payı burada katlanır. Bu yüzden:
- **Oran metrikleri** (1000 kcal başına şeker, harcama payı, ultra-işlenmiş harcama payı) **mutlak gram metriklerinden** daha güvenilir. İsviçre çalışması da yoğunluk tabanlı göreli ölçülerin mutlak alımdan daha güçlü korelasyon verdiğini raporluyor ([Wu vd. 2021](https://doi.org/10.3390/nu14010159)).
- Her metrik "kapsama" göstergesiyle sunulmalı (ör. "sepetin %72'si ürün düzeyinde, %20'si kategori tahmini, %8'i bilinmiyor").

### 3.2 Kategori → ortalama besin profili kaynakları

| Kaynak | Kapsam | Erişim / lisans | NutriScan için |
|---|---|---|---|
| **TürKomp** | 14 gıda grubu, **645 gıda**, 100 bileşen, ~63.000 değer ([TürKomp](https://turkomp.tarimorman.gov.tr/main)) | Kişisel kullanım bedelsiz. **Ticari kullanım ayrı sözleşme ve ücretle.** Bilgisayar programı ya da sitede kullanımda **yıllık** ücret. 2026 tarifesi (KDV hariç): 1 ürün 3.052 TL · 26–100 ürün 75.902 TL · 251–645 ürün 176.065 TL. Yetkili kurum: Bursa Gıda ve Yem Kontrol Merkez Araştırma Enstitüsü, bursagida@tarimorman.gov.tr. Kaynak gösterimi zorunlu ([Veri kullanımı](https://turkomp.tarimorman.gov.tr/useofdata)). **API bulunamadı** | Türk jenerik gıdaları (ekmek, beyaz peynir, bulgur) için en doğru kaynak. Akademik ve ticari olmayan kullanım için **yazılı izin** istenmeli; "kişisel kullanım" bir uygulamayı kapsamıyor **[değerlendirme]** |
| **Ciqual 2025 (ANSES, Fransa)** | 3.484 gıda, 74 bileşen | **Licence Ouverte Etalab 2.0**, XLS/XML indirilebilir ([Ciqual 2025](https://ciqual.anses.fr/cms/en/2025-anses-ciqual-table), [Recherche Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FRDMHWY)) | Hukuken en temiz jenerik kaynak. Türk ürünlerine (sucuk, tahin helva vb.) eşleme elle yapılmalı |
| **USDA FoodData Central / FNDDS** | Geniş; FNDDS "yiyecek kodu → besin" | CC0 (01, §2) | Kategori ortalaması için yedek. ABD formülasyonu farklı olabilir |
| **OFF kategori ortalamaları** | OFF ürün sayfasında "Compared to: <kategori>" altında kategori ortalaması 100 g başına gösteriliyor (Nutella sayfasında "Cocoa and hazelnuts spreads" ile kendim kontrol ettim, [örnek](https://world.openfoodfacts.org/product/3017624010701)) | ODbL. Ayrı bir kategori ortalaması API'si **bulunamadı**; mirror'dan kendimiz hesaplayabiliriz | TR ürünleriyle kendi ortalamamız: kategori başına medyan + çeyrekler arası aralık. TR'de NOVA doluluğu ~%10 (01, §1.6), yani **ultra-işlenmiş oranı OFF'tan gelmez**; kendi sınıflandırıcımız gerekir |

### 3.3 Satın alma verisinden diyet kalitesi: yöntemler ve bilinen limitler
- **GPQI-2016 (USDA):** Satın alımlar USDA Food Plan'ın **29 kategorisine** eşleniyor. Harcama payı, standart paylarla karşılaştırılıyor. HEI'ye paralel 11 bileşen ([Brewster vd.](https://www.sciencedirect.com/science/article/abs/pii/S0889157517301667)). HEI-2015 ile karşılaştırmada bileşen korelasyonlarının en zayıfları Süt 0,67, Rafine tahıl 0,66, Tatlı/şekerli içecek 0,65 (arama özetinden; [JAND](https://www.sciencedirect.com/science/article/abs/pii/S2212267218308487)). Hane skorunun bireyi temsil edip etmediği ayrıca tartışmalı ([BJN 2020](https://pubmed.ncbi.nlm.nih.gov/33267922/)).
  - **[değerlendirme]** GPQI'nin "harcama payı" mantığı bizim veriye doğal uyuyor. Kütle bilinmese de TL payı bilinir. MVP'de "sepet karnesi"nin bir bacağı harcama payı tabanlı olabilir.
- **Supreme Nudge (Hollanda, n=227):** Sadakat kartı alımlarından hesaplanan diyet kalitesi ile FFQ arasında **ρ = 0,31**. Satın alma skoru sistematik olarak **daha düşük** çıkıyor ([Colizzi vd., BJN 2024](https://doi.org/10.1017/s0007114524002630)).
- **İsviçre (n=89, iki zincirin dijital fişi):** Beş indeks karşılaştırılmış (FSA-NPS DI, GPQI, HEI-2015, HETI, HPI). **En iyisi FSA-NPS DI.** Bildirilen limitler ([Wu vd. 2021](https://doi.org/10.3390/nu14010159)):
  - israf, hazırlama, **dışarıda yeme**, gecikmeli tüketim,
  - hane içi paylaşım (örnekleri: evde et alınıyorsa vegan bireyin de et yediği varsayılıyor),
  - besin veritabanı eksikleri,
  - %69,6 eşleşme oranı.
- **Appelhans vd. (IJBNPA 2017, ABD, N=196 hane):** 14 günde 16.356 satın alma kalemi fişle toplanmış; araştırmacılar evleri 4 kez ziyaret edip her ürünün ambalajını ve besin tablosunu fotoğraflamış. Satın alma HEI-2010'u ile 24 saatlik hatırlama arasında **ρc = 0,57** (orta uyum). Sonuçları: genel diyet kalitesi için makul, ama **tekil besin öğelerini (ör. şeker, sodyum) tahminde daha az kullanışlı** ([DOI](https://doi.org/10.1186/s12966-017-0502-2)). **[değerlendirme]** Bu, bizim "kişi başı şeker/tuz" hedefimizin en zayıf halka olduğunu gösteriyor. Üstelik onlarda ambalaj fotoğrafı vardı, bizde yok.
- **İsraf:** Küresel hane gıda israfı kişi başı **79 kg/yıl** ([UNEP Food Waste Index 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024)). Türkiye'ye özgü güncel UNEP rakamını doğrulayamadım.
- **Tasarım sonucu [değerlendirme]:**
  - Ürün "ne yediğin"i değil **"eve ne girdiği"ni** puanlamalı; dil buna göre kurulmalı ("sepet karnesi", "diyet skoru" değil).
  - Kişi başına bölme için hane büyüklüğü + yaş grubu sorulmalı ve sonuç aralıkla gösterilmeli.
  - Pazar ve dışarıda yeme için "bu ay pazardan/dışarıdan ne kadar?" gibi tek soruluk düzeltme alınabilir.

---

## 4. Topluluk fiyat verisi ve kişisel enflasyon

### 4.1 KVKK: fiş kişisel veri mi?
- **Fiş fotoğrafı** kişisel veri içerebilir: maskeli kart numarası, sadakat kartı ya da telefon bilgisi, e-Arşiv'de TCKN, mağaza + saniye hassasiyetinde zaman. KVKK, sadakat kartı ve telefon numarasının alışverişte kullanımını ayrıca düzenlemiş ([ilke kararı duyurusu](https://www.kvkk.gov.tr/Icerik/8899/sadakat-kart-uyeligi-bulunan-bir-kisinin-cep-telefonu-numarasinin-veya-sadakat-kart-numarasinin-ucuncu-bir-kisi-tarafindan-alisveris-esnasinda-kullanilmasi-hakkinda-ilke-karari-nda-veri-sorumlulari-icin-ongorulen-uyum-suresinin-uzatilmasi-hakkinda-kamuoyu-duyurusu)).
- Hesaba bağlı **alışveriş geçmişi** kişisel veri: kimliği belirli kişiye ilişkin bilgi (KVKK m.3). Mobil uygulama rehberinde satın alma, tutar ve tarih bilgileri kişisel veri örnekleri arasında ([KVKK mobil uygulama tavsiyeleri](https://www.kvkk.gov.tr/SharedFolderServer/CMSFiles/8ba209bb-fa93-4479-84f0-dd55aac97a0f.pdf)).
- **Sağlık çıkarımı riski [değerlendirme]:** Glutensiz, diyabetik ya da bebek maması gibi alımlar sağlık durumuna işaret edebilir. Alışveriş geçmişi özel nitelikli veriye yaklaşır; sağlık profiliyle birleştiğinde kesinlikle öyle olur (01-mevzuat-risk §1).
- **Anonim veri KVKK dışında** (01-mevzuat-risk). Yönetmelik ve Rehber'deki yöntemler: maskeleme, genelleştirme, alt/üst sınır kodlama, toplulaştırma, **k-anonimlik, l-çeşitlilik, t-yakınlık** ([Yönetmelik](https://www.kvkk.gov.tr/Icerik/5441/KISISEL-VERILERIN-SILINMESI-YOK-EDILMESI-VEYA-ANONIM-HALE-GETIRILMESI-HAKKINDA-YONETMELIK), [Rehber](https://www.kvkk.gov.tr/Icerik/2038/kisisel-verilerin-silinmesi-yok-edilmesi-veya-anonim-hale-getirilmesi)).
- **Önerilen ayrım [değerlendirme, hukuki görüş değil]:**
  - **Kişisel katman:** Kullanıcının fişleri, satırları, hane profili. Rıza + aydınlatma. Ham fiş görseli çıkarım sonrası silinir ya da kart, telefon ve TCKN bölgeleri karartılarak saklanır.
  - **Fiyat gözlem katmanı:** `(ürün, zincir, il/ilçe ya da şube, birim fiyat, gün/hafta)`. Kullanıcı kimliği, saat ve fiş no **yok**. Yayımlanan her hücrede **en az k farklı katkıcı** şartı (ör. k=3–5). Tek kişilik hücre yayımlanmaz.
  - Mükerrer kontrolü için fiş anahtarının (1.1) yalnız tek yönlü hash'i tutulur.

### 4.2 Veri kalitesi, aykırı değer ve sahte veri
- **Emsal:** BLS, benzin fiyatında kitle kaynaklı ikincil veriyi (ayda ~6,1 milyon gözlem, geleneksel yöntemde ~4.000) 2017–2019 testlerinden sonra Temmuz 2021'de TÜFE'ye aldı. 3,5 yıllık karşılaştırmada ABD düzeyinde >%1 fark görülmemiş. Geleneksel toplama yedek olarak sürüyor ([BLS vaka çalışması](https://www.bls.gov/cpi/additional-resources/case-study-gasoline-price-data.htm)).
- **Nijerya gıda fiyatı çalışmaları:**
  - Kitle kaynaklı veri formal örnekleme dayanmadığı için doğrudan çıkarımda kullanılamıyor. Çözüm: **post-stratifikasyonla yeniden ağırlıklandırma** ([Arbia vd., arXiv 2003.12542](https://arxiv.org/abs/2003.12542)).
  - Ön işleme: standart ve **mekânsal aykırı değer** temizliği. Çoklu hesapla mükerrer gönderim, olası sahtecilik türü olarak ele alınıyor ([Scientific Data 2023](https://www.nature.com/articles/s41597-023-02211-1), arama özeti).
  - Kitle kaynaklı fiyatlar anketörle toplanan fiyatlarla r = 0,78–0,99 uyumlu çıkmış ([PLOS One 2025](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0320720)).
- **NutriScan'e özgü riskler ve azaltma [değerlendirme]:**
  - **Fiyat anlamı:** Raf fiyatı mı, ödenen fiyat mı? Satır indirimi ve sepet sonu sadakat indirimi (Money vb.) fiyatı değiştirir. Öneri: "satır indirimi düşülmüş birim fiyat" standart; sepet düzeyi indirim ayrı alan, endekse girmez.
  - **OCR hatası:** Ondalık virgül (`12,50` ↔ `1250`), 1/7 karışması (ReceiptBench'te raporlanan algı hatası). Satır tutarı = adet × birim fiyat kontrolü + ürün-zincir-hafta medyanından robust sapma (MAD) eşiği.
  - **Sahte fiş:** Görsel düzenleme ya da üretilmiş fiş. Aritmetik ve KDV tutarlılığı, cihaz sicil no ↔ mağaza tutarlılığı, aynı ürünün diğer kullanıcılar ve (izin varsa) marketfiyati ile karşılaştırması, kullanıcı itibarı ve oran sınırı.
  - **Mükerrer:** Fiş anahtarı hash'i (Qumpara da aynı fişi ikinci kez reddediyor).
  - **Örneklem yanlılığı:** Katkıcılar şehir ve zincir olarak dengesiz olur. Endeks yayımlanacaksa post-stratifikasyon; yayımlanmayacaksa kişisel kullanımla sınırla.

### 4.3 Kişisel enflasyon metodolojisi
- **TÜİK:** TÜFE **zincirlenmiş Laspeyres**, ağırlıklar yıllık güncelleniyor; 2026'dan itibaren 2025=100 bazı ([Kuveyt Türk Portföy özeti](https://www.kuveytturkportfoy.com.tr/blog/finans/tefe-ve-tufe-nedir-nasil-hesaplanir-ve-aralarindaki-farklar-nelerdir/), [TÜİK veri portalı](https://veriportali.tuik.gov.tr/Kategori/GetKategori?p=Enflasyon-ve-Fiyat-106)). TÜİK metodoloji PDF'i bana 403 verdi; formül ayrıntısını birincil kaynaktan doğrulayamadım.
- **Kişisel enflasyon hesaplayıcı emsali (ONS):** Kullanıcının kategori harcamaları × resmî kategori endeksleri. Kendi limiti: kategori içi fiyat farkını ve harcama değişimini yakalayamıyor ([ONS](https://www.ons.gov.uk/economy/inflationandpriceindices/articles/howisinflationaffectingyourhouseholdcosts/2022-03-23), [yöntem](https://www.ons.gov.uk/economy/inflationandpriceindices/methodologies/methodologytocalculatecpihconsistentinflationratesforukhouseholdgroups)). TCMB'nin genel enflasyon hesaplayıcısı da var ([TCMB](https://herkesicin.tcmb.gov.tr/wps/wcm/connect/ekonomi/hie/icerik/enflasyon+hesaplayici)).
- **Tarayıcı (scanner) verisi yöntemleri:** Birim değer, **GEKS-Törnqvist** gibi çok taraflı endeksler zincir kaymasını (chain drift) azaltıyor. Zincirlenmiş Törnqvist'ten kaçınılması öneriliyor. Ürün giriş-çıkışı (churn) düzeltilmezse yanlılık oluşuyor ([IMF bölüm 6](https://www.imf.org/~/media/Files/Data/CPI/companion-publication/chapter-6-chain-drift-problem-and-multilateral-indices.ashx?la=en), [Eurostat genel bakış](https://unece.org/sites/default/files/2021-05/Session_1_Eurostat_Paper.pdf), [ESCoE 2024](https://escoe-website.s3.amazonaws.com/wp-content/uploads/2024/07/30082424/ESCoE-DP-2024-08.pdf)).
- **Önerilen katmanlı tasarım [değerlendirme]:**

| Seviye | Ne | Veri ihtiyacı | MVP? |
|---|---|---|---|
| **A** | Kişisel ağırlık (fişten, TÜFE gıda alt gruplarına eşlenmiş harcama payı) × **TÜİK alt endeksleri** → "senin gıda enflasyonun" | Kullanıcı başı 1–2 aylık fiş; fiyat verisi gerekmez | ✅ Az veriyle sağlam. TÜİK alt endekslerine programatik erişimi kontrol etmedim |
| **B** | Kullanıcının baz dönem sepeti, güncel **topluluk fiyatlarıyla** yeniden fiyatlanır (Laspeyres, sabit miktar). Kategori içinde eşleşen ürünlerin fiyat oranları Jevons ile birleştirilir | Ürün-zincir-hafta başına yeterli gözlem; kütle ve boy bilgisi (küçülen paket) | 🟡 Pilot: yalnız sık ürünler, güven aralığıyla |
| **C** | GEKS-Törnqvist ile çok taraflı endeks | Yoğun, sürekli veri | ❌ Kapsam dışı |

- **Az veriyle güvenilirlik [değerlendirme]:**
  - Bir hane her ay aynı ürünü almaz; eşleşen fiyat oranı seyrek kalır. Seviye A her zaman gösterilir, B yalnız kapsama eşiği (ör. sepet harcamasının ≥ %50'si eşleşen fiyatlı) aşılınca gösterilir.
  - Kalite ve boy ayarı için birim fiyat (TL/kg) kullanılır; bu da SKU eşleşmesine bağlı (3.1).

---

## 5. marketfiyati.org.tr: katalog olarak değeri ve izin yolu
- **Ne:** Sanayi ve Teknoloji Bakanlığı ile TÜBİTAK BİLGEM'in platformu; A101, BİM, CarrefourSA, Hakmar, Migros, Tarım Kredi, ŞOK. ~50 bin ürün. Veri zincirlerden TCMB ile yürütülen proje kapsamında aktarılıyor; BİLGEM aykırı değer temizliği yapıyor ([TÜBİTAK](https://tubitak.gov.tr/tr/haber/zincir-market-fiyatlarina-aninda-erisimin-onu-acildi), [Webrazzi](https://webrazzi.com/2025/02/11/sanayi-ve-teknoloji-bakanligi-ndan-market-fiyatlarini-karsilastiran-platform-market-fiyati/)).
- **Veri alanları (resmî doküman değil, topluluk kodundan):** Ürün `id, title, brand, imageUrl, categories[]`; şube bazında `depotName, marketAdi, price, latitude, longitude, indexTime`. Uç noktalar `/api/v2/search`, `/searchByIdentity` (`identityType: id | barcode`), `/searchByCategories` ([topluluk MCP sunucusu](https://github.com/EnesCinr/market-fiyatlari-mcp-server)). Sitenin kendi JS paketinde `/api/v2/nearest` ve `/api/v2/searchAlternative` çağrıları var (kendim baktım). Frontend `identityType: "id"` kullanıyor; **barkodla sorgunun çalıştığını doğrulamadım**.
- **Bilinen zayıflık:** Bir kullanıcı kategorilemenin yetersiz olduğunu yazmış (yağlı ve yağsız süt aynı seviyede, ilgisiz ürünler aynı kategoride) ([X gönderisi](https://x.com/uygunbodur/status/1889568880693006698), anekdot). Bir topluluk deposunda API'nin bot koruması olduğu not edilmiş ([mekruhsah/market-fiyat](https://github.com/mekruhsah/market-fiyat)).
- **Değeri [değerlendirme]:**
  1. Fiş satırlarını eşleyeceğimiz **en iyi hedef katalog**. Tam da bu 7 zincirin ürün adı, marka ve kategorisi; OFF TR'nin (~22 bin, çoğu eksik) kapsamadığı çeşitliliği kapsar.
  2. Topluluk fiyatları için **referans ve sahte veri kontrolü**.
  3. `searchAlternative` tam "akıllı takas" semantiği taşıyor.
- **Hukuk:** Kullanım Koşulları, yazılı izin olmadan kopyalama, işleme ve herhangi bir amaçla kullanımı yasaklıyor (01, §2; [Kullanım Koşulları](https://marketfiyati.org.tr/kullanim-kosullari)). **İzinsiz scraping önerilmez** (01-mevzuat-risk §6.2 ile aynı sonuç).
- **İzin yolu:** Sitede yayımlanan iletişim adresleri **marketfiyati.iletisim@tubitak.gov.tr** ve **mavp@sanayi.gov.tr** (site JS paketinden). Resmî bir "veri/API başvuru" formu **bulunamadı**. Öneri [değerlendirme]:
  - danışman imzalı, üniversite antetli başvuru;
  - ticari olmayan akademik kullanım, istenen alanlar (yalnız katalog: ad, marka, kategori, varsa barkod; fiyat opsiyonel), güncelleme sıklığı;
  - yeniden dağıtım yok, atıf var;
  - talep: toplu dışa aktarım ya da anahtarlı API.
  - Cevap gelmezse B planı: OFF + kendi topluluk kataloğumuz.
- **Sonuç (28 Eyl 2026, Market Fiyatı ekibinin e-postası):** Talep reddedildi. TÜBİTAK BİLGEM projenin teknik yürütücüsü; üçüncü taraflara, bağımsız geliştiricilere ya da akademik çalışmalara ham veri, CSV ya da API vermeye yetkili değil. Paylaşım yalnız Sanayi ve Teknoloji Bakanlığı ile Ticaret Bakanlığı'nın resmî sözleşme ve kurumlar arası protokolleriyle. Yukarıdaki üç değer (eşleme hedefi katalog, sahte fiyat referansı, `searchAlternative`) kaybedildi; eşleme hedefi kendi doğrulanmış kataloğumuz (Migros → A101) + OFF adayları. Yazılı red sonrası kazıma kesin kapsam dışı (ADR-002).

---

## 6. Sonuç

### 6.1 Alt başlık hükümleri
| # | Alt başlık | Hüküm |
|---|---|---|
| 1 | Fiş yapısı / GİB / zincir dijital kanalları | 🟡. Kâğıt fiş yapılandırılmamış; GİB'den doğrulama yok (🔴); online fatura temiz (🟢) |
| 2 | Satır okuma + satır→ürün eşleştirme | 🟡 okuma / 🔴→🟡 eşleştirme (topluluk sözlüğüne bağlı) |
| 3 | Kategori fallback + diyet kalitesi geçerliliği | 🟡. Açık kaynaklar var, TürKomp izin ister; kütle ve kapsama limitleri |
| 4 | Topluluk fiyatı (KVKK, kalite) + kişisel enflasyon | 🟡 fiyat verisi / 🟢 Seviye A enflasyon |
| 5 | marketfiyati.org.tr | 🔴 izinsiz / 🟢 izinle |

### 6.2 En büyük 5 risk ve azaltma
| # | Risk | Nerede kırılır | Azaltma |
|---|---|---|---|
| 1 | **Kütle/miktar belirsizliği** | Paketli satırda gram yok. SKU eşleşmezse kişi başı şeker/tuz tahmini katlanan hatayla çıkar | Oran metrikleri (1000 kcal başına, harcama payı) birincil; mutlak gram ikincil ve aralıklı. Kapsama göstergesi. Ad içindeki gramaj çıkarımı. Varsayılan paket boyu tablosu |
| 2 | **Satır okuma halüsinasyonu + eşleştirme soğuk başlangıcı** | VLM'ler toplamı tutturmak için satır uyduruyor (ReceiptBench). Ürün sözlüğü boşken çoğu satır onay istiyor ve kullanıcı yorulur | Aritmetik ve KDV kontrolü kodda. LLM yalnız aday listesinden seçer. Zincir başına topluluk sözlüğü. Ekip ilk 2–3 haftada kendi fişleriyle sözlüğü tohumlar. Online fatura kanalı önceliklendirilir |
| 3 | **Kapsama kör noktaları** | Semt pazarı ÖKC'den muaf, dışarıda yeme, fırın/bakkal, yüklenmeyen fişler. Sepet karnesi sistematik yanlı olur | "Sepet karnesi" dili (diyet değil). Aylık tek soruluk pazar/dışarıda yeme düzeltmesi. Kapsama yüzdesinin gösterilmesi |
| 4 | **Topluluk fiyat kalitesi ve sahte veri** | Ondalık/OCR hatası, indirim semantiği, sahte fiş, az katkıcı. Endeks gürültüsü, yanlış "ucuz alternatif" | Birim fiyat standardı. Robust aykırı değer (MAD), mükerrer hash, itibar, k-eşiği. Seviye A enflasyonu varsayılan yap, B'yi kapsama eşiğine bağla. İzin varsa marketfiyati referansı |
| 5 | **Hukuk ve lisans** | Fiş görselinde kişisel veri; alışverişten sağlık çıkarımı; yurt dışı VLM'e görsel gönderimi (01-mevzuat); TürKomp ve marketfiyati izinleri | Görsel redaksiyonu + çıkarım sonrası silme. Fiyat katmanını kimliksizleştirme. VLM'e yalnız fiş görseli (profil yok). TürKomp ve marketfiyati'ye danışman imzalı yazılı başvuru; olmazsa Ciqual/USDA + OFF |

### 6.3 MVP'de fişten ne kadar otomatik? (tümü **[VARSAYIM]**, ölçülmedi)
Koşul: Zincir market fişi, düzgün ışıkta çekilmiş, dilimlenmiş foto; online faturalar ayrı kanal.

| Adım | İlk gün (sözlük boş) | ~3 ay topluluk sözlüğüyle | Not |
|---|---|---|---|
| Fiş başlığı: tarih, zincir, toplam | %95+ | %95+ | Toplam kontrolü bunu doğrular |
| Satır metninin doğru okunması | %85–95 | aynı | Aritmetik tutmayan fişler (%10–20) kullanıcıya düşer |
| Gıda satırının **kategoriye** otomatik atanması | %75–90 | %85–95 | Sepet karnesinin çoğu için yeterli |
| Gıda satırının **SKU'ya** güvenle eşlenmesi | %25–50 (katalog: OFF TR; marketfiyati izni varsa üst uç) | zincir başına %60–80 | İsviçre: en sık ~6 bin ürün alımların ~%70'i |
| Online sipariş faturası (PDF/XML) satırları | %95+ okuma, SKU %50–70 | %80+ | Tam ürün adı varsayımı test edilmeli |

**Mesaj [değerlendirme]:** MVP'de gerçekçi söz şu: *"Satırların çoğu otomatik kategorilenir. Ürün düzeyi eşleşme başta yaklaşık yarıda kalır, kalanı tek dokunuşla onaylanır; onaylar herkes için sözlüğü büyütür."* Bu rakamlar 2 haftalık bir spike'ta ölçülmeden proposal'a **yazılmamalı**. Önerilen ölçüm:
- 3 zincirden 100–150 fiş + 20 online fatura,
- elle etiketlenmiş altın standart,
- metrikler: satır F1, kategori doğruluğu, SKU top-1, fiş başına onay süresi.

### 6.4 Levent'e açık sorular
1. Ekip kendi market fişlerini (maskelenmiş) eval seti için toplamaya razı mı? Hedef: 2 haftada 100+ fiş.
2. marketfiyati.org.tr ve TürKomp'a danışman imzalı resmî başvuru yapılabilir mi? Proposal tarihi (18 Ekim) öncesi gönderilirse cevap süresi belirsiz.
3. "Akıllı takas" fiyatı neye dayanacak: topluluk fiyatı mı, marketfiyati izni mi, yoksa yalnız kullanıcının kendi geçmiş fiyatları mı?
4. Kişisel enflasyon MVP'de Seviye A (TÜİK alt endeksleri) ile yetinebilir mi?
5. Online sipariş faturası kanalı (PDF/XML yükleme ya da e-posta yönlendirme) MVP kapsamına girsin mi? Mağaza fişinden daha temiz veri verir ama kullanıcı tabanı farklı olabilir.

---

## Ek: Yöntem notları (2026-09-24)
- **GİB taslak kılavuzu** PDF'i indirilip `pdftotext` ile tarandı: "karekod", "QR", "e-posta", "doğrula" geçişleri ve Bölüm 2–3 okundu. **VUK GT 593** tam metni okundu. **ÖKC muafiyet listesi** PDF'inde "pazar" arandı. ynokc.gib.gov.tr son duyuruları (11136–11162) başlık düzeyinde kontrol edildi.
- **A101 fatura portalı** HTML'i incelendi: alanlar `fatNo` (Belge No/ETTN/Fatura No), fatura tarihi, `amount`, captcha; butonlar "Xml İndir" ve "Pdf İndir". Sorgu yapılmadı.
- **marketfiyati.org.tr:** Yalnız ön yüz JS paketinde iletişim e-postaları ve uç nokta adları arandı. **API'ye veri isteği atılmadı** (Kullanım Koşulları gereği). Alan adları üçüncü taraf açık kaynak koddan alındı.
- **TürKomp** kullanım koşulları ve 2026 ücret tablosu doğrudan siteden okundu (çerezli istekle; çerezsiz istekte kısa sayfa dönüyor).
- **OFF kategori ortalaması:** Bir ürün sayfasında "Compared to: <kategori>" bloğu kontrol edildi.
- **Erişilemeyenler:** PwC bülteni, A101 SSS, CarrefourSA fatura bulucu (403), PMC makaleleri (captcha; özetler Europe PMC API'den alındı), TÜİK metodoloji PDF'i (403), Springer tam metinleri (giriş duvarı; Türkçe OCR makalesinin ön baskısı okundu). Bu kaynaklardan gelen bilgiler metinde "arama özeti" diye işaretlendi.
- Türkçe fiş veri seti araması: Hugging Face API (`search=turkish receipt`, `receipt` içinde tr/turk/fis süzmesi) ve GitHub depo araması ("turkish receipt", "fiş ocr", "market fişi").
