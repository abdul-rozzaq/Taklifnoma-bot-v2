import re
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards.user import get_contact_keyboard, get_language_keyboard, get_main_menu_keyboard
from bot.services.translation import translation
from bot.services.service import BotService
from bot.states.registration import RegistrationState
from bot.models import BotUser

router = Router()


@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    """Start komandasi"""

    msg_user = message.from_user
    user = await BotService.get_or_create_user(user_id=msg_user.id, first_name=msg_user.first_name, username=msg_user.username)

    await message.answer(translation.get_text("welcome", lang=user.language), reply_markup=ReplyKeyboardRemove())
    await state.clear()

    await message.answer(translation.get_text("select_language", lang=user.language), reply_markup=get_language_keyboard())


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

    await callback.message.edit_text(translation.get_text("language_selected", lang))
    await callback.message.answer(
        translation.get_text("main_menu", lang=user_obj.language),
        reply_markup=get_main_menu_keyboard(user_obj.language, is_admin),
    )


@router.message(RegistrationState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Ism qayta ishlash"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)
    name = message.text.strip()

    if len(name) < 5:
        await message.answer(translation.get_text("name_too_short", lang=lang))
        return

    user = await BotService.get_or_create_user(user_id=msg_user.id)
    user.full_name = name
    await user.asave()

    await state.update_data(full_name=name)
    await message.answer(translation.get_text("enter_phone", lang), reply_markup=get_contact_keyboard(lang))
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
        await message.answer(translation.get_text("invalid_phone", lang=lang))
        return

    await state.update_data(phone=phone)
    await message.answer(translation.get_text("enter_passport", lang), reply_markup=ReplyKeyboardRemove())
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
        await message.answer(translation.get_text("invalid_passport", lang=lang))
        return

    # Passport mavjudligini tekshirish
    if await BotService.check_passport_exists(passport):
        await message.answer(translation.get_text("passport_exists", lang=lang))
        await state.clear()
        return

    # Ma'lumotlarni olish
    state_data = await state.get_data()
    full_name = state_data.get("full_name")
    phone = state_data.get("phone")

    # Foydalanuvchini ro'yhatga olish
    success = await BotService.register_user(msg_user.id, full_name, phone, passport)

    if success:
        await message.answer(translation.get_text("registration_success", lang=lang))
        is_admin = await BotService.is_admin(msg_user.id)
        await message.answer(translation.get_text("main_menu", lang=lang), reply_markup=get_main_menu_keyboard(lang, is_admin))
    else:
        await message.answer(translation.get_text("error", lang=lang))

    await state.clear()


@router.message(lambda message: message.text and translation.get_text("registration_menu", "uz") in message.text or translation.get_text("registration_menu", "ru") in message.text)
async def handle_registration_menu(message: Message, state: FSMContext):
    """Ro'yhatdan o'tish menyusi"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)

    # Foydalanuvchi ro'yhatdan o'tganligini tekshirish
    if await BotService.check_user_registered(msg_user.id):
        await message.answer(translation.get_text("already_registered", lang=lang))
        return

    # Ro'yhatdan o'tish jarayonini boshlash
    await message.answer(translation.get_text("enter_name", lang))
    await state.set_state(RegistrationState.waiting_for_name)


@router.message(lambda message: message.text and translation.get_text("admin_panel", "uz") in message.text or translation.get_text("admin_panel", "ru") in message.text)
async def handle_admin_panel(message: Message):
    """Admin panel"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)

    # Admin ekanligini tekshirish
    if not await BotService.is_admin(msg_user.id):
        await message.answer(translation.get_text("error", lang=lang))
        return

    # Admin panel funksiyalari bu yerda qo'shiladi
    await message.answer("🔧 Admin panel (tez orada qo'shiladi)")


@router.message(lambda message: message.text and translation.get_text("back_to_menu", "uz") in message.text or translation.get_text("back_to_menu", "ru") in message.text)
async def handle_back_to_menu(message: Message, state: FSMContext):
    """Asosiy menyuga qaytish"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)
    is_admin = await BotService.is_admin(msg_user.id)

    await state.clear()
    await message.answer(translation.get_text("main_menu", lang=lang), reply_markup=get_main_menu_keyboard(lang, is_admin))


@router.message(lambda message: message.text and translation.get_text("tutors_menu", "uz") in message.text or translation.get_text("tutors_menu", "ru") in message.text)
async def handle_tutors_menu(message: Message):
    """Tutorlar menyusi"""
    msg_user = message.from_user
    lang = await BotService.get_user_language(msg_user.id)

    # Foydalanuvchi ro'yhatdan o'tganligini tekshirish
    if not await BotService.check_user_registered(msg_user.id):
        await message.answer(translation.get_text("registration_required", lang=lang))
        return

    try:
        from bot.models import UserMentor

        # Foydalanuvchi objektini olish
        user = await BotUser.objects.aget(telegram_id=msg_user.id)

        # Foydalanuvchiga biriktirilgan mentorlarni olish
        mentors = []
        async for user_mentor in UserMentor.objects.filter(user=user).select_related("mentor"):
            if user_mentor.mentor.is_active:
                mentors.append(user_mentor.mentor)

        if not mentors:
            await message.answer(translation.get_text("no_tutors", lang=lang))
        else:
            response = translation.get_text("your_tutors", lang=lang) + "\n\n"
            for i, mentor in enumerate(mentors, 1):
                response += f"{i}. {mentor.name}\n"
                if mentor.description:
                    response += f"   📝 {mentor.description}\n"
                if mentor.phone:
                    response += f"   📞 {mentor.phone}\n"
                if mentor.email:
                    response += f"   📧 {mentor.email}\n"
                response += "\n"

            await message.answer(response)

    except Exception as e:
        print("Error", e)
        await message.answer(translation.get_text("error", lang=lang))
