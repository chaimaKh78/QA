path = 'tests/security/test_owasp_top10.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Total lignes: {len(lines)}")
for i, line in enumerate(lines):
    print(f"{i+1}: {line}", end='')
