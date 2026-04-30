path = 'tests/security/test_owasp_top10.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(467, 480):
    print(f"{i+1}: {repr(lines[i])}")
