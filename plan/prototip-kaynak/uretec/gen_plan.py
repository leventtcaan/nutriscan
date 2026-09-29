"""Grup: plan-liste-asistan. M28–M33 (plan, menü, liste) ve M42–M45 (asistan).
Kararı Hane Planlama Motoru (MSM) ve kural motoru verir; asistan (LLM) yalnız anlatır.
Çalıştır: python3 gen_plan.py  → project/<stem>.dc.html + check() çıktısı.
"""
from lib import *

G = "plan-liste-asistan"

# ---------------------------------------------------------------- küçük yardımcılar (yalnız bu grup)
SCROLL = ('class="pad" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; '
          'padding-top: 4px; padding-bottom: 8px"')


def scroll(inner, extra=""):
    return f'<div {SCROLL[:-1]}{extra}">{inner}</div>'


def bar(inner):
    return (f'<div class="pad" style="display: flex; gap: 8px; padding-top: 8px; padding-bottom: 22px; flex-shrink: 0; '
            f'border-top: 1px solid #ece5d6; background: #f5f1e8">{inner}</div>')


def st(text, s="done"):
    """Canlı adım satırı: done · run · wait · err · warn."""
    dots = {
        "done": f'<span class="dot">{icon("check", 10, 3.2)}</span>',
        "run": f'<span class="dot" style="background: #f7e8c4; color: #6b4700">{icon("clock", 10, 3)}</span>',
        "wait": '<span class="dot" style="background: #e9e3d6"></span>',
        "err": f'<span class="dot" style="background: #f6ddd6; color: #7d2317">{icon("x", 10, 3.2)}</span>',
        "warn": f'<span class="dot" style="background: #f7e8c4; color: #6b4700">{icon("alert", 10, 3.2)}</span>',
    }
    tstyle = {"run": ' style="font-weight: 700; color: #1c2420"', "wait": ' class="mut"'}.get(s, "")
    return f'<div class="step">{dots[s]}<span{tstyle}>{text}</span></div>'


def gapchip(text, proven=True):
    """Optimallik rozeti. Hüküm rozeti değildir; biçimi (hap, şimşek) hükümlerden ayrışır."""
    c = ("border-color: #bcd6c6; background: #eef5f0; color: #17503a" if proven
         else "border-color: #e6d7a9; background: #fbf5e3; color: #5e4d17")
    return f'<span class="chip" style="{c}">{icon("bolt", 13, 2.2)}{text}</span>'


def progress(pct, color="#1f5c45"):
    return (f'<div style="height: 6px; border-radius: 3px; background: #e9e3d6; overflow: hidden">'
            f'<div style="width: {pct}%; height: 6px; background: {color}"></div></div>')


def sechead(title, meta=""):
    m = f'<span class="mut" style="font-size: 12px">{meta}</span>' if meta else ""
    return (f'<div style="display: flex; justify-content: space-between; align-items: baseline; padding-top: 6px">'
            f'<span style="font-size: 13px; font-weight: 700; color: #3d4742">{title}</span>{m}</div>')


def srctag(t):
    return f'<span class="mut" style="font-size: 11.5px; border: 1px solid #e2dbcb; border-radius: 6px; padding: 0 5px">{t}</span>'


def skel(w="100%", h=14):
    return f'<div class="skel" style="width: {w}; height: {h}px"></div>'


def mem(letter, name, sub, v):
    return (f'<div class="li" style="font-size: 14px">{av(letter)}<span style="flex-grow: 1"><b style="display: block; '
            f'font-size: 14px">{name}</b><span class="mut" style="font-size: 12px">{sub}</span></span>{v}</div>')


def foot(t):
    return f'<div class="mono" style="text-align: center; padding-top: 2px">{t}</div>'


def inputbar(placeholder="Bir şey sor ya da yaz…", disabled=False, value=""):
    dis = ' disabled=""' if disabled else ""
    val = f' value="{value}"' if value else ""
    bg = "#eceae4" if disabled else "#fff"
    micbg = "#b9beb9" if disabled else "#1f5c45"
    return (f'<div class="pad" style="padding-top: 8px; padding-bottom: 8px; display: flex; gap: 8px; align-items: center; flex-shrink: 0">'
            f'<label style="flex-grow: 1; display: flex; align-items: center; height: 46px; border: 1.5px solid #cfc6b3; border-radius: 23px; '
            f'background: {bg}; padding: 0 16px"><input type="text" placeholder="{placeholder}" aria-label="Asistana yaz"{dis}{val} '
            f'style="border: 0; outline: 0; font: inherit; font-size: 14.5px; width: 100%; background: transparent"></label>'
            f'<button type="button" aria-label="Sesle sor"{dis} style="width: 46px; height: 46px; border-radius: 50%; border: 0; '
            f'background: {micbg}; color: #fff; display: flex; align-items: center; justify-content: center">{icon("mic", 20, 2)}</button></div>')


def ok(t="Engel bulunmadı"):
    return verdict("ok", t)


# ================================================================ M28 · Plan hazırlanıyor
def m28():
    eb = "Plan · 29 Eylül – 3 Ekim"

    def shell(steps, card, actions, title="Planın hazırlanıyor", cap="Hane Planlama Motoru çalışıyor"):
        b = header(title, back="M18-Menu.dc.html", eb=eb)
        b += scroll(
            f'<div class="card" style="display: flex; flex-direction: column; gap: 2px">'
            f'<div style="font-size: 13px; font-weight: 700; color: #3d4742; padding-bottom: 4px">{cap}</div>'
            f'{steps}</div>{card}'
            f'{foot("karar motordan · asistan yalnız anlatır")}')
        return phone(b + bar(actions))

    s_done = (st("Kileri okudum · 12 kalem, 2'sinin SKT'si bu hafta") +
              st("84 tariften 31'i kesin kısıtlara takıldı, elendi · 53 aday kaldı"))

    # 1 · çözülüyor
    run = (s_done +
           st("Menü, liste ve market birlikte çözülüyor", "run") +
           f'<div style="padding: 4px 0 6px 24px; display: flex; flex-direction: column; gap: 5px">{progress(60)}'
           f'<div style="display: flex; justify-content: space-between" class="mono"><span>1,8 sn</span><span>zaman sınırı 3 sn</span></div></div>' +
           st("Sonuç kural motoruyla yeniden kontrol edilecek", "wait"))
    sk = "".join(
        f'<div class="card" style="display: flex; gap: 12px; align-items: center"><span class="eb" style="width: 34px">{d}</span>'
        f'<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 6px">{skel("70%")}{skel("40%", 10)}</div></div>'
        for d in ["PZT", "SAL", "ÇAR", "PER", "CUM"])
    p1 = shell(run, sk, '<a class="btn2" href="M18-Menu.dc.html" style="flex: 1">Vazgeç</a>')

    def summary(total, extra=""):
        return (f'<div class="card" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; text-align: center">'
                f'<div><div style="font-size: 21px; font-weight: 700">5</div><div class="mut" style="font-size: 12px">akşam yemeği</div></div>'
                f'<div><div style="font-size: 21px; font-weight: 700">{total}</div><div class="mut" style="font-size: 12px">bütçe 6.500</div></div>'
                f'<div><div style="font-size: 21px; font-weight: 700">2</div><div class="mut" style="font-size: 12px">market</div></div></div>{extra}')

    # 2 · kanıtlı en iyi
    s2 = s_done + st("Menü, liste ve market birlikte çözüldü · 0,8 sn") + st("Kural motoru yeniden kontrol etti · 20 öğün, 0 ihlal")
    c2 = summary("5.940 TL",
                 f'<div class="card" style="display: flex; flex-direction: column; gap: 8px">{gapchip("Çözüm 0,8 sn · en iyisi kanıtlandı (boşluk %0)")}'
                 f'<div style="font-size: 13.5px; line-height: 1.45">Bu kısıtlarla daha ucuz bir plan yok; motor bunu kanıtladı.</div>'
                 f'<div style="display: flex; justify-content: space-between; align-items: center"><span class="dr">DR pln_42c1</span>'
                 f'<a class="why" href="M31-PlanNedenMobil.dc.html">Bu plan neden böyle?</a></div></div>')
    p2 = shell(s2, c2, '<a class="btn" href="M29-PlanFarki.dc.html" style="flex: 1">Planı gör</a>', "Planın hazır", "Hane Planlama Motoru bitirdi")

    # 3 · süre doldu
    s3 = (s_done + st("3 sn doldu · bulunan en iyi plan tutuldu", "warn") +
          st("Kural motoru yeniden kontrol etti · 20 öğün, 0 ihlal"))
    c3 = summary("6.020 TL",
                 f'<div class="card" style="display: flex; flex-direction: column; gap: 8px">{gapchip("En iyiye en fazla %[..] uzak", False)}'
                 f'<div style="font-size: 13.5px; line-height: 1.45">3 saniyede en iyisi kanıtlanamadı. Kesin kısıtlar bu planda da korunuyor; '
                 f'yalnız biraz daha ucuz bir plan olabilir.</div>'
                 f'<div style="display: flex; justify-content: space-between; align-items: center"><span class="dr">DR pln_42c2</span>'
                 f'<a class="why" href="M31-PlanNedenMobil.dc.html">Bu plan neden böyle?</a></div></div>')
    p3 = shell(s3, c3, '<button class="btn2" type="button" style="flex: 1">Biraz daha ara</button>'
                       '<a class="btn" href="M29-PlanFarki.dc.html" style="flex: 1.3">Bu planı gör</a>', "Plan hazır, süre doldu", "Hane Planlama Motoru süre sınırında durdu")

    # 4 · olursuz
    s4 = s_done + st("Birlikte çözüldü · bu kısıtlarla plan yok", "err") + st("Kontrol edilecek plan çıkmadı", "wait")
    c4 = (banner("warn", "<b>Bu kısıtlarla plan çıkmadı.</b> Bir hata yok; bütçe, süre ve kesin kısıtlar aynı anda sağlanamıyor.") +
          '<div class="card" style="display: flex; flex-direction: column; gap: 8px"><div style="font-size: 13px; font-weight: 700; color: #3d4742">Çakışan sınırlar</div>'
          f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{chip_soft("Bütçe ≤ 4.000 TL")}{chip_soft("Hafta içi ≤ 45 dk")}'
          f'{chip_hard("Selin: gluten")}{chip_hard("Ela: fındık, yer fıstığı")}</div>'
          f'<div style="display: flex; gap: 8px; font-size: 13px; color: #3d4742; line-height: 1.45">{icon("lock", 16, 2)}'
          f'<span>Kesin kısıtları hiçbir seçenekte gevşetmiyoruz; yalnız yumuşak sınırlar değişebilir.</span></div></div>')
    p4 = shell(s4, c4, '<a class="btn" href="M08-Olursuz.dc.html" style="flex: 1">Seçenekleri gör</a>', "Plan çıkmadı", "Hane Planlama Motoru bitirdi")

    # 5 · sunucu hatası
    s5 = st("Kileri okudum · 12 kalem") + st("Sunucuya ulaşılamadı · plan hazırlanamadı", "err") + st("Kontrol yapılmadı", "wait")
    c5 = (banner("err", "<b>Sunucuya ulaşılamıyor.</b> Eski planın ve listen yerinde; hiçbir şey değişmedi.") +
          '<div class="card" style="display: flex; flex-direction: column; gap: 8px; font-size: 13.5px; line-height: 1.45">'
          '<b>Planı elle kurabilirsin</b><span>Menüden yemekleri kendin seç. Sunucu dönünce her yemek kural motorundan geçer; '
          'o zamana kadar sonucu şöyle görünür:</span>'
          f'<div>{verdict("unk")}</div></div>')
    p5 = shell(s5, c5, '<button class="btn2" type="button" style="flex: 1">Tekrar dene</button>'
                       '<a class="btn" href="M18-Menu.dc.html" style="flex: 1.3">Planı elle kur</a>', "Plan hazırlanamadı", "Hane Planlama Motoru durdu")

    return states_board([("Çözülüyor · 3 sn sınırı", p1), ("Kanıtlı en iyi · boşluk %0", p2),
                         ("Süre doldu · Biraz daha ara", p3), ("Olursuz → M08", p4), ("Sunucu hatası · Planı elle kur", p5)])


