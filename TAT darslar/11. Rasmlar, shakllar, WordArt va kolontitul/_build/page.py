# -*- coding: utf-8 -*-
"""Dars sahifasi (dars.html): 9-darsning bosh qismi (CSS, navigatsiya) + 10-darsning mazmuni."""
import importlib.util
import json
import os
import re

from handouts import POSTER_CSS, kc, sample_sheet
from svgs import kol_pages, wordart
from variants import CRITERIA, TEXNIKUM, VARIANTS
from topics import TOPICS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TAT = os.path.dirname(ROOT)
BASE = os.path.join(TAT, '9. Matn kiritish va rasmiy hujjatlar', 'dars.html')
THEME_SCRIPT = os.path.join(TAT, '6. Windows operatsion tizimi', 'scripts', 'apply-cover-themes.py')
IMG_FROM_LESSON = './tarqatma/rasmlar'

TITLE = '11-Dars: Word’da rasmlar, shakllar, WordArt va kolontitul'


def read(name):
    with open(os.path.join(HERE, name), encoding='utf8') as f:
        return f.read()


def K(s):
    return kc(s).replace('<span class="key-cap">', '<span class="key-cap">')


def ico(path, size=20, sw=2.2):
    return '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % (size, size, sw, path)


I_IMG = '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>'
I_SHAPE = '<rect x="3" y="3" width="9" height="9" rx="1"/><circle cx="17" cy="17" r="4.5"/><path d="M12 12l0 0"/>'
I_KOL = '<rect x="5" y="2" width="14" height="20" rx="1.5"/><line x1="5" y1="6.5" x2="19" y2="6.5"/><line x1="5" y1="17.5" x2="19" y2="17.5"/><line x1="9" y1="11" x2="15" y2="11"/>'
I_SMART = '<rect x="9" y="3" width="6" height="5" rx="1"/><rect x="3" y="16" width="6" height="5" rx="1"/><rect x="15" y="16" width="6" height="5" rx="1"/><path d="M12 8v4M6 16v-4h12v4"/>'
I_WORD = '<path d="M4 7V4h16v3M9 20h6M12 4v16"/>'


def op_card(icon_cls, icon_path, title, rows):
    out = '<div class="op-card"><div class="op-head"><div class="card-icon %s">%s</div><h4>%s</h4></div>' % (icon_cls, ico(icon_path), title)
    for lab, cls, text in rows:
        style = ''
        out += '<div class="op-row"><span class="op-label %s">%s</span><span>%s</span></div>' % (cls, lab, text)
    return out + '</div>'


def crumb(*parts):
    return '<span class="crumb">' + ' › '.join('<b>%s</b>' % p for p in parts) + '</span>'


def section(sid, num, title, desc, body, teacher=False, last=False):
    cls = 'section-block' + (' teacher-only' if teacher else '')
    style = ' style="margin-bottom: 1rem;"' if last else ''
    return ('<section id="%s" class="%s"%s>\n<div class="section-head">\n<span class="section-num">%s</span>\n'
            '<h2 class="section-title">%s</h2>\n<p class="section-desc">%s</p>\n</div>\n%s\n</section>\n' % (sid, cls, style, num, title, desc, body))


# ----------------------------------------------------------------------------
# 1-QISM: TO'RT VOSITA
# ----------------------------------------------------------------------------
def sec_tools():
    cards = [
        ('#60a5fa', I_IMG, 'Rasm', 'Picture / Рисунок',
         'Tayyor rasm fayli: fotosurat, rentgen, sxema, logotip. Siz uni chizmaysiz — faqat hujjatga qo‘yib, o‘lchamini va joyini sozlaysiz.',
         '<b>O‘xshatish:</b> kitobga yopishtirilgan tayyor surat.', 'Rasm formati (Picture Format)'),
        ('#34d399', I_SHAPE, 'Shakllar', 'Shapes / Фигуры',
         'Word ichida o‘zingiz chizadigan oddiy figuralar: to‘rtburchak, strelka, yulduz, izoh. Ichiga matn yozish mumkin.',
         '<b>O‘xshatish:</b> konstruktor g‘ishtlari — o‘zingiz yig‘asiz.', 'Shakl formati (Shape Format)'),
        ('#f59e0b', I_KOL, 'Kolontitul', 'Header & Footer / Колонтитул',
         'Sahifaning yuqori va pastki chetidagi, barcha betlarda takrorlanadigan yozuv: hujjat nomi, sana va avtomatik sahifa raqami.',
         '<b>O‘xshatish:</b> kitob sahifasi tepasidagi nom va pastidagi raqam.', 'Kolontitul asboblari (Header &amp; Footer)'),
        ('#f472b6', I_WORD, 'WordArt', 'WordArt / WordArt',
         'Bezakli yozuv: rangli, konturli, soyali, egri. Plakat va e’lon sarlavhasi uchun. Aslida bu alohida ramkadagi matn.',
         '<b>O‘xshatish:</b> devoriy gazeta sarlavhasi.', 'Shakl formati (Shape Format)'),
    ]
    html = '<div class="grid-4">'
    for c, ic, name, en, what, ana, tab in cards:
        html += ('<div class="tool4" style="--tc:%s"><div class="t-ic">%s</div><h3>%s</h3><div class="t-en">%s</div><p>%s</p><p>%s</p>'
                 '<span class="t-tab">Bosilganda: %s</span></div>' % (c, ico(ic, 22), name, en, what, ana, tab))
    html += '</div>'
    html += '''<div class="lead-line"><strong>Hammasi bir joyda:</strong> <b>Qo‘shish</b> (Insert / Вставка) yorlig‘i. <b>Illyustratsiyalar</b> (Illustrations) guruhida — Rasmlar va Shakllar; <b>Matn</b> (Text) guruhida — WordArt; <b>Kolontitul</b> (Header &amp; Footer) guruhida — Yuqori kolontitul, Pastki kolontitul va Sahifa raqami.
    Qaysi vosita ekanini aniqlashning eng oson yo‘li: elementni <b>bir marta bosing</b> — yuqorida mos yorliq paydo bo‘ladi (yuqoridagi kartochkalarning pastki qismida yozilgan).</div>'''
    html += '''<div class="table-container"><table class="ext-table">
<thead><tr><th>Vosita</th><th>Qayerdan qo‘shiladi</th><th>Nimadan tayyorlanadi</th><th>Tibbiy misol</th><th>Rasmiy hujjatda</th></tr></thead><tbody>
<tr><td><strong>Rasm</strong></td><td>Qo‘shish › Rasmlar</td><td>tayyor fayl (JPG, PNG)</td><td>rentgen, dori qadog‘i, ko‘rsatma rasmi</td><td>o‘rinli bo‘lsa (ilova, hisobot)</td></tr>
<tr><td><strong>Shakllar</strong></td><td>Qo‘shish › Shakllar</td><td>o‘zingiz chizasiz</td><td>blok-sxema, “Diqqat!” izohi, strelka</td><td>kamdan-kam</td></tr>
<tr><td><strong>Kolontitul</strong></td><td>Qo‘shish › Yuqori / Pastki kolontitul, Sahifa raqami</td><td>matn + avtomatik maydon</td><td>referat, hisobot, kasallik tarixi</td><td><b>ha</b> — ko‘p betli hujjatda kerak</td></tr>
<tr><td><strong>WordArt</strong></td><td>Qo‘shish › WordArt</td><td>matn + bezak</td><td>sanitariya byulleteni sarlavhasi</td><td><b>yo‘q</b> (ariza, hisobot, dalolatnoma)</td></tr>
</tbody></table></div>'''
    return section('sec-tools', '1-Qism', 'To‘rtta vosita: qaysi biri nima uchun?',
                   'Word hujjatini matndan tashqari <strong>ko‘rgazmali</strong> qilish uchun to‘rtta vosita bor. Ular bir-biriga o‘xshab ketadi, shuning uchun avval <strong>nima uchun kerakligini</strong> bilib oling, keyin bittalab o‘rganamiz.', html)


# ----------------------------------------------------------------------------
# 2-QISM: RASM
# ----------------------------------------------------------------------------
WRAP_P = (' '.join(VARIANTS[0]['paras'])).replace('"', '')


