"""
Vues de l'application Promotions.
"""

from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Promotion, NewsletterSubscription


class PromotionListView(ListView):
    """Liste des promotions actives."""

    model = Promotion
    template_name = 'promotions/promotion_list.html'
    context_object_name = 'promotions'

    def get_queryset(self):
        return Promotion.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).order_by('-is_featured', '-start_date')


class PromotionDetailView(DetailView):
    """Détail d'une promotion."""

    model = Promotion
    template_name = 'promotions/promotion_detail.html'
    context_object_name = 'promotion'
    slug_field = 'code'
    slug_url_kwarg = 'code'


class NewsletterSubscribeView(View):
    """Inscription à la newsletter (API)."""

    def post(self, request):
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()

        if not email:
            return JsonResponse({'success': False, 'error': "L'email est requis."})

        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name}
        )

        if created:
            return JsonResponse({'success': True, 'message': "Merci pour votre inscription !"})
        else:
            return JsonResponse({'success': False, 'error': "Cet email est déjà inscrit."})
