path = 'tests/test_regression.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = [
    '        profile, _ = UserProfile.objects.update_or_create(\n',
    '            user=user,\n',
    '            defaults={\n',
    '                "phone": "+216 22 333 444",\n',
    '                "city": "Tunis",\n',
    '                "country": "Tunisie",\n',
    '                "nationality": "Tunisienne",\n',
    '                "gender": "M",\n',
    '            }\n',
    '        )\n',
]
lines[241:251] = new_lines

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
