from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GameSnapshot:
    game_id: int
    chat_id: int
    status: str
    current_round_id: int | None = None
    current_word_id: int | None = None
    current_word_text: str | None = None
    current_explainer_tg_id: int | None = None
    preferred_next_explainer_tg_id: int | None = None
    claim_available_at: datetime | None = None
    scores: dict[int, int] = field(default_factory=dict)
    round_number: int = 0
    dirty: bool = False


active_games: dict[int, GameSnapshot] = {}


def set_snapshot(snapshot: GameSnapshot) -> None:
    active_games[snapshot.chat_id] = snapshot


def get_snapshot(chat_id: int) -> GameSnapshot | None:
    return active_games.get(chat_id)


def remove_snapshot(chat_id: int) -> None:
    active_games.pop(chat_id, None)
