path = 'tests/security/test_security_manual.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(88, 100):
    print(f"{i+1}: {lines[i]}", end='')
