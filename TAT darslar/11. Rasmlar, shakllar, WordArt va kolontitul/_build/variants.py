# -*- coding: utf-8 -*-
"""
Word 3-dars amaliy ishi: 6 ta variant (bitta A4 varaqli tibbiy axborot varaqasi).
Har bir variantda to'rtta vosita ishlatiladi: WordArt, rasm, shakllar, kolontitul (avtomatik sahifa raqami).
Variantlar bir-biridan kolontitul matni, rasm, WordArt effekti va ranglari bilan farq qiladi.

Matnni o'zgartirish uchun shu faylni tahrirlang va build.py ni qayta ishga tushiring.
"""

TEXNIKUM = 'Shahrisabz Tibbiyot Texnikumi'

# SmartArt turlari: (kategoriya uzbekcha/EN/RU, maket EN, maket uzbekcha)
KINDS = {
    'process': ('Jarayon (Process / Процесс)', 'Basic Chevron Process', 'Oddiy chevron jarayon'),
    'cycle': ('Sikl (Cycle / Цикл)', 'Basic Cycle', 'Oddiy sikl'),
    'hierarchy': ('Ierarxiya (Hierarchy / Иерархия)', 'Organization Chart', 'Tashkiliy diagramma'),
    'pyramid': ('Piramida (Pyramid / Пирамида)', 'Basic Pyramid', 'Oddiy piramida'),
    'venn': ('Aloqa (Relationship / Отношение)', 'Basic Venn', 'Oddiy Venn diagrammasi'),
    'list': ('Ro‘yxat (List / Список)', 'Basic Block List', 'Oddiy blok ro‘yxati'),
}

