"""savollar_manba.txt -> shpargalka.html (A4, chop etishga mos)

Ishga tushirish:  python shpargalka.py
"""
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAVZU = [
    ("FUN", "Funksional chizma (GOST 21.208)"),
    ("ELK", "Elektr chizmalar va apparatlar"),
    ("CAD", "AutoCAD"),
    ("LOY", "Loyihalash va hujjatlar"),
    ("ROS", "Avtomatik rostlash"),
    ("OLC", "O'lchash asboblari"),
    ("PNV", "Pnevmatika va trubalar"),
    ("SHK", "Shchit, kabel, montaj"),
    ("SIG", "Signallash va himoya"),
]

rows = {k: [] for k, _ in MAVZU}
n = 0
for line in (HERE / "savollar_manba.txt").read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"):
        continue
    n += 1
    code, q, right, *_ = line.split("|")
    rows[code].append((n, q.strip(), right.strip()))
assert n == 200, n

e = html.escape
qa = "".join(
    f'<h3>{e(name)} <small>({len(rows[k])})</small></h3>'
    + "".join(f'<p><b class="n">{i}.</b> {e(q)} — <b>{e(a)}</b></p>' for i, q, a in rows[k])
    for k, name in MAVZU
)

template = (HERE / "shpargalka_shablon.html").read_text(encoding="utf-8")
(HERE / "shpargalka.html").write_text(template.replace("<!--SAVOLLAR-->", qa), encoding="utf-8")
print("OK: shpargalka.html yaratildi (200 ta savol)")
