# Rapport de Tests de Performance — NouvelAir

## Informations Générales

| Champ | Valeur |
|-------|--------|
| **Projet** | NouvelAir — Compagnie Aérienne |
| **Date du test** | {{DATE}} |
| **Environnement** | Développement local |
| **Système d'exploitation** | Windows 11 |
| **Python** | 3.x |
| **Django** | 5.x |
| **Serveur** | runserver (development server) |
| **Base de données** | SQLite 3 |
| **Navigateur** | N/A (tests backend Locust) |
| **Outil de test** | Locust {{LOCUST_VERSION}} |

---

## 1. Résumé Exécutif

Ce rapport présente les résultats des tests de performance effectués sur l'application
NouvelAir. Les tests ont été réalisés dans un environnement de développement local pour
établir une **ligne de base (baseline)** des performances et identifier les éventuels
goulots d'étranglement avant la mise en production.

### Conclusions principales

- **Statut global** : {{STATUS_GLOBAL}}
- **Points critiques** : {{POINTS_CRITIQUES}}
- **Recommandation prioritaire** : {{RECOMMANDATION_PRIORITAIRE}}

---

## 2. Méthodologie de Test

### 2.1 Types de tests exécutés

| Type de test | Utilisateurs | Spawn Rate | Durée | Objectif |
|-------------|-------------|-----------|-------|----------|
| **Baseline** | 10 | 2/s | 2 min | Établir la référence |
| **Charge (Load)** | 50 | 5/s | 5 min | Trafic normal |
| **Stress** | 200 | 10/s | 10 min | Identifier les limites |
| **Spike** | 100 | 100/s | 2 min | Pic soudain |
| **Endurance** | 30 | 3/s | 15 min | Stabilité longue durée |

### 2.2 Endpoints testés

| Endpoint | Description | Poids |
|----------|-------------|-------|
| `/` | Page d'accueil | 5 |
| `/destinations/` | Liste des destinations | 3 |
| `/promotions/` | Offres promotionnelles | 3 |
| `/flights/aeroports/` | Liste des aéroports | 2 |
| `/flights/api/airports/autocomplete/?q=TUN` | Autocomplétion | 2 |
| `/reservations/mes-reservations/` | Mes réservations (protégé) | 1 |
| `/reservations/recherche/` | Recherche de réservation | 1 |
| `/compte/connexion/` | Authentification | 1 |

### 2.3 Scénarios utilisateur simulés

1. **Visiteur curieux** : Navigation sur les pages publiques
2. **Voyageur** : Recherche de vols et autocomplétion
3. **Client enregistré** : Consultation de ses réservations
4. **Nouvel utilisateur** : Visite des pages d'inscription

---

## 3. Seuils de Performance (SLA)

| Endpoint | p50 (ms) | p95 (ms) | p99 (ms) | Criticité |
|----------|----------|----------|----------|-----------|
| Accueil | 1000 | 3000 | 5000 | HAUT |
| Recherche vols | 1500 | 5000 | 8000 | MOYEN |
| Autocomplétion | 100 | 500 | 1000 | CRITIQUE |
| Destinations | 800 | 2500 | 4000 | MOYEN |
| Promotions | 900 | 2800 | 4500 | MOYEN |
| Connexion | 500 | 2000 | 3000 | HAUT |
| Mes réservations | 1200 | 3500 | 6000 | MOYEN |
| Liste aéroports | 700 | 2200 | 3500 | BAS |

**Seuils globaux** :
- Taux d'erreur maximum : 1%
- Temps de réponse moyen maximum : 2 secondes
- RPS minimum : 5 requêtes/seconde

---

## 4. Résultats du Test de Charge (Load Test)

### 4.1 Métriques globales

| Métrique | Valeur | Seuil | Statut |
|----------|--------|-------|--------|
| Requêtes totales | {{TOTAL_REQUESTS}} | - | - |
| Requêtes/s (RPS) | {{RPS}} | > 5 | {{RPS_STATUS}} |
| Temps moyen (ms) | {{AVG_TIME}} | < 2000 | {{AVG_STATUS}} |
| Erreurs | {{ERRORS}} | < 1% | {{ERROR_STATUS}} |
| Durée totale | 5 min | - | - |

### 4.2 Résultats par endpoint

