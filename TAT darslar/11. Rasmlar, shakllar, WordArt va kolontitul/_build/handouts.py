# -*- coding: utf-8 -*-
"""Tarqatma varaqlari: topshiriq (1-bet), namuna (2-bet) va o'qituvchi varaqlari. HTML -> PDF."""
import os
import re
import subprocess

from svgs import wordart
from variants import CRITERIA, GRADES, TEXNIKUM, VARIANTS, hf_text

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

with open(os.path.join(HERE, 'sheet.css'), encoding='utf8') as f:
    SHEET_CSS = f.read()


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def kc(s):
    return re.sub(r'\[\[(.+?)\]\]', r'<span class="key-cap">\1</span>', s)


# ----------------------------------------------------------------------------
# NAMUNA VARAG'I: haqiqiy A4, to'rtta vosita raqamlangan
# ----------------------------------------------------------------------------
POSTER_CSS = '''
  .sheet.poster { padding: 2cm; font-family: "Times New Roman", Times, serif; font-size: 14pt; line-height: 1.2; }
  .poster .mk { position: absolute; width: 0.55cm; height: 0.55cm; border-radius: 50%; background: #185abd; color: #fff;
    font: 700 9pt/0.55cm Arial, sans-serif; text-align: center; z-index: 5; box-shadow: 0 0 0 1.5pt #fff; }
  .poster .wa { position: relative; height: 3.2cm; }
  .poster .wa svg { position: absolute; left: 0; top: 0; }
  .poster .body { position: relative; margin-top: 0.3cm; overflow: hidden; }
  .poster .body p { text-align: justify; text-indent: 1.25cm; margin: 0; }
  .poster .pic { float: left; width: 5.5cm; margin: 0.1cm 0.45cm 0.25cm 0; position: relative; }
  .poster .pic img { width: 100%; display: block; }
  .poster .pic .mk { left: 0.12cm; top: 0.12cm; }
  .poster .shp { position: relative; height: 3cm; margin-top: 0.1cm; }
  .poster .shp .mk { right: 10.5cm; top: 0.35cm; }
  .poster .callout { position: absolute; right: 2.1cm; top: 0.5cm; width: 8cm; height: 1.7cm; border-radius: 0.4cm; color: #fff;
    font: 700 14pt/1.1 Calibri, Arial, sans-serif; display: flex; align-items: center; justify-content: center; text-align: center;
    padding: 0 0.3cm; border: 1.5pt solid rgba(0,0,0,0.35); }
  .poster .callout::after { content: ""; position: absolute; left: 1.2cm; bottom: -0.5cm; border-left: 0.35cm solid transparent;
    border-right: 0.35cm solid transparent; border-top: 0.55cm solid var(--cc); }
  .poster .star { position: absolute; right: 0; top: 0; width: 3cm; height: 3cm; }
  .poster .star svg { width: 100%; height: 100%; display: block; }
  .poster .star span { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
    font: 700 30pt Calibri, Arial, sans-serif; color: #fff; padding-top: 0.15cm; }
  .poster .sa { position: relative; margin-top: 0.15cm; padding-left: 0.1cm; }
  .poster .sa .lh { font-weight: 700; margin: 0 0 0.05cm 0; text-indent: 0; }
  .poster .sa ol { margin: 0; padding-left: 1.1cm; } .poster .sa li { margin-bottom: 0.04cm; }
  .poster .hdr, .poster .ftr { position: absolute; left: 2cm; right: 2cm; display: grid; grid-template-columns: 1fr 1fr 1fr; font: 10pt "Times New Roman", serif; color: #444; }
  .poster .hdr { top: 1cm; padding-bottom: 0.1cm; } .poster .ftr { bottom: 1.25cm; padding-top: 0.1cm; }
  .poster .hdr.line { border-bottom: 0.75pt solid #444; } .poster .hdr span:nth-child(2), .poster .ftr span:nth-child(2) { text-align: center; }
  .poster .hdr span:nth-child(3), .poster .ftr span:nth-child(3) { text-align: right; } .poster .it { font-style: italic; }
  .poster .hdr .mk { left: -0.8cm; top: -0.1cm; } .poster .ftr .mk { left: -0.8cm; top: 0; }
  .poster .fld { background: #d9d9d9; padding: 0 1pt; }
  .poster .legend { position: absolute; left: 2cm; right: 2cm; bottom: 0.35cm; font: 8pt Arial, sans-serif; color: #888; text-align: center; }
  .pic.st-1 img { border: 7px solid #fff; box-shadow: 0 0 0 1px #bbb, 0 1px 4px rgba(0,0,0,0.25); }
  .pic.st-2 img { box-shadow: 5px 6px 8px rgba(0,0,0,0.45); }
  .pic.st-3 img { -webkit-mask-image: linear-gradient(to right, transparent, #000 14%, #000 86%, transparent), linear-gradient(to bottom, transparent, #000 14%, #000 86%, transparent);
    -webkit-mask-composite: source-in; mask-composite: intersect; }
  .pic.st-4 img { border-radius: 0.3cm; border: 1px solid #aaa; }
  .pic.st-4 { -webkit-box-reflect: below 1px linear-gradient(transparent 62%, rgba(255,255,255,0.35)); }
  .pic.st-5 img { border: 8px solid #fff; box-shadow: 0 0 0 1px #aaa, inset 0 0 0 3px #e3e3e3; outline: 1px solid #ccc; }
  .pic.st-6 img { border: 7px ridge #b7bcc2; border-radius: 3px; }
'''


