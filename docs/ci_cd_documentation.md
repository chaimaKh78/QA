# Documentation CI/CD - NouvelAir
# ================================
# Version: 1.0.0
# Date: Jour 9
# Auteur: Équipe QA NouvelAir

## 1. Architecture du Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NouvelAir QA Pipeline                           │
│                  (GitHub Actions Workflow)                          │
│                                                                     │
│  Déclencheurs: push (main, sprint1, sprint2) / PR (main)           │
└──────────────┬──────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────┐
│   1. LINT            │ ◄── flake8 + pylint
│   (Statut: gate)     │
└──────┬───────────────┘
       │
       ├──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ 2. UNIT    │ │ 3. INTEG   │ │ 4. BDD     │ │ 7. SECURE  │
│   TESTS    │ │   TESTS    │ │  (behave)  │ │  (bandit)  │
│ (matrix)   │ │            │ │            │ │            │
│ py 3.10    │ │            │ │            │ │            │
│ py 3.11    │ │            │ │            │ │            │
│ py 3.12    │ │            │ │            │ │            │
└──────┬─────┘ └──────┬─────┘ └────────────┘ └────────────┘
       │              │
       ├──────────────┤
       ▼              ▼
┌──────────────────────┐ ┌──────────────────────┐
│ 5. E2E TESTS         │ │ 6. PERFORMANCE       │
│   (Playwright)       │ │   (Locust)           │
│   ◄── Chromium       │ │   ◄── 10 users, 60s  │
│   ◄── Screenshots    │ │   ◄── Latency < 3s   │
└──────────┬───────────┘ └──────────┬───────────┘
           │                        │
           └────────────┬───────────┘
                        ▼
           ┌─────────────────────────┐
           │ 8. PIPELINE STATUS      │
           │   ◄── Résumé global     │
           │   ◄── Badges statut     │
           └─────────────────────────┘
```

## 2. Description des Jobs

### Job 1: Linting
- **Objectif**: Vérifier la qualité du code source
- **Outils**: flake8 (style) + pylint (qualité)
- **Configuration**: `.flake8` + `.pylintrc`
- **Critère de succès**: 0 erreur fatale (E9, F63, F7, F82)
- **Durée typique**: ~30 secondes

### Job 2: Tests Unitaires
- **Objectif**: Valider le comportement isolé de chaque composant
- **Outils**: pytest + pytest-cov
- **Strategy**: Matrix sur Python 3.10, 3.11, 3.12
- **Critère de succès**: Couverture >= 80%, 0 test échoué
- **Durée typique**: ~1-2 minutes par version Python

### Job 3: Tests d'Intégration
- **Objectif**: Vérifier le bon fonctionnement des modules ensemble
- **Outils**: pytest
- **Critère de succès**: 0 test échoué
- **Durée typique**: ~1-2 minutes

### Job 4: Tests BDD (Behave)
- **Objectif**: Valider les scénarios métier en langage naturel
- **Outils**: behave + behave-django
- **Tags**: sprint1, sprint2
- **Critère de succès**: Tous les scénarios passent
- **Durée typique**: ~1-3 minutes

### Job 5: Tests End-to-End
- **Objectif**: Simuler le parcours utilisateur complet
- **Outils**: pytest-playwright (Chromium)
- **Dépend de**: Tests unitaires + Tests d'intégration
- **Artifacts**: Captures d'écran en cas d'échec
- **Durée typique**: ~2-5 minutes

### Job 6: Tests de Performance
- **Objectif**: Vérifier les performances sous charge légère
- **Outils**: Locust
- **Configuration**: 10 utilisateurs, montée progressive, 60 secondes
- **Critère de succès**: Latence médiane < 3000ms
- **Durée typique**: ~2 minutes

### Job 7: Tests de Sécurité
- **Objectif**: Détecter les vulnérabilités dans le code et les dépendances
- **Outils**: bandit (code) + safety (dépendances)
- **Critère de succès**: 0 vulnérabilité HIGH
- **Durée typique**: ~30 secondes

### Job 8: Statut Global du Pipeline
- **Objectif**: Fournir un résumé consolidé de tous les jobs
- **Exécution**: Toujours (même si des jobs ont échoué)
- **Sortie**: Tableau de bord dans le summary GitHub

## 3. Portes de Qualité (Quality Gates)

Le pipeline impose les portes de qualité suivantes :

| Critère | Seuil | Job |
|---------|-------|-----|
| Erreurs fatales flake8 | 0 | lint |
| Couverture de code | >= 80% | unit-tests |
| Tests unitaires échoués | 0 | unit-tests |
| Tests d'intégration échoués | 0 | integration-tests |
| Scénarios BDD échoués | 0 | bdd-tests |
| Tests E2E échoués | 0 | e2e-tests |
| Vulnérabilités HIGH | 0 | security-tests |
| Latence médiane | < 3000ms | performance-tests |

Si une porte n'est pas respectée, le job échoue et bloque les jobs dépendants.

## 4. Comment Ajouter de Nouveaux Tests

### Ajouter un test unitaire

1. Créer le fichier dans `tests/unit/` :
   ```bash
   # tests/unit/test_nouveau_module.py
   import pytest

   @pytest.mark.unit
   def test_ma_nouvelle_fonctionnalite():
       assert True
   ```

2. Le test sera automatiquement ramassé par le pipeline.

### Ajouter un test d'intégration

1. Créer le fichier dans `tests/integration/` :
   ```bash
   # tests/integration/test_nouveau_module.py
   import pytest

   @pytest.mark.integration
   @pytest.mark.django_db
   def test_mon_integration():
       assert True
   ```

### Ajouter un scénario BDD

1. Créer le fichier feature dans `features/` :
   ```gherkin
   # features/nouvelle_fonctionnalite.feature
   Feature: Nouvelle fonctionnalité

     @sprint2
     Scenario: Test de base
       Given je suis sur la page d'accueil
       When je clique sur le lien
       Then je vois le résultat
   ```

### Ajouter un test de régression

1. Ajouter le test dans `tests/test_regression.py` :
   ```python
   @pytest.mark.regression
   @pytest.mark.django_db
   def test_regression_ma_fonctionnalite():
       # Ce test s'assure que la fonctionnalité reste stable
       assert True
   ```

### Ajouter un test E2E

1. Créer le fichier dans `tests/e2e/` :
   ```python
   # tests/e2e/test_mon_parcours.py
   import pytest

   @pytest.mark.e2e
   def test_parcours_complet(page):
       page.goto("/recherche/")
       assert page.title() != ""
   ```

## 5. Comment Consulter les Rapports

### Depuis GitHub

1. Allez sur l'onglet **Actions** du dépôt
2. Sélectionnez le run le plus récent
3. Cliquez sur un job pour voir les logs
4. Le **Summary** affiche un tableau de bord consolidé

### Télécharger les Artifacts

1. Sur la page du workflow run
2. Scrollez jusqu'à la section **Artifacts**
3. Téléchargez les rapports :
   - `coverage-report-py312`: Rapport de couverture HTML
   - `lint-reports`: Rapports flake8 et pylint
   - `integration-results`: Résultats JUnit XML
   - `bdd-results`: Résultats Behave
   - `e2e-screenshots`: Captures d'écran (si échec)
   - `performance-report`: Rapport Locust HTML
   - `security-reports`: Rapports Bandit et Safety

### Rapport de Couverture Local

```bash
# Ouvrir le rapport HTML de couverture
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## 6. Comment Gérer les Échecs

