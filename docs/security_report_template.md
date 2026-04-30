# Rapport de Sécurité — NouvelAir

## Informations Générales

| Champ | Valeur |
|-------|--------|
| **Projet** | NouvelAir — Compagnie Aérienne |
| **Date du scan** | {{DATE}} |
| **Environnement** | Développement local |
| **Système d'exploitation** | Windows 11 |
| **Python** | 3.x |
| **Django** | 5.x |
| **Exécutant** | {{EXECUTANT}} |

---

## 1. Résumé Exécutif

Ce rapport présente les résultats de l'audit de sécurité de l'application
NouvelAir. L'audit couvre l'analyse statique du code (Bandit), la vérification
des dépendances (Safety), les tests de sécurité manuels et la couverture du
OWASP Top 10 (2021).

### Score de sécurité global

| Catégorie | Score | Statut |
|-----------|-------|--------|
| Analyse statique (Bandit) | {{BANDIT_SCORE}}/100 | {{BANDIT_STATUS}} |
| Dépendances (Safety) | {{SAFETY_SCORE}}/100 | {{SAFETY_STATUS}} |
| Tests manuels | {{MANUAL_SCORE}}/100 | {{MANUAL_STATUS}} |
| OWASP Top 10 | {{OWASP_SCORE}}/100 | {{OWASP_STATUS}} |
| **Score global** | **{{GLOBAL_SCORE}}/100** | **{{GLOBAL_STATUS}}** |

### Conclusions principales

- **Vulnérabilités critiques** : {{CRITICAL_COUNT}}
- **Vulnérabilités hautes** : {{HIGH_COUNT}}
- **Vulnérabilités moyennes** : {{MEDIUM_COUNT}}
- **Vulnérabilités basses** : {{LOW_COUNT}}

---

## 2. Outils et Méthodologie

### 2.1 Outils utilisés

| Outil | Version | Type de scan | Couverture |
|-------|---------|-------------|-----------|
| **Bandit** | {{BANDIT_VERSION}} | Analyse statique Python | Code Python du projet |
| **Safety** | {{SAFETY_VERSION}} | CVE des dépendances | requirements.txt |
| **Django check --deploy** | 5.x | Configuration sécurité | Settings Django |
| **Tests manuels** | Custom | Tests fonctionnels sécurité | Endpoints principaux |
| **OWASP Top 10** | Custom | Tests de vulnérabilités | 6 catégories sur 10 |

### 2.2 Méthodologie

1. **Analyse statique** : Scan complet du code Python avec Bandit
2. **Vérification des dépendances** : Cross-reference avec la base de données CVE de PyPI
3. **Configuration Django** : Vérification des paramètres de sécurité
4. **Tests manuels** : 10 tests de sécurité avec le client de test Django
5. **OWASP Top 10** : 6 tests ciblés sur les vulnérabilités les plus critiques

---

## 3. Résultats Bandit (Analyse Statique)

### 3.1 Résumé

| Sévérité | Nombre | Détails |
|----------|--------|---------|
| 🔴 **Haute** | {{BANDIT_HIGH}} | {{BANDIT_HIGH_DETAILS}} |
| 🟠 **Moyenne** | {{BANDIT_MEDIUM}} | {{BANDIT_MEDIUM_DETAILS}} |
| 🟡 **Basse** | {{BANDIT_LOW}} | {{BANDIT_LOW_DETAILS}} |
| 🔵 **Info** | {{BANDIT_INFO}} | {{BANDIT_INFO_DETAILS}} |
| **Total** | {{BANDIT_TOTAL}} | |

### 3.2 Findings détaillés

