# -*- coding: utf-8 -*-
"""
TAYYOR MATERIALLAR (ko'rsatmasiz): talabalarga to'g'ridan-to'g'ri beriladigan varaqlar.

  1. 35 ta variant: anatomiya/farmakologiya — rasm qidirish so'zlari + tayyor ma'lumot; 1 ta WordArt'li namuna
  2. 6 ta variant: shakllardan yig'iladigan tayyor rasm (nishon rasm + shakllar ro'yxati)
  3. 6 ta variant: kolontitul va avtomatik sahifa raqami (nishon ko'rinish + yoziladigan matn + sozlamalar)

Ishga tushirish (shu papkada):  python ready_materials.py
Natija: ../tarqatma/tayyor/
"""
import os

from handouts import POSTER_CSS, print_doc, to_pdf
from ready_data import ANATOMIYA_XIRURGIYA, NAMUNA
from svgs import kol_pages, wordart

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_HTML = os.path.join(HERE, 'out', 'tayyor')
PDF_DIR = os.path.join(ROOT, 'tarqatma', 'tayyor')
IMG = '../../../tarqatma/rasmlar'
TEX = 'Shahrisabz Tibbiyot Texnikumi'

CSS = '''
  .sheet.rv { font-family: Arial, Helvetica, sans-serif; font-size: 10pt; line-height: 1.4; padding: 1.3cm 1.7cm 1.2cm 1.7cm; }
  .rv .info-fio { margin: 0.25cm 0 0.3cm 0; }
  .rv .band { display: flex; align-items: center; gap: 0.35cm; margin: 0.1cm 0 0.15cm 0; }
  .rv .tag { background: var(--tc); color: #fff; font-weight: 700; font-size: 9pt; letter-spacing: 0.06em; text-transform: uppercase; padding: 0.08cm 0.35cm; border-radius: 3pt; }
  .rv .no { margin-left: auto; font-weight: 800; font-size: 11pt; color: var(--tc); }
  .rv h1 { font-size: 24pt; line-height: 1.12; color: #111; margin: 0.1cm 0 0.3cm 0; font-family: Arial, sans-serif; }
  .rv .box { border: 0.9pt solid #d2dae8; border-left: 4pt solid var(--tc); border-radius: 3pt; padding: 0.22cm 0.4cm; margin-bottom: 0.3cm; }
  .rv .box h2 { margin: 0 0 0.12cm 0; padding: 0; border: 0; font-size: 10.5pt; text-transform: uppercase; letter-spacing: 0.04em; color: var(--tc); }
  .rv .kw { display: flex; flex-wrap: wrap; gap: 0.18cm; margin-bottom: 0.12cm; }
  .rv .kw span { border: 0.9pt solid var(--tc); border-radius: 10pt; padding: 0.04cm 0.32cm; font-weight: 700; font-size: 9.5pt; }
  .rv .box p { margin: 0 0 0.1cm 0; }
  .rv .box ol { margin: 0.08cm 0 0 0; padding-left: 0.6cm; } .rv .box li { margin-bottom: 0.1cm; font-size: 10.5pt; }
  .rv .box li::marker { font-weight: 700; color: var(--tc); }
  .rv .lead { font-size: 11pt; font-weight: 700; }
  .rv table.rdy { width: 100%; border-collapse: collapse; font-size: 10pt; }
  .rv table.rdy td { border: 0.75pt solid #c9d6ea; padding: 0.1cm 0.2cm; vertical-align: top; }
  .rv table.rdy td:first-child { width: 4.2cm; font-weight: 700; background: #f3f6fb; }
  .rv .big { font-family: "Arial Black", Arial, sans-serif; font-weight: 900; font-size: 13pt; letter-spacing: 0.02em; }
  .rv .frame { height: 6.2cm; border: 1.2pt dashed #9aa8bd; border-radius: 4pt; display: flex; align-items: center; justify-content: center; color: #8793a8; font-size: 10pt; margin-bottom: 0.3cm; text-align: center; }
  .rv .fig { text-align: center; margin: 0.15cm 0 0.3cm 0; border: 0.75pt solid #d2dae8; border-radius: 4pt; padding: 0.25cm; background: #fff; }
  .rv .fig svg { display: block; margin: 0 auto; }
  .rv table.leg { width: 100%; border-collapse: collapse; font-size: 9.6pt; }
  .rv table.leg th { background: var(--tc); color: #fff; text-align: left; padding: 0.07cm 0.2cm; font-size: 9pt; }
  .rv table.leg td { border: 0.75pt solid #c9d6ea; padding: 0.07cm 0.2cm; vertical-align: top; }
  .rv table.leg td:first-child { font-weight: 700; }
  .rv .sw { display: inline-block; width: 0.34cm; height: 0.34cm; border-radius: 2pt; vertical-align: -1.5pt; margin-right: 0.12cm; border: 0.5pt solid #0004; }
  .rv .cols { display: grid; grid-template-columns: 1.1fr 1fr; gap: 0.4cm; }
  .rv .txtlist { margin: 0; padding-left: 0.6cm; font-size: 10.5pt; } .rv .txtlist li { margin-bottom: 0.06cm; }
  .rv .txtlist .l2 { margin-left: 0.6cm; list-style: circle; }
  .rv .sign { display: flex; justify-content: space-between; margin-top: 0.3cm; font-size: 10pt; }
  .sheet.poster.nm { padding: 1.8cm 1.8cm 1.5cm 1.8cm; }
  .sheet.poster.nm .wa { height: 3.6cm; }
  .sheet.poster.nm .sub { text-align: center; font-size: 17pt; font-style: italic; margin: 0.05cm 0 0.3cm 0; }
  .sheet.poster.nm .body p { text-indent: 1.25cm; margin-bottom: 0.08cm; }
  .sheet.poster.nm .pic { width: 6cm; }
  .sheet.poster.nm .pic .cap { text-align: center; font-size: 10pt; font-style: italic; text-indent: 0; margin-top: 0.1cm; }
  .sheet.poster.nm .nlab { position: absolute; top: 0.5cm; left: 1.8cm; font: 700 9pt Arial; color: #fff; background: #d6246e; padding: 0.06cm 0.3cm; border-radius: 3pt; letter-spacing: 0.05em; }
''' + POSTER_CSS


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8', newline='\n') as f:
        f.write(text)


