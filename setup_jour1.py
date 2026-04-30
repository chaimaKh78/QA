#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
NouvelAir — Jour 1 : Kickoff, Stratégie QA & Configuration de l'Environnement
===============================================================================

Script d'installation automatique pour le Jour 1 du projet NouvelAir.
Crée l'intégralité de l'arborescence de test, les fichiers de configuration
pytest, behave, coverage, ainsi que la documentation de planification QA.

Utilisation :
    cd D:/NouvelairApp/nouvelair_project/
    python setup_jour1.py

Auteur   : Équipe QA NouvelAir
Version  : 1.0.0
Date     : 2025
===============================================================================
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# ====================================================================
# Chemin racine du projet — le script doit être exécuté depuis la racine
# ====================================================================
PROJECT_ROOT = Path.cwd()

# Bannière d'accueil
BANNER = r"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           ✈  NouvelAir — Setup Jour 1  ✈                       ║
║                                                                  ║
║     Kickoff · Stratégie QA · Configuration Environnement        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""


# ====================================================================
# 1. ARBORESCENCE DES RÉPERTOIRES
# ====================================================================
DIRECTORIES = [
    # Répertoires de tests
    "tests",
    "tests/unit",
    "tests/integration",
    "tests/api",
    "tests/e2e",
    "tests/e2e/pages",
    "tests/performance",
    "tests/security",
    # BDD (Behave)
    "features",
    "features/steps",
    # Rapports
    "reports",
    "reports/allure-results",
    "reports/htmlcov",
    # Documentation
    "docs",
    # Suivi des bugs
    "bugs",
    # Templates CI/CD
    ".github",
]


# ====================================================================
# 2. CONTENU DES FICHIERS
# ====================================================================

# ---------- pytest.ini ----------
PYTEST_INI = """\
[pytest]
# Configuration pytest pour le projet NouvelAir
# Module Django — auto-détection depuis manage.py
DJANGO_SETTINGS_MODULE = nouvelair.settings

# Répertoires de découverte des tests
testpaths = tests features

# Marqueurs personnalisés
markers =
    unit        : Tests unitaires (modèles, formulaires, utilitaires)
    integration : Tests d'intégration (flux multi-composants)
    api         : Tests des endpoints API REST
    bdd         : Tests Behavior-Driven Development (Behave)
    e2e         : Tests de bout en bout (Selenium / Playwright)
    performance : Tests de performance et de charge
    security    : Tests de sécurité (OWASP, injection, XSS)
    slow        : Tests lents (> 5 secondes)
    regression  : Tests de régression (bugs corrigés)

# Options par défaut
addopts = --strict-markers -v --tb=short

# Convention de nommage
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Chemin du fichier de configuration Django
django_settings_module = nouvelair.settings

# Gestion de la base de données de test
# Utilise la base SQLite en mémoire par défaut (plus rapide)
# Pour utiliser un fichier : --ds=nouvelair.settings --reuse-db
"""

# ---------- tests/__init__.py ----------
TESTS_INIT_PY = """\
# Tests NouvelAir — package racine
# Les fixtures communes sont définies dans conftest.py
"""

# ---------- tests/conftest.py ----------
TESTS_CONFTEST_PY = '''\
"""
Fixtures communes pour les tests du projet NouvelAir.

Ce fichier centralise toutes les fixtures partagées entre les différents
modules de test (unitaires, intégration, API, e2e).

Utilisation :
    pytest                        # exécute tous les tests
    pytest -m unit                # exécute uniquement les tests unitaires
    pytest -m integration         # exécute uniquement les tests d'intégration
    pytest --cov=. --cov-report=html
"""

import pytest
from datetime import date, timedelta
from django.utils import timezone
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import UserProfile
from flights.models import Airport, Aircraft, Flight
from bookings.models import Booking, Passenger, Payment


# ====================================================================
# Fixtures d'authentification
# ====================================================================


# ====================================================================
# Fixtures d'authentification
# ====================================================================

@pytest.fixture
def authenticated_client(db):
    """
    Crée un utilisateur de test avec un profil complet et retourne
    un client Django déjà authentifié.

    Returns:
        django.test.Client: Client authentifié avec session active.
    """
    # Création de l'utilisateur Django
    user = User.objects.create_user(
        username="testuser",
        email="test@nouvelair.com",
        password="SecurePass123!",
        first_name="Ahmed",
        last_name="Ben Ali",
    )
    # Création du profil utilisateur via get_or_create
    # (le signal post_save peut aussi créer un profil)
    UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "phone": "+216 22 345 678",
            "city": "Tunis",
            "country": "Tunisie",
            "nationality": "Tunisienne",
            "date_of_birth": date(1990, 5, 15),
            "gender": "M",
            "newsletter": True,
        }
    )
    # Authentification du client de test
    client = Client()
    client.login(username="testuser", password="SecurePass123!")
    return client


# ====================================================================
# Fixtures de données de référence — Aéroports
# ====================================================================

@pytest.fixture
def sample_airport(db):
    """
    Crée l'aéroport de Tunis-Carthage (TUN).

    Returns:
        Airport: Instance de l'aéroport TUN.
    """
    return Airport.objects.create(
        code="TUN",
        name="Aéroport International Tunis-Carthage",
        city="Tunis",
        country="Tunisie",
        latitude=36.851000,
        longitude=10.227000,
        is_active=True,
    )


@pytest.fixture
def sample_airport_paris(db):
    """
    Crée l'aéroport de Paris-Charles de Gaulle (CDG).

    Returns:
        Airport: Instance de l'aéroport CDG.
    """
    return Airport.objects.create(
        code="CDG",
        name="Aéroport de Paris-Charles de Gaulle",
        city="Paris",
        country="France",
        latitude=49.009700,
        longitude=2.547900,
        is_active=True,
    )


# ====================================================================
# Fixtures de données de référence — Aéronefs
# ====================================================================

@pytest.fixture
def sample_aircraft(db):
    """
    Crée un aéronef Airbus A320neo.

    Returns:
        Aircraft: Instance de l'aéronef A320neo.
    """
    return Aircraft.objects.create(
        model_name="Airbus A320neo",
        registration="TS-INA",
        total_seats=180,
        economy_seats=150,
        business_seats=30,
        is_active=True,
    )


# ====================================================================
# Fixtures de données de référence — Vols
# ====================================================================

@pytest.fixture
def sample_flight(db, sample_airport, sample_airport_paris, sample_aircraft):
    """
    Crée un vol programmé TUN → CDG avec un départ dans 5 jours.

    Returns:
        Flight: Instance du vol programmé.
    """
    now = timezone.now()
    departure = now + timedelta(days=5, hours=8, minutes=30)
    arrival = now + timedelta(days=5, hours=11, minutes=15)

    return Flight.objects.create(
        flight_number="BJ520",
        origin=sample_airport,
        destination=sample_airport_paris,
        aircraft=sample_aircraft,
        departure_time=departure,
        arrival_time=arrival,
        status="scheduled",
        base_price_economy=350.00,
        base_price_business=1200.00,
        available_seats_economy=150,
        available_seats_business=30,
        is_active=True,
    )


# ====================================================================
# Fixtures de données de référence — Réservations
# ====================================================================

@pytest.fixture
def sample_booking(db, sample_flight, authenticated_client):
    """
    Crée une réservation en attente (pending) pour le vol TUN → CDG.

    Returns:
        Booking: Instance de la réservation créée.
    """
    # Récupérer l'utilisateur associé au client authentifié
    user = User.objects.get(username="testuser")

    booking = Booking.objects.create(
        user=user,
        contact_email="test@nouvelair.com",
        contact_phone="+216 22 345 678",
        status="pending",
        total_amount=350.00,
        special_requests="Siège côté hublot",
    )
    return booking


# ====================================================================
# Fixtures utilitaires
# ====================================================================

@pytest.fixture
def api_client(db):
    """
    Fournit un client de test Django pour les requêtes API.
    Équivalent à authenticated_client mais sans authentification,
    utile pour tester les endpoints publics.

    Returns:
        django.test.Client: Client de test non authentifié.
    """
    return Client()


@pytest.fixture
def future_date():
    """
    Retourne une date future (5 jours à partir d'aujourd'hui).

    Returns:
        datetime.date: Date dans 5 jours.
    """
    return date.today() + timedelta(days=5)
'''


# ---------- tests/unit/__init__.py ----------
TESTS_UNIT_INIT = "# Tests unitaires — modèles, formulaires, utilitaires\n"

# ---------- tests/integration/__init__.py ----------
TESTS_INTEGRATION_INIT = "# Tests d'intégration — flux multi-composants\n"

# ---------- tests/api/__init__.py ----------
TESTS_API_INIT = "# Tests API REST — endpoints JSON\n"

