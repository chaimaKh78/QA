# 📊 Rapport de Couverture de Tests — Sprint 1

> **Projet** : NouvelAir — Système de réservation aérienne
> **Date** : Sprint 1 — Jour 3
> **Auteur** : Équipe de développement

---

## 1. Comment exécuter les tests avec couverture

### Installation des prérequis

```bash
pip install pytest pytest-django pytest-cov
```

### Configuration minimale (`pytest.ini`)

Placez ce fichier à la racine du projet (à côté de `manage.py`) :

```ini
[pytest]
DJANGO_SETTINGS_MODULE = nouvelair.settings
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    integration: Tests d'intégration (Django Test Client)
testpaths = tests
```

### Commandes de base

```bash
# Exécuter uniquement les tests d'intégration
pytest tests/integration/ -m integration -v

# Exécuter avec couverture de code (terminal)
pytest tests/integration/ -m integration --cov=. --cov-report=term-missing

# Exécuter avec couverture de code (rapport HTML)
pytest tests/integration/ -m integration --cov=. --cov-report=html

# Exécuter avec couverture et rapport XML (pour CI)
pytest tests/integration/ -m integration --cov=. --cov-report=xml:coverage.xml

# Couverture par application spécifique
pytest tests/integration/ -m integration --cov=flights --cov=accounts --cov=bookings --cov=destinations --cov=promotions --cov-report=term-missing
```

---

## 2. Objectifs de couverture

| Application   | Cible (%) | Priorité | Modules critiques                       |
|---------------|-----------|----------|----------------------------------------|
| `flights`     | ≥ 85%     | 🔴 Haute | `views.py`, `models.py`, `forms.py`    |
| `accounts`    | ≥ 85%     | 🔴 Haute | `views.py`, `forms.py`, `signals.py`   |
| `bookings`    | ≥ 80%     | 🔴 Haute | `views.py`, `models.py`, `forms.py`    |
| `destinations`| ≥ 80%     | 🟡 Moyen | `views.py`, `models.py`                |
| `promotions`  | ≥ 75%     | 🟡 Moyen | `views.py`, `models.py`                |
| **Global**    | ≥ 80%     | —        | —                                      |

---

## 3. Comment lire le rapport HTML

1. Après exécution de `--cov-report=html`, un dossier `htmlcov/` est généré.
2. Ouvrez `htmlcov/index.html` dans votre navigateur.
3. **Navigation** :
   - Cliquez sur chaque module pour voir les lignes couvertes (vert) et non couvertes (rouge).
   - Les branches conditionnelles sont indiquées en orange/jaune.
4. **Indicateurs clés** :
   - **Lines** : pourcentage de lignes exécutées.
   - **Branches** : pourcentage de branches conditionnelles couvertes.

---

## 4. Modules à prioriser pour la couverture

### 🔴 Priorité haute — `flights/views.py`

Les vues critiques à couvrir en priorité :

| Vue                    | Lignes à couvrir             | Statut actuel |
|------------------------|------------------------------|---------------|
| `HomeView`             | GET, POST, validation        | ✅ Jour 3     |
| `FlightSearchResultsView` | GET avec/sans session     | ✅ Jour 3     |
| `FlightDetailView`     | GET, contexte, 404           | ✅ Jour 3     |
| `AirportListView`      | GET, queryset                | ✅ Jour 3     |
| `airport_autocomplete` | GET avec query, vide         | ✅ Jour 3     |

### 🔴 Priorité haute — `accounts/views.py`

| Vue               | Lignes à couvrir        | Statut actuel |
|-------------------|-------------------------|---------------|
| `LoginView`       | GET, POST, invalid     | ✅ Jour 3     |
| `LogoutView`      | GET, redirect          | ✅ Jour 3     |
| `RegisterView`    | GET, POST, duplicate   | ✅ Jour 3     |
| `ProfileView`     | GET, POST, update      | ✅ Jour 3     |

### 🔴 Priorité haute — `bookings/views.py`

| Vue                    | Lignes à couvrir              | Statut actuel |
|------------------------|-------------------------------|---------------|
| `BookingCreateView`    | GET, POST, session            | ✅ Jour 3     |
| `MyBookingsView`       | GET avec/sans auth            | ✅ Jour 3     |
| `BookingCancelView`    | POST, status change           | ✅ Jour 3     |
| `BookingLookupView`    | GET, POST, lookup by ref      | ✅ Jour 3     |
| `select_flight`        | GET, session, redirect        | ✅ Jour 3     |

---

## 5. Interpréter les résultats

### Couverture idéale : ≥ 90%
```
flights/views.py     92%  ██████████████████░░░  184/200 lignes
accounts/views.py    88%  █████████████████░░░░  132/150 lignes
bookings/views.py    85%  ████████████████░░░░░  170/200 lignes
```

### Couverture insuffisante : < 70%
- 🔴 Action requise : ajouter des tests pour les branches non couvertes.
- Vérifiez les gestionnaires d'erreur (`try/except`), les conditions `if/else` rares.

### Couverture acceptable : 70–85%
- 🟡 Amélioration continue : identifiez les scénarios limites (edge cases).

---

## 6. Bonnes pratiques

1. **Exécuter les tests avant chaque commit** :
   ```bash
   pytest tests/integration/ -m integration --cov=flights --cov=accounts --cov=bookings --cov-report=term-missing -q
   ```

2. **Ne jamais viser 100%** : les imports, la configuration et les handlers d'erreurs rarement atteignables n'ont pas besoin d'être couverts.

3. **Privilégier la qualité à la quantité** : un test d'intégration bien conçu vaut mieux que dix tests unitaires triviaux.

4. **Utiliser les marqueurs** : `@pytest.mark.integration` permet de séparer les tests unitaires des tests d'intégration dans les rapports.

5. **Couverture par branche** : utilisez `--cov-branch` pour vérifier la couverture des conditions booléennes.
   ```bash
   pytest tests/integration/ -m integration --cov=. --cov-branch --cov-report=html
   ```

---

## 7. Commande récapitulative

```bash
# 🚀 Commande complète recommandée pour le Sprint 1
pytest tests/integration/ -m integration \
    --cov=flights --cov=accounts --cov=bookings --cov=destinations --cov=promotions \
    --cov-report=term-missing:skip-covered \
    --cov-report=html \
    -v
```

---

*Document généré automatiquement par `setup_jour3.py`*
