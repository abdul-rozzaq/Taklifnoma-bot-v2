from django.conf import settings

from aiogram import Bot, Dispatcher, types


from motor.motor_asyncio import AsyncIOMotorClient

from bot.handlers.user import router as user_router
from bot.handlers.admin import router as admin_router
from bot.services.service import BotService


client = AsyncIOMotorClient(settings.MONGODB_URL)

webhook_dp = Dispatcher()

webhook_dp["service"] = BotService()

webhook_dp.include_router(router=user_router)
webhook_dp.include_router(router=admin_router)


async def feed_update(update: dict):
    try:
        aiogram_update = types.Update(**update)
        webhook_bot = Bot(token=settings.BOT_TOKEN)
        await webhook_dp.feed_update(bot=webhook_bot, update=aiogram_update)

    except Exception as e:
        print(e)

    finally:
        await webhook_bot.session.close()