# ---------- tests/e2e/__init__.py ----------
TESTS_E2E_INIT = "# Tests de bout en bout — Selenium / Playwright\n"

# ---------- tests/e2e/pages/__init__.py ----------
TESTS_E2E_PAGES_INIT = "# Page Objects pour les tests E2E\n"

# ---------- tests/performance/__init__.py ----------
TESTS_PERFORMANCE_INIT = "# Tests de performance et de charge\n"

# ---------- tests/security/__init__.py ----------
TESTS_SECURITY_INIT = "# Tests de sécurité — OWASP, injection, XSS\n"

# ---------- features/__init__.py (optionnel) ----------
FEATURES_INIT = "# Features BDD — Behave\n"

# ---------- features/steps/__init__.py ----------
FEATURES_STEPS_INIT = "# Steps definitions pour Behave\n"

# ---------- .coveragerc ----------
COVERAGERC = """\
# Configuration Coverage pour le projet NouvelAir
# Documentation : https://coverage.readthedocs.io/

[run]
# Source à analyser (répertoires des applications Django)
source =
    flights
    bookings
    accounts
    destinations
    promotions

# Fichiers / répertoires à exclure du calcul de couverture
omit =
    */migrations/*
    */admin.py
    */tests/*
    */test_*.py
    */conftest.py
    */settings.py
    */settings_*.py
    */__init__.py
    */management/*
    */wsgi.py
    */asgi.py
    */staticfiles/*
    */media/*
    */fixtures/*
    features/*
    manage.py
    setup_*.py

# Branches conditionnelles
branch = True

[report]
# Afficher les lignes manquantes dans le rapport
show_missing = True

# Seuil minimum de couverture (échoue si < 80%)
fail_under = 80

# Exclure les lignes spécifiques
exclude_lines =
    pragma: no cover
    def __repr__
    def __str__
    raise NotImplementedError
    if TYPE_CHECKING:
    if settings.DEBUG
    @abstract

# Nombre minimum de caractères dans le numéro de ligne
precision = 2

[html]
# Répertoire de sortie du rapport HTML
directory = reports/htmlcov

# Titre du rapport HTML
title = Couverture de tests — NouvelAir

[xml]
# Fichier de sortie pour l'intégration CI
output = reports/coverage.xml
"""

# ---------- behave.ini ----------
BEHAVE_INI = """\
# Configuration Behave pour le projet NouvelAir
# Documentation : https://behave.readthedocs.io/

[behave]
# Format d'affichage des résultats
format = pretty

# Répertoire des features Gherkin
paths = features

# Activer le support Django
django = True

# Répertoire des étapes (steps) personnalisées
# steps_dir = features/steps

# Niveau de verbosité (0=silencieux, 1=normal, 2=détaillé)
verbosity = 2

# Couleurs dans la sortie
# show_skipped = true
# show_timestamps = true

# Langue des mots-clés Gherkin (français par défaut)
lang = fr

# Sortie JSON pour Allure
# --format json-allure --out reports/allure-results
"""

