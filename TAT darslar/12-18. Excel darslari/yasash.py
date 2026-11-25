"""Excel darslari (12-18): har bir dars uchun 4 variant.

Natija (har bir dars papkasida):
  NN-dars - variantlar (talabaga).pdf     A4 tik, o'rtasidan qirqiladi: yuqorida 1-, pastda 2-variant (2-bet: 3 va 4)
  NN-dars - javoblar (o'qituvchi).xlsx    4 varaq, tayyor natija + nazorat kataklari (✓/✗)
  NN-dars - boshlang'ich fayl (talabaga).xlsx   faqat 15- va 16-dars (tayyor ma'lumot)

Excel ruscha bo'lsa formulalar o'zi ruscha ko'rinadi (SUM -> СУММ).
Ishga tushirish:  python yasash.py          (hamma darslar)
                  python yasash.py 15       (faqat 15-dars)
"""
import datetime as dt
import html
import math
import random
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

HERE = Path(__file__).resolve().parent
EDGE = next((p for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                         r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                         r"C:\Program Files\Google\Chrome\Application\chrome.exe"] if Path(p).exists()), None)
FONT = "Times New Roman"
BLACK = Side(style="thin", color="000000")
BOX = Border(left=BLACK, right=BLACK, top=BLACK, bottom=BLACK)
OK, BAD = "✓ To'g'ri", "✗ Xato"

# ======================================================================
#  Varaq tavsifi: bitta model ham Excelga, ham PDF varaqchaga chiziladi
# ======================================================================
FMT = {"int": "0", "num": "#,##0", "money": '#,##0 "so\'m"', "d1": "0.0", "d2": "0.00", "date": "DD.MM.YYYY", None: None}


def ko_rinish(v, fmt):
    """Excel ruscha ko'rsatadigan matn: 1 234 567, 36,6, 05.03.2027."""
    if v is None:
        return ""
    if isinstance(v, (dt.date, dt.datetime)):
        return v.strftime("%d.%m.%Y")
    if isinstance(v, str):
        return v
    if fmt in ("num", "money"):
        s = f"{round(v):,}".replace(",", "\u00a0")
        return s + (" so'm" if fmt == "money" else "")
    if fmt == "d1":
        return f"{v:.1f}".replace(".", ",")
    if fmt == "d2":
        return f"{v:.2f}".replace(".", ",")
    if isinstance(v, float) and not v.is_integer():
        return f"{v:g}".replace(".", ",")
    return str(int(v)) if isinstance(v, float) else str(v)


class Varaq:
    def __init__(self, nom):
        self.nom = nom
        self.c = {}            # (r, c) -> dict(v, val, fmt, bold, align)
        self.merges = []       # (r1, c1, r2, c2)
        self.boxes = []        # chegarali sohalar
        self.widths = {}
        self.steps = []        # talaba qadamlari
        self.nazorat = []      # (nomi, formula, kutilgan, izoh)
        self.cf = []           # (diapazon, operator, qiymat, rang)
        self.dv = []           # (diapazon, ro'yxat)
        self.table = None      # (ref, nom) — Smart jadval
        self.filter = None
        self.freeze = None
        self.charts = []       # (tur, spec)
        self.spark = None      # (ustun, r1, r2, c1, c2)
        self.extra = ""        # varaqchaga qo'shimcha HTML (savollar, diagramma eskizlari)
        self.card_rows = None  # varaqchada ko'rsatiladigan qatorlar (None = hammasi)
        self.card_note = ""

    def put(self, r, c, v, val=None, fmt=None, bold=False, align=None):
        self.c[(r, c)] = dict(v=v, val=v if val is None else val, fmt=fmt, bold=bold, align=align)

    def row(self, r, c0, values, fmts=None, bold=False):
        for i, v in enumerate(values):
            f = fmts[i] if fmts else None
            if isinstance(v, tuple):
                self.put(r, c0 + i, v[0], v[1], f, bold)
            else:
                self.put(r, c0 + i, v, None, f, bold)

    def title(self, text, ncols):
        self.put(1, 1, text, bold=True, align="center")
        self.merges.append((1, 1, 1, ncols))

    @property
    def maxr(self):
        return max(r for r, _ in self.c)

    @property
    def maxc(self):
        return max(c for _, c in self.c)


# ======================================================================
#  Ma'lumotlar
# ======================================================================
R = random.Random(2026)
FAM_E = ["Aliyev", "Karimov", "Rahimov", "Yusupov", "Toshmatov", "Nazarov", "Ergashev", "Saidov", "Qodirov", "Mirzayev",
         "Sobirov", "Xolmatov", "Abdullayev", "Usmonov", "Ismoilov", "Jo'rayev", "Hasanov", "Rustamov"]
ISM_E = ["Jasur", "Sardor", "Bekzod", "Otabek", "Anvar", "Sherzod", "Dilshod", "Akmal", "Javohir", "Ulug'bek"]
ISM_A = ["Dilnoza", "Malika", "Gulnora", "Nilufar", "Zarina", "Shahnoza", "Madina", "Feruza", "Sevara", "Kamola"]
BOLIM = ["Terapiya", "Xirurgiya", "Pediatriya", "Kardiologiya", "Nevrologiya"]


def odam(jins=None):
    j = jins or R.choice(["E", "A"])
    f = R.choice(FAM_E)
    return (f"{f} {R.choice(ISM_E)}", "Erkak") if j == "E" else (f"{f}a {R.choice(ISM_A)}", "Ayol")


def sana(y1, y2):
    return dt.date(R.randint(y1, y2), R.randint(1, 12), R.randint(1, 28))


def odamlar(n):
    seen, out = set(), []
    while len(out) < n:
        o = odam()
        if o[0] not in seen:
            seen.add(o[0]); out.append(o)
    return out


# ======================================================================
#  11-dars. Tanishuv: ma'lumot kiritish
# ======================================================================
def dars11():
    V = []
    turlar = [
        ("Terapiya bo'limi bemorlari", ["№", "F.I.Sh.", "Tug'ilgan sana", "Jinsi", "Palata"],
         lambda o: [sana(1950, 2000), o[1], R.randint(1, 12)], [None, None, "date", None, "int"], "Bemorlar"),
        ("Pediatriya bo'limi bemorlari", ["№", "F.I.Sh.", "Tug'ilgan sana", "Jinsi", "Vazni (kg)"],
         lambda o: [sana(2012, 2023), o[1], R.randint(12, 45)], [None, None, "date", None, "int"], "Bolalar"),
        ("Poliklinika xodimlari", ["№", "F.I.Sh.", "Tug'ilgan sana", "Lavozimi", "Ishga kirgan sana"],
         lambda o: [sana(1965, 2000), R.choice(["Shifokor", "Hamshira", "Laborant", "Feldsher"]), sana(2005, 2025)],
         [None, None, "date", None, "date"], "Xodimlar"),
        ("Emlash ro'yxati", ["№", "F.I.Sh.", "Tug'ilgan sana", "Vaksina", "Emlash sanasi"],
         lambda o: [sana(2019, 2025), R.choice(["BTsJ", "Gepatit B", "Qizamiq", "Poliomiyelit"]), sana(2026, 2026)],
         [None, None, "date", None, "date"], "Emlash"),
    ]
    for k, (nom, cols, gen, fmts, varaq) in enumerate(turlar, 1):
        s = Varaq(f"{k}-variant")
        s.title(nom, 5)
        s.row(3, 1, cols, bold=True)
        for i, o in enumerate(odamlar(8)):
            s.row(4 + i, 1, [i + 1, o[0]] + gen(o), fmts)
        s.boxes.append((3, 1, 11, 5))
        s.widths = {1: 5, 2: 22, 3: 14, 4: 12, 5: 16}
        s.steps = [f"A1 katakka sarlavha yozing: «{nom}».",
                   "3-qatorga ustun nomlarini kiriting (A3 dan E3 gacha).",
                   "A4 ga 1 yozing, avtoto'ldirish markerini A11 gacha torting (Ctrl bosib turing) — 1 dan 8 gacha chiqsin.",
                   "Jadvalni to'ldiring. Sanani kun.oy.yil ko'rinishida yozing (masalan 05.03.1985).",
                   "Ustunlar kengligini matnga moslang (ustun chegarasiga 2 marta bosing).",
                   f"Varaq nomini «{varaq}» qiling va faylni «Familiya_12-dars» nomi bilan saqlang."]
        s.nazorat = [("Oxirgi № (A11)", "=A11", 8, "Avtoto'ldirish to'g'ri bo'lsa 8"),
                     ("Kiritilgan qatorlar", "=COUNTA(B4:B11)", 8, "B4:B11 to'ldirilgan"),
                     ("Sana sifatida kiritilgan", "=COUNT(C4:C11)", 8, "Sana matn bo'lib qolsa kamroq chiqadi")]
        V.append(s)
    return "12", "Excel bilan tanishuv: interfeys va ma'lumot kiritish", V, None


