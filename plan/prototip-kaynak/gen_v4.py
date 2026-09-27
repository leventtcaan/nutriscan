# v4 ekranlarını üretir (M16–M21). Ortak başlık + gövdeler.
import sys
sys.path.insert(0, '.')
from tabs import nav

HEAD = '''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&amp;family=Instrument+Sans:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0;font-family:'Instrument Sans',system-ui,sans-serif;color:#1c2420;background:#f5f1e8}}
*{{box-sizing:border-box}}
a{{color:#1f5c45}}a:hover{{color:#15432f}}
.s{{width:390px;height:844px;background:#f5f1e8;display:flex;flex-direction:column;overflow:hidden;position:relative}}
.pad{{padding-left:16px;padding-right:16px}}
.disp{{font-family:'Fraunces',Georgia,serif;font-weight:600;letter-spacing:-0.01em;margin:0}}
.eb{{font-size:11.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#56615b}}
.mut{{color:#56615b}}
.mono{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;color:#56615b}}
.card{{background:#fffdf8;border:1px solid #e2dbcb;border-radius:16px;padding:12px 14px}}
.ib{{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;border:1px solid #e2dbcb;background:#fffdf8;color:#1c2420;text-decoration:none;flex-shrink:0}}
.v{{display:inline-flex;align-items:center;gap:5px;height:24px;padding:0 8px;border-radius:7px;font-size:12px;font-weight:700;white-space:nowrap}}
.vno{{background:#f6ddd6;color:#7d2317}}
.vwarn{{background:#f7e8c4;color:#6b4700}}
.vok{{background:#dbece2;color:#17503a}}
.vunk{{background:#e4e7e9;color:#3c4750}}
.av{{width:26px;height:26px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;color:#fff;flex-shrink:0}}
.why{{display:inline-flex;align-items:center;gap:4px;font-size:13px;font-weight:700;color:#1f5c45;text-decoration:none}}
.btn{{display:flex;align-items:center;justify-content:center;gap:8px;min-height:48px;border-radius:14px;background:#1f5c45;color:#fff;font-weight:700;font-size:15px;text-decoration:none;border:0;font-family:inherit;cursor:pointer;padding:0 16px}}
.btn:hover{{color:#fff;background:#184a37}}
.btn2{{display:flex;align-items:center;justify-content:center;gap:8px;min-height:48px;border-radius:14px;background:#fffdf8;color:#1c2420;font-weight:700;font-size:14px;text-decoration:none;border:1.5px solid #cfc6b3;font-family:inherit;cursor:pointer;padding:0 14px}}
.btn2:hover{{color:#1c2420}}
.sb{{height:38px;border-radius:10px;font:inherit;font-weight:700;font-size:13.5px;cursor:pointer;padding:0 12px;background:#1f5c45;color:#fff;border:0}}
.soft{{font-size:11.5px;font-weight:700;color:#5e4d17;background:#fbf5e3;border:1px dashed #8a7433;border-radius:6px;padding:1px 6px}}
.chip{{display:inline-flex;align-items:center;gap:5px;min-height:26px;padding:0 9px;border-radius:999px;border:1px solid #d6cdb9;background:#fffdf8;font-size:12px;font-weight:600}}
.step{{display:flex;gap:8px;align-items:flex-start;font-size:12.5px;line-height:1.4;color:#3d4742;padding:3px 0}}
.dot{{width:16px;height:16px;border-radius:50%;background:#dbece2;color:#17503a;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}}
.me{{align-self:flex-end;max-width:82%;background:#1c2420;color:#fff;border-radius:18px 18px 4px 18px;padding:10px 14px;font-size:14.5px;line-height:1.4}}
.bot{{align-self:flex-start;max-width:92%;background:#fffdf8;border:1px solid #e2dbcb;border-radius:18px 18px 18px 4px;padding:12px 14px;font-size:14px;line-height:1.45}}
.tabs{{margin-top:auto;height:80px;border-top:1px solid #e2dbcb;background:#fffdf8;display:flex;justify-content:space-around;align-items:flex-start;padding-top:10px;flex-shrink:0}}
.tab{{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11px;font-weight:600;color:#56615b;text-decoration:none;width:64px}}
.tab:hover{{color:#1c2420}}
.tabon{{color:#1f5c45}}
</style>
</helmet>
'''
FOOT = '''</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":390,"height":844}}'>
class Component extends DCLogic {
  renderVals() { return {}; }
}
</script>
</body>
</html>
'''
CHECK = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
BACK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"></path></svg>'
MIC = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3"></rect><path d="M5 11a7 7 0 0 0 14 0M12 18v3"></path></svg>'
X = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"></path></svg>'
OK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
Q = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .8-1 1.5v.7M12 17v.01"></path></svg>'

