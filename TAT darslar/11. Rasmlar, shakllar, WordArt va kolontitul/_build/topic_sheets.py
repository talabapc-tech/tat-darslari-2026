# -*- coding: utf-8 -*-
"""
Mavzu bo'yicha alohida tarqatma varaqlar (8 ta) va o'qituvchi kaliti.

Ishga tushirish (shu papkada):  python topic_sheets.py
Natija (../tarqatma/mavzu-varaqlari/):
  1-rasm-A.pdf ... 4-wordart-B.pdf   — talabaga: bitta A4 varoq (topshiriq, baholash, yozma savollar)
  barcha-mavzu-varaqlari.pdf          — 8 varoq bitta faylda (chop etish uchun)
  kalit-oqituvchi.pdf                 — o'qituvchiga: kutilgan natija, savollar javobi, tekshirish
"""
import math
import os

from handouts import SHEET_CSS, EXTRA_CSS, kc, print_doc, to_pdf
from svgs import PALETTES, kol_pages, smartart, wordart
from topics import GRADES20, TOPICS, check

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_HTML = os.path.join(HERE, 'out')
PDF_DIR = os.path.join(ROOT, 'tarqatma', 'mavzu-varaqlari')
IMG = '../../tarqatma/rasmlar'
TEXNIKUM = 'Shahrisabz Tibbiyot Texnikumi'

TOPIC_CSS = '''
  .sheet.tp { font-size: 8.9pt; line-height: 1.3; padding: 1.2cm 1.5cm 1.1cm 1.5cm; }
  .tp .info-fio { margin: 0.18cm 0 0.2cm 0; }
  .tp h1 { font-size: 13.5pt; margin: 0 0 0.12cm 0; }
  .tp .scn { background: #f1f6fd; border-left: 3pt solid var(--tc); padding: 0.14cm 0.26cm; margin-bottom: 0.14cm; font-size: 9pt; }
  .tp .txt { border: 0.75pt dashed #9fb4d6; padding: 0.1cm 0.26cm; margin-bottom: 0.14cm; font-size: 8.7pt; }
  .tp .txt ol { margin: 0; padding-left: 0.5cm; } .tp .txt li { margin-bottom: 0.03cm; }
  .tp .txt .tl { font-weight: 700; color: #185abd; font-size: 8pt; text-transform: uppercase; letter-spacing: 0.04em; }
  .tp table.crit td { padding: 1.5pt 4pt; font-size: 8.6pt; }
  .tp table.crit .pth { display: block; color: #6b7a90; font-size: 7.6pt; margin-top: 0.5pt; }
  .tp table.crit th { background: var(--tc); border-color: var(--tc); }
  .tp table.crit td.cn { color: var(--tc); }
  .tp .qs { margin: 0; padding-left: 0.55cm; } .tp .qs li { margin-bottom: 0.05cm; }
  .tp .qs .ln { border-bottom: 0.6pt solid #888; height: 0.42cm; margin-top: 0.02cm; }
  .tp .info-top, .tp .info-num { } .tp .info-num { background: var(--tc); }
  .tp .info-top { border-bottom-color: var(--tc); } .tp .info-top b { color: var(--tc); }
  .tp h2 { color: var(--tc); margin: 0.2cm 0 0.08cm 0; font-size: 9.6pt; }
  .tp .info-sign { margin-top: 0.15cm; font-size: 9.5pt; }
  .tp.key { padding-top: 1.1cm; }
  .tp .fig { background: #f4f6fa; border: 0.75pt solid #d4dbe8; border-radius: 3pt; padding: 0.25cm; margin: 0.12cm 0; text-align: center; }
  .tp .fig svg { max-width: 100%; }
  .tp .mockbox { position: relative; overflow: hidden; margin: 0 auto; background: #fff; box-shadow: 0 0 0 0.75pt #bbb; }
  .tp .mock { position: absolute; left: 0; top: 0; width: 21cm; height: 29.7cm; transform-origin: top left; transform: scale(0.5);
    font-family: "Times New Roman", serif; font-size: 12pt; line-height: 1.25; padding: 2cm; text-align: justify; background: #fff; text-align: left; }
  .tp .mock p { margin: 0; text-align: justify; text-indent: 1.25cm; }
  .tp .mock .cap { text-indent: 0; text-align: center; font-size: 10pt; font-style: italic; }
  .tp .ak li { margin-bottom: 0.06cm; }
  .tp .hint { background: #fff8e1; border-left: 3pt solid #e9a420; padding: 0.12cm 0.25cm; font-size: 8.8pt; margin-top: 0.12cm; }
'''