| Endpoint | # Requêtes | RPS | p50 (ms) | p95 (ms) | p99 (ms) | Erreur % | Statut |
|----------|-----------|-----|----------|----------|----------|----------|--------|
| `/ [Homepage]` | {{HOME_COUNT}} | {{HOME_RPS}} | {{HOME_P50}} | {{HOME_P95}} | {{HOME_P99}} | {{HOME_ERR}} | {{HOME_STATUS}} |
| `/destinations/` | {{DEST_COUNT}} | {{DEST_RPS}} | {{DEST_P50}} | {{DEST_P95}} | {{DEST_P99}} | {{DEST_ERR}} | {{DEST_STATUS}} |
| `/promotions/` | {{PROMO_COUNT}} | {{PROMO_RPS}} | {{PROMO_P50}} | {{PROMO_P95}} | {{PROMO_P99}} | {{PROMO_ERR}} | {{PROMO_STATUS}} |
| `/flights/aeroports/` | {{AIR_COUNT}} | {{AIR_RPS}} | {{AIR_P50}} | {{AIR_P95}} | {{AIR_P99}} | {{AIR_ERR}} | {{AIR_STATUS}} |
| `/flights/api/...autocomplete/` | {{AC_COUNT}} | {{AC_RPS}} | {{AC_P50}} | {{AC_P95}} | {{AC_P99}} | {{AC_ERR}} | {{AC_STATUS}} |
| `/reservations/mes-reservations/` | {{BK_COUNT}} | {{BK_RPS}} | {{BK_P50}} | {{BK_P95}} | {{BK_P99}} | {{BK_ERR}} | {{BK_STATUS}} |

### 4.3 Analyse

{{LOAD_ANALYSIS}}

---

## 5. Résultats du Test de Stress

### 5.1 Objectif

Identifier le point de rupture du système en augmentant progressivement
la charge jusqu'à 200 utilisateurs simultanés.

### 5.2 Montée en charge

| Phase | Utilisateurs | Durée | RPS | Temps moyen | Erreur % |
|-------|-------------|-------|-----|-------------|----------|
| Phase 1 | 10 → 50 | 1 min | {{S1_RPS}} | {{S1_AVG}} | {{S1_ERR}} |
| Phase 2 | 50 → 100 | 2 min | {{S2_RPS}} | {{S2_AVG}} | {{S2_ERR}} |
| Phase 3 | 100 → 150 | 3 min | {{S3_RPS}} | {{S3_AVG}} | {{S3_ERR}} |
| Phase 4 | 150 → 200 | 4 min | {{S4_RPS}} | {{S4_AVG}} | {{S4_ERR}} |

### 5.3 Point de rupture

{{RUPTURE_POINT}}

### 5.4 Analyse

{{STRESS_ANALYSIS}}

---

## 6. Résultats du Test de Spike

### 6.1 Scénario

Simulation d'un afflux massif et soudain de 100 utilisateurs simultanés,
comme lors d'une promotion flash ou d'un événement médiatique.

### 6.2 Résultats

| Phase | Utilisateurs | Durée | RPS | Erreur % |
|-------|-------------|-------|-----|----------|
| Pic | 100 | 30 s | {{SPIKE_RPS}} | {{SPIKE_ERR}} |
| Stabilisation | 100 | 1m30s | {{STABLE_RPS}} | {{STABLE_ERR}} |
| Déclin | 100 → 0 | 30 s | {{DECLINE_RPS}} | {{DECLINE_ERR}} |

### 6.3 Analyse

{{SPIKE_ANALYSIS}}

---

## 7. Résultats du Test d'Endurance

### 7.1 Objectif

Vérifier la stabilité du système sur une période prolongée (15 minutes)
pour détecter les fuites mémoire et la dégradation progressive.

### 7.2 Évolution des performances

| Intervalle | RPS | Temps moyen | Mémoire estimée |
|-----------|-----|-------------|-----------------|
| 0-3 min | {{E1_RPS}} | {{E1_AVG}} | {{E1_MEM}} |
| 3-6 min | {{E2_RPS}} | {{E2_AVG}} | {{E2_MEM}} |
| 6-9 min | {{E3_RPS}} | {{E3_AVG}} | {{E3_MEM}} |
| 9-12 min | {{E4_RPS}} | {{E4_AVG}} | {{E4_MEM}} |
| 12-15 min | {{E5_RPS}} | {{E5_AVG}} | {{E5_MEM}} |

