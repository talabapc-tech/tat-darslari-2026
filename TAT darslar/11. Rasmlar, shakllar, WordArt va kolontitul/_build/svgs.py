# -*- coding: utf-8 -*-
"""
SmartArt va WordArt chizmalari (SVG). Tarqatma namunasi va dars sahifasidagi ko'rgazmalar uchun.
Word'dagi shablonlarga o'xshash ko'rinishda chiziladi (rang, shakl, matn joylashuvi).
"""
import math

W, H = 680, 420   # SmartArt maydoni: 17 x 10,5 sm


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def lines(text, n):
    """Matnni ko'pi bilan n qatorga bo'ladi (so'z chegarasida)."""
    words = text.split()
    if n == 1 or len(words) == 1:
        return [text]
    if n >= 3 and len(words) >= 3:
        k = len(words)
        cut = [0, (k + 2) // 3, (2 * k + 2) // 3, k]
        return [' '.join(words[cut[i]:cut[i + 1]]) for i in range(3) if cut[i] < cut[i + 1]]
    best, bd = None, 1e9
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        d = abs(len(a) - len(b))
        if d < bd:
            best, bd = [a, b], d
    return best


def label(cx, cy, text, size, color='#fff', n=2, weight=600):
    ls = lines(text, n)
    y0 = cy - (len(ls) - 1) * size * 0.6
    out = ''
    for i, l in enumerate(ls):
        out += '<text x="%.1f" y="%.1f" font-size="%d" font-weight="%d" fill="%s" text-anchor="middle" dominant-baseline="middle">%s</text>' % (
            cx, y0 + i * size * 1.2, size, weight, color, esc(l))
    return out


def wrap(inner, w=W, h=H):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" style="display:block;font-family:Calibri,\'Segoe UI\',Arial,sans-serif">%s</svg>' % (w, h, inner))


def process(items, cols):
    n = len(items)
    cw = 150
    step = (W - 40 - cw) / (n - 1)
    out = ''
    for i, t in enumerate(items):
        x = 20 + i * step
        pts = '%.1f,130 %.1f,130 %.1f,210 %.1f,290 %.1f,290 %.1f,210' % (x, x + cw - 36, x + cw, x + cw - 36, x, x + 36)
        out += '<polygon points="%s" fill="%s" stroke="#fff" stroke-width="3"/>' % (pts, cols[i % len(cols)])
        out += label(x + cw / 2 + 6, 210, t, 15, n=3)
    return wrap(out)


def cycle(items, cols):
    n = len(items)
    cx, cy, rx, ry, r = W / 2, H / 2, 235, 140, 60
    out = '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="#c9d4e4" stroke-width="10"/>' % (cx, cy, rx, ry)
    pts = []
    for i in range(n):
        a = -math.pi / 2 + i * 2 * math.pi / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a), a))
    for i in range(n):  # o'qlar: doiralar orasida
        a = pts[i][2] + math.pi / n
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        ang = math.degrees(math.atan2(ry * math.cos(a), -rx * math.sin(a)))
        out += '<g transform="translate(%.1f %.1f) rotate(%.1f)"><polygon points="-12,-13 14,0 -12,13" fill="#7f93b2"/></g>' % (x, y, ang)
    for i, (x, y, a) in enumerate(pts):
        out += '<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" stroke="#fff" stroke-width="4"/>' % (x, y, r, cols[i % len(cols)])
        out += label(x, y, items[i], 13, n=2)
    return wrap(out)


def hierarchy(tree, cols):
    """tree = (matn, [bolalar...]) — 3 darajagacha."""
    levels = []

    def walk(node, d):
        while len(levels) <= d:
            levels.append([])
        levels[d].append(node)
        for ch in node[1]:
            walk(ch, d + 1)
    walk(tree, 0)
    pos = {}
    # barglar (eng quyi daraja) tekis joylashadi, ota-ona ularning o'rtasida
    leaves = []

    def collect(node):
        if not node[1]:
            leaves.append(node)
        for ch in node[1]:
            collect(ch)
    collect(tree)
    bw, bh = 140, 62
    gap = (W - 40 - bw * len(leaves)) / max(1, len(leaves) - 1) if len(leaves) > 1 else 0
    for i, lf in enumerate(leaves):
        pos[id(lf)] = 20 + bw / 2 + i * (bw + gap)

    def place(node):
        if node[1]:
            xs = [place(c) for c in node[1]]
            pos[id(node)] = (xs[0] + xs[-1]) / 2
        return pos[id(node)]
    place(tree)
    ly = [40, 175, 310]
    out = ''

    def edges(node, d):
        s = ''
        for c in node[1]:
            x1, y1, x2, y2 = pos[id(node)], ly[d] + bh, pos[id(c)], ly[d + 1]
            ym = (y1 + y2) / 2
            s += '<path d="M%.1f %.1f V%.1f H%.1f V%.1f" fill="none" stroke="#7f93b2" stroke-width="3"/>' % (x1, y1, ym, x2, y2)
            s += edges(c, d + 1)
        return s
    out += edges(tree, 0)

    def boxes(node, d):
        s = '<rect x="%.1f" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="#fff" stroke-width="3"/>' % (pos[id(node)] - bw / 2, ly[d], bw, bh, cols[d % len(cols)])
        s += label(pos[id(node)], ly[d] + bh / 2, node[0], 15, n=2)
        for c in node[1]:
            s += boxes(c, d + 1)
        return s
    out += boxes(tree, 0)
    return wrap(out)