# ================================================================ M29 · Plan farkı
def dayrow(day, old, new=None, note=""):
    if new:
        body = (f'<div style="font-size: 14px"><span class="mut" style="text-decoration: line-through">{old}</span></div>'
                f'<div style="font-size: 14.5px; font-weight: 700">{new}</div>')
        tag = f'<span class="chip" style="border-color: #1f5c45; color: #1f5c45">değişti</span>'
    else:
        body = f'<div style="font-size: 14px">{old}</div>'
        tag = '<span class="mut" style="font-size: 12px">aynı</span>'
    n = f'<div class="mut" style="font-size: 12px">{note}</div>' if note else ""
    return (f'<div class="li" style="align-items: flex-start"><span class="eb" style="width: 34px; padding-top: 2px">{day}</span>'
            f'<div style="flex-grow: 1">{body}{n}</div>{tag}</div>')


def listdiff(sign, name, p):
    col = "#17503a" if sign == "+" else "#7d2317"
    return (f'<div class="li"><span style="width: 18px; font-weight: 700; color: {col}">{"+" if sign == "+" else "−"}</span>'
            f'<span style="flex-grow: 1">{name}</span>{p}</div>')


def m29():
    diff = (
        '<div class="card" style="padding-top: 6px; padding-bottom: 4px">' +
        dayrow("PZT", "Ispanaklı yumurta") + dayrow("SAL", "Mercimek çorbası + pirinç pilavı") +
        dayrow("ÇAR", "Fırında tavuk ve patates", note="Balık yok · zaten uyuyordu") +
        dayrow("PER", "Zeytinyağlı taze fasulye + yoğurt") +
        dayrow("CUM", "Ev yapımı pizza · 4 kişi", "Patates oturtma + pirinç pilavı · 6 kişi", "misafirlerden biri glutensiz; tek tencere, ayrı taban gerekmez") +
        '</div>')
    lst = ('<div class="card" style="padding-top: 8px; padding-bottom: 4px"><div style="font-size: 13px; font-weight: 700; color: #3d4742">Listede</div>' +
           listdiff("+", "Kıyma 1 kg", price("459,00 TL", "ŞOK", "26 Eyl")) +
           listdiff("+", "Patates 2 kg", price("69,90 TL", "Tarım Kredi", "27 Eyl")) +
           listdiff("+", "Pirinç 1 kg", price("64,50 TL", "Tarım Kredi", "27 Eyl")) +
           listdiff("+", "Yoğurt 1 kg", price("56,00 TL", "ŞOK", "26 Eyl")) +
           listdiff("-", "Glutensiz pizza tabanı 2'li", price("119,90 TL", "Tarım Kredi", "27 Eyl")) +
           listdiff("-", "Mozzarella 200 g", price("89,50 TL", "ŞOK", "26 Eyl")) + '</div>')
    top = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
        '<div style="display: flex; justify-content: space-between; align-items: baseline"><span style="font-size: 13px; font-weight: 700; color: #3d4742">Bütçe</span>'
        '<span><span class="mut">5.940 TL</span> → <b style="font-size: 18px">6.380 TL</b> <span class="mut" style="font-size: 12px">/ 7.000 bu hafta</span></span></div>'
        f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{gapchip("0,9 sn · en iyisi kanıtlandı (boşluk %0)")}</div>'
        f'<div style="display: flex; gap: 8px; font-size: 13px; line-height: 1.4">{ok("0 ihlal")}'
        '<span>Kesin kısıtlar: 22 öğün kontrol edildi (4 kişi × 5 akşam + Cuma 2 misafir).</span></div>'
        '<div style="display: flex; justify-content: space-between; align-items: center; font-size: 12.5px">'
        '<a href="A01-KararIzi.dc.html" style="font-weight: 700">Karar izi · <span class="dr">DR pln_43a7</span></a>'
        '<a class="why" href="M31-PlanNedenMobil.dc.html">Neden böyle?</a></div>'
        '</div>')
    chains = (
        '<a class="card" href="M12-Market.dc.html" style="display: flex; gap: 10px; align-items: center; text-decoration: none; color: #1c2420">'
        f'{icon("store", 20)}<span style="flex-grow: 1"><b style="display: block; font-size: 14px">ŞOK 9 kalem · Tarım Kredi 8 kalem</b>'
        '<span class="mut" style="font-size: 12px">online katalog fiyatı · ŞOK 26 Eyl · Tarım Kredi 27 Eyl</span></span>'
        f'{icon("chev", 18)}</a>')
    b1 = header("Plan farkı", back="M28-PlanHazirlaniyor.dc.html", eb="Cuma 6 kişi · bütçe ≤ 7.000 TL")
    b1 += scroll(top + chains + diff + lst +
                 '<div class="mut" style="font-size: 12.5px; text-align: center">Onaylamadan hiçbir şey değişmez.</div>')
    p1 = phone(b1 + bar('<a class="btn2" href="M18-Menu.dc.html" style="flex: 1">Vazgeç</a>'
                        '<button class="btn" type="button" style="flex: 1.4">Onayla</button>'))

    # 2 · onaylandı + geri al
    def meal(day, name, sub, extra=""):
        return (f'<div class="card" style="display: flex; gap: 12px; align-items: flex-start"><span class="eb" style="width: 34px; padding-top: 2px">{day}</span>'
                f'<div style="flex-grow: 1"><div style="font-weight: 700; font-size: 15px">{name}</div><div class="mut" style="font-size: 12.5px; margin-top: 2px">{sub}</div>'
                f'<div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px">{extra}</div></div></div>')
    b2 = ('<div style="padding: 18px 16px 6px"><div class="eb">29 Eylül – 3 Ekim · hafta içi akşam</div>'
          '<h1 class="disp" style="font-size: 24px; margin-top: 2px">Bu haftanın menüsü</h1></div>')
    b2 += scroll(
        meal("PZT", "Ispanaklı yumurta", "15 dk · kilerdeki ıspanak", ok("4 kişi için engel yok")) +
        meal("SAL", "Mercimek çorbası + pirinç pilavı", "35 dk", ok("4 kişi için engel yok")) +
        meal("ÇAR", "Fırında tavuk ve patates", "45 dk · balık yok", ok("4 kişi için engel yok")) +
        meal("PER", "Zeytinyağlı taze fasulye + yoğurt", "40 dk · kilerdeki yoğurt", ok("4 kişi için engel yok")) +
        meal("CUM", "Patates oturtma + pirinç pilavı", "50 dk · 6 kişi",
             ok("6 kişi için engel yok") + '<span class="chip" style="border-color: #1f5c45; color: #1f5c45">yeni</span>') +
        '<a class="card" href="M33-Liste.dc.html" style="display: flex; justify-content: space-between; align-items: center; text-decoration: none; '
        'color: #1c2420; background: #eef5f0; border-color: #bcd6c6"><span><b style="display: block">Liste güncellendi · 20 kalem</b>'
        f'<span class="mut" style="font-size: 12.5px">6.380 TL · ŞOK + Tarım Kredi</span></span>{icon("chev", 18)}</a>')
    t2 = (f'<div class="toast" role="status">{icon("check", 18, 2.4)}<span>Plan güncellendi · Cuma 6 kişi</span>'
          f'<a href="M29-PlanFarki.dc.html">Geri al</a></div>')
    p2 = phone(b2, tab="Menü", extra=t2)

    # 3 · plan eskidi
    b3 = header("Plan eskidi", back="M05-BuHafta.dc.html", eb="29 Eylül – 3 Ekim")
    b3 += scroll(
        banner("warn", "<b>Ela'nın profili değişti</b> (sürüm 4 · velisi Selin \"süt\" ekledi). Planın 2 yemeği yeniden değerlendirildi.") +
        '<div class="card" style="padding-top: 6px; padding-bottom: 4px">'
        f'<div class="li" style="align-items: flex-start"><span class="eb" style="width: 34px; padding-top: 2px">PER</span><div style="flex-grow: 1">'
        f'<div style="font-weight: 700">Zeytinyağlı taze fasulye + yoğurt</div><div class="mut" style="font-size: 12.5px">Eşleşen içerik: yoğurt (süt)</div>'
        f'<div style="display: flex; gap: 12px; align-items: center; margin-top: 6px">{verdict("no", "Ela için uygun değil")}'
        f'<a class="why" href="M10-Neden.dc.html">Neden?</a></div></div></div>'
        f'<div class="li" style="align-items: flex-start"><span class="eb" style="width: 34px; padding-top: 2px">PZT</span><div style="flex-grow: 1">'
        f'<div style="font-weight: 700">Ispanaklı yumurta</div><div class="mut" style="font-size: 12.5px">Yeniden kontrol · süt içeriği yok</div>'
        f'<div style="margin-top: 6px">{ok("4 kişi için engel yok")}</div></div></div></div>'
        '<div class="card" style="font-size: 13.5px; line-height: 1.45; display: flex; flex-direction: column; gap: 6px">'
        '<b>Diğer 3 yemek değişmedi.</b><span class="mut">Perşembe için yeni plan hazırlanır ve farkı onayına gelir. Onaylayana kadar eski plan '
        'görünür kalır, Perşembe işaretli durur.</span></div>' +
        foot("profil sürüm 3 → 4 · plan pln_43a7 eskidi"))
    p3 = phone(b3 + bar('<a class="btn2" href="M49-ProfilSurum.dc.html" style="flex: 1">Profili gör</a>'
                        '<a class="btn" href="M28-PlanHazirlaniyor.dc.html" style="flex: 1.6">Perşembe için yeni plan</a>'))
    return states_board([("Fark · onay bekliyor", p1), ("Onaylandı · Geri al", p2), ("Plan eskidi · profil değişti", p3)])


