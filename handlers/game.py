from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from keyboards.game import claim_keyboard, round_keyboard
from models.crocodile import CrocodileGame
from services.chats import upsert_crocodile_chat_from_message
from services.game_runtime import locked_game
from services.game_state import (
    create_game,
    finish_game,
    get_active_game,
    scoreboard_text,
    skip_round,
    start_round,
)
from services.users import get_or_create_user, telegram_user_id, user_mention

router = Router()


def is_group(message: Message) -> bool:
    return message.chat.type in {"group", "supergroup"}


def is_future(value) -> bool:
    now = datetime.now(timezone.utc) if value.tzinfo else datetime.now()
    return value > now


async def add_to_group_keyboard(message: Message) -> InlineKeyboardMarkup | None:
    bot_info = await message.bot.get_me()
    if not bot_info.username:
        return None
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Guruhga qo'shish",
                    url=f"https://t.me/{bot_info.username}?startgroup=true",
                )
            ]
        ]
    )


@router.message(Command("start", "help"))
async def start_help(message: Message) -> None:
    keyboard = await add_to_group_keyboard(message)
    await message.answer(
        "🐊 <b>Univers Krokodil</b> - do'stlar bilan so'z topish o'yini.\n\n"
        "Botni guruhga qo'shing va guruhda <b>/play</b> yozing. "
        "Keyin kimdir <b>boshlovchi bo'lish</b> tugmasini bosadi.\n\n"
        "Boshlovchiga yashirin so'z ko'rsatiladi. U so'zni aytmasdan, "
        "imo-ishora yoki tushuntirish orqali boshqalarga topdiradi. "
        "Guruhdagilar javobni chatga yozadi.\n\n"
        "Kim birinchi bo'lib to'g'ri topsa, ball oladi va keyingi so'zni "
        "tushuntirish navbatini olishi mumkin.\n\n"
        "O'yinni tugatish uchun guruhda <b>/stop</b> yozing.",
        reply_markup=keyboard,
    )


@router.message(Command("play"))
async def play(message: Message) -> None:
    if not is_group(message):
        await message.answer("Krokodil o'yini faqat guruh yoki superguruhda ishlaydi.")
        return

    await upsert_crocodile_chat_from_message(message.chat, message.bot)
    user = await get_or_create_user(message.from_user)
    async with locked_game(message.chat.id):
        game = await get_active_game(message.chat.id)
        if game:
            await message.answer(
                "🎮 Bu guruhda krokodil o'yini allaqachon boshlangan.\nKim so'zni tushuntiradi?",
                reply_markup=claim_keyboard(game.id),
            )
            return
        game = await create_game(message.chat.id, message.chat.type, user)
        sent = await message.answer(
            "🎮 Krokodil o'yini boshlandi.\nKim so'zni tushuntiradi?",
            reply_markup=claim_keyboard(game.id),
        )
        game.message_id = sent.message_id
        await game.save()


@router.message(Command("stop"))
async def stop(message: Message) -> None:
    if not is_group(message):
        await message.answer("Bu komanda guruhdagi o'yin uchun.")
        return
    async with locked_game(message.chat.id):
        game = await get_active_game(message.chat.id)
        if not game:
            await message.answer("Bu guruhda active krokodil o'yini yo'q.")
            return
        scores = await scoreboard_text(game)
        await finish_game(game)
    await message.answer(f"🛑 Krokodil o'yini tugadi.\n\n{scores}")


@router.callback_query(F.data.startswith("cr:claim:"))
async def claim_turn(callback: CallbackQuery) -> None:
    if not callback.message or not callback.from_user:
        await callback.answer()
        return
    game_id = int(callback.data.rsplit(":", 1)[1])
    tg_user = callback.from_user
    user = await get_or_create_user(tg_user)

    async with locked_game(callback.message.chat.id):
        game = await CrocodileGame.get_or_none(id=game_id, chat_id=callback.message.chat.id)
        if not game or game.status not in {"waiting", "active", "paused"}:
            await callback.answer("O'yin topilmadi yoki tugagan.", show_alert=True)
            return
        await game.fetch_related("last_correct_user")
        if game.current_explainer_id:
            await callback.answer("Hozir boshqa o'yinchi so'zni tushuntiryapti.", show_alert=True)
            return
        if game.last_correct_user and telegram_user_id(game.last_correct_user) != tg_user.id:
            claim_at = game.claim_available_at
            if claim_at and is_future(claim_at):
                await callback.answer(
                    "Navbat hozir so'zni taxmin qilgan o'yinchida.", show_alert=True
                )
                return
        try:
            game, _ = await start_round(game, user)
        except ValueError:
            await callback.answer(
                "So'zlar bazasi bo'sh. Avval /import_words orqali so'zlarni yuklang.",
                show_alert=True,
            )
            return
        await callback.message.answer(
            f"{user_mention(user)} so'zni tushuntiradi 🌙",
            reply_markup=round_keyboard(game.id),
        )
        await callback.answer("Navbat sizda!")


@router.callback_query(F.data.startswith("cr:show_word:"))
async def show_word(callback: CallbackQuery) -> None:
    game_id = int(callback.data.rsplit(":", 1)[1])
    game = await CrocodileGame.get_or_none(id=game_id).prefetch_related(
        "current_explainer", "current_word"
    )
    if not game or not game.current_word:
        await callback.answer("Hozir active so'z yo'q.", show_alert=True)
        return
    if not game.current_explainer or telegram_user_id(game.current_explainer) != callback.from_user.id:
        await callback.answer("So'zni faqat tushuntiruvchi ko'ra oladi.", show_alert=True)
        return
    await callback.answer(game.current_word.text, show_alert=True)


@router.callback_query(F.data.startswith("cr:new_word:"))
async def new_word(callback: CallbackQuery) -> None:
    if not callback.message:
        await callback.answer()
        return
    game_id = int(callback.data.rsplit(":", 1)[1])
    async with locked_game(callback.message.chat.id):
        game = await CrocodileGame.get_or_none(id=game_id, chat_id=callback.message.chat.id)
        if not game:
            await callback.answer("O'yin topilmadi.", show_alert=True)
            return
        await game.fetch_related("current_explainer")
        if not game.current_explainer or telegram_user_id(game.current_explainer) != callback.from_user.id:
            await callback.answer("Yangi so'zni faqat tushuntiruvchi oladi.", show_alert=True)
            return
        explainer = game.current_explainer
        await skip_round(game)
        try:
            game, _ = await start_round(game, explainer)
        except ValueError:
            await callback.answer(
                "So'zlar bazasi bo'sh. Avval /import_words orqali so'zlarni yuklang.",
                show_alert=True,
            )
            return
        await callback.answer(game.current_word.text, show_alert=True)
