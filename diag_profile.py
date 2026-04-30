import glob

for fpath in ['tests/conftest.py', 'tests/unit/test_models_accounts.py']:
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'get_or_create' in line or 'update_or_create' in line:
            start = max(0, i-1)
            end = min(len(lines), i+10)
            print(f"--- {fpath} ligne {i+1} ---")
            for j in range(start, end):
                print(f"  {j+1}: {lines[j]}", end='')
            print()