def image_ref(base, fname):
    return '%s/%s' % (base, fname)


def hf_html(d, V, markers):
    out = ''
    for k in ('l', 'c', 'r'):
        t = esc(d.get(k, ''))
        t = t.replace('{p}', '<span class="fld">1</span>').replace('{n}', '<span class="fld">1</span>')
        out += '<span>%s</span>' % t
    return out


def poster_body(V, img_base, markers=True):
    cc, sc = V['shape_colors']
    mk = (lambda n: '<span class="mk">%d</span>' % n) if markers else (lambda n: '')
    wa = V['wa']
    war = wordart(wa['text'], wa['effect'], wa['c1'], wa['c2'], wa['stroke'], uid='v%d' % V['n'])
    paras = ''.join('<p>%s</p>' % esc(p) for p in V['paras'])
    star = ('<svg viewBox="0 0 100 100"><polygon points="50,4 61,36 95,37 68,57 78,92 50,71 22,92 32,57 5,37 39,36" '
            'fill="%s" stroke="rgba(0,0,0,0.35)" stroke-width="2"/></svg><span>%s</span>' % (sc, esc(V['star'])))
    hf = V['hf']
    lis = ''.join('<li>%s</li>' % esc(x) for x in V['items'])
    return '''<div class="hdr%(hl)s%(it)s">%(m4)s%(hh)s</div><div class="ftr%(it)s">%(ff)s</div>
<div class="wa">%(m1)s%(war)s</div>
<div class="body"><div class="pic st-%(n)d">%(m2)s<img src="%(img)s" alt=""></div>%(paras)s</div>
<div class="shp">%(m3)s<div class="callout" style="background:%(cc)s;--cc:%(cc)s">%(call)s</div><div class="star">%(star)s</div></div>
<div class="sa"><p class="lh">Bosqichlar:</p><ol>%(lis)s</ol></div>''' % dict(
        hl=' line' if hf['line'] else '', it=' it' if hf['it'] else '', m4=mk(4), hh=hf_html(hf['h'], V, markers), ff=hf_html(hf['f'], V, markers),
        m1=mk(1), war=war, n=V['n'], m2=mk(2), img=image_ref(img_base, V['pic']['file']), paras=paras,
        m3=mk(3), cc=cc, call=esc(V['callout']), star=star, lis=lis)


