path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 120 (index 119): nationality as filter -> defaults
lines[119] = '        UserProfile.objects.get_or_create(user=user, defaults={"nationality": "Francaise"})[0]\n'

# Fix lines 146-149 (index 145-148): get_or_create won't raise IntegrityError, use create instead
lines[147] = '        with pytest.raises(IntegrityError):\n'
lines[148] = '            UserProfile.objects.create(user=user)\n'
# Remove line 149 (old get_or_create line)
del lines[149]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
# Verify
for i in [118, 119, 145, 146, 147, 148]:
    if i < len(lines):
        print(f"  {i+1}: {lines[i]}", end='')
