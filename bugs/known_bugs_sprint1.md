# 🐛 Bugs Connus — Sprint 1

## NouvelAir — Registre des Anomalies

| **Document** | Registre des Bugs Connus |
|---|---|
| **Version** | 1.0.0 |
| **Date de mise à jour** | 23/04/2026 |
| **Sprint** | Sprint 1 |
| **Statut** | En cours de suivi |

---

## Résumé

| Statut | Nombre |
|---|:---:|
| ✅ Corrigé | 5 |
| 🟡 Ouvert | 2 |
| **Total** | **7** |

---

## Liste des Bugs

### BUG-001 — Fichiers statiques manquants

| Champ | Détail |
|---|---|
| **Titre** | Fichiers statiques manquants (style.css, main.js, favicon.ico) |
| **Sévérité** | 🟢 Low |
| **Priorité** | Basse |
| **Composant** | `nouvelair/static/` |
| **Statut** | 🟡 Ouvert |

**Description :**
Les fichiers statiques de base (`style.css`, `main.js`, `favicon.ico`) sont absents
du répertoire `nouvelair/static/`. Cela entraîne une page d'accueil sans mise en forme
et des erreurs 404 dans la console du navigateur.

**Impact :**
- L'interface utilisateur s'affiche sans les styles CSS
- Les interactions JavaScript ne fonctionnent pas
- L'icône de favori est manquante dans l'onglet du navigateur

**Résolution prévue :** Sprint 2 — Création des assets front-end.

---

### BUG-002 — Messages « Broken pipe » de Selenium dans les logs

| Champ | Détail |
|---|---|
| **Titre** | Messages « Broken pipe » de Selenium dans la sortie de test |
| **Sévérité** | 🟢 Low |
| **Priorité** | Basse |
| **Composant** | `ai_testing/tests_e2e.py` |
| **Statut** | 🟡 Ouvert |

**Description :**
Lors de l'exécution des tests E2E avec Selenium, des messages d'erreur « Broken pipe »
apparaissent dans la sortie standard. Ces messages n'affectent pas le résultat des tests
mais polluent les logs et rendent l'analyse plus difficile.

**Exemple de sortie :**
```
selenium.common.exceptions.WebDriverException: Message: 
connection refused or broken pipe
```

**Impact :**
- Pollution visuelle des logs de test
- Difficulté d'identification des vraies erreurs
- Aucun impact fonctionnel

**Résolution prévue :** Sprint 2 — Configuration du logging Selenium, redirection
stderr vers un fichier séparé.

---

### BUG-003 — Validation du formulaire de recherche : origine ≠ destination ✅

| Champ | Détail |
|---|---|
| **Titre** | FlightSearchForm : la validation n'empêche pas origin == destination |
| **Sévérité** | 🟡 Medium |
| **Priorité** | Moyenne |
| **Composant** | `flights/forms.py` — `FlightSearchForm` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Le formulaire de recherche de vols acceptait des recherches où l'aéroport d'origine
et l'aéroport de destination sont identiques (ex: TUN → TUN), ce qui est métieriquement
incorrect.

**Correction appliquée :**
Ajout d'une validation croisée dans la méthode `clean()` du formulaire :
```python
def clean(self):
    cleaned_data = super().clean()
    origin = cleaned_data.get('origin')
    destination = cleaned_data.get('destination')
    if origin and destination and origin == destination:
        raise forms.ValidationError(
            "L'aéroport d'origine et de destination doivent être différents."
        )
    return cleaned_data
```

**Test de non-régression :** `tests/unit/test_flight_forms.py::test_origin_destination_must_differ`

---

### BUG-004 — Double création du UserProfile lors de l'inscription ✅

| Champ | Détail |
|---|---|
| **Titre** | UserProfile créé en double lors de l'inscription d'un nouvel utilisateur |
| **Sévérité** | 🔴 High |
| **Priorité** | Haute |
| **Composant** | `accounts/views.py` — `register` + `accounts/signals.py` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Le profil utilisateur (`UserProfile`) était créé simultanément par la vue `register`
et par un signal `post_save`. Cela provoquait une erreur `IntegrityError` à cause de
la contrainte `OneToOneField` sur `user`.

**Correction appliquée :**
1. Suppression de la création manuelle dans `accounts/views.py`
2. Conservation exclusive du signal `post_save` pour la création automatique du profil
3. Utilisation de `get_or_create()` dans le signal pour gérer les cas de concurrence

