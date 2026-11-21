*NutriScan — güncel durum (27 Eylül)*

Geçen yıl danışmana anlattığımız konsepti (barkod + alerjen + diyabet gibi hastalıklar için RAG; "kararı LLM değil kural verir") yeniden inceledik. Ozan'ın hatırlattığı gibi hastalık tarafı yeni planda görünmüyordu. Plan buna göre güncellendi (tez v5.1). Aşağıdaki belgelerin hepsi bu güncel hâli yansıtıyor.

*Ne değişti*
1. *Sağlık durumu profili:* Üye isterse diyabet, hipertansiyon, çölyak ya da hamilelik seçer. Her durum kaynağı belli, sürümlü bir kurala bağlı (ör. 100 g'daki şeker/tuz eşiği). Kararı kural motoru verir; sonuç "Dikkat" + besin bilgisi. "Zararlı/riskli" demiyor, teşhis koymuyoruz; tıbbi cihaz sınırında kalmamak için dil bilgilendirme düzeyinde.
2. *Önce güvenlik:* Plan kurulurken sıra kesin kısıtlar → sağlık kuralları ve hedefler → hane tercihi ve kiler → fiyat. Bütçe amaç değil, sınır.
3. *RAG'ın yeri:* Anlamsal arama kararı vermiyor. Etiketteki yeni içerik adları için sözlüğe eşleme öneriyor (moderatör onaylıyor) ve açıklamada kaynağı alıntılıyor. Bu yöntem tam eşlemeye karşı ölçülecek (E2).
4. *Veri konumu netleşti:* Uygulama verisi Contabo'da (AB), minimize ve şifreli; hane bilgisiyle çalışan yapay zekâ Türkiye'de (EVREN). Prototipteki "veriler Türkiye'de" ifadeleri buna göre düzeltildi.

*Yeni işler (takvim v1.5)*
*A1.12* Sağlık durumu eşik tablosu v0 (her satır kaynaklı)
👤 Ozan (derleme) · Hilal (şema, onay) · ⏰ 1 Kasım
*A2.16* Sağlık kuralları kural motorunda + test seti
👤 Hilal · ⏰ 9 Aralık
*A3.7* RAG içerik eşleme + kaynak alıntısı
👤 Levent · ⏰ 29 Ocak

*Ekler*
• Proposal taslağı (6 sayfa, PDF + Word): teslim 18 Ekim, danışmana en geç 9 Ekim
• Takvim v1.5 (PDF) + çalışma akışı standardı (board, sprint, PR, agent promptu)
• Tez v5.1 ve ürün tanımı v5.1 (PDF)
• Prototip: https://claude.ai/artifact/T1NAJd4949veMC6Rx5rLUK
  Yeni/güncel ekranlar: M02 Hane kur · M09 Rafta · M22 "Neden dikkat?" · A01 Karar izi · A02 Katalog

*Ekipçe bakılacaklar (en geç 30 Eylül)*
• Takvim ve iş bölümüne onay ya da itiraz
• Proposal: rol ve iş paketi satırları, öğrenci numaraları, grup numarası
• Eşik tablosu (A1.12) iş bölümüne uygun mu

2 Ekim Cuma görüşmesine bu belgelerle gidiyoruz; Meeting Record aynı gün Teams'e yüklenecek.