# ======================================================================
#  12-dars. Formatlash, Smart jadval
# ======================================================================
def dars12():
    V = []
    turlar = [
        ("DORIXONA ZAXIRASI", ["Dori nomi", "Dozasi", "Narxi", "Soni (dona)", "Yaroqlilik muddati"],
         [("Paratsetamol", "500 mg"), ("Amoksitsillin", "250 mg"), ("Ibuprofen", "200 mg"), ("Analgin", "500 mg"),
          ("Seftriakson", "1 g"), ("Omeprazol", "20 mg"), ("Loratadin", "10 mg"), ("No-shpa", "40 mg")], (2000, 20000), (2026, 2028)),
        ("TIBBIY JIHOZLAR", ["Jihoz nomi", "Modeli", "Narxi", "Soni (dona)", "Xarid sanasi"],
         [("Tonometr", "Omron M2"), ("Termometr", "B.Well"), ("Glyukometr", "Accu-Chek"), ("Pulsoksimetr", "Armed"),
          ("Ingalyator", "Microlife"), ("Stetoskop", "Littmann"), ("Tarozi", "Seca 813"), ("Bo'y o'lchagich", "Seca 213")],
         (90000, 1500000), (2022, 2026)),
        ("LABORATORIYA REAKTIVLARI", ["Reaktiv nomi", "Hajmi", "Narxi", "Soni (dona)", "Yaroqlilik muddati"],
         [("Glyukoza testi", "100 ml"), ("Gemoglobin testi", "250 ml"), ("Xolesterin", "100 ml"), ("Bilirubin", "50 ml"),
          ("Kreatinin", "100 ml"), ("Mochevina", "200 ml"), ("ALT testi", "50 ml"), ("AST testi", "50 ml")],
         (120000, 600000), (2026, 2028)),
        ("BOG'LOV MATERIALLARI", ["Material nomi", "O'lchami", "Narxi", "Soni (dona)", "Kelgan sana"],
         [("Doka bint", "7 m × 14 sm"), ("Elastik bint", "5 m"), ("Leykoplastir", "2 × 500 sm"), ("Paxta", "100 g"),
          ("Steril salfetka", "10 × 10 sm"), ("Shprits", "5 ml"), ("Qo'lqop", "M o'lcham"), ("Niqob", "3 qatlam")],
         (800, 15000), (2025, 2026)),
    ]
    for k, (nom, cols, items, (p1, p2), (y1, y2)) in enumerate(turlar, 1):
        s = Varaq(f"{k}-variant")
        s.title(nom, 5)
        s.row(3, 1, cols, bold=True)
        for i, (a, b) in enumerate(items):
            narx = round(R.randint(p1, p2), -2)
            s.row(4 + i, 1, [a, b, narx, R.randint(10, 150), sana(y1, y2)], [None, None, "money", "int", "date"])
        s.boxes.append((3, 1, 11, 5))
        s.table = ("A3:E11", f"Jadval12_{k}")
        s.widths = {1: 20, 2: 14, 3: 16, 4: 12, 5: 18}
        s.steps = [f"A1 ga «{nom}» deb yozing. A1:E1 ni belgilab «Объединить и поместить в центре» bosing; shrift 14, qalin.",
                   "3-qatordan boshlab jadvalni kiriting.",
                   "A3:E11 ni belgilab Ctrl+T bosing (Smart jadval), «Таблица с заголовками» belgilangan bo'lsin.",
                   "Narxi ustuniga son formati bering: Формат ячеек → (все форматы) → # ##0 \"so'm\".",
                   "Sana ustuniga «Краткая дата» formatini bering.",
                   "Jadvalga «Все границы» chegarasini bering, sarlavha qatorini qalin qiling, ustunlarni moslang."]
        tot = sum(s.c[(r, 3)]["val"] for r in range(4, 12))
        s.nazorat = [("Qatorlar soni", "=COUNTA(A4:A11)", 8, "8 ta qator"),
                     ("Narxlar yig'indisi", "=SUM(C4:C11)", tot, "Narxlar son bo'lib kiritilgan bo'lsa to'g'ri chiqadi")]
        V.append(s)
    return "13", "Formatlash, Smart jadval, jadvalni bezash", V, None