VARIANTS = [
    dict(
        n=1, name='Qo‘l yuvish', title='Qo‘l yuvish bosqichlari',
        about='Sanitariya byulleteni: qo‘lni to‘g‘ri yuvish tartibi (jarayon sxemasi).',
        accent='#60a5fa', palette='blue',
        wa=dict(text='QO‘LLARNI TO‘G‘RI YUVING', effect='arch', c1='#5aa2ff', c2='#1d4ed8', stroke='#0b2a6b',
                tr='Yoy: yuqoriga (Arch Up / Дуга вверх)', color='ko‘k'),
        pic=dict(file='qol-yuvish.png', style='Oddiy ramka, oq (Simple Frame, White)'),
        paras=['Qo‘l yuvish — infeksiyadan saqlanishning eng oddiy va eng samarali usuli. Har bir bemorga yaqinlashishdan oldin va muolajadan keyin, shuningdek, tashqaridan kirganda, ovqatlanishdan oldin va hojatxonadan so‘ng qo‘lni sovun bilan yuvish shart.',
               'Qo‘lni kamida 20 soniya davomida yuving. Yuvish vaqtida barmoqlar orasi, tirnoq atrofi va bilak ham yuvilishi kerak. Yuvishni quyidagi tartibda bajaring: sxemadagi har bir bosqichni ketma-ket takrorlang.'],
        callout='Kamida 20 soniya yuving!', star='!', shape_colors=('#e9a420', '#d9534f'),
        kind='process',
        sa=['Kaftlarni ishqalang', 'Barmoq orasini yuving', 'Barmoq uchlarini ishqalang', 'Bosh barmoqni yuving', 'Chayib, quriting'],
        sa_why='Bosqichlar ketma-ket bajariladi, shuning uchun <b>Jarayon</b> (Process) turi tanlanadi.'),
    dict(
        n=2, name='Infeksiya zanjiri', title='Infeksiya zanjiri',
        about='Infeksiya qanday tarqalishi: zanjir halqalari (sikl sxemasi).',
        accent='#34d399', palette='green',
        wa=dict(text='INFEKSIYA ZANJIRI', effect='wave', c1='#7be495', c2='#12803b', stroke='#0a4a22',
                tr='To‘lqin 1 (Wave 1 / Волна 1)', color='yashil'),
        pic=dict(file='mikrob.png', style='Soyali to‘rtburchak (Drop Shadow Rectangle)'),
        paras=['Infeksiya hech qachon o‘z-o‘zidan paydo bo‘lmaydi: u zanjirning bir necha halqasi orqali tarqaladi. Zanjirning har bir halqasi oldingisiga bog‘liq bo‘lib, bitta halqa uzilsa, kasallik keyingi odamga o‘tmaydi.',
               'Hamshira vazifasi — halqalarni bilish va ularni o‘z vaqtida uzish: qo‘l gigiyenasi, dezinfeksiya, shaxsiy himoya vositalaridan foydalanish va bemorni ajratish. Zanjir halqalari quyidagi sxemada ko‘rsatilgan.'],
        callout='Zanjirni uzing!', star='!', shape_colors=('#2e9e5b', '#e9a420'),
        kind='cycle',
        sa=['Qo‘zg‘atuvchi', 'Manba', 'Chiqish yo‘li', 'Yuqish yo‘li', 'Kirish darvozasi', 'Sezgir organizm'],
        sa_why='Halqalar aylana bo‘ylab takrorlanadi, shuning uchun <b>Sikl</b> (Cycle) turi tanlanadi.'),
    dict(
        n=3, name='Bo‘lim tuzilmasi', title='Shifoxona bo‘limi tuzilmasi',
        about='Terapiya bo‘limida kim kimga bo‘ysunishi (ierarxiya sxemasi).',
        accent='#f59e0b', palette='orange',
        wa=dict(text='BO‘LIM TUZILMASI', effect='arch', c1='#ffc24d', c2='#d9730d', stroke='#7a3a00',
                tr='Yoy: yuqoriga (Arch Up / Дуга вверх)', color='to‘q sariq'),
        pic=dict(file='kasalxona.png', style='Yumshoq qirrali to‘rtburchak (Soft Edge Rectangle)'),
        paras=['Har bir kasalxona bo‘limida ish aniq tuzilma bo‘yicha olib boriladi. Bo‘lim mudiri butun bo‘lim ishi, bemorlarni davolash sifati va xodimlar intizomi uchun to‘liq javob beradi, rahbariyat oldida hisobot topshiradi.',
               'Hamshiralar va kichik hamshiralar katta hamshiraga, katta hamshira esa bo‘lim mudiriga bo‘ysunadi. Shifokorlar ham bo‘lim mudiriga hisobot beradi. Bo‘ysunish tartibi quyidagi sxemada ko‘rsatilgan.'],
        callout='Bo‘ysunish tartibini biling!', star='!', shape_colors=('#2f6fd0', '#e9a420'),
        kind='hierarchy',
        sa=('Bo‘lim mudiri', [('Katta hamshira', [('Hamshiralar', []), ('Kichik hamshiralar', [])]), ('Shifokorlar', [])]),
        sa_why='Bo‘ysunish “yuqoridan pastga” bo‘ladi, shuning uchun <b>Ierarxiya</b> (Hierarchy) turi tanlanadi.'),
    dict(
        n=4, name='Ovqatlanish piramidasi', title='Sog‘lom ovqatlanish piramidasi',
        about='Kundalik ovqat tarkibi: nimani ko‘p, nimani oz iste’mol qilish (piramida).',
        accent='#a78bfa', palette='purple',
        wa=dict(text='SOG‘LOM OVQATLANISH', effect='wave', c1='#b79cff', c2='#5b34c8', stroke='#2c1670',
                tr='To‘lqin 1 (Wave 1 / Волна 1)', color='binafsha'),
        pic=dict(file='ovqatlanish.png', style='Aks etgan yumaloq to‘rtburchak (Reflected Rounded Rectangle)'),
        paras=['Sog‘lom ovqatlanishda mahsulotlar teng miqdorda iste’mol qilinmaydi. Piramidaning asosidagi mahsulotlar kundalik ratsionning katta qismini tashkil etadi, uning cho‘qqisidagi mahsulotlar esa juda oz miqdorda yeyiladi.',
               'Piramida qoidasi bo‘yicha ovqatlanish yurak-qon tomir kasalliklari, qandli diabet va semirish xavfini sezilarli kamaytiradi. Mahsulot guruhlari ahamiyatiga ko‘ra quyidagi sxemada joylashtirilgan.'],
        callout='Shirinlik — kam!', star='!', shape_colors=('#7a5cc7', '#e9a420'),
        kind='pyramid',
        sa=['Non va yorma', 'Sabzavot va mevalar', 'Go‘sht, baliq, sut', 'Yog‘ va shirinlik'],
        sa_why='Darajalar “ko‘pdan ozga” tartiblangan, shuning uchun <b>Piramida</b> (Pyramid) turi tanlanadi. Eng pastki daraja — birinchi element.'),
    dict(
        n=5, name='Salomatlik omillari', title='Salomatlikning uch omili',
        about='Sog‘liq nimaga bog‘liq: o‘zaro bog‘liq omillar (Venn sxemasi).',
        accent='#f472b6', palette='blue',
        wa=dict(text='SALOMATLIK SIRLARI', effect='arch', c1='#ff8fb8', c2='#d6246e', stroke='#7a0f3c',
                tr='Yoy: yuqoriga (Arch Up / Дуга вверх)', color='pushti'),
        pic=dict(file='yurak.png', style='Qirrali, mat, oq (Beveled Matte, White)'),
        paras=['Salomatlik bitta omilga emas, bir nechta omilning birgalikdagi ta’siriga bog‘liq. Ular bir-birini to‘ldiradi: kundalik harakat ishtahani yaxshilaydi, to‘g‘ri ovqatlanish kuch beradi, sifatli uyqu esa organizmni tiklaydi.',
               'Uchala omil muvozanatda bo‘lsa, yurak va qon tomirlar sog‘lom ishlaydi, organizm kasalliklarga chidamli bo‘ladi, kayfiyat va mehnat qobiliyati yaxshilanadi. Omillar o‘zaro bog‘liqligi sxemada ko‘rsatilgan.'],
        callout='Muvozanat — asosiy qoida', star='!', shape_colors=('#d6246e', '#2e9e5b'),
        kind='venn',
        sa=['Harakat', 'Ovqatlanish', 'Uyqu'],
        sa_why='Omillar bir-biriga bog‘liq va kesishadi, shuning uchun <b>Aloqa</b> (Relationship) turidagi Venn tanlanadi.'),
    dict(
        n=6, name='Dori yuborish yo‘llari', title='Dori yuborish yo‘llari',
        about='Dori vositasi organizmga qanday yo‘llar bilan kiritiladi (blok ro‘yxati).',
        accent='#22d3ee', palette='blue',
        wa=dict(text='DORI YUBORISH YO‘LLARI', effect='wave', c1='#5ee0f5', c2='#0b7fa3', stroke='#06415a',
                tr='To‘lqin 1 (Wave 1 / Волна 1)', color='havorang'),
        pic=dict(file='dori-vositalari.png', style='Metall ramka (Metal Frame)'),
        paras=['Dori vositasi shifokor tayinlagan yo‘l bilan yuboriladi. Yuborish yo‘li dorining ta’sir tezligini, kuchini va davomiyligini belgilaydi: vena ichiga yuborilgan dori eng tez, og‘iz orqali berilgan dori esa sekinroq ta’sir qiladi.',
               'Hamshira har bir yo‘lning nomi va qisqartmasini bilishi, muolajani tayinlanganidek va sterillik qoidalariga rioya qilib bajarishi shart. Asosiy yo‘llar quyidagi sxemada keltirilgan.'],
        callout='Tayinlovni tekshiring!', star='!', shape_colors=('#0b7fa3', '#d9534f'),
        kind='list',
        sa=['Og‘iz orqali (per os)', 'Mushak ichiga (i/m)', 'Vena ichiga (i/v)', 'Teri ostiga (s/c)'],
        sa_why='Elementlar o‘zaro teng va ketma-ketlikka bog‘liq emas, shuning uchun <b>Ro‘yxat</b> (List) turi tanlanadi.'),
]

