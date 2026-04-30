import glob
for fpath in glob.glob('accounts/**/*.py', recursive=True):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'post_save' in content and ('create_user_profile' in content or 'UserProfile' in content):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'post_save' in line or 'create_user_profile' in line:
                start = max(0, i-1)
                end = min(len(lines), i+3)
                for j in range(start, end):
                    print(f"  {j+1} [{fpath}]: {lines[j]}")
                print()
