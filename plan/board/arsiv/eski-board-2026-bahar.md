---
title: Eski Azure Boards kaydı (2025–26 SWE dersi, Mart–Mayıs 2026) — silinmeden önce alınan özet
kaynak: dev.azure.com/hilalhocaoglu20/NutriScan (Basic süreç, "NutriScan Team"), REST API ile okundu 2026-09-27
not: Yalnız tarihçe/fikir kaydı; buradan hiçbir şey kalıcı kabul edilmez (feedback: eski repo sadece okuma). Silme Azure çöp kutusuna gider (geri alınabilir).
---
# Eski board özeti

- **92 iş öğesi** (90 Issue, 2 Task), ID 1–101 (bazı numaralar boş). Durum: 88 Done, 2 Doing (76, 93), 2 To Do (33, 97).
- Tek iterasyon (`Sprint 1`, 81 öğe) + kök (11 öğe); Area tek (`NutriScan`); hiyerarşi (Epic/ebeveyn) yok; açıklamaların çoğu boş.
- Atanan dağılımı: Hilal 37 · geçen yılın dördüncü üyesi (mobil) 20 · Levent 18 · Ozan 10 · atanmamış 7.
- Commit/PR bağlantısı yalnız Levent'in öğelerinde (Azure Repos; projede 4 eski repo var: nutriscan, nutriscan-backend, nutriscan-mobile, nutriscan-web — dokunulmadı).
- Stack: .NET (EF Core, Clean Architecture, Microsoft Identity/JWT), SQL Server → PostgreSQL, Redis, OFF API, Next.js web, Expo Router mobil.
- Bu yıl için ilginç olanlar (yalnız fikir): #69 "AI-Powered Semantic Allergen Mapping" (Hilal — A3.7 RAG eşlemesiyle ilgili deneyim), #49 "UNKNOWN safety status" (bugünkü "Doğrulanamadı"nın öncülü), #100 "Self / Family Mode", #13 sağlık profili (alerji + hastalık), #55 crowdsourcing + admin moderasyonu, #62/#81 SMTP parola düzeltmeleri (DURUM'daki "commit'li sır" sorusuyla ilişkili).

