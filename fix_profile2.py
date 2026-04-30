import glob

# Fix all 3 files that were incorrectly modified
for fpath in ['tests/conftest.py', 'tests/test_regression.py', 'tests/unit/test_models_accounts.py']:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'UserProfile.objects.update_or_create(defaults={' in content:
        content = content.replace(
            'UserProfile.objects.update_or_create(defaults={',
            'UserProfile.objects.get_or_create(user=user, defaults={'
        )
        # Now fix the closing: need to add closing ) after }
        # Find pattern: }\n        ) and replace with }\n        )[0]
        # Actually get_or_create returns tuple, let's use update_or_create properly
        # Let's just revert to a simpler approach
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {fpath}: fix1 applique")

# Now fix test_regression.py specifically
path = 'tests/test_regression.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 240-247 (index 239-246) - fix to proper get_or_create
new_lines = [
    '        profile, _ = UserProfile.objects.get_or_create(\n',
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
lines[239:247] = new_lines

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("  test_regression.py: OK")

# Fix conftest.py - find and fix the update_or_create pattern
path = 'tests/conftest.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
# Show context around update_or_create
if 'update_or_create' in content:
    idx = content.index('update_or_create')
    print(f"  conftest.py context: ...{repr(content[max(0,idx-50):idx+100])}...")
