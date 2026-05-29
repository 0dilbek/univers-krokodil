# Univers Krokodil Bot Task

## Maqsad

Univers Krokodil Bot - Telegram guruhlarida so'z topish o'yinini yuritadigan bot. Bot guruhga qo'shiladi, admin qilinadi va `/play` komandasi orqali yangi o'yin boshlanadi. O'yin arxitekturasi Univers Chess Bot loyihasiga o'xshash bo'lishi kerak: `bot.py`, `handlers/`, `models/`, `services/`, `keyboards/`, `constants.py`, `config.py`, `README.md`.

Bot mavjud Univers user/profil tizimiga ulanadi. `models/user.py` ichidagi `User`, `Profile`, `Transfers`, `Blocked_user` modellarini o'zgartirmaslik kerak. Krokodil o'yini uchun alohida profil, so'z va o'yin modellari qo'shiladi.

## Asosiy Talab

Bot vazifasi:

- guruhda `/play` orqali krokodil o'yinini yaratish;
- bazadan tasodifiy so'z tanlash;
- so'zni faqat tushuntiruvchi o'yinchiga ko'rsatish;
- qolgan guruh a'zolari javob yozishi;
- kim birinchi bo'lib to'g'ri javob yozsa yutadi;
- g'olib ball oladi va keyingi so'zni tushuntirish navbatini oladi;
- agar 15 soniya ichida hech kim javob topmasa yoki tushuntiruvchi kerakli harakatni qilmasa, istalgan foydalanuvchi navbatni o'ziga olishi mumkin;
- xabarlar tuzilishi, o'yin ketma-ketligi va tugmalar imkon qadar `@Crocodile_Game_Bot` flowiga o'xshashi kerak.

## Muhim UX Talab

Implementatsiya boshlashdan oldin `@Crocodile_Game_Bot` alohida test guruhda tekshiriladi va quyidagilar yozib olinadi:

- `/play` bosilganda qanday xabar chiqadi;
- o'yinchi navbat olganda qanday xabar chiqadi;
- tushuntiruvchiga so'z qanday ko'rsatiladi;
- guruhga so'z uzunligi yoki maskasi qanday ko'rsatiladi;
- to'g'ri javob topilganda qanday xabar chiqadi;
- vaqt tugaganda yoki navbat bo'shaganda qanday xabar chiqadi;
- keyboard tugmalari matni va ketma-ketligi qanday.

So'ng Univers Krokodil Bot xabarlari shu flowga maksimal yaqin qilinadi. To'liq nusxa olish shart emas, lekin foydalanuvchi tajribasi o'xshash bo'lishi kerak.

## Mavjud Modellar

Loyihada `models/user.py` ichida quyidagi mavjud modellar bor:

- `User` - Telegram foydalanuvchisi.
- `Profile` - asosiy profil, dollar/diamond kabi umumiy hisoblar shu yerda.
- `Transfers`.
- `Blocked_user`.

Bu modellar o'zgartirilmaydi. Krokodil statistikasi alohida modelda saqlanadi. Mukofot dollar berilsa, u `Profile.dollar`ga qo'shiladi.

## Yangi Modellar

Yangi modellar `models/crocodile.py` ichida bo'lishi tavsiya qilinadi. `models/__init__.py` Tortoise init ro'yxatiga `models.crocodile` qo'shiladi.

### CrocodileProfile

Har bir `User` uchun bitta krokodil profili.

Maydonlar:

- `id`.
- `user` - `User` foreign key, unique.
- `rating` - default `1000`.
- `points` - umumiy krokodil ballari.
- `games_count` - qatnashgan o'yinlar soni.
- `rounds_explained` - nechta so'z tushuntirgan.
- `correct_answers` - nechta so'z topgan.
- `wins` - o'yin yakunida birinchi o'rinlar soni.
- `created_at`.
- `updated_at`.

### CrocodileWord

So'zlar bazasi.

Maydonlar:

