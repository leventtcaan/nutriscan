---
title: 05 — v4 MENÜ ve MUTFAK — fizibilite ve derinlik (tarif verisi, LLM tarif güvenliği, menü optimizasyonu, kiler, öneri sistemi)
updated: 2026-09-24
durum: HAM ARAŞTIRMA — Levent onayı yok
dayanak: 04-vizyon-v4-tohum.md · 02-v2-yontem-literatur.md §7 (Akıllı Takas) · 01-danisman-bitirme.md §4 (P4, P7)
ek: 05-ek-menu_bench.py (sentetik benchmark) · 05-ek-menu_bench_sonuc.txt · 05-ek-menu_bench_parca.txt
---
# 05 — v4 MENÜ ve MUTFAK adımları: fizibilite ve derinlik

> **Ham araştırma — Levent'le netleştirilmedi, 2026-09-24**
> **Yöntem:** Web taraması yapıldı. Oturumun WebSearch kotası (200/200) taramanın ortasında doldu. Kalan kısım doğrudan sayfa çekerek ve HF, Kaggle, Crossref, arXiv, PubMed API'leriyle tamamlandı. Buna ek olarak kendi sentetik benchmark'ımızı koştuk (`05-ek-menu_bench.py`). Yük taşıyan makale künyelerinden ~35'i Crossref veya arXiv'de ayrıca doğrulandı.
> **İşaretler:** **DOĞRULANMADI** = birincil kaynaktan teyit edilemedi · **[yorum]** = bizim çıkarımımız · **[sentetik]** = kendi ürettiğimiz deney verisi, gerçek veri değil · **[tahmin]** = ölçülmemiş kaba hesap.
> **Tekrar edilmedi, üstüne kuruldu:** Akıllı Takas MILP'i (02 §7), P4/P7 ilk taslakları (01 §4), TürKomp ücret tablosu (02-v2-fis-veri §3.2), OFF ve marketfiyati erişimi (01-veri-fizibilite), UNEP 2021'deki 93 kg rakamı (02-v2-kirmizi-takim).

---

## 0. Özet

| Bileşen | Işık | Tek cümle |
|---|---|---|
| Türkçe tarif verisi | 🟡 | Açık lisanslı ve temiz bir set yok. HF'deki büyük setler Nefis Yemek Tarifleri ve yemek.com'dan kazınmış, bu sitelerin koşulları yazılı izin istiyor. **Ekibin yazdığı ~200 ev yemeği + LLM ile yapılandırma + insan onayı** yapılabilir. |
| Tariften besin değeri | 🟢 | FDC (CC0) + USDA retention/yield faktörleri + EuroFIR prosedürü ile deterministik hesap. LLM sayı üretmez. Ev ölçüleri TÜBER 2022'den. |
| LLM ile tarif uyarlama | 🟡 | Tek başına güvensiz. Doğrulama katmanı olan en iyi sistemde bile %1,5 ihlal kalıyor. Bir çalışmada RAG ikame tablosunun kendisi tehlikeli öneriler içeriyor. **Kürate ikame tablosu + alerjen ontolojisi + "bilinmiyor = yasak" kural motoru** ile yeşile çekilebilir. |
| Haftalık menü optimizasyonu | 🟢 (derinlik: yüksek) | Menü + paket tamsayılığı + kiler/israf + ≤2 market **birleşik** kurulunca problem gerçekten zorlaşıyor; çekirdek sepet (02 §7.8) ms'de çözülüyordu. [sentetik] 7 akşam × 100 tarifte 3 örneğin 1'i 60 s'de kanıtlanamadı. 14 öğün ve üstünde hiçbiri kanıtlanamadı. LP boşluğu %25–53. "Önce menü, sonra liste" yaklaşımı alım TL'sinde %2–32 daha kötü. **Exact vs NSGA-II için dürüst bir sahne** (§3.3). |
| Kiler takibi | 🟡 | Barkod 🟢, e-Arşiv ve fiş 🟡. **Buzdolabı fotoğrafı envanter kaynağı olarak 🔴**, onay katmanı olarak 🟡. Raf ömrü FoodKeeper'dan (CC0), bitmek-üzere tahmini Gamma–Poisson ile 🟢. Türkiye israf rakamı (UNEP 2024, 102 kg) ölçüme değil ekstrapolasyona dayanıyor. |
| Öneri sistemi | 🟡 | Pilot hacminde (20–40 hane) işbirlikçi filtreleme zayıf. Yol: **filtrele → sırala** + içerik + kohort popülerliği (k≥5) + Thompson örneklemesi. Çıktısı menü modelinin parametresi $\pi$ olur. "Senin gibi haneler" dar kohortlarda pilotta gösterilemeyebilir. |

---

## 1. Türkçe tarif verisi ve tariften besin değeri

### 1.1 Açık veri setleri: bol ama lisans zinciri kirli
Lisanslar dataset card'larından ve HF/Kaggle API'lerinden okundu.

