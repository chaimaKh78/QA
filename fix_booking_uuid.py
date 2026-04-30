path = 'tests/unit/test_models_bookings.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix indentation line 48 (index 47)
lines[47] = '        )\n'

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("test_models_bookings.py: OK")

# Check Booking model for reference field type
import glob, re
for fpath in glob.glob('bookings/models.py'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines_b = content.split('\n')
    for i, line in enumerate(lines_b):
        if 'reference' in line.lower() and ('field' in line.lower() or 'uuid' in line.lower() or 'char' in line.lower() or 'models' in line.lower()):
            print(f"  bookings/models.py {i+1}: {line.strip()}")
