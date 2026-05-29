from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    database_url: str
    bot_admin_ids: tuple[int, ...]


def parse_admin_ids(value: str) -> tuple[int, ...]:
    ids = []
    for item in value.split(","):
        item = item.strip()
        if item.isdigit():
            ids.append(int(item))
    return tuple(ids)


def load_settings() -> Settings:
    return Settings(
        bot_token=os.getenv("BOT_TOKEN", ""),
        database_url=os.getenv("DATABASE_URL", ""),
        bot_admin_ids=parse_admin_ids(os.getenv("BOT_ADMIN_IDS", "")),
    )


settings = load_settings()

TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": ["models.user", "models.crocodile", "aerich.models"],
            "default_connection": "default",
        }
    },
}