**Test de non-régression :** `tests/unit/test_user_profile.py::test_single_profile_on_registration`

---

### BUG-005 — Message d'erreur de login non cohérent ✅

| Champ | Détail |
|---|---|
| **Titre** | Le message d'erreur affiché lors d'un échec de connexion ne correspond pas au texte attendu par les tests |
| **Sévérité** | 🟡 Medium |
| **Priorité** | Moyenne |
| **Composant** | `accounts/views.py` — `login` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Le message d'erreur retourné par Django lors d'une mauvaise authentification était
« Please enter a correct username and password. » (message par défaut Django), tandis
que les tests attendaient un message personnalisé en français :
« Nom d'utilisateur ou mot de passe incorrect. »

**Correction appliquée :**
Utilisation du paramètre `error_messages` dans `AuthenticationForm` :
```python
class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Nom d'utilisateur ou mot de passe incorrect. "
            "Veuillez vérifier vos identifiants."
        ),
        'inactive': _("Ce compte est désactivé."),
    }
```

**Test de non-régression :** `tests/unit/test_account_forms.py::test_login_error_message_french`

---

### BUG-006 — Conflit de routage URL pour l'application promotions ✅

| Champ | Détail |
|---|---|
| **Titre** | Les URLs de l'application promotions entrent en conflit avec d'autres patterns |
| **Sévérité** | 🔴 High |
| **Priorité** | Haute |
| **Composant** | `promotions/urls.py` + `nouvelair/urls.py` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Le routage des URLs de l'application `promotions` générait des conflits avec les
patterns d'URL existants, provoquant des erreurs 404 ou des redirections incorrectes.
Les endpoints `/promotions/` et `/promo/` étaient en concurrence.

**Correction appliquée :**
1. Harmonisation des patterns URL dans `nouvelair/urls.py`
2. Utilisation d'un namespace dédié : `app_name = 'promotions'`
3. Ajout de `$` en fin de chaque pattern pour éviter les captures partielles
4. Vérification de l'absence de conflit avec `urlpatterns` des autres apps

**Test de non-régression :** `tests/integration/test_promotion_views.py::test_promotion_urls_resolve`

---

### BUG-007 — Tests E2E utilisant les mauvaises URLs d'application ✅

| Champ | Détail |
|---|---|
| **Titre** | Les tests E2E font référence à des URLs d'application incorrectes |
| **Sévérité** | 🔴 High |
| **Priorité** | Haute |
| **Composant** | `ai_testing/tests_e2e.py` |
| **Statut** | ✅ **Corrigé** |

**Description :**
Les tests de bout en bout utilisaient des chemins URL codés en dur qui ne
correspondaient pas aux véritables patterns de routage des applications Django.
Par exemple, `/flight/search/` au lieu de `/flights/search/` ou
`/booking/create/` au lieu de `/bookings/create/`.

**Correction appliquée :**
1. Remplacement des URL codées en dur par des appels à `reverse()` :
   ```python
   from django.urls import reverse
   url = reverse('flights:search')
   ```
2. Vérification systématique de chaque URL avec `resolve()`
3. Ajout d'un test de validation de toutes les URLs E2E

**Test de non-régression :** `tests/integration/test_url_resolution.py::test_all_e2e_urls_resolve`

---

## Statistiques

### Par sévérité

| Sévérité | Total | Corrigés | Ouverts |
|---|:---:|:---:|:---:|
| 🔴 Critical | 0 | 0 | 0 |
| 🔴 High | 3 | 3 | 0 |
| 🟡 Medium | 2 | 2 | 0 |
| 🟢 Low | 2 | 0 | 2 |

### Par composant

| Composant | Bugs |
|---|:---:|
| `flights/forms.py` | 1 |
| `accounts/views.py` | 1 |
| `accounts/signals.py` | 1 |
| `promotions/urls.py` | 1 |
| `nouvelair/urls.py` | 1 |
| `ai_testing/tests_e2e.py` | 1 |
| `nouvelair/static/` | 1 |

---

## Historique des modifications

| Date | Bug | Action | Auteur |
|---|---|---|---|
| 23/04/2026 | BUG-001 à BUG-007 | Création du registre initial | Équipe QA |