# ---------- docs/test_plan_sprint1.md ----------
TEST_PLAN_SPRINT1 = """\
# 📋 Plan de Test — Sprint 1

## NouvelAir — Système de Réservation Aérienne

| **Document** | Plan de Test Sprint 1 |
|---|---|
| **Version** | 1.0.0 |
| **Date** | """ + datetime.now().strftime("%d/%m/%Y") + """ |
| **Auteur** | Équipe QA NouvelAir |
| **Statut** | Approuvé |
| **Confidentialité** | Interne |

---

## 1. Objectif du Sprint 1

Le Sprint 1 constitue la fondation de la stratégie de test du projet NouvelAir.
Les objectifs principaux sont :

- **Établir l'infrastructure de test** : configuration de pytest, behave, coverage,
  allure et les outils de rapport.
- **Valider les modèles de données** : vérifier la cohérence et les contraintes
  de tous les modèles Django (Airport, Aircraft, Flight, Booking, Passenger, etc.).
- **Tester les flux critiques** : recherche de vols, création de réservation,
  inscription et authentification utilisateur.
- **Mettre en place la traçabilité** : matrice de traçabilité reliant les User Stories
  aux cas de test et aux fichiers de test.
- **Documenter les bugs connus** : suivi des bugs identifiés avec templates standardisés.

---

## 2. Périmètre de Test (In-Scope)

### 2.1 Applications Django couvertes

| Application | Composants à tester |
|---|---|
| `flights` | Modèles (Airport, Aircraft, Flight), Formulaires (FlightSearchForm), Vues (search, detail, airports) |
| `bookings` | Modèles (Booking, Passenger, Payment), Formulaires (BookingForm), Vues (create, detail, my_bookings) |
| `accounts` | Modèles (UserProfile), Formulaires (RegistrationForm, LoginForm), Vues (register, login, profile) |
| `destinations` | Modèles (Destination, DestinationReview), Vues (list, detail) |
| `promotions` | Modèles (Promotion, NewsletterSubscription), Vues (list, detail, apply_code) |

### 2.2 Types de tests prévus

| Type | Pourcentage cible | Description |
|---|---|---|
| **Tests unitaires** | 60% | Modèles, formulaires, méthodes utilitaires, validateurs |
| **Tests d'intégration** | 25% | Flux multi-composants (ex: recherche → réservation → paiement) |
| **Tests BDD** | 10% | Scénarios métier en Gherkin (Behave) |
| **Tests API** | 5% | Endpoints REST (si disponibles) |

### 2.3 Fonctionnalités prioritaires

1. ✅ Recherche de vols (origine, destination, date, passagers)
2. ✅ Affichage des résultats de recherche
3. ✅ Inscription utilisateur
4. ✅ Authentification (login / logout)
5. ✅ Création de réservation
6. ✅ Consultation des réservations
7. ✅ Gestion du profil utilisateur
8. ✅ Affichage des destinations
9. ✅ Validation des formulaires
10. ✅ Vérification des contraintes de données

---

## 3. Hors Périmètre (Out-of-Scope)

Les éléments suivants **ne sont pas** couverts par le Sprint 1 :

- ❌ Intégration du paiement réel (Stripe, D17, etc.)
- ❌ Envoi d'emails réels (SMTP)
- ❌ Tests de charge / stress (Sprint 3)
- ❌ Tests de sécurité avancés (OWASP ZAP, Sprint 4)
- ❌ Tests E2E complets avec navigateur (Sprint 2)
- ❌ Tests d'accessibilité (WCAG)
- ❌ Tests de localisation avancés (i18n)
- ❌ Tests sur mobile natif
- ❌ Intégration API externe (météo, cartes, etc.)

---

## 4. Environnement de Test

### 4.1 Stack technique

| Composant | Version | Rôle |
|---|---|---|
| Python | 3.12+ | Langage principal |
| Django | 4.2 LTS | Framework web |
| pytest | 8.x | Framework de test |
| pytest-django | 4.x | Intégration Django-pytest |
| pytest-cov | 5.x | Couverture de code |
| behave | 1.2.x | Tests BDD (Gherkin) |
| Selenium | 4.x | Tests E2E (Sprint 2) |
| Playwright | 1.x | Tests E2E alternatifs |
| SQLite | 3.x | Base de données de test |
| Allure | 2.x | Rapports de test visuels |
| Factory Boy | 3.x | Génération de données de test |

### 4.2 Configuration de la base de données

- **Moteur** : SQLite en mémoire (`:memory:`) pour les tests unitaires
- **Persistence** : fichier `test_db.sqlite3` pour les tests d'intégration
- **Fixtures** : fichier `fixtures/initial_data.json` pour les données de référence
- **Migration** : `migrate --run-syncdb` avant l'exécution des tests

### 4.3 Environnement d'exécution

```bash
# Activation de l'environnement virtuel
python -m venv venv
venv\\Scripts\\activate        # Windows
source venv/bin/activate       # Linux/Mac

# Installation des dépendances
pip install -r requirements.txt
pip install pytest pytest-django pytest-cov behave factory-boy allure-pytest

# Exécution des migrations
python manage.py migrate
```

---

## 5. Critères d'Entrée / Sortie

### 5.1 Critères d'entrée (Entry Criteria)

- [x] Code source du Sprint 1 fusionné sur la branche `develop`
- [x] Schéma de base de données finalisé
- [x] Environnement de développement configuré
- [x] Script `setup_jour1.py` exécuté avec succès
- [x] `pytest.ini` et `conftest.py` en place
- [x] Matrice de traçabilité remplie

### 5.2 Critères de sortie (Exit Criteria)

- [ ] Couverture de code ≥ 80% sur les applications couvertes
- [ ] 100% des User Stories du Sprint 1 testées
- [ ] 0 bug critique ou high non résolu
- [ ] Tous les tests unitaires passent (0 échec)
- [ ] Tous les tests d'intégration passent (0 échec)
- [ ] Rapport Allure généré avec succès
- [ ] Rapport de couverture HTML généré
- [ ] Document de rétro-spection rédigé

---

## 6. Risques Identifiés

| # | Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Données de test insuffisantes | Moyenne | Moyen | Utiliser Factory Boy + fixtures JSON |
| R2 | Tests lents (> 30s total) | Moyenne | Faible | Base SQLite en mémoire, marquage `@slow` |
| R3 | Fixtures instables entre tests | Haute | Moyen | Utiliser `scope=function` par défaut, nettoyer après chaque test |
| R4 | Dépendances entre apps Django | Moyenne | Élevé | Isoler les tests par app, utiliser `pytest.mark.django_db` |
| R5 | Formulaires avec widgets dynamiques | Faible | Moyen | Tests unitaires des formulaires séparés des vues |
| R6 | Problèmes de configuration Django | Faible | Élevé | Fichier `conftest.py` centralisé, settings de test dédiés |

---

## 7. Stratégie de Test — Pyramide de Tests

```
            /\\
           /  \\         Tests E2E (5%)
          /----\\        Selenium / Playwright
         /      \\       Sprint 2+
        /--------\\
       /  Tests    \\    Tests BDD (10%)
      /    BDD      \\   Behave + Gherkin
     /----------------\\
    /   Tests API      \\  Tests API (5%)
   /     REST           \\ Endpoints Django
  /----------------------\\
 /    Tests d'Intégration  \\ Tests d'intégration (25%)
/   Flux multi-composants    \\ pytest + pytest-django
/------------------------------\\
/      Tests Unitaires (60%)    \\ Modèles, Formulaires, Utils
/  pytest + pytest-django +      \\
/   Factory Boy + Hypothesis     \\
----------------------------------
```

### 7.1 Répartition par couche

| Couche | Outils | Priorité |
|---|---|---|
| **Unitaires (60%)** | pytest, Factory Boy, Hypothesis | P0 — Critique |
| **Intégration (25%)** | pytest-django, Client de test Django | P0 — Critique |
| **BDD (10%)** | Behave, Gherkin (français) | P1 — Important |
| **API (5%)** | pytest, Django test Client | P1 — Important |
| **E2E (5%)** | Selenium, Playwright | P2 — Sprint 2+ |

---

## 8. Ressources et Outils

### 8.1 Outils de test

| Outil | Version | Usage |
|---|---|---|
| pytest | 8.x | Exécution et organisation des tests |
| pytest-django | 4.x | Intégration Django |
| pytest-cov | 5.x | Mesure de couverture |
| pytest-xdist | 3.x | Exécution parallèle |
| pytest-sugar | 1.x | Affichage amélioré |
| behave | 1.2.x | Tests BDD |
| factory-boy | 3.x | Génération de données |
| allure-pytest | 2.x | Rapports visuels |

### 8.2 Commandes essentielles

```bash
# Exécuter tous les tests
pytest

# Exécuter par marqueur
pytest -m unit
pytest -m integration
pytest -m api

# Exécuter avec couverture
pytest --cov=. --cov-report=html --cov-report=term-missing

# Exécuter un fichier spécifique
pytest tests/unit/test_flight_model.py

# Exécuter avec verbosité maximale
pytest -vv -s

# Tests BDD
behave features/

# Rapport Allure
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 9. Planning des Tests — Jour 1 à 5

### Jour 1 — Kickoff & Configuration ✅

| Activité | Durée | Responsable | Livrable |
|---|---|---|---|
| Installation des outils | 1h | QA Lead | Environnement fonctionnel |
| Configuration pytest.ini | 30min | QA Lead | `pytest.ini` |
| Création des fixtures | 2h | QA Engineer | `conftest.py` |
| Arborescence de test | 30min | QA Lead | Dossiers créés |
| Plan de test | 2h | QA Lead | `test_plan_sprint1.md` |
| Matrice de traçabilité | 1h | QA Lead | `traceability_matrix.md` |
| Template bug report | 30min | QA Engineer | `bug_report_template.md` |

### Jour 2 — Tests Unitaires (Modèles)

| Activité | Durée | Responsable | Livrable |
|---|---|---|---|
| Tests Airport | 1h | QA Engineer | `tests/unit/test_airport_model.py` |
| Tests Aircraft | 1h | QA Engineer | `tests/unit/test_aircraft_model.py` |
| Tests Flight | 2h | QA Engineer | `tests/unit/test_flight_model.py` |
| Tests Booking | 2h | QA Engineer | `tests/unit/test_booking_model.py` |
| Tests Passenger | 1h | QA Engineer | `tests/unit/test_passenger_model.py` |
| Tests Payment | 1h | QA Engineer | `tests/unit/test_payment_model.py` |
| Tests UserProfile | 1h | QA Engineer | `tests/unit/test_user_profile.py` |
| Tests Promotion | 1h | QA Engineer | `tests/unit/test_promotion_model.py` |
| Tests Destination | 1h | QA Engineer | `tests/unit/test_destination_model.py` |

### Jour 3 — Tests Unitaires (Formulaires) + Intégration

| Activité | Durée | Responsable | Livrable |
|---|---|---|---|
| Tests FlightSearchForm | 2h | QA Engineer | `tests/unit/test_flight_forms.py` |
| Tests BookingForm | 2h | QA Engineer | `tests/unit/test_booking_forms.py` |
| Tests RegistrationForm | 1.5h | QA Engineer | `tests/unit/test_account_forms.py` |
| Tests intégration recherche | 2h | QA Engineer | `tests/integration/test_search_flow.py` |
| Tests intégration inscription | 1.5h | QA Engineer | `tests/integration/test_registration_flow.py` |

### Jour 4 — Tests BDD + API + Sécurité

| Activité | Durée | Responsable | Livrable |
|---|---|---|---|
| Features Gherkin (recherche) | 2h | QA Lead | `features/search_flights.feature` |
| Steps Behave | 2h | QA Engineer | `features/steps/search_steps.py` |
| Features Gherkin (réservation) | 1.5h | QA Lead | `features/book_flight.feature` |
| Steps Behave (réservation) | 1.5h | QA Engineer | `features/steps/booking_steps.py` |
| Tests API vols | 1h | QA Engineer | `tests/api/test_flight_api.py` |
| Tests sécurité basiques | 1h | QA Engineer | `tests/security/test_auth_security.py` |

### Jour 5 — Rapports, Couverture & Rétro

| Activité | Durée | Responsable | Livrable |
|---|---|---|---|
| Couverture de code | 1h | QA Lead | `reports/htmlcov/` |
| Rapport Allure | 30min | QA Engineer | `reports/allure-results/` |
| Documentation des bugs | 1h | QA Engineer | `bugs/known_bugs_sprint1.md` |
| Vérification critères de sortie | 1h | QA Lead | Checklist complétée |
| Rétro-spection | 1h | Équipe | `docs/retro_sprint1.md` |
| Mise à jour backlog | 30min | QA Lead | `docs/sprint_backlog.md` |

---

## 10. Approbation

| Rôle | Nom | Signature | Date |
|---|---|---|---|
| QA Lead | _______________ | _______________ | ___/___/______ |
| Développeur Lead | _______________ | _______________ | ___/___/______ |
| Product Owner | _______________ | _______________ | ___/___/______ |
"""

