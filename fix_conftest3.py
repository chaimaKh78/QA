path = 'tests/conftest.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def django_db_setup():
    """Let pytest-django manage the test DB automatically."""
    pass'''

if old in content:
    content = content.replace(old, '')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - django_db_setup supprime entierement")
else:
    print("FAIL")