- `id`.
- `text` - so'z matni, unique.
- `language` - masalan `uz`, default `uz`.
- `category` - hayvon, narsa, kasb, film va hokazo, null bo'lishi mumkin.
- `difficulty` - `easy`, `medium`, `hard`, default `medium`.
- `is_active` - default `true`.
- `created_at`.
- `updated_at`.

So'zlar admin command yoki seed script orqali qo'shilishi mumkin. Boshlang'ich seed fayl bo'lsa yaxshi: `data/words_uz.txt`.

### CrocodileGame

Guruhdagi active o'yin.

Maydonlar:

- `id`.
- `chat_id` - guruh/supergroup ID.
- `chat_type` - `group` yoki `supergroup`.
- `status` - `waiting`, `active`, `paused`, `finished`, `cancelled`.
- `starter` - o'yinni boshlagan `User`.
- `current_explainer` - hozir so'z tushuntirayotgan `User`, null bo'lishi mumkin.
- `current_word` - hozirgi `CrocodileWord`, null bo'lishi mumkin.
- `round_number` - nechanchi round.
- `message_id` - asosiy game status xabari.
- `word_message_id` - tushuntiruvchiga yuborilgan private yoki guruhdagi service xabar IDsi, kerak bo'lsa.
- `round_started_at`.
- `claim_available_at` - 15 soniyadan keyin navbat olish ochiladigan vaqt.
- `last_activity_at` - oxirgi topilgan javob yoki yangi so'z olingan vaqt.
- `last_correct_user` - oxirgi topgan foydalanuvchi.
- `created_at`.
- `updated_at`.
- `finished_at`.

Bir guruhda bir vaqtning o'zida faqat bitta active/waiting o'yin bo'lishi kerak.

### CrocodileRound

Har bir so'z/round tarixi.

Maydonlar:

- `id`.
- `game` - `CrocodileGame`.
- `word` - `CrocodileWord`.
- `explainer` - tushuntiruvchi `User`.
- `winner` - topgan `User`, null bo'lishi mumkin.
- `round_number`.
- `status` - `active`, `guessed`, `skipped`, `timeout`, `cancelled`.
- `started_at`.
- `claim_available_at`.
- `finished_at`.
- `answer_message_id` - to'g'ri javob yozilgan xabar IDsi, null bo'lishi mumkin.

### CrocodileGuess

Javob urinishlari tarixi.

Maydonlar:

- `id`.
- `round` - `CrocodileRound`.
- `user` - javob yozgan `User`.
- `message_id` - Telegram message ID.
- `text` - foydalanuvchi yozgan matn.
- `is_correct` - boolean.
- `created_at`.

Har bir noto'g'ri javobni yozish shart emas, lekin anti-spam, audit va statistika uchun foydali. Agar DB yukini kamaytirish kerak bo'lsa, faqat to'g'ri javob yozilishi mumkin.

### CrocodileScore

Guruhdagi bitta o'yin ichidagi hisob.

Maydonlar:

- `id`.
- `game` - `CrocodileGame`.
- `user` - `User`.
- `points` - shu o'yindagi ball.
- `correct_answers`.
- `rounds_explained`.
- `created_at`.
- `updated_at`.

`game + user` unique bo'lishi kerak.

## Ball Berish Qoidasi

Boshlang'ich qoidalar:

- to'g'ri topgan foydalanuvchiga `+1` ball;
- topgan foydalanuvchi keyingi round tushuntiruvchisiga aylanadi;
- o'yin davomida hisob `CrocodileScore`da saqlanadi;
- umumiy statistika `CrocodileProfile`ga yoziladi.

Keyinroq dollar mukofoti qo'shilsa, faqat game yakunida TOP 1 yoki TOP 3ga `Profile.dollar` orqali beriladi.

O'yin ichida kim qancha ball ishlaganini bot reyting ko'rinishida chiqarib turadi. Bu `/top` global reytingdan alohida bo'ladi: `/top` umumiy profil reytingi, o'yin ichidagi reyting esa faqat shu `CrocodileGame` scorelari.

## O'yin Flow

### 1. Botni Guruhga Qo'shish

