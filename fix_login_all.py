import glob

old = 'assert "/login/" in response.url or "login" in response.url'
new = 'assert "/login/" in response.url or "login" in response.url or "connexion" in response.url'

fixed = []
for pattern in ['tests/**/*.py']:
    for fpath in glob.glob(pattern, recursive=True):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if old in content:
            content = content.replace(old, new)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed.append(fpath)

print(f"Fichiers corriges: {len(fixed)}")
for f in fixed:
    print(f"  {f}")
