"""NutriScan prototip bileşenleri (v5.2). Mevcut artboard'ların görsel dilini birebir izler.
Kullanım: from lib import *; write("M23-Giris", "M23 · Giriş", states_board([...]))
Her fonksiyon iyi biçimli HTML döndürür (bütün etiketler kapalı, özellikler tırnaklı).
"""
import html as _h
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "project")
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600'
         '&amp;family=Instrument+Sans:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap" rel="stylesheet">')

BASE = """body{margin:0;font-family:'Instrument Sans',system-ui,sans-serif;color:#1c2420;background:#f5f1e8}
*{box-sizing:border-box}
a{color:#1f5c45}a:hover{color:#15432f}
.disp{font-family:'Fraunces',Georgia,serif;font-weight:600;letter-spacing:-0.01em;margin:0}
.eb{font-size:11.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#56615b}
.mut{color:#56615b}
.mono{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;color:#56615b}
.src{font-size:11.5px;color:#56615b}
.v{display:inline-flex;align-items:center;gap:5px;height:24px;padding:0 8px;border-radius:7px;font-size:12px;font-weight:700;white-space:nowrap}
.vno{background:#f6ddd6;color:#7d2317}
.vwarn{background:#f7e8c4;color:#6b4700}
.vok{background:#dbece2;color:#17503a}
.vunk{background:#e4e7e9;color:#3c4750}
.av{width:26px;height:26px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;color:#fff;flex-shrink:0}
.chip{display:inline-flex;align-items:center;gap:5px;min-height:26px;padding:0 9px;border-radius:999px;border:1px solid #d6cdb9;background:#fffdf8;font-size:12px;font-weight:600}
.hard{border:1.5px solid #8e2b1d;color:#7d2317;background:#fbeee9}
.cond{border:1.5px solid #2d5a7b;color:#1f4460;background:#e8f0f6}
.soft{border:1.5px dashed #8a7433;color:#5e4d17;background:#fbf5e3}
.none{border:1px solid #d6cdb9;color:#56615b;background:#fffdf8}
.condtag{font-size:11.5px;font-weight:700;color:#1f4460;background:#e8f0f6;border:1px solid #2d5a7b;border-radius:6px;padding:1px 6px}
.bn{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-radius:12px;font-size:13px;line-height:1.45}
.bn svg{flex-shrink:0}
.bninfo{background:#eef5f0;border:1px solid #bcd6c6;color:#17503a}
.bnwarn{background:#fbf5e3;border:1px solid #e6d7a9;color:#5e4d17}
.bnerr{background:#fbeee9;border:1px solid #e0b6aa;color:#7d2317}
.bnmute{background:#eceae4;border:1px solid #d6d2c7;color:#3c4750}
.skel{background:#e9e3d6;border-radius:8px}
.dr{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;color:#56615b;background:#efeadf;border-radius:5px;padding:1px 5px}
.xr{display:inline-flex;align-items:center;gap:4px;font-size:10.5px;font-weight:700;border-radius:5px;padding:1px 6px;border:1.5px solid}
.xrm{color:#17503a;border-color:#17503a;background:#eef5f0}
.xrl{color:#4b3f8a;border-color:#4b3f8a;background:#f0eefa}
.xrf{color:#3c4750;border-color:#3c4750;background:#eceae4}
label.fl{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:700;color:#3d4742}
input.in,select.in{height:46px;border:1.5px solid #cfc6b3;border-radius:12px;padding:0 12px;font:inherit;font-size:15px;background:#fff;color:#1c2420}
.tg{position:relative;width:44px;height:26px;border-radius:13px;background:#cfc6b3;flex-shrink:0;display:inline-block}
.tg::after{content:'';position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff}
.tgon{background:#1f5c45}
.tgon::after{left:21px}
"""

