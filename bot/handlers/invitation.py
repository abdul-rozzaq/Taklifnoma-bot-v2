# bot/handlers/invitations.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

from bot.models import Invitation, InvitationStatus
from bot.services.service import BotService
from bot.services.translation import TranslationService

router = Router()


@router.callback_query(F.data.startswith("accept_"))
async def accept_invitation(callback: CallbackQuery, service: BotService):
    lang = await service.get_user_language(callback.from_user.id)
    invitation_id = callback.data.split("_")[1]

    try:
        await service.set_invitation_status(invitation_id=invitation_id, status=InvitationStatus.ACCPTED)
        invitation = await service.get_invitation(invitation_id=invitation_id)

        if invitation:
            event = invitation.event

            await callback.message.edit_caption(
                caption=TranslationService.get_text(
                    "invitation_accept",
                    lang=lang,
                    title=event.title,
                    description=event.description,
                    start_date=event.start_date.strftime("%d.%m.%Y %H:%M"),
                    location=event.location,
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await callback.message.edit_caption(
                caption=TranslationService.get_text("error", lang=lang),
            )

    except Invitation.DoesNotExist:
        await callback.answer("❌ Taklifnoma topilmadi!", show_alert=True)


@router.callback_query(F.data.startswith("decline_"))
async def decline_invitation(callback: CallbackQuery, service: BotService):
    lang = await service.get_user_language(callback.from_user.id)
    invitation_id = callback.data.split("_")[1]

    try:
        await service.set_invitation_status(invitation_id, status=InvitationStatus.DECLINED)
        invitation = await service.get_invitation(invitation_id=invitation_id)

        if invitation is not None:
            await callback.message.edit_caption(
                caption=TranslationService.get_text("invitation_declined", lang=lang, title=invitation.event.title),
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await callback.message.edit_caption(
                caption=TranslationService.get_text("error", lang=lang),
            )

    except Invitation.DoesNotExist:
        await callback.answer("❌ Taklifnoma topilmadi!", show_alert=True)
