with open('pytest.ini', 'r', encoding='utf-8') as f:
    content = f.read()

if 'serialized_rollback' not in content:
    # Add after [pytest] line
    content = content.replace(
        '[pytest]',
        '[pytest]\ndjango_db_serialized_rollback = false'
    )
    with open('pytest.ini', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - serialized_rollback = false ajoute a pytest.ini")
else:
    print("SKIP - serialized_rollback deja present")
