path = 'tests/test_regression.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(235, 250):
    print(f"{i+1}: {lines[i]}", end='')
