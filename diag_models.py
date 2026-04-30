# Fix conftest.py
path = 'tests/conftest.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace lines 163-172
new_conftest = [
    '    profile, _ = UserProfile.objects.get_or_create(\n',
    '        user=user,\n',
    '        defaults={\n',
    '            "phone": "+216 22 345 678",\n',
    '            "city": "Tunis",\n',
    '            "country": "Tunisie",\n',
    '            "nationality": "Tunisienne",\n',
    '            "date_of_birth": date(1990, 5, 15),\n',
    '            "gender": "M",\n',
    '            "newsletter": True,\n',
    '        }\n',
    '    )\n',
]
lines[162:172] = new_conftest

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("conftest.py: OK")

# Fix test_models_accounts.py
path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: lines 66-76 get_or_create with bad dict syntax
old1 = '        profile = UserProfile.objects.get_or_create(user=user, defaults={\n            user=user,\n            phone="+33 6 12 34 56 78",\n            address="12 Rue de la Paix",\n            city="Paris",\n            country="France",\n            date_of_birth=date(1985, 7, 14),\n            nationality="Francaise",\n            passport_number="FR12345678",\n            gender="M",'
print(f"old1 found: {old1[:50] in content}")

# Use line-by-line approach
lines2 = content.split('\n')
print(f"Total lines: {len(lines2)}")
for i in range(63, 80):
    print(f"  {i+1}: {repr(lines2[i])}")