def student_sheet(T, S):
    rows = ''.join('<tr><td class="cn">%d</td><td>%s<span class="pth">%s</span></td><td class="cb">%d</td><td class="cg"></td></tr>'
                   % (i + 1, kc(r[0]), r[1], r[2]) for i, r in enumerate(S['rows']))
    txt = ''
    if S['text']:
        txt = '<div class="txt"><div class="tl">Berilgan ma’lumot</div><ol>%s</ol></div>' % ''.join('<li>%s</li>' % t for t in S['text'])
    qs = ''.join('<li>%s<div class="ln"></div><div class="ln"></div></li>' % q for q in S['qs'])
    grades = '; '.join('%s → %s' % (a, b.split()[0]) for a, b in GRADES20)
    return '''<div class="sheet info tp" style="--tc:%(c)s">
  <div class="info-top"><div><b>Tibbiyotda axborot texnologiyalari</b><br>Word 3-dars • mavzu varog‘i: <b>%(name)s</b></div><span class="info-num">%(n)d-%(name)s • %(v)s</span></div>
  <div class="info-fio"><span>F.I.O.:</span><span>Guruh:</span><span>Sana:</span></div>
  <h1>%(title)s</h1>
  <div class="scn"><b>Vaziyat:</b> %(scn)s</div>
  %(txt)s
  <h2>Topshiriq va baholash (20 ball)</h2>
  <table class="crit"><thead><tr><th>№</th><th>Talab va qayerda bajariladi</th><th>Maks.</th><th>Ball</th></tr></thead><tbody>%(rows)s
  <tr class="tot"><td></td><td>Jami</td><td class="cb">20</td><td class="cg"></td></tr></tbody></table>
  <h2>Yozma savollar (qisqa javob bering)</h2>
  <ol class="qs">%(qs)s</ol>
  <div class="info-sign"><span><b>Baho:</b> ______ <span class="gr">(%(grades)s)</span></span><span>O‘qituvchi imzosi: __________</span></div>
  <div class="info-foot"><span>%(tex)s</span><span>Mavzu varog‘i: %(name)s • %(v)s</span></div>
</div>''' % dict(c=T['color'], name=T['name'], n=T['n'], v=S['v'], title=S['title'], scn=kc(S['scenario']), txt=txt, rows=rows, qs=qs, grades=grades, tex=TEXNIKUM)


# ----------------------------------------------------------------------------
# KUTILGAN NATIJA RASMLARI
# ----------------------------------------------------------------------------
def mockbox(inner, scale=0.66, crop=19.5):
    w, h = 21 * scale, crop * scale
    return '<div class="mockbox" style="width:%.2fcm;height:%.2fcm"><div class="mock" style="transform:scale(%.3f)">%s</div></div>' % (w, h, scale, inner)


def img(name, w, extra=''):
    return '<img src="%s/%s" style="width:%scm;%s" alt="">' % (IMG, name, w, extra)


