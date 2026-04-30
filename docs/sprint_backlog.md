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
