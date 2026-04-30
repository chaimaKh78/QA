"""
Configuration des URLs pour l'application Accounts.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.RegisterView.as_view(), name='register'),
    path('connexion/', views.LoginView.as_view(), name='login'),
    path('deconnexion/', views.LogoutView.as_view(), name='logout'),
    path('profil/', views.ProfileView.as_view(), name='profile'),
]
