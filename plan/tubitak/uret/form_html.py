"""2209a-basvuru-metni.md'den TÜBİTAK Araştırma Önerisi Formu düzeninde tek parça HTML üretir.
Kullanım: python3 plan/tubitak/uret/form_html.py <logo.png> <çıktı.html>"""
import base64, html, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
s = (ROOT / "2209a-basvuru-metni.md").read_text(encoding="utf-8")
logo = base64.b64encode(open(sys.argv[1], "rb").read()).decode()

def sec(a, b):
    i = s.index(a) + len(a)
    return s[i:s.index(b, i)].strip()

def inline(t):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(t, quote=False))

def blocks(md):
    out = []
    for b in re.split(r"\n\s*\n", md.strip()):
        lines = b.split("\n")
        if all(re.match(r"\d+\.\s", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\.\s', '', l))}</li>" for l in lines) + "</ol>")
        elif not b.startswith(">"):
            out.append(f"<p>{inline(b.replace(chr(10), ' '))}</p>")
    return "".join(out)

def table(md, head):
    rows = [l for l in md.split("\n") if l.startswith("| ") and not l.startswith("|---")][1:]
    cells = [[c.strip() for c in r.split("|")[1:-1]] for r in rows]
    th = "".join(f"<th>{html.escape(h)}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"

title = sec("**Proje Başlığı** (en fazla 495 karakter)", "**Anahtar")
kw = sec("**Anahtar Kelimeler** (3–5, virgülle)", "**Bilimsel")
ozet = blocks(sec("**Proje Özeti** (25–450 kelime)", "\n---"))
s11 = blocks(sec("### 1.1. Konunun Önemi ve Araştırma Önerisinin Bilimsel Niteliği", "### 1.2."))
s12 = blocks(sec("### 1.2. Amaç ve Hedefler", "### 2. Yöntem"))
s2 = blocks(sec("### 2. Yöntem", "### 3.1."))
t31 = table(sec("### 3.1. Çalışma Takvimi", "### 3.2."), ["Proje Süresi (Ay)", "Faaliyetler", "Kim(ler) Tarafından Gerçekleştirileceği", "Başarı Ölçütü ve Araştırmanın Başarısına Katkısı"])
t32 = table(sec("### 3.2. Risk Yönetimi", "### 3.3."), ["En Önemli Riskler", "Alınacak Tedbirler (B Planı)"])
t33 = table(sec("### 3.3. Araştırma Olanakları", "### 4."), ["Kuruluşta Bulunan Altyapı/Ekipman Türü, Modeli (Laboratuvar, Araç, Makine-Teçhizat vb.)", "Projede Kullanım Amacı"])
t4 = table(sec("### 4. Araştırma Önerisinin Yaygın Etkisi", "### 5."), ["Çıktı, Etki ve Kazanımlar", "Öngörülen Çıktı(lar), Etki(ler) ve Kazanım(lar)"])
s5 = blocks(sec("### 5. Belirtmek İstediğiniz Diğer Konular", "### 6. Ekler"))
refs = [l for l in sec("## Kaynaklar (Kaynakça kutusu, en fazla 32.000 karakter)", "\n---").split("\n\n") if l.startswith("[")]
reflist = "".join(f"<p class='ref'>{html.escape(r)}</p>" for r in refs)

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 9.6pt; line-height: 1.38; color: #000; margin: 0; }
.cover { height: 255mm; display: flex; flex-direction: column; align-items: center; text-align: center; page-break-after: always; }
.cover img { width: 46mm; margin-top: 8mm; }
.cover h1 { font-size: 13pt; font-weight: 700; margin: 48mm 0 0; line-height: 1.35; }
.cover h2 { font-size: 13pt; font-weight: 700; margin: 26mm 0 0; }
.cover .yil { margin-top: 62mm; font-size: 11pt; }
.cover .donem { margin-top: 6mm; font-size: 11pt; }
.head { text-align: center; font-weight: 700; font-size: 10pt; line-height: 1.35; margin-bottom: 7mm; }
h3 { font-size: 10.5pt; font-weight: 700; margin: 6mm 0 2mm; break-after: avoid; page-break-after: avoid; }
h4 { font-size: 10pt; font-weight: 700; margin: 4mm 0 1.5mm; break-after: avoid; page-break-after: avoid; }
.box p, .box li { orphans: 3; widows: 3; }
.box { border: 0.6pt solid #000; padding: 2.4mm 3mm; margin-bottom: 2.5mm; }
.box p { margin: 0 0 2mm; text-align: justify; }
.box p:last-child { margin-bottom: 0; }
.box ol { margin: 0 0 2mm; padding-left: 5mm; }
.box li { margin-bottom: 1mm; text-align: justify; }
.lbl { font-weight: 700; }
table { width: 100%; border-collapse: collapse; margin-bottom: 3mm; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #d9d9d9; font-weight: 700; font-size: 9pt; border: 0.6pt solid #000; padding: 1.6mm; text-align: center; vertical-align: middle; }
td { border: 0.6pt solid #000; padding: 1.6mm; vertical-align: top; font-size: 9pt; }
td:first-child { }
.t31 td:first-child { text-align: center; width: 16mm; }
.ref { margin: 0 0 1.6mm; text-align: left; }
"""

doc = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>2209-A Araştırma Önerisi Formu</title><style>{CSS}</style></head><body>
<section class="cover"><img src="data:image/png;base64,{logo}" alt="TÜBİTAK"><h1>TÜBİTAK 2209-A ÜNİVERSİTE ÖĞRENCİLERİ ARAŞTIRMA<br>PROJELERİ DESTEKLEME PROGRAMI</h1><h2>ARAŞTIRMA ÖNERİSİ FORMU</h2><div class="yil">2026 Yılı</div><div class="donem">1. Dönem Başvurusu</div></section>
<div class="head">TÜBİTAK 2209-A ÜNİVERSİTE ÖĞRENCİLERİ ARAŞTIRMA PROJELERİ DESTEKLEME PROGRAMI<br>ARAŞTIRMA ÖNERİSİ FORMU<br>2026 Yılı 1. Dönem Başvurusu</div>
<h3>A. GENEL BİLGİLER</h3>
<div class="box"><span class="lbl">Başvuru Sahibinin Adı Soyadı:</span> LEVENT CAN CEYLAN</div>
<div class="box"><span class="lbl">Araştırma Önerisinin Başlığı:</span> {html.escape(title)}</div>
<div class="box"><span class="lbl">Akademik Danışmanın Adı Soyadı:</span> TAHA YİĞİT ALKAN</div>
<h3>ÖZET</h3><div class="box">{ozet}</div>
<div class="box"><span class="lbl">Anahtar Kelimeler:</span> {html.escape(kw)}</div>
<h3>1. ARAŞTIRMA ÖNERİSİNİN BİLİMSEL NİTELİĞİ</h3>
<h4>1.1. Konunun Önemi ve Araştırma Önerisinin Bilimsel Niteliği</h4><div class="box">{s11}</div>
<h4>1.2. Amaç ve Hedefler</h4><div class="box">{s12}</div>
<h3>2. YÖNTEM</h3><div class="box">{s2}</div>
<h3>3. PROJE YÖNETİMİ</h3>
<h4>3.1. Çalışma Takvimi</h4><div class="t31">{t31}</div>
<h4>3.2. Risk Yönetimi</h4>{t32}
<h4>3.3. Araştırma Olanakları</h4>{t33}
<h3>4. ARAŞTIRMA ÖNERİSİNİN YAYGIN ETKİSİ</h3>{t4}
<h3>5. BELİRTMEK İSTEDİĞİNİZ DİĞER KONULAR</h3><div class="box">{s5}</div>
<h3>6. EKLER</h3>
<h4>EK-1: KAYNAKLAR</h4><div class="box">{reflist}</div>
</body></html>"""
pathlib.Path(sys.argv[2]).write_text(doc, encoding="utf-8")
print("yazıldı", sys.argv[2], len(doc))
