"""Grup web-admin: W06–W09, A05–A10 (1440×900). Çalıştır: python3 gen_web.py"""
from lib import *

G = "web-admin"


# ---------------------------------------------------------------- küçük yardımcılar (yalnız inline stil)
def h1row(title, right=""):
    return (f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 16px">'
            f'<h1 class="disp" style="font-size: 28px">{title}</h1>'
            f'<div class="mut" style="font-size: 13.5px; text-align: right">{right}</div></div>')


def h2(t, right=""):
    r = f'<span class="mut" style="font-size: 12.5px">{right}</span>' if right else ""
    return (f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px">'
            f'<h2 class="disp" style="font-size: 19px">{t}</h2>{r}</div>')


def pill(cls, t):
    """Admin durum etiketi (hüküm değildir)."""
    return f'<span class="cf {cls}">{t}</span>'


def wpill(t, tone="gr"):
    """Web durum etiketi (web CSS'inde .cf yok)."""
    c = {"gr": ("#e4e7e9", "#3c4750"), "md": ("#f7e8c4", "#6b4700"), "lo": ("#f6ddd6", "#7d2317"),
         "hi": ("#dbece2", "#17503a"), "dk": ("#1c2420", "#fff")}[tone]
    return (f'<span style="display: inline-flex; align-items: center; height: 22px; padding: 0 8px; border-radius: 6px; '
            f'font-size: 11.5px; font-weight: 700; background: {c[0]}; color: {c[1]}; white-space: nowrap">{t}</span>')


def ph(t="[..]"):
    return f'<span class="dr">{t}</span>'


def kv(k, v, top=True):
    bt = "border-top: 1px solid #eeeae2; " if top else ""
    return (f'<div style="{bt}display: flex; justify-content: space-between; gap: 14px; padding: 7px 0; font-size: 13.5px">'
            f'<span class="mut" style="flex-shrink: 0">{k}</span><span style="text-align: right">{v}</span></div>')


def small(t, extra=""):
    return f'<div class="mut" style="font-size: 12.5px; line-height: 1.45; {extra}">{t}</div>'


def ab(t, kind="bed", extra=""):
    return f'<button class="b {kind}" type="button" style="{extra}">{t}</button>'


def cb(label, checked=False, disabled=False, idp="c", note=""):
    ch = " checked" if checked else ""
    dis = " disabled" if disabled else ""
    n = f'<span class="mut" style="font-size: 12px; font-weight: 400; display: block">{note}</span>' if note else ""
    return (f'<label style="display: flex; gap: 10px; align-items: flex-start; min-height: 30px; font-size: 14px; font-weight: 600; '
            f'cursor: pointer"><input type="checkbox"{ch}{dis} style="width: 18px; height: 18px; margin: 2px 0 0; accent-color: #1f5c45; '
            f'flex-shrink: 0"><span>{label}{n}</span></label>')


def rb(name, label, checked=False, note=""):
    ch = " checked" if checked else ""
    n = f'<span class="mut" style="font-size: 12px; font-weight: 400; display: block">{note}</span>' if note else ""
    return (f'<label style="display: flex; gap: 10px; align-items: flex-start; min-height: 30px; font-size: 14px; font-weight: 600; '
            f'cursor: pointer"><input type="radio" name="{name}"{ch} style="width: 18px; height: 18px; margin: 2px 0 0; '
            f'accent-color: #1f5c45; flex-shrink: 0"><span>{label}{n}</span></label>')


def tgbtn(on, label):
    return (f'<button type="button" aria-pressed="{"true" if on else "false"}" aria-label="{label}" '
            f'style="background: none; border: 0; padding: 9px 0; cursor: pointer; display: inline-flex">{toggle(on, label)}</button>')


def bar(pct_px, total=120, target=None, color="#1f5c45", empty=False):
    """Küçük yatay çubuk (örnek görünüm). pct_px: dolu genişlik (px), target: hedef çizgisi (px)."""
    fill = "" if empty else f'<span style="position: absolute; left: 0; top: 0; bottom: 0; width: {pct_px}px; background: {color}; border-radius: 4px"></span>'
    tg = (f'<span style="position: absolute; left: {target}px; top: -3px; bottom: -3px; width: 2px; background: #1c2420"></span>'
          if target is not None else "")
    return (f'<span style="position: relative; display: inline-block; width: {total}px; height: 8px; border-radius: 4px; '
            f'background: #e9e4d8">{fill}{tg}</span>')


TD = 'style="padding: 10px 8px"'
NW = "white-space: nowrap; padding: 0 10px; font-size: 13.5px"


# ================================================================ A05 · Toplayıcı sağlığı
def chain_row(name, adapter, status, cekim, kapsama, yas, ttl, uyum, broken=False):
    return (f'<tr><td {TD}><div style="font-size: 16px; font-weight: 700">{name}</div>'
            f'<div class="mut" style="font-size: 12px">{adapter}</div></td>'
            f'<td {TD}>{status}</td><td {TD}>{cekim}</td><td {TD}>{kapsama}</td><td {TD}>{yas}</td><td {TD}>{ttl}</td>'
            f'<td {TD}>{uyum}</td>'
            f'<td {TD}><div style="display: flex; flex-direction: column; gap: 6px; align-items: stretch">'
            f'{ab("Şimdi çek", "bed", NW)}{ab("Zinciri durdur", "bno", NW)}</div></td></tr>')


def lines(*xs):
    return "".join(f'<div style="font-size: 13px; line-height: 1.5">{x}</div>' for x in xs)


def coverage_chart():
    """Kapsama zaman grafiği: iki seri, hedef çizgisi. Değerler örnek görünüm, ölçüm değil."""
    days = ["21", "22", "23", "24", "25", "26", "27", "28"]
    sok = [132, 137, 139, 141, 142, 143, 143, 144]
    tk = [106, 113, 118, 123, 127, 129, 131, 0]
    x0, y0 = 46, 160
    out = [f'<svg width="560" height="194" viewBox="0 0 560 194" role="img" aria-label="Fiyatlı SKU kapsaması, 21–28 Eylül, '
           f'ŞOK ve Tarım Kredi; örnek görünüm, değerler ölçülecek">',
           '<g font-family="Instrument Sans, sans-serif" font-size="11" fill="#56615b">',
           f'<line x1="{x0}" y1="{y0}" x2="550" y2="{y0}" stroke="#cfc9bb"></line>',
           f'<line x1="{x0}" y1="{y0 - 135}" x2="550" y2="{y0 - 135}" stroke="#1c2420" stroke-dasharray="5 4"></line>',
           f'<text x="4" y="{y0 - 131}" fill="#1c2420" font-weight="700">hedef</text>',
           f'<text x="4" y="{y0 - 119}" fill="#1c2420" font-weight="700">%90</text>',
           f'<text x="4" y="{y0 + 4}">%0</text>']
    for i, d in enumerate(days):
        bx = x0 + 10 + i * 62
        out.append(f'<rect x="{bx}" y="{y0 - sok[i]}" width="20" height="{sok[i]}" rx="3" fill="#1f5c45"></rect>')
        if tk[i]:
            out.append(f'<rect x="{bx + 24}" y="{y0 - tk[i]}" width="20" height="{tk[i]}" rx="3" fill="#3d5a80"></rect>')
        else:
            out.append(f'<rect x="{bx + 24}" y="{y0 - 130}" width="20" height="130" rx="3" fill="none" stroke="#7d2317" '
                       f'stroke-width="1.5" stroke-dasharray="4 3"></rect>'
                       f'<text x="{bx + 34}" y="{y0 + 30}" text-anchor="end" fill="#7d2317" font-weight="700">TK çekim yok</text>')
        out.append(f'<text x="{bx + 22}" y="{y0 + 16}" text-anchor="middle">{d} Eyl</text>')
    out.append('</g></svg>')
    return "".join(out)


def legend():
    sw = lambda c, t, dash=False: (f'<span style="display: inline-flex; align-items: center; gap: 6px; font-size: 12.5px">'
                                   f'<span style="width: 12px; height: 12px; border-radius: 3px; '
                                   f'{"border: 1.5px dashed #7d2317" if dash else "background: " + c}"></span>{t}</span>')
    return (f'<div style="display: flex; gap: 16px; flex-wrap: wrap">{sw("#1f5c45", "ŞOK")}{sw("#3d5a80", "Tarım Kredi")}'
            f'{sw("", "çekim başarısız", True)}</div>')