def doc(sheets, title):
    return print_doc(sheets, title).replace('</style></head>', CSS + '</style></head>')


def head(code, tc, no):
    return ('<div class="info-top"><div><b>Tibbiyotda axborot texnologiyalari</b><br>Word amaliy ishi • tayyor material</div><span class="info-num" style="background:%s">%s</span></div>'
            '<div class="info-fio"><span>F.I.O.:</span><span>Guruh:</span><span>Sana:</span></div>' % (tc, no))


# ---------------------------------------------------------------------------
# 1. ANATOMIYA / XIRURGIYA: 35 variant + namuna
# ---------------------------------------------------------------------------
def variant_sheet(i, t):
    fan, mavzu, kw, intro, facts, know, cap = t
    tc = '#185abd' if fan == 'Anatomiya' else '#7a3fb5'
    chips = ''.join('<span>%s</span>' % esc(k) for k in kw)
    lis = ''.join('<li>%s</li>' % esc(f) for f in facts)
    return '''<div class="sheet info rv" style="--tc:%(tc)s">
  %(head)s
  <div class="band"><span class="tag">%(fan)s</span><span class="no">Variant № %(n)02d</span></div>
  <h1>%(mavzu)s</h1>
  <div class="box"><h2>1. Rasm toping</h2>
    <div class="kw">%(chips)s</div>
    <p>Internetdan qidiring (Google • Yandex • Wikipedia). Kerakli rasm: <b>qismlari nomi yozilgan (belgilangan) sxema</b>, sifati yaxshi, kamida 800 piksel. Rasmni <b>rasmlar</b> papkasiga «%(n)02d-%(low)s» nomi bilan saqlang.</p></div>
  <div class="box"><h2>2. Ma’lumot — shu matnni hujjatga yozing</h2>
    <p class="lead">%(intro)s</p>
    <ol>%(lis)s</ol></div>
  <div class="box"><h2>3. Hujjatga qo‘yiladigan tayyor yozuvlar</h2>
    <table class="rdy">
      <tr><td>Sarlavha (WordArt)</td><td class="big">%(up)s</td></tr>
      <tr><td>Rasm tagidagi yozuv</td><td>1-rasm. %(cap)s</td></tr>
      <tr><td>Izoh shakli ichida</td><td><b>Bilasizmi?</b> %(know)s</td></tr>
      <tr><td>Manba qatori</td><td>Manba: (rasm olingan saytning nomi)</td></tr>
    </table></div>
  <div class="box"><h2>Hujjat tarkibi (A4, bitta bet)</h2>
    <p>WordArt sarlavha • rasm (matn bilan o‘ralgan) • ma’lumot matni • «Bilasizmi?» izoh shakli • rasm tagidagi yozuv • manba.</p></div>
  <div class="sign"><span><b>Baho:</b> ______ / 5</span><span>O‘qituvchi imzosi: __________</span></div>
  <div class="info-foot"><span>%(tex)s</span><span>%(fan)s • Variant %(n)02d • %(mavzu)s</span></div>
</div>''' % dict(tc=tc, head=head('', tc, '%s • %02d' % (fan, i)), fan=fan, n=i, mavzu=esc(mavzu), chips=chips, low=esc(mavzu.lower().replace(' ', '-')),
                 intro=esc(intro), lis=lis, up=esc(mavzu.upper()), cap=esc(cap), know=esc(know), tex=TEX)


def namuna_sheet():
    N = NAMUNA
    war = wordart(N['title'], 'arch', '#ff8fb8', '#c2185b', '#6a0c35', uid='nm')
    paras = '<p>%s</p>' % esc(N['intro'])
    for i, f in enumerate(N['facts'], 1):
        paras += '<p>%d. %s</p>' % (i, esc(f))
    star = ('<svg viewBox="0 0 100 100"><polygon points="50,4 61,36 95,37 68,57 78,92 50,71 22,92 32,57 5,37 39,36" fill="#e9a420" stroke="rgba(0,0,0,0.35)" stroke-width="2"/></svg><span>!</span>')
    return '''<div class="sheet poster nm"><span class="nlab">NAMUNA — tayyor hujjat ko‘rinishi</span>
<div class="wa">%(war)s</div>
<div class="sub">%(sub)s</div>
<div class="body"><div class="pic st-1"><img src="%(img)s/%(pic)s" alt=""><div class="cap">%(cap)s</div></div>%(paras)s</div>
<div class="shp"><div class="callout" style="background:#c2185b;--cc:#c2185b">%(call)s</div><div class="star">%(star)s</div></div>
<p style="font:italic 10pt Arial;color:#666;margin-top:0.2cm;text-align:left;text-indent:0">%(src)s</p>
</div>''' % dict(war=war, sub=esc(N['subtitle']), img=IMG, pic=N['pic'], cap=esc(N['caption']), paras=paras, call=esc(N['callout']), star=star, src=esc(N['source']))


