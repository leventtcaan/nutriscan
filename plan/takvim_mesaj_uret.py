"""plan/takvim.md → WhatsApp mesajı (toplanti/ekip-takvim-whatsapp.md) + PDF için HTML.
Tek kaynak takvim.md; mesaj ondan üretilir, elle düzenlenmez.
Çalıştır: python3 plan/takvim_mesaj_uret.py
"""
import re, html, pathlib, datetime

KOK = pathlib.Path(__file__).resolve().parent.parent
SRC = KOK / "plan" / "takvim.md"
OUT_MSG = KOK / "toplanti" / "ekip-takvim-whatsapp.md"
OUT_HTML = KOK / "toplanti" / "ekip-takvim.html"
KISI = {"L": "Levent", "H": "Hilal", "O": "Ozan", "E": "Ekip"}

def temizle(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = t.replace("`", "")
    return t.strip()

def kisiler(t):
    # "L (motor) · O (arayüz)" → "Levent (motor) · Ozan (arayüz)"
    return re.sub(r"\b([LHOE])\b", lambda m: KISI[m.group(1)], temizle(t))

s = SRC.read_text(encoding="utf-8")
satirlar = s.splitlines()

# sabit tarihler
sabit = []
i = satirlar.index("## 1. Sabit dış tarihler (pazarlıksız)")
for l in satirlar[i + 3:]:
    if not l.startswith("|"):
        break
    c = [x.strip() for x in l.strip("|").split("|")]
    sabit.append((temizle(c[0]), temizle(c[1])))

# aşamalar
asamalar = []
cur = None
for l in satirlar:
    m = re.match(r"^### (Aşama \d+ — .+)$", l)
    if m:
        cur = {"baslik": m.group(1), "isler": []}
        asamalar.append(cur)
        continue
    if cur and re.match(r"^\| A\d", l):
        c = [x.strip() for x in l.strip("|").split("|")]
        cur["isler"].append({"id": c[0], "is": temizle(c[1]), "kim": kisiler(c[2]),
                             "bagli": temizle(c[3]), "engec": temizle(c[4]), "kacarsa": temizle(c[5])})
    if l.startswith("## 4."):
        cur = None

# ---- WhatsApp mesajı
m = ["*NutriScan — Takvim* (plan/takvim.md'den üretildi, " + datetime.date.today().strftime("%d.%m.%Y") + ")", "",
     "Her iş: *ne* · 👤 kim · 🔗 neye bağlı · ⏰ en geç. Daha erken bitmesi serbest; en geç tarihi kaçarsa önceden yazılı \"kaçarsa\" planı uygulanır (tam liste PDF'te).",
     "Kısaltma: işler ID ile (A2.4 gibi) birbirine bağlanıyor; bir iş, bağlı olduğu işler bitmeden bitmiş sayılmaz.", "",
     "*📌 Sabit tarihler*"]
for t, n in sabit:
    m.append(f"• *{t}* — {n}")
for a in asamalar:
    m += ["", f"*{a['baslik']}*"]
    for x in a["isler"]:
        m.append(f"*{x['id']}* {x['is']}")
        m.append(f"   👤 {x['kim']} · 🔗 {x['bagli']} · ⏰ {x['engec']}")
OUT_MSG.write_text("\n".join(m) + "\n", encoding="utf-8")

# ---- PDF için HTML (tablolu, tam)
def tr(cells, th=False):
    tag = "th" if th else "td"
    return "<tr>" + "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in cells) + "</tr>"
h = ["<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>NutriScan Takvim</title><style>",
     "body{font-family:-apple-system,Helvetica,Arial,sans-serif;font-size:10.5px;color:#1c2420;margin:24px}",
     "h1{font-size:20px;margin:0 0 4px}h2{font-size:14px;margin:18px 0 6px;color:#1f5c45}p{margin:4px 0}",
     "table{border-collapse:collapse;width:100%;margin:4px 0 8px}th,td{border:1px solid #cfc6b3;padding:4px 6px;vertical-align:top;text-align:left}",
     "th{background:#efe9dc}td:first-child{white-space:nowrap;font-weight:600}.k{color:#56615b}",
     "</style></head><body>",
     "<h1>NutriScan — Takvim</h1>",
     f"<p class='k'>Kaynak: plan/takvim.md · üretildi {datetime.date.today().strftime('%d.%m.%Y')} · Her işte yalnız <b>en geç</b> tarihi; en geç kaçarsa “kaçarsa” sütunu uygulanır. Kişi: Levent · Hilal · Ozan · Ekip.</p>",
     "<h2>Sabit tarihler</h2><table>", tr(["Tarih", "Ne"], True)]
h += [tr([t, n]) for t, n in sabit]
h.append("</table>")
for a in asamalar:
    h.append(f"<h2>{html.escape(a['baslik'])}</h2><table>")
    h.append(tr(["ID", "İş", "Kim", "Bağlı olduğu", "En geç", "Kaçarsa"], True))
    h += [tr([x["id"], x["is"], x["kim"], x["bagli"], x["engec"], x["kacarsa"]]) for x in a["isler"]]
    h.append("</table>")
h.append("</body></html>")
OUT_HTML.write_text("".join(h), encoding="utf-8")
print(OUT_MSG, sum(len(a["isler"]) for a in asamalar), "iş")
