path = 'tests/security/test_owasp_top10.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Insert response = client.get("/") at line 475 (index 474)
lines.insert(474, '        response = client.get("/")\n')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(473, 479):
    print(f"  {i+1}: {lines[i]}", end='')