1. Bot guruhga qo'shiladi.
2. Bot admin qilinadi.
3. Bot xabarlarni o'qiy olishi kerak. Privacy mode o'chirilgan bo'lishi yoki bot admin sifatida kerakli xabarlarni olishi kerak.
4. Private chatda `/play` ishlamasligi kerak, foydalanuvchiga guruhda ishlashi aytiladi.

### 2. `/play` Bilan O'yin Boshlash

1. Foydalanuvchi guruhda `/play` yozadi.
2. Bot shu guruhda active o'yin bor-yo'qligini tekshiradi.
3. Active o'yin bo'lsa, mavjud o'yin status xabarini qaytaradi.
4. Active o'yin bo'lmasa, `CrocodileGame` yaratiladi.
5. Bot o'yin boshlanganini va boshlovchi kerakligini bildiradigan xabar yuboradi:

```text
🎮 Krokodil o'yini boshlandi.
Kim so'zni tushuntiradi?
```

6. Xabar ostida bitta tugma bo'ladi:

```text
👋 Boshlovchi bo'lishni xohlayman!
```

7. `/play` xabaridan keyin o'yinni to'xtatish tugmasi chiqmaydi. O'yin faqat `/stop` komandasi orqali to'xtatiladi.

### 3. Tushuntiruvchi Navbat Oladi

1. `👋 Boshlovchi bo'lishni xohlayman!` tugmasini bosgan foydalanuvchi current explainer bo'ladi.
2. Agar current explainer allaqachon bor bo'lsa, boshqa foydalanuvchiga ruxsat berilmaydi.
3. Bazadan random active so'z tanlanadi.
4. Round yaratiladi.
5. Bot guruhga active round xabarini yuboradi yoki mavjud xabarni edit qiladi. Bu xabarda aynan kim so'zni tushuntirayotgani aytiladi:

```text
<explainer> so'zni tushuntiradi 🌙
```

6. Shu xabar ostida 2 ta tugma bo'ladi:

```text
👀 So'zni ko'rish
⏭️ Yangi so'z
```

7. `👀 So'zni ko'rish` tugmasini faqat current explainer bosishi mumkin. Bot so'zni callback alert orqali ko'rsatadi, shunda so'z guruhga chiqmaydi.
8. `⏭️ Yangi so'z` tugmasini faqat current explainer bosishi mumkin. Agar berilgan so'zni tushuntirolmasa, yangi random so'z oladi. Eski round `skipped` bo'ladi, yangi round shu explainer bilan boshlanadi.
9. Bitta roundda birdaniga bir nechta current explainer bo'lib qolmasligi shart.

### 4. Guruh Javob Yozadi

1. Bot guruhga round boshlanganini yozadi.
2. Guruh xabarida tushuntiruvchi mention qilinadi.
3. So'zning o'zi guruhga chiqmaydi.
4. Istasa so'z uzunligi maska sifatida chiqadi: `_ _ _ _ _`.
5. Guruhdagi barcha oddiy message handlerlar javob sifatida tekshiriladi.
6. Tushuntiruvchi o'zi javob berolmaydi.
7. Botlar javob berolmaydi.
8. Javob case-insensitive, ortiqcha space va belgilar normalize qilingan holda tekshiriladi.
9. Tushuntiruvchi so'zni to'g'ridan-to'g'ri chatga yozib yuborsa ham bu javob sifatida qabul qilinmaydi.

### 5. To'g'ri Javob

1. Kimdir so'zni to'g'ri yozsa, round darhol tugaydi.
2. `CrocodileGuess.is_correct=true` yoziladi.
3. G'olibga ball qo'shiladi.
4. `CrocodileProfile` yangilanadi.
5. Bot guruhga rasmga o'xshash topildi xabarini yuboradi. Bu yerda `taxmin qildi` degani foydalanuvchi so'zni to'g'ri topganini anglatadi. Xabarda kim qaysi so'zni taxmin qilgani aytiladi:

```text
💚 <winner> <word> so'zini taxmin qildi
```

