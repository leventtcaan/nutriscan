> **Ham araştırma — ekiple netleştirilmedi, 2026-09-25**
> Kapsam: barındırma (TR), öğrenci kredileri, dağıtım topolojisi, gözlemlenebilirlik, push/e-posta, maliyet, ADR taslakları.
> Kur: **1 USD ≈ 48,85 TL** (25.09.2026 piyasa, [Investing](https://tr.investing.com/currencies/usd-try)). Fiyatlar 25.09.2026'da sağlayıcı sayfasından okundu. "(doğrulanmadı)" işaretli satırlar tahmin ya da ikincil kaynaktır.
> Bağlı dosyalar: `01-mevzuat-risk.md` §1.4 (yurt dışı aktarım) · `05-sistem-fmea.md` ALT-06/07/11/12/15, K06/K15/K19, RPO/RTO · `09-evren-ve-board-notu.md` · `07-tez-v5.md`.

---

## 0. Kısa hüküm

1. **Hiperskalerlerin Türkiye bölgesi yok.** Google Cloud–Turkcell bölgesi Ankara'da, inşaat 2026 Q1'de başlıyor, tam kapasite **2028**. Proje takvimine yetişmez. Azure'un TR bölgesi duyurulmadı. AWS'nin de TR bölgesi yok. DigitalOcean, Hetzner ve **Contabo'nun TR lokasyonu yok.** Contabo 9 bölgede çalışıyor (DE, UK, ABD, SG, JP, AU, IN). Liderin Contabo VPS'i hangi bölgede olursa olsun **yurt dışında**.
2. **Türkiye'de yönetilen PostgreSQL + S3 veren tek doğrulanmış seçenek Huawei Cloud TR-Istanbul** (`tr-west-1`, 3 AZ; RDS for PostgreSQL pgvector 0.8.x destekliyor). Fiyat konsolda görünüyor, dışarıdan okunamadı.
3. **Öneri:** Türk VPS'lerde **self-host** kurulum yapılır. Birincil: **Radore İstanbul** (ISO 27001). Yedek/DR: **Netinternet İlkbyte, Denizli** (ayrı sağlayıcı, ayrı şehir, ISO 27001/27701/22301). Kurulum Docker Compose ile. Beta dönemi toplam **≈ 60–75 USD/ay (≈ 3.000–3.700 TL, KDV dahil)**.
4. **Contabo VPS'i ve Azure öğrenci kredisi yalnızca sentetik veriyle** kullanılır (staging/demo/CI). Gerçek hane verisi, yedekler, loglar, trace'ler ve crash raporları asla yurt dışına çıkmaz.

---

## 1. Türkiye'de barındırma seçenekleri

### 1.1 Karşılaştırma tablosu (hedef: 2–4 vCPU, 4–8 GB RAM, 80+ GB SSD)

| Sağlayıcı | TR veri merkezi | Aylık fiyat (25.09.2026) | Yönetilen PG | S3 nesne depolama | Yedek/snapshot | ISO 27001 | Faturalama | Not |
|---|---|---|---|---|---|---|---|---|
| **Radore** | Evet, İstanbul Levent (Metrocity), "Tier III standardında" (Uptime sertifikası yok) | **Disk-Elite 4 vCPU/8 GB/300 GB NVMe: 29,50 USD** + KDV · Disk-Advance 2/4/200: 17 USD · RAM-Advance 2/16/100: 21 USD · RAM-Elite 4/32/150: 40 USD | Sayfada yok | Sayfada yok | "Otomatik yedekleme" var | Evet (2015'ten beri) | USD fiyat, TL karşılığı; kart (doğrulanmadı) | [radore.com/services/cloud-server](https://radore.com/services/cloud-server) · [veri merkezi](https://radore.com/data-center) |
| **Netinternet / İlkbyte Cloud** | Evet, **Denizli** (PAÜ Teknokent, kendi DC'si) | Cloud II 3/4/40: 10,99 USD · **Cloud III 4/8/80: 21,99 USD** · Cloud IV 4/12/120: 32,99 USD (saatlik faturalama) | Yok | Yok (yönetilen yedek/DR hizmeti var) | Sayfada belirtilmemiş | **Evet** + ISO 27701 (kişisel veri), 22301 (iş sürekliliği) | USD; KDV durumu belirsiz | API var ([apidocs.ilkbyte.com](https://apidocs.ilkbyte.com)) · [ilkbyte](https://www.ilkbyte.com/kiralik-sunucu-paketlerimiz/cloud-sunucu) · [netinternet.tr](https://www.netinternet.tr/) |
| **Natro XCloud** | DC konumu sayfada yok (doğrulanmadı) | Medium 2/4/60: 488 TL · Large 2/6/100: 635 TL · **Pro 4/8/200: 1.465 TL** (KDV dahil) | Yok | Yok | **Ücretsiz yedek + snapshot** | Sayfada yok | TL | [natro.com](https://www.natro.com/sunucu-kiralama/vps-cloud-server) |
| **Veridyen PRO Bulut** | Sayfada yok (doğrulanmadı) | 2/8/120 NVMe: **1.403 TL/ay** (en küçük paket) | Yok | Yok | Ek hizmet | ISO 27001 + 9001 (firma beyanı) | TL | [veridyen.com](https://www.veridyen.com/sunucu/pro-bulut-sunucu) |
| **Turhost** | Normal "Sanal Sunucu" ürününde konum belirsiz. Ayrıca "VPS **TR** Sunucu" ürünü var; bu, diğer ürünlerin yurt dışında olabileceğine işaret ediyor | Sanal Sunucu 2/4/40 NVMe: 18,99 USD (kampanyada 9,99) + KDV | Yok | Yok | ? | ? | USD/TL, taksit | [turhost](https://www.turhost.com/sunucu/sanal-sunucu/) · [VPS TR](https://www.turhost.com/sunucu/vps-tr-sunucu/) |
| **İsimtescil VDS** | "Türkiye" | VDS-Super-Eko 2/4/40: 14,99 USD · **VDS-S 4/8/80: 25,99 USD** | Yok | Yok | Destek paketine göre | ? | USD | [isimtescil.net/sunucu](https://www.isimtescil.net/sunucu) |
| **Netlen** | İstanbul, "Tier III" | Cloud-3 2/4/40: 356 TL · **Cloud-4 2/8/70: 578 TL** | Yok | Yok | Snapshot var | Beyan yok | TL, saatlik | En ucuzu. Kurumsal güvence zayıf. [netlen](https://www.netlen.com.tr/cloud-server) |
| **Turkcell Bulut** (Sanal Sunucu / Sanal Veri Merkezi) | Evet: İstanbul, Kocaeli, Ankara | **Liste fiyatı yok**, teklif ya da kurumsal portal ile; günlük ücretlendirme | Yalnız MS SQL kiralama anılıyor | Sayfada yok | ? | Turkcell kurumsal (doğrulanmadı) | Kurumsal | [docs.turkcellbulut.com](https://docs.turkcellbulut.com/articles/sanalsunucu/vps-gs.html) · [SVM](https://www.turkcell.com.tr/kurumsal/dijital-is-servisleri/bulut-depolama/sanal-veri-merkezi) |
| **Türk Telekom Bulut** | Evet (konumlar açıklanmamış) | Sanal Veri Merkezi "450 TL/ay'dan başlayan"; sanal sunucu yedeği 340 TL'den | Yok | **Var, "proje bazlı" fiyat** | Yedekleme/replikasyon ürünleri var | ? | **TL, kredi kartı, saatlik** (AA haberi) · **30 gün ücretsiz deneme** | [turktelekombulut.com/urunler](https://turktelekombulut.com/urunler) · [AA](https://www.aa.com.tr/tr/isdunyasi/guncel/turk-telekom-bulut-ile-tum-bulut-servisleri-tek-platformda/676730) |
| **Huawei Cloud TR-Istanbul** | Evet, `tr-west-1`, 3 AZ (2023'te 78 servisle açıldı; Ankara'da DR sitesi) | **Konsolda. Dışarıdan doğrulanamadı** | **Evet: RDS for PostgreSQL, pgvector 0.8.0 (PG13–17) / 0.8.2 (PG18)** | **Evet: OBS** | Evet (yönetilen) | Huawei Cloud genel (doğrulanmadı) | Kullandıkça öde; kart/USD (doğrulanmadı) | [pgvector listesi](https://support.huaweicloud.com/intl/en-us/usermanual-rds-pg/rds_09_0045.html) · [Xinhua 2023](https://english.news.cn/20230713/d27b34a162fd493ab86a3f5b76e99181/c.html) · [TR fiyat](https://www.huaweicloud.com/intl/tr-tr/pricing.html) |
| **Bulutistan** | Evet, 5 lokasyon (Nutanix) | **Teklif ile**, TL fiyat modeli | ? | STaaS var | Var | CSA STAR (ISO 27001 doğrulanmadı) | TL, kurumsal satış | [bulutistan.com](https://bulutistan.com/en/cloud-server/) |
| **CloudRUX** | İstanbul Ümraniye | Teklif | PostgreSQL "kurulum/bakım" hizmeti | S3 var, fiyat yok | ? | ISO 27001 | ? | [cloudrux](https://www.cloudrux.com/tr/bulut/s3) |
| **Google Cloud TR** | **Yok (Ankara, 2028 hedefi)** | — | — | — | — | — | — | [Tech Capital](https://thetechcapital.com/turkcell-google-cloud-plan-sovereign-cloud-region-in-ankara-by-2028/) · [AA](https://www.aa.com.tr/en/economy/turkcell-google-cloud-to-build-hyperscale-data-centers-in-turkiye/3780306) |
| **Azure** | **Yok** (TR bölgesi duyurulmadı; Suudi Arabistan 2026 Q4) | — | — | — | — | — | — | [MS Community](https://techcommunity.microsoft.com/discussions/azurepartners/new-azure-region---turkey/4003617) |
| **DigitalOcean / Hetzner** | **Yok** (DO'da TR talebi "fikir" olarak duruyor) | — | — | — | — | — | — | [DO ideas](https://ideas.digitalocean.com/infrastructure/p/turkey-data-center) · [Hetzner DC](https://www.hetzner.com/unternehmen/rechenzentrum/) |
| **Contabo** | **Yok.** EU trafiği Almanya'dan (5 DC), ayrıca UK, ABD×3, SG, JP, AU, IN | Core VPS 5,50 €'dan | — | Var (EU/ABD) | — | — | — | [contabo.com/en/locations](https://contabo.com/en/locations/) |

**Öğrenci/akademik indirim:** Taranan TR sağlayıcıların hiçbirinde yayımlanmış öğrenci indirimi bulunamadı. TT Bulut'un 30 günlük ücretsiz denemesi demo için kullanılabilir. **(Soru)** Akdeniz Üniversitesi BİDB'nin bitirme projelerine sunucu verip vermediği danışmana sorulmalı. Veri TR'de kalır ve ücretsizdir. Karşılığında erişim ve kontrol kısıtlı olabilir.

**Levent'in Contabo VPS'i:** Bölgesi `my.contabo.com` → VPS → Region alanında ya da sunucuda `curl ipinfo.io` ile öğrenilir. Hangi bölge çıkarsa çıksın TR dışındadır.

### 1.2 Neden yönetilen DB değil de self-host PostgreSQL?
- Taranan TR VPS sağlayıcılarının hiçbirinde self-servis yönetilen PostgreSQL yok. Tek istisna Huawei TR (pgvector'lı RDS).
- Huawei RDS'in fiyatı konsol dışında doğrulanamadı. Hesap açma ve ödeme adımları (uluslararası kart, kurumsal doğrulama) öğrenci ekibi için belirsiz. Bir ekip üyesi Huawei konsolunda 1 saatlik keşif yapıp gerçek fiyatı yazarsa bu karar yeniden açılır (bkz. ADR-H2).
- 20–40 hanelik beta'da DB küçük kalır (tahmin: < 5 GB). Self-host PG + pgBackRest ile RPO 15 dk rahatça tutturulur.

---

## 2. Öğrenci kaynakları ve KVKK sınırı

**GitHub Student Developer Pack (resmi sayfa, 25.09.2026):** [education.github.com/pack](https://education.github.com/pack)
- **Azure:** 100 USD kredi + 25+ ücretsiz servis (18+). **TR bölgesi yok.**
- **Heroku:** 24 ay boyunca aylık 13 USD (ABD/AB).
- **DigitalOcean artık pakette yok.** İkincil kaynağa göre 200 USD'lik kredi 1 Ağustos 2026'da sona erdi ([aistudentdiscount](https://aistudentdiscount.com/digitalocean-github-student-developer-pack-credits/)). Resmi sayfada listelenmediği teyit edildi.
- Sentry (50K hata/ay), Datadog Pro (2 yıl), New Relic, **Doppler Team** (sır yönetimi), MongoDB 50 USD, Appwrite, LocalStack. Alan adı: Namecheap .me 1 yıl, .TECH 1 yıl, Name.com.

**Hangi bileşen nerede olabilir:**

| Bileşen | Yurt dışı olabilir mi? | Koşul |
|---|---|---|
| Kaynak kod, CI derleme/test (GitHub Actions hosted runner), konteyner imajları (GHCR) | **Evet** | Testler yalnız sentetik fikstürle çalışır. Repoda gerçek veri, dump ya da log yok (K15/K19). |
| Staging / demo ortamı (Contabo, Azure kredisi) | **Evet, yalnız sentetik veriyle** | Seed script'iyle üretilmiş sahte haneler. Ekip üyelerinin gerçek alerji bilgisi dahil **hiçbir gerçek profil** girilmez. Prod dump'ı staging'e **asla** taşınmaz. Staging'de kayıt ekranı kapalı ya da davetle açılır, çünkü dışarıdan gerçek kullanıcı gelirse veri yurt dışına çıkmış olur. |
| Proje yönetimi (Azure Boards / GitHub Projects) | Evet | Issue'lara gerçek kullanıcı verisi, ekran görüntüsü ya da log yapıştırılmaz. |
| **Prod DB, nesne depolama (etiket/fiş görseli), Redis** | **Asla** | TR. |
| **Yedekler** (şifreli olsalar bile) | **Asla** | Şifreli kişisel veri de kişisel veridir (muhafazakâr yorum). İkinci konum TR'de başka bir sağlayıcı olur. |
| **Log, trace, metrik, crash raporu, LLM trace'i** | **Asla** (içerik sızabilir) | Self-host, TR. |
| Sentry SaaS / Datadog / New Relic (öğrenci paketi) | **Prod için hayır** | Yalnız staging'de denenebilir. Prod'da kullanılırsa K06 ihlali riski doğar. |
| Push (FCM/APNs) | Zorunlu olarak yurt dışı | Jenerik içerik (S18), data-only + kimlik doğrulamalı çekme (§5). |
| LLM | TR (EVREN) | Yurt dışı LLM yalnız K06 maskeleme kapısından geçerek yedek yol olarak kullanılır. |

---

## 3. Dağıtım topolojisi

### 3.1 Diyagram (metin)

```
                         [ Kullanıcı: mobil (RN) / web / admin ]
                                        │ HTTPS (TLS: Let's Encrypt, Caddy)
                                        │ DNS: yalnız DNS (CDN/proxy YOK — Cloudflare turuncu bulut kapalı)
                                        ▼
┌──────────────────────── TR · Radore İstanbul ─────────────────────────┐
│ prod-app  (4 vCPU / 8 GB / 300 GB NVMe)       docker compose          │
│  caddy ── web+admin statik ── /api → spring-boot (modüler monolit)    │
│  postgres 17 + pgvector   redis (yalnız önbellek/kuyruk, kalıcı değil)│
│  garage|seaweedfs (S3 API, görseller: kısa TTL + lifecycle)            │
│  otel-collector (agent) · node-exporter · pgbackrest (WAL push)        │
│  nftables ÇIKIŞ allowlist: EVREN, FCM/APNs, SMTP(TR), OFF, GHCR,       │
│    LE ACME, OS repo  (DOCKER-USER zinciri)                             │
└──────┬──────────────────────────────┬─────────────────────────────────┘
       │ OTLP (WireGuard)             │ WAL + tam yedek (SSH/pgBackRest; yedek sunucusu ÇEKER)
       ▼                              ▼
┌──── TR · Radore İstanbul ────┐   ┌──── TR · İlkbyte Denizli (başka sağlayıcı/şehir) ────┐
│ ops (2 vCPU / 16 GB / 100 GB)│   │ backup+DR (3–4 vCPU / 4–8 GB)                         │
│ Grafana · Prometheus · Loki  │   │ pgBackRest repo (AES-256, 14 gün PITR)                │
│ Tempo · Alertmanager         │   │ restic: nesne depolama + config (günlük)              │
│ GlitchTip (web+mobil crash)  │   │ "sıcak kurtarma": docker + compose hazır → RTO ≤ 4 sa │
│ Langfuse v3 (LLM trace)      │   │ prod'un bu makinede SİLME yetkisi yok (pull modeli)   │
└──────────────────────────────┘   └───────────────────────────────────────────────────────┘

┌──── YURT DIŞI (yalnız sentetik) ─────────────────────────────────────┐
│ GitHub (repo, Actions, GHCR imajları) · Contabo VPS = staging/demo  │
│ Azure Boards · FCM/APNs (jenerik payload)                           │
└──────────────────────────────────────────────────────────────────────┘
 LLM: EVREN (TR) ← yalnız prod-app'ten, K06 kapısından
```

**Minimum varyant (bütçe sıkışırsa):** ops kutusu kaldırılır. Grafana `otel-lgtm` tek konteyneri (512 MB–2 GB) ve GlitchTip (~512 MB) prod-app'e alınır. Langfuse ertelenir; LLM çağrıları OTel span'i + Postgres'te `llm_call` tablosu olarak tutulur. 8 GB RAM'de sığar ama sıkı olur (§4).

### 3.2 Docker Compose mu, k3s mi?
**Compose.** Tek düğüm var (prod-app), 3 kişilik ekip var, kimse ops'a tam zamanlı bakamaz. k3s'in getirdikleri (rolling update, self-heal, çok düğüm) tek düğümde çok az kazanç sağlıyor. Buna karşın maliyeti yüksek: ingress/cert-manager/PVC/Helm öğrenme yükü, etcd/sqlite bakımı, hata ayıklama yüzeyi. Compose'da `healthcheck` + `restart: unless-stopped` + blue/green için Caddy upstream değişimi (iki app konteyneri, ~10 sn kesinti ya da sıfır kesinti) beta için yeterli. **Ne zaman k3s:** 2+ uygulama düğümü gerekirse ya da ekip K8s öğrenmeyi bilinçli olarak öğrenme hedefi yaparsa (öğrenme hattı konusu olabilir, prod'da değil).

### 3.3 CI/CD
- **GitHub Actions (hosted runner):** derleme, birim ve entegrasyon testleri (Testcontainers + sentetik veri), gitleaks, SBOM/Trivy, imajı GHCR'a push. Bu adımların hepsinde veri yok, dolayısıyla yurt dışı sorun değil.
- **Prod'a dağıtım:** `production` environment + zorunlu reviewer (2 kişiden 1 onay). İş SSH ile prod'a bağlanır. SSH anahtarı `ForceCommand /opt/deploy/deploy.sh <tag>` ile tek komuta kilitlidir. Script sırayla: imajı çeker, Flyway migration'ı ayrı konteynerde çalıştırır, yeni app'i kaldırır, healthcheck'i bekler, Caddy'yi yeni upstream'e çevirir, eski konteyneri durdurur. Başarısız olursa önceki tag'e döner.
- **Self-hosted runner kullanılmaz.** Prod'daki bir runner PR kodunu prod ağında çalıştırır; kötü niyetli ya da hatalı bir PR prod'a erişir. Tek istisna: CI'da gerçek TR kaynağına erişim gerekirse (şu an gerekmiyor) runner ayrı bir TR VM'de ve yalnız `main` için çalışır.
- Alternatif (daha güvenli ama daha karmaşık): **pull tabanlı dağıtım.** Sunucu GHCR'daki imzalı tag'i izler (cosign doğrulaması). Böylece CI'ın prod'a hiç anahtarı olmaz. Beta sonrası değerlendirilir.

### 3.4 Sır yönetimi (FMEA ALT-07 → ADR)
- **SOPS + age:** `deploy/secrets.prod.enc.yaml` repoda şifreli durur. age özel anahtarı yalnız prod-app'te (`/etc/nutriscan/age.key`, 0400) ve iki ekip üyesinin parola yöneticisinde bulunur. CI'da prod sırrı yoktur; yalnız deploy SSH anahtarı ve GHCR token'ı vardır.
- Ortam başına ayrı sır tutulur, staging ≠ prod. 90 günde bir rotasyon yapılır. gitleaks pre-commit + CI + GitHub push protection açık tutulur.
- Doppler (öğrenci paketinde ücretsiz) daha rahat ama ABD SaaS'ı; sır kişisel veri değil, yine de kontrol düzlemi yurt dışına çıkar. Karar: SOPS; Doppler yalnız staging için isteğe bağlı.

### 3.5 TLS ve alan adı
- Caddy ile otomatik Let's Encrypt (ACME). HSTS açık. `api.`, `app.` ve `admin.` alt alan adları ayrı. Admin paneli ek olarak IP allowlist ya da WireGuard arkasında tutulur.
- **CDN/proxy yok.** Cloudflare proxy (turuncu bulut) TLS'i yurt dışında sonlandırır ve sağlık verisi Cloudflare'den geçer; bu, yurt dışına aktarım demektir. Cloudflare yalnız DNS olarak kullanılabilir (gri bulut). Statik web/admin dosyaları Caddy'den servis edilir. Beta ölçeğinde CDN gerekmez.
- Alan adı: `.com.tr` (TRABİS, belge şartı 2022'de kalktı; fiyat doğrulanmadı, ~yıllık birkaç yüz TL) ya da `.app/.com` (~10–15 USD/yıl, doğrulanmadı). Öğrenci paketindeki `.me` / `.tech` 1 yıl ücretsiz ama 2. yıl ücretli. Canlı Haziran 2027 ve sonrası için kalıcı bir alan adı seçilmeli.

### 3.6 Yedekleme ve felaket kurtarma (hedef: RPO ≤ 15 dk, RTO ≤ 4 saat)

| Veri | Yöntem | RPO | Konum |
|---|---|---|---|
| PostgreSQL | **pgBackRest**: sürekli WAL arşivi (`archive_timeout=60s`), haftalık tam + günlük diff yedek, AES-256-CBC repo şifrelemesi, 14 gün PITR | **≈ 1–2 dk** | İlkbyte Denizli (repo host). Radore'nin kendi "otomatik yedeği" ek katman olarak kullanılır. |
| Nesne depolama (görseller) | Kısa ömürlü (TTL; tasarımda ≤ 72 saat önerilir, veri politikası ADR'ı ile netleşir). Yedeklenmez ya da restic ile günlük yedeklenir. Kayıp kabul edilebilir, kullanıcı yeniden tarar. | 24 sa / kabul | İlkbyte |
| Redis | Yedek yok (önbellek + yeniden üretilebilir kuyruk) | — | — |
| Config, compose, Caddyfile | Git (repo) + SOPS | 0 | GitHub |
| Hane başı veri anahtarları (crypto-shredding, ALT-06) | Ayrı ve ayrıca şifreli yedek. Anahtar silindiğinde yedekteki veri okunamaz. | 15 dk | İlkbyte, DB'den ayrı dizin/anahtar |

- **Fidye yazılımına karşı:** Yedek sunucusu prod'dan **çeker**. pgBackRest repo host modunda prod'un repo üzerinde silme yetkisi yoktur. Ek olarak restic `--append-only` (rest-server) kullanılır.
- **DR runbook'u (RTO ≤ 4 sa):** (1) İlkbyte DR kutusunda `pgbackrest restore --type=time` çalıştırılır. (2) Compose ile app, Caddy ve S3 ayağa kaldırılır. (3) DNS A kaydı değiştirilir (TTL 300 sn). (4) Doğrulama sorguları çalıştırılır. Tahmini süre 1–2 saat. Tatbikat **aylık** yapılır (FMEA K-tatbikat), süre ölçülüp kayda geçer.
- İzleme: "yedek yaşı" metriği yayınlanır. 2 gün yedek yoksa sayfa alarmı düşer (FMEA OPS-03).

---

## 4. Gözlemlenebilirlik (self-host, TR)

| Bileşen | Kaynak ihtiyacı | Tek VPS'e sığar mı | Kaynak |
|---|---|---|---|
| **Grafana otel-lgtm** (Collector + Prometheus + Tempo + Loki + Pyroscope + Grafana, tek konteyner) | 512 MB istek / 2 GB limit | Evet. **Grafana "dev/demo/test için" diyor**; beta ölçeğinde yeterli, ama retention/kalıcı volume ayarı elle yapılmalı. | [github](https://github.com/grafana/docker-otel-lgtm) |
| Grafana + Prometheus + Loki + Tempo (ayrı konteynerler) | ~1,5–3 GB toplam (tahmin, doğrulanmadı) | Evet (ops kutusu) | — |
| **SigNoz** (ClickHouse tabanlı, tek paket) | Kesin alt sınır 4 GB, pratikte 8 GB; AVX2 gerekli | Tek başına yarım kutu kaplıyor | [SigNoz docs](https://signoz.io/docs/install/docker/) · [sumguy](https://sumguy.com/self-host-signoz/) |
| **Langfuse v3** (web, worker, Postgres, ClickHouse, Redis, MinIO/S3) | **4 vCPU / 16 GB önerilen**, 8 GB "alt sınır"; ClickHouse tek başına 8 GB istiyor; 100 GB disk | **prod-app'e sığmaz.** Ops kutusunda (16 GB) düşük hacimle çalışır; CPU 2 vCPU'da darboğaz olabilir (ölçülecek). | [Langfuse](https://langfuse.com/self-hosting/deployment/infrastructure/containers) · [v2→v3 tartışması](https://github.com/orgs/langfuse/discussions/5785) |
| **Sentry self-host** | **Min 16 GB RAM + 16 GB swap, 4 CPU, 40+ konteyner**; boş kurulum ~13 GB | **Hayır**, bu ölçek için aşırı | [DeepWiki](https://deepwiki.com/getsentry/self-hosted/3.1-system-requirements) · [issue #3467](https://github.com/getsentry/self-hosted/issues/3467) |
| **GlitchTip** (Sentry SDK uyumlu, Django, 4 konteyner) | ~512 MB | **Evet** | [selfhosting.sh](https://selfhosting.sh/compare/glitchtip-vs-sentry/) |

**Öneri:** OTel Java agent (Spring Boot) → Collector → Prometheus/Loki/Tempo + Grafana. Hata izleme için **GlitchTip**; web ve mobil Sentry SDK'ları DSN olarak GlitchTip'i gösterir. **Langfuse v3** ops kutusunda çalışır. Kaynak yetmezse LLM çağrıları OTel GenAI semantik konvansiyonlarıyla Tempo'ya ve Postgres `llm_call` tablosuna yazılır, Langfuse ertelenir.
**(Doğrulanmadı)** GlitchTip'in native (iOS/Android NDK) crash desteği Sentry'den zayıf olabilir. RN JS hataları sorunsuz geçer; native çökme sembolikasyonu beta öncesi test edilmeli.

**Sağlık verisinin gözlem kanallarına sızmaması için kurallar (K06, ALT-11, ALT-15):**
1. Log ve trace **allowlist** ile çalışır. Span attribute'larında yalnız `householdId` (opak UUID), `traceId`, ürün barkodu, hüküm kodu bulunur. Alerji, kısıt, üye adı, serbest metin, LLM prompt gövdesi **yazılmaz**. Logback'te maskeleme deseni uygulanır, OTel Collector'da `attributes/redaction` processor'ı çalışır.
2. LLM prompt/yanıt içeriği yalnız TR'deki Langfuse'a gider, saklama süresi 30 gün (ya da kısıtlanmış). Prompt'ta sağlık alanı zaten yoktur; bu durum K06 kapısıyla garanti altına alınır.
3. Mobil crash SDK'sında `sendDefaultPii=false` ayarlanır. `beforeSend` / `beforeBreadcrumb` içinde istek/yanıt gövdesi, ekran adı parametreleri, kullanıcı e-postası ve `extra` alanları temizlenir. Session replay kapalıdır. `setUser` yalnız opak id alır.
4. **Crashlytics / Sentry SaaS / Datadog / New Relic prod'da kullanılmaz.** Kullanılmak zorunda kalınırsa yalnız stack trace ve cihaz modeli gönderilir; custom key/log kullanılmaz. Bu durum veri akış envanterine yazılır.
5. CI kapısı: log/telemetri çağrılarında sağlık sözlüğü (alerjen adları, "çölyak", "gluten" vb.) grep ile taranır. Nightly kanarya testi: sentetik bir "fındık" profili tarama yapar, ardından Loki/Tempo/GlitchTip'te "fındık" araması **0 sonuç** dönmelidir.

---

## 5. Mobil push ve e-posta

**Push (FCM/APNs, zorunlu yurt dışı):**
- Payload **data-only + jenerik** olur: `{"t":"list_update"}`. Görünen metin "Listende bir güncelleme var" gibidir. Ad, üye, kısıt, ürün–alerjen eşleşmesi taşımaz (S18, ALT-12). Uygulama açılınca içerik kimlik doğrulamalı API'den çekilir.
- **Expo Push Service** kullanılırsa o da ABD'de bir ara katmandır, dolayısıyla aynı kural geçerlidir. Mümkünse FCM/APNs'e backend'den doğrudan gönderilir.
- **Açık soru (hukuk):** Push token'ı cihaz tanımlayıcısıdır, yani kişisel veri sayılabilir. Google ve Apple'a düzenli aktarım yapılmış olur. Sağlık verisi değil, ama m.9 kapsamında aydınlatma metnine yazılmalı. Google/Apple'ın TR standart sözleşme durumu doğrulanmadı (bkz. 01-mevzuat §1.4).
- Çıkışta ve hesap silmede token iptal edilir. İdempotency key, günlük üst sınır ve devre kesici uygulanır (ALT-12).

**İşlem e-postası (doğrulama, şifre sıfırlama):**
E-posta adresi sağlık verisi değildir ama kişisel veridir. Yurt dışı SaaS'lar (SendGrid, Mailgun, Postmark, SES) m.9 yükü getirir. **TR'de SMTP tercih edilir.**

| Seçenek | Konum | Fiyat (25.09.2026) | Not |
|---|---|---|---|
| **SenderTR** (Alastyr Telekomünikasyon A.Ş., İzmir) | "Tüm sunucularımız Türkiye sınırlarında" (beyan) | **İlk 1.000 e-posta ücretsiz**; 10.000 kredi 1.799 TL (süresiz kredi) | SMTP relay (587) + REST API. **Beta aşamasında bir ürün**, kesinti riski var. [sendertr.com](https://sendertr.com/) |
| Alastyr / İsimkayıt / SunucuPARK kurumsal mail SMTP | TR (Alastyr İzmir DC beyanı) | Kurumsal mail paketi (fiyat doğrulanmadı) | Toplu gönderim için değil, düşük hacim için yeterli. [alastyr](https://www.alastyr.com/hosting/email-hosting) |
| Uzman Posta | TR | Teklif | Kurumsal. [uzmanposta.com](https://uzmanposta.com/) |
| Self-host Postfix (prod-app) | TR | 0 | **Önerilmez.** Yeni VPS IP'sinin itibarı düşük, Gmail/Outlook spam'e atar, bakım yükü getirir. |

Beta hacmi çok düşük (40 hane × birkaç e-posta). SenderTR'nin ücretsiz 1.000 kredisi büyük ihtimalle beta'yı karşılar. Yedek olarak kurumsal mail SMTP'si tutulur. SPF, DKIM ve DMARC (`p=quarantine`) şart. E-posta içeriği de jenerik olur ("Şifre sıfırlama bağlantın"); içinde sağlık bilgisi bulunmaz.

---

## 6. Önerilen barındırma ve maliyet

### 6.1 Birincil ve yedek
- **Birincil (prod-app + ops): Radore İstanbul.** ISO 27001 (2015'ten beri), İstanbul Levent DC, NVMe, 4/8/300 paketi 29,50 USD. Otomatik yedek dahil. Fiyat/disk oranı iyi (300 GB). USD fiyatlı; TL kur riski var.
- **Yedek/DR: Netinternet İlkbyte, Denizli.** Farklı şirket, farklı şehir (İstanbul deprem riskine karşı coğrafi ayrım). ISO 27001 + **27701** (kişisel veri yönetimi) + **22301** (iş sürekliliği). API var, saatlik faturalama. DR tatbikatında makineyi saatlik açıp kapatmak ucuz.
- **Plan B (birincil yerine):** İlkbyte Cloud III (4/8/80, 21,99 USD) birincil olur, Radore yedek olur. Disk küçük (80 GB), ama DB küçük olduğu için yeter.
- **Plan C (ops yükünü azaltmak için):** Huawei Cloud TR-Istanbul (yönetilen PG + pgvector + OBS). Fiyat konsolda doğrulanırsa değerlendirilir.
- **TL'yle ve kurumsal fatura isteyen bir durum çıkarsa** (üniversite ödüyorsa vb.): Türk Telekom Bulut ya da Turkcell Bulut; teklif alınmalı.

### 6.2 Aylık maliyet tablosu (1 USD = 48,85 TL; KDV %20)

**A) Geliştirme + demo dönemi (Ekim 2026 – Mart 2027; yalnız sentetik veri)**

| Kalem | Nerede | USD/ay | TL/ay |
|---|---|---|---|
| Staging/demo (sentetik) | Liderin mevcut Contabo VPS'i | 0 (zaten ödeniyor) | 0 |
| Yedek staging (Contabo yetmezse) | Azure for Students 100 USD kredi | 0 | 0 |
| TR "duman testi" kutusu (isteğe bağlı; Mart'ta prod provası) | İlkbyte Cloud II, saatlik | ~0–11 | ~0–540 |
| CI, repo, GHCR, Boards | GitHub Free / Azure DevOps (5 kullanıcı ücretsiz) | 0 | 0 |
| LLM (EVREN) | TR | **0 (1 Kasım'a kadar); sonrası bilinmiyor** | ? |
| Alan adı | — | ~1 (yıllık ~12 USD / 12, doğrulanmadı) | ~50 |
| **Toplam** | | **≈ 1–12 USD** | **≈ 50–600 TL** |

**B) Beta + jüri dönemi (Nisan – Haziran 2027; gerçek veri, 20–40 hane)**

| Kalem | Paket | USD/ay (KDV hariç) | Not |
|---|---|---|---|
| prod-app | Radore Disk-Elite 4/8/300 | 29,50 | |
| ops (gözlem + GlitchTip + Langfuse) | Radore RAM-Advance 2/16/100 | 21,00 | Minimum varyantta 0 |
| backup + DR | İlkbyte Cloud II 3/4/40 (repo) → tatbikatta geçici Cloud III | 10,99 (+ saatlik tatbikat ~1) | 40 GB diski DB büyüklüğüne göre izlenmeli |
| E-posta | SenderTR ücretsiz 1.000 | 0 | Aşılırsa bir kerelik 1.799 TL |
| Push | FCM/APNs | 0 | Apple Developer 99 USD/yıl ayrı kalem (iOS yayını için) |
| LLM | EVREN | ? | Fiyat 1 Kasım sonrası öğrenilecek |
| Alan adı | — | ~1 | |
| **Ara toplam** | | **≈ 62,5 USD** | |
| **KDV dahil** | | **≈ 75 USD ≈ 3.650 TL/ay** | Kişi başı ≈ 1.220 TL/ay |
| **Minimum varyant** (ops yok, Langfuse yok) | Radore 29,50 + İlkbyte 10,99 + ~1 | **≈ 50 USD ≈ 2.430 TL/ay (KDV dahil)** | |

3 aylık beta + jüri toplamı: **≈ 7.300–11.000 TL**. Haziran sonrası "canlıda kalma" aynı tabloyla devam eder.
**Fiyat riski:** Radore ve İlkbyte USD fiyatlı. TL yıllık %20–30 değer kaybederse bütçe buna göre şişer. Yıllık ön ödeme indirimleri sorulmalı (TR sağlayıcılarında yaygın, ~%30; doğrulanmadı).

---

## 7. ADR taslakları (plan/kararlar.md'ye aday — ekip onayı bekliyor)

**ADR-H1 · Prod barındırma: Türk VPS sağlayıcısında self-host (Radore İstanbul)**
- *Ne:* Prod-app ve ops kutuları Radore İstanbul VPS'inde çalışır.
- *Neden:* KVKK m.9 (sağlık verisinin sistematik yurt dışı aktarımı hukuka aykırı risk taşır). ISO 27001. Liste fiyatı açık, kredi kartıyla self-servis. 300 GB NVMe.
- *Alternatifler:* Huawei TR (yönetilen), Turkcell/TT Bulut, İlkbyte, Natro, Contabo/Hetzner/DO/Azure.
- *Neden değil:* Hiperskalerlerin ve Contabo/Hetzner/DO'nun TR bölgesi yok (GCP-Turkcell 2028). Huawei'nin fiyatı ve hesap süreci doğrulanamadı. Turkcell/TT/Bulutistan teklif usulü çalışıyor, kurumsal satış süreci öğrenci ekibi için yavaş. Natro/Veridyen'de DC konumu ve ISO sayfada yok. İlkbyte'ın diski küçük; yedek rolünde daha değerli.

**ADR-H2 · PostgreSQL: yönetilen değil, Docker'da self-host + pgBackRest**
- *Neden:* TR VPS'lerde yönetilen PG yok. Beta DB'si küçük. pgvector sürümünü kendimiz seçeriz. PITR ile RPO ≈ 1–2 dk.
- *Alternatif:* Huawei RDS for PostgreSQL (pgvector 0.8.x).
- *Neden değil (şimdilik):* Fiyat bilinmiyor, sağlayıcı bağımlılığı getiriyor. *Tekrar açılma koşulu:* Konsolda aylık fiyat ≤ 40 USD çıkarsa ve ekip DB operasyonunu taşıyamazsa.

**ADR-H3 · Orkestrasyon: Docker Compose (k3s değil)**
- *Neden:* Tek düğüm, 3 kişi. Öğrenme ve hata ayıklama yüzeyi küçük. Blue/green Caddy ile yapılabiliyor.
- *Alternatif:* k3s, Nomad, Coolify/Dokploy (PaaS katmanı).
- *Neden değil:* k3s tek düğümde az kazanç sağlarken operasyon yükünü artırıyor. Coolify/Dokploy ek bir kontrol düzlemi getiriyor ve sır/ağ davranışı daha az şeffaf. Bu, egress denetimi (K06) açısından sakıncalı.

**ADR-H4 · Nesne depolama: prod-app'te self-host S3 (Garage ya da SeaweedFS) + TTL**
- *Neden:* TR'de fiyatı açık, self-servis bir S3 hizmeti bulunamadı (TT: "proje bazlı"; Bizim Bulut/Narbulut/CloudRUX: fiyat yok). Görseller kısa ömürlü ve küçük. S3 API kodun taşınabilirliğini korur.
- *Alternatifler:* MinIO, Huawei OBS, TT nesne depolama, düz dosya sistemi.
- *Neden değil:* **(doğrulanmadı, kontrol edilmeli)** MinIO topluluk sürümü 2025'te yönetim arayüzünü ve hazır imaj dağıtımını kısıtladı; lisans (AGPL) ve bakım belirsizliği var. OBS/TT için fiyat bilinmiyor. Düz dosya sistemi ise ileride S3'e geçişi zorlaştırır.

**ADR-H5 · Ortam ayrımı: staging yurt dışında olabilir, yalnız sentetik veriyle**
- *Ne:* Contabo VPS ya da Azure kredisi staging/demo için kullanılır. Prod verisi prod dışına çıkmaz (K19). Staging kaydı davetle açılır.
- *Neden:* Mevcut kaynağı değerlendirir, maliyeti sıfıra indirir.
- *Alternatif:* Staging de TR'de olur (+11–22 USD/ay).
- *Neden değil:* Sentetik veriyle yurt dışı hukuken sorunsuz. Risk "staging'e gerçek veri girmesi"; bu risk seed-only kuralı ve kayıt kapısıyla yönetilir.

**ADR-H6 · CI/CD: GitHub Actions (hosted) + kısıtlı SSH deploy; self-hosted runner yok**
- *Neden:* CI veri görmüyor. Prod'da runner olması PR kodunu prod ağında çalıştırmak anlamına gelir. `ForceCommand` + environment onayı saldırı yüzeyini daraltır.
- *Alternatif:* Prod'da self-hosted runner; pull tabanlı GitOps (Watchtower/cosign).
- *Neden değil:* Runner güvenlik riski taşıyor. Pull modeli daha iyi ama beta için karmaşık; sürüm 2'ye bırakıldı.

**ADR-H7 · Sırlar: SOPS + age**
- *Neden:* Sırlar repoda şifreli durur, sunucu dışında açık hali bulunmaz. Ek SaaS gerektirmez. Denetim izi git geçmişinden gelir.
- *Alternatif:* Vault (tek kişilik ekipler için ağır), Doppler (ABD SaaS'ı, öğrenci paketiyle ücretsiz), GitHub Secrets (CI'a prod sırrı taşır).
- *Neden değil:* Yukarıda parantez içinde.

**ADR-H8 · Gözlemlenebilirlik: OTel + Grafana (Prometheus/Loki/Tempo) + GlitchTip + Langfuse v3, hepsi TR'de, ops kutusunda**
- *Alternatif:* SigNoz, Sentry self-host, SaaS (Sentry/Datadog/New Relic öğrenci paketi).
- *Neden değil:* SigNoz ve Langfuse ikisi de ClickHouse istiyor; iki ClickHouse 16 GB'a sığmaz. Sentry self-host 16 GB+ istiyor. SaaS, sağlık verisi sızıntı kanalı demek (ALT-15).

**ADR-H9 · Yedek ve DR: pgBackRest + restic → ikinci TR sağlayıcı (İlkbyte Denizli), pull modeli, aylık restore tatbikatı**
- *Alternatif:* Yalnız sağlayıcının kendi yedeği; yurt dışı S3 (Backblaze/Wasabi, ucuz).
- *Neden değil:* Tek sağlayıcı tek arıza noktası demek. Yurt dışı yedek şifreli olsa da aktarım sayılır (muhafazakâr yorum).

**ADR-H10 · Dış kanallar: push jenerik + data-only; e-posta TR SMTP (SenderTR, yedek kurumsal mail); CDN/proxy yok**
- *Alternatif:* SendGrid/SES/Postmark, Cloudflare proxy.
- *Neden değil:* E-posta adresinin ve TLS sonlandırmanın yurt dışına çıkması m.9 yükü getirir. Beta hacminde TR SMTP yeterli.

---

## 8. Riskler

| # | Risk | Etki | Önlem |
|---|---|---|---|
| R1 | **Ops yükü:** self-host PG, S3, gözlem ve yedek, 3 kişilik öğrenci ekibinin sınav dönemiyle çakışır | Kesinti, yedek sessizce durur | Runbook'lar, "yedek yaşı" alarmı, nöbet çizelgesi. Minimum varyant. Huawei yönetilen PG'nin Plan C olarak açık tutulması. |
| R2 | Kur riski (USD fiyatlı VPS) | Bütçe şişer | Yıllık ön ödeme; TL fiyatlı alternatif (Natro XCloud Pro 1.465 TL KDV dahil). |
| R3 | "TR sağlayıcı" markası altında **yurt dışı sunucu** (Turhost'un ayrı "VPS TR" ürünü bu riski gösteriyor) | Farkında olmadan aktarım | Sözleşmede ve panelde DC konumunun **yazılı teyidi**; IP'nin geolocation/ASN kontrolü. |
| R4 | EVREN'in 1 Kasım sonrası fiyatı ve üretim şartları belirsiz | LLM maliyeti ya da erişim kaybı | K17: LLM'siz mod; yedek yol yalnız K06 maskeleme kapısıyla. |
| R5 | Langfuse v3 2 vCPU'da yavaş kalır ya da ClickHouse RAM'i taşar | Ops kutusu çöker, gözlem kaybolur | ClickHouse bellek limiti; Langfuse erteleme seçeneği; ops kutusu prod-app'ten ayrı olduğu için çekirdek hizmet etkilenmez. |
| R6 | GlitchTip native crash desteği zayıf | Mobil çökme kör noktası | Beta öncesi test; gerekirse yalnız stack trace'li, PII'siz Crashlytics (envantere yazılır). |
| R7 | Push token ve e-posta adresinin yurt dışına aktarımının hukuki niteliği | KVKK bildirimi/sözleşme eksikliği | Aydınlatma metnine yazılır, danışmana/hukukçuya sorulur (01-mevzuat §1.4). |
| R8 | SenderTR beta aşamasında | E-posta doğrulama akışı durur | İkinci SMTP (kurumsal mail) yapılandırılmış hazır bekler; sağlayıcı soyutlaması. |
| R9 | Docker, ufw/nftables kurallarını baypas eder | Egress allowlist'i (K06) boşa düşer | Kurallar `DOCKER-USER` zincirine yazılır; egress testi CI'da. |
| R10 | Tek bölge (İstanbul) + deprem | Uzun kesinti | DR Denizli'de; RTO tatbikatı. |

---

## 9. Proposal teknoloji tablosu için 2–3 satır

| Katman | Teknoloji | Gerekçe |
|---|---|---|
| Barındırma & dağıtım | Türkiye'deki ISO 27001 sertifikalı VPS'ler (birincil İstanbul, yedek/DR Denizli), Docker Compose, GitHub Actions, Caddy (otomatik TLS) | KVKK m.9: sağlık verisi ve yedekleri yurt dışına çıkmaz; tek düğüm ve 3 kişilik ekip için en az operasyon yükü |
| Veri & yedekleme | PostgreSQL 17 + pgvector, S3 uyumlu self-host nesne depolama (kısa ömürlü görseller), pgBackRest PITR (RPO ≤ 15 dk, RTO ≤ 4 sa, aylık restore tatbikatı) | Ölçülebilir güvenilirlik hedefleri FMEA'dan gelir ve tatbikatla kanıtlanır |
| Gözlemlenebilirlik | OpenTelemetry → Prometheus/Loki/Tempo/Grafana, GlitchTip (hata/crash), Langfuse (LLM izleme), tamamı Türkiye'de self-host | Log, trace ve crash kanallarından sağlık verisinin yurt dışına sızmasını engeller (tek egress kapısı, K06) |

---

## 10. Açık sorular (Levent / ekip / danışman)
1. Contabo VPS'inin bölgesi neresi? (Yalnız staging için kullanılacak; bilgi amaçlı.)
2. Üniversite (BİDB) bitirme projelerine sunucu veriyor mu?
3. Bütçe: Beta için ~2.400–3.700 TL/ay'ı kim ödüyor? Fatura kimin adına kesilecek? (Veri sorumlusu kim olacak sorusuyla bağlantılı; bkz. 01-mevzuat.)
4. Huawei Cloud konsolunda TR-Istanbul için RDS PG (2 vCPU/4 GB) ve ECS 4/8 fiyatı: bir ekip üyesi 1 saatlik keşif yapıp not etsin.
5. EVREN 1 Kasım sonrası fiyat ve üretim kullanım şartları.
6. MinIO topluluk sürümünün 2025 sonrası durumu (ADR-H4 varsayımı) doğrulanmalı.

## Kaynaklar (toplu)
- Contabo lokasyonları: https://contabo.com/en/locations/
- GCP–Turkcell: https://www.aa.com.tr/en/economy/turkcell-google-cloud-to-build-hyperscale-data-centers-in-turkiye/3780306 · https://thetechcapital.com/turkcell-google-cloud-plan-sovereign-cloud-region-in-ankara-by-2028/ · https://www.datacenterdynamics.com/en/news/google-and-turkcell-team-up-for-cloud-region-and-data-center-in-t%C3%BCrkiye/
- Azure TR: https://techcommunity.microsoft.com/discussions/azurepartners/new-azure-region---turkey/4003617 · https://news.microsoft.com/source/emea/2026/02/microsoft-confirms-saudi-arabia-datacenter-region-available-for-customers-to-run-cloud-workloads-from-q4-2026/
- Hetzner: https://www.hetzner.com/unternehmen/rechenzentrum/ · DO: https://ideas.digitalocean.com/infrastructure/p/turkey-data-center
- Huawei TR: https://english.news.cn/20230713/d27b34a162fd493ab86a3f5b76e99181/c.html · https://support.huaweicloud.com/intl/en-us/usermanual-rds-pg/rds_09_0045.html · https://www.huaweicloud.com/intl/tr-tr/pricing.html
- Radore: https://radore.com/services/cloud-server · https://radore.com/data-center · https://www.datacenters.com/providers/radore-data-centers
- İlkbyte/Netinternet: https://www.ilkbyte.com/kiralik-sunucu-paketlerimiz/cloud-sunucu · https://www.netinternet.tr/
- Natro: https://www.natro.com/sunucu-kiralama/vps-cloud-server · Veridyen: https://www.veridyen.com/sunucu/pro-bulut-sunucu · Turhost: https://www.turhost.com/sunucu/sanal-sunucu/ · İsimtescil: https://www.isimtescil.net/sunucu · Netlen: https://www.netlen.com.tr/cloud-server
- Turkcell Bulut: https://docs.turkcellbulut.com/articles/sanalsunucu/vps-gs.html · TT Bulut: https://turktelekombulut.com/urunler · Bulutistan: https://bulutistan.com/en/cloud-server/ · CloudRUX: https://www.cloudrux.com/tr/bulut/s3
- GitHub Student Pack: https://education.github.com/pack · DO kredisinin sonu (ikincil): https://aistudentdiscount.com/digitalocean-github-student-developer-pack-credits/
- Langfuse: https://langfuse.com/self-hosting/deployment/infrastructure/containers · https://github.com/orgs/langfuse/discussions/5785
- Sentry self-host: https://deepwiki.com/getsentry/self-hosted/3.1-system-requirements · GlitchTip: https://selfhosting.sh/compare/glitchtip-vs-sentry/
- otel-lgtm: https://github.com/grafana/docker-otel-lgtm · SigNoz: https://signoz.io/docs/install/docker/
- SenderTR: https://sendertr.com/ · Alastyr mail: https://www.alastyr.com/hosting/email-hosting
- Kur: https://tr.investing.com/currencies/usd-try
