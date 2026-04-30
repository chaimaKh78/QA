path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace lines 96-115 (index 95-114)
new_auto = [
    '        # Disconnect signal to test manual creation\n',
    '        from django.db.models.signals import post_save\n',
    '        post_save.disconnect(receiver=create_user_profile, sender=User)\n',
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
    '            post_save.connect(create_user_profile, sender=User)\n',
    '        \n',
]

# Find start line (index 95)
start_idx = 95
# Find end - look for next def or class
end_idx = start_idx
for i in range(start_idx, len(lines)):
    if i > start_idx and (lines[i].strip().startswith('def ') or lines[i].strip().startswith('class ')):
        end_idx = i
        break
    if i == len(lines) - 1:
        end_idx = len(lines)

lines[start_idx:end_idx] = new_auto

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"OK - remplace lignes {start_idx+1}-{end_idx}")
for i in range(start_idx, start_idx + len(new_auto) + 2):
    if i < len(lines):
        print(f"  {i+1}: {lines[i]}", end='')