MOBILE = BASE + """.s{width:390px;height:844px;background:#f5f1e8;display:flex;flex-direction:column;overflow:hidden;position:relative;flex-shrink:0}
.pad{padding-left:16px;padding-right:16px}
.card{background:#fffdf8;border:1px solid #e2dbcb;border-radius:16px;padding:12px 14px}
.ib{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;border:1px solid #e2dbcb;background:#fffdf8;color:#1c2420;text-decoration:none;flex-shrink:0}
.why{display:inline-flex;align-items:center;gap:4px;font-size:13px;font-weight:700;color:#1f5c45;text-decoration:none}
.btn{display:flex;align-items:center;justify-content:center;gap:8px;min-height:48px;border-radius:14px;background:#1f5c45;color:#fff;font-weight:700;font-size:15px;text-decoration:none;border:0;font-family:inherit;cursor:pointer;padding:0 16px}
.btn:hover{color:#fff;background:#184a37}
.btn2{display:flex;align-items:center;justify-content:center;gap:8px;min-height:48px;border-radius:14px;background:#fffdf8;color:#1c2420;font-weight:700;font-size:14px;text-decoration:none;border:1.5px solid #cfc6b3;font-family:inherit;cursor:pointer;padding:0 14px}
.btn2:hover{color:#1c2420}
.sb{height:38px;border-radius:10px;font:inherit;font-weight:700;font-size:13.5px;cursor:pointer;padding:0 12px;background:#1f5c45;color:#fff;border:0;text-decoration:none;display:inline-flex;align-items:center}
.sb:hover{color:#fff}
.sb2{height:38px;border-radius:10px;font:inherit;font-weight:700;font-size:13.5px;cursor:pointer;padding:0 12px;background:#fffdf8;color:#1c2420;border:1.5px solid #cfc6b3;text-decoration:none;display:inline-flex;align-items:center}
.mr{display:flex;align-items:center;gap:10px;padding:9px 0;text-decoration:none;color:#1c2420;border-top:1px solid #ece5d6}
.mr:hover{color:#1c2420;background:#faf6ee}
.li{display:flex;align-items:center;gap:10px;padding:9px 0;border-top:1px solid #ece5d6;font-size:14px}
.step{display:flex;gap:8px;align-items:flex-start;font-size:12.5px;line-height:1.4;color:#3d4742;padding:3px 0}
.dot{width:16px;height:16px;border-radius:50%;background:#dbece2;color:#17503a;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.me{align-self:flex-end;max-width:82%;background:#1c2420;color:#fff;border-radius:18px 18px 4px 18px;padding:10px 14px;font-size:14.5px;line-height:1.4}
.bot{align-self:flex-start;max-width:92%;background:#fffdf8;border:1px solid #e2dbcb;border-radius:18px 18px 18px 4px;padding:12px 14px;font-size:14px;line-height:1.45}
.sheet{position:absolute;left:0;right:0;bottom:0;background:#fffdf8;border-radius:22px 22px 0 0;border-top:1px solid #e2dbcb;padding:10px 16px 24px;display:flex;flex-direction:column;gap:10px}
.grab{width:40px;height:5px;border-radius:3px;background:#d6cdb9;align-self:center}
.scrim{position:absolute;inset:0;background:rgba(28,36,32,.38)}
.toast{position:absolute;left:16px;right:16px;bottom:96px;background:#1c2420;color:#fff;border-radius:14px;padding:12px 14px;display:flex;align-items:center;gap:10px;font-size:14px}
.toast a{color:#9fd4b8;font-weight:700;margin-left:auto;text-decoration:none}
.tabs{margin-top:auto;height:80px;border-top:1px solid #e2dbcb;background:#fffdf8;display:flex;justify-content:space-around;align-items:flex-start;padding-top:10px;flex-shrink:0}
.tab{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11px;font-weight:600;color:#56615b;text-decoration:none;width:64px}
.tab:hover{color:#1c2420}
.tabon{color:#1f5c45}
.cap{font-size:13px;font-weight:700;color:#3d4742;height:28px;display:flex;align-items:center;gap:8px}
.capn{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:22px;border-radius:6px;background:#1c2420;color:#fff;font-size:11.5px;padding:0 6px}
"""

WEB = BASE + """.w{width:1440px;height:900px;background:#f5f1e8;display:flex;flex-direction:column;overflow:hidden}
.nav{height:64px;display:flex;align-items:center;gap:28px;padding:0 32px;border-bottom:1px solid #e2dbcb;background:#fffdf8;flex-shrink:0}
.nl{font-size:14px;font-weight:600;color:#56615b;text-decoration:none;height:64px;display:flex;align-items:center;border-bottom:2px solid transparent}
.nl:hover{color:#1c2420}
.nlon{color:#1c2420;border-bottom-color:#1f5c45}
.card{background:#fffdf8;border:1px solid #e2dbcb;border-radius:16px;padding:16px 18px}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:46px;border-radius:12px;background:#1f5c45;color:#fff;font-weight:700;font-size:15px;text-decoration:none;border:0;font-family:inherit;cursor:pointer;padding:0 20px}
.btn:hover{color:#fff}
.btn2{display:inline-flex;align-items:center;justify-content:center;min-height:46px;border-radius:12px;background:transparent;color:#1c2420;font-weight:700;font-size:15px;border:1.5px solid #cfc6b3;font-family:inherit;cursor:pointer;padding:0 18px;text-decoration:none}
.li{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-top:1px solid #ece5d6;font-size:14px;gap:10px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{text-align:left;font-size:12px;color:#56615b;font-weight:700;padding:8px 10px;border-bottom:1px solid #e2dbcb}
td{padding:9px 10px;border-bottom:1px solid #ece5d6;vertical-align:top}
"""

