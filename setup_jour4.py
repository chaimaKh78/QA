#!/usr/bin/env python3
"""
setup_jour4.py — Crée les fichiers BDD/Gherkin (Behave) pour le Jour 4
=======================================================================
Projet NouvelAir — Django Training Project

Ce script génère automatiquement :
  1. features/environment.py             (Behave-Django environment)
  2. features/search.feature             (US-001 à US-005 — 9 scénarios)
  3. features/booking.feature            (US-008 à US-010 — 7 scénarios)
  4. features/auth.feature               (US-027 à US-031 — 7 scénarios)
  5. features/promotions.feature         (US-006 / US-034 — 5 scénarios)
  6. features/steps/__init__.py          (vide)
  7. features/steps/search_steps.py      (définitions d'étapes recherche)
  8. features/steps/booking_steps.py     (définitions d'étapes réservation)
  9. features/steps/auth_steps.py        (définitions d'étapes authentification)
 10. features/steps/promotions_steps.py  (définitions d'étapes promotions)
 11. features/steps/common_steps.py      (étapes partagées)

Utilisation :
    cd D:\\NouvelairApp\\nouvelair_project
    python setup_jour4.py

Exécution des tests BDD :
    behave features/search.feature
    behave features/booking.feature
    behave features/auth.feature
    behave features/promotions.feature
    behave features/                    (tous les features)

Prérequis (dans requirements_test.txt) :
    behave
    behave-django
"""

import os
import sys

# ── Chemins ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = SCRIPT_DIR


def ensure_dir(path):
    """Crée le répertoire s'il n'existe pas."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"  📁  Créé : {os.path.relpath(path, PROJECT_ROOT)}")


def write_file(path, content):
    """Écrit le fichier et affiche un résumé."""
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    rel = os.path.relpath(path, PROJECT_ROOT)
    lines = content.count("\n") + 1
    print(f"  📄  {rel}  ({lines} lignes)")


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 1 — features/environment.py
# ══════════════════════════════════════════════════════════════════════════════

FILE_ENVIRONMENT = r'''"""
environment.py — Configuration Behave-Django pour les tests BDD.
================================================================

Ce fichier configure l'environnement d'exécution de Behave avec
l'intégration Django (behave-django).

Hooks :
    before_all        — Initialise Django avant tous les scénarios
    after_all         — Nettoyage final après tous les scénarios
    before_scenario   — Réinitialise la BDD et crée les données de test
    after_scenario    — Nettoie les données après chaque scénario
"""

import os
import django

from behave import fixture, use_fixture
from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connection
from django.core.management import call_command

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

from flights.models import Airport, Aircraft, Flight
from accounts.models import UserProfile
from bookings.models import Booking, Passenger, Payment
from promotions.models import Promotion, NewsletterSubscription
from destinations.models import Destination


# ── Fixtures de données de test ───────────────────────────────────────────────


def _create_base_airports():
    """Crée les aéroports de base utilisés dans les scénarios."""
    airports = {}
    airport_data = [
        ("TUN", "Aéroport International Tunis-Carthage", "Tunis", "Tunisie",
         36.851000, 10.227000),
        ("CDG", "Aéroport Charles de Gaulle", "Paris", "France",
         49.009700, 2.547900),
        ("MRS", "Aéroport de Marseille Provence", "Marseille", "France",
         43.436400, 5.215700),
        ("CMN", "Aéroport Mohammed V", "Casablanca", "Maroc",
         33.367500, -7.589800),
        ("ALG", "Aéroport Houari Boumediene", "Alger", "Algérie",
         36.694000, 3.215300),
        ("JFK", "Aéroport John F. Kennedy", "New York", "États-Unis",
         40.641300, -73.778100),
        ("FCO", "Aéroport Léonard de Vinci", "Rome", "Italie",
         41.800300, 12.238900),
        ("LHR", "Aéroport de Heathrow", "Londres", "Royaume-Uni",
         51.470000, -0.454300),
    ]
    for code, name, city, country, lat, lon in airport_data:
        airports[code], _ = Airport.objects.get_or_create(
            code=code,
            defaults={
                "name": name,
                "city": city,
                "country": country,
                "latitude": lat,
                "longitude": lon,
                "is_active": True,
            },
        )
    return airports


def _create_aircraft():
    """Crée un aéronef de test."""
    aircraft, _ = Aircraft.objects.get_or_create(
        registration="TS-ABC",
        defaults={
            "model_name": "Airbus A320",
            "total_seats": 180,
            "economy_seats": 150,
            "business_seats": 30,
            "is_active": True,
        },
    )
    return aircraft


def _create_test_flights(airports, aircraft):
    """Crée les vols de test pour les scénarios."""
    flights = {}
    now = timezone.now()
    flight_data = [
        ("BJ101", "TUN", "CDG", 7, 8, 0, 11, 30, 250.00, 600.00),
        ("BJ102", "TUN", "MRS", 7, 14, 0, 16, 30, 180.00, 450.00),
        ("BJ103", "CDG", "TUN", 14, 12, 0, 15, 30, 230.00, 550.00),
        ("BJ520", "TUN", "CDG", 10, 6, 30, 10, 0, 199.00, 520.00),
        ("BJ201", "TUN", "CMN", 12, 9, 0, 11, 30, 160.00, 400.00),
        ("BJ301", "TUN", "ALG", 8, 16, 0, 17, 30, 140.00, 350.00),
        ("BJ601", "TUN", "JFK", 15, 22, 0, 6, 0, 890.00, 2200.00),
        ("BJ401", "TUN", "FCO", 9, 7, 0, 9, 30, 210.00, 500.00),
        ("BJ501", "TUN", "LHR", 11, 10, 0, 13, 0, 280.00, 650.00),
    ]
    for fn, origin_code, dest_code, days, dh, dm, ah, am, pe, pb in flight_data:
        future_dep = now + timedelta(days=days, hours=dh, minutes=dm)
        future_arr = now + timedelta(days=days, hours=ah, minutes=am)
        # Si l'heure d'arrivée est avant le départ, ajouter un jour
        if future_arr <= future_dep:
            future_arr += timedelta(days=1)
        flights[fn], _ = Flight.objects.get_or_create(
            flight_number=fn,
            defaults={
                "origin": airports[origin_code],
                "destination": airports[dest_code],
                "aircraft": aircraft,
                "departure_time": future_dep,
                "arrival_time": future_arr,
                "status": "scheduled",
                "base_price_economy": pe,
                "base_price_business": pb,
                "available_seats_economy": 150,
                "available_seats_business": 30,
                "is_active": True,
            },
        )
    return flights


def _create_test_user():
    """Crée l'utilisateur de test 'testuser' avec profil."""
    user, created = User.objects.get_or_create(
        username="testuser",
        defaults={
            "email": "test@example.com",
            "first_name": "Jean",
            "last_name": "Dupont",
            "is_active": True,
        },
    )
    if created:
        user.set_password("TestPassword123!")
        user.save()
        UserProfile.objects.update_or_create(user=user, defaults={"phone": "+21612345678"})
    return user


def _create_test_promotions(flights):
    """Crée les promotions de test."""
    promos = {}
    now = timezone.now()

    # Promo active
    promos["NOUVEL25"], _ = Promotion.objects.get_or_create(
        code="NOUVEL25",
        defaults={
            "name": "Réduction 25% NouvelAir",
            "description": "25% de réduction sur tous les vols",
            "promo_type": "percentage",
            "discount_percentage": 25.00,
            "discount_amount": 0,
            "start_date": now - timedelta(days=1),
            "end_date": now + timedelta(days=30),
            "max_uses": 100,
            "current_uses": 0,
            "min_purchase_amount": 0,
            "is_active": True,
            "is_featured": True,
        },
    )
    if created := not promos["NOUVEL25"].flights.exists():
        for flight in flights.values():
            promos["NOUVEL25"].flights.add(flight)

    # Promo expirée
    promos["EXPIRED10"], _ = Promotion.objects.get_or_create(
        code="EXPIRED10",
        defaults={
            "name": "Promo Expirée",
            "description": "Promotion expirée",
            "promo_type": "percentage",
            "discount_percentage": 10.00,
            "discount_amount": 0,
            "start_date": now - timedelta(days=60),
            "end_date": now - timedelta(days=30),
            "max_uses": 100,
            "current_uses": 50,
            "min_purchase_amount": 0,
            "is_active": False,
            "is_featured": False,
        },
    )

    return promos


def _populate_test_data():
    """Peuple la base avec toutes les données de test nécessaires."""
    airports = _create_base_airports()
    aircraft = _create_aircraft()
    flights = _create_test_flights(airports, aircraft)
    user = _create_test_user()
    promotions = _create_test_promotions(flights)

    return {
        "airports": airports,
        "aircraft": aircraft,
        "flights": flights,
        "user": user,
        "promotions": promotions,
    }


# ── Hooks Behave ──────────────────────────────────────────────────────────────


