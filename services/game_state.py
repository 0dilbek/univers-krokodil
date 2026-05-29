from datetime import datetime, timedelta, timezone
from html import escape

from models.crocodile import (
    CrocodileGame,
    CrocodileGuess,
    CrocodileProfile,
    CrocodileRound,
    CrocodileScore,
)
from models.user import User
from services.runtime_state import GameSnapshot, remove_snapshot, set_snapshot
from services.users import display_name, telegram_user_id
from services.words import get_random_word

from constants import ACTIVE_GAME_STATUSES, CLAIM_LOCK_SECONDS


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


async def get_active_game(chat_id: int) -> CrocodileGame | None:
    return (
        await CrocodileGame.filter(chat_id=chat_id, status__in=ACTIVE_GAME_STATUSES)
        .order_by("-id")
        .first()
    )


async def create_game(chat_id: int, chat_type: str, starter: User) -> CrocodileGame:
    game = await CrocodileGame.create(
        chat_id=chat_id,
        chat_type=chat_type,
        starter=starter,
        status="waiting",
        last_activity_at=now_utc(),
    )
    set_snapshot(GameSnapshot(game_id=game.id, chat_id=chat_id, status=game.status))
    return game


async def start_round(game: CrocodileGame, explainer: User) -> tuple[CrocodileGame, CrocodileRound]:
    word = await get_random_word()
    claim_at = now_utc() + timedelta(seconds=CLAIM_LOCK_SECONDS)
    game.current_explainer = explainer
    game.current_word = word
    game.status = "active"
    game.round_number += 1
    game.round_started_at = now_utc()
    game.claim_available_at = claim_at
    game.last_activity_at = now_utc()
    await game.save()

    round_ = await CrocodileRound.create(
        game=game,
        word=word,
        explainer=explainer,
        round_number=game.round_number,
        claim_available_at=claim_at,
    )
    score, _ = await CrocodileScore.get_or_create(game=game, user=explainer)
    score.rounds_explained += 1
    await score.save()

    profile, _ = await CrocodileProfile.get_or_create(user=explainer)
    profile.rounds_explained += 1
    await profile.save()

    set_snapshot(
        GameSnapshot(
            game_id=game.id,
            chat_id=game.chat_id,
            status=game.status,
            current_round_id=round_.id,
            current_word_id=word.id,
            current_word_text=word.text,
            current_explainer_tg_id=telegram_user_id(explainer),
            preferred_next_explainer_tg_id=None,
            claim_available_at=claim_at,
            round_number=game.round_number,
            dirty=False,
        )
    )
    return game, round_


async def skip_round(game: CrocodileGame) -> None:
    active_round = (
        await CrocodileRound.filter(game=game, status="active").order_by("-id").first()
    )
    if active_round:
        active_round.status = "skipped"
        active_round.finished_at = now_utc()
        await active_round.save()


async def finish_round_with_winner(
    game: CrocodileGame,
    winner: User,
    message_id: int,
    answer_text: str,
) -> CrocodileRound | None:
    round_ = (
        await CrocodileRound.filter(game=game, status="active")
        .prefetch_related("word")
        .order_by("-id")
        .first()
    )
    if not round_:
        return None

    await CrocodileGuess.create(
        round=round_,
        user=winner,
        message_id=message_id,
        text=answer_text[:512],
        is_correct=True,
    )
    round_.winner = winner
    round_.status = "guessed"
    round_.finished_at = now_utc()
    round_.answer_message_id = message_id
    await round_.save()

    score, _ = await CrocodileScore.get_or_create(game=game, user=winner)
    score.points += 1
    score.correct_answers += 1
    await score.save()

    profile, _ = await CrocodileProfile.get_or_create(user=winner)
    profile.points += 1
    profile.correct_answers += 1
    await profile.save()

    claim_at = now_utc() + timedelta(seconds=CLAIM_LOCK_SECONDS)
    game.current_explainer = None
    game.current_word = None
    game.status = "waiting"
    game.last_correct_user = winner
    game.claim_available_at = claim_at
    game.last_activity_at = now_utc()
    await game.save()

    set_snapshot(
        GameSnapshot(
            game_id=game.id,
            chat_id=game.chat_id,
            status=game.status,
            preferred_next_explainer_tg_id=telegram_user_id(winner),
            claim_available_at=claim_at,
            round_number=game.round_number,
            dirty=False,
        )
    )
    return round_


async def finish_game(game: CrocodileGame) -> None:
    active_round = await CrocodileRound.filter(game=game, status="active").first()
    if active_round:
        active_round.status = "cancelled"
        active_round.finished_at = now_utc()
        await active_round.save()
    game.status = "finished"
    game.current_explainer = None
    game.current_word = None
    game.finished_at = now_utc()
    game.last_activity_at = now_utc()
    await game.save()
    remove_snapshot(game.chat_id)


async def scoreboard_text(game: CrocodileGame) -> str:
    scores = (
        await CrocodileScore.filter(game=game)
        .prefetch_related("user")
        .order_by("-points", "created_at")
        .limit(10)
    )
    if not scores:
        return "Hozircha ball yo'q."
    lines = ["🏆 Hisob:"]
    for index, score in enumerate(scores, start=1):
        lines.append(f"{index}. {escape(display_name(score.user))} - {score.points}")
    return "\n".join(lines)


async def group_rating_text(chat_id: int) -> str:
    scores = (
        await CrocodileScore.filter(game__chat_id=chat_id)
        .prefetch_related("user")
        .order_by("-points", "created_at")
    )
    totals: dict[int, dict[str, object]] = {}
    for score in scores:
        item = totals.setdefault(
            score.user_id,
            {"name": display_name(score.user), "points": 0, "correct_answers": 0},
        )
        item["points"] += score.points
        item["correct_answers"] += score.correct_answers

    if not totals:
        return "Bu guruhda hali reyting yo'q."

    rows = sorted(
        totals.values(),
        key=lambda item: (-int(item["points"]), -int(item["correct_answers"]), str(item["name"])),
    )[:10]
    lines = ["🏆 Guruh reytingi:"]
    for index, item in enumerate(rows, start=1):
        lines.append(f"{index}. {escape(str(item['name']))} - {item['points']} ball")
    return "\n".join(lines)