ADMIN = BASE.replace("background:#f5f1e8}", "background:#f3f1ec}", 1) + """.w{width:1440px;height:900px;background:#f3f1ec;display:flex;overflow:hidden}
.side{width:240px;background:#1c2420;color:#d9ded9;display:flex;flex-direction:column;padding:22px 14px;gap:4px;flex-shrink:0}
.sl{display:flex;align-items:center;height:38px;padding:0 12px;border-radius:9px;font-size:14px;font-weight:600;color:#c3cac5;text-decoration:none}
.sl:hover{color:#fff;background:#2a332e}
.slon{background:#2f3a34;color:#fff}
.card{background:#fff;border:1px solid #e0dcd2;border-radius:14px;padding:18px 20px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{text-align:left;font-size:12px;color:#58625c;font-weight:700;padding:8px 10px;border-bottom:1px solid #e0dcd2}
td{padding:9px 10px;border-bottom:1px solid #eeeae2;vertical-align:top}
.cf{display:inline-flex;height:22px;align-items:center;padding:0 7px;border-radius:6px;font-size:11.5px;font-weight:700}
.hi{background:#dbece2;color:#17503a}
.md{background:#f7e8c4;color:#6b4700}
.lo{background:#f6ddd6;color:#7d2317}
.gr{background:#e4e7e9;color:#3c4750}
.b{display:inline-flex;align-items:center;justify-content:center;min-height:40px;border-radius:10px;font-weight:700;font-size:14px;font-family:inherit;cursor:pointer;padding:0 16px;text-decoration:none}
.bok{background:#1f5c45;color:#fff;border:0}
.bok:hover{color:#fff}
.bed{background:#fff;color:#1c2420;border:1.5px solid #cfc9bb}
.bno{background:#fff;color:#7d2317;border:1.5px solid #e0b6aa}
textarea{width:100%;height:60px;border:1.5px solid #cfc9bb;border-radius:10px;padding:10px 12px;font:inherit;font-size:14px;resize:none;color:#1c2420}
"""

