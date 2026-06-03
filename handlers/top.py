from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import settings
from models.crocodile import CrocodileProfile
from services.game_state import get_active_game, group_rating_text, scoreboard_text
from services.permissions import is_group_admin, is_group_chat
from services.users import display_name

router = Router()


@router.message(Command("top"))
async def top(message: Message) -> None:
    if is_group_chat(message):
        await message.answer(await group_rating_text(message.chat.id))
        return

    if not message.from_user or message.from_user.id not in settings.bot_admin_ids:
        await message.answer("Bu buyruq faqat bot admini uchun.")
        return

    profiles = (
        await CrocodileProfile.all()
        .prefetch_related("user")
        .order_by("-points", "-rating")
        .limit(10)
    )
    if not profiles:
        await message.answer("Hali krokodil reytingi yo'q.")
        return
    lines = ["🏆 Global Krokodil TOP"]
    for index, profile in enumerate(profiles, start=1):
        lines.append(f"{index}. {display_name(profile.user)} - {profile.points} ball")
    await message.answer("\n".join(lines))


@router.message(Command("reyting"))
async def reyting(message: Message) -> None:
    if not is_group_chat(message):
        await message.answer("Guruh reytingi faqat guruhda ko'rsatiladi.")
        return
    if not await is_group_admin(message):
        await message.answer("Reytingni faqat guruh adminlari ko'ra oladi.")
        return

    game = await get_active_game(message.chat.id)
    if game:
        await message.answer(await scoreboard_text(game))
        return

    await message.answer(await group_rating_text(message.chat.id))