def fig_rasm(S, v):
    t = S['text']
    wm = '<img src="%s/%s" style="position:absolute;left:4.5cm;top:9cm;width:%scm;opacity:0.18;filter:grayscale(1)" alt="">' % (IMG, 'kasalxona.png' if v == 'A' else 'dori-vositalari.png', 12 if v == 'A' else 11)
    if v == 'A':
        body = ('<p>%s</p>' % t[0]).replace('<p>', '<p>' + img('qol-yuvish.png', 6, 'float:left;margin:0 0.4cm 0.2cm 0;border:6px solid #fff;box-shadow:0 0 0 1px #bbb,0 1px 4px #0005') + '', 1)
        body += ('<p>%s</p>' % t[1]).replace('<p>', '<p>' + img('stetoskop.png', 4.5, 'float:right;margin:0 0 0.2cm 0.4cm;border:3px solid #1f3a73;transform:rotate(5deg);aspect-ratio:1/1;object-fit:cover'), 1)
        body += '<p>%s</p>' % t[2]
        body += '<div style="clear:both;text-align:center;margin-top:0.3cm">%s<div class="cap" style="text-indent:0">1-rasm. Qo‘l yuvish • 2-rasm. Fonendoskop • 3-rasm. Tonometr</div></div>' % img('tonometr.png', 9, 'filter:brightness(1.2)')
    else:
        body = ('<p>%s</p>' % t[0]).replace('<p>', '<p>' + img('mikrob.png', 7, 'float:right;margin:0 0 0.2cm 0.4cm;box-shadow:5px 6px 8px #0006'), 1)
        body += ('<p>%s</p>' % t[1]).replace('<p>', '<p>' + img('ovqatlanish.png', 5, 'float:left;margin:0 0.4cm 0.2cm 0;border-radius:50%;aspect-ratio:1/1;object-fit:cover;border:3px solid #2e9e5b'), 1)
        body += '<p>%s</p>' % t[2]
        body += '<div style="clear:both;text-align:center;margin-top:0.3cm">%s<div class="cap" style="text-indent:0">1-rasm. Mikroblar • 2-rasm. Ovqatlanish • 3-rasm. Stetoskop</div></div>' % img('stetoskop.png', 8)
    return mockbox(wm + body)


FLOW = {
    'A': dict(nodes=[
        ('t', 'Bemor murojaati', 170, 25, '#2e9e5b'), ('p', 'Ro‘yxatga olish', 170, 95, '#2f6fd0'), ('d', 'Shoshilinch yordam kerakmi?', 170, 190, '#e9a420'),
        ('p', 'Reanimatsiya bo‘limiga yuborish', 430, 190, '#d9534f'), ('p', 'Navbatchi shifokor ko‘rigi', 170, 290, '#2f6fd0'), ('d', 'Yotqizish kerakmi?', 170, 385, '#e9a420'),
        ('p', 'Bo‘limga yotqizish', 430, 385, '#2f6fd0'), ('p', 'Uyga tavsiyalar bilan qaytarish', 170, 475, '#2f6fd0'), ('t', 'Tugash', 170, 550, '#2e9e5b')],
        edges=[(0, 1, 'd', ''), (1, 2, 'd', ''), (2, 3, 'r', 'Ha'), (2, 4, 'd', 'Yo‘q'), (4, 5, 'd', ''), (5, 6, 'r', 'Ha'), (5, 7, 'd', 'Yo‘q'), (7, 8, 'd', ''), (3, 8, 'e', ''), (6, 8, 'e', '')]),
    'B': dict(nodes=[
        ('t', 'Shifokor tayinlovi', 170, 25, '#7a5cc7'), ('p', 'Tayinlovni tekshirish', 170, 95, '#3f9ad6'), ('d', 'Allergiya bormi?', 170, 190, '#e8890c'),
        ('p', 'Shifokorga xabar berish', 430, 190, '#d9534f'), ('p', 'Dorini tayyorlash', 170, 290, '#3f9ad6'), ('d', 'Bemor rozimi?', 170, 385, '#e8890c'),
        ('p', 'Sababini yozib qo‘yish', 430, 385, '#d9534f'), ('p', 'Dorini yuborish', 170, 475, '#3f9ad6'), ('t', 'Qaydnomaga yozish', 170, 550, '#7a5cc7')],
        edges=[(0, 1, 'd', ''), (1, 2, 'd', ''), (2, 3, 'r', 'Ha'), (2, 4, 'd', 'Yo‘q'), (4, 5, 'd', ''), (5, 7, 'd', 'Ha'), (5, 6, 'r', 'Yo‘q'), (7, 8, 'd', ''), (3, 8, 'e', ''), (6, 8, 'e', '')]),
}


