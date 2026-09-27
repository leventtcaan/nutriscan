"""Ekip paketi: tez + ürün tanımı md → PDF, proposal + takvim PDF'lerini kopyalar.
Çalıştır: python3 plan/ekip_paketi_uret.py <klasör-adı>   (ör. 2026-09-27-ekip-paketi)
Önce: python3 plan/takvim_mesaj_uret.py (+ Chrome ile takvim PDF) ve plan/proposal/build_docx.py (+ Pages PDF)."""
import markdown, re, pathlib, subprocess, shutil, sys
KOK = pathlib.Path(__file__).resolve().parents[1]
OUT = KOK / "toplanti" / (sys.argv[1] if len(sys.argv) > 1 else "ekip-paketi")
OUT.mkdir(parents=True, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CSS = """body{font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;font-size:10.5pt;line-height:1.45;color:#1c2420;max-width:180mm;margin:0 auto}
h1{font-size:18pt;border-bottom:2px solid #1f5c45;padding-bottom:4px}h2{font-size:13pt;color:#1f5c45;margin-top:18px}h3{font-size:11pt}
table{border-collapse:collapse;width:100%;font-size:9pt;margin:6px 0}th,td{border:1px solid #d6cdb9;padding:4px 6px;vertical-align:top;text-align:left}th{background:#eef5f0}
blockquote{border-left:3px solid #1f5c45;margin:6px 0;padding:2px 10px;color:#3d4742}code{font-size:9pt}pre{background:#f5f1e8;padding:8px 10px;border-radius:6px;white-space:pre-wrap;font-size:8.5pt;line-height:1.35}li{margin:2px 0}
@page{size:A4;margin:14mm}"""

def md_to_html(t):
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)
    # markdown listeden önce boş satır ister
    lines, prev = [], ""
    for l in t.splitlines():
        if re.match(r"^(\d+\.|-)\s", l) and prev.strip() and not re.match(r"^(\d+\.|-)\s|^\s", prev):
            lines.append("")
        lines.append(l); prev = l
    return markdown.markdown("\n".join(lines), extensions=["tables", "fenced_code"])

for src, name, title in [("arastirma/07-tez-v5.md", "NutriScan-Tez-v5.1", "NutriScan Tez v5.1"),
                         ("plan/urun-tanimi.md", "NutriScan-Urun-Tanimi-v5.1", "NutriScan Ürün Tanımı v5.1"),
                         ("plan/calisma-akisi.md", "NutriScan-Calisma-Akisi", "NutriScan Çalışma Akışı")]:
    body = md_to_html((KOK / src).read_text(encoding="utf-8"))
    h = OUT / (name + ".html")
    h.write_text(f"<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head>"
                 f"<body><p style='color:#56615b;font-size:9pt'>Ekip içi belge · kaynak: {src}</p>{body}</body></html>", encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT / (name + '.pdf')}", f"file://{h.resolve()}"], capture_output=True)
    h.unlink()
for f in ["plan/proposal/NutriScan_CSE491_Proposal_v0.pdf", "plan/proposal/NutriScan_CSE491_Proposal_v0.docx", "toplanti/NutriScan-Takvim.pdf"]:
    shutil.copy(KOK / f, OUT)
print("paket:", OUT, sorted(p.name for p in OUT.iterdir()))
