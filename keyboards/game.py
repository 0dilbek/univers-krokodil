from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from constants import BTN_CLAIM, BTN_NEW_WORD, BTN_SHOW_WORD
from models.crocodile import CrocodileCategory


async def category_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    all_cats = await CrocodileCategory.filter(is_active=True).order_by("order")
    normal = [c for c in all_cats if not c.is_special]
    special = [c for c in all_cats if c.is_special]

    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for cat in normal:
        row.append(InlineKeyboardButton(
            text=f"{cat.emoji} {cat.display_name}",
            callback_data=f"cr:cat:{cat.slug}:{chat_id}",
        ))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    for cat in special:
        rows.append([InlineKeyboardButton(
            text=f"{cat.emoji} {cat.display_name}",
            callback_data=f"cr:cat:{cat.slug}:{chat_id}",
        )])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def claim_keyboard(game_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BTN_CLAIM, callback_data=f"cr:claim:{game_id}")]
        ]
    )


def round_keyboard(game_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=BTN_SHOW_WORD, callback_data=f"cr:show_word:{game_id}"),
                InlineKeyboardButton(text=BTN_NEW_WORD, callback_data=f"cr:new_word:{game_id}"),
            ]
        ]
    )