### Échec de Linting

1. Télécharger l'artifact `lint-reports`
2. Corriger les erreurs identifiées
3. Vérifier localement : `flake8 . --config=.flake8`
4. Pousser la correction

### Échec des Tests Unitaires

1. Vérifier les logs du job dans GitHub Actions
2. Identifier le test qui échoue
3. Reproduire localement :
   ```bash
   pytest tests/unit/ -m unit -v --tb=long
   ```
4. Corriger et pousser

### Échec des Tests d'Intégration

1. Vérifier les logs et le rapport JUnit
2. Télécharger l'artifact `integration-results`
3. Reproduire localement :
   ```bash
   pytest tests/integration/ -m integration -v --tb=long
   ```

### Échec des Tests BDD

1. Vérifier les logs Behave
2. Vérifier que les fixtures et steps sont à jour
3. Exécuter localement :
   ```bash
   behave features/ --tags=sprint1,sprint2 -f pretty
   ```

### Échec des Tests E2E

1. Télécharger les captures d'écran (`e2e-screenshots`)
2. Analyser visuellement la cause de l'échec
3. Vérifier que le sélecteur CSS/ID est toujours valide

### Échec de Performance

1. Télécharger `performance-report.html`
2. Identifier l'endpoint lent
3. Optimiser (requêtes, cache, etc.)

### Échec de Sécurité

1. Télécharger `bandit_results.json` et `safety_screen.txt`
2. Analyser chaque vulnérabilité HIGH
3. Appliquer les corrections recommandées
4. Mettre à jour les dépendances si nécessaire

## 7. Stratégie de Branches

```
main ─────────────────────────────────────────────────────────► (production)
  │
  ├── sprint1 ──── (feature sprint 1)
  │     │
  │     └── feature/login ──── (développement spécifique)
  │
  ├── sprint2 ──── (feature sprint 2)
  │     │
  │     └── feature/booking ──── (développement spécifique)
  │
  └── feature/xxx ──── (création de PR vers main)
```

### Règles de branchement

- **main**: Branche protégée, déploiement automatique
- **sprint1/sprint2**: Branches de développement par sprint
- **feature/***: Branches de fonctionnalités, créées depuis un sprint
- Les PR vers `main` déclenchent le pipeline complet
- Les pushes sur les branches sprint déclenchent aussi le pipeline

### Workflow recommandé

1. Créer une branche `feature/mon-travail` depuis `sprintX`
2. Développer et tester localement avec `python scripts/run_full_suite.py`
3. Commiter et pousser
4. Le pipeline CI/CD s'exécute automatiquement
5. Corriger les éventuels échecs
6. Créer une PR vers `main` quand tout passe
7. Le pipeline s'exécute à nouveau sur la PR
8. Merger après approbation
