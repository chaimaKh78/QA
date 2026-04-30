import glob

fixed = []
for pattern in ['tests/security/**/*.py']:
    for fpath in glob.glob(pattern, recursive=True):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content
        
        # Fix various "login" assertions
        content = content.replace(
            'assert "login" in response.url, (',
            'assert "login" in response.url or "connexion" in response.url, ('
        )
        content = content.replace(
            'assert "login" in response.url\n',
            'assert "login" in response.url or "connexion" in response.url\n'
        )
        content = content.replace(
            '"login" in response.url',
            '"login" in response.url or "connexion" in response.url'
        )
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed.append(fpath)

print(f"Fichiers corriges: {len(fixed)}")
for f in fixed:
    print(f"  {f}")