def sample_sheet(V, img_base, label=True, markers=True):
    lab = '<span class="sheet-label">Namuna • %d-variant</span>' % V['n'] if label else ''
    leg = ('<div class="legend">1 — WordArt • 2 — Rasm • 3 — Shakllar (guruhlangan) • 4 — Kolontitul (yuqori va pastki). '
           'Raqamlar faqat izoh: hujjatga yozilmaydi. Kulrang fon — avtomatik maydon.</div>') if markers else ''
    return '<div class="sheet poster">%s%s%s</div>' % (lab, poster_body(V, img_base, markers), leg)


# ----------------------------------------------------------------------------
# TOPSHIRIQ VARAG'I
# ----------------------------------------------------------------------------
def steps(V):
    wa, st, hf = V['wa'], V['pic']['style'], V['hf']
    return [
        'Word → <b>Yangi hujjat</b>. Darhol [[Ctrl]]+[[S]]: nom <b>Familiya_V%d</b>. <b>Maket → Maydonlar → Maxsus maydonlar</b>: to‘rt tomondan <b>2 sm</b>. '
        'Shrift: Times New Roman, 14 pt.' % V['n'],
        'Namunadagi <b>ikki abzats</b>ni tering ([[Ctrl]]+[[J]], xatboshi 1,25 sm), so‘ng <b>«Bosqichlar»</b> ro‘yxatini <b>raqamlab</b> yozing (Bosh sahifa → Raqamlash). Yuqorida WordArt uchun bo‘sh qator qoldirmang.',
        '<b>WordArt:</b> <b>Qo‘shish → WordArt</b> → istalgan uslub. «TEXT» ni o‘chirib yozing: <b>%s</b>. Sarlavhani varaq tepasiga, o‘rtaga qo‘ying.' % esc(wa['text']),
        '<b>WordArt effekti:</b> <b>Shakl formati → Matn effektlari → Transformatsiya</b>: <b>%s</b>. Matn to‘ldirish va konturni <b>%s</b> ranglarda o‘zgartiring.' % (wa['tr'], wa['color']),
        '<b>Rasm:</b> <b>Qo‘shish → Rasmlar → Bu qurilma</b> → <b>rasmlar</b> papkasidan <b>%s</b>. Eni <b>5,5 sm</b>: faqat <u>burchakdagi</u> nuqtadan torting (yon nuqtadan tortsangiz, rasm cho‘ziladi).' % V['pic']['file'],
        '<b>Matn bilan o‘rash:</b> <b>Rasm formati → Matn bilan o‘rash → Kvadrat</b>. Rasmni birinchi abzats boshiga, chap tomonga sudrab qo‘ying: matn uni aylanib o‘tsin.',
        '<b>Rasm uslubi:</b> <b>Rasm formati → Rasm uslublari</b> → <b>%s</b>.' % st,
        '<b>Shakllar:</b> <b>Qo‘shish → Shakllar → Izohlar</b> → «Yumaloq to‘rtburchak izoh», ichiga «<b>%s</b>». Ikkinchisi: <b>Yulduzlar va lentalar</b> → «5 uchli yulduz» ([[Shift]] ni bosib turib chizing), ichiga «<b>!</b>». '
        'Ranglar: <b>Shakl formati → Shakl to‘ldirish</b>.' % esc(V['callout']),
        '<b>Guruhlash:</b> [[Ctrl]] ni bosib turib ikkala shaklni tanlang → o‘ng tugma → <b>Guruhlash → Guruhlash</b>. Guruhni namunadagidek, matn tagiga joylang.',
        '<b>Yuqori kolontitul:</b> <b>Qo‘shish → Yuqori kolontitul → Bo‘sh</b> (yoki varaq yuqori chetiga ikki marta bosing). Yozing: %s. Shrift 10 pt%s.' % (hf['how_h'], ', <b>chiziq</b> bilan' if hf['line'] else ''),
        '<b>Pastki kolontitul va avtomatik sahifa raqami:</b> %s. Raqam <b>qo‘lda yozilmaydi</b> — bosganda kulrang fon (maydon) ko‘rinsin. [[Esc]] — kolontitulni yopish.' % hf['how_f'],
        'Hammasi <b>bitta betga</b> sig‘sin, hech narsa boshqasini yopmasin. [[Ctrl]]+[[S]] va o‘qituvchini chaqiring.',
    ]