def a05():
    right = ("Son yenileme 28 Eyl 2026 09:14 · kural K21 <b>ÖNERİ</b> (ADR-015)")
    top = h1row("Toplayıcı", right)
    bn = banner("err", "<b>Tarım Kredi adapter'ı kırıldı</b> (28 Eyl 03:02): ürün sayfasında fiyat alanı bulunamadı, site yapısı "
                "değişmiş olabilir. Tarım Kredi fiyatları <b>Doğrulanamadı</b>, optimizasyona girmiyor; <b>12 plan etkilendi</b> ve "
                "yeniden değerlendirildi. <a href=\"A01-KararIzi.dc.html\">Etkilenen planlar</a> · "
                "<a href=\"A03-Audit.dc.html\">Çekim kaydı</a>")
    k_sok = f'<div style="font-size: 13px">{ph("[ölçülecek]")}</div><div style="margin: 6px 0 2px">{bar(98, 120, 108)}</div>' + small("hedef ≥%90 (çizgi)")
    k_tk = (f'<div style="font-size: 13px">{ph("[ölçülecek]")}</div><div style="margin: 6px 0 2px">{bar(0, 120, 108, empty=True)}</div>'
            + small("bugün çekim yok"))
    rows = (
        chain_row("ŞOK", "adapter v[..] · online katalog",
                  f'{pill("hi", "Çalışıyor")}' + small("Son çekim hatasız", "margin-top: 4px"),
                  lines("Son başarılı: <b>28 Eyl 03:00</b>", "Sonraki: 29 Eyl 03:00", "Heartbeat: 2 dk önce"),
                  k_sok,
                  f'<div style="font-size: 13px">{ph("[ölçülecek]")}</div>' + small("hedef ≤14 gün"),
                  f'<div style="font-size: 13px">{ph("[ölçülecek]")} fiyat</div>' + small("TTL yapılandırmadan"),
                  lines("robots.txt 28 Eyl 02:58", "ürün yolları açık", "Koruma: algılanmadı")) +
        chain_row("Tarım Kredi", "adapter v[..] · online katalog",
                  f'{pill("lo", "Başarısız")}' + small("Fiyat alanı bulunamadı, 3 deneme · iş çalışıyor", "margin-top: 4px"),
                  lines("Son başarılı: <b>26 Eyl 03:00</b>", "Sonraki deneme: 28 Eyl 15:00",
                        "Heartbeat: 1 dk önce"),
                  k_tk,
                  f'<div style="font-size: 13px">{ph("[ölçülecek]")}</div>' + small("hedef ≤14 gün"),
                  f'<div>{verdict("unk")}</div>' + small("Tüm Tarım Kredi fiyatları", "margin-top: 4px"),
                  lines("robots.txt 28 Eyl 02:59", "ürün yolları açık", "Koruma: algılanmadı"), broken=True))
    table = (f'<div class="card" style="padding: 14px 18px">{h2("Zincirler", "zincir başına bir satır · A2.4-c · durdurma gerekçe ister, audit log’a yazılır")}'
             f'<table style="margin-top: 6px; table-layout: fixed"><thead><tr><th style="width: 120px">Zincir</th><th style="width: 140px">Durum</th>'
             f'<th style="width: 175px">Çekim</th><th style="width: 140px">Fiyatlı SKU kapsaması</th><th style="width: 100px">Medyan fiyat yaşı</th>'
             f'<th style="width: 150px">TTL’i aşan → Doğrulanamadı</th><th style="width: 145px">robots.txt · koruma</th><th style="width: 130px">Eylem</th></tr></thead>'
             f'<tbody>{rows}</tbody></table></div>')
    ev = [("28 Eyl 03:02", "collector.run.fail", "Tarım Kredi · fiyat alanı bulunamadı"),
          ("27 Eyl 11:20", "collector.fetch.manual", "ŞOK · Levent · gerekçe: sözlüğe 6 malzeme eklendi")]
    evh = "".join(f'<div style="display: flex; gap: 10px; padding: 6px 0; border-top: 1px solid #eeeae2; font-size: 12.5px">'
                  f'<span class="mono" style="width: 86px; flex-shrink: 0">{t}</span><span class="mono" style="width: 150px; '
                  f'flex-shrink: 0; color: #1c2420">{k}</span><span>{d}</span></div>' for t, k, d in ev)
    chart = (f'<div class="card" style="padding: 14px 18px; display: flex; flex-direction: column; gap: 6px">'
             f'{h2("Kapsama, son 8 çekim günü", "örnek görünüm · değerler [ölçülecek]")}{legend()}{coverage_chart()}'
             f'<div style="font-size: 13px; font-weight: 700; margin-top: 2px">Son olaylar</div>{evh}</div>')
    perm = (
        f'<div class="card" style="padding: 14px 18px; display: flex; flex-direction: column">'
        f'{h2("Kimlik, kurallar ve izin", "K21 · K18")}'
        f'<div style="margin-top: 6px">'
        + kv("Bot adı (User-Agent)", '<span class="mono" style="color: #1c2420">NutriScanBot/[..]</span>', False)
        + kv("İletişim", f'{ph("[iletişim adresi]")} · User-Agent içinde')
        + kv("Hız sınırı ve zaman penceresi", "yapılandırma dosyasından · kodda sabit yok")
        + kv("Kapsam", "yalnız tarif sözlüğündeki malzemeler · katalog aynalanmaz")
        + kv("Giriş, CAPTCHA, bot koruması", "algılanırsa çekim kendiliğinden durur · aşılmaz")
        + kv("Her kayıt", "kaynak URL + çekim tarihi · ham veri yayımlanmaz")
        + kv("Yazılı izin", f'ŞOK {pill("gr", "Talep edilmedi")} · Tarım Kredi {pill("gr", "Talep edilmedi")}')
        + kv("Kamuya açık sürümde fiyat karşılaştırma", pill("lo", "Kapalı"))
        + '</div>'
        + small("İzin durumu üç değer alır: talep edilmedi · bekliyor · var. İzin gelene kadar veri yalnız geliştirme, "
                "deney ve demoda kullanılır. Açık ret ya da itiraz gelirse o zincirde toplama durur "
                "(<a href=\"A05b-ToplayiciDurduruldu.dc.html\">durdurulmuş hâl</a>).", "margin-top: 8px")
        + '</div>')
    bottom = (f'<div style="display: grid; grid-template-columns: 600px minmax(0, 1fr); gap: 16px; flex-grow: 1; min-height: 0">'
              f'{chart}{perm}</div>')
    return admin(top + bn + table + bottom, active="Toplayıcı", who="Levent · Admin")


def a05b():
    top = h1row("Toplayıcı", "Tarım Kredi durduruldu · 27 Eyl 2026 10:42")
    bn = banner("warn", "<b>Tarım Kredi'de toplama durduruldu:</b> kaynaktan itiraz geldi (27 Eyl). K21 gereği itiraz kapanana kadar "
                "yeni çekim yapılmaz. Tarım Kredi fiyatları <b>Doğrulanamadı</b>; planlar yalnız ŞOK fiyatıyla kuruluyor.")
    rows = (f'<tr><td {TD}><b>ŞOK</b></td><td {TD}>{pill("hi", "Çalışıyor")}</td><td {TD}>Son başarılı 28 Eyl 03:00<br>heartbeat 2 dk önce</td>'
            f'<td {TD}>{pill("gr", "Talep edilmedi")}</td><td {TD}>{ab("Şimdi çek")}</td></tr>'
            f'<tr><td {TD}><b>Tarım Kredi</b></td><td {TD}>{pill("gr", "Durduruldu")}'
            f'<div class="mut" style="font-size: 12px; margin-top: 4px">itiraz · 27 Eyl 10:42</div></td>'
            f'<td {TD}>Son başarılı 26 Eyl 03:00<br>iş kapalı · heartbeat “durduruldu”</td>'
            f'<td {TD}>{pill("md", "İtiraz açık")}</td>'
            f'<td {TD}><button class="b bed" type="button" disabled style="opacity: .55; white-space: nowrap">Yeniden başlat</button>'
            f'<div class="mut" style="font-size: 11.5px; margin-top: 4px">İtiraz kapanana kadar kapalı</div></td></tr>')
    table = (f'<div class="card" style="padding: 14px 18px">{h2("Zincirler")}<table style="margin-top: 6px; table-layout: fixed"><thead><tr>'
             f'<th style="width: 100px">Zincir</th><th style="width: 120px">Durum</th><th>Çekim</th><th style="width: 124px">İzin</th>'
             f'<th style="width: 150px">Eylem</th></tr></thead><tbody>{rows}</tbody></table></div>')
    dialog = (
        '<div class="card" style="border: 2px solid #1c2420; display: flex; flex-direction: column; gap: 12px">'
        f'{h2("Zinciri durdur · Tarım Kredi")}'
        '<label class="fl" for="nd">Neden<select class="in" id="nd"><option>Kaynaktan itiraz</option><option>Açık ret</option>'
        '<option>Koruma ya da CAPTCHA algılandı</option><option>Adapter bakımı</option></select></label>'
        '<label class="fl" for="ref">Yazışma ya da talep numarası<input class="in" id="ref" type="text" value="ITR-2026-001"></label>'
        '<label class="fl" for="gr">Gerekçe (zorunlu)<textarea id="gr">Tarım Kredi yazılı itiraz iletti; K21 gereği toplama durduruluyor.</textarea></label>'
        + small("Onaylayınca: zamanlanmış iş kapanır · Tarım Kredi fiyatları Doğrulanamadı olur ve optimizasyona girmez · açık planlar "
                "yeniden değerlendirilir (S16) · işlem audit log'a yazılır (K16). Audit yazılamazsa durdurma da yapılmaz.")
        + f'<div style="display: flex; gap: 10px">{ab("Durdur ve kaydet", "bok")}{ab("Vazgeç")}</div></div>')
    steps = [("27 Eyl 09:58", "İtiraz alındı", "User-Agent'taki iletişim adresine, Tarım Kredi'den"),
             ("27 Eyl 10:42", "Toplama durduruldu", "Levent · gerekçe ve talep no audit'te · <span class=\"mono\">collector.pause</span>"),
             ("27 Eyl 10:42", "Fiyatlar Doğrulanamadı", "Tarım Kredi fiyatları karara ve optimizasyona girmiyor (K11)"),
             ("27 Eyl 10:44", "Planlar yeniden değerlendirildi", f"{ph()} plan · yalnız ŞOK fiyatıyla"),
             ("açık", "Mevcut kayıtlar", f"silme ya da saklama: {ph('[ekip kararı · ADR]')}"),
             ("açık", "İtirazın yanıtı", f"{ph()} · yeniden başlatma yalnız itiraz kapanınca")]
    st = "".join(f'<div style="display: flex; gap: 12px; padding: 8px 0; border-top: 1px solid #eeeae2">'
                 f'<span class="mono" style="width: 86px; flex-shrink: 0">{t}</span><div><div style="font-size: 14px; font-weight: 700">{a}</div>'
                 f'<div class="mut" style="font-size: 12.5px">{b}</div></div></div>' for t, a, b in steps)
    timeline = f'<div class="card">{h2("Olay akışı", "K21 · K16 · S16")}<div style="margin-top: 6px">{st}</div></div>'
    audit = (f'<div class="card" style="background: #1c2420; color: #d9ded9; border: 0">'
             f'<div style="font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 8px">Audit kaydı</div>'
             f'<div class="mono" style="color: #c3cac5; line-height: 1.7">collector.pause · chain=TARIM_KREDI<br>reason=SOURCE_OBJECTION · '
             f'ref=ITR-2026-001<br>actor=levent · role=ADMIN · 2026-09-27T10:42<br>prevHash=9c1e… · hash=4a7b…</div>'
             f'<div style="margin-top: 8px"><a href="A03-Audit.dc.html" style="color: #9fd4b8">Audit log\'da aç</a></div></div>')
    body = (f'<div style="display: grid; grid-template-columns: minmax(0, 1fr) 420px; gap: 16px; flex-grow: 1; min-height: 0">'
            f'<div style="display: flex; flex-direction: column; gap: 16px; min-width: 0">{table}{timeline}</div>'
            f'<div style="display: flex; flex-direction: column; gap: 16px">{dialog}{audit}</div></div>')
    return admin(top + bn + body, active="Toplayıcı", who="Levent · Admin")