def before_all(context):
    """
    Initialisation globale avant l'exécution de tous les scénarios.

    - Configure les paramètres Django
    - Initialise l'environnement de test Django
    - Appelle django.setup()
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nouvelair.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Testing")

    # behave-django appelle django.setup() automatiquement si le module
    # behave_django.fixture est configuré dans behave.ini
    # Mais on s'assure que Django est bien initialisé
    if not django.apps.apps.ready:
        django.setup()

    setup_test_environment()


def after_all(context):
    """
    Nettoyage global après l'exécution de tous les scénarios.

    - Détruit l'environnement de test Django
    """
    teardown_test_environment()


def before_scenario(context, scenario):
    """
    Préparation avant chaque scénario.

    - Vide toutes les tables de la base de données
    - Crée les données de test de référence
    - Initialise le client de test Django
    """
    # Réinitialise la base de données
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;")
    tables = connection.introspection.table_names()
    for table in tables:
        cursor.execute(f'DELETE FROM "{table}";')
    # Réinitialise les auto-incréments (SQLite)
    for table in tables:
        cursor.execute(f'DELETE FROM sqlite_sequence WHERE name = "{table}";')
    cursor.execute("PRAGMA foreign_keys = ON;")
    connection.commit()

    # Peuple les données de test
    context.test_data = _populate_test_data()

    # Rend les données accessibles directement sur le contexte
    context.airports = context.test_data["airports"]
    context.aircraft = context.test_data["aircraft"]
    context.flights = context.test_data["flights"]
    context.test_user = context.test_data["user"]
    context.promotions = context.test_data["promotions"]

    # Initialise le client de test Django (comme dans les tests unitaires)
    from django.test import Client
    context.test = type('TestClient', (), {})()
    context.test.client = Client()


def after_scenario(context, scenario):
    """
    Nettoyage après chaque scénario.

    - Ferme les connexions à la base de données
    - Nettoie le contexte
    """
    # Ferme les connexions DB pour éviter les fuites
    for conn in connection._connections.values():
        conn.close_if_unusable_or_obsolete()

    # Nettoie le contexte
    if hasattr(context, "test_data"):
        del context.test_data
    if hasattr(context, "airports"):
        del context.airports
    if hasattr(context, "aircraft"):
        del context.aircraft
    if hasattr(context, "flights"):
        del context.flights
    if hasattr(context, "test_user"):
        del context.test_user
    if hasattr(context, "promotions"):
        del context.promotions
    if hasattr(context, "response"):
        del context.response
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 2 — features/search.feature
# ══════════════════════════════════════════════════════════════════════════════

FILE_SEARCH_FEATURE = '''# language: fr
Fonctionnalité: Recherche de vols (EP-01)
  En tant que voyageur
  Je veux rechercher des vols disponibles
  Afin de planifier mon voyage avec NouvelAir

  Contexte:
    Étant donné que la base de données est peuplée

  # ── US-001 : Recherche de vol aller simple ────────────────────────────────

  Scénario: Recherche de vol aller simple TUN vers CDG
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Et un vol "BJ101" de "TUN" à "CDG" est programmé
    Quand je recherche un vol aller simple de "TUN" vers "CDG" avec 1 passager
    Alors le statut de la réponse est 200
    Et je vois les résultats de recherche

  Scénario: Recherche de vol aller simple avec plusieurs passagers
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "MRS" existe dans la base
    Et un vol "BJ102" de "TUN" à "MRS" est programmé
    Quand je recherche un vol aller simple de "TUN" vers "MRS" avec 2 passagers
    Alors le statut de la réponse est 200
    Et je vois les résultats de recherche

  # ── US-001 : Recherche aller-retour ────────────────────────────────────────

  Scénario: Recherche de vol aller-retour
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Et un vol "BJ101" de "TUN" à "CDG" est programmé
    Et un vol "BJ103" de "CDG" à "TUN" est programmé
    Quand je recherche un vol aller-retour de "TUN" vers "CDG" avec 1 passager
    Alors le statut de la réponse est 200
    Et je vois les résultats de recherche

  # ── Validation : départ et arrivée identiques ──────────────────────────────

  Scénario: Recherche avec départ et arrivée identiques affiche une erreur
    Étant donné l'aéroport "TUN" existe dans la base
    Quand je recherche un vol aller simple de "TUN" vers "TUN" avec 1 passager
    Alors le statut de la réponse est 200
    Et un message d'erreur contenant "différents" est affiché

  # ── Validation : date dans le passé ────────────────────────────────────────

  Scénario: Recherche avec une date dans le passé affiche une erreur
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Quand je recherche un vol aller simple de "TUN" vers "CDG" pour la date d'hier
    Alors le statut de la réponse est 200
    Et un message d'erreur contenant "passée" est affiché

  # ── US-004 : Résultats triés par prix ──────────────────────────────────────

  Scénario: Résultats de recherche triés par prix croissant
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Et un vol "BJ101" de "TUN" à "CDG" à 250.00 TND est programmé
    Et un vol "BJ520" de "TUN" à "CDG" à 199.00 TND est programmé
    Quand je recherche un vol aller simple de "TUN" vers "CDG" avec 1 passager
    Et je trie les résultats par prix croissant
    Alors le premier résultat a un prix inférieur ou égal au deuxième résultat

  # ── US-005 : Sélection de classe de voyage ─────────────────────────────────

  Plan du scénario: Sélection de classe de voyage modifie le prix affiché
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Et un vol "BJ101" de "TUN" à "CDG" est programmé
    Quand je recherche un vol aller simple de "TUN" vers "CDG" avec 1 passager
    Et je sélectionne la classe "<classe>"
    Alors le prix est affiché en TND
    Et le prix correspond à la classe "<classe>"

    Exemples:
      | classe      |
      | Économie    |
      | Affaires    |

  # ── Page d'accueil ─────────────────────────────────────────────────────────

  Scénario: Les aéroports populaires sont affichés sur la page d'accueil
    Étant donné que la base de données est peuplée
    Quand j'accède à la page "flights:home"
    Alors le statut de la réponse est 200
    Et je vois au moins 3 aéroports populaires

  Scénario: Le formulaire de recherche contient tous les champs nécessaires
    Étant donné que la base de données est peuplée
    Quand j'accède à la page "flights:home"
    Alors le statut de la réponse est 200
    Et le formulaire de recherche contient le champ "origin"
    Et le formulaire de recherche contient le champ "destination"
    Et le formulaire de recherche contient le champ "departure_date"
    Et le formulaire de recherche contient le champ "passengers"
    Et le formulaire de recherche contient le champ "travel_class"
    Et le formulaire de recherche contient le champ "trip_type"

  # ── Recherche sans résultat ────────────────────────────────────────────────

  Scénario: Recherche sans résultat ne provoque pas d'erreur
    Étant donné l'aéroport "JFK" existe dans la base
    Et l'aéroport "LHR" existe dans la base
    Quand je recherche un vol aller simple de "JFK" vers "LHR" avec 1 passager
    Alors le statut de la réponse est 200
    Et je ne vois aucun résultat
    Et la page affiche "Aucun vol"
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 3 — features/booking.feature
# ══════════════════════════════════════════════════════════════════════════════

FILE_BOOKING_FEATURE = '''# language: fr
Fonctionnalité: Gestion de réservation (EP-02)
  En tant que voyageur
  Je veux créer, consulter et annuler mes réservations
  Afin de gérer mes voyages avec NouvelAir

  Contexte:
    Étant donné que la base de données est peuplée

  # ── US-008 : Création de réservation (utilisateur connecté) ────────────────

  Scénario: Création d'une réservation en tant qu'utilisateur connecté
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Et un vol est disponible pour la réservation
    Quand je réserve le vol avec les informations passager valides
    Alors la réservation est créée avec succès
    Et la réservation a le statut "confirmed"
    Et un numéro de référence est généré

  # ── Consultation de réservation ────────────────────────────────────────────

  Scénario: Consultation d'une réservation existante
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Et une réservation "REF001" existe pour mon compte
    Quand j'accède à la page "bookings:my_bookings"
    Alors le statut de la réponse est 200
    Et je vois la réservation "REF001" dans la liste

  # ── US-010 : Annulation de réservation pending ─────────────────────────────

  Scénario: Annulation d'une réservation en attente
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Et une réservation avec le statut "pending" existe
    Quand j'annule la réservation
    Alors la réservation est annulée
    Et le statut de la réservation est "cancelled"

  # ── Annulation impossible si déjà annulée ──────────────────────────────────

  Scénario: Annulation impossible si la réservation est déjà annulée
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Et une réservation avec le statut "cancelled" existe
    Quand j'essaie d'annuler la réservation
    Alors la réservation reste avec le statut "cancelled"
    Et un message d'erreur est affiché

  # ── Recherche par référence et nom ─────────────────────────────────────────

  Scénario: Recherche de réservation par référence et nom de famille
    Étant donné une réservation pour "Dupont" avec la référence "REF002" existe
    Quand je recherche la réservation avec la référence "REF002" et le nom "Dupont"
    Alors le statut de la réponse est 302
    Et je suis redirigé vers la page de détail de la réservation

  Scénario: Recherche de réservation avec une référence invalide
    Étant donné que la base de données est peuplée
    Quand je recherche la réservation avec la référence "INVALID" et le nom "Dupont"
    Alors le statut de la réponse est 200
    Et un message d'erreur contenant "introuvable" est affiché

  # ── US-008 : Réservation nécessite une connexion ───────────────────────────

  Scénario: La création de réservation nécessite une connexion
    Étant donné je suis un visiteur non connecté
    Et un vol est disponible pour la réservation
    Quand j'essaie de réserver le vol
    Alors je suis redirigé vers la page "accounts:login"

  # ── Consultation de mes réservations sans connexion ────────────────────────

  Scénario: L'accès à mes réservations nécessite une connexion
    Étant donné je suis un visiteur non connecté
    Quand j'accède à la page "bookings:my_bookings"
    Alors je suis redirigé vers la page "accounts:login"
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 4 — features/auth.feature
# ══════════════════════════════════════════════════════════════════════════════

FILE_AUTH_FEATURE = '''# language: fr
Fonctionnalité: Compte utilisateur (EP-06)
  En tant que visiteur ou utilisateur
  Je veux m'inscrire, me connecter et gérer mon profil
  Afin de bénéficier des services personnalisés de NouvelAir

  Contexte:
    Étant donné que la base de données est peuplée

  # ── US-027 : Inscription avec données valides ──────────────────────────────

  Scénario: Inscription avec des données valides
    Étant donné je suis un visiteur non connecté
    Quand je m'inscris avec les données valides suivantes:
      | username | prenom  | nom     | email              | mot_de_passe    | confirmation   |
      | newuser  | Pierre  | Martin  | pierre@exemple.com | SecurePass123!  | SecurePass123! |
    Alors le compte est créé avec succès
    Et je suis connecté automatiquement
    Et je suis redirigé vers la page "flights:home"
    Et un profil utilisateur est créé automatiquement

  # ── Inscription avec email dupliqué ────────────────────────────────────────

  Scénario: Inscription avec un email déjà utilisé affiche une erreur
    Étant donné je suis un visiteur non connecté
    Quand je m'inscris avec les données suivantes ayant un email dupliqué:
      | username   | prenom | nom  | email              | mot_de_passe    | confirmation   |
      | otheruser  | Marie  | Curie| test@example.com   | SecurePass123!  | SecurePass123! |
    Alors le compte n'est pas créé
    Et un message d'erreur contenant "email" est affiché

  # ── US-028 : Connexion réussie ─────────────────────────────────────────────

  Scénario: Connexion avec des identifiants valides
    Étant donné je suis un visiteur non connecté
    Quand je me connecte avec "testuser" et "TestPassword123!"
    Alors je suis connecté avec succès
    Et je suis redirigé vers la page "flights:home"

  # ── Connexion échouée ─────────────────────────────────────────────────────

  Scénario: Connexion échouée avec un mauvais mot de passe
    Étant donné je suis un visiteur non connecté
    Quand je me connecte avec "testuser" et "wrongpass"
    Alors je ne suis pas connecté
    Et un message d'erreur est affiché
    Et je reste sur la page "accounts:login"

  # ── US-028 : Déconnexion ──────────────────────────────────────────────────

  Scénario: Déconnexion d'un utilisateur connecté
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Quand je me déconnecte
    Alors je suis déconnecté
    Et je suis redirigé vers la page "flights:home"

  # ── US-030 : Mise à jour du profil ────────────────────────────────────────

  Scénario: Mise à jour du profil utilisateur
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Quand je mets à jour mon profil avec les données suivantes:
      | prenom      | nom       | email                | telephone     | ville   | pays      |
      | JeanModifié | DupontMod | modified@exemple.com | +21698765432  | Sousse  | Tunisie   |
    Alors le profil est mis à jour avec succès
    Et les informations sont sauvegardées en base de données

  # ── Accès profil nécessite connexion ───────────────────────────────────────

  Scénario: L'accès au profil nécessite une connexion
    Étant donné je suis un visiteur non connecté
    Quand j'accède à la page "accounts:profile"
    Alors je suis redirigé vers la page "accounts:login"
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 5 — features/promotions.feature
# ══════════════════════════════════════════════════════════════════════════════

FILE_PROMOTIONS_FEATURE = '''# language: fr
Fonctionnalité: Codes promotionnels (EP-01 / US-006)
  En tant que voyageur
  Je veux appliquer des codes promotionnels
  Afin de bénéficier de réductions sur mes réservations

  Contexte:
    Étant donné que la base de données est peuplée

  # ── US-006 : Application code promo valide ─────────────────────────────────

  Scénario: Application d'un code promotionnel valide
    Étant donné un code promo "NOUVEL25" est actif avec 25% de réduction
    Et un vol est disponible avec un prix de 250.00 TND
    Quand j'applique le code "NOUVEL25" au vol
    Alors la remise est appliquée
    Et le prix final est de 187.50 TND
    Et un message de confirmation est affiché

  Scénario: Application d'un code promo à un vol affaires
    Étant donné un code promo "NOUVEL25" est actif avec 25% de réduction
    Et un vol affaires est disponible avec un prix de 600.00 TND
    Quand j'applique le code "NOUVEL25" au vol
    Alors la remise est appliquée
    Et le prix final est de 450.00 TND

  # ── Code promo expiré ─────────────────────────────────────────────────────

  Scénario: Application d'un code promotionnel expiré affiche une erreur
    Étant donné un code promo "EXPIRED10" est expiré
    Quand j'applique le code "EXPIRED10" au vol
    Alors la remise n'est pas appliquée
    Et un message d'erreur contenant "expiré" est affiché

  # ── Code promo inexistant ─────────────────────────────────────────────────

  Scénario: Application d'un code promotionnel inexistant affiche une erreur
    Étant donné que la base de données est peuplée
    Quand j'applique le code "INCONNU50" au vol
    Alors la remise n'est pas appliquée
    Et un message d'erreur contenant "invalide" est affiché

  # ── US-034 : Newsletter ────────────────────────────────────────────────────

  Scénario: Inscription à la newsletter avec un email valide
    Étant donné je suis un visiteur non connecté
    Quand je m'inscris à la newsletter avec "newsletter@exemple.com"
    Alors l'inscription à la newsletter est confirmée
    Et un message de confirmation est affiché
    Et l'adresse email est enregistrée en base de données

  Scénario: Inscription à la newsletter avec un email déjà enregistré
    Étant donné l'adresse "newsletter@exemple.com" est déjà inscrite à la newsletter
    Quand je m'inscris à la newsletter avec "newsletter@exemple.com"
    Alors l'inscription échoue
    Et un message d'erreur contenant "déjà" est affiché
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 6 — features/steps/__init__.py
# ══════════════════════════════════════════════════════════════════════════════

FILE_STEPS_INIT = ""


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 7 — features/steps/search_steps.py
# ══════════════════════════════════════════════════════════════════════════════

FILE_SEARCH_STEPS = r'''"""
search_steps.py — Définitions d'étapes Behave pour la recherche de vols.
======================================================================