def sec_pic():
    cards = '<div class="grid-2">'
    cards += op_card('', I_IMG, '1. Rasmni hujjatga qo‘yish', [
        ('Avval', 'keys', 'Kursorni rasm turishi kerak bo‘lgan <b>abzats boshiga</b> qo‘ying — rasm kursor turgan joyga tushadi.'),
        ('Yo‘l', 'mouse', crumb('Qo‘shish', 'Rasmlar (Pictures)', 'Bu qurilma (This Device)') + ' → fayl → <b>Qo‘shish</b>.'),
        ('Tezkor', 'keys', 'Rasmni papkadan Word oynasiga <b>sudrab tashlash</b> yoki nusxalab <span class="key-cap">Ctrl</span> + <span class="key-cap">V</span>.'),
        ('Eslatma', 'mouse', '“Stok rasmlar” va “Onlayn rasmlar” internet va Microsoft 365 talab qiladi. Bizning darsda rasmlar <b>rasmlar</b> papkasida.'),
    ])
    cards += op_card('green', I_IMG, '2. Hajmini o‘zgartirish', [
        ('Qanday', 'mouse', 'Rasmni bosing: atrofida <b>8 ta nuqta</b> paydo bo‘ladi.'),
        ('To‘g‘ri', 'keys', '<b>Burchakdagi</b> nuqtani torting — rasm nisbati saqlanadi, tekis kattalashadi yoki kichrayadi.'),
        ('Xato', 'mouse', '<b>Yon tomondagi</b> (chap, o‘ng, tepa, past) nuqta — rasm cho‘ziladi: dumaloq narsa oval bo‘lib qoladi.'),
        ('Aniq', 'keys', crumb('Rasm formati', 'O‘lcham', 'Eni (Width)') + ' = 5,5 sm. “Nisbatni saqlash” yoqiq bo‘lsa, bo‘yi o‘zi o‘zgaradi.'),
    ])
    cards += op_card('yellow', I_IMG, '3. Kesish va bezash', [
        ('Kesish', 'mouse', crumb('Rasm formati', 'Kesish (Crop / Обрезка)') + ' → qora chiziqlarni ichkariga torting → <span class="key-cap">Enter</span>. Rasm kichraymaydi, ortiqcha qismi yashiriladi.'),
        ('Uslub', 'keys', crumb('Rasm formati', 'Rasm uslublari (Picture Styles)') + ': ramka, soya, yumaloq burchak, aks.'),
        ('Tuzatish', 'mouse', crumb('Rasm formati', 'Tuzatishlar') + ': yorqinlik va kontrast. <b>Fonni olib tashlash</b> (Remove Background) ham shu yorlig‘da.'),
        ('Qaytarish', 'keys', '<b>Rasmni tiklash</b> (Reset Picture) — barcha o‘zgartirishlar bekor qilinadi.'),
    ])
    cards += op_card('rose', I_IMG, '4. Matn bilan o‘rash — eng muhim sozlama', [
        ('Yo‘l', 'mouse', crumb('Rasm formati', 'Matn bilan o‘rash (Wrap Text / Обтекание текстом)') + ' yoki rasm yonidagi kichik <b>Maket parametrlari</b> (Layout Options) tugmasi.'),
        ('Nima', 'keys', 'Rasm matn bilan <b>qanday joylashishini</b> belgilaydi: 7 ta variant.'),
        ('Nega', 'mouse', 'Word’da qo‘yilgan rasm “Matn qatorida” holatida bo‘ladi va <b>sudralmaydi</b>. Rasmni erkin joylash uchun boshqa variant tanlanadi.'),
        ('Bizda', 'keys', 'Amaliy ishda — <b>Kvadrat</b> (Square). Quyidagi laboratoriyada hammasini o‘zingiz ko‘ring.'),
    ])
    cards += '</div>'
    lab = '''<h3 class="sub-title">%s Matn bilan o‘rash laboratoriyasi</h3>
<p class="section-desc" style="margin-bottom:0.4rem;">Tugmalarni bosing: rasm bir xil, matn bir xil — faqat <b>o‘rash usuli</b> o‘zgaradi.</p>
<div class="wl-box">
  <div class="wl-modes" id="wl-modes">
    <button type="button" data-m="inline">Matn qatorida</button><button type="button" data-m="square">Kvadrat</button><button type="button" data-m="tight">Qattiq</button>
    <button type="button" data-m="topbottom">Tepa va past</button><button type="button" data-m="behind">Matn orqasida</button><button type="button" data-m="front">Matn oldida</button>
  </div>
  <div class="wl-grid">
    <div class="wl-page" id="wl-page" data-mode="inline"><div class="wl-pic" id="wl-pic"></div><p id="wl-text">%s</p></div>
    <div class="wl-info" id="wl-info"></div>
  </div>
</div>''' % (ico(I_IMG, 20), WRAP_P)
    return section('sec-pic', '2-Qism', 'Rasmlar bilan ishlash',
                   'Rasm — tayyor fayl. Uni hujjatga qo‘yish oson, lekin chiroyli chiqishi uchun <strong>uchta narsa</strong> kerak: nisbatni buzmasdan kattalashtirish, kerak bo‘lsa kesish va <strong>matn bilan o‘rashni</strong> to‘g‘ri tanlash.',
                   cards + lab)


# ----------------------------------------------------------------------------
# 3-QISM: SHAKLLAR
# ----------------------------------------------------------------------------
def flow_svg():
    boxes = [('Qabul bo‘limi', '#2f6fd0'), ('Shifokor ko‘rigi', '#2e9e5b'), ('Davolash', '#e9a420')]
    out = ''
    for i, (t, c) in enumerate(boxes):
        x = 20 + i * 220
        out += '<rect x="%d" y="30" width="160" height="60" rx="10" fill="%s"/><text x="%d" y="66" font-size="17" font-weight="700" fill="#fff" text-anchor="middle">%s</text>' % (x, c, x + 80, t)
        if i < 2:
            out += '<path d="M%d 60h40" stroke="#555" stroke-width="4"/><polygon points="%d,48 %d,60 %d,72" fill="#555"/>' % (x + 166, x + 206, x + 218, x + 206)
    out += '<g transform="translate(540 0)"><path d="M0 24h120a10 10 0 0 1 10 10v36a10 10 0 0 1 -10 10h-80l-20 18v-18h-20a10 10 0 0 1 -10 -10v-36a10 10 0 0 1 10 -10z" fill="#d9534f" transform="translate(0 0)"/>'
    out += '<text x="60" y="58" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">Diqqat!</text></g>'
    return '<div class="shape-demo"><svg viewBox="0 0 700 110" width="100%%" style="display:block;font-family:Calibri,Arial,sans-serif">%s</svg></div>' % out


def sec_shape():
    c = '<div class="grid-2">'
    c += op_card('', I_SHAPE, '1. Shakl chizish', [
        ('Yo‘l', 'mouse', crumb('Qo‘shish', 'Shakllar (Shapes / Фигуры)') + ' → ro‘yxatdan shakl → varaqda sichqonchani <b>bosib turib torting</b>.'),
        ('Guruhlar', 'keys', 'Chiziqlar, To‘rtburchaklar, Asosiy shakllar, Strelkalar, Blok-sxema, Yulduzlar va lentalar, <b>Izohlar</b> (Callouts).'),
        ('Shift', 'mouse', '<span class="key-cap">Shift</span> ni bosib turib chizsangiz — <b>to‘g‘ri nisbat</b>: aylana, kvadrat, to‘g‘ri chiziq, muntazam yulduz.'),
        ('Nusxa', 'keys', '<span class="key-cap">Ctrl</span> ni bosib turib shaklni sudrang — <b>nusxasi</b> hosil bo‘ladi.'),
    ])
    c += op_card('green', I_SHAPE, '2. Shakl ichiga matn yozish', [
        ('Yo‘l', 'mouse', 'Shaklni <b>o‘ng tugma</b> bilan bosing › <b>Matn qo‘shish</b> (Add Text / Добавить текст). Yoki shaklni tanlab, to‘g‘ridan-to‘g‘ri yozing.'),
        ('Matn', 'keys', 'Shrift va o‘lchami <b>Bosh sahifa</b> yorlig‘ida o‘zgartiriladi: avval matnni belgilang.'),
        ('Sig‘masa', 'mouse', 'Matn shakldan katta bo‘lsa — shaklni kattalashtiring yoki shriftni kichraytiring. Alohida “Matn maydoni” qo‘shish shart emas.'),
    ])
    c += op_card('yellow', I_SHAPE, '3. Rang berish va bezash', [
        ('Yo‘l', 'mouse', crumb('Shakl formati', 'Shakl uslublari (Shape Styles)') + ' — tayyor ranglar.'),
        ('To‘ldirish', 'keys', '<b>Shakl to‘ldirish</b> (Shape Fill) — ichki rang; <b>Shakl konturi</b> (Shape Outline) — chiziq rangi va qalinligi.'),
        ('Effekt', 'mouse', '<b>Shakl effektlari</b> (Shape Effects): soya, yaltirash, hajm.'),
    ])
    c += op_card('rose', I_SHAPE, '4. Guruhlash va tartib', [
        ('Tanlash', 'keys', '<span class="key-cap">Ctrl</span> ni bosib turib shakllarni birin-ketin bosing — hammasi tanlanadi.'),
        ('Guruhlash', 'mouse', 'O‘ng tugma › <b>Guruhlash</b> (Group / Группировать) › <b>Guruhlash</b>. Endi shakllar bitta butun bo‘lib siljiydi va o‘lchami o‘zgaradi.'),
        ('Tartib', 'keys', 'Shakllar ustma-ust tushganda: <b>Oldinga olib chiqish</b> / <b>Orqaga yuborish</b> (Bring Forward / Send Backward).'),
        ('Eslatma', 'mouse', 'Guruhni yechish: o‘ng tugma › Guruhlash › <b>Guruhni yechish</b>.'),
    ])
    c += '</div>' + flow_svg()
    c += '''<div class="callout warn">%s<span><strong>Ehtiyot bo‘ling:</strong> Word’da chizilgan shakl odatda <b>matn oldida</b> turadi va matnni yopib qo‘yishi mumkin. Shaklni matn ustiga tashlab yubormang: <b>Shakl formati › Matn bilan o‘rash › Kvadrat</b> qiling yoki bo‘sh joyga qo‘ying.</span></div>''' % ico('<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>', 18, 2.4)
    return section('sec-shape', '3-Qism', 'Shakllar bilan ishlash',
                   'Shakl — Word ichida o‘zingiz chizadigan figura. Bitta shakl kam foyda beradi, lekin bir nechtasi <strong>guruhlansa</strong>, blok-sxema, izoh va ko‘rsatkichlar tayyorlash mumkin.', c)