def info_sheet(V, rel_pics):
    tools = [('1', 'WordArt', 'bezakli sarlavha'), ('2', 'Rasm', 'tayyor rasm fayli'), ('3', 'Shakllar', 'izoh va yulduz'), ('4', 'Kolontitul', 'yuqori va pastki')]
    crit = ''.join('<tr><td class="cn">%d</td><td><b>%s</b> — %s</td><td class="cb">0,5</td><td class="cg"></td></tr>'
                   % (i + 1, a, b.replace('Familiya_V№', 'Familiya_V%d' % V['n'])) for i, (a, b) in enumerate(CRITERIA))
    grades = '; '.join('%s → %s' % (a, b.split()[0]) for a, b in GRADES)
    return '''<div class="sheet info">
  <div class="info-top"><div><b>Tibbiyotda axborot texnologiyalari</b><br>Word 3-dars: rasm, shakl, WordArt va kolontitul • amaliy ish</div><span class="info-num">%(n)d-variant</span></div>
  <div class="info-fio"><span>F.I.O.:</span><span>Guruh:</span><span>Sana:</span></div>
  <h1>%(n)d-variant: %(title)s</h1>
  <p class="info-goal"><b>Hujjat:</b> %(about)s Keyingi betdagi namunani Word’da xuddi shunday tayyorlang. Namunadagi raqamlar vositani bildiradi: %(tools)s. Rasm fayli: <b>rasmlar / %(pic)s</b>.</p>
  <h2>Topshiriq sharti</h2>
  <ol class="steps">%(steps)s</ol>
  <h2>Baholash (o‘qituvchi to‘ldiradi)</h2>
  <table class="crit"><thead><tr><th>№</th><th>Mezon</th><th>Maks.</th><th>Ball</th></tr></thead><tbody>%(crit)s
    <tr class="tot"><td></td><td>Jami</td><td class="cb">5</td><td class="cg"></td></tr></tbody></table>
  <div class="info-sign"><span><b>Baho:</b> ______ <span class="gr">(%(grades)s)</span></span><span>O‘qituvchi imzosi: __________</span></div>
  <div class="info-foot"><span>%(tex)s</span><span>1-bet: topshiriq • 2-bet: namuna</span></div>
</div>''' % dict(n=V['n'], title=V['title'], about=V['about'], pic=V['pic']['file'],
                 tools=', '.join('<b>%s</b> — %s' % (a, b) for _, a, b in tools),
                 steps=''.join('<li>%s</li>' % kc(x) for x in steps(V)),
                 crit=crit, grades=grades, tex=TEXNIKUM)