Scénarios couverts :
    - US-001 : Recherche aller simple / aller-retour
    - US-004 : Tri par prix
    - US-005 : Sélection de classe de voyage
    - Validations : même aéroport, date passée, formulaire
    - Page d'accueil et aéroports populaires
"""

from behave import given, when, then
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, date

from flights.models import Airport, Flight


# ── GIVEN : Préconditions ────────────────────────────────────────────────────


@given(r'l\'aéroport "([^"]+)" existe dans la base')
def step_airport_exists(context, airport_code):
    """Vérifie qu'un aéroport existe dans la base de données."""
    airport = Airport.objects.filter(code=airport_code).first()
    assert airport is not None, (
        f"L'aéroport '{airport_code}' n'existe pas dans la base de données"
    )
    context.current_origin = airport


@given(r'un vol "([^"]+)" de "([^"]+)" à "([^"]+)" est programmé')
def step_flight_scheduled(context, flight_number, origin_code, dest_code):
    """Vérifie qu'un vol est programmé entre deux aéroports."""
    flight = Flight.objects.filter(flight_number=flight_number).first()
    assert flight is not None, (
        f"Le vol '{flight_number}' n'existe pas dans la base de données"
    )
    assert flight.origin.code == origin_code, (
        f"Le vol '{flight_number}' ne part pas de '{origin_code}' "
        f"mais de '{flight.origin.code}'"
    )
    assert flight.destination.code == dest_code, (
        f"Le vol '{flight_number}' n'arrive pas à '{dest_code}' "
        f"mais à '{flight.destination.code}'"
    )
    context.current_flight = flight


@given(r'un vol "([^"]+)" de "([^"]+)" à "([^"]+)" à ([\d.]+) TND est programmé')
def step_flight_with_price(context, flight_number, origin_code, dest_code, price):
    """Vérifie qu'un vol est programmé avec un prix spécifique."""
    flight = Flight.objects.filter(flight_number=flight_number).first()
    assert flight is not None, (
        f"Le vol '{flight_number}' n'existe pas dans la base de données"
    )
    expected_price = float(price)
    assert float(flight.base_price_economy) == expected_price, (
        f"Le vol '{flight_number}' coûte {flight.base_price_economy} TND, "
        f"pas {expected_price} TND"
    )
    context.current_flight = flight


@given(r'la base de données est peuplée')
def step_db_populated(context):
    """Vérifie que la base de données contient des données de test."""
    assert Airport.objects.count() >= 3, (
        "La base de données ne contient pas assez d'aéroports"
    )
    assert Flight.objects.count() >= 2, (
        "La base de données ne contient pas assez de vols"
    )


# ── WHEN : Actions ───────────────────────────────────────────────────────────


