import pathlib
p = pathlib.Path("tests/conftest.py")
c = p.read_text(encoding="utf-8")
old = "def django_db_setup():\n    pass"
new = "def django_db_setup():\n    from django.conf import settings\n    settings.DATABASES[\"default\"] = {\n        \"ENGINE\": \"django.db.backends.sqlite3\",\n        \"NAME\": \":memory:\",\n    }"
c = c.replace(old, new)
p.write_text(c, encoding="utf-8")
print("OK" if ":memory:" in p.read_text() else "FAIL")