def build_anatomy():
    folder = os.path.join(PDF_DIR, 'anatomiya-farmakologiya')
    sheets = []
    ns = namuna_sheet()
    write(os.path.join(OUT_HTML, 'namuna.html'), doc([ns], 'Namuna'))
    n = to_pdf(os.path.join(OUT_HTML, 'namuna.html'), os.path.join(folder, 'namuna-wordart.pdf'))
    print('namuna-wordart', n, 'bet')
    allp = [ns]
    for i, t in enumerate(ANATOMIYA_XIRURGIYA, 1):
        sh = variant_sheet(i, t)
        allp.append(sh)
        nm = 'variant-%02d' % i
        write(os.path.join(OUT_HTML, nm + '.html'), doc([sh], nm))
        pg = to_pdf(os.path.join(OUT_HTML, nm + '.html'), os.path.join(folder, nm + '.pdf'))
        assert pg == 1, (nm, pg)
    write(os.path.join(OUT_HTML, 'anatomiya-farmakologiya.html'), doc(allp, '35 variant'))
    pg = to_pdf(os.path.join(OUT_HTML, 'anatomiya-farmakologiya.html'), os.path.join(PDF_DIR, 'anatomiya-farmakologiya-35-variant.pdf'))
    print('anatomiya-farmakologiya-35-variant', pg, 'bet (kutilgan 36)')
    assert pg == 36


# ---------------------------------------------------------------------------
# 2. SHAKLLAR: 6 tayyor rasm
# ---------------------------------------------------------------------------
FONT = 'font-family:Calibri,Arial,sans-serif'


def svg(inner, w=600, h=480):
    return '<svg viewBox="0 0 %d %d" width="15.5cm" style="%s">%s</svg>' % (w, h, FONT, inner)


def t(x, y, s, size=20, fill='#222', weight=700, anchor='middle'):
    return '<text x="%s" y="%s" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s" dominant-baseline="middle">%s</text>' % (x, y, size, weight, fill, anchor, s)


def sh_first_aid():
    b = '<rect x="40" y="40" width="400" height="260" rx="36" fill="#2e9e5b" stroke="#1b6b3b" stroke-width="5"/>'
    b += '<rect x="115" y="150" width="150" height="40" fill="#fff"/><rect x="170" y="95" width="40" height="150" fill="#fff"/>'
    b += t(360, 150, 'BIRINCHI', 28, '#fff') + t(360, 188, 'YORDAM', 28, '#fff') + t(360, 232, 'punkti', 20, '#d7f5e1', 600)
    b += '<circle cx="480" cy="70" r="56" fill="#d9534f" stroke="#8a1f1c" stroke-width="5"/>' + t(480, 70, '103', 36, '#fff')
    b += '<polygon points="60,350 360,350 360,328 440,378 360,428 360,406 60,406" fill="#2f6fd0" stroke="#1d4a96" stroke-width="4"/>' + t(205, 378, '2-qavat, 12-xona', 22, '#fff')
    return svg(b, 600, 460)
SH_FIRST_AID_LEG = [
    ('Yumaloq burchakli to‘rtburchak', '1', '#2e9e5b', '10 × 6,5 sm; kontur to‘q yashil, 3 pt'),
    ('Xoch (Cross)', '1', '#ffffff', '3,8 × 3,8 sm; yumaloq to‘rtburchak ustida, chapda'),
    ('Matn maydoni', '2', '—', '«BIRINCHI YORDAM» (qalin, 20 pt, oq), «punkti» (14 pt)'),
    ('Oval', '1', '#d9534f', '2,8 × 2,8 sm; ichida «103» (oq, qalin, 22 pt)'),
    ('O‘ng strelka (Right Arrow)', '1', '#2f6fd0', '7,5 × 2,4 sm; ichida «2-qavat, 12-xona» (oq, 14 pt)'),
]


def sh_dori():
    b = '<g transform="rotate(-28 190 150)"><path d="M90 115h100v70h-100a35 35 0 0 1 0-70z" fill="#d9534f" stroke="#7a1f1c" stroke-width="4"/>'
    b += '<path d="M190 115h100a35 35 0 0 1 0 70h-100z" fill="#fff" stroke="#7a1f1c" stroke-width="4"/></g>'
    for (x, y, c) in [(420, 90, '#ffd43b'), (500, 160, '#74c0fc'), (410, 190, '#b197fc')]:
        b += '<circle cx="%d" cy="%d" r="42" fill="%s" stroke="#444" stroke-width="3"/><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#444" stroke-width="3"/>' % (x, y, c, x - 36, y, x + 36, y)
    b += '<path d="M120 380 C70 330 100 270 150 270 C190 270 220 320 190 370 C175 395 145 400 120 380z" fill="#3ba0e6" stroke="#1d5f94" stroke-width="4" transform="rotate(-15 140 330)"/>'
    b += '<rect x="260" y="270" width="300" height="140" rx="12" fill="#e9ecef" stroke="#6c757d" stroke-width="4"/>'
    for r in range(2):
        for c in range(4):
            b += '<circle cx="%d" cy="%d" r="24" fill="%s" stroke="#6c757d" stroke-width="3"/>' % (310 + c * 65, 315 + r * 65, '#fff' if (r + c) % 3 else '#ffd43b')
    b += '<rect x="60" y="425" width="480" height="48" rx="12" fill="#f4c542" stroke="#9a7a0b" stroke-width="3"/>' + t(300, 449, 'Dori — faqat shifokor tavsiyasi bilan!', 22, '#3d2f00')
    return svg(b, 600, 500)
