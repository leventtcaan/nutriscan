Fixes AB#

## Ne
<!-- 1–3 madde: bu PR neyi değiştiriyor. Tek modül. -->

## Neden
<!-- Hangi PBI ve kabul kriteri; hangi omurga parçası ya da deney (E1/E2/E3) -->

## Alternatif
<!-- Başka nasıl yapılabilirdi, neden o değil. Kalıcı bir tercihse plan/kararlar/ADR-0NN bu PR'da -->

## Nasıl doğrularım
<!-- İnceleyenin kendi makinesinde koşacağı komutlar ve beklenen çıktı -->

## Kabul kriterleri
<!-- plan/board/promptlar/<ID>.md'deki her madde → kanıt (test adı / komut çıktısı / ekran görüntüsü) -->
- [ ]

## Sözleşme etkisi
<!-- yok / eklemeli / kırıcı (kırıcıysa contract-change etiketi + iki sahip onayı) -->

## AI kullanımı
<!-- "AI agent" de, araç adı yazma · ne için kullanıldı · hangi kısmı insan yazdı ya da karar verdi · agent'ın önerip reddedilen şey -->

## Sürprizler
<!-- Beklenmeyen davranış, yarım kalan, sonraki PBI'a taşınan -->

## İnceleyen için 3 soru
1.
2.
3.

## Kontrol listesi
- [ ] CI yeşil; kontrol komutlarının çıktısı yukarıda
- [ ] Tek modül, ≤ ~400 satır (üretilmiş kod ve veri hariç)
- [ ] Anayasa: "güvenli" yok · belirsizlik → Doğrulanamadı · logda sağlık verisi yok · hardcode/sır yok
- [ ] Arayüzse `arayuz-tasarim` kontrol listesi + iOS/Android (ya da dar/geniş web) ekran görüntüleri
- [ ] Commit ve PR'da AI imzası yok
- [ ] Agent'ın yazdığını okudum ve anlatabilirim (sahip işaretler)
- [ ] `oturumlar/<kişi>.md` girdisi eklendi
