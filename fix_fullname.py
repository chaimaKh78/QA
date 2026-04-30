path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace line 121 - just use the profile created by signal
lines[120] = '        # Profile auto-created by signal, just use it\n'

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(119, 124):
    print(f"  {i+1}: {lines[i]}", end='')
