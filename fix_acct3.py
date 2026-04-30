path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix 1: test_profile_auto_creation - disconnect signal before test
# Replace lines 97-108 (index 96-107)
new_auto = [
    '        # Disconnect signal to test manual creation\n',
    '        from django.db.models.signals import post_save\n',
    '        post_save.disconnect(sender=User, dispatch_uid="create_user_profile")\n',
    '        try:\n',
    '            user = User.objects.create_user(\n',
    '                username="test_auto_profile",\n',
    '                email="auto@example.com",\n',
    '            )\n',
    '            assert UserProfile.objects.filter(user=user).count() == 0\n',
    '            create_user_profile(sender=User, instance=user, created=True)\n',
    '            assert UserProfile.objects.filter(user=user).count() == 1\n',
    '            profile = user.profile\n',
    '            assert profile is not None\n',
    '            assert isinstance(profile, UserProfile)\n',
    '        finally:\n',
    '            post_save.connect(create_user_profile, sender=User, dispatch_uid="create_user_profile")\n',
]
lines[96:108] = new_auto

# Fix 2: lines 121-123 duplicate get_or_create + undefined 'profile'
# Find line with "profile.full_name"
for i, line in enumerate(lines):
    if 'assert profile.full_name == "Marie Curie"' in line:
        # Replace the line before and this line
        lines[i] = '        assert user.profile.full_name == "Marie Curie"\n'
        # Remove duplicate get_or_create lines before it
        if i >= 2 and 'get_or_create' in lines[i-1]:
            del lines[i-1]
        if i >= 2 and 'get_or_create' in lines[i-2]:
            del lines[i-2]
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
# Verify
for i in range(95, 125):
    if i < len(lines):
        print(f"  {i+1}: {lines[i]}", end='')
