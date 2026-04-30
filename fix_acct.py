path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'class TestUserProfile:\n\n\n    def test_profile_creation'
new = '@pytest.mark.django_db\nclass TestUserProfile:\n\n\n    def test_profile_creation'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK")
else:
    print("FAIL")
