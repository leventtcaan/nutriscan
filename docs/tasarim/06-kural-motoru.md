# 06 · Kural motoru (C6)

> **Durum:** ÖNERİ (18 Kasım 2026). K5, K6, K13 ve AGENTS.md kırmızı çizgi 1–4'ü çalışan değişmezlere çevirir.
> Denetimdeki A1–A7 ve B1–B2 bulgularının düzeltmesi burada tanımlanır.

## 1. Girdi ve çıktı

```
evaluate(mentions, may_contain, claims, nutrition, conditions, kb) -> ConditionResult[]
```

Motor saf bir fonksiyondur: ağ, saat, rastgelelik yok. Aynı girdi + aynı `kb` sürümü → aynı çıktı (NFR-1).

## 2. Değişmezler (invariants): kod düzeyinde zorlanır, CI'da test edilir

| # | Değişmez | Neden | Denetim |
|---|---|---|---|
| D1 | Yalnız `etkin` satırlar yüklenir; taslak satır ürün modunda hiçbir sonucu etkilemez | K6 | B1, B2 |
| D2 | Tanınan içerik sayısı 0 ise (boş, yalnız gürültü, hepsi tanınmayan) hiçbir durum "Engel bulunmadı" olamaz | Kırmızı çizgi 3 | A1 |
| D3 | Bir durumda tanınmayan ya da belirsiz (`ambiguous`, `abstain`) ifade varsa ve o durumun `varlik` satırı varsa sonuç "Engel bulunmadı" olamaz → "Doğrulanamadı" | Kırmızı çizgi 3 | — (bugün de var) |
| D4 | "İçerebilir" ifadesi varken, durumun `icerebilir` satırı yoksa ve o ifade durumun `varlik` hedeflerinden birine eşleşiyorsa sonuç "Engel bulunmadı" olamaz → "Dikkat" | Kırmızı çizgi 3 | A2 |
| D5 | Etkin satırı olmayan durum → "Doğrulanamadı" + kapsam notu | FR-13 | — |
| D6 | Sonuç, tetiklenen satırların en ağır olanıdır: Uygun değil > Dikkat > Doğrulanamadı > Engel bulunmadı | K5 | — |
| D7 | Miktar karşılaştırmaları ham değerle yapılır (yuvarlama yok); türetilen alan `derived_field` tablosundan | — | A7 |
| D8 | Olumsuz beyan (`negated = true`) beyan kuralını tetiklemez | — | A6 |
| D9 | Muafiyet alt bileşenlere de uygulanır: "glikoz şurubu (buğday)" muaf kavramın altındaki "buğday" ayrıca tetiklemez | Kuralın amacı (1169/2011 Ek II) | A11 |
| D10 | LLM, kanıt (CTD/JECFA) ve anlamsal puan sonucu değiştirmez; motorun girdisi değildir | K5, K13 | — |

**Özellik testi (property test):** rastgele bir etikete rastgele tanınmayan ifade eklendiğinde hiçbir durumun sonucu
daha az ağır bir sınıfa geçmez. Bu tek test D2–D4'ün ruhunu (belirsizlik yalnız riski artırır) toptan yakalar.

## 3. Değerlendirme algoritması

```
for durum in istenen_durumlar:
    satirlar = kb.etkin_satirlar(durum)
    if not satirlar: sonuc(durum) = DOGRULANAMADI + kapsam notu            # D5
    tetiklenen = []
    # 1. geçiş: bagimlilik'i olmayan satırlar · 2. geçiş: varsayilan ve bagimlilik'li satırlar ([04 §3](04-veri-modeli.md))
    for satir in iki_geçiş(satirlar):
        varlik     → hedef ∩ (kavram ∪ üst_kavramlar) ≠ ∅, muaflar hariç (alt bileşen dahil, D9)
        icerebilir → aynı test, yalnız may_contain ifadelerinde
        beyan      → claims içinde code == hedef ve not negated (D8)
        miktar     → değer = nutrition[hedef] ya da türetilen; yoksa atla (eksik_veri ele alır)
                     bant = bantlar[her_ikisi] ya da bantlar[sivi if basis == per_100ml else kati];
                     ilk "değer ≤ sınır" adımı; son adım ">" (D7)
        eksik_veri → nutrition[hedef] yoksa tetiklenir, missing_inputs += hedef
        varsayilan → bagimlilik'teki satırların hiçbiri tetiklenmediyse
    sonuc = en_agir(tetiklenen)                                              # D6
    uygula D2, D3, D4 → gerekirse "uncertainty" gerekçesiyle yükselt
```

