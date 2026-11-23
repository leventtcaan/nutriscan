# 09 · Değerlendirme protokolü (eşleme sınavı + kural sınavı)

> **Durum:** ÖNERİ (18 Kasım 2026). TÜBİTAK 2.2, 2.4 ve 2.6'yı ve K9'u çalıştırılabilir bir protokole çevirir.
> Bu belge, TÜBİTAK İP1'in "deney protokolü" çıktısının ilk sürümüdür. Kod: `eval/`.

## 1. İki katman (Ö-01)

| | Eşleme sınavı | Kural sınavı |
|---|---|---|
| **CSE 491 finali** (~18 Aralık) | 100 ifade, iki etiketleyici | 20 ürün × durum senaryosu |
| **TÜBİTAK / CSE 492** | ≥ 400 ifade, kappa raporu, 30/70 geliştirme/test | ≥ 40 senaryo |

İlk katmanın 100 ifadesi ve 20 senaryosu ikinci katmanın **geliştirme kümesine** girer; biçim aynıdır.

## 2. Veri kümesi ve ayrım

**Kaynaklar**
- **Ön çalışma kümesi:** 60 OFF ürününden 894 ifade. Ekip çevirilerinin 65'i bu etiketlerden türetildi (denetim B4).
  Bu yüzden bu küme **yalnız geliştirme** amacıyla kullanılır; test kümesine hiçbir ifadesi giremez.
- **Saha kümesi:** Antalya'da 10 satış noktasında, ürün satın alınmadan fotoğraflanan ambalajlar (TÜBİTAK 2.2).
  Test kümesi yalnız buradan çekilir. Fotoğraf çekmeden önce mağaza yönetiminden izin alınır.

**Tabakalar** (her ifade bir tabakaya girer; tabaka etiketlemeden önce, ham metne bakılarak atanır):
`tr_ad` (Türkçe bileşen adı) · `e_kodu` · `bilesik` (parantezli/sınıf: madde) · `ingilizce` · `ocr_hatali` ·
`sozluk_disi_aday` (ön kontrolde taban yöntemin bulamadığı).

Son tabaka, hibrit yöntemin etkisinin ölçülebilmesi için **fazla örneklenir**. TÜBİTAK 2.2'deki taahhüt bu:
hibrit yalnız taban yöntemin eşleştiremediği ifadelerde devreye girer.

**TÜBİTAK'tan sapma (Ö-12):** TÜBİTAK 2.2 ön çalışma örneklemini ve saha fotoğraflarını tek kümede birleştirip 30/70'i
bütüne uygular. Bu protokol, sızıntıyı önlemek için ön çalışma ifadelerini yalnız geliştirmeye koyar. Sonuç: toplam ≥ 400
ifade ve %70 test için **en az 280 saha ifadesi** test kümesine gerekir. Sapma danışman onayı ister; onaylanmazsa TÜBİTAK
planı uygulanır ve ekip çevirilerinden türetilmiş ifadeler raporda ayrıca işaretlenir.

**CSE 491 finali için:** saha toplama M2'de başlar. 100 ifadelik sınavın test kısmına yetecek saha ifadesi yoksa sınav
"geliştirme kümesinde kuru koşu" diye adlandırılır ve genelleme iddiası taşımaz.

**Ayrım:** saha kümesinde tabaka başına %30 geliştirme, %70 test. Ayrım sabit bir tohumla (`seed`) yapılır.
`eval/splits/{dev,test}.jsonl` dosyaları ve SHA-256 karmaları commit'lenir; bu karmalar değerlendirme raporlarında
yazılır. Test dosyasının karması değişirse değerlendirme betiği çalışmaz.

## 3. Etiketleme

**Kayıt biçimi** (`eval/data/ifadeler.jsonl`, satır başına bir ifade):

```json
{"id": "s-0412", "raw": "glikoz şurubu (buğday)", "label_source": "saha:antalya-03", "stratum": "bilesik",
 "annotator_1": {"concept_id": "en:wheat-glucose-syrup", "status": "eslesti", "note": ""},
 "annotator_2": {"concept_id": "en:wheat-glucose-syrup", "status": "eslesti", "note": ""},
 "gold": {"concept_id": "en:wheat-glucose-syrup", "status": "eslesti", "resolution": "uyum"}}
```

`status` değerleri: `eslesti` · `taksonomide_yok` · `belirsiz`.

**Kılavuz** (`eval/kilavuz.md`, İP1 çıktısı): kimyasala inme kuralı (K4), karışımlar, köken bilgisi ("(buğday)"),
yazım hataları, ne zaman "belirsiz" deneceği. Kılavuz önce geliştirme kümesinin küçük bir parçasında (öneri: 50 ifade)
denenir, sonra dondurulur.

**Uyum:** iki etiketleyici birbirini görmeden etiketler. Cohen kappa, `status` ve `concept_id` birleşik etiketi
üzerinden hesaplanır; hedef ≥ 0,80. Değer **düzeltme yapılmadan** raporlanır. Uyuşmazlıklar gerekçesiyle
`gold.resolution` alanına yazılır.

