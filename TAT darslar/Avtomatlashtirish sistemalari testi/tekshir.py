"""To'g'ri javob uzunligi bo'yicha bilinib qolmaganini tekshiradi.

Ishga tushirish:  python tekshir.py
Teng taqsimlanganda to'g'ri javob ~25% savolda eng uzun, ~25% da eng qisqa bo'ladi.
"""
from pathlib import Path

rows = [l.split("|") for l in (Path(__file__).resolve().parent / "savollar_manba.txt")
        .read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
eng_uzun = eng_qisqa = 0
yaqqol = []
for n, p in enumerate(rows, 1):
    r, w = len(p[2]), [len(x) for x in p[3:6]]
    if r > max(w):
        eng_uzun += 1
        if r > max(w) * 1.25 and r - max(w) > 8:
            yaqqol.append(n)
    if r < min(w):
        eng_qisqa += 1
faqat = [n for n, p in enumerate(rows, 1) if any(x.strip().lower().startswith("faqat") for x in p[3:6])]
print(f"Jami: {len(rows)}")
print(f"To'g'ri javob eng uzun: {eng_uzun} ({eng_uzun * 100 // len(rows)}%)")
print(f"To'g'ri javob eng qisqa: {eng_qisqa} ({eng_qisqa * 100 // len(rows)}%)")
print(f"Yaqqol uzun (>25%): {len(yaqqol)} {yaqqol}")
print(f"Xato variantlarda 'Faqat ...' bilan boshlanadigan: {len(faqat)} {faqat}")
