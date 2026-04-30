path = 'tests/factories.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Add missing fields to FlightFactory after duration line
for i, line in enumerate(lines):
    if 'duration = factory.LazyAttribute' in line and 'flight' in lines[min(i+3, len(lines)-1)].lower() or 'flight_number' in lines[max(i-5,0)].lower():
        # Insert after the duration line
        idx = i + 1
        # Find the next blank line
        while idx < len(lines) and lines[idx].strip():
            idx += 1
        # Insert before the blank line
        insert_lines = [
            '    base_price_economy = factory.LazyFunction(\n',
            '        lambda: __import__("decimal").Decimal(__import__("random").uniform(100, 800)).quantize(__import__("decimal").Decimal("0.01")))\n',
            '    base_price_business = factory.LazyFunction(\n',
            '        lambda: __import__("decimal").Decimal(__import__("random").uniform(300, 2000)).quantize(__import__("decimal").Decimal("0.01")))\n',
            '    available_seats_economy = 150\n',
            '    available_seats_business = 20\n',
        ]
        for j, il in enumerate(insert_lines):
            lines.insert(idx + j, il)
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(33, 58):
    if i < len(lines):
        print(f"  {i+1}: {lines[i]}", end='')
