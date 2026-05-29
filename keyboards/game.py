from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from constants import BTN_CLAIM, BTN_NEW_WORD, BTN_SHOW_WORD


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