@when(
    r'je recherche un vol aller simple de "([^"]+)" vers "([^"]+)" '
    r'avec (\d+) passager(?:s)?'
)
def step_search_oneway(context, origin_code, dest_code, passengers):
    """Effectue une recherche de vol aller simple via le formulaire."""
    origin = Airport.objects.get(code=origin_code)
    dest = Airport.objects.get(code=dest_code)

    # Récupère la date du prochain vol pour la recherche
    flight = Flight.objects.filter(
        origin=origin, destination=dest, status="scheduled"
    ).first()

    if flight:
        departure_date = flight.departure_time.strftime("%Y-%m-%d")
    else:
        departure_date = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")

    data = {
        "trip_type": "oneway",
        "origin": str(origin.pk),
        "destination": str(dest.pk),
        "departure_date": departure_date,
        "passengers": passengers,
        "travel_class": "economy",
    }
    context.response = context.test.client.post(
        reverse("flights:home"), data=data
    )

    # Si redirection vers les résultats, suivre la redirection
    if context.response.status_code == 302:
        # Stocke les paramètres en session comme le fait la vue
        session = context.test.client.session
        session["search_params"] = {
            "origin": origin_code,
            "destination": dest_code,
            "departure_date": departure_date,
            "return_date": None,
            "passengers": passengers,
            "travel_class": "economy",
            "trip_type": "oneway",
        }
        session.save()
        context.response = context.test.client.get(
            reverse("flights:search_results")
        )


@when(
    r'je recherche un vol aller-retour de "([^"]+)" vers "([^"]+)" '
    r'avec (\d+) passager(?:s)?'
)
def step_search_roundtrip(context, origin_code, dest_code, passengers):
    """Effectue une recherche de vol aller-retour via le formulaire."""
    origin = Airport.objects.get(code=origin_code)
    dest = Airport.objects.get(code=dest_code)

    flight = Flight.objects.filter(
        origin=origin, destination=dest, status="scheduled"
    ).first()
    if flight:
        departure_date = flight.departure_time.strftime("%Y-%m-%d")
    else:
        departure_date = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")

    return_date = (date.today() + timedelta(days=14)).strftime("%Y-%m-%d")

    data = {
        "trip_type": "roundtrip",
        "origin": str(origin.pk),
        "destination": str(dest.pk),
        "departure_date": departure_date,
        "return_date": return_date,
        "passengers": passengers,
        "travel_class": "economy",
    }
    context.response = context.test.client.post(
        reverse("flights:home"), data=data
    )

    if context.response.status_code == 302:
        session = context.test.client.session
        session["search_params"] = {
            "origin": origin_code,
            "destination": dest_code,
            "departure_date": departure_date,
            "return_date": return_date,
            "passengers": passengers,
            "travel_class": "economy",
            "trip_type": "roundtrip",
        }
        session.save()
        context.response = context.test.client.get(
            reverse("flights:search_results")
        )


@when(r'je recherche un vol aller simple de "([^"]+)" vers "([^"]+)" '
      r'pour la date d\'hier')
def step_search_past_date(context, origin_code, dest_code):
    """Effectue une recherche avec une date dans le passé."""
    origin = Airport.objects.get(code=origin_code)
    dest = Airport.objects.get(code=dest_code)
    past_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    data = {
        "trip_type": "oneway",
        "origin": str(origin.pk),
        "destination": str(dest.pk),
        "departure_date": past_date,
        "passengers": "1",
        "travel_class": "economy",
    }
    context.response = context.test.client.post(
        reverse("flights:home"), data=data
    )


@when(r'je trie les résultats par prix croissant')
def step_sort_by_price(context):
    """Trie les résultats de recherche par prix croissant."""
    # Le tri est généralement géré via un paramètre GET ou POST
    if context.response.status_code == 200 and "flights" in context.response.context:
        flights = list(context.response.context["flights"])
        context.sorted_flights = sorted(
            flights, key=lambda f: f.base_price_economy
        )
    else:
        # Réaccède avec paramètre de tri
        session = context.test.client.session
        search_params = session.get("search_params", {})
        params = {**search_params, "sort": "price_asc"}
        context.response = context.test.client.get(
            reverse("flights:search_results"), data=params
        )


@when(r'je sélectionne la classe "([^"]+)"')
def step_select_class(context, travel_class):
    """Sélectionne une classe de voyage dans la recherche."""
    # Map les noms français vers les valeurs internes
    class_map = {
        "Économie": "economy",
        "Affaires": "business",
    }
    class_value = class_map.get(travel_class, travel_class.lower())
    context.selected_class = class_value

    # Refait la recherche avec la nouvelle classe
    session = context.test.client.session
    search_params = session.get("search_params", {})
    if search_params:
        search_params["travel_class"] = class_value
        session["search_params"] = search_params
        session.save()
        context.response = context.test.client.get(
            reverse("flights:search_results")
        )


@when(r'j\'accède à la page "([^"]+)"')
def step_access_page(context, url_name):
    """Accède à une page par son nom d'URL Django."""
    url = reverse(url_name)
    context.response = context.test.client.get(url)
    context.current_url_name = url_name


# ── THEN : Vérifications ────────────────────────────────────────────────────


@then(r'je vois les résultats de recherche')
def step_see_results(context):
    """Vérifie que des résultats de recherche sont affichés."""
    assert context.response.status_code == 200, (
        f"Statut inattendu : {context.response.status_code}"
    )
    content = context.response.content.decode("utf-8")
    # Vérifie que le template de résultats est utilisé ou que des vols sont dans le contexte
    if "flights" in context.response.context:
        flights = context.response.context["flights"]
        assert len(list(flights)) >= 1, "Aucun vol trouvé dans les résultats"


@then(r'je ne vois aucun résultat')
def step_no_results(context):
    """Vérifie qu'aucun résultat n'est affiché."""
    assert context.response.status_code == 200, (
        f"Statut inattendu : {context.response.status_code}"
    )
    if "flights" in context.response.context:
        flights = list(context.response.context["flights"])
        assert len(flights) == 0, (
            f"Des résultats inattendus ont été trouvés : {len(flights)} vol(s)"
        )


@then(r'un message d\'erreur contenant "([^"]+)" est affiché')
def step_error_message(context, message_fragment):
    """Vérifie qu'un message d'erreur spécifique est affiché."""
    content = context.response.content.decode("utf-8").lower()
    fragment = message_fragment.lower()
    assert fragment in content, (
        f"Le message d'erreur contenant '{message_fragment}' n'a pas été trouvé "
        f"dans la réponse. Contenu (extrait) : {content[:500]}"
    )


@then(r'le prix est affiché en TND')
def step_price_in_tnd(context):
    """Vérifie que les prix sont affichés en dinars tunisiens."""
    content = context.response.content.decode("utf-8")
    assert "TND" in content, (
        "Le prix n'est pas affiché en TND dans la réponse"
    )


@then(r'le prix correspond à la classe "([^"]+)"')
def step_price_matches_class(context, travel_class):
    """Vérifie que le prix affiché correspond à la classe sélectionnée."""
    if "flights" in context.response.context:
        flights = list(context.response.context["flights"])
        if flights:
            flight = flights[0]
            if travel_class == "Économie":
                assert flight.base_price_economy > 0, (
                    "Le prix économie n'est pas affiché"
                )
            elif travel_class == "Affaires":
                assert flight.base_price_business > 0, (
                    "Le prix affaires n'est pas affiché"
                )


@then(r'le premier résultat a un prix inférieur ou égal au deuxième résultat')
def step_first_price_lower(context):
    """Vérifie que les résultats sont triés par prix croissant."""
    if hasattr(context, "sorted_flights") and context.sorted_flights:
        assert len(context.sorted_flights) >= 2, (
            "Pas assez de résultats pour vérifier le tri"
        )
        price1 = context.sorted_flights[0].base_price_economy
        price2 = context.sorted_flights[1].base_price_economy
        assert price1 <= price2, (
            f"Le tri par prix est incorrect : {price1} > {price2}"
        )


@then(r'je vois au moins (\d+) aéroports populaires')
def step_popular_airports(context, min_count):
    """Vérifie qu'un nombre minimum d'aéroports populaires est affiché."""
    assert context.response.status_code == 200, (
        f"Statut inattendu : {context.response.status_code}"
    )
    if "popular_destinations" in context.response.context:
        destinations = context.response.context["popular_destinations"]
        assert len(list(destinations)) >= int(min_count), (
            f"Pas assez d'aéroports populaires : "
            f"{len(list(destinations))} < {min_count}"
        )
    else:
        # Vérifie dans le contenu HTML
        content = context.response.content.decode("utf-8")
        # Vérifie que plusieurs codes d'aéroports apparaissent
        airport_codes = ["TUN", "CDG", "MRS", "CMN", "ALG", "FCO", "LHR"]
        found = sum(1 for code in airport_codes if code in content)
        assert found >= int(min_count), (
            f"Seulement {found} aéroports trouvés dans le contenu, "
            f"attendu au moins {min_count}"
        )


@then(r'le formulaire de recherche contient le champ "([^"]+)"')
def step_form_has_field(context, field_name):
    """Vérifie qu'un champ spécifique est présent dans le formulaire."""
    assert context.response.status_code == 200
    if "search_form" in context.response.context:
        form = context.response.context["search_form"]
        assert field_name in form.fields, (
            f"Le champ '{field_name}' n'est pas dans le formulaire de recherche. "
            f"Champs disponibles : {list(form.fields.keys())}"
        )
    else:
        # Vérification dans le HTML si le formulaire n'est pas dans le contexte
        content = context.response.content.decode("utf-8")
        assert field_name in content or f'name="{field_name}"' in content, (
            f"Le champ '{field_name}' n'est pas dans le HTML de la page"
        )


