# -*- coding: utf-8 -*-
import json
import os

questions = [
    # =========================================================================
    # 1-BO'LIM: AXBOROT, UNING TURLARI, XOSSALARI VA O'LCHOV BIRLIKLARI (1–30)
    # =========================================================================
    {
        "id": 1,
        "topic": "Axborot asoslari",
        "q": "'Axborot' so'zi arabchadan tarjima qilinganda qanday ma'noni anglatadi?",
        "opts": ["Xabarlar, ma'lumotlar", "Hisob-kitob, raqamlar", "Texnika, asboblar", "Dasturlar to'plami"],
        "ans": 0
    },
    {
        "id": 2,
        "topic": "Axborot asoslari",
        "q": "Inson tashqi olamdagi axborotning eng katta qismini (taxminan 80-90%) qaysi sezgi a'zosi orqali qabul qiladi?",
        "opts": ["Eshitish a'zosi (quloq)", "Ko'rish a'zosi (ko'z)", "Sezish a'zosi (teri)", "Hid bilish a'zosi (burun)"],
        "ans": 1
    },
    {
        "id": 3,
        "topic": "Axborot asoslari",
        "q": "Sezgi a'zolari orqali qabul qilinishiga ko'ra axborot qanday turlarga bo'linadi?",
        "opts": ["Vizual, audial, ta'm bilish, hid bilish, taktil", "Faqat matnli va sonli", "Faqat kompyuter va telefon axboroti", "Faqat dasturiy va texnik"],
        "ans": 0
    },
    {
        "id": 4,
        "topic": "Axborot turlari",
        "q": "Taqdim etilish shakliga ko'ra kompyuterda axborot qanday asosiy turlarga ajratiladi?",
        "opts": ["Matnli, sonli, grafik, audio, video", "Faqat kitoblar va jurnallar", "Faqat internet va tarmoq", "Faqat ichki va tashqi"],
        "ans": 0
    },
    {
        "id": 5,
        "topic": "Axborot turlari",
        "q": "Tibbiyotda bemor kardiogrammasi (EKG) tasmisidagi chiziqlar qaysi turdagi axborotga misol bo'ladi?",
        "opts": ["Matnli axborot", "Grafik axborot", "Tovushli axborot", "Raqamli kodli axborot"],
        "ans": 1
    },
    {
        "id": 6,
        "topic": "Axborot turlari",
        "q": "Bemorning tana harorati ko'rsatkichi (masalan, 37.2 °C) qaysi turdagi axborotga kiradi?",
        "opts": ["Sonli axborot", "Grafik axborot", "Video axborot", "Tovushli axborot"],
        "ans": 0
    },
    {
        "id": 7,
        "topic": "Axborot turlari",
        "q": "Shifokor stetoskop orqali yurak urishini eshitishi axborotning qaysi turiga kiradi?",
        "opts": ["Grafik axborot", "Matnli axborot", "Tovushli (audio) axborot", "Sonli axborot"],
        "ans": 2
    },
    {
        "id": 8,
        "topic": "Axborot xossalari",
        "q": "Axborotning voqelikka mos kelishi, xatosiz va to'g'ri bo'lishi uning qaysi xossasi deyiladi?",
        "opts": ["Tushunarlilik", "Ishonchlilik (aniqlik)", "Qimmatlilik", "Dolzarblik"],
        "ans": 1
    },
    {
        "id": 9,
        "topic": "Axborot xossalari",
        "q": "To'g'ri qaror qabul qilish uchun axborotning yetarli hajmda bo'lishi qaysi xossa hisoblanadi?",
        "opts": ["To'liqlik", "Ixchamlik", "Maxfiylik", "Chiroylilik"],
        "ans": 0
    },
    {
        "id": 10,
        "topic": "Axborot xossalari",
        "q": "Axborotning ayni vaqtda kerakli, o'z vaqtida olingan va foydali bo'lishi nima deyiladi?",
        "opts": ["Eskirganlik", "Dolzarblik", "Qisqalik", "Oddiylik"],
        "ans": 1
    },
    {
        "id": 11,
        "topic": "Axborot xossalari",
        "q": "Axborot uni qabul qiluvchiga tushunarli tilda va shaklda bayon etilishi qaysi xossa?",
        "opts": ["Tushunarlilik", "Maxfiylik", "Hajmdorlik", "Murakkablik"],
        "ans": 0
    },
    {
        "id": 12,
        "topic": "Axborot xossalari",
        "q": "Axborot qo'yilgan maqsadga erishishda qanchalik foyda berishini ifodalovchi xossa qaysi?",
        "opts": ["Qimmatlilik (foydalilik)", "Og'irlik", "Rang-baranglik", "Doimiylik"],
        "ans": 0
    },
    {
        "id": 13,
        "topic": "Axborot jarayonlari",
        "q": "Axborot bilan bajariladigan asosiy jarayonlar to'g'ri ko'rsatilgan qatorni toping:",
        "opts": [
            "To'plash, saqlash, uzatish, qayta ishlash",
            "Faqat o'chirish va yopish",
            "Faqat sotish va sotib olish",
            "Faqat qog'ozga chop etish"
        ],
        "ans": 0
    },
    {
        "id": 14,
        "topic": "Axborot jarayonlari",
        "q": "Hamshira bemorning qon bosimi natijasini kompyuter bazasiga yozishi qaysi axborot jarayoniga kiradi?",
        "opts": ["Axborotni to'plash (kiritish)", "Axborotni yo'qotish", "Axborotni buzish", "Axborotni arxivdan chiqarish"],
        "ans": 0
    },
    {
        "id": 15,
        "topic": "Axborot jarayonlari",
        "q": "Bemorlarning elektron arxivini kompyuterning qattiq diskida saqlash qaysi jarayonga misol?",
        "opts": ["Axborotni saqlash", "Axborotni uzatish", "Axborotni yo'q qilish", "Axborotni chop etish"],
        "ans": 0
    },
    {
        "id": 16,
        "topic": "Axborot jarayonlari",
        "q": "Rentgen suratini shifokor kabinetiga lokal tarmoq orqali jo'natish qaysi jarayonga kiradi?",
        "opts": ["Axborotni qayta ishlash", "Axborotni uzatish", "Axborotni qirqish", "Axborotni o'chirish"],
        "ans": 1
    },
    {
        "id": 17,
        "topic": "Axborot jarayonlari",
        "q": "Bemorning bo'yi va vazni asosida uning tana massasi indeksini (BMI) dasturda hisoblab topish qaysi jarayon?",
        "opts": ["Axborotni qayta ishlash", "Axborotni uzatish", "Axborotni yo'qotish", "Axborotni skanerlash"],
        "ans": 0
    },
    {
        "id": 18,
        "topic": "O'lchov birliklari",
        "q": "Axborotning eng kichik o'lchov birligi nima deb ataladi?",
        "opts": ["Bayt", "Bit", "Kilobayt", "Gigabayt"],
        "ans": 1
    },
    {
        "id": 19,
        "topic": "O'lchov birliklari",
        "q": "1 bayt necha bitga teng?",
        "opts": ["2 bit", "4 bit", "8 bit", "16 bit"],
        "ans": 2
    },
    {
        "id": 20,
        "topic": "O'lchov birliklari",
        "q": "1 Kilobayt (KB) necha baytga teng?",
        "opts": ["1000 bayt", "1024 bayt", "512 bayt", "2048 bayt"],
        "ans": 1
    },
    {
        "id": 21,
        "topic": "O'lchov birliklari",
        "q": "1 Megabayt (MB) necha Kilobaytga teng?",
        "opts": ["1000 KB", "1024 KB", "2048 KB", "100 KB"],
        "ans": 1
    },
    {
        "id": 22,
        "topic": "O'lchov birliklari",
        "q": "1 Gigabayt (GB) necha Megabaytga teng?",
        "opts": ["1024 MB", "1000 MB", "500 MB", "2048 MB"],
        "ans": 0
    },
    {
        "id": 23,
        "topic": "O'lchov birliklari",
        "q": "1 Terabayt (TB) necha Gigabaytga teng?",
        "opts": ["1000 GB", "1024 GB", "512 GB", "2000 GB"],
        "ans": 1
    },
    {
        "id": 24,
        "topic": "O'lchov birliklari",
        "q": "1 Petabayt (PB) necha Terabaytga teng?",
        "opts": ["1024 TB", "100 TB", "10000 TB", "512 TB"],
        "ans": 0
    },
    {
        "id": 25,
        "topic": "O'lchov birliklari",
        "q": "Axborot o'lchov birliklarining o'sish tartibi qaysi qatorda to'g'ri ko'rsatilgan?",
        "opts": [
            "Bit, bayt, Kilobayt, Megabayt, Gigabayt, Terabayt",
            "Bayt, bit, Megabayt, Kilobayt, Gigabayt",
            "Terabayt, Gigabayt, Megabayt, Kilobayt, bayt",
            "Bit, Kilobayt, bayt, Gigabayt, Megabayt"
        ],
        "ans": 0
    },
    {
        "id": 26,
        "topic": "O'lchov birliklari",
        "q": "Standart matn faylida har bir harf, raqam yoki probel xotirada qancha joy egallaydi?",
        "opts": ["1 bit", "1 bayt (8 bit)", "1 Kilobayt", "10 bayt"],
        "ans": 1
    },
    {
        "id": 27,
        "topic": "O'lchov birliklari",
        "q": "16 bit necha baytga teng bo'ladi?",
        "opts": ["1 bayt", "2 bayt", "4 bayt", "8 bayt"],
        "ans": 1
    },
    {
        "id": 28,
        "topic": "O'lchov birliklari",
        "q": "2048 Kilobayt axborot necha Megabayt bo'ladi?",
        "opts": ["1 MB", "2 MB", "4 MB", "20 MB"],
        "ans": 1
    },
    {
        "id": 29,
        "topic": "O'lchov birliklari",
        "q": "4 Gigabayt hajmli USB fleshkaga taxminan necha Megabayt axborot sig'adi?",
        "opts": ["400 MB", "1024 MB", "4096 MB", "8192 MB"],
        "ans": 2
    },
    {
        "id": 30,
        "topic": "O'lchov birliklari",
        "q": "Quyidagi xotira hajmlaridan qaysi biri eng kattasi hisoblanadi?",
        "opts": ["500 Megabayt", "2 Gigabayt", "1 Terabayt", "900 Kilobayt"],
        "ans": 2
    },

    # =========================================================================
    # 2-BO'LIM: AXBOROT XAVFSIZLIGI VA TEXNIKA XAVFSIZLIGI (31–55)
    # =========================================================================
    {
        "id": 31,
        "topic": "Axborot xavfsizligi",
        "q": "Axborot xavfsizligi nima?",
        "opts": [
            "Axborotning maxfiyligi, butunligi va erkin foydalanish imkoniyatini himoyalash",
            "Faqat kompyuterni elektrdan o'chirish",
            "Faqat yangi o'yinlar o'rnatish",
            "Faqat kompyuter changini artish"
        ],
        "ans": 0
    },
    {
        "id": 32,
        "topic": "Axborot xavfsizligi",
        "q": "Axborotning maxfiyligi (konfidensiallik) deganda nima tushuniladi?",
        "opts": [
            "Axborotdan faqat ruxsati bor shaxslarning foydalana olishi",
            "Axborotni hammaga bepul tarqatish",
            "Axborot hajmini qisqartirish",
            "Axborotni internetga ochiq joylash"
        ],
        "ans": 0
    },
    {
        "id": 33,
        "topic": "Axborot xavfsizligi",
        "q": "Axborotning butunligi (yaxlitligi) deganda nima tushuniladi?",
        "opts": [
            "Axborotning ruxsatsiz o'zgartirilishi yoki yo'q qilinishining oldini olish",
            "Axborotni faqat bitta kompyuterda ko'rish",
            "Axborotni doimiy ravishda o'chirib turish",
            "Axborotga rasm qo'shish"
        ],
        "ans": 0
    },
    {
        "id": 34,
        "topic": "Axborot xavfsizligi",
        "q": "Axborot xavfsizligida 'zaxira nusxa' (Backup) nima uchun olinadi?",
        "opts": [
            "Tizim buzilganda yoki virus tushganda ma'lumotlarni qayta tiklash uchun",
            "Kompyuterni tezroq ishlashga majburlash uchun",
            "Monitor ekranini yorug' qilish uchun",
            "Klaviatura tugmalarini tozalash uchun"
        ],
        "ans": 0
    },
    {
        "id": 35,
        "topic": "Axborot xavfsizligi",
        "q": "Quyidagilardan qaysi biri eng ishonchli parol hisoblanadi?",
        "opts": ["12345678", "Ali1995", "Tr#9kL!2026mQ", "password"],
        "ans": 2
    },
    {
        "id": 36,
        "topic": "Axborot xavfsizligi",
        "q": "Parol yaratishda qaysi odat eng xavfli hisoblanadi?",
        "opts": [
            "Tug'ilgan sana, ism yoki ketma-ket raqamlardan foydalanish",
            "Katta va kichik harflarni aralashtirish",
            "Belgilar sonini 10 tadan oshirish",
            "Maxsus belgilarni qo'shish"
        ],
        "ans": 0
    },
    {
        "id": 37,
        "topic": "Axborot xavfsizligi",
        "q": "Kompyuter virusi nima?",
        "opts": [
            "Kompyuter ishiga zarar yetkazuvchi va o'z-o'zidan ko'payuvchi maxsus zararli dastur",
            "Kompyuter ichiga kirib qolgan chang zarralari",
            "Kompyuterning eskirib qolgan qismi",
            "Monitor ekranidagi dog'"
        ],
        "ans": 0
    },
    {
        "id": 38,
        "topic": "Axborot xavfsizligi",
        "q": "Viruslar kompyuterga ko'pincha qanday yo'llar bilan yuqadi?",
        "opts": [
            "Tekshirilmagan fleshkalar va shubhali internet saytlaridan yuklab olish orqali",
            "Klaviaturani qattiq bosish orqali",
            "Monitorni o'chirib yoqish orqali",
            "Kompyuter yonida gaplashish orqali"
        ],
        "ans": 0
    },
    {
        "id": 39,
        "topic": "Axborot xavfsizligi",
        "q": "Antivirus dasturlarining asosiy vazifasi nima?",
        "opts": [
            "Viruslarni qidirib topish, zararsizlantirish va tizimni himoya qilish",
            "Matn terish va jadvallar tuzish",
            "Musiqa va videolarni ijro etish",
            "Kompyuter ekranini o'chirib qo'yish"
        ],
        "ans": 0
    },
    {
        "id": 40,
        "topic": "Axborot xavfsizligi",
        "q": "Quyidagilardan qaysi biri antivirus dasturi hisoblanadi?",
        "opts": ["Kaspersky (yoki Windows Defender)", "Microsoft Excel", "Adobe Photoshop", "WinRAR"],
        "ans": 0
    },
    {
        "id": 41,
        "topic": "Axborot xavfsizligi",
        "q": "Fishing (Phishing) hujumi nima?",
        "opts": [
            "Soxta sayt yoki xabarlar orqali foydalanuvchining login va parolini aldab olish",
            "Kompyuter sichqonchasini tez bosish",
            "Kompyuterga yangi o'yin o'rnatish",
            "Fayllarni boshqa papkaga ko'chirish"
        ],
        "ans": 0
    },
    {
        "id": 42,
        "topic": "Texnika xavfsizligi",
        "q": "Kompyuter xonasida texnika xavfsizligi qoidalariga ko'ra nima qilish qat'iyan taqiqlanadi?",
        "opts": [
            "Ho'l qo'l bilan qurilmalarga tegish va kompyuter yonida suyuqlik ichish",
            "Klaviatura tugmalarini bosish",
            "Monitorda matn o'qish",
            "Sichqonchani harakatlantirish"
        ],
        "ans": 0
    },
    {
        "id": 43,
        "topic": "Texnika xavfsizligi",
        "q": "Ko'rish qobiliyatini asrash uchun monitor bilan ko'z orasidagi masofa qancha bo'lishi kerak?",
        "opts": ["10–20 sm", "50–70 sm", "1.5–2 metr", "5 sm"],
        "ans": 1
    },
    {
        "id": 44,
        "topic": "Texnika xavfsizligi",
        "q": "Kompyuterda ishlaganda ko'z va tanani toliqishdan saqlash uchun qanday qoidaga amal qilish kerak?",
        "opts": [
            "Har 40-45 daqiqa ishlashdan so'ng 10-15 daqiqa tanaffus qilish va ko'z mashqlarini bajarish",
            "Kun bo'yi to'xtovsiz ekranga qarab o'tirish",
            "Monitorni ko'zga juda yaqin olib kelish",
            "Qorong'i xonada ekranni eng yorug' holatga qo'yish"
        ],
        "ans": 0
    },
    {
        "id": 45,
        "topic": "Axborot xavfsizligi",
        "q": "Tibbiyot xodimining kompyuteridagi bemorlarning shaxsiy kasallik tarixi qaysi toifaga kiradi?",
        "opts": [
            "Ommaviy reklama axboroti",
            "Shaxsiy va shifokorlik siri bo'lgan maxfiy axborot",
            "Barcha ko'rishi majburiy bo'lgan ochiq axborot",
            "Keraksiz axborot"
        ],
        "ans": 1
    },
    {
        "id": 46,
        "topic": "Axborot xavfsizligi",
        "q": "Ish joyidan vaqtincha ketayotganda kompyuter ekranini begonalardan tezkor qulflash (Lock) tugmalari qaysi?",
        "opts": ["Win + L", "Ctrl + Z", "Alt + F4", "Ctrl + P"],
        "ans": 0
    },
    {
        "id": 47,
        "topic": "Texnika xavfsizligi",
        "q": "Kompyuter simlaridan tutun yoki kuyindi hidi chiqsa, birinchi navbatda nima qilish kerak?",
        "opts": [
            "Darhol qurilmani elektr tarmog'idan uzish va o'qituvchi/mutaxassisga xabar berish",
            "Suv sepib o'chirish",
            "Ishlashni davom ettirish",
            "Monitorni yopib qo'yish"
        ],
        "ans": 0
    },
    {
        "id": 48,
        "topic": "Axborot xavfsizligi",
        "q": "Begona fleshkani kompyuterga ulaganda birinchi bo'lib qanday xavfsizlik chorasi ko'riladi?",
        "opts": [
            "Uni antivirus dasturi yordamida tekshirish",
            "Ichidagi barcha fayllarni darhol ochib ko'rish",
            "Fleshkani formatlash",
            "Kompyuterni o'chirib yoqish"
        ],
        "ans": 0
    },
    {
        "id": 49,
        "topic": "Axborot xavfsizligi",
        "q": "Ikki bosqichli autentifikatsiya (2FA) nima uchun xizmat qiladi?",
        "opts": [
            "Hisob qaydnomasiga kirishda parol bilan birga telefon kodini talab qilib, xavfsizlikni oshirish",
            "Kompyuterni ikki barobar tezroq yoqish",
            "Klaviatura tilini ikki marta o'zgartirish",
            "Internet tezligini oshirish"
        ],
        "ans": 0
    },
    {
        "id": 50,
        "topic": "Axborot xavfsizligi",
        "q": "Bemorlarning elektron ma'lumotlarini ruxsatsiz ommaviy ijtimoiy tarmoqlarga tarqatish qanday oqibatga olib keladi?",
        "opts": [
            "Qonuniy javobgarlikka va shifokorlik sirini buzishga",
            "Bemorning tezroq tuzalishiga",
            "Kompyuter xotirasi ko'payishiga",
            "Hech qanday oqibat bo'lmaydi"
        ],
        "ans": 0
    },
    {
        "id": 51,
        "topic": "Axborot xavfsizligi",
        "q": "Elektron pochtaga noma'lum jo'natuvchidan kelgan shubhali havola (link) ni bosish nima uchun xavfli?",
        "opts": [
            "Virus yuqishi yoki parollar o'g'irlanishi mumkin",
            "Monitor rangi o'zgaradi",
            "Klaviatura harflari o'chib ketadi",
            "Printer qog'ozi tugaydi"
        ],
        "ans": 0
    },
    {
        "id": 52,
        "topic": "Axborot xavfsizligi",
        "q": "Kiberxavfsizlikda 'Ijtimoiy muhandislik' (Social engineering) nima?",
        "opts": [
            "Insonlarni aldash va ishonchiga kirish orqali maxfiy ma'lumotlarni qo'lga kiritish usuli",
            "Kompyuterlarni ta'mirlash muhandisligi",
            "Yangi internet kabelini tortish",
            "Robotlar yasash ilmi"
        ],
        "ans": 0
    },
    {
        "id": 53,
        "topic": "Axborot xavfsizligi",
        "q": "Muhim fayllarning zaxira nusxasi (Backup) qayerda saqlanishi eng xavfsiz hisoblanadi?",
        "opts": [
            "Alohida tashqi diskda yoki ishonchli bulutli xotirada",
            "Faqat ish stolidagi bitta papkada",
            "Kompyuter savatida (Korzina)",
            "Hech qayerda saqlamaslik kerak"
        ],
        "ans": 0
    },
    {
        "id": 54,
        "topic": "Axborot xavfsizligi",
        "q": "Kompyuterga yangi dasturlar o'rnatishda nimalarga e'tibor berish lozim?",
        "opts": [
            "Dastur faqat rasmiy va ishonchli manbadan olingan bo'lishiga",
            "Dastur eng ko'p joy egallashiga",
            "Dastur qimmat bo'lishiga",
            "Dasturda ko'p reklamalar bo'lishiga"
        ],
        "ans": 0
    },
    {
        "id": 55,
        "topic": "Axborot xavfsizligi",
        "q": "Xizmat kompyuteringiz parolini hamkasblaringizga aytishingiz mumkinmi?",
        "opts": [
            "Yo'q, shaxsiy hisob parolini hech kimga oshkor qilish mumkin emas",
            "Ha, xohlagan odamga aytish mumkin",
            "Faqat qog'ozga yozib monitorga yopishtirib qo'yish kerak",
            "Faqat tushlik vaqtida aytish mumkin"
        ],
        "ans": 0
    },

    # =========================================================================
    # 3-BO'LIM: SANOQ SISTEMALARI (ODDIY TUSHUNCHALAR, MASALASIZ) (56–65)
    # =========================================================================
    {
        "id": 56,
        "topic": "Sanoq sistemalari",
        "q": "Sanoq sistemasi nima?",
        "opts": [
            "Sonlarni yozish va ifodalash qoidalari to'plami",
            "Kompyuterning sovutish tizimi",
            "Klaviatura tugmalari soni",
            "Printerda chop etish tezligi"
        ],
        "ans": 0
    },
    {
        "id": 57,
        "topic": "Sanoq sistemalari",
        "q": "Zamonaviy kompyuter texnikasi asosan qaysi sanoq sistemasida ishlaydi?",
        "opts": ["O'nlik", "Ikkilik", "Rim", "Sakkizlik"],
        "ans": 1
    },
    {
        "id": 58,
        "topic": "Sanoq sistemalari",
        "q": "Ikkilik sanoq sistemasining asosi nechaga teng?",
        "opts": ["1 ga", "2 ga", "8 ga", "10 ga"],
        "ans": 1
    },
    {
        "id": 59,
        "topic": "Sanoq sistemalari",
        "q": "Ikkilik sanoq sistemasida qanday raqamlar ishlatiladi?",
        "opts": ["0 va 1", "1 va 2", "0 dan 9 gacha", "Faqat 0"],
        "ans": 0
    },
    {
        "id": 60,
        "topic": "Sanoq sistemalari",
        "q": "O'nlik sanoq sistemasining asosi nechaga teng?",
        "opts": ["2 ga", "8 ga", "10 ga", "16 ga"],
        "ans": 2
    },
    {
        "id": 61,
        "topic": "Sanoq sistemalari",
        "q": "O'nlik sanoq sistemasida nechta raqam ishlatiladi?",
        "opts": ["10 ta (0 dan 9 gacha)", "9 ta (1 dan 9 gacha)", "2 ta (0 va 1)", "Cheksiz"],
        "ans": 0
    },
    {
        "id": 62,
        "topic": "Sanoq sistemalari",
        "q": "Odamlar kundalik hayotida hisob-kitob qilish uchun eng ko'p qaysi sanoq sistemasidan foydalanadilar?",
        "opts": ["Ikkilik", "O'nlik", "O'n oltilik", "Sakkizlik"],
        "ans": 1
    },
    {
        "id": 63,
        "topic": "Sanoq sistemalari",
        "q": "Sakkizlik sanoq sistemasida qaysi raqamlar ishlatiladi?",
        "opts": ["0 dan 7 gacha", "0 dan 8 gacha", "1 dan 8 gacha", "Faqat 0 va 8"],
        "ans": 0
    },
    {
        "id": 64,
        "topic": "Sanoq sistemalari",
        "q": "O'n oltilik sanoq sistemasining asosi nechaga teng?",
        "opts": ["8 ga", "10 ga", "12 ga", "16 ga"],
        "ans": 3
    },
    {
        "id": 65,
        "topic": "Sanoq sistemalari",
        "q": "O'n oltilik sanoq sistemasida 0 dan 9 gacha bo'lgan raqamlardan tashqari qaysi harflar ishlatiladi?",
        "opts": ["A, B, C, D, E, F", "X, Y, Z", "K, L, M, N", "Alpha, Beta"],
        "ans": 0
    },

    # =========================================================================
    # 4-BO'LIM: KLAVIATURA VA SICHQONCHA (66–85)
    # =========================================================================
    {
        "id": 66,
        "topic": "Klaviatura",
        "q": "Klaviatura kompyuterning qanday qurilmasi hisoblanadi?",
        "opts": ["Axborotni kiritish qurilmasi", "Axborotni chiqarish qurilmasi", "Axborotni saqlash qurilmasi", "Sovutish qurilmasi"],
        "ans": 0
    },
    {
        "id": 67,
        "topic": "Klaviatura",
        "q": "Klaviaturaning eng yuqori qatorida joylashgan F1–F12 tugmalari qaysi guruhga kiradi?",
        "opts": ["Funksional tugmalar", "Alfavit-raqamli tugmalar", "Kursor boshqarish tugmalari", "Raqamli blok"],
        "ans": 0
    },
    {
        "id": 68,
        "topic": "Klaviatura",
        "q": "Matn kiritishda yangi qatorga o'tish yoki buyruqni tasdiqlash uchun qaysi tugma bosiladi?",
        "opts": ["Shift", "Enter", "Ctrl", "Alt"],
        "ans": 1
    },
    {
        "id": 69,
        "topic": "Klaviatura",
        "q": "Bitta katta harf yozish yoki klavishning yuqori belgisini chiqarish uchun qaysi tugma bosib turiladi?",
        "opts": ["Shift", "Caps Lock", "Tab", "Spacebar"],
        "ans": 0
    },
    {
        "id": 70,
        "topic": "Klaviatura",
        "q": "Barcha harflarni doimiy ravishda katta qilib yozish rejimini yoqish/o'chirish tugmasi qaysi?",
        "opts": ["Num Lock", "Caps Lock", "Scroll Lock", "Backspace"],
        "ans": 1
    },
    {
        "id": 71,
        "topic": "Klaviatura",
        "q": "Kursordan chapda turgan belgini o'chirish uchun qaysi tugma bosiladi?",
        "opts": ["Delete", "Backspace", "Insert", "Escape"],
        "ans": 1
    },
    {
        "id": 72,
        "topic": "Klaviatura",
        "q": "Kursordan o'ngda turgan belgini yoki belgilangan faylni o'chirish tugmasi qaysi?",
        "opts": ["Delete", "Backspace", "Home", "End"],
        "ans": 0
    },
    {
        "id": 73,
        "topic": "Klaviatura",
        "q": "Matnda so'zlar orasida bo'sh joy qoldirish uchun klaviaturaning qaysi eng uzun tugmasi bosiladi?",
        "opts": ["Probel (Spacebar)", "Tab", "Enter", "Shift"],
        "ans": 0
    },
    {
        "id": 74,
        "topic": "Klaviatura",
        "q": "Bajarilayotgan amalni yoki ochilgan muloqot oynasini bekor qilish (chiqish) tugmasi qaysi?",
        "opts": ["Esc (Escape)", "Enter", "F5", "Home"],
        "ans": 0
    },
    {
        "id": 75,
        "topic": "Klaviatura",
        "q": "Matnda tabulyatsiya (standart kattalikdagi bo'shliq) tashlash yoki keyingi maydonga o'tish tugmasi qaysi?",
        "opts": ["Tab", "Ctrl", "Alt", "Pause"],
        "ans": 0
    },
    {
        "id": 76,
        "topic": "Klaviatura",
        "q": "Klaviaturaning o'ng tomonidagi qo'shimcha raqamlar blokini yoqish/o'chirish tugmasi nima deb ataladi?",
        "opts": ["Caps Lock", "Num Lock", "Scroll Lock", "Insert"],
        "ans": 1
    },
    {
        "id": 77,
        "topic": "Klaviatura",
        "q": "Kursorni matn satrining eng boshiga tezkor o'tkazish uchun qaysi tugma bosiladi?",
        "opts": ["Home", "End", "Page Up", "Page Down"],
        "ans": 0
    },
    {
        "id": 78,
        "topic": "Klaviatura",
        "q": "Kursorni matn satrining eng oxiriga tezkor o'tkazish uchun qaysi tugma bosiladi?",
        "opts": ["End", "Home", "Insert", "Delete"],
        "ans": 0
    },
    {
        "id": 79,
        "topic": "Klaviatura",
        "q": "Hujjatni bir ekran balandligida yuqoriga varoqlash tugmasi qaysi?",
        "opts": ["Page Up", "Page Down", "Home", "Up Arrow"],
        "ans": 0
    },
    {
        "id": 80,
        "topic": "Klaviatura",
        "q": "Hujjatni bir ekran balandligida pastga varoqlash tugmasi qaysi?",
        "opts": ["Page Down", "Page Up", "End", "Down Arrow"],
        "ans": 0
    },
    {
        "id": 81,
        "topic": "Sichqoncha",
        "q": "Sichqonchaning chap tugmasini bir marta bosish qanday vazifani bajaradi?",
        "opts": ["Ob'ektni tanlash (belgilash)", "Dasturni o'chirib yuborish", "Kompyuterni o'chirish", "Matnni chop etish"],
        "ans": 0
    },
    {
        "id": 82,
        "topic": "Sichqoncha",
        "q": "Sichqonchaning chap tugmasini ikki marta tezkor bosish (double click) nima qiladi?",
        "opts": ["Fayl yoki dasturni ochadi", "Faylni butunlay o'chiradi", "Fayl nomini o'zgartiradi", "Kompyuterni qulflaydi"],
        "ans": 0
    },
    {
        "id": 83,
        "topic": "Sichqoncha",
        "q": "Sichqonchaning o'ng tugmasi bosilganda ekranda nima paydo bo'ladi?",
        "opts": ["Kontekst menyu (qo'shimcha amallar ro'yxati)", "O'yinlar ro'yxati", "Internet sahifasi", "Kalkulyator"],
        "ans": 0
    },
    {
        "id": 84,
        "topic": "Sichqoncha",
        "q": "Sichqoncha g'ildirakchasi (Scroll) asosan nima uchun xizmat qiladi?",
        "opts": ["Sahifani yuqoriga va pastga aylantirish (varoqlash)", "Kompyuter tovushini o'chirish", "Kursor rangini o'zgartirish", "Fayllarni qirqish"],
        "ans": 0
    },
    {
        "id": 85,
        "topic": "Sichqoncha",
        "q": "Sichqoncha yordamida ob'ektni bosib turib boshqa joyga ko'chirish amali nima deyiladi?",
        "opts": ["Sudrab o'tkazish (Drag and Drop)", "Nusxalash", "Arxivlash", "Formatlash"],
        "ans": 0
    },

    # =========================================================================
    # 5-BO'LIM: KOMPYUTER VA UNING QURILMALARI (HARDWARE) (86–150)
    # =========================================================================
    {
        "id": 86,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuterning apparat ta'minoti ingliz tilida nima deb ataladi?",
        "opts": ["Software", "Hardware", "Freeware", "Malware"],
        "ans": 1
    },
    {
        "id": 87,
        "topic": "Kompyuter qurilmalari",
        "q": "Tizim bloki (System Unit) nima?",
        "opts": [
            "Kompyuterning asosiy ichki qurilmalari joylashgan korpus",
            "Faqat elektr simlari to'plami",
            "Faqat klaviatura va sichqoncha",
            "Faqat monitor ekrani"
        ],
        "ans": 0
    },
    {
        "id": 88,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuterning 'miyasi' deb qaysi qurilmaga aytiladi?",
        "opts": ["Protsessor (CPU)", "Qattiq disk", "Videokarta", "Quvvat bloki"],
        "ans": 0
    },
    {
        "id": 89,
        "topic": "Kompyuter qurilmalari",
        "q": "Markaziy protsessor (CPU) ning asosiy vazifasi nima?",
        "opts": [
            "Barcha arifmetik-mantiqiy amallarni bajarish va qurilmalarni boshqarish",
            "Matnni qog'ozga bosib chiqarish",
            "Tasvirni ekranda ko'rsatish",
            "Musiqa chalish"
        ],
        "ans": 0
    },
    {
        "id": 90,
        "topic": "Kompyuter qurilmalari",
        "q": "Protsessorning ishlash tezligi (chastotasi) qaysi o'lchov birligida o'lchanadi?",
        "opts": ["Gerts (MGts, GGts)", "Bayt (KB, MB)", "Piksel", "Dyuym"],
        "ans": 0
    },
    {
        "id": 91,
        "topic": "Kompyuter qurilmalari",
        "q": "Protsessor ichida joylashgan eng yuqori tezlikdagi maxsus oraliq xotira nima deyiladi?",
        "opts": ["Kesh xotira (Cache)", "Fleshka", "Qattiq disk", "Optik disk"],
        "ans": 0
    },
    {
        "id": 92,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuterning barcha ichki qismlari ulanadigan eng asosiy katta plata nima deb ataladi?",
        "opts": ["Ona plata (Motherboard)", "Tovush kartasi", "Tarmoq kartasi", "Videokarta"],
        "ans": 0
    },
    {
        "id": 93,
        "topic": "Kompyuter qurilmalari",
        "q": "Ona platadagi protsessor o'rnatiladigan maxsus uyacha nima deb ataladi?",
        "opts": ["Soket (Socket)", "Slot", "Port", "Chipset"],
        "ans": 0
    },
    {
        "id": 94,
        "topic": "Kompyuter qurilmalari",
        "q": "Tezkor xotira (RAM / OZU) ning asosiy vazifasi nima?",
        "opts": [
            "Hozir ishlab turgan dasturlar va ma'lumotlarni vaqtincha saqlash",
            "Kompyuter o'chganda ham ma'lumotlarni umrbod saqlash",
            "Tasvir sifatini oshirish",
            "Qurilmalarni sovitish"
        ],
        "ans": 0
    },
    {
        "id": 95,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuter elektr tarmog'idan uzilganda qaysi xotiradagi ma'lumotlar butunlay o'chib ketadi?",
        "opts": ["Tezkor xotira (RAM)", "Qattiq disk (HDD)", "SSD disk", "Fleshka"],
        "ans": 0
    },
    {
        "id": 96,
        "topic": "Kompyuter qurilmalari",
        "q": "Hozirgi zamonaviy kompyuterlarda tezkor xotira (RAM) hajmi odatda qaysi birlikda o'lchanadi?",
        "opts": ["Gigabayt (GB, masalan 8 GB, 16 GB)", "Kilobayt (KB)", "Gerts (GGts)", "Dyuym"],
        "ans": 0
    },
    {
        "id": 97,
        "topic": "Kompyuter qurilmalari",
        "q": "Doimiy xotira (ROM / PZU) ning xususiyati qanday?",
        "opts": [
            "U faqat o'qish uchun mo'ljallangan va elektr o'chganda ma'lumotlar saqlanib qoladi",
            "U har kuni o'chib ketadi",
            "U faqat o'yinlar uchun ishlatiladi",
            "U kompyuterga ulanmaydi"
        ],
        "ans": 0
    },
    {
        "id": 98,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuter yoqilganda qurilmalarni tekshirib, operatsion tizimni yuklovchi boshlang'ich dasturiy ta'minot nima?",
        "opts": ["BIOS (yoki UEFI)", "Microsoft Word", "Antivirus", "Paint"],
        "ans": 0
    },
    {
        "id": 99,
        "topic": "Kompyuter qurilmalari",
        "q": "Ma'lumotlarni magnit plastinkalarda uzoq vaqt doimiy saqlovchi xotira qurilmasi qaysi?",
        "opts": ["Qattiq magnit disk (HDD)", "Tezkor xotira (RAM)", "Kesh xotira", "Protsessor"],
        "ans": 0
    },
    {
        "id": 100,
        "topic": "Kompyuter qurilmalari",
        "q": "SSD (Solid State Drive) disklarning oddiy HDD disklardan asosiy ustunligi nimada?",
        "opts": [
            "Aylanuvchi mexanik qismlari yo'qligi va o'qish/yozish tezligi ancha yuqoriligi",
            "Kattaroq va og'irroq ekanligi",
            "Faqat magnit bilan ishlashi",
            "Elektr energiyasini ko'p sarflashi"
        ],
        "ans": 0
    },
    {
        "id": 101,
        "topic": "Kompyuter qurilmalari",
        "q": "USB flesh-xotira (fleshka) qanday xotira turiga kiradi?",
        "opts": [
            "Doimiy, ko'chma elektron xotira",
            "Faqat vaqtinchalik xotira",
            "Magnit lentali xotira",
            "Protsessor ichki xotirasi"
        ],
        "ans": 0
    },
    {
        "id": 102,
        "topic": "Kompyuter qurilmalari",
        "q": "Grafik axborotni qayta ishlab, monitorga tasvir chiqarish uchun javobgar qurilma qaysi?",
        "opts": ["Videokarta (GPU)", "Tovush kartasi", "Tarmoq kartasi", "Ona plata"],
        "ans": 0
    },
    {
        "id": 103,
        "topic": "Kompyuter qurilmalari",
        "q": "Videokartaning tasvirlarni saqlash uchun mo'ljallangan o'z shaxsiy xotirasi nima deb ataladi?",
        "opts": ["Video xotira (VRAM)", "Kesh xotira", "BIOS", "ROM"],
        "ans": 0
    },
    {
        "id": 104,
        "topic": "Kompyuter qurilmalari",
        "q": "Rozetkadagi 220V o'zgaruvchan tokni kompyuter qismlariga mos kuchlanishga aylantirib beruvchi qurilma qaysi?",
        "opts": ["Quvvat bloki (Power Supply Unit - PSU)", "Kuler", "Videokarta", "Monitor"],
        "ans": 0
    },
    {
        "id": 105,
        "topic": "Kompyuter qurilmalari",
        "q": "Quvvat blokining quvvati qaysi birlikda o'lchanadi?",
        "opts": ["Vatt (W)", "Volt (V)", "Amper (A)", "Gerts (Hz)"],
        "ans": 0
    },
    {
        "id": 106,
        "topic": "Kompyuter qurilmalari",
        "q": "Protsessorni qizib ketishdan saqlab, uni sovitib turuvchi ventilyatorli qurilma nima deyiladi?",
        "opts": ["Kuler (Cooler)", "Quvvat bloki", "Ona plata", "Videokarta"],
        "ans": 0
    },
    {
        "id": 107,
        "topic": "Kompyuter qurilmalari",
        "q": "Protsessor va kuler radiatori orasiga issiqlik o'tkazuvchanlikni oshirish uchun nima surtiladi?",
        "opts": ["Termopasta", "Oddiy yelim", "Yog'", "Spirt"],
        "ans": 0
    },
    {
        "id": 108,
        "topic": "Kompyuter qurilmalari",
        "q": "Elektr to'satdan o'chganda kompyuterga ma'lum vaqt quvvat berib, fayllarni saqlashga imkon yaratuvchi qurilma nima?",
        "opts": ["Uzluksiz quvvat manbai (UPS)", "Stabilizator", "Kuler", "Fleshka"],
        "ans": 0
    },
    {
        "id": 109,
        "topic": "Kompyuter qurilmalari",
        "q": "Monitor qanday qurilma hisoblanadi?",
        "opts": ["Vizual axborotni chiqarish qurilmasi", "Axborotni kiritish qurilmasi", "Xotira qurilmasi", "Sovitish qurilmasi"],
        "ans": 0
    },
    {
        "id": 110,
        "topic": "Kompyuter qurilmalari",
        "q": "Monitor ekranidagi tasvirni hosil qiluvchi eng kichik yorug' nuqta nima deb ataladi?",
        "opts": ["Piksel (Pixel)", "Bayt", "Dyuym", "Nuqta"],
        "ans": 0
    },
    {
        "id": 111,
        "topic": "Kompyuter qurilmalari",
        "q": "Monitor ekranining o'lchami (diagonali) qaysi o'lchov birligida o'lchanadi?",
        "opts": ["Dyuymda (Inch)", "Santimetrda", "Pikselda", "Litrlarda"],
        "ans": 0
    },
    {
        "id": 112,
        "topic": "Kompyuter qurilmalari",
        "q": "Monitorning ekranda tasvirni chizish aniqligi (masalan, 1920x1080) nima deb ataladi?",
        "opts": ["Ekran aniqligi / ruxsat etish qobiliyati (Resolution)", "Ekran og'irligi", "Chastota", "Yorug'lik burchagi"],
        "ans": 0
    },
    {
        "id": 113,
        "topic": "Kompyuter qurilmalari",
        "q": "Hozirgi zamonaviy ingichka monitorlar asosan qaysi displey texnologiyasiga asoslangan?",
        "opts": ["LCD, LED va OLED", "Elektron nurli trubka (CRT)", "Plazma trubka", "Mexanik disklar"],
        "ans": 0
    },
    {
        "id": 114,
        "topic": "Kompyuter qurilmalari",
        "q": "Printer qanday qurilma hisoblanadi?",
        "opts": ["Matn va rasmlarni qog'ozga bosib chiqarish qurilmasi", "Axborotni kompyuterga kiritish qurilmasi", "Xotira qurilmasi", "Ovoz chiqarish qurilmasi"],
        "ans": 0
    },
    {
        "id": 115,
        "topic": "Kompyuter qurilmalari",
        "q": "Maxsus kukunli bo'yoq (toner) yordamida tez va sifatli chop etadigan printer turi qaysi?",
        "opts": ["Lazerli printer", "Purkovchi printer", "Matritsali printer", "Plotter"],
        "ans": 0
    },
    {
        "id": 116,
        "topic": "Kompyuter qurilmalari",
        "q": "Suyuq siyohni mayda tomchilar holida purkash orqali rangli hujjat va suratlarni chop etuvchi printer turi qaysi?",
        "opts": ["Purkovchi (Struyniy) printer", "Lazerli printer", "Matritsali printer", "Teletayp"],
        "ans": 0
    },
    {
        "id": 117,
        "topic": "Kompyuter qurilmalari",
        "q": "Kassalarda chek chiqarish uchun ignachalar orqali lentaga urib ishlaydigan printer turi qaysi?",
        "opts": ["Matritsali printer", "Lazerli printer", "Purkovchi printer", "3D printer"],
        "ans": 0
    },
    {
        "id": 118,
        "topic": "Kompyuter qurilmalari",
        "q": "Printerning chop etish tezligi ko'pincha qaysi birlikda o'lchanadi?",
        "opts": ["PPM (bir daqiqadagi sahifalar soni)", "MB/sekund", "Gerts", "Dyuym"],
        "ans": 0
    },
    {
        "id": 119,
        "topic": "Kompyuter qurilmalari",
        "q": "Printerning chop etish sifati va aniqligi qaysi o'lchov birligida belgilanadi?",
        "opts": ["DPI (bir dyuymdagi nuqtalar soni)", "KB", "MGts", "Volt"],
        "ans": 0
    },
    {
        "id": 120,
        "topic": "Kompyuter qurilmalari",
        "q": "Printer, skaner va kserokopiyani bitta korpusda birlashtirgan qurilma nima deyiladi?",
        "opts": ["Ko'p funksiyali qurilma (MFU / KFQ)", "Plotter", "Modem", "Strimer"],
        "ans": 0
    },
    {
        "id": 121,
        "topic": "Kompyuter qurilmalari",
        "q": "Qog'ozdagi rasm yoki matnli hujjatni kompyuterga raqamli ko'rinishda o'tkazuvchi qurilma qaysi?",
        "opts": ["Skaner", "Printer", "Monitor", "Plotter"],
        "ans": 0
    },
    {
        "id": 122,
        "topic": "Kompyuter qurilmalari",
        "q": "Katta formatdagi chizmalar, anatomiya plakatlari va sxemalarni qog'ozga chiqarish uchun qaysi qurilma ishlatiladi?",
        "opts": ["Plotter (Grafopostroitel)", "Oddiy skaner", "Veb-kamera", "Mikrofon"],
        "ans": 0
    },
    {
        "id": 123,
        "topic": "Kompyuter qurilmalari",
        "q": "Tovush axborotini kompyuterga kiritish qurilmasi qaysi?",
        "opts": ["Mikrofon", "Karnay (Kolonka)", "Quloqchin", "Videokarta"],
        "ans": 0
    },
    {
        "id": 124,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuterdagi tovushni eshitish uchun qaysi chiqarish qurilmalari ishlatiladi?",
        "opts": ["Kolonkalar (dinamiklar) va quloqchinlar (naushnik)", "Mikrofon", "Skaner", "Klaviatura"],
        "ans": 0
    },
    {
        "id": 125,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuter ekranidagi tasvirni katta oq doska yoki devorga kattalashtirib ko'rsatish qurilmasi nima?",
        "opts": ["Multimedia proyektori", "Skaner", "Printer", "Videokarta"],
        "ans": 0
    },
    {
        "id": 126,
        "topic": "Kompyuter qurilmalari",
        "q": "Internet orqali videoqo'ng'iroq va konferensiyalarda tasvirni uzatuvchi qurilma nima?",
        "opts": ["Veb-kamera", "Skaner", "Monitor", "Plotter"],
        "ans": 0
    },
    {
        "id": 127,
        "topic": "Kompyuter qurilmalari",
        "q": "Noutbuklarda sichqoncha o'rnini bosuvchi sensorli panel nima deb ataladi?",
        "opts": ["Tachpad (Touchpad)", "Kuler", "Drayver", "Slot"],
        "ans": 0
    },
    {
        "id": 128,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuterni kabel orqali lokal tarmoqqa va internetga ulaydigan qurilma nima?",
        "opts": ["Tarmoq kartasi (Network card)", "Tovush kartasi", "Videokarta", "Quvvat bloki"],
        "ans": 0
    },
    {
        "id": 129,
        "topic": "Kompyuter qurilmalari",
        "q": "Lokal tarmoq kabeli kompyuterning qaysi portiga ulanadi?",
        "opts": ["RJ-45 (LAN port)", "USB", "HDMI", "VGA"],
        "ans": 0
    },
    {
        "id": 130,
        "topic": "Kompyuter qurilmalari",
        "q": "Fleshka, sichqoncha, klaviatura va printerni ulashda eng keng qo'llaniladigan universal port qaysi?",
        "opts": ["USB port", "LPT port", "COM port", "PS/2 port"],
        "ans": 0
    },
    {
        "id": 131,
        "topic": "Kompyuter qurilmalari",
        "q": "Qaysi zamonaviy USB turi ikki tomonlama simmetrik ulanishga va yuqori tezlikka ega?",
        "opts": ["USB Type-C", "USB 1.0", "Mini-USB", "Micro-USB"],
        "ans": 0
    },
    {
        "id": 132,
        "topic": "Kompyuter qurilmalari",
        "q": "Monitorni kompyuterga ulab, ham yuqori sifatli tasvir, ham ovoz uzatuvchi zamonaviy port qaysi?",
        "opts": ["HDMI", "VGA", "PS/2", "COM"],
        "ans": 0
    },
    {
        "id": 133,
        "topic": "Kompyuter qurilmalari",
        "q": "Monitorni kompyuterga ulash uchun mo'ljallangan ko'k rangli eski analog port nima deyiladi?",
        "opts": ["VGA", "HDMI", "USB", "LAN"],
        "ans": 0
    },
    {
        "id": 134,
        "topic": "Kompyuter qurilmalari",
        "q": "Quloqchin va mikrofon ulanadigan standart dumaloq 3.5 mm port nima deb ataladi?",
        "opts": ["Audio Jack (Mini-Jack)", "USB", "HDMI", "Soket"],
        "ans": 0
    },
    {
        "id": 135,
        "topic": "Kompyuter qurilmalari",
        "q": "Quyidagi qatorda faqat axborotni kiritish qurilmalari ko'rsatilgan javobni toping:",
        "opts": [
            "Klaviatura, sichqoncha, skaner, mikrofon",
            "Monitor, printer, kolonka, proyektor",
            "Qattiq disk, RAM, kuler, ona plata",
            "Videokarta, protsessor, naushnik"
        ],
        "ans": 0
    },
    {
        "id": 136,
        "topic": "Kompyuter qurilmalari",
        "q": "Quyidagi qatorda faqat axborotni chiqarish qurilmalari ko'rsatilgan javobni toping:",
        "opts": [
            "Monitor, printer, kolonka, naushnik",
            "Klaviatura, skaner, sichqoncha",
            "Mikrofon, veb-kamera, tachpad",
            "Protsessor, RAM, ona plata"
        ],
        "ans": 0
    },
    {
        "id": 137,
        "topic": "Kompyuter qurilmalari",
        "q": "Ham axborotni kiritish, ham chiqarish funksiyasini bir vaqtda bajaradigan qurilma qaysi?",
        "opts": ["Sensorli ekran (Touchscreen)", "Oddiy sichqoncha", "Oddiy monitor", "Klaviatura"],
        "ans": 0
    },
    {
        "id": 138,
        "topic": "Kompyuter qurilmalari",
        "q": "Shaxsiy kompyuterning ishlashi uchun zarur bo'lgan minimal asosiy tarkibiga nimalar kiradi?",
        "opts": [
            "Tizim bloki, monitor, klaviatura, sichqoncha",
            "Printer, skaner, plotter, kamera",
            "Faqat monitor va fleshka",
            "Faqat kuler va tovush kartasi"
        ],
        "ans": 0
    },
    {
        "id": 139,
        "topic": "Kompyuter qurilmalari",
        "q": "Tashqi qattiq disklar (External HDD) kompyuterga odatda qaysi port orqali ulanadi?",
        "opts": ["USB port orqali", "VGA port orqali", "Audio port orqali", "PS/2 orqali"],
        "ans": 0
    },
    {
        "id": 140,
        "topic": "Kompyuter qurilmalari",
        "q": "Optik disklarni (CD, DVD) o'qish va yozish uchun kompyuterga qanday qurilma o'rnatiladi?",
        "opts": ["Optik disk yurituvchi (CD/DVD drive)", "HDD", "SSD", "Modem"],
        "ans": 0
    },
    {
        "id": 141,
        "topic": "Kompyuter qurilmalari",
        "q": "Standart oddiy CD diskning axborot sig'imi taxminan qancha bo'ladi?",
        "opts": ["700 MB", "4.7 GB", "100 KB", "1 TB"],
        "ans": 0
    },
    {
        "id": 142,
        "topic": "Kompyuter qurilmalari",
        "q": "Standart bir qatlamli DVD diskning axborot sig'imi taxminan qancha bo'ladi?",
        "opts": ["4.7 GB", "700 MB", "128 MB", "1 TB"],
        "ans": 0
    },
    {
        "id": 143,
        "topic": "Kompyuter qurilmalari",
        "q": "Qurilmalarni (sichqoncha, quloqchin) simsiz tarzda yaqin masofada (10 metrgacha) ulash texnologiyasi nima?",
        "opts": ["Bluetooth", "Kabel", "Infraqizil", "Sputnik"],
        "ans": 0
    },
    {
        "id": 144,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuterning simsiz internet va tarmoqqa ulanishini ta'minlovchi adapter nima?",
        "opts": ["Wi-Fi adapter", "Tovush adapteri", "Kuler", "Optik privod"],
        "ans": 0
    },
    {
        "id": 145,
        "topic": "Kompyuter qurilmalari",
        "q": "Tovush kartasi (Sound card) ning vazifasi nima?",
        "opts": [
            "Tovush signallarini raqamli axborotga va aksincha tovushga aylantirish",
            "Tasvirlarni qog'ozga chiqarish",
            "Kompyuterni elektr bilan ta'minlash",
            "Fayllarni arxivlash"
        ],
        "ans": 0
    },
    {
        "id": 146,
        "topic": "Kompyuter qurilmalari",
        "q": "Dori qutilari yoki bemor bilaguzuklaridagi shtrix-kod va QR-kodlarni kompyuterga o'qib kirituvchi qurilma nima?",
        "opts": ["Shtrix-kod skaneri", "Oddiy printer", "Veb-kamera", "Kolonka"],
        "ans": 0
    },
    {
        "id": 147,
        "topic": "Kompyuter qurilmalari",
        "q": "Kompyuter o'chirilganda ham ona platadagi vaqt va BIOS sozlamalarini saqlab turuvchi qism nima?",
        "opts": ["CR2032 batareykasi", "Kuler", "Protsessor", "Quvvat bloki"],
        "ans": 0
    },
    {
        "id": 148,
        "topic": "Kompyuter qurilmalari",
        "q": "Tizim bloki orqasidagi turli xil ulagichlar joylashgan panel nima deb ataladi?",
        "opts": ["Kiritish-chiqarish paneli (I/O panel)", "Kuler paneli", "Xotira paneli", "Drayver"],
        "ans": 0
    },
    {
        "id": 149,
        "topic": "Kompyuter qurilmalari",
        "q": "USB fleshkani kompyuterdan sug'urib olishdan oldin nima uchun 'Xavfsiz ajratish' (Безопасное извлечение) buyrug'i bosiladi?",
        "opts": [
            "Fayllar to'liq yozib bo'linganligiga ishonch hosil qilish va ularning buzilishini oldini olish uchun",
            "Fleshkani zaryadlash uchun",
            "Kompyuter o'chib qolmasligi uchun",
            "Fleshka hajmini oshirish uchun"
        ],
        "ans": 0
    },
    {
        "id": 150,
        "topic": "Kompyuter qurilmalari",
        "q": "Noutbuklarning oddiy stol kompyuterlaridan (PC) asosiy qulayligi va farqi nimada?",
        "opts": [
            "Ixchamligi, yengilligi va akkumulyator orqali zaryad bilan mustaqil ishlay olishida",
            "Faqat internetda ishlashida",
            "Klaviatura ulanmasligida",
            "Faqat o'yinlar uchun mosligida"
        ],
        "ans": 0
    },

    # =========================================================================
    # 6-BO'LIM: WINDOWS OPERATSION TIZIMI (151–165)
    # =========================================================================
    {
        "id": 151,
        "topic": "Windows OT",
        "q": "Operatsion tizim (OT) ning asosiy vazifasi nima?",
        "opts": [
            "Kompyuter qurilmalarini boshqarish va inson bilan kompyuter muloqotini ta'minlash",
            "Faqat matn terish",
            "Faqat internet saytlarini ko'rish",
            "Faqat musiqalarni ochish"
        ],
        "ans": 0
    },
    {
        "id": 152,
        "topic": "Windows OT",
        "q": "Kompyuter yoqilganda ekranda ochiladigan asosiy bosh ish maydoni nima deb ataladi?",
        "opts": ["Ish stoli (Desktop)", "Vazifalar paneli", "Savat", "Mundarija"],
        "ans": 0
    },
    {
        "id": 153,
        "topic": "Windows OT",
        "q": "Ekran pastki qismida joylashgan, Pusk tugmasi va ochiq dasturlar belgisi turadigan yo'lakcha nima deyiladi?",
        "opts": ["Vazifalar paneli (Taskbar)", "Holat paneli", "Sarlavha satri", "Menyu satri"],
        "ans": 0
    },
    {
        "id": 154,
        "topic": "Windows OT",
        "q": "Windows-da barcha dasturlar, sozlamalar va kompyuterni o'chirish menyusini ochuvchi asosiy tugma qaysi?",
        "opts": ["Boshlash (Pusk / Start)", "Yordam", "Shift", "Enter"],
        "ans": 0
    },
    {
        "id": 155,
        "topic": "Windows OT",
        "q": "Ish stolida biron fayl yoki dasturga tez kirish uchun yaratilgan ko'rsatkich belgi nima deb ataladi?",
        "opts": ["Yorliq (Shortcut / Yarlik)", "Arxiv", "Drayver", "Piksel"],
        "ans": 0
    },
    {
        "id": 156,
        "topic": "Windows OT",
        "q": "Yorliq (shortcut) belgisining oddiy fayldan asosiy vizual farqi nimada?",
        "opts": [
            "Uning chap pastki burchagida kichik o'q (strelka) belgisi bo'ladi",
            "U qizil rangda bo'ladi",
            "Uning kengaytmasi bo'lmaydi",
            "Uni o'chirib bo'lmaydi"
        ],
        "ans": 0
    },
    {
        "id": 157,
        "topic": "Windows OT",
        "q": "Ochiq dastur oynasini butun ekranga yoyish (kattalashtirish) tugmasi qaysi?",
        "opts": ["Kattalashtirish (Maximize / To'rtburchak belgi)", "Kichraytirish (Chiziqcha)", "Yopish (Qizil X)", "Aylantirish"],
        "ans": 0
    },
    {
        "id": 158,
        "topic": "Windows OT",
        "q": "Ochiq dastur oynasini ekrandan yashirib, Vazifalar paneliga buklab qo'yish tugmasi qaysi?",
        "opts": ["Kichraytirish (Minimize / Chiziqcha belgi)", "Yopish (X)", "Kattalashtirish", "Yangilash"],
        "ans": 0
    },
    {
        "id": 159,
        "topic": "Windows OT",
        "q": "Dastur oynasini butunlay yopish tugmasi qaysi?",
        "opts": ["Yopish (Close / Qizil X belgisi)", "Chiziqcha belgi", "To'rtburchak belgi", "Strelka"],
        "ans": 0
    },
    {
        "id": 160,
        "topic": "Windows OT",
        "q": "Ochiq dastur oynasini klaviatura orqali tezkor yopish tugmalar birikmasi qaysi?",
        "opts": ["Alt + F4", "Ctrl + C", "Ctrl + V", "Shift + Enter"],
        "ans": 0
    },
    {
        "id": 161,
        "topic": "Windows OT",
        "q": "Barcha ochiq oynalarni tezda buklab, to'g'ridan-to'g'ri Ish stolini (Desktop) ko'rsatish birikmasi qaysi?",
        "opts": ["Win + D", "Ctrl + P", "Alt + Shift", "Ctrl + S"],
        "ans": 0
    },
    {
        "id": 162,
        "topic": "Windows OT",
        "q": "Ochiq dastur oynalari o'rtasida klaviatura orqali tezkor almashish uchun qaysi tugmalar bosiladi?",
        "opts": ["Alt + Tab", "Ctrl + Z", "Win + L", "Shift + F5"],
        "ans": 0
    },
    {
        "id": 163,
        "topic": "Windows OT",
        "q": "Windows tizimida dastur yoki fayllarni tezkor qidirish oynasini ochish tugmasi qaysi?",
        "opts": ["Win + S", "Ctrl + N", "Alt + P", "Shift + D"],
        "ans": 0
    },
    {
        "id": 164,
        "topic": "Windows OT",
        "q": "Butun ekran tasvirini (skrinshot) xotiraga nusxalab olish tugmasi qaysi?",
        "opts": ["Print Screen (PrtScn)", "Scroll Lock", "Pause Break", "F1"],
        "ans": 0
    },
    {
        "id": 165,
        "topic": "Windows OT",
        "q": "Windows-da kompyuter sozlamalari, qurilmalarni o'rnatish va dasturlarni o'chirish qayerdan bajariladi?",
        "opts": ["Boshqaruv paneli (Control Panel / Sozlamalar)", "Savat (Korzina)", "Bloknot", "Paint"],
        "ans": 0
    },

    # =========================================================================
    # 7-BO'LIM: FAYLLAR, PAPKALAR VA ARXIVLASH (166–185)
    # =========================================================================
    {
        "id": 166,
        "topic": "Fayllar va arxivlash",
        "q": "Fayl nima?",
        "opts": [
            "Xotirada ma'lum bir nomga ega bo'lgan va yaxlit saqlanadigan ma'lumotlar to'plami",
            "Faqat kompyuter ekrani",
            "Faqat klaviatura tugmasi",
            "Faqat printer qog'ozi"
        ],
        "ans": 0
    },
    {
        "id": 167,
        "topic": "Fayllar va arxivlash",
        "q": "Fayl nomi qanday 2 ta qismdan iborat bo'ladi?",
        "opts": [
            "Faylning asosiy nomi va kengaytmasi",
            "Harf va raqam",
            "Protsessor va monitor",
            "Parol va login"
        ],
        "ans": 0
    },
    {
        "id": 168,
        "topic": "Fayllar va arxivlash",
        "q": "Fayl nomi bilan uning kengaytmasi o'rtasida qanday belgi qo'yiladi?",
        "opts": ["Nuqta (.)", "Vergul (,)", "Ikki nuqta (:)", "Tiziqcha (-)"],
        "ans": 0
    },
    {
        "id": 169,
        "topic": "Fayllar va arxivlash",
        "q": "Fayl kengaytmasi (.docx, .xlsx, .jpg va h.k.) nimani bildiradi?",
        "opts": [
            "Faylning qaysi turga mansubligini va uni qaysi dastur ochishini",
            "Fayl narxini",
            "Kompyuter markasini",
            "Foydalanuvchining yoshini"
        ],
        "ans": 0
    },
    {
        "id": 170,
        "topic": "Fayllar va arxivlash",
        "q": "Fayllarni tartibli joylashtirish va guruhlash uchun xizmat qiluvchi katalog nima deyiladi?",
        "opts": ["Papka (Folder)", "Yorliq", "Kengaytma", "Kesh"],
        "ans": 0
    },
    {
        "id": 171,
        "topic": "Fayllar va arxivlash",
        "q": "Windows-da yangi papka yaratishning tezkor klaviatura tugmalari qaysi?",
        "opts": ["Ctrl + Shift + N", "Ctrl + N", "Alt + F4", "Ctrl + P"],
        "ans": 0
    },
    {
        "id": 172,
        "topic": "Fayllar va arxivlash",
        "q": "Belgilangan fayl yoki papkaning nomini o'zgartirish (Rename) tugmasi qaysi?",
        "opts": ["F2", "F1", "F5", "Esc"],
        "ans": 0
    },
    {
        "id": 173,
        "topic": "Fayllar va arxivlash",
        "q": "Fayldan nusxa olish (Copy) uchun qaysi klavishlar birikmasi bosiladi?",
        "opts": ["Ctrl + C", "Ctrl + V", "Ctrl + X", "Ctrl + Z"],
        "ans": 0
    },
    {
        "id": 174,
        "topic": "Fayllar va arxivlash",
        "q": "Faylni boshqa joyga ko'chirish uchun kesib olish (Cut) birikmasi qaysi?",
        "opts": ["Ctrl + X", "Ctrl + C", "Ctrl + V", "Ctrl + A"],
        "ans": 0
    },
    {
        "id": 175,
        "topic": "Fayllar va arxivlash",
        "q": "Nusxalangan yoki kesilgan faylni yangi joyga qo'yish (Paste / Joylashtirish) tugmalari qaysi?",
        "opts": ["Ctrl + V", "Ctrl + C", "Ctrl + X", "Ctrl + S"],
        "ans": 0
    },
    {
        "id": 176,
        "topic": "Fayllar va arxivlash",
        "q": "Oxirgi bajarilgan xato amalni bekor qilish (orqaga qaytarish) tezkor tugmasi qaysi?",
        "opts": ["Ctrl + Z", "Ctrl + Y", "Ctrl + D", "Alt + Z"],
        "ans": 0
    },
    {
        "id": 177,
        "topic": "Fayllar va arxivlash",
        "q": "Faylni belgilab Delete tugmasi bosilsa, u qayerga tushadi?",
        "opts": ["Savatga (Korzina / Recycle Bin)", "Fleshkaga", "Doimiy yo'qoladi", "Internetga"],
        "ans": 0
    },
    {
        "id": 178,
        "topic": "Fayllar va arxivlash",
        "q": "Faylni Savatga tushirmasdan, butunlay o'chirib yuborish uchun qaysi birikma bosiladi?",
        "opts": ["Shift + Delete", "Ctrl + Delete", "Alt + Delete", "Win + Delete"],
        "ans": 0
    },
    {
        "id": 179,
        "topic": "Fayllar va arxivlash",
        "q": "Savatdagi faylni avvalgi o'chirilgan joyiga qaytarish amali nima deb ataladi?",
        "opts": ["Tiklash (Restore / Vosstanovit)", "Nusxalash", "Ko'chirish", "Formatlash"],
        "ans": 0
    },
    {
        "id": 180,
        "topic": "Fayllar va arxivlash",
        "q": "Arxivlash nima?",
        "opts": [
            "Fayl va papkalarni bitta faylga jamlab, ularning hajmini siqish",
            "Fayllarni chop etish",
            "Fayllarni internetda qidirish",
            "Fayl nomini o'chirish"
        ],
        "ans": 0
    },
    {
        "id": 181,
        "topic": "Fayllar va arxivlash",
        "q": "Fayllarni arxivlashdan asosiy maqsad nima?",
        "opts": [
            "Xotirada joy tejash va internet orqali uzatishni qulaylashtirish",
            "Fayl matnini kattalashtirish",
            "Faylni rasmga aylantirish",
            "Kompyuterni o'chirish"
        ],
        "ans": 0
    },
    {
        "id": 182,
        "topic": "Fayllar va arxivlash",
        "q": "Quyidagilardan qaysi biri arxivator dasturlar hisoblanadi?",
        "opts": ["WinRAR va 7-Zip", "Microsoft Word va Excel", "Photoshop va Paint", "VLC va Media Player"],
        "ans": 0
    },
    {
        "id": 183,
        "topic": "Fayllar va arxivlash",
        "q": "Quyidagilardan qaysi biri arxiv fayl kengaytmasi EMAS?",
        "opts": [".docx", ".zip", ".rar", ".7z"],
        "ans": 0
    },
    {
        "id": 184,
        "topic": "Fayllar va arxivlash",
        "q": "Arxiv ichidagi fayllarni tashqariga, asl holida ochib chiqarish amali nima deyiladi?",
        "opts": ["Arxivdan chiqarish (Extract / Izvech)", "Siqish", "Tiklash", "O'chirish"],
        "ans": 0
    },
    {
        "id": 185,
        "topic": "Fayllar va arxivlash",
        "q": "Arxivlangan fayllarga begona kishilar kira olmasligi uchun nima qilish mumkin?",
        "opts": ["Maxsus himoya paroli o'rnatish", "Faylni qizil rangga bo'yash", "Fayl nomini o'chirish", "Fleshkani yashirish"],
        "ans": 0
    },

    # =========================================================================
    # 8-BO'LIM: MS OFFICE VA WORD (1-DARS: MATN TERISH VA FORMATLASH) (186–200)
    # =========================================================================
    {
        "id": 186,
        "topic": "MS Word 1-dars",
        "q": "Microsoft Word dasturi qanday dastur hisoblanadi?",
        "opts": [
            "Matnli hujjatlar yaratish va tahrirlash uchun matn muharriri",
            "Jadvallar bilan hisob-kitob qilish dasturi",
            "Komppyuterni virusdan tozalash dasturi",
            "Internet brauzeri"
        ],
        "ans": 0
    },
    {
        "id": 187,
        "topic": "MS Word 1-dars",
        "q": "Zamonaviy Microsoft Word hujjatlarining standart fayl kengaytmasi qanday bo'ladi?",
        "opts": [".docx", ".xlsx", ".pptx", ".txt"],
        "ans": 0
    },
    {
        "id": 188,
        "topic": "MS Word 1-dars",
        "q": "Word dasturida yangi bo'sh hujjat ochilganda unga avtomatik qanday nom beriladi?",
        "opts": ["Hujjat 1 (Document 1)", "Matn 1", "Yangi fayl", "Word fayli"],
        "ans": 0
    },
    {
        "id": 189,
        "topic": "MS Word 1-dars",
        "q": "Word dasturi oynasining yuqori qismidagi buyruqlar va tablar joylashgan keng panel nima deyiladi?",
        "opts": ["Lenta (Ribbon)", "Holat satri", "Sarlavha", "Vazifalar paneli"],
        "ans": 0
    },
    {
        "id": 190,
        "topic": "MS Word 1-dars",
        "q": "Word-da rasmiy hujjatlar va kasallik tarixlarini chop etish uchun standart qog'oz o'lchami qaysi?",
        "opts": ["A4 (210 x 297 mm)", "A3", "A5", "Letter"],
        "ans": 0
    },
    {
        "id": 191,
        "topic": "MS Word 1-dars",
        "q": "Word-da varaq yo'nalishi (Orientatsiya) qanday 2 ta turga bo'linadi?",
        "opts": [
            "Kitobcha (Portret) va Albomcha (Landshaft)",
            "Katta va kichik",
            "Oq va qora",
            "Qalin va yupqa"
        ],
        "ans": 0
    },
    {
        "id": 192,
        "topic": "MS Word 1-dars",
        "q": "Varaq chetlaridan matngacha bo'lgan bo'sh masofalar nima deb ataladi?",
        "opts": ["Hoshiyalar / Maydonlar (Margins)", "Abzats", "Interval", "Shablon"],
        "ans": 0
    },
    {
        "id": 193,
        "topic": "MS Word 1-dars",
        "q": "Rasmiy hujjatlar va tibbiy epikrizlarda eng ko'p ishlatiladigan standart shrift turi qaysi?",
        "opts": ["Times New Roman", "Comic Sans", "Impact", "Chiller"],
        "ans": 0
    },
    {
        "id": 194,
        "topic": "MS Word 1-dars",
        "q": "Rasmiy hujjatlarda asosiy matn uchun shrift o'lchami (kegl) odatda necha pt qilib olinadi?",
        "opts": ["14 pt (yoki 12 pt)", "24 pt", "8 pt", "36 pt"],
        "ans": 0
    },
    {
        "id": 195,
        "topic": "MS Word 1-dars",
        "q": "Word-da tanlangan matnni qalin (жирный / bold) ko'rinishga keltirish tezkor tugmasi qaysi?",
        "opts": ["Ctrl + B", "Ctrl + I", "Ctrl + U", "Ctrl + K"],
        "ans": 0
    },
    {
        "id": 196,
        "topic": "MS Word 1-dars",
        "q": "Word-da matnni qiya (kursiv / italic) qilish uchun qaysi klavishlar birikmasi bosiladi?",
        "opts": ["Ctrl + I", "Ctrl + B", "Ctrl + U", "Ctrl + L"],
        "ans": 0
    },
    {
        "id": 197,
        "topic": "MS Word 1-dars",
        "q": "Word-da matn ostiga chizish (подчеркнутый / underline) tezkor tugmasi qaysi?",
        "opts": ["Ctrl + U", "Ctrl + B", "Ctrl + I", "Ctrl + E"],
        "ans": 0
    },
    {
        "id": 198,
        "topic": "MS Word 1-dars",
        "q": "Hujjatdagi barcha matn va ob'ektlarni birvarakayiga to'liq belgilash (Select All) birikmasi qaysi?",
        "opts": ["Ctrl + A", "Ctrl + S", "Ctrl + P", "Ctrl + F"],
        "ans": 0
    },
    {
        "id": 199,
        "topic": "MS Word 1-dars",
        "q": "Yozilgan hujjatni xotiraga tezkor saqlash (Save) uchun qaysi tugmalar bosiladi?",
        "opts": ["Ctrl + S", "Ctrl + O", "Ctrl + N", "Ctrl + W"],
        "ans": 0
    },
    {
        "id": 200,
        "topic": "MS Word 1-dars",
        "q": "Hujjatni printerda chop etish (Print) muloqot oynasini ochish tezkor tugmasi qaysi?",
        "opts": ["Ctrl + P", "Ctrl + S", "Ctrl + Z", "Ctrl + C"],
        "ans": 0
    }
]

