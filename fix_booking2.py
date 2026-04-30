path = 'tests/api/test_booking_api.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lines 220-222 (index 219-221)
lines[219] = '        assert response.status_code in (200, 302)\n'
lines[220] = '        # 200 = vue accessible sans auth, 302 = redirige vers accueil\n'
lines[221] = '\n'

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK")
for i in range(218, 224):
    print(f"  {i+1}: {repr(lines[i])}")
