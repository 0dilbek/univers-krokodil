from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from models.crocodile import CrocodileWord
from services.words import import_words_from_file

router = Router()


@router.message(Command("addword"))
async def add_word(message: Message) -> None:
    text = message.text.partition(" ")[2].strip()
    if not text:
        await message.answer("Foydalanish: /addword <so'z>")
        return
    word, created = await CrocodileWord.get_or_create(text=text, defaults={"language": "uz"})
    if not created and not word.is_active:
        word.is_active = True
        await word.save()
    await message.answer("✅ So'z qo'shildi." if created else "ℹ️ Bu so'z bazada bor.")


@router.message(Command("delword"))
async def del_word(message: Message) -> None:
    text = message.text.partition(" ")[2].strip()
    if not text:
        await message.answer("Foydalanish: /delword <so'z yoki id>")
        return
    query = CrocodileWord.filter(id=int(text)) if text.isdigit() else CrocodileWord.filter(text=text)
    word = await query.first()
    if not word:
        await message.answer("So'z topilmadi.")
        return
    word.is_active = False
    await word.save()
    await message.answer("✅ So'z inactive qilindi.")


@router.message(Command("words_count"))
async def words_count(message: Message) -> None:
    count = await CrocodileWord.filter(is_active=True).count()
    await message.answer(f"Active so'zlar: {count}")


@router.message(Command("import_words"))
async def import_words(message: Message) -> None:
    count = await import_words_from_file("data/words_uz.txt")
    await message.answer(f"✅ Import qilindi: {count} ta yangi so'z.")
