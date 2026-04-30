path = 'tests/test_regression.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = [
    '    profile, _ = UserProfile.objects.get_or_create(\n',
    '        user=user,\n',
    '        defaults={\n',
    '            "phone": "+216 22 333 444",\n',
    '            "address": "12 Rue Habib Bourguiba",\n',
    '            "city": "Tunis",\n',
    '            "country": "Tunisie",\n',
    '            "date_of_birth": date(1990, 5, 15),\n',
    '            "nationality": "Tunisienne",\n',
    '            "gender": "M",\n',
    '            "newsletter": True,\n',
    '        }\n',
    '    )\n',
]
lines[112:123] = new_lines

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(111, 125):
    print(f"  {i+1}: {lines[i]}", end='')
