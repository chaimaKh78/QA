with open('flights/models.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'class Flight' in line and 'models.Model' in line:
        for j in range(i, min(i+60, len(lines))):
            print(f"  {j+1}: {lines[j]}", end='')
        break