print(f"Jami tayyorlangan savollar soni: {len(questions)}")

# Mavzular statistikasi
from collections import Counter
topic_counts = Counter(q["topic"] for q in questions)
for topic, count in topic_counts.items():
    print(f" - {topic}: {count} ta")

base_dir = r"c:\Users\user\Desktop\TAT darslar\TAT darslar"

import random
rnd = random.Random(42)

for item in questions:
    correct_text = item["opts"][item["ans"]]
    opts = list(item["opts"])
    rnd.shuffle(opts)
    item["opts"] = opts
    item["ans"] = opts.index(correct_text)

# 1. JSON fayl
json_path = os.path.join(base_dir, "testlar_banki_200.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
print(f"JSON fayl yaratildi: {json_path}")

# 2. Chop etish va o'qish uchun qulay to'liq test hujjati (.txt)
txt_path = os.path.join(base_dir, "testlar_banki_200.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("   SHAHRISABZ TIBBIYOT TEXNIKUMI\n")
    f.write("   FAN: TIBBIYOTDA AXBOROT TEXNOLOGIYALARI\n")
    f.write("   TEST SAVOLLARI BANKI (200 TA SAVOL)\n")
    f.write("   QAMROV: 1-mavzudan MS Word 1-darsigacha (Hardware, Xavfsizlik, O'lchovlar)\n")
    f.write("=" * 80 + "\n\n")

    letters = ["A", "B", "C", "D"]
    for item in questions:
        f.write(f"{item['id']}. {item['q']}\n")
        for idx, opt in enumerate(item["opts"]):
            f.write(f"   {letters[idx]}) {opt}\n")
        f.write(f"   >>> To'g'ri javob: {letters[item['ans']]}\n\n")

    f.write("\n" + "=" * 80 + "\n")
    f.write("   TO'LIQ JAVOBLAR KALITI (ANSWER KEY 1-200)\n")
    f.write("=" * 80 + "\n")
    for i in range(0, len(questions), 10):
        chunk = questions[i:i+10]
        line = " | ".join(f"{q['id']}-{letters[q['ans']]}" for q in chunk)
        f.write(line + "\n")

print(f"To'liq matnli fayl yaratildi: {txt_path}")

# 3. MyTestX dasturiga to'g'ridan-to'g'ri import qilinadigan fayl (.txt)
# MyTestX import formati:
# 1. Savol matni
# +To'g'ri javob
# -Noto'g'ri javob
mytestx_path = os.path.join(base_dir, "testlar_banki_200_mytestx.txt")
with open(mytestx_path, "w", encoding="utf-8") as f:
    for item in questions:
        f.write(f"{item['id']}. {item['q']}\n")
        for idx, opt in enumerate(item["opts"]):
            prefix = "+" if idx == item["ans"] else "-"
            f.write(f"{prefix}{opt}\n")
        f.write("\n")

print(f"MyTestX fayl yaratildi: {mytestx_path}")
