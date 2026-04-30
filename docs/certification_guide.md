# 🎓 Guide de Certification — ISTQB, Playwright & GitHub Actions

> **Projet** : NouvelAir — Système de Réservation Aérienne
> **Formation** : Test/QA, Automatisation et Intelligence Artificielle
> **Date** : Jour 10 — Clôture

---

## Table des matières

1. [ISTQB Foundation Level (CTFL)](#1-istqb-foundation-level-ctfl)
2. [Playwright Certification](#2-playwright-certification)
3. [GitHub Actions Certification](#3-github-actions-certification)
4. [Plan de préparation recommandé](#4-plan-de-préparation-recommandé)

---

## 1. ISTQB Foundation Level (CTFL)

### 1.1 Présentation

L'**ISTQB Certified Tester Foundation Level (CTFL)** est la certification de référence
mondiale pour les testeurs logiciels. Elle valide les connaissances fondamentales du
test logiciel selon le syllabus officiel.

| Détail | Information |
|--------|-------------|
| **Nom officiel** | ISTQB Certified Tester Foundation Level |
| **Syllabus** | v4.0 (2023) |
| **Prérequis** | Aucun |
| **Format** | 40 questions QCM, 60 minutes |
| **Score minimum** | 65% (26/40) |
| **Langues** | Français, Anglais |
| **Coût** | ~250-300 € |
| **Validité** | À vie (pas de renouvellement) |

### 1.2 Correspondance avec le projet NouvelAir

Le tableau suivant montre comment chaque chapitre du syllabus ISTQB CTFL est couvert
par le projet NouvelAir :

#### Chapitre 1 : Fondamentaux du test logiciel

| Thème | Couvert dans le projet |
|-------|----------------------|
| 1.1 Qu'est-ce que le test ? | Jour 1 — Introduction et principes |
| 1.2 Pourquoi le test est-il nécessaire ? | BUG-001 à BUG-007 trouvés et résolus |
| 1.3 Principes généraux du test | 7 principes appliqués tout au long de la formation |
| 1.4 Principes fondamentaux du test | Toutes les catégories de tests implémentées |
| 1.5 Compétences du testeur | Compétences techniques acquises |

**Principes ISTQB appliqués dans le projet :**

| # | Principe | Application |
|---|----------|-------------|
| 1 | Le test montre la présence de défauts | 7+ bugs trouvés et documentés |
| 2 | Les tests exhaustifs sont impossibles | Stratégie de test par priorité |
| 3 | Test précoce (shift-left) | Tests dès le Sprint 1, Jour 3 |
| 4 | Regroupement des défauts | Concentration sur les modules critiques (flights, bookings) |
| 5 | Paradoxe du pesticide | Tests de régression variés |
| 6 | Le test dépend du contexte | Tests adaptés au contexte web Django |
| 7 | L'absence d'erreur est un piège | Tests de l'expérience utilisateur réelle (E2E) |

#### Chapitre 2 : Tests tout au long du cycle de vie logiciel

| Thème | Couvert dans le projet |
|-------|----------------------|
| 2.1 Modèles de développement logiciel | Approche agile (2 sprints) |
| 2.2 Tâches de test dans le cycle | Planification, conception, exécution, rapport |
| 2.3 Bonnes pratiques de test | Revue de code, tests automatisés, CI/CD |
| 2.4 Dynamique de l'agile | Sprint planning, review, rétrospective |

**Niveaux de test implémentés :**

| Niveau | Outil | Tests |
|--------|-------|-------|
| Tests unitaires | pytest | 75+ |
| Tests d'intégration | Django Test Client | 35+ |
| Tests système | Playwright, API tests | 56+ |
| Tests d'acceptation | Behave (BDD) | 15 scénarios |

#### Chapitre 3 : Tests statiques

| Thème | Couvert dans le projet |
|-------|----------------------|
| 3.1 Principes et rôles | Revue de code continue via linting |
| 3.2 Processus de revue | CI/CD Job 1 (flake8 + pylint) |
| 3.3 Revue de code statique automatisée | flake8 (erreurs), pylint (qualité) |

**Outils utilisés :**

| Outil | Configuration | CI |
|-------|--------------|-----|
| flake8 | `.flake8` (max-line-length=120) | ✅ Job 1 |
| pylint | `.pylintrc` (plugin Django) | ✅ Job 1 |
| Bandit | Analyse sécurité | ✅ Job 7 |

#### Chapitre 4 : Techniques de conception de tests

| Thème | Couvert dans le projet |
|-------|----------------------|
| 4.1 Techniques boîte noire | Tests de vues, API, E2E |
| 4.2 Techniques boîte blanche | Couverture de code, branches |
| 4.3 Techniques basées sur l'expérience | Tests exploratoires, régression |

**Techniques appliquées :**

| Technique | Exemple dans le projet |
|-----------|----------------------|
| Partitionnement d'équivalence | Test email valide/invalide (accounts) |
| Analyse des valeurs limites | Test âge passager mineur/majeur (bookings) |
| Table de décisions | Test statut réservation (pending/confirmed/cancelled) |
| Transitions d'état | Test cycle de vie d'une réservation |
| Tests par paire | Test origine/destination (tous les aéroports) |
| Couverture de code | pytest-cov avec seuil 80% |

#### Chapitre 5 : Gestion des tests

| Thème | Couvert dans le projet |
|-------|----------------------|
| 5.1 Organisation des tests | 8 catégories (unit, integration, api, etc.) |
| 5.2 Planification et estimation | Planning Sprint 1 et Sprint 2 |
| 5.3 Suivi et monitoring | Métriques, rapports, CI/CD dashboard |
| 5.4 Signalement des défauts | 7 bugs documentés (BUG-001 à BUG-007) |

**Outils de gestion :**

| Outil | Usage |
|-------|-------|
| pytest marqueurs | @pytest.mark.unit, @pytest.mark.integration |
| JUnit XML | Rapports standardisés pour CI |
| GitHub Issues | Suivi des bugs (template) |
| Rapports Markdown | Documentation des métriques |

#### Chapitre 6 : Outils de test

| Thème | Couvert dans le projet |
|-------|----------------------|
| 6.1 Types d'outils | 10+ outils utilisés |
| 6.2 Intégration des outils | Pipeline CI/CD unifié |
| 6.3 Avantages et risques | Bonnes pratiques documentées |

**Outils maîtrisés :**

| Catégorie | Outil | Niveau |
|-----------|-------|--------|
| Exécution de tests | pytest | ⭐⭐⭐ |
| BDD | Behave | ⭐⭐ |
| E2E | Playwright | ⭐⭐⭐ |
| Performance | Locust | ⭐⭐ |
| Sécurité | Bandit, Safety | ⭐⭐ |
| Couverture | pytest-cov | ⭐⭐⭐ |
| Linting | flake8, pylint | ⭐⭐ |
| CI/CD | GitHub Actions | ⭐⭐ |
| Mock/Factories | Factory Boy | ⭐⭐⭐ |
| Génération de données | AI tools | ⭐⭐ |

### 1.3 Ressources de préparation

| Ressource | Type | Coût |
|-----------|------|------|
| [ISTQB Syllabus CTFL v4.0](https://www.istqb.org/documents) | Officiel | Gratuit |
| [ISTQB Glossary](https://glossary.istqb.org/) | Référence | Gratuit |
| *Foundation of Software Testing* (Dorothy Graham) | Livre | ~40 € |
| [ISTQB Mock Exams](https://www.istqb.org/certifications/path-to-certification) | QCM | Gratuit |
| Udemy : ISTQB CTFL Course | Vidéo | ~15 € |

### 1.4 Exemple de questions type (pratiquées sur le projet)

**Q1 : Quel principe de test est illustré par la découverte de BUG-002 (XSS)
malgré les tests de sécurité existants ?**

a) Le test montre la présence de défauts ✅
b) Les tests exhaustifs sont possibles
c) L'absence d'erreur signifie un logiciel de qualité
d) Le regroupement des défauts

**Q2 : Les tests BDD (Behave) correspondent à quel niveau de test ?**

a) Tests unitaires
b) Tests d'intégration
c) Tests système
d) Tests d'acceptation ✅

