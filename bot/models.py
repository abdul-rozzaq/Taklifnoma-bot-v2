from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BotUser(BaseModel):
    ROLE_CHOICES = [
        ("user", "Foydalanuvchi"),
        ("mentor", "Mentor"),
        ("admin", "Admin"),
    ]

    LANGUAGE_CHOICES = [
        ("uz", "O'zbekcha"),
        ("ru", "Русский"),
    ]

    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    passport = models.CharField(max_length=20, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="uz")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"

    class Meta:
        verbose_name = "Bot foydalanuvchisi"
        verbose_name_plural = "Bot foydalanuvchilari"


class Event(BaseModel):
    invitation_photo = models.ImageField(upload_to="invitation-photos/", null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4090)
    start_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name="created_events")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tadbir"
        verbose_name_plural = "Tadbirlar"


class Achievement(BaseModel):
    owner = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to="achievement-files/")

    def __str__(self):
        return self.title


class InvitationStatus(models.TextChoices):
    PENDING = ("pending", "Pending")
    ACCPTED = ("accepted", "Accepted")
    DECLINED = ("declined", "Declined")


class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=InvitationStatus.choices, default=InvitationStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")
