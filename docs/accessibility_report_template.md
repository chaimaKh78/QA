# 📋 Rapport d'Accessibilité — NouvelAir

> **Projet:** NouvelAir — Système de réservation aérienne  
> **Date:** [DATE_DE_GENERATION]  
> **Standard:** WCAG 2.1 Niveau AA  
> **Outil:** axe-core + axe-playwright-python  
> **Version:** [VERSION]

---

## 1. Résumé des résultats

| Métrique | Valeur |
|----------|--------|
| Pages analysées | [NOMBRE] |
| Violations totales | [NOMBRE] |
| 🔴 Critiques | [NOMBRE] |
| 🟠 Sérieuses | [NOMBRE] |
| 🟡 Modérées | [NOMBRE] |
| 🔵 Mineures | [NOMBRE] |
| Tests réussis | [NOMBRE] |
| Taux de conformité | [POURCENTAGE]% |

### Statut global

- [ ] ✅ **CONFORME** — Aucune violation critique ni sérieuse
- [ ] ⚠️ **PARTIELLEMENT CONFORME** — Violations modérées à corriger
- [ ] ❌ **NON CONFORME** — Violations critiques ou sérieuses détectées

---

## 2. Détail des violations par sévérité

### 🔴 Violations critiques

> Empêchent totalement l'utilisation du site pour certains utilisateurs.

| ID | Description | Pages affectées | Éléments |
|----|-------------|-----------------|----------|
| [VIOLATION_ID] | [DESCRIPTION] | [PAGES] | [NOMBRE] éléments |

### 🟠 Violations sérieuses

> Gênent significativement l'utilisation du site.

| ID | Description | Pages affectées | Éléments |
|----|-------------|-----------------|----------|
| [VIOLATION_ID] | [DESCRIPTION] | [PAGES] | [NOMBRE] éléments |

### 🟡 Violations modérées

> Gênent partiellement l'utilisation du site.

| ID | Description | Pages affectées | Éléments |
|----|-------------|-----------------|----------|
| [VIOLATION_ID] | [DESCRIPTION] | [PAGES] | [NOMBRE] éléments |

### 🔵 Violations mineures

> Problèmes cosmétiques d'accessibilité.

| ID | Description | Pages affectées | Éléments |
|----|-------------|-----------------|----------|
| [VIOLATION_ID] | [DESCRIPTION] | [PAGES] | [NOMBRE] éléments |

---

## 3. Résultats par page

### Page d'accueil (`/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_page_d_accueil.html`

### Page de connexion (`/compte/connexion/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_connexion.html`

### Page d'inscription (`/compte/inscription/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_inscription.html`

### Page de recherche (`/recherche/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_recherche.html`

### Page des destinations (`/destinations/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_destinations.html`

### Page « Mes réservations » (`/reservations/mes-reservations/`)

- **Statut:** [✅ CONFORME / ⚠️ PARTIELLEMENT CONFORME / ❌ NON CONFORME]
- **Violations:** [NOMBRE]
- **Rapport détaillé:** `reports/accessibility/a11y_mes_reservations.html`

---

## 4. Recommandations

### 🔴 Priorité haute — Critiques et sérieuses

1. **[RECOMMANDATION_1]**
   - Violation: [VIOLATION_ID]
   - Action: [DESCRIPTION_DE_LA_CORRECTION]
   - Impact utilisateur: [EXPLICATION]

2. **[RECOMMANDATION_2]**
   - Violation: [VIOLATION_ID]
   - Action: [DESCRIPTION_DE_LA_CORRECTION]
   - Impact utilisateur: [EXPLICATION]

### 🟡 Priorité moyenne — Modérées

1. **[RECOMMANDATION_3]**
   - Violation: [VIOLATION_ID]
   - Action: [DESCRIPTION_DE_LA_CORRECTION]

### 🔵 Priorité basse — Mineures

1. **[RECOMMANDATION_4]**
   - Violation: [VIOLATION_ID]
   - Action: [DESCRIPTION_DE_LA_CORRECTION]

---

## 5. Bonnes pratiques identifiées

- [ ] Utilisation de balises sémantiques HTML5 (`<nav>`, `<main>`, `<footer>`)
- [ ] Labels associés aux champs de formulaire
- [ ] Alt text sur les images
- [ ] Contraste de couleurs suffisant
- [ ] Navigation au clavier fonctionnelle
- [ ] Focus visible sur les éléments interactifs
- [ ] ARIA labels sur les éléments dynamiques
- [ ] Skip navigation link

---

## 6. Historique des audits

| Date | Version | Violations critiques | Violations totales | Taux de conformité |
|------|---------|---------------------|--------------------|--------------------|
| [DATE] | [VERSION] | [NOMBRE] | [NOMBRE] | [POURCENTAGE]% |

---

## 7. Ressources

- [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/)
- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Pa11y — Accessible Web Testing](https://pa11y.org/)

---

*Ce rapport a été généré automatiquement par les tests E2E NouvelAir (Jour 7).*