# ======================================================================
#  13-dars. Sodda formulalar
# ======================================================================
def dars13():
    V = []
    # 1-variant: dorixona
    s = Varaq("1-variant"); s.title("Dorixona: sotilgan dorilar", 4)
    s.row(3, 1, ["Dori nomi", "Narxi (so'm)", "Soni", "Jami (so'm)"], bold=True)
    dor = ["Paratsetamol", "Ibuprofen", "Analgin", "Loratadin", "Omeprazol", "No-shpa", "Sitramon", "Aspirin"]
    tot = 0
    for i, d in enumerate(dor):
        r = 4 + i; narx = round(R.randint(2000, 15000), -2); n = R.randint(3, 40); tot += narx * n
        s.row(r, 1, [d, narx, n, (f"=B{r}*C{r}", narx * n)], [None, "num", "int", "num"])
    s.put(12, 3, "Jami:", bold=True)
    s.put(12, 4, "=" + "+".join(f"D{r}" for r in range(4, 12)), tot, "num", bold=True)
    s.boxes.append((3, 1, 12, 4)); s.widths = {1: 18, 2: 14, 3: 8, 4: 16}
    s.steps = ["Jadvalni A3:C11 ga kiriting, sarlavha qatori qalin bo'lsin.",
               "D4 ga =B4*C4 yozing, Enter bosing.",
               "D4 ni belgilab, markerni D11 gacha torting — formula hamma qatorga ko'chadi.",
               "C12 ga «Jami:» deb yozing, D12 ga =D4+D5+D6+D7+D8+D9+D10+D11 yozing.",
               "B va D ustunlariga «Числовой» format bering (разделитель групп разрядов, 0 kasr).",
               "Bitta narxni o'zgartirib ko'ring: D ustuni va Jami o'zi yangilanadimi?"]
    s.nazorat = [("Jami (D12)", "=D12", tot, "Narx × Soni yig'indisi"), ("3-qator (D6)", "=D6", s.c[(6, 4)]["val"], "B6*C6")]
    V.append(s)
    # 2-variant: ovqatlanish
    s = Varaq("2-variant"); s.title("Bemorning kunlik ovqatlanishi", 4)
    s.row(3, 1, ["Taom", "Kaloriya (1 porsiya)", "Porsiya", "Jami kaloriya"], bold=True)
    taom = [("Sutli bo'tqa", 210), ("Non (1 bo'lak)", 80), ("Tovuq sho'rva", 150), ("Guruch", 190), ("Bug'da pishgan baliq", 170),
            ("Sabzavotli salat", 60), ("Olma", 50), ("Kefir", 110)]
    tot = 0
    for i, (t, kal) in enumerate(taom):
        r = 4 + i; p = R.randint(1, 3); tot += kal * p
        s.row(r, 1, [t, kal, p, (f"=B{r}*C{r}", kal * p)], [None, "int", "int", "int"])
    s.put(12, 3, "Jami:", bold=True)
    s.put(12, 4, "=" + "+".join(f"D{r}" for r in range(4, 12)), tot, "int", bold=True)
    s.boxes.append((3, 1, 12, 4)); s.widths = {1: 22, 2: 20, 3: 9, 4: 14}
    s.steps = ["Jadvalni A3:C11 ga kiriting, sarlavha qatori qalin bo'lsin.",
               "D4 ga =B4*C4 yozing va D11 gacha torting.",
               "C12 ga «Jami:», D12 ga =D4+D5+D6+D7+D8+D9+D10+D11 yozing.",
               "B3 kabi uzun sarlavhalar uchun «Переносить текст» ni yoqing.",
               "Porsiyani o'zgartirib, Jami kaloriya o'zgarishini tekshiring."]
    s.nazorat = [("Jami kaloriya (D12)", "=D12", tot, "Kaloriya × Porsiya yig'indisi")]
    V.append(s)
    # 3-variant: TVI
    s = Varaq("3-variant"); s.title("Tana vazni indeksi (TVI)", 5)
    s.row(3, 1, ["Bemor", "Bo'yi (sm)", "Bo'yi (m)", "Vazni (kg)", "TVI"], bold=True)
    for i, o in enumerate(odamlar(8)):
        r = 4 + i; sm = R.randint(150, 192); kg = R.randint(45, 110)
        s.row(r, 1, [o[0], sm, (f"=B{r}/100", sm / 100), kg, (f"=D{r}/(C{r}*C{r})", kg / (sm / 100) ** 2)],
              [None, "int", "d2", "int", "d1"])
    s.boxes.append((3, 1, 11, 5)); s.widths = {1: 22, 2: 10, 3: 10, 4: 11, 5: 9}
    s.card_note = "TVI = Vazn / (Bo'y × Bo'y), bo'y metrda. 18,5–25 — normal."
    s.steps = ["Jadvalni kiriting: A — bemor, B — bo'yi (sm), D — vazni (kg).",
               "C4 ga =B4/100 yozing (sm → metr) va C11 gacha torting.",
               "E4 ga =D4/(C4*C4) yozing va E11 gacha torting. Qavsni unutmang!",
               "C ustuniga 2 ta, E ustuniga 1 ta kasr xona qoldiring (Уменьшить разрядность).",
               "Qavssiz =D4/C4*C4 yozib ko'ring — natija nega boshqacha?"]
    s.nazorat = [("3-bemor TVI (E6)", "=ROUND(E6,1)", round(s.c[(6, 5)]["val"], 1), "Qavs to'g'ri qo'yilgan bo'lsa"),
                 ("8-bemor bo'yi, m (C11)", "=C11", s.c[(11, 3)]["val"], "=B11/100")]
    V.append(s)
    # 4-variant: ombor qoldig'i
    s = Varaq("4-variant"); s.title("Dori ombori: oy oxiridagi qoldiq", 5)
    s.row(3, 1, ["Dori nomi", "Oy boshida", "Kirim", "Chiqim", "Qoldiq"], bold=True)
    dor = ["Paratsetamol", "Seftriakson", "Analgin", "Dimedrol", "Glyukoza 5%", "Natriy xlorid", "Eufillin", "Diklofenak"]
    tq = 0
    for i, d in enumerate(dor):
        r = 4 + i; b = R.randint(20, 200); kir = R.randint(0, 150); ch = R.randint(10, b + kir - 5); q = b + kir - ch; tq += q
        s.row(r, 1, [d, b, kir, ch, (f"=B{r}+C{r}-D{r}", q)], [None, "int", "int", "int", "int"])
    s.put(12, 4, "Jami:", bold=True)
    s.put(12, 5, "=" + "+".join(f"E{r}" for r in range(4, 12)), tq, "int", bold=True)
    s.boxes.append((3, 1, 12, 5)); s.widths = {1: 18, 2: 11, 3: 9, 4: 9, 5: 10}
    s.card_note = "Qoldiq = Oy boshida + Kirim − Chiqim"
    s.steps = ["Jadvalni A3:D11 ga kiriting.",
               "E4 ga =B4+C4-D4 yozing va E11 gacha torting.",
               "D12 ga «Jami:», E12 ga =E4+E5+E6+E7+E8+E9+E10+E11 yozing.",
               "Bitta Chiqim sonini o'zgartiring: Qoldiq va Jami o'zgardimi?",
               "Sarlavha qatorini qalin qiling, jadvalga chegara bering."]
    s.nazorat = [("Jami qoldiq (E12)", "=E12", tq, "Qoldiqlar yig'indisi")]
    V.append(s)
    return "14", "Sodda formulalar: = + − * /", V, None


# ======================================================================
#  14-dars. Funksiyalar: СУММ, СРЗНАЧ, МАКС, МИН, СЧЁТ, СЧЁТЗ
# ======================================================================
def dars14():
    V = []
    KUN = ["Du", "Se", "Chor", "Pay", "Ju"]
    turlar = [
        ("Shifokorlar qabul qilgan bemorlar soni", "Shifokor", [f"Dr. {odam('E')[0].split()[0]}" for _ in range(8)], (8, 30)),
        ("Bo'limlar bo'yicha dori sarfi (dona)", "Bo'lim", BOLIM + ["Reanimatsiya", "Travmatologiya", "Ginekologiya"], (20, 90)),
        ("Laboratoriyada bajarilgan tahlillar", "Tahlil turi",
         ["Umumiy qon", "Umumiy siydik", "Glyukoza", "Xolesterin", "Bilirubin", "Kreatinin", "Koagulogramma", "Gormonlar"], (5, 60)),
        ("Tez yordam brigadalari chaqiruvlari", "Brigada", [f"{i}-brigada" for i in range(1, 9)], (3, 18)),
    ]
    for k, (nom, ust, nomlar, (a, b)) in enumerate(turlar, 1):
        s = Varaq(f"{k}-variant"); s.title(nom, 10)
        s.row(3, 1, [ust] + KUN + ["Jami", "O'rtacha", "Eng ko'p", "Eng kam"], bold=True)
        hamma = []
        for i, n in enumerate(nomlar):
            r = 4 + i; v = [R.randint(a, b) for _ in range(5)]; hamma += v
            s.row(r, 1, [n] + v + [(f"=SUM(B{r}:F{r})", sum(v)), (f"=AVERAGE(B{r}:F{r})", sum(v) / 5),
                                   (f"=MAX(B{r}:F{r})", max(v)), (f"=MIN(B{r}:F{r})", min(v))],
                  [None] + ["int"] * 6 + ["d1", "int", "int"])
        s.boxes.append((3, 1, 11, 10))
        jami = sum(hamma)
        s.put(13, 1, "Ro'yxatdagilar soni:", bold=True); s.put(13, 7, "=COUNTA(A4:A11)", 8, "int", bold=True)
        s.put(14, 1, "Kiritilgan sonlar soni:", bold=True); s.put(14, 7, "=COUNT(B4:F11)", 40, "int", bold=True)
        s.put(15, 1, "Hafta bo'yicha jami:", bold=True); s.put(15, 7, "=SUM(G4:G11)", jami, "int", bold=True)
        for r in (13, 14, 15):
            s.merges.append((r, 1, r, 6))
        s.boxes += [(13, 1, 15, 7)]
        s.widths = {1: 22, **{c: 6 for c in range(2, 7)}, 7: 8, 8: 9, 9: 9, 10: 9}
        s.steps = ["Jadvalni A3:F11 ga kiriting, sarlavhani qalin qiling.",
                   "G4: =СУММ(B4:F4)   H4: =СРЗНАЧ(B4:F4)   I4: =МАКС(B4:F4)   J4: =МИН(B4:F4).",
                   "G4:J4 ni birga belgilab, 11-qatorgacha torting. H ustunida 1 ta kasr xona qoldiring.",
                   "A13:F13 ni birlashtiring, «Ro'yxatdagilar soni:» yozing; G13: =СЧЁТЗ(A4:A11).",
                   "G14: =СЧЁТ(B4:F11)  (nechta son kiritilgan);  G15: =СУММ(G4:G11).",
                   "Formulani qo'lda yozish o'rniga fx tugmasidan (Мастер функций) ham foydalanib ko'ring."]
        s.nazorat = [("Hafta jami (G15)", "=G15", jami, "Hamma sonlar yig'indisi"),
                     ("1-qator o'rtacha (H4)", "=ROUND(H4,1)", round(s.c[(4, 8)]["val"], 1), "СРЗНАЧ(B4:F4)"),
                     ("СЧЁТ natijasi (G14)", "=G14", 40, "8 qator × 5 kun")]
        V.append(s)
    return "15", "Funksiyalar: СУММ, СРЗНАЧ, МАКС, МИН, СЧЁТ, СЧЁТЗ", V, None