# ================================================================ M30 · Yemek detayı
def m30():
    def ing(name, right):
        return f'<div class="li" style="font-size: 14px"><span style="flex-grow: 1">{name}</span>{right}</div>'

    def pantry(t):
        return f'<span class="chip">{icon("fridge", 13, 2)}{t}</span>'

    def base(extra_top="", cooked=False):
        b = header("Zeytinyağlı taze fasulye + yoğurt", back="M18-Menu.dc.html", eb="Perşembe 2 Ekim · akşam")
        head = ('<div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center"><span class="chip">40 dk</span><span class="chip">4 porsiyon</span>'
                + ('<span class="chip" style="border-color: #1f5c45; color: #1f5c45">pişirildi</span>' if cooked else "") + '</div>')
        why = ('<div class="card"><div style="font-size: 13px; font-weight: 700; color: #3d4742; padding-bottom: 4px">Neden bu yemek?</div>'
               + st("Kilerdeki yoğurt SKT'den (29 Eyl) önce kullanılıyor")
               + st("Hafta içi süre sınırı (≤ 45 dk) içinde")
               + st("Hanenin önceki onaylarına göre üst sıralarda")
               + '</div>')
        members = ('<div class="card" style="padding-top: 8px; padding-bottom: 4px"><div style="display: flex; justify-content: space-between; align-items: center">'
                   '<span style="font-size: 13px; font-weight: 700; color: #3d4742">Evdekiler için</span><a class="why" href="M10-Neden.dc.html">Neden?</a></div>'
                   + mem("S", "Selin", "gluten kontrol edildi", ok())
                   + mem("E", "Ela", "fındık, yer fıstığı kontrol edildi", ok())
                   + mem("M", "Murat", "diyabet kuralı kontrol edildi", ok())
                   + mem("C", "Can", "kısıtı yok", ok()) + '</div>')
        ings = ('<div class="card" style="padding-top: 8px; padding-bottom: 4px"><div style="font-size: 13px; font-weight: 700; color: #3d4742">Malzemeler</div>'
                + ing("Taze fasulye 1 kg", price("64,90 TL", "ŞOK", "26 Eyl"))
                + ing("Domates 1 kg", price("34,50 TL", "Tarım Kredi", "27 Eyl"))
                + ing("Yoğurt 1 kg", pantry("kilerden · SKT 29 Eyl"))
                + ing("Soğan, zeytinyağı", pantry("kilerden"))
                + f'<div class="li" style="font-size: 14px"><b style="flex-grow: 1">Porsiyon maliyeti</b>{price("24,85 TL", "ŞOK + Tarım Kredi", "26–27 Eyl")}</div>'
                + '</div>')
        return b + scroll(head + extra_top + why + ings + members)

    acts = ('<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; width: 100%">'
            '<a class="btn2" href="M30-YemekDetay.dc.html">Bu günü değiştir</a>'
            f'<button class="btn2" type="button">{icon("lock", 16, 2)}Kilitle</button>'
            '<button class="btn2" type="button">Çıkar</button>'
            '<button class="btn" type="button">Pişirildi</button></div>')
    p1 = phone(base() + bar(acts))

    def alt(name, sub, delta, chain, date):
        return (f'<div class="li" style="align-items: center"><div style="flex-grow: 1"><b style="display: block; font-size: 14.5px">{name}</b>'
                f'<span class="mut" style="font-size: 12.5px">{sub}</span><div style="margin-top: 4px">{ok("4 kişi için engel yok")}</div></div>'
                f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 6px">{price(delta, chain, date)}'
                f'<a class="sb" href="M28-PlanHazirlaniyor.dc.html">Seç</a></div></div>')
    sheet = ('<div class="scrim"></div><div class="sheet" role="dialog" aria-label="Perşembe için alternatifler"><div class="grab"></div>'
             '<div style="display: flex; justify-content: space-between; align-items: center"><h2 class="disp" style="font-size: 20px">Perşembe için 3 alternatif</h2>'
             f'<a class="ib" href="M30-YemekDetay.dc.html" aria-label="Kapat">{icon("close", 18, 2)}</a></div>'
             '<div class="mut" style="font-size: 13px; line-height: 1.45">Hepsi kesin kısıtlardan geçti. Seçince plan yeniden çözülür (en çok 3 sn) ve farkı onayına gelir.</div>'
             '<div>'
             + alt("Kıymalı ıspanak + yoğurt", "30 dk · kilerdeki yoğurdu kullanır", "+18,00 TL", "ŞOK", "26 Eyl")
             + alt("Nohutlu pirinç pilavı + cacık", "35 dk · kilerdeki yoğurdu kullanır", "−12,00 TL", "Tarım Kredi", "27 Eyl")
             + alt("Fırında sebzeli tavuk", "45 dk · yoğurt kilerde kalır", "+46,00 TL", "ŞOK", "26 Eyl")
             + '</div></div>')
    p2 = phone(base(), extra=sheet)

    cooked = ('<div class="card" style="display: flex; flex-direction: column; gap: 6px; background: #eef5f0; border-color: #bcd6c6">'
              '<b style="font-size: 14px">Kilerden düşüldü</b>'
              '<div style="font-size: 13.5px">Yoğurt 1 kg · soğan 2 adet · zeytinyağı ≈ 100 ml</div>'
              '<a class="why" href="M41-Kiler.dc.html">Kileri aç</a></div>'
              '<div class="card" style="display: flex; flex-direction: column; gap: 8px"><b style="font-size: 14px">Nasıldı?</b>'
              '<div style="display: flex; gap: 8px"><button class="sb2" type="button">Yine yapalım</button><button class="sb2" type="button">Pek sevilmedi</button></div>'
              '<span class="mut" style="font-size: 12px">Yanıtın yalnız sonraki önerilerin sırasını etkiler.</span></div>')
    t3 = (f'<div class="toast" role="status" style="bottom: 24px">{icon("check", 18, 2.4)}<span>Pişirildi · kiler güncellendi</span>'
          f'<a href="M30-YemekDetay.dc.html">Geri al</a></div>')
    p3 = phone(base(cooked, cooked=True), extra=t3)
    return states_board([("İçerik", p1), ("Bu günü değiştir · 3 alternatif", p2), ("Pişirildi · kiler düştü", p3)])


