# NutriScan

Hanenin haftalık yemek ve alışveriş planını kuran, zincirden bağımsız asistan. CSE 491/492 bitirme projesi
(Akdeniz Üniversitesi Bilgisayar Mühendisliği, 2026–27). Ekip: Levent Can Ceylan, Şükran Hilal Hocaoğlu, Ozan Karadaş.
Danışman: Arş. Gör. Dr. Taha Yiğit Alkan.

**İlk kez açıyorsan:** [`plan/ilk-prompt.md`](plan/ilk-prompt.md) (kurulum + ilk prompt).
**Agent'lar için kurallar:** [`AGENTS.md`](AGENTS.md) · **Şu an:** [`DURUM.md`](DURUM.md) · **Board:** https://dev.azure.com/hilalhocaoglu20/NutriScan

| | |
|---|---|
| Ürün yönü (tez v5.1) | [`arastirma/07-tez-v5.md`](arastirma/07-tez-v5.md) |
| Ürün tanımı, FR/NFR | [`plan/urun-tanimi.md`](plan/urun-tanimi.md) |
| Değişmez kurallar | [`docs/anayasa.md`](docs/anayasa.md) |
| Kararlar | [`plan/kararlar.md`](plan/kararlar.md) |
| Takvim ("en geç" tarihleri) | [`plan/takvim.md`](plan/takvim.md) |
| Çalışma akışı (board → agent → PR) | [`plan/calisma-akisi.md`](plan/calisma-akisi.md) |
| İş listesi ve promptlar | [`plan/board/`](plan/board/) |
| Prototip ekranları | [`plan/prototip-kaynak/`](plan/prototip-kaynak/) |

Stack (ADR-006/007): Java 25 · Spring Boot 4.1 · Spring Modulith · PostgreSQL 18 + pgvector · OR-Tools CP-SAT ·
Spring AI · Expo (React Native) · Vite + React · Contabo VPS. Kod iskeleti Sprint 0'da gelir.