# ======================================================================
#  15-dars. Saralash, filtr, shartli formatlash, kiritishni tekshirish
# ======================================================================
def dars15():
    V, start = [], []
    n = 30

    def build(k, nom, cols, rows, fmts, sort_col, sort_desc, sort_text, flt, cf, dv_col, dv_list, widths):
        # boshlang'ich (saralanmagan) va javob (saralangan) varaqlar
        for kind in ("start", "javob"):
            s = Varaq(f"{k}-variant"); s.title(nom, len(cols))
            s.row(3, 1, ["№"] + cols, bold=True)
            data = sorted(rows, key=lambda x: x[sort_col], reverse=sort_desc) if kind == "javob" else rows
            for i, rr in enumerate(data):
                s.row(4 + i, 1, [i + 1 if kind == "start" else rows.index(rr) + 1] + list(rr), [None] + fmts)
            s.boxes.append((3, 1, 3 + n, len(cols) + 1))
            s.widths = widths
            s.freeze = "A4"; s.filter = f"A3:{CL(len(cols) + 1)}{3 + n}"
            if kind == "javob":
                ccol = CL(cf[0] + 2)
                s.cf.append((f"{ccol}4:{ccol}{3 + n}", cf[1], cf[2], "FFC7CE"))
                dcol = CL(dv_col + 2)
                s.dv.append((f"{dcol}4:{dcol}{3 + n}", dv_list))
                (fc1, fv1), (fc2, op2, fv2) = flt
                ans = sum(1 for rr in rows if rr[fc1] == fv1 and (rr[fc2] > fv2 if op2 == ">" else rr[fc2] < fv2))
                cfn = sum(1 for rr in rows if (rr[cf[0]] > cf[2] if cf[1] == ">" else rr[cf[0]] < cf[2]))
                c1, c2, cc = CL(fc1 + 2), CL(fc2 + 2), CL(cf[0] + 2)
                op_cf = '">"&' if cf[1] == ">" else '"<"&'
                s.nazorat = [
                    ("Filtr savoliga javob", f'=COUNTIFS({c1}4:{c1}{3 + n},"{fv1}",{c2}4:{c2}{3 + n},"{op2}"&{fv2})', ans,
                     "Talaba filtrdan keyin topgan son (varaqchaga yozadi)"),
                    ("Shartli formatlangan kataklar", f"=COUNTIF({cc}4:{cc}{3 + n},{op_cf}{cf[2]})", cfn, "Rangga bo'yalgan kataklar soni"),
                    ("Saralash: birinchi qiymat", f"={CL(sort_col + 2)}4", data[0][sort_col], "Saralangandan keyin 4-qatordagi qiymat"),
                ]
                s.card_rows = (1, 9)
                s.card_note = f"Namuna: saralangandan keyingi birinchi 6 qator (jami {n} qator)."
                s.steps = [f"Boshlang'ich fayldagi «{k}-variant» varag'ini oching (jadval tayyor, {n} qator).",
                           f"Jadvalni «{cols[sort_col]}» ustuni bo'yicha {sort_text} saralang (Данные → Сортировка).",
                           f"Ctrl+Shift+L bilan filtr qo'ying. {flt_text(cols, flt)} Nechta? Javobni pastga yozing. Filtrni tozalang.",
                           f"«{cols[cf[0]]}» ustunida {cf[3]} — qizil rangga bo'yang (Условное форматирование → Правила выделения ячеек).",
                           f"«{cols[dv_col]}» ustuniga ochiladigan ro'yxat qo'ying (Данные → Проверка данных → Список).",
                           "Sarlavhani qotiring: A4 ni tanlab Вид → Закрепить области."]
                s.extra = '<p class="javob">Filtr savoliga javob: ________ ta</p>'
                V.append(s)
            else:
                start.append(s)

    def flt_text(cols, flt):
        (c1, v1), (c2, op, v2) = flt
        return f"«{cols[c1]}» = {v1} va «{cols[c2]}» {op} {ko_rinish(v2, None)} bo'lganlarni toping."

    # 1-variant: bemorlar
    rows = [(odam()[0], R.randint(5, 85), R.choice(BOLIM), round(R.uniform(36.0, 39.2), 1), R.randint(58, 118)) for _ in range(n)]
    build(1, "Statsionar bemorlari", ["F.I.Sh.", "Yoshi", "Bo'lim", "Harorat", "Puls"], rows, [None, "int", None, "d1", "int"],
          1, True, "kamayish tartibida (kattadan kichikka)", ((2, "Xirurgiya"), (1, ">", 60)), (3, ">", 37.5, "37,5 dan yuqori harorat"),
          2, BOLIM, {1: 5, 2: 22, 3: 7, 4: 14, 5: 9, 6: 7})
    # 2-variant: dorilar
    GUR = ["Antibiotik", "Og'riq qoldiruvchi", "Vitamin", "Antigistamin"]
    dn = ["Amoksitsillin", "Seftriakson", "Azitromitsin", "Paratsetamol", "Ibuprofen", "Analgin", "Ketorol", "Askorbin kislota",
          "B12 vitamini", "D3 vitamini", "Loratadin", "Suprastin", "Setirizin", "Sefazolin", "Diklofenak"]
    rows = [(f"{R.choice(dn)} №{R.randint(1, 99)}", R.choice(GUR), round(R.randint(3000, 60000), -2), R.randint(5, 120), sana(2026, 2028))
            for _ in range(n)]
    build(2, "Dorixona ombori", ["Dori nomi", "Guruhi", "Narxi (so'm)", "Soni", "Yaroqlilik muddati"], rows,
          [None, None, "num", "int", "date"], 2, True, "kamayish tartibida (qimmatdan arzonga)",
          ((1, "Antibiotik"), (3, "<", 50)), (3, "<", 20, "soni 20 tadan kam dorilar"), 1, GUR,
          {1: 5, 2: 22, 3: 17, 4: 13, 5: 7, 6: 14})
    # 3-variant: tahlillar
    rows = [(odam()[0], R.choice(BOLIM), R.randint(90, 165), round(R.uniform(3.6, 9.5), 1), sana(2026, 2026)) for _ in range(n)]
    build(3, "Qon tahlili natijalari", ["F.I.Sh.", "Bo'lim", "Gemoglobin (g/l)", "Glyukoza (mmol/l)", "Sana"], rows,
          [None, None, "int", "d1", "date"], 2, False, "o'sish tartibida (kichikdan kattaga)",
          ((1, "Terapiya"), (3, ">", 6.1)), (2, "<", 110, "gemoglobini 110 dan past"), 1, BOLIM,
          {1: 5, 2: 22, 3: 14, 4: 14, 5: 14, 6: 12})
    # 4-variant: xodimlar
    LAV = ["Shifokor", "Hamshira", "Laborant", "Feldsher"]
    rows = [(odam()[0], R.choice(LAV), R.choice(BOLIM), R.randint(1, 35), round(R.randint(3500000, 9000000), -4)) for _ in range(n)]
    build(4, "Shifoxona xodimlari", ["F.I.Sh.", "Lavozimi", "Bo'lim", "Staji (yil)", "Ish haqi (so'm)"], rows,
          [None, None, None, "int", "num"], 3, True, "kamayish tartibida (ko'pdan kamga)",
          ((1, "Hamshira"), (3, ">", 10)), (4, ">", 7000000, "ish haqi 7 000 000 dan yuqori"), 1, LAV,
          {1: 5, 2: 22, 3: 12, 4: 14, 5: 11, 6: 15})
    return "16", "Saralash, filtr, shartli formatlash va kiritishni tekshirish", V, start