def step(t):
    return f'<div class="step"><span class="dot">{CHECK}</span><span>{t}</span></div>'

def inputbar():
    return f'''  <div class="pad" style="padding-top: 8px; padding-bottom: 8px; display: flex; gap: 8px; align-items: center; flex-shrink: 0">
    <label style="flex-grow: 1; display: flex; align-items: center; height: 46px; border: 1.5px solid #cfc6b3; border-radius: 23px; background: #fff; padding: 0 16px"><input type="text" placeholder="Bir şey sor ya da yaz…" aria-label="Asistana yaz" style="border: 0; outline: 0; font: inherit; font-size: 14.5px; width: 100%; background: transparent"></label>
    <button type="button" aria-label="Sesle sor" style="width: 46px; height: 46px; border-radius: 50%; border: 0; background: #1f5c45; color: #fff; display: flex; align-items: center; justify-content: center; cursor: pointer">{MIC}</button>
  </div>
'''

BODIES = {}

BODIES['M16-Asistan.dc.html'] = ('Asistan', f'''<div class="s">
  <div style="display: flex; align-items: center; justify-content: space-between; padding: 18px 16px 8px">
    <div><div class="eb">Migros · Lara</div><h1 class="disp" style="font-size: 24px; margin-top: 2px">Asistan</h1></div>
    <span class="chip" title="Hane bilgisi Türkiye'de işlenir"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#1f5c45" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 4v5c0 4.5-3.5 8-8 9-4.5-1-8-4.5-8-9V7z"></path></svg>Hane verisi Türkiye'de</span>
  </div>
  <div class="pad" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-bottom: 6px">
    <div class="me"><span style="display: inline-flex; align-items: center; gap: 6px; font-size: 11.5px; opacity: .75; margin-bottom: 2px">{MIC.replace('width="20" height="20"','width="12" height="12"')} sesle</span><br>Bunu Ela yiyebilir mi?<div style="margin-top: 6px; font-size: 12px; background: #2e3833; border-radius: 8px; padding: 4px 8px; display: inline-block">Fındık Kremalı Gofret 36 g · az önce okuttun</div></div>
    <div class="bot">
      <div style="padding-bottom: 6px; border-bottom: 1px solid #ece5d6; margin-bottom: 8px">
        {step("Ürünü doğrulanmış katalogda buldum · 12 Eylül")}
        {step("Ela'nın profiline baktım · sürüm 3")}
        {step("Kural motoru çalıştı · 2 eşleşme")}
      </div>
      <span class="v vno">{X}Ela için uygun değil</span>
      <div style="margin-top: 6px">İçindekilerde <b>fındık ezmesi</b> var. Ayrıca paket “eser miktarda yer fıstığı içerebilir” diyor.</div>
      <div style="display: flex; gap: 14px; margin-top: 8px"><a class="why" href="M10-Neden.dc.html">Neden?</a><a class="why" href="M16-Asistan.dc.html">Yerine ne alayım?</a></div>
    </div>
    <div class="me">Yerine ne alayım? 25 lirayı geçmesin.</div>
    <div class="bot">
      <div style="padding-bottom: 6px; border-bottom: 1px solid #ece5d6; margin-bottom: 8px">
        {step("Aynı reyonda 6 aday buldum")}
        {step("Dördünüz için tek tek kontrol ettim")}
      </div>
      <div style="display: flex; flex-direction: column; gap: 8px">
        <div style="display: flex; align-items: center; gap: 10px"><span style="flex-grow: 1"><b>Sade pirinç patlağı</b> · 24,90 TL<br><span class="v vok" style="margin-top: 4px">{OK}4 kişi için engel yok</span></span><button class="sb" type="button">Listeye</button></div>
        <div style="display: flex; align-items: center; gap: 10px; border-top: 1px solid #ece5d6; padding-top: 8px"><span style="flex-grow: 1"><b>Sade mısır cipsi</b> · 19,50 TL<br><span class="v vunk" style="margin-top: 4px">{Q}Selin için doğrulanamadı</span></span><a class="why" href="M11-Dogrulanamadi.dc.html">Etiketi okut</a></div>
      </div>
    </div>
    <div class="mono" style="text-align: center">kararlar kural motorundan · asistan yalnız anlatır · scn_8f3a2c</div>
  </div>
{inputbar()}{nav('Asistan')}
</div>
''')

