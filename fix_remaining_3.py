import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print("=" * 55)
print("  Correction des 3 derniers tests")
print("=" * 55)

# ===================================================================
# FIX 1 : accounts/views.py - Ligne 30
# Le signal (FIX precedent) cree deja le profil automatiquement.
# UserProfile.objects.create() essaie de le creer une 2e fois => crash.
# Solution : remplacer create par get_or_create
# ===================================================================
print("\n[FIX 1/3] accounts/views.py - Eviter double creation profil ...")
filepath = os.path.join(BASE_DIR, 'accounts', 'views.py')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = "            UserProfile.objects.create(user=user)"
new = "            UserProfile.objects.get_or_create(user=user)"

if old in content:
    content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  OK - create() remplace par get_or_create()")
else:
    print("  SKIP - Deja corrige")

# ===================================================================
# FIX 2 : accounts/tests/test_models.py - test_login_invalid
# Le message d'erreur FR de Django est "Saisissez un nom d'utilisateur
# et un mot de passe valides." => contient "valides", pas "correct".
# ===================================================================
print("\n[FIX 2/3] accounts/tests/test_models.py - Assertion login ...")
filepath = os.path.join(BASE_DIR, 'accounts', 'tests', 'test_models.py')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Le test original verifiait 'invalid', puis on a change en 'correct'.
# Le vrai mot en FR est 'valides'.
old = "        self.assertContains(response, 'correct')"
new = "        self.assertContains(response, 'valides')"

if old in content:
    content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  OK - Assertion changee de 'correct' a 'valides'")
elif "self.assertContains(response, 'invalid')" in content:
    content = content.replace(
        "self.assertContains(response, 'invalid')",
        "self.assertContains(response, 'valides')"
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  OK - Assertion changee de 'invalid' a 'valides'")
else:
    print("  SKIP - Assertion deja modifiee ou pattern non trouve")

# ===================================================================
# FIX 3 : flights/tests/test_models.py - test_search_same_airport_error
# Le formulaire (flights/forms.py ligne 87) dit :
#   "... doivent etre différents."  (sans 'e' final)
# Mais le test cherche "différentes" (avec 'e').
# Correction : changer le test pour qu'il cherche "différents".
# ===================================================================
print("\n[FIX 3/3] flights/tests/test_models.py - Assertion differentes ...")
filepath = os.path.join(BASE_DIR, 'flights', 'tests', 'test_models.py')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Le test cherche "différentes" mais le message reel est "différents"
old = "        self.assertContains(response, 'différentes')"
new = "        self.assertContains(response, 'différents')"

if old in content:
    content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  OK - 'différentes' corrigé en 'différents'")
else:
    print("  SKIP - Deja corrige ou pattern non trouve")

# ===================================================================
# RESUME
# ===================================================================
print("\n" + "=" * 55)
print("  RESUME")
print("=" * 55)
print("""
  FIX 1 : accounts/views.py ligne 30
    -> create() remplace par get_or_create()
    -> Corrige : test_register_success (IntegrityError)

  FIX 2 : accounts/tests/test_models.py
    -> Assertion 'correct' remplacee par 'valides'
    -> Corrige : test_login_invalid

  FIX 3 : flights/tests/test_models.py
    -> 'différentes' corrigé en 'différents'
    -> Corrige : test_search_same_airport_error
""")
print("  RESULTAT ATTENDU : 70/70 tests OK")
print("=" * 55)
print("\nLancez : python manage.py test\n")