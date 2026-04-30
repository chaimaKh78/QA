"""
Configuration des URLs pour l'application Promotions.
"""

from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('', views.PromotionListView.as_view(), name='list'),
    path('newsletter/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('<str:code>/', views.PromotionDetailView.as_view(), name='detail'),
]