# ---------------------------------------------------------------- ikonlar (tek set, çizgi)
_P = {
    "back": '<path d="M15 6l-6 6 6 6"></path>', "close": '<path d="M6 6l12 12M18 6L6 18"></path>',
    "chev": '<path d="M9 6l6 6-6 6"></path>', "down": '<path d="M6 9l6 6 6-6"></path>',
    "scan": '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M7 12h10"></path>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"></rect><path d="M8 11V8a4 4 0 0 1 8 0v3"></path>',
    "pulse": '<path d="M3 12h4l2-4 4 8 2-4h6"></path>', "check": '<path d="M5 12.5l4.5 4.5L19 7.5"></path>',
    "x": '<path d="M7 7l10 10M17 7L7 17"></path>', "alert": '<path d="M12 8v5M12 16.5v.01"></path>',
    "q": '<path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5v.7M12 17v.01"></path>',
    "info": '<circle cx="12" cy="12" r="9"></circle><path d="M12 11v5M12 8v.01"></path>',
    "plus": '<path d="M12 5v14M5 12h14"></path>', "minus": '<path d="M5 12h14"></path>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"></path><path d="M10 20a2 2 0 0 0 4 0"></path>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"></rect><path d="M5 11a7 7 0 0 0 14 0M12 18v3"></path>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"></path><circle cx="12" cy="13" r="3.5"></circle>',
    "cart": '<path d="M3 4h2l2 11h11l2-8H6"></path><circle cx="9" cy="19" r="1.5"></circle><circle cx="17" cy="19" r="1.5"></circle>',
    "gear": '<circle cx="12" cy="12" r="3"></circle><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"></path>',
    "user": '<circle cx="12" cy="8" r="4"></circle><path d="M4 21c1-4 4.5-6 8-6s7 2 8 6"></path>',
    "users": '<circle cx="9" cy="8" r="3.5"></circle><path d="M2.5 20c.8-3.5 3.5-5 6.5-5s5.7 1.5 6.5 5"></path><path d="M16 5a3 3 0 0 1 0 6M18 15c2 .6 3.2 2.2 3.6 5"></path>',
    "doc": '<path d="M6 3h8l4 4v14H6z"></path><path d="M14 3v4h4M9 12h6M9 16h6"></path>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"></path>', "trash": '<path d="M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13"></path>',
    "refresh": '<path d="M20 11a8 8 0 1 0-2.3 5.7M20 5v6h-6"></path>', "wifioff": '<path d="M3 3l18 18M8.5 16.5a5 5 0 0 1 7 0M5 13a10 10 0 0 1 5-2.6M19 13a10 10 0 0 0-3-2M12 20v.01"></path>',
    "clock": '<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path>', "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"></path><circle cx="12" cy="12" r="3"></circle>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"></path>', "list": '<path d="M9 6h11M9 12h11M9 18h11M4 6v.01M4 12v.01M4 18v.01"></path>',
    "fridge": '<rect x="6" y="3" width="12" height="18" rx="2"></rect><path d="M6 10h12M9 6v2M9 13v3"></path>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"></path><path d="M8 10h8M8 13h5"></path>', "home": '<path d="M4 11l8-7 8 7v9H4z"></path>',
    "menu": '<rect x="4" y="5" width="16" height="15" rx="2"></rect><path d="M4 10h16M9 3v4M15 3v4"></path>',
    "key": '<circle cx="8" cy="14" r="4"></circle><path d="M11 11l9-9M16 6l3 3"></path>', "share": '<path d="M12 3v12M7 8l5-5 5 5M5 14v6h14v-6"></path>',
    "undo": '<path d="M9 7L4 12l5 5M4 12h11a5 5 0 0 1 0 10h-2"></path>', "search": '<circle cx="11" cy="11" r="6.5"></circle><path d="M16 16l4 4"></path>',
    "flag": '<path d="M5 21V4h11l-2 4 2 4H5"></path>', "bolt": '<path d="M13 3L5 14h6l-1 7 8-11h-6z"></path>',
    "store": '<path d="M4 9l1.5-5h13L20 9M4 9v11h16V9M4 9h16M10 20v-5h4v5"></path>', "fp": '<path d="M12 11v4M8 12a4 4 0 0 1 8 0c0 3-1 6-2 8M6 14c0-4 2.5-7 6-7s6 3 6 7M9 20c.8-1.5 1.2-3.5 1.2-6"></path>',
    "calendar": '<rect x="4" y="5" width="16" height="15" rx="2"></rect><path d="M4 10h16M9 3v4M15 3v4"></path>',
    "light": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9V16h7v-2.1A6 6 0 0 0 12 3z"></path>',
    "type": '<path d="M5 6V4h14v2M12 4v16M9 20h6"></path>', "globe": '<circle cx="12" cy="12" r="9"></circle><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"></path>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"></path>',
    "pause": '<path d="M9 5v14M15 5v14"></path>', "play": '<path d="M7 5l12 7-12 7z"></path>',
    "qr": '<rect x="4" y="4" width="6" height="6"></rect><rect x="14" y="4" width="6" height="6"></rect><rect x="4" y="14" width="6" height="6"></rect><path d="M14 14h2v2h-2zM18 18h2v2h-2zM14 18h2M18 14h2"></path>',
}


def icon(name, size=20, sw=1.8, color="currentColor"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_P[name]}</svg>')


def esc(t):
    return _h.escape(t, quote=False)


# ---------------------------------------------------------------- ürün kuralları: rozet, çip, fiyat
_V = {"no": ("vno", "x", "Uygun değil"), "warn": ("vwarn", "alert", "Dikkat"), "ok": ("vok", "check", "Engel bulunmadı"),
      "unk": ("vunk", "q", "Doğrulanamadı")}


def verdict(kind, text=None):
    """Dört durumlu hüküm rozeti: ikon + metin + renk (S22). 'Güvenli' yok."""
    c, ic, t = _V[kind]
    return f'<span class="v {c}">{icon(ic, 13, 2.6)}{text or t}</span>'


AVC = {"S": "#1f5c45", "M": "#3d5a80", "C": "#5f5390", "E": "#a24a28", "G": "#7a6a4a"}


def av(letter):
    return f'<span class="av" style="background: {AVC.get(letter, "#56615b")}">{letter}</span>'


