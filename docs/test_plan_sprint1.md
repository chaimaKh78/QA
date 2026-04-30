# 📋 Plan de Test — Sprint 1

## NouvelAir — Système de Réservation Aérienne

| **Document** | Plan de Test Sprint 1 |
|---|---|
| **Version** | 1.0.0 |
| **Date** | 23/04/2026 |
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
venv\Scripts\activate        # Windows
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
            /\
           /  \         Tests E2E (5%)
          /----\        Selenium / Playwright
         /      \       Sprint 2+
        /--------\
       /  Tests    \    Tests BDD (10%)
      /    BDD      \   Behave + Gherkin
     /----------------\
    /   Tests API      \  Tests API (5%)
   /     REST           \ Endpoints Django
  /----------------------\
 /    Tests d'Intégration  \ Tests d'intégration (25%)
/   Flux multi-composants    \ pytest + pytest-django
/------------------------------\
/      Tests Unitaires (60%)    \ Modèles, Formulaires, Utils
/  pytest + pytest-django +      \
/   Factory Boy + Hypothesis     \
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
