path = 'tests/security/test_owasp_top10.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Total lignes: {len(lines)}")
for i in range(448, min(475, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
