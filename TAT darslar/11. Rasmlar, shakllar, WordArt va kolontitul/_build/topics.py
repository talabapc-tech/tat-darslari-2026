# -*- coding: utf-8 -*-
"""
Mavzu bo'yicha alohida tarqatma varaqlar (har bir mavzu — alohida A4 varoq): jiddiyroq topshiriqlar.
4 mavzu x 2 variant (A, B) = 8 varoq. Har bir varoq 20 ball.

Qatorlar: (talab, yo'l, ball). Talab matnida [[Ctrl]] — tugma ko'rinishi, <b> — muhim parametr.
"""

GRADES20 = [('18–20', '«5» (a’lo)'), ('15–17', '«4» (yaxshi)'), ('12–14', '«3» (qoniqarli)'), ('11 va kam', 'qayta topshiriladi')]

TOPICS = [
    # ------------------------------------------------------------------ RASM
    dict(
        key='rasm', n=1, name='Rasm', color='#2f6fd0', code='R',
        sheets=[
            dict(
                v='A', title='Yangi hamshiralar uchun ko‘rsatma varaqasi',
                scenario='Siz bo‘lim katta hamshirasisiz. Yangi hamshiralar uchun <b>bir betli ko‘rsatma</b> tayyorlang: qo‘l gigiyenasi, qon bosimini o‘lchash va fonendoskopdan foydalanish. '
                         'Rasmlar <b>rasmlar</b> papkasida: <b>qol-yuvish.png, stetoskop.png, tonometr.png, kasalxona.png</b>.',
                text=['Har bir muolajadan oldin va keyin qo‘lni sovun bilan kamida 20 soniya yuving. Barmoq orasi va tirnoq atrofini unutmang.',
                      'Fonendoskopni quloqqa mahkam o‘rnating, membranani bemorning terisiga to‘g‘ridan-to‘g‘ri qo‘ying va tinch muhitda tinglang.',
                      'Qon bosimi manjetini yelkaga yuraq sathida bog‘lang, havoni asta-sekin yuboring va ko‘rsatkichni ikki marta o‘lchab yozib qo‘ying.'],
                rows=[
                    ('Hujjat: A4, kitob, maydonlar to‘rt tomondan <b>2 sm</b>; fayl <b>Familiya_R-A.docx</b>; <b>bitta bet</b>. Berilgan 3 abzatsni tering: Times New Roman <b>12 pt</b>, ikki tomonga, xatboshi 1,25 sm.', 'Maket › Maydonlar; Abzats oynasi', 3),
                    ('<b>qol-yuvish.png</b>: eni <b>6 sm</b>, <b>Kvadrat</b> o‘rash, 1-abzatsning chap tomonida. Rasm uslubi: <b>Oddiy ramka, oq</b>.', 'Rasm formati › O‘lcham; Matn bilan o‘rash; Rasm uslublari', 2),
                    ('<b>stetoskop.png</b>: avval <b>kvadrat qilib kesing</b> (nisbat 1:1), so‘ng eni = bo‘yi = <b>4,5 sm</b>. <b>Kvadrat</b> o‘rash, 2-abzatsning o‘ng tomonida. Kontur <b>1,5 pt</b>, to‘q ko‘k. <b>5°</b> ga buring.', 'Kesish › Nisbat › 1:1; Rasm konturi; Aylantirish', 3),
                    ('<b>tonometr.png</b>: <b>Tepa va past</b> o‘rash, 3-abzatsdan keyin <b>markazda</b>, eni <b>9 sm</b>. Yorqinlik <b>+20 %</b>.', 'Matn bilan o‘rash; Tuzatishlar › Yorqinlik', 2),
                    ('Har bir rasm tagida <b>avtomatik raqamli sarlavha</b>: «1-rasm. Qo‘l yuvish», «2-rasm. …», «3-rasm. …». Raqamlarni qo‘lda yozmang.', 'Havolalar › Sarlavha qo‘shish', 3),
                    ('<b>Suv belgisi:</b> kasalxona.png sahifa <b>markazida</b>, <b>Matn orqasida</b>, rangi <b>Oqartirish</b> (Washout), eni <b>12 sm</b>. Matn o‘qilishi kerak.', 'Rasm formati › Rang › Qayta bo‘yash', 3),
                    ('Har bir rasmga <b>muqobil matn</b> (1 gap): masalan, «Qo‘l yuvayotgan ikki qo‘l».', 'O‘ng tugma › Muqobil matn', 1),
                    ('Faylni kichraytiring: <b>Rasmlarni siqish</b> → «Elektron pochta (96 ppi)», <b>hujjatdagi barcha rasmlar</b>. Hajm <b>1 MB</b> dan oshmasin.', 'Rasm formati › Rasmlarni siqish', 1),
                    ('Tashqi ko‘rinish: bitta bet, rasmlar matnni yopmaydi, orasidagi masofa bir xil, hammasi chiroyli joylashgan.', '—', 2),
                ],
                qs=['Rasm sudralmasa, sababi nima va qanday tuzatiladi?',
                    'Rasmni <b>kesish</b> va <b>kichraytirish</b> farqi nimada?',
                    'Rasm “Matn orqasida” bo‘lib, uni bosib tanlab bo‘lmasa nima qilinadi?'],
                ans=['Rasm “Matn qatorida” holatida turibdi. Matn bilan o‘rash › Kvadrat (yoki boshqa) tanlanadi.',
                     'Kesishda ortiqcha qism yashiriladi, qolgan qismning o‘lchami saqlanadi; kichraytirishda butun rasm kichrayadi.',
                     'Bosh sahifa › Tanlash › Tanlash oynasi (Selection Pane) yoki Tanlash › Obyektlarni tanlash — ro‘yxatdan rasm tanlanadi.'],
                etalon='rasmA'),
            dict(
                v='B', title='Ota-onalar uchun eslatma: bolani infeksiyadan saqlash',
                scenario='Bolalar poliklinikasi uchun ota-onalarga <b>bir betli eslatma</b> tayyorlang. Rasmlar <b>rasmlar</b> papkasida: <b>mikrob.png, ovqatlanish.png, yurak.png, stetoskop.png, dori-vositalari.png</b>.',
                text=['Bola yo‘talganda yoki aksirganda og‘zini tirsagi bilan yopishni o‘rgating. Qo‘llar tez-tez sovun bilan yuvilsin.',
                      'Bolaning ovqatlanish tartibi me’yorida bo‘lsin: sabzavot, meva va yetarli suyuqlik organizm himoyasini kuchaytiradi.',
                      'Harorat ko‘tarilsa, o‘zboshimchalik bilan dori bermang. Shifokorni chaqiring va uning tavsiyasiga amal qiling.'],
                rows=[
                    ('Hujjat: A4, kitob, maydonlar to‘rt tomondan <b>2 sm</b>; fayl <b>Familiya_R-B.docx</b>; <b>bitta bet</b>. Berilgan 3 abzatsni tering: Times New Roman <b>12 pt</b>, ikki tomonga, xatboshi 1,25 sm.', 'Maket › Maydonlar; Abzats oynasi', 3),
                    ('<b>mikrob.png</b>: eni <b>7 sm</b>, <b>Kvadrat</b> o‘rash, 1-abzatsning <b>o‘ng</b> tomonida. Rasm uslubi: <b>Soyali to‘rtburchak</b>.', 'Rasm formati › O‘lcham; Matn bilan o‘rash; Rasm uslublari', 2),
                    ('<b>ovqatlanish.png</b>: <b>Shaklga kesish › Oval</b>, so‘ng <b>5 × 5 sm</b>. <b>Kvadrat</b> o‘rash, 2-abzatsning chap tomonida. Kontur <b>2 pt</b>, yashil.', 'Kesish › Shaklga kesish; Rasm konturi', 3),
                    ('<b>yurak.png</b>: <b>Tepa va past</b>, 3-abzatsdan keyin <b>markazda</b>, eni <b>8 sm</b>. Rasm effekti: <b>Aks ettirish</b> (Reflection). Kontrast <b>+15 %</b>.', 'Rasm effektlari; Tuzatishlar › Kontrast', 2),
                    ('<b>Rasmni almashtirish:</b> yurak.png ni <b>stetoskop.png</b> bilan almashtiring — o‘lcham, o‘rash va effektlar <b>saqlanib qolsin</b>. (Rasmni tiklash tugmasini bosmang.)', 'Rasm formati › Rasmni almashtirish', 3),
                    ('Har bir rasm tagida <b>avtomatik raqamli sarlavha</b> («1-rasm. …»). Raqamlar qo‘lda yozilmasin.', 'Havolalar › Sarlavha qo‘shish', 2),
                    ('<b>Suv belgisi:</b> dori-vositalari.png sahifa <b>markazida</b>, <b>Matn orqasida</b>, <b>Oqartirish</b>, eni <b>11 sm</b>; matn o‘qiladi.', 'Rasm formati › Rang › Qayta bo‘yash', 3),
                    ('Har bir rasmga <b>muqobil matn</b> yozing va hujjat rasmlarini <b>siqing</b> (96 ppi, barcha rasmlar).', 'O‘ng tugma › Muqobil matn; Rasmlarni siqish', 1),
                    ('Tashqi ko‘rinish: bitta bet, rasmlar matnni yopmaydi, masofalar bir xil.', '—', 1),
                ],
                qs=['“Matn qatorida” va “Kvadrat” holatlarining farqi nimada?',
                    '<b>Rasmni almashtirish</b> bilan <b>o‘chirib, yangisini qo‘yish</b> o‘rtasida qanday farq bor?',
                    'Hujjatdagi rasmlarni nima uchun siqish kerak?'],
                ans=['Matn qatorida rasm bitta katta harf kabi qatorda turadi, sudralmaydi; Kvadratda rasm erkin joylashadi, matn uni aylanib o‘tadi.',
                     'Almashtirishda joyi, o‘lchami, o‘rashi va effektlari saqlanadi; o‘chirib qo‘yilsa hammasini qaytadan sozlash kerak.',
                     'Fayl hajmi kichrayadi: pochta orqali yuborish, flesh-diskka yozish va ochish tezlashadi.'],
                etalon='rasmB'),
        ]),
    # ------------------------------------------------------------------ SHAKLLAR
    dict(
        key='shakllar', n=2, name='Shakllar', color='#2e9e5b', code='S',
        sheets=[
            dict(
                v='A', title='Blok-sxema: bemorni qabul bo‘limida qabul qilish algoritmi',
                scenario='Qabul bo‘limi uchun <b>blok-sxema</b> (algoritm) tuzing. Sxema <b>to‘qqizta shakl</b> va <b>o‘nta ulagich</b>dan iborat bo‘ladi. Shakllar matni: '
                         '<b>1</b> Bemor murojaati (boshlanish) • <b>2</b> Ro‘yxatga olish • <b>3</b> Shoshilinch yordam kerakmi? (qaror) • <b>4</b> Reanimatsiya bo‘limiga yuborish • '
                         '<b>5</b> Navbatchi shifokor ko‘rigi • <b>6</b> Yotqizish kerakmi? (qaror) • <b>7</b> Bo‘limga yotqizish • <b>8</b> Uyga tavsiyalar bilan qaytarish • <b>9</b> Tugash.',
                text=[],
                rows=[
                    ('Hujjat: A4, <b>albom</b> yo‘nalish, maydonlar <b>1,5 sm</b>; fayl <b>Familiya_S-A.docx</b>. Tepada sarlavha «Qabul qilish algoritmi»: Times New Roman <b>16 pt</b>, qalin, markazda.', 'Maket › Yo‘nalish, Maydonlar', 2),
                    ('Sxemani <b>Yangi chizma maydoni</b> ichida chizing: eni butun sahifa, bo‘yi taxminan <b>14 sm</b>.', 'Qo‘shish › Shakllar › Yangi chizma maydoni', 1),
                    ('To‘g‘ri shakl turlari: 1 va 9 — <b>Terminator</b>; 2, 4, 5, 7, 8 — <b>Jarayon</b>; 3 va 6 — <b>Qaror</b> (romb). Hammasi «Blok-sxema» guruhidan.', 'Shakllar › Blok-sxema', 3),
                    ('O‘lcham: jarayon va terminator <b>4 × 1,6 sm</b>, romblar <b>4,6 × 2,6 sm</b>. Bir xil turdagi shakllar aynan bir xil bo‘lsin.', 'Shakl formati › O‘lcham', 1),
                    ('Matn shakl ichida, <b>11 pt</b>, markazda, hech biri shakldan chiqib ketmasin.', 'Bosh sahifa › Shrift', 1),
                    ('Ranglar: 1 va 9 — <b>yashil</b>; romblar — <b>sariq</b>; 4 (reanimatsiya) — <b>qizil</b>; qolganlari — <b>ko‘k</b>. Kontur <b>1,5 pt</b>.', 'Shakl to‘ldirish; Shakl konturi', 2),
                    ('<b>Tekislash:</b> asosiy ustundagi shakllar <b>vertikal o‘q bo‘yicha markazlashgan</b> va <b>teng oraliqda</b> (Align Center + Distribute Vertically).', 'Shakl formati › Tekislash', 2),
                    ('<b>10 ta strelkali ulagich</b> (burchakli yoki to‘g‘ri), <b>ikki uchi shakllar nuqtalariga ulangan</b>. Sinov: 4-shaklni suring — ulagich ergashishi kerak (so‘ng <span class="key-cap">Ctrl</span> + <span class="key-cap">Z</span>).', 'Shakllar › Chiziqlar › Ulagich', 3),
                    ('Romblardan chiqqan yo‘llarda «<b>Ha</b>» va «<b>Yo‘q</b>» yozuvlari bor (4 ta).', 'Matn maydoni yoki ulagichga matn', 1),
                    ('«<b>Diqqat! 1 daqiqa ichida</b>» yozuvli <b>izoh shakli</b> (Callout) 4-shakl yonida, qizil.', 'Shakllar › Izohlar', 1),
                    ('Butun sxemani <b>guruhlang</b> va sahifa o‘rtasiga joylang. Tashqi ko‘rinish: bitta bet, hammasi o‘qiladi.', 'O‘ng tugma › Guruhlash', 3),
                ],
                qs=['<b>Shift</b> tugmasi shakl chizishda nima beradi?',
                    'Ulagich oddiy chiziqdan nimasi bilan farq qiladi?',
                    'Shakllarni <b>guruhlash</b> nima uchun kerak?'],
                ans=['Aylana, kvadrat, to‘g‘ri chiziq va muntazam yulduz — nisbat saqlanadi.',
                     'Ulagichning uchlari shakllarga ulanadi: shakl surilsa, ulagich ergashadi. Oddiy chiziq esa joyida qoladi.',
                     'Butun sxema bitta obyekt bo‘lib siljiydi va o‘lchami o‘zgaradi, tartibi buzilmaydi.'],
                etalon='flowA'),
            dict(
                v='B', title='Blok-sxema: dori vositasini bemorga yuborish xavfsizligi',
                scenario='Muolaja xonasi uchun dori yuborish <b>xavfsizlik algoritmini</b> blok-sxema ko‘rinishida tuzing: <b>to‘qqizta shakl</b>, <b>o‘nta ulagich</b>. Shakllar matni: '
                         '<b>1</b> Shifokor tayinlovi (boshlanish) • <b>2</b> Tayinlovni tekshirish • <b>3</b> Allergiya bormi? (qaror) • <b>4</b> Shifokorga xabar berish • '
                         '<b>5</b> Dorini tayyorlash • <b>6</b> Bemor rozimi? (qaror) • <b>7</b> Dorini yuborish • <b>8</b> Sababini yozib qo‘yish • <b>9</b> Qaydnomaga yozish (tugash).',
                text=[],
                rows=[
                    ('Hujjat: A4, <b>kitob</b> yo‘nalish, maydonlar <b>2 sm</b>; fayl <b>Familiya_S-B.docx</b>. Sarlavha «Dori yuborish algoritmi»: Times New Roman <b>16 pt</b>, qalin, markazda.', 'Maket › Yo‘nalish, Maydonlar', 2),
                    ('Sxemani <b>Yangi chizma maydoni</b> ichida chizing: eni <b>17 sm</b>, bo‘yi <b>20 sm</b> atrofida.', 'Qo‘shish › Shakllar › Yangi chizma maydoni', 1),
                    ('Shakl turlari: 1 va 9 — <b>Terminator</b>; 2, 4, 5, 7, 8 — <b>Jarayon</b>; 3 va 6 — <b>Qaror</b>. Hammasi «Blok-sxema» guruhidan.', 'Shakllar › Blok-sxema', 3),
                    ('O‘lcham: jarayon va terminator <b>5 × 1,5 sm</b>, romblar <b>5 × 2,6 sm</b>. Bir xil turdagi shakllar bir xil.', 'Shakl formati › O‘lcham', 1),
                    ('Matn shakl ichida, <b>11 pt</b>, markazda. Boshlanish va tugash shakllarida matn <b>qalin</b>.', 'Bosh sahifa › Shrift', 1),
                    ('Ranglar: 1 va 9 — <b>binafsha</b>; romblar — <b>to‘q sariq</b>; 4 va 8 — <b>qizil</b>; qolganlari — <b>havorang</b>. Kontur <b>1,5 pt</b>. Barcha shakllarga <b>yengil soya</b>.', 'Shakl to‘ldirish; Shakl effektlari › Soya', 2),
                    ('<b>Tekislash:</b> asosiy ustun markazlashgan va teng oraliqda; qaror shoxlari (4 va 8) <b>bir sathda</b> (Align Top yoki Middle).', 'Shakl formati › Tekislash', 2),
                    ('<b>10 ta strelkali ulagich</b>, ikki uchi shakllarga ulangan; <b>Ha / Yo‘q</b> yo‘llari uchun ulagich rangi har xil (yashil / qizil). Sinov: 5-shaklni suring.', 'Ulagich; Shakl konturi', 3),
                    ('Romblardan chiqqan 4 yo‘lda «<b>Ha</b>» va «<b>Yo‘q</b>» yozuvlari.', 'Matn maydoni yoki ulagichga matn', 1),
                    ('Pastda <b>izoh shakli</b>: «3 to‘g‘rilik: to‘g‘ri bemor, to‘g‘ri dori, to‘g‘ri doza».', 'Shakllar › Izohlar', 1),
                    ('Butun sxemani <b>guruhlang</b>, sahifa o‘rtasiga joylang. Bitta bet, hammasi o‘qiladi.', 'O‘ng tugma › Guruhlash', 3),
                ],
                qs=['Chizma maydoni (Drawing Canvas) nima uchun qulay?',
                    'Shaklni siljitganda ulagich ergashmasa, sabab nima?',
                    'Ustma-ust tushgan shakllarda qaysi biri tepada turishini qanday o‘zgartirasiz?'],
                ans=['Barcha shakllar bitta maydon ichida bo‘ladi, matn bilan aralashib ketmaydi, bir butun ko‘chiriladi.',
                     'Ulagichning uchi shaklning bog‘lanish nuqtasiga ulanmagan (erkin qolgan). Uni shakl chetidagi nuqtaga qayta ulash kerak.',
                     'Shakl formati › Oldinga olib chiqish / Orqaga yuborish.'],
                etalon='flowB'),
        ]),
    # ------------------------------------------------------------------ KOLONTITUL
    dict(
        key='kolontitul', n=3, name='Kolontitul', color='#e9a420', code='K',
        sheets=[
            dict(
                v='A', title='Referat: titul varag‘i, kolontitul va avtomatik sahifa raqami',
                scenario='Siz «Hamshiralik ishi tarixi» mavzusida <b>6 betli referat</b> tayyorlayapsiz. Matnni o‘zingiz yozmang: yangi hujjatda <b>=rand(12,6)</b> yozib <span class="key-cap">Enter</span> bosing (rus tilidagi Wordda <b>=рэнд(12,6)</b>) — Word tayyor matn yaratadi. '
                         'Betlar 6 tadan kam bo‘lsa, birinchi sonni oshiring. Birinchi bet — titul varag‘i: «REFERAT», mavzu va F.I.O.',
                text=[],
                rows=[
                    ('Hujjat: A4, maydonlar <b>3 / 1,5 / 2 / 2 sm</b>; fayl <b>Familiya_K-A.docx</b>; Times New Roman <b>14 pt</b>, interval <b>1,5</b>, xatboshi 1,25 sm; <b>6 bet</b>.', 'Maket › Maydonlar; Abzats oynasi', 3),
                    ('<b>Titul varag‘i</b> (1-bet): «REFERAT», mavzu, F.I.O. markazda; <b>2-betdan</b> matn boshlanadi (<span class="key-cap">Ctrl</span> + <span class="key-cap">Enter</span> bilan).', 'Qo‘shish › Sahifani uzish', 2),
                    ('<b>Yuqori kolontitul</b> (2-betdan): «Hamshiralik tarixi» — <b>markazda</b>, <b>kursiv</b>, Times New Roman <b>10 pt</b>, ostida <b>chiziq</b>.', 'Qo‘shish › Yuqori kolontitul; Bosh sahifa › Chegaralar', 4),
                    ('<b>Birinchi sahifa uchun alohida kolontitul:</b> titul varag‘ida kolontitul va raqam <b>ko‘rinmasin</b>.', 'Kolontitul asboblari › Konstruktor › Birinchi sahifa uchun alohida', 2),
                    ('<b>Avtomatik sahifa raqami:</b> pastki kolontitulda <b>o‘ng tomonda</b>, Times New Roman 12 pt. Titul ham hisobga olinadi: 2-betda «<b>2</b>» bo‘lsin.', 'Qo‘shish › Sahifa raqami › Sahifaning pastki qismi', 2),
                    ('Pastki kolontitulda <b>chapda</b> «Familiya Ism» yozuvi, o‘ngda <b>«X / Y»</b> (X — bet raqami, Y — jami betlar soni; ikkalasi <b>maydon</b>).', 'Qo‘shish › Tezkor bloklar › Maydon › Page va NumPages', 3),
                    ('Pastki kolontitul <b>markazida</b> <b>bugungi sana</b> — «<b>Avtomatik yangilash</b>» belgisi bilan.', 'Konstruktor › Sana va vaqt', 2),
                    ('Kolontitul matnining rangi <b>kulrang</b> (#7F7F7F), kolontitul masofasi yuqoridan va pastdan <b>1,25 sm</b>.', 'Shrift rangi; Kolontitul asboblari › Konstruktor › Joylashuv', 1),
                    ('Tekshirish: <span class="key-cap">Ctrl</span> + <span class="key-cap">P</span> — barcha betlarda raqamlar ketma-ket; kolontitul asosiy matnga tegmaydi; raqamlar qo‘lda yozilmagan.', 'Fayl › Chop etish', 1),
                ],
                qs=['Kolontitul nima va u qayerda yoziladi?',
                    'Sahifa raqamini nima uchun qo‘lda yozib bo‘lmaydi?',
                    'Titul varag‘ida raqam ko‘rinmasligi uchun nima qilinadi?'],
                ans=['Kolontitul — sahifaning yuqori va pastki chetidagi, barcha betlarda takrorlanadigan yozuv (hujjat nomi, sana, raqam). Qo‘shish › Yuqori / Pastki kolontitul orqali yoki chetga ikki marta bosib kiritiladi.',
                     'Raqam maydon (field) bo‘lishi kerak: bet qo‘shilsa yoki o‘chirilsa raqamlar o‘zi yangilanadi. Qo‘lda yozilsa har betda bir xil bo‘ladi va tartib buziladi.',
                     'Kolontitul asboblari › Konstruktor › «Birinchi sahifa uchun alohida kolontitul» (Different First Page) belgilanadi.'],
                etalon='kolA'),
            dict(
                v='B', title='Hisobot: juft va toq betlar, bo‘limlar, raqamlash',
                scenario='Davolash bo‘limining <b>8 betli yillik hisobotini</b> tayyorlang. Matn uchun yangi hujjatda <b>=rand(14,6)</b> yozib <span class="key-cap">Enter</span> bosing (rus tilidagi Wordda <b>=рэнд(14,6)</b>); betlar kam bo‘lsa, sonni oshiring. '
                         'Tuzilishi: <b>1-bo‘lim</b> — titul varag‘i va mundarija (1–2-betlar), <b>2-bo‘lim</b> — asosiy qism (3-betdan).',
                text=[],
                rows=[
                    ('Hujjat: A4, maydonlar <b>2 sm</b> (to‘rt tomondan); fayl <b>Familiya_K-B.docx</b>; Times New Roman <b>12 pt</b>; kamida <b>8 bet</b>.', 'Maket › Maydonlar', 2),
                    ('<b>Bo‘limlar:</b> 3-bet boshida <b>bo‘lim uzilishi</b> (Keyingi sahifadan). Hujjatda <b>2 ta bo‘lim</b> bo‘lsin.', 'Maket › Uzilishlar › Keyingi sahifa', 2),
                    ('<b>1-bo‘lim</b> (1–2-bet): titul va mundarija. Titulda kolontitul va raqam ko‘rinmasin.', 'Birinchi sahifa uchun alohida', 2),
                    ('<b>Toq va juft betlar uchun har xil kolontitul:</b> toq betda yuqorida <b>o‘ngda</b> «Davolash bo‘limi hisoboti»; juft betda yuqorida <b>chapda</b> «Shahrisabz Tibbiyot Texnikumi».', 'Konstruktor › Toq va juft sahifalar uchun har xil', 4),
                    ('Sahifa raqami <b>tashqi chetda</b>: toq betda pastda <b>o‘ngda</b>, juft betda pastda <b>chapda</b>. Raqamlar avtomatik.', 'Sahifa raqami › Sahifaning pastki qismi', 3),
                    ('<b>2-bo‘lim</b> kolontituli boshqacha: yuqorida «II bo‘lim. Natijalar». Buning uchun <b>«Oldingi bilan bog‘lash»</b> (Link to Previous) o‘chiriladi.', 'Konstruktor › Oldingi bilan bog‘lash', 4),
                    ('<b>Raqamlash formati:</b> 1-bo‘limda <b>rim raqamlari</b> (I, II), 2-bo‘limda <b>1 dan</b> qayta boshlansin (arab raqamlari).', 'Sahifa raqami › Sahifa raqami formati › Boshlash', 3),
                ],
                qs=['Toq va juft betlar uchun har xil kolontitul nima uchun kerak?',
                    'Bo‘limlar orasida kolontitul o‘zgarmasa, sabab nima?',
                    'Sahifa raqamini 1 dan emas, boshqa raqamdan qanday boshlash mumkin?'],
                ans=['Ikki tomonlama bosmada raqam va nom doim tashqi chetda turishi uchun (kitob, hisobot ko‘rinishi).',
                     'Yangi bo‘limda «Oldingi bilan bog‘lash» yoqilgan: kolontitul oldingisidan nusxa bo‘ladi. Uni o‘chirib, keyin matnni o‘zgartirish kerak.',
                     'Sahifa raqami › Sahifa raqami formati › «Boshlash» (Start at) maydoniga kerakli son yoziladi.'],
                etalon='kolB'),
        ]),
    # ------------------------------------------------------------------ WORDART
    dict(
        key='wordart', n=4, name='WordArt', color='#d6246e', code='W',
        sheets=[
            dict(
                v='A', title='Plakat: «Sog‘lom turmush tarzi haftaligi»',
                scenario='Texnikum yo‘lagiga osiladigan <b>A4 plakat</b> tayyorlang. Plakat matni: haftalik dastur — <b>Dushanba:</b> qo‘l gigiyenasi ustaxonasi; <b>Chorshanba:</b> qon bosimini bepul o‘lchash; <b>Juma:</b> sport musobaqasi. Rasm: <b>yurak.png</b>.',
                text=[],
                rows=[
                    ('Hujjat: A4, <b>kitob</b>, maydonlar <b>1,5 sm</b>; fayl <b>Familiya_W-A.docx</b>; <b>bitta bet</b>.', 'Maket › Maydonlar', 1),
                    ('<b>Asosiy sarlavha — WordArt:</b> «SOG‘LOM TURMUSH TARZI HAFTALIGI». Transformatsiya: <b>Yoy (yuqoriga)</b>. Eni <b>18 sm</b>, varaq tepasida, markazda.', 'Qo‘shish › WordArt; Shakl formati › Matn effektlari › Transformatsiya', 3),
                    ('Sarlavha bezagi: <b>gradient to‘ldirish</b> (ikki rang), kontur <b>1,5 pt</b>, <b>soya</b> (pastga-o‘ngga).', 'Matn to‘ldirish › Gradient; Matn konturi; Matn effektlari › Soya', 3),
                    ('<b>Ikkinchi WordArt — sana:</b> «9–15 noyabr». <b>Boshqa uslub</b> va <b>To‘lqin</b> transformatsiyasi, <b>8°</b> ga burilgan.', 'Shakl formati; Aylantirish', 2),
                    ('<b>Matn maydoni:</b> haftalik dastur (3 qator). Times New Roman <b>14 pt</b>; <b>konturi yo‘q</b>, fon rangi och. Birinchi abzatsda <b>bosh harf</b> (Drop Cap, 2 qator).', 'Qo‘shish › Matn maydoni; Bosh harf', 3),
                    ('<b>Shior</b> (oddiy matn, WordArt emas): «Harakat — hayot!» — <b>Bosh sahifa › Matn effektlari</b> bilan (soya yoki yaltirash). Tekshirib ko‘ring: bosilganda <b>Shakl formati</b> chiqmaydi.', 'Bosh sahifa › Matn effektlari va tipografika', 2),
                    ('<b>yurak.png</b>: eni <b>5 sm</b>, <b>Kvadrat</b> o‘rash, o‘ng tomonda. Sahifa <b>chegarasi</b>: 3 pt chiziq yoki naqsh.', 'Matn bilan o‘rash; Maket › Sahifa chegaralari', 2),
                    ('Tashqi ko‘rinish: WordArt <b>ko‘pi bilan 2 ta</b>; matn va fon <b>kontrast</b>, hammasi o‘qiladi; elementlar bir-birini yopmaydi; bitta bet.', '—', 4),
                ],
                qs=['WordArt oddiy matn effektidan nimasi bilan farq qiladi?',
                    'Qaysi hujjatlarda WordArt ishlatilmaydi va nima uchun?',
                    'WordArt’da matn o‘zgartirilmasa, nima qilinadi?'],
                ans=['WordArt alohida ramkali shakl: sudrash, burish, egrilash mumkin. Matn effekti esa oddiy matnda qoladi.',
                     'Rasmiy hujjatlarda (ariza, hisobot, dalolatnoma): ular qat’iy talabga ega — TNR 14 pt, qalin, markazda; bezak hujjat jiddiyligini buzadi.',
                     'Ramka ichiga bosib, matnni belgilab yozing (yoki ramkani tanlab, matnni kiriting).'],
                etalon='wordA'),
            dict(
                v='B', title='Plakat: «Qon topshirish kuni — hayot ulashing»',
                scenario='Texnikum yo‘lagiga osiladigan <b>A4 plakat</b> tayyorlang. Plakat matni: <b>Sana:</b> 20-noyabr, <b>joy:</b> texnikum sport zali, <b>vaqt:</b> 9:00–14:00; donorlarga tavsiya: nonushta qiling, ko‘p suyuqlik iching. Rasm: <b>qol-yuvish.png</b> yoki <b>yurak.png</b>.',
                text=[],
                rows=[
                    ('Hujjat: A4, <b>albom</b>, maydonlar <b>1,5 sm</b>; fayl <b>Familiya_W-B.docx</b>; <b>bitta bet</b>.', 'Maket › Yo‘nalish, Maydonlar', 1),
                    ('<b>Asosiy sarlavha — WordArt:</b> «QON TOPSHIRING — HAYOT ULASHING». Transformatsiya: <b>To‘lqin</b>. Eni <b>24 sm</b>, markazda.', 'WordArt; Matn effektlari › Transformatsiya', 3),
                    ('Sarlavha bezagi: <b>gradient</b> to‘ldirish (qizil → to‘q qizil), kontur <b>2 pt</b>, <b>3-O aylanish</b> yoki <b>aks ettirish</b> effekti.', 'Matn to‘ldirish; Matn konturi; Matn effektlari', 3),
                    ('<b>Ikkinchi WordArt — sana:</b> «20-NOYABR». <b>Boshqa uslub</b>, <b>Shishirish</b> (Inflate) yoki <b>Yoy</b> transformatsiyasi, <b>–6°</b> burilgan.', 'Shakl formati; Aylantirish', 2),
                    ('<b>Matn maydoni:</b> joy, vaqt va tavsiyalar (4 qator), TNR <b>14 pt</b>; konturi yo‘q; fon <b>to‘ldirilgan</b>; ro‘yxat <b>markerli</b>.', 'Matn maydoni; Bosh sahifa › Markerlar', 3),
                    ('<b>Shior</b> (oddiy matn): «Bitta tomchi — bitta umr» — <b>Bosh sahifa › Matn effektlari</b> bilan. Bosilganda <b>Shakl formati</b> <u>chiqmasligi</u> kerak.', 'Matn effektlari va tipografika', 2),
                    ('Rasm: eni <b>6 sm</b>, <b>Kvadrat</b> o‘rash; yonida «<b>Muhim!</b>» <b>shakli</b> (yulduz yoki izoh) — rasm va shakl <b>guruhlangan</b>.', 'O‘rash; Shakllar; Guruhlash', 2),
                    ('Tashqi ko‘rinish: WordArt <b>ko‘pi bilan 2 ta</b>; kontrast; o‘qilishi; <b>sahifa chegarasi</b>; bitta bet.', 'Maket › Sahifa chegaralari', 4),
                ],
                qs=['Transformatsiya qayerda va nima beradi?',
                    'Nima uchun plakatda WordArt ko‘p ishlatilmaydi?',
                    'WordArt va matn maydoni (Text Box) farqi nimada?'],
                ans=['Shakl formati › Matn effektlari › Transformatsiya: matn egri yo‘l bo‘ylab joylashadi (yoy, to‘lqin va h.k.).',
                     'Ko‘p bezak e’tiborni tarqatadi, o‘qilishi yomonlashadi; asosiy fikr yo‘qoladi.',
                     'WordArt — bezakli yozuv uchun ramka (effektlar, transformatsiya); matn maydoni — oddiy matn uchun ramka (ko‘p qatorli).'],
                etalon='wordB'),
        ]),
]


def check():
    for t in TOPICS:
        for s in t['sheets']:
            tot = sum(r[2] for r in s['rows'])
            assert tot == 20, (t['key'], s['v'], tot)
    return True


if __name__ == '__main__':
    check()
    print('OK', sum(len(t['sheets']) for t in TOPICS), 'varoq')