# ================================================================ A06 · Eşleme kuyruğu
def qitem(t, s, on=False):
    bg = "background: #f3efe6; border-color: #1c2420; " if on else ""
    return (f'<a href="A06-Esleme.dc.html" style="{bg}display: flex; flex-direction: column; gap: 2px; padding: 8px 10px; '
            f'border-radius: 9px; border: 1px solid transparent; text-decoration: none; color: #1c2420; font-size: 13.5px">'
            f'<b>{t}</b><span class="src">{s}</span></a>')


def qhead(t):
    return f'<div class="eb" style="padding: 10px 10px 2px">{t}</div>'


def a06():
    top = h1row("Eşleme kuyruğu", "Malzeme → ürün 4 · Barkod → ürün 2 · İçerik adı 1 · eşlenmemiş 6")
    unm = ["taze fasulye · online katalogda yok", "lor peyniri", "kinoa", "tam buğday bulguru", "kuru börülce", "glutensiz yufka"]
    left = ('<nav class="card" aria-label="Eşleme kuyruğu" style="padding: 6px; display: flex; flex-direction: column; gap: 2px; overflow: hidden">'
            + qhead("Malzeme → zincir ürünü")
            + qitem("yoğurt 1 kg", "5 aday · ŞOK + Tarım Kredi", True)
            + qitem("süt 1 L", "4 aday · sözlüğe yeni eklendi")
            + qitem("glutensiz makarna 500 g", "2 aday · yalnız ŞOK")
            + qitem("pirinç patlağı", "3 aday · gramaj farklı")
            + qhead("Barkod → zincir ürünü")
            + qitem("869[..] · Kakaolu kek 45 g", "“Bu ürün hangisi?” · 3 hane seçti")
            + qitem("869[..] · Nohut 1 kg", "1 hane seçti")
            + qhead("İçerik adı (RAG önerisi)")
            + qitem("glikoz-fruktoz şurubu", "→ eklenmiş şeker · onay bekliyor")
            + qhead("Eşlenmemiş malzemeler")
            + "".join(f'<div style="font-size: 13px; padding: 4px 10px">{u}</div>' for u in unm)
            + small("Sözlükte var, iki zincirde de aday yok. Taze meyve-sebze için fiyat yalnız tahmini referans, karar girdisi değil.",
                    "padding: 4px 10px")
            + '</nav>')

    def cand(chain, name, gram, pr, score, note, checked=False, dis=False):
        ch = " checked" if checked else ""
        td = 'style="padding: 7px 6px"'
        return (f'<tr><td {td}><input type="checkbox"{ch} aria-label="{chain} · {name} adayını seç" '
                f'style="width: 18px; height: 18px; accent-color: #1f5c45"></td>'
                f'<td {td}><b>{chain}</b></td><td {td}><div style="font-weight: 600; white-space: nowrap">{name}</div>'
                f'<div class="src" style="white-space: nowrap">{note}</div></td><td {td}>{gram}</td><td {td}>{pr}</td>'
                f'<td {td}><a href="#" style="font-size: 13px">{ph("[bağlantı]")}</a></td><td {td}>{score}</td></tr>')
    rows = (cand("ŞOK", "[Marka] Tam yağlı yoğurt", "1.000 g", price("69,90 TL", "ŞOK", "26 Eyl"),
                 pill("hi", "Yüksek · ad + gramaj"), "içindekiler adayı: süt, yoğurt kültürü", True)
            + cand("Tarım Kredi", "[Marka] Yoğurt", "1.000 g", price("64,50 TL", "Tarım Kredi", "27 Eyl"),
                   pill("hi", "Yüksek · ad + gramaj"), "içindekiler adayı: süt, yoğurt kültürü", True)
            + cand("ŞOK", "[Marka] Süzme yoğurt", "750 g", price("74,90 TL", "ŞOK", "26 Eyl"),
                   pill("md", "Orta · gramaj farklı"), "birim fiyatla karşılaştırılır · kıvam farklı")
            + cand("Tarım Kredi", "[Marka] Meyveli yoğurt", "1.000 g", price("79,00 TL", "Tarım Kredi", "27 Eyl"),
                   pill("lo", "Düşük · içerik farklı"), "meyve ve eklenmiş şeker · ayrı malzeme"))
    detail = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 10px; min-height: 0">'
        '<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px">'
        '<div><div style="font-size: 20px; font-weight: 700">yoğurt 1 kg <span class="mono">ING-0142</span></div>'
        '<div class="mut" style="font-size: 13px">Sözlük malzemesi · 9 tarifte · adaylar toplayıcıdan · skor ad + gramaj benzerliği</div></div>'
        f'{pill("gr", "İnsan onayı şart (K01)")}</div>'
        '<table style="table-layout: fixed"><thead><tr><th style="width: 34px"><span style="position: absolute; left: -9999px">Seç</span></th>'
        '<th style="width: 96px">Zincir</th><th>Aday ürün</th><th style="width: 74px">Gramaj</th>'
        '<th style="width: 180px">Fiyat · kaynak · tarih</th><th style="width: 84px">Kaynak</th><th style="width: 156px">Öneri skoru</th></tr></thead>'
        f'<tbody>{rows}</tbody></table>'
        '<div style="display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 14px; align-items: end">'
        '<label style="display: flex; flex-direction: column; gap: 6px; font-size: 13px; font-weight: 700">Gerekçe (zorunlu)'
        '<textarea placeholder="Örn. ad ve gramaj tutuyor, içindekiler adayı süt + kültür; meyveli ürün ayrı malzeme"></textarea></label>'
        '<div style="padding: 10px 12px; border-radius: 10px; background: #fbf5e3; border: 1px solid #e6d7a9; font-size: 13px; line-height: 1.45">'
        '<b>Onaylarsan:</b> seçili 2 ürün “yoğurt 1 kg” olarak fiyatlanır; 9 tarif ve açık planlar yeniden hesaplanır. '
        'İçindekiler adayı ayrıca A02 moderasyonundan geçer.</div></div>'
        f'<div style="display: flex; gap: 10px; align-items: center">{ab("Seçilenleri onayla", "bok")}{ab("Tümünü reddet", "bno")}'
        f'<span class="mut" style="font-size: 12.5px; margin-left: auto">Gerekçe boşken iki düğme de çalışmaz · her işlem audit log\'a yazılır.</span></div>'
        '</div>')
    barcode = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
        f'{h2("Barkod → zincir ürünü")}'
        '<div style="font-size: 13.5px"><span class="mono" style="color: #1c2420">869[..]</span> katalogda tanınmadı; kullanıcıların '
        '“Bu ürün hangisi?” seçimleri:</div>'
        '<div style="display: flex; flex-direction: column">'
        + kv("ŞOK · [Marka] Kakaolu kek 45 g", "3 hane seçti", False)
        + kv("ŞOK · [Marka] Kakaolu kek 40 g", "1 hane seçti")
        + kv("Tarım Kredi", "aday yok")
        + '</div>'
        + small("Onaya kadar eşleme yalnız seçen hanede “aday”; içerik hükmü değişmez, kimliği kesin olmayan ürüne “Engel "
                "bulunmadı” gösterilmez (S11). Gerekçe onay penceresinde zorunlu.")
        + f'<div style="display: flex; gap: 8px; margin-top: auto">{ab("45 g ile eşle", "bok")}{ab("Reddet", "bno")}</div>'
        + '</div>')
    rag = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
        f'{h2("İçerik adı eşleme · RAG önerisi", "FR-29 · SHOULD")}'
        '<div style="font-size: 15px"><b>“glikoz-fruktoz şurubu”</b> → sözlük: <b>eklenmiş şeker</b></div>'
        '<div style="border-left: 3px solid #cfc9bb; padding: 2px 0 2px 10px; font-size: 13px; line-height: 1.45">'
        f'Kaynak pasajı: {ph("[KAYNAK · belge, madde, tarih]")}</div>'
        + kv("Durum", pill("md", "Onay bekliyor · kullanılmıyor"), False)
        + kv("Onaylarsan", "HLT-SUGAR bu adı eklenmiş şeker sayar")
        + small("Anlamsal arama yalnız öneri üretir, karar yolunda yok (anayasa §3.4). Riski artıran eşleme tek onayla, "
                "azaltan eşleme iki kişi onayıyla geçer (K12).")
        + f'<div style="display: flex; gap: 8px; margin-top: auto">{ab("Onayla", "bok")}{ab("Reddet", "bno")}</div></div>')
    right = (f'<div style="display: flex; flex-direction: column; gap: 16px; min-width: 0; min-height: 0">{detail}'
             f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px">{barcode}{rag}</div></div>')
    body = (f'<div style="display: grid; grid-template-columns: 250px minmax(0, 1fr); gap: 16px; flex-grow: 1; min-height: 0">'
            f'{left}{right}</div>')
    return admin(top + body, active="Eşleme kuyruğu")


# ================================================================ A07 · Sözleşme panosu
S_RULES = [
    ("S1", "Her karar “Neden?” taşır", "UI–DR sözleşme testi", "A1.4-a"),
    ("S2", "Bilmediğini söyler, tahmin yok", "Property testi", "A2.3-a"),
    ("S3", "Sepeti konuşur, yargılamaz", "Yasaklı kelime testi", "A2.16-a"),
    ("S4", "Onaysız hiçbir şey değişmez", "Onay kartı testi", "A2.11-a"),
    ("S5", "Önce değer, sonra sağlık bilgisi", "Onboarding akış testi", "A2.2-d"),
    ("S6", "Her durum tasarlanır", "Ekran kabul kriteri", "[..]"),
    ("S7", "Bildirimde sağlık verisi yok", "Bildirim şablonu", "[..]"),
    ("S8", "Bilinmiyor, yok değildir", "Property test", "A2.3-a"),
    ("S9", "Katılaştırmak kolay, gevşetmek zor", "Profil API testi", "A2.2-b"),
    ("S10", "Kesin kısıtı yalnız sahibi açar", "Property + red-team", "A2.2-b"),
    ("S11", "“Engel yok” yalnız kesin ürüne", "Raf API testi", "A2.8-b"),
    ("S12", "Türkçeye dürüst çözümleme", "Altın set", "A2.3-b"),
    ("S13", "Araç kazanır, anlatım düşer", "Claim checker", "A2.11-a"),
    ("S14", "Tıbbi sınır sabit kuralla", "Sabit yanıt testi", "A2.11-a"),
    ("S15", "Sohbet ve ses TR'de maskelenir", "Kanarya testi", "A2.10-a"),
    ("S16", "Sürüm değişirse yeniden bakılır", "Olay testi", "A2.2-b"),
    ("S17", "Düzeltme haneye bildirilir", "Etki analizi testi", "A2.12-b"),
    ("S18", "Ad + kısıt birlikte taşınmaz", "Bildirim şablonu", "[..]"),
    ("S19", "Herkes kendi verisini verir", "Davet akışı testi", "A2.2-b"),
    ("S20", "Silme gerçektir (anahtar imhası)", "Silme testi", "A2.2-c"),
    ("S21", "LLM'siz mod vardır", "Chaos testi", "[..]"),
    ("S22", "Karar yalnız renkle verilmez", "UI bileşen testi", "A1.7-b"),
]
K_RULES = [
    ("K01", "LLM karar ve fiyat üretemez", "ArchUnit + rozet", "[..]"),
    ("K02", "Her iddia araç çıktısına bağlı", "Claim checker", "[..]"),
    ("K03", "Güvenlik monotonluğu", "Property + red-team", "[..]"),
    ("K04", "Dış içerik talimat olmaz", "Injection korpusu", "[..]"),
    ("K05", "Asistanın dış iletişimi yok", "Araç envanteri, CSP", "[..]"),
    ("K06", "Tek egress kapısı, fail-closed", "Egress kanaryası", "[..]"),
    ("K07", "Kiracı ayrımı (token, RLS)", "İki-hane, RLS", "[..]"),
    ("K08", "Değişmez Decision Record", "DR kapsama SLI", "[..]"),
    ("K09", "Sürümlü config, eval kapısı", "CI kapısı, geri alma", "A1.2-c"),
    ("K10", "Bağımsız doğrulayıcı", "İhlal sayacı", "[..]"),
    ("K11", "Veri kalitesi kapısı, TTL", "Fuzz, tazelik SLO", "A2.4-b"),
    ("K12", "Asimetrik moderasyon", "Birim test, audit", "[..]"),
    ("K13", "OFF verisi ayrı şemada", "Şema/rol, import", "[..]"),
    ("K14", "Yüklenen dosya korkulukları", "Kötü dosya korpusu", "[..]"),
    ("K15", "Sır repoda ve istemcide yok", "gitleaks kapısı", "[..]"),
    ("K16", "Audit append-only, zincirli", "Zincir doğrulama", "[..]"),
    ("K17", "Kota ve LLM'siz mod", "Chaos (LLM kapalı)", "[..]"),
    ("K18", "Gözlemlenebilirlik, heartbeat", "Log kanaryası", "A2.4-b"),
    ("K19", "Prod verisi prod dışına çıkmaz", "Erişim logu", "[..]"),
    ("K20", "Geri alma, kanıtlı kurtarma", "Tatbikat, göç", "[..]"),
    ("K21", "Dış veri toplama kuralları", "Adapter testleri", "A2.4-b"),
]


def rule_table(title, sub, rules, foot=""):
    tdp = 'style="padding: 3px 5px; font-size: 12px; white-space: nowrap; line-height: 1.35"'
    rows = []
    for rid, txt, test, pbi in rules:
        st = pill("md", "ÖNERİ") if rid == "K21" else pill("hi", "KABUL")
        pb = ph() if pbi == "[..]" else f'<span class="mono" style="color: #1c2420">{pbi}</span>'
        bg = ' style="background: #fbf5e3"' if rid == "K21" else ""
        rows.append(f'<tr{bg}><td {tdp}><b>{rid}</b></td><td {tdp}>{txt}</td><td {tdp}>{test}</td>'
                    f'<td {tdp}>{pb}</td><td {tdp}>{ph()}</td><td {tdp}>{st}</td></tr>')
    th = 'style="padding: 4px 5px"'
    return (f'<div class="card" style="padding: 12px 12px; overflow: hidden">{h2(title, sub)}'
            f'<table style="margin-top: 4px"><thead><tr><th {th}>#</th><th {th}>Kural (kısaltılmış)</th><th {th}>Zorlayan test</th>'
            f'<th {th}>PBI</th><th {th}>Son CI</th><th {th}>Durum</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
            f'{small(foot, "margin-top: 8px") if foot else ""}</div>')


def a07():
    top = h1row("Sözleşme panosu", "Kaynak: docs/anayasa.md · 29 Eyl 2026 · demo adım 6")
    strip = ('<div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap">'
             f'{pill("hi", "42 KABUL")}{pill("md", "1 ÖNERİ · K21")}{pill("gr", "Son CI: [..] · kod iskeleti A1.3 ile gelir")}'
             '<span class="mut" style="font-size: 13px; margin-left: auto">Madde eklemek, kaldırmak ya da gevşetmek yeni ADR ister. '
             'Kırmızı test = birleştirme engeli.</span></div>')
    grid = (f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; flex-grow: 1; min-height: 0">'
            f'{rule_table("Ürün sözleşmesi · S1–S22", "kullanıcıya verilen söz", S_RULES)}'
            f'{rule_table("Mimari kurallar · K01–K21", "kapattığı hata modları", K_RULES, "K21 ÖNERİ: ADR-015 ekip onayı bekliyor; ÖNERİ'yi KABUL'e yalnız ekip çevirir. Zorlayan testleri A2.4-b getirir; toplayıcı panosu A05.")}</div>')
    return admin(top + strip + grid, active="Sözleşme panosu", who="Levent · Admin")


# ================================================================ A08 · Kurallar ve sözlük
def a08():
    top = h1row("Kurallar ve sözlük", "Yayında: alerjen paketi v0.3 · sağlık eşik tablosu v0 · sözlük v0.4")
    packs = [("Alerjen paketi", "14 alerjen + çölyak/gluten · eser uyarısı", "v0.3", pill("hi", "Yayında")),
             ("Sağlık durumu kuralları", "diyabet · hipertansiyon · hamilelik", "v0", pill("md", "Taslak · kaynak eksik")),
             ("Malzeme sözlüğü", "eş anlamlılar · türevler · “içermez” kalıbı", "v0.4", pill("hi", "Yayında")),
             ("İçerik adı eşlemeleri", "RAG önerisi, moderatör onaylı", "v0.1", pill("hi", "Yayında"))]
    ph_ = "".join(f'<div class="card" style="padding: 12px 14px; display: flex; flex-direction: column; gap: 4px">'
                  f'<div style="display: flex; justify-content: space-between; gap: 8px"><b style="font-size: 14.5px">{a}</b>'
                  f'<span class="mono" style="color: #1c2420">{v}</span></div><div class="mut" style="font-size: 12.5px">{b}</div>'
                  f'<div>{s}</div></div>' for a, b, v, s in packs)
    packs_row = f'<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px">{ph_}</div>'
    td = 'style="padding: 7px 8px; font-size: 13px"'
    thr = [("HLT-SUGAR-01", "Diyabet", "Toplam şeker", "≥ 22,5 g / 100 g", verdict("warn")),
           ("HLT-SUGAR-02", "Diyabet", "Eklenmiş şeker adı içerikte", "içerik kuralı", verdict("warn")),
           ("HLT-SALT-01", "Hipertansiyon", "Tuz", f'≥ {ph()} g / 100 g', verdict("warn")),
           ("HLT-PREG-01", "Hamilelik", f'İçerik kuralı {ph()}', "içerik kuralı", verdict("warn")),
           ("HLT-ANY-00", "Hepsi", "Besin tablosu yok", "—", verdict("unk"))]
    rows = "".join(
        f'<tr><td {td}><span class="mono" style="color: #1c2420">{i}</span></td><td {td}>{d}</td><td {td}>{n}</td><td {td}>{e}</td>'
        f'<td {td}>{v}</td><td {td}>{ph("[KAYNAK]")}</td><td {td}>{ph()}</td><td {td}>{ph()}</td><td {td}>{ph()}</td>'
        f'<td {td}>{pill("md", "[bekliyor]")}</td></tr>' for i, d, n, e, v in thr)
    th = 'style="padding: 6px 8px"'
    table = (
        '<div class="card" style="padding: 14px 18px">'
        f'{h2("Sağlık eşik tablosu v0", "bilgilendirme dili · “Dikkat” + besin bilgisi + kaynak (anayasa §3)")}'
        f'<table style="margin-top: 6px"><thead><tr><th {th}>Kural</th><th {th}>Durum</th><th {th}>Besin / içerik</th><th {th}>Eşik</th>'
        f'<th {th}>Sonuç</th><th {th}>Kaynak belge</th><th {th}>Madde</th><th {th}>Tarih</th><th {th}>Doğrulayan</th>'
        f'<th {th}>Diyetisyen</th></tr></thead><tbody>{rows}</tbody></table>'
        + small("Kaynaksız eşik yayına çıkmaz: CI veri doğrulayıcısı (A1.2-c) kaynak, madde, tarih ve doğrulayan alanı boş satırı reddeder. "
                "Çölyak bu tabloda değil; kesin kısıt olarak alerjen paketinde.", "margin-top: 8px")
        + '</div>')
    gate = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 6px">'
        f'{h2("Değişiklik: sözlük v0.4 → v0.5", "K09")}'
        + kv("Katılaştıran", "“kakao yağı” fındık eser uyarısına bağlandı", False)
        + kv("Gevşeten", "“hindistan cevizi” ağaç yemişi grubundan çıktı")
        + kv("Altın set (n ≥ 300) · yanlış negatif", f'{ph("[ölçülecek]")} · kapı: 0')
        + kv("Sağlık tablosu uyumu", f'{ph("[ölçülecek]")} · kapı: %100')
        + kv("Replay · son 7 günün kararları", ph("[ölçülecek]"))
        + small("Kapıdan geçmeyen sürüm yayına çıkamaz.")
        + '</div>')
    impact = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
        f'{h2("Etki raporu", "yayından önce")}'
        '<div style="font-size: 22px; font-weight: 700">312 ürün: 40 katılaşır, 3 gevşer</div>'
        + small("Katılaşan 40 üründe hüküm ağırlaşır: etkilenen hanelere düzeltme bildirimi gider (S17). "
                "Gevşeyen 3 ürün için iki kişi onayı ve kanıt gerekir (K12).")
        + kv("1. onay", "Hilal · 28 Eyl 16:10 · kanıt: [KAYNAK]", True)
        + kv("2. onay", pill("md", "Bekliyor"))
        + f'<div style="display: flex; gap: 8px; margin-top: 2px"><button class="b bok" type="button" disabled style="opacity: .55">Yayına al</button>'
        f'{ab("Onayla (2. kişi)")}</div>'
        + small("Yayına al: iki onay ve kapı tamamlanınca açılır. Değişikliği öneren ikinci onayı veremez.")
        + '</div>')
    vers = [("sözlük v0.4", "22 Eyl · Levent + Hilal", "Yayında"), ("sözlük v0.3", "15 Eyl · Hilal", ""),
            ("alerjen paketi v0.3", "20 Eyl · Levent + Hilal", "Yayında"), ("alerjen paketi v0.2", "12 Eyl · Levent", "")]
    vh = "".join(f'<div style="display: flex; align-items: center; gap: 10px; padding: 6px 0; border-top: 1px solid #eeeae2">'
                 f'<div style="flex-grow: 1"><div style="font-size: 13.5px; font-weight: 700">{a}</div>'
                 f'<div class="mut" style="font-size: 12px">{b}</div></div>'
                 + (pill("hi", s) if s else ab("Bu sürüme geri al", "bed", "min-height: 34px; font-size: 13px; padding: 0 10px"))
                 + '</div>' for a, b, s in vers)
    versions = (f'<div class="card" style="display: flex; flex-direction: column; gap: 4px">{h2("Sürümler ve geri al", "K09 · S16")}{vh}'
                + small("Geri alma tek komuttur ve audit log'a yazılır; açık plan, liste ve önbellek yeniden değerlendirilir.")
                + '</div>')
    bottom = (f'<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; flex-grow: 1; min-height: 0">'
              f'{gate}{impact}{versions}</div>')
    return admin(top + packs_row + table + bottom, active="Kurallar ve sözlük", who="Levent · Admin")


