# 03 · API sözleşmesi

> **Durum:** ÖNERİ (18 Kasım 2026). Makinece okunur sözleşme: [openapi.yaml](openapi.yaml) (OpenAPI 3.1).
> Mobil uygulama tiplerini bu dosyadan üretir; servis yanıtlarının bu şemaya uyduğu bir sözleşme testiyle denetlenir.

## 1. Uç noktalar

| Metot ve yol | Ne yapar | Not |
|---|---|---|
| `POST /v1/analyses` | Düzeltilmiş metin + besin değerleri + durum kimlikleri → durum başına sonuç | Durumsuz; gövde saklanmaz, loglanmaz |
| `GET /v1/conditions` | Desteklenen durumlar, etkin/taslak kural sayısı, kapsam notu, gereken besin alanları | Profil ekranı bunu kullanır |
| `GET /v1/version` | KB, kural, eşik, model ve servis sürümleri | Raporlar ve hata ayıklama için |
| `GET /healthz` | Servis ve bağımlılık durumu (PostgreSQL, Qdrant, LLM) | LLM kapalıysa `disabled`, servis yine `ok` |

## 2. Örnek

İstek:

```json
{
  "ingredients_text": "İçindekiler: buğday unu, şeker, glikoz şurubu, bitkisel yağ (palm), renklendirici (E102). Eser miktarda süt içerebilir.",
  "nutrition": {"basis": "per_100g", "sugars_g": 48, "salt_g": 0.3},
  "conditions": ["colyak", "diyabet"]
}
```

Yanıt (kısaltılmış):

```json
{
  "request_id": "0f6c…",
  "versions": {"service": "0.1.0", "kb": "a1b2c3d-5e6f…", "rules": "9c…", "thresholds": "77…", "embedding_model": null, "llm_model": null},
  "mentions": [
    {"id": "m1", "raw": "buğday unu", "normalized": "buğday unu", "kind": "ingredient", "expression_type": "food_raw_material",
     "match": {"concept_id": "en:wheat-flour", "concept_name_tr": "buğday unu", "method": "exact", "score": 1.0}, "allergen_group": "gluten"}
  ],
  "results": [
    {"condition_id": "colyak", "outcome": "NOT_SUITABLE", "outcome_label_tr": "Uygun değil",
     "reasons": [{"rule_id": "CEL-01", "rule_version": "1", "rule_type": "presence", "outcome": "NOT_SUITABLE",
                  "detail": "bulunan: buğday unu → buğday", "mention_ids": ["m1"],
                  "source": {"document": "Reg. (EU) No 1169/2011", "section": "Ek II madde 1", "source_type": "regulation"}}],
     "missing_inputs": [], "unknown_mentions": [],
     "coverage": {"active_rules": 4, "note_tr": "Gluten varlığı, 'içerebilir' uyarısı ve 'glutensiz' beyanı kontrol edilir."}},
    {"condition_id": "diyabet", "outcome": "CAUTION", "outcome_label_tr": "Dikkat", "reasons": ["…şekerler 48 g / 100 g…"]}
  ],
  "explanation": {"text_tr": "…", "generator": "template", "guard_passed": true},
  "disclaimer": "Bu bilgi tıbbi tavsiye değildir; teşhis ya da tedavi amacı taşımaz."
}
```

## 3. Sözleşme kuralları

1. **Belirsizlik hata değildir.** Tanınmayan ifade, eksik besin değeri ve kuralsız durum 200 yanıtında
   `UNVERIFIED` olarak döner; `missing_inputs` ve `unknown_mentions` nedenini söyler.
2. **Hatalar** RFC 9457 `application/problem+json`: 422 geçersiz alan, bilinmeyen durum kimliği ya da 8.000 karakteri
   aşan metin; 413 istek gövdesi 64 KB'tan büyük; 429 hız sınırı; 500 iç hata.
3. **Uydurma yok:** istemci etikette olmayan besin değerini göndermez; sunucu eksik değeri tahmin etmez.
4. **Sürüm:** yol başında `/v1`. Geriye uyumsuz değişiklik `/v2` açar; alan eklemek uyumlu sayılır.
5. **Sıralama:** `results`, isteğin `conditions` sırasındadır; istemci kartları önem sırasına göre kendisi dizer.
6. **Gizlilik:** servis loglarına yalnız `request_id`, süreler, ifade sayısı, yöntem dağılımı ve sürümler yazılır.
