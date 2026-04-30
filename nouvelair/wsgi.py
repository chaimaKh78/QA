"""
Configuration WSGI pour le projet NouvelAir.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nouvelair.settings')
application = get_wsgi_application()
