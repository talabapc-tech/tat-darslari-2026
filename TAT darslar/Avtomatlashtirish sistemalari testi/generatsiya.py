"""savollar_manba.txt -> savollar.js, savollar.json, mytestx.txt

Ishga tushirish:  python generatsiya.py
Javob variantlari har safar bir xil (seed=2026) tartibda aralashtiriladi.
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAVZULAR = {
    "CAD": "AutoCAD",
    "FUN": "Funksional chizma (GOST 21.208)",
    "ELK": "Elektr chizmalar va apparatlar",
    "LOY": "Loyihalash va hujjatlar",
    "ROS": "Avtomatik rostlash",
    "OLC": "O'lchash asboblari",
    "PNV": "Pnevmatika va trubali o'tkazishlar",
    "SHK": "Shchit, kabel va montaj",
    "SIG": "Signallash va himoya",
}

rng = random.Random(2026)
items = []
for n, line in enumerate((HERE / "savollar_manba.txt").read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip() or line.startswith("#"):
        continue
    parts = line.split("|")
    if len(parts) != 7:
        raise SystemExit(f"{n}-qator: 7 ta maydon kerak, {len(parts)} ta topildi")
    code, q, right, w1, w2, w3, izoh = (p.strip() for p in parts)
    if code not in MAVZULAR:
        raise SystemExit(f"{n}-qator: noma'lum mavzu {code}")
    opts = [right, w1, w2, w3]
    if len(set(opts)) != 4:
        raise SystemExit(f"{n}-qator: variantlar takrorlangan")
    rng.shuffle(opts)
    items.append({"id": len(items) + 1, "topic": MAVZULAR[code], "q": q,
                  "opts": opts, "ans": opts.index(right), "izoh": izoh})

if len(items) != 200:
    raise SystemExit(f"200 ta savol kutilgan, {len(items)} ta topildi")

(HERE / "savollar.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / "savollar.js").write_text(
    "// generatsiya.py tomonidan yaratilgan — qo'lda tahrirlamang\nwindow.SAVOLLAR = "
    + json.dumps(items, ensure_ascii=False) + ";\n", encoding="utf-8")

lines = []
for it in items:
    lines.append(f"{it['id']}. {it['q']}")
    lines += [("+" if i == it["ans"] else "-") + o for i, o in enumerate(it["opts"])]
    lines.append("")
(HERE / "mytestx.txt").write_text("\n".join(lines), encoding="utf-8")

dist = [sum(1 for it in items if it["ans"] == k) for k in range(4)]
print(f"OK: {len(items)} ta savol. To'g'ri javob o'rinlari A/B/C/D: {dist}")
