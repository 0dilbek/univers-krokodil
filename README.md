# Univers Krokodil Bot

Telegram guruhlarida krokodil so'z topish o'yinini yuritadigan aiogram + Tortoise bot.

## Ishga Tushirish

1. Virtual muhitni tayyorlang va dependencylarni o'rnating:

```bash
pip install -r requirements.txt
```

2. Bot token va DB URL kiriting:

```bash
export BOT_TOKEN="123:ABC"
export DATABASE_URL="sqlite://db.sqlite3"
export BOT_ADMIN_IDS="123456789"
```

3. Botni ishga tushiring:

```bash
python bot.py
```

4. Boshlang'ich so'zlarni import qiling:

```text
/import_words
```

## BotFather Va Guruh Talablari

Bot guruhdagi oddiy javoblarni o'qishi kerak. BotFather orqali privacy mode o'chirilishi tavsiya qilinadi. Guruhda botni admin qilish ham message eventlar barqarorroq kelishiga yordam beradi.

Bot ishlayotgan guruhlar `CrocodileChat` modelida saqlanadi: guruh nomi, turi, username, a'zolar soni va taklif havolasi. Bu ma'lumotlar `/play` bosilganda yoziladi va background task orqali har kuni yangilanadi. Taklif havolasini olish uchun botda yetarli admin huquqi bo'lishi kerak; aks holda link bo'sh qolishi mumkin.

## Flow

Guruh admini `/play` yozganda bot o'yin yaratadi va `👋 Boshlovchi bo'lishni xohlayman!` tugmasini chiqaradi. Boshlovchi tugmani bosgach, random so'z tanlanadi. So'z guruhga yozilmaydi; `👀 So'zni ko'rish` tugmasi orqali faqat tushuntiruvchiga callback alertda ko'rsatiladi.

Guruhdagi oddiy matnlar javob sifatida tekshiriladi. Birinchi to'g'ri topgan foydalanuvchi `+1` ball oladi va 15 soniya davomida keyingi boshlovchi bo'lishda ustuvor huquqqa ega bo'ladi. 15 soniyadan keyin istalgan foydalanuvchi navbatni olishi mumkin.

O'yin faqat guruh admini yuborgan `/stop` komandasi bilan tugatiladi. Tugaganda shu o'yin ichidagi hisob chiqariladi.

## Commandlar

- `/start`, `/help` - qisqa ma'lumot.
- `/play` - guruhda o'yin boshlash, faqat guruh adminlari uchun.
- `/stop` - active o'yinni tugatish, faqat guruh adminlari uchun.
- `/profile` - krokodil statistikasi.
- `/top` - guruhda shu guruh TOP reytingi, bot bilan privat chatda global TOP reyting, faqat bot admini uchun.
- `/reyting` - guruhdagi active o'yin hisobi yoki guruh reytingi, faqat guruh adminlari uchun.
- `/addword <so'z>` - so'z qo'shish.
- `/delword <so'z yoki id>` - so'zni inactive qilish.
- `/words_count` - active so'zlar soni.
- `/import_words` - `data/words_uz.txt` faylidan so'z import qilish.

## Eslatma

`@Crocodile_Game_Bot` flowini real Telegram test guruhida ko'rish bu muhitda bajarilmadi. Matn va tugmalar `task.md`da yozilgan kuzatilgan flowga moslab tuzildi.
# univers-krokodil