---

## 2. Playwright Certification

### 2.1 Présentation

**Playwright** est un framework de test E2E développé par Microsoft. Bien qu'il n'existe
pas de certification officielle, Microsoft propose des badges de compétence et des
parcours de formation reconnus.

| Détail | Information |
|--------|-------------|
| **Éditeur** | Microsoft |
| **Langues** | Python, JavaScript/TypeScript, Java, .NET |
| **Navigateurs** | Chromium, Firefox, WebKit |
| **Documentation** | [playwright.dev](https://playwright.dev/) |
| **Formation** | [Microsoft Learn](https://learn.microsoft.com/) |

### 2.2 Compétences validées par le projet

| Compétence | Niveau | Scénarios dans le projet |
|-----------|--------|------------------------|
| Installation et configuration | ⭐⭐⭐ | Playwright + pytest-playwright |
| Sélecteurs CSS/XPath | ⭐⭐⭐ | Tous les 26 tests E2E |
| Attentes explicites | ⭐⭐⭐ | `expect().to_be_visible()`, `to_have_text()` |
| Captures d'écran | ⭐⭐ | `--screenshot=on` en CI |
| Navigation multi-pages | ⭐⭐⭐ | Flux complets (recherche → réservation → confirmation) |
| Gestion des formulaires | ⭐⭐⭐ | Inscription, connexion, recherche de vol |
| Authentification | ⭐⭐⭐ | Login, logout, session management |
| Assertions | ⭐⭐⭐ | 26 scénarios avec assertions complètes |
| Fixtures | ⭐⭐ | conftest.py, configurations réutilisables |
| Multi-navigateurs | ⭐⭐ | Chromium (CI), possibilité Firefox/WebKit |
| Debugging | ⭐⭐ | Trace viewer, Playwright Inspector |
| Page Objects | ⭐ | Potentiel d'amélioration identifié |

### 2.3 Ressources de préparation

| Ressource | Type | Lien |
|-----------|------|------|
| Playwright Documentation | Officiel | [playwright.dev/python](https://playwright.dev/python/) |
| Playwright Best Practices | Guide | [playwright.dev/python/docs/best-practices](https://playwright.dev/python/docs/best-practices) |
| Microsoft Learn - Testing | Formation | [learn.microsoft.com](https://learn.microsoft.com/) |
| Playwright YouTube Channel | Vidéos | [youtube.com/@MicrosoftPlaywright](https://youtube.com/@MicrosoftPlaywright) |

---

## 3. GitHub Actions Certification

### 3.1 Présentation

GitHub Actions est la plateforme d'intéautomatisation de GitHub. Microsoft propose
le badge **GitHub Actions Certification** validant les compétences de CI/CD.

| Détail | Information |
|--------|-------------|
| **Éditeur** | GitHub (Microsoft) |
| **Certification** | GitHub Actions (Beta) |
| **Format** | Examen en ligne |
| **Coût** | Gratuit (en beta) |
| **Prérequis** | Connaissance de Git, YAML |

### 3.2 Compétences validées par le projet

| Compétence | Niveau | Implémentation dans le projet |
|-----------|--------|-------------------------------|
| Workflow YAML | ⭐⭐⭐ | `.github/workflows/tests.yml` |
| Triggers (push/PR) | ⭐⭐⭐ | branches, pull_request |
| Matrix strategy | ⭐⭐⭐ | Python 3.10, 3.11, 3.12 |
| Jobs et dépendances | ⭐⭐⭐ | 7 jobs avec `needs` |
| Steps et actions réutilisables | ⭐⭐⭐ | checkout, setup-python, upload-artifact |
| Variables d'environnement | ⭐⭐ | `env:` global |
| Secrets | ⭐ | Potentiel identifié |
| Artifacts | ⭐⭐⭐ | 7 types d'artifacts |
| Step Summary ($GITHUB_STEP_SUMMARY) | ⭐⭐⭐ | Tableaux Markdown dans chaque job |
| Conditions (if: always()) | ⭐⭐ | Upload toujours, status final |
| Runners (ubuntu-latest) | ⭐⭐ | Configuration des exécuteurs |
| Cache (pip cache) | ⭐⭐ | Optimisation des temps de build |

### 3.3 Pipeline CI/CD — Structure

```yaml
# Structure du workflow (7 jobs)
name: NouvelAir QA Pipeline
on:
  push: [main, sprint1, sprint2]
  pull_request: [main]

jobs:
  lint → unit-tests (matrix) → e2e-tests
       → integration-tests  → e2e-tests
       → bdd-tests
       → security-tests
       → performance-tests (avec serveur Django)
  pipeline-status (final)
```

### 3.4 Ressources de préparation

| Ressource | Type | Lien |
|-----------|------|------|
| GitHub Actions Documentation | Officiel | [docs.github.com/actions](https://docs.github.com/actions) |
| GitHub Skills - CI/CD | Interactive | [skills.github.com](https://skills.github.com/) |
| GitHub Actions Certification Study Guide | Guide | [GitHub Training](https://training.github.com/) |
| Awesome GitHub Actions | Communauté | [github.com/sdras/awesome-actions](https://github.com/sdras/awesome-actions) |

---

## 4. Plan de préparation recommandé

### 4.1 Semaine 1 : ISTQB CTFL

| Jour | Activité | Durée |
|------|----------|-------|
| Lundi | Chapitre 1 + 2 (Fondamentaux + Cycle de vie) | 3 h |
| Mardi | Chapitre 3 (Tests statiques) | 2 h |
| Mercredi | Chapitre 4 (Techniques de test) | 3 h |
| Jeudi | Chapitre 5 + 6 (Gestion + Outils) | 2 h |
| Vendredi | Examen blanc + révision | 3 h |

### 4.2 Semaine 2 : Playwright + GitHub Actions

| Jour | Activité | Durée |
|------|----------|-------|
| Lundi | Playwright : selectors, assertions | 3 h |
| Mardi | Playwright : page objects, debugging | 2 h |
| Mercredi | GitHub Actions : workflows, triggers | 3 h |
| Jeudi | GitHub Actions : matrix, artifacts | 2 h |
| Vendredi | Exercices pratiques + révision | 3 h |

### 4.3 Planning complet (2 semaines)

```
Semaine 1 : ISTQB CTFL                           Semaine 2 : Outils
─────────────────────────                        ─────────────────────
Lun : Ch. 1-2 Fondamentaux                       Lun : Playwright avancé
Mar : Ch. 3 Tests statiques                      Mar : Page Objects + Debug
Mer : Ch. 4 Techniques de test                   Mer : GitHub Actions YAML
Jeu : Ch. 5-6 Gestion + Outils                   Jeu : Matrix + Artifacts
Ven : Examen blanc ISTQB                         Ven : Projet pratique
     ────────────────                            ─────────────────
     📝 Objectif : 26/40 QCM                     🎯 Objectif : Pipeline complet
```

### 4.4 Budget estimé

| Certification | Coût | Date recommandée |
|--------------|------|-----------------|
| ISTQB CTFL v4.0 | ~250 € | Semaine 3 |
| Playwright (formation) | Gratuit | Continue |
| GitHub Actions (beta) | Gratuit | Semaine 3 |
| **Total** | **~250 €** | — |

---

## Conclusion

Le projet NouvelAir fournit une base solide et pratique pour la préparation aux
certifications ISTQB, Playwright et GitHub Actions. Les 250+ tests implémentés,
le pipeline CI/CD à 7 jobs et les 7+ bugs documentés constituent un portfolio
démontrant des compétences réelles et vérifiables.

> **Prochaines étapes** :
> 1. Réviser le syllabus ISTQB CTFL v4.0 avec les exemples du projet
> 2. Approfondir les compétences Playwright (Page Objects)
> 3. Pratiquer GitHub Actions avec des workflows avancés
> 4. Passer les certifications (ISTQB en priorité)

---

*Document généré automatiquement par `setup_jour10.py` — Jour 10*
