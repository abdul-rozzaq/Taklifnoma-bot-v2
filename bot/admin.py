from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.db import transaction
from django.contrib import admin

from bot.services.telegram import TelegramService

from .models import BotUser, Event, Achievement, Invitation

import asyncio


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "invitation_stats", "action_buttons")
    list_filter = ("created_at", "created_by")
    search_fields = ("title", "description")

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:object_id>/send-invitations/",
                self.admin_site.admin_view(self.send_invitations_view),
                name="events_event_send_invitations",
            ),
        ]
        return custom_urls + urls

    def invitation_stats(self, obj):
        """Invitation statistikasini ko'rsatish"""
        total = obj.invitation_set.count()
        accepted = obj.invitation_set.filter(status="accepted").count()
        declined = obj.invitation_set.filter(status="declined").count()
        pending = obj.invitation_set.filter(status="pending").count()

        return format_html('<span title="Jami: {}, Qabul: {}, Rad: {}, Kutilmoqda: {}">' "📊 {}/{} ({}P)</span>", total, accepted, declined, pending, accepted, total, pending)

    invitation_stats.short_description = "Taklifnomalar"

    def action_buttons(self, obj):
        """Action tugmalarini ko'rsatish"""
        return format_html('<a class="button" href="{}">📤 Taklifnoma yuborish</a>', reverse("admin:events_event_send_invitations", args=[obj.pk]))

    action_buttons.short_description = "Amallar"

    def send_invitations_view(self, request, object_id):
        """Taklifnoma yuborish sahifasi"""

        event = Event.objects.get(id=object_id)

        if request.method == "POST":
            selected_users = request.POST.getlist("selected_users")

            if selected_users:
                return self._process_invitations(request, event, selected_users)
            else:
                messages.error(request, "Hech qanday foydalanuvchi tanlanmagan!")

        all_users = BotUser.objects.all()

        existing_invitations = Invitation.objects.filter(event=event).values_list("user_id", flat=True)

        available_users = all_users.exclude(id__in=existing_invitations)

        context = {
            "event": event,
            "available_users": available_users,
            "existing_invitations_count": len(existing_invitations),
            "title": f'"{event.title}" uchun taklifnoma yuborish',
        }

        return render(request, "admin/send_invitations.html", context)

    def _process_invitations(self, request, event, selected_users):
        """Tanlangan userlarga invitation yuborish"""
        try:
            with transaction.atomic():
                invitations = []

                for user_id in selected_users:
                    user = BotUser.objects.get(id=user_id)

                    invitation, created = Invitation.objects.get_or_create(event=event, user=user, defaults={"status": "pending"})

                    if created:
                        invitations.append(invitation)

                if invitations:
                    service = TelegramService()

                    success_count, failed_count = asyncio.run(service.send_multiple_invitations(invitations))

                    if success_count > 0:
                        messages.success(request, f"{success_count} ta taklifnoma muvaffaqiyatli yuborildi!")

                    if failed_count > 0:
                        messages.warning(request, f"{failed_count} ta taklifnoma yuborishda xatolik yuz berdi.")
                else:
                    messages.info(request, "Barcha tanlangan foydalanuvchilarga allaqachon taklifnoma yuborilgan.")

        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")

        return redirect("admin:bot_event_changelist")


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["created_at", "updated_at"]
    list_filter = ["created_at"]


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ["full_name", "telegram_id", "phone", "passport", "language", "role", "is_registered", "created_at"]
    list_filter = ["language", "role", "is_registered", "created_at"]
    search_fields = ["full_name", "passport", "phone", "telegram_id"]
    list_editable = ["role", "is_registered"]
    readonly_fields = ["telegram_id", "created_at", "updated_at"]


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ["pk", "event", "user", "status", "created_at"]
    list_filter = ["event"]