# ======================================================================
#  16-dars. Diagrammalar va sparklaynlar
# ======================================================================
def dars16():
    V, start = [], []
    turlar = [
        ("Bemorlar harorati (°C)", "Bemor", ["1-kun", "2-kun", "3-kun", "4-kun", "5-kun"],
         [odam()[0] for _ in range(6)], lambda: round(R.uniform(36.2, 38.9), 1), "d1", "line",
         "Bo'limlar bo'yicha bemorlar", BOLIM, (8, 40)),
        ("Qon bosimi, sistolik (mm sim. ust.)", "Bemor", ["1-kun", "2-kun", "3-kun", "4-kun", "5-kun"],
         [odam()[0] for _ in range(6)], lambda: R.randint(105, 175), "int", "line",
         "Tashxislar ulushi", ["Gipertoniya", "Qandli diabet", "Pnevmoniya", "Gastrit", "Boshqa"], (5, 35)),
        ("Bo'limlarga yotqizilgan bemorlar", "Bo'lim", ["Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"],
         BOLIM + ["Travmatologiya"], lambda: R.randint(20, 95), "int", "bar",
         "Bemorlar yosh guruhlari bo'yicha", ["0–17 yosh", "18–40 yosh", "41–60 yosh", "60+ yosh"], (30, 140)),
        ("Dorilar sarfi (qadoq)", "Dori", ["Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"],
         ["Paratsetamol", "Seftriakson", "Analgin", "Ibuprofen", "Omeprazol", "Loratadin"], lambda: R.randint(40, 300), "int", "bar",
         "Dori guruhlari ulushi", ["Antibiotiklar", "Og'riq qoldiruvchilar", "Vitaminlar", "Boshqalar"], (50, 400)),
    ]
    for k, (nom, ust, kunlar, nomlar, gen, fmt, chart, pnom, plabels, (pa, pb)) in enumerate(turlar, 1):
        data = [[gen() for _ in range(5)] for _ in nomlar]     # bir marta yaratiladi: boshlang'ich fayl = javob fayli
        pv = [R.randint(pa, pb) for _ in plabels]
        last = 3 + len(nomlar)
        pr = last + 2
        for kind in ("start", "javob"):
            s = Varaq(f"{k}-variant"); s.title(nom, 7)
            s.row(3, 1, [ust] + kunlar + ["Dinamika"], bold=True)
            for i, (n, v) in enumerate(zip(nomlar, data)):
                s.row(4 + i, 1, [n] + v, [None] + [fmt] * 5)
            s.boxes.append((3, 1, last, 7))
            s.row(pr, 1, [pnom, "Soni"], bold=True)
            for i, (lab, x) in enumerate(zip(plabels, pv)):
                s.row(pr + 1 + i, 1, [lab, x], [None, "int"])
            s.boxes.append((pr, 1, pr + len(pv), 2))
            s.pr, s.plabels, s.pv = pr, plabels, pv
            s.widths = {1: 24, **{c: 9 for c in range(2, 7)}, 7: 16}
            s.data, s.nomlar, s.kunlar, s.fmt, s.chart, s.nom_ = data, nomlar, kunlar, fmt, chart, nom
            (start if kind == "start" else V).append(s)
    for k, b in enumerate(V, 1):
        pv = b.pv
        last = 3 + len(b.nomlar)
        b.spark = ("G", 4, last, "B", "F")
        if b.chart == "line":
            b.charts.append(("line", dict(row=4, title=f"{b.nomlar[0]} — {b.nom_.split('(')[0].strip().lower()}", last=last)))
        else:
            b.charts.append(("bar", dict(last=last, title=b.nom_)))
        b.charts.append(("pie", dict(r1=b.pr, r2=b.pr + len(pv), title=b.c[(b.pr, 1)]["v"])))
        typ = "chiziqli (График)" if b.chart == "line" else "ustunli (Гистограмма)"
        what = f"1-qator ({b.nomlar[0]}) uchun" if b.chart == "line" else "butun jadval (A3:F" + str(last) + ") uchun"
        b.steps = [f"Boshlang'ich fayldagi «{k}-variant» varag'ini oching (jadval tayyor).",
                   f"{what} {typ} diagramma qo'shing: belgilang → Вставка → Диаграммы.",
                   "Diagrammaga sarlavha yozing; o'q nomlarini qo'shing (+ tugmasi → Названия осей).",
                   f"A{b.pr}:B{b.pr + len(pv)} bo'yicha doiraviy (Круговая) diagramma qo'shing, foizlarni ko'rsating (Подписи данных).",
                   f"G4:G{last} ga sparklayn qo'ying: Вставка → Спарклайны → График, diapazon B4:F{last}.",
                   "Sparklaynda eng yuqori nuqtani belgilang (Конструктор → Максимальная точка)."]
        b.nazorat = [("Doiraviy diagramma ma'lumoti jami", f"=SUM(B{b.pr + 1}:B{b.pr + len(pv)})", sum(pv), "Ma'lumot o'zgarmaganini tekshiradi")]
        b.extra = eskiz(b)
        b.card_rows, b.card_more = (1, last), False
        b.card_note = (f"Jadval va doiraviy diagramma ma'lumoti (A{b.pr}:B{b.pr + len(pv)}) boshlang'ich faylda tayyor. "
                       "Natija taxminan shunday bo'ladi:")
    return "17", "Diagrammalar va sparklaynlar", V, start


# ---------- oq-qora diagramma eskizlari (varaqcha uchun) ----------
def svg_line(vals, labels, w=230, h=110):
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.2 or 1
    lo -= pad; hi += pad
    xs = [30 + i * (w - 45) / (len(vals) - 1) for i in range(len(vals))]
    ys = [10 + (hi - v) / (hi - lo) * (h - 35) for v in vals]
    pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in zip(xs, ys))
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" fill="none" stroke="#000"/>',
           f'<line x1="30" y1="{h - 25}" x2="{w - 10}" y2="{h - 25}" stroke="#000"/><line x1="30" y1="8" x2="30" y2="{h - 25}" stroke="#000"/>',
           f'<polyline points="{pts}" fill="none" stroke="#000" stroke-width="1.6"/>']
    out += [f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.2" fill="#000"/>' for x, y in zip(xs, ys)]
    out += [f'<text x="{x:.0f}" y="{h - 12}" font-size="8" text-anchor="middle">{html.escape(l)}</text>' for x, l in zip(xs, labels)]
    return "".join(out) + "</svg>"


def svg_bar(series, labels, w=230, h=110):
    hi = max(max(s) for s in series)
    n, m = len(labels), len(series)
    gw = (w - 45) / n
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" fill="none" stroke="#000"/>',
           f'<line x1="30" y1="{h - 25}" x2="{w - 10}" y2="{h - 25}" stroke="#000"/><line x1="30" y1="8" x2="30" y2="{h - 25}" stroke="#000"/>']
    shades = ["#000", "#555", "#888", "#aaa", "#ccc", "#eee"]
    for i in range(n):
        for j, s in enumerate(series):
            bh = s[i] / hi * (h - 40)
            x = 33 + i * gw + j * (gw - 6) / m
            out.append(f'<rect x="{x:.1f}" y="{h - 25 - bh:.1f}" width="{(gw - 6) / m:.1f}" height="{bh:.1f}" fill="{shades[j % 6]}" stroke="#000" stroke-width="0.4"/>')
        out.append(f'<text x="{33 + i * gw + (gw - 6) / 2:.0f}" y="{h - 12}" font-size="8" text-anchor="middle">{html.escape(labels[i][:6])}</text>')
    return "".join(out) + "</svg>"


