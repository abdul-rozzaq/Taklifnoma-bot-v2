import asyncio

from django.conf import settings

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode


from bot.keyboards.user import get_invitation_buttons
from bot.models import Event, Invitation
from bot.services.translation import TranslationService
from bot.utils import chunked


class TelegramService:
    _instance = None
    _bot = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_bot(self):
        if self._bot is None:
            session = AiohttpSession()
            self._bot = Bot(token=settings.BOT_TOKEN, session=session)

        return self._bot

    async def close(self):
        if self._bot:
            await self._bot.session.close()
            self._bot = None

    async def send_invitation(self, invitation: Invitation):
        event: Event = invitation.event

        message = TranslationService.get_text(
            "invitation_text",
            lang=invitation.user.language,
            title=event.title,
            description=event.description % invitation.user.__dict__,
            start_date=event.start_date.strftime("%d.%m.%Y %H:%M"),
            location=event.location,
        )

        bot = await self.get_bot()

        try:
            if event.invitation_photo:
                await bot.send_photo(
                    chat_id=invitation.user.telegram_id,
                    photo=FSInputFile(event.invitation_photo.path) if event.invitation_photo else None,
                    caption=message,
                    reply_markup=get_invitation_buttons(invitation_id=invitation.id),
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                await bot.send_message(
                    chat_id=invitation.user.telegram_id,
                    text=message,
                    reply_markup=get_invitation_buttons(invitation_id=invitation.id),
                    parse_mode=ParseMode.MARKDOWN,
                )

            return True
        except Exception as e:
            err_message = f"Xato - User {invitation.user.telegram_id}: {e}"
            print(err_message)
            return False

    async def send_multiple_invitations(self, invitations, batch_size=15):
        success_count = 0
        failed_count = 0

        try:
            for chunk in chunked(invitations, batch_size):
                results = await asyncio.gather(*[self.send_invitation(inv) for inv in chunk], return_exceptions=True)
                success_count += sum(1 for r in results if r is True)
                failed_count += sum(1 for r in results if r is False or isinstance(r, Exception))

                print("process")
                await asyncio.sleep(1)
        finally:
            await self.close()

        return success_count, failed_count
