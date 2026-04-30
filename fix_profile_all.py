import glob, re

fixed = []
for pattern in ['tests/**/*.py']:
    for fpath in glob.glob(pattern, recursive=True):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'UserProfile.objects.create(' in content:
            content = content.replace('UserProfile.objects.create(', 'UserProfile.objects.update_or_create(defaults={')
            # Now fix the closing - replace ) that closes create with })
            # This is tricky, better to do it file by file
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed.append(fpath)

print(f"Fichiers traites: {len(fixed)}")
for f in fixed:
    print(f"  {f}")

# For test_regression.py specifically, fix the exact pattern
path = 'tests/test_regression.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''profile = UserProfile.objects.update_or_create(defaults={
            user=user,
            phone="+216 22 333 444",
            city="Tunis",
            country="Tunisie",
            nationality="Tunisienne",
            gender="M",
        })'''

new = '''profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "phone": "+216 22 333 444",
                "city": "Tunis",
                "country": "Tunisie",
                "nationality": "Tunisienne",
                "gender": "M",
            }
        )'''

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("test_regression.py: OK")
else:
    print("test_regression.py: pattern non trouve, affichage lignes 238-250")
    lines = content.split('\n')
    for i in range(239, 250):
        print(f"  {i+1}: {repr(lines[i])}")