def svg_pie(vals, labels, w=230, h=110):
    tot = sum(vals); a = -math.pi / 2; cx, cy, r = 55, h / 2, h / 2 - 8
    shades = ["#fff", "#bbb", "#777", "#333", "#ddd"]
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" fill="none" stroke="#000"/>']
    for i, v in enumerate(vals):
        b = a + v / tot * 2 * math.pi
        large = 1 if b - a > math.pi else 0
        x1, y1, x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a), cx + r * math.cos(b), cy + r * math.sin(b)
        out.append(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f} Z" fill="{shades[i % 5]}" stroke="#000" stroke-width="0.8"/>')
        m = (a + b) / 2
        out.append(f'<text x="{cx + r * 0.62 * math.cos(m):.0f}" y="{cy + r * 0.62 * math.sin(m) + 3:.0f}" font-size="8" text-anchor="middle" '
                   f'fill="{"#fff" if i % 5 == 3 else "#000"}">{round(v / tot * 100)}%</text>')
        out.append(f'<rect x="112" y="{12 + i * 16}" width="9" height="9" fill="{shades[i % 5]}" stroke="#000"/>'
                   f'<text x="125" y="{20 + i * 16}" font-size="8.5">{html.escape(labels[i])}</text>')
        a = b
    return "".join(out) + "</svg>"


def eskiz(s):
    if s.chart == "line":
        c1 = svg_line(s.data[0], s.kunlar, w=250, h=100)
    else:
        c1 = svg_bar([list(col) for col in zip(*s.data)], s.nomlar, w=250, h=100)
    return f'<div class="eskiz">{c1}{svg_pie(s.pv, s.plabels, w=250, h=100)}</div>'


# ======================================================================
#  17-dars. Yakuniy amaliy ish (A/B/C daraja)
# ======================================================================
def dars17():
    V = []
    TAHLIL = {"Umumiy qon": 35000, "Glyukoza": 25000, "Xolesterin": 45000, "Biokimyo": 120000, "Koagulogramma": 80000}
    DORI = {"Paratsetamol": ("Og'riq qoldiruvchi", 3500), "Ibuprofen": ("Og'riq qoldiruvchi", 9800), "Analgin": ("Og'riq qoldiruvchi", 4200),
            "Sitramon": ("Og'riq qoldiruvchi", 6500), "Amoksitsillin": ("Antibiotik", 18500), "Seftriakson": ("Antibiotik", 9900),
            "Loratadin": ("Antigistamin", 7400), "Suprastin": ("Antigistamin", 12600), "Omeprazol": ("Oshqozon", 14300),
            "No-shpa": ("Spazmolitik", 23700)}

    def tahlil():
        t = R.choice(list(TAHLIL)); return (odam()[0], t, TAHLIL[t], R.randint(1, 3))

    def dori():
        d = R.choice(list(DORI)); return (d, DORI[d][0], DORI[d][1], R.randint(2, 25))
    turlar = [
        ("Laboratoriya: qon tahlillari", ["Bemor", "Tahlil turi", "Narxi (so'm)", "Soni"], tahlil),
        ("Dorixona: kunlik savdo", ["Dori nomi", "Guruhi", "Narxi (so'm)", "Soni"], dori),
        ("Statsionar: davolanish xarajati", ["Bemor", "Bo'lim", "Kunlik narx (so'm)", "Yotgan kunlar"],
         lambda: (odam()[0], R.choice(BOLIM), R.choice([150000, 180000, 220000, 250000]), R.randint(3, 14))),
        ("Emlash xonasi: oylik hisobot", ["Vaksina", "Ishlab chiqaruvchi", "Doza narxi (so'm)", "Emlanganlar"],
         lambda: (R.choice(["BTsJ", "Gepatit B", "Qizamiq", "Poliomiyelit", "Gripp", "AKDS", "Pnevmokokk", "Rotavirus"]),
                  R.choice(["Hindiston", "Rossiya", "Fransiya", "Koreya"]), round(R.randint(25000, 180000), -3), R.randint(10, 90))),
    ]
    for k, (nom, cols, gen) in enumerate(turlar, 1):
        s = Varaq(f"{k}-variant"); s.title(nom.upper(), 6)
        s.row(3, 1, ["№"] + cols + ["Jami (so'm)"], bold=True)
        seen, rows = set(), []
        while len(rows) < 8:
            x = gen()
            if x[0] not in seen:
                seen.add(x[0]); rows.append(x)
        rows.sort(key=lambda x: -(x[2] * x[3]))
        jami = []
        for i, x in enumerate(rows):
            r = 4 + i; jami.append(x[2] * x[3])
            s.row(r, 1, [i + 1, x[0], x[1], x[2], x[3], (f"=D{r}*E{r}", x[2] * x[3])], [None, None, None, "num", "int", "num"])
        s.boxes.append((3, 1, 11, 6))
        lab = [("Umumiy summa:", "=SUM(F4:F11)", sum(jami)), ("O'rtacha summa:", "=AVERAGE(F4:F11)", sum(jami) / 8),
               ("Eng katta summa:", "=MAX(F4:F11)", max(jami)), ("Eng kichik summa:", "=MIN(F4:F11)", min(jami))]
        for i, (t, f, v) in enumerate(lab):
            s.put(13 + i, 4, t, bold=True); s.merges.append((13 + i, 4, 13 + i, 5)); s.put(13 + i, 6, f, v, "num", bold=True)
        s.boxes.append((13, 4, 16, 6))
        s.cf.append(("F4:F11", ">", round(sum(jami) / 8), "FFC7CE"))
        s.widths = {1: 5, 2: 20, 3: 18, 4: 17, 5: 12, 6: 16}
        s.charts.append(("bar17", dict(title=nom)))
        s.card_hide = True     # nazorat ishi: varaqchada formula natijalari ko'rsatilmaydi
        s.card_note = "F ustuni va F13:F16 kataklarini formulalar bilan o'zingiz hisoblaysiz."
        s.steps = ["A daraja («3»): jadvalni tuzing, A1:F1 ni birlashtiring, chegara bering, narxga son formati. F4: =D4*E4, F11 gacha torting.",
                   "B daraja («4»): F13: =СУММ(F4:F11), F14: =СРЗНАЧ(F4:F11). Jadvalni «Jami» bo'yicha kamayish tartibida saralang, filtr qo'ying.",
                   "C daraja («5»): F15: =МАКС(F4:F11), F16: =МИН(F4:F11). F ustunida o'rtachadan katta summalarni qizil qiling.",
                   "C daraja («5»): B va F ustunlari bo'yicha ustunli diagramma (Гистограмма) qo'shing, sarlavha yozing.",
                   "Faylni «Familiya_18-dars_" + str(k) + "-variant» nomi bilan saqlang."]
        s.nazorat = [("A: umumiy summa (F13)", "=F13", sum(jami), "F ustuni to'g'ri bo'lsa"),
                     ("B: o'rtacha (F14)", "=ROUND(F14,0)", math.floor(sum(jami) / 8 + 0.5), "СРЗНАЧ (Excel 0,5 ni yuqoriga yaxlitlaydi)"),
                     ("C: eng katta (F15)", "=F15", max(jami), "МАКС")]
        V.append(s)
    return "18", "Yakuniy amaliy ish (oraliq nazorat uchun)", V, None


