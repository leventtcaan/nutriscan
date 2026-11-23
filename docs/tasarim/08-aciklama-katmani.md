# 08 · Açıklama katmanı (C8, LLM)

> **Durum:** ÖNERİ (18 Kasım 2026). K11'i uygular. Sağlayıcı ve model seçimi açık (Ö-08); bu belge sağlayıcıdan
> bağımsız bir arayüz tanımlar.

## 1. Görev ve sınır

LLM tek bir iş yapar: kural motorunun **yapılandırılmış** sonucunu kısa, sade bir Türkçe paragrafa çevirmek. Sonucu
değiştiremez, yeni sağlık iddiası ekleyemez, teşhis koyamaz (K11, kırmızı çizgi 1–2). Rozet her zaman API'nin
`outcome` alanından çizilir, açıklama metninden çizilmez ([07 §4](07-mobil-uygulama.md)).

## 2. Akış

```mermaid
flowchart LR
  R[ConditionResult[]<br/>+ kural açıklamaları<br/>+ kaynak adları] --> P[İstem şablonu<br/>sürümlü dosya]
  P --> L[LLM<br/>zaman aşımı 2 sn]
  L --> G{Denetim}
  G -- geçti --> OK[generator = llm]
  G -- kaldı / hata / zaman aşımı --> T[Şablon metin<br/>generator = template]
```

- **Girdi:** yalnız yapılandırılmış alanlar: durum adı, sonuç etiketi, tetiklenen kuralların `aciklama_tr` metni,
  eşleşen ifadelerin kavram adları, kaynak belge adları, `missing_inputs`. **Ham etiket metni ve profil gönderilmez**;
  durum adları istekte zaten vardır ama kullanıcı kimliğiyle ilişkilendirilmez.
- **İstem şablonu:** `service/nutriscan/explain/prompts/aciklama_v1.md`. Sürümü yanıttaki `versions.explanation_prompt`
  alanına, model adı `versions.llm_model` alanına yazılır.
- **Gizlilik:** durum adları üçüncü taraf bir sağlayıcıya gittiği için sağlayıcıda istek saklamama ve eğitimde kullanmama
  koşulu aranır (Ö-08); koşul sağlanamazsa yalnız şablon açıklayıcı kullanılır.

## 3. Denetim (guard) kuralları

Denetimden geçmeyen metin kullanıcıya gösterilmez; şablon kullanılır. Kurallar deterministik koddur:

1. **Sonuç sadakati:** metinde geçen her durum için sonuç etiketi, `outcome_label_tr` ile birebir aynı. Denetim önce dört
   sonuç etiketini metinden çıkarır, sonra kalan metinde başka bir sonuç ifadesi ("sorun yok", "uygundur" gibi eşanlamlılar)
   arar; böylece "Uygun değil" etiketi kendi kendini yakalamaz.
2. **Yasaklı dil:** `güvenli`, `zararlı`, `tetikler`, `tedavi`, `önler`, `iyileştirir`, `teşhis` ve
   `data/sozluk/yasakli_ifadeler.toml`'daki liste. Sabit yasal bilgilendirme cümlesi izin listesindedir ve LLM metnine eklenmez.
3. **Kapsam:** metinde adı geçen içerik ve durumlar girdide olanlarla sınırlı (sözlükten ad çıkarımıyla kontrol).
4. **Sayı uydurmama:** metindeki her sayı girdide var (besin değeri, eşik).
5. **Uzunluk:** ≤ 600 karakter (öneri değer; M3'te ekran testine göre ayarlanır).

Değerlendirmede bütün test senaryolarının açıklamaları bu denetimden geçirilir ve geçme oranı raporlanır (NFR-5).

## 4. Şablon metin

Şablonlar `service/nutriscan/explain/templates/*.tr.txt` dosyalarındadır, durum × sonuç × gerekçe türüne göre
seçilir. Örnek (çölyak, Uygun değil, varlık): *"Çölyak için: **Uygun değil**. Etikette {ifade} var; bu, gluten içeren
bir tahıldır ({kaynak}). Bu bir sağlık tavsiyesi değildir."* Şablonlar uygulamanın LLM'siz de tam çalışmasını sağlar
(K11); demo internet olmadan da yapılabilir.

## 5. Sağlayıcı arayüzü

```python
class Explainer(Protocol):
    def explain(self, results: list[ConditionResult], timeout_s: float) -> Explanation: ...
```

Uygulamalar: `TemplateExplainer` (varsayılan, her zaman var) ve `LlmExplainer` (Ö-08 kararından sonra). Anahtar
yalnız ortam değişkeninden okunur (`NUTRISCAN_LLM_API_KEY`), loglanmaz. LLM kapalıyken `/healthz` `llm: disabled`
döner ve servis tam çalışır.

## 6. Kaynak araştırmasında LLM (K11, K13)

Kural *taslağı* hazırlarken LLM kullanılabilir. Kural: LLM'in önerdiği her satır `yazan` alanında insan adıyla,
`not` alanında "LLM taslağı, kaynak elle doğrulandı" notuyla girer; kaynak bölümü insan tarafından açılıp okunmadan
satır PR'a giremez. Bu, çalışma zamanından ayrı ve PR incelemesine tabi bir süreçtir.