# ================================================================ M31 · Bu plan neden böyle? (mobil)
def m31():
    def nstep(n, title, text, right):
        return (f'<div class="li" style="align-items: flex-start"><span class="capn" style="margin-top: 1px">{n}</span>'
                f'<div style="flex-grow: 1"><b style="display: block; font-size: 14px">{title}</b>'
                f'<div class="mut" style="font-size: 12.5px; line-height: 1.4; margin-top: 2px">{text}</div>'
                f'<div style="margin-top: 6px">{right}</div></div></div>')

    head = header("Bu plan neden böyle?", back="M17-PazarPlani.dc.html", eb="Plan · 29 Eylül – 3 Ekim")
    meta = '<div class="mono">pln_42c1 · kural 2.3 · optimizasyon 0.9 · katalog 0.3</div>'

    steps = ('<div class="card" style="padding-top: 4px; padding-bottom: 4px">'
             + nstep(1, "Kileri okuduk", "12 kalem. Ispanak (28 Eyl) ve yoğurt (29 Eyl) bu hafta bitiyor; \"önce kullan\" kısıtı eklendi.",
                     '<span class="chip">2 kalem kurtarıldı</span>')
             + nstep(2, "Kesin kısıtlarla adayları eledik", "84 tariften 31'i çıktı: 9'u Ela (fındık, yer fıstığı), 22'si Selin (gluten). "
                     "Bu tarifler çözücüye hiç verilmedi.", chip_hard("31 tarif elendi"))
             + nstep(3, "Beğeniyi tahmin ettik", "Onayladığınız ve reddettiğiniz yemekler. Yeni tarifler de ara ara deneniyor.",
                     '<span class="mono">öneri modeli v0.4</span>')
             + nstep(4, "Menü, alışveriş ve market birlikte", "Paket boyutları, ortak malzemeler, en çok 2 market ve bütçe aynı modelde.",
                     gapchip("0,8 sn · en iyisi kanıtlandı (boşluk %0)"))
             + nstep(5, "Sonucu yeniden kontrol ettik", "20 öğün ve 20 alışveriş kalemi kural motorundan tekrar geçti. Açıklamalar bu kayıttan yazıldı.",
                     ok("0 ihlal"))
             + '</div>')
    p1 = phone(head + scroll(meta + steps + '<div class="mut" style="font-size: 12px">Fiyatlar: online katalog · ŞOK 26 Eyl · Tarım Kredi 27 Eyl</div>'))

    costs = ('<div class="card"><div style="font-size: 13px; font-weight: 700; color: #3d4742">Birlikte planlamanın farkı</div>'
             '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-top: 8px">'
             '<div style="padding: 10px; border-radius: 12px; background: #efeadf"><div class="mut" style="font-size: 12px">Önce menü, sonra liste</div>'
             '<div style="font-size: 22px; font-weight: 700">6.310 TL</div><div class="mut" style="font-size: 12px">1 paket ıspanak artar</div></div>'
             '<div style="padding: 10px; border-radius: 12px; background: #eef5f0; color: #17503a"><div style="font-size: 12px">Birlikte</div>'
             '<div style="font-size: 22px; font-weight: 700">5.940 TL</div><div style="font-size: 12px">artan yok · −370 TL</div></div></div></div>'
             '<div class="card"><div style="font-size: 13px; font-weight: 700; color: #3d4742">Evdeki alerjinin bu haftaki maliyeti</div>'
             '<div style="font-size: 26px; font-weight: 700; margin-top: 4px">62 TL</div>'
             '<div style="font-size: 13.5px; line-height: 1.45">Selin\'in glutensiz pizza tabanı ve ekmeği, Ela için pirinç patlağı. Bu bir kısıtın bedeli; '
             'gevşetmiyoruz, yalnız görünür kılıyoruz.</div></div>'
             '<div class="card" style="display: flex; flex-direction: column; gap: 6px"><b>Beğenmediğin bir yemek mi var?</b>'
             '<span class="mut" style="font-size: 13px; line-height: 1.45">Bir günü kilitle, değiştir ya da çıkar; plan kalan kısıtlarla yeniden kurulur ve farkı onayına gelir.</span>'
             '<a class="why" href="M30-YemekDetay.dc.html">Yemeği aç</a></div>')
    p2 = phone(head + scroll(costs + meta) + bar('<a class="btn2" href="M17-PazarPlani.dc.html" style="flex: 1">Plana dön</a>'))

    tl = ('<div class="card" style="padding-top: 4px; padding-bottom: 4px">'
          + nstep(4, "Menü, alışveriş ve market birlikte", "3 sn zaman sınırı doldu. Motor o ana kadar bulduğu en iyi planı tuttu ve en iyiye olan "
                  "uzaklığın üst sınırını hesapladı.", gapchip("En iyiye en fazla %[..] uzak", False))
          + nstep(5, "Sonucu yeniden kontrol ettik", "Kesin kısıtlar bu planda da tam kontrol edildi; boşluk yalnız maliyeti ilgilendirir.", ok("0 ihlal"))
          + '</div>'
          '<div class="card" style="display: flex; flex-direction: column; gap: 8px; font-size: 13.5px; line-height: 1.45">'
          '<b>Daha iyisini aramak ister misin?</b><span class="mut">Arama bir kez daha, daha uzun süreyle çalışır; bulunan plan farkıyla onayına gelir.</span>'
          '<a class="sb" href="M28-PlanHazirlaniyor.dc.html" style="align-self: flex-start">Biraz daha ara</a></div>')
    p3 = phone(header("Bu plan neden böyle?", back="M17-PazarPlani.dc.html", eb="Plan · süre doldu")
               + scroll('<div class="mono">pln_42c2 · kural 2.3 · optimizasyon 0.9</div>' + tl))
    return states_board([("Adımlar · kanıtlı plan", p1), ("Maliyet karşılaştırması", p2), ("Süre dolmuş planın nedeni", p3)])


# ================================================================ M32 · Doğal dille değişiklik
DEMO = "Cuma 6 kişiyiz, biri çölyak. Bütçe 7.000'i geçmesin, Çarşamba balık olmasın."


def m32():
    head = header("Planı değiştir", back="M18-Menu.dc.html", eb="Menü · 29 Eylül – 3 Ekim")

    def rb(chip, note):
        return (f'<div class="li" style="align-items: flex-start; flex-direction: column; gap: 4px">{chip}'
                f'<span class="mut" style="font-size: 12.5px; line-height: 1.4">{note}</span></div>')

    readback = ('<div class="bot" style="max-width: 100%"><div style="font-weight: 700; font-size: 15px; padding-bottom: 4px">Anladığım şu</div>'
                + rb('<span class="chip">Cuma akşamı · +2 kişi</span>', "6 kişi: hane 4 + 2 misafir")
                + rb(chip_hard("Misafir: glutensiz"), "Yalnız Cuma yemeğine bağlı · ad sorulmaz · Cuma'dan sonra silinir")
                + rb('<span class="chip">Bütçe ≤ 7.000 TL · yalnız bu hafta</span>', "Sonraki hafta 6.500 TL'ye döner")
                + rb('<span class="chip">Çarşamba · balık yok</span>', "Şu anki planda Çarşamba zaten balık yok")
                + f'<div class="li" style="gap: 8px; font-size: 13px; font-weight: 700; color: #3d4742">{icon("lock", 16, 2)}Kesin kısıtlar değişmedi</div>'
                + '</div>'
                + banner("info", "\"Biri çölyak\" misafirlerden biri olarak alındı. Selin'i kastettiysen düzelt; onun kısıtı zaten planda."))
    acts = ('<div style="display: flex; gap: 8px"><button class="btn2" type="button" style="flex: 1">Düzelt</button>'
            '<a class="btn" href="M28-PlanHazirlaniyor.dc.html" style="flex: 1.4">Uygula</a></div>')
    p1 = phone(head + scroll(f'<div class="me">{DEMO}</div>' + readback + acts
                             + foot("metni asistan okudu · planı Hane Planlama Motoru kurar")) + inputbar())

    refuse = ('<div class="bot" style="max-width: 100%; display: flex; flex-direction: column; gap: 8px">'
              f'<div style="display: flex; gap: 8px; align-items: flex-start">{icon("lock", 18, 2.2, "#7d2317")}'
              '<b style="font-size: 14.5px; line-height: 1.4">Kesin kısıt yazıyla gevşemez; yalnız velisi Ela\'nın profilinden değiştirebilir.</b></div>'
              f'<div>{chip_hard("Ela: fındık, yer fıstığı")}</div>'
              '<span class="mut" style="font-size: 13px">Bu istek kaydedilmedi; plan değişmedi. Doğum günü için fındıksız tatlı ekleyebilirim.</span>'
              '<div style="display: flex; gap: 14px"><a class="why" href="M49-ProfilSurum.dc.html">Ela\'nın profili</a>'
              '<a class="why" href="M30-YemekDetay.dc.html">Fındıksız tatlı öner</a></div></div>')
    p2 = phone(head + scroll('<div class="me">Ela bu hafta fındık yiyebilir, doğum günü var.</div>' + refuse
                             + foot("sabit yanıt · kısıt gevşetme isteği · S10")) + inputbar())

    def fl(lab, ctl):
        return f'<label class="fl">{lab}{ctl}</label>'
    form = (banner("mute", "Asistan şu an kapalı; değişikliği formla yap. Plan yine Hane Planlama Motoru'nda kurulur.") +
            '<div class="card" style="display: flex; flex-direction: column; gap: 12px">'
            + fl("Gün", '<select class="in"><option>Cuma</option><option>Pazartesi</option><option>Salı</option><option>Çarşamba</option><option>Perşembe</option></select>')
            + '<div style="display: flex; justify-content: space-between; align-items: center"><span style="font-size: 13px; font-weight: 700; color: #3d4742">Kişi sayısı</span>'
            f'<span style="display: flex; align-items: center; gap: 10px"><button class="ib" type="button" aria-label="Bir kişi azalt">{icon("minus", 18, 2)}</button>'
            f'<b style="font-size: 18px">6</b><button class="ib" type="button" aria-label="Bir kişi ekle">{icon("plus", 18, 2)}</button></span></div>'
            + '<div style="display: flex; flex-direction: column; gap: 6px"><span style="font-size: 13px; font-weight: 700; color: #3d4742">Misafirin kesin kısıtı</span>'
            '<label style="display: flex; gap: 8px; align-items: center; min-height: 44px; font-size: 14px"><input type="checkbox" checked="">Gluten (çölyak)</label>'
            '<label style="display: flex; gap: 8px; align-items: center; min-height: 44px; font-size: 14px"><input type="checkbox">Başka bir kısıt seç</label></div>'
            + fl("Bu haftanın bütçe üst sınırı", '<input class="in" type="text" value="7.000 TL">')
            + fl("Kaçınılacak", '<select class="in"><option>Çarşamba · balık</option><option>Seç</option></select>')
            + '</div>')
    p3 = phone(head + scroll(form) + bar('<a class="btn" href="M28-PlanHazirlaniyor.dc.html" style="flex: 1">Uygula</a>'))

    ex = "".join(f'<button class="sb2" type="button">{t}</button>' for t in ["Cuma 2 misafir", "Bütçe 6.000 TL", "Salı balık olmasın"])
    notunder = ('<div class="bot" style="max-width: 100%; display: flex; flex-direction: column; gap: 8px">'
                '<b style="font-size: 14.5px">Bunu bir plan değişikliğine çeviremedim.</b>'
                '<span style="font-size: 13.5px">Plan hafta içi 5 akşamı kapsıyor; hafta sonu planda yok. Hangi günü ve neyi değiştirmek istediğini yazar mısın?</span>'
                f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{ex}</div>'
                '<a class="why" href="M32-DogalDil.dc.html">Formla değiştir</a></div>')
    p4 = phone(head + scroll('<div class="me">Hafta sonu şu işi yapalım, geçen seferki gibi.</div>' + notunder
                             + foot("anlaşılamadı · plan değişmedi")) + inputbar())
    return states_board([("Geri okuma · Anladığım şu", p1), ("Gevşetme reddi", p2), ("Asistan kapalı · form", p3), ("Anlaşılamadı", p4)])