# ================================================================ A09 · KVKK talepleri
def a09():
    top = h1row("KVKK talepleri", "Yasal yanıt süresi 30 gün · her işlem audit log'a yazılır (K16)")
    kpis = [("Açık talep", "4"), ("7 günden az kalan", "1"), ("Süresi geçen", "0"), ("Ortalama kapanış", "[ölçülecek]")]
    kh = "".join(f'<div class="card" style="padding: 12px 16px"><div class="mut" style="font-size: 12.5px; font-weight: 600">{a}</div>'
                 f'<div style="font-size: 24px; font-weight: 700">{b}</div></div>' for a, b in kpis)
    krow = f'<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px">{kh}</div>'

    def sla(left, total=30):
        w = int(110 * (total - left) / total)
        col = "#7d2317" if left <= 7 else "#1f5c45"
        return (f'<div style="font-size: 13px; font-weight: 700">{left} gün kaldı</div>'
                f'<div style="margin-top: 4px">{bar(w, 110, None, col)}</div>')
    reqs = [("KVK-0412", "m.11 · bilgi talebi", "hane_7f3…", "3 Eyl", sla(5), pill("md", "Yanıt taslağı"), "Levent", True),
            ("KVK-0415", "Hesap silme", "hane_a21…", "20 Eyl", sla(22), pill("gr", "Kimlik doğrulandı"), "Hilal", False),
            ("KVK-0416", "Veri indirme", "hane_12c…", "25 Eyl", sla(27), pill("hi", "Hazır · 24 saat"), "otomatik", False),
            ("KVK-0417", "m.11 · düzeltme", "hane_7f3…", "27 Eyl", sla(29), pill("gr", "Yeni"), "atanmadı", False)]
    td = 'style="padding: 8px 8px"'
    SEL = ' style="background: #f3efe6"'
    rows = "".join(
        f'<tr{SEL if on else ""}>'
        f'<td {td}><span class="mono" style="color: #1c2420">{n}</span></td><td {td}><b>{t}</b></td>'
        f'<td {td}><span class="mono">{h}</span></td><td {td}>{d}</td><td {td}>{s}</td><td {td}>{st}</td><td {td}>{a}</td></tr>'
        for n, t, h, d, s, st, a, on in reqs)
    queue = (f'<div class="card" style="padding: 14px 18px">{h2("Kuyruk", "hane kimliği maskeli · ad ve sağlık verisi bu listede yok")}'
             f'<table style="margin-top: 6px"><thead><tr><th>Talep</th><th>Tür</th><th>Hane</th><th>Geliş</th><th style="width: 140px">Süre</th>'
             f'<th>Durum</th><th>Atanan</th></tr></thead><tbody>{rows}</tbody></table></div>')
    steps = [("Kimlik", "Uygulama içi oturumla doğrulandı · 3 Eyl"),
             ("Kapsam", "İşlenen veri kategorileri, amaçlar, aktarım yapılan yerler"),
             ("Yanıt", "Uygulama içinde, okunur PDF · e-postayla veri gönderilmez"),
             ("Sağlık verisi", "Yalnız sahibine gösterilir; hanenin diğer yetişkinleri “hane üyesi 2” olarak görünür")]
    sh = "".join(kv(a, b, i > 0) for i, (a, b) in enumerate(steps))
    detail = (f'<div class="card" style="display: flex; flex-direction: column; gap: 6px">{h2("KVK-0412 · m.11 bilgi talebi", "5 gün kaldı")}'
              f'{sh}<div style="display: flex; gap: 8px; margin-top: 4px">{ab("Yanıtı gönder", "bok")}{ab("Süre uzatma notu ekle")}</div>'
              + small("Silme talebinde çocuk profilleri ve anahtar imhası önizlemesi gösterilir (S20); yedeklerden düşme süresi "
                      f"{ph()}.") + '</div>')
    left = f'<div style="display: flex; flex-direction: column; gap: 16px; min-width: 0">{queue}{detail}</div>'
    access = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 10px">'
        f'{h2("Destek erişimi", "süreli ve gerekçeli · K16")}'
        '<div style="padding: 10px 12px; border-radius: 10px; background: #eef5f0; border: 1px solid #bcd6c6; font-size: 13.5px">'
        '<b>Açık pencere:</b> Hilal · <span class="mono">hane_a21…</span> · talep KVK-0415<br>60 dakikadan <b>42 dk</b> kaldı · '
        'sağlık alanları maskeli</div>'
        f'<div>{ab("Pencereyi şimdi kapat", "bno")}</div>'
        '<div style="border-top: 1px solid #eeeae2; padding-top: 10px; font-size: 14px; font-weight: 700">Yeni pencere iste</div>'
        '<label class="fl" for="tn">Talep numarası (zorunlu)<select class="in" id="tn"><option>KVK-0412 · m.11 bilgi talebi</option>'
        '<option>KVK-0417 · m.11 düzeltme</option></select></label>'
        '<label class="fl" for="ge">Gerekçe (zorunlu)<textarea id="ge" placeholder="Örn. bilgi talebinin kapsamı için karar kayıtlarının listesi gerekiyor"></textarea></label>'
        + kv("Süre", "60 dk · yapılandırmadan · uzatılamaz, yeniden istenir", False)
        + kv("Görünen", "karar kayıtları ve katalog verisi · sağlık alanları maskeli")
        + f'<div>{ab("Pencereyi aç", "bok")}</div>'
        + small("Her erişim hanenin erişim geçmişine yazılır; kullanıcı bunu hane ve gizlilik sayfasında görür "
                "(<a href=\"W07-HaneWeb.dc.html\">W07</a>).")
        + '</div>')
    body = (f'<div style="display: grid; grid-template-columns: minmax(0, 1fr) 400px; gap: 16px; flex-grow: 1; min-height: 0">'
            f'{left}{access}</div>')
    return admin(top + krow + body, active="KVKK talepleri", who="Levent · Admin")