# ----------------------------------------------------------------------------
# 4-QISM: KOLONTITUL VA AVTOMATIK SAHIFA RAQAMI
# ----------------------------------------------------------------------------
def sec_kol():
    zones = kol_pages([
        dict(label='1-bet', h=dict(c='Hamshiralik tarixi'), f=dict(r='1'), hline=True),
        dict(label='2-bet', h=dict(c='Hamshiralik tarixi'), f=dict(r='2'), hline=True),
        dict(label='3-bet', h=dict(c='Hamshiralik tarixi'), f=dict(r='3'), hline=True)])
    intro = ('<div class="lead-line"><strong>Kolontitul</strong> (Header &amp; Footer / Колонтитул) — sahifaning <b>yuqori va pastki chetidagi</b> (rasmda ko‘k zona) yozuv. '
             'U <b>barcha betlarda takrorlanadi</b>: hujjat nomi, sana, muallif va <b>sahifa raqami</b> shu yerda yoziladi. '
             'Muhim qoida: sahifa raqami <b>qo‘lda yozilmaydi</b> — u <b>avtomatik maydon</b>, bet qo‘shilsa yoki o‘chirilsa, raqamlar o‘zi to‘g‘rilanadi.</div>'
             '<div class="fig-box"><div style="width:100%%;max-width:34rem;margin:0 auto">%s</div></div>' % zones)
    c = '<div class="grid-2">'
    c += op_card('yellow', I_KOL, '1. Kolontitul qo‘yish va yopish', [
        ('Yo‘l', 'mouse', crumb('Qo‘shish', 'Kolontitul guruhi', 'Yuqori kolontitul / Pastki kolontitul') + ' → <b>Bo‘sh</b> (Blank).'),
        ('Tezkor', 'keys', 'Varaqning <b>yuqori yoki pastki chetiga ikki marta bosing</b> — kolontitul rejimi ochiladi. Asosiy matn xira bo‘lib qoladi.'),
        ('Yozish', 'mouse', 'Matnni yozing; <span class="key-cap">Ctrl</span> + <span class="key-cap">E</span> markazga, <span class="key-cap">Ctrl</span> + <span class="key-cap">R</span> o‘ngga. Shriftni <b>Bosh sahifa</b> da o‘zgartiring (odatda 10 pt).'),
        ('Yopish', 'keys', '<span class="key-cap">Esc</span> yoki <b>Kolontitulni yopish</b> (Close Header and Footer) yoki asosiy matnga ikki marta bosish.'),
    ])
    c += op_card('green', I_KOL, '2. Avtomatik sahifa raqami', [
        ('Yo‘l', 'mouse', crumb('Qo‘shish', 'Sahifa raqami (Page Number)') + ' → joyni tanlang: <b>Sahifaning yuqori / pastki qismi</b> → uslub (masalan, Oddiy raqam 3 — o‘ngda).'),
        ('Maydon', 'keys', 'Raqamni bosing: <b>kulrang fon</b> paydo bo‘lsa — bu maydon (avtomatik). Bet qo‘shsangiz, raqamlar o‘zi o‘zgaradi.'),
        ('X dan Y', 'mouse', '«Sahifa 2 dan 6» — <b>Qo‘shish › Tezkor bloklar › Maydon</b>: <b>Page</b> (joriy bet) va <b>NumPages</b> (jami betlar).'),
        ('Format', 'keys', crumb('Sahifa raqami', 'Sahifa raqami formati') + ': rim raqamlari (I, II, III) va <b>Boshlash</b> (Start at) — qaysi raqamdan boshlash.'),
    ])
    c += op_card('rose', I_KOL, '3. Maxsus kolontitul', [
        ('Yo‘l', 'mouse', 'Kolontitul ichida <b>Kolontitul asboblari › Konstruktor</b> (Header &amp; Footer Design) yorlig‘i.'),
        ('1-bet', 'keys', '<b>Birinchi sahifa uchun alohida kolontitul</b> (Different First Page): titul varag‘ida kolontitul va raqam ko‘rinmaydi.'),
        ('Toq/juft', 'mouse', '<b>Toq va juft sahifalar uchun har xil</b> (Different Odd &amp; Even): ikki tomonlama bosma uchun — raqam doim tashqi chetda.'),
        ('Eslatma', 'keys', 'Hujjatda sana kerak bo‘lsa: <b>Konstruktor › Sana va vaqt</b> → «<b>Avtomatik yangilash</b>» belgisi.'),
    ])
    c += op_card('purple', I_KOL, '4. Bo‘limlar va raqamlashni qayta boshlash', [
        ('Bo‘lim', 'mouse', crumb('Maket', 'Uzilishlar', 'Keyingi sahifa (Next Page)') + ' — hujjat bo‘limlarga bo‘linadi.'),
        ('Bog‘lash', 'keys', 'Yangi bo‘limda kolontitul boshqacha bo‘lishi uchun <b>Oldingi bilan bog‘lash</b> (Link to Previous) tugmasini <b>o‘chiring</b>.'),
        ('Raqam', 'mouse', crumb('Sahifa raqami formati', 'Boshlash') + ' = 1 — asosiy qism 1-betdan boshlansin; titul va mundarija — rim raqamlarida.'),
    ])
    c += '</div>'
    lab = '''<h3 class="sub-title">%s Kolontitul laboratoriyasi</h3>
<p class="section-desc" style="margin-bottom:0.4rem;">Rejimni tanlang va <b>yangi bet qo‘shib</b> ko‘ring: avtomatik raqamlarda tartib o‘zi saqlanadi, qo‘lda yozilgan raqamlarda esa buziladi.</p>
<div class="kl-box">
  <div class="wl-modes" id="kl-modes">
    <button type="button" data-m="same">Hamma betda bir xil</button><button type="button" data-m="first">Birinchi bet alohida</button><button type="button" data-m="oddeven">Toq va juft betlar har xil</button>
  </div>
  <div class="wl-modes" id="kl-num">
    <button type="button" data-n="auto">Raqam: avtomatik (maydon)</button><button type="button" data-n="manual">Raqam: qo‘lda yozilgan</button>
    <button type="button" id="kl-add">+ 2-betdan keyin yangi bet qo‘shish</button><button type="button" id="kl-reset">Boshidan</button>
  </div>
  <div class="kl-pages" id="kl-pages"></div>
  <div class="wl-info" id="kl-info" style="margin-top:0.8rem"></div>
</div>''' % ico(I_KOL, 20)
    tip = '''<div class="callout warn">%s<span><strong>Kolontitul — sahifa chekkasida, asosiy matnda emas.</strong> Pastki chekkaga «2» deb qo‘lda yozib qo‘ysangiz, u oddiy matn bo‘ladi: bet qo‘shilganda yoki matn siljiganda raqam boshqa betga o‘tib ketadi. Shuning uchun raqamni faqat <b>Qo‘shish › Sahifa raqami</b> orqali qo‘ying.</span></div>''' % ico('<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>', 18, 2.4)
    return section('sec-kol', '4-Qism', 'Kolontitul va avtomatik sahifa raqami',
                   'Ko‘p betli hujjat (referat, hisobot, kurs ishi) uchun <strong>kolontitul</strong> va <strong>avtomatik sahifa raqami</strong> zarur. Uzun matnni qo‘lda raqamlash ham xato, ham ko‘p vaqt oladi — Word buni o‘zi bajaradi.', intro + c + lab + tip)