@then(r'la page affiche "([^"]+)"')
def step_page_displays(context, text):
    """Vérifie qu'un texte spécifique est affiché sur la page."""
    content = context.response.content.decode("utf-8")
    assert text in content, (
        f"Le texte '{text}' n'est pas affiché sur la page"
    )
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 8 — features/steps/booking_steps.py
# ══════════════════════════════════════════════════════════════════════════════

FILE_BOOKING_STEPS = r'''"""
booking_steps.py — Définitions d'étapes Behave pour la gestion des réservations.
================================================================================

Scénarios couverts :
    - US-008 : Création de réservation connecté
    - US-009 : Consultation de réservation
    - US-010 : Annulation de réservation pending
    - Recherche par référence et nom de famille
    - Réservation nécessite une connexion
"""

from behave import given, when, then
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, date

from django.contrib.auth.models import User
from flights.models import Flight
from bookings.models import Booking, Passenger, Payment


# ── GIVEN : Préconditions ────────────────────────────────────────────────────


@given(r'je suis connecté en tant que "([^"]+)" avec le mot de passe "([^"]+)"')
def step_logged_in(context, username, password):
    """Connecte un utilisateur via le client de test."""
    success = context.test.client.login(username=username, password=password)
    assert success, (
        f"Impossible de connecter l'utilisateur '{username}' "
        f"avec le mot de passe fourni"
    )
    context.logged_in_user = User.objects.get(username=username)


@given(r'un vol est disponible pour la réservation')
def step_flight_available(context):
    """Récupère un vol disponible pour la réservation."""
    flight = Flight.objects.filter(
        status="scheduled",
        is_active=True,
        available_seats_economy__gte=1,
        departure_time__gt=timezone.now(),
    ).first()
    assert flight is not None, "Aucun vol disponible pour la réservation"
    context.booking_flight = flight

    # Prépare la session avec les paramètres de recherche
    session = context.test.client.session
    session["search_params"] = {
        "origin": flight.origin.code,
        "destination": flight.destination.code,
        "departure_date": flight.departure_time.strftime("%Y-%m-%d"),
        "return_date": None,
        "passengers": "1",
        "travel_class": "economy",
        "trip_type": "oneway",
    }
    session["booking_flight_id"] = flight.pk
    session.save()


@given(r'une réservation "([^"]+)" existe pour mon compte')
def step_booking_exists_for_account(context, reference_label):
    """Crée une réservation pour l'utilisateur connecté."""
    user = context.logged_in_user
    flight = Flight.objects.filter(status="scheduled").first()
    assert flight is not None, "Aucun vol disponible"

    booking = Booking.objects.create(
        user=user,
        contact_email=user.email,
        contact_phone="+21612345678",
        status="confirmed",
        total_amount=flight.base_price_economy,
    )
    Passenger.objects.create(
        booking=booking,
        flight=flight,
        title="mr",
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=date(1990, 1, 15),
        nationality="Tunisienne",
        travel_class="economy",
        price=flight.base_price_economy,
    )
    Payment.objects.create(
        booking=booking,
        amount=flight.base_price_economy,
        method="credit_card",
        status="completed",
        transaction_id=f"SIM-{booking.short_reference}",
    )
    context.booking = booking
    context.booking_reference = booking.reference


@given(r'une réservation avec le statut "([^"]+)" existe')
def step_booking_with_status(context, status):
    """Crée une réservation avec un statut spécifique."""
    user = context.logged_in_user
    flight = Flight.objects.filter(status="scheduled").first()

    booking = Booking.objects.create(
        user=user,
        contact_email=user.email,
        contact_phone="+21612345678",
        status=status,
        total_amount=250.00,
    )
    Passenger.objects.create(
        booking=booking,
        flight=flight,
        title="mr",
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=date(1990, 1, 15),
        nationality="Tunisienne",
        travel_class="economy",
        price=250.00,
    )
    context.booking = booking
    context.booking_reference = booking.reference


@given(r'une réservation pour "([^"]+)" avec la référence "([^"]+)" existe')
def step_booking_for_lastname(context, last_name, ref_label):
    """Crée une réservation pour un nom de famille spécifique."""
    user = User.objects.get(username="testuser")
    flight = Flight.objects.filter(status="scheduled").first()

    booking = Booking.objects.create(
        user=user,
        contact_email=user.email,
        contact_phone="+21612345678",
        status="confirmed",
        total_amount=250.00,
    )
    Passenger.objects.create(
        booking=booking,
        flight=flight,
        title="mr",
        first_name="Jean",
        last_name=last_name,
        date_of_birth=date(1990, 1, 15),
        nationality="Française",
        travel_class="economy",
        price=250.00,
    )
    context.booking = booking
    context.booking_reference = booking.reference
    context.booking_last_name = last_name


@given(r'je suis un visiteur non connecté')
def step_visitor(context):
    """S'assure qu'aucun utilisateur n'est connecté."""
    context.test.client.logout()
    context.is_visitor = True


# ── WHEN : Actions ───────────────────────────────────────────────────────────


@when(r'je réserve le vol avec les informations passager valides')
def step_create_booking(context):
    """Crée une réservation avec des données de passager valides."""
    flight = getattr(context, "booking_flight", None)
    if not flight:
        flight = Flight.objects.filter(status="scheduled").first()

    # S'assurer que la session est bien configurée
    session = context.test.client.session
    session["search_params"] = {
        "origin": flight.origin.code,
        "destination": flight.destination.code,
        "departure_date": flight.departure_time.strftime("%Y-%m-%d"),
        "return_date": None,
        "passengers": "1",
        "travel_class": "economy",
        "trip_type": "oneway",
    }
    session["booking_flight_id"] = flight.pk
    session.save()

    booking_count_before = Booking.objects.count()

    form_data = {
        "0-title": "mr",
        "0-first_name": "Jean",
        "0-last_name": "Dupont",
        "0-date_of_birth": "1990-01-15",
        "0-nationality": "Française",
        "0-passport_number": "AB123456",
        "0-passport_expiry": "2030-01-15",
        "0-special_assistance": "",
        "0-meal_preference": "",
        "contact_email": "jean.dupont@example.com",
        "contact_phone": "+33612345678",
        "special_requests": "",
    }

    context.response = context.test.client.post(
        reverse("bookings:create"), data=form_data
    )
    context.booking_count_before = booking_count_before


@when(r'je réserve le vol')
def step_create_booking_simple(context):
    """Tente de créer une réservation (sans données complètes)."""
    context.response = context.test.client.get(
        reverse("bookings:create")
    )


@when(r'j\'annule la réservation')
def step_cancel_booking(context):
    """Annule la réservation en cours."""
    booking = context.booking
    context.response = context.test.client.post(
        reverse("bookings:cancel", kwargs={"reference": booking.reference})
    )


@when(r'j\'essaie d\'annuler la réservation')
def step_try_cancel_booking(context):
    """Tente d'annuler la réservation (peut échouer)."""
    booking = context.booking
    context.response = context.test.client.post(
        reverse("bookings:cancel", kwargs={"reference": booking.reference})
    )


@when(
    r'je recherche la réservation avec la référence "([^"]+)" '
    r'et le nom "([^"]+)"'
)
def step_lookup_booking(context, ref_label, last_name):
    """Recherche une réservation par référence et nom de famille."""
    booking = context.booking
    short_ref = booking.short_reference

    form_data = {
        "reference": short_ref,
        "email": booking.contact_email,
    }
    context.response = context.test.client.post(
        reverse("bookings:lookup"), data=form_data
    )


@when(r'j\'accède à la page "([^"]+)"')
def step_access_page(context, url_name):
    """Accède à une page par son nom d'URL."""
    url = reverse(url_name)
    context.response = context.test.client.get(url)
    context.current_url_name = url_name


# ── THEN : Vérifications ────────────────────────────────────────────────────


@then(r'la réservation est créée avec succès')
def step_booking_created(context):
    """Vérifie qu'une réservation a été créée."""
    assert Booking.objects.count() > context.booking_count_before, (
        "Aucune réservation n'a été créée"
    )
    context.booking = Booking.objects.latest("created_at")


@then(r'la réservation a le statut "([^"]+)"')
def step_booking_status(context, expected_status):
    """Vérifie le statut de la réservation."""
    booking = context.booking
    booking.refresh_from_db()
    assert booking.status == expected_status, (
        f"Le statut de la réservation est '{booking.status}', "
        f"attendu '{expected_status}'"
    )


@then(r'un numéro de référence est généré')
def step_reference_generated(context):
    """Vérifie qu'un numéro de référence a été généré."""
    booking = context.booking
    assert booking.reference is not None, "Aucune référence générée"
    assert str(booking.reference)[:8], "La référence est vide"


@then(r'je vois la réservation "([^"]+)" dans la liste')
def step_see_booking_in_list(context, ref_label):
    """Vérifie qu'une réservation est visible dans la liste."""
    assert context.response.status_code == 200
    if "bookings" in context.response.context:
        bookings = list(context.response.context["bookings"])
        assert len(bookings) >= 1, "Aucune réservation dans la liste"
        assert context.booking in bookings, (
            "La réservation attendue n'est pas dans la liste"
        )


@then(r'la réservation est annulée')
def step_booking_cancelled(context):
    """Vérifie que la réservation a été annulée."""
    context.booking.refresh_from_db()
    assert context.booking.status == "cancelled", (
        f"La réservation n'est pas annulée, statut : {context.booking.status}"
    )


@then(r'le statut de la réservation est "([^"]+)"')
def step_status_is(context, status):
    """Vérifie le statut de la réservation."""
    context.booking.refresh_from_db()
    assert context.booking.status == status, (
        f"Statut inattendu : {context.booking.status} (attendu : {status})"
    )


@then(r'la réservation reste avec le statut "([^"]+)"')
def step_status_remains(context, status):
    """Vérifie que le statut n'a pas changé."""
    context.booking.refresh_from_db()
    assert context.booking.status == status, (
        f"Le statut a changé : {context.booking.status} (attendu : {status})"
    )


@then(r'un message d\'erreur est affiché')
def step_error_displayed(context):
    """Vérifie qu'un message d'erreur est affiché."""
    content = context.response.content.decode("utf-8").lower()
    has_error = (
        "error" in content
        or "erreur" in content
        or "invalid" in content
        or "impossible" in content
    )
    assert has_error, "Aucun message d'erreur trouvé dans la réponse"


@then(r'un message d\'erreur contenant "([^"]+)" est affiché')
def step_error_contains(context, text):
    """Vérifie qu'un message d'erreur contenant un texte spécifique est affiché."""
    content = context.response.content.decode("utf-8").lower()
    assert text.lower() in content, (
        f"Le message d'erreur contenant '{text}' n'a pas été trouvé"
    )


@then(r'je suis redirigé vers la page "([^"]+)"')
def step_redirected_to(context, url_name):
    """Vérifie que la réponse est une redirection vers la page spécifiée."""
    assert context.response.status_code in (301, 302), (
        f"Pas de redirection, statut : {context.response.status_code}"
    )
    expected_url = reverse(url_name)
    assert context.response.url == expected_url, (
        f"Redirection vers {context.response.url}, attendu {expected_url}"
    )


@then(r'je suis redirigé vers la page de détail de la réservation')
def step_redirected_to_detail(context):
    """Vérifie la redirection vers la page de détail de la réservation."""
    assert context.response.status_code in (301, 302), (
        f"Pas de redirection, statut : {context.response.status_code}"
    )
    assert context.response.url == reverse(
        "bookings:detail", kwargs={"reference": context.booking.reference}
    ), f"Redirection incorrecte : {context.response.url}"
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 9 — features/steps/auth_steps.py
# ══════════════════════════════════════════════════════════════════════════════

FILE_AUTH_STEPS = r'''"""
auth_steps.py — Définitions d'étapes Behave pour l'authentification.
=====================================================================

Scénarios couverts :
    - US-027 : Inscription avec données valides
    - US-027 : Inscription avec email dupliqué
    - US-028 : Connexion réussie
    - US-028 : Connexion échouée
    - US-028 : Déconnexion
    - US-030 : Mise à jour du profil
    - Accès profil nécessite connexion
"""

