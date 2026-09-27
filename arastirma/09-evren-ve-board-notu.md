---
title: EVREN LLM katmanı + proje takip aracı — doğrulanmış notlar
updated: 2026-09-25
kaynak: evren.ssyz.org.tr/llm-inference (Levent'in Chrome oturumu, 25 Eyl 2026 okundu) · Microsoft/GitHub dokümanları
---
# EVREN (SSB) — LLM çıkarım katmanı (25 Eylül 2026 itibarıyla sayfada yazanlar)
- OpenAI uyumlu tek API; `model="auto"` yönlendirici. OpenAI SDK, Codex CLI, Vercel AI SDK uyumlu.
- **Veri egemenliği:** istem, yanıt ve kullanım kayıtları Türkiye'de bare-metal altyapıda; "yurt dışına veri aktarımı yapılmaz" (sayfa beyanı).
- **Kota:** 10M token/gün, 500K TPM (burst), 32 paralel istek. **1 Kasım 2026'ya kadar 0 kredi (ücretsiz test).** Sonrası kredi — ücret/şartlar okunmadı.
- **Modeller (13/13 çevrimiçi):** glm-5.3 (amiral, 512K bağlam, araç kullanımı), deepseek-v4.1-flash (kod/ajan, 1M, görsel), deepseek-v4-flash (1 Kas'ta kalkıyor), qwen3.8-flash-next, gemma-4-31b (görsel, bbox, belge okuma), qwen3-vl-30b (video), **qwen3-embedding-8b (TR-TEB'de 1.)**, qwen3-vl-reranker-8b, **qwen3-guard-4b (içerik güvenliği)**, **dots-ocr / deepseek-ocr-2 (OCR)**, **qwen3-asr-1.7b (Türkçe konuşma tanıma)**.
- Sayfada "tahmini bekleme: uzun" göstergesi → gecikme riski ölçülmeli.
- **NutriScan'e etkisi:** asistan orkestrasyonu, etiket/fiş OCR, Türkçe gömme (katalog/tarif arama), ses tanıma ve güvenlik sınıflandırıcısı Türkiye'de çalışabilir → 05-agent-mimarisi'ndeki "tamamen TR" (B) mimarisi artık gerçekçi; hibrit bulut yolu yedek. **Açık:** ticari/üretim kullanım şartları, 1 Kasım sonrası kredi fiyatı, Türkçe tool-calling doğruluğu (ölçülecek).

# Proje takip aracı
- **Azure DevOps (Boards):** ilk 5 kullanıcı ücretsiz (Basic: Boards, Repos, Pipelines, Artifacts). Scrum süreç şablonu: PBI, Task, Bug, Sprint, backlog, capacity, burndown. Resmi Microsoft MCP sunucusu (uzak sunucu GA, 2026) → work item okuma/yazma, WIQL. GitHub entegrasyonu: Azure Boards GitHub App; commit/PR'da `AB#<id>` ile iş öğesine bağlanır.
  Kaynaklar: https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/ · https://github.com/microsoft/azure-devops-mcp · https://learn.microsoft.com/en-us/azure/devops/release-notes/2026/sprint-278-update · https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops
- **GitHub Projects:** iteration alanı (sprint), board/table/roadmap, sub-issue; ama yerleşik backlog/PBI kavramı yok, sprint düzeni elle kurulur. https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields
- **Self-host (Contabo VPS: Plane/Taiga/OpenProject):** mümkün ama bakım, yedek, güvenlik yükü; Azure Boards ücretsiz ve yönetilen olduğu için gereksiz.