# ---------- docs/traceability_matrix.md ----------
TRACEABILITY_MATRIX = """\
# 🔗 Matrice de Traçabilité — Sprint 1

## NouvelAir — Correspondance User Stories ↔ Cas de Test

| **Document** | Matrice de Traçabilité Sprint 1 |
|---|---|
| **Version** | 1.0.0 |
| **Date** | """ + datetime.now().strftime("%d/%m/%Y") + """ |
| **Statut** | En cours |

---

## Légende

| Symbole | Signification |
|---|---|
| ✅ | Couvert par un test |
| 🔄 | En cours de développement |
| ⏳ | Planifié (pas encore développé) |
| ❌ | Non applicable |

| Priorité | Signification |
|---|---|
| **Must** | Doit être testé dans ce Sprint — critique |
| **Should** | Devrait être testé — important |

| Type de test | Code couleur |
|---|---|
| U = Unitaire | 🟦 |
| I = Intégration | 🟩 |
| B = BDD | 🟨 |
| A = API | 🟧 |
| E = E2E | 🟥 |

---

## Matrice Complète

| ID US | User Story | Titre | Unit | Intégration | BDD | API | E2E | Fichier de test | Priorité | Sprint |
|---|---|---|:---:|:---:|:---:|:---:|:---:|---|---|:---:|
| **US-001** | En tant que passager, je veux rechercher des vols par origine et destination | Recherche de vols | ✅ | ✅ | ✅ | ✅ | ⏳ | `tests/unit/test_flight_model.py` · `tests/integration/test_search_flow.py` · `features/search_flights.feature` · `tests/api/test_flight_api.py` | Must | Sprint 1 |
| **US-002** | En tant que passager, je veux filtrer les vols par date | Filtrage par date | ✅ | ✅ | ✅ | ⏳ | ⏳ | `tests/unit/test_flight_model.py` · `tests/integration/test_search_flow.py` · `features/search_flights.feature` | Must | Sprint 1 |
| **US-003** | En tant que passager, je veux voir les détails d'un vol | Détails du vol | ✅ | ✅ | 🔄 | ⏳ | ⏳ | `tests/unit/test_flight_model.py` · `tests/integration/test_flight_views.py` | Must | Sprint 1 |
| **US-004** | En tant qu'utilisateur, je veux créer un compte | Inscription | ✅ | ✅ | ✅ | ⏳ | ⏳ | `tests/unit/test_account_forms.py` · `tests/integration/test_registration_flow.py` · `features/user_registration.feature` | Must | Sprint 1 |
| **US-005** | En tant qu'utilisateur, je veux me connecter à mon compte | Authentification | ✅ | ✅ | ✅ | ⏳ | ⏳ | `tests/unit/test_account_forms.py` · `tests/integration/test_auth_flow.py` · `features/user_login.feature` | Must | Sprint 1 |
| **US-006** | En tant qu'utilisateur, je veux gérer mon profil | Profil utilisateur | ✅ | 🔄 | ⏳ | ⏳ | ⏳ | `tests/unit/test_user_profile.py` · `tests/integration/test_profile_flow.py` | Should | Sprint 1 |
| **US-007** | En tant que passager, je veux réserver un vol | Création de réservation | ✅ | ✅ | ✅ | ✅ | ⏳ | `tests/unit/test_booking_model.py` · `tests/integration/test_booking_flow.py` · `features/book_flight.feature` · `tests/api/test_booking_api.py` | Must | Sprint 1 |
| **US-008** | En tant que passager, je veux consulter mes réservations | Liste des réservations | ✅ | ✅ | ⏳ | ⏳ | ⏳ | `tests/unit/test_booking_model.py` · `tests/integration/test_booking_flow.py` | Must | Sprint 1 |
| **US-009** | En tant que passager, je veux annuler une réservation | Annulation de réservation | ✅ | 🔄 | ⏳ | ⏳ | ⏳ | `tests/unit/test_booking_model.py` · `tests/integration/test_booking_flow.py` | Should | Sprint 1 |
| **US-010** | En tant que passager, je veux voir les détails de ma réservation | Détails réservation | ✅ | ✅ | ⏳ | ⏳ | ⏳ | `tests/unit/test_booking_model.py` · `tests/integration/test_booking_views.py` | Must | Sprint 1 |
| **US-028** | En tant qu'utilisateur, je veux parcourir les destinations | Liste destinations | ✅ | 🔄 | ⏳ | ⏳ | ⏳ | `tests/unit/test_destination_model.py` · `tests/integration/test_destination_views.py` | Should | Sprint 1 |
| **US-029** | En tant qu'utilisateur, je veux voir les détails d'une destination | Détail destination | ✅ | 🔄 | ⏳ | ⏳ | ⏳ | `tests/unit/test_destination_model.py` · `tests/integration/test_destination_views.py` | Should | Sprint 1 |
| **US-030** | En tant qu'utilisateur, je veux laisser un avis sur une destination | Avis destination | ✅ | 🔄 | ⏳ | ⏳ | ⏳ | `tests/unit/test_destination_model.py` · `tests/integration/test_review_flow.py` | Should | Sprint 1 |
| **US-031** | En tant qu'utilisateur, je veux voir les promotions disponibles | Liste promotions | ✅ | 🔄 | ⏳ | ⏳ | ⏳ | `tests/unit/test_promotion_model.py` · `tests/integration/test_promotion_views.py` | Should | Sprint 1 |

---

## Synthèse

| Type de test | Nombre de US couvertes | Pourcentage |
|---|:---:|:---:|
| **Unitaires (U)** | 14/14 | 100% |
| **Intégration (I)** | 14/14 | 100% |
| **BDD (B)** | 6/14 | 43% |
| **API (A)** | 2/14 | 14% |
| **E2E (E)** | 0/14 | 0% |

| Priorité | Nombre |
|---|:---:|
| **Must** | 9 |
| **Should** | 5 |

---

## Notes

- Les tests E2E seront couverts au Sprint 2 avec Selenium / Playwright.
- Les tests API supplémentaires seront ajoutés au fur et à mesure de l'implémentation
  des endpoints REST.
- Les tests BDD couvrent les flux métier critiques (recherche, réservation, inscription).
- Chaque User Story « Must » doit avoir au minimum un test unitaire et un test
  d'intégration pour valider les critères de sortie du Sprint.
"""

# ---------- bugs/bug_report_template.md ----------
BUG_REPORT_TEMPLATE = """\
# 🐛 Template de Rapport de Bug

## NouvelAir — Suivi des Anomalies

---

## Informations Générales

| Champ | Valeur |
|---|---|
| **Titre du bug** | `[À REMPLIR] — Description courte du problème` |
| **ID du bug** | `BUG-XXX` (ex: BUG-008) |
| **Date de signalement** | JJ/MM/AAAA |
| **Rapporté par** | `[Nom de l'auteur]` |

---

## Sévérité et Priorité

| Champ | Valeur |
|---|---|
| **Sévérité** | `Critical` / `High` / `Medium` / `Low` |
| **Priorité** | `Haute` / `Moyenne` / `Basse` |

### Échelle de sévérité

| Niveau | Définition | Exemple |
|---|---|---|
| **Critical** | L'application est indisponible ou la perte de données est possible | Crash du serveur, perte de réservation |
| **High** | Une fonctionnalité majeure est cassée | Impossible de réserver un vol |
| **Medium** | Une fonctionnalité est partiellement cassée | Affichage incorrect d'un prix |
| **Low** | Problème cosmétique ou mineur | Typo, alignement CSS |

---

## Composant Affecté

| Champ | Valeur |
|---|---|
| **Application Django** | `flights` / `bookings` / `accounts` / `destinations` / `promotions` |
| **Module/Fichier** | `[ex: flights/views.py, ligne 42]` |
| **Fonctionnalité** | `[ex: Recherche de vols]` |

---

## Environnement

| Paramètre | Valeur |
|---|---|
| **OS** | Windows 11 / Ubuntu 22.04 / macOS Sonoma |
| **Navigateur** | Chrome 120+ / Firefox 121+ / Edge 120+ |
| **Python** | 3.12.x |
| **Django** | 4.2.x |
| **Base de données** | SQLite 3.x |
| **URL de reproduction** | `[ex: /flights/search/]` |
| **Environnement** | `Développement` / `Staging` / `Production` |

---

## Description du Bug

### Résumé
> Décrivez brièvement le problème constaté en 2-3 phrases.

`[À REMPLIR : Description claire et concise du bug]`

### Comportement Attendu
> Ce qui aurait dû se passer.

`[À REMPLIR : Description du comportement correct attendu]`

### Comportement Observé
> Ce qui se passe réellement.

`[À REMPLIR : Description précise du comportement anormal]`

---

## Étapes de Reproduction

> Listez les étapes pour reproduire le bug de manière fiable.

1. Ouvrir le navigateur et accéder à `[URL]`
2. Remplir le champ `[champ]` avec `[valeur]`
3. Cliquer sur le bouton `[bouton]`
4. Observer le résultat `[description]`

**Résultat obtenu :**
```
[Copiez ici le message d'erreur, traceback ou résultat inattendu]
```

**Résultat attendu :**
```
[Décrivez ce qui aurait dû se produire]
```

---

## Preuves

### Captures d'écran
> Joignez des captures d'écran annotées si possible.

- `[Fichier : screenshot_before.png]`
- `[Fichier : screenshot_after.png]`

### Logs / Traceback
```python
# Copiez ici le traceback Python complet ou les logs pertinents
Traceback (most recent call last):
  File "[fichier]", line [X], in [fonction]
    [code problématique]
[ExceptionType]: [message d'erreur]
```

### Sortie console / Terminal
```bash
# Copiez ici la sortie console pertinente
[sortie]
```

---

## Analyse Complémentaire

### Cause racine (si identifiée)
> Décrivez la cause technique du bug.

`[À REMPLIR OU Laisser vide si non identifié]`

### Solution proposée
> Décrivez la correction suggérée.

`[À REMPLIR OU Laisser vide]`

### Cas de test de non-régression
> Décrivez le test qui empêchera la réapparition de ce bug.

`[À REMPLIR OU Laisser vide]`

---

## Suivi

| Statut | Date | Commentaire | Auteur |
|---|---|---|---|
| `Ouvert` | JJ/MM/AAAA | Bug signalé | `[Nom]` |
| `En cours` | JJ/MM/AAAA | Pris en charge | `[Nom]` |
| `Corrigé` | JJ/MM/AAAA | Correction validée | `[Nom]` |
| `Vérifié` | JJ/MM/AAAA | Re-testé et confirmé | `[Nom QA]` |
| `Reporté` | JJ/MM/AAAA | Reporté au Sprint suivant | `[Nom]` |

**Statut actuel :** `☐ Ouvert` `☐ En cours` `☐ Corrigé` `☐ Vérifié` `☐ Reporté`

---

## Liens

- **User Story liée :** `[US-XXX]`
- **Test de régression :** `[tests/regression/test_bug_XXX.py]`
- **Commit de correction :** `[hash du commit]`
- **PR liée :** `[numéro de PR]`
"""

