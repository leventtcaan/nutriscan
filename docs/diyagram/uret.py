"""NutriScan akış diyagramı (tek sayfa) üretici.
Çalıştır: python3 docs/diyagram/uret.py  → docs/akis-diyagrami.html
Metin değişirse burada değiştir; koordinatlar ızgaradan hesaplanır.
"""
import html, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "akis-diyagrami.html"
W, H = 1540, 1446
LH = 15  # satır yüksekliği

svg = []
def add(s): svg.append(s)
e = html.escape

def lines(x, y, rows, cls="t", lh=LH):
    """rows: [(metin, sınıf_ek)]; y ilk satırın tabanı"""
    out = [f'<text x="{x}" y="{y}" class="{cls}">']
    for i, r in enumerate(rows):
        txt, extra = (r, "") if isinstance(r, str) else r
        dy = 0 if i == 0 else lh
        c = f' class="{extra}"' if extra else ""
        out.append(f'<tspan x="{x}" dy="{dy}"{c}>{e(txt)}</tspan>')
    out.append("</text>")
    add("".join(out))

def step(x, y, w, h, no, title, tech, example, risk):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="box"/>')
    add(f'<circle cx="{x+18}" cy="{y+20}" r="11" class="num"/>')
    add(f'<text x="{x+18}" y="{y+24}" class="numt" text-anchor="middle">{no}</text>')
    add(f'<text x="{x+36}" y="{y+25}" class="h">{e(title)}</text>')
    cy = y + 46
    lines(x + 12, cy, tech, "t"); cy += LH * len(tech) + 8
    if example:
        add(f'<line x1="{x+12}" y1="{cy-10}" x2="{x+w-12}" y2="{cy-10}" class="sep"/>')
        lines(x + 12, cy + 4, example, "ex"); cy += LH * len(example) + 12
    if risk:
        add(f'<rect x="{x+6}" y="{cy-8}" width="{w-12}" height="{LH*len(risk)+14}" rx="6" class="riskbg"/>')
        lines(x + 12, cy + 7, risk, "rk")

