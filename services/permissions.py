from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message


GROUP_ADMIN_STATUSES = {"administrator", "creator"}


def is_group_chat(message: Message) -> bool:
    return message.chat.type in {"group", "supergroup"}


async def is_group_admin(message: Message) -> bool:
    if not is_group_chat(message) or not message.from_user:
        return False
    try:
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    except (TelegramBadRequest, TelegramForbiddenError):
        return False
    return member.status in GROUP_ADMIN_STATUSES
