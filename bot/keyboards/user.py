from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from bot.services.translation import translation


def get_language_keyboard():
    """Til tanlash klaviaturasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            ],
        ],
    )


def get_contact_keyboard(lang: str = "uz"):
    """Kontakt ulashish klaviaturasi"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=translation.get_text("share_contact", lang), request_contact=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_main_menu_keyboard(lang: str = "uz", is_admin: bool = False):
    """Asosiy menyu klaviaturasi"""
    buttons = [
        [
            KeyboardButton(text=translation.get_text("registration_menu", lang)),
            KeyboardButton(text=translation.get_text("tutors_menu", lang)),
        ],
    ]

    if is_admin:
        buttons.append([KeyboardButton(text=translation.get_text("admin_panel", lang))])

    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_back_to_menu_keyboard(lang: str = "uz"):
    """Asosiy menyuga qaytish klaviaturasi"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=translation.get_text("back_to_menu", lang))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
