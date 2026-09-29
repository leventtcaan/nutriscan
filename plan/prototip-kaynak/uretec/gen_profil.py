"""M57 · Profil (v5.2). Yardımcılar gen_onboarding.py'den kopyalandı (o dosya import edilince tüm grubu yeniden yazar)."""
import sys
sys.path.insert(0, "/private/tmp/claude-501/-Users-leventcanceylan-Documents-Senior-Design-Project/ffa0d232-b07b-48c4-a5e2-68075ec2f3fa/scratchpad/proto")
from lib import *
_lib_banner = banner
def banner(kind, text, ic=None):
    return (_lib_banner(kind, text, ic).replace(f'<div class="bn bn{kind}">', f'<div class="bn bn{kind}"><span style="display: flex; flex-shrink: 0">', 1)
            .replace('</svg>', '</svg></span>', 1))
def switch(on, label):
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
    return (f'<a href="{href}" style="display: flex; align-items: center; gap: 10px; min-height: 46px; padding: 4px 0; {bt}'
            f'text-decoration: none; color: {col}">{i}<span style="flex-grow: 1"><b style="display: block; font-size: 14px">{title}</b>{d}</span>'
            f'{icon("chev", 16, 2, "#56615b")}</a>')
def sheet(inner, scrim=True):
    s = '<div class="scrim"></div>' if scrim else ""
    return f'{s}<div class="sheet" role="dialog" aria-modal="true" aria-labelledby="so-t"><div class="grab"></div>{inner}</div>'
def tag(t, kind="mute"):
    c = {"mute": "background: #e4e7e9; color: #3c4750", "warn": "background: #f7e8c4; color: #6b4700",
         "ok": "background: #dbece2; color: #17503a", "err": "background: #f6ddd6; color: #7d2317"}[kind]
    return f'<span style="display: inline-flex; align-items: center; gap: 4px; font-size: 11.5px; font-weight: 700; border-radius: 6px; padding: 2px 7px; flex-shrink: 0; {c}">{t}</span>'
def sect(t):
    return f'<div style="font-size: 13px; font-weight: 700; color: #3d4742; padding: 2px 0 0">{t}</div>'
def body(inner, gap=8):
    return (f'<div class="pad" style="flex-grow: 1; min-height: 0; overflow-y: auto; display: flex; flex-direction: column; gap: {gap}px; '
            f'padding-top: 4px; padding-bottom: 16px">{inner}</div>')
def big_av(letter, name, meta):
    return (f'<div style="display: flex; align-items: center; gap: 12px; padding: 2px 0">'
            f'<span aria-hidden="true" style="width: 52px; height: 52px; border-radius: 50%; background: {AVC[letter]}; color: #fff; display: flex; '
            f'align-items: center; justify-content: center; font-weight: 700; font-size: 22px; flex-shrink: 0">{letter}</span>'
            f'<div style="min-width: 0"><div style="font-weight: 700; font-size: 17px">{name}</div>'
            f'<div class="mut" style="font-size: 13px; line-height: 1.4">{meta}</div></div></div>')
def links(first_rows=""):
    return ('<div class="card" style="padding-top: 2px; padding-bottom: 2px">'
            + first_rows
            + lrow("Rızalarım", "M50-Rizalar.dc.html", "kişi ve amaç başına · geri alınabilir", first=not first_rows, ic="shield")
            + lrow("Ayarlar", "M53-Ayarlar.dc.html", "bildirim, ses, erişilebilirlik", ic="gear")
            + lrow("Verilerimi indir", "M51-VeriIndir.dc.html", ic="download")
            + lrow("Hesabı sil", "M52-HesapSil.dc.html", danger=True, ic="trash")
            + '</div>')
SIGNOUT = '<a class="btn2" href="M57-Profil.dc.html" style="flex-shrink: 0">Çıkış yap</a>'