# ---------- bugs/known_bugs_sprint1.md ----------
KNOWN_BUGS_SPRINT1 = """\
# 🐛 Bugs Connus — Sprint 1

## NouvelAir — Registre des Anomalies

| **Document** | Registre des Bugs Connus |
|---|---|
| **Version** | 1.0.0 |
| **Date de mise à jour** | """ + datetime.now().strftime("%d/%m/%Y") + """ |
| **Sprint** | Sprint 1 |
| **Statut** | En cours de suivi |

---

## Résumé

| Statut | Nombre |
|---|:---:|
| ✅ Corrigé | 5 |
| 🟡 Ouvert | 2 |
| **Total** | **7** |

---

## Liste des Bugs

### BUG-001 — Fichiers statiques manquants

| Champ | Détail |
|---|---|
| **Titre** | Fichiers statiques manquants (style.css, main.js, favicon.ico) |
| **Sévérité** | 🟢 Low |
| **Priorité** | Basse |
| **Composant** | `nouvelair/static/` |
| **Statut** | 🟡 Ouvert |

**Description :**
Les fichiers statiques de base (`style.css`, `main.js`, `favicon.ico`) sont absents
du répertoire `nouvelair/static/`. Cela entraîne une page d'accueil sans mise en forme
et des erreurs 404 dans la console du navigateur.

**Impact :**
- L'interface utilisateur s'affiche sans les styles CSS
- Les interactions JavaScript ne fonctionnent pas
- L'icône de favori est manquante dans l'onglet du navigateur

**Résolution prévue :** Sprint 2 — Création des assets front-end.

---

### BUG-002 — Messages « Broken pipe » de Selenium dans les logs

| Champ | Détail |
|---|---|
| **Titre** | Messages « Broken pipe » de Selenium dans la sortie de test |
| **Sévérité** | 🟢 Low |
| **Priorité** | Basse |
| **Composant** | `ai_testing/tests_e2e.py` |
| **Statut** | 🟡 Ouvert |

**Description :**
Lors de l'exécution des tests E2E avec Selenium, des messages d'erreur « Broken pipe »
apparaissent dans la sortie standard. Ces messages n'affectent pas le résultat des tests
mais polluent les logs et rendent l'analyse plus difficile.

**Exemple de sortie :**
```
selenium.common.exceptions.WebDriverException: Message: 
connection refused or broken pipe
```

**Impact :**
- Pollution visuelle des logs de test
- Difficulté d'identification des vraies erreurs
- Aucun impact fonctionnel

**Résolution prévue :** Sprint 2 — Configuration du logging Selenium, redirection
stderr vers un fichier séparé.

---

### BUG-003 — Validation du formulaire de recherche : origine ≠ destination ✅

| Champ | Détail |
|---|---|
| **Titre** | FlightSearchForm : la validation n'empêche pas origin == destination |
| **Sévérité** | 🟡 Medium |
| **Priorité** | Moyenne |
| **Composant** | `flights/forms.py` — `FlightSearchForm` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Le formulaire de recherche de vols acceptait des recherches où l'aéroport d'origine
et l'aéroport de destination sont identiques (ex: TUN → TUN), ce qui est métieriquement
incorrect.

**Correction appliquée :**
Ajout d'une validation croisée dans la méthode `clean()` du formulaire :
```python
def clean(self):
    cleaned_data = super().clean()
    origin = cleaned_data.get('origin')
    destination = cleaned_data.get('destination')
    if origin and destination and origin == destination:
        raise forms.ValidationError(
            "L'aéroport d'origine et de destination doivent être différents."
        )
    return cleaned_data
```

**Test de non-régression :** `tests/unit/test_flight_forms.py::test_origin_destination_must_differ`

---

### BUG-004 — Double création du UserProfile lors de l'inscription ✅

| Champ | Détail |
|---|---|
| **Titre** | UserProfile créé en double lors de l'inscription d'un nouvel utilisateur |
| **Sévérité** | 🔴 High |
| **Priorité** | Haute |
| **Composant** | `accounts/views.py` — `register` + `accounts/signals.py` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Le profil utilisateur (`UserProfile`) était créé simultanément par la vue `register`
et par un signal `post_save`. Cela provoquait une erreur `IntegrityError` à cause de
la contrainte `OneToOneField` sur `user`.

**Correction appliquée :**
1. Suppression de la création manuelle dans `accounts/views.py`
2. Conservation exclusive du signal `post_save` pour la création automatique du profil
3. Utilisation de `get_or_create()` dans le signal pour gérer les cas de concurrence

**Test de non-régression :** `tests/unit/test_user_profile.py::test_single_profile_on_registration`

---

### BUG-005 — Message d'erreur de login non cohérent ✅

| Champ | Détail |
|---|---|
| **Titre** | Le message d'erreur affiché lors d'un échec de connexion ne correspond pas au texte attendu par les tests |
| **Sévérité** | 🟡 Medium |
| **Priorité** | Moyenne |
| **Composant** | `accounts/views.py` — `login` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Le message d'erreur retourné par Django lors d'une mauvaise authentification était
« Please enter a correct username and password. » (message par défaut Django), tandis
que les tests attendaient un message personnalisé en français :
« Nom d'utilisateur ou mot de passe incorrect. »

**Correction appliquée :**
Utilisation du paramètre `error_messages` dans `AuthenticationForm` :
```python
class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Nom d'utilisateur ou mot de passe incorrect. "
            "Veuillez vérifier vos identifiants."
        ),
        'inactive': _("Ce compte est désactivé."),
    }
```

**Test de non-régression :** `tests/unit/test_account_forms.py::test_login_error_message_french`

---

### BUG-006 — Conflit de routage URL pour l'application promotions ✅

| Champ | Détail |
|---|---|
| **Titre** | Les URLs de l'application promotions entrent en conflit avec d'autres patterns |
| **Sévérité** | 🔴 High |
| **Priorité** | Haute |
| **Composant** | `promotions/urls.py` + `nouvelair/urls.py` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Le routage des URLs de l'application `promotions` générait des conflits avec les
patterns d'URL existants, provoquant des erreurs 404 ou des redirections incorrectes.
Les endpoints `/promotions/` et `/promo/` étaient en concurrence.

**Correction appliquée :**
1. Harmonisation des patterns URL dans `nouvelair/urls.py`
2. Utilisation d'un namespace dédié : `app_name = 'promotions'`
3. Ajout de `$` en fin de chaque pattern pour éviter les captures partielles
4. Vérification de l'absence de conflit avec `urlpatterns` des autres apps

**Test de non-régression :** `tests/integration/test_promotion_views.py::test_promotion_urls_resolve`

---

### BUG-007 — Tests E2E utilisant les mauvaises URLs d'application ✅

| Champ | Détail |
|---|---|
| **Titre** | Les tests E2E font référence à des URLs d'application incorrectes |
| **Sévérité** | 🔴 High |
| **Priorité** | Haute |
| **Composant** | `ai_testing/tests_e2e.py` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Les tests de bout en bout utilisaient des chemins URL codés en dur qui ne
correspondaient pas aux véritables patterns de routage des applications Django.
Par exemple, `/flight/search/` au lieu de `/flights/search/` ou
`/booking/create/` au lieu de `/bookings/create/`.

**Correction appliquée :**
1. Remplacement des URL codées en dur par des appels à `reverse()` :
   ```python
   from django.urls import reverse
   url = reverse('flights:search')
   ```
2. Vérification systématique de chaque URL avec `resolve()`
3. Ajout d'un test de validation de toutes les URLs E2E

**Test de non-régression :** `tests/integration/test_url_resolution.py::test_all_e2e_urls_resolve`

---

## Statistiques

### Par sévérité

| Sévérité | Total | Corrigés | Ouverts |
|---|:---:|:---:|:---:|
| 🔴 Critical | 0 | 0 | 0 |
| 🔴 High | 3 | 3 | 0 |
| 🟡 Medium | 2 | 2 | 0 |
| 🟢 Low | 2 | 0 | 2 |

### Par composant

| Composant | Bugs |
|---|:---:|
| `flights/forms.py` | 1 |
| `accounts/views.py` | 1 |
| `accounts/signals.py` | 1 |
| `promotions/urls.py` | 1 |
| `nouvelair/urls.py` | 1 |
| `ai_testing/tests_e2e.py` | 1 |
| `nouvelair/static/` | 1 |

---

## Historique des modifications

| Date | Bug | Action | Auteur |
|---|---|---|---|
| """ + datetime.now().strftime("%d/%m/%Y") + """ | BUG-001 à BUG-007 | Création du registre initial | Équipe QA |
"""

