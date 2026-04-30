path = 'tests/security/test_security_manual.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Total: {len(lines)}")
for i in range(225, min(260, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
