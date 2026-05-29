from aiogram import Router

from handlers import admin, answers, game, profiles, top

router = Router()
router.include_router(game.router)
router.include_router(profiles.router)
router.include_router(top.router)
router.include_router(admin.router)
router.include_router(answers.router)
