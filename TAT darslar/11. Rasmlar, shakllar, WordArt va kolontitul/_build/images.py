# -*- coding: utf-8 -*-
"""
Talabalar uchun rasmlar to'plami: 8 ta tibbiy mavzudagi rasm (PNG, 1200x900).
Rasmlar SVG'da chiziladi va Chrome orqali PNG'ga o'giriladi — internet va tashqi rasm kerak emas.

Ishga tushirish (shu papkada):  python images.py
Natija: ../tarqatma/rasmlar/*.png va ../tarqatma/rasmlar.zip
"""
import os
import subprocess
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'tarqatma', 'rasmlar')
SVG_DIR = os.path.join(HERE, 'out', 'svg')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

W, H = 800, 600
SKIN, SKIN_D = '#f6c9a5', '#e5a97f'


def frame(body, c1, c2):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
            '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient></defs>'
            '<rect width="%d" height="%d" fill="url(#bg)"/>%s</svg>' % (W, H, W, H, c1, c2, W, H, body))


def hands():
    # Ikki kaft: barmoqlar, kaft, bosh barmoq
    def hand(cx, flip):
        s = -1 if flip else 1
        g = '<g transform="translate(%d 360) scale(%d 1)">' % (cx, s)
        for i, (dx, dy, h) in enumerate([(-62, -150, 150), (-24, -178, 178), (14, -170, 170), (52, -140, 140)]):
            g += '<rect x="%d" y="%d" width="32" height="%d" rx="16" fill="%s" stroke="%s" stroke-width="3"/>' % (dx - 16, dy, h, SKIN, SKIN_D)
        g += '<rect x="-84" y="-60" width="170" height="150" rx="60" fill="%s" stroke="%s" stroke-width="3"/>' % (SKIN, SKIN_D)
        g += '<rect x="-122" y="-34" width="34" height="100" rx="17" transform="rotate(-24 -105 16)" fill="%s" stroke="%s" stroke-width="3"/>' % (SKIN, SKIN_D)
        return g + '</g>'
    return hand(300, False) + hand(500, True)


def img_qol():
    b = '<rect x="90" y="40" width="250" height="34" rx="17" fill="#8fa3b8"/><rect x="90" y="40" width="46" height="130" rx="20" fill="#8fa3b8"/>'
    b += '<rect x="300" y="62" width="40" height="26" rx="8" fill="#6f8399"/>'
    b += ''.join('<path d="M%d %d q-9 16 0 26 q9 -10 0 -26z" fill="#3ba0e6"/>' % (320, y) for y in (110, 160))
    b += hands()
    b += ''.join('<circle cx="%d" cy="%d" r="%d" fill="#ffffff" fill-opacity="0.75" stroke="#bfe3ff" stroke-width="3"/>' % c
                 for c in [(250, 250, 26), (330, 200, 18), (470, 230, 30), (560, 300, 20), (400, 150, 14), (220, 330, 16), (590, 210, 14)])
    b += '<rect x="0" y="540" width="800" height="60" fill="#9bd0f5"/>'
    return frame(b, '#e6f4ff', '#bfe0fb')


