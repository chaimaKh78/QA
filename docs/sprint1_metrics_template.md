# 📊 Métriques de Qualité - Sprint 1 (NouvelAir)

> **Projet:** NouvelAir - Système de Réservation Aérienne  
> **Sprint:** 1  
> **Date de mise à jour:** JJ/MM/AAAA  
> **Équipe:** [Noms des membres]

---

## 1. Métriques de Tests Unitaires

| Métrique | Cible | Réel | Statut |
|----------|-------|------|--------|
| Nombre total de tests unitaires | ≥ 30 | `_ _ _` | ⬜ |
| Tests passés | 100% | `_ _ _` | ⬜ |
| Tests échoués | 0 | `_ _ _` | ⬜ |
| Taux de réussite | 100% | `_ _ _ %` | ⬜ |
| Temps d'exécution moyen | < 10s | `_ _ _ s` | ⬜ |

### Répartition par application

| Application | Tests | Passés | Échoués | Couverture |
|-------------|-------|--------|---------|------------|
| `flights` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| `bookings` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| `accounts` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| `destinations` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| `promotions` | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |

---

## 2. Métriques de Tests d'Intégration

| Métrique | Cible | Réel | Statut |
|----------|-------|------|--------|
| Nombre total de tests d'intégration | ≥ 15 | `_ _ _` | ⬜ |
| Tests passés | 100% | `_ _ _` | ⬜ |
| Tests échoués | 0 | `_ _ _` | ⬜ |
| Temps d'exécution total | < 30s | `_ _ _ s` | ⬜ |

### Scénarios d'intégration testés

| Scénario | Endpoint(s) | Statut | Remarques |
|----------|-------------|--------|-----------|
| Recherche de vol complète | `POST /` → `/recherche/` | ⬜ | |
| Création de réservation | `POST /reservations/creer/` | ⬜ | |
| Recherche de réservation | `POST /reservations/recherche/` | ⬜ | |
| Inscription + Connexion | `POST /compte/inscription/` → `/connexion/` | ⬜ | |
| Annulation de réservation | `POST /reservations/annuler/` | ⬜ | |

---

## 3. Métriques BDD (Gherkin)

| Métrique | Cible | Réel | Statut |
|----------|-------|------|--------|
| Nombre de scénarios Gherkin | ≥ 10 | `_ _ _` | ⬜ |
| Scénarios passés (Behave) | 100% | `_ _ _` | ⬜ |
| Étapes définies (steps) | ≥ 30 | `_ _ _` | ⬜ |
| Fichiers feature | ≥ 5 | `_ _ _` | ⬜ |

### Répartition par fichier feature

| Feature File | Scénarios | Passés | Échoués |
|--------------|-----------|--------|---------|
| `search_flights.feature` | `_ _ _` | `_ _ _` | `_ _ _` |
| `booking_management.feature` | `_ _ _` | `_ _ _` | `_ _ _` |
| `user_authentication.feature` | `_ _ _` | `_ _ _` | `_ _ _` |
| `newsletter.feature` | `_ _ _` | `_ _ _` | `_ _ _` |
| `booking_lookup.feature` | `_ _ _` | `_ _ _` | `_ _ _` |

---

## 4. Métriques API

| Métrique | Cible | Réel | Statut |
|----------|-------|------|--------|
| Nombre total de tests API | ≥ 30 | `_ _ _` | ⬜ |
| Tests API passés | 100% | `_ _ _` | ⬜ |
| Temps de réponse moyen | < 500ms | `_ _ _ ms` | ⬜ |
| Taux d'erreur API | 0% | `_ _ _ %` | ⬜ |

### Détail par endpoint API

| Endpoint | Méthode | Tests | Passés | Temps moyen |
|----------|---------|-------|--------|-------------|
| `/api/airports/autocomplete/` | GET | 10 | `_ _ _` | `_ _ _ ms` |
| `/reservations/recherche/` | GET/POST | 4 | `_ _ _` | `_ _ _ ms` |
| `/reservations/creer/` | POST | 2 | `_ _ _` | `_ _ _ ms` |
| `/reservations/annuler/<uuid>` | POST | 2 | `_ _ _` | `_ _ _ ms` |
| `/compte/connexion/` | POST | 3 | `_ _ _` | `_ _ _ ms` |
| `/compte/inscription/` | POST | 2 | `_ _ _` | `_ _ _ ms` |
| `/compte/deconnexion/` | GET | 1 | `_ _ _` | `_ _ _ ms` |
| `/promotions/newsletter/` | POST | 5 | `_ _ _` | `_ _ _ ms` |

---

## 5. Couverture de Code

| Application | Lignes totales | Lignes couvertes | Couverture % | Statut |
|-------------|---------------|------------------|--------------|--------|
| `flights` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| `bookings` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| `accounts` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| `destinations` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| `promotions` | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |
| **Total** | `_ _ _` | `_ _ _` | `_ _ _ %` | ⬜ |

### Commande de génération du rapport

```bash
coverage run --source='.' manage.py test
coverage report --skip-covered
coverage html
```

---

## 6. Bugs Documentés

| ID | Sévérité | Description | Statut | Assigné | Date |
|----|----------|-------------|--------|---------|------|
| BUG-001 | 🔴 Critique | `_ _ _` | ⬜ Ouvert | `_ _ _` | JJ/MM |
| BUG-002 | 🟡 Moyen | `_ _ _` | ⬜ Ouvert | `_ _ _` | JJ/MM |
| BUG-003 | 🟢 Mineur | `_ _ _` | ⬜ Résolu | `_ _ _` | JJ/MM |

---

## 7. Taux de Réussite Global

| Catégorie | Tests | Passés | Échoués | Taux |
|-----------|-------|--------|---------|------|
| Unitaires | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| Intégration | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| BDD (Gherkin) | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| API | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |
| **Total** | `_ _ _` | `_ _ _` | `_ _ _` | `_ _ _ %` |

### Objectifs Sprint 2

- [ ] Atteindre ≥ 80% de couverture de code
- [ ] Zéro test échoué
- [ ] Temps d'exécution total < 60s
- [ ] Tous les endpoints API testés

---

*Généré automatiquement - Template Sprint 1 NouvelAir*
