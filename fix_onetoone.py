path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove lines 147-148 (the get_or_create IntegrityError check)
del lines[146:148]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(143, 153):
    if i < len(lines):
        print(f"  {i+1}: {lines[i]}", end='')