def selin(sheet_html=""):
    head = header("Profil", "M05-BuHafta.dc.html", eb="Hesabın")
    acct = ('<div class="card" style="padding-top: 2px; padding-bottom: 2px">'
            + srow("Apple ile giriş", "Parola tutmuyoruz; giriş Apple ya da Google hesabınla.", tag("Bağlı", "ok"), True)
            + srow("Google ile giriş", None, '<button class="sb2" type="button" style="min-height: 44px">Bağla</button>')
            + '</div>')
    mine = ('<div class="card" style="display: flex; flex-direction: column; gap: 6px">'
            '<div class="eb" style="font-size: 11px">Kesin kısıtın</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{chip_hard("Çölyak · gluten")}</div>'
            + lrow("Profil sürümleri", "M49-ProfilSurum.dc.html", "sürüm 2 · 22 Eylül · değişiklik yalnız burada", first=False)
            + '</div>')
    avs = "".join(av(x) for x in "SEMC")
    home = ('<a class="card" href="M15-Hane.dc.html" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: #1c2420">'
            f'<span style="flex-grow: 1; min-width: 0"><b style="display: block; font-size: 14px">Aydın hanesi · yönetici</b>'
            f'<span style="display: flex; gap: 4px; margin-top: 6px">{avs}</span>'
            f'<span class="mut" style="display: block; font-size: 12.5px; margin-top: 4px">Selin, Ela, Murat, Can · üyeleri yönet</span></span>'
            f'{icon("chev", 16, 2, "#56615b")}</a>')
    inner = (big_av("S", "Selin Aydın", "planlayan · Aydın hanesi yöneticisi")
             + acct + mine + home + links() + SIGNOUT)
    return phone(head + body(inner), extra=sheet_html)

def murat():
    head = header("Profil", "M05-BuHafta.dc.html", eb="Hesabın · Murat'ın telefonu")
    acct = ('<div class="card" style="padding-top: 2px; padding-bottom: 2px">'
            + srow("Google ile giriş", "Parola yok.", tag("Bağlı", "ok"), True) + '</div>')
    mine = ('<div class="card" style="display: flex; flex-direction: column; gap: 6px">'
            '<div class="eb" style="font-size: 11px">Kesin kısıt</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{chip_none()}</div>'
            '<div class="eb" style="font-size: 11px; margin-top: 4px">Sağlık durumu ve hedef</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 6px">{chip_cond("Diyabet")}{chip_soft("Hedef: şekeri azalt")}</div>'
            '<div class="mut" style="font-size: 12px; line-height: 1.4">Diyabet kuralı kaynak ve diyetisyen onayı bekliyor; o zamana kadar ürün sonuçların Doğrulanamadı görünür.</div>'
            + srow("Hanede yalnız sonuç görünsün", "Açarsan Selin, Ela ve Can diyabetini ve hedefini görmez; yalnız sonuçları görür.",
                   switch(False, "Hanede yalnız sonuç görünsün"))
            + lrow("Profil sürümleri", "M49-ProfilSurum.dc.html", "sürüm 2 · 23 Eylül · yalnız sen değiştirirsin")
            + '</div>')
    home = ('<a class="card" href="M15-Hane.dc.html" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: #1c2420">'
            '<span style="flex-grow: 1; min-width: 0"><b style="display: block; font-size: 14px">Aydın hanesi · üye</b>'
            '<span class="mut" style="display: block; font-size: 12.5px; margin-top: 2px">Yönetici: Selin · haneyi gör</span></span>'
            f'{icon("chev", 16, 2, "#56615b")}</a>')
    inner = big_av("M", "Murat Aydın", "üye · kendi profilini yönetir") + acct + mine + home + links() + SIGNOUT
    return phone(head + body(inner))

def signout():
    sh = sheet(
        '<h2 id="so-t" class="disp" style="font-size: 21px">Çıkış yapılsın mı?</h2>'
        '<div style="font-size: 14px; line-height: 1.45">Bu cihazdaki oturum kapanır. Hane, liste ve profilin hesabında kalır; '
        'yeniden Apple ile girince geri gelir.</div>'
        + banner("info", "Eşitlenmeyi bekleyen değişiklik yok.", "check")
        + '<button class="btn" type="button">Çıkış yap</button>'
        + '<a class="btn2" href="M57-Profil.dc.html">Vazgeç</a>'
        + '<div class="mut" style="font-size: 12px; line-height: 1.4; text-align: center">Çıkış hesabını silmez. Silmek istersen: '
          '<a href="M52-HesapSil.dc.html" style="font-weight: 700">Hesabı sil</a>.</div>')
    return selin(sh)

p = write("M57-Profil", "M57 · Profil — MUST (v5.2)", states_board([
    ("Selin · kendi profili", selin()),
    ("Murat · kendi profili (üye)", murat()),
    ("Çıkış onayı", signout()),
]), "mobile", group="profil")
print(p, check(p))