CRITERIA = [
    ('Hujjat va fayl', 'A4, kitob, maydonlar 2 sm; bitta betda; fayl Familiya_V№.docx nomi bilan saqlangan'),
    ('Matn', 'ikki abzats to‘liq terilgan va «Bosqichlar» raqamlangan ro‘yxati bor; Times New Roman 14 pt, ikki tomonga, imlo xatosiz'),
    ('WordArt', 'sarlavha haqiqiy WordArt (bosilganda “Shakl formati” chiqadi), matni to‘g‘ri'),
    ('WordArt effekti', 'matn effekti “Transformatsiya” qo‘llangan, rang va kontur o‘zgartirilgan'),
    ('Rasm', 'ko‘rsatilgan rasm, eni 5,5 sm, nisbati buzilmagan (cho‘zilmagan)'),
    ('Matn bilan o‘rash', '“Kvadrat”: rasm abzats boshida chapda, matn uni aylanib o‘tadi'),
    ('Rasm uslubi', 'berilgan rasm uslubi qo‘llangan'),
    ('Shakllar', 'ikki shakl chizilgan, birining ichida matn bor, ranglari o‘zgartirilgan'),
    ('Guruhlash va tartib', 'ikki shakl bitta guruhga birlashtirilgan; hech narsa matn va boshqa elementni yopmaydi'),
    ('Kolontitul', 'yuqori kolontitulda berilgan matn; pastki kolontitulda sahifa raqami <b>avtomatik maydon</b> (bosganda kulrang fon); shrift 10 pt'),
]