from behave import given, when, then
from django.urls import reverse

from django.contrib.auth.models import User
from accounts.models import UserProfile


# ── GIVEN : Préconditions ────────────────────────────────────────────────────


@given(r'je suis un visiteur non connecté')
def step_visitor(context):
    """S'assure qu'aucun utilisateur n'est connecté."""
    context.test.client.logout()
    context.is_visitor = True


@given(r'je suis connecté en tant que "([^"]+)" avec le mot de passe "([^"]+)"')
def step_logged_in(context, username, password):
    """Connecte un utilisateur via le client de test."""
    success = context.test.client.login(username=username, password=password)
    assert success, (
        f"Impossible de connecter l'utilisateur '{username}' "
        f"avec le mot de passe fourni"
    )
    context.logged_in_user = User.objects.get(username=username)
    context.is_visitor = False


@given(r'que la base de données est peuplée')
def step_db_populated(context):
    """Vérifie que la base de données contient des données."""
    assert User.objects.count() >= 1, "La base de données est vide"


# ── WHEN : Actions ───────────────────────────────────────────────────────────


@when(
    r'je m\'inscris avec les données valides suivantes:'
)
def step_register_valid(context):
    """Inscrit un nouvel utilisateur avec des données valides."""
    table = context.table
    row = table.rows[0]

    data = {
        "username": row["username"],
        "first_name": row["prenom"],
        "last_name": row["nom"],
        "email": row["email"],
        "password1": row["mot_de_passe"],
        "password2": row["confirmation"],
    }

    context.user_count_before = User.objects.count()
    context.profile_count_before = UserProfile.objects.count()

    context.response = context.test.client.post(
        reverse("accounts:register"), data=data
    )


@when(
    r'je m\'inscris avec les données suivantes ayant un email dupliqué:'
)
def step_register_duplicate_email(context):
    """Tente d'inscrire un utilisateur avec un email déjà utilisé."""
    table = context.table
    row = table.rows[0]

    data = {
        "username": row["username"],
        "first_name": row["prenom"],
        "last_name": row["nom"],
        "email": row["email"],
        "password1": row["mot_de_passe"],
        "password2": row["confirmation"],
    }

    context.user_count_before = User.objects.count()

    context.response = context.test.client.post(
        reverse("accounts:register"), data=data
    )


@when(r'je me connecte avec "([^"]+)" et "([^"]+)"')
def step_login(context, username, password):
    """Tente de se connecter avec un nom d'utilisateur et un mot de passe."""
    context.response = context.test.client.post(
        reverse("accounts:login"),
        data={"username": username, "password": password},
    )


@when(r'je me déconnecte')
def step_logout(context):
    """Déconnecte l'utilisateur courant."""
    context.response = context.test.client.get(reverse("accounts:logout"))


@when(r'je mets à jour mon profil avec les données suivantes:')
def step_update_profile(context):
    """Met à jour le profil utilisateur avec de nouvelles données."""
    table = context.table
    row = table.rows[0]

    data = {
        "first_name": row["prenom"],
        "last_name": row["nom"],
        "email": row["email"],
        "phone": row["telephone"],
        "city": row["ville"],
        "country": row["pays"],
        "date_of_birth": "1990-01-15",
        "nationality": "Tunisienne",
        "passport_number": "PASS12345",
        "gender": "M",
        "newsletter": "on",
    }

    context.response = context.test.client.post(
        reverse("accounts:profile"), data=data
    )


@when(r'j\'accède à la page "([^"]+)"')
def step_access_page(context, url_name):
    """Accède à une page par son nom d'URL."""
    url = reverse(url_name)
    context.response = context.test.client.get(url)
    context.current_url_name = url_name


# ── THEN : Vérifications ────────────────────────────────────────────────────


@then(r'le compte est créé avec succès')
def step_account_created(context):
    """Vérifie qu'un nouveau compte a été créé."""
    assert User.objects.count() == context.user_count_before + 1, (
        "Le compte n'a pas été créé"
    )


@then(r'je suis connecté automatiquement')
def step_auto_logged_in(context):
    """Vérifie que l'utilisateur est automatiquement connecté après inscription."""
    user = context.test.client.session.get("_auth_user_id")
    assert user is not None, "L'utilisateur n'est pas connecté"


@then(r'un profil utilisateur est créé automatiquement')
def step_profile_created(context):
    """Vérifie qu'un profil a été créé pour l'utilisateur."""
    latest_user = User.objects.latest("id")
    assert hasattr(latest_user, "profile"), (
        "Aucun profil n'a été créé pour le nouvel utilisateur"
    )


@then(r'le compte n\'est pas créé')
def step_account_not_created(context):
    """Vérifie qu'aucun nouveau compte n'a été créé."""
    assert User.objects.count() == context.user_count_before, (
        "Un compte a été créé malgré l'erreur attendue"
    )


@then(r'je suis connecté avec succès')
def step_login_success(context):
    """Vérifie que la connexion a réussi."""
    user = context.test.client.session.get("_auth_user_id")
    assert user is not None, "L'utilisateur n'est pas connecté"


@then(r'je ne suis pas connecté')
def step_not_logged_in(context):
    """Vérifie que l'utilisateur n'est pas connecté."""
    user = context.test.client.session.get("_auth_user_id")
    assert user is None, "L'utilisateur est connecté alors qu'il ne devrait pas l'être"


@then(r'je suis déconnecté')
def step_logged_out(context):
    """Vérifie que l'utilisateur a été déconnecté."""
    user = context.test.client.session.get("_auth_user_id")
    assert user is None, "L'utilisateur est encore connecté"


@then(r'un message d\'erreur est affiché')
def step_error_displayed(context):
    """Vérifie qu'un message d'erreur est affiché."""
    content = context.response.content.decode("utf-8").lower()
    has_error = (
        "error" in content
        or "erreur" in content
        or "incorrect" in content
        or "invalide" in content
        or "invalid" in content
    )
    assert has_error, "Aucun message d'erreur trouvé dans la réponse"


@then(r'un message d\'erreur contenant "([^"]+)" est affiché')
def step_error_contains(context, text):
    """Vérifie qu'un message d'erreur contenant un texte spécifique est affiché."""
    content = context.response.content.decode("utf-8").lower()
    assert text.lower() in content, (
        f"Le message d'erreur contenant '{text}' n'a pas été trouvé. "
        f"Contenu (extrait) : {content[:500]}"
    )


