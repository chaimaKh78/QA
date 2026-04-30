path = 'tests/factories.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# After line 19: is_active = True, add latitude and longitude
lines.insert(19, '    latitude = factory.LazyFunction(lambda: __import__("random").uniform(-90, 90))\n')
lines.insert(20, '    longitude = factory.LazyFunction(lambda: __import__("random").uniform(-180, 180))\n')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(9, 25):
    print(f"  {i+1}: {lines[i]}", end='')
