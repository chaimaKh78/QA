path = 'tests/security/test_auth_security.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    print(f"{i+1}: {line}", end='')
