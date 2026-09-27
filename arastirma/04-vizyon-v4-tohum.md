---
title: NutriScan v4 — vizyon tohumu (ajanlara bağlam)
updated: 2026-09-24
durum: HİPOTEZ — doğrulanacak, Levent onayı yok
---
# NutriScan v4 — Evin gıda asistanı

## Neden v4
- v3 (plan-önce sepet optimizasyonu) derin ama **dar**: eski MVP'deki tarama/aile/liste/LLM katmanlarını kesip yerine bir optimizasyon motoru koydu → Levent: "yeniden pişirilmiş, düşünsel olarak geri gitmiş", **görünür AI katmanı yok**.
- Levent'in yeni çerçevesi: kapsamı ve karmaşıklığı sınırlama; ekip agent + harness mimarisiyle hızlı üretecek; AI ürünün görünür yüzü olmalı; her akış happy path + edge case ile düşünülmeli.

## Tek cümle (hipotez)
NutriScan, hanenin **tüm gıda döngüsünü** — ne pişirilecek, ne alınacak, nereden, evde ne var, kime ne uygun — bilen ve yöneten **yapay zekâ destekli bir hane asistanıdır**; konuşur, görür, planlar ve hatırlar, ama her kararı **doğrulanabilir motorlara** dayandırır ve nedenini gösterir.

## Döngü: MENÜ → LİSTE → MARKET → MUTFAK → ÖĞREN
1. **Menü** — haftalık yemek planı (hane üyelerinin kısıtları, bütçe, süre, evde olanı önce kullan, çeşitlilik).
2. **Liste** — menüden + alışkanlıktan otomatik liste; en az değişiklikle iyileştirme (v3'ün Akıllı Takası).
3. **Market** — hangi marketten (≤2), rafta hane bazlı karar, rafı fotoğrafla çok ürün tarama.
4. **Mutfak** — kiler/buzdolabı durumu (fiş, fatura, barkod, buzdolabı fotoğrafı), son kullanma, bitmek üzere tahmini, "evde ne var ne pişirsem".
5. **Öğren** — plan vs gerçek, kabul edilen/edilmeyen öneriler, sepet göstergesi, kişisel enflasyon, tercih modeli.

## Yedi katman
| Katman | İçerik | Görünür AI mı |
|---|---|---|
| **Asistan** (yüz) | Sohbet + ses; hane hafızası; araç kullanan agent; proaktif öneriler ("Pazar sabahı planın hazır"); yaptığı adımları şeffaf gösterir | **Evet — ana yüz** |
| **Göz** (algı) | Barkod, etiket okuma, raf fotoğrafı (çok ürün), fiş/e-Arşiv, buzdolabı/kiler fotoğrafı, restoran menüsü | Evet |
| **Akıl** (motorlar) | Güvenlik kural motoru (deterministik), optimizasyon (menü, sepet, market), öneri sistemi (içerik + işbirlikçi — danışmanın alanı), tarif motoru (LLM üretir, kural motoru doğrular) | Kısmen (sonuçları) |
| **Hafıza** (hane grafiği) | Üyeler, kısıtlar, tercihler, kiler, alışveriş geçmişi, ürün bilgi grafiği (içerik → alerjen → ürün), tarif değişikliği takibi | Dolaylı |
| **Topluluk** (veri döngüsü) | Topluluk kataloğu + fiyat, moderasyon, OFF'a katkı, "senin gibi hanelerin sevdiği" | Evet |
| **Güven** | Neden? katmanı, karar kaydı, audit, KVKK, eval'ler, guardrail'ler | Evet (şeffaflık) |
| **Platform** | Mobil (yakala + asistan), web (stüdyo + raporlar), admin/ops, (ileride) API/MCP | — |

## Mimari ilke: "LLM orkestra eder, motorlar karar verir"
- LLM kullanıcının niyetini anlar, araçları çağırır, sonucu anlatır. **Uygunluk kararı, optimizasyon, fiyat, kiler** hep deterministik/doğrulanabilir araçlardan gelir. LLM bir araç sonucunu değiştiremez; her iddia bir araç çıktısına referans verir.
- **Gizlilik-koruyan agent (hipotez):** LLM sağlık verisini hiç görmez; üyeler ve kısıtlar sembolik yer tutucularla (`ÜYE_2`, `KISIT_7`) temsil edilir, LLM cevabı yer tutucularla yazar, sunucu Türkiye'de doldurur. Alternatif: hassas yollar için Türkiye'de barındırılan açık ağırlıklı model.

## Yeni "wow" adayları
- Pazar sabahı proaktif plan: "5 akşam yemeği, 1.850 TL, Ela için fındıksız, kilerdeki yoğurt ve ıspanak kullanıldı — onaylar mısın?"
- Rafı tek fotoğrafla tara: raftaki ürünler hane için renklenir.
- Buzdolabı fotoğrafı → "evde ne var" + bu akşam için 3 tarif.
- Sesli: markette "Bunu Ela yiyebilir mi?"
- Tarif değişikliği radarı: daha önce aldığın ürünün içeriği değişti ve artık Ela için uygun değil → bildirim.
- "Fındık alerjili çocuğu olan hanelerin en sevdiği atıştırmalıklar" (kısıt-farkında işbirlikçi öneri).
- Agent'ın adımlarını canlı izleme: "Katalogda arıyorum → Ela için kontrol ediyorum → 3 plan hesapladım".

## v3'ten korunan derinlik
Akıllı Takas MILP, sağlığın fiyatı, exact vs NSGA-II, market seçimi, fiş eşleştirme, NL→kısıt derleyici, dört durumlu karar, karar izi/audit, KVKK tasarımı.