def pyramid(items, cols):
    """items — pastdan yuqoriga."""
    n = len(items)
    top, bot, lh = 20, 400, (400 - 20) / n
    cx = W / 2
    half_bot, half_top = 310, 80

    def half(y):  # y bo'yicha yarim kenglik
        return half_top + (half_bot - half_top) * (y - top) / (bot - top)
    out = ''
    for i, t in enumerate(items):
        y2 = bot - i * lh
        y1 = y2 - lh
        pts = '%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' % (cx - half(y1), y1, cx + half(y1), y1, cx + half(y2), y2, cx - half(y2), y2)
        out += '<polygon points="%s" fill="%s" stroke="#fff" stroke-width="4"/>' % (pts, cols[i % len(cols)])
        out += label(cx, (y1 + y2) / 2, t, 18, n=2 if i == n - 1 else 1)
    return wrap(out)


def venn(items, cols):
    r = 128
    centers = [(W / 2, 150), (W / 2 - 112, 268), (W / 2 + 112, 268)]
    out = ''
    for (x, y), c in zip(centers, cols):
        out += '<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" fill-opacity="0.62" stroke="#fff" stroke-width="3"/>' % (x, y, r, c)
    dirs = [(0, -52), (-70, 42), (70, 42)]
    for (x, y), (dx, dy), t in zip(centers, dirs, items):
        out += label(x + dx, y + dy, t, 17, color='#10223a', n=1, weight=700)
    return wrap(out)


