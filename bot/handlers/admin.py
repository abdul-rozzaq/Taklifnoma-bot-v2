from typing import Optional
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import MessageOriginType, ParseMode
from aiogram.filters import StateFilter

from bot.keyboards.admin import get_admin_buttons, get_confirmation_buttons
from bot.keyboards.user import get_back_to_menu_keyboard
from bot.models import BotUser
from bot.services.translation import TranslationService
from bot.filters.text import TextFilter
from bot.services.service import BotService
from bot.states.add_admin import AddAdminState

router = Router()


@router.message(TextFilter(TranslationService.get_text("admin_panel", "all")))
async def handle_admin_panel(message: Message, state: FSMContext):
    await state.clear()

    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)

    if not await BotService.is_admin(msg_user.id):
        await message.answer(TranslationService.get_text("error", lang=lang))
        return

    await message.answer(TranslationService.get_text("admin_panel_title", lang), reply_markup=get_admin_buttons(lang))


@router.message(TextFilter(TranslationService.get_text("add_admin", "all")))
async def handle_add_admin(message: Message, state: FSMContext):
    lang = await BotService.get_user_language(message.from_user.id)
    await message.answer(TranslationService.get_text("enter_admin_id", lang), reply_markup=get_back_to_menu_keyboard())
    await state.set_state(AddAdminState.waiting_for_forward_message)


@router.message(AddAdminState.waiting_for_forward_message)
async def handle_add_admin_forward_message(message: Message, state: FSMContext, service: BotService):
    telegram_id = message.text
    lang = await BotService.get_user_language(message.from_user.id)

    if message.forward_origin:
        forward_origin = message.forward_origin

        if forward_origin.type == MessageOriginType.USER:
            forward_user = forward_origin.sender_user
            telegram_id = forward_user.id

        elif forward_origin.type == MessageOriginType.HIDDEN_USER:
            user_name = forward_origin.sender_user_name
            await message.answer(f"Foydalanuvchi *{user_name}* habar uzatishni o'chirib qo'ygan. Iltimos Telegram ID yuboring.", parse_mode=ParseMode.MARKDOWN_V2)
            return

    if not str(telegram_id).isdigit():
        await message.answer(TranslationService.get_text("invalid_telegram_id", lang))
        return

    telegram_id = int(telegram_id)
    user: Optional[BotUser] = await service.find_user(telegram_id)

    if not user:
        await message.answer(TranslationService.get_text("user_not_found", lang))
        return

    user_info = TranslationService.get_text(
        "user_info",
        lang,
        id=user.pk,
        telegram_id=user.telegram_id,
        full_name=user.full_name or "",
        phone=user.phone if hasattr(user, "phone") else "yo‘q",
        language=user.get_language_display(),
        role=user.get_role_display(),
    )
    await message.answer(user_info, parse_mode=ParseMode.MARKDOWN)

    await state.update_data(admin_id=telegram_id)
    await message.answer(
        TranslationService.get_text("admin_id_accepted", lang, telegram_id=telegram_id),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_confirmation_buttons(lang),
    )
    await state.set_state(AddAdminState.waiting_for_confirmation)


@router.message(StateFilter(AddAdminState.waiting_for_confirmation), TextFilter(TranslationService.get_text("admin_confirm", "all")))
async def handle_admin_confirm(message: Message, state: FSMContext, service: BotService):
    data = await state.get_data()
    admin_id = data.get("admin_id")
    lang = await BotService.get_user_language(message.from_user.id)

    if admin_id:
        await service.add_admin(admin_id)
        await message.answer(TranslationService.get_text("admin_added", lang), reply_markup=get_admin_buttons(lang))
    else:
        await message.answer(TranslationService.get_text("error", lang))

    await state.clear()


@router.message(StateFilter(AddAdminState.waiting_for_confirmation), TextFilter(TranslationService.get_text("admin_cancel", "all")))
async def handle_admin_cancel(message: Message, state: FSMContext):
    lang = await BotService.get_user_language(message.from_user.id)
    await message.answer(TranslationService.get_text("admin_cancelled", lang), reply_markup=get_admin_buttons(lang))
    await state.clear()