# ================================================================ A10 · Admin girişi (kabuksuz)
def a10():
    col = 'class="card" style="display: flex; flex-direction: column; gap: 12px; padding: 22px 24px"'
    step = lambda n, t: (f'<div style="display: flex; align-items: center; gap: 10px"><span style="display: inline-flex; '
                         f'align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 7px; '
                         f'background: #1c2420; color: #fff; font-size: 13px; font-weight: 700">{n}</span>'
                         f'<h2 class="disp" style="font-size: 20px">{t}</h2></div>')
    p1 = (f'<div {col}>{step(1, "Giriş")}'
          '<div style="font-size: 14.5px; line-height: 1.5">Ekip hesabınla giriş yap. Parola bu ekranda sorulmaz; kimlik sağlayıcıya '
          'yönlendirilirsin (OAuth2 / PKCE).</div>'
          f'{ab("Ekip hesabıyla devam et", "bok", "min-height: 46px")}'
          + small("Yalnız rol atanmış hesaplar girer. Kullanıcı uygulamasının hesabı admin paneline açılmaz.")
          + banner("err", "Bu hesaba admin rolü atanmamış. Rol için bir admine başvur.")
          + small("Yukarıdaki satır: rolü olmayan hesap durumu.")
          + '</div>')
    code_in = "".join(f'<input type="text" inputmode="numeric" maxlength="1" value="{d}" aria-label="Kod hanesi {i + 1}" '
                      f'style="width: 46px; height: 54px; text-align: center; font: inherit; font-size: 22px; font-weight: 700; '
                      f'border: 1.5px solid #cfc9bb; border-radius: 10px">' for i, d in enumerate("4829  "))
    p2 = (f'<div {col}>{step(2, "İki adımlı doğrulama")}'
          '<div style="font-size: 14.5px; line-height: 1.5">Doğrulama uygulamandaki 6 haneli kodu gir. Bu adım atlanamaz.</div>'
          f'<div style="display: flex; gap: 8px">{code_in}</div>'
          f'<div style="display: flex; gap: 10px">{ab("Doğrula", "bok", "min-height: 46px")}{ab("Donanım anahtarı kullan", "bed", "min-height: 46px")}</div>'
          + kv("Hatalı deneme sınırı", f'{ph()} · sonra hesap kilitlenir', False)
          + kv("Oturum süresi", "hareketsizlikte kapanır · süre yapılandırmadan")
          + kv("“Bu cihazı hatırla”", "yok · her girişte iki adım")
          + banner("warn", "Kod doğrulanamadı. Saatin doğru olduğundan emin ol ve yeni kodu gir.")
          + small("Yukarıdaki satır: hatalı kod durumu. Başarısız her deneme audit log'a yazılır.")
          + '</div>')
    roles = [("Moderatör", "katalog moderasyonu · eşleme kuyruğu · karar izi (okuma) · audit (okuma)"),
             ("Admin", "moderatörün tümü + kural yayını · toplayıcıyı durdurma · KVKK talepleri · destek erişimi · rol atama")]
    rh = "".join(kv(f"<b style='color: #1c2420'>{a}</b>", b, i > 0) for i, (a, b) in enumerate(roles))
    people = [("Levent", "Admin"), ("Hilal", "Moderatör"), ("Ozan", "Moderatör")]
    ppl = "".join(f'<tr><td style="padding: 7px 8px"><b>{a}</b></td><td style="padding: 7px 8px">'
                  f'<select class="in" aria-label="{a} rolü" style="height: 40px; font-size: 14px"><option{" selected" if b == "Admin" else ""}>Admin</option>'
                  f'<option{" selected" if b == "Moderatör" else ""}>Moderatör</option><option>Rol yok</option></select></td>'
                  f'<td style="padding: 7px 8px">{pill("hi", "MFA açık")}</td></tr>' for a, b in people)
    p3 = (f'<div {col}>{step(3, "Roller ve rol atama")}{rh}'
          f'<table><thead><tr><th>Kişi</th><th>Rol</th><th>MFA</th></tr></thead><tbody>{ppl}</tbody></table>'
          '<label style="display: flex; flex-direction: column; gap: 6px; font-size: 13px; font-weight: 700" for="rg">Gerekçe (zorunlu)'
          '<textarea id="rg" placeholder="Örn. Ozan kurallar ekranında vekil olacak"></textarea></label>'
          f'<div>{ab("Rol değişikliğini kaydet", "bok")}</div>'
          + small("Yalnız admin rol atar; kimse kendi rolünü değiştiremez. MFA'sı olmayan hesaba rol atanmaz. Değişiklik audit log'a yazılır.")
          + '</div>')
    html = ('<div class="w" style="flex-direction: column; padding: 40px 48px; gap: 24px">'
            '<div style="display: flex; align-items: baseline; gap: 14px"><span style="font-family: \'Fraunces\', Georgia, serif; '
            'font-size: 30px; font-weight: 600">NutriScan</span><span class="mut" style="font-size: 15px">admin paneli</span>'
            '<span class="mut" style="font-size: 13px; margin-left: auto">Giriş sonrası: <a href="A04-Operasyon.dc.html">Operasyon</a></span></div>'
            '<h1 class="disp" style="font-size: 34px">Admin girişi</h1>'
            '<div style="display: grid; grid-template-columns: 1fr 1fr 1.2fr; gap: 20px; flex-grow: 1; min-height: 0; align-items: start">'
            f'{p1}{p2}{p3}</div></div>')
    return html, 1440, 900


