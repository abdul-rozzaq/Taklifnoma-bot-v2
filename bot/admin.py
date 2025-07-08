from django.contrib import admin
from .models import BotUser, Event, EventRegistration, UserMentor


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ["full_name", "telegram_id", "phone", "passport", "language", "role", "is_registered", "created_at"]
    list_filter = ["language", "role", "is_registered", "created_at"]
    search_fields = ["full_name", "passport", "phone", "telegram_id"]
    list_editable = ["role", "is_registered"]
    readonly_fields = ["telegram_id", "created_at", "updated_at"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date", "location", "max_participants", "is_active", "created_by", "created_at"]
    list_filter = ["is_active", "start_date", "created_at"]
    search_fields = ["title", "description", "location"]
    list_editable = ["is_active"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "start_date"


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ["event", "user", "registered_at"]
    list_filter = ["event", "registered_at"]
    search_fields = ["event__title", "user__full_name"]
    readonly_fields = ["registered_at"]


# @admin.register(Mentor)
# class MentorAdmin(admin.ModelAdmin):
#     list_display = ["name", "phone", "email", "is_active", "created_at"]
#     list_filter = ["is_active", "created_at"]
#     search_fields = ["name", "phone", "email"]
#     list_editable = ["is_active"]
#     readonly_fields = ["created_at"]


@admin.register(UserMentor)
class UserMentorAdmin(admin.ModelAdmin):
    list_display = ["user", "mentor", "assigned_at"]
    list_filter = ["mentor", "assigned_at"]
    search_fields = ["user__full_name", "mentor__name"]
    readonly_fields = ["assigned_at"]