# ======================================================================
#  Excel yozish
# ======================================================================
def excel(path, varaqlar, javob):
    wb = Workbook(); wb.remove(wb.active)
    sparks = {}
    for s in varaqlar:
        ws = wb.create_sheet(s.nom)
        for (r, c), d in s.c.items():
            cell = ws.cell(row=r, column=c, value=d["v"])
            cell.font = Font(name=FONT, size=14 if r == 1 else 11, bold=d["bold"])
            if FMT[d["fmt"]]:
                cell.number_format = FMT[d["fmt"]]
            if d["align"] == "center" or (r == 3 and d["bold"]):
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for r1, c1, r2, c2 in s.merges:
            ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
        for r1, c1, r2, c2 in s.boxes:
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    ws.cell(row=r, column=c).border = BOX
        for c, w in s.widths.items():
            ws.column_dimensions[CL(c)].width = w
        ws.row_dimensions[3].height = 32
        if javob:
            if s.table:
                t = Table(displayName=s.table[1], ref=s.table[0])
                t.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=True)
                ws.add_table(t)
            elif s.filter:
                ws.auto_filter.ref = s.filter
            for rng_, op, val, color in s.cf:
                ws.conditional_formatting.add(rng_, CellIsRule(operator={">": "greaterThan", "<": "lessThan"}[op],
                                                               formula=[str(val)], fill=PatternFill("solid", fgColor=color)))
            for rng_, lst in s.dv:
                dv = DataValidation(type="list", formula1='"' + ",".join(lst) + '"', allow_blank=False)
                dv.error, dv.errorTitle = "Ro'yxatdan tanlang", "Noto'g'ri qiymat"
                ws.add_data_validation(dv); dv.add(rng_)
            if s.freeze:
                ws.freeze_panes = s.freeze
            charts(ws, s)
            if s.spark:
                sparks[s.nom] = s.spark
            nazorat(ws, s)
    wb.save(path)
    if sparks:
        add_sparklines(path, wb.sheetnames, sparks)


def charts(ws, s):
    pos = f"{CL(s.maxc + 2 if not s.nazorat else 1)}1"
    anchor_row = s.maxr + 3
    for i, (typ, d) in enumerate(s.charts):
        if typ == "line":
            ch = LineChart(); ch.add_data(Reference(ws, min_col=2, max_col=6, min_row=d["row"], max_row=d["row"]), from_rows=True)
            ch.set_categories(Reference(ws, min_col=2, max_col=6, min_row=3, max_row=3)); ch.legend = None
        elif typ == "bar":
            ch = BarChart(); ch.add_data(Reference(ws, min_col=2, max_col=6, min_row=3, max_row=d["last"]), titles_from_data=True)
            ch.set_categories(Reference(ws, min_col=1, min_row=4, max_row=d["last"])); ch.legend.overlay = False
        elif typ == "bar17":
            ch = BarChart(); ch.add_data(Reference(ws, min_col=6, min_row=3, max_row=11), titles_from_data=True)
            ch.set_categories(Reference(ws, min_col=2, min_row=4, max_row=11)); ch.legend = None
        else:
            ch = PieChart(); ch.add_data(Reference(ws, min_col=2, min_row=d["r1"], max_row=d["r2"]), titles_from_data=True)
            ch.set_categories(Reference(ws, min_col=1, min_row=d["r1"] + 1, max_row=d["r2"]))
            ch.dataLabels = DataLabelList(); ch.dataLabels.showPercent = True
            ch.legend.overlay = False
        ch.title = d["title"]; ch.title.overlay = False; ch.roundedCorners = False
        if typ != "pie":
            ch.x_axis.delete = False; ch.y_axis.delete = False
        ch.height, ch.width = 7.5, 14
        ws.add_chart(ch, f"{'A' if i == 0 else 'H'}{anchor_row}")


def nazorat(ws, s):
    if not s.nazorat:
        return
    col = s.maxc + 2
    hdr = ["Nazorat katagi (o'qituvchi uchun)", "Talabada", "Kutilgan", "Tekshiruv"]
    for i, h in enumerate(hdr):
        c = ws.cell(row=3, column=col + i, value=h)
        c.font = Font(name=FONT, bold=True); c.border = BOX; c.fill = PatternFill("solid", fgColor="FFE699")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for k, (nom, f, kut, izoh) in enumerate(s.nazorat, 1):
        r = 3 + k
        a, b = f"{CL(col + 1)}{r}", f"{CL(col + 2)}{r}"
        vals = [nom, f, kut, f'=IF(ABS({a}-{b})<0.01,"{OK}","{BAD}")']
        for i, v in enumerate(vals):
            c = ws.cell(row=r, column=col + i, value=v)
            c.font = Font(name=FONT); c.border = BOX; c.fill = PatternFill("solid", fgColor="FFF2CC")
            c.alignment = Alignment(wrap_text=True, vertical="center")
            if i in (1, 2) and isinstance(kut, (int, float)) and abs(kut) >= 1000:
                c.number_format = "#,##0"
        ws.cell(row=r, column=col + 2).comment = Comment(izoh, "O'qituvchi")
    ws.column_dimensions[CL(col)].width = 30
    for i in (1, 2, 3):
        ws.column_dimensions[CL(col + i)].width = 13
    rr = f"{CL(col + 3)}4:{CL(col + 3)}{3 + len(s.nazorat)}"
    ws.conditional_formatting.add(rr, CellIsRule(operator="equal", formula=[f'"{OK}"'], fill=PatternFill("solid", fgColor="C6EFCE")))
    ws.conditional_formatting.add(rr, CellIsRule(operator="equal", formula=[f'"{BAD}"'], fill=PatternFill("solid", fgColor="FFC7CE")))


def add_sparklines(path, names, sparks):
    tmp = Path(tempfile.mkdtemp()) / "x.xlsx"
    with zipfile.ZipFile(path) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for item in zi.infolist():
            data = zi.read(item.filename)
            for nom, (col, r1, r2, c1, c2) in sparks.items():
                if item.filename == f"xl/worksheets/sheet{names.index(nom) + 1}.xml":
                    sl = "".join(f"<x14:sparkline><xm:f>'{nom}'!{c1}{r}:{c2}{r}</xm:f><xm:sqref>{col}{r}</xm:sqref></x14:sparkline>"
                                 for r in range(r1, r2 + 1))
                    ext = ('<extLst><ext uri="{05C60535-1F16-4fd2-B633-F4F36F0B64E0}" '
                           'xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main">'
                           '<x14:sparklineGroups xmlns:xm="http://schemas.microsoft.com/office/excel/2006/main">'
                           '<x14:sparklineGroup displayEmptyCellsAs="gap" high="1" markers="1">'
                           '<x14:colorSeries rgb="FF000000"/><x14:colorNegative rgb="FF000000"/><x14:colorAxis rgb="FF000000"/>'
                           '<x14:colorMarkers rgb="FF000000"/><x14:colorFirst rgb="FF000000"/><x14:colorLast rgb="FF000000"/>'
                           '<x14:colorHigh rgb="FFC00000"/><x14:colorLow rgb="FF000000"/>'
                           f'<x14:sparklines>{sl}</x14:sparklines></x14:sparklineGroup></x14:sparklineGroups></ext></extLst>')
                    data = data.decode("utf-8").replace("</worksheet>", ext + "</worksheet>").encode("utf-8")
            zo.writestr(item, data)
    shutil.move(tmp, path)


