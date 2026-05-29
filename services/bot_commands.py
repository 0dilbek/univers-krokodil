from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeDefault,
)


async def setup_bot_commands(bot: Bot) -> None:
    private_commands = [
        BotCommand(command="start", description="Bot haqida ma'lumot"),
        BotCommand(command="help", description="O'yin qo'llanmasi"),
        BotCommand(command="profile", description="Krokodil profilingiz"),
        BotCommand(command="profil", description="Krokodil profilingiz"),
    ]
    group_commands = [
        BotCommand(command="play", description="Krokodil o'yinini boshlash"),
        BotCommand(command="stop", description="O'yinni tugatish"),
        BotCommand(command="reyting", description="Guruh reytingini ko'rish"),
        BotCommand(command="profile", description="Krokodil profilingiz"),
        BotCommand(command="profil", description="Krokodil profilingiz"),
        BotCommand(command="help", description="O'yin qo'llanmasi"),
    ]

    await bot.set_my_commands(private_commands, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(group_commands, scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(private_commands, scope=BotCommandScopeDefault())
