from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('flights.urls')),
    path('destinations/', include('destinations.urls')),
    path('promotions/', include('promotions.urls')),
    path('bookings/', include('bookings.urls')),
    path('accounts/', include('accounts.urls')),
    path('mentions-legales/', TemplateView.as_view(template_name='legal.html'), name='legal'),
    path('conditions-generales/', TemplateView.as_view(template_name='terms.html'), name='terms'),
]