# ----------------------------------------------------------------------------
# O'QITUVCHI VARAQLARI
# ----------------------------------------------------------------------------
def teacher_sheets():
    check = [
        ('Fayl', '<b>Familiya_V№.docx</b>, bitta bet, <b>Maket → Maydonlar</b>: 2 sm (1-mezon).'),
        ('Elementni bosing', 'Har bir elementga <b>bir marta bosing</b> va yuqorida qaysi yorliq paydo bo‘lishiga qarang — vosita shu bilan aniqlanadi (3, 5, 8, 10-mezonlar).'),
        ('WordArt', 'Bosilganda <b>Shakl formati</b> chiqadi va ichida matnni tahrirlash mumkin. Agar yorliq chiqmasa — sarlavha oddiy matn (shrift effekti) yoki rasm: 0 ball.'),
        ('Rasm', 'Bosilganda <b>Rasm formati</b> chiqadi. Cho‘zilganini ko‘z bilan ko‘ring: dumaloq narsa oval bo‘lib qolgan bo‘ladi (5-mezon). <b>Eni</b> 5,5 sm — shu yorliqning o‘ng tomonida.'),
        ('Matn bilan o‘rash', 'Rasmni bosib, <b>Matn bilan o‘rash</b> ro‘yxatida <b>Kvadrat</b> belgilanganini ko‘ring. Matn rasmning o‘ng tomonidan o‘tib ketishi kerak (6-mezon).'),
        ('Shakllar va guruh', 'Shaklni <b>bir marta</b> bosing: ikkala shakl birga tanlansa — guruhlangan (9-mezon). Faqat bittasi tanlansa — guruhlanmagan.'),
        ('Kolontitul', 'Varaqning yuqori yoki pastki chetiga <b>ikki marta bosing</b>: kolontitul rejimi ochilib, <b>Kolontitul asboblari</b> yorlig‘i chiqadi (10-mezon). Sahifa raqamini bosganda <b>kulrang fon</b> chiqsa — avtomatik maydon. Raqam qo‘lda yozilgan bo‘lsa (bosilganda fon yo‘q) yoki matn kolontitulda emas, sahifa ichida yozilgan bo‘lsa — 0 ball.'),
    ]
    rules = [
        'Har bir mezon to‘liq bajarilsa 0,5 ball, bajarilmasa 0 ball; yarim ball qo‘yilmaydi — tekshirish tez va bir xil bo‘ladi.',
        'Rang nomi qat’iy talab emas: namunaga yaqin ranglar (to‘ldirish va kontur o‘zgargan bo‘lsa) 4-mezonga yetarli.',
        'Rasm uslubi nomi o‘zgargan bo‘lsa (Word versiyasiga qarab) — namunadagi ko‘rinishga o‘xshash bo‘lsa, 7-mezon beriladi.',
        'Word’ning eski versiyasida (2010) ba’zi uslublar va “Transformatsiya” nomi boshqacha bo‘lishi mumkin — talabaga ko‘rinishi bo‘yicha baho bering.',
        'Ikki talabaning fayli bir xil bo‘lsa (rasm va matn ham) — ikkalasiga qayta topshiriq. Yonma-yon o‘tirganlarga turli variant bering.',
    ]
    page1 = '''<div class="sheet info teacher">
  <div class="info-top"><div><b>Tibbiyotda axborot texnologiyalari</b><br>Word 3-dars amaliy ishi • faqat o‘qituvchi uchun</div><span class="info-num">O‘qituvchi</span></div>
  <h1 style="margin-top:0.4cm">Amaliy ishni tekshirish tartibi</h1>
  <p class="info-goal">Asosiy usul: <b>elementni bir marta bosib, qaysi yorliq chiqishiga qarang</b>. Sarlavhani oddiy matn bilan “WordArt”ga o‘xshatib ishlagan yoki sahifa raqamini qo‘lda yozib “kolontitul” deb topshirgan ishni shu yo‘l bilan 5 soniyada aniqlaysiz. Bitta ishga 2–3 daqiqa ketadi.</p>
  <h2>Qadamlar</h2>
  <table class="crit chk"><thead><tr><th>Nima</th><th>Qanday tekshiriladi</th></tr></thead><tbody>%s</tbody></table>
  <h2>Mezonlar</h2>
  <table class="crit"><thead><tr><th>№</th><th>Mezon</th><th>Ball</th></tr></thead><tbody>%s</tbody></table>
  <p class="info-goal" style="margin-top:0.15cm">%s</p>
  <h2>Baholash qoidalari</h2>
  <ul class="rules">%s</ul>
  <div class="info-foot"><span>%s</span><span>1-bet: tekshirish tartibi • 2-bet: variant parametrlari • 3-bet: qaydnoma</span></div>
</div>''' % (
        ''.join('<tr><td class="cn">%s</td><td>%s</td></tr>' % (a, kc(b)) for a, b in check),
        ''.join('<tr><td class="cn">%d</td><td><b>%s</b> — %s</td><td class="cb">0,5</td></tr>' % (i + 1, a, b) for i, (a, b) in enumerate(CRITERIA)),
        'Jami: 5 ball. ' + ' &nbsp;•&nbsp; '.join('%s → <b>%s</b>' % g for g in GRADES),
        ''.join('<li>%s</li>' % kc(r) for r in rules), TEXNIKUM)

    rows = ''
    for V in VARIANTS:
        rows += ('<tr><td class="cn">%d</td><td><b>%s</b></td><td>%s<br>%s</td><td>%s<br><i>%s</i></td><td>Yuqori: %s<br>Pastki: %s</td></tr>'
                 % (V['n'], V['name'], V['wa']['tr'], V['wa']['color'], V['pic']['file'], V['pic']['style'], hf_text(V, 'h'), hf_text(V, 'f')))
    page2 = '''<div class="sheet info teacher">
  <div class="info-top"><div><b>Tibbiyotda axborot texnologiyalari</b><br>Word 3-dars amaliy ishi • variant parametrlari</div><span class="info-num">O‘qituvchi</span></div>
  <h1 style="margin-top:0.4cm">Variantlar: nimani qidirish kerak</h1>
  <p class="info-goal">Har bir variantda bir xil to‘rt vosita bor, farqi — kolontitul matni, rasm, uslub va WordArt effekti. Jadval tekshirishda tez qarab chiqish uchun.</p>
  <table class="crit"><thead><tr><th>№</th><th>Variant</th><th>WordArt (effekt, rang)</th><th>Rasm fayli va uslubi</th><th>Kolontitul (yuqori / pastki)</th></tr></thead><tbody>%s</tbody></table>
  <h2>Hamma variantlarda bir xil</h2>
  <ul class="rules"><li>Varaq A4, kitob, maydonlar 2 sm; matn Times New Roman 14 pt, ikki tomonga, xatboshi 1,25 sm.</li>
  <li>Rasm eni 5,5 sm, «Kvadrat» o‘rash, abzats boshida chapda.</li>
  <li>Ikki shakl: izoh (ichida matn) va 5 uchli yulduz (ichida «!»), ikkalasi guruhlangan.</li>
  <li>Yuqori kolontitul va pastki kolontitul (avtomatik sahifa raqami), shrift 10 pt; hammasi bitta betda.</li></ul>
  <div class="info-foot"><span>%s</span><span>2-bet: variant parametrlari</span></div>
</div>''' % (rows, TEXNIKUM)

    head = ''.join('<th>%d</th>' % i for i in range(1, 11))
    rows = ''.join('<tr><td class="cn">%d</td><td></td><td></td>%s<td></td><td></td></tr>' % (i, '<td></td>' * 10) for i in range(1, 31))
    leg = '; '.join('%d — %s' % (i + 1, a.lower()) for i, (a, b) in enumerate(CRITERIA))
    page3 = '''<div class="sheet info teacher">
  <div class="info-top"><div><b>Tibbiyotda axborot texnologiyalari</b><br>Word 3-dars amaliy ishi • baholash qaydnomasi</div><span class="info-num">Qaydnoma</span></div>
  <div class="info-fio"><span>Guruh:</span><span>Sana:</span><span>O‘qituvchi:</span></div>
  <table class="reg"><thead><tr><th>№</th><th class="fio">F.I.O.</th><th class="w1">Var.</th>%s<th class="w2">Jami</th><th class="w2">Baho</th></tr></thead><tbody>%s</tbody></table>
  <p class="reg-legend">%s. Har bir mezon 0,5 ball.</p>
  <div class="info-foot"><span>%s</span><span>Imzo: ______________</span></div>
</div>''' % (head, rows, leg, TEXNIKUM)
    return [page1, page2, page3]


