conftest_path = 'tests/conftest.py'
with open(conftest_path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        "TEST": {
            "NAME": db_file,
        },'''

new = '''        "TEST": {
            "NAME": db_file,
            "SERIALIZED_ROLLBACK": False,
        },'''

if old in content:
    content = content.replace(old, new)
    with open(conftest_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - SERIALIZED_ROLLBACK = False ajoute")
else:
    print("FAIL - texte non trouve")