# ----------------------------------------------------------------------------
# 5-QISM: WORDART
# ----------------------------------------------------------------------------
def sec_word():
    demo = '''<div class="wa-row">
  <div class="wa-cell"><div class="wa-txt a">QO‘L YUVING</div><small>To‘ldirish — gradient, kontur, soya</small></div>
  <div class="wa-cell"><div class="wa-txt b">SALOMATLIK</div><small>Faqat kontur (to‘ldirishsiz)</small></div>
  <div class="wa-cell">%s<small>Transformatsiya: Yoy (Arch Up)</small></div>
</div>''' % wordart('SOG‘LOM TURMUSH', 'arch', '#7be495', '#12803b', '#0a4a22', w=680, h=130, uid='dm')
    c = '<div class="grid-2">'
    c += op_card('rose', I_WORD, '1. WordArt qo‘yish', [
        ('Yo‘l', 'mouse', crumb('Qo‘shish', 'Matn guruhi', 'WordArt') + ' → uslub tanlang.'),
        ('Matn', 'keys', 'Hujjatda “<b>Bu yerga matn kiriting</b>” (Your text here) yozuvli ramka paydo bo‘ladi. Matn belgilangan — shunchaki o‘z matningizni yozing.'),
        ('Joy', 'mouse', 'Ramkani sudrab joyiga qo‘ying. Boshqa matn bilan aralashmasligi uchun: <b>Matn bilan o‘rash › Tepa va past</b>.'),
    ])
    c += op_card('purple', I_WORD, '2. Bezash', [
        ('Yo‘l', 'mouse', crumb('Shakl formati', 'WordArt uslublari') + ' guruhi.'),
        ('Rang', 'keys', '<b>Matn to‘ldirish</b> (Text Fill) — harf rangi; <b>Matn konturi</b> (Text Outline) — harf chizig‘i.'),
        ('Effekt', 'mouse', '<b>Matn effektlari</b> (Text Effects): Soya, Aks, Yaltirash, <b>Transformatsiya</b> (Transform).'),
        ('Egri', 'keys', 'Transformatsiya › <b>Yoy</b> (Arch) yoki <b>To‘lqin</b> (Wave) — yozuv egriladi.'),
    ])
    c += '</div>'
    rule = '''<div class="callout warn">%s<span><strong>Qachon ishlatiladi, qachon ishlatilmaydi.</strong> WordArt — <b>plakat, e’lon, sanitariya byulleteni va taqdimot sarlavhasi</b> uchun. <b>Ariza, tushuntirish xati, hisobot, dalolatnoma</b> kabi rasmiy hujjatlarda WordArt ishlatilmaydi: 9-darsdagi talab — Times New Roman, 14 pt, qalin va markazda. Bir varaqda ko‘pi bilan <b>bitta</b> WordArt bo‘lsin.</span></div>''' % ico('<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>', 18, 2.4)
    rule += '''<div class="callout">%s<span><b>WordArt va oddiy matn effekti farqi:</b> <b>Bosh sahifa › Matn effektlari</b> (A harfi) — oddiy matnga bezak beradi, matn qatorda qoladi. <b>WordArt</b> esa alohida ramka: uni sudrab surish, aylantirish va egrilash mumkin.</span></div>''' % ico('<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>', 18, 2.4)
    return section('sec-word', '5-Qism', 'WordArt: bezakli yozuv',
                   '<strong>WordArt</strong> matnni <strong>rangli, konturli, soyali va egri</strong> qiladi. Kuchli vosita, lekin uni me’yorida ishlatish kerak: ko‘p bezak hujjatni o‘qishga qiyin qiladi.', demo + c + rule)


# ----------------------------------------------------------------------------
# 6-QISM: TRENAJYOR
# ----------------------------------------------------------------------------
QUIZ = [
    ['Bemorning rentgen suratini hujjatga kiritish kerak.', 'rasm', 'Tayyor surat fayli — <b>Rasm</b>.'],
    ['“Qabul bo‘limi → Ko‘rik → Davolash” blok-sxemasini qutilar va strelkalarni o‘zingiz joylashtirib chizish.', 'shakl', 'Erkin chizish — <b>Shakllar</b> (to‘rtburchak va strelkalar).'],
    ['Referatning har bir betida tepada mavzu nomi, pastda sahifa raqami bo‘lishi kerak.', 'kolontitul', 'Barcha betlarda takrorlanadigan yozuv — <b>Kolontitul</b>.'],
    ['Sanitariya byulleteniga rangli, yoysimon “QO‘LINGIZNI YUVING!” sarlavhasi.', 'wordart', 'Bezakli, egri sarlavha — <b>WordArt</b>.'],
    ['Ariza matnining tepasiga “ARIZA” so‘zini chiroyli, rangli qilib yozish.', 'hech', 'Rasmiy hujjat sarlavhasi oddiy: Times New Roman, qalin, markazda. <b>Hech biri</b> — WordArt rasmiy hujjatga qo‘yilmaydi.'],
    ['Rasm ustiga “Diqqat!” yozuvli yulduzcha qo‘yish.', 'shakl', 'Ichiga matn yoziladigan yulduz — <b>Shakl</b>.'],
    ['Telefondan olingan fotosuratning chetini kesib, ortiqcha qismini olib tashlash.', 'rasm', 'Rasmni qirqish — <b>Rasm</b> (Rasm formati › Kesish).'],
    ['20 betli hisobotni raqamlash: o‘rtaga yangi bet qo‘shilsa, raqamlar o‘zi to‘g‘rilansin.', 'kolontitul', 'Avtomatik raqam — <b>Kolontitul</b> (Qo‘shish › Sahifa raqami), qo‘lda yozilmaydi.'],
    ['Hisobotning sarlavhasini yirik rangli WordArt bilan bezash.', 'hech', 'Hisobot — rasmiy hujjat, <b>hech biri</b>. Sarlavha oddiy qalin matn bo‘ladi.'],
    ['Plakatdagi sarlavhaga soya va kontur berish, ramkasini sudrab surish.', 'wordart', 'Soyali, konturli, sudraladigan ramka — <b>WordArt</b>.'],
]


def sec_train():
    body = '''<div class="fx-box">
  <div class="fx-head"><div class="goal-progress"><i id="qz-bar"></i></div><span id="qz-score">0 / 10</span><button type="button" class="fmt-reset" id="qz-reset">Boshidan</button></div>
  <ol class="fx-list" id="qz-list"></ol>
  <div class="goal-status" id="qz-status">Javob berilgan: 0 ta</div>
</div>'''
    return section('sec-train', '6-Qism • Trenajyor', 'Qaysi vosita kerak?',
                   'Har bir vaziyat uchun mos vositani tanlang. E’tibor bering: ba’zi vaziyatlarda to‘g‘ri javob — <strong>hech biri</strong>.', body)


