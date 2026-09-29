"""Grup: onboarding-ayarlar. M23–M27 (onboarding) ve M49–M53 (ayarlar ve gizlilik), gap_spec.md §C 1–5 ve 27–31.
Çalıştır: python3 gen_onboarding.py  → project/<stem>.dc.html + check() çıktısı.
"""
import os
from lib import *

G = "onboarding-ayarlar"

_lib_banner = banner


def banner(kind, text, ic=None):
    """lib.banner + ikonun daralmasını önler (.bn içinde svg flex-shrink yok)."""
    return (_lib_banner(kind, text, ic).replace(f'<div class="bn bn{kind}">', f'<div class="bn bn{kind}"><span style="display: flex; flex-shrink: 0">', 1)
            .replace('</svg>', '</svg></span>', 1))

# ---------------------------------------------------------------- küçük yardımcılar (yalnız bu grup)


def onb_head(back, label, pct):
    """M02/M03 ile aynı ilerleme başlığı (Adım n / 4)."""
    return (f'<div style="display: flex; align-items: center; gap: 12px; padding: 18px 16px 8px">'
            f'<a class="ib" href="{back}" aria-label="Geri">{icon("back", 20, 2)}</a>'
            f'<div style="flex-grow: 1"><div class="eb">{label}</div>'
            f'<div style="height: 4px; background: #e2dbcb; border-radius: 2px; margin-top: 8px">'
            f'<div style="width: {pct}%; height: 4px; background: #1f5c45; border-radius: 2px"></div></div></div></div>')


def ttl(h, p=None, size=27):
    sub = f'<p class="mut" style="margin: 0; font-size: 14.5px; line-height: 1.45">{p}</p>' if p else ""
    return (f'<div class="pad" style="display: flex; flex-direction: column; gap: 6px; padding-top: 6px">'
            f'<h1 class="disp" style="font-size: {size}px; line-height: 1.12">{h}</h1>{sub}</div>')


def body(inner, gap=10):
    return (f'<div class="pad" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; gap: {gap}px; '
            f'padding-top: 12px; padding-bottom: 8px">{inner}</div>')


def foot(inner):
    return (f'<div class="pad" style="display: flex; flex-direction: column; gap: 8px; padding-top: 8px; padding-bottom: 24px; '
            f'flex-shrink: 0">{inner}</div>')


def note(t, center=True):
    al = "text-align: center; " if center else ""
    return f'<div class="mut" style="{al}font-size: 12px; line-height: 1.4">{t}</div>'


def sect(t):
    return f'<div style="font-size: 13px; font-weight: 700; color: #3d4742; padding-bottom: 2px">{t}</div>'


def bdis(t):
    """Pasif birincil düğme."""
    return (f'<button class="btn" type="button" disabled="" style="background: #cfc6b3; color: #fff; cursor: not-allowed">'
            f'{t}</button>')


def bdanger(t, href="#"):
    return f'<a class="btn" href="{href}" style="background: #8e2b1d">{t}</a>'


def cb(text, checked=False, sub=None, disabled=False):
    c = ' checked=""' if checked else ""
    d = ' disabled=""' if disabled else ""
    s = f'<span class="mut" style="display: block; font-size: 12.5px; margin-top: 2px">{sub}</span>' if sub else ""
    return (f'<label style="display: flex; gap: 10px; align-items: flex-start; padding: 10px 0; min-height: 44px; font-size: 14px; '
            f'line-height: 1.4; cursor: pointer"><input type="checkbox"{c}{d} style="width: 22px; height: 22px; margin: 0; '
            f'accent-color: #1f5c45; flex-shrink: 0"><span>{text}{s}</span></label>')


