"""
Administration de l'application Destinations.
"""

from django.contrib import admin
from .models import Destination, DestinationImage, DestinationReview


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary')


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'airport', 'rating', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DestinationImageInline]


@admin.register(DestinationReview)
class DestinationReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved')
    search_fields = ('destination__name', 'user__username', 'title')
    list_editable = ('is_approved',)