def store(x, y, w, h, title, rows, kind="db"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="store {kind}"/>')
    add(f'<text x="{x+12}" y="{y+22}" class="sh">{e(title)}</text>')
    lines(x + 12, y + 42, rows, "st")

def src(x, y, w, h, title, rows):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="src"/>')
    add(f'<text x="{x+10}" y="{y+20}" class="sh">{e(title)}</text>')
    lines(x + 10, y + 38, rows, "st")

def arrow(points, cls="flow", label=None, lx=None, ly=None, anchor="start"):
    pts = " ".join(f"{a},{b}" for a, b in points)
    add(f'<polyline points="{pts}" class="ln {cls}" marker-end="url(#m-{cls})"/>')
    if label:
        add(f'<text x="{lx}" y="{ly}" class="al {cls}t" text-anchor="{anchor}">{e(label)}</text>')

LANES = []
def lane(y, h, name, sub, tint):
    cy = y + h / 2
    LANES.append(f'<rect x="8" y="{y}" width="{W-16}" height="{h}" rx="12" class="lane {tint}"/>'
                 f'<text transform="translate(26,{cy}) rotate(-90)" text-anchor="middle" class="lane-h">{e(name)}</text>'
                 f'<text transform="translate(42,{cy}) rotate(-90)" text-anchor="middle" class="lane-s">{e(sub)}</text>')

# ---------------- şeritler
LA, LB, LC, LD = (16, 252), (282, 330), (626, 166), (806, 238)
lane(*LA, "TELEFON", "Expo · React Native", "la")
lane(*LB, "SERVİS", "Python · FastAPI · her taramada", "lb")
lane(*LC, "BİLGİ TABANI", "PostgreSQL + Qdrant", "lc")
lane(*LD, "ÖNCEDEN HAZIRLANIR", "ekip · bir kez", "ld")

# ---------------- telefon
ay, ah = 62, 190
step(30, ay, 196, ah, 1, "Profil + fotoğraf",
     ["Kullanıcı durumlarını seçer", "Profil yalnız telefonda", "Paketin arkası çekilir"],
     ["Selin: çölyak + diyabet"],
     ["Kural tablosunda olmayan", "durum → kapsam kartı uyarır"])
step(250, ay, 206, ah, 2, "OCR + düzeltme",
     ["Cihazda metin tanıma", "Kullanıcı hatayı düzeltir"],
     ["Fotoğraf → düz metin"],
     ["Okunamadı → tekrar çek / elle yaz", "Besin tablosu yok → miktar", "kuralları \"Doğrulanamadı\""])

ex_x, ex_y, ex_w = 480, 62, 736
add(f'<rect x="{ex_x}" y="{ex_y}" width="{ex_w}" height="132" rx="10" class="excard"/>')
add(f'<text x="{ex_x+14}" y="{ex_y+22}" class="sh">Örnek etiket · diyagramdaki bütün örnek değerler bu pakete ait</text>')
lines(ex_x + 14, ex_y + 48, [
    "İçindekiler: buğday unu, şeker, glikoz şurubu, bitkisel yağ (palm),",
    "             renklendirici (E102), eser miktarda süt içerebilir.",
    "Besin değerleri / 100 g: karbonhidrat 72 g · şekerler 48 g ·",
    "                         doymuş yağ 9 g · tuz 0,3 g",
], "mono", 18)

step(1240, ay, 240, ah, 8, "Sonuç ekranı",
     ["Durum başına 4 sonuçtan biri", "Gerekçe · kaynak · kapsam ▸"],
     ["Çölyak: Uygun değil (buğday)", "Diyabet: şeker 48 g/100 g"],
     ["Sunucuda hiçbir şey saklanmaz"])

# ---------------- servis
by, bh, bw = 330, 270, 238
xs = [30, 284, 538, 792, 1046]
step(xs[0], by, bw, bh, 3, "Böl + türle",
     ["Virgül ve paranteze göre böl", "\"sınıf: madde\", \"X içerir\" ayrılır", "\"içerebilir\" ve beyanlar ayrılır", "Türler aşağıdaki tabloda ↓"],
     ["renklendirici (E102) → sınıf+E102", "süt içerebilir → içerebilir: süt", "Glutensiz. → beyan, içerik değil"],
     ["Sayı/harf artığı (\"6\", \"b\") → gürültü", "Tanınmayan → \"bilinmeyen\""])
step(xs[1], by, bw, bh, 4, "Eşle (kimlik bul)",
     ["① E-kodu (E102, E 102, E-102)", "② birebir eşanlamlı (TR + EN)", "③ Türkçe çoğul (-ler/-lar)", "④ bulanık · ⑤ OFF'ta yoksa Qdrant vektör adayı"],
     ["E102 → Tartrazin (①)", "vericiler → verici (③ çoğul)", "60 etiket: tanınmayan %57 → %25"],
     ["OFF'ta olmayan terim → embedding + Qdrant adayı", "Aday doğrulama/kanonik bağlama açık iş", "Belirsizse tahmin yok"])
step(xs[2], by, bw, bh, 5, "Kural motoru (karar)",
     ["Her durum için kural türüne bak", "varlık · miktar · beyan · varsayılan", "IS_A: buğday unu → buğday", "7 durum · 17 kural · ağaç aşağıda ↓"],
     ["çölyak × buğday unu → Uygun değil", "diyabet × şeker 48 g → Dikkat", "glikoz şurubu → gluten sayılmaz"],
     ["Miktar gerekli, yok → besin tablosunu", "iste; gelmezse \"Doğrulanamadı\"", "Kural yok → \"Doğrulanamadı\"", "Tanınmayan varsa \"Engel yok\" denmez"])
step(xs[3], by, bw, bh, 6, "Kanıt ekle (bilgi)",
     ["Yalnız tekil kimyasallar için", "CTD: ilişki bildiren çalışmalar", "JECFA: katkı değerlendirmesi, ADI"],
     ["E102: CTD ilişkileri + JECFA", "→ \"Kaynaklar ▸\" altında"],
     ["İlişki ≠ neden → uyarı üretmez", "Etikette miktar yok → ADI", "hesabı yapılmaz, yalnız bilgi"])
step(xs[4], by, bw, bh, 7, "Mesajı yaz (LLM)",
     ["Girdi: yapılandırılmış sonuç", "LLM sade Türkçe metin yazar", "Denetleyici: sonuç aynı mı,", "yasaklı kelime var mı?"],
     ["\"Buğday unu içerdiği için", " çölyak açısından uygun değil.\""],
     ["Sonucu değiştirdi / \"güvenli\"", "yazdı → reddedilir → şablon", "LLM yanıt vermedi → şablon"])

# ---------------- bilgi tabanı
sy, sh_ = 668, 118
store(284, sy, 238, sh_, "kavram + eşanlamlı", ["5.459 kavram · 10.465 eşanlamlı", "+ 81 ekip çevirisi (2 onay)", "İlişki: SAME_AS · IS_A ·", "CONTEXTUAL · üst kavram zinciri"])
store(538, sy, 238, sh_, "Qdrant", ["Yalnız alias vektörleri", "+ concept_id etiketi", "Kapatılıp açılarak ölçülür"], "vec")
store(792, sy, 238, sh_, "kurallar + kanıt haritası", ["17 kural · 7 durum", "tür · hedef · sonuç · eksik veri", "kaynak · doğrulama · 2 onay"], "rule")
store(1046, sy, 238, sh_, "evidence", ["CTD / JECFA kayıtları", "ilişki türü · çalışma sayısı", "Yalnız bilgi, karar vermez"])
store(1300, sy, 180, sh_, "source", ["Kaynak + lisans", "sürüm · indirme tarihi", "Kaydı olmayan", "veri girmez"])

# ---------------- kaynaklar
dy, dh = 890, 100
src(30, dy, 210, dh, "OFF taksonomileri (ODbL)", ["içerik · katkı · katkı sınıfı", "TR/EN adlar, IS_A zinciri"])
src(252, dy, 200, dh, "Ekip çevirisi", ["tanınmayan sık ifadeler", "→ Türkçe karşılık, 2 onay"])
src(464, dy, 200, dh, "CTD sözlüğü + PubChem", ["Kimyasal adları, CAS, MeSH,", "eşanlamlılar"])
src(676, dy, 150, dh, "Embedding modeli", ["Çok dilli; alias", "metinleri → vektör"])
src(838, dy, 230, dh, "Mevzuat + kılavuzlar", ["AB 1169/2011 · 1924/2006 · 828/2014", "WHO 2012 · EFSA 2010 · KDIGO 2024"])
src(1080, dy, 200, dh, "CTD ilişkileri + JECFA", ["kimyasal–hastalık ilişkileri", "katkı değerlendirmeleri"])
src(1292, dy, 188, dh, "Ekip denetimi", ["2 kişi bağımsız onay", "lisans kaydı"])

# ---------------- akış okları (ana yol)
mid = by + 21
arrow([(226, 157), (250, 157)], "flow")
arrow([(353, 252), (353, 300), (149, 300), (149, by)], "flow", "metin + besin değerleri + profil (HTTPS)", 158, 318)
for x0 in (268, 522, 776, 1030):
    arrow([(x0, mid), (x0 + 16, mid)], "flow")
arrow([(1284, mid), (1360, mid), (1360, 252)], "flow", "mesaj + gerekçe", 1368, 296)

# ---------------- eksik veri: kural motoru telefondan besin tablosunu ister
arrow([(620, by), (620, 272), (430, 272), (430, 252)], "ask", "miktar gerekli → \"besin tablosunu da okut\"", 440, 268)

# ---------------- veri okuma (taramada)
arrow([(360, by + bh), (360, sy)], "data", "okur", 366, 640)
arrow([(480, by + bh), (480, 626 + 6), (657, 626 + 6), (657, sy)], "data", "③ benzer alias", 560, 626)
arrow([(911, by + bh), (911, sy)], "data", "kuralları okur", 917, 640)
arrow([(1165, by + bh), (1165, sy)], "data", "okur", 1171, 640)

# ---------------- hazırlık
bus = 866
arrow([(135, dy), (135, bus), (403, bus), (403, sy + sh_)], "prep", "içe aktar + 2 onay", 412, bus - 6)
arrow([(352, dy), (352, bus)], "prep")
arrow([(564, dy), (564, bus), (403, bus)], "prep")
arrow([(522, sy + 60), (538, sy + 60)], "prep")
arrow([(751, dy), (751, 846), (657, 846), (657, sy + sh_)], "prep", "vektöre çevir", 666, 840)
arrow([(953, dy), (953, bus), (911, bus), (911, sy + sh_)], "prep", "kurala çevir + 2 onay", 920, bus - 6)
arrow([(1180, dy), (1180, bus), (1165, bus), (1165, sy + sh_)], "prep", "seçili maddeler", 1188, bus - 6)
arrow([(1386, dy), (1386, sy + sh_)], "prep", "kaydeder", 1394, bus - 6)

# ---------------- adımların içi: türler (3. adım) ve karar ağacı (5. adım)
LE = (1060, 372)
lane(*LE, "ADIMLARIN İÇİ", "3. ve 5. adım ayrıntı", "lc")
ty = 1086
add(f'<text x="30" y="{ty+14}" class="h">3. adımın içi: etiketteki ifade türleri</text>')
cols = (30, 214, 424)
rows = [("Tür", "Örnek", "Nereye gider", "sh"),
        ("katkı maddesi (E-kodu)", "E102, E330", "varlık kuralı + CTD bilgisi", "t"),
        ("katkı sınıfı", "renklendirici, emülgatör", "yalnız etiket: madde değil", "t"),
        ("gıda kavramı", "buğday unu, glikoz şurubu", "IS_A zinciri → varlık kuralı", "t"),
        ("  (tekil / karışım / hammadde)", "gluten = karışım", "ayrımı kuralın türü belirler", "st"),
        ("besin değeri (tablodan)", "şekerler 48 g, tuz 0,3 g", "miktar kuralı", "t"),
        ("beyan", "glutensiz", "beyan kuralı", "t"),
        ("içerebilir", "eser miktarda süt", "içerebilir kuralı → Dikkat", "t"),
        ("bilinmeyen", "çevrilmemiş ifade", "\"Engel bulunmadı\"yı engeller", "t"),
        ("gürültü", "\"6\", \"b\"", "sayılmaz", "t")]
yy = ty + 44
for a, b, c, cls in rows:
    for x, txt in zip(cols, (a, b, c)):
        add(f'<text x="{x}" y="{yy}" class="{cls}">{e(txt)}</text>')
    add(f'<line x1="30" y1="{yy+8}" x2="690" y2="{yy+8}" class="sep"/>')
    yy += 29

tx = 726
add(f'<text x="{tx}" y="{ty+14}" class="h">5. adımın içi: kullanıcının her durumu için karar ağacı</text>')
add(f'<rect x="{tx}" y="{ty+30}" width="754" height="40" rx="8" class="box"/>')
add(f'<text x="{tx+377}" y="{ty+55}" class="sh" text-anchor="middle">Kılavuz / mevzuat bu durum için neye bakıyor?</text>')
bx = [(tx, 236, "VARLIK", ["çölyak × gluten · PKU × aspartam", "IS_A zincirinde hedef var mı?"],
       [("var → Uygun değil", "rk"), ("\"içerebilir\" → Dikkat", "rk"), ("yok + beyan → Engel bulunmadı", "t"), ("yok, beyan yok → Dikkat", "t")]),
      (tx + 258, 236, "MİKTAR", ["diyabet × şeker · böbrek × sodyum", "besin tablosu var mı?"],
       [("var → yasal bantla karşılaştır", "t"), ("bant üstü → Dikkat", "rk"), ("yok → kullanıcıdan iste", "t"), ("gelmezse → Doğrulanamadı", "t")]),
      (tx + 516, 238, "KURAL YOK", ["astım × E102 · fosfat (bekliyor)", "mevzuat/kılavuz bir şey demiyor"],
       [("→ Doğrulanamadı", "t"), ("+ CTD'den araştırma bilgisi", "t"), ("  (uyarı değil, kaynakla)", "st")])]
for x, w, title, sub, outs in bx:
    add(f'<rect x="{x}" y="{ty+96}" width="{w}" height="214" rx="10" class="box"/>')
    add(f'<text x="{x+12}" y="{ty+120}" class="h">{e(title)}</text>')
    lines(x + 12, ty + 142, sub, "st")
    add(f'<line x1="{x+12}" y1="{ty+178}" x2="{x+w-12}" y2="{ty+178}" class="sep"/>')
    lines(x + 12, ty + 198, [(o, c) for o, c in outs], "t", 19)
    arrow([(x + w / 2, ty + 70), (x + w / 2, ty + 96)], "flow")
add(f'<text x="{tx}" y="{ty+334}" class="st">Her durumda: tanınmayan içerik varsa \"Engel bulunmadı\" → \"Doğrulanamadı\". Ayrımı içeriğin türü değil kuralın türü belirler.</text>')

svg_txt = "\n".join(LANES) + '\n<g transform="translate(44,0)">\n' + "\n".join(svg) + "\n</g>"

PAGE = f'''<title>NutriScan Akış Diyagramı</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: tek figür; yatay akan diyagram kendi kabında kayar, sayfa kaymaz */
:root{{
  --bg:#f4f6f5; --ink:#17201c; --muted:#5b6862; --line:#cfd7d2; --box:#ffffff;
  --la:#eef2fb; --lb:#eef5f1; --lc:#f3f0fa; --ld:#f6f3ec;
  --flow:#2f43b0; --data:#0f7a6e; --prep:#8a6a1e; --risk:#b3261e; --riskbg:#fdeceb;
  --vec:#e8eefc; --rule:#e7f3ec; --ex:#5b3fa0;
  --f-d:"Bricolage Grotesque",ui-sans-serif,system-ui,sans-serif;
  --f-b:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  --f-m:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{
  --bg:#101513; --ink:#e4ebe7; --muted:#9aa8a1; --line:#33403a; --box:#18201d;
  --la:#161c2a; --lb:#14211b; --lc:#1c1828; --ld:#211d14;
  --flow:#93a3ff; --data:#5fd0c0; --prep:#e0b765; --risk:#ff8a80; --riskbg:#3a1714;
  --vec:#1d2540; --rule:#16301f; --ex:#c2a8ff; color-scheme:dark}}}}
:root[data-theme="dark"]{{
  --bg:#101513; --ink:#e4ebe7; --muted:#9aa8a1; --line:#33403a; --box:#18201d;
  --la:#161c2a; --lb:#14211b; --lc:#1c1828; --ld:#211d14;
  --flow:#93a3ff; --data:#5fd0c0; --prep:#e0b765; --risk:#ff8a80; --riskbg:#3a1714;
  --vec:#1d2540; --rule:#16301f; --ex:#c2a8ff; color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font:400 15px/1.55 var(--f-b);margin:0}}
.wrap{{max-width:1620px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 48px;display:grid;gap:16px}}
h1{{font:700 clamp(24px,3vw,34px)/1.15 var(--f-d);margin:0;text-wrap:balance}}
p{{margin:0;max-width:95ch}} .muted{{color:var(--muted)}}
.legend{{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:13.5px;align-items:center}}
.legend span{{display:inline-flex;gap:8px;align-items:center}}
.legend i{{display:inline-block;width:28px;height:0;border-top:2.5px solid currentColor}}
.legend i.d{{border-top-style:dashed}} .legend i.p{{border-top-style:dotted}}
.legend b{{display:inline-block;width:14px;height:14px;border-radius:4px}}
.k-flow{{color:var(--flow)}} .k-data{{color:var(--data)}} .k-prep{{color:var(--prep)}} .k-risk{{color:var(--risk)}} .k-ex{{color:var(--ex)}}
figure{{margin:0;display:grid;gap:10px}}
.scroll{{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--bg)}}
svg{{display:block;width:100%;min-width:1240px;max-width:{W}px;height:auto;margin:0 auto}}
figcaption{{font-size:14px;color:var(--muted)}}
/* svg sınıfları */
.lane{{stroke:none}} .la{{fill:var(--la)}} .lb{{fill:var(--lb)}} .lc{{fill:var(--lc)}} .ld{{fill:var(--ld)}}
.lane-h{{font:700 13px var(--f-m);letter-spacing:.08em;fill:var(--ink)}} .lane-s{{font:400 11px var(--f-m);fill:var(--muted)}}
.box{{fill:var(--box);stroke:var(--line);stroke-width:1.2}}
.excard{{fill:var(--box);stroke:var(--ex);stroke-width:1.2;stroke-dasharray:5 4}}
.num{{fill:var(--flow)}} .numt{{font:600 12px var(--f-b);fill:var(--box)}}
.h{{font:700 14.5px var(--f-d);fill:var(--ink)}}
.t{{font:400 12.5px var(--f-b);fill:var(--ink)}}
.ex{{font:500 11px var(--f-m);fill:var(--ex)}}
.mono{{font:400 13px var(--f-m);fill:var(--ink)}}
.rk{{font:500 12px var(--f-b);fill:var(--risk)}}
.riskbg{{fill:var(--riskbg)}}
.sep{{stroke:var(--line);stroke-width:1}}
.store{{fill:var(--box);stroke:var(--data);stroke-width:1.4}} .store.vec{{fill:var(--vec)}} .store.rule{{fill:var(--rule)}}
.src{{fill:var(--box);stroke:var(--prep);stroke-width:1.2;stroke-dasharray:3 3}}
.sh{{font:600 13px var(--f-b);fill:var(--ink)}} .st{{font:400 12px var(--f-b);fill:var(--muted)}}
.ln{{fill:none;stroke-width:2;stroke-linejoin:round}}
.flow{{stroke:var(--flow);stroke-width:2.6}} .data{{stroke:var(--data);stroke-dasharray:6 4}} .prep{{stroke:var(--prep);stroke-dasharray:2 4;stroke-linecap:round}} .ask{{stroke:var(--risk);stroke-width:2;stroke-dasharray:7 4}}
.al{{font:500 11.5px var(--f-m)}} .flowt{{fill:var(--flow)}} .datat{{fill:var(--data)}} .prept{{fill:var(--prep)}}
.mk-flow{{fill:var(--flow)}} .mk-data{{fill:var(--data)}} .mk-prep{{fill:var(--prep)}} .mk-ask{{fill:var(--risk)}} .askt{{fill:var(--risk)}}
.say{{border-left:3px solid var(--flow);padding-left:14px;max-width:110ch}}
</style>
<div class="wrap">
  <h1>NutriScan: bir etiketin baştan sona yolculuğu</h1>
  <p class="muted">Soldan sağa ana yol (1 → 8). Her kutuda: ne yapar · nasıl · örnek değer · <span class="k-risk">ters giderse</span>. Alt şeritler, adımların okuduğu veriyi ve o verinin nereden geldiğini gösterir.</p>
  <div class="legend">
    <span class="k-flow"><i></i>ana akış (her taramada)</span>
    <span class="k-data"><i class="d"></i>bilgi tabanından okuma</span>
    <span class="k-prep"><i class="p"></i>önceden hazırlık (ekip)</span>
    <span class="k-ex"><b style="background:currentColor;opacity:.25"></b>örnek değer</span>
    <span class="k-risk"><i class="d"></i>eksik veriyi kullanıcıdan iste</span>
    <span class="k-risk"><b style="background:var(--riskbg);border:1px solid currentColor"></b>ters giderse</span>
  </div>
  <figure>
    <div class="scroll">
      <svg viewBox="0 0 {W} {H}" role="img" aria-label="NutriScan akışı: telefonda fotoğraf ve OCR, serviste böl-türle, eşle (sözlük, bulanık, Qdrant), kural motoru karar verir, kanıt bilgi olarak eklenir, LLM mesajı yazar ve denetlenir, sonuç telefonda gösterilir; bilgi tabanı ve kaynakları altta.">
        <defs>
          <marker id="m-flow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mk-flow"/></marker>
          <marker id="m-data" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mk-data"/></marker>
          <marker id="m-ask" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mk-ask"/></marker>
          <marker id="m-prep" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mk-prep"/></marker>
        </defs>
{svg_txt}
      </svg>
    </div>
    <figcaption>Sağlık sonucunu yalnız gözden geçirilmiş kural tablosu verir. OFF taksonomisinde olmayan terimler Qdrant vektör aramasıyla eşleşme adayı alır; aday doğrulama ve kanonik kavrama bağlama yöntemi açık iştir. CTD/JECFA araştırma bilgisi sağlar; LLM/araçlar kural araştırması ve taslağına yardım edebilir, doğrulanmamış kural etkinleştirilmez.</figcaption>
  </figure>
  <p class="say"><b>Kural hazırlığı.</b> AI veya uygun araçlar resmî mevzuat ve klinik kılavuzlardan kaynak konumu belirtilmiş taslak kural satırları çıkarabilir. İki ekip üyesi satırı kaynağından bağımsız doğrulamadan kural tablosuna girmez; AI eşik uydurmaz, kuralı onaylamaz ve kullanıcı sonucunu belirlemez. Araç seçimi henüz açık.</p>
  <p class="say"><b>60 saniyede anlatım.</b> Kullanıcı sağlık durumlarını seçip paketin arkasının fotoğrafını çeker; metin telefonda okunur ve gerekirse düzeltilir. Servis listeyi parçalara ayırır ve her parçanın türünü belirler: tek bir madde mi, sınıf mı, karışım mı, hammadde mi, besin değeri mi. Sonra önce sözlükte birebir ve bulanık eşleşmeyi dener; OFF taksonomisinde bulunmayan içerik/kimyasal terimler embedding edilerek Qdrant'ta aday aranır. Adayı doğrulama ve kanonik kimliğe bağlama yöntemi netleşene kadar emin olunmayan eşleşmeye karar verilmez. Kimliği belli parçalar kural tablosuna gider: çölyakta buğday varsa "Uygun değil", diyabette şeker miktarı besin tablosundan okunur. Tek maddeler için CTD ve JECFA'dan bilgi eklenir ama uyarı üretmez. LLM sonucu sade Türkçeye çevirir; sonucu değiştirirse ya da yanıt vermezse şablon metin gösterilir. Bilgi tabanını ekip önceden doldurur: Gıda Kodeksi, OFF taksonomisi ve CTD sözlüğünden eşanlamlılar, klinik kılavuzlardan iki kişi onaylı kurallar.</p>
</div>
'''
OUT.write_text(PAGE, encoding="utf-8")
print("yazıldı:", OUT)