SH_DORI_LEG = [
    ('Bir tomoni yumaloq to‘rtburchak (Round Same Side Corner Rectangle)', '2', '#d9534f / #ffffff', '1 ta: 3,5 × 2 sm, ikkinchisi oq; yonma-yon qo‘ying — kapsula bo‘ladi'),
    ('Oval', '3 + 8', '#ffd43b • #74c0fc • #b197fc', '3 ta tabletka (3 × 3 sm) + blisterdagi 8 ta (1,6 sm); tabletka ustida chiziq'),
    ('Ko‘z yoshi (Teardrop)', '1', '#3ba0e6', '3 × 3 sm, aylantirilgan — tomchi'),
    ('To‘rtburchak (yumaloq)', '2', '#e9ecef • #f4c542', 'Blister 8 × 3,6 sm; pastdagi lenta 12,5 × 1,2 sm, ichida yozuv'),
]


def sh_odam():
    b = '<circle cx="300" cy="70" r="42" fill="#f6c9a5" stroke="#b9855d" stroke-width="4"/>'
    b += '<rect x="185" y="125" width="34" height="175" rx="17" fill="#f6c9a5" stroke="#b9855d" stroke-width="4"/><rect x="381" y="125" width="34" height="175" rx="17" fill="#f6c9a5" stroke="#b9855d" stroke-width="4"/>'
    b += '<rect x="225" y="120" width="150" height="195" rx="32" fill="#a5d8ff" stroke="#3b82b8" stroke-width="4"/>'
    b += '<rect x="235" y="305" width="60" height="170" rx="26" fill="#6c8ebf" stroke="#3a587f" stroke-width="4"/><rect x="305" y="305" width="60" height="170" rx="26" fill="#6c8ebf" stroke="#3a587f" stroke-width="4"/>'
    b += '<ellipse cx="268" cy="188" rx="26" ry="40" fill="#ffb4c1" stroke="#c9677a" stroke-width="3"/><ellipse cx="332" cy="188" rx="26" ry="40" fill="#ffb4c1" stroke="#c9677a" stroke-width="3"/>'
    b += '<path d="M315 238 C290 222 290 200 308 200 C316 200 318 208 318 208 C318 208 322 200 330 200 C348 200 346 222 322 238z" fill="#d9253a" stroke="#7a0f1c" stroke-width="3"/>'
    b += '<polygon points="236,262 296,262 288,286 244,286" fill="#8b5a2b" stroke="#4a2f14" stroke-width="3"/><ellipse cx="342" cy="270" rx="24" ry="16" fill="#f59f00" stroke="#9a5f00" stroke-width="3"/>'
    for (bx, by, lab, tx, ty) in [(30, 110, 'O‘pka', 244, 188), (30, 215, 'Jigar', 240, 272), (460, 150, 'Yurak', 324, 218), (460, 255, 'Oshqozon', 348, 270)]:
        b += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#444" stroke-width="3"/>' % (bx + (110 if bx < 300 else 0), by + 20, tx, ty)
        b += '<rect x="%d" y="%d" width="110" height="40" rx="8" fill="#fff" stroke="#444" stroke-width="3"/>' % (bx, by) + t(bx + 55, by + 20, lab, 19)
    return svg(b, 600, 500)
SH_ODAM_LEG = [
    ('Oval', '1 + 3', 'teri rangi • pushti • to‘q sariq', 'Bosh 2,8 × 2,8 sm; ikki o‘pka 1,8 × 2,8 sm; oshqozon 1,7 × 1,1 sm'),
    ('Yumaloq burchakli to‘rtburchak', '5', '#a5d8ff • #f6c9a5 • #6c8ebf', 'Tana 5 × 6,5 sm; 2 qo‘l 1,2 × 6 sm; 2 oyoq 2 × 5,7 sm'),
    ('Yurak (Heart)', '1', '#d9253a', '1,8 × 1,6 sm; o‘pkalar orasida, o‘rtadan sal o‘ngda'),
    ('Trapetsiya', '1', '#8b5a2b', 'Jigar: 2 × 0,8 sm, rasmda chap tomonda (bemorning o‘ng tomoni)'),
    ('Chiziqli izoh (Callout: Line)', '4', '#ffffff', 'O‘pka, Jigar, Yurak, Oshqozon — 3,6 × 1,3 sm, 14 pt, chiziq organga qaratilgan'),
]


def sh_palata():
    b = '<rect x="30" y="30" width="540" height="400" fill="#fffdf5" stroke="#3a3a3a" stroke-width="9"/>'
    b += '<rect x="210" y="22" width="180" height="16" fill="#a5d8ff" stroke="#3b82b8" stroke-width="3"/>' + t(300, 56, 'Deraza', 14, '#3b82b8', 600)
    b += '<path d="M70 430 L70 360 A70 70 0 0 1 140 430z" fill="#ffe8cc" stroke="#9a5f00" stroke-width="3"/>' + t(110, 408, 'Eshik', 14, '#7a4a00', 600)
    for k, y in enumerate([80, 170]):
        b += '<rect x="45" y="%d" width="130" height="62" fill="#fff" stroke="#444" stroke-width="3"/><rect x="48" y="%d" width="30" height="56" rx="10" fill="#74c0fc" stroke="#2b7bb9" stroke-width="2"/>' % (y, y + 3)
        b += '<rect x="425" y="%d" width="130" height="62" fill="#fff" stroke="#444" stroke-width="3"/><rect x="522" y="%d" width="30" height="56" rx="10" fill="#74c0fc" stroke="#2b7bb9" stroke-width="2"/>' % (y, y + 3)
        b += '<rect x="180" y="%d" width="30" height="30" fill="#e9ecef" stroke="#444" stroke-width="2"/><rect x="390" y="%d" width="30" height="30" fill="#e9ecef" stroke="#444" stroke-width="2"/>' % (y + 16, y + 16)
    b += t(300, 215, 'Palata № 5', 30, '#222') + t(300, 250, '4 o‘rinli', 20, '#555', 600)
    b += '<rect x="440" y="340" width="110" height="64" rx="10" fill="#d0ebff" stroke="#3b82b8" stroke-width="3"/>' + t(495, 372, 'Qo‘l yuvish', 15, '#1d5f94', 600)
    return svg(b, 600, 450)
