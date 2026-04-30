path = 'tests/unit/test_models_accounts.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'UserProfile.objects.get_or_create(\n            user=user,\n            defaults={',
    'UserProfile.objects.update_or_create(\n            user=user,\n            defaults={'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
