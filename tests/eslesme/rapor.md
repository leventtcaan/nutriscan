# Eşleme ve kural raporu — 3 etiket

Toplam ifade: **20** · E-kodu: 4 · birebir: 9 · bulanık: 0 · fonksiyon adı: 4 · **tanınmayan: 3** (%15)

**Tanınmayan ifadeler (Türkçeleştirme listesi):** mısır unu, pirinç unu, aroma verici

## Örnek bisküvi (diyagramdaki) *(örnek etiket)*

> İçindekiler: buğday unu, şeker, glikoz şurubu, bitkisel yağ (palm), renklendirici (E102). Eser miktarda süt içerebilir.

| Etiketteki ifade | Eşleşen kavram | Yöntem |
|---|---|---|
| buğday unu | buğday unu `en:wheat-flour` | exact |
| şeker | Şeker `en:sugar` | exact |
| glikoz şurubu | glikoz şurubu `en:glucose-syrup` | exact |
| bitkisel yağ | Bitkisel yağ `en:vegetable-oil` | exact |
| palm | palm `en:palm` | exact |
| renklendirici | — `` | function_label |
| E102 | Tartrazin `E102` | e_code |
| süt *(içerebilir)* | Süt `en:milk` | exact |

| Durum | Sonuç | Neden | Kaynak |
|---|---|---|---|
| Çölyak | **Uygun değil** | CEL-01: Gluten içeren tahıl ya da ondan yapılmış içerik var (bulunan: buğday unu) | Reg. (EU) 1169/2011 Ek II madde 1 (gluten içeren tahıllar ve muafiyetler); TGK Gıda Etiketleme Yönetmeliği (RG 29960) alerjen eki |
| Diyabet | **Dikkat** | DM-01: sekerler 48.0 g / 100 g (sınırın üstünde) | Reg. (EC) No 1924/2006 Ek (SUGARS-FREE; LOW SUGARS); TGK Beslenme ve Sağlık Beyanları Yönetmeliği (RG 29960) Ek-1 |
| Kronik böbrek hastalığı | **Engel bulunmadı** | CKD-01: sodyum 0.12 g / 100 g (≤ 0.12) | Reg. (EC) No 1924/2006 Ek (LOW / VERY LOW SODIUM/SALT); Reg. (EU) 1169/2011 Ek I (tuz = sodyum × 2,5); KDIGO 2024 (bağlam: sodyum < 2 g/gün) |

## Örnek glutensiz kraker *(örnek etiket)*

> İçindekiler: mısır unu, pirinç unu, ayçiçek yağı, tuz, kabartıcı (E500). Glutensiz.

| Etiketteki ifade | Eşleşen kavram | Yöntem |
|---|---|---|
| mısır unu | — `` | unknown |
| pirinç unu | — `` | unknown |
| ayçiçek yağı | Ayçiçek yağı `en:sunflower-oil` | exact |
| tuz | tuz `en:salt` | exact |
| kabartıcı | — `` | function_label |
| E500 | E500(iii) `E500` | e_code |

| Durum | Sonuç | Neden | Kaynak |
|---|---|---|---|
| Çölyak | **Doğrulanamadı** | CEL-03: Gluten kaynağı yok ve etikette 'glutensiz' beyanı var (≤ 20 mg/kg) (beyan: glutensiz); -: tanınmayan içerik: mısır unu, pirinç unu | Karar belgesi ilke 3; Reg. (EU) No 828/2014 ('gluten-free' ≤ 20 mg/kg) |
| Diyabet | **Engel bulunmadı** | DM-01: sekerler 2.1 g / 100 g (≤ 5.0) | Reg. (EC) No 1924/2006 Ek (SUGARS-FREE; LOW SUGARS); TGK Beslenme ve Sağlık Beyanları Yönetmeliği (RG 29960) Ek-1 |
| Kronik böbrek hastalığı | **Dikkat** | CKD-01: sodyum 0.56 g / 100 g (sınırın üstünde) | Reg. (EC) No 1924/2006 Ek (LOW / VERY LOW SODIUM/SALT); Reg. (EU) 1169/2011 Ek I (tuz = sodyum × 2,5); KDIGO 2024 (bağlam: sodyum < 2 g/gün) |

## Örnek şekerli içecek *(örnek etiket)*

> İçindekiler: su, şeker, asitlik düzenleyici (E330), aroma verici, renklendirici (E150d).

| Etiketteki ifade | Eşleşen kavram | Yöntem |
|---|---|---|
| su | Su `en:water` | exact |
| şeker | Şeker `en:sugar` | exact |
| asitlik düzenleyici | — `` | function_label |
| E330 | sitrik asit `E330` | e_code |
| aroma verici | — `` | unknown |
| renklendirici | — `` | function_label |
| E150d | Sülfit amonyak karamel `E150D` | e_code |

| Durum | Sonuç | Neden | Kaynak |
|---|---|---|---|
| Çölyak | **Dikkat** | CEL-04: Gluten kaynağı görünmüyor ama 'glutensiz' beyanı yok; çapraz bulaşma bilinmiyor (varsayılan) | Ekip kararı (belirsizlik riski yalnız artırır) |
| Diyabet | **Dikkat** | DM-01: sekerler 11.0 g / 100 ml (sınırın üstünde) | Reg. (EC) No 1924/2006 Ek (SUGARS-FREE; LOW SUGARS); TGK Beslenme ve Sağlık Beyanları Yönetmeliği (RG 29960) Ek-1 |
| Kronik böbrek hastalığı | **Doğrulanamadı** | CKD-03: besin tablosu gerekli → kullanıcıdan istenir | Ekip kararı (K5 eksik veri) |

