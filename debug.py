import os, re
BASE = os.path.dirname(os.path.abspath(__file__))

for name, path in [
    ('forms.py', os.path.join(BASE, 'flights', 'forms.py')),
    ('test (240-260)', os.path.join(BASE, 'flights', 'tests', 'test_models.py')),
    ('views.py', os.path.join(BASE, 'flights', 'views.py')),
]:
    print(f'\n===== {name} =====')
    if not os.path.exists(path):
        print('NOT FOUND')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'test' in name:
        lines = content.split('\n')
        for i, l in enumerate(lines[239:260], 240):
            print(f'{i}: {l}')
    else:
        print(content)

# Find search template
for d in [os.path.join(BASE, 'flights', 'templates', 'flights'),
          os.path.join(BASE, 'templates', 'flights')]:
    if os.path.isdir(d):
        for fn in os.listdir(d):
            if 'search' in fn.lower() or 'home' in fn.lower():
                print(f'\n===== template: {fn} =====')
                with open(os.path.join(d, fn), 'r', encoding='utf-8') as f:
                    print(f.read())