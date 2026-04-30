path = 'tests/integration/test_views_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(173, 180):
    print(f"{i+1}: {repr(lines[i])}")
