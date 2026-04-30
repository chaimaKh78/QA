"""
Context processors globaux pour le projet NouvelAir.
Ces variables sont accessibles dans tous les templates.
"""

from .settings import SITE_NAME, SITE_TAGLINE, CURRENCY


def site_settings(request):
    """Renvoie les paramètres du site pour tous les templates."""
    return {
        'site_name': SITE_NAME,
        'site_tagline': SITE_TAGLINE,
        'currency': CURRENCY,
    }
