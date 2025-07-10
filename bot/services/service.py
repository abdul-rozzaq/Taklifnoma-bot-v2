from django.conf import settings

from typing import Optional

from bot.models import Achievement, BotUser, Invitation

from asgiref.sync import sync_to_async


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
    async def add_admin(telegram_id: int):
        try:
            user = await BotUser.objects.aget(telegram_id=telegram_id)
            user.role = "admin"
            await user.asave()

            return user

        except BotUser.DoesNotExist:
            return None

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

    @staticmethod
    @sync_to_async
    def get_user_achievements(user_id: int):
        achievements = Achievement.objects.filter(owner__telegram_id=user_id).values("pk", "title", "description", "file")
        return list(achievements)

    @staticmethod
    async def get_achievement(title: str):
        try:
            achievement = await Achievement.objects.aget(title=title)
            return achievement
        except Achievement.DoesNotExist:
            return None

    @staticmethod
    async def find_user(telegram_id: int):
        try:
            user = await BotUser.objects.aget(telegram_id=telegram_id)

            return user
        except BotUser.DoesNotExist:
            return None

    @staticmethod
    async def get_user_invitations(telegram_id):
        user = await BotUser.objects.filter(telegram_id=telegram_id).afirst()
        if not user:
            return []
        return await Invitation.objects.filter(owner=user).all()