def chip_hard(t):
    return f'<span class="chip hard">{icon("lock", 13, 2.2)}{t}</span>'


def chip_cond(t):
    return f'<span class="chip cond">{icon("pulse", 13, 2.2)}{t}</span>'


def chip_soft(t):
    return f'<span class="chip soft">{t}</span>'


def chip_none(t="Kısıt yok"):
    return f'<span class="chip none">{t}</span>'


def price(amount, chain="ŞOK", date="26 Eyl", stale=False):
    """Fiyat her zaman zincir + 'online katalog' + tarih taşır (ADR-015). Eski fiyat Doğrulanamadı."""
    if stale:
        return (f'<span style="display: inline-flex; flex-direction: column; align-items: flex-end"><s class="mut">{amount}</s>'
                f'<span class="src">{chain} · fiyat eski ({date}) · Doğrulanamadı</span></span>')
    return (f'<span style="display: inline-flex; flex-direction: column; align-items: flex-end"><b>{amount}</b>'
            f'<span class="src">{chain} · online katalog · {date}</span></span>')


def banner(kind, text, ic=None):
    ic = ic or {"info": "info", "warn": "alert", "err": "alert", "mute": "info"}[kind]
    return f'<div class="bn bn{kind}">{icon(ic, 18, 2)}<span>{text}</span></div>'


def xr(kind, text):
    """Röntgen modu rozeti: m = motor, l = LLM, f = sabit yanıt."""
    ic = {"m": "bolt", "l": "chat", "f": "shield"}[kind]
    return f'<span class="xr xr{kind}">{icon(ic, 11, 2.4)}{text}</span>'


def toggle(on=False, label=""):
    return f'<span class="tg{" tgon" if on else ""}" role="img" aria-label="{label} {"açık" if on else "kapalı"}"></span>'


# ---------------------------------------------------------------- mobil
TABS = [("M05-BuHafta.dc.html", "home", "Bu hafta"), ("M18-Menu.dc.html", "menu", "Menü"), ("M34-Tarayici.dc.html", "scan", "Tara"),
        ("M19-Mutfak.dc.html", "fridge", "Mutfak"), ("M16-Asistan.dc.html", "chat", "Asistan")]


def tabs(active=None):
    out = ['<nav class="tabs" aria-label="Ana gezinme">']
    for href, ic, label in TABS:
        out.append(f'<a class="tab{" tabon" if label == active else ""}" href="{href}">{icon(ic, 22)}{label}</a>')
    return "".join(out) + "</nav>"


def header(title, back=None, right="", eb=None, close=False):
    b = (f'<a class="ib" href="{back}" aria-label="{"Kapat" if close else "Geri"}">{icon("close" if close else "back", 20, 2)}</a>'
         if back else "")
    e = f'<div class="eb">{eb}</div>' if eb else ""
    return (f'<div style="display: flex; align-items: center; gap: 12px; padding: 16px 16px 8px">{b}'
            f'<div style="flex-grow: 1; min-width: 0">{e}<h1 class="disp" style="font-size: 24px">{title}</h1></div>{right}</div>')


def phone(body, tab=None, extra=""):
    """Tek telefon ekranı (390×844). body: ekran içeriği; tab: aktif sekme adı; extra: sheet/toast gibi üst katman."""
    return f'<div class="s">{body}{tabs(tab) if tab else ""}{extra}</div>'


def btn(t, href="#", secondary=False):
    return f'<a class="{"btn2" if secondary else "btn"}" href="{href}">{t}</a>'


def states_board(states):
    """Aynı ekranın durumları yan yana: [(etiket, phone_html), ...] → (html, w, h)."""
    n = len(states)
    w, h = n * 390 + (n - 1) * 40, 844 + 36
    cols = "".join(
        f'<div style="display: flex; flex-direction: column; gap: 8px; width: 390px">'
        f'<div class="cap"><span class="capn">{i + 1}</span>{lab}</div>{ph}</div>'
        for i, (lab, ph) in enumerate(states))
    return f'<div style="width: {w}px; height: {h}px; display: flex; gap: 40px">{cols}</div>', w, h


# ---------------------------------------------------------------- web ve admin kabukları
WEBNAV = [("W03-Panel.dc.html", "Bu hafta"), ("W01-Studyo.dc.html", "Planlama Stüdyosu"), ("W02-SaglikFiyati.dc.html", "Sağlığın fiyatı"),
          ("W03-Panel.dc.html", "Geçmiş"), ("W07-HaneWeb.dc.html", "Hane"), ("W04-Seffaflik.dc.html", "Nasıl karar veriyoruz")]