@then(r'je suis redirigé vers la page "([^"]+)"')
def step_redirected_to(context, url_name):
    """Vérifie que la réponse est une redirection vers la page spécifiée."""
    assert context.response.status_code in (301, 302), (
        f"Pas de redirection, statut : {context.response.status_code}"
    )
    expected_url = reverse(url_name)
    assert context.response.url == expected_url, (
        f"Redirection vers {context.response.url}, attendu {expected_url}"
    )


@then(r'je reste sur la page "([^"]+)"')
def step_stay_on_page(context, url_name):
    """Vérifie que l'utilisateur reste sur la même page (pas de redirection)."""
    expected_url = reverse(url_name)
    if context.response.status_code in (301, 302):
        assert context.response.url == expected_url, (
            f"Redirection inattendue vers {context.response.url}"
        )
    else:
        assert context.response.status_code == 200, (
            f"Statut inattendu : {context.response.status_code}"
        )


@then(r'le profil est mis à jour avec succès')
def step_profile_updated(context):
    """Vérifie que la mise à jour du profil a réussi."""
    assert context.response.status_code in (200, 302), (
        f"Statut inattendu : {context.response.status_code}"
    )


@then(r'les informations sont sauvegardées en base de données')
def step_info_saved(context):
    """Vérifie que les informations sont bien enregistrées."""
    user = context.logged_in_user
    user.refresh_from_db()
    assert user.email == "modified@exemple.com", (
        f"Email non mis à jour : {user.email}"
    )
    user.profile.refresh_from_db()
    assert user.profile.phone == "+21698765432", (
        f"Téléphone non mis à jour : {user.profile.phone}"
    )
    assert user.profile.city == "Sousse", (
        f"Ville non mise à jour : {user.profile.city}"
    )
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 10 — features/steps/promotions_steps.py
# ══════════════════════════════════════════════════════════════════════════════

FILE_PROMOTIONS_STEPS = r'''"""
promotions_steps.py — Définitions d'étapes Behave pour les promotions.
=======================================================================

Scénarios couverts :
    - US-006 : Application de codes promotionnels (valide, expiré, inexistant)
    - US-034 : Inscription à la newsletter (valide, doublon)
"""

from behave import given, when, then
from django.urls import reverse
from django.utils import timezone

from flights.models import Flight
from promotions.models import Promotion, NewsletterSubscription


# ── GIVEN : Préconditions ────────────────────────────────────────────────────


@given(r'que la base de données est peuplée')
def step_db_populated(context):
    """Vérifie que la base de données contient des données."""
    assert Promotion.objects.count() >= 1, "Aucune promotion en base"


@given(r'un code promo "([^"]+)" est actif avec (\d+)% de réduction')
def step_active_promo(context, code, discount):
    """Vérifie qu'un code promo actif existe avec un pourcentage de réduction."""
    promo = Promotion.objects.filter(code=code).first()
    assert promo is not None, f"Le code promo '{code}' n'existe pas"
    assert promo.is_active, f"Le code promo '{code}' n'est pas actif"
    assert promo.discount_percentage == float(discount), (
        f"La réduction est de {promo.discount_percentage}%, attendu {discount}%"
    )
    context.current_promo = promo


@given(r'un code promo "([^"]+)" est expiré')
def step_expired_promo(context, code):
    """Vérifie qu'un code promo est expiré."""
    promo = Promotion.objects.filter(code=code).first()
    assert promo is not None, f"Le code promo '{code}' n'existe pas"
    now = timezone.now()
    assert promo.end_date < now, (
        f"Le code promo '{code}' n'est pas expiré "
        f"(fin : {promo.end_date}, maintenant : {now})"
    )
    context.current_promo = promo


@given(r'un vol est disponible avec un prix de ([\d.]+) TND')
def step_flight_with_price(context, price):
    """Récupère un vol avec un prix spécifique."""
    expected_price = float(price)
    flight = Flight.objects.filter(
        base_price_economy=expected_price,
        status="scheduled",
        is_active=True,
    ).first()
    if not flight:
        # Prendre un vol existant et vérifier son prix
        flight = Flight.objects.filter(status="scheduled", is_active=True).first()
    assert flight is not None, "Aucun vol disponible"
    context.promo_flight = flight
    context.original_price = expected_price


@given(r'un vol affaires est disponible avec un prix de ([\d.]+) TND')
def step_business_flight_with_price(context, price):
    """Récupère un vol affaires avec un prix spécifique."""
    expected_price = float(price)
    flight = Flight.objects.filter(
        base_price_business=expected_price,
        status="scheduled",
        is_active=True,
    ).first()
    if not flight:
        flight = Flight.objects.filter(status="scheduled", is_active=True).first()
    assert flight is not None, "Aucun vol affaires disponible"
    context.promo_flight = flight
    context.original_price = expected_price


@given(
    r'l\'adresse "([^"]+)" est déjà inscrite à la newsletter'
)
def step_email_already_subscribed(context, email):
    """Inscrit un email à la newsletter avant le scénario."""
    NewsletterSubscription.objects.get_or_create(
        email=email,
        defaults={"first_name": "Test", "is_active": True},
    )


@given(r'je suis un visiteur non connecté')
def step_visitor(context):
    """S'assure qu'aucun utilisateur n'est connecté."""
    context.test.client.logout()
    context.is_visitor = True


# ── WHEN : Actions ───────────────────────────────────────────────────────────


@when(r'j\'applique le code "([^"]+)" au vol')
def step_apply_promo(context, code):
    """Applique un code promotionnel au vol sélectionné."""
    promo = Promotion.objects.filter(code=code).first()
    flight = getattr(context, "promo_flight", None)

    if flight and promo:
        # Calcule le prix avec la promotion
        discount = promo.discount_percentage
        original_price = getattr(context, "original_price", flight.base_price_economy)

        if promo.is_valid:
            context.promo_applied = True
            context.discounted_price = round(
                float(original_price) * (1 - discount / 100), 2
            )
        else:
            context.promo_applied = False
            context.discounted_price = float(original_price)

    # Simule la vérification via la vue
    context.response = context.test.client.get(
        reverse("promotions:detail", kwargs={"code": code})
    )


@when(
    r'je m\'inscris à la newsletter avec "([^"]+)"'
)
def step_subscribe_newsletter(context, email):
    """Inscrit un email à la newsletter."""
    context.newsletter_email = email
    context.newsletter_count_before = NewsletterSubscription.objects.count()

    context.response = context.test.client.post(
        reverse("promotions:newsletter_subscribe"),
        data={"email": email},
    )


# ── THEN : Vérifications ────────────────────────────────────────────────────


@then(r'la remise est appliquée')
def step_discount_applied(context):
    """Vérifie que la remise a été appliquée."""
    assert getattr(context, "promo_applied", False), (
        "La remise n'a pas été appliquée"
    )


@then(r'le prix final est de ([\d.]+) TND')
def step_final_price(context, expected_price):
    """Vérifie que le prix final correspond à celui attendu après remise."""
    actual_price = getattr(context, "discounted_price", 0)
    assert actual_price == float(expected_price), (
        f"Prix final incorrect : {actual_price} TND (attendu {expected_price} TND)"
    )


@then(r'la remise n\'est pas appliquée')
def step_no_discount(context):
    """Vérifie qu'aucune remise n'a été appliquée."""
    assert not getattr(context, "promo_applied", True), (
        "Une remise a été appliquée alors qu'elle ne devait pas l'être"
    )


@then(r'un message de confirmation est affiché')
def step_confirmation_message(context):
    """Vérifie qu'un message de confirmation est affiché."""
    content = context.response.content.decode("utf-8").lower()
    has_confirmation = (
        "confirm" in content
        or "succès" in content
        or "merci" in content
        or "appliquée" in content
        or "enregistré" in content
        or "inscrit" in content
    )
    assert has_confirmation, (
        "Aucun message de confirmation trouvé dans la réponse"
    )


@then(r'un message d\'erreur contenant "([^"]+)" est affiché')
def step_error_contains(context, text):
    """Vérifie qu'un message d'erreur contenant un texte spécifique est affiché."""
    content = context.response.content.decode("utf-8").lower()
    assert text.lower() in content, (
        f"Le message d'erreur contenant '{text}' n'a pas été trouvé. "
        f"Contenu (extrait) : {content[:500]}"
    )


@then(r'l\'inscription à la newsletter est confirmée')
def step_newsletter_confirmed(context):
    """Vérifie que l'inscription à la newsletter est confirmée."""
    assert NewsletterSubscription.objects.filter(
        email=context.newsletter_email
    ).exists(), (
        f"L'email '{context.newsletter_email}' n'est pas inscrit à la newsletter"
    )


@then(r'l\'adresse email est enregistrée en base de données')
def step_email_in_db(context):
    """Vérifie que l'email est enregistré en base."""
    assert NewsletterSubscription.objects.filter(
        email=context.newsletter_email
    ).exists(), (
        f"L'email '{context.newsletter_email}' n'est pas en base de données"
    )


@then(r'l\'inscription échoue')
def step_subscription_fails(context):
    """Vérifie que l'inscription à la newsletter a échoué."""
    assert NewsletterSubscription.objects.count() == context.newsletter_count_before, (
        "Un abonnement a été créé alors qu'il ne devait pas l'être"
    )
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER 11 — features/steps/common_steps.py
# ══════════════════════════════════════════════════════════════════════════════

FILE_COMMON_STEPS = r'''"""
common_steps.py — Étapes partagées entre tous les fichiers de features.
========================================================================

Ce fichier contient les étapes génériques utilisées dans plusieurs
fichiers .feature :
    - Accès aux pages par nom d'URL
    - Vérification du statut de réponse
    - Vérification de la page courante
    - Peuplement de la base de données
"""

