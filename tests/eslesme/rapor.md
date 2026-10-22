# Eşleme ve kural raporu — 3 etiket

Toplam ifade: **20** · E-kodu: 4 · birebir: 16 · çoğul: 0 · gürültü: 0 · bulanık: 0 · fonksiyon adı: 0 · **tanınmayan: 0** (%0)

## Örnek bisküvi (diyagramdaki) *(örnek etiket)*

> İçindekiler: buğday unu, şeker, glikoz şurubu, bitkisel yağ (palm), renklendirici (E102). Eser miktarda süt içerebilir.

| Etiketteki ifade | Eşleşen kavram | Yöntem |
|---|---|---|
| buğday unu | buğday unu `en:wheat-flour` | exact |
| şeker | Şeker `en:sugar` | exact |
| glikoz şurubu | glikoz şurubu `en:glucose-syrup` | exact |
| bitkisel yağ | Bitkisel yağ `en:vegetable-oil` | exact |
| palm | palm `en:palm` | exact |
| renklendirici | Colour `en:colour` | exact |
| E102 | Tartrazin `E102` | e_code |
| süt *(içerebilir)* | Süt `en:milk` | exact |

| Durum | Sonuç | Neden | Kaynak |
|---|---|---|---|
| Çölyak | **Uygun değil** | CEL-01: Gluten ya da gluten içeren tahıldan yapılmış içerik var (bulunan: buğday unu) | Reg. (EU) 1169/2011 Ek II madde 1 (gluten içeren tahıllar ve muafiyetler); TGK Gıda Etiketleme Yönetmeliği (RG 29960) alerjen eki |
| Diyabet | **Dikkat** | DM-01: sekerler 48.0 g / 100 g (sınırın üstünde) | Reg. (EC) No 1924/2006 Ek (SUGARS-FREE; LOW SUGARS); TGK Beslenme ve Sağlık Beyanları Yönetmeliği (RG 29960) Ek-1 |
| Kronik böbrek hastalığı | **Engel bulunmadı** | CKD-01: sodyum 0.12 g / 100 g (≤ 0.12) | Reg. (EC) No 1924/2006 Ek (LOW / VERY LOW SODIUM/SALT); Reg. (EU) 1169/2011 Ek I (tuz = sodyum × 2,5); KDIGO 2024 (bağlam: sodyum < 2 g/gün) |

## Örnek glutensiz kraker *(örnek etiket)*

> İçindekiler: mısır unu, pirinç unu, ayçiçek yağı, tuz, kabartıcı (E500). Glutensiz.

| Etiketteki ifade | Eşleşen kavram | Yöntem |
|---|---|---|
| mısır unu | corn flour `en:corn-flour` | exact |
| pirinç unu | rice flour `en:rice-flour` | exact |
| ayçiçek yağı | Ayçiçek yağı `en:sunflower-oil` | exact |
| tuz | tuz `en:salt` | exact |
| kabartıcı | Kabartma ajanı `en:raising-agent` | exact |
| E500 | Sodium carbonates `E500` | e_code |

| Durum | Sonuç | Neden | Kaynak |
|---|---|---|---|
| Çölyak | **Engel bulunmadı** | CEL-03: Gluten kaynağı yok ve etikette 'glutensiz' beyanı var (≤ 20 mg/kg) (beyan: glutensiz) | Reg. (EU) No 828/2014 ('gluten-free' ≤ 20 mg/kg) |
| Diyabet | **Engel bulunmadı** | DM-01: sekerler 2.1 g / 100 g (≤ 5.0) | Reg. (EC) No 1924/2006 Ek (SUGARS-FREE; LOW SUGARS); TGK Beslenme ve Sağlık Beyanları Yönetmeliği (RG 29960) Ek-1 |
| Kronik böbrek hastalığı | **Dikkat** | CKD-01: sodyum 0.56 g / 100 g (sınırın üstünde) | Reg. (EC) No 1924/2006 Ek (LOW / VERY LOW SODIUM/SALT); Reg. (EU) 1169/2011 Ek I (tuz = sodyum × 2,5); KDIGO 2024 (bağlam: sodyum < 2 g/gün) |

## Örnek şekerli içecek *(örnek etiket)*

> İçindekiler: su, şeker, asitlik düzenleyici (E330), aroma verici, renklendirici (E150d).

| Etiketteki ifade | Eşleşen kavram | Yöntem |
|---|---|---|
| su | Su `en:water` | exact |
| şeker | Şeker `en:sugar` | exact |
| asitlik düzenleyici | Acidity regulator `en:acidity-regulator` | exact |
| E330 | sitrik asit `E330` | e_code |
| aroma verici | flavouring `en:flavouring` | exact |
| renklendirici | Colour `en:colour` | exact |
| E150d | Sülfit amonyak karamel `E150D` | e_code |

| Durum | Sonuç | Neden | Kaynak |
|---|---|---|---|
| Çölyak | **Dikkat** | CEL-04: Gluten kaynağı görünmüyor ama 'glutensiz' beyanı yok; çapraz bulaşma bilinmiyor (varsayılan) | Ekip kararı (belirsizlik riski yalnız artırır) |
| Diyabet | **Dikkat** | DM-01: sekerler 11.0 g / 100 ml (sınırın üstünde) | Reg. (EC) No 1924/2006 Ek (SUGARS-FREE; LOW SUGARS); TGK Beslenme ve Sağlık Beyanları Yönetmeliği (RG 29960) Ek-1 |
| Kronik böbrek hastalığı | **Doğrulanamadı** | CKD-03: besin tablosu gerekli → kullanıcıdan istenir | Ekip kararı (K5 eksik veri) |

