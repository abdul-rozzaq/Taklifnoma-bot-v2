class TranslationService:
    UZ = "uz"
    RU = "ru"

    TEXTS = {
        UZ: {
            "welcome": "🎉 Taqdirlash marosimi botiga xush kelibsiz!",
            "select_language": "Iltimos, tilni tanlang:",
            "share_contact": "📞 Kontaktni ulashish",
            "registration_menu": "📲 Ro'yhatdan o'tish",
            "achievements_menu": "🏆 Yutuqlarim",
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
            "admin_panel": "⚙️ Admin panel",
            "admin_panel_title": "🔧 Admin panel (tez orada qo'shiladi)",
            "invalid_telegram_id": "Noto'g'ri Telegram ID. Iltimos, raqamli ID yuboring.",
            "user_not_found": "Bunday foydalanuvchi topilmadi.",
            "admin_id_accepted": "Foydalanuvchi ID: `{telegram_id}` to'g'ri qabul qilindi. Davom etish uchun tasdiqlang.",
            "user_info": "👤 *Foydalanuvchi ma'lumotlari:*\nID: `{id}`\nTelegram ID: `{telegram_id}`\nIsm: *{full_name}*\nTelefon: `{phone}`\nTil: *{language}*\nRol: *{role}*\n",
            "back_to_menu": "🔙 Asosiy menyuga qaytish",
            "no_tutors": "❌ Sizga hech qanday tutor biriktirilmagan.",
            "your_tutors": "👨‍🏫 Sizning tutorlaringiz:",
            "registration_required": "❌ Avval ro'yhatdan o'tishingiz kerak!",
            "phone_format_example": "Masalan: +998901234567",
            "passport_format_example": "Masalan: AB1234567 yoki AA1234567",
            "continue_registration": "📝 Ro'yhatdan o'tishni davom ettirish",
            "registration_cancelled": "❌ Ro'yhatdan o'tish bekor qilindi",
            "choose_action": "Harakatni tanlang:",
            "no_achievement": "Sizda hali yutuqlar mavjud emas.",
            "upload_certificate": "📤 Sertifikat yuklash",
            "add_admin": "➕ Admin qo'shish",
            "statistics": "📊 Statistika",
            "enter_admin_id": "🆔 Yangi admin ID sini kiriting yoki undan habarni forward qiling:",
            "admin_confirm": "✅ Tasdiqlash",
            "admin_cancel": "❌ Bekor qilish",
            "admin_cancelled": "❌ Jarayon bekor qilindi",
            "my_invitations": "🎟 Mening taklifnomalarim",
            "no_invitations": "Sizda taklifnomalar yo‘q.",
            "your_invitations": "Sizning taklifnomalaringiz:",
            # no russian translation
            "invitation_text": "🎉 *Yangi event taklifnomasi!*\n\n📋 *{title}*\n📝 {description}\n📅 *Sana:* {start_date}\n📍 *Manzil:* {location}\n\nIltimos, javobingizni tanlang:",
            "invitation_accept": "✅ *Ajoyib!*\n\nSiz '*{title}*' eventiga qatnashishga rozilik bildirdingiz!\n\n📅 *Sana:* {start_date}\n📍 *Manzil:* {location}\n\nEvent vaqti yaqinlashganda sizga eslatma yuboramiz! 🔔",
            "invitation_declined": "❌ *Afsuski!*\n\nSiz '*{title}*' eventiga qatnashishdan bosh tortdingiz.\n\nKeyingi eventlarda ko'rishguncha! 👋",
        },
        RU: {
            "welcome": "🎉 Добро пожаловать в бот церемонии награждения!",
            "select_language": "Пожалуйста, выберите язык:",
            "share_contact": "📞 Поделиться контактом",
            "registration_menu": "📲 Регистрация",
            "achievements_menu": "🏆 Мои достижения",
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
            "admin_panel": "⚙️ Панель администратора",
            "admin_panel_title": "🔧 Панель администратора (скоро будет добавлено)",
            "invalid_telegram_id": "Неверный Telegram ID. Пожалуйста, введите числовой ID.",
            "user_not_found": "Пользователь с таким ID не найден.",
            "admin_id_accepted": "ID пользователя: `{telegram_id}` успешно принят. Для продолжения подтвердите.",
            "user_info": "👤 *Информация о пользователе:*\nID: `{id}`\nTelegram ID: `{telegram_id}`\nИмя: *{full_name}*\nТелефон: `{phone}`\nЯзык: *{language}*\nРоль: *{role}*\n",
            "back_to_menu": "🔙 Вернуться в главное меню",
            "no_tutors": "❌ Вам не назначены наставники.",
            "your_tutors": "👨‍🏫 Ваши наставники:",
            "registration_required": "❌ Сначала необходимо зарегистрироваться!",
            "phone_format_example": "Например: +998901234567",
            "passport_format_example": "Например: AB1234567 или AA1234567",
            "continue_registration": "📝 Продолжить регистрацию",
            "registration_cancelled": "❌ Регистрация отменена",
            "choose_action": "Выберите действие:",
            "no_achievement": "У вас пока нет достижений.",
            "upload_certificate": "📤 Загрузить сертификат",
            "add_admin": "➕ Добавить администратора",
            "statistics": "📊 Статистика",
            "enter_admin_id": "🆔 Введите ID нового администратора или перешлите его сообщение:",
            "my_invitations": "🎟 Мои приглашения",
            "no_invitations": "У вас нет приглашений.",
            "your_invitations": "Ваши приглашения:",
        },
    }

    @classmethod
    def get_text(cls, text: str, lang: str = "uz", **kwargs) -> str:
        if lang == "all":
            return [cls.get_text(text, lng, **kwargs) for lng in list(cls.TEXTS.keys())]

        value = cls.TEXTS.get(lang, cls.TEXTS[cls.UZ]).get(text, text)
        if kwargs:
            try:
                return value.format(**kwargs)
            except Exception as e:
                print(e)
                return value
        return value
