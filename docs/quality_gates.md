# Portes de Qualité (Quality Gates) - NouvelAir
# ================================================
# Version: 1.0.0
# Date: Jour 9
# Auteur: Équipe QA NouvelAir

## Vue d'ensemble

Les **portes de qualité** sont des seuils obligatoires que le code doit franchir
avant d'être accepté dans la branche `main`. Elles garantissent un niveau de
qualité constant et préviennent les régressions.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PORTES DE QUALITÉ                              │
│                                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ LINTING │  │ COUVERT. │  │ INTEG.  │  │  BDD    │  │ SECURE  │ │
│  │  0 err  │  │  >= 80% │  │  0 fail │  │  0 fail │  │ 0 HIGH  │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘ │
│       │            │            │            │             │       │
│       └────────────┴────────────┴────────────┴─────────────┘       │
│                              │                                     │
│                        ┌─────▼──────┐                              │
│                        │  PIPELINE  │                              │
│                        │   PASS ✅   │                              │
│                        └────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. Couverture de Tests Unitaires >= 80%

### Description
Le pourcentage de code couvert par les tests unitaires doit être d'au moins 80%.
Cela garantit que la majorité du code métier est testée.

### Configuration
```yaml
# .github/workflows/tests.yml
pytest tests/unit/ -m unit --cov --cov-report=xml --cov-report=html --cov-fail-under=80
```

### Comment mesurer localement
```bash
pytest tests/unit/ -m unit --cov --cov-report=term-missing
```

### Comment améliorer la couverture
1. Identifier les fichiers/modules avec la couverture la plus basse
2. Ajouter des tests pour les branches de code non couvertes
3. Prioriser les chemins critiques (paiement, réservation, auth)

### Exemple de sortie
```
---------- coverage: platform linux, python 3.12.0 ----------
TOTAL                                  4521    785    82.6%
```
Si le total est < 80%, le pipeline **échoue**.

### Fichiers exclus de la couverture
- `migrations/` (générés automatiquement)
- `*/admin.py` (interface admin Django)
- `*/tests/*` (le code de test lui-même)

---

## 2. Tests d'Intégration: Tous Passent

### Description
Tous les tests d'intégration doivent réussir sans exception. Les tests d'intégration
vérifient que les modules fonctionnent correctement ensemble.

### Configuration
```yaml
pytest tests/integration/ -m integration -v
```

### Critères
- **0 test échoué**: Tous les tests doivent passer
- **0 erreur inattendue**: Pas d'exception non gérée

### Comment mesurer localement
```bash
pytest tests/integration/ -m integration -v --tb=short
```

### Types de tests d'intégration
- Test des vues avec Client Django
- Test des workflows multi-étapes (recherche → réservation → paiement)
- Test des interactions entre modèles
- Test des signaux et hooks

---

## 3. Tests BDD: Tous les Scénarios Verts

### Description
Tous les scénarios Behave marqués avec les tags `sprint1` ou `sprint2` doivent
passer (statut "vert"). Les scénarios BDD décrivent le comportement attendu
en langage naturel.

### Configuration
```bash
behave features/ --tags=sprint1,sprint2 -f pretty
```

### Critères
- **0 scénario échoué**: Tous les scénarios doivent passer
- **0 step undefined**: Tous les steps doivent avoir une implémentation

### Comment mesurer localement
```bash
behave features/ --tags=sprint1,sprint2 -f pretty --no-capture
```

### Tags disponibles
- `@sprint1`: Scénarios du sprint 1
- `@sprint2`: Scénarios du sprint 2
- `@wip`: Scénarios en cours (ignorés en CI)

### Structure d'un scénario
```gherkin
@sprint2
Scenario: Un utilisateur peut réserver un vol
  Given je suis sur la page d'accueil
  And je recherche un vol de TUN vers CDG
  When je sélectionne un vol
  And je remplis les informations passager
  Then la réservation est confirmée
```

---

## 4. Sécurité: 0 Vulnérabilité HIGH

### Description
L'analyse de sécurité doit détecter 0 vulnérabilité de sévérité HIGH. Cela inclut
la vérification du code source (bandit) et des dépendances (safety).

### Configuration
```yaml
# Code source
bandit -r . -f json -o bandit_results.json

# Dépendances
safety check
```

### Critères
- **0 HIGH** dans les résultats bandit
- **0 HIGH/Critical** dans les résultats safety

### Comment mesurer localement
```bash
# Analyser le code source
bandit -r . -f screen

# Vérifier les dépendances
safety check
```

