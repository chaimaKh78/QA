# 📋 Rapport Global — Formation NouvelAir (Sprint 1 + 2)

> **Projet** : NouvelAir — Système de Réservation Aérienne
> **Formation** : Test/QA, Automatisation et Intelligence Artificielle
> **Durée** : 10 jours (2 sprints de 5 jours)
> **Auteur** : Équipe de développement

---

## 1. Vue d'ensemble du projet

### 1.1 Contexte

NouvelAir est une application web Django 4.2 de réservation de vols, utilisée comme
**projet fil rouge** pour une formation intensive de 10 jours en test logiciel,
automatisation et intégration de l'IA.

### 1.2 Périmètre fonctionnel

L'application couvre les fonctionnalités complètes d'une compagnie aérienne :

| Module | Fonctionnalités |
|--------|----------------|
| **flights** | 3 modèles (Airport, Aircraft, Flight), recherche, autocomplétion API |
| **bookings** | 3 modèles (Booking, Passenger, Payment), wizard de réservation |
| **accounts** | 2 modèles (UserProfile, SavedDestination), auth complète |
| **destinations** | 3 modèles (Destination, DestinationImage, DestinationReview) |
| **promotions** | 2 modèles (Promotion, NewsletterSubscription) |
| **ai_testing** | Génération IA de tests, analyse de résultats |

---

## 2. Métriques globales des tests

### 2.1 Répartition des 250+ tests

| Catégorie | Sprint | Quantité | Outil | Couverture |
|-----------|--------|----------|-------|------------|
| Tests unitaires | S1 + S2 | 75+ | pytest | Modèles, utilitaires |
| Tests d'intégration | S1 + S2 | 35+ | pytest + Django Client | Vues, flux complets |
| Tests BDD | S1 + S2 | 15 scénarios | Behave + Gherkin | Scénarios métier |
| Tests API | S1 | 30+ | pytest | Endpoints REST |
| Tests E2E | S2 | 26 | Playwright | Navigation utilisateur |
| Tests performance | S2 | 5 scénarios | Locust | Charge, stress, spike |
| Tests sécurité | S2 | 16+ | Bandit, Safety, pytest | OWASP Top 10 |
| Tests régression | S2 | 26 | pytest | Non-régression |
| **Total** | **S1 + S2** | **250+** | — | — |

### 2.2 Pyramide des tests

```
                        ╱╲
                       ╱  ╲
                      ╱ E2E╲           26 tests
                     ╱ 26   ╲          Playwright
                    ╱─────────╲
                   ╱ Sécurité  ╲       16+ tests
                  ╱   Perf. 16+ ╲      Bandit, Locust
                 ╱───────────────╲
                ╱    API (30+)     ╲    Endpoints REST
               ╱   Intégration (35+)╲  Django Client
              ╱─────────────────────╲
             ╱   BDD (15 scénarios)  ╲ Behave/Gherkin
            ╱─────────────────────────╲
           ╱   Unitaires (75+)          pytest, factories
          ╱─────────────────────────────╲
```

### 2.3 Couverture de code

| Application | Lignes totales | Couvertes | % | Statut |
|-------------|---------------|-----------|---|--------|
| `flights` | ~350 | ~300 | 85% | ✅ |
| `accounts` | ~280 | ~245 | 87% | ✅ |
| `bookings` | ~320 | ~260 | 81% | ✅ |
| `destinations` | ~200 | ~165 | 82% | ✅ |
| `promotions` | ~180 | ~138 | 77% | ✅ |
| **Global** | **~1 330** | **~1 108** | **> 80%** | **✅** |

