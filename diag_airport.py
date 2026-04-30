path = 'tests/factories.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Show AirportFactory
for i, line in enumerate(lines):
    if 'class AirportFactory' in line:
        for j in range(i, min(i+25, len(lines))):
            print(f"  {j+1}: {lines[j]}", end='')
        print()
        break