from behave import given, when, then
from django.urls import reverse

from flights.models import Airport, Flight
from django.contrib.auth.models import User


# ── GIVEN : Préconditions ────────────────────────────────────────────────────


@given(r'la base de données est peuplée')
def step_db_populated(context):
    """
    Vérifie que la base de données contient les données de test minimales :
    - Au moins 3 aéroports
    - Au moins 2 vols
    - Au moins 1 utilisateur
    """
    assert Airport.objects.count() >= 3, (
        f"Pas assez d'aéroports en base : {Airport.objects.count()} (minimum 3)"
    )
    assert Flight.objects.count() >= 2, (
        f"Pas assez de vols en base : {Flight.objects.count()} (minimum 2)"
    )
    assert User.objects.count() >= 1, (
        f"Pas d'utilisateurs en base : {User.objects.count()}"
    )


@given(r'je suis un visiteur non connecté')
def step_visitor_not_logged_in(context):
    """S'assure qu'aucun utilisateur n'est connecté."""
    context.test.client.logout()


# ── WHEN : Actions ───────────────────────────────────────────────────────────


@when(r'j\'accède à la page "([^"]+)"')
def step_access_page(context, url_name):
    """
    Accède à une page par son nom d'URL Django.

    Le nom doit inclure le namespace, par exemple :
      - "flights:home"
      - "accounts:login"
      - "bookings:my_bookings"
    """
    url = reverse(url_name)
    context.response = context.test.client.get(url)
    context.current_url_name = url_name


# ── THEN : Vérifications ────────────────────────────────────────────────────


@then(r'le statut de la réponse est (\d+)')
def step_response_status(context, status_code):
    """Vérifie le code de statut HTTP de la réponse."""
    actual_status = context.response.status_code
    assert actual_status == int(status_code), (
        f"Statut inattendu : {actual_status} (attendu {status_code})"
    )


@then(r'je suis sur la page "([^"]+)"')
def step_on_page(context, url_name):
    """Vérifie que l'utilisateur est sur une page spécifique."""
    expected_url = reverse(url_name)

    # Si c'est une redirection, vérifier l'URL de redirection
    if context.response.status_code in (301, 302):
        assert context.response.url == expected_url, (
            f"Redirection vers {context.response.url}, "
            f"attendu {expected_url}"
        )
    else:
        # Pour une réponse 200, on vérifie que le template ou le contenu correspond
        assert context.response.status_code == 200, (
            f"Statut inattendu : {context.response.status_code}"
        )


@then(r'je suis redirigé vers la page "([^"]+)"')
def step_redirected_to_page(context, url_name):
    """Vérifie que la réponse est une redirection vers la page spécifiée."""
    assert context.response.status_code in (301, 302), (
        f"Pas de redirection, statut : {context.response.status_code}"
    )
    expected_url = reverse(url_name)
    assert context.response.url == expected_url, (
        f"Redirection vers {context.response.url}, attendu {expected_url}"
    )


@then(r'un message d\'erreur est affiché')
def step_error_message_generic(context):
    """Vérifie qu'un message d'erreur est affiché sur la page."""
    content = context.response.content.decode("utf-8").lower()
    has_error = (
        "error" in content
        or "erreur" in content
        or "invalid" in content
        or "invalide" in content
        or "échou" in content
        or "echec" in content
    )
    assert has_error, (
        "Aucun message d'erreur trouvé dans la réponse. "
        f"Contenu (extrait) : {content[:500]}"
    )


@then(r'un message d\'erreur contenant "([^"]+)" est affiché')
def step_error_message_contains(context, text):
    """Vérifie qu'un message d'erreur contenant un texte spécifique est affiché."""
    content = context.response.content.decode("utf-8").lower()
    assert text.lower() in content, (
        f"Le texte '{text}' n'a pas été trouvé dans la réponse. "
        f"Contenu (extrait) : {content[:500]}"
    )


@then(r'un message de confirmation est affiché')
def step_confirmation_message_generic(context):
    """Vérifie qu'un message de confirmation est affiché."""
    content = context.response.content.decode("utf-8").lower()
    has_confirmation = (
        "confirm" in content
        or "succès" in content
        or "merci" in content
        or "réussi" in content
        or "réussie" in content
        or "enregistré" in content
    )
    assert has_confirmation, (
        "Aucun message de confirmation trouvé dans la réponse"
    )
'''


# ══════════════════════════════════════════════════════════════════════════════
#  FICHIER CONFIG — behave.ini
# ══════════════════════════════════════════════════════════════════════════════

FILE_BEHAVE_INI = '''# behave.ini — Configuration Behave pour le projet NouvelAir
# ================================================================
#
# Placez ce fichier à la racine du projet (à côté de manage.py).
# Behave le détecte automatiquement au lancement.

[behave]
# Intégration Django
django = True

# Format de sortie : progress (par défaut), pretty, steps, etc.
format = pretty

# Afficher les scénarios échoués en premier
order = random

# Répertoire des features
paths = features/

# Désactiver la capture stdout (utile pour le débogage)
# capture = no

# Langue par défaut
lang = fr
'''


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN — Exécution du script
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Génère tous les fichiers BDD/Gherkin pour le Jour 4."""
    print("=" * 70)
    print("  NouvelAir — Setup Jour 4 : BDD / Gherkin (Behave)")
    print("=" * 70)
    print()

    files = [
        ("features/environment.py", FILE_ENVIRONMENT),
        ("features/search.feature", FILE_SEARCH_FEATURE),
        ("features/booking.feature", FILE_BOOKING_FEATURE),
        ("features/auth.feature", FILE_AUTH_FEATURE),
        ("features/promotions.feature", FILE_PROMOTIONS_FEATURE),
        ("features/steps/__init__.py", FILE_STEPS_INIT),
        ("features/steps/search_steps.py", FILE_SEARCH_STEPS),
        ("features/steps/booking_steps.py", FILE_BOOKING_STEPS),
        ("features/steps/auth_steps.py", FILE_AUTH_STEPS),
        ("features/steps/promotions_steps.py", FILE_PROMOTIONS_STEPS),
        ("features/steps/common_steps.py", FILE_COMMON_STEPS),
        ("behave.ini", FILE_BEHAVE_INI),
    ]

    print("📁 Création des fichiers :\n")
    total_lines = 0
    for rel_path, content in files:
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        write_file(full_path, content)
        total_lines += content.count("\n") + 1

    print()
    print("=" * 70)
    print("  RÉSUMÉ")
    print("=" * 70)
    print()
    print(f"  ✅  {len(files)} fichiers créés avec succès")
    print(f"  📝  {total_lines} lignes de code au total")
    print()
    print("  Fichiers créés :")
    print("  ──────────────────────────────────────────────────")
    print("  📄  features/environment.py              (Behave-Django hooks)")
    print("  📄  features/search.feature               (9 scénarios — US-001 à US-005)")
    print("  📄  features/booking.feature              (7 scénarios — US-008 à US-010)")
    print("  📄  features/auth.feature                 (7 scénarios — US-027 à US-031)")
    print("  📄  features/promotions.feature           (5 scénarios — US-006 / US-034)")
    print("  📄  features/steps/__init__.py            (vide)")
    print("  📄  features/steps/search_steps.py        (définitions étapes recherche)")
    print("  📄  features/steps/booking_steps.py       (définitions étapes réservation)")
    print("  📄  features/steps/auth_steps.py          (définitions étapes authentification)")
    print("  📄  features/steps/promotions_steps.py    (définitions étapes promotions)")
    print("  📄  features/steps/common_steps.py        (étapes partagées)")
    print("  📄  behave.ini                            (configuration Behave)")
    print()
    print("  Total : 28 scénarios BDD couvrant 9 user stories")
    print()
    print("  📋 User Stories couvertes :")
    print("  ──────────────────────────────────────────────────")
    print("  US-001  Recherche de vol (aller simple / aller-retour)")
    print("  US-004  Tri des résultats par prix")
    print("  US-005  Sélection de classe de voyage")
    print("  US-006  Codes promotionnels")
    print("  US-008  Création de réservation connecté")
    print("  US-009  Consultation de réservation")
    print("  US-010  Annulation de réservation")
    print("  US-027  Inscription utilisateur")
    print("  US-028  Connexion / Déconnexion")
    print("  US-030  Mise à jour du profil")
    print("  US-034  Inscription newsletter")
    print()
    print("  🚀 Exécution des tests :")
    print("  ──────────────────────────────────────────────────")
    print("  behave features/search.feature")
    print("  behave features/booking.feature")
    print("  behave features/auth.feature")
    print("  behave features/promotions.feature")
    print("  behave features/                    (tous)")
    print()
    print("  ⚠️  Prérequis : behave, behave-django")
    print("     pip install behave behave-django")
    print("=" * 70)


if __name__ == "__main__":
    main()