# ----------------------------------------------------------------------------
# 7-QISM: AMALIY ISH
# ----------------------------------------------------------------------------
def sec_practice():
    steps = '''<div class="timeline steps-flow">
<div class="tl-item key"><strong>1. Variantni oling</strong>Tarqatmaga F.I.O., guruh va sanani yozing.</div>
<div class="tl-item"><strong>2. Fayl va sahifa</strong>Yangi hujjat → <code>Familiya_V№.docx</code>; maydonlar 2 sm.</div>
<div class="tl-item"><strong>3. Matn</strong>Namunadagi ikki abzatsni tering va formatlang.</div>
<div class="tl-item"><strong>4. WordArt va rasm</strong>Sarlavha, rasm, Kvadrat o‘rash, uslub.</div>
<div class="tl-item"><strong>5. Shakllar va kolontitul</strong>Izoh + yulduz → guruhlash; yuqori va pastki kolontitul.</div>
<div class="tl-item key"><strong>6. Tekshirib topshiring</strong>Bitta betga sig‘dimi? <span class="key-cap">Ctrl</span> + <span class="key-cap">S</span>, o‘qituvchini chaqiring.</div>
</div>'''
    cards = ''
    for V in VARIANTS:
        hfv = V['hf']
        cards += '''<article class="var-card" style="--vc:%(c)s">
<div class="var-top"><span class="var-num">%(n)d-variant</span><span class="var-int">Kolontitul</span></div>
<h3>%(name)s</h3>
<p>%(about)s</p>
<div class="var-sa">Yuqori: <b>%(hh)s</b> • rasm: <b>%(pic)s</b></div>
<button type="button" class="var-preview-btn" data-variant="%(n)d">Namunani ko‘rish</button>
<div class="var-actions">
<a href="./tarqatma/%(n)d-variant.pdf" class="nav-btn" download>PDF yuklab olish</a>
<a href="./tarqatma/rasmlar/%(pic)s" class="nav-btn" download>Rasm fayli</a>
</div>
<template class="var-sample">%(sample)s</template>
</article>
''' % dict(n=V['n'], name=V['name'], about=V['about'], c=V['accent'], hh=' / '.join(hfv['h'].values()), pic=V['pic']['file'],
           sample=sample_sheet(V, IMG_FROM_LESSON, label=False, markers=True))
    downloads = '''<div class="var-all">
<a href="./tarqatma/barcha-variantlar.pdf" class="nav-btn nav-btn-primary" download>%s<span>Barcha variantlar — bitta PDF (12 bet)</span></a>
<a href="./tarqatma/rasmlar.zip" class="nav-btn" download><span>Rasmlar to‘plami (ZIP, 8 ta rasm)</span></a>
<a href="./tarqatma/barcha-variantlar.pdf" class="nav-btn" target="_blank" rel="noopener"><span>Ochib ko‘rish / chop etish</span></a>
</div>
<p class="var-note" style="margin-top:0.6rem;">Dars oldidan <b>rasmlar</b> papkasini (yoki ZIP’ni) talabalar kompyuterlariga nusxalab qo‘ying — rasmlar internetsiz ishlatiladi.</p>''' % ico('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>', 15, 2.5)

    topic_cards = ''
    for T in TOPICS:
        for S in T['sheets']:
            nm = '%d-%s-%s' % (T['n'], T['key'], S['v'])
            topic_cards += ('<article class="var-card" style="--vc:%s"><div class="var-top"><span class="var-num">%s • %s</span><span class="var-int">20 ball</span></div>'
                            '<h3>%s</h3><p>%d ta talab + 3 ta yozma savol</p>'
                            '<div class="var-actions"><a href="./tarqatma/mavzu-varaqlari/%s.pdf" class="nav-btn" download>PDF yuklab olish</a></div></article>\n'
                            % (T['color'], T['name'], S['v'], S['title'], len(S['rows']), nm))
    topics_html = ('<h3 class="sub-title">%s Mavzu bo‘yicha alohida varoqlar (jiddiyroq topshiriqlar)</h3>'
                   '<p class="section-desc" style="margin-bottom:1rem;">Har bir mavzu — <strong>alohida A4 varoq</strong>: vaziyat, 8–11 ta aniq talab (o‘lcham, rang, yo‘l), baholash jadvali (20 ball) va 3 ta yozma savol. '
                   'Har mavzuda <strong>A</strong> va <strong>B</strong> variant: yonma-yon o‘tirganlarga turli variant bering.</p>'
                   '<div class="var-grid">\n%s</div>'
                   '<div class="var-all"><a href="./tarqatma/mavzu-varaqlari/barcha-mavzu-varaqlari.pdf" class="nav-btn nav-btn-primary" download><span>Barcha 8 varoq — bitta PDF</span></a>'
                   '<a href="./tarqatma/mavzu-varaqlari/kalit-oqituvchi.pdf" class="nav-btn teacher-only" download><span>O‘qituvchi kaliti (kutilgan natija, javoblar)</span></a></div>'
                   % (ico('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>', 20, 2.2), topic_cards))

    ready_html = ('<h3 class="sub-title">%s Tayyor materiallar (ko‘rsatmasiz, to‘g‘ridan-to‘g‘ri beriladi)</h3>'
                  '<p class="section-desc" style="margin-bottom:1rem;">Har bir varoq — tayyor: topshiriq mazmuni, tayyor matn va nishon rasm/sxema. Alohida varoq sifatida chop etib beriladi.</p>'
                  '<div class="var-grid">'
                  '<article class="var-card" style="--vc:#7a3fb5"><div class="var-top"><span class="var-num">35 variant</span><span class="var-int">Anatomiya + Farmakologiya</span></div><h3>Rasm va ma’lumot topish</h3>'
                  '<p>26 ta anatomiya va 9 ta farmakologiya mavzusi: rasm qidirish so‘zlari, tayyor 5 bandli ma’lumot, WordArt sarlavha, «Bilasizmi?» yozuvi. Birinchi bet — WordArt’li <b>namuna</b>.</p>'
                  '<div class="var-actions"><a href="./tarqatma/tayyor/anatomiya-farmakologiya-35-variant.pdf" class="nav-btn nav-btn-primary" download>Hammasi — bitta PDF (36 bet)</a>'
                  '<a href="./tarqatma/tayyor/anatomiya-farmakologiya/namuna-wordart.pdf" class="nav-btn" download>Namuna (WordArt)</a></div>'
                  '<p class="var-note" style="margin-top:0.5rem;">Alohida varoqlar: <code>tarqatma/tayyor/anatomiya-farmakologiya/variant-01.pdf … variant-35.pdf</code></p></article>'
                  '<article class="var-card" style="--vc:#2e9e5b"><div class="var-top"><span class="var-num">6 variant</span><span class="var-int">Shakllar</span></div><h3>Shakllardan tayyor rasm</h3>'
                  '<p>Birinchi yordam belgisi, dori plakati, a’zolar sxemasi, palata rejasi, qon aylanishi, xavfsizlik belgilari — nishon rasm va shakllar ro‘yxati.</p>'
                  '<div class="var-actions"><a href="./tarqatma/tayyor/shakllar-6-variant.pdf" class="nav-btn nav-btn-primary" download>6 variant — bitta PDF</a></div>'
                  '<p class="var-note" style="margin-top:0.5rem;">Alohida: <code>tarqatma/tayyor/shakllar/variant-1.pdf … 6</code></p></article>'
                  '<article class="var-card" style="--vc:#e9a420"><div class="var-top"><span class="var-num">6 variant</span><span class="var-int">Kolontitul</span></div><h3>Kolontitul va sahifa raqami</h3>'
                  '<p>Referat, kuzatuv varaqasi, hisobot (toq/juft), yo‘riqnoma, kurs ishi (2 bo‘lim), kasallik tarixi — nishon ko‘rinish, kolontitul matni va sozlamalar.</p>'
                  '<div class="var-actions"><a href="./tarqatma/tayyor/kolontitul-6-variant.pdf" class="nav-btn nav-btn-primary" download>6 variant — bitta PDF</a></div>'
                  '<p class="var-note" style="margin-top:0.5rem;">Alohida: <code>tarqatma/tayyor/kolontitul/variant-1.pdf … 6</code></p></article>'
                  '</div>' % ico('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>', 20, 2.2))
    crit = '''<h3 class="sub-title">%s Ish qanday baholanadi?</h3>
<p class="section-desc" style="margin-bottom:1rem;">10 ta mezon, har biri <strong>0,5 ball</strong>, jami <strong>5 ball</strong>. <strong>4,5–5</strong> ball — «5», <strong>3,5–4</strong> — «4», <strong>2,5–3</strong> — «3», undan kam — qayta topshiriladi.</p>
<div class="table-container"><table class="ext-table crit-table"><thead><tr><th>№</th><th>Mezon</th><th>Nimaga qaraladi</th><th>Ball</th></tr></thead><tbody id="crit-body"></tbody></table></div>''' % ico('<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>', 20, 2.2)
    tips = '''<div class="grid-2" style="margin-top:1.15rem;">
<div class="concept-card"><h3>Ko‘p uchraydigan xatolar</h3><ul class="check-list cross">
<li>Rasm yon nuqtadan tortilib, <b>cho‘zilib</b> ketgan.</li>
<li>Rasm “Matn qatorida” holatida qolgan va sudralmayapti.</li>
<li>Ikkita shakl <b>guruhlanmagan</b> — bittasini siljitganda ikkinchisi qoladi.</li>
<li>Sahifa raqami <b>qo‘lda yozilgan</b> (bosganda kulrang fon yo‘q).</li>
<li>Sarlavha WordArt emas, oddiy matnga effekt berilgan.</li>
<li>Hamma narsa 2-betga o‘tib ketgan (rasm juda katta, ortiqcha <span class="key-cap">Enter</span>).</li>
</ul></div>
<div class="concept-card"><h3>Topshirishdan oldin o‘zingizni tekshiring</h3><ul class="check-list">
<li>Har bir elementni <b>bir marta bosing</b>: Rasm formati va Shakl formati chiqyaptimi? Kolontitulga ikki marta bosganda Kolontitul asboblari ochilyaptimi?</li>
<li>Rasm doira joyida doira, to‘rtburchak joyida to‘rtburchak bo‘lib turibdimi?</li>
<li>Matn rasmni <b>aylanib o‘tyaptimi</b>?</li>
<li>Shakllardan birini bosing: ikkalasi birga tanlanyaptimi?</li>
<li><span class="key-cap">Ctrl</span> + <span class="key-cap">P</span> — oldindan ko‘rishda namunaga o‘xshaydimi, bitta betmi?</li>
</ul></div></div>'''
    return section('sec-practice', '7-Qism • Kompyuterda bajariladi', 'Amaliy ish: tibbiy axborot varaqasi',
                   'O‘qituvchi har bir talabaga bitta variant tarqatmasini beradi. Tarqatmaning 1-betida topshiriq sharti va baholash jadvali, 2-betida esa tayyor varaqning <strong>haqiqiy A4 o‘lchamdagi namunasi</strong>. Namunadagi raqamlar vositani bildiradi: <strong>1 — WordArt, 2 — Rasm, 3 — Shakllar, 4 — Kolontitul</strong>. Raqamlar hujjatga yozilmaydi.',
                   steps + '<h3 class="sub-title">%s 6 ta variant</h3>\n<!-- VARIANTS_START -->\n<div class="var-grid">\n%s</div>\n<!-- VARIANTS_END -->\n' % (ico('<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>', 20, 2.2), cards)
                   + downloads + ready_html + topics_html + crit + tips)


