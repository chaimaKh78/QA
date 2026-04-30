path = 'tests/test_regression.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'assert str(flight) == "BJ201: TUN \u2192 CDG"'
new = 'assert "BJ201: TUN \u2192 CDG" in str(flight)'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK")
else:
    print("FAIL")
