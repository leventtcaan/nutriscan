"""plan/takvim.md + plan/board/pbi.yaml → Azure Boards içe aktarım CSV'si, backlog özeti ve PBI promptları.
Çalıştır: python3 plan/board/board_uret.py
Çıktılar (elle düzenlenmez):
  plan/board/azure-import.csv   Epic (aşama) → Feature (takvim satırı) → PBI (yaml) ağacı
  plan/board/backlog.md         sprint × kişi özeti + kontrol uyarıları
  plan/board/promptlar/<ID>.md  agent'a verilecek prompt (calisma-akisi.md §7 şablonu)
"""
import csv, datetime, html, pathlib, re, sys
import yaml

KOK = pathlib.Path(__file__).resolve().parents[2]
TAKVIM = KOK / "plan/takvim.md"
PBI = KOK / "plan/board/pbi.yaml"
OUT = KOK / "plan/board"
KISI = {"L": "Levent", "H": "Hilal", "O": "Ozan", "E": "Ekip"}
AY = {"Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4, "Mayıs": 5, "Haziran": 6,
      "Temmuz": 7, "Ağustos": 8, "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12}


def temizle(t):
    return re.sub(r"\*\*(.+?)\*\*", r"\1", t).replace("`", "").strip()


def tarih(t):
    m = re.search(r"(\d{1,2})\s+(" + "|".join(AY) + ")", t)
    if not m:
        return None
    ay = AY[m.group(2)]
    return datetime.date(2026 if ay >= 9 else 2027, ay, int(m.group(1)))


# ---- takvim: epic + feature
epics, features = [], {}
cur = None
for l in TAKVIM.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^### Aşama (\d+) — (.+)$", l)
    if m:
        cur = {"no": m.group(1), "baslik": f"A{m.group(1)} · {m.group(2)}"}
        epics.append(cur)
        continue
    if l.startswith("## 4."):
        cur = None
    if cur and re.match(r"^\| A\d", l):
        c = [x.strip() for x in l.strip("|").split("|")]
        features[c[0]] = {"id": c[0], "epic": cur["baslik"], "is": temizle(c[1]), "sahip": temizle(c[2]),
                          "bagli": temizle(c[3]), "engec": temizle(c[4]), "kacarsa": temizle(c[5]),
                          "tarih": tarih(temizle(c[4]))}

veri = yaml.safe_load(PBI.read_text(encoding="utf-8"))
pbis = veri["pbi"]
ortak_baglam = veri.get("varsayilan_baglam", [])
ids = {p["id"] for p in pbis}
KAP = veri.get("kapasite", {"varsayilan": 13})


def pbi_tarih(p):
    return tarih(p["en_gec"]) if p.get("en_gec") else features[p["feature"]]["tarih"]


def pbi_engec(p):
    return p.get("en_gec") or features[p["feature"]]["engec"]

# ---- kontroller
uyari = []
for p in pbis:
    if p["feature"] not in features:
        uyari.append(f"{p['id']}: feature {p['feature']} takvimde yok")
    for b in p.get("bagli", []) or []:
        if b not in ids:
            uyari.append(f"{p['id']}: bağımlılık {b} yaml'da yok")
            continue
        pb = next(x for x in pbis if x["id"] == b)
        if p["feature"] in features and pb["feature"] in features:
            tb, tp = pbi_tarih(pb), pbi_tarih(p)
            if tb and tp and tb > tp:
                uyari.append(f"{p['id']} (en geç {pbi_engec(p)}) → {b} (en geç {pbi_engec(pb)}): bağımlılık daha geç bitiyor")
    if p.get("effort") not in (1, 2, 3, 5, 8):
        uyari.append(f"{p['id']}: effort {p.get('effort')} geçersiz")
    if p.get("agent") != "insan" and not p.get("kabul"):
        uyari.append(f"{p['id']}: kabul kriteri yok")
yuk = {}
for p in pbis:
    for k in re.findall(r"[LHO]", p["sahip"]) if p["sahip"] != "E" else ["L", "H", "O"]:
        yuk.setdefault((p["sprint"], k), 0)
        yuk[(p["sprint"], k)] += p["effort"] if p["sahip"] != "E" else 1
for (sp, k), v in sorted(yuk.items()):
    sinir = KAP.get(sp, {}).get(k, KAP["varsayilan"]) if isinstance(KAP.get(sp), dict) else KAP["varsayilan"]
    if v > sinir and sp != "Hazırlık":
        uyari.append(f"{sp} · {KISI[k]}: {v} Effort > {sinir}")


# ---- prompt
def prompt(p):
    f = features[p["feature"]]
    baglam = ortak_baglam + [x for x in (p.get("modul_agents") or [])] + (p.get("baglam") or [])
    if p.get("modul"):
        baglam.insert(1, f"{p['modul']} içindeki AGENTS.md (varsa)")
    s = [f"# {p['id']} · {p['baslik']}",
         (f"_AB#{AB[p['id']]} · Feature {f['id']} (AB#{AB.get(f['id'], '?')}): {f['is']}_" if p["id"] in AB
          else f"_AB#<id> — board'a alınınca doldurulur · Feature {f['id']}: {f['is']}_"), "",
         f"**Sahip:** {KISI.get(p['sahip'], p['sahip'])} · **Agent:** {p['agent']} · **Modül:** {p.get('modul', '—')} · "
         f"**Effort:** {p['effort']} · **Sprint:** {p['sprint']} · **En geç:** {pbi_engec(p)}", ""]
    if p.get("bagli"):
        s.append(f"**Önce bitmiş olmalı:** {', '.join(p['bagli'])} (bitmediyse sözleşme/fixture/mock ile çalış; yoksa DUR)")
    if p.get("kurallar"):
        s.append(f"**İlgili kurallar:** {p['kurallar']}")
    s.append(f"**Sözleşme etkisi:** {p.get('sozlesme', 'yok')}")
    s += ["", "## Bağlam (önce oku)"] + [f"- {b}" for b in baglam]
    s += ["", "## Görev", p["gorev"].strip()]
    s += ["", "## Kapsam"]
    if p.get("degistir"):
        s.append("- Değiştirebileceğin yer: " + ", ".join(f"`{x}`" for x in p["degistir"]))
    sozlesmeli = any("contracts" in x for x in (p.get("degistir") or []))
    s.append("- Dokunma: " + (", ".join(f"`{x}`" for x in p["dokunma"]) if p.get("dokunma") else "görevin modülü dışındaki her şey")
             + (". Başka modüle dokunman gerekirse DUR ve PR açıklamasına \"contract-change gerekli\" yaz."
                if sozlesmeli else ". Başka modüle ya da `contracts/`'a dokunman gerekirse DUR ve PR açıklamasına \"contract-change gerekli\" yaz."))
    if sozlesmeli:
        s.append("- Bu PBI sözleşme ekliyor: `contracts/` değişikliği aynı PR'da, `contract-change` etiketiyle; tüketici modül sahiplerinin onayı istenir.")
    s.append("- Bilmediğin sürüm, API, kaynak ya da sayıyı uydurma: resmi dokümandan doğrula; doğrulayamazsan `[..]` bırak ve PR'da yaz.")
    s += ["", "## Adımlar", "1. Önce planı yaz (değişecek dosyalar + yazılacak testler) ve PR açıklamasının başına koy; sonra uygula."]
    for i, a in enumerate(p.get("adimlar") or [], 2):
        s.append(f"{i}. {a}")
    n = len(p.get("adimlar") or []) + 2
    s.append(f"{n}. Uygula; her kabul kriteri için test yaz.")
    s.append(f"{n + 1}. Yerelde çalıştır: " + (" · ".join(f"`{c}`" for c in p["komutlar"]) if p.get("komutlar") else "modülün build/test/lint komutları (AGENTS.md)"))
    s += ["", "## Kabul kriterleri"] + [f"- [ ] {k}" for k in p.get("kabul", [])]
    mod = (p.get("area") or "platform").split("\\")[-1] or "platform"
    ab = AB.get(p["id"], "<id>")
    s += ["", "## Teslim",
          f"- Dal: `{mod}/AB{ab}-<kısa-ad>` · Commit/PR başlığı: `<tip>({mod}): … AB#{ab}` · PR gövdesi: `Fixes AB#{ab}`",
          "- PR şablonunu doldur, kabul kriterlerini işaretle, UI ise ekran görüntüsü ekle; ≤400 satır, tek modül.",
          "- \"Agent'ın yazdığını okudum ve açıklayabilirim\" kutusunu sahip işaretler (agent değil)."]
    return "\n".join(s) + "\n"


AB = {}
if (OUT / "azure-idler.yaml").exists():
    AB = {str(k): v for k, v in (yaml.safe_load((OUT / "azure-idler.yaml").read_text(encoding="utf-8")) or {}).items()}
(OUT / "promptlar").mkdir(exist_ok=True)
for eski in (OUT / "promptlar").glob("*.md"):
    eski.unlink()
for p in pbis:
    if p["agent"] != "insan":
        (OUT / "promptlar" / f"{p['id']}.md").write_text(prompt(p), encoding="utf-8")

# ---- CSV (Azure Boards: Work Items → Import from CSV, ağaç için Title 1/2/3)
AREA = "NutriScan"


def area(a):
    return AREA if not a or a == "proje" else f"{AREA}\\{a}"


def sprint(s):
    return f"{AREA}\\{s}"


def aciklama_pbi(p):
    parca = [f"<p>{html.escape(p['gorev'].strip())}</p>"]
    if p["agent"] != "insan":
        parca.append(f"<p><b>Prompt:</b> plan/board/promptlar/{p['id']}.md · Agent: {p['agent']}</p>")
    if p.get("bagli"):
        parca.append(f"<p><b>Bağlı:</b> {', '.join(p['bagli'])}</p>")
    parca.append(f"<p><b>En geç:</b> {html.escape(pbi_engec(p))}</p>")
    return "".join(parca)


rows = []
for e in epics:
    rows.append({"Work Item Type": "Epic", "Title 1": e["baslik"]})
    for f in [x for x in features.values() if x["epic"] == e["baslik"]]:
        rows.append({"Work Item Type": "Feature", "Title 2": f"[{f['id']}] {f['is']}",
                     "Description": f"<p><b>Sahip:</b> {html.escape(re.sub(r'\b([LHOE])\b', lambda m: KISI[m.group(1)], f['sahip']))} · "
                                    f"<b>Bağlı:</b> {html.escape(f['bagli'])} · <b>En geç:</b> {html.escape(f['engec'])} · "
                                    f"<b>Kaçarsa:</b> {html.escape(f['kacarsa'])}</p>",
                     "Tags": f"takvim:{f['id']}"})
        for p in [x for x in pbis if x["feature"] == f["id"]]:
            etiket = [f"sahip:{KISI.get(p['sahip'], p['sahip']).lower()}", f"agent:{p['agent']}", f"omurga:{p.get('omurga', 'zemin')}"]
            if p.get("sozlesme", "yok").startswith(("eklemeli", "kırıcı")):
                etiket.append("contract-change")
            rows.append({"Work Item Type": "Product Backlog Item", "Title 3": f"[{p['id']}] {p['baslik']}",
                         "Description": aciklama_pbi(p),
                         "Acceptance Criteria": "<ul>" + "".join(f"<li>{html.escape(k)}</li>" for k in p.get("kabul", [])) + "</ul>",
                         "Area Path": area(p.get("area")), "Iteration Path": sprint(p["sprint"]),
                         "Effort": p["effort"], "Tags": "; ".join(etiket)})
kolon = ["ID", "Work Item Type", "Title 1", "Title 2", "Title 3", "Description", "Acceptance Criteria",
         "Area Path", "Iteration Path", "Effort", "Tags"]
with open(OUT / "azure-import.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=kolon)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in kolon})

# ---- backlog.md
b = ["---", "title: NutriScan backlog özeti (üretildi — elle düzenleme)",
     f"updated: {datetime.date.today().isoformat()}", "kaynak: plan/board/pbi.yaml + plan/takvim.md", "---",
     "# Backlog özeti", "",
     f"{len(epics)} epic · {len(features)} feature · {len(pbis)} PBI ({sum(1 for p in pbis if p['agent'] != 'insan')} promptlu). "
     "PBI'a bölünmemiş feature'lar sırası gelince bölünür (sprint planlamadan önce).", ""]
for sp in dict.fromkeys(p["sprint"] for p in pbis):
    b += [f"## {sp}", "| PBI | İş | Sahip | Agent | Effort | Bağlı | En geç |", "|---|---|---|---|---|---|---|"]
    for p in [x for x in pbis if x["sprint"] == sp]:
        b.append(f"| {p['id']} | {p['baslik']} | {KISI.get(p['sahip'], p['sahip'])} | {p['agent']} | {p['effort']} | "
                 f"{', '.join(p.get('bagli') or []) or '—'} | {pbi_engec(p)} |")
    yk = " · ".join(f"{KISI[k]} {v}" for (s, k), v in sorted(yuk.items()) if s == sp)
    b += ["", f"Yük (Effort): {yk}", ""]
bol = [f for f in features.values() if f["id"] not in {p["feature"] for p in pbis}]
b += ["## Henüz PBI'a bölünmemiş feature'lar", ", ".join(f["id"] for f in bol), "",
      "## Kontrol uyarıları", *([f"- {u}" for u in uyari] or ["- yok"])]
(OUT / "backlog.md").write_text("\n".join(b) + "\n", encoding="utf-8")

print(f"{len(epics)} epic, {len(features)} feature, {len(pbis)} PBI → azure-import.csv, backlog.md, "
      f"{len(list((OUT / 'promptlar').glob('*.md')))} prompt")
for u in uyari:
    print("UYARI:", u)

# ---- azure-items.json (REST ile yükleme için; CSV ile aynı içerik + atama, tarih, prompt, ekip Task'ları)
import json, markdown as _md

if not (OUT / "kisiler.yaml").exists():  # kişisel veri (e-posta) — yalnız board'a yükleyen kişide bulunur
    print("kisiler.yaml yok → azure-items.json üretilmedi (board yüklemesi gerekmiyorsa sorun değil)")
    sys.exit(0)
KISILER = yaml.safe_load((OUT / "kisiler.yaml").read_text(encoding="utf-8"))["kisiler"]


def eposta(kod):
    k = re.findall(r"\b[LHO]\b", kod)
    return KISILER[k[0]]["azure"] if k else None


def iso(t):
    return t.isoformat() + "T00:00:00Z" if t else None


def epic_tarih(baslik):
    m = re.search(r"\(([^)]*)\)", baslik)
    if not m:
        return None, None
    parca = m.group(1).split("→")
    return (tarih(parca[0]) if len(parca) > 1 else None), tarih(parca[-1])


items = []
for ei, e in enumerate(epics):
    bas, son = epic_tarih(e["baslik"])
    items.append({"key": f"E{e['no']}", "type": "Epic", "title": e["baslik"], "parent": None,
                  "fields": {"System.Description": f"<p>Takvim aşaması (plan/takvim.md §3). Tarihler: {html.escape(e['baslik'])}</p>",
                             "Microsoft.VSTS.Scheduling.StartDate": iso(bas), "Microsoft.VSTS.Scheduling.TargetDate": iso(son),
                             "System.Tags": f"asama:A{e['no']}"},
                  "assign": KISILER["L"]["azure"]})
    for f in [x for x in features.values() if x["epic"] == e["baslik"]]:
        sah = re.sub(r"\b([LHOE])\b", lambda m: KISI[m.group(1)], f["sahip"])
        items.append({"key": f["id"], "type": "Feature", "title": f"[{f['id']}] {f['is']}", "parent": f"E{e['no']}",
                      "fields": {"System.Description": f"<p><b>Sahip:</b> {html.escape(sah)}<br><b>Bağlı:</b> {html.escape(f['bagli'])}<br>"
                                                       f"<b>En geç:</b> {html.escape(f['engec'])}<br><b>Kaçarsa:</b> {html.escape(f['kacarsa'])}</p>"
                                                       f"<p>Kaynak: plan/takvim.md · PBI'lar: plan/board/pbi.yaml</p>",
                                 "Microsoft.VSTS.Scheduling.TargetDate": iso(f["tarih"]), "System.Tags": f"takvim:{f['id']}"},
                      "assign": eposta(f["sahip"]) or KISILER["L"]["azure"]})
        for p in [x for x in pbis if x["feature"] == f["id"]]:
            etiket = [f"sahip:{KISI.get(p['sahip'], p['sahip']).lower()}", f"agent:{p['agent']}", f"omurga:{p.get('omurga', 'zemin')}", f"takvim:{f['id']}"]
            if str(p.get("sozlesme", "yok")).startswith(("eklemeli", "kırıcı")):
                etiket.append("contract-change")
            aciklama = f"<p>{html.escape(p['gorev'].strip())}</p><p><b>En geç:</b> {html.escape(pbi_engec(p))}"
            if p.get("bagli"):
                aciklama += f" · <b>Önce bitmeli:</b> {', '.join(p['bagli'])}"
            aciklama += "</p>"
            if p["agent"] != "insan":
                aciklama += (f"<hr><p><b>Agent promptu</b> (repoda: plan/board/promptlar/{p['id']}.md — önce pbi-baslat skill'i)</p>"
                             + _md.markdown((OUT / "promptlar" / f"{p['id']}.md").read_text(encoding="utf-8"), extensions=["tables"]))
            items.append({"key": p["id"], "type": "Product Backlog Item", "title": f"[{p['id']}] {p['baslik']}", "parent": f["id"],
                          "fields": {"System.Description": aciklama,
                                     "Microsoft.VSTS.Common.AcceptanceCriteria": "<ul>" + "".join(f"<li>{html.escape(k)}</li>" for k in p.get("kabul", [])) + "</ul>",
                                     "Microsoft.VSTS.Scheduling.Effort": p["effort"], "System.AreaPath": area(p.get("area")),
                                     "System.IterationPath": sprint(p["sprint"]), "System.Tags": "; ".join(etiket)},
                          "assign": eposta(p["sahip"]) or KISILER["L"]["azure"]})
            if p["sahip"] == "E":
                for k in ["L", "H", "O"]:
                    pay = (p.get("paylar") or {}).get(k)
                    items.append({"key": f"{p['id']}-{k}", "type": "Task", "title": f"[{p['id']}] {KISILER[k]['kisa']} payı",
                                  "parent": p["id"], "fields": {"System.AreaPath": area(p.get("area")), "System.IterationPath": sprint(p["sprint"]),
                                                                "System.Tags": f"takvim:{f['id']}",
                                                                "System.Description": (f"<p>{html.escape(pay)}</p><p><b>Üst iş:</b> {html.escape(p['baslik'])} · "
                                                                                       f"<b>En geç:</b> {html.escape(pbi_engec(p))}</p>") if pay else None},
                                  "assign": KISILER[k]["azure"]})
for it in items:
    it["fields"] = {k: v for k, v in it["fields"].items() if v is not None}
(OUT / "azure-items.json").write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
print(f"azure-items.json: {len(items)} öğe, {len(json.dumps(items, ensure_ascii=False)) // 1024} KB")