def web(content, active=None, right="Aydın hanesi · Selin", nav=True):
    links = "".join(f'<a class="nl{" nlon" if lab == active else ""}" href="{h}">{lab}</a>' for h, lab in WEBNAV)
    n = (f'<nav class="nav" aria-label="Ana gezinme"><span style="font-family: \'Fraunces\', Georgia, serif; font-weight: 600; '
         f'font-size: 20px; margin-right: 12px">NutriScan</span>{links}<span style="margin-left: auto; font-size: 14px; '
         f'font-weight: 600">{right}</span></nav>') if nav else ""
    return f'<div class="w">{n}{content}</div>', 1440, 900


ADMNAV = [("A04-Operasyon.dc.html", "Operasyon"), ("A05-Toplayici.dc.html", "Toplayıcı"), ("A01-KararIzi.dc.html", "Karar izi"),
          ("A02-Katalog.dc.html", "Katalog moderasyonu"), ("A06-Esleme.dc.html", "Eşleme kuyruğu"), ("A08-Kurallar.dc.html", "Kurallar ve sözlük"),
          ("A07-SozlesmePanosu.dc.html", "Sözleşme panosu"), ("A03-Audit.dc.html", "Audit log"), ("A09-KVKK.dc.html", "KVKK talepleri")]


def admin(content, active=None, who="Hilal · Moderatör"):
    links = "".join(f'<a class="sl{" slon" if lab == active else ""}" href="{h}">{lab}</a>' for h, lab in ADMNAV)
    side = (f'<nav class="side" aria-label="Admin gezinme"><div style="font-family: \'Fraunces\', Georgia, serif; font-size: 18px; '
            f'color: #fff; padding: 0 12px 16px">NutriScan <span style="font-family: \'Instrument Sans\', sans-serif; font-size: 12px; '
            f'color: #9aa59f">admin</span></div>{links}<div style="margin-top: auto; font-size: 12.5px; color: #9aa59f; '
            f'padding: 0 12px">{who}</div></nav>')
    return (f'<div class="w">{side}<div style="flex-grow: 1; display: flex; flex-direction: column; padding: 26px 32px; gap: 16px; '
            f'min-width: 0">{content}</div></div>', 1440, 900)


# ---------------------------------------------------------------- dosya yazımı
REGISTRY = {}


def write(stem, title, board, kind="mobile", group=None):
    """board: (html, w, h) ya da phone html (mobil tek ekran). Dosyayı project/<stem>.dc.html'e yazar."""
    if isinstance(board, str):
        board = (board, 390, 844)
    body, w, h = board
    css = {"mobile": MOBILE, "web": WEB, "admin": ADMIN}[kind]
    props = json.dumps({"$preview": {"width": w, "height": h}}).replace("'", "&#39;")
    doc = (f'<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<title>{esc(title)}</title>\n'
           f'<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n{FONTS}\n<style>\n{css}</style>\n</helmet>\n'
           f'{body}\n</x-dc>\n<script type="text/x-dc" data-dc-script data-props=\'{props}\'>\n'
           f'class Component extends DCLogic {{\n  renderVals() {{ return {{}}; }}\n}}\n</script>\n</body>\n</html>\n')
    path = os.path.join(ROOT, f"{stem}.dc.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    REGISTRY[stem] = {"title": title, "w": w, "h": h, "group": group}
    reg = os.path.join(os.path.dirname(ROOT), "registry.json")
    old = json.load(open(reg)) if os.path.exists(reg) else {}
    old[stem] = REGISTRY[stem]
    json.dump(old, open(reg, "w"), ensure_ascii=False, indent=1)
    return path


def check(path):
    """İyi biçim denetimi: void olmayan her etiket kapanmış mı."""
    from html.parser import HTMLParser
    VOID = {"meta", "link", "br", "img", "input", "hr", "source", "area", "col", "wbr"}

    class P(HTMLParser):
        def __init__(s):
            super().__init__(); s.st = []; s.err = []

        def handle_starttag(s, t, a):
            if t not in VOID: s.st.append(t)

        def handle_endtag(s, t):
            if t in VOID: return
            if s.st and s.st[-1] == t: s.st.pop()
            else: s.err.append(f"kapanış {t} beklenen {s.st[-1] if s.st else None}")
    p = P(); p.feed(open(path, encoding="utf-8").read())
    return p.err + ([f"açık kaldı: {p.st}"] if p.st else [])