{{#each BANDIT_FINDINGS}}
#### [{{ID}}] {{TITLE}} — {{SEVERITY}}

- **Fichier** : `{{FILE}}`
- **Ligne** : {{LINE}}
- **Confiance** : {{CONFIDENCE}}
- **Description** : {{DESCRIPTION}}
- **Rémédiation** : {{REMEDIATION}}

---

{{/each}}

### 3.3 Analyse Bandit

{{BANDIT_ANALYSIS}}

---

## 4. Résultats Safety (Vulnérabilités des Dépendances)

### 4.1 Résumé

| Statut | Nombre |
|--------|--------|
| ✅ Aucune vulnérabilité | {{SAFETY_SAFE}} |
| ⚠ Vulnérabilités trouvées | {{SAFETY_VULN}} |

### 4.2 Détails des vulnérabilités

{{#if SAFETY_HAS_VULNS}}

| Package | Version installée | CVE | Sévérité CVSS | Description |
|---------|------------------|-----|---------------|-------------|
{{#each SAFETY_VULN_LIST}}
| {{PACKAGE}} | {{VERSION}} | {{CVE_ID}} | {{CVSS}} | {{ADVISORY}} |
{{/each}}

{{else}}

✅ **Aucune vulnérabilité connue** dans les dépendances du projet.

{{/if}}

### 4.3 Analyse Safety

{{SAFETY_ANALYSIS}}

---

## 5. Résultats des Tests Manuels

### 5.1 Résumé

| # | Test | Résultat | Détails |
|---|------|----------|---------|
| 1 | CSRF token sur page d'accueil | {{T1_RESULT}} | {{T1_DETAIL}} |
| 2 | POST sans CSRF → 403 | {{T2_RESULT}} | {{T2_DETAIL}} |
| 3 | XSS dans recherche autocomplete | {{T3_RESULT}} | {{T3_DETAIL}} |
| 4 | Injection SQL autocomplete | {{T4_RESULT}} | {{T4_DETAIL}} |
| 5 | URL protégée → redirection | {{T5_RESULT}} | {{T5_DETAIL}} |
| 6 | Rate limiting connexion | {{T6_RESULT}} | {{T6_DETAIL}} |
| 7 | Session expiry | {{T7_RESULT}} | {{T7_DETAIL}} |
| 8 | HTTPS enforcement | {{T8_RESULT}} | {{T8_DETAIL}} |
| 9 | Password pas dans réponse | {{T9_RESULT}} | {{T9_DETAIL}} |
| 10 | DEBUG mode | {{T10_RESULT}} | {{T10_DETAIL}} |

**Score** : {{MANUAL_PASSED}}/10 tests réussis

### 5.2 Analyse des tests manuels

{{MANUAL_ANALYSIS}}

---

## 6. Couverture OWASP Top 10 (2021)

### 6.1 Matrice de couverture

| ID | Catégorie | Testé | Statut | Vulnérabilités trouvées |
|----|-----------|-------|--------|------------------------|
| A01 | Broken Access Control | ✅ Oui | {{A01_STATUS}} | {{A01_COUNT}} |
| A02 | Cryptographic Failures | ✅ Oui | {{A02_STATUS}} | {{A02_COUNT}} |
| A03 | Injection | ✅ Oui | {{A03_STATUS}} | {{A03_COUNT}} |
| A04 | Insecure Design | ✅ Oui | {{A04_STATUS}} | {{A04_COUNT}} |
| A05 | Security Misconfiguration | ✅ Oui | {{A05_STATUS}} | {{A05_COUNT}} |
| A06 | Vulnerable Components | ⚠️ Partiel | {{A06_STATUS}} | {{A06_COUNT}} |
| A07 | XSS | ✅ Oui | {{A07_STATUS}} | {{A07_COUNT}} |
| A08 | Software & Data Integrity | ⚠️ Partiel | {{A08_STATUS}} | {{A08_COUNT}} |
| A09 | Logging & Monitoring | ⚠️ Partiel | {{A09_STATUS}} | {{A09_COUNT}} |
| A10 | SSRF | ❌ Non testé | {{A10_STATUS}} | {{A10_COUNT}} |

### 6.2 Détails des tests OWASP

#### A01 — Broken Access Control
- **Tests** : Accès admin sans permission, sous-pages admin, profil d'un autre utilisateur
- **Résultats** : {{A01_DETAILS}}

#### A02 — Cryptographic Failures
- **Tests** : Hachage des mots de passe, complexité de la clé secrète
- **Résultats** : {{A02_DETAILS}}

#### A03 — Injection
- **Tests** : 10 payloads SQL injection, 7 payloads XSS via autocomplete
- **Résultats** : {{A03_DETAILS}}

#### A04 — Insecure Design
- **Tests** : Fuite de données dans les erreurs, énumération d'utilisateurs
- **Résultats** : {{A04_DETAILS}}

#### A05 — Security Misconfiguration
- **Tests** : DEBUG mode, ALLOWED_HOSTS, headers de sécurité, Debug Toolbar
- **Résultats** : {{A05_DETAILS}}

#### A07 — Cross-Site Scripting
- **Tests** : XSS réfléchi, XSS dans formulaires, XSS dans JSON
- **Résultats** : {{A07_DETAILS}}

---

## 7. Matrice des Risques

| Risque | Probabilité | Impact | Score | Priorité |
|--------|------------|--------|-------|----------|
| {{RISK_1}} | {{R1_PROB}} | {{R1_IMPACT}} | {{R1_SCORE}} | {{R1_PRIORITY}} |
| {{RISK_2}} | {{R2_PROB}} | {{R2_IMPACT}} | {{R2_SCORE}} | {{R2_PRIORITY}} |
| {{RISK_3}} | {{R3_PROB}} | {{R3_IMPACT}} | {{R3_SCORE}} | {{R3_PRIORITY}} |
| {{RISK_4}} | {{R4_PROB}} | {{R4_IMPACT}} | {{R4_SCORE}} | {{R4_PRIORITY}} |
| {{RISK_5}} | {{R5_PROB}} | {{R5_IMPACT}} | {{R5_SCORE}} | {{R5_PRIORITY}} |

### Échelle de risque

| Score | Niveau | Action requise |
|-------|--------|---------------|
| 9-10 | 🔴 Critique | Correction immédiate |
| 7-8 | 🟠 Haut | Correction sous 48h |
| 5-6 | 🟡 Moyen | Correction sous 1 semaine |
| 3-4 | 🔵 Bas | Correction planifiée |
| 1-2 | ⚪ Info | Surveillance |

---

## 8. Scores CVSS

### 8.1 Vulnérabilités avec score CVSS

| Vulnérabilité | CVSS v3.1 | Vecteur | Sévérité |
|--------------|-----------|---------|----------|
| {{CVSS_1_NAME}} | {{CVSS_1_SCORE}} | {{CVSS_1_VECTOR}} | {{CVSS_1_SEVERITY}} |
| {{CVSS_2_NAME}} | {{CVSS_2_SCORE}} | {{CVSS_2_VECTOR}} | {{CVSS_2_SEVERITY}} |
| {{CVSS_3_NAME}} | {{CVSS_3_SCORE}} | {{CVSS_3_VECTOR}} | {{CVSS_3_SEVERITY}} |

### 8.2 Distribution CVSS

```
Critique (9.0-10.0) : ██████████ {{CVSS_CRITICAL}}
Haut (7.0-8.9)      : ████████   {{CVSS_HIGH}}
Moyen (4.0-6.9)     : ██████     {{CVSS_MEDIUM}}
Bas (0.1-3.9)       : ████       {{CVSS_LOW}}
Info (0.0)          : ██         {{CVSS_INFO}}
```

---

## 9. Recommandations

### 9.1 Actions immédiates (Critique / Haut)

#### REC-001: {{REC_1_TITLE}}
- **Priorité** : 🔴 CRITIQUE
- **Catégorie OWASP** : {{REC_1_OWASP}}
- **CVSS** : {{REC_1_CVSS}}
- **Description** : {{REC_1_DESC}}
- **Rémédiation** :
  1. {{REC_1_STEP_1}}
  2. {{REC_1_STEP_2}}
  3. {{REC_1_STEP_3}}
- **Estimation** : {{REC_1_EFFORT}}

#### REC-002: {{REC_2_TITLE}}
- **Priorité** : 🟠 HAUTE
- **Catégorie OWASP** : {{REC_2_OWASP}}
- **CVSS** : {{REC_2_CVSS}}
- **Description** : {{REC_2_DESC}}
- **Rémédiation** :
  1. {{REC_2_STEP_1}}
  2. {{REC_2_STEP_2}}
- **Estimation** : {{REC_2_EFFORT}}

### 9.2 Actions planifiées (Moyen)

#### REC-003: {{REC_3_TITLE}}
- **Priorité** : 🟡 MOYENNE
- **Description** : {{REC_3_DESC}}
- **Rémédiation** : {{REC_3_STEPS}}

### 9.3 Bonnes pratiques recommandées

1. **Rate limiting** : Implémenter django-ratelimit ou django-axes pour la protection brute-force
2. **HTTPS** : Configurer SECURE_SSL_REDIRECT=True en production
3. **Headers CSP** : Définir une politique Content-Security-Policy stricte
4. **Logging** : Activer le logging des événements de sécurité
5. **Dépendances** : Configurer des mises à jour automatiques des dépendances
6. **Tests CI/CD** : Intégrer Bandit et Safety dans le pipeline CI/CD

---

## 10. Conclusion

### 10.1 État de sécurité du projet

{{CONCLUSION}}

### 10.2 Prochaines étapes

1. Corriger les vulnérabilités critiques et hautes identifiées
2. Configurer les paramètres de sécurité pour la production
3. Mettre en place le rate limiting sur les endpoints sensibles
4. Intégrer les outils de sécurité dans le pipeline CI/CD
5. Planifier un audit de sécurité régulier (mensuel)

---

## Annexe A: Commandes de scan

```bash
# Analyse statique avec Bandit
bandit -r . -f html -o reports/security/bandit_report.html        --exclude tests/,migrations/,__pycache__/

# Vérification des dépendances avec Safety
safety check -r requirements.txt --json

# Vérifications Django
python manage.py check --deploy

# Tests de sécurité manuels
python manage.py test tests.security.test_security_manual -v2

# Tests OWASP
python manage.py test tests.security.test_owasp_top10 -v2

# Scan complet
python tests/security/run_security_scan.py
```

## Annexe B: Glossaire

| Terme | Définition |
|-------|-----------|
| **CVSS** | Common Vulnerability Scoring System |
| **CVE** | Common Vulnerabilities and Exposures |
| **CSRF** | Cross-Site Request Forgery |
| **XSS** | Cross-Site Scripting |
| **SQLi** | SQL Injection |
| **OWASP** | Open Web Application Security Project |
| **SLA** | Service Level Agreement |

---

*Rapport généré automatiquement — NouvelAir Sprint 1, Jour 8*
*Date: {{DATE}}*
*Analyste: {{EXECUTANT}}*
