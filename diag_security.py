path = 'tests/security/test_auth_security.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Show lines 60-80
for i in range(59, min(80, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