# ----------------------------------------------------------------------------
# O'QITUVCHI BO'LIMLARI
# ----------------------------------------------------------------------------
def sec_plan():
    rows = [
        ('0–5', 'Kirish', 'Doskada yoki proyektorda ikki varaq ko‘rsating: faqat matndan iborat qo‘l yuvish qoidasi va <b>1-variant namunasi</b> (rasm + sxema + sarlavha). <em>“Qaysi birini uzoqdan o‘qiysiz? Qaysi biri yodda qoladi?”</em> deb so‘rang. Shundan so‘ng to‘rt vositani nomlang.', 'Javob beradi, to‘rt vosita nomini daftarga yozadi.'),
        ('5–13', '<b>1. Rasm</b>', '<span class="pl-tag">Ko‘rsating, 3 daq</span> rasm qo‘yish → burchakdan kichraytirish → <b>yon nuqtadan cho‘zib ko‘rsating</b> (ataylab!) → <b>Kvadrat</b> o‘rash → sudrab joylash. Keyin <b>wrap laboratoriyasini</b> proyektorda 6 holat bilan aylantiring.', '<span class="pl-tag pr">Birga, 5 daq</span> rasmni qo‘yib, Kvadrat qiladi va abzats boshiga joylaydi.'),
        ('13–21', '<b>2. Shakllar</b>', '<span class="pl-tag">Ko‘rsating, 3 daq</span> izoh chizing, ichiga matn yozing, rang bering, ikkinchi shaklni <span class="key-cap">Shift</span> bilan chizing. <b>Guruhlamasdan bittasini siljiting</b> — ikkinchisi qolib ketadi; so‘ng guruhlang.', '<span class="pl-tag pr">Birga, 5 daq</span> ikki shakl chizadi, guruhlaydi.'),
        ('21–30', '<b>3. Kolontitul</b>', '<span class="pl-tag">Ko‘rsating, 4 daq</span> 4 betli hujjat yarating (<b>=rand(8,6)</b> + Enter). Yuqori kolontitul → matn; <b>Sahifa raqami</b> → pastda. Raqam <b>maydon</b> ekanini (kulrang fon) ko‘rsating, o‘rtaga bet qo‘shib raqamlar o‘zgarishini isbotlang; so‘ng <b>birinchi sahifa alohida</b> belgisini yoqing. <b>Laboratoriyani</b> proyektorda aylantiring.', '<span class="pl-tag pr">Birga, 5 daq</span> yuqori kolontitul va avtomatik raqam, titulda raqamsiz.'),
        ('30–36', '<b>4. WordArt</b>', 'WordArt qo‘ying, <b>Transformatsiya › Yoy</b> ko‘rsating. Asosiy fikr: <em>“Qayerda mumkin, qayerda mumkin emas?”</em> — 9-darsdagi rasmiy talablar bilan bog‘lang.', 'Sarlavha yozadi, effekt beradi.'),
        ('36–42', 'Trenajyor', '“Qaysi vosita?” — 10 savol. Juftlikda ishlashga ruxsat bering, xatolar bo‘yicha qisqa muhokama qiling (ayniqsa “hech biri” javoblari).', 'Juftlikda javob beradi.'),
        ('42–72', '<b>Amaliy ish</b>', 'Variant tarqating (yonma-yon o‘tirganlarga <b>turli variant</b>). Aylanib yurib, quyidagi xatolarga e’tibor bering. 62-daqiqada: <em>“10 daqiqa qoldi, kolontitulga o‘ting”</em>.', 'Tarqatmadagi 11 qadamni bajaradi, faylni saqlaydi.'),
        ('72–80', 'Topshirish va xulosa', 'Ishlarni <b>elementni bosib yorliqni ko‘rish</b> usuli bilan tekshiring (2–3 daq har biri). Ulgurmaganlar — keyingi darsda. Xulosa: har bir vosita haqida bir jumla.', 'Faylni ko‘rsatadi, 4 jumla bilan xulosa qiladi.'),
    ]
    t = '<div class="table-container"><table class="ext-table plan-table"><thead><tr><th>Daqiqa</th><th>Blok</th><th>O‘qituvchi nima qiladi</th><th>Talaba nima qiladi</th></tr></thead><tbody>'
    for a, b, c, d in rows:
        t += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (a, b, K(c), d)
    t += '</tbody></table></div>'
    t += '<p class="var-note" style="margin-top:0.6rem;">Reja 80 daqiqalik dars (bir juftlik) uchun. Dars 45 daqiqa bo‘lsa: 1–4 bloklarni va trenajyorni shu darsda, amaliy ishni keyingi darsda o‘tkazing.</p>'
    boxes = '''<div class="grid-2">
<div class="say-box"><h4>Har bir vositani bitta jumlada ayting</h4><ul>
<li><em>Rasm</em> — tayyor surat, siz uni faqat joyiga qo‘yasiz.</li>
<li><em>Shakl</em> — o‘zingiz chizadigan figura, ichiga matn yozish mumkin.</li>
<li><em>Kolontitul</em> — sahifa chetidagi takrorlanuvchi yozuv; raqamni Word o‘zi qo‘yadi.</li>
<li><em>WordArt</em> — plakat sarlavhasi uchun bezakli yozuv; rasmiy hujjatga qo‘yilmaydi.</li></ul></div>
<div class="say-box"><h4>Uch usul, ular yaxshi ishlaydi</h4><ul>
<li><em>Ko‘rsat → birga qil → o‘zing qil.</em> Har blokda nazariya 3–4 daqiqadan oshmasin, keyin darhol mini-topshiriq.</li>
<li><em>Xatoni ataylab qiling.</em> Rasmni yon nuqtadan cho‘zing, shaklni guruhlamasdan siljiting — talaba o‘z ko‘zi bilan ko‘rsa, yodda qoladi.</li>
<li><em>Misolni tibbiyotdan oling:</em> qo‘l yuvish, infeksiya zanjiri, bo‘lim tuzilmasi — talaba uchun tanish va foydali.</li></ul></div>
</div>
<div class="say-box"><h4>Amaliy ish paytida eng ko‘p so‘raladigan savollar</h4><ul>
<li><em>“Rasm qimirlamayapti!”</em> — “Matn qatorida” holati. <b>Matn bilan o‘rash › Kvadrat</b> qildiring.</li>
<li><em>“Rasm cho‘zilib ketdi.”</em> — yon nuqtadan tortilgan. <span class="key-cap">Ctrl</span> + <span class="key-cap">Z</span>, keyin burchakdan; yoki <b>Rasmni tiklash</b>.</li>
<li><em>“Shaklga yozgan matnim ko‘rinmayapti.”</em> — shrift rangi fon rangi bilan bir xil yoki shakl kichik.</li>
<li><em>“Sahifa raqami hamma betda bir xil (1)!”</em> — raqam qo‘lda yozilgan yoki har bir betga alohida qo‘yilgan. Faqat <b>bitta</b> kolontitulda <b>Qo‘shish › Sahifa raqami</b> bo‘lsin.</li>
<li><em>“Titul varag‘ida ham raqam chiqyapti.”</em> — <b>Konstruktor › Birinchi sahifa uchun alohida kolontitul</b> belgilanmagan.</li>
<li><em>“Hammasi ikkinchi betga o‘tib ketdi.”</em> — rasm kattaligini kamaytiring, ortiqcha <span class="key-cap">Enter</span>larni o‘chiring (¶ ni yoqing).</li>
<li><em>“WordArt matnini o‘zgartira olmayapman.”</em> — ramka ichiga bosing, matnni belgilab yozing.</li></ul></div>'''
    return section('sec-plan', '8-Qism • Faqat o‘qituvchi', 'Darsni qanday o‘tkazish: reja va tushuntirish',
                   'Dars to‘rtta blokdan iborat. Har bir blok bir xil: <strong>o‘qituvchi ko‘rsatadi, talaba darhol takrorlaydi, mini-topshiriq bajariladi</strong>. Nazariyani uzoq gapirmang — talaba tugmani o‘zi bosganda o‘rganadi.', t + boxes, teacher=True)