6. Shu xabar ostida yana bitta tugma chiqadi:

```text
👋 Boshlovchi bo'lishni xohlayman!
```

7. To'g'ri topgan foydalanuvchi keyingi tushuntiruvchi bo'lishga birinchi haqli nomzod sifatida runtime stateda saqlanadi.
8. Shu foydalanuvchiga tushuntirish navbatini olish uchun 15 soniya vaqt beriladi.
9. 15 soniya ichida faqat taxmin qilgan/topgan foydalanuvchi `👋 Boshlovchi bo'lishni xohlayman!` tugmasi orqali navbatni olishi mumkin.
10. Agar taxmin qilgan odam 15 soniya ichida bosmasa, keyin tugmani bosgan istalgan odam navbatni olib ketadi.
11. Xabarda yoki alohida status xabarida o'yin ichidagi ball reytingi ko'rsatiladi.

Muhim ketma-ketlik:

- round boshlanganda faqat `<explainer> so'zni tushuntiradi` mazmunidagi xabar chiqadi;
- javob topilganda faqat `<winner> <word> so'zini taxmin qildi` mazmunidagi xabar chiqadi;
- bu ikki holat aralashib ketmasligi kerak.

### 6. 15 Soniyadan Keyin Navbat Olish

1. Har round boshlanganda yoki navbat bo'shaganda `claim_available_at = now + 15 seconds` yoziladi.
2. To'g'ri topgan foydalanuvchi bo'lsa, 15 soniya davomida navbat faqat unga tegishli.
3. Shu 15 soniyada boshqa foydalanuvchi tugmani bossa, bot `Navbat hozir so'zni taxmin qilgan o'yinchida` mazmunida callback alert qaytaradi.
4. 15 soniyadan keyin tugmani birinchi bosgan istalgan foydalanuvchi navbatni o'ziga olishi mumkin.
5. Buni watchdog service tekshiradi yoki callback bosilganda lazy tekshiradi.

### 7. O'yinni Tugatish

Tugatish variantlari:

- `/stop` komandasi;
- admin yoki o'yin starteri tugatishi;
- uzoq vaqt activity bo'lmasa watchdog avtomatik tugatishi.

Tugaganda:

- `CrocodileGame.status = finished`;
- active round bo'lsa `cancelled` yoki `timeout`;
- final scoreboard va shu o'yindagi reyting yuboriladi;
- umumiy profil statistikasi yangilanadi.

## Handlerlar

Tavsiya qilingan fayllar:

- `handlers/game.py` - `/play`, `/stop`, asosiy callbacklar.
- `handlers/answers.py` - guruhdagi matn javoblarini tekshirish.
- `handlers/profiles.py` - `/profile`.
- `handlers/top.py` - `/top`.
- `handlers/admin.py` - so'z qo'shish/o'chirish/import qilish, kerak bo'lsa.

Routerlar `handlers/__init__.py` ichida bitta root routerga ulanadi.

## Keyboardlar

`keyboards/game.py`:

- `claim_keyboard(game)` - `👋 Boshlovchi bo'lishni xohlayman!` tugmasi.
- `round_keyboard(game)` - active tushuntiruvchi uchun `👀 So'zni ko'rish` va `⏭️ Yangi so'z` tugmalari.

Callback data formatlari:

```text
cr:claim:<game_id>
cr:show_word:<game_id>
cr:new_word:<game_id>
cr:noop
```

Har callbackda tekshiriladi:

- game mavjudmi;
- game status active/waitingmi;
- callback shu guruhdagi gamega tegishlimi;
- bosgan user bot emasmi;
- `claim` uchun navbat olishga ruxsat bormi.
- `show_word` va `new_word` uchun bosgan user current explainer ekanmi.

## Service Qatlamlari

Tavsiya qilingan fayllar:

