from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from constants import (
    BTN_CAT_ARALASH,
    BTN_CAT_KINO,
    BTN_CAT_MUSIQA,
    BTN_CAT_ODDIY,
    BTN_CAT_TARIXIY,
    BTN_CLAIM,
    BTN_NEW_WORD,
    BTN_SHOW_WORD,
)


def category_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=BTN_CAT_ODDIY, callback_data=f"cr:cat:oddiy:{chat_id}"),
                InlineKeyboardButton(text=BTN_CAT_KINO, callback_data=f"cr:cat:kino:{chat_id}"),
            ],
            [
                InlineKeyboardButton(text=BTN_CAT_TARIXIY, callback_data=f"cr:cat:tarixiy:{chat_id}"),
                InlineKeyboardButton(text=BTN_CAT_MUSIQA, callback_data=f"cr:cat:musiqa:{chat_id}"),
            ],
            [
                InlineKeyboardButton(text=BTN_CAT_ARALASH, callback_data=f"cr:cat:aralash:{chat_id}"),
            ],
        ]
    )


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