BODIES['M17-PazarPlani.dc.html'] = ('Pazar planı', f'''<div class="s">
  <div style="display: flex; align-items: center; gap: 12px; padding: 18px 16px 6px">
    <a class="ib" href="M05-BuHafta.dc.html" aria-label="Geri">{BACK}</a>
    <div><div class="eb">Pazar 27 Eylül · asistandan</div><h1 class="disp" style="font-size: 24px; margin-top: 2px">Haftalık planın hazır</h1></div>
  </div>
  <div class="pad" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; padding-top: 4px; padding-bottom: 8px">
    <div class="card" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; text-align: center">
      <div><div style="font-size: 21px; font-weight: 700">5</div><div class="mut" style="font-size: 12px">akşam yemeği</div></div>
      <div><div style="font-size: 21px; font-weight: 700">5.940 TL</div><div class="mut" style="font-size: 12px">bütçe 6.500</div></div>
      <div><div style="font-size: 21px; font-weight: 700">2</div><div class="mut" style="font-size: 12px">market</div></div>
    </div>
    <div class="card" style="display: flex; flex-direction: column; gap: 8px; font-size: 13.5px; line-height: 1.45">
      <div style="display: flex; gap: 8px"><span class="v vok" style="flex-shrink: 0">{OK}</span><span><b>Kilerdekiler önce:</b> yoğurt (SKT 29 Eyl) ve ıspanak (SKT 28 Eyl) pazartesi ve perşembe kullanılıyor.</span></div>
      <div style="display: flex; gap: 8px"><span class="v vok" style="flex-shrink: 0">{OK}</span><span><b>Kesin kısıtlar:</b> 5 yemek × 4 kişi = 20 öğün kontrol edildi; Ela için fındık, Selin için gluten yok.</span></div>
      <div style="display: flex; gap: 8px"><span class="v vok" style="flex-shrink: 0">{OK}</span><span><b>3 takas dahil:</b> ayda ~340 TL daha az, eklenmiş şeker −%25.</span></div>
      <div style="display: flex; gap: 8px"><span class="v vok" style="flex-shrink: 0">{OK}</span><span><b>A101 + Migros:</b> tek markete göre 212 TL daha az.</span></div>
    </div>
    <div class="card">
      <div style="font-size: 13px; font-weight: 700; color: #3d4742; padding-bottom: 4px">Nasıl hazırladım</div>
      {step("Kileri okudum · 12 kalem, 2'si bu hafta bozulacak")}
      {step("Tarif havuzundan 84 aday aldım")}
      {step("Kesin kısıtlara takılan 31 tarifi eledim")}
      {step("Menüyü, alışverişi ve marketi birlikte planladım · 0,8 sn")}
      {step("Sonucu kural motoruyla yeniden kontrol ettim")}
      <a class="why" href="W05-PlanNeden.dc.html" style="margin-top: 6px">Bu plan neden böyle?</a>
    </div>
    <div class="mut" style="font-size: 12.5px; text-align: center">Onaylamadan hiçbir şey değişmez.</div>
  </div>
  <div class="pad" style="display: flex; gap: 8px; padding-bottom: 22px; padding-top: 6px; flex-shrink: 0">
    <a class="btn2" href="M18-Menu.dc.html" style="flex: 1">Değiştir</a>
    <a class="btn" href="M18-Menu.dc.html" style="flex: 1.4">Onayla</a>
  </div>
</div>
''')

