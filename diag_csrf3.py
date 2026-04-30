path = 'tests/security/test_security_manual.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(96, 112):
    print(f"{i+1}: {repr(lines[i])}")
