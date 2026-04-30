path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lines 142-153 (index 141-152)
new_lines = [
    '        # Profile auto-created by signal\n',
    '        assert user.profile.user == user\n',
    '        # Verifier que l\'on ne peut pas creer deux profils pour le meme user\n',
    '        from django.db import IntegrityError\n',
    '        with pytest.raises(IntegrityError):\n',
    '            UserProfile.objects.create(user=user)\n',
    '\n',
    '    def test_profile_newsletter_default(self):\n',
    '        """Test que newsletter est False par defaut."""\n',
    '        user = User.objects.create_user(\n',
    '            username="newsletter_test",\n',
    '            email="newsletter@example.com",\n',
    '        )\n',
    '        profile = user.profile\n',
    '        assert profile.newsletter is False\n',
]

lines[141:153] = new_lines

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(140, 160):
    if i < len(lines):
        print(f"  {i+1}: {lines[i]}", end='')
