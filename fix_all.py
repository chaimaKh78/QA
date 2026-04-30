import os
import sys

# Detect encoding
def read_file(filepath):
    """Read file with UTF-8 encoding."""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    return None

def write_file(filepath, content):
    """Write file with UTF-8 encoding."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

fixes_applied = 0
fixes_failed = 0

print("=" * 60)
print("  NouvelAir - Script de correction global")
print("=" * 60)
print()

# =============================================
# FIX 1: base.html - URL namespaces
# =============================================
print("[FIX 1] base.html - Correction des URLs...")
base_html_path = os.path.join(BASE_DIR, 'nouvelair', 'templates', 'base.html')
content = read_file(base_html_path)

if content and "{% url 'home' %}" in content:
    # Full corrected base.html
    corrected_base = r'''{% load static %}
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ site_name }}{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-nouvelair sticky-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'flights:home' %}">
                <i class="fas fa-plane me-2"></i>{{ site_name }}
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'flights:home' %}"><i class="fas fa-home me-1"></i>Accueil</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'flights:search_results' %}"><i class="fas fa-search me-1"></i>Reservation</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'destinations:list' %}"><i class="fas fa-map-marker-alt me-1"></i>Destinations</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'promotions:list' %}"><i class="fas fa-tags me-1"></i>Offres</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'bookings:lookup' %}"><i class="fas fa-suitcase me-1"></i>Ma Reservation</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
                                <i class="fas fa-user-circle me-1"></i>{{ user.first_name|default:user.username }}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="{% url 'accounts:profile' %}"><i class="fas fa-user me-2"></i>Mon Profil</a></li>
                                <li><a class="dropdown-item" href="{% url 'bookings:my_bookings' %}"><i class="fas fa-list me-2"></i>Mes Reservations</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{% url 'accounts:logout' %}"><i class="fas fa-sign-out-alt me-2"></i>Deconnexion</a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:login' %}"><i class="fas fa-sign-in-alt me-1"></i>Connexion</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:register' %}"><i class="fas fa-user-plus me-1"></i>Inscription</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Contenu principal -->
    {% block content %}{% endblock %}

    <!-- Footer -->
    <footer class="bg-dark text-white py-5 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <h5><i class="fas fa-plane me-2"></i>{{ site_name }}</h5>
                    <p class="text-white-50">{{ site_tagline }}</p>
                    <div class="social-links">
                        <a href="#" class="text-white me-3"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" class="text-white me-3"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="text-white me-3"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="text-white"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                </div>
                <div class="col-md-2 mb-4">
                    <h6>Navigation</h6>
                    <ul class="list-unstyled">
                        <li><a href="{% url 'flights:home' %}" class="text-white-50 text-decoration-none">Accueil</a></li>
                        <li><a href="{% url 'destinations:list' %}" class="text-white-50 text-decoration-none">Destinations</a></li>
                        <li><a href="{% url 'promotions:list' %}" class="text-white-50 text-decoration-none">Offres</a></li>
                        <li><a href="{% url 'flights:airport_list' %}" class="text-white-50 text-decoration-none">Aeroports</a></li>
                    </ul>
                </div>
                <div class="col-md-2 mb-4">
                    <h6>Assistance</h6>
                    <ul class="list-unstyled">
                        <li><a href="{% url 'bookings:lookup' %}" class="text-white-50 text-decoration-none">Ma Reservation</a></li>
                        <li><a href="{% url 'legal' %}" class="text-white-50 text-decoration-none">Mentions Legales</a></li>
                        <li><a href="{% url 'terms' %}" class="text-white-50 text-decoration-none">Conditions Generales</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-4">
                    <h6>Newsletter</h6>
                    <p class="text-white-50 small">Recevez nos meilleures offres directement par email.</p>
                    <form id="newsletter-form" class="d-flex">
                        <input type="email" id="newsletter-email" class="form-control me-2" placeholder="Votre email" required>
                        <button type="submit" class="btn btn-nouvelair">S'abonner</button>
                    </form>
                </div>
            </div>
            <hr class="border-secondary">
            <div class="row">
                <div class="col-md-6 text-white-50 small">
                    &copy; {{ site_name }} - Tous droits reserves
                </div>
                <div class="col-md-6 text-end text-white-50 small">
                    Projet Fil Rouge - Formation Test/QA &amp; IA
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>'''
    write_file(base_html_path, corrected_base)
    print("    OK: base.html corrige (URLs avec namespaces)")
    fixes_applied += 1
elif content and "{% url 'flights:home' %}" in content:
    print("    SKIP: base.html deja corrige")
else:
    print("    ERREUR: base.html non trouve")
    fixes_failed += 1

# =============================================
# FIX 2: home.html - duration_format
# =============================================
print("[FIX 2] home.html - Correction duration_format...")
home_html_path = os.path.join(BASE_DIR, 'flights', 'templates', 'flights', 'home.html')
content = read_file(home_html_path)

if content and "|duration_format" in content:
    content = content.replace("{{ flight.duration|duration_format }}", "{{ flight.duration }}")
    write_file(home_html_path, content)
    print("    OK: home.html corrige")
    fixes_applied += 1
elif content:
    print("    SKIP: home.html deja corrige")
else:
    print("    ERREUR: home.html non trouve")
    fixes_failed += 1

# =============================================
# FIX 3: search_results.html - duration_format
# =============================================
print("[FIX 3] search_results.html - Correction duration_format...")
search_html_path = os.path.join(BASE_DIR, 'flights', 'templates', 'flights', 'search_results.html')
content = read_file(search_html_path)

if content and "|duration_format" in content:
    content = content.replace("{{ flight.duration|duration_format }}", "{{ flight.duration }}")
    write_file(search_html_path, content)
    print("    OK: search_results.html corrige")
    fixes_applied += 1
elif content:
    print("    SKIP: search_results.html deja corrige")
else:
    print("    ERREUR: search_results.html non trouve")
    fixes_failed += 1

# =============================================
# FIX 4: flight_detail.html - duration_format
# =============================================
print("[FIX 4] flight_detail.html - Correction duration_format...")
detail_html_path = os.path.join(BASE_DIR, 'flights', 'templates', 'flights', 'flight_detail.html')
content = read_file(detail_html_path)

if content and "|duration_format" in content:
    content = content.replace("{{ flight.duration|duration_format }}", "{{ flight.duration }}")
    content = content.replace("{{ sf.duration|duration_format }}", "{{ sf.duration }}")
    write_file(detail_html_path, content)
    print("    OK: flight_detail.html corrige")
    fixes_applied += 1
elif content:
    print("    SKIP: flight_detail.html deja corrige")
else:
    print("    ERREUR: flight_detail.html non trouve")
    fixes_failed += 1

# =============================================
# FIX 5: flights/views.py - airport_autocomplete
# =============================================
print("[FIX 5] flights/views.py - Correction import models.Q...")
views_path = os.path.join(BASE_DIR, 'flights', 'views.py')
content = read_file(views_path)

if content and "models.Q(" in content and "from django.db import models" not in content:
    # Add the missing import
    content = content.replace(
        "from .models import Airport, Flight, Aircraft",
        "from django.db import models\nfrom .models import Airport, Flight, Aircraft"
    )
    write_file(views_path, content)
    print("    OK: flights/views.py corrige (import models ajoute)")
    fixes_applied += 1
elif content and "models.Q(" in content and "from django.db import models" in content:
    print("    SKIP: flights/views.py deja corrige")
elif content:
    print("    OK: flights/views.py n'utilise pas models.Q (pas de correction necessaire)")
else:
    print("    ERREUR: flights/views.py non trouve")
    fixes_failed += 1

# =============================================
# FIX 6: flights/models.py - get_duration_display
# =============================================
print("[FIX 6] flights/models.py - Ajout get_duration_display()...")
models_path = os.path.join(BASE_DIR, 'flights', 'models.py')
content = read_file(models_path)

if content and "get_duration_display" not in content:
    # Add get_duration_display method to Flight model
    method_code = """
    def get_duration_display(self):
        \"\"\"Retourne la duree du vol formattee (ex: 2h30).\"\"\"
        if self.duration:
            total_seconds = int(self.duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            if hours > 0 and minutes > 0:
                return f"{hours}h{minutes:02d}"
            elif hours > 0:
                return f"{hours}h"
            else:
                return f"{minutes}min"
        return "N/A"
"""
    # Insert before get_current_price_economy
    content = content.replace(
        "    def get_current_price_economy(self):",
        method_code + "\n    def get_current_price_economy(self):"
    )
    write_file(models_path, content)
    print("    OK: flights/models.py corrige (methode get_duration_display ajoutee)")
    fixes_applied += 1
elif content:
    print("    SKIP: flights/models.py a deja get_duration_display")
else:
    print("    ERREUR: flights/models.py non trouve")
    fixes_failed += 1

# =============================================
# FIX 7: Update templates to use get_duration_display instead of raw duration
# =============================================
# Only needed if we switched from duration_format to raw duration
# We should use {{ flight.get_duration_display }} for nice formatting
for tpl_name, tpl_path in [
    ("home.html", home_html_path),
    ("search_results.html", search_html_path),
    ("flight_detail.html", detail_html_path),
]:
    content = read_file(tpl_path)
    if content and "{{ flight.duration }}" in content:
        content = content.replace("{{ flight.duration }}", "{{ flight.get_duration_display }}")
        # Also fix sf.duration in flight_detail
        content = content.replace("{{ sf.duration }}", "{{ sf.get_duration_display }}")
        write_file(tpl_path, content)
        print(f"    OK: {tpl_name} mis a jour avec get_duration_display")
        fixes_applied += 1

# =============================================
# FIX 8: bookings/models.py - meal_preference choices
# =============================================
print("[FIX 8] bookings/models.py - Ajout des choix meal_preference...")
bookings_models_path = os.path.join(BASE_DIR, 'bookings', 'models.py')
content = read_file(bookings_models_path)

if content and "meal_preference" in content and "MEAL_CHOICES" not in content:
    # meal_preference is just a CharField with blank=True, no choices - this is fine
    # But let's check if the PassengerForm needs MEAL_CHOICES
    print("    INFO: meal_preference est un CharField libre, pas de correction necessaire")
elif content:
    print("    SKIP: bookings/models.py deja a MEAL_CHOICES")
else:
    print("    ERREUR: bookings/models.py non trouve")
    fixes_failed += 1

# =============================================
# Summary
# =============================================
print()
print("=" * 60)
print(f"  Resultat: {fixes_applied} correction(s) appliquee(s)")
if fixes_failed > 0:
    print(f"  Attention: {fixes_failed} correction(s) echouee(s)")
print("=" * 60)
print()
print("Redemarrez le serveur :")
print("  python manage.py runserver")
print()