def block_list(items, cols):
    out = ''
    bw, bh = 300, 150
    for i, t in enumerate(items):
        x = 30 + (i % 2) * (bw + 20)
        y = 30 + (i // 2) * (bh + 30)
        out += '<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="%s" stroke="#fff" stroke-width="3"/>' % (x, y, bw, bh, cols[i % len(cols)])
        out += label(x + bw / 2, y + bh / 2, t, 22, n=2)
    return wrap(out)


MAKERS = dict(process=process, cycle=cycle, hierarchy=hierarchy, pyramid=pyramid, venn=venn, list=block_list)

# Turlar bo'yicha rang to'plamlari ("Rangli — aksent ranglar" ga o'xshash)
PALETTES = {
    'blue': ['#2f6fd0', '#2a9d8f', '#e9a420', '#d9534f', '#7a5cc7', '#3f9ad6'],
    'green': ['#2e9e5b', '#2f6fd0', '#e9a420', '#d9534f', '#7a5cc7', '#2a9d8f'],
    'orange': ['#e8890c', '#2f6fd0', '#2e9e5b', '#d9534f', '#7a5cc7', '#2a9d8f'],
    'purple': ['#7a5cc7', '#2f6fd0', '#2e9e5b', '#e9a420', '#d9534f', '#2a9d8f'],
}


def smartart(kind, data, palette='blue'):
    return MAKERS[kind](data, PALETTES[palette])


# ----------------------------------------------------------------------------
# WORDART
# ----------------------------------------------------------------------------
def wordart(text, effect, c1, c2, stroke, w=680, h=130, uid='w'):
    """effect: 'arch' | 'wave' | 'plain'. Matn gradient bilan to'ldiriladi, kontur va soya bor."""
    defs = ('<defs><linearGradient id="g%(u)s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%(a)s"/><stop offset="1" stop-color="%(b)s"/></linearGradient>'
            '<filter id="s%(u)s" x="-10%%" y="-30%%" width="120%%" height="180%%"><feDropShadow dx="3" dy="4" stdDeviation="2.2" flood-color="#000" flood-opacity="0.35"/></filter>' % dict(u=uid, a=c1, b=c2))
    fs = max(34, min(54, int(600 / (len(text) * 0.84))))
    style = 'font-family:\'Arial Black\',Impact,Arial,sans-serif;font-weight:900;font-size:%dpx;fill:url(#g%s);stroke:%s;stroke-width:2.2;paint-order:stroke;stroke-linejoin:round' % (fs, uid, stroke)
    if effect == 'arch':
        path = 'M 30 112 Q 340 -34 650 112'
    elif effect == 'wave':
        path = 'M 20 86 C 150 56, 230 116, 340 86 S 540 56, 660 86'
    else:
        path = 'M 20 84 L 660 84'
    defs += '<path id="p%s" d="%s"/></defs>' % (uid, path)
    body = ('<text filter="url(#s%(u)s)" style="%(st)s" text-anchor="middle"><textPath href="#p%(u)s" startOffset="50%%" textLength="%(tl)d" lengthAdjust="spacingAndGlyphs">%(t)s</textPath></text>'
            % dict(u=uid, st=style, tl=600 if effect != 'plain' else 620, t=esc(text)))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" style="display:block">%s%s</svg>' % (w, h, defs, body))


# ----------------------------------------------------------------------------
# KOLONTITUL: kichik A4 sahifalar (yuqori va pastki kolontitul zonalari ko'rsatilgan)
# ----------------------------------------------------------------------------
def kol_pages(pages, scale_h=330):
    """pages: [{'label':'1-bet','h':{'l','c','r'},'f':{'l','c','r'},'titul':bool,'hline':bool,'fline':bool,'it':bool,'hbig':str}]"""
    n = len(pages)
    out = ''
    for i, p in enumerate(pages):
        x0 = i * 250 + 20
        out += '<rect x="%d" y="10" width="210" height="297" fill="#fff" stroke="#9aa8bd" stroke-width="1.5"/>' % x0
        out += '<rect x="%d" y="10" width="210" height="46" fill="#e8f0fe"/><rect x="%d" y="261" width="210" height="46" fill="#e8f0fe"/>' % (x0, x0)
        out += '<line x1="%d" y1="56" x2="%d" y2="56" stroke="#7f9fd6" stroke-width="1" stroke-dasharray="4 3"/><line x1="%d" y1="261" x2="%d" y2="261" stroke="#7f9fd6" stroke-width="1" stroke-dasharray="4 3"/>' % (x0, x0 + 210, x0, x0 + 210)
        style = 'font-size:11.5px;font-weight:700;fill:#0b3d91;%s' % ('font-style:italic;' if p.get('it') else '')
        for key, y, line in (('h', 38, p.get('hline')), ('f', 287, p.get('fline'))):
            d = p.get(key) or {}
            for al, anchor, dx in (('l', 'start', 14), ('c', 'middle', 105), ('r', 'end', 196)):
                if d.get(al):
                    col = '#c0392b' if d[al].startswith('MAXFIY') else '#0b3d91'
                    out += '<text x="%d" y="%d" text-anchor="%s" style="%s" fill="%s">%s</text>' % (x0 + dx, y, anchor, style, col, esc(d[al]))
            if line:
                yy = 45 if key == 'h' else 268
                out += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#0b3d91" stroke-width="1.4"/>' % (x0 + 14, yy, x0 + 196, yy)
        if p.get('hbig'):
            out += '<text x="%d" y="38" text-anchor="middle" style="font-size:12px;font-weight:800;fill:#0b3d91">%s</text>' % (x0 + 105, esc(p['hbig']))
        if p.get('titul'):
            for k, (yy, w, hh) in enumerate([(110, 150, 9), (130, 110, 6), (150, 130, 6), (215, 80, 5)]):
                out += '<rect x="%d" y="%d" width="%d" height="%d" rx="2" fill="#aab4c6"/>' % (x0 + 105 - w / 2, yy, w, hh)
        else:
            for k in range(11):
                w = 182 if k % 5 != 4 else 110
                out += '<rect x="%d" y="%d" width="%d" height="4" rx="2" fill="#d3d9e5"/>' % (x0 + 14, 72 + k * 17, w)
        out += '<text x="%d" y="324" text-anchor="middle" style="font-size:11px;fill:#444">%s</text>' % (x0 + 105, esc(p.get('label', '')))
    return '<svg viewBox="0 0 %d 332" width="100%%" style="display:block;font-family:Arial,Helvetica,sans-serif">%s</svg>' % (n * 250 + 20, out)
