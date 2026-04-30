path = 'tests/security/test_auth_security.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '        assert response.status_code == 302  # Redirects to login, (\n            f"Redirect devrait pointer vers login, obtenu: {response.url}"\n        )'

new = '        assert "login" in response.url, (\n            f"Redirect devrait pointer vers login, obtenu: {response.url}"\n        )'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - indentation corrigee")
else:
    print("FAIL - texte non trouve")
    # Debug
    lines = content.split('\n')
    for i in range(66, 72):
        print(f"  {i+1}: {repr(lines[i])}")