SH_PALATA_LEG = [
    ('To‘rtburchak', '1 + 4 + 2', '#fffdf5 • #ffffff • #e9ecef', 'Xona 17 × 12 sm (kontur 7 pt); 4 karavot 3,9 × 1,9 sm; 4 tumbochka 0,9 × 0,9 sm'),
    ('Yumaloq burchakli to‘rtburchak', '4 + 1', '#74c0fc • #d0ebff', '4 ta yostiq 0,9 × 1,7 sm; 1 ta qo‘l yuvish joyi 3,3 × 1,9 sm'),
    ('To‘rtburchak (deraza)', '1', '#a5d8ff', '5,5 × 0,5 sm, yuqori devorda'),
    ('Chorak aylana (Arc / Pie)', '1', '#ffe8cc', 'Eshik: 2 × 2 sm, pastki chap burchakda'),
    ('Matn maydoni', '4', '—', '«Palata № 5» (qalin, 20 pt), «4 o‘rinli», «Deraza», «Eshik»'),
]


def sh_qon():
    def arrow(x1, y1, x2, y2, c):
        return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="14"/><polygon points="%s" fill="%s"/>' % (x1, y1, x2, y2, c, _head(x1, y1, x2, y2), c)

    def _head(x1, y1, x2, y2):
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        p = [(x2 + 28 * math.cos(a), y2 + 28 * math.sin(a)), (x2 + 22 * math.cos(a + 2.2), y2 + 22 * math.sin(a + 2.2)), (x2 + 22 * math.cos(a - 2.2), y2 + 22 * math.sin(a - 2.2))]
        return ' '.join('%.0f,%.0f' % q for q in p)
    b = '<ellipse cx="300" cy="80" rx="105" ry="52" fill="#ffb4c1" stroke="#c9677a" stroke-width="4"/>' + t(300, 80, 'O‘pka', 24)
    b += '<ellipse cx="300" cy="500" rx="140" ry="48" fill="#ffd8a8" stroke="#c77a1a" stroke-width="4"/>' + t(300, 500, 'A’zolar va to‘qimalar', 22)
    b += '<path d="M300 400 C190 330 215 255 300 305 C385 255 410 330 300 400z" fill="#d9253a" stroke="#7a0f1c" stroke-width="4" transform="translate(0 -20) scale(1)"/>' + t(300, 300, 'Yurak', 22, '#fff')
    b += arrow(255, 255, 235, 150, '#2f6fd0') + arrow(375, 150, 350, 255, '#d9253a')
    b += arrow(355, 395, 385, 455, '#d9253a') + arrow(215, 455, 245, 395, '#2f6fd0')
    b += t(110, 200, 'Kichik doira', 20, '#2f6fd0') + t(110, 225, '(o‘pka orqali)', 15, '#555', 600)
    b += t(500, 430, 'Katta doira', 20, '#d9253a') + t(500, 455, '(butun tana)', 15, '#555', 600)
    b += '<rect x="30" y="300" width="14" height="14" fill="#d9253a"/>' + t(52, 307, 'kislorodli qon', 14, '#333', 600, 'start')
    b += '<rect x="30" y="325" width="14" height="14" fill="#2f6fd0"/>' + t(52, 332, 'kislorodi kam qon', 14, '#333', 600, 'start')
    return svg(b, 600, 560)
SH_QON_LEG = [
    ('Yurak (Heart)', '1', '#d9253a', '4,5 × 4 sm, markazda; ichida «Yurak» (oq, qalin)'),
    ('Oval', '2', '#ffb4c1 • #ffd8a8', 'O‘pka 5,5 × 2,6 sm (tepada); A’zolar va to‘qimalar 7 × 2,4 sm (pastda)'),
    ('Strelka (Up / Down Arrow, aylantirilgan)', '4', '#2f6fd0 (2 ta) • #d9253a (2 ta)', 'Uzunligi ~3 sm; ko‘k — kislorodi kam qon, qizil — kislorodli qon'),
    ('Matn maydoni', '4', '—', '«Kichik doira», «Katta doira» + ostida izoh (kichik harf); «kislorodli / kislorodi kam qon» yozuvlari'),
    ('Kvadrat', '2', '#d9253a • #2f6fd0', '0,5 × 0,5 sm — belgilar (legenda) uchun'),
]


def sh_belgilar():
    b = '<polygon points="150,30 270,240 30,240" fill="#ffd43b" stroke="#222" stroke-width="10" stroke-linejoin="round"/>' + t(150, 190, '!', 90, '#222', 900)
    b += t(150, 275, 'Diqqat!', 22)
    b += '<circle cx="450" cy="135" r="95" fill="#fff" stroke="#d9253a" stroke-width="22"/><rect x="395" y="115" width="110" height="22" fill="#444"/><rect x="480" y="115" width="25" height="22" fill="#f59f00"/><line x1="385" y1="215" x2="515" y2="55" stroke="#d9253a" stroke-width="22"/>'
    b += t(450, 275, 'Chekish taqiqlanadi', 21)
    b += '<rect x="55" y="320" width="190" height="190" rx="28" fill="#2f6fd0" stroke="#1d4a96" stroke-width="6"/>' + t(150, 415, 'i', 130, '#fff', 900)
    b += t(150, 535, 'Axborot', 22)
    b += '<polygon points="390,320 510,320 570,380 570,450 510,510 390,510 330,450 330,380" fill="#d9253a" stroke="#7a1f1c" stroke-width="6"/>' + t(450, 415, 'STOP', 42, '#fff', 900)
    b += t(450, 535, 'Kirish mumkin emas', 21)
    return svg(b, 600, 570)
