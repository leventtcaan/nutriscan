---
title: 10 — Arayüz stack'i (mobil + web + admin) — AI agent'lı tek sahip için
updated: 2026-09-25
durum: HAM ARAŞTIRMA — ekiple netleştirilmedi, 2026-09-25
dayanak: 07-tez-v5.md (§4 UX, §8 takvim, §9 demo) · plan/kararlar.md (ADR-004 bileşen sahipliği, ADR-005 araçlar) · 08-ekip-calisma-modeli.md §3 (monorepo, contract-first, üretilmiş API istemcisi)
---
# 10 — Arayüz stack'i

> **Ham araştırma — ekiple netleştirilmedi, 2026-09-25.** "(doğrulanmadı)" ve "(ikincil kaynak)" etiketlerine dikkat. Kişi adı yok; "arayüz sahibi" = ADR-004'te mobil + web + admin arayüzlerinin sahibi.

## 0. Kısa sonuç
1. **Öneri:** **React ailesi, tek TypeScript monorepo.** Mobil = **Expo (SDK 56+, development build)** + Expo Router · Web (Planlama Stüdyosu, hane paneli) ve Admin = **Vite + React SPA** (TanStack Router + TanStack Query + shadcn/ui + TanStack Table + Recharts) · Ortak paketler: `packages/api-client` (OpenAPI → **Orval** ile TanStack Query hook'ları + Zod şemaları; mobil ve web aynı hook'ları kullanır), `packages/tokens` (tasarım token'ları, tek kaynak), `packages/ui-core` (karar rozeti gibi kritik bileşenlerin platformdan bağımsız mantığı).
2. **Neden:** (a) Mobil yerel yetenekler (barkod, cihazda STT, push, çevrimdışı, store yayını) için JS dünyasında en olgun yol Expo + EAS; (b) agent'ların en çok veri gördüğü ve benchmark'larda Angular'dan önde olduğu çatı React; (c) ekibin geçen yıl React/Expo tecrübesi var → diğer iki üye arayüzde **vekil** olabilir (ADR-004 "her modülün vekili var"); (d) Next.js yerine Vite SPA: backend Spring, web giriş yapılmış uygulama → SSR/RSC'nin getirdiği "ayak tabancaları" gereksiz.
3. **En güçlü alternatif:** Angular (web + admin) + Ionic/Capacitor (mobil). Angular'ın agent araçları (resmi MCP sunucusu, `ng new`'de AI kural dosyası, **Antigravity için resmi `GEMINI.md`**) gerçekten iyi ve konvansiyonu güçlü. Seçilmeme nedenleri: mobil tarafta Ionic'in ticari servislerinin kapanması (Appflow 2027 sonu) ve eklentilerin üçüncü taraf ekiplere bağımlılığı, WebView içinde UI, ekipte Angular bilen vekil yok, ve **Gemini'nin Angular'da eski idiomlara kaydığına dair 2026 gözlemi** (tam bu ekibin kombinasyonu).
4. **Karar kapısı (öneri):** arayüz sahibinin Angular tercihi ciddi bir tercih; bu yüzden **Sprint 0 öncesi 2 günlük spike**: aynı iki ekran (barkod → ürün kartı + karar rozeti; Stüdyo'da Pareto grafiği + kaydırıcı) Antigravity ile iki stack'te yazılır; build/lint/test hatası, düzeltme turu sayısı ve süre ölçülür. Veri React'i desteklemezse ADR yeniden açılır.

---

## 1. Seçenekler — karşılaştırma

### 1.1 Özet tablo
| Ölçüt | (a) Angular + Ionic/Capacitor | (b) React: Expo (mobil) + Vite React (web/admin) | (b') Expo Router universal (mobil + web tek app) | (c) Flutter (mobil + web) | (d) Kotlin/Compose Multiplatform |
|---|---|---|---|---|---|
| Tek kod tabanı | **En yüksek**: tek dil + tek framework; servisler, API istemcisi, hatta bileşenler paylaşılır (Ionic bileşenleri web component) | Orta-yüksek: dil, API hook'ları, Zod, token'lar, iş mantığı ortak; **UI bileşenleri ayrı** (RN vs DOM) | Yüksek (mobil + tüketici web aynı dosyalar); admin yine ayrı olmalı | En yüksek (tek UI ağacı) | Mobil yüksek; web Beta |
| Barkod (EAN-13) | `@capacitor-mlkit/barcode-scanning` (Capawesome, ML Kit, EAN-13 destekli, format kısıtlanabilir) | `expo-camera` (Android: Google Code Scanner, iOS 16+: VisionKit DataScanner) veya `react-native-vision-camera` v5 (ML Kit/VisionKit, tarama bölgesi, köşe noktaları) | = (b) | `mobile_scanner` (CameraX/ML Kit, iOS Vision) | yerel ML Kit/VisionKit (en doğrudan) |
| Cihazda STT | `@capgo/capacitor-speech-recognition` v8 (iOS 26+ SpeechAnalyzer yolu) veya Capawesome ML Kit GenAI Speech (alpha, Gemini Nano cihaz desteği sınırlı) | `expo-speech-recognition` (jamsch; iOS 17+, Android 13+ on-device; `requiresOnDeviceRecognition`) | = (b) | `speech_to_text` (doğrulanmadı) | yerel API'ler |
| Push | `@capacitor/push-notifications` (resmi) | `expo-notifications` (FCM/APNs; Expo push servisi opsiyonel) | = (b) | `firebase_messaging` | yerel |
| Çevrimdışı + güvenli saklama | Capawesome SQLite (SQLCipher), Secure Preferences, Vault (Identity Vault'un yerine) | `expo-sqlite`, `expo-secure-store`, TanStack Query persist | = (b) | `sqflite`/`drift`, `flutter_secure_storage` | SQLDelight |
| Store yayını | Xcode/Android Studio yerel veya 3. taraf bulut (Capawesome Cloud, Codemagic…); **Appflow yeni satış yok, 31 Ara 2027'de kapanıyor** | **EAS Build/Submit** (bulutta iOS build, Mac şart değil), EAS Update | = (b) | Codemagic / yerel | yerel |
| Web: grafik + admin tablo | Angular Material + CDK Table, ngx-echarts; **PrimeNG Haziran 2026'da kapalı kaynağa geçti** (Community lisans ücretsiz ama grafik "Pro") | En geniş ekosistem: shadcn/ui, TanStack Table, Recharts/ECharts, react-admin/shadcn-admin-kit, Refine | RN-web ile yoğun masaüstü tablo/grafik zor; `'use dom'` DOM bileşenleriyle web kütüphanesi kullanılabilir | Canvas render; tablo/grafik paketleri daha dar | Web (Wasm) Beta |
| Erişilebilirlik | Web standartları (ARIA) + Angular Aria (v22'de stabil); mobilde WebView üzerinden ekran okuyucu | RN `accessibilityRole/Label`; web'de Radix/shadcn ARIA | RN-web ARIA'ya çevirir | **Web'de en zayıf** (canvas; semantik ağaç var ama HTML eşdeğeri değil) | Web'de zayıf |
| AI agent uygunluğu (§2) | Güçlü resmi araçlar, konvansiyon; benchmark'ta React'in biraz gerisinde, Gemini eski idiom riski | En çok eğitim verisi, en çok benchmark; resmi AGENTS.md/MCP/skills (Expo), Next.js evals | = (b), RN-web kenar durumları agent'ı zorlar | Resmi Dart/Flutter MCP + Gemini CLI eklentisi; Dart verisi JS'ten az | En az veri |
| Ekip geçmişi | Arayüz sahibinin tercihi; diğerleri bilmiyor | Ekip geçen yıl Next.js + Expo yazdı | = (b) | Kimse bilmiyor | Kotlin Java'ya yakın ama UI yeni |

### 1.2 (a) Angular + Ionic/Capacitor
- **Durum (Eylül 2026):** Angular 22 (3 Haziran 2026) — OnPush varsayılan, Signal Forms, `resource/httpResource`, Angular Aria stabil; Angular 21'de zoneless ve Vitest varsayılan ([Angular v22 duyurusu](https://blog.angular.dev/announcing-angular-v22-c52bb83a4664), [Angular 21 — Ninja Squad](https://blog.ninja-squad.com/2025/11/20/what-is-new-angular-21.0)). Ionic Framework 9 (Ağustos 2026) Angular 18–22'yi destekliyor, standalone varsayılan ([Ionic 9](https://ionic.io/blog/announcing-ionic-framework-9)). Capacitor 8.5 (Temmuz 2026, UIScene), Capacitor 9 Kasım sonu bekleniyor ([Capacitor 8.5](https://ionic.io/blog/capacitor-8-5-released), [Road to Capacitor 9](https://ionic.io/blog/the-road-to-capacitor-9)).
- **Şirket riski:** OutSystems Şubat 2025'te Ionic'in ticari ürünlerini (Appflow, Identity Vault, Portals) yeni satışa kapattı; açık kaynak Ionic + Capacitor sürdürülüyor. Ionic, Eylül 2026'da Capawesome'ı tercihli geçiş ortağı ilan etti ([Ionic duyurusu](https://ionic.io/blog/important-announcement-the-future-of-ionics-commercial-products), [Wikipedia](https://en.wikipedia.org/wiki/Ionic_(mobile_app_framework))). Sonuç: kritik eklentiler (barkod, güvenli saklama) fiilen Capawesome/Capgo gibi küçük ekiplere bağlı.
- **Barkod:** Capawesome ML Kit eklentisi yerel ML Kit'i kullanır, EAN-13 dahil 13 format; `formats` ile kısıtlama hızı artırır ([Capawesome](https://capawesome.io/docs/sdks/capacitor/mlkit/barcode-scanning/)). Kamera önizlemesi WebView'in arkasında çizilir → UI şeffaflık düzeni gerekir (bilinen desen).
- **Artısı:** tek framework; Angular'ın opinionated yapısı (DI, router, forms, HttpClient, CLI şemaları) agent'a "tek doğru yol" verir. **Eksisi:** mobil deneyim WebView; mobil ekosistem küçük; ekipte ikinci Angular bilen yok.

### 1.3 (b) React: Expo + Vite React
- **Durum:** Expo SDK 55 (25 Şub 2026) Legacy Architecture'ı kaldırdı; SDK 56 (21 May 2026) RN 0.85, Hermes v1 varsayılan, Expo UI stabil, Expo Router React Navigation'dan ayrıldı, yeni projeler **AGENTS.md + CLAUDE.md** ile geliyor ([SDK 55](https://expo.dev/changelog/sdk-55), [SDK 56](https://expo.dev/changelog/sdk-56)).
- **Barkod:** başlangıç için `expo-camera` yeterli (Expo Go'da çalışır); tarama bölgesi, köşe noktası, fps kontrolü gerekirse VisionCamera v5. Margelo'nun Ağustos 2026 rehberi: yalnız gereken formatları istemek ölçülebilir şekilde hızlandırır; **EAN-13 için sayısal gecikme verisi yok** ([Margelo](https://margelo.com/blog/react-native-barcode-scanner), [Scanbot karşılaştırma](https://scanbot.io/blog/react-native-vision-camera-vs-expo-camera/)).
- **STT:** `expo-speech-recognition` — iOS 17+ ve Android 13+ cihazda tanıma; Android'de dil modeli indirilmeli (`androidTriggerOfflineModelDownload`) ([GitHub](https://github.com/jamsch/expo-speech-recognition)). **Türkçe'nin cihazda (iOS SpeechTranscriber / Android offline) desteklendiği doğrulanamadı** → Sprint 0'da `getSupportedLocales()` ile test.
- **Monorepo:** Expo SDK 52+ Metro'yu monorepo için otomatik yapılandırıyor; SDK 54+ pnpm isolated install destekli ama "bazı RN kütüphaneleri sorun çıkarabilir" → gerekirse `nodeLinker: hoisted` ([Expo monorepo](https://docs.expo.dev/guides/monorepos/)). 08 dokümanındaki "EAS + pnpm" şüphesi buradan cevaplanıyor: destekli, kaçış yolu var.
- **Neden Next.js değil Vite:** backend Spring; SSR/SEO ihtiyacı yok (Stüdyo ve admin giriş arkasında); App Router'ın server/client sınırı ve önbellek davranışı zayıf agent için hata kaynağı. Vite SPA + TanStack Router dosya tabanlı ve tip güvenli rotalar verir.

### 1.4 (b') Expo Router universal (mobil + web tek uygulama)
- Aynı `app/` klasörü mobilde stack, web'de sayfa olur; statik render üretim varsayılanı; RN-web ~30–40 KB gzip ek yük ([Expo Router](https://docs.expo.dev/router/introduction/), [Expo web](https://docs.expo.dev/workflow/web/), ikincil: [RN Relay](https://reactnativerelay.com/article/react-native-web-expo-cross-platform-2026)). SDK 56'da web için streaming SSR `unstable_` önekiyle geldi.
- Web kütüphaneleri (shadcn, grafik) native'de `'use dom'` DOM bileşenleriyle WebView içinde çalışır; paylaşılmazsa bileşen başına ~300 KB büyüme ([DOM components](https://docs.expo.dev/guides/dom-components/), ikincil: [SDK 56 özeti](https://dev.to/expo/expo-sdk-56-5eb5)).
- **Değerlendirme:** Stüdyo ve admin masaüstü, veri yoğun ekranlar; mobil ekranların web kopyasına ihtiyaç yok. Universal model burada tasarruftan çok RN-web kenar durumu getirir. **Önerilmiyor**; ileride "mobil ekranın web'de de açılması" istenirse aynı monorepo'da açılabilir.

### 1.5 (c) Flutter
- Dashboard tipi giriş arkası web için Wasm ile "üretime uygun" deniyor, ama **2026'da web'in en büyük açığı erişilebilirlik** (canvas; semantik ağaç HTML eşdeğeri değil) (ikincil: [Softaims](https://softaims.com/blog/flutter-web-desktop-production-ready-2026)). Tezde erişilebilirlik (renk + ikon + metin) zorunlu.
- Google'ın resmi Dart/Flutter MCP sunucusu ve Gemini CLI Flutter eklentisi var ([Dart MCP](https://dart.dev/tools/mcp-server), [Flutter AI](https://docs.flutter.dev/ai/get-started)) — Antigravity ile uyum iyi olabilir, ama ekipte Dart bilen yok, OpenAPI → Dart istemci üretimi TS kadar olgun değil (doğrulanmadı), admin tablo/grafik ekosistemi dar.

### 1.6 (d) Kotlin/Compose Multiplatform
- iOS Mayıs 2025'te stabil (1.8.0); web (Wasm) 1.9.0'da **Beta** ([JetBrains 1.8](https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/), [1.9 web beta](https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/)). Kotlin, Java bilen ekibe yakın; ama web + admin için Beta ve agent eğitim verisi en az olan seçenek. **Elendi.**

---

## 2. AI coding agent'ların bu çatılarda kod kalitesi — kanıt

| Kanıt | Ne söylüyor | Güç |
|---|---|---|
| **Web-Bench** (arXiv 2505.07473, 2025) — 20 ardışık görevli projeler, E2E testli | En iyi model (Claude 3.7 thinking, Best-of-5) Pass@1: **Vue %60, Svelte %55, React %44, Angular %40**. Yazarlar: Angular "en karmaşık gramer", daha az veri; JSX veri yoğunluğunu artırıyor ([arXiv](https://arxiv.org/html/2505.07473v1)) | Orta: 2025 modelleri; fark React–Angular arası küçük (4 puan) |
| **Next.js Agent Evals** (Vercel, son koşu 22 Eyl 2026) | Güncel üst modeller %90–97. **Gemini CLI + Gemini 3.1 Pro (Nisan 2026): %58 → AGENTS.md ile %71**; Gemini 3.8 Flash (OpenCode): %90 → %97 ([nextjs.org/evals](https://nextjs.org/evals)). AGENTS.md ile paketlenmiş doküman, skill yaklaşımını geçmiş ([Next.js 16.2 AI](https://nextjs.org/blog/next-16-2-ai)) | Güçlü ama yalnız Next.js; **Gemini tarafında talimat dosyasının etkisi büyük** |
| **ANGULARarchitects** (27 May 2026, uygulayıcı gözlemi) | Angular için Codex (GPT 5.5) ≈ Claude (Opus 4.7) en iyi; **Antigravity "henüz rekabetçi değil"**; Gemini 3.5 Flash "sinyaller ve yeni control flow'da eski Angular idiomlarına daha sık kayıyor", "daha çok yönlendirme istiyor" ([blog](https://www.angulararchitects.io/blog/ai-apps-harnesses-for-angular/)) | Anekdot ama **tam bu ekibin kombinasyonu** (Antigravity + Gemini + Angular) |
| **WebDev Arena** | React + TypeScript + Tailwind zorunlu; framework karşılaştırması yapmıyor ([arena.ai](https://arena.ai/blog/webdev-arena), ikincil: [Developers Digest](https://www.developersdigest.tech/blog/web-dev-arena)) | Framework sorusu için **kanıt değil**; ama ekosistemin React'e göre ayarlandığını gösteriyor |
| **Angular Web Codegen Scorer** (Google Angular ekibi) | Build, runtime hatası, a11y, güvenlik, best practice ölçer; ekip prompt'u iyileştirip LLM'lerin **97 üstü** skor almasını sağladığını söylüyor; framework-bağımsız ama **karşılaştırmalı skor tablosu yayınlanmadı** ([GitHub](https://github.com/angular/web-codegen-scorer), [InfoWorld](https://www.infoworld.com/article/4061080/web-codegen-scorer-evaluates-ai-generated-web-code.html)) | Angular'ın "doğru talimatla kalite yükselir" iddiasının dayanağı; bağımsız doğrulama yok |
| **React Native Evals** (Callstack, 2026) | 39–43 görev (animasyon, async state, navigasyon); sonuçlar etkileşimli sitede — **model bazlı sayıları çekemedim** ([duyuru](https://www.callstack.com/blog/announcing-react-native-evals)) | Doğrulanamadı |
| Flutter/Dart | "Tipli dil daha az halüsinasyon" iddiası ikincil ve ölçümsüz; JS/TS'nin veri üstünlüğü de ikincil ([Droids On Roids](https://www.thedroidsonroids.com/blog/flutter-vs-react-native-comparison)) | Zayıf |
| Varsayılan yığın eğilimi | v0, Lovable, Bolt fiilen React + Tailwind + shadcn'e kilitli; neden: korpus (ikincil, [blog](https://saschb2b.com/blog/llm-default-react-stack)) | Zayıf ama tutarlı |

**Resmi agent desteği (2026):**
| | Angular | Expo / React | Flutter |
|---|---|---|---|
| llms.txt | var (llms.txt + llms-full.txt) | var (~54 KB) ([Expo llms](https://docs.expo.dev/llms/)) | — (doğrulanmadı) |
| MCP sunucusu | Angular CLI MCP (v20.2'de geldi, v21'de stabil): `get_best_practices`, `search_documentation`, `find_examples` ([angular.dev/ai](https://angular.dev/ai/develop-with-ai), [angular.love](https://angular.love/angular-cli-mcp-server-keep-your-ai-up-to-date)) | Expo MCP: doküman, EAS build logları, simülatör ekran görüntüsü ([Expo agents](https://docs.expo.dev/agents/)) | Dart/Flutter MCP (resmi) |
| Proje talimat dosyası | `ng new` / `ng generate ai-config` → AGENTS.md, CLAUDE.md, Gemini vb. ([ai-config](https://angular.dev/cli/generate/ai-config)); **Antigravity için resmi `GEMINI.md`** | `create-expo-app` → AGENTS.md (+ CLAUDE.md, SDK 56); `create-next-app` → AGENTS.md | Gemini CLI Flutter eklentisi kuralları |
| Skills | topluluk | Resmi Expo Skills (Claude Code, Codex eklentisi); **Gemini/Antigravity resmi olarak anılmıyor** | Gemini CLI eklentisi |

**Antigravity notu:** Antigravity kökte ve alt klasörlerde `AGENTS.md`/`GEMINI.md`'yi okur (frontmatter'sız, hep aktif), `.agents/rules/*.md` (trigger: always_on / model_decision / glob / manual), dosya başı 24 KB, always-on kurallar toplam 20k token bütçesi ([Antigravity Rules](https://antigravity.google/docs/rules)). **Model seçici**: Gemini 3.8/3.7/3.6 Flash, Gemini 3.1 Pro, **Claude Sonnet 4.6 ve Claude Opus 4.6 (thinking)**, GPT-OSS-120b — Free/AI Pro/Ultra planlarında hepsi var, Enterprise'da yalnız Gemini ([Antigravity Models](https://antigravity.google/docs/models/)). Kotalar Mart 2026'da daraltıldı (Pro/Claude haftalık yenileme; ikincil). → **Arayüz sahibi kritik parçalarda Antigravity içinden Claude Opus'a geçebilir**; bu, "zayıf agent" riskini stack'ten bağımsız azaltan en ucuz önlem.

**Sonuç (§2):** "Angular agent için daha güvenli" iddiasını destekleyen **bağımsız ölçüm bulamadım**; mevcut tek karşılaştırmalı benchmark React'i Angular'ın hafifçe önüne koyuyor ve Gemini + Angular kombinasyonu için olumsuz bir 2026 uygulayıcı gözlemi var. Angular'ın gücü resmi araçlarda ve konvansiyonda — bunlar kaliteyi artırıyor ama benchmark'la gösterilmiş bir üstünlük değil. Her iki tarafta da **en büyük kaldıraç talimat dosyası + CI kapısı** (Gemini'de Next.js evals'ta +13 puan).

---

## 3. Ekip dinamiği
- **Tercih vs geçmiş:** Arayüz sahibi Angular istiyor; ekip geçen yıl Next.js + Expo yazdı. Agent'lı çağda "kim yazıyor" kadar **"kim review edip vekil olabiliyor"** önemli (ADR-004: her modülün vekili var; 08 §3.g "sahip darboğazı"). Angular'da vekillik fiilen kimsede olmaz; React'te diğer iki üye (ve güçlü agent'ları) arayüz PR'ını okuyup düzeltebilir.
- **Öğrenme eğrisi:** Angular 21–22 hızlı değişti (zoneless, OnPush varsayılan, Signal Forms, yeni control flow) → modeller eski idiomlara kayıyor (§2). React'te de tuzak var (useEffect ile veri çekme, durum dağınıklığı, React 19 RSC) — bunları **stack seçimiyle** (Vite SPA, RSC yok) ve **lint kurallarıyla** kapatmak mümkün.
- **Konvansiyon gücü:** Angular'ın opinionated yapısı agent'a "tek yol" verir — gerçek avantaj. React'te bu yol biz tarafından yazılmalı: kök `AGENTS.md` + `apps/*/AGENTS.md` içinde **"izinli kütüphaneler listesi"** (TanStack Query = tek sunucu durumu, Zustand = tek istemci durumu, shadcn/ui = tek bileşen seti, form = React Hook Form + Zod, stil = Tailwind), ESLint ile zorlanır. Böylece React "opinionated hale getirilmiş" olur. Bedeli: kuralları platform rolü yazar (ADR-004'te zaten onun işi).
- **Tercihe saygı:** Karar, arayüz sahibinin tercihinin üstüne yazılmamalı → §0.4'teki **2 günlük spike** tercih ile veriyi aynı masaya koyar. Arayüz sahibi Angular'da belirgin şekilde daha hızlı ve daha az hatalı çıkarsa (a) seçilir; o durumda riskler §5.3'teki önlemlerle yönetilir.

---

## 4. Admin iskeleti ve tasarım sistemi

### 4.1 Admin
Admin ekranları (karar izi arama, audit tablo, moderasyon diff'i, deney paneli) çoğunlukla **özel**, saf CRUD az (katalog düzeltme). Öneri:
- `apps/admin` = ayrı Vite React uygulaması (ayrı deploy, ayrı rol koruması; ADR-004 klasör yapısıyla uyumlu), `apps/web` ile aynı `packages/ui`'ı kullanır.
- **Tablolar:** shadcn/ui "data table" deseni + TanStack Table (sunucu tarafı sayfalama/filtre, üretilmiş hook'larla).
- **CRUD ekranları:** yalnız katalog düzeltmesi gibi kaynak-merkezli ekranlarda **shadcn-admin-kit** (react-admin headless çekirdek + shadcn; Marmelab 2026'da aktif, haftalık bugfix) ([Marmelab Şubat 2026](https://marmelab.com/blog/2026/02/26/react-admin-february-2026-update.html), [shadcn-admin-kit](https://marmelab.com/shadcn-admin-kit/)). Alternatif **Refine v5** (headless, TanStack Query, shadcn entegrasyonu) ([Refine](https://github.com/refinedev/refine)). İkisi de API'yi kendi "data provider" sözleşmesine uydurmayı ister → üretilmiş istemci üstüne ince bir provider yazılır; Sprint 0'da 1 ekranla denenir, uymazsa atlanır.
- **Grafik:** Recharts (React'te en yaygın, agent'ın en çok gördüğü; Pareto için ScatterChart + çizgi); çok nokta/etkileşim gerekirse Apache ECharts (canvas) ([LogRocket 2026](https://blog.logrocket.com/best-react-chart-libraries-2026/)). Mobilde grafik gerekmiyor (Stüdyo web'de).
- **Moderasyon diff'i:** metin/JSON diff bileşeni (ör. `react-diff-viewer-continued`, doğrulanmadı) — Sprint 0'da seçilir.
- **Angular tarafı (alternatif için):** Angular Material + CDK Table + ngx-echarts. **PrimeNG 28 Haziran 2026'da repoyu arşivleyip kapalı kaynak "PrimeUI" lisansına geçti**; öğrenci/küçük kuruluşa ücretsiz Community lisans var ama grafik ve bazı bileşenler "Pro"; topluluk fork'u (OpenNG) Beta hedefinde ([Ng-News 26/17](https://dev.to/playfulprogramming-angular/ng-news-2617-primengs-new-licensing-and-a2ui-for-angular-4eik)) → Angular seçilirse PrimeNG'den kaçınılmalı.

### 4.2 Tasarım sistemi — kritik bileşenler tek kaynaktan
Tez §3: "hüküm rozeti yalnız karar kaydından çizilir"; renk + ikon + metin zorunlu. Bu bir **güvenlik bileşeni**, stil meselesi değil.
- `packages/tokens`: token'lar tek JSON (renk, tipografi, boşluk, **hüküm renk/ikon eşlemesi**) → build adımıyla (ör. Style Dictionary) web için Tailwind v4 `@theme` CSS değişkenleri, mobil için TS sabitleri üretilir. NativeWind v5 Tailwind v4 ile aynı CSS-first token modelini kullanıyor ama **hâlâ release candidate** ([NativeWind v5](https://www.nativewind.dev/v5)) → mobilde başlangıç için düz `StyleSheet` + üretilmiş TS token'ları; NativeWind v5 stabil olunca değerlendirilir.
- `packages/ui-core` (saf TS, React'siz): `verdictPresentation(decisionRecord) → {tone, icon, label, a11yLabel}` gibi **tek fonksiyon**; web (`VerdictBadge.tsx`, DOM) ve mobil (`VerdictBadge.native.tsx`) yalnız bu çıktıyı çizer. Birim testi + `contracts/decision-record.schema.json` fixture'larıyla tablo testi (4 hüküm × "Doğrulanamadı" dahil). ESLint kuralı: `apps/*` içinde hüküm rengini/metnini elle yazmak yasak (yalnız `ui-core` import'u).
- Röntgen modu rozetleri ("Motor karar verdi · DR#…" / "LLM anlattı · claim checker ✓") aynı paketten.

---

## 5. ÖNERİ — ADR taslağı

### ADR-006 (taslak) — Arayüz stack'i: React + Expo, tek TS monorepo
- **Ne:**
  - `apps/mobile`: **Expo SDK 56+** (development build, Expo Go değil), Expo Router, EAS Build/Submit/Update.
  - `apps/web` ve `apps/admin`: **Vite + React 19 SPA**, TanStack Router, TanStack Query, shadcn/ui + Tailwind v4, TanStack Table, Recharts; admin CRUD için shadcn-admin-kit (Sprint 0 denemesine bağlı).
  - `packages/api-client`: `contracts/openapi` → **Orval** ile TanStack Query hook'ları + Zod şemaları (+ MSW mock'ları → backend bitmeden ekran geliştirme) ([Orval](https://orval.dev/)); elle düzenlenmez (08 §3.a).
  - `packages/tokens`, `packages/ui-core` (§4.2), `packages/ui` (web shadcn bileşenleri).
  - pnpm workspaces (08 §3.b); Expo için gerekirse `nodeLinker: hoisted`.
- **Neden:** (1) mobil yerel yetenek ve store yayınında en olgun JS yolu (EAS; Mac'siz iOS build); (2) agent'lar için en çok veri, React ≥ Angular benchmark'ı ve Gemini + Angular'a dair olumsuz 2026 gözlemi; (3) ekibin React/Expo geçmişi → arayüz modüllerinde gerçek vekillik; (4) API istemcisi, Zod doğrulaması, token'lar ve hüküm mantığı mobil ile web arasında **aynı paket**; (5) Vite SPA ile SSR/RSC tuzakları yok.
- **Alternatif 1 — Angular 22 (web + admin) + Ionic 9/Capacitor 8 (mobil).** **Neden değil:** mobilde WebView UI ve Ionic'in ticari servislerinin kapanmasıyla eklenti/build zincirinin küçük üçüncü taraflara kalması; ekipte Angular vekili yok; Angular'ın agent üstünlüğü benchmark'la gösterilemedi, Gemini'de eski idiom gözlemi var. **Ne zaman seçilir:** spike'ta arayüz sahibi Angular'da belirgin şekilde iyi çıkarsa — o durumda: Angular Material (PrimeNG değil), `ng generate ai-config --tool=gemini` + resmi `GEMINI.md`, Angular MCP, Capawesome barkod + Capgo STT, bulut build için Capawesome Cloud veya Codemagic.
- **Alternatif 2 — Expo Router universal (mobil + web tek app).** **Neden değil:** Stüdyo/admin masaüstü ve veri yoğun; RN-web kenar durumları zayıf agent için tuzak; mobil ekranın web kopyası gerekmiyor.
- **Alternatif 3 — Flutter.** **Neden değil:** web erişilebilirliği (canvas) tez gereksinimine ters; Dart ekipte yok; admin ekosistemi dar.
- **Alternatif 4 — Next.js web.** **Neden değil:** SSR/SEO ihtiyacı yok; App Router server/client sınırı ve önbellek davranışı ek hata yüzeyi.
- **Alternatif 5 — Compose Multiplatform.** **Neden değil:** web Beta, agent verisi en az.

### 5.1 Mobilde kritik yerel yetenekler — önerilen eklentiler
| Yetenek | Öneri | Yedek | Sprint 0 testi |
|---|---|---|---|
| Barkod (EAN-13/8, UPC) | `expo-camera` barcode (formatlar yalnız `ean13, ean8, upc_a, upc_e`) | `react-native-vision-camera` v5 code scanner (tarama bölgesi, köşe noktası) | Gerçek raf ürünleriyle 30 tarama: ilk okuma süresi (medyan, p90), yanlış okuma; düşük ışık; iOS + Android |
| Etiket/fiş fotoğrafı | `expo-camera` (foto) / `expo-image-picker` | VisionCamera | Çözünürlük + dosya boyutu; görsel cihazda kalır mı (gizlilik) |
| Sesli soru (STT) | `expo-speech-recognition`, `requiresOnDeviceRecognition: true` | Türkçe cihazda yoksa: Gizlilik Kapısı arkasında TR sunucuda STT **veya** özellik demo şeridinde kalır (tez §8) | `getSupportedLocales()` → `tr-TR` cihazda var mı (iOS 17+/26, Android 13+) |
| Push (jenerik içerik) | `expo-notifications` + FCM/APNs; Spring doğrudan FCM/APNs'e ya da Expo push servisine | — | Bildirim metninde sağlık verisi yok (lint/test) |
| Çevrimdışı mini önbellek | `expo-sqlite` (kurallar + son katalog) + TanStack Query persist | MMKV | Uçak modunda barkod → yerel hüküm ("Doğrulanamadı" düşüşü) |
| Hassas veri | `expo-secure-store` (anahtar/tokens); sağlık verisi şifreli SQLite | — | Silme/anahtar imhası akışı |
| Erişilebilirlik | RN `accessibilityRole/Label/State`; hüküm = renk + ikon + metin (`ui-core`) | — | VoiceOver/TalkBack ile 5 ana akış |
| Store | EAS Build + EAS Submit; Google Play kapalı test **12 test kullanıcısı × 14 gün** (personal hesap, uygulama başına) ([Play Console](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en)); organizasyon hesabı bu şarttan muaf | — | Play kapalı testini D3'ten çok önce (Şubat) başlatmak; EAS ücretsiz plan build kotası (doğrulanmadı) |

### 5.2 Riskler ve azaltma (React seçimi için)
| Risk | Azaltma |
|---|---|
| Antigravity/Gemini'nin React'te de tutarsız kod üretmesi | Kök + `apps/*/AGENTS.md` (Next.js evals'ta Gemini +13 puan); Expo'nun ürettiği AGENTS.md korunur; kritik ekranlarda Antigravity içinde **Claude Opus**'a geçiş; CI kapıları (typecheck strict, ESLint, test) herkese aynı (08 §3.g) |
| React "ayak tabancaları" (useEffect ile fetch, durum dağınıklığı) | İzinli kütüphane listesi + ESLint (`react-hooks`, `no-restricted-imports`: fetch/axios yalnız `api-client`'ta); React Compiler (doğrulanmadı—Sprint 0'da) |
| Arayüzün kritik iş taşıması | Hüküm/kısıt mantığı **backend + `ui-core`'da**; arayüz yalnız çizer; `ui-core` sahibi ≠ arayüz sahibi olabilir (öneri: platform rolü review eder) |
| Arayüz sahibinin motivasyonu (Angular isteği) | Spike + ortak karar; Angular bilgisi Stüdyo'nun sinyal/zoneless benzeri kavramlarında boşa gitmez; alternatif ADR hazır |
| Expo SDK yükseltme yükü (yılda ~3 SDK) | Proje boyunca tek SDK (56 veya 57), freeze'de yükseltme yok; Expo Skills'in yükseltme akışı Claude/Codex'te |
| Türkçe cihazda STT yok | §5.1 yedekleri; ses zaten demo şeridinde |
| pnpm + Expo çözümleme sorunları | `nodeLinker: hoisted` kaçış yolu; walking skeleton'da (08 §3.f) EAS build ilk hafta denenir |

### 5.3 Riskler (Angular seçilirse — alternatif için hazır)
Capacitor 9 geçişi (Kasım 2026) projenin ortasına denk gelir → 8.x'te kal; barkod/STT/secure storage eklentileri Capawesome/Capgo'ya bağlı → sürüm sabitle; bulut iOS build için Capawesome Cloud/Codemagic ya da Mac; PrimeNG yok; `GEMINI.md` + Angular MCP zorunlu.

### 5.4 Proposal teknoloji tablosu için satırlar
| Katman | Teknoloji | Gerekçe (tek cümle) |
|---|---|---|
| Mobil (iOS + Android) | React Native + Expo (SDK 56, EAS Build/Submit), cihazda ML Kit/VisionKit barkod, cihazda konuşma tanıma | Tek TypeScript kod tabanından iki store; barkod ve ses cihazda işlenir (gizlilik). |
| Web + Admin | React 19 + Vite, TanStack Router/Query/Table, shadcn/ui, Recharts | Giriş arkası, veri yoğun planlama ve denetim ekranları için olgun, erişilebilir bileşen ekosistemi. |
| Ortak katman | OpenAPI → üretilmiş TypeScript istemcisi (Orval + Zod), tek kaynaklı tasarım token'ları ve hüküm rozeti paketi | Mobil, web ve admin aynı API sözleşmesini ve aynı güvenlik-kritik gösterimi kullanır. |

---

## 6. Doğrulanamayanlar / açık
- **EAN-13 tarama gecikmesi** için hiçbir çatıda yayımlanmış sayısal ölçüm bulamadım; üçünde de tarama yerel ML Kit/VisionKit'te koştuğu için farkın çatıdan değil kütüphane/ayar seçiminden gelmesi beklenir (çıkarım). Sprint 0 ölçümü şart.
- Türkçe'nin iOS SpeechTranscriber / Android offline modelde cihazda desteklenmesi — doğrulanmadı.
- React Native Evals model bazlı skorları — çekilemedi.
- Angular Web Codegen Scorer'ın framework karşılaştırmalı sonucu yok; "97+" ekip beyanı.
- Antigravity kota ayrıntıları (Mart 2026 değişikliği) ikincil kaynak; Claude modellerinin öğrenci planında ne kadar kullanılabildiği denenmeli.
- EAS ücretsiz plan build kotası, Apple Developer Program ücreti ve hesap türü (kişisel/organizasyon) — Sprint 0'da resmi sayfadan teyit.
- `react-diff-viewer-continued`, React Compiler'ın Expo SDK 56'daki durumu — doğrulanmadı.

## 7. Karar için sorular (Levent + arayüz sahibi)
1. 2 günlük spike yapılsın mı (öneri: evet, 19 Ekim'den önce)? Ölçüt: build/lint/test hatası, düzeltme turu, süre, arayüz sahibinin memnuniyeti.
2. Arayüz sahibi Antigravity'de kritik işlerde Claude Opus'u kullanabilir mi (kota/plan)?
3. `packages/ui-core` (hüküm rozeti mantığı) kimin sahipliğinde: arayüz sahibi mi, platform rolü mü (öneri: kod arayüz sahibinde, zorunlu review platform rolünde)?
4. Google Play: kişisel hesap mı (12 × 14 gün kapalı test), organizasyon hesabı mı (muaf, D-U-N-S gerekir — doğrulanmadı)?