def sec_check():
    body = '''<div class="var-all" style="margin-top:0;">
<a href="./tarqatma/oqituvchi-qollanma.pdf" class="nav-btn nav-btn-primary" download>%s<span>Tekshirish tartibi, variant parametrlari va qaydnoma (PDF, 3 bet)</span></a>
</div>
<div class="grid-2" style="margin-top:1.15rem;">
<div class="op-card"><div class="op-head"><div class="card-icon green">%s</div><h4>Qaysi vosita ishlatilganini 5 soniyada aniqlash</h4></div>
<div class="op-row"><span class="op-label keys">Rasm</span><span>Bosilganda <b>Rasm formati</b> yorlig‘i chiqadi.</span></div>
<div class="op-row"><span class="op-label keys">WordArt</span><span>Bosilganda <b>Shakl formati</b> chiqadi, ichida matnni tahrirlash mumkin. Yorliq chiqmasa — oddiy matn yoki rasm.</span></div>
<div class="op-row"><span class="op-label keys">Shakl</span><span>Bosilganda <b>Shakl formati</b>. <b>Ikkalasi birga</b> tanlansa — guruhlangan.</span></div>
<div class="op-row"><span class="op-label keys">Kolontitul</span><span>Yuqori/pastki chetga ikki marta bosilganda <b>Kolontitul asboblari</b> ochiladi; raqamni bosganda <b>kulrang fon</b> bo‘lishi kerak.</span></div></div>
<div class="op-card"><div class="op-head"><div class="card-icon">%s</div><h4>Bitta ishni 2–3 daqiqada tekshirish</h4></div>
<div class="op-row"><span class="op-label keys">1</span><span>Fayl nomi, bitta bet, maydonlar 2 sm (1-mezon).</span></div>
<div class="op-row"><span class="op-label keys">2</span><span>Matn namuna bilan solishtirildi, shrift tekshirildi (2-mezon).</span></div>
<div class="op-row"><span class="op-label keys">3</span><span>Sarlavhani bosing → WordArt, effekt (3–4-mezonlar).</span></div>
<div class="op-row"><span class="op-label keys">4</span><span>Rasmni bosing → eni, nisbati, o‘rash, uslub (5–7-mezonlar).</span></div>
<div class="op-row"><span class="op-label keys">5</span><span>Shakllar va guruh, so‘ng kolontitul (8–10-mezonlar).</span></div></div>
</div>
<div class="callout good">%s<span><strong>Kelishilgan qoidalar:</strong> rang qat’iy talab emas — namunaga yaqin bo‘lsa bo‘ladi. Rasm uslubining nomi Word versiyasiga qarab boshqacha bo‘lishi mumkin — namunadagi ko‘rinishga qarang. Ikki talabaning fayli bir xil bo‘lsa, ikkalasiga ham qayta topshiriq bering. Yarim ball (0,25) qo‘yilmaydi.</span></div>''' % (
        ico('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>', 15, 2.5),
        ico('<path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z"/>', 20, 2.3), ico('<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>', 20, 2.3),
        ico('<polyline points="20 6 9 17 4 12"/>', 18, 2.4))
    return section('sec-check', '9-Qism • Faqat o‘qituvchi', 'Ishlarni tekshirish va baholash',
                   'Ish to‘rtta vositadan iborat bo‘lgani uchun tekshirishning eng tez yo‘li — <strong>elementni bir marta bosib, qaysi yorliq chiqishiga qarash</strong>. Sahifa raqamini qo‘lda yozib “kolontitul” deb topshirgan yoki sarlavhani oddiy matn effekti bilan qilgan talabani shu usul bilan darhol bilasiz.', body, teacher=True)


QA = [
    ['Qo‘shish yorlig‘ida rasm, shakl, WordArt va kolontitul qayerda joylashgan?',
     '<p><b>Qo‘shish</b> (Insert / Вставка) yorlig‘ida: <b>Illyustratsiyalar</b> guruhida — Rasmlar, Shakllar; <b>Matn</b> guruhida — WordArt; <b>Kolontitul</b> guruhida — Yuqori kolontitul, Pastki kolontitul, Sahifa raqami.</p>'],
    ['Rasm, shakl, WordArt va kolontitul o‘rtasida qanday farq bor?',
     '<ul><li><b>Rasm</b> — tayyor fayl (surat);</li><li><b>Shakl</b> — Word ichida o‘zingiz chizadigan figura;</li><li><b>WordArt</b> — bezakli yozuv (alohida ramkadagi matn);</li><li><b>Kolontitul</b> — sahifaning yuqori/pastki chetidagi, har betda takrorlanadigan yozuv (sahifa raqami shu yerda).</li></ul>'],
    ['Rasmni cho‘zmasdan qanday kattalashtirish yoki kichraytirish mumkin?',
     '<p><b>Burchakdagi</b> nuqtani torting yoki <b>Rasm formati › O‘lcham › Eni</b> maydoniga qiymat yozing (“Nisbatni saqlash” yoqilgan bo‘lsa, bo‘yi o‘zi o‘zgaradi). Yon tomondagi nuqta rasmni cho‘zadi.</p>'],
    ['Nega rasm sudralmaydi va uni qanday erkin joylash mumkin?',
     '<p>Word rasmni “<b>Matn qatorida</b>” (In Line with Text) holatida qo‘yadi — u bitta katta harf kabi qatorda turadi. <b>Rasm formati › Matn bilan o‘rash</b> ro‘yxatidan <b>Kvadrat</b> (yoki boshqasi) tanlansa, rasmni erkin sudrash mumkin.</p>'],
    ['Matn bilan o‘rashning qanday turlari bor va qaysi biri eng ko‘p ishlatiladi?',
     '<p>Yettita: Matn qatorida, Kvadrat, Qattiq, Orqali, Tepa va past, Matn orqasida, Matn oldida. Eng ko‘p ishlatiladigani — <b>Kvadrat</b>: matn rasmning ramkasini aylanib o‘tadi.</p>'],
    ['Rasm matn orqasida turishi uchun nima qilinadi?',
     '<p><b>Matn bilan o‘rash › Matn orqasida</b> (Behind Text). Rasm to‘q bo‘lsa, matn o‘qilmaydi — rasmni <b>Tuzatishlar</b> orqali ochroq qiling.</p>'],
    ['Aylana yoki kvadratni to‘g‘ri nisbatda qanday chizish mumkin?',
     '<p><span class="key-cap">Shift</span> tugmasini bosib turib shaklni chizing. Shu usul to‘g‘ri chiziq va muntazam yulduz uchun ham ishlaydi.</p>'],
    ['Shakl ichiga matn qanday yoziladi?',
     '<p>Shaklni o‘ng tugma bilan bosib, <b>Matn qo‘shish</b> (Add Text) ni tanlang yoki shaklni tanlab shunchaki yozing. Shrift va rangi <b>Bosh sahifa</b> yorlig‘ida o‘zgartiriladi.</p>'],
    ['Shakllarni guruhlash nima uchun kerak va qanday bajariladi?',
     '<p>Guruhlangan shakllar bitta butun bo‘lib siljiydi va o‘lchami birga o‘zgaradi, tartibi buzilmaydi. <span class="key-cap">Ctrl</span> bilan shakllarni tanlang → o‘ng tugma › <b>Guruhlash › Guruhlash</b>.</p>'],
    ['Kolontitul nima va u qayerda yoziladi?',
     '<p>Kolontitul — sahifaning yuqori va pastki chetidagi, barcha betlarda takrorlanadigan yozuv (hujjat nomi, sana, sahifa raqami). <b>Qo‘shish › Yuqori / Pastki kolontitul</b> orqali yoki varaq chetiga ikki marta bosib kiritiladi.</p>'],
    ['Sahifa raqamini nima uchun qo‘lda yozib bo‘lmaydi va uni qanday qo‘yish kerak?',
     '<p>Qo‘lda yozilgan raqam oddiy matn: bet qo‘shilsa yoki matn siljisa, tartib buziladi. To‘g‘ri yo‘l: <b>Qo‘shish › Sahifa raqami</b> — bu avtomatik maydon (bosganda kulrang fon), raqamlar o‘zi yangilanadi.</p>'],
    ['Titul varag‘ida raqam ko‘rinmasligi uchun nima qilinadi?',
     '<p><b>Kolontitul asboblari › Konstruktor › Birinchi sahifa uchun alohida kolontitul</b> (Different First Page) belgilanadi. Raqamlash baribir titul bilan hisoblanadi: keyingi bet «2» bo‘ladi.</p>'],
    ['«Sahifa X dan Y» ko‘rinishi qanday hosil qilinadi?',
     '<p><b>Qo‘shish › Tezkor bloklar › Maydon</b>: <b>Page</b> (joriy bet raqami) va <b>NumPages</b> (jami betlar soni) maydonlari kiritiladi, ular orasiga «dan» so‘zi yoziladi.</p>'],
    ['Toq va juft betlar uchun har xil kolontitul nima uchun kerak?',
     '<p>Ikki tomonlama bosmada (kitob, hisobot) raqam va nom doim <b>tashqi chetda</b> turishi uchun: toq betda o‘ngda, juft betda chapda. <b>Konstruktor › Toq va juft sahifalar uchun har xil</b>.</p>'],
    ['Hujjatning ikkinchi qismida kolontitul va raqamni boshqacha qilish uchun nima qilinadi?',
     '<p>Hujjat <b>bo‘limlarga</b> bo‘linadi (<b>Maket › Uzilishlar › Keyingi sahifa</b>), yangi bo‘limda <b>«Oldingi bilan bog‘lash»</b> o‘chiriladi. Raqamni 1 dan boshlash: <b>Sahifa raqami formati › Boshlash</b>.</p>'],
    ['WordArt nima va oddiy matn effektidan qanday farq qiladi?',
     '<p>WordArt — alohida <b>ramkadagi</b> bezakli matn: uni sudrash, aylantirish, egrilash mumkin. <b>Bosh sahifa › Matn effektlari</b> esa oddiy matn qatorida qoladi.</p>'],
    ['Rasmiy hujjatda WordArt ishlatsa bo‘ladimi?',
     '<p>Yo‘q. Ariza, tushuntirish xati, hisobot, dalolatnoma kabi hujjatlarda sarlavha oddiy: Times New Roman, qalin, markazda (9-dars). WordArt faqat plakat, e’lon, byulleten va taqdimot sarlavhasi uchun.</p>'],
    ['Rasmni qirqish (Crop) rasmni kichraytirishdan nimasi bilan farq qiladi?',
     '<p>Kichraytirishda butun rasm kichrayadi; qirqishda <b>ortiqcha qismi yashiriladi</b>, qolgan qismining o‘lchami saqlanadi. Qirqilgan qism “Rasmni tiklash” bilan qaytariladi.</p>'],
    ['Shakllar ustma-ust tushganda qaysi biri tepada turishini qanday o‘zgartirish mumkin?',
     '<p>Shaklni tanlab, <b>Shakl formati › Oldinga olib chiqish</b> yoki <b>Orqaga yuborish</b> (Bring Forward / Send Backward) tugmalaridan foydalaning.</p>'],
]


