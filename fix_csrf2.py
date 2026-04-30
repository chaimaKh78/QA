path = 'tests/security/test_security_manual.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Insert closing ) after line 105 (index 105)
lines.insert(105, '        )\n')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(99, 110):
    print(f"  {i+1}: {lines[i]}", end='')