def fig_flow(v):
    spec = FLOW[v]
    nodes = spec['nodes']

    def box(n):
        k, t, cx, cy, c = n
        w, h = (160, 44) if k != 'd' else (190, 84)
        return k, t, cx, cy, c, w, h

    arrow = '<marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#444"/></marker>'
    edge_svg = label_svg = shapes = texts = ''
    for a, b, kind, lab in spec['edges']:
        _, _, ax, ay, _, aw, ah = box(nodes[a])
        _, _, bx, by, _, bw, bh = box(nodes[b])
        lx = ly = 0
        if kind == 'd':
            x1, y1, x2, y2 = ax, ay + ah / 2, bx, by - bh / 2
            path = 'M%d %d L%d %d' % (x1, y1, x2, y2)
            lx, ly = x1 + 6, (y1 + y2) / 2 - 2
        elif kind == 'r':
            x1, y1, x2, y2 = ax + aw / 2, ay, bx - bw / 2, by
            path = 'M%d %d L%d %d' % (x1, y1, x2, y2)
            lx, ly = (x1 + x2) / 2 - 8, y1 - 5
        else:  # tugash shaklining o'ng chetiga: o'ngdagi umumiy yo'l orqali
            x1, y1, x2, y2 = ax + aw / 2, ay, bx + bw / 2, by
            path = 'M%d %d L590 %d L590 %d L%d %d' % (x1, y1, y1, y2, x2, y2)
        edge_svg += '<path d="%s" fill="none" stroke="#444" stroke-width="2" marker-end="url(#ar)"/>' % path
        if lab:
            label_svg += '<text x="%d" y="%d" font-size="13" font-weight="700" fill="#333">%s</text>' % (lx, ly, lab)
    for n in nodes:
        k, t, cx, cy, c, w, h = box(n)
        if k == 't':
            shapes += '<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="%s" stroke="#0004" stroke-width="1.5"/>' % (cx - w / 2, cy - h / 2, w, h, h / 2, c)
        elif k == 'p':
            shapes += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#0004" stroke-width="1.5"/>' % (cx - w / 2, cy - h / 2, w, h, c)
        else:
            shapes += '<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="#0004" stroke-width="1.5"/>' % (cx, cy - h / 2, cx + w / 2, cy, cx, cy + h / 2, cx - w / 2, cy, c)
        words = t.split()
        mid = (len(words) + 1) // 2 if len(t) > 18 else len(words)
        ls = [' '.join(words[:mid]), ' '.join(words[mid:])] if mid < len(words) else [t]
        fc = '#222' if k == 'd' else '#fff'
        for i, l in enumerate(ls):
            texts += '<text x="%d" y="%.1f" font-size="12.5" font-weight="700" fill="%s" text-anchor="middle" dominant-baseline="middle">%s</text>' % (cx, cy + (i - (len(ls) - 1) / 2) * 15, fc, l)
    return '<svg viewBox="40 0 600 590" height="12.3cm" style="font-family:Calibri,Arial,sans-serif"><defs>%s</defs>%s%s%s%s</svg>' % (arrow, edge_svg, shapes, texts, label_svg)


def fig_kol(v):
    if v == 'A':
        pages = [dict(label='1-bet (titul): kolontitul yo‘q', titul=True),
                 dict(label='2-bet', h=dict(c='Hamshiralik tarixi'), f=dict(l='Aliyev A.', c='01.11.2026', r='2 / 6'), hline=True, it=True),
                 dict(label='3-bet (6-betgacha shunday)', h=dict(c='Hamshiralik tarixi'), f=dict(l='Aliyev A.', c='01.11.2026', r='3 / 6'), hline=True, it=True)]
    else:
        pages = [dict(label='1-bet (1-bo‘lim, titul)', titul=True),
                 dict(label='2-bet (juft)', h=dict(l='Shahrisabz Tibbiyot Texnikumi'), f=dict(l='II')),
                 dict(label='3-bet (2-bo‘lim, toq)', h=dict(r='II bo‘lim. Natijalar'), f=dict(r='1'))]
    return '<div style="width:15.5cm;margin:0 auto">%s</div>' % kol_pages(pages)


