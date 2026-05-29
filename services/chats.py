from datetime import datetime, timezone

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Chat as TelegramChat

from models.crocodile import CrocodileChat


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


async def upsert_crocodile_chat_from_message(chat: TelegramChat, bot: Bot) -> CrocodileChat:
    record, _ = await CrocodileChat.get_or_create(
        chat_id=chat.id,
        defaults={
            "chat_type": chat.type,
            "title": chat.title,
            "username": chat.username,
            "is_active": True,
        },
    )
    record.chat_type = chat.type
    record.title = chat.title
    record.username = chat.username
    record.is_active = True
    await enrich_chat_record(record, bot)
    return record


async def enrich_chat_record(record: CrocodileChat, bot: Bot) -> None:
    try:
        chat = await bot.get_chat(record.chat_id)
        record.chat_type = chat.type
        record.title = chat.title
        record.username = chat.username
        if getattr(chat, "invite_link", None):
            record.invite_link = chat.invite_link
    except (TelegramBadRequest, TelegramForbiddenError):
        record.is_active = False
        record.last_synced_at = now_utc()
        await record.save()
        return

    try:
        record.members_count = await bot.get_chat_member_count(record.chat_id)
    except (TelegramBadRequest, TelegramForbiddenError):
        record.members_count = None

    if not record.invite_link:
        try:
            record.invite_link = await bot.export_chat_invite_link(record.chat_id)
        except (TelegramBadRequest, TelegramForbiddenError):
            record.invite_link = None

    record.is_active = True
    record.last_synced_at = now_utc()
    await record.save()


async def refresh_all_crocodile_chats(bot: Bot) -> None:
    async for record in CrocodileChat.filter(is_active=True):
        await enrich_chat_record(record, bot)
