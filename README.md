Library Desktop Program

Dastur logikasi: Python
GUI(grafik interface): Tkinter
Ma'lumotlar bazasi: SQLite

Agar faylga export qilishni ham istasak moboda hisobot topshirishga kerak bo'lib qolsa quyidagilardan ham foydalanamiz
    Faylga export: pandas, openpyxl
    Hisobotlar PDF formatida: FPDF, ReportLab


Pandas hamda Openpyxl ni qanday o'rnatishni ko'rib chiqamiz.
Kali linux foydalanuvchilari uchun tizimda Python kutubxonalarini global miqyosda o‘rnatish xavfsizlik nuqtai nazaridan cheklanganligi uchun Virtual Environment (virtual muhit yaratgan holda kutubxonalarni o'rnatib olamiz.
Bu usul bizga nima beradi ya'ni bunda biz kutubxonani Linux tizimiga emas balki faqat shu dastur uchun ishlaydigan qiladi degani. Endi buni qanday o'rnatishni ko'rib chiqamiz.
    1. python3 -m venv venv      //////// (Bu buyruqdan so‘ng chap tomondagi fayllar ro‘yxatida venv degan yangi papka paydo bo‘ladi).
    2. source venv/bin/activate     ////////// (Buni bajarganingizdan so‘ng terminalda satr boshi (venv) yozuvi bilan boshlanadi. Bu — virtual muhit ishlayotganini bildiradi).
    3. pip install pandas openpyxl fpdf  /////// (Kutubxonalarni o'rnatamiz.)