def meal(day, name, meta, extra=''):
    return f'''    <div class="card" style="display: flex; gap: 12px; align-items: flex-start">
      <div style="width: 44px; flex-shrink: 0; text-align: center"><div class="eb" style="font-size: 11px">{day}</div></div>
      <div style="flex-grow: 1">
        <div style="font-weight: 700; font-size: 15px">{name}</div>
        <div class="mut" style="font-size: 12.5px; margin-top: 2px">{meta}</div>
        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px"><span class="v vok">{OK}4 kişi için engel yok</span>{extra}</div>
      </div>
      <button type="button" aria-label="{name} yerine başka yemek" style="width: 40px; height: 40px; border-radius: 10px; border: 1.5px solid #cfc6b3; background: #fffdf8; cursor: pointer; display: flex; align-items: center; justify-content: center"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1c2420" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h13l-3-3M20 17H7l3 3"></path></svg></button>
    </div>
'''

BODIES['M18-Menu.dc.html'] = ('Haftanın menüsü', f'''<div class="s">
  <div style="padding: 18px 16px 6px"><div class="eb">29 Eylül – 3 Ekim · hafta içi akşam</div><h1 class="disp" style="font-size: 24px; margin-top: 2px">Bu haftanın menüsü</h1></div>
  <div class="pad" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; padding-top: 4px; padding-bottom: 8px">
{meal('PZT', 'Ispanaklı yumurta', '15 dk · kilerdeki ıspanak kullanılıyor', '<span class="chip">kilerden</span>')}
{meal('SAL', 'Mercimek çorbası + pirinç pilavı', '35 dk · Selin için glutensiz, ayrıca bir şey gerekmez')}
{meal('ÇAR', 'Fırında tavuk ve patates', '45 dk · hafta içi süre sınırını aşmıyor')}
{meal('PER', 'Zeytinyağlı taze fasulye + yoğurt', '40 dk · kilerdeki yoğurt kullanılıyor', '<span class="chip">kilerden</span>')}
{meal('CUM', 'Ev yapımı pizza', '50 dk · Selin için glutensiz taban ayrı', '<span class="soft">hane içi bölme · +38 TL</span>')}
    <div style="display: flex; gap: 8px"><button class="btn2" type="button" style="flex: 1">Misafir ekle</button><button class="btn2" type="button" style="flex: 1">Süreyi değiştir</button></div>
    <a class="card" href="M06-Takas.dc.html" style="display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: #1c2420; background: #eef5f0; border-color: #bcd6c6"><span><b style="display: block">Bu menüden liste: 23 kalem</b><span class="mut" style="font-size: 12.5px">alışkanlıklarınla birlikte · 3 takas dahil</span></span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1f5c45" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"></path></svg></a>
  </div>
{nav('Menü')}
</div>
''')

