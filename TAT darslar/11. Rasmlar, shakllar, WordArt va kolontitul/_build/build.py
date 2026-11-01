# -*- coding: utf-8 -*-
"""
Word 3-dars (10-dars): tarqatma PDF'lar va dars sahifasi (dars.html).

Ishga tushirish (shu papkada):
    python images.py   # bir marta: rasmlar to'plami (tarqatma/rasmlar, rasmlar.zip)
    python build.py    # tarqatma PDF'lar va ../dars.html
Natija:
  ../tarqatma/N-variant.pdf             — talabaga: 1-bet topshiriq, 2-bet namuna (A4)
  ../tarqatma/barcha-variantlar.pdf     — 6 variant bitta faylda (chop etish uchun)
  ../tarqatma/oqituvchi-qollanma.pdf    — o'qituvchiga: tekshirish tartibi, variant parametrlari, qaydnoma
  ../dars.html                          — dars sahifasi
Matnni o'zgartirish uchun variants.py (yoki page.py) ni tahrirlang va qayta ishga tushiring.
"""
import os
import sys

from handouts import print_doc, sample_sheet, info_sheet, teacher_sheets, to_pdf
from variants import VARIANTS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_HTML = os.path.join(HERE, 'out')
PDF_DIR = os.path.join(ROOT, 'tarqatma')
# PDF yasaladigan HTML _build/out/ ichida: rasmlarga nisbiy yo'l
IMG_FROM_OUT = '../../tarqatma/rasmlar'


def write(path, text):
    with open(path, 'w', encoding='utf8', newline='\n') as f:
        f.write(text)


def main():
    os.makedirs(OUT_HTML, exist_ok=True)
    ok = True
    all_sheets = []
    for V in VARIANTS:
        sheets = [info_sheet(V, IMG_FROM_OUT), sample_sheet(V, IMG_FROM_OUT)]
        all_sheets += sheets
        src = os.path.join(OUT_HTML, '%d-variant.html' % V['n'])
        write(src, print_doc(sheets, '%d-variant: %s' % (V['n'], V['name'])))
        pages = to_pdf(src, os.path.join(PDF_DIR, '%d-variant.pdf' % V['n']))
        ok &= pages == 2
        print('%d-variant (%s): %d bet %s' % (V['n'], V['name'], pages, 'OK' if pages == 2 else 'DIQQAT: 2 bet kutilgan'))

    src = os.path.join(OUT_HTML, 'barcha-variantlar.html')
    write(src, print_doc(all_sheets, 'Word 3-dars: barcha variantlar'))
    pages = to_pdf(src, os.path.join(PDF_DIR, 'barcha-variantlar.pdf'))
    ok &= pages == len(all_sheets)
    print('Barcha variantlar: %d bet (kutilgan %d)' % (pages, len(all_sheets)))

    src = os.path.join(OUT_HTML, 'oqituvchi-qollanma.html')
    write(src, print_doc(teacher_sheets(), 'Word 3-dars: o‘qituvchi qo‘llanmasi'))
    pages = to_pdf(src, os.path.join(PDF_DIR, 'oqituvchi-qollanma.pdf'))
    ok &= pages == 3
    print('O‘qituvchi qo‘llanmasi: %d bet (kutilgan 3)' % pages)

    try:
        from page import build_page
    except ImportError:
        build_page = None
    if build_page:
        write(os.path.join(ROOT, 'dars.html'), build_page())
        print('dars.html yozildi')

    import topic_sheets
    topic_sheets.main()
    import ready_materials
    ready_materials.main()

    if not ok:
        sys.exit(1)


if __name__ == '__main__':
    main()