SH_BELGI_LEG = [
    ('Teng yonli uchburchak (Isosceles Triangle)', '1', '#ffd43b', '5,5 × 5 sm; kontur qora, 4 pt; ichida «!» (qalin, 48 pt)'),
    ('«Taqiq» belgisi (No Symbol)', '1', '#d9253a', '4,5 × 4,5 sm; ichida kichik to‘rtburchaklardan «sigareta»'),
    ('Yumaloq burchakli to‘rtburchak', '1', '#2f6fd0', '4,8 × 4,8 sm; ichida «i» (oq, qalin, 66 pt)'),
    ('Sakkizburchak (Octagon)', '1', '#d9253a', '5 × 5 sm; ichida «STOP» (oq, qalin, 28 pt)'),
    ('Matn maydoni', '4', '—', 'Belgilar ostida: Diqqat! • Chekish taqiqlanadi • Axborot • Kirish mumkin emas (14 pt)'),
]

SHAKLLAR = [
    ('Birinchi yordam punkti belgisi', 'Poliklinika koridori uchun yo‘naltiruvchi belgi.', sh_first_aid, SH_FIRST_AID_LEG, '#2e9e5b'),
    ('Dori vositalari plakati', 'Dorixona vitrinasi uchun tabletka, kapsula va tomchi tasviri.', sh_dori, SH_DORI_LEG, '#7a5cc7'),
    ('Ichki a’zolar joylashuvi sxemasi', 'Anatomiya xonasi uchun odam silueti va asosiy a’zolar.', sh_odam, SH_ODAM_LEG, '#2f6fd0'),
    ('Kasalxona palatasi rejasi', 'Bo‘lim ko‘rsatkichi: 4 o‘rinli palataning rejasi.', sh_palata, SH_PALATA_LEG, '#e8890c'),
    ('Qon aylanishi sxemasi', 'Katta va kichik qon aylanish doiralarining soddalashtirilgan sxemasi.', sh_qon, SH_QON_LEG, '#d6246e'),
    ('Kasalxonadagi xavfsizlik belgilari', 'To‘rtta ogohlantiruvchi va axborot belgisi.', sh_belgilar, SH_BELGI_LEG, '#2a9d8f'),
]


def shape_sheet(i, spec):
    title, about, fn, leg, tc = spec
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        a, n, ('—' if c == '—' else ''.join('<span class="sw" style="background:%s"></span>' % x.strip() for x in c.replace('•', '/').split('/') if x.strip().startswith('#')) + ('' if all(x.strip().startswith('#') for x in c.replace('•', '/').split('/')) else c)), d) for a, n, c, d in leg)
    return '''<div class="sheet info rv" style="--tc:%(tc)s">
  %(head)s
  <div class="band"><span class="tag">Shakllar</span><span class="no">Variant № %(i)d</span></div>
  <h1 style="font-size:20pt">%(title)s</h1>
  <p style="margin:0 0 0.15cm 0">%(about)s Pastdagi tayyor rasmni Word’da <b>faqat shakllardan</b> (Qo‘shish › Shakllar) yig‘ing. Hammasi bitta A4 betga sig‘sin, shakllarni <b>guruhlang</b>.</p>
  <div class="fig">%(fig)s</div>
  <table class="leg"><thead><tr><th>Shakl</th><th>Soni</th><th>Rangi</th><th>O‘lcham va matn</th></tr></thead><tbody>%(rows)s</tbody></table>
  <div class="sign"><span>Fayl: <b>Familiya_Shakl%(i)d.docx</b></span><span><b>Baho:</b> ______ / 5 &nbsp; O‘qituvchi imzosi: __________</span></div>
  <div class="info-foot"><span>%(tex)s</span><span>Shakllar • Variant %(i)d</span></div>
</div>''' % dict(tc=tc, head=head('', tc, 'Shakllar • %d' % i), i=i, title=title, about=about, fig=fn(), rows=rows, tex=TEX)


def build_shapes():
    folder = os.path.join(PDF_DIR, 'shakllar')
    allp = []
    for i, spec in enumerate(SHAKLLAR, 1):
        sh = shape_sheet(i, spec)
        allp.append(sh)
        nm = 'variant-%d' % i
        write(os.path.join(OUT_HTML, 'shakl-' + nm + '.html'), doc([sh], nm))
        assert to_pdf(os.path.join(OUT_HTML, 'shakl-' + nm + '.html'), os.path.join(folder, nm + '.pdf')) == 1, nm
    write(os.path.join(OUT_HTML, 'shakllar.html'), doc(allp, 'Shakllar'))
    pg = to_pdf(os.path.join(OUT_HTML, 'shakllar.html'), os.path.join(PDF_DIR, 'shakllar-6-variant.pdf'))
    print('shakllar-6-variant', pg, 'bet'); assert pg == 6


# ---------------------------------------------------------------------------
# 3. KOLONTITUL: 6 tayyor hujjat (avtomatik sahifa raqami)
# ---------------------------------------------------------------------------
DATE = '01.11.2026'

