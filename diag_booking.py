path = 'tests/api/test_booking_api.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(210, min(240, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
