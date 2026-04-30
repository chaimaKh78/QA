# generate_json_results.py
import os, re, json, datetime, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))

print("Running tests...")
venv_python = os.path.join(BASE, 'venv', 'Scripts', 'python.exe')
result = subprocess.run(
    [venv_python, 'manage.py', 'test', '-v', '2'],
    capture_output=True, text=True, cwd=BASE,
    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
)
output = result.stdout + result.stderr

with open(os.path.join(BASE, 'test_output.txt'), 'w', encoding='utf-8') as f:
    f.write(output)

lines = output.split('\n')
parsed = []
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    m1 = re.match(r'^(test_\w+)\s+\(([\w.]+)\)\s*$', line)
    if m1 and i + 1 < len(lines):
        next_line = lines[i + 1].strip()
        m2 = re.match(r'^(.+?)\s*\.\.\.\s*(ok|FAIL|ERROR)', next_line)
        if m2:
            parsed.append({
                'name': m1.group(1),
                'module': m1.group(2),
                'description': m2.group(1).strip(),
                'passed': m2.group(2) == 'ok',
                'status': m2.group(2).upper()
            })
            i += 2
            continue
    i += 1

if not parsed:
    print(f"WARNING: 0 tests parsed. Output length: {len(output)}")
    print(output[:500])
    sys.exit(1)

with open(os.path.join(BASE, 'test_results.json'), 'w', encoding='utf-8') as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)

passed = sum(1 for t in parsed if t['passed'])
print(f"Done: {len(parsed)} tests, {passed} passed, {len(parsed)-passed} failed")