# ================================================================ W06 · Web giriş
def qr_svg(n=25, m=7):
    import hashlib
    cells = []

    def finder(x, y):
        return (f'<rect x="{x * m}" y="{y * m}" width="{7 * m}" height="{7 * m}" fill="#1c2420"></rect>'
                f'<rect x="{(x + 1) * m}" y="{(y + 1) * m}" width="{5 * m}" height="{5 * m}" fill="#fff"></rect>'
                f'<rect x="{(x + 2) * m}" y="{(y + 2) * m}" width="{3 * m}" height="{3 * m}" fill="#1c2420"></rect>')
    for y in range(n):
        for x in range(n):
            if (x < 8 and y < 8) or (x > n - 9 and y < 8) or (x < 8 and y > n - 9):
                continue
            if hashlib.md5(f"{x},{y}".encode()).digest()[0] % 2:
                cells.append(f'<rect x="{x * m}" y="{y * m}" width="{m}" height="{m}" fill="#1c2420"></rect>')
    s = n * m
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" role="img" aria-label="Giriş için QR kodu (örnek)">'
            f'<rect width="{s}" height="{s}" fill="#fff"></rect>{"".join(cells)}{finder(0, 0)}{finder(n - 7, 0)}{finder(0, n - 7)}</svg>')


def w06():
    topbar = ('<div style="height: 64px; display: flex; align-items: center; padding: 0 32px; border-bottom: 1px solid #e2dbcb; '
              'background: #fffdf8; flex-shrink: 0"><span style="font-family: \'Fraunces\', Georgia, serif; font-weight: 600; '
              'font-size: 20px">NutriScan</span><span class="mut" style="margin-left: 14px; font-size: 14px">web</span>'
              '<a href="W04-Seffaflik.dc.html" style="margin-left: auto; font-size: 14px; font-weight: 600">Nasıl karar veriyoruz</a></div>')
    qr = (
        '<div class="card" style="display: flex; gap: 24px; padding: 24px">'
        f'<div style="padding: 10px; background: #fff; border: 1px solid #e2dbcb; border-radius: 12px; align-self: flex-start">{qr_svg()}</div>'
        '<div style="display: flex; flex-direction: column; gap: 10px">'
        '<h2 class="disp" style="font-size: 22px">Telefonunla giriş yap</h2>'
        '<ol style="margin: 0; padding-left: 20px; font-size: 14.5px; line-height: 1.8">'
        '<li>Telefonunda NutriScan\'i aç.</li><li>Ayarlar\'da “Web\'de oturum aç”a dokun.</li><li>Bu kodu okut, telefonda onayla.</li></ol>'
        + small(f"Kod tek kullanımlık, {ph()} sn sonra yenilenir. Telefonda hangi tarayıcının istediği gösterilir.")
        + '<div style="margin-top: auto; display: flex; gap: 10px"><a class="btn2" href="W06-GirisWeb.dc.html">Kodu yenile</a></div>'
        '</div></div>')
    alt = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 12px; padding: 24px">'
        '<h2 class="disp" style="font-size: 22px">Ya da hesabınla</h2>'
        '<a class="btn" href="W03-Panel.dc.html" style="background: #1c2420">Apple ile devam et</a>'
        '<a class="btn2" href="W03-Panel.dc.html">Google ile devam et</a>'
        + cb("Bu cihazı hatırla", False, note="Varsayılan kapalı. Ortak bilgisayarda işaretleme.")
        + cb("Ekran paylaşımı modunda aç", False, note="Üye adları ve nedenler gizlenir; sunum ve görüntülü görüşme için.")
        + '<div style="border-top: 1px solid #ece5d6; padding-top: 10px">'
        + small("30 dakika hareketsiz kalırsan oturum kapanır; açık bir değişiklik varsa kaydedilmez, plan onaysız değişmez.")
        + '</div></div>')
    expired = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 10px">'
        f'<div style="display: flex; gap: 8px; align-items: center">{icon("clock", 20)}<b style="font-size: 16px">Oturumun kapandı</b></div>'
        '<div style="font-size: 14px; line-height: 1.5">30 dakika işlem yapılmadı. Kaydedilmemiş bir değişiklik yoktu.</div>'
        '<div style="display: flex; gap: 10px"><a class="btn" href="W06-GirisWeb.dc.html">Yeniden giriş yap</a></div>'
        + small("Durum: hareketsizlik sonrası.") + '</div>')
    qexp = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 10px">'
        f'<div style="display: flex; gap: 8px; align-items: center">{icon("qr", 20)}<b style="font-size: 16px">Kodun süresi doldu</b></div>'
        '<div style="font-size: 14px; line-height: 1.5">Telefonda onay gelmedi. Yeni kod oluştur ve tekrar okut.</div>'
        '<div><a class="btn2" href="W06-GirisWeb.dc.html">Yeni kod</a></div>' + small("Durum: QR zaman aşımı.") + '</div>')
    share_rows = [("Üye 1", "1 kesin kısıt", "gizli neden"), ("Üye 2", "2 kesin kısıt", "gizli neden"),
                  ("Üye 3", "1 hedef", "gizli neden"), ("Üye 4", "kısıt yok", "—")]
    sr = "".join(f'<div class="li"><span><b>{a}</b> <span class="mut" style="font-size: 12.5px">{b}</span></span>'
                 f'<span class="mut" style="font-size: 12.5px">{c}</span></div>' for a, b, c in share_rows)
    share = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 8px"><b style="font-size: 16px">Ekran paylaşımı modu</b>{wpill("Açık", "dk")}</div>'
        '<div style="font-size: 13.5px; line-height: 1.5">Adlar “Üye 1…4”, kısıt ve sağlık nedenleri “gizli” görünür. Tutarlar ve '
        'plan açık kalır. Üst çubuktaki etiketle her an kapatılır.</div>'
        f'{sr}' + small("Durum: giriş sonrası Planlama Stüdyosu listesi, maskeli.") + '</div>')
    body = (
        '<div style="flex-grow: 1; display: grid; grid-template-columns: minmax(0, 1fr) 420px; gap: 24px; padding: 32px 48px; min-height: 0">'
        '<div style="display: flex; flex-direction: column; gap: 18px; min-width: 0">'
        '<div><h1 class="disp" style="font-size: 36px">Haftanı büyük ekranda planla</h1>'
        '<div class="mut" style="font-size: 16px; margin-top: 6px">Web; Planlama Stüdyosu, sağlığın fiyatı ve hane paneli içindir. '
        'Hanenin kuruluşu ve profiller telefonda.</div></div>'
        f'<div style="display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 18px">{qr}{alt}</div>'
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px">{expired}{qexp}</div>'
        '</div>'
        f'<div style="display: flex; flex-direction: column; gap: 18px">{share}'
        '<div class="card" style="display: flex; flex-direction: column; gap: 6px">'
        '<b style="font-size: 15px">Web\'de olmayanlar</b>'
        '<div style="font-size: 13.5px; line-height: 1.5">Barkod tarama, kesin kısıtı gevşetme ve hesabı silme telefonda, yeniden kimlik '
        'doğrulamayla yapılır. Web\'den kesin kısıt yalnız katılaştırılır.</div></div>'
        '</div></div>')
    return web(topbar + body, nav=False)


