import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from aiogram.exceptions import TelegramRetryAfter

T = TypeVar("T")


async def telegram_retry(call: Callable[[], Awaitable[T]]) -> T:
    try:
        return await call()
    except TelegramRetryAfter as exc:
        await asyncio.sleep(exc.retry_after)
        return await call()