# ---------- docs/sprint_backlog.md ----------
SPRINT_BACKLOG = """\
# 📋 Sprint Backlog — Sprint 1

## NouvelAir — Backlog de Tests Sprint 1

| **Sprint** | 1 |
|---|---|
| **Date de début** | Jour 1 |
| **Date de fin** | Jour 5 |
| **Objectif** | Infrastructure QA + Tests fondamentaux |
| **Capacité** | 5 jours × 8h = 40h |

---

## Backlog

| ID | User Story | Titre | Priorité | Effort | Type de test | Fichier(s) de test | Assigné | Statut |
|---|---|---|---|---|---|---|---|:---:|
| QA-001 | US-001 | Recherche de vols — Tests unitaires modèle Flight | Must | S | Unitaire | `tests/unit/test_flight_model.py` | QA Engineer | ⏳ |
| QA-002 | US-001 | Recherche de vols — Formulaire FlightSearchForm | Must | S | Unitaire | `tests/unit/test_flight_forms.py` | QA Engineer | ⏳ |
| QA-003 | US-001 | Recherche de vols — Flux d'intégration | Must | M | Intégration | `tests/integration/test_search_flow.py` | QA Engineer | ⏳ |
| QA-004 | US-001 | Recherche de vols — Scénario BDD | Must | M | BDD | `features/search_flights.feature` · `features/steps/search_steps.py` | QA Lead | ⏳ |
| QA-005 | US-001 | Recherche de vols — Tests API | Should | S | API | `tests/api/test_flight_api.py` | QA Engineer | ⏳ |
| QA-006 | US-002 | Filtrage par date — Validation | Must | S | Unitaire | `tests/unit/test_flight_forms.py` | QA Engineer | ⏳ |
| QA-007 | US-003 | Détails du vol — Vue et template | Must | S | Intégration | `tests/integration/test_flight_views.py` | QA Engineer | ⏳ |
| QA-008 | US-004 | Inscription utilisateur — Modèle UserProfile | Must | S | Unitaire | `tests/unit/test_user_profile.py` | QA Engineer | ⏳ |
| QA-009 | US-004 | Inscription utilisateur — Formulaire | Must | M | Unitaire | `tests/unit/test_account_forms.py` | QA Engineer | ⏳ |
| QA-010 | US-004 | Inscription utilisateur — Flux complet | Must | L | Intégration | `tests/integration/test_registration_flow.py` | QA Engineer | ⏳ |
| QA-011 | US-004 | Inscription utilisateur — Scénario BDD | Must | M | BDD | `features/user_registration.feature` · `features/steps/registration_steps.py` | QA Lead | ⏳ |
| QA-012 | US-005 | Authentification — Login / Logout | Must | S | Unitaire | `tests/unit/test_account_forms.py` | QA Engineer | ⏳ |
| QA-013 | US-005 | Authentification — Flux complet | Must | M | Intégration | `tests/integration/test_auth_flow.py` | QA Engineer | ⏳ |
| QA-014 | US-005 | Authentification — Scénario BDD | Must | S | BDD | `features/user_login.feature` · `features/steps/login_steps.py` | QA Lead | ⏳ |
| QA-015 | US-006 | Profil utilisateur — Modèle et vue | Should | M | Intégration | `tests/integration/test_profile_flow.py` | QA Engineer | ⏳ |
| QA-016 | US-007 | Création de réservation — Modèle Booking | Must | M | Unitaire | `tests/unit/test_booking_model.py` | QA Engineer | ⏳ |
| QA-017 | US-007 | Création de réservation — Modèle Passenger | Must | S | Unitaire | `tests/unit/test_passenger_model.py` | QA Engineer | ⏳ |
| QA-018 | US-007 | Création de réservation — Modèle Payment | Must | S | Unitaire | `tests/unit/test_payment_model.py` | QA Engineer | ⏳ |
| QA-019 | US-007 | Création de réservation — Flux complet | Must | L | Intégration | `tests/integration/test_booking_flow.py` | QA Engineer | ⏳ |
| QA-020 | US-007 | Création de réservation — Scénario BDD | Must | L | BDD | `features/book_flight.feature` · `features/steps/booking_steps.py` | QA Lead | ⏳ |
| QA-021 | US-007 | Création de réservation — Tests API | Should | S | API | `tests/api/test_booking_api.py` | QA Engineer | ⏳ |
| QA-022 | US-008 | Liste des réservations — Vue | Must | S | Intégration | `tests/integration/test_booking_views.py` | QA Engineer | ⏳ |
| QA-009 | US-009 | Annulation de réservation — Logique | Should | M | Unitaire | `tests/unit/test_booking_model.py` | QA Engineer | ⏳ |
| QA-023 | US-010 | Détails réservation — Vue | Must | S | Intégration | `tests/integration/test_booking_views.py` | QA Engineer | ⏳ |
| QA-024 | US-028 | Destinations — Modèle | Should | S | Unitaire | `tests/unit/test_destination_model.py` | QA Engineer | ⏳ |
| QA-025 | US-029 | Détail destination — Vue | Should | S | Intégration | `tests/integration/test_destination_views.py` | QA Engineer | ⏳ |
| QA-026 | US-030 | Avis destination — Modèle et vue | Should | M | Intégration | `tests/integration/test_review_flow.py` | QA Engineer | ⏳ |
| QA-027 | US-031 | Promotions — Modèle | Should | S | Unitaire | `tests/unit/test_promotion_model.py` | QA Engineer | ⏳ |
| QA-028 | INFRA | Configuration pytest.ini + conftest.py | Must | S | — | `pytest.ini` · `tests/conftest.py` | QA Lead | ✅ |
| QA-029 | INFRA | Configuration coverage (.coveragerc) | Must | XS | — | `.coveragerc` | QA Lead | ✅ |
| QA-030 | INFRA | Configuration Behave (behave.ini) | Must | XS | — | `behave.ini` | QA Lead | ✅ |
| QA-031 | INFRA | Plan de test Sprint 1 | Must | M | — | `docs/test_plan_sprint1.md` | QA Lead | ✅ |
| QA-032 | INFRA | Matrice de traçabilité | Must | M | — | `docs/traceability_matrix.md` | QA Lead | ✅ |
| QA-033 | INFRA | Template rapport de bug | Must | S | — | `bugs/bug_report_template.md` | QA Engineer | ✅ |
| QA-034 | INFRA | Registre des bugs connus | Must | S | — | `bugs/known_bugs_sprint1.md` | QA Engineer | ✅ |
| QA-035 | INFRA | Template PR GitHub | Should | XS | — | `.github/PULL_REQUEST_TEMPLATE.md` | QA Lead | ✅ |
| QA-036 | INFRA | Tests sécurité basiques | Should | S | Sécurité | `tests/security/test_auth_security.py` | QA Engineer | ⏳ |

---

## Légende Effort

| Code | Effort | Description |
|---|---|---|
| **XS** | < 1h | Micro-tâche (configuration, template) |
| **S** | 1-2h | Petite tâche (test unitaire simple) |
| **M** | 2-4h | Tâche moyenne (test d'intégration, feature BDD) |
| **L** | 4-8h | Grande tâche (flux complet E2E) |
| **XL** | > 8h | Tâche très grande (suite de tests complète) |

---

## Légende Statut

| Symbole | Statut |
|---|---|
| ✅ | Terminé |
| 🔄 | En cours |
| ⏳ | À faire |
| ❌ | Bloqué |

---

## Synthèse de l'effort

| Catégorie | Nombre | Effort total estimé |
|---|:---:|:---:|
| Tests unitaires | 12 | ~18h |
| Tests d'intégration | 12 | ~30h |
| Tests BDD | 6 | ~16h |
| Tests API | 3 | ~4h |
| Tests sécurité | 1 | ~1h |
| Infrastructure | 9 | ~10h |
| **TOTAL** | **43** | **~79h** |

> **Note :** L'effort total dépasse la capacité du Sprint (40h). Les tâches
> marquées « Should » sont candidates à être repoussées au Sprint 2 si nécessaire.
> Les tâches « Must » constituent le minimum viable du Sprint.
"""

