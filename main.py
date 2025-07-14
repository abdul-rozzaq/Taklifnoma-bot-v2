import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from bot.models import BotUser, Event

event = Event.objects.first()
user = BotUser.objects.first()


text = "Salom %(full_name)s, Pasport %(passport)s"


print(text % user.__dict__)
