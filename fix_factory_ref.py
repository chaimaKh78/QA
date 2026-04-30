path = 'tests/factories.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '    reference = factory.Sequence(lambda n: \'REF%08d\' % n)'
new = '    reference = factory.LazyFunction(lambda: __import__("uuid").uuid4())'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - BookingFactory.reference utilise uuid4 maintenant")
else:
    print("FAIL")