| Set | Tarif | Alanlar | Kaynak site | Kartta yazan lisans |
|---|---|---|---|---|
| [mmkocak/turkish-recipes-175K](https://huggingface.co/datasets/mmkocak/turkish-recipes-175K) | 174.975 | Malzeme satırı (miktar metnin içinde), adımlar, porsiyon, süre | "Halka açık Türkçe kaynaklar". URL'ler kasıtlı silinmiş | Apache-2.0 |
| [Ethosoft/Turkish-Recipe-Corpus](https://huggingface.co/datasets/Ethosoft/Turkish-Recipe-Corpus) | 74.768 | Malzeme, adımlar, kategori. Porsiyon ve süre yok | Belirtilmemiş | CC BY 4.0 |
| [AnIl-c/yemek_tarifleri](https://huggingface.co/datasets/AnIl-c/yemek_tarifleri) | 101.993 | Malzeme, yapılış, puan, yorum sayısı, URL | **nefisyemektarifleri.com** (kartta yazıyor) | CC BY-NC 4.0 |
| [habanoz/yemek_tarif_24k_raw](https://huggingface.co/datasets/habanoz/yemek_tarif_24k_raw) | 23.905 | Ham HTML | **yemek.com** (URL'lerden) | Yok |
| [104bit/turkish-recipe-dataset](https://huggingface.co/datasets/104bit/turkish-recipe-dataset) | 3.320 | **Yapılandırılmış** `{isim, miktar, birim}`, süre, zorluk. Porsiyon çoğunlukla boş | ye-mek.net kaynaklı setten Llama ile yapılandırılmış | MIT |
| Kaggle [ezgicinkilic/…platform-dataset](https://www.kaggle.com/datasets/ezgicinkilic/turkish-recipe-sharing-platform-dataset) | 800.140 satır | Ad, URL, kategori. Malzeme yok | nefisyemektarifleri.com | CC BY-NC 4.0 |

- **Hakemli bir Türkçe tarif veri seti bulunamadı.** Epicure ([arXiv 2605.22391](https://arxiv.org/abs/2605.22391)) 4,14 milyon tarifi 7'den fazla dilde topluyor ve Türkçe de içinde. Ama Türkçe kısmın kaynağı, sayısı ve veri lisansı **DOĞRULANMADI**.
- **Büyük İngilizce setler ticari kullanıma kapalı:**
  - RecipeNLG: ticari olmayan araştırma ([HF](https://huggingface.co/datasets/mbien/recipe_nlg)).
  - Recipe1M: araştırma amaçlı, hesap açıp koşul kabulü gerekiyor.
  - Food.com: Kaggle'da "© Original Authors" ([Kaggle](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)).
- **[yorum]** Bir kullanıcı veriyi HF'ye yüklerken MIT, Apache ya da CC seçebilir. Ama sahip olmadığı bir hakkı başkasına devredemez. Kaynağı nefisyemektarifleri veya yemek.com olan setlerde çelişki kesin. Kaynağı gizlenmiş setlerde ise (mmkocak, Ethosoft) kaynak doğrulanamıyor.

### 1.2 Sitelerin koşulları ve hukuk
- **nefisyemektarifleri.com** ([koşullar](https://www.nefisyemektarifleri.com/gizlilik-politikasi/)):
  - İçerik yazılı izin alınmadan kopyalanamaz ve çoğaltılamaz.
  - [robots.txt](https://www.nefisyemektarifleri.com/robots.txt) GPTBot, ClaudeBot, CCBot ve **Scrapy** kullanıcı ajanını engelliyor. Ayrıca `Content-Signal: ai-train=no, ai-input=no` satırı var.
- **yemek.com** ([Kullanım Koşulları](https://yemek.com/kullanim-kosullari/)):
  - Yazılı izin olmadan kişisel ya da ticari kullanım yasak.
  - robots.txt serbest, ama bu koşulları ortadan kaldırmaz.
- **FSEK:**
  - Eser tanımı "sahibinin hususiyetini taşıma" şartı arıyor (m.1/B, [5846 PDF](https://www.mevzuat.gov.tr/mevzuatmetin/1.3.5846.pdf)).
  - Bir hukuk bloğuna göre tarifin kendisi (malzeme ve yöntem) büyük olasılıkla eser sayılmaz, ama anlatım metni ve fotoğraf korunur ([Sezer & Utkaner](https://sezerutkaner.com/blog/yemek-tariflerinin-hukuki-korumasi/)). Bu bir blog görüşü. Yargıtay kararı **bulunamadı**.
- **Asıl risk, veri tabanı yapımcısı hakkı:**
  - FSEK **Ek Madde 8**, esaslı yatırım yapan veri tabanı yapımcısına bir hak tanıyor. İçeriğin önemli bir kısmının aktarılması, yapımcının iznine bağlı. Koruma 15 yıl.
  - Toplu kazıma tam bu maddeye giriyor.
  - Türk hukukunda metin ve veri madenciliği istisnası yok ([Sertel 2024, SDÜ HFD](https://dergipark.org.tr/tr/download/article-file/3957512)).
- **Sonuç:**
  - 🔴 Kazıma.
  - 🟡 HF setleri yalnız ekip içinde geliştirme için kullanılabilir: parser ve NER testi, malzeme sözlüğü için frekans çıkarma. Kullanıcıya içerik olarak gösterilmez.

### 1.3 Önerilen yol: ekibin küratörlüğünde ~200 ev yemeği
1. **Liste.** TÜBER'deki gıda grubu dengesine göre ~200 Türk ev yemeği seçilir: ana yemek, sebze, bakliyat, çorba, pilav/makarna, kahvaltılık. Tarif metnini ekip kendi cümleleriyle yazar. Aile tarifleri de olur. Böylece telif ve veri tabanı riski en düşük kalır.
2. **LLM ile yapılandırma.** Serbest metin şu şemaya çevrilir: `{malzeme_id, miktar, birim, opsiyonel, ikame_slotu}`, adımlar, süre, porsiyon. 104bit setinin şeması iyi bir başlangıç. Ama o sette porsiyon alanının çoğu boş kalmış. Bu yüzden porsiyon ve birim **insan tarafından** doldurulur.
3. **Kanonik malzeme sözlüğü** (~300–400 kalem). Her kalemde şunlar tutulur: FDC/Ciqual ID, yoğunluk (g/mL), yenmeyen kısım oranı, alerjen etiketi, raf ömrü kategorisi (§4), fiyat kataloğundaki ürün eşlemesi (v3 katalog).
4. **İnsan onayı.** Her tarifi 2 kişi kontrol eder. Alerjen alanları çift onaydan geçer.
5. **Varyasyon.** "Glutensiz makarnayla", "fındıksız" gibi varyasyonlar serbest üretilmez. Yalnız onaylı ikame tablosundan alınır, kural motorundan geçer (§2.5), insan onaylar, sonra kataloğa girer. **Canlıda serbest tarif üretimi yok.**
- **[tahmin] Efor:** Tarif başına ~10 dk yazım + ~5 dk onay. 200 tarif ≈ 50 saat, 3 kişiye bölünce kişi başı ~17 saat. Malzeme sözlüğü ve FDC eşlemesi ayrıca ~15–20 saat.
- **Kalite ve güvenlik riskleri:**
  - LLM yapılandırırken malzeme atlayabilir. Bileşik malzeme ayrıştırmada F1 Llama-3-70B'de 0,894, GPT-4o'da 0,842. Yağ, baharat ve tatlandırıcı sık atlanıyor; bu gizli alerjen demek (Kopitar 2025, [doi:10.3390/nu17091492](https://doi.org/10.3390/nu17091492)).
  - Birim belirsizliği (bkz. 1.4).
  - Porsiyon uydurma.
  - Önlem: şema doğrulayıcı + "tarifteki her malzeme sözlükte var" kontrolü + insan onayı.

### 1.4 Tariften besin değeri: deterministik hesap
**Porsiyon başına besin** (EuroFIR harmonizasyonu; Reinivuo, Bell, Ovaskainen 2009, JFCA 22:410, [doi:10.1016/j.jfca.2009.04.003](https://doi.org/10.1016/j.jfca.2009.04.003)):
$$
N_{rk}=\frac{1}{s_r}\sum_{i\in r} m_{ri}\,(1-\theta_i)\,\frac{c_{ik}}{100}\,RF_{ik},\qquad
N^{100g}_{rk}=\frac{s_r\,N_{rk}}{Y_r\sum_i m_{ri}(1-\theta_i)}\cdot 100
$$
- $m_{ri}$: çiğ gram.
- $\theta_i$: yenmeyen kısım oranı.
- $c_{ik}$: 100 g'daki besin miktarı.
- $RF_{ik}$: retention faktörü.
- $Y_r$: pişmiş/çiğ ağırlık verimi.
- $s_r$: porsiyon sayısı.

**Kaynaklar:**
- *USDA Table of Nutrient Retention Factors, Release 6* (2007) ([PDF](https://www.ars.usda.gov/ARSUserFiles/80400525/Data/retn/retn06.pdf)). ~290 gıda için 16 vitamin, 8 mineral ve alkol faktörü var. Makrobesin faktörü yok; enerji ve yağ değişimi yield ile hesaplanır.
- *USDA Agriculture Handbook 102* (Matthews & Garrison 1975), yield tabloları ([PDF](https://www.ars.usda.gov/ARSUserFiles/80400535/Data/Classics/ah102.pdf)).
- EuroFIR kılavuzu (Machackova ve ark. 2018, Food Chem 238:35, [PubMed 28867099](https://pubmed.ncbi.nlm.nih.gov/28867099/)).

**Hata payı:**
- 12 diyet uygulamasının tarif fonksiyonu referans hesapla karşılaştırılmış. Referans alımın %5'inden büyük farklar mikrobesinlerde %49, enerji ve makrolarda %20 oranında görülmüş. Farkın ana kaynağı kullanılan besin veri tabanı. Retention faktörleri B6, B12 ve folatı %45'ten fazla düşürüyor (Zhang ve ark. 2019, Nutrients, [doi:10.3390/nu11010200](https://doi.org/10.3390/nu11010200)).
- **[yorum]** Bu yüzden ekranda makrolar ve Na gösterilir. Mikrobesinler ya gösterilmez ya da "tahmini" diye etiketlenir.

**Malzeme → veri tabanı eşleme:**
- Önce embedding ile ilk K aday çekilip sonra LLM'e seçtirildiğinde doğruluk %90,7 (ASA24→FooDB) ve %65,4 (NHANES→DFG2). LLM tek başına büyük veri tabanında daha kötü (Lemay ve ark. 2026, J Nutr, [doi:10.1016/j.tjnut.2026.101678](https://doi.org/10.1016/j.tjnut.2026.101678)).
- **[yorum]** Bu, v3'teki fiş eşleştirmesiyle **aynı desen**: aday çek → sırala → emin değilsen çekimser kal → insan onaylar (03-tez-v3 K5). Tek altyapı iki işi görür.

**LLM'e besin sayısı ürettirilmez:** Peru yemeklerinde Gemma-3 27B'nin kalori tahmininde uyum %45, ortalama mutlak hata 108 kcal (Carrillo-Larco ve ark. 2026, J Nutr, [doi:10.1016/j.tjnut.2026.101786](https://doi.org/10.1016/j.tjnut.2026.101786)).

**Veri tabanı seçimi:**
- FDC: CC0, API saatte 1.000 istek ([API guide](https://fdc.nal.usda.gov/api-guide/)).
- Ciqual: Etalab açık lisans.
- TürKomp: ücretli (02-v2-fis-veri §3.2).
- **[yorum]** Türk jeneriklerinin (bulgur, tarhana, sucuk, pekmez, tahin helva) FDC/Ciqual karşılığı zayıf. Bu ~20–40 kalem için ya etiket/OFF kategori medyanı kullanılır ya da TürKomp'a izin başvurusu yapılır.

**Ev ölçüleri** (TÜBER 2022, [PDF](https://hsgm.saglik.gov.tr/depo/birimler/saglikli-beslenme-ve-hareketli-hayat-db/Dokumanlar/Rehberler/Turkiye_Beslenme_Rehber_TUBER_2022_min.pdf)):
- Standart ölçü aracı "kupa" = 240 mL.
- Piyasadaki kaplar çok değişken: su bardağı 200–560 mL, çay bardağı 85–165 mL. Yemek kaşığı zamanla 15 mL'den 10–12 mL'ye inmiş.
- Metinde "1 çay bardağı (100 mL)" ve "1 tatlı kaşığı (5 g) sıvı yağ" gibi kullanımlar da geçiyor.
- **Sonuç:** Kendi ölçü standardımızı tanımlarız ve her malzeme için yoğunluk tutarız.
- Doğrulama ve atıf için: Rakıcıoğlu, Tek, Ayaz, Pekcan, *Yemek ve Besin Fotoğraf Kataloğu: Ölçü ve Miktarlar*, 9. bs., Ankara Nobel, 2025 ([yayınevi](https://www.ankaranobel.com/yemek-ve-besin-fotograf-katalogu-olcu-ve-miktarlar)). Ücretli bir kitap; tabloları toptan kopyalanmaz.
- Brüt/net miktarlar için: Merdol, *Standart Yemek Tarifeleri*, 7. bs., Hatiboğlu, 2018.

### 1.5 Porsiyonlama (hane üyelerine ölçekleme)
- Üye enerji gereksinimi TÜBER Ek 1.1.x tablolarından alınır: yaş, cinsiyet ve fiziksel aktivite düzeyine (PAL) göre. Örnek: 30–39 yaş erkek, PAL 1,6 → 2.452 kcal/gün.
- Hane düzeyinde toplam, "yetişkin erkek eşdeğeri" (AME) yaklaşımıyla ifade edilir. Yanlış atfetme enerji yeterliliğini −%29 ile +%2 arasında saptırabiliyor (Weisell & Dop 2012, [PubMed 23193766](https://pubmed.ncbi.nlm.nih.gov/23193766/)).
- **Menü modeline giriş:** Öğün $t$'de yiyen üyeler $E_t$ ise porsiyon ölçeği $\sigma_t=\sum_{m\in E_t}E_m/E_{\text{ref}}$ olur. Tarif $s_r$ porsiyonluk yazılmışsa malzeme ihtiyacı $\sigma_t\,m_{ri}/s_r$ olur. Üyeye düşen besin payı 02 §6'daki $\omega$ ile aynı mantıkla hesaplanır.

---

## 2. LLM ile tarif üretimi ve uyarlama güvenliği

### 2.1 Kanıt: LLM tek başına güvenlik kararı veremez
- **Pak'nSave "Savey Meal-bot"** ([The Guardian, 10.08.2023](https://www.theguardian.com/world/2023/aug/10/pak-n-save-savey-meal-bot-ai-app-malfunction-recipes)): Kullanıcılar ev kimyasallarını malzeme olarak girdi. Bot, klor gazı üreten bir "aromatic water mix" tarifini içecek diye önerdi. Ders: **girdi beyaz listesi** şart.
- **Niszczota & Rybicka 2023** (Nutrition 112:112076, [doi](https://doi.org/10.1016/j.nut.2023.112076)): Alerjisi olan hipotetik bireyler için 56 diyet üretildi. Sonuç: diyetler "genel olarak doğru ama zararlı olabilir". "4 diyette kuruyemiş sızdı" bilgisi yalnız basındaki alıntıda var, **DOĞRULANMADI**.
- **Mathes ve ark. 2025** (JACI In Practice, [doi](https://doi.org/10.1016/j.jaip.2025.03.030)): 120 alerjoloji sorusunda ortalama 4,1/5. 6 kritik hata var; biri pediatrik gıda alerjisiyle ilgili ve potansiyel olarak hayati.
- **Vij ve ark. 2025** ([arXiv 2502.02028](https://arxiv.org/abs/2502.02028)): Küçük modellerle tarif üretimi ve alerjen ikamesi. Ajan raporuna göre RAG için kurdukları **ikame tablosunun kendisi** bağlama göre tehlikeli satırlar içeriyor. Satır düzeyinde yalnız ajan okudu:
  - yer fıstığı → badem/kaju ezmesi
  - buğday → yulaf unu
  - süt → kaju kreması, tahin
  - susam → ayçekirdeği
  - **[yorum]** Bu tablo test edilmesi gereken bir girdi. CI'da **negatif test** olarak kullanılabilir.
- **Correia & Feng 2026** (J Food Prot, [doi](https://doi.org/10.1016/j.jfp.2026.100852)): 20 gıda güvenliği pratiği 4 sohbet botuna soruldu. Uzmanlarla uyum sınırlı, tekrarlar arasında tutarsız. Prompt tasarımı tek başına yetmiyor.
- **Pişirme güvenliği:** İnsan yazımı 474 kanatlı tarifinin yalnız ~%33,5'i iç sıcaklık veriyor (Chambers 2018, [doi:10.3390/foods7080126](https://doi.org/10.3390/foods7080126)). **[yorum]** LLM bu uyarıyı kendiliğinden eklemeyebilir. Uyarı şablondan eklenmeli.
- FoodGuardBench (01-ai-feature-havuzu) de LLM'lerin gıda güvenliği hizalamasının zayıf olduğunu ve jailbreak'e açık olduğunu gösteriyor.

### 2.2 İkame araştırmaları güvenliği ölçmüyor
- **GISMo / Recipe1MSubs** (Fatemi ve ark. 2023, [arXiv 2302.07960](https://arxiv.org/abs/2302.07960)): Hit@1 %20,56, MRR 31,51. "Doğru" ikame, kullanıcı yorumlarında geçen ikame demek; **güvenli** demek değil.
- **Senath ve ark. 2025** ([arXiv 2412.04922](https://arxiv.org/abs/2412.04922)): Zero-shot LLM'lerde Hit@1 %5,96–14,20. İnce ayarlı Mistral-7B'de %22,04.
- **SHARE** (EMNLP 2022, [arXiv 2105.08185](https://arxiv.org/abs/2105.08185)): Önce ikame, sonra adımları yeniden yazma; iki ayrı aşama. **[yorum]** Güvenlik kapısı ile mutfak kalitesi ayrı katmanlar olmalı.
- **Derleme** (Kim, Venkataramanan, Sheth 2025, [arXiv 2501.01958](https://arxiv.org/abs/2501.01958)): İkame verileri uzmanlarca doğrulanmamış, standart benchmark yok, tıbbi kılavuzlara nadiren atıf var.

### 2.3 Çapraz reaksiyon: kural motorunun bilmesi gerekenler (tıbbi tavsiye değil, kural mantığı)
**Mevzuat:**
- TGK Etiketleme Yönetmeliği (RG 26.01.2017, 29960 mük., [metin](https://www.resmigazete.gov.tr/eskiler/2017/01/20170126M1-6.htm)) Ek-1 ile AB 1169/2011 Ek II aynı 14 alerjeni sayıyor ([AB metni](https://www.legislation.gov.uk/eur/2011/1169/annex/II/adopted)). Bunlar arasında: gluten tahılları (yulaf dahil), ağaç yemişleri (fındık dahil), susam, acı bakla (lupin).
- "Glutensiz" etiketi en fazla 20 mg/kg gluten demek (AB 828/2014).
- FDA: hindistan cevizi artık majör alerjen sayılan ağaç yemişi değil (taslak 2022, final Ocak 2025, [FDA](https://www.fda.gov/food/food-allergensgluten-free-guidance-documents-regulatory-information/frequently-asked-questions-food-allergen-labeling-guidance-industry)).

**Tehlikeli ikame örnekleri:**
- **Lupin ↔ yer fıstığı.**
  - Yer fıstığına duyarlı 39 yetişkinin %82'si lupine de duyarlı, %35'inde klinik olarak anlamlı. En düşük tetikleyici doz 0,5 mg (Peeters 2009, [doi](https://doi.org/10.1111/j.1398-9995.2008.01818.x)).
  - Yer fıstığı alerjililerin %44'ünde yükleme testiyle lupin alerjisi doğrulanmış (Aguilera-Insunza 2023, [doi](https://doi.org/10.1016/j.anai.2022.09.036)).
  - **Tuzak:** Glutensiz un karışımları lupin içerebilir. Aynı hanede çölyaklı ve yer fıstığı alerjili üye varsa bu ikame tehlikeli.
- **Ağaç yemişleri arası.**
  - En az bir kuruyemiş veya susam alerjisi olan 122 çocukta, yükleme testiyle doğrulanmış eşlik eden alerji %60,7. Güçlü kümeler: kaju–Antep fıstığı, ceviz–pekan(–fındık–makadamya) (Brough 2020, [doi](https://doi.org/10.1016/j.jaci.2019.09.036)).
  - EAACI 2024 kılavuzuna göre zaten tolere edilen ilişkili gıdalar otomatik olarak yasaklanmamalı (Santos ve ark., Allergy, [doi:10.1111/all.16345](https://doi.org/10.1111/all.16345)). Bu yüzden kural motorunda bu kenar **"yasak" değil, "onay gerekir"** olur.
- **Ayçekirdeği.**
  - "Alerjensiz yer fıstığı alternatifi" diye popülerleşiyor. 235 hastada reaksiyonların ~1/4'ü anafilaksi, tanı olasılığı yıllık OR 1,21 ile artıyor (Treffeisen 2024, [doi](https://doi.org/10.1016/j.jaip.2024.07.029)).
  - Ayçekirdeğinden kaçınması önerilen 230 hastanın 229'unda başka bir gıda alerjisi var, çoğunlukla ağaç yemişi, susam veya yer fıstığı. Buna karşılık 72 yükleme testinin %83'ü negatif (Shah 2026, [doi](https://doi.org/10.1016/j.jaip.2026.03.032)).
- **Yulaf.**
  - Saf yulaf çölyakta semptom ve histolojiyi etkilemedi; kanıt kalitesi düşük (Pinto-Sánchez 2017, [doi](https://doi.org/10.1053/j.gastro.2017.04.009)).
  - Kanada'da ticari yulafın ~%88'i 20 mg/kg'ın üzerinde (Koerner 2011, [doi](https://doi.org/10.1080/19440049.2011.579626)).
  - Türkiye'de "glutensiz" etiketli 15 yulaf ürününün 10'u 20 ppm'in üzerinde. Bu hakemsiz bir preprint (Atasoy 2024, [doi](https://doi.org/10.21203/rs.3.rs-5454884/v1)).
- **Tahin** susam ezmesidir. "Süt yerine tahin" gibi bir ikame susam alerjisini devreye sokar.

**"Fındık yerine ayçekirdeği" kuralı [yorum]:**
- Ayçekirdeği 14'lü listede yok. Bu yüzden etikette vurgulanması zorunlu değil ve ürün verisi zayıf.
- Kural motoru bu ikameyi yalnız şu üç koşul birlikte sağlanırsa onaylar:
  - (a) profilde "ayçekirdeği: tolere ediyor (beyan)" işaretli,
  - (b) susam veya birden fazla kuruyemiş alerjisi kayıtlı değil,
  - (c) ürün "kuruyemiş içerebilir" uyarısı taşımıyor.
- Bunlardan biri eksikse sonuç "onay gerekir" olur, sessiz ikame yapılmaz.

### 2.4 Doğrulama katmanı olan sistemler
- **CARE** (Fu ve ark. 2026, Foods, [doi:10.3390/foods15101647](https://doi.org/10.3390/foods15101647)): Bilgi grafiği + kural kontrolü + isteğe bağlı ajan denetçi. Kısıt karşılama hızlı modda %85,0, doğrulama açıkken %98,5. **Kalan %1,5 ihlal alerjen için kabul edilemez.**
- **NutriOrion** ([arXiv 2602.18650](https://arxiv.org/abs/2602.18650)): Kontrendikasyonları üretim sırasında "sert negatif kısıt" olarak veriyor. Buna rağmen 330 hastada ilaç–besin etkileşimi ihlali %12,1. **Prompt'a konan kısıt bir garanti değil.**
- **FKG.in doğrulaması** ([arXiv 2608.29249](https://arxiv.org/abs/2608.29249)) ve **FoodOntoRAG** ([arXiv 2603.09758](https://arxiv.org/abs/2603.09758)): Malzeme adını ontolojiye bağlıyor; güven skoru düşükse yeniden deniyor. Bizim normalizasyon adımımız için iyi bir model.
- **JSON şeması** ([JSONSchemaBench, arXiv 2501.10868](https://arxiv.org/abs/2501.10868)) sözdizimini garanti eder, anlamı etmez. Format kısıtı akıl yürütmeyi de düşürebilir ([arXiv 2408.02442](https://arxiv.org/abs/2408.02442)).

### 2.5 Önerilen tarif motoru: "LLM önerir, kural motoru karar verir"
```
istek → girdi beyaz listesi (gıda sözlüğü; gıda dışı red)
      → aday tarifler (yalnız onaylı katalog)
      → LLM uyarlama: yalnız ikame_slotu'nda, seçenekler kürate ikame tablosundan
      → şema doğrulama → malzeme → kanonik ID (substring eşleme YASAK)
      → alerjen kapanışı (ontoloji) + çapraz risk kenarları ("onay gerekir")
      → bilinmeyen/açılmamış bileşik malzeme ⇒ FAIL-CLOSED
      → besin: deterministik (§1.4) · pişirme güvenliği: şablon uyarı
      → dört durumlu karar (v3) + karar izi → kullanıcı
```
**Değişmez (invariant), property testinde denetlenir:**
$$
\forall r'\in\text{Çıktı}:\ \ \mathrm{cl}\big(\mathrm{ing}(r')\big)\cap\bigcup_{m\in E_t}A_m=\emptyset\ \ \wedge\ \ \mathrm{unk}(r')=\emptyset
$$
- $\mathrm{cl}$, ontolojideki kapanış. Örnekler: fındık ⊂ ağaç yemişi; tahin ⊂ susam; bulgur, irmik, kuskus ⊂ buğday ⊂ gluten; yulaf → gluten. Yulaf yalnız "sertifikalı glutensiz" ve profilde izin varsa serbest.
- **Türkçe ad tuzakları:** hindistan cevizi ve muskat cevizi ceviz değil. Yer fıstığı baklagil, Antep fıstığı ağaç yemişi. Brezilya fındığı fındık değil ama ağaç yemişi.

**Değerlendirme seti (150–200 altın vaka):**
- Kapsam: ad tuzakları, gizli alerjen içeren bileşik malzemeler ("hazır sos", "glutensiz un karışımı"), lupin/yulaf/tahin/hindistan cevizi vakaları, çok üyeli çakışmalar (fındık + çölyak + yer fıstığı), gıda dışı girdiler (Pak'nSave), FoodGuardBench tarzı jailbreak'ler, Vij tablosundaki satırlar (negatif test).
- **Metrikler:** alerjen ihlali = 0 (CI'da sert kapı), gereksiz engelleme oranı, besin hesabı MAPE.
- **[yorum]** Bu, v3'teki K4 (güvenli NL → kısıt derleyicisi) ile aynı güvenlik felsefesi. Kural motoru ve ontoloji tek bir paylaşılan modül olur.

---

## 3. Haftalık menü optimizasyonu: birleşik problem (MENÜ → LİSTE → MARKET)

### 3.1 Literatür: parçalar var, birleşimi yok
**Klasik ve derlemeler:**
- Balintfy 1964, CACM, ilk bilgisayarlı menü planlama ([doi:10.1145/364005.364087](https://doi.org/10.1145/364005.364087)).
- Balintfy ve ark. 1978, Math Prog: tercih ve ikili yemek uyumu ([doi:10.1007/BF01609000](https://doi.org/10.1007/BF01609000)).
- Koroušić Seljak 2009, JFCA: n günlük plan çok boyutlu sırt çantasına indirgenip evrimsel algoritmayla çözülüyor ([doi:10.1016/j.jfca.2009.02.006](https://doi.org/10.1016/j.jfca.2009.02.006)). Yöntem ayrıntısı yalnız özetten görüldü.
- Ngo ve ark. 2016 derlemesi ([doi:10.3844/jcssp.2016.582.596](https://doi.org/10.3844/jcssp.2016.582.596)).

**Kurumsal menü MIP/ILP'leri:**
- Benvenuti & De Santis 2020 ([doi:10.3389/fnut.2020.562833](https://doi.org/10.3389/fnut.2020.562833)): okul ve bakımevi menüsü. Tekrar sınırları günlük, haftalık ve toplam düzeyde.
- Padovan ve ark. 2023 ([doi:10.1186/s40795-023-00705-0](https://doi.org/10.1186/s40795-023-00705-0)): 205 yemek, 1 ay; tekrar aralığı, doku ve renk kısıtları.
- Arriz-Jorquiera 2024, Waste Management ([doi:10.1016/j.wasman.2023.12.010](https://doi.org/10.1016/j.wasman.2023.12.010)): 1.000 yataklı bir hastane. Çok amaçlı MIP ile israf −%19,7, maliyet −%32,7.
- **Bu çalışmaların hiçbirinde çözüm süresi raporlanmıyor.**

**Türk yazarlar (danışmana yakın referanslar):**
- Kahraman & Seven 2005 GECCO: iki amaçlı GA ([doi:10.1145/1102256.1102345](https://doi.org/10.1145/1102256.1102345)).
- Türkmenoğlu, Uyar, Kıraz 2021, Health Inform J: many-objective diyet ([doi:10.1177/1460458220976719](https://doi.org/10.1177/1460458220976719)).
- **Şahin & Aytekin Şahin 2024, ESWA 252:124213** ([doi:10.1016/j.eswa.2024.124213](https://doi.org/10.1016/j.eswa.2024.124213)): NSGA-II, NSGA-III, SMS-EMOA ve AGE-MOEA karşılaştırılmış. Açık kaynak **EvoMeal** (pymoo, LGPL-3, [GitHub](https://github.com/omursahin/EvoMeal)). **Proposal'da anılmalı.**
- Eren, Kaçmaz, Şengül 2018 ([doi:10.20854/bujse.330745](https://doi.org/10.20854/bujse.330745)): diyabet dahil hastane menüsü, bulanık hedef programlama.
- Okumuş & Küçükoğlu 2025 ([doi:10.17482/uumfd.1571735](https://doi.org/10.17482/uumfd.1571735)): zincir market indirimli gezgin satın alıcı problemi, tabu arama ile Gurobi karşılaştırması. **Türkiye market bağlamına en yakın çalışma.**

**Metasezgisel menü planlama:**
- Marrero ve ark. 2020 ([doi:10.3390/math8111960](https://doi.org/10.3390/math8111960)): ILS-MOEA/D. Tek amaçlı memetik algoritma daha ucuz menü buluyor; çok amaçlı yaklaşım biraz daha pahalıya belirgin biçimde daha az tekrar veriyor.
- Ramos-Pérez ve ark. 2021 ([doi:10.3390/math9010080](https://doi.org/10.3390/math9010080)).

**Hane ve israf (en yakın komşular):**
- **van Rooijen, Gerdessen, Claassen, de Leeuw 2024, RCR 205:107559** ([doi:10.1016/j.resconrec.2024.107559](https://doi.org/10.1016/j.resconrec.2024.107559)). Ajan tam metni okudu.
  - MILP (Gurobi): ikili tarif–gün değişkeni, **tamsayı paket adedi**, stok akışı, 4 kişi × 5 akşam, tek market.
  - Yalnız israf minimize edilince israf **0 g/kişi/gün** ve 2,61 €. Yalnız maliyet minimize edilince 43 g ve 1,77 €.
  - İsrafı sıfırlayan plan görece pahalı paket boyutlarını seçiyor. Tarif sayısı ve çözüm süresi metinde bulunamadı.
- **van Rooijen ve ark. 2025, SPC** ([doi:10.1016/j.spc.2025.05.015](https://doi.org/10.1016/j.spc.2025.05.015)): Kayan ufuk, 21 gün, kimin yemekte olacağı belirsiz. Tarifi evdeki stoğa göre seçmek israfı ~3 g/gün'e indiriyor. Yalnız özet görüldü. **"Kilerdekini önce kullan"ın model kanıtı.**
- **Hespanhol & Aswani 2018, ACC** ([doi:10.23919/ACC.2018.8430885](https://doi.org/10.23919/ACC.2018.8430885)): Aile planı, bozulma dinamiği, ~2.000 tarif × 150 malzeme. Kesin çözüm yerine **derandomize yuvarlamalı yaklaşım algoritması** kullanılmış. Kesin yöntemin ölçekte zorlandığının dolaylı işareti.
- **Cooper ve ark. 2023, RCR** ([doi:10.1016/j.resconrec.2023.106986](https://doi.org/10.1016/j.resconrec.2023.106986)): Randomize deney; haftada bir "use-up day" israfı %33 (Kanada) ve %46 (ABD) düşürüyor. Davranışsal kanıt.

**Market tarafı:**
- Gezgin satın alıcı problemi (TPP) derlemesi: Manerba ve ark. 2017 ([doi:10.1016/j.ejor.2016.12.017](https://doi.org/10.1016/j.ejor.2016.12.017)).
- Promosyon paketli TPP: Küçükoğlu 2025 ([doi:10.1111/itor.70106](https://doi.org/10.1111/itor.70106)). Büyük örneklerde matsezgisel (M-ALNS) Gurobi'yi geçiyor.
- İnternet alışverişi optimizasyonu (ISOP) güçlü NP-zor (Błażewicz ve ark. 2010, [doi:10.2478/v10006-010-0028-0](https://doi.org/10.2478/v10006-010-0028-0)).
- **Önemli:** TPP ve ISOP çalışmaları alışveriş listesini **hazır veri** olarak alıyor.

**Tarif + LLM + tamsayı programlama:** Marin ve ark. ([arXiv 2511.18483](https://arxiv.org/abs/2511.18483)). 157 tarif LLM ile standartlaştırılıp besin veri tabanına eşlenmiş, ikili tamsayı programlamayla 15 haftalık menü kurulmuş. Bizim tarif hattımıza (§1.3) en yakın emsal.

**Araçlar:**
- **Timefold'da menü veya yemek planlama quickstart'ı yok.** GitHub'daki 15 use-case listelendi, en son sürüm v2.6.0. Python sürümü arşivlenmiş.
- OR-Tools'ta resmi bir menü örneği yok. En yakın şablon personel çizelgeleme.
- jMetal 7.5 (MIT) NSGA-II, MOEA/D ve SMS-EMOA içeriyor.

**Ticari uygulamalar:** Eat This Much'ta sanal kiler ve bütçe var; algoritması açıklanmıyor. Paprika'da kiler ve son kullanma tarihi var. Samsung Food'da ücretli kiler özelliği var. **Hiçbiri birden fazla market arasında fiyat optimizasyonu iddia etmiyor.**

**Boşluk [yorum, "taramamızda bulunamadı" dili]:**
1. Menü + tamsayı paket + ≤2 market **tek modelde** yok. van Rooijen tek market kullanıyor; TPP ve ISOP listeyi hazır alıyor.
2. Aynı ortak planda **farklı tıbbi kısıtları olan hane üyeleri** yok. Hastane çalışmaları her hasta grubuna ayrı menü kuruyor.
3. Aynı hane örneklerinde **exact ile GA'yı karşılaştıran ölçek eğrisi** raporlanmamış.
4. Türk tarifleri ve Türk market fiyatlarıyla kurulmuş bir model yok.

### 3.2 Formülasyon: MSM (Menü–Sepet–Market), Akıllı Takas'ın üstüne
**Kümeler:**
- $T$: öğün slotları (gün × öğün). $d(t)$, slotun günü.
- $E_t\subseteq M$: o öğünde yiyen üyeler.
- $R_t$: slot $t$ için aday tarifler. Yapısal eleme ile kurulur, aşağıda (A).
- $I$: kanonik malzemeler. $P_i$: malzeme $i$'nin ürün/paket seçenekleri; $0\in P_i$ alışılmış ürün, diğerleri Akıllı Takas adayları.
- $S$: yarıçap içindeki marketler.
- $L^{\text{alış}}$: tarif dışı alışkanlık satırları (süt, ekmek, kahvaltılık). Bunlar 02 §7'nin satırlarıdır ve §4.3'teki tükenme tahmini ile tetiklenir.

**Parametreler:**
- $a_{ri}$: porsiyon başı çiğ gram. $\sigma_t$: porsiyon ölçeği (§1.5).
- $g_p$: paket gramajı. $c_{ps}$: paketin $s$ marketindeki fiyatı.
- $h_i,\,e_i$: kilerdeki miktar ve son gün.
- $\ell_i$: raf ömrü (§4.1).
- $v_i$: gram başına israf değeri.
- $\tau_r$: hazırlama süresi. $\pi_{rt}$: beklenen beğeni/kabul (§5'ten gelir).
- $b_{rk}$: porsiyon başı besin.
- $\omega_{mt}$: üye payı.

**Değişkenler:**
- $y_{rt}\in\{0,1\}$: slot $t$'ye tarif $r$ atanır.
- $n_{ips}\in\mathbb Z_{\ge0}$: malzeme $i$ için $s$ marketinden alınan $p$ paketi adedi.
- $z_s\in\{0,1\}$: market $s$ seçilir.
- $u_i\ge0$: kilerden kullanılan miktar. $w_i\ge0$: israf.
- $x_{\ell j}$: alışkanlık satırı seçimi (02 §7).

$$
\begin{aligned}
\text{(A)}\;& y_{rt}=0 && \text{eğer } \mathrm{cl}(\mathrm{ing}(r))\cap \textstyle\bigcup_{m\in E_t}A_m\neq\emptyset \ \ \text{(değişken silinir)}\\
\text{(M1)}\;& \textstyle\sum_{r\in R_t} y_{rt}=1 && \forall t\\
\text{(M2)}\;& \textstyle\sum_t y_{rt}\le 1,\quad \sum_{r\in C_c}\sum_{t:\,d(t)\in\{d,d+1\}} y_{rt}\le 1 && \forall r;\ \forall c,d \ \ \text{(tekrar, kategori penceresi)}\\
\text{(M3)}\;& \textstyle\sum_{t\in T^{\text{hi}}}\sum_r \tau_r y_{rt}\le \bar\tau && \text{(hafta içi süre bütçesi)}\\
\text{(M4)}\;& q_i=\textstyle\sum_{t}\sum_r \sigma_t a_{ri}\,y_{rt},\qquad u_i\le h_i,\quad u_i\le \textstyle\sum_{t:\,d(t)<e_i}\sum_r\sigma_t a_{ri}y_{rt} && \text{(kileri SKT'den önce kullan)}\\
\text{(M5)}\;& u_i+\textstyle\sum_{p\in P_i}\sum_{s} g_p\,n_{ips}\ \ge\ q_i && \text{(kapsama; paket tamsayılı)}\\
\text{(M6)}\;& w_i\ \ge\ \big(u_i+\textstyle\sum_{p,s} g_p n_{ips}-q_i\big)\cdot\mathbb 1[\ell_i\le H] + (h_i-u_i)\cdot\mathbb 1[e_i\le H] && \text{(artan bozulur + kiler israfı)}\\
\text{(M7)}\;& n_{ips}\le U_{ip}\,z_s,\qquad \textstyle\sum_s z_s\le 2 && \text{(≤2 market; 02 §7.11)}\\
\text{(M8)}\;& n_{ips}\le U_{ip}\,(1-y_{rt}) && \forall p:\alpha_p\cap\textstyle\bigcup_{m\in E_t}A_m\ne\emptyset,\ i\in r\\
\text{(M9)}\;& \textstyle\sum_{t}\sum_r \omega_{mt}\,b_{rk}\,y_{rt}\ \le\ U_{mk}+s^+_{mk} && \text{(üye besin hedefi, yumuşak)}\\
\text{(M10)}\;& \textstyle\sum_{i}\sum_{p\ne0}\delta_{ip}+\sum_{\ell}\sum_{j\ne0}x_{\ell j}\ \le\ k,\qquad \sum_s n_{ips}\le U_{ip}\,\delta_{ip},\ \ \delta_{ip}\in\{0,1\} && \text{(Akıllı Takas kardinalitesi)}
\end{aligned}
$$
- **(M8):** Paket düzeyinde alerjen. Aynı malzemeyi kullanan bir öğünde kısıtlı üye yiyorsa o ürün alınamaz. (A) tarif düzeyinde, (M8) ürün düzeyinde çalışır; iki katman birbirini tamamlar.
- **(M10):** 02 §7.5'teki (C3) kısıtının bu modele genişlemiş hali. $\delta_{ip}$ = "malzeme $i$ için alışılmıştan farklı ürün $p$ seçildi" göstergesi.
- $H$: plan ufku (gün). $U_{ip}$: paket adedi üst sınırı. $\mathbb 1[\cdot]$ parametre, değişken değil. Model bu yüzden doğrusal kalıyor.
- **Amaç (skaler sürüm):**
$$
\min\ \underbrace{\textstyle\sum c_{ps}n_{ips}+\sum_\ell\sum_j c_{\ell j}x_{\ell j}}_{f_1:\ \text{TL}}
+\lambda_w\underbrace{\textstyle\sum_i v_i w_i}_{f_2:\ \text{israf}}
+\lambda_\tau\textstyle\sum_s\tau_s z_s
-\lambda_p\underbrace{\textstyle\sum_{r,t}\pi_{rt}y_{rt}}_{f_3:\ \text{beğeni}}
-\lambda_h\,H(y,x)+\textstyle\sum\rho\,s^+
$$
  Çok amaçlı sürümde $(f_1,f_2,-f_3)$ ya da sağlık eklenirse 4 amaç kullanılır.

**Menüden listeye türetim:**
- Liste, çözümün kendisidir: $\{(i,p,s,n_{ips})\}\ \cup\ \{x_{\ell j}\}$.
- "Alışveriş listesi türetimi" ayrı bir adım olmaktan çıkar. Kilerde olan malzeme $u_i$ ile düşülür, paket yuvarlaması modelin içindedir.
- **[yorum]** v3'ün "liste → takas" akışı burada "menü + alışkanlık → birleşik sepet" olur. Akıllı Takas, $P_i$ ve $L^{\text{alış}}$ üzerindeki seçim olarak **aynen korunur**.

**Sınıf [yorum]:**
- Atama (M1–M2) + tamsayı örtü (covering) sırt çantası (M5) + sabit maliyetli tesis seçimi (M7) + MMKP (Akıllı Takas) bir arada.
- **Market sayısı sınırı genel κ olduğunda** model ISOP'u özel durum olarak içerir ($|T|=0$, yalnız alışkanlık satırları). Bu haliyle **güçlü NP-zor** (Błażewicz 2010).
- **κ=2'de** market kısmı sayımla polinomdur: $|S|=10$ için 55 küme. Bu durumda zorluk menü × paket etkileşiminden gelir. Menü sabitken bile problem tamsayı örtü sırt çantası ve MMKP içerir, yani **NP-zordur**.
- **Zorluğun kaynağı:** Malzeme ortaklığından doğan **ölçek ekonomisi.** Paket maliyeti $y$'nin ayrılamayan, basamaklı bir fonksiyonu. Aynı ıspanağı iki tarifte kullanmak ikinci tarifin marjinal maliyetini sıfırlayabiliyor. LP gevşetmesi bunu göremiyor: $n$ kesirli olunca paket artığı ve israf yok oluyor.

### 3.3 [sentetik] Ölçüm: birleşik problem gerçekten zor mu?
**Deney kurulumu:**
- Kod: `arastirma/05-ek-menu_bench.py`. Model (A), (M1)–(M7) ve besin/süre kısıtlarının basitleştirilmiş halini içeriyor. Akıllı Takas'ın (M8)–(M10) kısmı yok. Yani ölçülen şey **alt sınır zorluk**.
- Üreteç:
  - Malzemelerin %50'si bozulabilir, raf ömrü 3–10 gün.
  - Paketli ürünlerde 1–3 paket boyutu (200 g – 2 kg). Manav ürünleri 100 g adımla.
  - Tarif başına 4–10 malzeme, Zipf dağılımıyla ortak malzeme (soğan, salça, yağ).
  - Hane 4 kişi; fındık ve gluten yasak.
  - Kilerde malzemelerin %10'u, son günleri 1–7.
  - Market fiyat çarpanı 0,85–1,2, bulunurluk %90.
- Donanım ve yazılım: Apple M1 (8 çekirdek), OR-Tools 9.15. SCIP tek iş parçacığı, CP-SAT 8 işçi. Süre sınırı 60 s, ölçek başına 3 örnek.
- **Sıralı taban çizgisi:** (1) kiler-farkında ama paket, market ve israfı görmeyen doğrusal maliyetle menü seçilir. (2) Menü sabitlenip sepet ve market kesin çözülür. Bugünkü "önce menü, sonra liste" akışının karşılığı bu.

**Sonuçlar** (her ölçekte 3 örnek; ham çıktı `arastirma/05-ek-menu_bench_sonuc.txt`):

| Ölçek | Slot × tarif × malzeme × market | Değişken | Kanıtlanmış optimum, 60 s içinde | 60 s sonunda boşluk (SCIP / CP-SAT) | LP gevşetmesi boşluğu | Sıralı, birleşikten kötü |
|---|---|---|---|---|---|---|
| S0 | 5 × 50 × 60 × 2 | ~250 | CP-SAT 3/3 (0,4–1,5 s) · SCIP 2/3 | 0 / 0 | %34–39 | %4–22 |
| **S1** | **7 akşam × 100 × 120 × 4** | ~800–970 | CP-SAT 2/3 (21 s, 54 s) · SCIP 1/3 (49 s) | %0–4,8 / %0–4,8 | %29–42 | %15–40 |
| S2 | 7 × 200 × 200 × 8 | ~2.300–2.900 | SCIP 1/3 (55 s) · CP-SAT 0/3 | %0–4,9 / %3,2–5,9 | %25–36 | %5–22 |
| S3 | 14 (öğle+akşam) × 200 × 200 × 8 | ~2.900–3.600 | 0/3 | %9,1–12,0 / %3,3–8,7 | %32–38 | %11–16 |
| S4 | 14 × 400 × 300 × 10 | ~5.300–6.800 | 0/3 | %21–26 / %5,0–8,0 | %37–45 | %30–42 |
| S5 | 28 (2 hafta) × 400 × 300 × 10 | ~7.400–9.400 | 0/3 | %24–40 / %8,1–18,2 | %47–53 | %26–56 |

**Tablonun okunuşu:**
- **Boşluk:** Çözücünün bulduğu çözüm ile iki çözücünün en iyi alt sınırı arasındaki fark. Yani gerçek optimallik boşluğunun **üst sınırı**.
- **Sıralı fark:** Birleşik modelde bulunan en iyi çözüme göre ölçüldü, dolayısıyla birleşimin değerinin **alt sınırı**. Amaç TL + israf + yol − beğeni karışımı olduğu için yüzdeler karışık birimli. TL bileşenleri aşağıda.
- **Sıralı yaklaşımın 2. aşaması** (menü sabitken sepet + market) 0,0–3,2 s sürdü. Zorluk tek başına sepette değil, **menü ile paketin birleşmesinde.**

**TL bileşenleri** (birleşik = CP-SAT'ın 60 s'lik çözümü, sıralı = önce menü sonra sepet; ham çıktı `arastirma/05-ek-menu_bench_parca.txt`):

| Örnek | Alım TL (birleşik / sıralı) | İsraf TL (birleşik / sıralı) | Yol (birleşik / sıralı) | Beğeni puanı, TL eşdeğeri (birleşik / sıralı) |
|---|---|---|---|---|
| S1-0 | 3.455 / 5.058 (−%32) | 1.537 / 1.648 | 69 / 114 | 645 / 645 |
| S1-1 | 3.257 / 3.621 (−%10) | 1.003 / 1.231 | 57 / 101 | 580 / 645 |
| S1-2 | 2.397 / 3.463 (−%31) | 1.171 / 1.264 | 24 / 56 | 450 / 555 |
| S3-0 | 5.368 / 6.911 (−%22) | 3.855 / 3.856 | 22 / 22 | 1.140 / 965 |
| S3-1 | 5.345 / 5.470 (−%2) | 3.111 / 3.680 | 52 / 74 | 1.160 / 1.100 |
| S3-2 | 4.365 / 4.922 (−%11) | 2.126 / 2.071 | 26 / 55 | 1.195 / 1.055 |

- **Kazancın çoğu alım TL'sinden geliyor, %2–32.** Birleşik model paket artığını paylaşan tarifleri seçip daha az paket alıyor. İsrafta fark −%19 ile +%3 arasında.
- Birleşik model bazen **beğeniden ödün veriyor** (S1-1, S1-2). Bu, λ ağırlıklarının seçimidir. Çok amaçlı sürüm bu ödünleşimi kullanıcıya açık gösterir.
- **Uyarı:** Üreteçte israf alımın %30–70'i çıkıyor, bu **gerçekçi değil.** Sebepleri: bozulabilir oranı %50, raf ömrü 3–10 gün, ufuk sonundaki artığın tamamı israf sayılıyor, kiler israfı da ekleniyor. Mutlak TL değerleri anlamsız. Yalnız **yön** ve **zorluk** bilgi taşıyor.

**Yorum [sentetik veriye dayalı, gerçek veriyle tekrar edilmeli]:**
1. **Evet, birleşik problem gerçek bir ölçek zorluğu yaratıyor.** Çekirdek Akıllı Takas'ta (02 §7.8) LP boşluğu ≈%0 ve çözüm ms düzeyindeydi. Burada LP boşluğu **%25–53**, ve en küçük gerçekçi ölçekte (bir haftanın akşamları, 100 tarif) bile optimumun kanıtı 60 s'yi zorluyor. Nedeni, paket tamsayılığının yarattığı ve LP'nin göremediği malzeme ortaklığı ekonomisi (§3.2).
2. **Çok amaçlı cephe pahalı.** ε-constraint ile 50 noktalık bir cephe, S1'de bile nokta başına onlarca saniye demek; S3 ve üstünde her nokta boşluk bırakıyor. **NSGA-II ya da matsezgiselin anlamlı rakip olduğu yer tam burası.** v3'ün dürüst hipotezinde ("çekirdekte GA'ya gerek yok") eksik kalan sahne bu.
3. **Ürün açısından:** Kullanıcı planı saniyeler içinde bekler. O yüzden üretimde zaman sınırlı çözüm, sıralı çözümle ısıtma ve boşluğun raporlanması gerekiyor. Bu hem mühendislik gereği hem de araştırma sorusu: "t saniyede hangi yöntem hangi kaliteyi veriyor?"
4. **Sınırlar:**
   - Üreteç sentetik. Bozulabilir oranı, paket boyutları ve ortak malzeme dağılımı zorluğu belirliyor. Gerçek katalog ve 120 tarifle tekrar ölçülmeli.
   - SCIP tek iş parçacığıyla, CP-SAT 8 işçiyle koştu; eşit kaynak değil.
   - HiGHS ve Gurobi denenmedi.
   - (M8)–(M10) eklenince problem daha da zorlaşır.

---

## 4. Mutfak: kiler ve buzdolabı takibi

### 4.1 Raf ömrü ve yasal tanımlar
**USDA FoodKeeper:**
- data.gov'da XLS ve JSON olarak var, lisansı **CC0** ([katalog](https://catalog.data.gov/dataset/fsis-foodkeeper-data)). FSIS sunucusu indirmeyi engelledi; ajan Wayback'teki 14.03.2025 kopyasını indirip çözümledi.
- İçerik: **661 ürün, 14 ana kategori.**
- Alanlar: kiler, buzdolabı ve dondurucu süreleri. `DOP_*` alanları "satın alma tarihinden itibaren" demek. Bunlara ek olarak `*_After_Opening` ve `Refrigerate_After_Thawing` var.
- Kapsam: 499 üründe buzdolabı, 331'inde kiler süresi var. **Açıldıktan sonra** süre yalnız 146 üründe (buzdolabı).
- **Son içerik sürümü 128, tarihi 06.09.2018.** Tablo eski ama kategori düzeyinde yeterli.

**Diğer kaynaklar:**
- **StillTasty** koşulları ticari yeniden kullanımı yasaklıyor ([ToS](https://www.stilltasty.com/Staticpages/view/Terms%20of%20Use)). **Kullanılamaz.**
- **WRAP / Love Food Hate Waste** rehberleri niceliksel değil (gün sayısı yok).
- **Türkiye:** Tüketici için resmi bir raf ömrü veri seti **bulunamadı.** Bakanlığın raf ömrü kılavuzu üreticiye yönelik ([PDF](https://kirklareli.tarimorman.gov.tr/Belgeler/001.098/G%C4%B1da%20Etiketlerinde%20Raf%20%C3%96mr%C3%BC%20Bilgisinin%20Belirlenmesi%20Ve%20Belirtilmesi%20Hakk%C4%B1nda%20K%C4%B1lavuz.pdf)). Gıdayı üç gruba ayırıyor: kolay bozulan ≤60 gün, yarı dayanıklı 60 gün–6 ay, dayanıklı ≥6 ay. Bir de kural koyuyor: TETT geçse de görünüş, koku ve tat bozulmamışsa gıda tüketilebilir.

**TGK Etiketleme Yönetmeliği** (RG 26.01.2017):
- **STT** (m.4/v): mikrobiyolojik açıdan kolay bozulan gıdanın tüketilebileceği son tarih.
- **TETT** (m.4/bb): uygun muhafazada gıdanın kendine has özelliklerini koruduğu süre.
- m.27: STT'si geçmiş gıda "güvenilir olmayan gıda" sayılır.

**Sonuç [yorum]:**
- STT → **katı uyarı**. TETT → **yumuşak uyarı**, "koku ve görünüşü kontrol et" metniyle.
- Türkçe kategori → FoodKeeper eşleme tablosu elle kurulur (~100–150 kategori, CC0).
- Varsayılan son gün: satın alma tarihi + `DOP_*` aralığının **alt** sınırı. Ambalajdaki tarih girildiyse o geçerli. Ürün açıldıysa `*_After_Opening` kullanılır.
- Bu tarih §3.2'de $\ell_i$ ve $e_i$ parametresi olarak menü modeline girer.

### 4.2 Girdi kanalları
| Kanal | Işık | Gerekçe | Asgari yaklaşım |
|---|---|---|---|
| **Barkod ("eve girdi")** | 🟢 | Kesin kimlik veriyor. OFF'ta TR etiketli **11.415** ürün var (API, 24.09.2026). Kapsam sınırlı ama v3 katalog v0 bu açığı kapatıyor. | Bilinmeyen ürünü kullanıcı bir kez adlandırır. STT/TETT isteğe bağlı: elle ya da OCR ile. |
| **e-Arşiv fatura** (online market) | 🟡 | GİB e-Arşiv Kılavuzu v1.18: UBL-TR, `EARSIVFATURA`. PDF'e XML gömmek zorunlu. `InvoiceLine` içinde `Item/Name` zorunlu; `SellersItemIdentification` ve `ManufacturersItemIdentification` seçimli. GTIN'in doğal yeri olan `StandardItemIdentification` fatura kaleminde **yok**. GİB'in örnek faturasındaki kalem yalnız `EKMEK`. ([kılavuz](https://ebelge.gib.gov.tr/dosyalar/kilavuzlar/e-Arsiv_Teknik_Kilavuzu_V.1.18.pdf)) | Ad, miktar, birim ve fiyat garanti. **Barkod garanti değil.** Migros ve A101 faturalarında iç kod ya da barkod olup olmadığı **DOĞRULANMADI**; 3–5 gerçek faturaya bakılmalı. |
| **Fiş fotoğrafı** | 🟡 | VLM veya OCR ile yapılabilir. Karşılaştırma için Donut, CORD fiş setinde ~%91,3 alan doğruluğuna ulaşıyor (ince ayarlı, [GitHub](https://github.com/clovaai/donut)). Türk fişinde kısaltmalar ve barkod yokluğu var (02-v2-fis-veri). | v3 fiş hattı olduğu gibi kullanılır. Kiler için ek bir iş yok. |
| **Buzdolabı fotoğrafı** | 🔴 ana kaynak olarak / 🟡 onay katmanı olarak | Aşağıdaki 4.4'e bakın. | Yalnız "şunlar hâlâ duruyor mu?" onayı. Envanteri **yazmaz**. |

**Envanter modeli [yorum]:**
- Olay tabanlı çalışır. Giriş = barkod, e-Arşiv veya fiş. Çıkış = tek dokunuş "bitti" ya da "attım", ya da menüde pişirildi işaretiyle $q_i$ kadar otomatik düşüm.
- Stok miktarı kesin değil, **tahmindir.** Arayüzde "yaklaşık" diye gösterilir.

### 4.3 "Bitmek üzere": kategori önselli Gamma–Poisson
**Literatür:**
- NBD / Poisson–gamma karışımı klasik satın alma modeli (Ehrenberg 1959, [doi:10.2307/2985810](https://doi.org/10.2307/2985810)).
- Aralıklı talep için Croston/SBA (Syntetos & Boylan 2005, [doi:10.1016/j.ijforecast.2004.10.001](https://doi.org/10.1016/j.ijforecast.2004.10.001)).
- **Amazon "Buy It Again"** (Bhagat ve ark. KDD 2018, [doi:10.1145/3219819.3219891](https://doi.org/10.1145/3219819.3219891)): Poisson–Gamma, gamma önseli empirical Bayes ile. Tıklama oranında %7'nin üzerinde artış.
- TIFU-KNN (Hu ve ark. SIGIR 2020, [doi:10.1145/3397271.3401066](https://doi.org/10.1145/3397271.3401066)): basit kişisel frekans yöntemi, derin next-basket modellerini sık sık geçiyor.
- **Derin model gerekmiyor.**

**Model [yorum], hane $h$ × kategori $c$:** Tüketim hızı $\lambda_{hc}$ (birim/gün) için kategori düzeyinde önsel kullanılır:
$$
\lambda_{hc}\sim\mathrm{Gamma}(a_c,b_c),\qquad (a_c,b_c)\ \text{tüm hanelerden empirical Bayes ile}
$$
Gözlem: $k$'inci alımda $Q_k$ birim alındı ve bu miktar $\Delta t_k$ günde bitti. Aralık bir sonraki alımla ya da "bitti" dokunuşuyla kapanır. Buna göre sonsal:
$$
\lambda_{hc}\mid\mathcal D\sim\mathrm{Gamma}\Big(a_c+\textstyle\sum_k Q_k,\ \ b_c+\textstyle\sum_k \Delta t_k\Big)
$$
Son alımdan $\tau$ gün sonra stoğun bitmiş olma olasılığı:
$$
\Pr[\text{bitti}]=\Pr\!\left[\lambda_{hc}\ge \frac{S_0}{\tau}\right]=1-F_{\Gamma}\!\left(\frac{S_0}{\tau};\,a',b'\right)
$$
- Olasılık ≥ 0,7 olduğunda kalem listeye "muhtemelen bitti" etiketiyle önerilir. Kalem $L^{\text{alış}}$'e girer ve Akıllı Takas'a oradan geçer (§3.2).
- Kapalı formda hesaplanıyor, açıklanabilir ("genelde 6 günde bitiriyorsun"), küçük veride önsel sayesinde kararlı.
- Seyrek alınan ürünlerde Croston/SBA kullanılır.
- **Ölçüm:** "Bitti" dokunuşları gerçek değer kabul edilir. Metrik, bitiş gününe göre ±2 gün isabet oranı.

### 4.4 Buzdolabı fotoğrafından tanıma: 2024–2026 durumu
**Samsung Family Hub "AI Vision Inside":**
- Duyuruya göre **37 taze ürün** tanıyor. İşlenmiş ürünler kullanıcının adlandırdığı **en fazla 50 ürünle** sınırlı. Dipnotlarda şunlar yazıyor: ürünler kapıdan tek tek taranmalı, kapı rafı ve dondurucu tanınmıyor, doğruluk garanti edilmiyor ([Samsung CA](https://news.samsung.com/ca/samsung-unveils-new-refrigerator-lineup-equipped-with-screens-and-enhanced-ai-vision-inside-feature)).
- CES 2026'da Gemini tabanlı sürüm duyuruldu; doğruluk rakamı yok.
- **[yorum]** Sektör lideri bile statik raf fotoğrafını değil, **kapıdan giren ve çıkan tek ürünü** tanıyor. "Giriş olayı" modelimizle aynı mantık.

**Akademik:**
- Dai 2024, Frontiers in AI ([doi:10.3389/frai.2024.1442948](https://doi.org/10.3389/frai.2024.1442948)): özel veri setlerinde mAP50 %96,5–97,2. Ancak paketli ürüne odaklı; sayım ve tarih okuma yok.
- "VLMs are blind" ([arXiv 2407.06581](https://arxiv.org/abs/2407.06581)): GPT-4o ve Gemini 1.5 Pro temel görsel testlerde ortalama ~%58. Öğeler üst üste bindiğinde ya da birbirine yakın olduğunda başarı düşüyor.
- VLM'ler karmaşık sahnede güvenilir sayamıyor ([arXiv 2512.15254](https://arxiv.org/abs/2512.15254)).
- **Buzdolabına özgü bir GPT-4o/Gemini envanter benchmark'ı bulunamadı.**

**Sonuç:**
- Wow anı ("buzdolabı fotoğrafı → evde ne var + 3 tarif") **demo olarak yapılabilir**. Ama envanteri yazamaz.
- Doğru kullanım: Fotoğraftan çıkan liste mevcut envanterle karşılaştırılır. Kullanıcıya "şunları görmedim, bitti mi?" / "şunu gördüm, eklensin mi?" diye sorulur, **kullanıcı onaylar.**
- Kendi küçük test setimiz (20–30 buzdolabı fotoğrafı, elle sayılmış) ile ürün düzeyinde duyarlılık ve kesinlik ölçülür, raporda dürüstçe verilir.

### 4.5 İsraf: Türkiye verisi ve müdahale kanıtı
**UNEP Food Waste Index (ajan raporları indirip taradı):**
- **2021:** Türkiye 93 kg/kişi/yıl, **düşük güven**.
- **2024:** Türkiye **102 kg/kişi/yıl**, **düşük güven** (s.172). Aynı raporda Türkiye için "no estimates for household food waste" yazıyor. Yani rakam **ölçüm değil, başka ülkelerden ekstrapolasyon.** Küresel hane israfı 79 kg/kişi/yıl ([UNEP](https://www.unep.org/resources/publication/food-waste-index-report-2024)).
- **Proposal'a etkisi:** v3 ve kırmızı takım belgelerindeki "93 kg" ifadesi güncellenmeli: "UNEP 2024 tahmini 102 kg, düşük güven, ölçüme dayanmıyor". Basında TİSVA'ya atfedilen 102 kg da aynı ekstrapolasyon.

**Türkiye'deki ölçümler:**
- Pekcan ve ark. (Hacettepe/FAO 2006, [PDF](https://www.fao.org/4/am063e/am063e00.pdf)): Ankara, 500 hane. Kişi başı günde **318,8 g** atılıyor, israf günlük enerji alımının %9,8'i. Tartım değil, 24 saatlik hatırlama anketi; yenmeyen kısımlar da dahil.
- Songür Bozdağ & Çakıroğlu 2021: 1.488 hane, çevrimiçi anket. En sık nedenler küflenme, buzdolabında unutma ve tarihin geçmesi. **Bu üç neden doğrudan Mutfak adımının hedefi.**
- **Tartıma dayalı ulusal bir hane israfı ölçümü yok.**

**Müdahale kanıtı:**
- Reynolds ve ark. 2019, Food Policy ([doi:10.1016/j.foodpol.2019.01.009](https://doi.org/10.1016/j.foodpol.2019.01.009)): buzdolabı kamerası ve paylaşım uygulamaları için "little or no robust evidence".
- **Seta ve ark. 2026, Detritus** ([doi:10.31025/2611-4135/2026.19596](https://doi.org/10.31025/2611-4135/2026.19596)): Japonya, 126 hane, kontrol gruplu. Oyunlaştırılmış buzdolabı öz-izleme uygulaması. İsraf otomatik tartıyla ölçülmüş: müdahale grubunda haftalık **−190 g (−%45)**, kontrolde −%13.
- Cooper 2023'teki "use-up day" deneyi (§3.1) ve van Rooijen 2025'teki stoğa göre tarif seçimi modeli de aynı yönü gösteriyor.
- **[yorum]** Bizim beta'da ölçüm "attım" beyanına dayanacak, yani sapmalı olacak. İddia **"israf azalır" değil**, "kilerdeki SKT'si yaklaşan ürünlerin plana alınma oranı" ve "beyan edilen israf" olarak kurulmalı.

### 4.6 Mevcut uygulamalar
SuperCook, NoWaste, KitchenPal, Samsung Food, Cooklist, Paprika:
- Kiler takibi ve "kilerdekiyle tarif" yaygın.
- Cooklist sadakat kartından otomatik alım çekiyor; ABD'deki e-Arşiv karşılığı.
- Türkiye'de öne çıkmış yerli bir oyuncu yok; küçük uygulamaların değerlendirme sayısı 0–21.
- **Hiçbiri kiler + menü + çok üyeli alerjen + çok market fiyatını birlikte optimize etmiyor.**
- Kilerin kendisi özgün değil. Özgünlük, **kilerin optimizasyona girdi olması**: (M4) ve (M6) kısıtları ile $L^{\text{alış}}$ tetikleyicisi.

---

## 5. Öneri sistemi (danışmanın alanı): kısıt-farkında, küçük veri

### 5.1 Literatür: kısıt nerede uygulanıyor?
**Derlemeler:**
- Trattner & Elsweiler 2017 ([arXiv 1711.02760](https://arxiv.org/abs/1711.02760)).
- Min, Jiang, Jain 2020, IEEE TMM ([doi:10.1109/TMM.2019.2958761](https://doi.org/10.1109/TMM.2019.2958761)).
- **Bondevik ve ark. 2024, ESWA** ([doi:10.1016/j.eswa.2023.122166](https://doi.org/10.1016/j.eswa.2023.122166)): 67 çalışma. Çoğu içerik tabanlı, değerlendirme ağırlıkla offline doğruluk.
- **Dong ve ark. 2026, JMIR** ([doi:10.2196/77726](https://doi.org/10.2196/77726)): kronik hastalıklar için 15 sistem. %40'ı kısıt tabanlı. **Hiçbiri uzun vadeli davranışı ölçmemiş.**

| Çalışma | Kısıt nerede | Not |
|---|---|---|
| Chen ve ark. WSDM 2021 ([doi](https://doi.org/10.1145/3437963.3441816)) | **Sorguda, sembolik** (bilgi grafı üzerinde QA) | Kişiselleştirilmemiş tabanlara göre +%59,7 |
| HUMMUS, RecSys 2023 ([doi](https://doi.org/10.1145/3604915.3609491)) | **Post-hoc** eşik filtresi | Food.com'dan. Veri yalnız eğitim/bilim amaçlı |
| MOPI-HFRS, KDD 2025 ([doi](https://doi.org/10.1145/3690624.3709382)) | **Loss'ta, yumuşak** (Pareto) | Sert alerjen kısıtı yok |
| Wang & Wang, Electronics 2026 ([doi](https://doi.org/10.3390/electronics15122628)) | **Cezaya dayalı** alerjen skoru (çapraz reaksiyon dahil) | N=20. Deterministik garanti yok |
| Yum-me, TOIS 2017 ([doi](https://doi.org/10.1145/3072614)) | **Önce filtrele, sonra sırala** | Görsel ikili seçimle onboarding |
| Harvey & Elsweiler, RecSys 2015 ([doi](https://doi.org/10.1145/2792838.2796551)) | Öğün planı kısıtlı sırt çantası olarak | Öneri ile optimizasyonun erken köprüsü |

**Sonuç [yorum]:**
- Alerjen bir doğruluk sorusu değil, bir **olurluk kısıtı.** Yeri aday üretim aşamasıdır: filtre → sırala → son listede ikinci kontrol.
- Sağlık ve çeşitlilik yumuşak hedeftir. Yeniden sıralamada ya da görünürlük (exposure) kısıtında kullanılır (Singh & Joachims 2018, [doi](https://doi.org/10.1145/3219819.3220088)).

### 5.2 Veri hacmi gerçeği
**Pilot kaba hesabı [tahmin]:** 20–40 hane × haftada ~5 akşam × 6 hafta ≈ **600–1.200 menü kabul/red olayı** ve ~200 tarif.
- **Kluver & Konstan 2014** ([doi](https://doi.org/10.1145/2645710.2645742)): İlk birkaç puanda basit taban çizgisi üç yaygın CF algoritmasından iyi. ItemItem yeni kullanıcıda çok kötü.
- **Dacrema ve ark. 2019** ([doi](https://doi.org/10.1145/3298689.3347058)): İncelenen 18 nöral yöntemin 7'si yeniden üretilebilmiş, bunların 6'sı çoğu zaman basit sezgisel yöntemlere yeniliyor.
- **Kesin bir "N etkileşim" eşiği literatürde yok.**
- **Veri transferi:** Food.com'un lisansı "© Original Authors", HUMMUS yalnız eğitim/bilim amaçlı. Bu veriler **üründe kullanılamaz**; yalnız offline simülatör ya da ön deney için olur. Ayrıca ABD tercih dağılımı Türk hanesine taşınmamalı [yorum].
- **"Senin gibi haneler" pilotta [yorum]:** "Fındık alerjili çocuklu hane" gibi dar bir kohort pilotta muhtemelen 2–5 hane olur. k≥5 eşiği sağlanamaz. Yani bu wow anı **pilot verisiyle dürüstçe gösterilemeyebilir.**
  - Seçenek (a): daha geniş kohorta geri çekilmek ("çocuklu haneler") ve bunu etiketlemek.
  - Seçenek (b): simülatörde göstermek.

### 5.3 Katmanlı yaklaşım
Eşikler bizim önerimiz, literatürle kesinleşmedi.
- **v0 (ilk gün): içerik + kural.**
  - Sert filtre, fail-closed.
  - Onboarding: ikili görsel seçim veya grup tabanlı tercih toplama. Chang ve ark. 2015'te süre yarıya inmiş, memnuniyet artmış ([doi](https://doi.org/10.1145/2675133.2675210)).
  - Güvenli küme içinde içerik benzerliği + genel popülerlik.
- **v1 (~15–20 aktif hane): kohort popülerliği, geri çekilme ve büzülmeyle.**
$$
\hat p_{c,r}=\frac{s_{c,r}+\kappa\,\hat p_{\text{üst}(c),r}}{n_{c,r}+\kappa},\qquad \text{göster} \iff |\text{hane}(c)|\ge k\ (k=5)
$$
  - $s$: kabul sayısı, $n$: gösterim sayısı. Kohort ağacı: {alerjen kümesi × çocuk var/yok} → {çocuk var/yok} → tüm haneler.
- **v2 (~30+ hane, hane başına 20–30 etkileşim): güvenli küme içinde Beta–Bernoulli Thompson örneklemesi.**
  - Önsel kohorttan gelir: $\mathrm{Beta}(\kappa\hat p_{c,r},\,\kappa(1-\hat p_{c,r}))$.
  - Matris faktörizasyonu (MF/BPR), ancak offline'da popülerlik tabanını güven aralığıyla geçerse devreye girer.

**Optimizasyona bağlantı (danışmanın iki alanı tek boru hattında) [yorum]:**
- Öneri sisteminin çıktısı bir liste değil, **menü modelinin parametresi:** $\pi_{rt}$ (M-amaç, $f_3$) ve Akıllı Takas'ın $\pi_{\ell j}$'si.
- Yani **"öneri sistemi optimizasyonun girdisini öğrenir, optimizasyon da öneri sisteminin göstereceği kümeyi kısıtlar."**
- Thompson örneklemesi keşfi yalnız olurlu (güvenli) küme içinde yapar (02 §7.10'daki P2 politikasıyla aynı).

### 5.4 Gizlilik
- **Toplu çıktı da sızdırır:**
  - "Birlikte alınanlar" listelerinin zaman içindeki değişimi bireysel işlemleri ele verebiliyor (Calandrino ve ark. 2011, [doi:10.1109/SP.2011.40](https://doi.org/10.1109/SP.2011.40)).
  - Bir kullanıcının eğitim verisinde olup olmadığı yalnız önerilerden çıkarılabiliyor (Zhang ve ark. CCS 2021, [doi](https://doi.org/10.1145/3460120.3484770)).
- **Tasarım:** k-anonim eşik + **haftalık toplu yayın** (farklılık saldırısına karşı) + isteğe bağlı DP gürültüsü (ReuseKNN 2023, [doi](https://doi.org/10.1145/3608481)).
- **Federated öneri** 20–40 hane için gereğinden ağır. Kapsam dışı.
- **KVKK m.6:** sağlık verisi özel nitelikli; dayanak açık rıza, Kurul'un 2018/10 kararındaki önlemler uygulanır. Alerjinin sağlık verisi sayılması yorumdur, hukuki teyit gerekir. Veri Türkiye'de tutulur (01-mevzuat-risk ile uyumlu).

### 5.5 Küçük pilotta değerlendirme
- **Offline sonuç online'ı öngörmeyebilir:** Offline'da en iyi olan "en popüler" stratejisi canlıda en kötüsü çıkmış (Garcin ve ark. 2014, [doi](https://doi.org/10.1145/2645710.2645745)).
- **A/B yerine interleaving:** Aynı hanede iki algoritmanın listesi karıştırılarak gösterilir (Chapelle ve ark. 2012, [doi](https://doi.org/10.1145/2094072.2094078)).
- **Ölçülecekler:**
  - Kısıt ihlali = 0 (metrik değil, geçme koşulu).
  - Kabul oranı: pişirdi / satın aldı.
  - Kapsam ve çeşitlilik.
  - Kısa ResQue anketi ([doi](https://doi.org/10.1145/2043932.2043962)).
  - Offline'da leave-one-out ve bootstrap güven aralığıyla, **her model popülerlik tabanına karşı.**

---

## 6. Sonuç

### 6.1 Adım adım ışıklar
| Adım | Bileşen | Işık | Neden / koşul |
|---|---|---|---|
| **MENÜ** | Tarif verisi | 🟡 → 🟢 | Açık ve temiz set yok, kazıma 🔴. Ekip ~200 tarifi yazarsa 🟢 olur [tahmin: ~50 saat + ~15–20 saat sözlük]. |
| | Tariften besin + porsiyon | 🟢 | FDC CC0 + USDA retention/yield + TÜBER ölçü ve enerji tabloları, deterministik hesap. Mikrobesin "tahmini" etiketiyle. |
| | LLM tarif üretimi | 🔴 canlıda serbest üretim | Kanıtlar LLM'in güvenlik kararı veremeyeceğini gösteriyor (§2.1, §2.4). |
| | LLM uyarlama (ikame slotu) | 🟡 → 🟢 | Kürate ikame tablosu + ontoloji kapanışı + fail-closed + 0-ihlal CI kapısı şartıyla. |
| | Menü optimizasyonu (birleşik MSM) | 🟢 teknik, derinlik **yüksek** | Formülasyon hazır. Ölçek zorluğu gerçek (§3.3). Ürün için zaman sınırlı çözüm şart. |
| **LİSTE** | Menüden listeye türetim | 🟢 | Ayrı bir adım değil, MSM çözümünün kendisi. Akıllı Takas içinde korunuyor. |
| **MUTFAK** | Barkod "eve girdi" | 🟢 | Kesin kimlik. Katalog v0 ile kapsam artıyor. |
| | e-Arşiv / fiş | 🟡 | Ad, miktar ve fiyat var, barkod garanti değil. v3 eşleştirme hattıyla aynı altyapı. |
| | Raf ömrü | 🟢 | FoodKeeper CC0 (661 ürün) + STT/TETT kuralı. Türkçe kategori eşlemesi elle yapılır. |
| | Bitmek üzere | 🟢 | Kategori önselli Gamma–Poisson, kapalı form, küçük veride kararlı. |
| | Buzdolabı fotoğrafı | 🔴 envanter kaynağı olarak / 🟡 onay katmanı olarak | Samsung bile 37 taze ürün ve tek tek tarama ile sınırlı. VLM sayımı zayıf. |
| | İsraf ölçümü | 🟡 | Kendi ölçümümüz beyana dayanacak. Türkiye rakamı (102 kg) ölçüm değil. |
| **ÖNERİ** | v0 içerik + kural | 🟢 | Filtre → sırala. |
| | Kohort ("senin gibi haneler") | 🟡 | k≥5 eşiği pilotta dar kohortlarda tutmaz; geniş kohorta geri çekilme ya da simülasyon gerekir. |
| | İşbirlikçi filtreleme / matris faktörizasyonu | 🔴 pilot ölçeğinde | Kanıt: küçük veride basit tabanlar CF'yi yeniyor (Kluver 2014, Dacrema 2019). |

### 6.2 En büyük riskler ve çözümleri
1. **Kapsam patlaması.** v4, v3 çekirdeğinin üstüne menü, kiler ve öneri ekliyor.
   - **Çözüm:** Menü MVP'si yalnız hafta içi 5 akşam yemeği ve 120 tarif; sonra 200'e çıkılır.
   - Kiler MVP'si: barkod ve fişle "eve girdi" + SKT + "bitti" dokunuşu.
   - Öneri MVP'si: v0.
   - Buzdolabı fotoğrafı could.
2. **Tarif verisinin hukuki temizliği.**
   - **Çözüm:** Tarifleri ekip yazar. HF setleri yalnız geliştirme içinde kullanılır. Kazıma yok.
3. **LLM tarif güvenliği.**
   - **Çözüm:** Canlıda serbest üretim yok. Uyarlama yalnız ikame slotlarında, kural motoru fail-closed. CI'da 150–200 vakalık altın set ve 0-ihlal kapısı. İkame tablosunun kendisi de test edilir.
4. **Birleşik modelin çözüm süresi.**
   - **Çözüm:** Zaman sınırı (ör. 5 s) + sıralı çözümden ısıtma + boşluğu gösterme ("bu plan en iyiye en fazla %X uzak") + arka planda iyileştirme. Aynı zamanda araştırma sorusu (D2).
5. **Kiler doğruluğu.** Stok tahmini yanlışsa menü de yanlış olur.
   - **Çözüm:** Stok "yaklaşık" gösterilir. Planın kullandığı kiler kalemleri onaylatılır ("yoğurt hâlâ var mı?"). Kullanıcı "yok" derse $h_i=0$ alınıp yeniden çözülür. Bu da canlı yeniden optimizasyon demo anı olur.
6. **Öneri sistemi için pilot verisi yetersiz.**
   - **Çözüm:** Katmanlı yol (v0 → v1 → v2) ve Food.com tohumlu offline simülatör. İddia "kabul oranı" ile sınırlanır.
7. **Zayıf israf rakamları.**
   - **Çözüm:** Metinde "UNEP 2024 tahmini 102 kg/kişi/yıl, düşük güven, ekstrapolasyon" diye yazılır. Kendi metriğimiz "SKT'si yaklaşan kiler ürününün plana alınma oranı" + "beyan edilen israf".

### 6.3 Danışmana gösterilecek derinlik noktaları
**D1 — Birleşik MSM formülasyonu ve zorluğun kaynağı.** Formülasyon §3.2'deki (A), (M1)–(M10). Sınıfı: atama + tamsayı örtü sırt çantası + sabit maliyetli tesis seçimi + MMKP. Genel market sınırı κ'da ISOP'u içerir, dolayısıyla güçlü NP-zor. κ=2'de de NP-zor (§3.2). Zorluk tek ifadeyle şöyle yazılabilir:
$$
\min_{y}\ \Phi(y),\qquad \Phi(y)=\min_{n,z,u}\Big\{\textstyle\sum c\,n+\lambda_w\sum v\,w\ :\ (\text{M4–M7})\Big\}
$$
- $\Phi$, menü $y$'nin **ayrılamayan, basamaklı** bir fonksiyonu. Paket artığı malzeme ortaklığıyla sıfırlanabiliyor.
- LP gevşetmesi bunu görmüyor: [sentetik] boşluk %25–53, Akıllı Takas'ta ≈%0.

**D2 — Exact ile NSGA-II/matsezgisel karşılaştırması (v3'teki K3'ün asıl sahnesi).**
- **Yöntemler:**
  - (E1) Monolitik MILP (SCIP/HiGHS/CP-SAT), zaman sınırlı, boşluk raporlu.
  - (E2) Ayrıştırma: ≤2 market kümesi sayılır (|S|=10 için 55 alt problem), her biri MILP.
  - (H1) **NSGA-II menü üzerinde + iç kesin sepet.** Gen = slot başına tarif; tekrar ve kategori için onarım. İç sepet + market MILP'i [sentetik] 0,0–3,2 s sürüyor, bu yüzden önbellek ya da hızlı iç sezgisel gerekir.
  - (H2) Saf NSGA-II: menü + paket için tamsayı kodlama.
  - (H3) Timefold yerel arama (üretim adayı).
  - (B) Sıralı taban çizgisi + açgözlü.
- **Amaçlar:** $f_1$ TL, $f_2$ israf, $f_3$ beğeni (+ sağlık $H$).
- **Metrikler:** hypervolume, IGD+ (küçük ölçekte kesin cepheye, büyükte birleşik en iyi bilinen cepheye göre), time-to-target, boşluk.
- **Tasarım:** 20 senaryo × 30 tohum. Faktörler: slot {5, 7, 14}, tarif {50, 100, 200, 400}, market {2, 4, 8, 10}, kiler dolu/boş, hane tipi. Danışmanın WB-MCLP makalesindeki 20 senaryolu tasarımın paraleli.
- **İstatistik:** Wilcoxon, Friedman + Holm, $A_{12}$ (02 §7.10).
- **Dürüst hipotez:** S0'da exact saniyede kesin sonuç veriyor. S1–S2'de bazı örnekler 60 s'de kanıtlanıyor, bazıları kanıtlanamıyor. S3'ten itibaren hiçbiri kanıtlanamıyor. 3 amaçlı cephe exact için pahalı; GA ve matsezgiselin gerekçesi burada. Gerçek veride zorluk daha az çıkarsa, bu da dürüstçe raporlanır.

**D3 — "Birleşimin değeri" ve "israfın fiyatı".**
$$
\mathrm{VoI}=f\big(y^{\text{sıralı}},\,n^{*}(y^{\text{sıralı}})\big)-f^{*}_{\text{birleşik}}\ \ \ge 0,
\qquad
\Pi_w(W)=\min\{f_1 : f_2\le W\}
$$
- [sentetik] VoI, birleşik amaca göre %4–56. Yalnız alım TL'sine bakınca %2–32.
- $\Pi_w$ eğrisinin eğimi: **1 kg israfı önlemenin TL bedeli.** Akıllı Takas'taki "sağlığın fiyatı"nın (02 §7.9) kardeşi, ε-taramasıyla kesin çıkarılır.
- Hane için anlamı: "Bu hafta israfı yarıya indirmek X TL." X gerçek veriyle hesaplanacak.

**D4 — Güvenliğin yapıyla sağlanması.**
- Tarif düzeyi: (A) değişken eleme.
- Ürün düzeyi: (M8).
- Ontolojide alerjen kapanışı $\mathrm{cl}(\cdot)$ ve property testteki değişmez (§2.5).
- EAACI'ye dayanan "onay gerekir" kenarları.
- **LLM hiçbir aşamada olurluk kümesini değiştiremez.**

**D5 — Öneri ile optimizasyonun köprüsü (danışmanın iki alanı).**
- Kohort-hiyerarşik Bayes önseli $\hat p_{c,r}$ → Thompson örneklemesi → çıktı, menü modelindeki $\pi_{rt}$ parametresi.
- Keşif yalnız olurlu kümede yapılır.
- Gizlilik: k-anonimlik + haftalık toplu yayın.
- Değerlendirme: simülatörde regret, pilotta interleaving.

**D6 — Kiler, optimizasyonun girdisi.**
- FoodKeeper ve STT/TETT'ten $e_i$ ve $\ell_i$ gelir.
- Gamma–Poisson tükenme olasılığı $1-F_\Gamma(S_0/\tau)$, $L^{\text{alış}}$ satırlarını tetikler.
- Kilerde duran ve SKT'si yaklaşan ürün (M4) üzerinden menüye girer.
- Böylece MUTFAK → MENÜ → LİSTE döngüsü **tek bir model** içinde kapanır.

### 6.4 Önceki belgelere etkisi (Levent onayıyla işlenecek)
- **03-tez-v3 §8** "yemek planı kapsam dışı" diyor, **00-sentez** "TR tarif verisi yok" diyor. Veri sorunu küratörlükle çözülebildiği için bu gerekçe zayıfladı. Ayrıca birleşik MSM, **exact vs GA çalışmasının en güçlü sahnesi** olabilir.
- **"93 kg"** ifadesi → "UNEP 2024: 102 kg/kişi/yıl, düşük güven, ekstrapolasyon".
- **K3'ün dürüst hipotezi** güncellenir: çekirdek sepet ms'de çözülüyor, ama birleşik menü–sepet–market kesin yöntemi zorluyor.

---

## 7. Açık sorular

**Levent'e:**
1. Menü kapsamı: yalnız hafta içi akşam yemeği mi (öneri), yoksa kahvaltı ve öğle de mi? Ölçek ve tarif sayısı buna bağlı.
2. ~200 tarifi kim yazacak? Ekip mi, aile tarifleri mi? Bir diyetisyen tarifleri ya da ikame tablosunu onaylayabilir mi?
3. Buzdolabı fotoğrafı wow'u "onay katmanı" rolüyle kabul mü? Envanteri yazamaz.
4. "Senin gibi haneler" pilotta k eşiğine takılacak. Geniş kohort mu gösterilsin, simülasyon mu?

**Danışmana:**
1. Birleşik MSM, exact vs NSGA-II çalışmasının **ana sahnesi** yapılabilir mi? v3'teki "3 amaçlı sepet + market" yerine ya da yanına.
2. Matsezgisel (GA + iç MILP), "GA tarafı" olarak kabul görür mü, yoksa saf NSGA-II mi bekler?
3. Öneri tarafında işbirlikçi filtrelemeyi hangi ölçekte anlamlı görür? Food.com tohumlu bir simülatörle regret ölçümü kabul mü? (Lisans: yalnız offline araştırma.)

**Doğrulanacaklar:**
- Migros ve A101 e-Arşiv faturalarında barkod ya da iç kod var mı: 3–5 gerçek fatura incelenmeli.
- TürKomp'a izin başvurusu (Türk jenerikleri için; 02-v2-fis-veri ile birlikte).
- van Rooijen 2024'ün tarif sayısı ve çözüm süresi; EvoMeal'in örnek boyutu. Ajanlar tam metinde bulamadı.
- Benchmark'ın gerçek veriyle tekrarı (katalog v0 + ilk 120 tarif). Sentetik üretecin israf oranı muhtemelen abartılı.
- "Fındık → ayçekirdeği" gibi ikame kurallarının bir alerji uzmanı ya da diyetisyence gözden geçirilmesi. Buradaki mantık tıbbi tavsiye değil.

---

## Kaynakça (seçme; hepsi metinde linkli)
**Tarif verisi ve besin hesabı:**
- TÜBER 2022 (Sağlık Bak. Yayın No 1031).
- Reinivuo ve ark. 2009 JFCA [doi:10.1016/j.jfca.2009.04.003](https://doi.org/10.1016/j.jfca.2009.04.003).
- USDA Retention Factors Rel. 6 (2007).
- USDA AH-102 (1975).
- Zhang ve ark. 2019 Nutrients [doi:10.3390/nu11010200](https://doi.org/10.3390/nu11010200).
- Lemay ve ark. 2026 J Nutr [doi:10.1016/j.tjnut.2026.101678](https://doi.org/10.1016/j.tjnut.2026.101678).
- Kopitar ve ark. 2025 Nutrients [doi:10.3390/nu17091492](https://doi.org/10.3390/nu17091492).
- Carrillo-Larco ve ark. 2026 J Nutr [doi:10.1016/j.tjnut.2026.101786](https://doi.org/10.1016/j.tjnut.2026.101786).
- Weisell & Dop 2012 [PubMed 23193766](https://pubmed.ncbi.nlm.nih.gov/23193766/).
- FSEK 5846 Ek m.8.

**LLM güvenliği ve alerji:**
- Niszczota & Rybicka 2023 [doi:10.1016/j.nut.2023.112076](https://doi.org/10.1016/j.nut.2023.112076).
- Mathes ve ark. 2025 [doi:10.1016/j.jaip.2025.03.030](https://doi.org/10.1016/j.jaip.2025.03.030).
- Vij ve ark. 2025 [arXiv 2502.02028](https://arxiv.org/abs/2502.02028).
- Correia & Feng 2026 [doi:10.1016/j.jfp.2026.100852](https://doi.org/10.1016/j.jfp.2026.100852).
- Fatemi ve ark. 2023 [arXiv 2302.07960](https://arxiv.org/abs/2302.07960).
- Fu ve ark. 2026 (CARE) [doi:10.3390/foods15101647](https://doi.org/10.3390/foods15101647).
- NutriOrion [arXiv 2602.18650](https://arxiv.org/abs/2602.18650).
- Peeters 2009 [doi](https://doi.org/10.1111/j.1398-9995.2008.01818.x).
- Brough 2020 [doi](https://doi.org/10.1016/j.jaci.2019.09.036).
- Santos ve ark. 2024 EAACI [doi:10.1111/all.16345](https://doi.org/10.1111/all.16345).
- Treffeisen 2024 [doi](https://doi.org/10.1016/j.jaip.2024.07.029).
- Shah 2026 [doi](https://doi.org/10.1016/j.jaip.2026.03.032).
- TGK Etiketleme Yönetmeliği (RG 26.01.2017, 29960 mük.).

**Menü optimizasyonu:**
- van Rooijen ve ark. 2024 [doi:10.1016/j.resconrec.2024.107559](https://doi.org/10.1016/j.resconrec.2024.107559).
- van Rooijen ve ark. 2025 [doi:10.1016/j.spc.2025.05.015](https://doi.org/10.1016/j.spc.2025.05.015).
- Hespanhol & Aswani 2018 [doi:10.23919/ACC.2018.8430885](https://doi.org/10.23919/ACC.2018.8430885).
- Şahin & Aytekin Şahin 2024 [doi:10.1016/j.eswa.2024.124213](https://doi.org/10.1016/j.eswa.2024.124213).
- Marrero ve ark. 2020 [doi:10.3390/math8111960](https://doi.org/10.3390/math8111960).
- Benvenuti & De Santis 2020 [doi:10.3389/fnut.2020.562833](https://doi.org/10.3389/fnut.2020.562833).
- Arriz-Jorquiera 2024 [doi:10.1016/j.wasman.2023.12.010](https://doi.org/10.1016/j.wasman.2023.12.010).
- Cooper ve ark. 2023 [doi:10.1016/j.resconrec.2023.106986](https://doi.org/10.1016/j.resconrec.2023.106986).
- Błażewicz ve ark. 2010 [doi:10.2478/v10006-010-0028-0](https://doi.org/10.2478/v10006-010-0028-0).
- Küçükoğlu 2025 [doi:10.1111/itor.70106](https://doi.org/10.1111/itor.70106).
- Okumuş & Küçükoğlu 2025 [doi:10.17482/uumfd.1571735](https://doi.org/10.17482/uumfd.1571735).
- Marin ve ark. [arXiv 2511.18483](https://arxiv.org/abs/2511.18483).
- Kahraman & Seven 2005 [doi:10.1145/1102256.1102345](https://doi.org/10.1145/1102256.1102345).
- Türkmenoğlu ve ark. 2021 [doi:10.1177/1460458220976719](https://doi.org/10.1177/1460458220976719).

**Kiler ve israf:**
- USDA FoodKeeper (data.gov, CC0).
- Bhagat ve ark. 2018 [doi:10.1145/3219819.3219891](https://doi.org/10.1145/3219819.3219891).
- Syntetos & Boylan 2005 [doi:10.1016/j.ijforecast.2004.10.001](https://doi.org/10.1016/j.ijforecast.2004.10.001).
- UNEP Food Waste Index 2021 ve 2024.
- Pekcan ve ark. 2006 (FAO).
- Reynolds ve ark. 2019 [doi:10.1016/j.foodpol.2019.01.009](https://doi.org/10.1016/j.foodpol.2019.01.009).
- Seta ve ark. 2026 [doi:10.31025/2611-4135/2026.19596](https://doi.org/10.31025/2611-4135/2026.19596).
- Dai 2024 [doi:10.3389/frai.2024.1442948](https://doi.org/10.3389/frai.2024.1442948).
- GİB e-Arşiv Teknik Kılavuzu v1.18.

**Öneri sistemi:**
- Bondevik ve ark. 2024 [doi:10.1016/j.eswa.2023.122166](https://doi.org/10.1016/j.eswa.2023.122166).
- Dong ve ark. 2026 [doi:10.2196/77726](https://doi.org/10.2196/77726).
- Chen ve ark. 2021 [doi:10.1145/3437963.3441816](https://doi.org/10.1145/3437963.3441816).
- HUMMUS 2023 [doi:10.1145/3604915.3609491](https://doi.org/10.1145/3604915.3609491).
- MOPI-HFRS 2025 [doi:10.1145/3690624.3709382](https://doi.org/10.1145/3690624.3709382).
- Wang & Wang 2026 [doi:10.3390/electronics15122628](https://doi.org/10.3390/electronics15122628).
- Harvey & Elsweiler 2015 [doi:10.1145/2792838.2796551](https://doi.org/10.1145/2792838.2796551).
- Kluver & Konstan 2014 [doi:10.1145/2645710.2645742](https://doi.org/10.1145/2645710.2645742).
- Ferrari Dacrema ve ark. 2019 [doi:10.1145/3298689.3347058](https://doi.org/10.1145/3298689.3347058).
- Calandrino ve ark. 2011 [doi:10.1109/SP.2011.40](https://doi.org/10.1109/SP.2011.40).
- Zhang ve ark. 2021 CCS [doi:10.1145/3460120.3484770](https://doi.org/10.1145/3460120.3484770).
- Garcin ve ark. 2014 [doi:10.1145/2645710.2645745](https://doi.org/10.1145/2645710.2645745).

**Doğrulama notu:** Yukarıdaki DOI'lerin tamamı 2026-09-24'te Crossref API'sinden ya da arXiv abs sayfasından başlık eşleşmesiyle kontrol edildi. Tam metnini ajanların okuduğu çalışmalar metinde belirtildi; diğerleri özet düzeyinde.
