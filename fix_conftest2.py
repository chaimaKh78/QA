path = 'tests/conftest.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def django_db_setup():
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
            "SERIALIZED_ROLLBACK": False,
        },
    }'''

new = 'def django_db_setup():\n    """Let pytest-django manage the test DB automatically."""\n    pass'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - django_db_setup simplifie (pass)")
else:
    print("FAIL - texte non trouve, essai alternatif...")
    # Try to find the function
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def django_db_setup' in line:
            for j in range(i, min(i+20, len(lines))):
                print(f"  {j+1}: {repr(lines[j])}")
            break
