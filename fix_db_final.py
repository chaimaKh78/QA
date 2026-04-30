conftest_path = 'tests/conftest.py'
with open(conftest_path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }'''

new = '''@pytest.fixture(scope="session")
def django_db_setup():
    """
    Configuration de la base de donnees de test.
    Utilise un fichier SQLite temporaire.
    """
    import tempfile
    from django.conf import settings
    db_file = tempfile.mktemp(suffix=".sqlite3")
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": db_file,
        "TEST": {
            "NAME": db_file,
        },
    }'''

if old in content:
    content = content.replace(old, new)
    with open(conftest_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - django_db_setup: :memory: remplace par fichier temporaire")
else:
    print("FAIL - ancien texte non trouve dans conftest.py")
    # Debug: show lines 46-53
    lines = content.split('\n')
    for i in range(45, min(53, len(lines))):
        print(f"  {i+1}: {repr(lines[i])}")
