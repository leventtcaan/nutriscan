---
title: Faz 1 Sentezi — NutriScan problem & fizibilite
updated: 2026-09-24
durum: ÖNERİ — Levent onayı bekliyor
---
# Faz 1 Sentezi

Kaynak raporlar: `01-rakip-pazar.md` · `01-veri-fizibilite.md` · `01-mevzuat-risk.md` · `01-danisman-bitirme.md` · `01-ai-feature-havuzu.md` · (eski repo analizi sadece sohbette)

## 1. Beş gerçek
1. **Çekirdek fikir özgün değil.** Global: Fig, Yuka, CodeCheck, Fooducate. TR: Ürün Dedektörü (alerji/hamilelik/çölyak profili), ÇabukBak (~80k barkod), Gluten Tarayıcı (2015'ten beri). Ama TR'de pazarı domine eden yok; Fig/Yuka TR'de yok.
2. **Asıl darboğaz veri.** OFF'ta TR: 11.411 ürün, içindekiler tamam ~%25 (CSV'de 869-prefix 19.375 barkod, içindekiler dolu %14,5). OFF'un alerjen taksonomisinde Türkçe yok; TR örneklemde sütlü ürünlerin ~%20'sinde alerjen etiketi eksik. OFF'u tamamlayan ücretsiz/yasal ikinci TR kaynağı yok.
3. **LLM karar veremez.** Literatür (NutriBench, FoodGuardBench, FAM-Bench, OmniFood-Bench): LLM tanıma/açıklamada iyi, "bu kişi için güvenli mi" kararında güvenilmez.
4. **Mevzuat tasarımı belirliyor.** Sağlık verisi özel nitelikli; yurt dışına sistematik aktarımda açık rıza yetmez (7499 s. Kanun) → profil TR'de tutulmalı, LLM'e sadece ürün verisi gitmeli. "Güvenli" demek ve hastalık yönetimi dili tıbbi cihaz/sorumluluk riski. TR'de "iz miktarda içerebilir" beyanı gönüllü → beyan yokluğu ≠ güvenli.
5. **Danışman profili:** Arş. Gör. Dr. T. Y. Alkan — veri madenciliği + **öneri sistemleri** kökenli, doktorası mekânsal optimizasyon (MCLP vs GA, 20 senaryo). CSE 413'ün ruhu: "exact çözüm + sezgisel + aradaki gap'i dürüst istatistikle ölç". Bitirme komisyonu üyesi.

## 2. Önerilen tez (tek cümle)
> NutriScan, Türkiye'de taranan bir gıda ürününün hanedeki her kişi için **neden** uygun olup olmadığını — veri yetersizse "bilmiyorum" diyerek — açıklanabilir biçimde söyleyen, veri yoksa etiketi okuyarak veriyi kendisi üreten ve kişinin kısıtlarına uygun, bütçeye duyarlı **alternatif/sepet önerisini optimizasyonla** hesaplayan bir sistemdir.

## 3. Üç sütun + bir zemin
| Sütun | İçerik | Ölçülebilir iddia |
|---|---|---|
| **Güven** — karar motoru | Deterministik kural + TR alerjen/eş anlamlı sözlüğü (TGK Ek-1 14 alerjen, E-kodları, türevler), 4 durumlu sonuç ("güvenli" kelimesi yok), Decision Record, LLM sadece açıklar ve sadece risk ekleyebilir | Elle etiketli TR golden set'te false-negative oranı; kural vs LLM vs hibrit kıyası |
| **Kapsama** — veri döngüsü | OFF TR mirror (dump + delta), etiket fotoğrafı → vision LLM → kullanıcı onayı → moderasyon → OFF'a geri katkı | TR içindekiler kapsamı %X → %Y; OCR doğruluğu kendi setimizde |
| **Akıl** — optimizasyon | P2 güvenli ikame (öneri + ILP; hocanın iki alanı), P1/P3 bütçe-kısıtlı sepet (LP dualite/gölge fiyat; exact ε-constraint vs NSGA-II) | Optimalite gap'i, hypervolume, 30 seed |
| **Zemin** — ürün kalitesi | Hane modu (davetle, doğru rıza), admin: karar izi, audit log, moderasyon, kural versiyonlama, LLM izleme; structured logging ilk sprintten | Hocaların geçen yılki eleştirisine doğrudan cevap |

## 4. Kapsam dışı (şimdilik / future work)
Tabak fotoğrafıyla kalori, CGM/Health Connect, markete sepet aktarma, tam diyetisyen paneli, haftalık yemek planı (TR tarif verisi yok), gamification.

## 5. Proposal'a kadar takvim (deadline 18 Eki)
| Hafta | Tarih | Çıktı |
|---|---|---|
| 2 | 24–27 Eyl | Tez + kapsam onayı (Levent) · ürün tanımı · FR/NFR taslağı |
| 3 | 28 Eyl–4 Eki | Stack/mimari ADR'leri · wireframe v0 · danışman görüşmesi #1 (tez + optimizasyon açısı) |
| 4 | 5–11 Eki | Proposal tam taslak · iş paketleri · ekip/agent standartları · taslak hocaya |
| 5 | 12–18 Eki | Revizyon + danışman onayı + Teams'e yükleme |
Sonrası: 8. hafta ara rapor + ara sunum; dönem sonu çalışan ilk prototip + final rapor.