def seg(legend, name, options, selected=None, err=None, cols=None):
    """Radyo grubu; seçili olan koyu. name her durumda benzersiz olmalı (aynı belgede)."""
    cols = cols or len(options)
    items = []
    for o in options:
        on = o == selected
        st = ("background: #1f5c45; color: #fff; border-color: #1f5c45" if on
              else "background: #fff; color: #1c2420; border-color: #cfc6b3")
        chk = ' checked=""' if on else ""
        items.append(f'<label style="position: relative; display: flex; align-items: center; justify-content: center; min-height: 44px; '
                     f'border: 1.5px solid; border-radius: 12px; font-size: 14px; font-weight: 700; cursor: pointer; {st}">'
                     f'<input type="radio" name="{name}"{chk} style="position: absolute; opacity: 0; width: 1px; height: 1px">{o}</label>')
    e = (f'<span id="{name}-err" style="font-size: 12.5px; color: #7d2317; font-weight: 600">{err}</span>' if err else "")
    return (f'<fieldset style="border: 0; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px"'
            f'{f" aria-describedby=\"{name}-err\"" if err else ""}>'
            f'<legend style="font-size: 13px; font-weight: 700; color: #3d4742; padding: 0 0 6px">{legend}</legend>'
            f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 6px">{"".join(items)}</div>{e}</fieldset>')


def field(label, value="", hint=None, err=None, fid="f", ph=""):
    bd = "border-color: #8e2b1d" if err else ""
    inv = f' aria-invalid="true" aria-describedby="{fid}-err"' if err else ""
    h = f'<span class="mut" style="font-weight: 500; font-size: 12.5px">{hint}</span>' if hint else ""
    e = f'<span id="{fid}-err" style="font-size: 12.5px; color: #7d2317; font-weight: 600">{err}</span>' if err else ""
    return (f'<label class="fl">{label}<input class="in" type="text" value="{value}" placeholder="{ph}"{inv} '
            f'style="{bd}">{h}{e}</label>')


def switch(on, label):
    """Gerçek anahtar: button role=switch, 44 px dokunma alanı; görseli lib.toggle()."""
    return (f'<button type="button" role="switch" aria-checked="{"true" if on else "false"}" aria-label="{label}" '
            f'style="border: 0; background: none; padding: 0; min-width: 44px; min-height: 44px; display: flex; align-items: center; '
            f'justify-content: flex-end; cursor: pointer">{toggle(on, label)}</button>')


def srow(title, desc=None, right="", first=False):
    bt = "" if first else "border-top: 1px solid #ece5d6; "
    d = f'<span class="mut" style="display: block; font-size: 12.5px; line-height: 1.4; margin-top: 2px">{desc}</span>' if desc else ""
    return (f'<div style="display: flex; align-items: center; gap: 10px; padding: 6px 0; min-height: 52px; {bt}">'
            f'<span style="flex-grow: 1; min-width: 0"><b style="display: block; font-size: 14px">{title}</b>{d}</span>{right}</div>')


def lrow(title, href, desc=None, danger=False, first=False, ic=None):
    col = "#7d2317" if danger else "#1c2420"
    bt = "" if first else "border-top: 1px solid #ece5d6; "
    d = f'<span class="mut" style="display: block; font-size: 12.5px; font-weight: 500">{desc}</span>' if desc else ""
    i = f'<span style="color: {col}; display: flex">{icon(ic, 18, 2)}</span>' if ic else ""
    return (f'<a href="{href}" style="display: flex; align-items: center; gap: 10px; min-height: 48px; padding: 6px 0; {bt}'
            f'text-decoration: none; color: {col}">{i}<span style="flex-grow: 1"><b style="display: block; font-size: 14px">{title}</b>{d}</span>'
            f'{icon("chev", 16, 2, "#56615b")}</a>')


def dotrow(t, done=True, active=False):
    if done:
        d = f'<span class="dot">{icon("check", 11, 3)}</span>'
    elif active:
        d = f'<span class="dot" style="background: #f7e8c4; color: #6b4700">{icon("clock", 11, 2.6)}</span>'
    else:
        d = '<span class="dot" style="background: #fffdf8; border: 1.5px solid #cfc6b3"></span>'
    return f'<div class="step">{d}<span>{t}</span></div>'


def sheet(inner, scrim=True):
    s = '<div class="scrim"></div>' if scrim else ""
    return f'{s}<div class="sheet" role="dialog" aria-modal="true"><div class="grab"></div>{inner}</div>'


def faceid(reason, cancel="#"):
    return sheet(
        f'<div style="display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 8px 0 4px; text-align: center">'
        f'<span style="width: 64px; height: 64px; border-radius: 18px; background: #eef5f0; color: #1f5c45; display: flex; '
        f'align-items: center; justify-content: center">{icon("fp", 34, 1.8)}</span>'
        f'<b style="font-size: 17px">Kimliğini doğrula</b>'
        f'<span class="mut" style="font-size: 13.5px; line-height: 1.45">{reason}</span></div>'
        f'<button class="btn" type="button">{icon("fp", 20, 2)}Face ID ile doğrula</button>'
        f'<a class="btn2" href="{cancel}">Vazgeç</a>'
        f'{note("Face ID yoksa cihaz kodun istenir. Oturumun açık olması yetmez.")}')


def member(letter, name, meta, chips="", extra=""):
    return (f'<div class="card" style="display: flex; gap: 12px">{av(letter)}<div style="flex-grow: 1; min-width: 0">'
            f'<div style="font-weight: 700">{name} <span class="mut" style="font-weight: 500">· {meta}</span></div>'
            f'{f"<div style=\"display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px\">{chips}</div>" if chips else ""}'
            f'{extra}</div></div>')


def tag(t, kind="mute"):
    c = {"mute": "background: #e4e7e9; color: #3c4750", "warn": "background: #f7e8c4; color: #6b4700",
         "ok": "background: #dbece2; color: #17503a", "err": "background: #f6ddd6; color: #7d2317"}[kind]
    return f'<span style="display: inline-flex; align-items: center; gap: 4px; font-size: 11.5px; font-weight: 700; border-radius: 6px; padding: 2px 7px; {c}">{t}</span>'


def mono_box(t):
    return (f'<div style="display: flex; align-items: center; gap: 8px; background: #efeadf; border-radius: 10px; padding: 10px 12px">'
            f'{icon("link", 16, 2, "#56615b")}<span class="mono" style="font-size: 12.5px; color: #1c2420; flex-grow: 1">{t}</span></div>')


OUT = []


def emit(stem, title, board, kind="mobile"):
    p = write(stem, title, board, kind, group=G)
    OUT.append((stem, p))


# ================================================================ M23 · Giriş ve hesap
def m23_brand():
    return (f'<div class="pad" style="padding-top: 26px; display: flex; align-items: center; gap: 10px">'
            f'<a class="ib" href="Main.dc.html" aria-label="Geri">{icon("back", 20, 2)}</a>'
            f'<span style="font-family: \'Fraunces\', Georgia, serif; font-weight: 600; font-size: 20px">NutriScan</span></div>')


def m23_screen(state):
    head = m23_brand() + ttl("Hesabınla devam et",
                             "Hane profilleri ve rızalar hesabına bağlı kalır. Sağlık bilgisini burada sormayız.", 29)
    apple = '<a class="btn" href="M02-Hane.dc.html" style="background: #1c2420">Apple ile devam et</a>'
    google = '<a class="btn2" href="M02-Hane.dc.html">Google ile devam et</a>'
    mail = f'<a class="btn2" href="M02-Hane.dc.html">{icon("chat", 18, 2)}E-posta ile devam et</a>'
    sample = (f'<a class="why" href="M05-BuHafta.dc.html" style="justify-content: center; min-height: 44px">'
              f'Hesap açmadan örnek haneyle gez</a>')
    legal = note('Devam edersen <a href="W04-Seffaflik.dc.html">aydınlatma metnini</a> okuyabilirsin; '
                 'onay kutuları ayrı ekranda ve boş gelir.')
    top = ""
    if state == "loading":
        apple = (f'<button class="btn" type="button" aria-busy="true" style="background: #1c2420">{icon("refresh", 18, 2)}'
                 f'Apple ile bağlanılıyor…</button>')
        google = '<button class="btn2" type="button" disabled="" style="opacity: .45">Google ile devam et</button>'
        mail = f'<button class="btn2" type="button" disabled="" style="opacity: .45">{icon("chat", 18, 2)}E-posta ile devam et</button>'
        top = banner("mute", "Apple penceresi açıldı. İşlem bitince buraya dönersin.", "clock")
        sample = '<a class="why" href="M23-Giris.dc.html" style="justify-content: center; min-height: 44px">Vazgeç</a>'
    elif state == "neterr":
        top = (banner("err", "İnternete ulaşamadık. Bağlantını kontrol et ve tekrar dene. Hiçbir bilgi kaydedilmedi.", "wifioff")
               + '<button class="btn2" type="button">' + icon("refresh", 18, 2) + 'Tekrar dene</button>')
    elif state == "cancel":
        top = banner("mute", "Giriş tamamlanmadı: Google penceresi kapatıldı. Hesap açılmadı, hiçbir bilgi kaydedilmedi.", "info")
    inner = (f'{top}<div style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px">{apple}{google}{mail}</div>'
             f'<div style="display: flex; align-items: center; gap: 10px; margin-top: 4px"><span style="flex-grow: 1; height: 1px; '
             f'background: #e2dbcb"></span><span class="mut" style="font-size: 12.5px">ya da</span><span style="flex-grow: 1; '
             f'height: 1px; background: #e2dbcb"></span></div>{sample}')
    return phone(head + body(inner) + foot(legal))


def m23_resume():
    head = m23_brand() + ttl("Kaldığın yerden devam et", "Selin olarak girdin. Kurulumun yarıda kalmış; baştan başlaman gerekmez.", 27)
    card = (f'<div class="card">{sect("Kurulum · 4 adım")}'
            f'{dotrow("Hane · 4 kişi eklendi")}'
            f'{dotrow("İzin · aydınlatma okundu, açık rıza bekliyor", done=False, active=True)}'
            f'{dotrow("İlk liste ve bütçe", done=False)}{dotrow("İlk plan", done=False)}</div>')
    inv = (f'<a class="card" href="M26-Davet.dc.html" style="display: flex; gap: 10px; align-items: center; text-decoration: none; '
           f'color: #1c2420">{av("M")}<span style="flex-grow: 1"><b style="display: block; font-size: 14px">Murat · davet bekliyor</b>'
           f'<span class="mut" style="font-size: 12.5px">Katılana kadar onun için “Engel bulunmadı” göstermeyiz.</span></span>'
           f'{icon("chev", 16, 2, "#56615b")}</a>')
    return phone(head + body(card + inv) + foot(btn("Kaldığın yerden devam et", "M03-Riza.dc.html")
                                                + btn("Haneyi baştan kur", "M02-Hane.dc.html", True)))


emit("M23-Giris", "M23 · Giriş ve hesap — MUST (v5.2)", states_board([
    ("Varsayılan", m23_screen("default")),
    ("Yükleniyor", m23_screen("loading")),
    ("Ağ hatası", m23_screen("neterr")),
    ("İptal edilen giriş", m23_screen("cancel")),
    ("Girişten sonra · yarım kurulum", m23_resume()),
]))

# ================================================================ M24 · Üye ekle
AGES = ["0–3", "4–12", "13–17", "Yetişkin"]


def m24(state):
    head = onb_head("M02-Hane.dc.html", "Adım 1 / 4 · Hane", 25) + ttl("Kişi ekle", "Takma ad yeter. Fotoğraf istemiyoruz; baş harf kullanırız.", 27)
    nm = {"empty": "", "adult": "Murat", "child": "Ela", "err": ""}[state]
    age = {"empty": None, "adult": "Yetişkin", "child": "4–12", "err": "4–12"}[state]
    f1 = field("Takma ad", nm, None if state == "err" else "Evde nasıl sesleniyorsanız.",
               "Takma ad gerekli." if state == "err" else None, fid=f"m24-{state}-nick", ph="ör. Ela")
    f2 = seg("Yaş aralığı", f"m24-{state}-age", AGES, age)
    parts = [f1, f2]
    if state == "err":
        parts.insert(0, banner("err", "Kaydetmeden önce 2 alanı düzelt."))
    if state == "adult":
        parts.append(seg("Rol", "m24-adult-role", ["Üye", "Yönetici"], "Üye"))
        parts.append(
            f'<div class="card" style="border-color: #bcd6c6; background: #eef5f0">'
            f'<b style="display: block; font-size: 14.5px">Murat'"'"'ın bilgisini Murat girer</b>'
            f'<div style="font-size: 13.5px; line-height: 1.45; margin-top: 4px; color: #17503a">Yetişkinin kısıtını ve sağlık durumunu '
            f'başkası giremez. Davet gönderirsin; Murat kendi telefonundan ekler ve kendi iznini verir.</div></div>')
        parts.append(
            f'<div style="display: flex; align-items: center; gap: 10px; padding: 4px 2px; color: #56615b; font-size: 13.5px">'
            f'{icon("lock", 16, 2)}<span style="flex-grow: 1">Onun yerine ben gireyim</span>{tag("Kapalı")}</div>')
    if state in ("child", "err"):
        parts.append(
            f'<div class="card" style="padding-top: 2px; padding-bottom: 2px">'
            f'{cb("Bu çocuğun velisiyim", checked=(state == "child"), sub="Kısıtlarını sen girersin; her değişiklik profil sürümü olarak kaydedilir.")}</div>')
        if state == "err":
            parts.append('<span style="font-size: 12.5px; color: #7d2317; font-weight: 600; margin-top: -4px">'
                         'Veli onayı olmadan çocuk profili açılmaz.</span>')
        else:
            parts.append(note("Rol: üye · veli: Selin. Çocuk profili hesap açmaz, davet almaz.", False))
    if state == "empty":
        f = bdis("Devam")
    elif state == "adult":
        f = btn(f'{icon("share", 18, 2)}Davet gönder', "M26-Davet.dc.html")
    elif state == "child":
        f = btn("Kısıtları seç", "M25-KisitSecici.dc.html")
    else:
        f = '<button class="btn" type="button">Kısıtları seç</button>'
    return phone(head + body("".join(parts), 14) + foot(f))


emit("M24-UyeEkle", "M24 · Üye ekle — MUST (v5.2)", states_board([
    ("Boş", m24("empty")), ("Yetişkin · davet", m24("adult")), ("Çocuk · veli", m24("child")), ("Doğrulama hatası", m24("err")),
]))

# ================================================================ M25 · Kesin kısıt, sağlık durumu, hedef
ALLERGENS = ["Gluten içeren tahıllar", "Kabuklular", "Yumurta", "Balık", "Yer fıstığı", "Soya", "Süt", "Sert kabuklu meyveler",
             "Kereviz", "Hardal", "Susam", "Sülfitler", "Acı bakla (lupin)", "Yumuşakçalar"]


def pill(t, on=False, kind="hard"):
    if on:
        st = {"hard": "border: 1.5px solid #8e2b1d; color: #7d2317; background: #fbeee9",
              "cond": "border: 1.5px solid #2d5a7b; color: #1f4460; background: #e8f0f6",
              "soft": "border: 1.5px dashed #8a7433; color: #5e4d17; background: #fbf5e3"}[kind]
    else:
        st = ("border: 1.5px dashed #cfc6b3; color: #3d4742; background: #fffdf8" if kind == "soft"
              else "border: 1px solid #cfc6b3; color: #3d4742; background: #fffdf8")
    ic = {"hard": "lock", "cond": "pulse", "soft": None}[kind]
    i = icon(ic, 13, 2.2) if (on and ic) else ""
    return (f'<button type="button" aria-pressed="{"true" if on else "false"}" style="display: inline-flex; align-items: center; '
            f'gap: 5px; min-height: 44px; padding: 0 12px; border-radius: 999px; font: inherit; font-size: 13px; font-weight: 600; '
            f'cursor: pointer; {st}">{i}{t}</button>')


def allergen_grid(selected=(), partial=()):
    out = []
    for a in ALLERGENS:
        on = a in selected
        lab = a
        if a in partial:
            lab = f'{a} · {partial[a]}'
            on = True
        out.append(pill(lab, on))
    return f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{"".join(out)}</div>'


def search(ph, val=""):
    return (f'<label style="display: flex; align-items: center; gap: 8px; height: 46px; border: 1.5px solid #cfc6b3; border-radius: 12px; '
            f'padding: 0 12px; background: #fff">{icon("search", 18, 2, "#56615b")}<span style="position: absolute; left: -9999px">{ph}</span>'
            f'<input type="search" value="{val}" placeholder="{ph}" style="border: 0; outline: 0; font: inherit; font-size: 15px; '
            f'flex-grow: 1; background: transparent; color: #1c2420"></label>')


HEALTH_NOTE = (f'<div style="display: flex; gap: 8px; align-items: flex-start; font-size: 12.5px; line-height: 1.4; color: #1f4460">'
               f'<span style="flex-shrink: 0">{icon("info", 16, 2)}</span><span><b>Tıbbi cihaz değildir, teşhis sorulmaz.</b> Kişi kendisi seçer; kaynaklı besin kuralıyla '
               f'yalnız “Dikkat” deriz.</span></div>')


def health_block(sel=None, goals=(), who_self=True):
    h = "".join(pill(t, t == sel, "cond") for t in ["Diyabet", "Hipertansiyon", "Hamilelik"])
    g = "".join(pill(t, t in goals, "soft") for t in ["Şekeri azalt", "Tuzu azalt"])
    return (f'<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
            f'<div style="display: flex; align-items: center; gap: 8px">{sect("Sağlık durumu")}{tag("İsteğe bağlı")}</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{h}</div>{HEALTH_NOTE}</div>'
            f'<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
            f'<div style="display: flex; align-items: center; gap: 8px">{sect("Hedef")}{tag("Zorlamayız")}</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{g}</div>'
            f'<div class="mut" style="font-size: 12.5px; line-height: 1.4">Mümkün olduğunca gözetiriz; kesin kısıt gibi uygulanmaz.</div></div>')


def m25_ela():
    head = onb_head("M24-UyeEkle.dc.html", "Adım 1 / 4 · Ela'nın profili", 25) + ttl(
        "Ela neye kesin olarak dokunmamalı?", "Veli olarak sen giriyorsun. 14 düzenlenmiş alerjen ve diyet tercihleri.", 24)
    clar = (f'<div class="card" style="border-color: #e6d7a9; background: #fbf5e3">'
            f'<b style="display: block; font-size: 14px; color: #5e4d17">“Fıstık” yazdın; hangisi?</b>'
            f'<div style="font-size: 12.5px; color: #5e4d17; margin: 2px 0 8px">Etiketlerde ayrı geçerler; birini seçmezsen kaydetmeyiz.</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{pill("Yer fıstığı", True)}{pill("Antep fıstığı")}{pill("Çam fıstığı")}</div></div>')
    chosen = (f'<div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center">'
              f'<span class="mut" style="font-size: 12.5px; font-weight: 700">Seçilen:</span>{chip_hard("Fındık")}{chip_hard("Yer fıstığı")}</div>')
    lst = (f'{sect("14 alerjen")}{allergen_grid(("Yer fıstığı",), {"Sert kabuklu meyveler": "fındık"})}'
           f'{sect("Diyet tercihleri")}<div class="mut" style="font-size: 12.5px">[sözlükten] · ör. vejetaryen, helal</div>')
    return phone(head + body(search("Alerjen ya da diyet ara", "fıstık") + clar + chosen + lst, 10)
                 + foot(btn("Kaydet · profil sürümü 1", "M02-Hane.dc.html")))


def m25_selin():
    head = onb_head("M02-Hane.dc.html", "Adım 1 / 4 · Senin profilin", 25) + ttl(
        "Senin kesin kısıtların", "Kendi profilini sen yönetirsin.", 24)
    lact = (f'<div class="card" style="border-color: #bcd6c6; background: #eef5f0">'
            f'<b style="display: block; font-size: 14px; color: #17503a">Laktoz, süt alerjisiyle aynı değil</b>'
            f'<div style="font-size: 12.5px; line-height: 1.45; color: #17503a; margin: 2px 0 8px">Süt alerjisi kesin kısıttır; süt '
            f'proteini içeren her ürün “Uygun değil” olur. Laktoz için diyet tercihini seç.</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{pill("Süt (alerji)")}{pill("Laktozsuz (tercih)")}</div></div>')
    chosen = (f'<div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center">'
              f'<span class="mut" style="font-size: 12.5px; font-weight: 700">Seçilen:</span>{chip_hard("Çölyak · gluten")}</div>')
    custom = (f'<div class="card" style="display: flex; flex-direction: column; gap: 8px">{field("Listede yok mu? Özel kısıt yaz", "", None, None, "m25-custom", "ör. kinoa")}'
              f'<div style="display: flex; gap: 8px; align-items: flex-start; font-size: 12.5px; line-height: 1.4; color: #5e4d17">'
              f'<span style="flex-shrink: 0">{icon("alert", 16, 2)}</span><span>Bunu içindekiler listesinde bulamazsam “Engel bulunmadı” demem; en iyi sonuç '
              f'{verdict("warn")} olur.</span></div></div>')
    return phone(head + body(search("Alerjen ya da diyet ara", "laktoz") + lact + chosen + custom, 10)
                 + foot(btn("Kaydet · profil sürümü 1", "M02-Hane.dc.html")))


def m25_murat():
    head = onb_head("M27-DavetKabul.dc.html", "Aydın hanesi · davetle", 60) + ttl(
        "Profilini kur, Murat", "Selin bunu senin yerine giremez. Kesin kısıtın yoksa boş bırak.", 24)
    hard = (f'<div class="card" style="display: flex; flex-direction: column; gap: 8px">{sect("Kesin kısıt")}'
            f'{search("Alerjen ya da diyet ara")}<div class="mut" style="font-size: 12.5px">Seçilmedi · 14 alerjen ve diyet tercihleri</div></div>')
    return phone(head + body(hard + health_block("Diyabet", ("Şekeri azalt",)), 10)
                 + foot(btn("Kaydet ve katılma isteği gönder", "M27-DavetKabul.dc.html")))


def m25_noconsent():
    head = onb_head("M02-Hane.dc.html", "Adım 1 / 4 · Senin profilin", 25) + ttl(
        "Senin kesin kısıtların", "Kendi profilini sen yönetirsin.", 24)
    chosen = (f'<div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center">'
              f'<span class="mut" style="font-size: 12.5px; font-weight: 700">Seçilen:</span>{chip_hard("Çölyak · gluten")}</div>')
    base = head + body(search("Alerjen ya da diyet ara") + chosen + allergen_grid(("Gluten içeren tahıllar",)), 10)
    sh = sheet(
        f'<b style="font-size: 18px; font-family: \'Fraunces\', Georgia, serif">Kaydetmek için izin gerekiyor</b>'
        f'<div style="font-size: 14px; line-height: 1.45">Çölyak bir sağlık bilgisidir. Kaydetmeden önce açık rızanı istiyoruz. '
        f'Aydınlatma metni ayrı, onay kutusu boş gelir.</div>'
        f'{banner("mute", "İzin vermezsen genel modda devam edersin: liste, bütçe ve genel tarama çalışır; kişisel sonuç görünmez.")}'
        f'{btn("İzin ekranına git", "M03-Riza.dc.html")}{btn("Kaydetmeden çık", "M04-Liste.dc.html", True)}')
    return phone(base + foot(bdis("Kaydet")), extra=sh)


emit("M25-KisitSecici", "M25 · Kesin kısıt, sağlık durumu ve hedef seçici — MUST (v5.2)", states_board([
    ("Ela · veli girer · netleştirme", m25_ela()),
    ("Selin · kendi profili · laktoz ve özel kısıt", m25_selin()),
    ("Murat · davetle kendi profili", m25_murat()),
    ("Rıza yok · kaydetmek için izin", m25_noconsent()),
]))

# ================================================================ M26 · Davet gönderildi / bekliyor


def m26(state):
    head = header("Murat'a davet", "M02-Hane.dc.html", eb="Aydın hanesi")
    mrow_meta = {"sent": "davet bekliyor", "expired": "davetin süresi doldu", "req": "katılmak istiyor"}[state]
    unk = (f'<div class="mut" style="font-size: 12.5px; margin-top: 6px; line-height: 1.4">Kısıtı bilinmiyor. Katılana kadar '
           f'onun için “Engel bulunmadı” göstermeyiz; sonucu {verdict("unk")} olur.</div>')
    m = member("M", "Murat", mrow_meta, "", unk if state != "req" else "")
    if state == "sent":
        inner = (m + f'<div class="card" style="display: flex; flex-direction: column; gap: 8px">{sect("Davet bağlantısı")}'
                 f'{mono_box("[davet bağlantısı]")}'
                 f'<div class="mut" style="font-size: 12.5px">Tek kullanımlık · 21 Eylül’de gönderildi · 28 Eylül’e kadar geçerli</div>'
                 f'<div style="display: flex; gap: 8px"><button class="sb" type="button" style="flex: 1; justify-content: center; min-height: 44px">'
                 f'{icon("share", 16, 2)}&#160;WhatsApp ile paylaş</button><button class="sb2" type="button" style="flex: 1; '
                 f'justify-content: center; min-height: 44px">Bağlantıyı kopyala</button></div></div>'
                 f'<div class="card">{sect("Mesajda ne yazıyor")}<div style="font-size: 13.5px; line-height: 1.45; font-style: italic">'
                 f'“Selin seni NutriScan’de Aydın hanesine davet etti. [davet bağlantısı]”</div>'
                 f'<div class="mut" style="font-size: 12px; margin-top: 4px">Mesajda kimsenin kısıtı ya da sağlık bilgisi yok.</div></div>')
        f = (f'<div style="display: flex; gap: 8px"><button class="btn2" type="button" style="flex: 1">{icon("bell", 18, 2)}Hatırlat</button>'
             f'<button class="btn2" type="button" style="flex: 1; color: #7d2317">Daveti iptal et</button></div>')
    elif state == "expired":
        inner = (banner("warn", "Davetin süresi 28 Eylül’de doldu. Bağlantı artık açılmaz; kimse onunla katılamaz.", "clock") + m
                 + note("Tek kullanımlık bağlantılar 7 gün geçerli. Yeni davet eskisini geçersiz kılar.", False))
        f = btn(f'{icon("refresh", 18, 2)}Yeni davet gönder', "M26-Davet.dc.html") + '<button class="btn2" type="button" style="color: #7d2317">Murat’ı haneden çıkar</button>'
    else:
        inner = (m + f'<div class="card" style="border-color: #bcd6c6; background: #eef5f0; display: flex; flex-direction: column; gap: 6px">'
                 f'<b style="font-size: 15px; color: #17503a">Murat katılmak istiyor</b>'
                 f'<div style="font-size: 13.5px; line-height: 1.45; color: #17503a">Bağlantıyı açtı, kendi iznini verdi ve profilini kurdu. '
                 f'Onaylarsan haneye katılır; kısıtlarını ve sağlık durumunu kendisi yönetir.</div></div>'
                 f'<div class="card">{sect("Hanede görünecek olan")}'
                 f'<div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px">{chip_cond("Diyabet")}{chip_soft("Hedef: şekeri azalt")}</div>'
                 f'<div class="mut" style="font-size: 12.5px; margin-top: 6px">Murat bunları paylaşmayı seçti; istediği an “yalnız sonuç” yapabilir.</div></div>'
                 + banner("mute", "Bu kişiyi tanımıyorsan ya da bağlantı başkasına geçtiyse reddet.", "shield"))
        f = btn("Onayla", "M02-Hane.dc.html") + '<button class="btn2" type="button" style="color: #7d2317">Reddet</button>'
    return phone(head + body(inner) + foot(f))


emit("M26-Davet", "M26 · Davet gönderildi / bekliyor — MUST (v5.2)", states_board([
    ("Gönderildi · bekliyor", m26("sent")), ("Süresi doldu", m26("expired")), ("Katılım isteği · kurucu onayı", m26("req")),
]))

# ================================================================ M27 · Davet kabul (Murat'ın telefonu)


def m27(state):
    eb = "Murat'ın telefonu"
    if state == "invite":
        head = header("Davet", None, eb=eb)
        inner = (f'<div style="padding-top: 8px">{av("S")}</div>'
                 f'<h2 class="disp" style="font-size: 26px; line-height: 1.15">Selin seni Aydın hanesine davet etti</h2>'
                 f'<div style="font-size: 14.5px; line-height: 1.5; color: #3d4742">Hane için haftalık yemek ve alışveriş planı kurulur. '
                 f'Senin kısıtlarını ve sağlık durumunu yalnız sen girersin; Selin onları değiştiremez.</div>'
                 f'<div class="card">{dotrow("Hesabını aç ya da gir", False, True)}{dotrow("Aydınlatma metnini oku, iznini ver", False)}'
                 f'{dotrow("Profilini kur", False)}{dotrow("Selin onaylayınca katılırsın", False)}</div>'
                 + note("Bağlantı tek kullanımlık; 28 Eylül’e kadar geçerli.", False))
        f = btn("Devam et", "M23-Giris.dc.html") + '<button class="btn2" type="button">Katılmak istemiyorum</button>'
    elif state == "consent":
        head = header("İzin", "M27-DavetKabul.dc.html", eb=eb)
        inner = (f'<div style="font-size: 14.5px; line-height: 1.45; color: #3d4742">İki ayrı metin var: biri bilgilendirme, biri onay. '
                 f'Selin'"'"'in verdiği izin seni kapsamaz.</div>'
                 f'<div class="card"><div class="eb" style="font-size: 11px">1 · Aydınlatma metni</div>'
                 f'<div style="font-size: 14px; line-height: 1.45; margin-top: 6px">Hangi veriyi, neden, ne kadar süre tuttuğumuzu ve '
                 f'haklarını anlatır. Onay değildir.</div>'
                 f'<a href="W04-Seffaflik.dc.html" style="display: inline-flex; align-items: center; min-height: 44px; font-weight: 700; font-size: 14px">Metni oku</a></div>'
                 f'<div class="card" style="padding-top: 10px; padding-bottom: 4px"><div class="eb" style="font-size: 11px">2 · Açık rıza</div>'
                 f'{cb("Gireceğim sağlık durumu ve hedef bilgisinin hanenin alışveriş ve plan önerileri için işlenmesine onay veriyorum.", sub="Gerekli yalnız sağlık bilgisi girersen. İstediğin an geri alırsın.")}</div>'
                 + banner("info", "Sağlık bilgin kendi hesabında kalır. Selin bu izni göremez, geri alamaz.", "shield"))
        f = bdis("Onayla ve profilimi kur") + btn("Sağlık bilgisi olmadan katıl", "M27-DavetKabul.dc.html", True)
    elif state == "waiting":
        head = header("Katılma isteğin gönderildi", None, eb=eb)
        inner = (member("M", "Murat", "sen", chip_cond("Diyabet") + chip_soft("Hedef: şekeri azalt"),
                        f'<a class="why" href="M25-KisitSecici.dc.html" style="margin-top: 8px; min-height: 44px">Profilimi düzenle</a>')
                 + f'<div class="card">{srow("Hanede yalnız sonuç görünsün", "Açarsan Selin, Ela ve Can diyabet ve hedefini görmez; yalnız “Dikkat” gibi sonuçları görür.", switch(False, "Hanede yalnız sonuç görünsün"), True)}</div>'
                 + banner("mute", "Selin onaylayınca katılırsın. O zamana kadar planda senin için sonuç çıkmaz.", "clock"))
        f = '<button class="btn2" type="button">İsteği geri çek</button>'
    else:
        head = header("Aydın hanesine katıldın", None, eb=eb)
        inner = (banner("info", "Selin isteğini 23 Eylül’de onayladı. Profilin sürüm 1 olarak kaydedildi.", "check")
                 + member("M", "Murat", "sen", chip_cond("Diyabet") + chip_soft("Hedef: şekeri azalt"))
                 + f'<div class="card">{sect("Hanede kim ne görür")}'
                   f'<div class="li" style="border-top: 0">{icon("eye", 18, 2, "#56615b")}<span style="flex-grow: 1">Sonuçların</span>{tag("Görünür", "ok")}</div>'
                   f'<div class="li">{icon("pulse", 18, 2, "#56615b")}<span style="flex-grow: 1">Diyabet ve hedef</span>{tag("Görünür", "ok")}</div>'
                   f'<div class="li">{icon("lock", 18, 2, "#56615b")}<span style="flex-grow: 1">Değiştirme yetkisi</span>{tag("Yalnız sen")}</div>'
                   f'<a class="why" href="M49-ProfilSurum.dc.html" style="min-height: 44px">Profil ve paylaşım ayarları</a></div>')
        f = btn("Bu haftaya git", "M05-BuHafta.dc.html")
    return phone(head + body(inner, 12) + foot(f))


emit("M27-DavetKabul", "M27 · Davet kabul (Murat'ın telefonu) — MUST (v5.2)", states_board([
    ("Davet", m27("invite")), ("Rıza · kutu boş", m27("consent")), ("Bekliyor · kurucu onayı", m27("waiting")),
    ("Kabul edildi", m27("done")),
]))

# ================================================================ M49 · Profil düzenle ve sürüm geçmişi


def removable(t):
    return (f'<span style="display: inline-flex; align-items: center; gap: 2px">{chip_hard(t)}'
            f'<button type="button" aria-label="{t} kısıtını kaldır" style="width: 44px; height: 44px; border: 0; background: none; '
            f'color: #7d2317; display: flex; align-items: center; justify-content: center; cursor: pointer">{icon("close", 16, 2.2)}</button></span>')


def versions(rows):
    out = "".join(
        f'<div style="display: flex; gap: 10px; padding: 8px 0; border-top: 1px solid #ece5d6; font-size: 13px; line-height: 1.4">'
        f'<span class="dr" style="align-self: flex-start">s{v}</span><span style="flex-grow: 1"><b>{d}</b> · {t} '
        f'<span class="mut">· {w}</span></span></div>' for v, d, t, w in rows)
    return (f'<div class="card" style="padding-bottom: 6px">{sect("Sürüm geçmişi")}{out}'
            f'<div class="mut" style="font-size: 11.5px; padding-top: 4px">Eski kararlar hangi sürümle verildiyse onu gösterir.</div></div>')


ELA_V = [(2, "20 Eylül", "“Yer fıstığı” eklendi", "Selin"), (1, "18 Eylül", "Profil açıldı · “Fındık”", "Selin")]


def m49_ela(extra=""):
    head = header("Ela'nın profili", "M15-Hane.dc.html", eb="7 yaş · veli: Selin")
    card = (f'<div class="card" style="display: flex; flex-direction: column; gap: 6px">{sect("Kesin kısıt")}'
            f'<div style="display: flex; flex-wrap: wrap; gap: 4px 6px">{removable("Fındık")}{removable("Yer fıstığı")}</div>'
            f'{btn(icon("plus", 18, 2) + "Kesin kısıt ekle", "M25-KisitSecici.dc.html", True)}'
            f'<div class="mut" style="font-size: 12.5px; line-height: 1.4">Eklemek tek adımdır. Kaldırmak ya da gevşetmek kimlik '
            f'doğrulaması ister; yalnız veli yapabilir.</div></div>'
            f'<div class="card">{srow("Sağlık durumu", "Eklenmedi · isteğe bağlı", f"<a class=\"sb2\" href=\"M25-KisitSecici.dc.html\">Ekle</a>", True)}</div>')
    return head + body(card + versions(ELA_V))


def m49_preview():
    sh = sheet(
        f'<b style="font-size: 18px; font-family: \'Fraunces\', Georgia, serif">Ela’dan “Fındık” kaldırılsın mı?</b>'
        f'<div class="card" style="background: #fbf5e3; border-color: #e6d7a9">{sect("Etki önizlemesi")}'
        f'<div class="step">{icon("refresh", 16, 2)}<span><b>2 plan yemeği</b> yeniden değerlendirilecek.</span></div>'
        f'<div class="step">{icon("refresh", 16, 2)}<span>Liste ve kilerdeki sonuçlar yeni sürümle yeniden hesaplanır.</span></div>'
        f'<div class="step">{icon("doc", 16, 2)}<span>Önceki kararlar sürüm 2 ile kayıtlı kalır.</span></div></div>'
        f'<div style="font-size: 13px; line-height: 1.45; color: #3d4742">Yalnız profil sahibi, çocukta veli kaldırabilir. Asistan, plan '
        f'ya da yazılı istek bunu yapamaz.</div>'
        f'<button class="btn" type="button" style="background: #8e2b1d">{icon("fp", 20, 2)}Kimliğimi doğrula ve kaldır</button>'
        f'<a class="btn2" href="M49-ProfilSurum.dc.html">Vazgeç</a>')
    return phone(m49_ela(), extra=sh)


def m49_done():
    head = header("Ela'nın profili", "M15-Hane.dc.html", eb="7 yaş · veli: Selin")
    card = (f'<div class="card" style="display: flex; flex-direction: column; gap: 6px">{sect("Kesin kısıt")}'
            f'<div style="display: flex; flex-wrap: wrap; gap: 4px 6px">{removable("Yer fıstığı")}</div>'
            f'{btn(icon("plus", 18, 2) + "Kesin kısıt ekle", "M25-KisitSecici.dc.html", True)}</div>'
            + banner("warn", "2 plan yemeği yeniden değerlendiriliyor. Sonuç gelene kadar bu yemekler için “Doğrulanamadı” görünür.", "refresh"))
    v = [(3, "27 Eylül", "“Fındık” kaldırıldı · Face ID", "Selin")] + ELA_V
    toast = (f'<div class="toast" style="bottom: 24px">{icon("check", 18, 2.4)}<span>Fındık kaldırıldı · sürüm 3</span>'
             f'<a href="M49-ProfilSurum.dc.html">Geri al</a></div>')
    return phone(head + body(card + versions(v)), extra=toast)


def m49_other():
    head = header("Murat'ın profili", "M15-Hane.dc.html", eb="Yetişkin · kendi hesabı")
    card = (banner("mute", "Murat kendi profilini yönetir. Sen görebilirsin, değiştiremezsin.", "lock")
            + f'<div class="card" style="display: flex; flex-direction: column; gap: 8px; opacity: .85">{sect("Kesin kısıt")}'
              f'<div>{chip_none("Kısıt yok")}</div>{sect("Sağlık durumu ve hedef")}'
              f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{chip_cond("Diyabet")}{chip_soft("Hedef: şekeri azalt")}</div>'
              f'<button class="btn2" type="button" disabled="" style="opacity: .5; cursor: not-allowed">Düzenle</button></div>'
            + versions([(1, "23 Eylül", "Murat sağlık durumu olarak “diyabet” seçti", "Murat")]))
    return phone(head + body(card))


emit("M49-ProfilSurum", "M49 · Profil düzenle ve sürüm geçmişi — MUST (v5.2)", states_board([
    ("Ela · veli düzenler", phone(m49_ela())),
    ("Kaldır · etki önizlemesi", m49_preview()),
    ("Yeniden kimlik doğrulama", phone(m49_ela(), extra=faceid("Ela’nın kesin kısıtını kaldırmak için. Yalnız veli Selin yapabilir.", "M49-ProfilSurum.dc.html"))),
    ("Kaldırıldı · sürüm 3 · geri al", m49_done()),
    ("Başkasının profili · pasif", m49_other()),
]))

# ================================================================ M50 · Rızalar ve geri alma önizlemesi


def consent_card(title, meta, status, action, kind="ok"):
    return (f'<div class="card" style="display: flex; flex-direction: column; gap: 6px">'
            f'<div style="display: flex; align-items: flex-start; gap: 8px"><b style="flex-grow: 1; font-size: 14.5px">{title}</b>{tag(status, kind)}</div>'
            f'<div class="mut" style="font-size: 12.5px; line-height: 1.4">{meta}</div>{action}</div>')


def m50_list(banner_html=""):
    return phone(m50_inner(banner_html))


def m50_inner(banner_html=""):
    head = header("Rızalar", "M15-Hane.dc.html", eb="Hane ve gizlilik")
    c1 = consent_card("Sağlık bilgisi · hane kararları", "Selin (çölyak), Ela ve Can (veli onayı) · metin sürümü 1.0 · 22 Eylül 2026",
                      "Verildi", '<a class="sb2" href="M50-Rizalar.dc.html" style="align-self: flex-start">Geri al</a>')
    c2 = consent_card("Kimliksiz toplu istatistik", "İsteğe bağlı · metin sürümü 1.0", "Verilmedi",
                      '<button class="sb2" type="button" style="align-self: flex-start">İzin ver</button>', "mute")
    notice = (f'<div class="card">{lrow("Aydınlatma metni", "W04-Seffaflik.dc.html", "Bilgilendirme; onay değildir · sürüm 1.0 · okundu 22 Eylül", first=True, ic="doc")}</div>')
    mur = note("Murat’ın rızası kendi hesabında. Sen göremez ve geri alamazsın.", False)
    return head + body(banner_html + c1 + c2 + notice + mur)


def m50_preview():
    works = "".join(f'<div class="step"><span class="dot">{icon("check", 11, 3)}</span><span>{t}</span></div>'
                    for t in ["Liste ve bütçe", "Genel modda tarama (kişisel sonuç olmadan)", "Kiler"])
    stops = "".join(f'<div class="step"><span class="dot" style="background: #eceae4; color: #3c4750">{icon("minus", 11, 3)}</span><span>{t}</span></div>'
                    for t in ["Kişisel sonuçlar (Selin, Ela, Can)", "Kısıtlı plan", "İçerik değişikliği radarı", "Sağlığın fiyatı"])
    sh = sheet(
        f'<b style="font-size: 18px; font-family: \'Fraunces\', Georgia, serif">Sağlık bilgisi rızasını geri alırsan</b>'
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">'
        f'<div class="card" style="padding: 10px">{sect("Çalışmaya devam eder")}{works}</div>'
        f'<div class="card" style="padding: 10px">{sect("Kapanır")}{stops}</div></div>'
        f'<div style="font-size: 13px; line-height: 1.45; color: #3d4742">Kayıtlı sağlık bilgisi işlenmez; silme süresi: [..]. '
        f'Murat’ın rızası etkilenmez.</div>'
        f'{bdanger("Rızayı geri al", "M50-Rizalar.dc.html")}{btn("Vazgeç", "M50-Rizalar.dc.html", True)}')
    return phone(m50_inner(), extra=sh)


def m50_receipt():
    head = header("Rıza geri alındı", "M15-Hane.dc.html", eb="Makbuz")
    rec = (f'<div class="card" style="display: flex; flex-direction: column; gap: 4px">'
           f'<div class="li" style="border-top: 0"><span class="mut" style="flex-grow: 1">Amaç</span><b>Sağlık bilgisi · hane kararları</b></div>'
           f'<div class="li"><span class="mut" style="flex-grow: 1">Tarih</span><b>27 Eylül 2026 · 14:05</b></div>'
           f'<div class="li"><span class="mut" style="flex-grow: 1">Kim</span><b>Selin</b></div>'
           f'<div class="li"><span class="mut" style="flex-grow: 1">Makbuz no</span><span class="dr">[..]</span></div></div>'
           + banner("mute", "Genel moddasın. Tarama sonuçlarında kişi adı ve kişisel hüküm yok; liste, bütçe ve kiler çalışıyor.", "info")
           + note("Makbuz Rızalar sayfasında kalır.", False))
    return phone(head + body(rec) + foot(btn("Yeniden izin ver", "M03-Riza.dc.html", True) + btn("Bu haftaya git", "M05-BuHafta.dc.html")))


def m50_reconsent():
    b = banner("warn", "Açık rıza metni güncellendi (sürüm 1.1). Değişen bölüm: [..]. Onaylamazsan “Neler değişir” listesi geçerli olur.", "doc")
    head = header("Rızalar", "M15-Hane.dc.html", eb="Hane ve gizlilik")
    c1 = consent_card("Sağlık bilgisi · hane kararları", "Onaylı sürüm 1.0 · yeni sürüm 1.1 bekliyor", "Yeniden onay gerekli",
                      '<div style="display: flex; gap: 8px"><a class="sb" href="M03-Riza.dc.html">Yeni metni oku ve onayla</a>'
                      '<a class="sb2" href="M50-Rizalar.dc.html">Neler değişir</a></div>', "warn")
    notice = f'<div class="card">{lrow("Aydınlatma metni", "W04-Seffaflik.dc.html", "Bilgilendirme; onay değildir · sürüm 1.0", first=True, ic="doc")}</div>'
    return phone(head + body(b + c1 + notice + note("Onay kutusu boş gelir; eski onayın yeni metne taşınmaz.", False)))


emit("M50-Rizalar", "M50 · Rızalar ve geri alma önizlemesi — MUST (v5.2)", states_board([
    ("Amaç bazlı rızalar", m50_list()),
    ("Geri alma önizlemesi", m50_preview()),
    ("Makbuz · genel mod", m50_receipt()),
    ("Metin sürümü değişti · yeniden rıza", m50_reconsent()),
]))

# ================================================================ M51 · Verilerimi indir
INCL = ["Senin profilin, sürümleri ve rızaların", "Velisi olduğun Ela ve Can’ın profilleri", "Planlar, listeler, “aldım” işaretleri, kiler",
        "Tarama geçmişi ve hata bildirimlerin"]


def m51(state):
    head = header("Verilerimi indir", "M15-Hane.dc.html", eb="Hane ve gizlilik")
    if state == "req":
        inc = "".join(f'<div class="step"><span class="dot">{icon("doc", 11, 2.6)}</span><span>{t}</span></div>' for t in INCL)
        inner = (f'<div class="card">{sect("Dosyada neler var")}{inc}</div>'
                 f'<div class="card">{sect("Diğer yetişkinler")}<div style="font-size: 13.5px; line-height: 1.45">Murat dosyanda '
                 f'“hane üyesi 2” olarak görünür; adı, kısıtı ve sağlık bilgisi yer almaz.</div></div>'
                 + banner("info", "İki biçim: makinece okunur JSON ve okunur PDF özeti. Bağlantı yalnız uygulama içinde açılır; e-postayla gönderilmez.", "shield"))
        f = btn("Verilerimi hazırla", "M51-VeriIndir.dc.html")
    elif state == "prep":
        inner = (f'<div class="card">{sect("Hazırlanıyor")}'
                 f'{dotrow("Profil, sürümler ve rızalar")}{dotrow("Planlar, listeler ve kiler")}'
                 f'{dotrow("Diğer yetişkinler maskeleniyor", False, True)}{dotrow("Okunur PDF özeti", False)}</div>'
                 + banner("mute", "Süre: [ölçülecek]. Sayfadan çıkabilirsin; hazır olunca uygulama içinde bildiririz. Bildirimde veri özeti yok.", "clock"))
        f = '<button class="btn2" type="button">Talebi iptal et</button>'
    elif state == "ready":
        files = (f'<div class="card">'
                 f'<div class="li" style="border-top: 0">{icon("doc", 20, 1.8)}<span style="flex-grow: 1"><b style="display: block">Veri dosyası · JSON</b>'
                 f'<span class="mut" style="font-size: 12.5px">[boyut]</span></span></div>'
                 f'<div class="li">{icon("doc", 20, 1.8)}<span style="flex-grow: 1"><b style="display: block">Okunur özet · PDF</b>'
                 f'<span class="mut" style="font-size: 12.5px">Hane: Selin (sen), Ela, Can, hane üyesi 2</span></span></div></div>')
        inner = (banner("info", "Hazır. Bağlantı 24 saat geçerli ve tek kullanımlık: 28 Eylül 14:05’e kadar.", "clock") + files
                 + note("İndirme bu cihazda, uygulama içinde olur. Paylaşmadan önce dosyada sağlık bilgisi olduğunu unutma.", False))
        f = f'<button class="btn" type="button">{icon("fp", 20, 2)}Face ID ile indir</button>'
    else:
        inner = (banner("mute", "Bağlantı 27 Eylül 14:20’de kullanıldı ve kapandı. Yeni bir kopya için yeniden talep et.", "lock")
                 + f'<div class="card">{srow("Son talep", "27 Eylül 2026 · JSON + PDF · kullanıldı", tag("Kapandı"), True)}</div>')
        f = btn("Yeniden talep et", "M51-VeriIndir.dc.html")
    return phone(head + body(inner) + foot(f))


emit("M51-VeriIndir", "M51 · Verilerimi indir — MUST (v5.2)", states_board([
    ("Talep", m51("req")), ("Hazırlanıyor", m51("prep")), ("Hazır · 24 saat · tek kullanım", m51("ready")),
    ("Kullanıldı / süresi doldu", m51("used")),
]))

# ================================================================ M52 · Hesabı sil


def m52_preview():
    return phone(m52_preview_inner() + foot(btn("Devam", "M52-HesapSil.dc.html")))


def m52_preview_inner():
    head = header("Hesabı sil", "M15-Hane.dc.html", eb="Hane ve gizlilik")
    gone = "".join(f'<div class="step"><span class="dot" style="background: #f6ddd6; color: #7d2317">{icon("trash", 11, 2.6)}</span><span>{t}</span></div>'
                   for t in ["Hesabın ve giriş bağlantıların", "Senin profilin, sağlık bilgin ve sürümleri", "Rızaların ve makbuzların",
                             "Senin planların, listelerin, tarama geçmişin"])
    stay = "".join(f'<div class="step"><span class="dot" style="background: #e4e7e9; color: #3c4750">{icon("home", 11, 2.6)}</span><span>{t}</span></div>'
                   for t in ["Aydın hanesi ve Murat’ın hesabı", "Ela ve Can’ın profilleri (hanede kalır)",
                             "Kimliksiz katkılar: doğrulanmış etiket, hata bildirimi; sana bağlanamaz"])
    inner = (f'<div class="card">{sect("Silinecekler")}{gone}</div><div class="card">{sect("Kalanlar")}{stay}</div>'
             f'<div class="card" style="display: flex; flex-direction: column; gap: 6px">{sect("Yöneticiliği devret")}'
             f'<label class="fl" style="font-weight: 600">Yeni yönetici ve çocukların velisi<select class="in"><option>Murat</option></select></label></div>'
             + note("Önce <a href=\"M51-VeriIndir.dc.html\">verilerini indirmek</a> isteyebilirsin.", False))
    return head + body(inner)


def m52_final():
    head = header("Son onay", "M52-HesapSil.dc.html", eb="Hesabı sil")
    inner = (f'<div class="card" style="display: flex; flex-direction: column; gap: 6px">{sect("Silme nasıl gerçek olur")}'
             f'<div style="font-size: 13.5px; line-height: 1.5">Sağlık bilgin sana özel bir anahtarla şifreli. Silme tamamlanınca bu anahtar '
             f'imha edilir; yedeklerde kalan kopyalar da okunamaz olur. Bu adımdan sonra kimse, biz de dahil, o bilgiyi açamaz.</div></div>'
             + banner("warn", "[geri alma penceresi: açık soru] Pencere kapanınca anahtar imha edilir.", "clock")
             + f'<div class="card" style="padding-top: 2px; padding-bottom: 2px">{cb("Silineni ve kalanı okudum; yöneticilik Murat’a geçecek.")}</div>')
    return phone(head + body(inner) + foot(bdanger("Hesabımı sil", "M52-HesapSil.dc.html") + btn("Vazgeç", "M15-Hane.dc.html", True)))


def m52_receipt():
    head = header("Silme talebin alındı", None, eb="Makbuz")
    rec = (f'<div class="card" style="display: flex; flex-direction: column; gap: 4px">'
           f'<div class="li" style="border-top: 0"><span class="mut" style="flex-grow: 1">Talep</span><b>Hesap ve kişisel veri silme</b></div>'
           f'<div class="li"><span class="mut" style="flex-grow: 1">Tarih</span><b>27 Eylül 2026 · 14:12</b></div>'
           f'<div class="li"><span class="mut" style="flex-grow: 1">Anahtar imhası</span><b>[geri alma penceresi sonunda]</b></div>'
           f'<div class="li"><span class="mut" style="flex-grow: 1">Makbuz no</span><span class="dr">[..]</span></div></div>'
           + banner("info", "Murat hanenin yöneticisi oldu; Ela ve Can’ın velisi o. Bu cihazdaki oturum kapatıldı.", "users"))
    return phone(head + body(rec) + foot('<button class="btn2" type="button">' + icon("download", 18, 2) + 'Makbuzu kaydet</button>'
                                         + btn("Karşılamaya dön", "Main.dc.html")))


emit("M52-HesapSil", "M52 · Hesabı sil — MUST (v5.2)", states_board([
    ("Önizleme · silinen ve kalan", m52_preview()),
    ("Yeniden kimlik doğrulama", phone(m52_preview_inner(),
                                       extra=faceid("Hesabını silmek için. Oturumun açık olması yetmez.", "M52-HesapSil.dc.html"))),
    ("Son onay · anahtar imhası", m52_final()),
    ("Makbuz", m52_receipt()),
]))

# ================================================================ M53 · Ayarlar


def card_sec(title, rows):
    return f'<div style="display: flex; flex-direction: column; gap: 6px">{sect(title)}<div class="card" style="padding-top: 4px; padding-bottom: 4px">{rows}</div></div>'


def m53_top():
    head = header("Ayarlar", "M15-Hane.dc.html", eb="Selin")
    notif = card_sec("Bildirimler",
                     srow("Sessiz saat", "22:00–08:00 · bu saatlerde yalnız öncelikli bildirim gelir", switch(True, "Sessiz saat"), True)
                     + srow("Haftalık sınır", "Haftada en çok [..] bildirim", '<button class="sb2" type="button" style="min-height: 44px">Değiştir</button>')
                     + srow("Öncelikli (P0)", "Kesin kısıtla ilgili düzeltmeler · kapatılamaz", tag("Hep açık")))
    notif += note("Bildirimde kişi adı ve kısıt birlikte yazılmaz.", False)
    voice = card_sec("Ses", srow("Sesli yanıtta ayrıntı", "Kapalıyken yalnız sonucu söyler; kişi adı ve nedeni ekranda kalır.",
                                 switch(False, "Sesli yanıtta ayrıntı"), True))
    a11y = card_sec("Erişilebilirlik",
                    srow("Yazı boyutu", "Sistem ayarını izler", '<a class="sb2" href="M56-Erisilebilirlik.dc.html">Önizle</a>', True)
                    + srow("Titreşim", "Tarama sonucu gelince", switch(True, "Titreşim"))
                    + srow("Azaltılmış hareket", "Sistem ayarını izler", switch(True, "Azaltılmış hareket")))
    return phone(head + body(notif + voice + a11y, 12))


def m53_bottom():
    head = header("Ayarlar", "M15-Hane.dc.html", eb="Selin")
    ai = card_sec("Yapay zekâ",
                  srow("İşleme yalnız Türkiye’de", "Asistan ve etiket okuma Türkiye’deki sunucularda çalışır. Sağlık bilgin hiçbir durumda yurt dışına gitmez.",
                       switch(True, "Yapay zekâ işleme yalnız Türkiye"), True)
                  + srow("Röntgen modu", f'Her öğede kararı kim verdi: {xr("m", "Motor")} {xr("l", "LLM")} {xr("f", "Sabit")}',
                         switch(False, "Röntgen modu"))
                  + lrow("Röntgen modunu önizle", "M45-Rontgen.dc.html"))
    mk = card_sec("Marketler",
                  cb("ŞOK", True, "Fiyat var · online katalog") + '<div style="height: 1px; background: #ece5d6"></div>'
                  + cb("Tarım Kredi", True, "Fiyat var · online katalog")
                  + note("Diğer zincirlerde fiyat karşılaştırması yok. Konum sormuyoruz; şube seçilmez.", False))
    about = card_sec("Hakkında",
                     f'<div style="display: flex; flex-direction: column; gap: 8px; padding: 8px 0; font-size: 13.5px; line-height: 1.45">'
                     f'<div style="display: flex; gap: 8px"><span style="flex-shrink: 0">{icon("info", 18, 2, "#1f4460")}</span><span><b>Tıbbi cihaz değildir.</b> Teşhis koymaz; '
                     f'sağlık durumunda yalnız kaynaklı besin kuralıyla “Dikkat” der.</span></div>'
                     f'<div style="display: flex; gap: 8px"><span style="flex-shrink: 0">{icon("store", 18, 2, "#56615b")}</span><span>Fiyatlar ŞOK ve Tarım Kredi’nin herkese açık '
                     f'web kataloğundan, tarihiyle; mağazada farklı olabilir.</span></div>'
                     f'<div style="display: flex; gap: 8px"><span style="flex-shrink: 0">{icon("shield", 18, 2, "#56615b")}</span><span>Veriyi robots kurallarına uyan, kendini tanıtan '
                     f'bir toplayıcıyla, yalnız tariflerimizin gerektirdiği ürünler için alırız; ham veriyi yayımlamayız.</span></div></div>'
                     + lrow("Nasıl karar veriyoruz", "W04-Seffaflik.dc.html")
                     + srow("Uygulama sürümü", None, '<span class="dr">[..]</span>'))
    return phone(head + body(ai + mk + about, 12))


emit("M53-Ayarlar", "M53 · Ayarlar — SHOULD (v5.2)", states_board([
    ("Üst · bildirim, ses, erişilebilirlik", m53_top()),
    ("Alt · yapay zekâ, marketler, hakkında", m53_bottom()),
]))

# ---------------------------------------------------------------- denetim
if __name__ == "__main__":
    import json
    reg = json.load(open(os.path.join(os.path.dirname(ROOT), "registry.json")))
    for stem, p in OUT:
        errs = check(p)
        r = reg[stem]
        print(f"{stem:18s} {r['w']}×{r['h']}  check={errs}")
