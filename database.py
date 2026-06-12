from tortoise import Tortoise


MIGRATIONS = [
    """
    ALTER TABLE crocodile_games
    ADD COLUMN IF NOT EXISTS category VARCHAR(64) NULL;
    """,
]


async def run_migrations() -> None:
    conn = Tortoise.get_connection("default")
    for sql in MIGRATIONS:
        await conn.execute_script(sql)
