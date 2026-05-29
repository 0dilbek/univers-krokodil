from aiogram import F, Router
from aiogram.types import Message

from keyboards.game import claim_keyboard
from services.answers import is_correct_answer
from services.game_runtime import locked_game
from services.game_state import finish_round_with_winner, get_active_game
from services.users import get_or_create_user, telegram_user_id, user_mention

router = Router()


@router.message(F.text, ~F.text.startswith("/"))
async def check_answer(message: Message) -> None:
    if message.chat.type not in {"group", "supergroup"} or not message.from_user:
        return
    if message.from_user.is_bot:
        return

    async with locked_game(message.chat.id):
        game = await get_active_game(message.chat.id)
        if not game or game.status != "active":
            return
        await game.fetch_related("current_explainer", "current_word")
        if not game.current_explainer or not game.current_word:
            return
        if telegram_user_id(game.current_explainer) == message.from_user.id:
            return
        if not is_correct_answer(message.text, game.current_word.text):
            return

        winner = await get_or_create_user(message.from_user)
        word_text = game.current_word.text
        round_ = await finish_round_with_winner(
            game=game,
            winner=winner,
            message_id=message.message_id,
            answer_text=message.text,
        )
        if not round_:
            return

    await message.answer(
        f"💚 {user_mention(winner)} {word_text} so'zini taxmin qildi\n\n"
        "Keyingi boshlovchi kim?",
        reply_markup=claim_keyboard(game.id),
    )
