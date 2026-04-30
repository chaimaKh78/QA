path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix 1: lines 66-77 (index 65-76) - bad defaults dict syntax
new1 = [
    '        profile, _ = UserProfile.objects.get_or_create(\n',
    '            user=user,\n',
    '            defaults={\n',
    '                "phone": "+33 6 12 34 56 78",\n',
    '                "address": "12 Rue de la Paix",\n',
    '                "city": "Paris",\n',
    '                "country": "France",\n',
    '                "date_of_birth": date(1985, 7, 14),\n',
    '                "nationality": "Francaise",\n',
    '                "passport_number": "FR12345678",\n',
    '                "gender": "M",\n',
    '                "newsletter": True,\n',
    '            }\n',
    '        )\n',
]
lines[65:77] = new1

# Show lines 115-150 for remaining fixes
for i in range(114, 150):
    print(f"  {i+1}: {lines[i]}", end='')