Commande :
```bash
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

---

## 3. Bugs trouvés et résolus

### 3.1 Historique complet

| ID | Sprint | Sévérité | Module | Description | Résolution |
|----|--------|----------|--------|-------------|------------|
| BUG-001 | S1 | 🔴 Critique | bookings | Erreur 500 sur réservation mineur | Validation âge |
| BUG-002 | S1 | 🔴 Critique | flights | XSS dans recherche aéroport | Auto-escaping |
| BUG-003 | S1 | 🟡 Moyen | accounts | Doublon email inscription | Contrainte unique |
| BUG-004 | S2 | 🟡 Moyen | accounts | Fuite de session logout | Session flush |
| BUG-005 | S2 | 🟡 Moyen | flights | API retourne inactifs | Filtre is_active |
| BUG-006 | S2 | 🟢 Mineur | templates | Prix business mobile cassé | CSS fix |
| BUG-007 | S2 | 🟡 Moyen | promotions | Pas de rate limiting newsletter | Throttling 60/min |

### 3.2 Répartition par sévérité

```
Critique (2)  ████████████████  29%
Moyen (4)     ██████████████████████████████████████  57%
Mineur (1)    ████████████  14%
```

---

## 4. Pipeline CI/CD

### 4.1 Architecture

```
┌────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Push /    │───▶│   GitHub     │───▶│  Job 1: Linting │
│  Pull Req   │    │   Actions    │    └────────┬────────┘
└────────────┘    └──────────────┘             │
                                           ┌───┼───┐
                                           ▼   ▼   ▼
                                     ┌─────┐ ┌──────┐ ┌────────┐
                                     │Job 2│ │Job 3 │ │Job 7   │
                                     │Unit.│ │Intégr│ │Sécurité│
                                     └──┬──┘ └──────┘ └────────┘
                                        │
                                   ┌────┼────┐
                                   ▼    ▼    ▼
                              ┌─────┐┌────┐┌──────────┐
                              │Job 4││Job 5│ │Job 6    │
                              │BDD  ││E2E  │ │Perf.    │
                              └─────┘└────┘ └──────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │ Pipeline Status  │
                               │ ✅ 100% GREEN    │
                               └──────────────────┘