def fig_word(v):
    if v == 'A':
        title = wordart('SOG‘LOM TURMUSH TARZI HAFTALIGI', 'arch', '#7be495', '#12803b', '#0a4a22', uid='ka')
        date = wordart('9–15 NOYABR', 'wave', '#ffb347', '#d9730d', '#7a3a00', h=130, uid='kb')
        inner = ('<div style="border:3pt solid #12803b;position:absolute;inset:0.7cm"></div><div style="width:18cm;margin:0.2cm auto 0">%s</div>'
                 '<div style="width:9cm;transform:rotate(8deg);margin:0 0 0 1cm">%s</div>'
                 '<div style="position:absolute;left:2.3cm;top:9.4cm;width:11.5cm;background:#e7f7ec;padding:0.3cm;font-size:14pt;text-align:left"><p style="text-indent:0"><b style="float:left;font-size:40pt;line-height:0.85;margin-right:4pt;color:#12803b">D</b>ushanba: qo‘l gigiyenasi ustaxonasi.</p><p style="text-indent:0">Chorshanba: qon bosimini bepul o‘lchash.</p><p style="text-indent:0">Juma: sport musobaqasi.</p></div>'
                 '<div style="position:absolute;left:2.3cm;top:14.6cm;font:italic 700 24pt Arial;color:#12803b;text-shadow:3px 3px 4px #0005">Harakat — hayot!</div>'
                 '<img src="%s/yurak.png" style="position:absolute;right:2.3cm;top:9.4cm;width:5cm" alt="">') % (title, date, IMG)
    else:
        title = wordart('QON TOPSHIRING — HAYOT ULASHING', 'wave', '#ff6b6b', '#a01010', '#4a0606', uid='kc')
        date = wordart('20-NOYABR', 'arch', '#ffd36b', '#d98a00', '#6b3d00', h=130, uid='kd')
        inner = ('<div style="border:3pt double #a01010;position:absolute;inset:0.7cm"></div><div style="width:18cm;margin:0.2cm auto 0">%s</div>'
                 '<div style="width:9cm;transform:rotate(-6deg);margin:0 0 0 1cm">%s</div>'
                 '<div style="position:absolute;left:2.3cm;top:9.4cm;width:11.5cm;background:#fdeaea;padding:0.3cm;font-size:14pt;text-align:left"><p style="text-indent:0">• Joy: texnikum sport zali</p><p style="text-indent:0">• Vaqt: 9:00–14:00</p><p style="text-indent:0">• Nonushta qiling, ko‘p suyuqlik iching</p><p style="text-indent:0">• Pasport yoningizda bo‘lsin</p></div>'
                 '<div style="position:absolute;left:2.3cm;top:14.6cm;font:italic 700 24pt Arial;color:#a01010;text-shadow:3px 3px 4px #0005">Bitta tomchi — bitta umr</div>'
                 '<img src="%s/yurak.png" style="position:absolute;right:2.3cm;top:9.4cm;width:6cm" alt="">'
                 '<div style="position:absolute;right:2.3cm;top:12.6cm;width:5cm;height:1.5cm;background:#ffd36b;border-radius:0.3cm;display:flex;align-items:center;justify-content:center;font:700 14pt Calibri;color:#6b3d00">Muhim!</div>') % (title, date, IMG)
    return mockbox('<div style="margin:-2cm">%s</div>' % inner)


def fig_for(S):
    e = S['etalon']
    if e.startswith('rasm'):
        return fig_rasm(S, e[-1])
    if e.startswith('flow'):
        return '<div class="fig" style="padding:0.15cm">%s</div>' % fig_flow(e[-1])
    if e.startswith('kol'):
        return '<div class="fig" style="padding:0.2cm">%s</div>' % fig_kol(e[-1])
    return fig_word(e[-1])


