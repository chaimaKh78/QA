path = 'tests/conftest.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove the django_db_setup fixture (lines 46-61 approx)
# Also find the line 'import tempfile' if it was added
new_lines = []
skip = False
skip_range = None
for i, line in enumerate(lines):
    # Detect start of django_db_setup fixture
    if '@pytest.fixture(scope="session")' in line and i+1 < len(lines) and 'def django_db_setup' in lines[i+1]:
        skip = True
        continue
    if skip:
        if line.strip() and not line.startswith(' ') and not line.startswith('\t') and line.strip() != '':
            skip = False
        elif 'def django_db_setup' in line:
            continue
        else:
            continue
    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"OK - django_db_setup supprime ({len(lines)} -> {len(new_lines)} lignes)")
# Show lines 40-55 to verify
with open(path, 'r', encoding='utf-8') as f:
    vl = f.readlines()
for i in range(39, min(60, len(vl))):
    print(f"  {i+1}: {vl[i]}", end='')
