import re

from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.filters.text import TextFilter
from bot.keyboards.user import get_achievements_keyboard, get_contact_keyboard, get_language_keyboard, get_main_menu_keyboard
from bot.models import Achievement
from bot.services.translation import TranslationService
from bot.services.service import BotService
from bot.states.achievements import AchievementState
from bot.states.registration import RegistrationState

router = Router()


@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    """Start komandasi"""

    msg_user = message.from_user
    user = await BotService.get_or_create_user(user_id=msg_user.id, first_name=msg_user.first_name, username=msg_user.username)

    await message.answer(TranslationService.get_text("welcome", lang=user.language), reply_markup=ReplyKeyboardRemove())
    await state.clear()

    await message.answer(TranslationService.get_text("select_language", lang=user.language), reply_markup=get_language_keyboard())


@router.message(TextFilter(TranslationService.get_text("back_to_menu", "all")))
async def handle_back_to_menu(message: Message, state: FSMContext):
    """Asosiy menyuga qaytish"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)
    is_admin = await BotService.is_admin(msg_user.id)

    await state.clear()
    await message.answer(TranslationService.get_text("main_menu", lang=lang), reply_markup=get_main_menu_keyboard(lang, is_admin))


@router.callback_query(lambda c: c.data.startswith("lang_"))
async def handle_language_callback(callback: CallbackQuery, state: FSMContext):
    """Til tanlash callback"""

    user = callback.from_user
    lang = callback.data.split("_")[1]

    user_obj = await BotService.get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )
    user_obj.language = lang
    await user_obj.asave()

    is_admin = await BotService.is_admin(user.id)

    await callback.message.edit_text(TranslationService.get_text("language_selected", lang))
    await callback.message.answer(
        TranslationService.get_text("main_menu", lang=user_obj.language),
        reply_markup=get_main_menu_keyboard(user_obj.language, is_admin),
    )


@router.message(RegistrationState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Ism qayta ishlash"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)
    name = message.text.strip()

    if len(name) < 5:
        await message.answer(TranslationService.get_text("name_too_short", lang=lang))
        return

    user = await BotService.get_or_create_user(user_id=msg_user.id)
    user.full_name = name
    await user.asave()

    await state.update_data(full_name=name)
    await message.answer(TranslationService.get_text("enter_phone", lang), reply_markup=get_contact_keyboard(lang))
    await state.set_state(RegistrationState.waiting_for_phone)


@router.message(RegistrationState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Telefon raqami qayta ishlash"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)

    phone = None

    # Agar kontakt yuborilgan bo'lsa
    if message.contact:
        phone = message.contact.phone_number
    # Agar matn shaklida yuborilgan bo'lsa
    elif message.text:
        phone_text = message.text.strip()
        # Telefon raqami formatini tekshirish
        phone_pattern = r"^[\+]?[0-9]{9,15}$"
        if re.match(phone_pattern, phone_text.replace(" ", "").replace("-", "")):
            phone = phone_text

    if not phone:
        await message.answer(TranslationService.get_text("invalid_phone", lang=lang))
        return

    await state.update_data(phone=phone)
    await message.answer(TranslationService.get_text("enter_passport", lang), reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.waiting_for_passport)


@router.message(RegistrationState.waiting_for_passport)
async def process_passport(message: Message, state: FSMContext):
    """Passport raqami qayta ishlash"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)
    passport = message.text.strip().upper()

    # Passport formatini tekshirish (masalan: AB1234567)
    passport_pattern = r"^[A-Z]{2}[0-9]{7}$"
    if not re.match(passport_pattern, passport):
        await message.answer(TranslationService.get_text("invalid_passport", lang=lang))
        return

    # Passport mavjudligini tekshirish
    if await BotService.check_passport_exists(passport):
        await message.answer(TranslationService.get_text("passport_exists", lang=lang))
        await state.clear()
        return

    # Ma'lumotlarni olish
    state_data = await state.get_data()
    full_name = state_data.get("full_name")
    phone = state_data.get("phone")

    # Foydalanuvchini ro'yhatga olish
    success = await BotService.register_user(msg_user.id, full_name, phone, passport)

    if success:
        await message.answer(TranslationService.get_text("registration_success", lang=lang))
        is_admin = await BotService.is_admin(msg_user.id)
        await message.answer(TranslationService.get_text("main_menu", lang=lang), reply_markup=get_main_menu_keyboard(lang, is_admin))
    else:
        await message.answer(TranslationService.get_text("error", lang=lang))

    await state.clear()


@router.message(TextFilter(TranslationService.get_text("registration_menu", "all")))
async def handle_registration_menu(message: Message, state: FSMContext):
    """Ro'yhatdan o'tish menyusi"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)

    # Foydalanuvchi ro'yhatdan o'tganligini tekshirish
    if await BotService.check_user_registered(msg_user.id):
        await message.answer(TranslationService.get_text("already_registered", lang=lang))
        return

    # Ro'yhatdan o'tish jarayonini boshlash
    await message.answer(TranslationService.get_text("enter_name", lang))
    await state.set_state(RegistrationState.waiting_for_name)


@router.message(TextFilter(TranslationService.get_text("achievements_menu", "all")))
async def handle_achievements_menu(message: Message, state: FSMContext):
    """Yutuqlarim bo'limi"""
    await state.set_state(AchievementState.waiting_for_achievement)

    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)

    achievements = await BotService.get_user_achievements(msg_user.id)

    if achievements:
        await message.answer("Sertifikatlardan birini tanlang: ", reply_markup=get_achievements_keyboard(achievements))
    else:
        await message.answer(TranslationService.get_text("no_achievement", lang=lang))


@router.message(AchievementState.waiting_for_achievement)
async def handle_achievement_name(message: Message, service: BotService, state: FSMContext):
    title = message.text
    achievement: Optional[Achievement] = await service.get_achievement(title)

    if not achievement:
        await message.answer("Yutuq topilmadi")
        return

    # Faylni to'g'ri formatga o'tkazish
    file_path = achievement.file.path if hasattr(achievement.file, "path") else achievement.file

    # Chiroyli caption tuzish
    caption = f"🏆 <b>{achievement.title}</b>\n" f"📅 {achievement.created_at.strftime('%d.%m.%Y')}\n" f"\n{achievement.description}"

    await message.answer_document(FSInputFile(file_path), caption=caption, parse_mode="HTML")


@router.message(TextFilter(TranslationService.get_text("my_invitations", "all")))
async def handle_my_invitations(message: Message, state: FSMContext, service: BotService):
    lang = await BotService.get_user_language(message.from_user.id)
    invitations = await service.get_user_invitations(message.from_user.id)
    if not invitations:
        await message.answer(TranslationService.get_text("no_invitations", lang), reply_markup=get_main_menu_keyboard(lang))
        return
    text = TranslationService.get_text("your_invitations", lang) + "\n"
    for inv in invitations:
        text += f"• {inv.event.title} | {inv.code}\n"
    await message.answer(text, reply_markup=get_main_menu_keyboard(lang))
