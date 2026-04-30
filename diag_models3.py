path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(63, 82):
    print(f"{i+1}: {lines[i]}", end='')