### Sévérités prises en compte

| Sévérité | Action | Pipeline |
|----------|--------|----------|
| HIGH | ❌ Bloquant | Échec du pipeline |
| MEDIUM | ⚠️ Avertissement | Continue |
| LOW | ℹ️ Information | Continue |

### Exemples de vulnérabilités courantes
- Utilisation de `assert` dans le code de production
- Mots de passe codés en dur
- Utilisation de `eval()` ou `exec()`
- Dépendances avec des CVE connues

---

## 5. Performance: Latence Médiane < 3 secondes

### Description
Sous une charge de 10 utilisateurs simultanés pendant 60 secondes,
la latence médiane des requêtes doit rester en dessous de 3000ms.

### Configuration
```yaml
locust -f locustfile_qa.py \
  --users 10 \
  --spawn-rate 2 \
  --run-time 60s \
  --headless
```

### Critères
- **Latence médiane < 3000ms** pour l'ensemble des endpoints
- **0 erreur 5xx** pendant le test

### Comment mesurer localement
```bash
# 1. Démarrer le serveur
python manage.py runserver

# 2. Exécuter le test de charge (dans un autre terminal)
locust -f scripts/locustfile_qa.py \
  --host=http://localhost:8000 \
  --users 10 --spawn-rate 2 --run-time 60s --headless
```

### Endpoints testés
| Endpoint | Priorité | Seuil |
|----------|----------|-------|
| `/` (Accueil) | Critique | < 500ms |
| `/recherche/` (Recherche) | Critique | < 1000ms |
| `/aeroports/` (Aéroports) | Normal | < 1000ms |
| `/promotions/` (Promotions) | Normal | < 1500ms |
| `/destinations/` (Destinations) | Normal | < 1500ms |

### Améliorations recommandées
- Ajouter du cache (Redis) pour les pages statiques
- Optimiser les requêtes SQL avec `select_related` / `prefetch_related`
- Utiliser la pagination pour les listes longues
- Activer la compression gzip

---

## 6. Flake8: 0 Erreurs

### Description
Le linter flake8 ne doit détecter aucune erreur fatale. Les erreurs fatales
incluent les erreurs de syntaxe, d'importation et d'exécution.

### Configuration
```ini
# .flake8
max-line-length = 120
exclude = migrations, venv, __pycache__, .git
ignore = E203, E266, E501, W503
```

### Critères
- **0 erreur fatale** (catégories E9, F63, F7, F82)
- Les avertissements (W, E, C) sont tolérés mais affichés

### Comment mesurer localement
```bash
flake8 . --config=.flake8 --count --show-source
```

### Erreurs fatales bloquantes

| Code | Description |
|------|-------------|
| E999 | SyntaxError |
| F63 | Comparaison incorrecte (True/False/None) |
| F7 | Erreur de syntaxe (indentation, etc.) |
| F82 | Import non défini |
| E901 | SyntaxError / IndentationError |

### Avertissements non bloquants
- `E501`: Ligne trop longue (géré par `max-line-length`)
- `W503`: Saut de ligne avant opérateur binaire (conflit Black)
- `E203`: Espace avant `:` (conflit Black)

---

## Résumé des Portes de Qualité

| # | Porte | Seuil | Vérifié par |
|---|-------|-------|-------------|
| 1 | Couverture tests unitaires | >= 80% | pytest-cov |
| 2 | Tests d'intégration | 0 échoué | pytest |
| 3 | Tests BDD | 0 échoué | behave |
| 4 | Sécurité | 0 HIGH | bandit + safety |
| 5 | Performance | Latence < 3s | locust |
| 6 | Linting | 0 erreur | flake8 |

## Franchise vs Échec

- **Franchise (✅)**: Toutes les portes sont respectées → Le code peut être mergé
- **Échec (❌)**: Au moins une porte n'est pas respectée → Le code doit être corrigé

## Évolution des Seuils

Les seuils peuvent être ajustés au fil du projet :

| Phase | Couverture | Performance | Sécurité |
|-------|-----------|-------------|----------|
| Sprint 1 | 70% | < 5000ms | 0 HIGH |
| Sprint 2 | 80% | < 3000ms | 0 HIGH |
| Sprint 3+ | 85% | < 2000ms | 0 HIGH + 0 MEDIUM |

Pour modifier un seuil, éditez le fichier `.github/workflows/tests.yml`
et la variable d'environnement correspondante.
