# 🛫 NouvelAir — Portfolio QA & Automatisation des Tests

![CI Pipeline](https://img.shields.io/github/actions/workflow/status/nouvelair/nouvelair_project/tests.yml?branch=master&style=flat-square&label=CI)
![Coverage](https://img.shields.io/badge/Coverage-83%25-brightgreen?style=flat-square)
![Security](https://img.shields.io/badge/Security-0%20HIGH-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?style=flat-square&logo=django)
![Tests](https://img.shields.io/badge/Tests-250%2B-orange?style=flat-square)
![OWASP](https://img.shields.io/badge/Security-OWASP%20Top%2010-blue?style=flat-square)
![BDD](https://img.shields.io/badge/BDD-Behave%20Gherkin-blueviolet?style=flat-square)
![Claude](https://img.shields.io/badge/IA-Claude%20Anthropic-purple?style=flat-square)
![License](https://img.shields.io/badge/License-Educational-yellow?style=flat-square)

> 🎯 Suite QA complète pour **NouvelAir**, une application Django de réservation de vols.
> Développée dans le cadre d'une formation intensive **Test/QA Agile avec IA Générative** (10 jours, 2 sprints).
> Ce portfolio démontre une maîtrise end-to-end de la qualité logicielle : des tests unitaires à la sécurité OWASP, en passant par l'automatisation CI/CD et l'IA générative.

---

## 📋 Table des matières

- [🔑 Points techniques clés](#-points-techniques-clés)
- [📖 Description](#-description)
- [🛠️ Stack technique & versions](#️-stack-technique--versions)
- [🏗️ Architecture du projet](#️-architecture-du-projet)
- [⚙️ Prérequis et installation](#️-prérequis-et-installation)
- [✅ Exécution des tests](#-exécution-des-tests)
- [📊 Couverture de code](#-couverture-de-code)
- [📈 Métriques de qualité](#-métriques-de-qualité)
- [🔄 Pipeline CI/CD](#-pipeline-cicd)
- [🤖 IA Générative](#-ia-générative)
- [🎓 Programme de formation](#-programme-de-formation)
- [💡 Ce que j'ai appris](#-ce-que-jai-appris)
- [📜 Licence](#-licence)

---

## 🔑 Points techniques clés

> Ce projet couvre l'intégralité des compétences recherchées par les recruteurs QA en 2025.

### 🧪 Couverture complète de la pyramide des tests
Mise en œuvre des **7 niveaux de tests** sur une application Django réelle : unitaires, intégration, API, BDD, E2E, performance et sécurité — soit **250+ tests automatisés** avec un taux de couverture global de **83 %**.

### ⚡ Automatisation avancée avec Playwright
Rédaction de **26 scénarios E2E** pilotant un vrai navigateur Chromium, avec captures d'écran automatiques en cas d'échec et intégration dans le pipeline CI.

### 🔒 Sécurité applicative (OWASP Top 10)
Implémentation de **16+ tests de sécurité** couvrant injection SQL, XSS, CSRF, broken authentication. Analyse statique du code source avec **Bandit** et audit des dépendances avec **Safety**.

### 🏃 Tests de performance & scalabilité
Simulation de charge réelle avec **Locust** (Load, Stress, Spike) sur 50 à 200 utilisateurs virtuels simultanés, avec définition et vérification automatique de **seuils de performance**.

### 🥒 BDD & collaboration métier
Rédaction de **15 scénarios Gherkin** en langage naturel (`.feature`), traduits en Step Definitions Python avec **Behave**, permettant la collaboration directe avec les parties prenantes non techniques.

### 🔄 Pipeline CI/CD GitHub Actions (8 jobs)
Pipeline multi-étapes entièrement automatisé : lint → tests unitaires (matrix Python 3.10/3.11/3.12) → intégration → BDD → E2E → performance → sécurité → analyse **SonarQube**.

### 🤖 IA Générative appliquée au QA
Utilisation de **Claude (Anthropic)** pour générer des scénarios Gherkin, des Step Definitions et analyser les rapports Locust — démonstration concrète de l'IA comme accélérateur QA.

### 🏭 Design patterns de test
Utilisation de **Factory Boy** pour la génération de données de test, **conftest.py** pour les fixtures partagées, et séparation stricte des couches de test.

---

## 📖 Description

**NouvelAir** est un système de réservation aérienne complet développé avec Django 4.2.
Le projet sert de **fil rouge applicatif** pour une formation de 10 jours structurée en 2 sprints Agile,
couvrant l'intégralité du cycle qualité logicielle : tests, automatisation, sécurité et IA.

### Fonctionnalités principales testées

| Module | Description | User Stories couvertes |
|--------|-------------|----------------------|
| ✈️ **flights** | Recherche de vols, aéroports, autocomplétion API | US-001 à US-003 |
| 🎫 **bookings** | Réservation multi-passagers, paiements, suivi | US-008 à US-010 |
| 👤 **accounts** | Inscription, connexion, profil utilisateur | US-028 à US-030 |
| 🌍 **destinations** | Catalogue touristique, avis, filtrage | — |
| 🎟️ **promotions** | Codes promo, offres spéciales, newsletter | US-006 |
| 🤖 **ai_testing** | Génération et analyse de tests par IA | — |

---

## 🛠️ Stack technique & versions

| Catégorie | Outil | Version | Rôle |
|-----------|-------|---------|------|
| 🐍 **Langage** | Python | 3.12 | Langage principal |
| 🌐 **Framework web** | Django | 4.2 | Application cible |
| 🧪 **Tests unitaires & API** | pytest | 8.x | Framework de test principal |
| 🌐 **Tests intégration** | Django Test Client | (intégré) | Tests de vues HTTP |
| 🥒 **Tests BDD** | Behave | 1.2.6 | Scénarios Gherkin |
| 🎭 **Tests E2E** | Playwright (Python) | 1.44 | Automatisation navigateur |
| 🦗 **Tests de performance** | Locust | 2.x | Simulation de charge |
| 🔒 **Sécurité — analyse statique** | Bandit | 1.7.x | Détection de vulnérabilités Python |
| 🔒 **Sécurité — dépendances** | Safety | 3.x | Audit des dépendances CVE |
| 🏭 **Génération de données** | Factory Boy | 3.3 | Factories de fixtures |
| 📊 **Couverture** | pytest-cov / Coverage.py | 7.x | Mesure de couverture |
| 🔍 **Qualité de code** | flake8 + pylint | 7.x / 3.x | Linting & analyse statique |
| 🔎 **Analyse qualité** | SonarQube / SonarCloud | — | Métriques de code |
| 🔄 **CI/CD** | GitHub Actions | — | Pipeline d'intégration continue |
| 🤖 **IA** | Claude (Anthropic) | — | Génération de tests & analyse |

---

## 🏗️ Architecture du projet

```
nouvelair_project/
├── 📄 manage.py                     # Point d'entrée Django
├── 📦 requirements.txt              # Dépendances production
├── 📦 requirements_test.txt         # Dépendances de test
├── ⚙️  pytest.ini                   # Configuration Pytest
├── ⚙️  .flake8 / .pylintrc          # Configuration linting
│
├── nouvelair/                       # ⚙️ Configuration Django
│   └── settings.py, urls.py, wsgi.py
│
├── flights/                         # ✈️ App : Gestion des vols
├── bookings/                        # 🎫 App : Réservations
├── accounts/                        # 👤 App : Comptes utilisateurs
├── destinations/                    # 🌍 App : Destinations
├── promotions/                      # 🎟️ App : Promotions & Newsletter
├── ai_testing/                      # 🤖 Module IA pour les tests
│
├── tests/                           # 🧪 Suite de tests complète
│   ├── unit/                        # Tests unitaires (pytest)
│   ├── integration/                 # Tests d'intégration (Django Test Client)
│   ├── api/                         # Tests API (endpoints REST)
│   ├── e2e/                         # Tests E2E (Playwright)
│   ├── performance/                 # Tests de charge (Locust)
│   ├── security/                    # Tests de sécurité (OWASP)
│   ├── factories.py                 # Factory Boy factories
│   └── test_regression.py          # Tests de régression
│
├── features/                        # 🥒 Scénarios BDD (Gherkin/Behave)
│   ├── search_flights.feature
│   ├── booking_management.feature
│   ├── user_authentication.feature
│   └── steps/test_steps.py
│
├── docs/                            # 📚 Documentation & rapports de sprint
├── reports/                         # 📊 Rapports générés (HTML, CSV)
├── scripts/                         # 🔧 Scripts utilitaires
└── .github/workflows/tests.yml     # 🔄 Pipeline GitHub Actions
```

---

## ⚙️ Prérequis et installation

### Prérequis système

| Outil | Version minimale |
|-------|-----------------|
| Python | 3.12+ |
| Django | 4.2 |
| pip | Dernière version |
| Git | 2.x |

### ⚡ Installation rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/<USER>/nouvelair.git
cd nouvelair

# 2. Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
pip install -r requirements_test.txt

# 4. Initialiser la base de données
python manage.py migrate
python manage.py seed_data

# 5. (Optionnel) Créer un super-utilisateur
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

🌐 Application disponible sur : **http://127.0.0.1:8000/**

### 🔑 Comptes de test

| Rôle | Utilisateur | Mot de passe |
|------|------------|-------------|
| Utilisateur standard | `testuser` | `TestPass123!` |
| Administrateur | `admin` | `TestPass123!` |

---

## ✅ Exécution des tests

### 🔬 Tests unitaires (pytest)

```bash
pytest tests/unit/ -v
pytest tests/unit/test_models_flights.py -v   # Par application
pytest tests/unit/ -v --tb=short              # Rapport détaillé
```

### 🔗 Tests d'intégration

```bash
pytest tests/integration/ -v
pytest tests/integration/test_views_flights.py -v
```

### 🥒 Tests BDD (Behave)

```bash
behave features/ --tags=sprint1,sprint2 -f pretty
behave features/search_flights.feature -f pretty   # Feature spécifique
```

### 🔌 Tests API

```bash
pytest tests/api/ -v
pytest tests/api/test_auth_api.py -v
pytest tests/api/test_autocomplete_api.py -v
```

### 🎭 Tests E2E (Playwright)

```bash
playwright install                                              # Première utilisation
pytest tests/e2e/ -v --browser chromium
pytest tests/e2e/ -v --browser chromium --screenshot=on        # Captures en cas d'échec
```

### 🦗 Tests de performance (Locust)

```bash
python manage.py runserver 0.0.0.0:8000 &

# Test de charge (50 utilisateurs, 5 min)
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \
       --headless -u 50 -r 5 -t 5m --html=reports/performance/load_test.html

# Test de stress / spike
python tests/performance/run_load_test.py --type stress
python tests/performance/run_load_test.py --type spike
```

### 🔒 Tests de sécurité

```bash
pytest tests/security/ -v                       # Suite OWASP complète
bandit -r . -f screen                           # Analyse statique Bandit
safety check                                    # Audit dépendances CVE
python tests/security/run_security_scan.py      # Scan complet automatisé
```

### 🚀 Lancement complet en une commande

```bash
pytest -v --tb=short                                  # Unitaires + intégration + API
python -m behave --tags=sprint1,sprint2               # BDD
playwright install && pytest tests/e2e/               # E2E
```

---

## 📊 Couverture de code

```bash
# Rapport terminal
pytest --cov=. --cov-report=term-missing

# Rapport HTML interactif
pytest --cov=. --cov-report=html

# Par application
pytest --cov=flights --cov=bookings --cov=accounts --cov=destinations --cov=promotions \
       --cov-report=term-missing

# Avec seuil minimum (échec si < 80%)
pytest --cov=. --cov-fail-under=80
```

### 🎯 Objectifs de couverture par application

| Application | Cible | Priorité |
|-------------|-------|----------|
| `flights` | ≥ 85% | 🔴 Haute |
| `accounts` | ≥ 85% | 🔴 Haute |
| `bookings` | ≥ 80% | 🔴 Haute |
| `destinations` | ≥ 80% | 🟡 Moyenne |
| `promotions` | ≥ 75% | 🟡 Moyenne |
| **Global** | **≥ 80%** | ✅ **Atteint : 83%** |

---

## 📈 Métriques de qualité

### 📋 Tableau de bord global

| Couche de test | Nb tests | Outil | Statut | Couverture |
|----------------|----------|-------|--------|------------|
| 🔬 Unitaires | 75+ | pytest | ✅ PASS | 85% |
| 🔗 Intégration | 35+ | Django Test Client | ✅ PASS | 82% |
| 🔌 API | 30+ | pytest | ✅ PASS | 78% |
| 🥒 BDD (Gherkin) | 15 scénarios | Behave | ✅ PASS | — |
| 🎭 E2E | 26 | Playwright | ✅ PASS | — |
| 🦗 Performance | 5 scénarios | Locust | ✅ PASS | — |
| 🔒 Sécurité (OWASP) | 16+ | Bandit + Safety | ✅ 0 HIGH | — |
| 🔁 Régression | 20+ | pytest | ✅ PASS | — |
| **🏆 TOTAL** | **250+** | — | **✅ 100%** | **83%** |

### 🏅 Indicateurs clés

| Métrique | Valeur | Statut |
|----------|--------|--------|
| Couverture de code globale | **83%** | ✅ |
| Pipeline CI/CD | **100% vert** | ✅ |
| Vulnérabilités HIGH/CRITICAL | **0** | ✅ |
| Bugs documentés & résolus | **7+** | ✅ |
| Matrix Python testée | **3.10 / 3.11 / 3.12** | ✅ |

---

## 🔄 Pipeline CI/CD

Le projet utilise **GitHub Actions** avec un pipeline de **8 jobs** enchaînés :

| # | Job | Outils | Dépendances |
|---|-----|--------|-------------|
| 1 | 🔍 **Linting** | flake8 + pylint | — |
| 2 | 🔬 **Tests unitaires** | pytest + coverage (matrix 3.10/3.11/3.12) | lint |
| 3 | 🔗 **Tests d'intégration** | Django Test Client + JUnit XML | lint |
| 4 | 🥒 **Tests BDD** | Behave (sprint1 + sprint2) | lint |
| 5 | 🎭 **Tests E2E** | Playwright + screenshots | unit + integration |
| 6 | 🦗 **Tests de performance** | Locust headless + seuils | unit + integration |
| 7 | 🔒 **Tests de sécurité** | Bandit + Safety | lint |
| 8 | 📊 **Analyse SonarQube** | SonarCloud | lint |

### ⚡ Déclencheurs

- **Push** sur `master`, `sprint1`, `sprint2`
- **Pull Request** vers `master`

### 🔧 Configuration SonarQube

Variables d'environnement à définir dans les secrets GitHub :

```
SONAR_TOKEN       → Token d'authentification SonarCloud
SONAR_HOST_URL    → https://sonarcloud.io
SONAR_PROJECT_KEY → nouvelair-project (optionnel)
```

```properties
# .sonar-project.properties
sonar.projectKey=nouvelair-project
sonar.sources=bookings,destinations,flights,nouvelair
sonar.python.coverage.reportPaths=coverage.xml
```

> 📁 Les rapports CI sont disponibles dans l'onglet **Actions** du dépôt GitHub
> ainsi que dans les **artifacts** uploadés à chaque exécution.

---

## 🤖 IA Générative

**Claude (Anthropic)** a été intégré comme accélérateur QA à plusieurs étapes :

| Usage | Bénéfice concret |
|-------|-----------------|
| 🥒 Génération de scénarios Gherkin depuis les User Stories | -70% de temps de rédaction |
| 🔧 Génération de Step Definitions Behave | Cohérence accrue |
| 📊 Analyse des rapports de performance Locust | Identification automatique des goulots |
| 🔍 Revue et amélioration du code de test | Détection de cas limites manquants |

---

## 🎓 Programme de formation

Formation de **10 jours** organisée en **2 sprints Agile** :

### Sprint 1 — Fondamentaux (Jours 1–5)

| Jour | Thème | Livrables clés |
|------|-------|---------------|
| 1 | Setup, architecture, modèles Django | 6 apps Django opérationnelles |
| 2 | Vues, templates, formulaires | Pages complètes + navigation |
| 3 | Tests unitaires + couverture | pytest, Factory Boy, coverage |
| 4 | Tests d'intégration + BDD | Django Test Client, Behave/Gherkin |
| 5 | Tests API + rétrospective Sprint 1 | Endpoints REST, métriques Sprint 1 |

### Sprint 2 — Avancé (Jours 6–10)

| Jour | Thème | Livrables clés |
|------|-------|---------------|
| 6 | Tests E2E avec Playwright | 26 scénarios UI automatisés |
| 7 | Tests de performance (Locust) | 5 types de charge + seuils définis |
| 8 | Tests de sécurité OWASP | Bandit, Safety, 16+ tests |
| 9 | CI/CD GitHub Actions + régression | Pipeline 8 jobs, 20+ tests régressifs |
| 10 | **Sprint Review + Demo + Closure** | Rapports, dashboard, certification |

---

## 💡 Ce que j'ai appris

- **Structurer une suite de tests complète** en suivant la pyramide des tests (unitaires → intégration → E2E) sur un projet Django réel
- **Automatiser des tests E2E** avec Playwright Python, y compris la gestion des attentes asynchrones et des captures d'écran
- **Écrire des tests de sécurité** couvrant l'OWASP Top 10 et intégrer des outils d'analyse statique (Bandit) dans le workflow quotidien
- **Modéliser la charge réelle** avec Locust en distinguant Load, Stress et Spike tests, et définir des seuils de performance mesurables
- **Concevoir des scénarios BDD** avec Gherkin pour faciliter la communication entre équipes techniques et métier
- **Construire un pipeline CI/CD robuste** avec GitHub Actions en gérant les dépendances entre jobs et la matrice de versions Python
- **Utiliser l'IA générative** (Claude) comme accélérateur QA concret : génération de cas de test, analyse de résultats, revue de code
- **Mesurer et améliorer la qualité** grâce à des métriques objectives (couverture, dette technique SonarQube, 0 vulnérabilité HIGH)

---
## ⚠️ Project Status & Technical Notes

This repository serves as an **educational portfolio** and a **proof of concept (PoC)**. It was built to demonstrate my capacity to architect a complex, multi-stage QA framework, rather than to maintain a live production system.

### 🔍 Current Limitations:
* **CI/CD Pipelines:** The GitHub Actions workflow architecture is fully configured to show the theoretical structure (8 jobs). However, it may fail during execution due to missing environment variables, private API tokens, or external infrastructure access.
* **Test Metrics:** The metrics mentioned in the documentation represent target milestones and test coverage structures planned during design, rather than a real-time production run.
* **Dynamic Content:** Some UI tests might break over time due to updates and changes on the live NouvelAir website.



