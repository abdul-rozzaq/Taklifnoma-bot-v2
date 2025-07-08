class TranslationService:
    UZ = "uz"
    RU = "ru"

    TEXTS = {
        UZ: {
            "welcome": "🎉 Taqdirlash marosimi botiga xush kelibsiz!",
            "select_language": "Iltimos, tilni tanlang:",
            "share_contact": "📞 Kontaktni ulashish",
            "registration_menu": "Ro'yhatdan o'tish",
            "tutors_menu": "Tutorlar bo'limi",
            "main_menu": "📋 Asosiy menyu:",
            "language_selected": "Til muvaffaqqiyatli o'rnatildi",
            "enter_name": "📝 Ism va familiyangizni kiriting:",
            "error": "❌ Xatolik yuz berdi. Qayta urinib ko'ring.",
            "enter_phone": "📱 Telefon raqamingizni yuboring:",
            "enter_passport": "📄 Passport seriyasi va raqamini kiriting:\n(masalan: AB1234567)",
            "name_too_short": "❌ Ism juda qisqa. Kamida 5 ta belgi kiriting.",
            "already_registered": "✅ Siz allaqachon ro'yhatdan o'tgansiz!",
            "passport_exists": "❌ Ushbu passport raqami bilan allaqachon ro'yhatdan o'tilgan!",
            "registration_success": "✅ Ro'yhatdan o'tish muvaffaqqiyatli yakunlandi!",
            "invalid_passport": "❌ Passport raqami noto'g'ri formatda. Iltimos, qayta kiriting.",
            "invalid_phone": "❌ Telefon raqami noto'g'ri. Iltimos, qayta kiriting.",
            "admin_panel": "🔧 Admin panel",
            "back_to_menu": "🔙 Asosiy menyuga qaytish",
            "no_tutors": "❌ Sizga hech qanday tutor biriktirilmagan.",
            "your_tutors": "👨‍🏫 Sizning tutorlaringiz:",
            # UZ bo'limiga qo'shish
            "registration_required": "❌ Avval ro'yhatdan o'tishingiz kerak!",
            "phone_format_example": "Masalan: +998901234567",
            "passport_format_example": "Masalan: AB1234567 yoki AA1234567",
            "continue_registration": "📝 Ro'yhatdan o'tishni davom ettirish",
            "cancel_registration": "❌ Bekor qilish",
            "registration_cancelled": "❌ Ro'yhatdan o'tish bekor qilindi",
            "choose_action": "Harakatni tanlang:",
        },
        RU: {
            "welcome": "🎉 Добро пожаловать в бот церемонии награждения!",
            "select_language": "Пожалуйста, выберите язык:",
            "share_contact": "📞 Поделиться контактом",
            "registration_menu": "Регистрация",
            "tutors_menu": "Раздел наставников",
            "main_menu": "📋 Главное меню:",
            "language_selected": "Язык успешно установлен",
            "enter_name": "📝 Введите ваше имя и фамилию:",
            "error": "❌ Произошла ошибка. Попробуйте еще раз.",
            "enter_phone": "📱 Отправьте ваш номер телефона:",
            "enter_passport": "📄 Введите серию и номер паспорта:\n(например: AB1234567)",
            "name_too_short": "❌ Имя слишком короткое. Введите минимум 5 символов.",
            "already_registered": "✅ Вы уже зарегистрированы!",
            "passport_exists": "❌ С этим номером паспорта уже зарегистрированы!",
            "registration_success": "✅ Регистрация успешно завершена!",
            "invalid_passport": "❌ Неверный формат номера паспорта. Пожалуйста, введите еще раз.",
            "invalid_phone": "❌ Неверный номер телефона. Пожалуйста, введите еще раз.",
            "admin_panel": "🔧 Панель администратора",
            "back_to_menu": "🔙 Вернуться в главное меню",
            "no_tutors": "❌ Вам не назначены наставники.",
            "your_tutors": "👨‍🏫 Ваши наставники:",
            # RU bo'limiga qo'shish
            "registration_required": "❌ Сначала необходимо зарегистрироваться!",
            "phone_format_example": "Например: +998901234567",
            "passport_format_example": "Например: AB1234567 или AA1234567",
            "continue_registration": "📝 Продолжить регистрацию",
            "cancel_registration": "❌ Отмена",
            "registration_cancelled": "❌ Регистрация отменена",
            "choose_action": "Выберите действие:",
        },
    }

    def get_text(self, text: str, lang: str = "uz") -> str:
        return self.TEXTS.get(lang, self.TEXTS[self.UZ]).get(text, text)


translation = TranslationService()
