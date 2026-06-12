from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message, TelegramObject


class DeleteCommandMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        result = await handler(event, data)
        if isinstance(event, Message) and event.entities:
            for entity in event.entities:
                if entity.type == "bot_command" and entity.offset == 0:
                    try:
                        await event.delete()
                    except (TelegramBadRequest, TelegramForbiddenError):
                        pass
                    break
        return result
