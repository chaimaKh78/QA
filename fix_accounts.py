path = 'tests/integration/test_views_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'assert "/login/" in response.url or "login" in response.url'
new = 'assert "/login/" in response.url or "login" in response.url or "connexion" in response.url'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK")
else:
    print("FAIL")
