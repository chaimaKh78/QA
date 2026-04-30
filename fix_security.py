path = 'tests/security/test_auth_security.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines 92-95 (index 91-94): broken assert
# Old lines 92-95:
#     if response.status_code in (301, 302):
#         assert response.status_code == 302  # Redirects to login, (
#             f"Redirect sans auth devrait aller vers login, obtenu: {response.url}"
#         )

# Replace with proper code
new_lines = [
    '        if response.status_code in (301, 302):\n',
    '            assert "login" in response.url, (\n',
    '                f"Redirect sans auth devrait aller vers login, obtenu: {response.url}"\n',
    '            )\n',
]

lines[91:95] = new_lines

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK - ligne 92-95 corrigees")
# Verify
with open(path, 'r', encoding='utf-8') as f:
    vlines = f.readlines()
for i in range(90, 96):
    print(f"  {i+1}: {vlines[i]}", end='')
