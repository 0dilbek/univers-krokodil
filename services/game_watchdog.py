import asyncio

from aiogram import Bot

from constants import ACTIVE_GAME_STATUSES, CHAT_REFRESH_INTERVAL_SECONDS, DB_FLUSH_INTERVAL_SECONDS
from models.crocodile import CrocodileGame, CrocodileRound
from services.chats import refresh_all_crocodile_chats
from services.game_state import finish_game
from services.runtime_state import GameSnapshot, set_snapshot
from services.users import telegram_user_id


async def restore_active_games_on_startup() -> None:
    games = (
        await CrocodileGame.filter(status__in=ACTIVE_GAME_STATUSES)
        .prefetch_related("current_word", "current_explainer", "last_correct_user")
    )
    for game in games:
        active_round = (
            await CrocodileRound.filter(game=game, status="active").order_by("-id").first()
        )
        if game.status == "active" and (not game.current_word or not game.current_explainer):
            game.status = "waiting"
            game.current_word = None
            game.current_explainer = None
            await game.save()

        set_snapshot(
            GameSnapshot(
                game_id=game.id,
                chat_id=game.chat_id,
                status=game.status,
                current_round_id=active_round.id if active_round else None,
                current_word_id=game.current_word.id if game.current_word else None,
                current_word_text=game.current_word.text if game.current_word else None,
                current_explainer_tg_id=(
                    telegram_user_id(game.current_explainer) if game.current_explainer else None
                ),
                preferred_next_explainer_tg_id=(
                    telegram_user_id(game.last_correct_user) if game.last_correct_user else None
                ),
                claim_available_at=game.claim_available_at,
                round_number=game.round_number,
                dirty=False,
            )
        )


async def watchdog_loop() -> None:
    while True:
        await asyncio.sleep(DB_FLUSH_INTERVAL_SECONDS)
        # Runtime state is flushed immediately in this single-process MVP.


async def chat_refresh_loop(bot: Bot) -> None:
    while True:
        await refresh_all_crocodile_chats(bot)
        await asyncio.sleep(CHAT_REFRESH_INTERVAL_SECONDS)


async def finish_idle_game(game: CrocodileGame) -> None:
    await finish_game(game)