def img_mikrob():
    def virus(cx, cy, r, col, dark):
        s = ''
        import math
        for k in range(14):
            a = k * 2 * math.pi / 14
            x1, y1 = cx + math.cos(a) * r, cy + math.sin(a) * r
            x2, y2 = cx + math.cos(a) * (r + r * 0.42), cy + math.sin(a) * (r + r * 0.42)
            s += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (x1, y1, x2, y2, dark, max(4, r // 9))
            s += '<circle cx="%.1f" cy="%.1f" r="%d" fill="%s"/>' % (x2, y2, max(6, r // 7), dark)
        s += '<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="5"/>' % (cx, cy, r, col, dark)
        s += '<circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity="0.55"/>' % (cx - r // 3, cy - r // 3, r // 5, dark)
        s += '<circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity="0.55"/>' % (cx + r // 3, cy + r // 4, r // 6, dark)
        return s
    b = virus(400, 300, 130, '#7ddc7a', '#2f9e44') + virus(150, 130, 50, '#ffb4b4', '#e03131') + virus(655, 150, 60, '#ffe08a', '#e8890c') \
        + virus(640, 470, 44, '#b7a6ff', '#6741d9') + virus(140, 470, 56, '#9ae6f2', '#0c8599')
    return frame(b, '#fff1f1', '#ffd9d9')


def img_stetoskop():
    b = '<path d="M250 70 v170 a110 110 0 0 0 220 0 v-170" fill="none" stroke="#3b4a5c" stroke-width="22" stroke-linecap="round"/>'
    b += '<path d="M360 350 v60 a120 120 0 0 0 240 0 v-70" fill="none" stroke="#3b4a5c" stroke-width="22" stroke-linecap="round"/>'
    b += '<circle cx="250" cy="62" r="24" fill="#c9d3de" stroke="#3b4a5c" stroke-width="8"/><circle cx="470" cy="62" r="24" fill="#c9d3de" stroke="#3b4a5c" stroke-width="8"/>'
    b += '<circle cx="600" cy="320" r="62" fill="#dfe6ee" stroke="#3b4a5c" stroke-width="14"/><circle cx="600" cy="320" r="36" fill="#9fb0c3"/>'
    b += '<circle cx="360" cy="350" r="16" fill="#e03131"/>'
    return frame(b, '#eef3f9', '#cfdbe9')


def img_ovqat():
    b = '<ellipse cx="400" cy="520" rx="330" ry="34" fill="#000" fill-opacity="0.08"/>'
    # olma
    b += '<path d="M230 190 c-70 -30 -150 20 -140 120 c8 90 80 170 140 160 c28 -4 36 -14 70 0 c60 14 130 -70 130 -160 c0 -100 -80 -150 -140 -120z" fill="#e8403a"/>'
    b += '<path d="M232 190 c-4 -30 8 -60 30 -80" stroke="#6b4423" stroke-width="12" fill="none" stroke-linecap="round"/>'
    b += '<path d="M268 130 c40 -50 100 -40 110 -30 c-10 50 -60 70 -110 30z" fill="#4caf50"/>'
    b += '<ellipse cx="170" cy="260" rx="22" ry="38" fill="#fff" fill-opacity="0.28" transform="rotate(20 170 260)"/>'
    # sabzi
    b += '<path d="M560 130 L640 470 L600 480 L520 150z" fill="#f08c00"/><path d="M560 130 L575 205 L540 210 Z" fill="#e67700"/>'
    b += '<path d="M548 130 c-24 -50 -10 -90 6 -100 M556 130 c10 -50 34 -80 50 -86 M566 132 c30 -34 64 -44 84 -34" stroke="#2f9e44" stroke-width="14" fill="none" stroke-linecap="round"/>'
    b += '<path d="M538 230 h38 M556 300 h36 M575 380 h34" stroke="#e67700" stroke-width="7" stroke-linecap="round"/>'
    # nok
    b += '<path d="M420 290 c-40 0 -52 50 -34 94 c10 26 -28 50 -28 86 c0 36 34 52 70 52 c36 0 70 -16 70 -52 c0 -36 -38 -60 -28 -86 c18 -44 6 -94 -34 -94z" fill="#cddc39" stroke="#9e9d24" stroke-width="5"/>'
    b += '<path d="M424 290 c2 -24 10 -44 24 -56" stroke="#6b4423" stroke-width="10" fill="none" stroke-linecap="round"/>'
    # stakan
    b += '<path d="M330 150 h100 l-12 120 h-76z" fill="#9bd0f5" fill-opacity="0.8" stroke="#4aa3e0" stroke-width="5"/><path d="M340 190 h80 l-6 80 h-68z" fill="#4aa3e0" fill-opacity="0.7"/>'
    return frame(b, '#f1fbe9', '#d5f0bd')


def img_yurak():
    b = '<path d="M0 430 H230 l30 -80 50 170 50 -240 40 150 30 -40 H800" stroke="#e03131" stroke-width="9" fill="none" stroke-linejoin="round" stroke-linecap="round" stroke-opacity="0.35"/>'
    b += '<path d="M400 520 C170 360 120 230 190 150 C250 85 350 105 400 190 C450 105 550 85 610 150 C680 230 630 360 400 520z" fill="#e03131"/>'
    b += '<path d="M230 190 C260 150 320 150 350 195" stroke="#fff" stroke-opacity="0.45" stroke-width="22" fill="none" stroke-linecap="round"/>'
    b += '<path d="M150 335 H300 l28 -64 46 150 40 -220 34 134 26 -34 H650" stroke="#ffffff" stroke-width="12" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
    return frame(b, '#fff0f0', '#ffd0d0')


def img_dori():
    b = '<ellipse cx="400" cy="540" rx="320" ry="26" fill="#000" fill-opacity="0.08"/>'
    # kapsula
    b += '<g transform="rotate(-32 270 230)"><rect x="140" y="170" width="260" height="120" rx="60" fill="#ffffff" stroke="#adb5bd" stroke-width="5"/>'
    b += '<path d="M270 170 h70 a60 60 0 0 1 60 60 v0 a60 60 0 0 1 -60 60 h-70z" fill="#e03131"/><rect x="140" y="170" width="260" height="120" rx="60" fill="none" stroke="#adb5bd" stroke-width="5"/></g>'
    # tabletkalar
    for (x, y, r, c) in [(560, 190, 60, '#ffd43b'), (640, 300, 46, '#74c0fc'), (520, 320, 38, '#b197fc')]:
        b += '<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="#00000022" stroke-width="5"/><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#00000033" stroke-width="6" stroke-linecap="round"/>' % (x, y, r, c, x - r + 12, y, x + r - 12, y)
    # shprits
    b += '<g transform="rotate(-18 400 440)"><rect x="200" y="410" width="320" height="64" rx="12" fill="#e7f5ff" stroke="#4aa3e0" stroke-width="6"/>'
    b += '<rect x="214" y="424" width="200" height="36" rx="6" fill="#74c0fc"/>' + ''.join('<line x1="%d" y1="410" x2="%d" y2="424" stroke="#4aa3e0" stroke-width="4"/>' % (x, x) for x in range(240, 420, 30))
    b += '<rect x="520" y="434" width="130" height="16" fill="#adb5bd"/><rect x="650" y="441" width="70" height="3" fill="#868e96"/>'
    b += '<rect x="160" y="418" width="40" height="48" rx="8" fill="#868e96"/><rect x="120" y="436" width="44" height="12" rx="6" fill="#868e96"/></g>'
    return frame(b, '#f3f0ff', '#dcd3ff')


def img_kasalxona():
    b = '<circle cx="660" cy="110" r="52" fill="#ffe066"/>'
    b += '<ellipse cx="170" cy="120" rx="80" ry="28" fill="#fff"/><ellipse cx="220" cy="100" rx="56" ry="28" fill="#fff"/>'
    b += '<rect x="0" y="470" width="800" height="130" fill="#8ce99a"/>'
    b += '<rect x="170" y="190" width="460" height="300" fill="#f1f3f5" stroke="#adb5bd" stroke-width="5"/>'
    b += '<rect x="120" y="270" width="120" height="220" fill="#dee2e6" stroke="#adb5bd" stroke-width="5"/><rect x="560" y="270" width="120" height="220" fill="#dee2e6" stroke="#adb5bd" stroke-width="5"/>'
    b += '<rect x="350" y="110" width="100" height="100" rx="8" fill="#e03131"/><rect x="390" y="126" width="20" height="68" fill="#fff"/><rect x="366" y="150" width="68" height="20" fill="#fff"/>'
    for r in range(3):
        for c in range(5):
            b += '<rect x="%d" y="%d" width="46" height="42" rx="4" fill="#a5d8ff" stroke="#74a8d6" stroke-width="3"/>' % (200 + c * 80, 220 + r * 66)
    b += '<rect x="360" y="400" width="80" height="90" rx="6" fill="#4aa3e0" stroke="#2b7bb9" stroke-width="4"/><line x1="400" y1="400" x2="400" y2="490" stroke="#2b7bb9" stroke-width="4"/>'
    for x in (140, 170, 580, 610):
        b += '<rect x="%d" y="310" width="30" height="30" rx="3" fill="#a5d8ff" stroke="#74a8d6" stroke-width="3"/>' % x
    return frame(b, '#d0ebff', '#a5d8ff')


def img_tonometr():
    import math
    b = '<rect x="80" y="300" width="300" height="190" rx="24" fill="#4aa3e0" stroke="#2b7bb9" stroke-width="6"/><rect x="100" y="326" width="260" height="22" rx="10" fill="#ffffff" fill-opacity="0.4"/>'
    b += '<path d="M380 400 C470 400 470 250 520 250" fill="none" stroke="#343a40" stroke-width="14" stroke-linecap="round"/>'
    b += '<circle cx="600" cy="250" r="125" fill="#f8f9fa" stroke="#495057" stroke-width="14"/>'
    for k in range(0, 11):
        a = math.radians(150 + k * 24)
        x1, y1 = 600 + math.cos(a) * 100, 250 + math.sin(a) * 100
        x2, y2 = 600 + math.cos(a) * 114, 250 + math.sin(a) * 114
        b += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#495057" stroke-width="6" stroke-linecap="round"/>' % (x1, y1, x2, y2)
    b += '<path d="M520 300 A95 95 0 0 1 600 155" stroke="#40c057" stroke-width="12" fill="none"/><path d="M600 155 A95 95 0 0 1 690 200" stroke="#fcc419" stroke-width="12" fill="none"/><path d="M690 200 A95 95 0 0 1 700 300" stroke="#fa5252" stroke-width="12" fill="none"/>'
    b += '<line x1="600" y1="250" x2="660" y2="190" stroke="#e03131" stroke-width="9" stroke-linecap="round"/><circle cx="600" cy="250" r="14" fill="#343a40"/>'
    b += '<ellipse cx="560" cy="500" rx="46" ry="34" fill="#343a40"/><path d="M540 470 C530 420 560 400 580 400" stroke="#343a40" stroke-width="14" fill="none"/>'
    return frame(b, '#e7f5ff', '#c5e4fb')


IMAGES = [
    ('qol-yuvish', img_qol),
    ('mikrob', img_mikrob),
    ('kasalxona', img_kasalxona),
    ('ovqatlanish', img_ovqat),
    ('yurak', img_yurak),
    ('dori-vositalari', img_dori),
    ('stetoskop', img_stetoskop),
    ('tonometr', img_tonometr),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)
    for name, fn in IMAGES:
        svg = os.path.join(SVG_DIR, name + '.svg')
        with open(svg, 'w', encoding='utf8') as f:
            f.write(fn())
        png = os.path.join(OUT, name + '.png')
        # 800x600 oynada 1,5x masshtab -> 1200x900 PNG
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--force-device-scale-factor=1.5', '--window-size=%d,%d' % (W, H),
                        '--screenshot=' + png, 'file:///' + svg.replace('\\', '/')],
                       check=True, capture_output=True)
        print('OK', name, os.path.getsize(png) // 1024, 'KB')
    zpath = os.path.join(os.path.dirname(OUT), 'rasmlar.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, _ in IMAGES:
            z.write(os.path.join(OUT, name + '.png'), 'rasmlar/' + name + '.png')
    print('ZIP', os.path.getsize(zpath) // 1024, 'KB')


if __name__ == '__main__':
    main()