# ================================================================ W07 · Hane ve gizlilik (web)
def w07():
    mem = [("S", "Selin", "planlayan · yönetici · kendi profili", chip_hard("Gluten (çölyak)"), "Profili düzenle", True),
           ("E", "Ela · 7", "veli: Selin", chip_hard("Fındık") + chip_hard("Yer fıstığı"), "Profili düzenle", True),
           ("M", "Murat", "kendi profilini yönetir", chip_soft("Şeker azalt"),
            "", False),
           ("C", "Can · 14", "veli: Selin", chip_none(), "Profili düzenle", True)]
    mh = ""
    for a, n, sub, chips, act, ed in mem:
        extra = ("" if ed else '<div class="mut" style="font-size: 12.5px; margin-top: 4px">Sağlık durumu yalnız Murat\'ta görünür; '
                 'hanede yalnız sonuç (Murat\'ın tercihi).</div>')
        btn_ = (f'<a class="btn2" href="W07-HaneWeb.dc.html" style="min-height: 40px; font-size: 13.5px; padding: 0 12px">{act}</a>'
                if ed else '<span class="mut" style="font-size: 12.5px">düzenleme kapalı</span>')
        mh += (f'<div style="display: flex; gap: 12px; padding: 12px 0; border-top: 1px solid #ece5d6; align-items: flex-start">{av(a)}'
               f'<div style="flex-grow: 1; min-width: 0"><div style="font-size: 15px; font-weight: 700">{n}</div>'
               f'<div class="mut" style="font-size: 12.5px">{sub}</div>'
               f'<div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px">{chips}</div>{extra}</div>{btn_}</div>')
    members = (
        f'<div class="card" style="display: flex; flex-direction: column">{h2("Üyeler", "4 kişi")}'
        f'<div style="margin-top: 6px">{mh}</div>'
        '<div style="display: flex; gap: 10px; margin-top: 10px"><button class="btn2" type="button">Üye ekle</button>'
        '<button class="btn2" type="button">Yöneticiliği devret</button></div>'
        + '<div class="mut" style="font-size: 12.5px; margin-top: 10px; line-height: 1.45">Kırmızı çerçeveli çipler kesin kısıttır; '
          'yalnız sahibi (çocukta veli) profilinden gevşetir. Yetişkinin bilgisini kendisi girer.</div>'
        + '</div>')
    ver = [("v3", "28 Eyl", "Yer fıstığı eklendi", "Selin (veli)"), ("v2", "14 Eyl", "Fındık eklendi", "Selin (veli)"),
           ("v1", "12 Eyl", "Profil oluşturuldu", "Selin (veli)")]
    vh = "".join(f'<div class="li"><span><span class="mono" style="color: #1c2420">{a}</span> · {c}</span>'
                 f'<span class="mut" style="font-size: 12.5px">{b} · {d}</span></div>' for a, b, c, d in ver)
    versions = (
        f'<div class="card" style="display: flex; flex-direction: column; gap: 8px">{h2("Ela · profil sürümleri", "S16")}{vh}'
        + small("Her karar profil sürümüne bağlıdır. Profil değişince açık plan ve liste yeniden değerlendirilir.")
        + '</div>')
    relax = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 10px">'
        f'{h2("Kesin kısıtı kaldır", "S9 · S10")}'
        '<div style="font-size: 14px; line-height: 1.5">Ela\'nın “Fındık” kısıtını kaldırmak için önce kimliğini yeniden doğrula. '
        'Bunu yalnız veli Selin yapabilir.</div>'
        + banner("warn", "Etki önizlemesi: 2 plan yemeği ve 1 liste kalemi yeniden değerlendirilecek.")
        + '<div style="display: flex; gap: 10px"><button class="btn" type="button">Kimliğimi doğrula</button>'
        '<button class="btn2" type="button">Vazgeç</button></div>'
        + small("Kısıt eklemek tek adım; kaldırmak ya da gevşetmek yeniden kimlik doğrulama ister.")
        + '</div>')
    cons = [("Hizmetin sunulması", "v1.0 · 12 Eyl", True), ("Sağlık bilgisi işleme · Selin", "v1.2 · 12 Eyl", True),
            ("Çocuk verisi · Ela, Can (veli)", "v1.2 · 12 Eyl", True), ("Asistan (Türkiye'de işlenir)", "v1.0 · 12 Eyl", True),
            ("Diyetisyenle paylaşım", "kapalı", False)]
    ch = "".join(f'<div class="li"><span><b style="font-size: 14px">{a}</b><br><span class="mut" style="font-size: 12px">{b}</span></span>'
                 f'{tgbtn(on, a)}</div>' for a, b, on in cons)
    consents = (
        f'<div class="card" style="display: flex; flex-direction: column">{h2("Rızalar", "amaç bazlı · Selin")}{ch}'
        + '<div style="padding: 10px 12px; border-radius: 12px; background: #f7f3ea; margin-top: 8px; font-size: 13px; line-height: 1.5">'
          '<b>Sağlık bilgisi onayını geri alırsan:</b> liste, bütçe, genel tarama ve kiler çalışır; kişisel sonuçlar, kısıtlı plan, '
          'radar ve sağlığın fiyatı kapanır. Onaydan önce bu özet gösterilir, sonra makbuz verilir.</div>'
        + '</div>')
    data = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 10px">'
        f'{h2("Verilerin")}'
        '<div style="display: flex; gap: 10px; flex-wrap: wrap"><button class="btn2" type="button">Verilerimi indir</button>'
        '<button class="btn2" type="button" style="color: #7d2317; border-color: #e0b6aa">Hesabı sil</button></div>'
        + small("İndirme: JSON + okunur PDF, hazırlanınca 24 saat geçerli, tek kullanımlık. Diğer yetişkinler “hane üyesi 2” olarak görünür.")
        + small("Silme: önce önizleme (hane, çocuk profilleri, anonim katkılar), sonra yeniden kimlik doğrulama. Anahtar imhası "
                f"geri alınamaz; geri alma penceresi {ph('[açık soru]')}.")
        + kv("Destek ekibi erişimi", "son 90 günde yok", True)
        + '</div>')
    body = (
        '<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 16px; padding: 24px 32px; min-height: 0">'
        + h1row("Hane ve gizlilik", "Aydın hanesi · 4 kişi · uygulama tıbbi cihaz değildir, teşhis sorulmaz")
        + '<div style="display: grid; grid-template-columns: 460px 400px minmax(0, 1fr); gap: 18px; flex-grow: 1; min-height: 0">'
        f'{members}<div style="display: flex; flex-direction: column; gap: 16px">{versions}{relax}</div>'
        f'<div style="display: flex; flex-direction: column; gap: 16px">{consents}{data}</div></div></div>')
    return web(body, active="Hane")


# ================================================================ W08 · Stüdyo durumları
def panel(n, title, inner):
    return (f'<div style="display: flex; flex-direction: column; gap: 6px; min-width: 0; min-height: 0">'
            f'<div style="font-size: 13px; font-weight: 700; color: #3d4742; display: flex; gap: 8px; align-items: center">'
            f'<span style="display: inline-flex; align-items: center; justify-content: center; min-width: 22px; height: 22px; '
            f'border-radius: 6px; background: #1c2420; color: #fff; font-size: 11.5px; padding: 0 6px">{n}</span>{title}</div>'
            f'<div class="card" style="flex-grow: 1; display: flex; flex-direction: column; gap: 10px; padding: 14px 16px; overflow: hidden">'
            f'{inner}</div></div>')


