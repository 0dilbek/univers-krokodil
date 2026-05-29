import asyncio
from contextlib import asynccontextmanager

_locks: dict[int, asyncio.Lock] = {}


def game_lock(chat_id: int) -> asyncio.Lock:
    lock = _locks.get(chat_id)
    if lock is None:
        lock = asyncio.Lock()
        _locks[chat_id] = lock
    return lock


@asynccontextmanager
async def locked_game(chat_id: int):
    lock = game_lock(chat_id)
    async with lock:
        yield