GRADES = [('4,5–5 ball', '«5» (a’lo)'), ('3,5–4 ball', '«4» (yaxshi)'), ('2,5–3 ball', '«3» (qoniqarli)'), ('2 ball va kam', '«2» (qayta topshiradi)')]


# Kolontitul sozlamalari (har variantda boshqacha). {p} — sahifa raqami maydoni, {n} — sahifalar soni maydoni.
HF = {
    1: dict(h=dict(l='Shahrisabz Tibbiyot Texnikumi', r='Qo‘l yuvish'), f=dict(c='Sahifa {p} dan {n}'), line=True, it=False,
            how_h='chapda «Shahrisabz Tibbiyot Texnikumi», o‘ngda «Qo‘l yuvish» ([[Tab]] ni ikki marta bosing)',
            how_f='markazda «Sahifa X dan Y» ko‘rinishida (Qo‘shish → Sahifa raqami → Sahifaning pastki qismi → «Sahifa X / Y» turi)'),
    2: dict(h=dict(c='Infeksiya zanjiri'), f=dict(r='{p} / {n}'), line=False, it=True,
            how_h='markazda «Infeksiya zanjiri», <b>kursiv</b> ([[Ctrl]]+[[E]], [[Ctrl]]+[[I]])',
            how_f='o‘ngda «X / Y» ko‘rinishida: raqam, «/» belgisi va sahifalar soni (Qo‘shish → Tezkor bloklar → Maydon → Page va NumPages)'),
    3: dict(h=dict(l='Terapiya bo‘limi', r='Sana (avtomatik)'), f=dict(c='— {p} —'), line=True, it=False,
            how_h='chapda «Terapiya bo‘limi», o‘ngda <b>bugungi sana</b> (Konstruktor → Sana va vaqt → «Avtomatik yangilash» belgisi)',
            how_f='markazda «— X —»: Sahifaning pastki qismi → Oddiy raqam 2, raqam atrofiga «—» yozing'),
    4: dict(h=dict(r='Sog‘lom ovqatlanish'), f=dict(l='Sahifa {p}'), line=False, it=False,
            how_h='o‘ngda «Sog‘lom ovqatlanish» ([[Ctrl]]+[[R]])',
            how_f='chapda «Sahifa X»: Sahifaning pastki qismi → Oddiy raqam 1; raqam oldidan «Sahifa » so‘zini yozing'),
    5: dict(h=dict(c='Salomatlik omillari'), f=dict(c='Sahifa {p} dan {n}'), line=True, it=True,
            how_h='markazda «Salomatlik omillari», <b>kursiv</b>, pastida chiziq (Bosh sahifa → Chegaralar → Pastki chegara)',
            how_f='markazda «Sahifa X dan Y» (Sahifa raqami → Sahifaning pastki qismi → «Sahifa X / Y» turi)'),
    6: dict(h=dict(l='Dori yuborish yo‘llari', r='Hamshiralik ishi'), f=dict(r='{p}'), line=True, it=False,
            how_h='chapda «Dori yuborish yo‘llari», o‘ngda «Hamshiralik ishi»',
            how_f='o‘ngda faqat raqam: Sahifa raqami → Sahifaning pastki qismi → Oddiy raqam 3'),
}


def flat(sa):
    if isinstance(sa, tuple):
        out = [sa[0]]
        for c in sa[1]:
            out += flat(c)
        return out
    return list(sa)


for _V in VARIANTS:
    _V['hf'] = HF[_V['n']]
    _V['items'] = flat(_V['sa'])


def hf_text(V, which):
    """Kolontitul matnini (tushunarli ko'rinishda) qaytaradi: 'chapda: …; o‘ngda: …'."""
    d = V['hf'][which]
    names = {'l': 'chapda', 'c': 'markazda', 'r': 'o‘ngda'}
    return '; '.join('%s: %s' % (names[k], d[k].replace('{p}', 'X').replace('{n}', 'Y')) for k in ('l', 'c', 'r') if k in d)
