"""
Administration de l'application Accounts.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, SavedDestination


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'newsletter')
    list_filter = ('newsletter', 'country')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(SavedDestination)
class SavedDestinationAdmin(admin.ModelAdmin):
    list_display = ('user', 'airport', 'created_at')
    list_filter = ('airport',)
    search_fields = ('user__username', 'airport__city')
