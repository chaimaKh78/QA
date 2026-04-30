path = 'tests/unit/test_models_bookings.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(85, 95):
    print(f"{i+1}: {lines[i]}", end='')