- `services/users.py` - `get_or_create_user`, `user_mention`, krokodil profil yaratish.
- `services/words.py` - random word tanlash, normalize qilish, import/seed.
- `services/runtime_state.py` - RAM ichidagi active game state, locklar, dirty state flaglari.
- `services/game_state.py` - game yaratish, round boshlash, round tugatish, score update.
- `services/answers.py` - javob normalize qilish va to'g'ri/noto'g'ri tekshirish.
- `services/game_runtime.py` - per-game lock, race condition oldini olish.
- `services/game_watchdog.py` - 15 soniya claim availability, idle timeout va periodic DB flush.
- `services/telegram_safe.py` - Telegram retry wrapper.

Race condition muhim: ikki odam bir vaqtda to'g'ri javob yozishi yoki ikki odam bir vaqtda navbat olish tugmasini bosishi mumkin. Shuning uchun `locked_game(chat_id/game_id)` ishlatiladi.

## Runtime State va DB Flush

O'yin jarayonida tez-tez keladigan javoblar va navbat claimlari sabab asosiy active state lokal Python process RAMida saqlanadi. Bu loyiha single-process bot sifatida ishlaydi, shuning uchun event loop ichidagi per-game locklar, Python runtime xotirasi va single-process GIL assumption active round uchun authoritative source bo'ladi.

RAM state tavsiya qilingan tuzilma:

- `active_games[chat_id]` - active game snapshot;
- `current_word_id`;
- `current_word_text`;
- `current_explainer_tg_id`;
- `preferred_next_explainer_tg_id`;
- `claim_available_at`;
- `scores`;
- `round_number`;
- `dirty` flag.

Muhim talablar:

- bir guruh uchun bitta `asyncio.Lock` bo'ladi;
- claim, new word va correct answer operatsiyalari lock ichida bajariladi;
- lock ichida tekshiruv va state update atomic bo'ladi;
- shu sabab birdaniga bir nechta odam yangi so'z aytuvchi bo'lib qolmaydi;
- background task vaqti-vaqti bilan dirty state'larni DBga flush qiladi;
- `/stop` bosilganda avval RAM state DBga flush qilinadi, keyin game finished qilinadi;
- bot restart bo'lsa, DBdagi active/waiting game'lar `paused` yoki `finished` holatga o'tkazilishi mumkin, chunki RAMdagi current word xavfsiz tiklanmasligi mumkin.

DB flush interval boshlang'ich qiymati: `5` soniya. Juda faol guruhlar uchun javob urinishlari DBga yozilmasligi yoki batch qilib yozilishi mumkin.

## Javobni Tekshirish

Normalize qoidalari:

- lowercase;
- bosh/oxir space olib tashlash;
- bir nechta spaceni bitta spacega tushirish;
- apostrof turlari bir xil qilinadi;
- `ё/е`, `ў/o'`, `ғ/g'`, `қ/q` kabi transliteratsiya masalalari keyinroq kengaytiriladi.

Boshlang'ich versiyada aniq tenglik yetarli:

```text
normalize(message.text) == normalize(current_word.text)
```

Keyinroq typo tolerance qo'shilishi mumkin.

## Bot Commandlar

Boshlang'ich komandalar:

- `/start` - bot haqida qisqa xabar.
- `/play` - guruhda yangi krokodil o'yini boshlash.
- `/stop` - active o'yinni tugatish.
- `/profile` - foydalanuvchining krokodil statistikasi.
- `/top` - global krokodil reytingi yoki umumiy ball bo'yicha TOP.
- `/help` - qisqa qo'llanma.

Admin komandalar keyinroq:

- `/addword <so'z>` - so'z qo'shish.
- `/delword <so'z yoki id>` - so'zni o'chirish yoki inactive qilish.
- `/words_count` - active so'zlar soni.

## Bot Admin va Privacy Talablari

- Bot guruhda oddiy javoblarni ko'rishi kerak.
- BotFather privacy mode o'chirilgan bo'lishi tavsiya qilinadi.
- Bot admin bo'lsa, kerakli message eventlar kelishi aniqroq bo'ladi.
- So'z callback alert orqali ko'rsatiladi, shuning uchun private chatga yuborish majburiy emas.
- Agar keyinroq private chat varianti qo'shilsa, foydalanuvchi botni oldin `/start` qilgan bo'lishi kerak.