BODIES['M19-Mutfak.dc.html'] = ('Mutfak', f'''<div class="s">
  <div style="padding: 18px 16px 6px"><div class="eb">Aydın hanesi</div><h1 class="disp" style="font-size: 24px; margin-top: 2px">Mutfak</h1></div>
  <div class="pad" style="display: flex; gap: 6px; padding-bottom: 8px">
    <a class="btn" href="M09-Tarama.dc.html" style="flex: 1; min-height: 44px; font-size: 13.5px; padding: 0 8px">Barkodla ekle</a>
    <a class="btn2" href="M13-Fis.dc.html" style="flex: 1; min-height: 44px; font-size: 13.5px; padding: 0 8px">Fiş / e-Arşiv</a>
    <a class="btn2" href="M19-Mutfak.dc.html" style="flex: 1; min-height: 44px; font-size: 13.5px; padding: 0 8px">Dolabı kontrol et</a>
  </div>
  <div class="pad" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; padding-bottom: 8px">
    <div class="card">
      <div style="font-size: 13px; font-weight: 700; color: #3d4742; padding-bottom: 4px">Yakında bitecek <span class="mut" style="font-weight: 500">· alım sıklığınıza göre tahmin</span></div>
      <div style="display: flex; align-items: center; gap: 10px; padding: 8px 0; border-top: 1px solid #ece5d6"><span style="flex-grow: 1"><b>Süt</b> <span class="mut" style="font-size: 12.5px">· ~2 gün</span></span><button class="sb" type="button">Listeye</button></div>
      <div style="display: flex; align-items: center; gap: 10px; padding: 8px 0; border-top: 1px solid #ece5d6"><span style="flex-grow: 1"><b>Yumurta</b> <span class="mut" style="font-size: 12.5px">· ~4 gün</span></span><button class="sb" type="button">Listeye</button></div>
    </div>
    <div class="card">
      <div style="font-size: 13px; font-weight: 700; color: #3d4742; padding-bottom: 4px">Son kullanma yaklaşan</div>
      <div style="display: flex; align-items: center; gap: 10px; padding: 8px 0; border-top: 1px solid #ece5d6"><span style="flex-grow: 1"><b>Ispanak</b> <span class="mut" style="font-size: 12.5px">· SKT 28 Eyl</span></span><span class="v vok">{OK}Pazartesi menüde</span></div>
      <div style="display: flex; align-items: center; gap: 10px; padding: 8px 0; border-top: 1px solid #ece5d6"><span style="flex-grow: 1"><b>Yoğurt 1 kg</b> <span class="mut" style="font-size: 12.5px">· SKT 29 Eyl</span></span><span class="v vok">{OK}Perşembe menüde</span></div>
    </div>
    <div class="card" style="border-color: #d6cdb9; background: #f7f3ea">
      <div style="font-size: 13px; font-weight: 700; color: #3d4742; padding-bottom: 4px">Emin olmadıklarımız</div>
      <div style="font-size: 13.5px; line-height: 1.4; padding: 6px 0">
        <b>Beyaz peynir</b> <span class="mut">· 12 gündür haber yok</span><br>
        <span class="mut" style="font-size: 12.5px">Kayıt zamanla gerçekten kopar; ara ara sormak planı doğru tutar.</span>
      </div>
      <div style="display: flex; gap: 8px"><button class="sb" type="button">Hâlâ var</button><button type="button" style="height: 38px; border-radius: 10px; font: inherit; font-weight: 700; font-size: 13.5px; cursor: pointer; padding: 0 12px; background: transparent; border: 1.5px solid #cfc6b3">Bitti</button></div>
    </div>
    <a class="card" href="M20-Radar.dc.html" style="display: flex; gap: 10px; align-items: center; text-decoration: none; color: #1c2420; border-color: #d9a597; background: #fcf1ed"><span class="v vno" style="flex-shrink: 0">{X}</span><span style="flex-grow: 1; font-size: 13.5px"><b>Kakaolu kekin içeriği değişti</b><br><span style="color: #5e1a10; font-size: 12.5px">Kilerinde 2 paket var · Ela için artık uygun değil</span></span></a>
    <a class="card" href="M14-PlanGercek.dc.html" style="display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: #1c2420"><span><b style="display: block; font-size: 14px">Geçen hafta: plan ve gerçek</b><span class="mut" style="font-size: 12.5px">%82 uyum · 3 takastan 2'si kalıcı</span></span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1f5c45" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"></path></svg></a>
  </div>
{nav('Mutfak')}
</div>
''')

