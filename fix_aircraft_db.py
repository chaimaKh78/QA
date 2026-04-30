path = 'tests/unit/test_models_flights.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'class TestAircraft:\n    """Tests unitaires du modele Aircraft."""'
new = '@pytest.mark.django_db\nclass TestAircraft:\n    """Tests unitaires du modele Aircraft."""'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK")
else:
    print("FAIL")
