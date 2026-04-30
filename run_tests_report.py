# run_tests_report.py
import subprocess, os, sys, datetime, re

BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE, 'test_reports'), exist_ok=True)

# Use the venv Python
venv_python = os.path.join(BASE, 'venv', 'Scripts', 'python.exe')

result = subprocess.run(
    [venv_python, 'manage.py', 'test', '-v', '2'],
    capture_output=True, text=True, cwd=BASE
)

output = result.stdout + result.stderr
lines = output.split('\n')

# Save raw output for debugging
with open(os.path.join(BASE, 'test_reports', 'raw.txt'), 'w', encoding='utf-8') as f:
    f.write(output)

# Parse tests
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
                'name': m1.group(2),
                'test': m1.group(1),
                'desc': m2.group(1).strip(),
                'status': m2.group(2)
            })
            i += 2
            continue
    i += 1

if not parsed:
    total_m = re.search(r'Ran (\d+) test', output)
    if total_m:
        n = int(total_m.group(1))
        has_ok = 'OK' in output.split('Ran')[-1]
        for x in range(n):
            parsed.append({'name': 'suite', 'test': f'test_{x+1}', 'desc': 'Auto-detected', 'status': 'ok' if has_ok else 'FAIL'})

passed = sum(1 for t in parsed if t['status'] == 'ok')
failed = sum(1 for t in parsed if t['status'] == 'FAIL')
errors = sum(1 for t in parsed if t['status'] == 'ERROR')

html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8"><title>NouvelAir - Rapport de Tests</title>
<style>
*{{box-sizing:border-box}}body{{font-family:'Segoe UI',Arial,sans-serif;margin:0;padding:30px;background:#f0f2f5}}
.header{{background:linear-gradient(135deg,#1a237e,#0d47a1,#01579b);color:#fff;padding:35px;border-radius:14px;margin-bottom:25px;box-shadow:0 4px 15px rgba(0,0,0,.2)}}
.header h1{{margin:0 0 8px;font-size:28px}}.header p{{margin:0;opacity:.85;font-size:15px}}
.timestamp{{text-align:right;color:#888;margin-bottom:15px;font-size:14px}}
.summary{{display:flex;gap:18px;margin-bottom:25px;flex-wrap:wrap}}
.stat{{padding:22px 35px;border-radius:12px;color:#fff;font-weight:700;font-size:20px;box-shadow:0 3px 10px rgba(0,0,0,.15);min-width:130px;text-align:center}}
.stat .label{{font-size:13px;font-weight:400;opacity:.9;margin-bottom:4px}}
.stat.total{{background:linear-gradient(135deg,#1565c0,#1976d2)}}
.stat.pass{{background:linear-gradient(135deg,#2e7d32,#43a047)}}
.stat.fail{{background:linear-gradient(135deg,#c62828,#e53935)}}
.stat.error{{background:linear-gradient(135deg,#e65100,#f57c00)}}
.progress{{height:8px;background:#e0e0e0;border-radius:4px;margin-bottom:25px;overflow:hidden}}
.progress .bar{{height:100%;background:linear-gradient(90deg,#2e7d32,#43a047);border-radius:4px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.08)}}
th{{background:#1a237e;color:#fff;padding:14px 18px;text-align:left;font-size:14px}}
td{{padding:12px 18px;border-bottom:1px solid #f0f0f0;font-size:14px}}
tr:last-child td{{border-bottom:none}}tr:hover{{background:#f8f9ff}}
.badge{{font-weight:700;padding:5px 14px;border-radius:20px;color:#fff;font-size:12px;text-transform:uppercase;letter-spacing:.5px}}
.badge.ok{{background:#2e7d32}}.badge.FAIL{{background:#c62828}}.badge.ERROR{{background:#e65100}}
.desc{{color:#666;font-size:13px}}.footer{{text-align:center;color:#aaa;margin-top:25px;font-size:13px}}
</style></head><body>
<div class="header"><h1>NouvelAir - Rapport de Tests</h1><p>Resultats des tests automatiques</p></div>
<div class="timestamp">Genere le {datetime.datetime.now().strftime("%d/%m/%Y a %H:%M:%S")}</div>
<div class="summary">
<div class="stat total"><div class="label">TOTAL</div>{len(parsed)}</div>
<div class="stat pass"><div class="label">PASS</div>{passed}</div>
<div class="stat fail"><div class="label">FAIL</div>{failed}</div>
<div class="stat error"><div class="label">ERROR</div>{errors}</div>
</div>
<div class="progress"><div class="bar" style="width:{passed*100//max(len(parsed),1)}%"></div></div>
<table><tr><th style="width:80px">Status</th><th>Module</th><th>Test</th><th>Description</th></tr>'''

for t in parsed:
    parts = t['name'].split('.')
    app = parts[0] if parts else ''
    cls = parts[-1] if parts else ''
    html += f'''<tr>
<td><span class="badge {t['status']}">{t['status']}</span></td>
<td>{app} <span style="color:#aaa">.{cls}</span></td>
<td><code>{t['test']}</code></td>
<td class="desc">{t['desc']}</td></tr>'''

html += '''</table><div class="footer">NouvelAir Test Suite &copy; 2026</div></body></html>'''

report_path = os.path.join(BASE, 'test_reports', 'report.html')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Parsed: {len(parsed)} tests | Pass: {passed} | Fail: {failed} | Error: {errors}')
print(f'Report: {report_path}')
if not parsed:
    print('Check test_reports/raw.txt for raw output')