Her tetiklenen satır yanıtta bir `Reason` olur: `rule_id`, `rule_version`, `rule_type`, `detail` (örn. "bulunan:
buğday unu → buğday"), `mention_ids` ve `source` (belge, bölüm, tür, URL). D2–D4 ile yapılan yükseltmeler de
`rule_type = uncertainty` gerekçesiyle görünür; kaynağı "AGENTS.md kırmızı çizgi 3" olarak yazılır (bugün yanlışlıkla
"Karar belgesi ilke 3" yazıyor).

## 4. Kural tablosunun bugünkü durumu ve M0 düzeltmeleri

Bu düzeltmeler **veri** değişikliğidir ve iki kişilik inceleme kuralına tabidir. Yazan Hilal (kural sahibi), inceleyen
iki kişi. Motor tarafındaki D1–D10 ise koddur; yazan Levent (kural motoru, TÜBİTAK İP4).

| Satır | Sorun | Önerilen değişiklik | Kaynak kontrolü |
|---|---|---|---|
| Tümü (17) | İncelenmemiş | `durum_satir = taslak`; inceleme takvimi M0–M1 | — |
| LAK-01 | Hedef dar (tereyağı, peynir, kazein, kefir, dondurma kaçıyor) | Hedefe süt ve süt ürünü kavram zinciri; OFF hiyerarşisinden kontrol | 1169/2011 Ek II md. 7 (süt ve süt ürünleri) |
| LAK, SUL | `icerebilir` satırı yok | LAK-03 ve SUL-03 `icerebilir` → Dikkat | Ekip kararı (ihtiyati), CEL-02 ile tutarlı |
| SUL-01 | `en:sulfite` hedefte değil | Ekle | 1169/2011 Ek II md. 12 |
| SUL-02, LAK-02 | "Beyan yok" → Engel bulunmadı | Kaynak türü `ekip_karari` olarak işaretle; D2 ve D4 bu satırların yanlış güvence vermesini engeller | — |
| CKD-02 | Kaynak yer tutucu | Kaynak bulunana kadar `taslak` | KDIGO 2024 bölümü aranacak |
| DM-01 | "Düşük şeker" beyan eşiği klinik eşik gibi kullanılıyor | Açıklamada "beyan sınırı" diye ayrı göster (`kaynak_turu = mevzuat`); risk tablosundaki madde | 1924/2006 Ek |
| CEL-04, PKU-02 | Kaynağı ekip kararı olan varsayılanlar | `kaynak_turu = ekip_karari`; uygulamada ayrı etiket | — |

## 5. Sağlık durumu listesi (Ö-05)

K2 listeyi "30 Ekim toplantısında netleşecek" diye bırakmıştı; kayıt yok. Öneri: **mevcut 7 durum v1 listesidir**
(çölyak, diyabet, kronik böbrek hastalığı, hipertansiyon, laktoz intoleransı, fenilketonüri, sülfit hassasiyeti).
Her birinin etiketten kontrol edilebilir bir ölçütü ve doğrulanmış bir kaynağı var. Yeni durum eklemenin tek yolu
satır eklemektir: `durumlar.csv` + en az bir etkin kural + kaynak kaydı. Astım listede **yoktur**; sülfit hassasiyeti
aracılığıyla ilgili etiket bilgisi zaten kapsanır. TÜBİTAK İP1 listeyi "belirlenen ölçütlere göre" kesinleştirir ve bu
öneri o ölçütlerin ilk uygulamasıdır.

## 6. Testler

- Her kural türü × her durum için en az bir pozitif, bir negatif test.
- A1–A8 için **regresyon testleri** (girdi, beklenen sonuç tam olarak denetim tablosundaki gibi).
- D1–D10 için birer test; özellik testi (§2).
- Senaryo testleri ([09 §5](09-degerlendirme-protokolu.md)): beklenen sonuç, sistem çalıştırılmadan önce kaynağa
  dayanılarak yazılır.
