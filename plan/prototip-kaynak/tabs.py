# v4 sekme çubuğu üretici
ICON={
 'home':'<path d="M4 11l8-7 8 7v9H4z"></path>',
 'menu':'<rect x="4" y="5" width="16" height="15" rx="2"></rect><path d="M4 10h16M9 3v4M15 3v4"></path>',
 'scan':'<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M7 12h10"></path>',
 'fridge':'<rect x="6" y="3" width="12" height="18" rx="2"></rect><path d="M6 10h12M9 6v2M9 13v3"></path>',
 'chat':'<path d="M4 5h16v11H9l-5 4z"></path><path d="M8 10h8M8 13h5"></path>',
}
TABS=[('M05-BuHafta.dc.html','home','Bu hafta'),('M18-Menu.dc.html','menu','Menü'),('M09-Tarama.dc.html','scan','Tara'),('M19-Mutfak.dc.html','fridge','Mutfak'),('M16-Asistan.dc.html','chat','Asistan')]
def nav(active):
    out=['  <nav class="tabs" aria-label="Ana gezinme">']
    for href,ic,label in TABS:
        cls='tab tabon' if label==active else 'tab'
        out.append(f'    <a class="{cls}" href="{href}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[ic]}</svg>{label}</a>')
    out.append('  </nav>')
    return '\n'.join(out)
