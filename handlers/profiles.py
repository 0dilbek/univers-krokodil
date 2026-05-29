from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from models.user import Profile
from services.users import get_crocodile_profile, get_or_create_user, user_mention

router = Router()


def univers_bots_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="♟ Univers Chess",
                    url="https://t.me/UniversCHessbot",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎭 Univers Mafia",
                    url="https://t.me/UnvMafiaBot",
                )
            ],
        ]
    )


@router.message(Command("profile", "profil"))
@router.message(F.text.regexp(r"^/(profile|profil)(@\w+)?$"))
async def profile(message: Message) -> None:
    if not message.from_user:
        return
    user = await get_or_create_user(message.from_user)
    stats = await get_crocodile_profile(user)
    profile, _ = await Profile.get_or_create(user=user)
    await message.answer(
        f"👤 {user_mention(user)}\n\n"
        f'<tg-emoji emoji-id="5215239948420003628">💵</tg-emoji> Dollar: {profile.dollar}\n'
        f'<tg-emoji emoji-id="5229173741451230931">💎</tg-emoji> Olmos: {profile.diamond}\n\n'
        f'<tg-emoji emoji-id="5210768496622840660">🎮</tg-emoji> Krokodil ball: {stats.points}\n'
        f'<tg-emoji emoji-id="5251332925135283922">⭐️</tg-emoji> '
        f"Tushuntirgan so'zlar: {stats.rounds_explained}",
        reply_markup=univers_bots_keyboard(),
    )
