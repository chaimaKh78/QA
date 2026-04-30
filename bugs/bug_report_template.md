# 🐛 Template de Rapport de Bug

## NouvelAir — Suivi des Anomalies

---

## Informations Générales

| Champ | Valeur |
|---|---|
| **Titre du bug** | `[À REMPLIR] — Description courte du problème` |
| **ID du bug** | `BUG-XXX` (ex: BUG-008) |
| **Date de signalement** | JJ/MM/AAAA |
| **Rapporté par** | `[Nom de l'auteur]` |

---

## Sévérité et Priorité

| Champ | Valeur |
|---|---|
| **Sévérité** | `Critical` / `High` / `Medium` / `Low` |
| **Priorité** | `Haute` / `Moyenne` / `Basse` |

### Échelle de sévérité

| Niveau | Définition | Exemple |
|---|---|---|
| **Critical** | L'application est indisponible ou la perte de données est possible | Crash du serveur, perte de réservation |
| **High** | Une fonctionnalité majeure est cassée | Impossible de réserver un vol |
| **Medium** | Une fonctionnalité est partiellement cassée | Affichage incorrect d'un prix |
| **Low** | Problème cosmétique ou mineur | Typo, alignement CSS |

---

## Composant Affecté

| Champ | Valeur |
|---|---|
| **Application Django** | `flights` / `bookings` / `accounts` / `destinations` / `promotions` |
| **Module/Fichier** | `[ex: flights/views.py, ligne 42]` |
| **Fonctionnalité** | `[ex: Recherche de vols]` |

---

## Environnement

| Paramètre | Valeur |
|---|---|
| **OS** | Windows 11 / Ubuntu 22.04 / macOS Sonoma |
| **Navigateur** | Chrome 120+ / Firefox 121+ / Edge 120+ |
| **Python** | 3.12.x |
| **Django** | 4.2.x |
| **Base de données** | SQLite 3.x |
| **URL de reproduction** | `[ex: /flights/search/]` |
| **Environnement** | `Développement` / `Staging` / `Production` |

---

## Description du Bug

### Résumé
> Décrivez brièvement le problème constaté en 2-3 phrases.

`[À REMPLIR : Description claire et concise du bug]`

### Comportement Attendu
> Ce qui aurait dû se passer.

`[À REMPLIR : Description du comportement correct attendu]`

### Comportement Observé
> Ce qui se passe réellement.

`[À REMPLIR : Description précise du comportement anormal]`

---

## Étapes de Reproduction

> Listez les étapes pour reproduire le bug de manière fiable.

1. Ouvrir le navigateur et accéder à `[URL]`
2. Remplir le champ `[champ]` avec `[valeur]`
3. Cliquer sur le bouton `[bouton]`
4. Observer le résultat `[description]`

**Résultat obtenu :**
```
[Copiez ici le message d'erreur, traceback ou résultat inattendu]
```

**Résultat attendu :**
```
[Décrivez ce qui aurait dû se produire]
```

---

## Preuves

### Captures d'écran
> Joignez des captures d'écran annotées si possible.

- `[Fichier : screenshot_before.png]`
- `[Fichier : screenshot_after.png]`

### Logs / Traceback
```python
# Copiez ici le traceback Python complet ou les logs pertinents
Traceback (most recent call last):
  File "[fichier]", line [X], in [fonction]
    [code problématique]
[ExceptionType]: [message d'erreur]
```

### Sortie console / Terminal
```bash
# Copiez ici la sortie console pertinente
[sortie]
```

---

## Analyse Complémentaire

### Cause racine (si identifiée)
> Décrivez la cause technique du bug.

`[À REMPLIR OU Laisser vide si non identifié]`

### Solution proposée
> Décrivez la correction suggérée.

`[À REMPLIR OU Laisser vide]`

### Cas de test de non-régression
> Décrivez le test qui empêchera la réapparition de ce bug.

`[À REMPLIR OU Laisser vide]`

---

## Suivi

| Statut | Date | Commentaire | Auteur |
|---|---|---|---|
| `Ouvert` | JJ/MM/AAAA | Bug signalé | `[Nom]` |
| `En cours` | JJ/MM/AAAA | Pris en charge | `[Nom]` |
| `Corrigé` | JJ/MM/AAAA | Correction validée | `[Nom]` |
| `Vérifié` | JJ/MM/AAAA | Re-testé et confirmé | `[Nom QA]` |
| `Reporté` | JJ/MM/AAAA | Reporté au Sprint suivant | `[Nom]` |

**Statut actuel :** `☐ Ouvert` `☐ En cours` `☐ Corrigé` `☐ Vérifié` `☐ Reporté`

---

## Liens

- **User Story liée :** `[US-XXX]`
- **Test de régression :** `[tests/regression/test_bug_XXX.py]`
- **Commit de correction :** `[hash du commit]`
- **PR liée :** `[numéro de PR]`