# ---------- .github/PULL_REQUEST_TEMPLATE.md ----------
PULL_REQUEST_TEMPLATE = """\
## 📋 Description

_Breve description des modifications apportées par cette Pull Request._

**Issue(s) liée(s) :** #XXX, #YYY

**Type de modification :**
- [ ] 🐛 Correction de bug
- [ ] ✨ Nouvelle fonctionnalité
- [ ] 🧪 Tests
- [ ] 📝 Documentation
- [ ] 🔧 Configuration / Infrastructure
- [ ] ♻️ Refactoring
- [ ] 🎨 Style / UI

---

## 🧪 Tests

- [ ] Des tests unitaires ont été ajoutés / modifiés
- [ ] Des tests d'intégration ont été ajoutés / modifiés
- [ ] Des tests BDD (Behave) ont été ajoutés / modifiés
- [ ] Tous les tests passent : `pytest`
- [ ] La couverture de code est ≥ 80% : `pytest --cov=.`
- [ ] Aucun marqueur orphelin : `pytest --strict-markers`

**Commandes exécutées :**
```bash
pytest -v
pytest --cov=. --cov-report=term-missing
```

---

## 📦 Changements

### Fichiers ajoutés
- `path/to/file1.py`
- `path/to/file2.py`

### Fichiers modifiés
- `path/to/file3.py`

### Fichiers supprimés
- `path/to/file4.py`

---

## ✅ Checklist de Revue

- [ ] Le code suit les conventions PEP 8
- [ ] Les commentaires et docstrings sont en français
- [ ] Les noms de variables et fonctions sont en anglais
- [ ] Les tests couvrent les cas nominaux et les cas d'erreur
- [ ] Les fixtures pytest sont correctement utilisées
- [ ] Aucun `print()` ou `debug` en production
- [ ] Les migrations sont fournies si nécessaire
- [ ] La documentation a été mise à jour si nécessaire
- [ ] Les marqueurs pytest sont corrects (`@pytest.mark.unit`, etc.)

---

## 🔍 Notes pour les relecteurs

_Points d'attention particuliers pour la revue de code._

- `[Ex: Le modèle Flight a été modifié — vérifier les impacts sur Booking]`
- `[Ex: La validation du formulaire a changé — vérifier les tests BDD]`

---

## 📸 Captures d'écran (si applicable)

_Ajoutez des captures d'écran pour les modifications visuelles._

| Avant | Après |
|---|---|
| ![Avant](lien) | ![Après](lien) |

---

**Merci pour votre revue !** ✈️ NouvelAir QA Team
"""

# ---------- README_QA_SECTION ----------
README_QA_SECTION = """
---

## 🧪 Testing & QA

### Structure des Tests

```
nouvelair_project/
├── tests/                      # Racine des tests
│   ├── conftest.py             # Fixtures communes (pytest)
│   ├── unit/                   # Tests unitaires (60%)
│   │   ├── test_flight_model.py
│   │   ├── test_booking_model.py
│   │   ├── test_account_forms.py
│   │   └── ...
│   ├── integration/            # Tests d'intégration (25%)
│   │   ├── test_search_flow.py
│   │   ├── test_booking_flow.py
│   │   └── ...
│   ├── api/                    # Tests API REST (5%)
│   │   ├── test_flight_api.py
│   │   └── ...
│   ├── e2e/                    # Tests bout en bout (5%)
│   │   ├── pages/              # Page Objects
│   │   └── ...
│   ├── performance/            # Tests de performance
│   └── security/               # Tests de sécurité
├── features/                   # Tests BDD (Behave / Gherkin)
│   ├── search_flights.feature
│   ├── book_flight.feature
│   └── steps/
│       ├── search_steps.py
│       └── booking_steps.py
├── reports/                    # Rapports de test
│   ├── allure-results/
│   └── htmlcov/
├── pytest.ini                  # Configuration pytest
├── behave.ini                  # Configuration Behave
├── .coveragerc                 # Configuration Coverage
└── bugs/                       # Suivi des anomalies
```

### Exécution des Tests

```bash
# Exécuter tous les tests
pytest

# Exécuter par type
pytest -m unit              # Tests unitaires uniquement
pytest -m integration       # Tests d'intégration
pytest -m api               # Tests API
pytest -m bdd               # Tests BDD

# Exécuter avec couverture
pytest --cov=. --cov-report=html --cov-report=term-missing

# Tests BDD (Behave)
behave features/

# Tests avec Allure
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Marqueurs pytest

| Marqueur | Description |
|---|---|
| `@pytest.mark.unit` | Test unitaire |
| `@pytest.mark.integration` | Test d'intégration |
| `@pytest.mark.api` | Test API |
| `@pytest.mark.bdd` | Test BDD |
| `@pytest.mark.e2e` | Test bout en bout |
| `@pytest.mark.performance` | Test de performance |
| `@pytest.mark.security` | Test de sécurité |
| `@pytest.mark.slow` | Test lent (> 5s) |
| `@pytest.mark.regression` | Test de régression |

### Couverture de Code

[![Coverage Status](https://img.shields.io/badge/coverage-80%25%2B-green)](reports/htmlcov/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

> Objectif : **≥ 80%** de couverture sur l'ensemble des applications.

### CI / CD

[![CI Pipeline](https://img.shields.io/badge/CI-pending-yellow)]()

Les tests sont exécutés automatiquement à chaque push et pull request.
"""


# ====================================================================
# FONCTIONS UTILITAIRES
# ====================================================================

def print_banner():
    """Affiche la bannière d'accueil."""
    print(BANNER)


def create_directories(base_path: Path) -> list:
    """
    Crée toute l'arborescence de répertoires.

    Args:
        base_path: Chemin racine du projet.

    Returns:
        Liste des répertoires créés.
    """
    created = []
    for directory in DIRECTORIES:
        full_path = base_path / directory
        if not full_path.exists():
            os.makedirs(full_path, exist_ok=True)
            created.append(str(full_path))
    return created


