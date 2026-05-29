from aiogram.types import User as TelegramUser
from html import escape

from models.crocodile import CrocodileProfile
from models.user import Profile, User


async def get_or_create_user(tg_user: TelegramUser) -> User:
    full_name = tg_user.full_name or tg_user.first_name or ""
    mention = f'<a href="tg://user?id={tg_user.id}">{escape(full_name or str(tg_user.id))}</a>'
    user, _ = await User.get_or_create(
        user_id=tg_user.id,
        defaults={
            "full_name": full_name,
            "mention": mention,
            "is_bot": tg_user.is_bot,
        },
    )
    changed = False
    updates = {
        "full_name": full_name,
        "mention": mention,
        "is_bot": tg_user.is_bot,
    }
    for attr, value in updates.items():
        if getattr(user, attr) != value:
            setattr(user, attr, value)
            changed = True
    if changed:
        await user.save()
    await Profile.get_or_create(user=user)
    await CrocodileProfile.get_or_create(user=user)
    return user


async def get_crocodile_profile(user: User) -> CrocodileProfile:
    profile, _ = await CrocodileProfile.get_or_create(user=user)
    return profile


def user_mention(user: User) -> str:
    if user.mention:
        return user.mention
    name = escape(display_name(user))
    return f'<a href="tg://user?id={user.user_id}">{name}</a>'


def display_name(user: User) -> str:
    return user.full_name or str(user.user_id)


def telegram_user_id(user: User) -> int:
    return user.user_id