## Minimal Ish Rejasi

1. Loyiha strukturasi Univers Chess Botga o'xshash ekanini tekshirish.
2. `models/user.py` mavjud modellariga tegmaslik.
3. `models/crocodile.py` yaratish.
4. `CrocodileProfile`, `CrocodileWord`, `CrocodileGame`, `CrocodileRound`, `CrocodileGuess`, `CrocodileScore` modellarini qo'shish.
5. `models/__init__.py`ga yangi model modulini ulash.
6. `services/users.py`da krokodil profil auto-create qilish.
7. `services/words.py`da random so'z tanlash va normalize funksiyalarini yozish.
8. `services/game_runtime.py`da lock mexanizmini yozish.
9. `services/runtime_state.py`da RAM active game state yozish.
10. `keyboards/game.py`da inline keyboardlar yozish.
11. `/play` handlerini yozish.
12. `cr:claim` callback orqali tushuntiruvchi navbat olishini yozish.
13. `cr:show_word` callback orqali so'zni faqat tushuntiruvchiga alert qilib ko'rsatishni yozish.
14. Guruhdagi text message handler orqali javob tekshirishni yozish.
15. To'g'ri javob topilganda ball, profile va next explainer flowini yozish.
16. 15 soniyadan keyin navbat olish ochilishini yozish.
17. `cr:new_word` callback orqali active tushuntiruvchi yangi so'z olishini yozish.
18. Periodic DB flush background taskini yozish.
19. `/stop` komandasini yozish.
20. `/profile` va `/top` komandalarini yozish.
21. `README.md`ga botni ishga tushirish, BotFather privacy/admin talablari va game flow yozish.
22. Seed words fayli yoki admin orqali so'z kiritish flowini qo'shish.

## Qabul Qilish Mezonlari

- Guruhda `/play` bosilganda yangi o'yin yaratiladi.
- Bir guruhda bir vaqtda bitta active o'yin bo'ladi.
- Bazadan random so'z tanlanadi.
- So'z guruhga ko'rinmaydi, tushuntiruvchiga alohida ko'rsatiladi.
- Guruhdagi javoblar real time tekshiriladi.
- To'g'ri javob yozgan birinchi user yutadi.
- G'olib ball oladi.
- G'olib keyingi tushuntirish navbatiga birinchi haqli bo'ladi.
- 15 soniyadan keyin istalgan user navbatni olishi mumkin.
- Active tushuntiruvchi `👀 So'zni ko'rish` orqali so'zni faqat o'zi ko'radi.
- Active tushuntiruvchi `⏭️ Yangi so'z` orqali yangi so'z oladi.
- Bir vaqtda bir nechta current explainer paydo bo'lmaydi.
- O'yin faqat `/stop` orqali to'xtatiladi.
- Shu o'yin ichidagi ballar reyting qilib chiqariladi.
- O'yin hisoblari `CrocodileScore`da saqlanadi.
- Umumiy statistika `CrocodileProfile`da saqlanadi.
- Existing `User/Profile` modeli o'zgarmaydi.
- Bot restartdan keyin DB schema buzilmaydi; RAMdagi current word xavfsiz tiklanmasligi sabab active game'lar `paused` yoki `finished` qilinadi.
- Race conditionlarda bitta round uchun faqat bitta winner yoziladi.

## Eslatmalar

- Xabarlar va tugmalar `@Crocodile_Game_Bot` flowiga o'xshash bo'lishi kerak, shuning uchun implementatsiya oldidan u bot test qilinadi.
- Bot admin qilinishi va privacy mode masalasi alohida READMEda yozilishi shart.
- Krokodil o'yini command-spamni kamaytirishi uchun asosiy interaction inline keyboard va oddiy javob message orqali bo'ladi.
- Agar guruh juda faol bo'lsa, noto'g'ri javoblarni DBga yozmaslik yoki rate-limit qo'shish mumkin.