def write_file(base_path: Path, relative_path: str, content: str) -> str:
    """
    Écrit un fichier avec encodage UTF-8.

    Args:
        base_path: Chemin racine du projet.
        relative_path: Chemin relatif du fichier.
        content: Contenu du fichier.

    Returns:
        Chemin complet du fichier écrit.
    """
    full_path = base_path / relative_path
    # Créer les répertoires parents si nécessaire
    os.makedirs(full_path.parent, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    return str(full_path)


def main():
    """Point d'entrée principal du script d'installation."""
    print_banner()

    # Vérification du répertoire courant
    expected_files = ["manage.py", "nouvelair"]
    has_manage = (PROJECT_ROOT / "manage.py").exists()
    has_settings = (PROJECT_ROOT / "nouvelair").exists() or (PROJECT_ROOT / "nouvelair_project").exists()

    if not has_manage:
        print("⚠️  AVERTISSEMENT : Le fichier 'manage.py' est introuvable.")
        print(f"    Répertoire courant : {PROJECT_ROOT}")
        print("    Assurez-vous d'exécuter ce script depuis la racine du projet Django.")
        print()

    print(f"📁 Répertoire racine : {PROJECT_ROOT}")
    print(f"   OS                : {os.name}")
    print(f"   Date              : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 1 : Création des répertoires
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 1/12 — Création de l'arborescence des répertoires")
    print("=" * 64)

    dirs_created = create_directories(PROJECT_ROOT)
    for d in dirs_created:
        print(f"   ✅ {d}")
    print(f"   📊 {len(dirs_created)} répertoire(s) créé(s)")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 2 : pytest.ini
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 2/12 — Configuration pytest (pytest.ini)")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, "pytest.ini", PYTEST_INI)
    print(f"   ✅ {path}")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 3 : tests/__init__.py
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 3/12 — Fichiers __init__.py des modules de test")
    print("=" * 64)

    init_files = {
        "tests/__init__.py": TESTS_INIT_PY,
        "tests/unit/__init__.py": TESTS_UNIT_INIT,
        "tests/integration/__init__.py": TESTS_INTEGRATION_INIT,
        "tests/api/__init__.py": TESTS_API_INIT,
        "tests/e2e/__init__.py": TESTS_E2E_INIT,
        "tests/e2e/pages/__init__.py": TESTS_E2E_PAGES_INIT,
        "tests/performance/__init__.py": TESTS_PERFORMANCE_INIT,
        "tests/security/__init__.py": TESTS_SECURITY_INIT,
        "features/__init__.py": FEATURES_INIT,
        "features/steps/__init__.py": FEATURES_STEPS_INIT,
    }

    for rel_path, content in init_files.items():
        p = write_file(PROJECT_ROOT, rel_path, content)
        print(f"   ✅ {p}")
    print(f"   📊 {len(init_files)} fichier(s) __init__.py créé(s)")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 4 : tests/conftest.py
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 4/12 — Fixtures communes (tests/conftest.py)")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, "tests/conftest.py", TESTS_CONFTEST_PY)
    print(f"   ✅ {path}")
    print("   📋 Fixtures disponibles :")
    print("      • db (pytest-django, via @pytest.mark.django_db)")
    print("      • authenticated_client")
    print("      • sample_airport (TUN)")
    print("      • sample_airport_paris (CDG)")
    print("      • sample_aircraft (A320neo)")
    print("      • sample_flight (BJ520)")
    print("      • sample_booking")
    print("      • api_client")
    print("      • future_date")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 5 : .coveragerc
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 5/12 — Configuration Coverage (.coveragerc)")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, ".coveragerc", COVERAGERC)
    print(f"   ✅ {path}")
    print("   📊 Seuil minimum : 80%")
    print("   📊 Source analysée : flights, bookings, accounts, destinations, promotions")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 6 : behave.ini
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 6/12 — Configuration Behave (behave.ini)")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, "behave.ini", BEHAVE_INI)
    print(f"   ✅ {path}")
    print("   🌐 Langue Gherkin : Français")
    print("   📂 Chemin features : features/")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 7 : docs/test_plan_sprint1.md
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 7/12 — Plan de test Sprint 1")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, "docs/test_plan_sprint1.md", TEST_PLAN_SPRINT1)
    print(f"   ✅ {path}")
    print("   📋 Sections : Objectif, Périmètre, Hors périmètre, Environnement,")
    print("      Critères d'entrée/sortie, Risques, Stratégie (pyramide),")
    print("      Ressources, Planning Jour 1-5, Approbation")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 8 : docs/traceability_matrix.md
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 8/12 — Matrice de traçabilité")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, "docs/traceability_matrix.md", TRACEABILITY_MATRIX)
    print(f"   ✅ {path}")
    print("   📊 14 User Stories tracées (US-001 à US-010, US-028 à US-031)")
    print("   📊 5 types de test couverts (U, I, B, A, E)")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 9 : bugs/bug_report_template.md
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 9/12 — Template de rapport de bug")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, "bugs/bug_report_template.md", BUG_REPORT_TEMPLATE)
    print(f"   ✅ {path}")
    print("   📋 Sections : Titre, ID, Sévérité, Priorité, Composant,")
    print("      Environnement, Description, Steps to Reproduce,")
    print("      Résultat Attendu / Obtenu, Preuves, Suivi")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 10 : bugs/known_bugs_sprint1.md
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 10/12 — Registre des bugs connus Sprint 1")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, "bugs/known_bugs_sprint1.md", KNOWN_BUGS_SPRINT1)
    print(f"   ✅ {path}")
    print("   📊 7 bugs documentés :")
    print("      • BUG-001 : Fichiers statiques manquants (Low, Ouvert)")
    print("      • BUG-002 : Selenium Broken pipe (Low, Ouvert)")
    print("      • BUG-003 : Validation origine≠destination (Medium, ✅ Corrigé)")
    print("      • BUG-004 : Double création UserProfile (High, ✅ Corrigé)")
    print("      • BUG-005 : Message login non cohérent (Medium, ✅ Corrigé)")
    print("      • BUG-006 : Conflit URL promotions (High, ✅ Corrigé)")
    print("      • BUG-007 : Tests E2E mauvaises URLs (High, ✅ Corrigé)")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 11 : docs/sprint_backlog.md
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 11/12 — Backlog Sprint 1")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, "docs/sprint_backlog.md", SPRINT_BACKLOG)
    print(f"   ✅ {path}")
    print("   📊 36 entrées (QA-001 à QA-036)")
    print("   📊 Effort estimé : ~79h (capacité Sprint : 40h)")
    print()

    # ─────────────────────────────────────────────────────────────
    # Étape 12 : .github/PULL_REQUEST_TEMPLATE.md
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ÉTAPE 12/12 — Template Pull Request GitHub")
    print("=" * 64)

    path = write_file(PROJECT_ROOT, ".github/PULL_REQUEST_TEMPLATE.md", PULL_REQUEST_TEMPLATE)
    print(f"   ✅ {path}")
    print()

    # ─────────────────────────────────────────────────────────────
    # Bonus : Section QA dans README.md
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  BONUS — Mise à jour du README.md")
    print("=" * 64)

    readme_path = PROJECT_ROOT / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            existing_content = f.read()

        # Vérifier si la section existe déjà
        if "## 🧪 Testing & QA" not in existing_content:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(existing_content + README_QA_SECTION)
            print(f"   ✅ Section 'Testing & QA' ajoutée à {readme_path}")
        else:
            print(f"   ℹ️  La section 'Testing & QA' existe déjà dans {readme_path}")
    else:
        # Créer le README avec la section QA
        readme_header = f"""\
# ✈️ NouvelAir — Système de Réservation Aérienne

> Votre Compagnie Aérienne de Confiance

## 🚀 Démarrage Rapide

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Accédez à l'application sur : http://127.0.0.1:8000/

"""
        write_file(PROJECT_ROOT, "README.md", readme_header + README_QA_SECTION)
        print(f"   ✅ README.md créé avec section 'Testing & QA'")
    print()

    # ─────────────────────────────────────────────────────────────
    # RÉSUMÉ FINAL
    # ─────────────────────────────────────────────────────────────
    print("=" * 64)
    print("  ✨  RÉSUMÉ DE L'INSTALLATION — Jour 1  ✨")
    print("=" * 64)
    print()

    # Comptage total des fichiers créés
    all_files = [
        "pytest.ini",
        ".coveragerc",
        "behave.ini",
        "tests/__init__.py",
        "tests/unit/__init__.py",
        "tests/integration/__init__.py",
        "tests/api/__init__.py",
        "tests/e2e/__init__.py",
        "tests/e2e/pages/__init__.py",
        "tests/performance/__init__.py",
        "tests/security/__init__.py",
        "tests/conftest.py",
        "features/__init__.py",
        "features/steps/__init__.py",
        "docs/test_plan_sprint1.md",
        "docs/traceability_matrix.md",
        "docs/sprint_backlog.md",
        "bugs/bug_report_template.md",
        "bugs/known_bugs_sprint1.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        "README.md (section QA ajoutée)",
    ]

    print(f"   📁 Répertoires créés    : {len(dirs_created)}")
    print(f"   📄 Fichiers créés        : {len(all_files)}")
    print(f"   📋 Fixtures pytest       : 10")
    print(f"   📊 Marqueurs pytest      : 9")
    print(f"   🐛 Bugs documentés       : 7")
    print(f"   📋 Backlog entries       : 36")
    print(f"   🔗 US tracées            : 14")
    print()

    print("   📂 Arborescence créée :")
    print()
    tree_lines = """\
    nouvelair_project/
    ├── pytest.ini                          ← Configuration pytest
    ├── behave.ini                          ← Configuration Behave
    ├── .coveragerc                         ← Configuration Coverage
    ├── README.md                           ← Section QA ajoutée
    ├── .github/
    │   └── PULL_REQUEST_TEMPLATE.md       ← Template PR
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py                     ← Fixtures communes
    │   ├── unit/                           ← Tests unitaires (60%)
    │   ├── integration/                    ← Tests intégration (25%)
    │   ├── api/                            ← Tests API REST (5%)
    │   ├── e2e/                            ← Tests E2E (5%)
    │   │   └── pages/                      ← Page Objects
    │   ├── performance/                    ← Tests performance
    │   └── security/                       ← Tests sécurité
    ├── features/
    │   ├── __init__.py
    │   └── steps/                          ← Steps Behave
    ├── docs/
    │   ├── test_plan_sprint1.md            ← Plan de test
    │   ├── traceability_matrix.md          ← Matrice de traçabilité
    │   └── sprint_backlog.md               ← Backlog Sprint 1
    ├── reports/
    │   ├── allure-results/                 ← Résultats Allure
    │   └── htmlcov/                        ← Rapport couverture HTML
    └── bugs/
        ├── bug_report_template.md          ← Template de bug
        └── known_bugs_sprint1.md           ← Bugs connus Sprint 1"""

    for line in tree_lines.split("\n"):
        print(f"   {line}")
    print()

    print("=" * 64)
    print("  🎉  Installation Jour 1 terminée avec succès !")
    print("=" * 64)
    print()
    print("  Prochaines étapes :")
    print("  1. Vérifier la configuration : pytest --collect-only")
    print("  2. Exécuter les tests existants : pytest -v")
    print("  3. Commencer les tests unitaires (Jour 2)")
    print("  4. Consulter le plan de test : docs/test_plan_sprint1.md")
    print()

    return 0


# ====================================================================
# Point d'entrée
# ====================================================================
if __name__ == "__main__":
    sys.exit(main())