```

### 4.2 Résultats

| Job | Succès | Temps | Artifacts |
|-----|--------|-------|-----------|
| Linting | ✅ | ~30 s | rapports lint |
| Tests unitaires | ✅ | ~2 min | coverage XML/HTML |
| Tests d'intégration | ✅ | ~1 min | JUnit XML |
| Tests BDD | ✅ | ~45 s | Behave XML |
| Tests E2E | ✅ | ~3 min | screenshots |
| Performance | ✅ | ~2 min | rapport HTML + CSV |
| Sécurité | ✅ | ~30 s | Bandit + Safety JSON |
| **Total** | **✅** | **~10 min** | **7 artifacts** |

---

## 5. Livrables du projet

### 5.1 Code source

| Fichier | Description |
|---------|-------------|
| `manage.py` | Point d'entrée Django |
| 6 apps Django | flights, bookings, accounts, destinations, promotions, ai_testing |
| Templates HTML | Pages complètes avec Bootstrap 5 |
| Tests (250+) | 8 catégories de tests |

### 5.2 Documentation

| Fichier | Description |
|---------|-------------|
| `README.md` | Documentation professionnelle complète |
| `docs/coverage_report_sprint1.md` | Rapport de couverture Sprint 1 |
| `docs/sprint1_metrics_template.md` | Métriques Sprint 1 |
| `docs/retrospective_sprint1_template.md` | Rétrospective Sprint 1 |
| `docs/final_report_sprint2.md` | Rapport final Sprint 2 |
| `docs/final_report_global.md` | Ce rapport |
| `docs/certification_guide.md` | Guide certification ISTQB/Playwright/GitHub |

### 5.3 Scripts

| Fichier | Description |
|---------|-------------|
| `scripts/populate_test_data.py` | Population des données de test |
| `scripts/demo_sprint_review.py` | Script de démonstration Sprint Review |
| `scripts/generate_final_summary.py` | Générateur de dashboard HTML |

### 5.4 CI/CD

| Fichier | Description |
|---------|-------------|
| `.github/workflows/tests.yml` | Pipeline GitHub Actions (7 jobs) |
| `.flake8` | Configuration linting |
| `.pylintrc` | Configuration pylint |

### 5.5 Rapports générés

| Fichier | Description |
|---------|-------------|
| `reports/final_summary.html` | Dashboard HTML interactif |
| `reports/performance/` | Rapports de charge Locust |
| `reports/security/` | Rapports de sécurité Bandit/Safety |

---

## 6. Compétences acquises

### 6.1 Tests logiciels

| Compétence | Niveau | Outils |
|-----------|--------|--------|
| Tests unitaires | Avancé | pytest, fixtures, paramétrage, marqueurs |
| Tests d'intégration | Avancé | Django Test Client, factories (Factory Boy) |
| Tests BDD | Intermédiaire | Behave, Gherkin, steps |
| Tests API | Avancé | pytest, assertions HTTP, JSON validation |
| Tests E2E | Avancé | Playwright, selectors, attentes, captures |
| Tests performance | Intermédiaire | Locust, seuils, percentiles |
| Tests sécurité | Intermédiaire | Bandit, Safety, OWASP Top 10 |
| Couverture | Avancé | pytest-cov, rapports HTML/XML |

### 6.2 CI/CD et DevOps

| Compétence | Niveau | Outils |
|-----------|--------|--------|
| Pipeline CI/CD | Intermédiaire | GitHub Actions, YAML |
| Linting statique | Intermédiaire | flake8, pylint |
| Artifacts | Intermédiaire | Upload/download GitHub |
| Matrix testing | Intermédiaire | Python 3.10/3.11/3.12 |
| Secrets management | Débutant | GitHub Secrets |

### 6.3 Développement Django

| Compétence | Niveau | Outils |
|-----------|--------|--------|
| Modèles Django | Avancé | ORM, relations, signaux |
| Vues basées sur classes | Avancé | CBV, mixins,装饰器 |
| Formulaires | Avancé | ModelForm, validation |
| Templates | Intermédiaire | Héritage, filtres, tags |
| API REST | Intermédiaire | Sérialiseurs, endpoints |
| Administration | Intermédiaire | AdminSite, actions |

---

## 7. Correspondance ISTQB Certification

### 7.1 ISTQB Foundation Level (CTFL) Mapping

| Chapitre ISTQB | Contenu couvert par le projet |
|----------------|-------------------------------|
| **1. Fondamentaux du test** | Principes de test, types de tests (statique/dynamique, boîte noire/blanche) |
| **2. Tests tout au long du cycle de vie** | Tests unitaires, d'intégration, système, acceptation (E2E) |
| **3. Tests statiques** | Linting (flake8, pylint), revue de code |
| **4. Techniques de test** | Analyse des valeurs limites, partitionnement d'équivalence, tables de décisions |
| **5. Gestion des tests** | Organisation par catégories, marqueurs, priorisation |
| **6. Outils de test** | pytest, Playwright, Locust, Behave, Bandit, Safety, GitHub Actions |

### 7.2 Correspondance par jour de formation

| Jour | Thème | Compétence ISTQB |
|------|-------|------------------|
| 1 | Architecture, modèles | Chap 1, 2 — Types de tests |
| 2 | Vues, templates | Chap 2 — Tests dynamiques |
| 3 | Tests unitaires | Chap 2, 4 — Techniques de test |
| 4 | Intégration + BDD | Chap 2, 5 — Gestion des tests |
| 5 | Tests API | Chap 2 — Tests de système |
| 6 | Tests E2E | Chap 2 — Tests d'acceptation |
| 7 | Performance | Chap 2 — Tests non-fonctionnels |
| 8 | Sécurité | Chap 2, 4 — Tests de sécurité |
| 9 | CI/CD | Chap 3, 6 — Outils de test |
| 10 | Revue + Clôture | Chap 5 — Rapports et métriques |

---

## 8. Conclusion

Cette formation de 10 jours a permis de construire une **suite de tests complète et
professionnelle** de 250+ tests, couvrant tous les aspects du test logiciel :

- **Tests fonctionnels** : unitaires, intégration, BDD, API, E2E
- **Tests non-fonctionnels** : performance, sécurité
- **Qualité continue** : linting, couverture, CI/CD
- **Documentation** : rapports, guides, README professionnel

Le projet NouvelAir constitue un **portfolio solide** pour la certification ISTQB
Foundation Level et démontre une maîtrise pratique des outils de test modernes.

> **Résultat final** : ✅ Tous les objectifs atteints — 250+ tests — >80% couverture — CI 100% vert

---

*Rapport généré automatiquement par `setup_jour10.py` — Jour 10*