def w08():
    p0 = panel(1, "Varsayılan · kanıtlı en iyi", (
        f'{h2("Seçenekler", "B önerilen")}'
        '<div style="display: flex; gap: 22px"><div><div class="mut" style="font-size: 12px">Haftalık</div>'
        '<div style="font-size: 22px; font-weight: 700">5.940 TL</div></div><div><div class="mut" style="font-size: 12px">Değişiklik</div>'
        '<div style="font-size: 22px; font-weight: 700">3</div></div></div>'
        f'<div>{wpill("Çözüm 0,8 sn · en iyisi kanıtlandı (boşluk %0)", "hi")}</div>'
        + small("Fiyatlar: ŞOK ve Tarım Kredi online katalog · en eski 3 gün.")
        + '<a class="btn2" href="W05-PlanNeden.dc.html" style="margin-top: auto">Bu plan neden böyle?</a>'))
    p1 = panel(2, "Çözülüyor (en çok 3 sn)", (
        f'{h2("Seçenekler hesaplanıyor")}'
        '<div style="font-size: 13.5px; line-height: 1.7">Kesin kısıtlar: 20 öğün kontrol edildi<br>84 tariften 31\'i elendi<br>'
        'Birlikte çözülüyor…</div>'
        f'<div style="display: flex; align-items: center; gap: 10px">{bar(100, 220, None)}<span class="mono" style="white-space: nowrap">1,2 / 3 sn</span></div>'
        '<div class="skel" style="height: 90px"></div>'
        + small("3 saniyede bitmezse o ana kadarki en iyi plan, uzaklık rozetiyle gösterilir.")))
    p2 = panel(3, "Süre doldu", (
        f'{h2("Seçenek C")}'
        '<div style="font-size: 22px; font-weight: 700">6.180 TL</div>'
        f'<div>{wpill("Süre doldu · en iyiye en fazla %4 uzak", "md")}</div>'
        + small("Plan tüm kesin kısıtları sağlıyor; yalnız en ucuz olduğu kanıtlanmadı.")
        + '<div style="display: flex; gap: 8px; margin-top: auto"><button class="btn" type="button">Biraz daha ara</button>'
        '<button class="btn2" type="button">Bunu seç</button></div>'))
    p3 = panel(4, "Plan çıkmadı", (
        f'{h2("Bu kısıtlarla plan çıkmadı")}'
        '<div style="font-size: 13.5px; line-height: 1.45">Bütçe 4.000 TL iken 4 kişinin kesin kısıtlarını sağlayan plan yok. '
        'Birini seç:</div>'
        + rb("olursuz", "Bütçeyi 5.720 TL yap", True, "en ucuz uygun plan")
        + rb("olursuz", "Değişiklik sınırını 3'ten 5'e çıkar")
        + rb("olursuz", "Tuz azaltma hedefini bu hafta dışarıda bırak")
        + small("Kesin kısıtlar hiçbir seçenekte gevşemez.")))
    p4 = panel(5, "Yazıyla gevşetme reddi", (
        '<label for="w8t" style="font-size: 13px; font-weight: 700">Yazarak değiştir</label>'
        '<textarea id="w8t" style="width: 100%; height: 56px; border: 1.5px solid #cfc6b3; border-radius: 12px; padding: 8px 10px; '
        'font: inherit; font-size: 14px; resize: none">Ela bu hafta fındık yiyebilir</textarea>'
        + banner("err", "Kesin kısıt yazıyla gevşemez. Yalnız velisi, Ela'nın profilinden değiştirebilir.")
        + '<a href="W07-HaneWeb.dc.html" style="font-size: 13.5px; font-weight: 700">Hane sayfasını aç</a>'
        + small("Mesajın diğer kısmı yoksa plan değişmez.")))
    stale = [("Az tuzlu beyaz peynir", "189,90 TL", "Tarım Kredi", "5 Eyl"), ("Tavuk göğüs 1 kg", "249,00 TL", "ŞOK", "6 Eyl"),
             ("Portakal 2 kg", "93,00 TL", "ŞOK", "4 Eyl")]
    sh = "".join(f'<div class="li" style="align-items: flex-start"><span>{a}</span>{price(b, c, d, stale=True)}</div>' for a, b, c, d in stale)
    p5 = panel(6, "Fiyat eski", (
        banner("mute", "3 kalemin fiyatı TTL'i aştı: Doğrulanamadı, optimizasyona girmedi.")
        + f'<div>{sh}</div>'
        + '<div style="font-size: 13.5px">Toplam aralıkla: <b>5.728–5.910 TL</b> · online katalog fiyatı</div>'))
    p6 = panel(7, "“Bu planı seç” · onay ve geri al", (
        '<div style="border: 1.5px solid #1c2420; border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 8px">'
        '<b style="font-size: 15px">B planını seç?</b>'
        '<div style="font-size: 13.5px; line-height: 1.45">5.940 TL · 3 değişiklik. Liste ve menü bu plana göre güncellenir; '
        'onaylamadan hiçbir şey değişmez.</div>'
        '<div style="display: flex; gap: 8px"><button class="btn" type="button">Onayla</button><button class="btn2" type="button">Vazgeç</button></div></div>'
        '<div style="background: #1c2420; color: #fff; border-radius: 12px; padding: 10px 12px; display: flex; align-items: center; '
        'gap: 10px; font-size: 13.5px; margin-top: auto">Plan B seçildi<button type="button" style="margin-left: auto; background: none; '
        'border: 0; color: #9fd4b8; font: inherit; font-weight: 700; cursor: pointer; min-height: 36px">Geri al</button></div>'))
    phone_mock = (
        '<div style="width: 190px; height: 300px; border: 2px solid #1c2420; border-radius: 22px; padding: 16px 12px; align-self: center; '
        'display: flex; flex-direction: column; gap: 8px; background: #f5f1e8">'
        '<b style="font-size: 14px; line-height: 1.3">Planlama Stüdyosu masaüstünde daha rahat</b>'
        '<div style="font-size: 12px; line-height: 1.4" class="mut">Seçenek grafiği geniş ekran için. Telefonda aynı plan “Bu hafta”da.</div>'
        '<a class="btn" href="M05-BuHafta.dc.html" style="min-height: 44px; font-size: 13px; padding: 0 10px; margin-top: auto">Bu hafta\'ya git</a>'
        '<a class="btn2" href="W01-Studyo.dc.html" style="min-height: 44px; font-size: 13px; padding: 0 10px">Yine de aç</a></div>')
    p7 = panel(8, "Mobil tarayıcıda", phone_mock)
    grid = (f'<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); grid-template-rows: 1fr 1fr; gap: 18px; '
            f'flex-grow: 1; min-height: 0">{p0}{p1}{p2}{p3}{p4}{p5}{p6}{p7}</div>')
    body = ('<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 14px; padding: 20px 32px; min-height: 0">'
            + h1row("Planlama Stüdyosu · durumlar", '<a href="W01-Studyo.dc.html">Stüdyoya dön</a> · Seçenekler panelinin 8 hâli')
            + grid + '</div>')
    return web(body, active="Planlama Stüdyosu")


# ================================================================ W09 · Diyetisyen paylaşımı
def w09():
    form = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
        f'{h2("Paylaşım oluştur")}'
        '<div style="font-size: 13px; font-weight: 700; color: #3d4742; margin-top: 4px">Kimin verisi</div>'
        + cb("Selin", True)
        + cb("Murat", False, True, note="Yalnız Murat kendi telefonundan onaylarsa eklenir.")
        + cb("Ela · 7", False, note="Çocuk varsayılan dışarıda.")
        + cb("Can · 14", False, note="Çocuk varsayılan dışarıda.")
        + '<label class="fl" for="dn" style="margin-top: 4px">Dönem<select class="in" id="dn"><option>Son 4 hafta</option>'
        '<option>Son 8 hafta</option></select></label>'
        '<div style="font-size: 13px; font-weight: 700; color: #3d4742">Metrikler</div>'
        + cb("Haftalık plan ve liste özeti", True) + cb("Şeker ve tuz eğilimi (etiket bilgisiyle)", True)
        + cb("Sağlığın fiyatı", False)
        + '<div style="font-size: 13px; font-weight: 700; color: #3d4742">Süre</div>'
        '<div style="display: flex; gap: 18px">' + rb("sure", "7 gün") + rb("sure", "14 gün", True) + rb("sure", "30 gün") + '</div>'
        + '<div style="padding: 10px 12px; border-radius: 12px; background: #f7f3ea">'
        + cb("Seçtiğim verinin bu diyetisyenle paylaşılmasına açık rıza veriyorum.", False,
             note="Ayrı rıza · hane rızasından bağımsız · istediğin an iptal")
        + '</div>'
        '<button class="btn" type="button" disabled style="opacity: .55">Paylaşımı oluştur</button>'
        + small("Düğme rıza kutusu işaretlenince açılır.") + '</div>')
    logs = [("28 Eyl 10:12", "Görüntüledi", "Özet · Selin"), ("26 Eyl 18:40", "Görüntüledi", "Şeker eğilimi"),
            ("25 Eyl 09:03", "Paylaşım oluşturuldu", "Selin")]
    lg = "".join(f'<tr><td style="padding: 7px 8px"><span class="mono">{a}</span></td><td style="padding: 7px 8px">{b}</td>'
                 f'<td style="padding: 7px 8px">{c}</td></tr>' for a, b, c in logs)
    active = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
        f'{h2("Açık paylaşım", "25 Eyl – 9 Eki")}'
        + kv("Diyetisyen", ph("[diyetisyen adı]"), False)
        + kv("Kapsam", "Selin · son 4 hafta · 2 metrik")
        + kv("Bağlantı", "tek adres · salt okunur")
        + kv("Erişim kodu", '<span class="mono" style="color: #1c2420">•••• ••</span> · bağlantıdan ayrı iletildi')
        + kv("Kalan", "11 gün")
        + '<div style="font-size: 13px; font-weight: 700; margin-top: 6px">Erişim kaydı</div>'
        f'<table><tbody>{lg}</tbody></table>'
        '<button class="btn2" type="button" style="color: #7d2317; border-color: #e0b6aa; align-self: flex-start">Paylaşımı iptal et</button>'
        + small("İptal anında geçerli; bağlantı ve kod çalışmaz olur.") + '</div>')
    guest = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px; border: 2px solid #1c2420">'
        '<div class="eb">Diyetisyenin gördüğü</div>'
        f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 8px"><b style="font-size: 15px">Aydın hanesi · Selin</b>{wpill("Salt okunur")}</div>'
        + '<div class="li"><span>Haftalık plan · 22–28 Eyl</span><span>5 akşam</span></div>'
        '<div class="li"><span>Şeker eğilimi</span><span class="mut" style="font-size: 12.5px">etiket bilgisi · [..]</span></div>'
        + small("9 Eki'ye kadar açık. Düzenleme, indirme ve diğer üyeler yok.") + '</div>')
    exp = (
        '<div class="card" style="display: flex; flex-direction: column; gap: 8px">'
        '<div class="eb">Süresi dolunca</div>'
        '<b style="font-size: 15px">Bu paylaşımın süresi doldu</b>'
        '<div style="font-size: 13.5px; line-height: 1.45">Hane yeni bir paylaşım oluşturabilir. Bu sayfada veri gösterilmez.</div></div>')
    body = (
        '<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 16px; padding: 24px 32px; min-height: 0">'
        + h1row("Diyetisyenle paylaş", "Aydın hanesi · <a href=\"W03-Panel.dc.html\">Hane paneline dön</a>")
        + '<div style="display: grid; grid-template-columns: 460px minmax(0, 1fr) 380px; gap: 18px; flex-grow: 1; min-height: 0">'
        f'{form}{active}<div style="display: flex; flex-direction: column; gap: 16px">{guest}{exp}</div></div></div>')
    return web(body, active="Bu hafta")


# ================================================================ yaz ve denetle
SCREENS = [
    ("W06-GirisWeb", "W06 · Web giriş (QR · hatırla kapalı · 30 dk · ekran paylaşımı) — SHOULD (v5.2)", w06, "web"),
    ("W07-HaneWeb", "W07 · Hane ve gizlilik (web) — SHOULD (v5.2)", w07, "web"),
    ("W08-StudyoDurumlar", "W08 · Stüdyo durumları (8 hâl) — SHOULD (v5.2)", w08, "web"),
    ("W09-Diyetisyen", "W09 · Diyetisyen paylaşımı — COULD (v5.2)", w09, "web"),
    ("A05-Toplayici", "A05 · Toplayıcı sağlığı (ŞOK çalışıyor · Tarım Kredi kırıldı) — MUST (v5.2)", a05, "admin"),
    ("A05b-ToplayiciDurduruldu", "A05b · Toplayıcı: itiraz geldi, durduruldu — MUST (v5.2)", a05b, "admin"),
    ("A06-Esleme", "A06 · Malzeme–ürün eşleme kuyruğu — MUST (RAG ayrıntısı SHOULD) (v5.2)", a06, "admin"),
    ("A07-SozlesmePanosu", "A07 · Sözleşme panosu (S1–S22, K01–K21) — MUST (v5.2)", a07, "admin"),
    ("A08-Kurallar", "A08 · Kurallar ve sözlük — SHOULD (v5.2)", a08, "admin"),
    ("A09-KVKK", "A09 · KVKK talepleri ve destek erişimi — SHOULD (v5.2)", a09, "admin"),
    ("A10-AdminGiris", "A10 · Admin girişi, MFA ve roller — MUST (v5.2)", a10, "admin"),
]

if __name__ == "__main__":
    bad = False
    for stem, title, fn, kind in SCREENS:
        p = write(stem, title, fn(), kind, group=G)
        errs = check(p)
        print(stem, "OK" if not errs else errs)
        bad = bad or bool(errs)
    raise SystemExit(1 if bad else 0)
