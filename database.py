from tortoise import Tortoise


MIGRATIONS = [
    """
    ALTER TABLE crocodile_games
    ADD COLUMN IF NOT EXISTS category VARCHAR(64) NULL;
    """,
    """
    INSERT INTO crocodile_categories (slug, display_name, emoji, "order", is_active, is_special) VALUES
        ('oddiy',   'Oddiy so''zlar',    '📝', 1,  TRUE, FALSE),
        ('kino',    'Kino va multfilm', '🎬', 2,  TRUE, FALSE),
        ('tarixiy', 'Tarixiy shaxslar','🏛️', 3,  TRUE, FALSE),
        ('musiqa',  'Musiqa',           '🎵', 4,  TRUE, FALSE),
        ('aralash', 'Aralash (barcha)', '🎲', 99, TRUE, TRUE)
    ON CONFLICT (slug) DO NOTHING;
    """,
]


async def run_migrations() -> None:
    conn = Tortoise.get_connection("default")
    for sql in MIGRATIONS:
        await conn.execute_script(sql)
