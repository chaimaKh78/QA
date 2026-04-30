import pathlib

p = pathlib.Path("tests/conftest.py")
c = p.read_text(encoding="utf-8")

old = '''@pytest.fixture(scope="session")
def django_db_setup():
    """
    Configuration de la base de donnees de test.
    Utilise la base SQLite par defaut de pytest-django.
    """
    pass'''

new = '''@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }'''

c = c.replace(old, new)
p.write_text(c, encoding="utf-8")
print("OK" if ":memory:" in p.read_text() else "FAIL")
