from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.services.translation import TranslationService


def get_admin_buttons(lang="uz") -> ReplyKeyboardMarkup:
    keyboards = [
        [KeyboardButton(text=TranslationService.get_text("upload_certificate", lang))],
        [
            KeyboardButton(text=TranslationService.get_text("add_admin", lang)),
            KeyboardButton(text=TranslationService.get_text("statistics", lang)),
        ],
        [KeyboardButton(text=TranslationService.get_text("back_to_menu", lang))],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboards,
        resize_keyboard=True,
    )


def get_admin_cancel_button(lang="uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TranslationService.get_text("admin_cancel", lang=lang))],
        ]
    )


def get_confirmation_buttons(lang="uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=TranslationService.get_text("admin_confirm", lang=lang)),
                KeyboardButton(text=TranslationService.get_text("admin_cancel", lang=lang)),
            ]
        ],
        resize_keyboard=True,
    )
