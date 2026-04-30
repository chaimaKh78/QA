path = 'tests/unit/test_models_flights.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(105, 125):
    print(f"{i+1}: {lines[i]}", end='')
