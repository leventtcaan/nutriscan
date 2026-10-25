# NutriScan

Paketli gıdanın içindekiler listesini ve besin tablosunu, kullanıcının seçtiği sağlık durumları için kaynaklı kurallarla değerlendirir; sonucu gerekçesi, kaynağı, kapsamı ve belirsizliğiyle gösterir. CSE 491/492 bitirme projesi · Akdeniz Üniversitesi Bilgisayar Mühendisliği · Grup 9 · Danışman: Dr. Taha Yiğit Alkan

**Tek doğruluk kaynağı:** [docs/mimari-karar-belgesi.md](docs/mimari-karar-belgesi.md). Güncel kapsam, kararlar ve uygulama durumu oradadır.

## V1 kapsamı

- Tek etiket başvurusu OCR ile okunur, kullanıcı metni düzeltebilir ve değerlendirme istek içinde yapılır.
- Ürün kataloğu, saklanan tarama geçmişi ve aynı kategoride alternatif ürün önerileri v1 kapsamında değildir.
- Hedef, etiketten kaynaklı kuralla değerlendirilebilen sağlık durumlarını kapsamak; kuralın olmadığı veya verinin yetmediği yerde **Doğrulanamadı** demektir. İlk kaynaklı kural tablosuna girecek sağlık durumlarının listesi 4. toplantı sonrası netleştirilecektir.
- Depodaki güncel kural dosyasında 17 satır ve 7 sağlık durumu bulunur. Bu, mevcut veri kapsamıdır; hedef kapsamla karıştırılmamalıdır.

## Hedeflenen mimari akış

```
etiket → OCR + kullanıcı düzeltmesi → böl + türle → sözlük/eşleme → kural tablosu → sonuç + kaynak + kapsam → açıklama
```

OFF taksonomisinde bulunmayan Türkçe eşanlamlılar, gıda ve kimyasal terimler embedding edilerek Qdrant'ta vektör aramasıyla eşleşme adayları bulunur. Adayı doğrulama ve kanonik kavrama bağlama yöntemi 4. toplantıda açık iş olarak bırakılmıştır; Qdrant sağlık sonucu vermez. Bu adım henüz kodda uygulanmamıştır. AI/araçlar kaynaklı kural araştırması ve taslağına yardım edebilir; her kural satırı iki ekip üyesince bağımsız doğrulanmadan etkinleştirilmez. Sonucu yalnız gözden geçirilmiş kural tablosu belirler; LLM sonucu değiştiremez.

## Repodaki mevcut uygulama

- `service/nutriscan/text.py`: etiket metnini ayırma ve normalize etme.
- `service/nutriscan/matcher.py`: E-kodu, birebir, Türkçe çoğul ve bulanık eşleşme.
- `service/nutriscan/rules.py`: CSV kural tablosuyla sonuç üretme.
- `service/run_labels.py`: etiket CSV'sinden Markdown raporu üretme.
- FastAPI uç noktası, mobil uygulama, Qdrant adımı ve LLM anlatım katmanı henüz bu repoda uygulanmış değildir; bunlar mimari plandaki sonraki parçalardır.

## Klasörler

| Klasör | İçerik | Sahibi |
|---|---|---|
| `docs/` | Karar belgesi, araştırma notları | Levent (editör) |
| `data/sozluk/` | Kavramlar ve eşanlamlılar | Ozan |
| `data/kurallar/` | Kural tablosu ve kanıt haritası | Hilal |
| `data/kanit/` | CTD/JECFA çıkarımları, yalnız bilgi | Hilal |
| `tests/` | Eşleme ve kural değerlendirme dosyaları | Hep birlikte |
| `service/` | Etiket işleme, eşleme ve kural prototipi | Levent |
| `app/` | Planlanan Expo mobil uygulaması | Ozan |
| `toplanti/` | Tarihli toplantı kayıtları ve hazırlıklar; güncel karar belgesi esas alınır | — |
| `plan/proposal/` | 18 Ekim hedefi için hazırlanmış tarihsel proposal v1 taslağı | — |
| `kaynak/` | Ders şablonları (değiştirilmez) | — |

## Kural hazırlığı ve güvence

AI veya ilgili araçlar, resmî mevzuat ve klinik kılavuzlardan kaynak konumu belirtilmiş aday kural satırları çıkarmada kullanılabilir. Eşik, kapsam ve istisnalar kaynaktan kontrol edilir; iki ekip üyesi bağımsız onaylamadan hiçbir satır `data/kurallar/` içine alınmaz. Kullanıcıya yönelik karar deterministik, onaylı kural tablosundan gelir.

Önceki yönün (hane planlama) belgeleri `arsiv/eski-yon-2026-10` etiketinde durur: `git checkout arsiv/eski-yon-2026-10`.