# ================================================================ M33 · Alışveriş listesi
def m33():
    def row(name, qty, src, p, v=None, act=""):
        vv = v or ok("4 kişi: engel yok")
        return (f'<div class="li" style="align-items: flex-start"><div style="flex-grow: 1; min-width: 0"><b style="font-size: 14px">{name}</b> '
                f'<span class="mut" style="font-size: 13px">{qty}</span><div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-top: 4px">'
                f'{srctag(src)}{vv}{act}</div></div>{p}</div>')

    def grp(title, meta, rows, more=""):
        m = f'<button class="sb2" type="button" style="margin: 6px 0 4px">{more}</button>' if more else ""
        return (f'<div class="card" style="padding-top: 8px; padding-bottom: 6px"><div style="display: flex; justify-content: space-between; align-items: baseline">'
                f'<b style="font-size: 14.5px">{title}</b><span class="mut" style="font-size: 12px">{meta}</span></div>{rows}{m}</div>')

    head = header("Alışveriş listesi", back="M18-Menu.dc.html", eb="29 Eylül – 3 Ekim · 20 kalem",
                  right=f'<a class="ib" href="M33-Liste.dc.html" aria-label="Listeyi paylaş">{icon("share", 20)}</a>')
    tools = ('<div style="display: flex; gap: 6px; flex-shrink: 0">'
             f'<button class="sb2" type="button">{icon("plus", 16, 2)}Kalem ekle</button>'
             '<a class="sb2" href="M06-Takas.dc.html">Takaslar</a><a class="sb2" href="M12-Market.dc.html">Marketi böl</a></div>')
    total = ('<div style="display: flex; justify-content: space-between; align-items: baseline; font-size: 13px"><span class="mut">Katalog fiyatıyla</span>'
             '<span><b style="font-size: 17px">6.380 TL</b> <span class="mut">· 3 kalem toplama girmedi</span></span></div>')
    gofret = row("Fındıklı gofret 36 g", "×2", "alışkanlık", price("37,00 TL", "ŞOK", "26 Eyl"),
                 verdict("no", "1 kişi için uygun değil"), '<a class="why" href="M06-Takas.dc.html">Takas</a>')
    sok = grp("ŞOK · 9 kalem", "online katalog · 26 Eyl",
              row("Kıyma", "1 kg", "menü · Cuma", price("459,00 TL", "ŞOK", "26 Eyl"))
              + row("Taze fasulye", "1 kg", "menü · Perşembe", price("64,90 TL", "ŞOK", "26 Eyl"))
              + gofret, "+6 kalem")
    tk = grp("Tarım Kredi · 8 kalem", "online katalog · 27 Eyl",
             row("Glutensiz ekmek", "×2", "menü + alışkanlık", price("139,80 TL", "Tarım Kredi", "27 Eyl"))
             + row("Pirinç", "1 kg", "kiler bitiyor", price("64,50 TL", "Tarım Kredi", "27 Eyl")), "+6 kalem")
    unk = grp("Fiyatı doğrulanamayanlar · 3", "toplama girmedi",
              row("Az tuzlu beyaz peynir", "500 g", "alışkanlık", price("189,90 TL", "ŞOK", "5 Eyl", stale=True))
              + '<div class="mut" style="font-size: 12px; padding: 4px 0">Fiyatı eski ya da iki zincirde de yok. Optimizasyona girmedi; mağazada bak.</div>',
              "+2 kalem")
    sok1 = grp("ŞOK · 9 kalem", "online katalog · 26 Eyl",
               row("Kıyma", "1 kg", "menü · Cuma", price("459,00 TL", "ŞOK", "26 Eyl")) + gofret, "+7 kalem")
    tk1 = grp("Tarım Kredi · 8 kalem", "online katalog · 27 Eyl",
              row("Glutensiz ekmek", "×2", "menü + alışkanlık", price("139,80 TL", "Tarım Kredi", "27 Eyl")), "+7 kalem")
    listbody = scroll(tools + total + sok1 + tk1 + unk)
    go = bar(f'<a class="btn" href="M13-Fis.dc.html" style="flex: 1">{icon("cart", 20)}Markete çıktım</a>')
    p1 = phone(head + listbody + go)

    # 2 · paylaşım önizlemesi
    prev = ('<div style="background: #fff; border: 1px solid #e2dbcb; border-radius: 12px; padding: 12px; font-size: 13.5px; line-height: 1.55">'
            '<b>Alışveriş listesi · 29 Eyl – 3 Eki</b><br><b>ŞOK</b>: kıyma 1 kg, taze fasulye 1 kg, fındıklı gofret ×2, süt 1 L ×3, yoğurt 1 kg, +4<br>'
            '<b>Tarım Kredi</b>: glutensiz ekmek ×2, pirinç 1 kg, patates 2 kg, +5<br><b>Diğer</b>: az tuzlu beyaz peynir 500 g, +2</div>')
    sheet = ('<div class="scrim"></div><div class="sheet" role="dialog" aria-label="Listeyi paylaş"><div class="grab"></div>'
             '<div style="display: flex; justify-content: space-between; align-items: center"><h2 class="disp" style="font-size: 20px">Listeyi paylaş</h2>'
             f'<a class="ib" href="M33-Liste.dc.html" aria-label="Kapat">{icon("close", 18, 2)}</a></div>' + prev
             + banner("info", "Yalnız ürün ve miktar gider. Kimin için olduğu, nedenler ve sağlık bilgisi paylaşılmaz.", "shield")
             + f'<div style="display: flex; justify-content: space-between; align-items: center; min-height: 44px; font-size: 14px"><span>Fiyatları ekle</span>{toggle(False, "Fiyatları ekle")}</div>'
             + '<div style="display: flex; gap: 8px"><button class="btn2" type="button" style="flex: 1">Metni kopyala</button>'
             f'<button class="btn" type="button" style="flex: 1">{icon("share", 18, 2)}Paylaş</button></div></div>')
    p2 = phone(head + listbody, extra=sheet)

    # 3 · fiyatlar eski
    tk_old = grp("Tarım Kredi · 8 kalem", "fiyat eski · 13 Eyl",
                 row("Glutensiz ekmek", "×2", "menü + alışkanlık", price("139,80 TL", "Tarım Kredi", "13 Eyl", stale=True))
                 + row("Pirinç", "1 kg", "kiler bitiyor", price("64,50 TL", "Tarım Kredi", "13 Eyl", stale=True)), "+6 kalem")
    b3 = scroll(banner("warn", "<b>Tarım Kredi fiyatları eski</b> (son çekim 13 Eyl, süre sınırı aşıldı). Bu kalemlerin fiyatı Doğrulanamadı; "
                               "toplama ve market bölmeye girmedi. Ürün sonuçları etkilenmez.")
                + '<div style="display: flex; justify-content: space-between; align-items: baseline; font-size: 13px"><span class="mut">Fiyatı bilinen 9 kalem</span>'
                  '<span><b style="font-size: 17px">[..] TL</b> <span class="mut">· 11 kalem toplama girmedi</span></span></div>'
                + tk_old + sok)
    p3 = phone(head + b3 + go)

    # 4 · son silinenler + çakışma
    conflict = ('<div class="card" style="border-color: #e6d7a9; background: #fbf5e3; display: flex; flex-direction: column; gap: 8px">'
                f'<div style="display: flex; gap: 8px; font-size: 13.5px; line-height: 1.45; color: #5e4d17">{icon("alert", 18, 2)}'
                '<span><b>Çakışma:</b> Murat "Süt 1 L" miktarını 2 yaptı, sen sildin. Geri alınsın mı?</span></div>'
                '<div style="display: flex; gap: 8px"><button class="sb" type="button">Geri al · 2 adet</button><button class="sb2" type="button">Silinmiş kalsın</button></div></div>')

    def gone(name, who, when):
        return (f'<div class="li"><div style="flex-grow: 1"><b style="font-size: 14px">{name}</b><div class="mut" style="font-size: 12px">{who} · {when}</div></div>'
                f'<button class="sb2" type="button">Geri ekle</button></div>')
    del_sheet = ('<div class="sheet" role="dialog" aria-label="Son silinenler" style="box-shadow: 0 -8px 24px rgba(28,36,32,.12)"><div class="grab"></div>'
                 '<div style="display: flex; justify-content: space-between; align-items: baseline"><h2 class="disp" style="font-size: 20px">Son silinenler</h2>'
                 '<span class="mut" style="font-size: 12px">7 gün saklanır</span></div>'
                 '<div>' + gone("Süt 1 L", "sen sildin", "bugün 10:12") + gone("Maden suyu 6'lı", "sen sildin", "bugün 10:11")
                 + gone("Mısır gevreği 400 g", "Murat sildi", "dün 21:40") + '</div></div>')
    p4 = phone(head + scroll(conflict + tools + total + sok), extra=del_sheet)

    # 5 · boş
    empty = ('<div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 12px; padding: 0 28px">'
             f'<span style="color: #56615b">{icon("list", 40, 1.6)}</span>'
             '<h2 class="disp" style="font-size: 22px">Listen henüz boş</h2>'
             '<p class="mut" style="margin: 0; font-size: 14.5px; line-height: 1.5">Plan onaylanınca menüden liste burada kurulur. İstersen kendin de kalem ekleyebilirsin.</p>'
             '<p class="mut" style="margin: 0; font-size: 12.5px">Fiyatlar ŞOK ve Tarım Kredi\'nin online kataloğundan, tarihiyle.</p>'
             '<a class="btn" href="M28-PlanHazirlaniyor.dc.html">Planı hazırla</a>'
             f'<button class="btn2" type="button">{icon("plus", 18, 2)}Kalem ekle</button></div>')
    p5 = phone(header("Alışveriş listesi", back="M18-Menu.dc.html", eb="29 Eylül – 3 Ekim") + empty)

    # 6 · yükleniyor
    sk = "".join(f'<div class="card" style="display: flex; flex-direction: column; gap: 10px">{skel("45%", 16)}'
                 + "".join(f'<div style="display: flex; justify-content: space-between; gap: 12px">{skel("55%")}{skel("22%")}</div>' for _ in range(3))
                 + '</div>' for _ in range(3))
    p6 = phone(header("Alışveriş listesi", back="M18-Menu.dc.html", eb="29 Eylül – 3 Ekim")
               + scroll('<div role="status" class="mut" style="font-size: 13px">Liste ve fiyatlar yükleniyor</div>' + sk))
    return states_board([("İçerik · 3 grup", p1), ("Paylaşım önizlemesi · neden yok", p2), ("Fiyatlar eski", p3),
                         ("Son silinenler · çakışma", p4), ("Boş", p5), ("Yükleniyor", p6)])


