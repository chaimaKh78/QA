# 📸 Régression Visuelle — Documentation

> **Projet:** NouvelAir — Système de réservation aérienne  
> **Outil:** Playwright + pixelmatch/Pillow  
> **Seuil par défaut:** 0.1% de pixels différents

---

## 1. Principe de la régression visuelle

La régression visuelle consiste à comparer automatiquement des screenshots
des pages web avec des images de référence (baselines). Si la différence
dépasse un seuil prédéfini, le test échoue, signalant un changement visuel
inattendu.

### Cycle de vie

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Page web   │ ──▶ │  Screenshot  │ ──▶ │  Comparaison │
│  (Playwright)│     │  (PNG)       │     │  (pixelmatch)│
└─────────────┘     └──────────────┘     └──────┬───────┘
                                               │
                                   ┌───────────▼───────────┐
                                   │   Diff < seuil ?      │
                                   │   ✓ Test passé        │
                                   │   ✗ Test échoué       │
                                   └───────────────────────┘
```

---

## 2. Installation des dépendances

```bash
# Dépendances principales
pip install playwright pytest-playwright Pillow pixelmatch numpy

# Installation du navigateur Chromium pour Playwright
playwright install chromium
```

### Dépendances optionnelles

| Package | Usage | Requis |
|---------|-------|--------|
| `playwright` | Navigation et screenshots | ✅ Oui |
| `pixelmatch` | Comparaison précise pixel-à-pixel | ⚠️ Recommandé |
| `Pillow` | Comparaison fallback par histogramme | ⚠️ Fallback |
| `numpy` | Calcul matriciel pour la comparaison | ⚠️ Fallback |

> **Note:** Si `pixelmatch` n'est pas disponible, le script utilise
> automatiquement `Pillow` + `numpy` comme méthode de comparaison alternative.

---

## 3. Exécution des tests

```bash
# Exécuter tous les tests visuels
pytest tests/e2e/test_visual_regression.py -v

# Exécuter avec le marqueur e2e
pytest -m "e2e and visual" -v

# Mettre à jour toutes les baselines
pytest tests/e2e/test_visual_regression.py --baseline-update -v

# Exécuter un test spécifique
pytest tests/e2e/test_visual_regression.py::TestVisualRegression::test_homepage_visual_regression -v

# Exécuter avec verbose détaillé
pytest tests/e2e/test_visual_regression.py -v --tb=short
```

---

## 4. Création et mise à jour des baselines

### Création initiale

Les baselines sont créées automatiquement lors de la première exécution
des tests. Si un baseline n'existe pas, le test le crée et se met en
`skip` pour vous inviter à relancer.

### Mise à jour manuelle

Lorsqu'un changement visuel est **volontaire** (redesign, nouveau contenu),
il faut mettre à jour les baselines :

```bash
# Option 1: Supprimer les anciens baselines et relancer les tests
rm -rf reports/baselines/*.png
pytest tests/e2e/test_visual_regression.py -v

# Option 2: Copier les screenshots courants comme nouveaux baselines
cp reports/screenshots/*_current.png reports/baselines/
# Renommer les fichiers (enlever "_current")
```

### Quand mettre à jour les baselines ?

- ✅ Après un **redesign** validé de la page
- ✅ Après modification **intentionnelle** du contenu
- ✅ Après mise à jour de la **typographie** ou des couleurs
- ❌ **NE JAMAIS** mettre à jour pour masquer une régression
- ❌ **NE JAMAIS** ignorer un test qui échoue sans investigation

---

## 5. Seuil de tolérance

Le seuil par défaut est de **0.1%** (1 pixel sur 1000). Ce seuil est
suffisamment strict pour détecter les changements visuels significatifs
tout en tolérant les micro-variations inévitables:

### Variations acceptées (sous le seuil)

- Rendu des polices (anti-aliasing légèrement différent)
- Images avec compression légèrement variable
- Animations non terminées au moment du screenshot
- Timestamps ou compteurs dynamiques

### Variations rejetées (au-dessus du seuil)

- Changement de mise en page
- Élément manquant ou ajouté
- Couleur de fond modifiée
- Taille de police changée
- Image remplacée

### Personnalisation du seuil

```python
# Dans le test, modifier le seuil :
diff_percentage = compare_screenshots(baseline_path, current_path, threshold=0.5)
assert diff_percentage < 0.5  # Seuil plus permissif (0.5%)
```

---

## 6. Structure des répertoires

```
reports/
├── baselines/           # Images de référence (versionnées dans git)
│   ├── homepage.png
│   ├── search_page.png
│   ├── login_page.png
│   ├── destination_page.png
│   ├── my_bookings_page.png
│   ├── mobile_homepage.png
│   └── tablet_homepage.png
├── screenshots/         # Screenshots capturés lors des tests
│   ├── homepage_current.png
│   ├── search_page_current.png
│   └── ...
├── diffs/               # Images de différence (baselines - actuels)
│   ├── homepage_current_diff.png
│   ├── search_page_current_diff.png
│   └── ...
└── accessibility/       # Rapports d'accessibilité (HTML + JSON)
    ├── a11y_page_d_accueil.html
    ├── a11y_page_d_accueil.json
    └── ...
```

### Recommandation Git

```gitignore
# Ignorer les screenshots courants et diffs (générés à chaque run)
reports/screenshots/
reports/diffs/

# VERSIONNER les baselines (ils sont la référence)
!reports/baselines/
!reports/baselines/*.png
```

---

## 7. Pages couvertes

| Page | URL | Viewport | Fichier baseline |
|------|-----|----------|-----------------|
| Accueil | `/` | Desktop (1280×720) | `homepage.png` |
| Accueil mobile | `/` | Mobile (375×667) | `mobile_homepage.png` |
| Accueil tablette | `/` | Tablette (768×1024) | `tablet_homepage.png` |
| Recherche | `/recherche/` | Desktop | `search_page.png` |
| Connexion | `/compte/connexion/` | Desktop | `login_page.png` |
| Destinations | `/destinations/` | Desktop | `destination_page.png` |
| Réservations | `/reservations/mes-reservations/` | Desktop | `my_bookings_page.png` |

---

## 8. Dépannage

### Playwright non installé

```
ERROR: Module 'playwright' not found
```

```bash
pip install playwright pytest-playwright
playwright install chromium
```

### Baseline manquant

```
AssertionError: Le baseline n'a pas été sauvegardé
```

→ Le test crée le baseline automatiquement. Relancez une seconde fois.

### Régression visuelle inattendue

```
AssertionError: Régression visuelle détectée: 0.2534%
```

1. Ouvrez le fichier diff dans `reports/diffs/`
2. Vérifiez si le changement est intentionnel
3. Si oui, mettez à jour le baseline (voir section 4)
4. Si non, identifiez et corrigez le bug CSS/HTML

---

*Documentation générée pour le projet NouvelAir — Jour 7 de la formation Django.*
