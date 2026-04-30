import subprocess, sys, os

os.chdir(r"D:\NouvelairApp\nouvelair_project")
print("=" * 50)
print("  VERIFICATION COMPLETE DES TESTS NOUVELAIR")
print("=" * 50)
print()

print("[1/5] Verification collection des tests...")
r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "--ignore=tests/e2e", "--co", "-q"], capture_output=True, text=True)
print(r.stdout[-500:] if len(r.stdout) > 500 else r.stdout)
if r.stderr:
    print(r.stderr[-300:])
print()

print("[2/5] Execution complete de la suite...")
r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "--ignore=tests/e2e", "-v", "--tb=short"], capture_output=True, text=True)
lines = r.stdout.split("\n")
for line in lines:
    if any(k in line for k in ["PASSED", "FAILED", "ERROR", "SKIPPED", "XFAIL", "passed", "failed", "error", "skipped", "xfailed", "warnings", "==="]):
        print(line)
print()

print("[3/5] Resume:")
for line in lines:
    if "passed" in line and ("failed" in line or "==" in line):
        print("  " + line.strip())
        break
print()

modules = [
    ("Unitaires", "tests/unit/"),
    ("Integration", "tests/integration/"),
    ("API", "tests/api/"),
    ("Securite", "tests/security/"),
    ("Smoke & Regression", "tests/test_smoke.py", "tests/test_regression.py"),
]

print("[4/5] Tests par module:")
for mod in modules:
    name = mod[0]
    args = [sys.executable, "-m", "pytest"] + list(mod[1:]) + ["-v", "--tb=no"]
    r = subprocess.run(args, capture_output=True, text=True)
    summary = ""
    for line in r.stdout.split("\n"):
        if "passed" in line:
            summary = line.strip()
            break
    print(f"  {name}: {summary}")
print()

print("[5/5] Resultat attendu: 229 passed, 4 skipped, 1 xfailed")
print("=" * 50)
