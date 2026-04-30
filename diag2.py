print("=== pytest.ini ===")
print(open("pytest.ini","r",encoding="utf-8").read())
print("=== conftest.py root ===")
import os
if os.path.exists("conftest.py"):
    print(open("conftest.py","r",encoding="utf-8").read())
else:
    print("(n existe pas)")
print("=== lines 40-60 de tests/conftest.py ===")
lines = open("tests/conftest.py","r",encoding="utf-8").readlines()
for i in range(40, min(60, len(lines))):
    print(f"{i}: {repr(lines[i])}")