# ================================================================ M42 · LLM kapalı
def m42():
    def qa(href, ic, t):
        return (f'<a class="btn2" href="{href}" style="flex-direction: column; min-height: 76px; gap: 4px; font-size: 14px">'
                f'{icon(ic, 22)}{t}</a>')
    head = ('<div style="display: flex; align-items: center; justify-content: space-between; padding: 18px 16px 8px">'
            '<div><div class="eb">ŞOK · alışveriş modu</div><h1 class="disp" style="font-size: 24px; margin-top: 2px">Asistan</h1></div>'
            f'<span class="chip" style="color: #3c4750">{icon("pause", 13, 2.2)}Asistan kapalı</span></div>')
    b1 = scroll(
        banner("mute", "<b>Asistan şu an kapalı; butonlarla devam et.</b> Tarama, liste ve plan kararları asistana bağlı değil, çalışmaya devam ediyor.") +
        '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px">'
        + qa("M34-Tarayici.dc.html", "scan", "Tara") + qa("M33-Liste.dc.html", "plus", "Listeye ekle")
        + qa("M06-Takas.dc.html", "refresh", "Takas öner") + qa("M17-PazarPlani.dc.html", "check", "Planı onayla") + '</div>'
        + sechead("Son tarama")
        + '<div class="card" style="display: flex; flex-direction: column; gap: 6px"><b style="font-size: 14.5px">Fındık Kremalı Gofret 36 g</b>'
        f'<div style="display: flex; gap: 12px; align-items: center">{verdict("no", "Ela için uygun değil")}<a class="why" href="M10-Neden.dc.html">Neden?</a></div>'
        '<span class="mut" style="font-size: 12px">Sonuç karar kaydından · açıklama şablondan</span></div>'
        + foot("asistan kapalı · kararlar kural motorundan"))
    p1 = phone(head + b1 + inputbar("Serbest metin şu an kapalı", disabled=True), tab="Asistan")

    # 2 · tarama normal
    b2 = ('<div style="display: flex; align-items: center; gap: 12px; padding: 16px 16px 8px">'
          f'<a class="ib" href="M05-BuHafta.dc.html" aria-label="Taramayı kapat">{icon("close", 20, 2)}</a>'
          '<span class="eb" style="flex-grow: 1">ŞOK · alışveriş modu</span></div>')
    b2 += scroll(
        banner("mute", "Asistan kapalı. Sonuçlar kural motorundan; açıklamalar sabit şablondan.") +
        '<div class="card" style="display: flex; gap: 12px; align-items: center">'
        '<div style="width: 56px; height: 56px; border-radius: 12px; background: #efe4cf; border: 1px solid #e2d4b6; flex-shrink: 0"></div>'
        '<div style="flex-grow: 1"><b style="display: block; font-size: 15px">Fındık Kremalı Gofret 36 g</b>'
        f'<div style="margin-top: 2px">{price("18,50 TL", "ŞOK", "26 Eyl")}</div></div></div>'
        '<div class="card" style="padding-bottom: 4px"><span style="font-size: 13px; font-weight: 700; color: #3d4742">Evdekiler için</span>'
        + mem("E", "Ela", "fındık ezmesi", verdict("no"))
        + mem("S", "Selin", "buğday unu (gluten)", verdict("no"))
        + mem("M", "Murat", '<span class="cond">Diyabet · şeker eşiği</span>', verdict("warn"))
        + mem("C", "Can", "kısıtı yok", ok()) + '</div>'
        '<div style="display: flex; justify-content: space-between; font-size: 12.5px"><a class="why" href="M10-Neden.dc.html">Neden?</a>'
        '<a href="M38-HataBildir.dc.html" style="font-weight: 700">Hata bildir</a></div>')
    p2 = phone(b2, tab="Tara")

    # 3 · plan onayı normal
    b3 = header("Haftalık planın hazır", back="M05-BuHafta.dc.html", eb="Pazar 27 Eylül")
    b3 += scroll(
        banner("mute", "Asistan kapalı; plan özeti sabit şablonla gösteriliyor.") +
        '<div class="card" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; text-align: center">'
        '<div><div style="font-size: 21px; font-weight: 700">5</div><div class="mut" style="font-size: 12px">akşam yemeği</div></div>'
        '<div><div style="font-size: 21px; font-weight: 700">5.940 TL</div><div class="mut" style="font-size: 12px">bütçe 6.500</div></div>'
        '<div><div style="font-size: 21px; font-weight: 700">2</div><div class="mut" style="font-size: 12px">market</div></div></div>'
        f'<div>{gapchip("Çözüm 0,8 sn · en iyisi kanıtlandı (boşluk %0)")}</div>'
        '<div class="card">' + st("Kesin kısıtlar: 20 öğün kontrol edildi · 0 ihlal") + st("Kilerden 2 kalem kullanıldı")
        + st("ŞOK + Tarım Kredi · online katalog, en eski 3 gün") + '<a class="why" href="M31-PlanNedenMobil.dc.html" style="margin-top: 6px">Bu plan neden böyle?</a></div>'
        + '<div class="mut" style="font-size: 12.5px; text-align: center">Onaylamadan hiçbir şey değişmez.</div>')
    p3 = phone(b3 + bar('<a class="btn2" href="M18-Menu.dc.html" style="flex: 1">Değiştir</a><a class="btn" href="M18-Menu.dc.html" style="flex: 1.4">Onayla</a>'))
    return states_board([("Asistan sekmesi · hızlı eylemler", p1), ("Tarama çalışıyor", p2), ("Plan onayı çalışıyor", p3)])


