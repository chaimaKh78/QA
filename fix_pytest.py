with open('pytest.ini', 'r', encoding='utf-8') as f:
    content = f.read()

old_line = 'django_db_serialized_rollback = false'
if old_line in content:
    content = content.replace(old_line + '\n', '')
    with open('pytest.ini', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - ligne supprimee de pytest.ini")
else:
    print("SKIP - ligne deja absente")
