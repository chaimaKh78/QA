path = 'tests/test_regression.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'client.post(reverse("accounts:logout"), follow=True)',
    'client.get(reverse("accounts:logout"), follow=True)'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("OK")
