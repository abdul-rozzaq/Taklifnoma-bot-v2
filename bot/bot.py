from django.conf import settings

from aiogram import Bot, Dispatcher, types

from bot.handlers.user import router
from bot.services.service import BotService


webhook_dp = Dispatcher()
webhook_dp["service"] = BotService()

webhook_dp.include_router(router=router)


async def feed_update(update: dict):
    try:
        aiogram_update = types.Update(**update)
        webhook_bot = Bot(token=settings.BOT_TOKEN)
        await webhook_dp.feed_update(bot=webhook_bot, update=aiogram_update)

    finally:
        await webhook_bot.session.close()