EXTRA_CSS = '''
  .sheet-label { position: absolute; top: 0.35cm; right: 1.5cm; font-family: Arial, Helvetica, sans-serif; font-size: 8pt; color: #a6a6a6; letter-spacing: 0.05em; text-transform: uppercase; z-index: 6; }
  .sheet.info { font-size: 9.2pt; line-height: 1.33; }
  .sheet.info h1 { font-size: 15pt; }
  .sheet.info h2 { margin: 0.24cm 0 0.1cm 0; font-size: 10pt; }
  .sheet.info ol.steps li { margin-bottom: 0.03cm; }
  .sheet.info ol.steps b, .sheet.info table b { color: #0b2a5b; }
  table.crit { width: 100%; border-collapse: collapse; font-size: 8.6pt; line-height: 1.25; }
  table.crit th { background: #185abd; color: #fff; font-weight: 700; padding: 2.5pt 4pt; text-align: left; border: 0.75pt solid #185abd; }
  table.crit td { border: 0.75pt solid #c9d6ea; padding: 1.4pt 4pt; vertical-align: top; }
  table.crit td.cn { width: 0.7cm; text-align: center; font-weight: 700; color: #185abd; }
  table.crit td.cb { width: 1.2cm; text-align: center; }
  table.crit td.cg { width: 1.4cm; }
  table.crit tr.tot td { font-weight: 700; background: #eef3fb; }
  table.crit .gr { font-weight: 400; font-size: 8pt; color: #333; }
  table.crit.chk td.cn { width: 2.6cm; text-align: left; }
  .info-sign { display: flex; justify-content: space-between; align-items: baseline; margin-top: 0.2cm; font-size: 10pt; }
  .info-sign .gr { font-size: 8pt; color: #555; }
  .sheet.info .info-fio { margin: 0.25cm 0 0.3cm 0; }
  .sheet.info ul.rules { padding-left: 0.5cm; }
  .sheet.info ul.rules li { margin-bottom: 0.08cm; }
  table.reg { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 8.5pt; margin-top: 0.2cm; }
  table.reg th { width: 0.72cm; }
  table.reg th.w1 { width: 1.1cm; } table.reg th.w2 { width: 1.4cm; }
  table.reg th { background: #185abd; color: #fff; border: 0.75pt solid #185abd; padding: 3pt 0; text-align: center; font-weight: 700; }
  table.reg td { border: 0.75pt solid #9fb4d6; height: 0.72cm; text-align: center; }
  table.reg th.fio { width: auto; }
  table.reg td.cn { width: 0.7cm; color: #185abd; font-weight: 700; }
  .reg-legend { font-size: 8.5pt; color: #333; margin-top: 0.2cm !important; }
''' + POSTER_CSS


def print_doc(sheets, title):
    return '''<!DOCTYPE html>
<html lang="uz"><head><meta charset="UTF-8"><title>%s</title>
<style>
  @page { size: A4; margin: 0; }
  html, body { margin: 0; padding: 0; background: #ffffff; }
  .sheet { page-break-after: always; break-after: page; }
  .sheet:last-child { page-break-after: auto; break-after: auto; }
%s%s</style></head><body>
%s
</body></html>''' % (title, SHEET_CSS, EXTRA_CSS, '\n'.join(sheets))


def to_pdf(html_path, pdf_path):
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                    '--print-to-pdf=' + pdf_path, 'file:///' + html_path.replace('\\', '/')],
                   check=True, capture_output=True)
    with open(pdf_path, 'rb') as f:
        return len(re.findall(rb'/Type\s*/Page[^s]', f.read()))