KOL = [
    dict(title='Referat: titul varag‘i va sahifa raqami', about='6 betli referat. Titul varag‘ida kolontitul va raqam yo‘q, 2-betdan boshlab bor.', tc='#d6246e',
         pages=[dict(label='1-bet (titul)', titul=True),
                dict(label='2-bet', h=dict(c='Qo‘l gigiyenasi'), f=dict(r='2'), it=True),
                dict(label='3-bet', h=dict(c='Qo‘l gigiyenasi'), f=dict(r='3'), it=True),
                ],
         text=[('Yuqori kolontitul', 'Qo‘l gigiyenasi  (markazda, kursiv)'), ('Pastki kolontitul', 'sahifa raqami (o‘ngda)')],
         rows=[('Hujjat hajmi', '6 bet'), ('Birinchi sahifa', 'alohida: titulda kolontitul va raqam yo‘q'), ('Toq / juft betlar', 'bir xil'),
               ('Raqam', 'o‘ngda; 2-betda «2» (titul hisobga olinadi)'), ('Shrift', 'Times New Roman, 10 pt'), ('Raqam turi', 'Sahifaning pastki qismi › Oddiy raqam 3')], rand='=rand(12,6)'),
    dict(title='Bemor kuzatuv varaqasi: «Sahifa X dan Y»', about='4 betli hujjat. Hamma betda bir xil kolontitul, sana avtomatik yangilanadi.', tc='#2f6fd0',
         pages=[dict(label='1-bet', h=dict(l='Tibbiyot texnikumi', r=DATE), f=dict(c='Sahifa 1 dan 4'), hline=True),
                dict(label='2-bet', h=dict(l='Tibbiyot texnikumi', r=DATE), f=dict(c='Sahifa 2 dan 4'), hline=True),
                dict(label='3-bet', h=dict(l='Tibbiyot texnikumi', r=DATE), f=dict(c='Sahifa 3 dan 4'), hline=True),
                ],
         text=[('Yuqori kolontitul', 'chapda «Tibbiyot texnikumi»; o‘ngda bugungi sana (avtomatik); ostida chiziq'), ('Pastki kolontitul', 'markazda «Sahifa X dan Y»')],
         rows=[('Hujjat hajmi', '4 bet'), ('Birinchi sahifa', 'boshqalar bilan bir xil'), ('Toq / juft betlar', 'bir xil'),
               ('Sana', 'Konstruktor › Sana va vaqt › «Avtomatik yangilash»'), ('Shrift', 'Times New Roman, 10 pt'), ('Raqam turi', 'Sahifa raqami › «Sahifa X / Y» turi')], rand='=rand(8,6)'),
    dict(title='Yillik hisobot: toq va juft betlar', about='8 betli hisobot. Toq va juft betlarda kolontitul va raqam turli tomonda.', tc='#e8890c',
         pages=[dict(label='1-bet (titul)', titul=True),
                dict(label='2-bet (juft)', h=dict(l='Shahrisabz Tibbiyot Texnikumi'), f=dict(l='2')),
                dict(label='3-bet (toq)', h=dict(r='Davolash bo‘limi hisoboti'), f=dict(r='3')),
                ],
         text=[('Toq betlar: yuqori', 'Davolash bo‘limi hisoboti  (o‘ngda)'), ('Juft betlar: yuqori', 'Shahrisabz Tibbiyot Texnikumi  (chapda)'), ('Raqam', 'toq betda pastda o‘ngda, juft betda pastda chapda')],
         rows=[('Hujjat hajmi', '8 bet'), ('Birinchi sahifa', 'alohida (titul)'), ('Toq / juft betlar', '<b>har xil</b>: Konstruktor › Toq va juft sahifalar uchun har xil'),
               ('Raqam', 'tashqi chetda'), ('Shrift', 'Times New Roman, 10 pt'), ('Raqam turi', 'Oddiy raqam 1 (toq) va Oddiy raqam 3 (juft)')], rand='=rand(14,6)'),
    dict(title='Yo‘riqnoma: birinchi bet alohida', about='5 betli yo‘riqnoma. Birinchi betda katta sarlavha kolontituli, keyingi betlarda oddiy kolontitul va «— X —» raqam.', tc='#7a5cc7',
         pages=[dict(label='1-bet', hbig='YO‘RIQNOMA № 3'),
                dict(label='2-bet', h=dict(l='Yo‘riqnoma № 3'), f=dict(c='— 2 —'), hline=True),
                dict(label='3-bet', h=dict(l='Yo‘riqnoma № 3'), f=dict(c='— 3 —'), hline=True),
                ],
         text=[('1-bet yuqori kolontituli', 'YO‘RIQNOMA № 3  (markazda, qalin, 14 pt)'), ('Qolgan betlarda yuqori', 'Yo‘riqnoma № 3  (chapda, chiziq bilan)'), ('Qolgan betlarda pastki', '— X —  (markazda)')],
         rows=[('Hujjat hajmi', '5 bet'), ('Birinchi sahifa', '<b>alohida</b> kolontitul (pastki qismi bo‘sh)'), ('Toq / juft betlar', 'bir xil'),
               ('Raqam', 'markazda: raqam atrofiga «—» yoziladi, raqam maydon bo‘lib qoladi'), ('Shrift', 'Times New Roman, 10 pt'), ('Raqam turi', 'Oddiy raqam 2')], rand='=rand(10,6)'),
    dict(title='Kurs ishi: ikki bo‘lim, rim va arab raqamlari', about='Titul va mundarija — 1-bo‘lim (rim raqamlari), asosiy qism — 2-bo‘lim (1 dan boshlanadi).', tc='#2e9e5b',
         pages=[dict(label='1-bet: titul', titul=True),
                dict(label='2-bet: mundarija', h=dict(c='Mundarija'), f=dict(c='II')),
                dict(label='3-bet: asosiy qism', h=dict(c='Asosiy qism'), f=dict(c='1')),
                ],
         text=[('1-bo‘lim: yuqori', 'Mundarija  (markazda)'), ('1-bo‘lim: pastki', 'rim raqami (II, III…)'), ('2-bo‘lim: yuqori', 'Asosiy qism  (markazda)'), ('2-bo‘lim: pastki', 'arab raqami, <b>1 dan</b> boshlanadi')],
         rows=[('Hujjat hajmi', '6 bet'), ('Bo‘limlar', '2 ta: 3-bet boshida Maket › Uzilishlar › Keyingi sahifa'), ('Birinchi sahifa', 'alohida (titul)'),
               ('2-bo‘lim kolontituli', '«Oldingi bilan bog‘lash» <b>o‘chirilgan</b>'), ('Raqam formati', '1-bo‘lim: I, II, III; 2-bo‘lim: 1, 2, 3 — Sahifa raqami › Sahifa raqami formati › Boshlash'), ('Shrift', 'Times New Roman, 10 pt')], rand='=rand(12,6)'),
    dict(title='Kasallik tarixi: maxfiy hujjat kolontituli', about='5 betli hujjat. Yuqorida bemor va karta raqami, pastda «MAXFIY» va sahifa raqami.', tc='#c0392b',
         pages=[dict(label='1-bet', h=dict(l='Karimov A.A.', r='Karta № 1254'), f=dict(l='MAXFIY', r='1 / 5'), hline=True, fline=True),
                dict(label='2-bet', h=dict(l='Karimov A.A.', r='Karta № 1254'), f=dict(l='MAXFIY', r='2 / 5'), hline=True, fline=True),
                dict(label='3-bet', h=dict(l='Karimov A.A.', r='Karta № 1254'), f=dict(l='MAXFIY', r='3 / 5'), hline=True, fline=True),
                ],
         text=[('Yuqori kolontitul', 'chapda «Karimov A.A.»; o‘ngda «Karta № 1254»; ostida chiziq'), ('Pastki kolontitul', 'chapda «MAXFIY» (qizil, qalin); o‘ngda «X / Y» (ikkalasi maydon); ustida chiziq')],
         rows=[('Hujjat hajmi', '5 bet'), ('Birinchi sahifa', 'boshqalar bilan bir xil'), ('Toq / juft betlar', 'bir xil'),
               ('Chiziqlar', 'yuqorida — pastki chegara, pastda — yuqori chegara (Bosh sahifa › Chegaralar)'), ('Shrift', 'Times New Roman, 10 pt'), ('Raqam turi', 'Qo‘shish › Tezkor bloklar › Maydon › Page va NumPages')], rand='=rand(10,6)'),
]


