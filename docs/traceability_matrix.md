# 🔗 Matrice de Traçabilité — Sprint 1

## NouvelAir — Correspondance User Stories ↔ Cas de Test

| **Document** | Matrice de Traçabilité Sprint 1 |
|---|---|
| **Version** | 1.0.0 |
| **Date** | 23/04/2026 |
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
