import os, glob

fixed_files = []
for pattern in ['tests/**/*.py']:
    for fpath in glob.glob(pattern, recursive=True):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'UserProfile.objects.create(user=' in content:
            content = content.replace(
                'UserProfile.objects.create(user=user)',
                'UserProfile.objects.get_or_create(user=user)[0]'
            )
            content = content.replace(
                'UserProfile.objects.create(user=',
                'UserProfile.objects.get_or_create(user='
            )
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_files.append(fpath)

print(f"Fichiers corriges: {len(fixed_files)}")
for f in fixed_files:
    print(f"  {f}")