# ================================================================ M43 · Onay kartı, geri al, iddia denetimi
def m43():
    head = ('<div style="display: flex; align-items: center; justify-content: space-between; padding: 18px 16px 8px">'
            '<div><div class="eb">ŞOK · alışveriş modu</div><h1 class="disp" style="font-size: 24px; margin-top: 2px">Asistan</h1></div></div>')
    item = ('<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px">'
            '<div><b style="display: block; font-size: 15px">Sade pirinç patlağı 100 g</b><span class="mut" style="font-size: 12.5px">1 adet · ŞOK grubuna</span>'
            f'<div style="margin-top: 6px">{ok("4 kişi için engel yok")}</div></div>{price("24,90 TL", "ŞOK", "26 Eyl")}</div>')
    card = ('<div class="bot" style="max-width: 100%; display: flex; flex-direction: column; gap: 10px; border: 1.5px solid #1f5c45">'
            '<b style="font-size: 15px">Sade pirinç patlağını listeye ekleyeyim mi?</b>' + item
            + '<div style="display: flex; gap: 8px"><button class="sb2" type="button" style="flex: 1; justify-content: center">Vazgeç</button>'
              '<button class="sb" type="button" style="flex: 1; justify-content: center">Onayla</button></div>'
            '<span class="mut" style="font-size: 12px">Onaylamadan liste değişmez.</span></div>')
    conv = ('<div class="me">Yerine ne alayım? 25 lirayı geçmesin.</div>'
            '<div class="bot"><div style="padding-bottom: 6px">' + st("Aynı reyonda 6 aday buldum") + st("Dördünüz için tek tek kontrol ettim")
            + '</div>Sade pirinç patlağında dördünüz için de engel bulunmadı.</div>'
            '<div class="me">Onu ekle.</div>')
    p1 = phone(head + scroll(conv + card + foot("karar dec_91e0 · asistan yalnız anlatır")) + inputbar(), tab="Asistan")

    done = ('<div class="bot" style="max-width: 100%; display: flex; flex-direction: column; gap: 8px">'
            f'<div style="display: flex; gap: 8px; align-items: center">{icon("check", 18, 2.4, "#17503a")}<b>Listeye eklendi</b></div>' + item
            + '<a class="why" href="M33-Liste.dc.html">Listeyi aç</a></div>')
    t2 = (f'<div class="toast" role="status" style="bottom: 152px">{icon("clock", 18, 2)}<span>Pirinç patlağı listede · 9 sn</span>'
          f'<a href="M43-OnayKarti.dc.html">Geri al</a></div>')
    p2 = phone(head + scroll(conv + done + foot("list.add onaylandı · 10 sn içinde geri alınabilir")) + inputbar(), tab="Asistan", extra=t2)

    fb = ('<div class="bot" style="max-width: 100%; display: flex; flex-direction: column; gap: 8px">'
          + banner("mute", "Anlatım karar kaydıyla çelişti; şablon açıklama gösteriliyor.", "shield")
          + '<b style="font-size: 15px">Fındık Kremalı Gofret 36 g</b>'
          f'<div>{verdict("no", "Ela için uygun değil")}</div>'
          '<div style="font-size: 13px; line-height: 1.5"><b>Eşleşen içerik:</b> fındık ezmesi<br><b>Kural:</b> ALG-TREENUT · sürüm 2.3<br>'
          '<b>Kaynak:</b> ŞOK web kataloğu içindekiler metni · ekip doğruladı 12 Eyl<br><b>Profil:</b> Ela · sürüm 3</div>'
          '<a class="why" href="M10-Neden.dc.html">Neden?</a></div>')
    p3 = phone(head + scroll('<div class="me">Bunu Ela yiyebilir mi?</div>' + fb
                             + foot("iddia denetimi: anlatım kayıtla uyuşmadı, gösterilmedi · scn_8f3a2c")) + inputbar(), tab="Asistan")
    return states_board([("Onay kartı", p1), ("Onaylandı · 10 sn Geri al", p2), ("İddia denetimi · şablon açıklama", p3)])


# ================================================================ M44 · Sesli mod
def m44():
    head = ('<div style="display: flex; align-items: center; gap: 12px; padding: 16px 16px 8px">'
            f'<a class="ib" href="M16-Asistan.dc.html" aria-label="Sesli modu kapat">{icon("close", 20, 2)}</a>'
            '<span class="eb" style="flex-grow: 1">ŞOK · sesli soru</span></div>')
    prod = ('<div class="chip" style="align-self: center">Tuzlu yer fıstığı 150 g · az önce okuttun</div>')
    bars = "".join(f'<span style="width: 6px; height: {h}px; border-radius: 3px; background: #1f5c45"></span>'
                   for h in [14, 28, 44, 30, 52, 36, 20, 40, 24, 12])
    listen = ('<div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 22px; padding: 0 24px">'
              + prod +
              f'<div style="display: flex; gap: 6px; align-items: center; height: 60px" role="img" aria-label="Ses seviyesi">{bars}</div>'
              '<div class="disp" style="font-size: 24px; text-align: center">Dinliyorum</div>'
              '<div class="mut" style="font-size: 16px; text-align: center">"Bunda fındık var mı, Ela yi…"</div></div>')
    stopbtn = ('<div style="display: flex; justify-content: center; padding-bottom: 36px">'
               '<button type="button" aria-label="Dinlemeyi bitir" style="width: 72px; height: 72px; border-radius: 50%; border: 0; background: #1f5c45; '
               f'color: #fff; display: flex; align-items: center; justify-content: center">{icon("mic", 30, 2)}</button></div>')
    p1 = phone(head + listen + stopbtn)

    conf = scroll(
        '<div class="card" style="display: flex; flex-direction: column; gap: 10px">'
        '<span class="eb">Duyduğum</span>'
        '<div style="font-size: 17px; line-height: 1.45">"Bunda <span style="background: #f7e8c4; border-bottom: 2px dashed #6b4700; padding: 0 2px">fındık</span> var mı, Ela yiyebilir mi?"</div>'
        + banner("warn", "\"Fındık\" kelimesinden emin değilim. Alerjen terimini yazıyla seç.")
        + '<div style="display: flex; flex-wrap: wrap; gap: 8px"><button class="sb" type="button">fındık</button><button class="sb2" type="button">yer fıstığı</button>'
          '<button class="sb2" type="button">Antep fıstığı</button><button class="sb2" type="button">Hiçbiri</button></div></div>'
        '<div class="card" style="display: flex; flex-direction: column; gap: 6px"><span class="eb">Anladığım</span>'
        '<b style="font-size: 17px">Bunu Ela yiyebilir mi?</b>'
        '<span class="mut" style="font-size: 13px; line-height: 1.45">Ela\'nın bütün kısıtlarına bakılır; yalnız söylediğin terime değil.</span></div>')
    p2 = phone(head + conf + bar('<button class="btn2" type="button" style="flex: 1">Yeniden söyle</button><button class="btn" type="button" style="flex: 1.3">Doğru, sor</button>'))

    ans = scroll(
        '<div class="card" style="display: flex; gap: 10px; align-items: flex-start; background: #1c2420; color: #fff; border-color: #1c2420">'
        f'<span style="flex-shrink: 0; margin-top: 2px">{icon("play", 18, 2)}</span><div><div style="font-size: 11.5px; font-weight: 700; letter-spacing: .08em; color: #9fd4b8">SESLİ YANIT</div>'
        '<div style="font-size: 16px; line-height: 1.45; margin-top: 4px">"Bir kişi için uygun değil, ayrıntı ekranda."</div></div></div>'
        '<div class="card" style="display: flex; gap: 12px; align-items: center">'
        '<div style="flex-grow: 1"><b style="display: block; font-size: 15px">Tuzlu yer fıstığı 150 g</b>'
        f'<div style="margin-top: 2px">{price("42,50 TL", "ŞOK", "26 Eyl")}</div></div></div>'
        '<div class="card" style="padding-bottom: 4px"><span style="font-size: 13px; font-weight: 700; color: #3d4742">Evdekiler için · yalnız ekranda</span>'
        + mem("E", "Ela", "yer fıstığı", verdict("no"))
        + mem("S", "Selin", "gluten kontrol edildi", ok())
        + mem("M", "Murat", "diyabet kuralı kontrol edildi", ok())
        + mem("C", "Can", "kısıtı yok", ok()) + '</div>'
        + banner("info", "Ses, üye adını ve kısıtı birlikte söylemez. Ayrıntı yalnız ekranda.", "shield"))
    p3 = phone(head + ans + bar('<button class="btn2" type="button" style="flex: 1">Tekrar dinle</button><a class="btn" href="M10-Neden.dc.html" style="flex: 1">Neden?</a>'))

    def setrow(lab, sub, on):
        return (f'<div class="li" style="align-items: center; min-height: 56px"><div style="flex-grow: 1"><b style="display: block; font-size: 14.5px">{lab}</b>'
                f'<span class="mut" style="font-size: 12.5px; line-height: 1.4">{sub}</span></div>{toggle(on, lab)}</div>')
    sets = scroll(
        '<div class="card" style="padding-top: 4px; padding-bottom: 4px">'
        + setrow("Sesli yanıt", "Soruya sesle de yanıt verir.", True)
        + setrow("Sesli yanıtta ayrıntı: kapalı", "Kapalıyken yalnız sonuç sayısı okunur: \"Bir kişi için uygun değil.\"", False)
        + '</div>'
        '<div class="card" style="font-size: 13.5px; line-height: 1.5; display: flex; flex-direction: column; gap: 6px">'
        '<b>Açarsan ne duyulur?</b><span>Yalnız içerik okunur, ad okunmaz: "Yer fıstığı içeriyor; bir kişi için uygun değil."</span>'
        '<span class="mut">Üye adı ile kısıt hiçbir ayarda birlikte okunmaz.</span></div>'
        '<a class="why" href="M53-Ayarlar.dc.html">Tüm ayarlar</a>')
    p4 = phone(header("Ses", back="M53-Ayarlar.dc.html", eb="Ayarlar") + sets)
    return states_board([("Dinliyor", p1), ("Anladığım · yazılı onay", p2), ("Sesli yanıt · ayrıntı ekranda", p3), ("Ayar notu", p4)])


