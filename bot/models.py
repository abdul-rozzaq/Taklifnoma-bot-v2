from django.db import models


class BotUser(models.Model):
    ROLE_CHOICES = [
        ("user", "Foydalanuvchi"),
        ("mentor", "Mentor"),
        ("admin", "Admin"),
    ]

    LANGUAGE_CHOICES = [
        ("uz", "O'zbekcha"),
        ("ru", "Русский"),
    ]

    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    passport = models.CharField(max_length=20, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="uz")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    is_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"

    class Meta:
        verbose_name = "Bot foydalanuvchisi"
        verbose_name_plural = "Bot foydalanuvchilari"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    max_participants = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name="created_events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tadbir"
        verbose_name_plural = "Tadbirlar"


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name="event_registrations")
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.event.title}"

    class Meta:
        unique_together = ["event", "user"]
        verbose_name = "Tadbir ro'yhatdan o'tish"
        verbose_name_plural = "Tadbir ro'yhatdan o'tishlar"


class UserMentor(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name="mentors")
    mentor = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name="users")
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.mentor.name}"

    class Meta:
        unique_together = ["user", "mentor"]
        verbose_name = "Foydalanuvchi mentor"
        verbose_name_plural = "Foydalanuvchi mentorlar"
