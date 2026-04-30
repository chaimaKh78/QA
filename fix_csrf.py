path = 'tests/security/test_security_manual.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lines 99-105: use Client with enforce_csrf_checks
old_lines = lines[98:105]
print("Old lines:")
for i, l in enumerate(old_lines):
    print(f"  {99+i}: {repr(l)}")

new_lines = [
    '        csrf_client = Client(enforce_csrf_checks=True)\n',
    '        response = csrf_client.post(\n',
    '            "/accounts/connexion/",\n',
    '            {\n',
    '                "username": "testuser",\n',
    '                "password": "testpass",\n',
    '            },\n',
]
lines[98:105] = new_lines

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