### 7.3 Dégradation

{{ENDURANCE_DEGRADATION}}

---

## 8. Comparaison avec les Seuils

| Endpoint | Seuil p95 | Mesuré p95 | Δ | Statut |
|----------|-----------|-----------|---|--------|
| Accueil | 3000 ms | {{M_HOME_P95}} | {{D_HOME}} | {{S_HOME}} |
| Autocomplétion | 500 ms | {{M_AC_P95}} | {{D_AC}} | {{S_AC}} |
| Destinations | 2500 ms | {{M_DEST_P95}} | {{D_DEST}} | {{S_DEST}} |
| Promotions | 2800 ms | {{M_PROMO_P95}} | {{D_PROMO}} | {{S_PROMO}} |

**Résumé** : {{THRESHOLD_SUMMARY}}

---

## 9. Recommandations

### 9.1 Actions prioritaires

1. **{{REC_1_TITLE}}**
   - Priorité: CRITIQUE
   - Impact: {{REC_1_IMPACT}}
   - Détail: {{REC_1_DETAIL}}

2. **{{REC_2_TITLE}}**
   - Priorité: HAUTE
   - Impact: {{REC_2_IMPACT}}
   - Détail: {{REC_2_DETAIL}}

### 9.2 Optimisations recommandées

3. **{{REC_3_TITLE}}**
   - Priorité: MOYENNE
   - Impact: {{REC_3_IMPACT}}
   - Détail: {{REC_3_DETAIL}}

4. **{{REC_4_TITLE}}**
   - Priorité: BASSE
   - Impact: {{REC_4_IMPACT}}
   - Détail: {{REC_4_DETAIL}}

### 9.3 Pour la production

- Remplacer `runserver` par Gunicorn + Nginx
- Utiliser PostgreSQL au lieu de SQLite
- Configurer le cache Redis pour les requêtes fréquentes
- Activer la compression Gzip
- Utiliser un CDN pour les assets statiques

---

## 10. Graphiques et Visualisations

### 10.1 Temps de réponse dans le temps

> Le graphique locust montre l'évolution du temps de réponse médian (vert)
> et du 95e percentile (jaune) au cours du test.

![Temps de réponse](reports/performance/load_test_files/locust_response_times_chart.png)

### 10.2 Requêtes par seconde

> Évolution du nombre de requêtes traitées par seconde au fil du test.

![RPS](reports/performance/load_test_files/locust_rps_chart.png)

### 10.3 Distribution des temps de réponse

> Histogramme montrant la distribution des temps de réponse pour chaque endpoint.

![Distribution](reports/performance/load_test_files/locust_response_time_distribution_chart.png)

### 10.4 Utilisateurs actifs

> Nombre d'utilisateurs simulés actifs pendant le test.

![Utilisateurs](reports/performance/load_test_files/locust_users_chart.png)

---

## Annexe A: Commandes utilisées

```bash
# Test de base (baseline)
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \
       --headless -u 10 -r 2 -t 2m \
       --html=reports/performance/baseline_test.html

# Test de charge
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \
       --headless -u 50 -r 5 -t 5m \
       --html=reports/performance/load_test.html

# Test de stress
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \
       --headless -u 200 -r 10 -t 10m \
       --html=reports/performance/stress_test.html

# Test de spike
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \
       --headless -u 100 -r 100 -t 2m \
       --html=reports/performance/spike_test.html

# Test d'endurance
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \
       --headless -u 30 -r 3 -t 15m \
       --html=reports/performance/endurance_test.html
```

---

## Annexe B: Glossaire

| Terme | Définition |
|-------|-----------|
| **RPS** | Requêtes Par Seconde |
| **p50** | 50e percentile (médiane) |
| **p95** | 95e percentile |
| **p99** | 99e percentile |
| **Spawn Rate** | Taux d'apparition des utilisateurs virtuels |
| **Think Time** | Temps de pause entre les requêtes |
| **SLA** | Service Level Agreement (accord de niveau de service) |

---

*Rapport généré automatiquement — NouvelAir Sprint 1, Jour 8*
*Date: {{DATE}}*
