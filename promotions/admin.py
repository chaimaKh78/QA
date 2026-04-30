"""
Administration de l'application Promotions.
"""

from django.contrib import admin
from .models import Promotion, NewsletterSubscription


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'promo_type', 'discount_percentage',
        'start_date', 'end_date', 'is_active', 'is_featured'
    )
    list_filter = ('promo_type', 'is_active', 'is_featured', 'start_date')
    search_fields = ('code', 'name', 'description')
    filter_horizontal = ('flights',)
    prepopulated_fields = {}


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_active', 'subscribed_at')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name')