# ================================================================ M45 · Röntgen modu
XRC = {"m": "#17503a", "l": "#4b3f8a", "f": "#3c4750"}


def xw(kind, text, inner, radius=16):
    return (f'<div style="position: relative; outline: 1.5px dashed {XRC[kind]}; outline-offset: 3px; border-radius: {radius}px; margin-top: 6px">'
            f'{inner}<span style="position: absolute; top: -12px; right: 8px">{xr(kind, text)}</span></div>')


def xbar():
    return ('<div style="display: flex; align-items: center; gap: 8px; background: #1c2420; color: #fff; padding: 8px 8px 8px 16px; font-size: 13px; flex-shrink: 0">'
            f'{icon("eye", 16, 2)}<b style="flex-grow: 1">Röntgen modu açık</b>'
            f'<a href="M53-Ayarlar.dc.html" aria-label="Röntgen modunu kapat" style="width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; color: #fff">{icon("close", 18, 2)}</a></div>')


def m45():
    # 1 · plan (M17 benzeri)
    h1 = header("Haftalık planın hazır", back="M05-BuHafta.dc.html", eb="Pazar 27 Eylül · asistandan")
    b1 = scroll(
        xw("m", "Motor karar verdi · DR pln_42c1",
           '<div class="card" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; text-align: center">'
           '<div><div style="font-size: 21px; font-weight: 700">5</div><div class="mut" style="font-size: 12px">akşam yemeği</div></div>'
           '<div><div style="font-size: 21px; font-weight: 700">5.940 TL</div><div class="mut" style="font-size: 12px">bütçe 6.500</div></div>'
           '<div><div style="font-size: 21px; font-weight: 700">2</div><div class="mut" style="font-size: 12px">market</div></div></div>')
        + xw("m", "Motor · boşluk %0", f'<div style="padding: 2px">{gapchip("Çözüm 0,8 sn · en iyisi kanıtlandı (boşluk %0)")}</div>', 999)
        + xw("m", "Kural motoru · 20 öğün",
             '<div class="card" style="font-size: 13.5px; line-height: 1.45">' + st("Kesin kısıtlar: 20 öğün kontrol edildi · 0 ihlal")
             + st("ŞOK + Tarım Kredi · online katalog, en eski 3 gün") + '</div>')
        + xw("l", "LLM anlattı · iddia denetimi ✓",
             '<div class="card" style="font-size: 13.5px; line-height: 1.5">Bu hafta kilerdeki yoğurdu ve ıspanağı bozulmadan kullanıyoruz. '
             'Cuma pizzasında Selin için glutensiz taban ayrı; iki market tek markete göre 212 TL daha az tutuyor.</div>')
        + xw("f", "Sabit yanıt", '<div class="mut" style="font-size: 12.5px; text-align: center; padding: 6px">Onaylamadan hiçbir şey değişmez.</div>', 10))
    p1 = phone(xbar() + h1 + b1 + bar('<a class="btn2" href="M18-Menu.dc.html" style="flex: 1">Değiştir</a><a class="btn" href="M18-Menu.dc.html" style="flex: 1.4">Onayla</a>'))

    # 2 · asistan (M16 benzeri)
    h2 = ('<div style="display: flex; align-items: center; justify-content: space-between; padding: 14px 16px 6px">'
          '<div><div class="eb">ŞOK · alışveriş modu</div><h1 class="disp" style="font-size: 24px; margin-top: 2px">Asistan</h1></div></div>')
    b2 = scroll(
        '<div class="me">Bunu Ela yiyebilir mi?</div>'
        + xw("m", "Motor karar verdi · DR scn_8f3a2c",
             '<div class="bot" style="max-width: 100%">' + st("Ürünü katalogda buldum · ŞOK web kataloğu, 12 Eyl") + st("Ela'nın profili · sürüm 3")
             + st("Kural motoru çalıştı · 2 eşleşme") + f'<div style="margin-top: 6px">{verdict("no", "Ela için uygun değil")}</div></div>', 18)
        + xw("l", "LLM anlattı · iddia denetimi ✓",
             '<div class="bot" style="max-width: 100%">İçindekilerde <b>fındık ezmesi</b> var. Paket ayrıca "eser miktarda yer fıstığı içerebilir" diyor.</div>', 18)
        + '<div class="me">Şekerim 280, ne yiyeyim?</div>'
        + xw("f", "Sabit yanıt",
             '<div class="bot" style="max-width: 100%">Bunu hekiminle konuşmalısın; doz ya da ilaç önerisi veremem. Ürünün etiket bilgisini gösterebilirim. '
             'Ben bir yapay zekâ asistanıyım, doktor değilim.</div>', 18))
    p2 = phone(xbar() + h2 + b2 + inputbar(), tab="Asistan")

    # 3 · açma ve lejant
    def leg(kind, text, desc):
        return (f'<div class="li" style="flex-direction: column; align-items: flex-start; gap: 4px">{xr(kind, text)}'
                f'<span style="font-size: 13.5px; line-height: 1.45">{desc}</span></div>')
    b3 = scroll(
        '<div class="card" style="padding-top: 4px; padding-bottom: 4px">'
        f'<div class="li" style="border-top: 0; min-height: 56px"><div style="flex-grow: 1"><b style="display: block; font-size: 14.5px">Röntgen modu</b>'
        f'<span class="mut" style="font-size: 12.5px">Ekrandaki her öğenin nereden geldiğini gösterir.</span></div>{toggle(True, "Röntgen modu")}</div></div>'
        + sechead("Rozetler ne demek")
        + '<div class="card" style="padding-top: 4px; padding-bottom: 4px">'
        + leg("m", "Motor karar verdi · DR pln_42c1", "Hüküm, fiyat, bütçe ve plan kural motorundan ya da Hane Planlama Motoru'ndan gelir. Kayıt kimliğiyle izlenir.")
        + leg("l", "LLM anlattı · iddia denetimi ✓", "Metni asistan yazdı; her sayı ve hüküm karar kaydıyla karşılaştırıldı. Çelişirse şablon gösterilir.")
        + leg("f", "Sabit yanıt", "Önceden yazılmış metin; tıbbi sınır, onay ve gizlilik cümleleri. Asistan değiştiremez.")
        + '</div>')
    p3 = phone(header("Yapay zekâ", back="M53-Ayarlar.dc.html", eb="Ayarlar") + b3)
    return states_board([("Plan ekranı (M17) üzerinde", p1), ("Asistan (M16) üzerinde", p2), ("Ayarlardan açma · rozetler", p3)])


# ================================================================ yazım
SCREENS = [
    ("M28-PlanHazirlaniyor", "M28 · Plan hazırlanıyor (canlı adımlar · 4 sonuç) — MUST (v5.2)", m28),
    ("M29-PlanFarki", "M29 · Plan farkı: onay, geri al, plan eskidi — MUST (v5.2)", m29),
    ("M30-YemekDetay", "M30 · Yemek detayı: Neden bu yemek? — SHOULD (v5.2)", m30),
    ("M31-PlanNedenMobil", "M31 · Bu plan neden böyle? (mobil) — SHOULD (v5.2)", m31),
    ("M32-DogalDil", "M32 · Doğal dille değişiklik: Anladığım şu — SHOULD (v5.2)", m32),
    ("M33-Liste", "M33 · Alışveriş listesi: ŞOK / Tarım Kredi / doğrulanamayan — MUST (v5.2)", m33),
    ("M42-LLMKapali", "M42 · Asistan kapalı: butonlarla devam — MUST (v5.2)", m42),
    ("M43-OnayKarti", "M43 · Onay kartı, 10 sn geri al, iddia denetimi — MUST (v5.2)", m43),
    ("M44-Sesli", "M44 · Sesli mod: ad + kısıt birlikte okunmaz — COULD (v5.2)", m44),
    ("M45-Rontgen", "M45 · Röntgen modu: motor · LLM · sabit yanıt — SHOULD (v5.2)", m45),
]

if __name__ == "__main__":
    for stem, title, fn in SCREENS:
        board = fn()
        path = write(stem, title, board, "mobile", group=G)
        errs = check(path)
        print(f"{stem:22s} {board[1]}x{board[2]}  check={errs}")