| ID | Tip | Durum | Atanan | Tarih | Başlık |
|---|---|---|---|---|---|
| 1 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-03-18 | Mobile dynamic theme support |
| 2 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-03-18 | Mobile Tab navigation implementation |
| 3 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-03-18 | Mobile UI layout for home tab |
| 4 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-03-18 | Mobile UI layout for scan tab |
| 5 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-03-18 | Mobile UI layout for List tab |
| 6 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-03-18 | Mobile UI layout for Profile tab |
| 7 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-03-18 | Mobile Auth backend connection |
| 8 | Issue | Done | Levent | 2026-03-18 | feat(web): Implement User Registration UI components |
| 9 | Task | Done | — | 2026-03-18 | feat(web): Implement Login UI and Authentication layout |
| 10 | Task | Done | — | 2026-03-18 | feat(web): Implement Login UI and Authentication layout |
| 11 | Issue | Done | Levent | 2026-03-18 | feat(web): Implement Login UI and Authentication layout |
| 12 | Issue | Done | Levent | 2026-03-18 | feat(backend): Setup Core Domain Entities and EF Core DbContext |
| 13 | Issue | Done | Levent | 2026-03-18 | feat(backend): Implement Health Profile and Family Group Endpoints |
| 14 | Issue | Done | Levent | 2026-03-18 | feat(backend): Implement Shopping List and Item Management |
| 15 | Issue | Done | Hilal | 2026-03-18 | Platform ve Database Migration (SQL Server → PostgreSQL) |
| 16 | Issue | Done | Hilal | 2026-03-18 | EF Core 1:1 Relationship Optimization |
| 17 | Issue | Done | Hilal | 2026-03-18 | Circular Dependency Resolution |
| 18 | Issue | Done | Hilal | 2026-03-18 | Identity & Auth System Implementation |
| 19 | Issue | Done | Hilal | 2026-03-18 | API Documentation & Integration Testing |
| 25 | Issue | Done | Ozan | 2026-03-18 | feat(web): Implement Main/Landing Page UI layout |
| 26 | Issue | Done | Ozan | 2026-03-18 | feat(web-admin): Implement Admin layout and Overview UI |
| 27 | Issue | Done | Ozan | 2026-03-18 | feat(web-admin): Implement Product Catalog UI |
| 28 | Issue | Done | Ozan | 2026-03-18 | feat(web-admin): Implement Review Management UI for crowdsourcing moderation |
| 29 | Issue | Done | Ozan | 2026-03-18 | feat(web-admin): Implement remaining Admin UI pages |
| 30 | Issue | Done | Ozan | 2026-03-18 | feat(web-portal): Implement User Dashboard and Account Settings UI |
| 31 | Issue | Done | Ozan | 2026-03-18 | feat(web-portal): Implement Family Profiles and Saved Products UI |
| 32 | Issue | Done | Ozan | 2026-03-18 | feat(web-admin): Integrate Approval Management UI with backend moderation API |
| 33 | Issue | To Do | Ozan | 2026-03-18 | feat(web-admin): Implement state management for Admin Dashboard metrics |
| 34 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-05 | Mobile UI layout for Profile/Settings |
| 35 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-06 | Mobile UI layout for Weekly Report Page |
| 36 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-06 | Mobile UI layout for search page |
| 37 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-07 | Mobile Scan function implementation |
| 39 | Issue | Done | Hilal | 2026-04-07 | feat(backend): Redis infrastructure |
| 40 | Issue | Done | Hilal | 2026-04-07 | feat(backend): ICacheService / RedisCacheService |
| 41 | Issue | Done | Hilal | 2026-04-07 | feat(backend): Integrate OpenFoodFacts API |
| 42 | Issue | Done | Hilal | 2026-04-07 | feat(backend): triple-layer product lookup (Redis → DB → OFF) |
| 43 | Issue | Done | Hilal | 2026-04-07 | fix(backend): JSON circular reference in product entities |
| 44 | Issue | Done | Hilal | 2026-04-07 | chore(backend): merge feature/off-api-client |
| 45 | Issue | Done | Hilal | 2026-04-13 | feat(backend): core Cross-Collision Engine (parallel) |
| 46 | Issue | Done | Hilal | 2026-04-13 | feat(backend): atomic transactions for product/allergen sync |
| 47 | Issue | Done | Hilal | 2026-04-13 | feat(backend): Admin API for allergen aliases and markers |
| 48 | Issue | Done | Hilal | 2026-04-13 | feat(backend): multi-language allergen dictionary (TR/EN) |
| 49 | Issue | Done | Hilal | 2026-04-13 | feat(backend): UNKNOWN safety status + force-refresh |
| 50 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-14 | Mobile Product Verdict Page UI |
| 51 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-14 | Mobile Profile tab pop-ups |
| 52 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-14 | Mobile update health info page |
| 53 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-14 | mobile edit profile page |
| 54 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-14 | mobile manage family page |
| 55 | Issue | Done | Levent | 2026-04-14 | feat(backend): Crowdsourcing and Admin Moderation |
| 56 | Issue | Done | Levent | 2026-04-14 | feat(backend): Health Dashboard and Gamification |
| 57 | Issue | Done | Hilal | 2026-04-21 | feat(backend): product scan history |
| 58 | Issue | Done | Hilal | 2026-04-21 | feat(backend): safe product alternative recommendations |
| 59 | Issue | Done | Hilal | 2026-04-21 | fix(backend): sync Identity auth layer with Domain User |
| 60 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-21 | Mobile Dashboard and Recent Scan endpoint connection |
| 61 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-04-21 | Mobile Shopping List endpoint connections |
| 62 | Issue | Done | Levent | 2026-04-21 | fix(core): clean smtp password spaces + deep exception logging |
| 64 | Issue | Done | Levent | 2026-04-28 | feat(auth): Email Confirmation and Mock Service |
| 65 | Issue | Done | Levent | 2026-04-28 | feat(account): profile update endpoint |
| 66 | Issue | Done | Levent | 2026-04-28 | feat(account): password account flows |
| 67 | Issue | Done | Levent | 2026-04-28 | feat(account): delete account endpoint |
| 69 | Issue | Done | Hilal | 2026-04-28 | Feat: AI-Powered Semantic Allergen Mapping |
| 70 | Issue | Done | Hilal | 2026-04-28 | Feat: End-to-End Clean Architecture Pipeline |
| 71 | Issue | Done | Hilal | 2026-04-28 | Feat: Robust Exception Handling & Validation |
| 72 | Issue | Done | Hilal | 2026-04-28 | Feat: Relational Database Schema Optimization |
| 73 | Issue | Done | Levent | 2026-04-28 | feat: PhoneNumber in Account DTOs |
| 74 | Issue | Done | Hilal | 2026-04-28 | Feat: Relational Data Enrichment for Scan History Analytics |
| 75 | Issue | Done | Hilal | 2026-05-01 | feat: Advanced Family Management (Invite Code & Smart Leave) |
| 76 | Issue | Doing | Ozan | 2026-05-01 | feat(web-account): Implement Family System |
| 77 | Issue | Done | Hilal | 2026-05-01 | feat(mobile): Dynamic User Identity and Profile Sync |
| 78 | Issue | Done | Hilal | 2026-05-01 | feat: Persistent Dietary Preference and Allergen Management |
| 79 | Issue | Done | Hilal | 2026-05-01 | feat: Intelligent Allergen Collision and Risk Analysis Engine |
| 80 | Issue | Done | Hilal | 2026-05-01 | feat(mobile): Dynamic Safety Communication and UI Feedback |
| 81 | Issue | Done | Levent | 2026-05-02 | fix(core): in-memory db transactions + real smtp injection |
| 82 | Issue | Done | Levent | 2026-05-02 | fix(auth): silent login, 401 on health profile submission |
| 83 | Issue | Done | Levent | 2026-05-02 | feat(dashboard): finalize v1 |
| 84 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-05-02 | Mobile Weekly Report Endpoint connection |
| 85 | Issue | Done | (geçen yılın dördüncü üyesi) | 2026-05-02 | Mobile Product page endpoint connection |
| 86 | Issue | Done | — | 2026-05-02 | Mobile update health endpoint connection |
| 87 | Issue | Done | — | 2026-05-02 | mobile edit profile endpoint connection |
| 88 | Issue | Done | Hilal | 2026-05-02 | mobile family management endpoint connections |
| 89 | Issue | Done | Levent | 2026-05-02 | feat(web): dynamic-health-reports |
| 90 | Issue | Done | Levent | 2026-05-02 | feat(admin): RBAC, dynamic admin overview, user/product management |
| 91 | Issue | Done | Hilal | 2026-05-02 | refactor: product scan response structure, mobile image fix |
| 92 | Issue | Done | Hilal | 2026-05-02 | feat(backend): product issue reporting |
| 93 | Issue | Doing | — | 2026-05-03 | Fix: Family System null errors |
| 94 | Issue | Done | — | 2026-05-03 | fix-mobile-scan-off-dashboard |
| 95 | Issue | Done | Hilal | 2026-05-03 | feat(fullstack): multi-shopping list architecture |
| 97 | Issue | To Do | — | 2026-05-03 | fix(mobile): bind dynamic barcode and remove dummy data |
| 98 | Issue | Done | Hilal | 2026-05-03 | fix(mobile): bind dynamic barcode and remove dummy data |
| 99 | Issue | Done | Hilal | 2026-05-03 | feat(profile & ui): capitalized real names in Auth DTOs |
| 100 | Issue | Done | Hilal | 2026-05-03 | feat(scan): "Self / Family Mode" toggle for product safety |
| 101 | Issue | Done | Hilal | 2026-05-03 | feat(ui): user full name on home screen |