**Kim:** TÜBİTAK İP2 tüm ekibi sayar ve uyuşmazlıkların "uzlaştırılması"nı ister. Öneri: her ifadeyi iki farklı üye
etiketler, uzlaşma olmazsa üçüncü üye hakemdir.

## 4. Metrikler (eşleme sınavı)

Her yöntem (A, B) için test kümesinde, `gold.status ∈ {eslesti, taksonomide_yok}` olan N ifade üzerinden. **Doğru**
cevabın tanımı: `eslesti` ifadede gold kavramın kabulü; `taksonomide_yok` ifadede çekimser kalmak (`abstain`/`unknown`).
`belirsiz` gold ifadeler metriklere girmez, ayrı tabloda sayılır.

| Metrik | Tanım |
|---|---|
| İlk aday doğruluğu | yukarıdaki tanıma göre doğru cevap / N |
| Kapsama | kavram kabul edilen ifade / N |
| Kabul edilenlerde isabet | doğru kabul / kabul edilen |
| **Yanlış kabul oranı** | (`eslesti` ifadede yanlış kavram kabulü + `taksonomide_yok` ifadede herhangi bir kavram kabulü) / N (H2'nin konusu) |
| Çekimserlik | `abstain` + `unknown` / N |
| Recall@5 | gold kavram ilk 5 aday içinde / N (yalnız B için anlamlı; A için bulanık eşleşmenin ilk 5'i) |

Tüm oranlar Wilson %95 güven aralığıyla verilir. Raporda alt tabaka tabloları vardır; örnek sayısı yetersiz alt gruplar
(öneri eşik: 30) yalnız betimsel olarak verilir. Eşik ön kayıtta sabitlenir.

**İstatistik**
- **H1** (hibrit doğruluğu artırır): aynı ifadeler üzerinde 2×2 tablo (A doğru/yanlış × B doğru/yanlış),
  **kesin McNemar testi** (uyuşmayan çiftler üzerinde iki yanlı binom testi). Uygulama standart kütüphaneyle
  (`math.comb`) yazılır, `scipy` ile çapraz kontrol edilir.
- **H2** (yanlış kabul kabul edilebilir sınırı aşmaz): fark `FA_B − FA_A` ve eşleştirilmiş fark için güven aralığı;
  aralığın üst sınırı önceden belirlenmiş **Δ** sınırının altındaysa H2 desteklenir. **Δ'nın sayısal değeri
  açıktır** (Ö-09) ve test çalıştırılmadan önce bu dosyaya ve commit'e yazılmalıdır.
- **Önceden kayıt:** H1, H2, Δ, metrikler, eşikler (`esikler.toml`) ve ayrım karmaları test çalıştırılmadan önce
  tek bir commit'te dondurulur (`eval/onkayit.md`). Bu, sonuca bakıp eşik değiştirme riskini kapatır.

## 5. Kural sınavı (senaryolar)

**Biçim** (`eval/senaryolar/*.yaml`):

```yaml
id: SC-007
urun: "bisküvi (saha:antalya-01, foto 0034)"
icindekiler: "buğday unu, şeker, glikoz şurubu, bitkisel yağ (palm), renklendirici (E102). Eser miktarda süt içerebilir."
besin: {basis: per_100g, sugars_g: 48, salt_g: 0.3}
beklenen:
  colyak:             {sonuc: Uygun değil, gerekce: "buğday unu → buğday", kaynak: "1169/2011 Ek II md.1"}
  diyabet:            {sonuc: Dikkat,      gerekce: "şekerler 48 g > 5 g",  kaynak: "1924/2006 Ek"}
  laktoz_intoleransi: {sonuc: Dikkat,      gerekce: "süt içerebilir",       kaynak: "ekip kararı (LAK-03)"}
yazan: Hilal
kontrol_eden: Ozan
yazildi: 2026-12-02
```

- Beklenen sonuç **sistem çalıştırılmadan önce**, kaynağa dayanılarak yazılır ve iki kişi kontrol eder.
- Metrikler: **kaçırılan uyarı** (beklenen Uygun değil/Dikkat, sistem daha hafif; en kritik), **gereksiz uyarı**
  (beklenen daha hafif, sistem daha ağır), **Doğrulanamadı oranı**, tam eşleşme oranı.
- Senaryo seti, denetimdeki A1–A8 kenar durumlarını içerir (boş etiket, noktasız "içerebilir", olumsuz beyan…).

## 6. Çıktı ve tekrarlanabilirlik

`python -m eval run --method A|B --split test` komutu, `eval/raporlar/<tarih>-<yöntem>.json` ve `.md` üretir.
Raporun başında `versions` (KB, kurallar, eşikler, model), ayrım karmaları ve komut satırı bulunur. İki çalıştırma
aynı sürümlerle aynı sayıyı verir (NFR-1).
