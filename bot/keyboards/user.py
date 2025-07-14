from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from bot.services.translation import TranslationService


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
            [KeyboardButton(text=TranslationService.get_text("share_contact", lang), request_contact=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_main_menu_keyboard(lang: str = "uz", is_admin: bool = False):
    """Asosiy menyu klaviaturasi"""
    buttons = [
        [
            KeyboardButton(text=TranslationService.get_text("my_invitations", lang)),
            KeyboardButton(text=TranslationService.get_text("achievements_menu", lang)),
        ],
    ]

    if is_admin:
        buttons.append([KeyboardButton(text=TranslationService.get_text("admin_panel", lang))])

    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_back_to_menu_keyboard(lang: str = "uz"):
    """Asosiy menyuga qaytish klaviaturasi"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TranslationService.get_text("back_to_menu", lang))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_achievements_keyboard(achievements: list, lang: str = "uz"):
    """Achievementlar uchun klaviatura"""

    keyboards = [[KeyboardButton(text=achievement["title"])] for achievement in achievements]

    keyboards.insert(0, [KeyboardButton(text=TranslationService.get_text("back_to_menu", lang=lang))])

    return ReplyKeyboardMarkup(
        keyboard=keyboards,
        resize_keyboard=True,
        selective=True,
    )


def get_invitation_buttons(invitation_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Qatnashaman", callback_data=f"accept_{invitation_id}"),
                InlineKeyboardButton(text="❌ Qatnashmayman", callback_data=f"decline_{invitation_id}"),
            ]
        ]
    )