# ======================================================================
#  PDF varaqchalar: A4 tik, ikki yarim (yuqori / past), o'rtadan qirqiladi
# ======================================================================
CSS = """
@page { size: A4; margin: 0; }
:root { --s: 1; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Times New Roman", Times, serif; color: #000; }
.page { width: 210mm; height: 297mm; page-break-after: always; position: relative; }
.page:last-child { page-break-after: auto; }
.half { height: 148.5mm; padding: 6mm 8mm 3mm; overflow: hidden; }
.cut { position: absolute; left: 0; right: 0; top: 148.5mm; border-top: 1px dashed #000; }
.cut span { position: absolute; left: 4mm; top: -2.6mm; background: #fff; font-size: calc(9pt * var(--s)); padding: 0 1mm; }
.top { display: flex; justify-content: space-between; align-items: baseline; font-size: calc(13pt * var(--s)); }
.top b { font-size: calc(14pt * var(--s)); }
.var { border: 1.5px solid #000; padding: 0 8px; font-weight: bold; font-size: calc(14pt * var(--s)); }
.who { font-size: calc(12pt * var(--s)); margin: 2mm 0 3mm; }
table.x { border-collapse: collapse; font-size: calc(12.5pt * var(--s)); margin-bottom: 1.5mm; table-layout: fixed; }
table.x td { padding: 0.6mm 1.5mm; white-space: nowrap; height: calc(6.3mm * var(--s)); overflow: hidden; }
table.x td.b { border: 1px solid #000; }
table.x td.h { font-weight: bold; text-align: center; white-space: normal; }
table.x td.n { text-align: right; }
table.x td.t { font-weight: bold; font-size: calc(14pt * var(--s)); text-align: center; }
table.x td.rn, table.x tr.cl td { color: #555; font-size: calc(9pt * var(--s)); text-align: center; padding: 0 1mm; }
table.x tr.cl td { height: calc(4mm * var(--s)); }
.note { font-size: calc(11.5pt * var(--s)); font-style: italic; margin: 0 0 1.5mm; }
.vz { font-size: calc(12.5pt * var(--s)); margin: 1.5mm 0 0; }
.vz ol { margin: 0.5mm 0 0 5mm; padding: 0; }
.vz li { margin-bottom: 0.8mm; }
.javob { font-size: calc(12.5pt * var(--s)); margin: 1.5mm 0 0; }
.eskiz { display: flex; gap: 4mm; margin: 0.5mm 0 1mm; }
.dots { color: #000; }
"""


FIT_JS = """<script>
(function () {
  var halves = [].slice.call(document.querySelectorAll('.half'));
  function ok() {
    return halves.every(function (h) {
      if (h.scrollHeight > h.clientHeight + 1) return false;
      return [].slice.call(h.querySelectorAll('table.x td')).every(function (t) { return t.scrollWidth <= t.clientWidth + 1; });
    });
  }
  var lo = 0.55, hi = 1.25;
  for (var i = 0; i < 14; i++) {
    var m = (lo + hi) / 2;
    document.documentElement.style.setProperty('--s', m);
    if (ok()) lo = m; else hi = m;
  }
  document.documentElement.style.setProperty('--s', lo);
})();
</script>"""


def card(s, dars, mavzu, k):
    r1, r2 = (1, s.maxr) if not s.card_rows else s.card_rows
    c2 = s.maxc
    in_box = lambda r, c: any(a <= r <= b and x <= c <= y for a, x, b, y in s.boxes)
    merged = {}
    for a, x, b, y in s.merges:
        merged[(a, x)] = y - x + 1
        for c in range(x + 1, y + 1):
            merged[(a, c)] = 0
    # ustun kengliklari (mm): Excel kengligiga mutanosib, lekin varaq eniga (186 mm) sig'adi
    mm = {c: s.widths.get(c, 9) * 1.9 for c in range(1, c2 + 1)}
    k_ = 188 / sum(mm.values())     # jadval varaq eniga to'liq yoyiladi
    mm = {c: v * k_ for c, v in mm.items()}
    cols = '<colgroup><col style="width:5mm">' + "".join(f'<col style="width:{mm[c]:.1f}mm">' for c in range(1, c2 + 1)) + "</colgroup>"
    rows = [cols, '<tr class="cl"><td></td>' + "".join(f"<td>{CL(c)}</td>" for c in range(1, c2 + 1)) + "</tr>"]
    for r in range(r1, r2 + 1):
        if r > 3 and s.card_rows and r > r2:
            break
        tds = [f'<td class="rn">{r}</td>']
        for c in range(1, c2 + 1):
            span = merged.get((r, c), 1)
            if span == 0:
                continue
            d = s.c.get((r, c))
            txt = html.escape(ko_rinish(d["val"], d["fmt"])) if d else ""
            if d and getattr(s, "card_hide", False) and isinstance(d["v"], str) and d["v"].startswith("="):
                txt = ""
            cls = []
            if in_box(r, c):
                cls.append("b")
            if r == 1 and d:
                cls.append("t")
            elif r == 3 and d and d["bold"]:
                cls.append("h")
            elif d and d["bold"]:
                txt = f"<b>{txt}</b>"
            if d and not isinstance(d["val"], str) and r != 1:
                cls.append("n")
            sp = f' colspan="{span}"' if span > 1 else ""
            tds.append(f'<td class="{" ".join(cls)}"{sp}>{txt}</td>')
        rows.append("<tr>" + "".join(tds) + "</tr>")
    if s.card_rows and getattr(s, "card_more", True):
        rows.append(f'<tr><td class="rn">…</td><td colspan="{c2}" class="note">… (jadval davom etadi)</td></tr>')
    steps = "".join(f"<li>{html.escape(t)}</li>" for t in s.steps)
    note = f'<p class="note">{html.escape(s.card_note)}</p>' if s.card_note else ""
    return (f'<div class="half"><div class="top"><span><b>Excel. {dars}-dars.</b> {html.escape(mavzu)}</span>'
            f'<span class="var">{k}-variant</span></div>'
            f'<div class="who">F.I.Sh.: ______________________________ &nbsp; Guruh: ________ &nbsp; Sana: ___________</div>'
            f'{note}<table class="x">{"".join(rows)}</table>{s.extra}'
            f'<div class="vz"><b>Vazifa:</b><ol>{steps}</ol></div></div>')


def pdf(path, varaqlar, dars, mavzu):
    pages = []
    for i in range(0, len(varaqlar), 2):
        halves = [card(s, dars, mavzu, i + j + 1) for j, s in enumerate(varaqlar[i:i + 2])]
        pages.append(f'<div class="page">{"".join(halves)}<div class="cut"><span>✂</span></div></div>')
    doc = f'<!doctype html><html lang="uz"><head><meta charset="utf-8"><title>{dars}-dars variantlar</title><style>{CSS}</style></head><body>{"".join(pages)}{FIT_JS}</body></html>'
    hp = path.with_suffix(".html")
    hp.write_text(doc, encoding="utf-8")
    if EDGE:
        prof = Path(tempfile.mkdtemp())
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={prof}",
                        f"--print-to-pdf={path}", hp.as_uri()], capture_output=True, timeout=120)
        shutil.rmtree(prof, ignore_errors=True)
    return hp


DARSLAR = {"12": dars11, "13": dars12, "14": dars13, "15": dars14, "16": dars15, "17": dars16, "18": dars17}
QISQA = {"12": "Tanishuv", "13": "Formatlash", "14": "Sodda formulalar", "15": "Funksiyalar", "16": "Filtr va saralash",
         "17": "Diagrammalar", "18": "Yakuniy ish"}

if __name__ == "__main__":
    only = sys.argv[1:] or list(DARSLAR)
    for key in DARSLAR:          # tasodifiy sonlar har doim bir xil chiqishi uchun hamma darslar tartib bilan quriladi
        dars, mavzu, V, start = DARSLAR[key]()
        if key not in only:
            continue
        d = HERE / f"{dars}-dars. {QISQA[key]}"
        d.mkdir(exist_ok=True)
        excel(d / f"{dars}-dars - javoblar (o'qituvchi).xlsx", V, True)
        if start:
            excel(d / f"{dars}-dars - boshlang'ich fayl (talabaga).xlsx", start, False)
        hp = pdf(d / f"{dars}-dars - variantlar (talabaga).pdf", V, dars, mavzu)
        print(dars, "->", d.name, "| html:", hp.name)
