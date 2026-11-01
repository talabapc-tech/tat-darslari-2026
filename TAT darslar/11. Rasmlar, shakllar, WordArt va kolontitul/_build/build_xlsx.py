# -*- coding: utf-8 -*-
"""35 variant ro'yxati (Excel): python build_xlsx.py  ->  ../tarqatma/tayyor/35-variant-royxat.xlsx"""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

from ready_data import ANATOMIYA_XIRURGIYA as D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'tarqatma', 'tayyor', '35-variant-royxat.xlsx')
F = 'Arial'
thin = Side(style='thin', color='B8C4D8')
bd = Border(left=thin, right=thin, top=thin, bottom=thin)
FILL = {'Anatomiya': 'E3EEFC', 'Farmakologiya': 'EBE0F7'}

wb = Workbook()
ws = wb.active
ws.title = '35 variant'
ws['A1'] = 'Word amaliy ishi: rasm va ma’lumot topish — 35 variant (anatomiya, farmakologiya)'
ws['A1'].font = Font(name=F, size=14, bold=True, color='0B2A5B')
ws.merge_cells('A1:I1')
ws['A2'] = 'Shahrisabz Tibbiyot Texnikumi • Tibbiyotda axborot texnologiyalari. Sariq kataklar (F–I) o‘qituvchi tomonidan to‘ldiriladi.'
ws['A2'].font = Font(name=F, size=10, italic=True, color='555555')
ws.merge_cells('A2:I2')
R0 = 4
for c, h in enumerate(['№', 'Fan', 'Mavzu', 'Rasm qidirish so‘zlari', 'Fayl', 'Talaba F.I.O.', 'Guruh', 'Topshirdi', 'Baho (5 ballik)'], 1):
    x = ws.cell(R0, c, h)
    x.font = Font(name=F, bold=True, color='FFFFFF')
    x.fill = PatternFill('solid', fgColor='185ABD')
    x.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    x.border = bd
for i, t in enumerate(D, 1):
    r = R0 + i
    for c, v in enumerate([i, t[0], t[1], ' • '.join(t[2]), 'variant-%02d.pdf' % i, None, None, None, None], 1):
        x = ws.cell(r, c, v)
        x.font = Font(name=F, size=10, bold=(c == 3))
        x.border = bd
        x.alignment = Alignment(vertical='center', wrap_text=(c in (3, 4)), horizontal='center' if c in (1, 2, 8, 9) else 'left')
        if c >= 6:
            x.fill = PatternFill('solid', fgColor='FFFBE0')
    ws.cell(r, 2).fill = PatternFill('solid', fgColor=FILL[t[0]])
last = R0 + len(D)
dv = DataValidation(type='list', formula1='"Ha,Yo‘q"', allow_blank=True)
ws.add_data_validation(dv)
dv.add('H%d:H%d' % (R0 + 1, last))
dv2 = DataValidation(type='whole', operator='between', formula1='0', formula2='5', allow_blank=True)
ws.add_data_validation(dv2)
dv2.add('I%d:I%d' % (R0 + 1, last))
s = last + 2
rows = [('Jami variantlar', '=COUNTA(C%d:C%d)' % (R0 + 1, last)),
        ('Talabaga berilgan', '=COUNTA(F%d:F%d)' % (R0 + 1, last)),
        ('Bo‘sh variantlar', '=D%d-D%d' % (s, s + 1)),
        ('Topshirganlar', '=COUNTIF(H%d:H%d,"Ha")' % (R0 + 1, last)),
        ('O‘rtacha baho', '=IFERROR(AVERAGE(I%d:I%d),0)' % (R0 + 1, last))]
for k, (a, f) in enumerate(rows):
    ws.cell(s + k, 3, a).font = Font(name=F, bold=True)
    c = ws.cell(s + k, 4, f)
    c.font = Font(name=F, bold=True, color='185ABD')
    c.alignment = Alignment(horizontal='left')
    c.number_format = '0.0' if 'AVERAGE' in f else '0'
for col, w in zip('ABCDEFGHI', [5, 14, 30, 46, 16, 28, 12, 11, 12]):
    ws.column_dimensions[col].width = w
ws.row_dimensions[R0].height = 30
ws.freeze_panes = 'A5'
ws.auto_filter.ref = 'A%d:I%d' % (R0, last)
ws.page_setup.orientation = 'landscape'
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.print_title_rows = '%d:%d' % (R0, R0)

w2 = wb.create_sheet('Tayyor ma’lumot')
for c, h in enumerate(['№', 'Mavzu', 'Kirish', '1-fakt', '2-fakt', '3-fakt', '4-fakt', '5-fakt', 'Bilasizmi?', 'Rasm tagidagi yozuv'], 1):
    x = w2.cell(1, c, h)
    x.font = Font(name=F, bold=True, color='FFFFFF')
    x.fill = PatternFill('solid', fgColor='185ABD')
    x.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    x.border = bd
for i, t in enumerate(D, 1):
    for c, v in enumerate([i, t[1], t[3]] + list(t[4]) + [t[5], '1-rasm. ' + t[6]], 1):
        x = w2.cell(i + 1, c, v)
        x.font = Font(name=F, size=10, bold=(c == 2))
        x.alignment = Alignment(wrap_text=True, vertical='top')
        x.border = bd
for col, w in zip('ABCDEFGHIJ', [5, 24, 40, 40, 40, 40, 40, 40, 40, 26]):
    w2.column_dimensions[col].width = w
w2.freeze_panes = 'C2'
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print('saved', OUT)
