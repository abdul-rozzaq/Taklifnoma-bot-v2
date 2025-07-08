from django.conf import settings
from typing import Optional
from bot.models import BotUser


class BotService:
    @staticmethod
    async def get_or_create_user(user_id: int, username: Optional[str] = None, first_name: Optional[str] = None) -> BotUser:
        """Foydalanuvchini olish yoki yaratish"""
        user, created = await BotUser.objects.aget_or_create(
            telegram_id=user_id,
            defaults={
                "full_name": first_name or username or f"User_{user_id}",
                "language": "uz",
            },
        )
        return user

    @staticmethod
    async def is_admin(user_id: int) -> bool:
        """Admin ekanligini tekshirish"""
        if user_id in settings.ADMIN_IDS:
            return True
        try:
            user = await BotUser.objects.aget(telegram_id=user_id)
            return user.role == "admin"
        except BotUser.DoesNotExist:
            return False

    @staticmethod
    async def get_user_language(user_id: int) -> str:
        """Foydalanuvchi tilini olish"""
        try:
            user = await BotUser.objects.aget(telegram_id=user_id)
            return user.language
        except BotUser.DoesNotExist:
            return "uz"

    @staticmethod
    async def check_user_registered(user_id: int) -> bool:
        """Foydalanuvchi ro'yhatdan o'tganligini tekshirish"""
        try:
            user = await BotUser.objects.aget(telegram_id=user_id)
            return user.is_registered
        except BotUser.DoesNotExist:
            return False

    @staticmethod
    async def check_passport_exists(passport: str) -> bool:
        """Passport raqami mavjudligini tekshirish"""
        try:
            await BotUser.objects.aget(passport=passport)
            return True
        except BotUser.DoesNotExist:
            return False

    @staticmethod
    async def register_user(user_id: int, full_name: str, phone: str, passport: str) -> bool:
        """Foydalanuvchini ro'yhatdan o'tkazish"""
        try:
            user = await BotUser.objects.aget(telegram_id=user_id)
            user.full_name = full_name
            user.phone = phone
            user.passport = passport
            user.is_registered = True
            await user.asave()
            return True
        except BotUser.DoesNotExist:
            return False
