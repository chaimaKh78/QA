lines = open("tests/conftest.py","r",encoding="utf-8").readlines()
for i in range(44, 52):
    print(repr(lines[i]))
