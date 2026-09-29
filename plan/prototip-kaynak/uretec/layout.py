"""Yeni artboard'ları canvas.json'a akış sıralarıyla ekler; mevcut 31 artboard'un yerine dokunmaz."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "project/canvas.json")))
REG = {}
for _f in os.listdir(os.path.join(HERE, "project")):
    if _f.endswith(".dc.html"):
        _t = open(os.path.join(HERE, "project", _f), encoding="utf-8").read()
        _m = re.search(r'"\$preview":\s*\{"width":\s*(\d+),\s*"height":\s*(\d+)', _t)
        _ti = re.search(r"<title>(.*?)</title>", _t, re.S)
        if _m:
            REG[_f[:-8]] = {"w": int(_m.group(1)), "h": int(_m.group(2)), "title": __import__("html").unescape(_ti.group(1).strip()) if _ti else _f}
files = sorted(f[:-8] for f in os.listdir(os.path.join(HERE, "project")) if f.endswith(".dc.html"))

ROWS = [
    ("t7", "7 · v5.2 — Hesap, hane ve davet", r"^M2[3-7]-"),
    ("t8", "8 · v5.2 — Plan, liste ve asistan", r"^(M2[89]|M3[0-3]|M4[2-5])-"),
    ("t9", "9 · v5.2 — Tara, ürün kaynağı ve kiler", r"^(M3[4-9]|M4[01])-"),
    ("t10", "10 · v5.2 — Bildirim, ayarlar, gizlilik ve sistem durumları", r"^(M4[6-9]|M5\d)-"),
    ("t11", "11 · v5.2 — Web: giriş, hane, stüdyo durumları, diyetisyen", r"^W(0[6-9]|\d\d)"),
    ("t12", "12 · v5.2 — Admin: toplayıcı, eşleme, sözleşme panosu, kurallar, KVKK", r"^A(0[5-9]|1\d)"),
]
y = max(b["y"] + b["h"] for b in C["boards"].values()) + 120 + 263
for nid, text, pat in ROWS:
    row = [f for f in files if re.match(pat, f) and f + ".dc.html" not in C["boards"]]
    if not row:
        continue
    x, hmax = 0, 0
    for f in row:
        r = REG.get(f)
        if not r:
            raise SystemExit(f"registry'de yok: {f}")
        key = f + ".dc.html"
        C["boards"][key] = {"x": x, "y": y, "w": r["w"], "h": r["h"], "title": r["title"], "is_interactive": True}
        C["order"].append(key)
        x += r["w"] + 80
        hmax = max(hmax, r["h"])
    C["notes"][nid] = {"x": 0, "y": y - 263, "text": text, "kind": "title1", "maxW": max(1840, x - 80)}
    y += hmax + 120 + 263

extra = [f for f in files if f + ".dc.html" not in C["boards"]]
if extra:
    raise SystemExit(f"yerleşmeyen dosya: {extra}")
json.dump(C, open(os.path.join(HERE, "project/canvas.json"), "w"), ensure_ascii=False, indent=1)
print(len(C["boards"]), "artboard")