CHECK_TIPS = {
    'rasm': 'Rasmni <b>bir marta bosing</b> → <b>Rasm formati</b> yorlig‘ida: <b>Eni</b> (o‘lcham), <b>Matn bilan o‘rash</b> ro‘yxati, <b>Rasm uslublari</b>. Cho‘zilgan rasm ko‘zga tashlanadi (dumaloq narsa oval). Sarlavhalar avtomatikmi — raqamni bosing: kulrang fon chiqsa, bu maydon (to‘g‘ri). Suv belgisi: bosilmasa, Tanlash oynasidan toping. Fayl hajmi: <b>Fayl › Ma’lumot</b>.',
    'shakllar': 'Shakllardan birini suring: <b>ulagichlar ergashsa</b> — ulangan, ergashmasa — ulanmagan (qaytaring: <span class="key-cap">Ctrl</span> + <span class="key-cap">Z</span>). Bir shaklni bosganda <b>hammasi tanlansa</b> — guruhlangan. O‘lcham: <b>Shakl formati › O‘lcham</b>. Shakl turini sichqonchani ustiga olib borib ko‘ring yoki shakl nomini <b>Tanlash oynasida</b> o‘qing.',
    'kolontitul': 'Varaqning yuqori yoki pastki chetiga <b>ikki marta bosing</b>: kolontitul rejimi ochilib, <b>Kolontitul asboblari</b> chiqadi. Sahifa raqamini bosganda <b>kulrang fon</b> chiqsa — maydon (avtomatik). Titulda raqam yo‘qligini va «Toq va juft…» belgisini <b>Konstruktor</b> yorlig‘ida ko‘ring. Bo‘limlarni <span class="key-cap">Ctrl</span> + <span class="key-cap">P</span> orqali varaqlab tekshiring.',
    'wordart': 'Sarlavhani bosing: <b>Shakl formati</b> chiqsa va ramka bo‘lsa — WordArt. <b>Shior</b> bosilganda ramka va Shakl formati <b>chiqmasligi</b> kerak (oddiy matn). Transformatsiya: <b>Shakl formati › Matn effektlari › Transformatsiya</b> — belgilangan variant ko‘rinadi. Kontrastni 1 metr naridan baholang.',
}


def key_page(T, S):
    ans = ''.join('<li><b>%d.</b> %s</li>' % (i + 1, a) for i, a in enumerate(S['ans']))
    qs = ''.join('<li>%s</li>' % q for q in S['qs'])
    return '''<div class="sheet info tp key" style="--tc:%(c)s">
  <div class="info-top"><div><b>Tibbiyotda axborot texnologiyalari</b><br>O‘qituvchi kaliti • Word 3-dars • %(name)s</div><span class="info-num">%(n)d-%(name)s • %(v)s</span></div>
  <h1 style="margin-top:0.25cm">%(title)s</h1>
  <h2>Kutilgan natija (taxminiy namuna)</h2>
  %(fig)s
  <h2>Yozma savollar va javoblari</h2>
  <ol class="qs ak">%(a)s</ol>
  <div class="hint"><b>Qanday tekshiriladi:</b> %(tip)s</div>
  <div class="info-foot"><span>%(tex)s</span><span>Kalit: %(name)s • %(v)s • 20 ball: %(gr)s</span></div>
</div>''' % dict(c=T['color'], name=T['name'], n=T['n'], v=S['v'], title=S['title'], fig=fig_for(S), a=''.join(
        '<li><i>%s</i><br>%s</li>' % (q, a) for q, a in zip(S['qs'], S['ans'])), tip=kc(CHECK_TIPS[T['key']]), tex=TEXNIKUM,
        gr='; '.join('%s — %s' % (a, b.split()[0]) for a, b in GRADES20))


def write(path, text):
    with open(path, 'w', encoding='utf8', newline='\n') as f:
        f.write(text)


def doc(sheets, title):
    return print_doc(sheets, title).replace('</style></head>', TOPIC_CSS + '</style></head>')


def main():
    check()
    os.makedirs(OUT_HTML, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)
    ok = True
    allsheets, keys = [], []
    for T in TOPICS:
        for S in T['sheets']:
            sh = student_sheet(T, S)
            allsheets.append(sh)
            keys.append(key_page(T, S))
            name = '%d-%s-%s' % (T['n'], T['key'], S['v'])
            write(os.path.join(OUT_HTML, name + '.html'), doc([sh], name))
            pages = to_pdf(os.path.join(OUT_HTML, name + '.html'), os.path.join(PDF_DIR, name + '.pdf'))
            ok &= pages == 1
            print(name, pages, 'bet', 'OK' if pages == 1 else 'DIQQAT: 1 bet kutilgan')
    for fname, sheets, ttl in (('barcha-mavzu-varaqlari', allsheets, 'Word 3-dars: mavzu varaqlari'), ('kalit-oqituvchi', keys, 'Word 3-dars: o‘qituvchi kaliti')):
        write(os.path.join(OUT_HTML, fname + '.html'), doc(sheets, ttl))
        pages = to_pdf(os.path.join(OUT_HTML, fname + '.html'), os.path.join(PDF_DIR, fname + '.pdf'))
        ok &= pages == len(sheets)
        print(fname, pages, 'bet (kutilgan %d)' % len(sheets))
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
