# ADR-007 · Arayüz stack'i: React ailesi

**Tarih / onay:** 2026-09-25, ekip

- **Ne:** Mobil Expo (React Native) + EAS; web ve admin Vite + React (TanStack Router/Query/Table, shadcn/ui, Recharts); ortak TS paketleri: OpenAPI → Orval istemcisi, tasarım token'ları, `ui-core` (hüküm rozeti mantığı).
- **Neden:** barkod/STT/push/store tarafında en olgun JS yolu Expo; tek karşılaştırmalı benchmark'ta React önde (Web-Bench %44 / %40); Gemini'nin Angular'da eski idiomlara kaydığı gözlemi; ekipte React/Expo geçmişi (vekillik mümkün); SSR gereksiz (Spring backend, giriş arkasında web).
- **Alternatif:** Angular 22 + Ionic/Capacitor · Flutter. **Neden değil:** WebView tabanlı mobil, Ionic ticari servislerinin kapanması, PrimeNG'nin kapalı kaynağa geçmesi, ekipte Angular vekili yok · Dart bilgisi yok, web erişilebilirliği zayıf. Ayrıntı `arastirma/10-stack-arayuz.md`.