def kol_sheet(i, K):
    tc = K['tc']
    texts = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (a, b) for a, b in K['text'])
    rows = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (a, b) for a, b in K['rows'])
    return '''<div class="sheet info rv" style="--tc:%(tc)s">
  %(head)s
  <div class="band"><span class="tag">Kolontitul</span><span class="no">Variant № %(i)d</span></div>
  <h1 style="font-size:20pt">%(title)s</h1>
  <p style="margin:0 0 0.1cm 0">%(about)s Pastdagi tayyor ko‘rinishni Word’da <b>kolontitul</b> va <b>avtomatik sahifa raqami</b> bilan yarating (Qo‘shish › Yuqori kolontitul / Pastki kolontitul / Sahifa raqami).
     Matn uchun yangi hujjatda <b>%(rand)s</b> yozib <b>Enter</b> bosing (rus tilidagi Wordda <b>=рэнд(…)</b>): Word tayyor matn yaratadi.</p>
  <div class="fig" style="padding:0.2cm"><div style="width:16.4cm;margin:0 auto">%(fig)s</div></div>
  <div class="cols">
    <div class="box"><h2>Kolontitulga yoziladigan matn</h2><table class="rdy">%(texts)s</table></div>
    <div class="box"><h2>Sozlamalar</h2><table class="rdy">%(rows)s</table></div>
  </div>
  <div class="sign"><span>Fayl: <b>Familiya_Kolontitul%(i)d.docx</b></span><span><b>Baho:</b> ______ / 5 &nbsp; O‘qituvchi imzosi: __________</span></div>
  <div class="info-foot"><span>%(tex)s</span><span>Kolontitul • Variant %(i)d</span></div>
</div>''' % dict(tc=tc, head=head('', tc, 'Kolontitul • %d' % i), i=i, title=K['title'], about=K['about'], rand=K['rand'], fig=kol_pages(K['pages']),
                 texts=texts, rows=rows, tex=TEX)


def build_kol():
    folder = os.path.join(PDF_DIR, 'kolontitul')
    allp = []
    for i, K in enumerate(KOL, 1):
        sh = kol_sheet(i, K)
        allp.append(sh)
        nm = 'variant-%d' % i
        write(os.path.join(OUT_HTML, 'kol-' + nm + '.html'), doc([sh], nm))
        assert to_pdf(os.path.join(OUT_HTML, 'kol-' + nm + '.html'), os.path.join(folder, nm + '.pdf')) == 1, nm
    write(os.path.join(OUT_HTML, 'kolontitul.html'), doc(allp, 'Kolontitul'))
    pg = to_pdf(os.path.join(OUT_HTML, 'kolontitul.html'), os.path.join(PDF_DIR, 'kolontitul-6-variant.pdf'))
    print('kolontitul-6-variant', pg, 'bet')
    assert pg == 6


def main():
    for d in ('anatomiya-farmakologiya', 'shakllar', 'kolontitul'):
        os.makedirs(os.path.join(PDF_DIR, d), exist_ok=True)
    build_anatomy()
    build_shapes()
    build_kol()


if __name__ == '__main__':
    main()