def sec_qa():
    body = '''<div class="qa-toolbar"><span class="qa-count" id="qa-count">ta savol</span>
<button type="button" class="nav-btn" id="qa-toggle" onclick="toggleAllAnswers()">%s<span>Barcha javoblarni ochish</span></button></div>
<div class="qa-list" id="qa-list"></div>''' % ico('<polyline points="6 9 12 15 18 9"/>', 15, 2.5)
    return section('sec-qa', '10-Qism • Faqat o‘qituvchi', 'Nazorat savollari va javoblari',
                   'Savol ustiga bosing, javobi ochiladi. Avval javobni o‘zingiz eslashga harakat qiling, so‘ng tekshiring.', body, teacher=True, last=True)


# ----------------------------------------------------------------------------
# SAHIFA
# ----------------------------------------------------------------------------
def hero_chips():
    chips = [
        ('sec-tools', '1. To‘rt vosita', I_IMG, ''), ('sec-pic', '2. Rasm', I_IMG, ''), ('sec-shape', '3. Shakllar', I_SHAPE, ''),
        ('sec-kol', '4. Kolontitul', I_KOL, ''), ('sec-word', '5. WordArt', I_WORD, ''),
        ('sec-train', '6. Trenajyor', '<polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>', ''),
        ('sec-practice', '7. Amaliy ish: 6 variant', '<polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>', ' chip-practice'),
        ('sec-plan', '8. Dars rejasi', '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>', ' teacher-only'),
        ('sec-check', '9. Tekshirish', '<path d="M9 11l3 3L22 4"/>', ' teacher-only'),
        ('sec-qa', '10. Savol-javob', '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', ' teacher-only'),
    ]
    return '\n'.join('<a href="#%s" class="hero-chip%s">%s %s</a>' % (i, x, ico(p, 16, 2.2), t) for i, t, p, x in chips)


def build_page():
    with open(BASE, encoding='utf8', newline='') as f:
        base = f.read()
    # 9-darsning boshi (CSS, navigatsiya): muqova mavzusi blokigacha
    head = base[:base.index('<!-- TAT_COVER_THEME_START -->')]
    head = re.sub(r'<title>.*?</title>', '<title>%s — Tibbiyotda Axborot Texnologiyalari</title>' % TITLE, head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">',
                  '<meta name="description" content="Word’da rasmlar, shakllar, WordArt, kolontitul va avtomatik sahifa raqami bilan ishlash: matn bilan o‘rash va kolontitul laboratoriyalari, trenajyor va 6 variantli amaliy ish.">',
                  head, count=1, flags=re.S)
    sp = importlib.util.spec_from_file_location('cover_themes', THEME_SCRIPT)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    theme = mod.block(11, 'splash')
    extra = '\n  <style id="lesson10-extra">\n%s\n%s\n  </style>\n' % (read('lesson_extra.css'), POSTER_CSS)

    nav = '''</head>
<body>

  <!-- MUQOVA -->
  <div class="splash-overlay" id="splash" onclick="scrollToLesson()">
    <div class="splash-content">
      <h1 class="splash-title">Word’da rasmlar, shakllar,<br>WordArt va kolontitul</h1>
      <p class="splash-date" id="splash-date-text">Bugun</p>
    </div>
  </div>

  <!-- YUQORI MENYU -->
  <header class="top-nav" id="lesson-start">
    <div class="container">
      <div class="nav-inner">
        <a href="../index.html" class="nav-brand" title="Bosh Mundarijaga qaytish">
          <div class="nav-logo-box"><img src="./images/logos/word.svg" alt=""></div>
          <div class="nav-title-block">
            <h1>11-Dars: Rasmlar, shakllar, WordArt, kolontitul</h1>
            <p>Shahrisabz Tibbiyot Texnikumi • Hamshiralik ishi</p>
          </div>
        </a>
        <div class="nav-actions">
          <a href="../index.html" class="nav-btn">%(back)s<span>Mundarija</span></a>
          <a href="#sec-practice" class="nav-btn nav-btn-primary"><span>Amaliy ish</span>%(fwd)s</a>
        </div>
      </div>
    </div>
  </header>

  <!-- HERO -->
  <div class="hero">
    <div class="container">
      <div class="hero-badge-row">
        <span class="hero-badge">%(badge)s 11-Dars • Word 3-dars</span>
        <span class="hero-date" id="hero-live-date">Bugun</span>
      </div>
      <h1 class="hero-title"><span>Word’da</span> rasmlar, shakllar, WordArt va kolontitul</h1>
      <p class="hero-desc">Hujjatni matndan tashqari ko‘rgazmali qilish uchun to‘rtta vosita: tayyor <strong>rasm</strong>, o‘zingiz chizadigan <strong>shakllar</strong>, bezakli <strong>WordArt</strong> va ko‘p betli hujjat uchun <strong>kolontitul</strong> (avtomatik sahifa raqami). Matn bilan o‘rash va kolontitul laboratoriyalari, “Qaysi vosita?” trenajyori va dars oxirida 6 variantli amaliy ish: har bir talaba tibbiy axborot varaqasi tayyorlaydi.</p>
      <div class="hero-quick-links">
%(chips)s
      </div>
    </div>
  </div>

  <main>
    <div class="container">
''' % dict(back=ico('<polyline points="15 18 9 12 15 6"/>', 15, 2.5), fwd=ico('<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>', 15, 2.5),
           badge=ico('<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>', 13, 2.5), chips=hero_chips())

    sections = ''.join([sec_tools(), sec_pic(), sec_shape(), sec_kol(), sec_word(), sec_train(), sec_practice(), sec_plan(), sec_check(), sec_qa()])

    tail = '''
    </div>
  </main>

  <!-- NAMUNANI KO'RISH OYNASI -->
  <div class="var-modal" id="var-modal" hidden>
    <div class="var-modal-box" role="dialog" aria-modal="true" aria-labelledby="var-modal-title">
      <div class="var-modal-head">
        <h3 id="var-modal-title">Namuna</h3>
        <a href="#" class="nav-btn" id="var-modal-pdf" download>PDF</a>
        <button type="button" class="nav-btn" id="var-modal-close" aria-label="Yopish">✕</button>
      </div>
      <div class="var-modal-body" id="var-modal-body"></div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer>
    <div class="container">
      <div class="footer-inner">
        <div><strong>%s</strong> — Tibbiyotda axborot texnologiyalari fani</div>
        <div><span>100%% Offline rejim • 11-Dars</span> • <a href="../index.html">Mundarija</a></div>
      </div>
    </div>
  </footer>

  <script>
%s
  </script>
</body>
</html>
'''
    js = read('lesson.js')
    js = js.replace('/*QUIZ*/[]', json.dumps(QUIZ, ensure_ascii=False))
    js = js.replace('/*CRIT*/[]', json.dumps([[a, b] for a, b in CRITERIA], ensure_ascii=False))
    js = js.replace('/*QA*/[]', json.dumps(QA, ensure_ascii=False))
    return head + extra + theme + nav + sections + (tail % (TEXNIKUM, js))
