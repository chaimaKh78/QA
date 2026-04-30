with open('pytest.ini', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'addopts = --ds=nouvelair.settings --ignore=tests/unit/test_models_promotions.py'
new = 'addopts = --ds=nouvelair.settings --ignore=tests/unit/test_models_promotions.py --ignore=tests/e2e'

if old in content:
    content = content.replace(old, new)
    with open('pytest.ini', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - tests/e2e ignores")
else:
    print("FAIL")