BODIES['M20-Radar.dc.html'] = ('İçerik değişikliği', f'''<div class="s">
  <div style="display: flex; align-items: center; gap: 12px; padding: 18px 16px 6px">
    <a class="ib" href="M19-Mutfak.dc.html" aria-label="Geri">{BACK}</a>
    <div><div class="eb">İçerik değişikliği radarı</div><h1 class="disp" style="font-size: 22px; margin-top: 2px; line-height: 1.15">Aldığınız bir ürünün tarifi değişti</h1></div>
  </div>
  <div class="pad" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; padding-top: 4px; padding-bottom: 8px">
    <div class="card">
      <div style="font-weight: 700; font-size: 15.5px">Kakaolu Kek 45 g</div>
      <div class="mut" style="font-size: 12.5px">Son 30 günde 3 kez aldınız · kilerde 2 paket</div>
      <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px"><span class="v vno">{X}Ela için artık uygun değil</span></div>
    </div>
    <div class="card" style="font-size: 13.5px; line-height: 1.5">
      <div style="font-size: 13px; font-weight: 700; color: #3d4742; padding-bottom: 6px">Ne değişti?</div>
      <div class="mut" style="font-size: 12px; font-weight: 700">ÖNCE</div>
      <div style="padding-bottom: 8px">… kakao, bitkisel yağ, emülgatör (soya lesitini), kabartıcı.</div>
      <div style="font-size: 12px; font-weight: 700; color: #7d2317">ŞİMDİ</div>
      <div>… kakao, bitkisel yağ, <span style="background: #f6ddd6; color: #5e1a10; font-weight: 700; padding: 0 3px; border-radius: 4px">fındık ezmesi (%2)</span>, emülgatör (soya lesitini), kabartıcı.</div>
    </div>
    <div class="card" style="font-size: 13px; line-height: 1.45">
      <div class="mut">Kaynak: etiket fotoğrafı, 25 Eylül · ekip doğruladı · Open Food Facts'e de bildirildi</div>
      <div style="margin-top: 6px; padding: 8px 10px; border-radius: 10px; background: #fbf5e3; color: #4f3f10"><b>Dikkat:</b> Raftaki ve kilerdeki eski paketler eski tarifi taşıyor olabilir. Elindeki paketin etiketine bak.</div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 8px">
      <a class="btn" href="M16-Asistan.dc.html">Ela için alternatif göster</a>
      <a class="btn2" href="M19-Mutfak.dc.html">Kilerdeki paketleri işaretle</a>
    </div>
    <div class="mut" style="font-size: 12px; text-align: center">Bu bildirim, ürünü son 30 günde alan ya da kilerinde tutan her haneye gitti.</div>
  </div>
</div>
''')

BODIES['M21-TibbiSinir.dc.html'] = ('Tıbbi sınır', f'''<div class="s">
  <div style="display: flex; align-items: center; justify-content: space-between; padding: 18px 16px 8px">
    <div><div class="eb">Ev</div><h1 class="disp" style="font-size: 24px; margin-top: 2px">Asistan</h1></div>
  </div>
  <div class="pad" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-bottom: 6px">
    <div class="me">Ela'nın fındık alerjisi var ama birazcık yese bir şey olmaz, değil mi?</div>
    <div class="bot">
      <span class="chip" style="margin-bottom: 8px">Sabit güvenlik yanıtı · yapay zekâ üretmedi</span>
      <div>Buna cevap veremem. Alerjide “ne kadarı sorun olmaz” sorusunu ancak Ela'nın doktoru cevaplayabilir.</div>
      <div style="margin-top: 8px">NutriScan, Ela'nın kesin kısıtını hiçbir koşulda gevşetmez. İstersen fındık içermeyen seçeneklere bakabiliriz.</div>
      <div style="display: flex; gap: 14px; margin-top: 8px"><a class="why" href="M16-Asistan.dc.html">Fındıksız seçenekler</a></div>
    </div>
    <div class="me">Dudağı şişiyor gibi</div>
    <div class="bot" style="border: 2px solid #8e2b1d; background: #fcf1ed">
      <div style="font-weight: 700; font-size: 16px; color: #5e1a10">Hemen 112'yi arayın.</div>
      <div style="margin-top: 6px; color: #5e1a10">Dudak ya da dil şişmesi, nefes darlığı, kusma, baş dönmesi acil durum belirtisi olabilir. Doktorunuzun verdiği bir adrenalin kalemi varsa talimata göre kullanın.</div>
      <a href="tel:112" style="display: flex; align-items: center; justify-content: center; gap: 8px; min-height: 52px; border-radius: 14px; background: #8e2b1d; color: #fff; font-weight: 700; font-size: 17px; text-decoration: none; margin-top: 10px">112'yi ara</a>
      <div class="mut" style="font-size: 12px; margin-top: 8px">Bu yanıt sabittir; yapay zekâya sorulmadan anında gösterilir.</div>
    </div>
  </div>
{inputbar()}{nav('Asistan')}
</div>
''')

for fn, (title, body) in BODIES.items():
    with open('project/' + fn, 'w') as f:
        f.write(HEAD.format(title=title) + body + FOOT)
print(list(BODIES))
