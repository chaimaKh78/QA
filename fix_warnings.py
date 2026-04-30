# fix_warnings.py
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# 1. Find settings.py to read STATIC_URL and STATICFILES_DIRS
settings_candidates = []
for root, dirs, files in os.walk(BASE):
    if 'settings.py' in files and 'templates' not in root:
        settings_candidates.append(os.path.join(root, 'settings.py'))

static_dirs = set()
static_dirs.add(os.path.join(BASE, 'static'))

for sp in settings_candidates:
    with open(sp, 'r', encoding='utf-8') as f:
        content = f.read()
    # Parse STATICFILES_DIRS
    matches = re.findall(r"'([^']*)'\s*\)", content)
    for m in matches:
        d = os.path.normpath(os.path.join(os.path.dirname(sp), m))
        if 'static' in m.lower():
            static_dirs.add(d)

# Also check templates dirs for static references
for root, dirs, files in os.walk(BASE):
    if 'base.html' in files:
        with open(os.path.join(root, 'base.html'), 'r', encoding='utf-8') as f:
            bcontent = f.read()
        # Find {% static %} tags to understand the path
        print(f"base.html found in: {root}")
        break

# 2. Create static files
for d in static_dirs:
    try:
        os.makedirs(os.path.join(d, 'css'), exist_ok=True)
        os.makedirs(os.path.join(d, 'js'), exist_ok=True)
        os.makedirs(os.path.join(d, 'img'), exist_ok=True)
        
        css = os.path.join(d, 'css', 'style.css')
        js = os.path.join(d, 'js', 'main.js')
        ico = os.path.join(d, 'favicon.ico')
        
        for f in [css, js]:
            if not os.path.exists(f):
                open(f, 'w').close()
                print(f'Created: {f}')
            else:
                print(f'Exists: {f}')
        
        if not os.path.exists(ico):
            open(ico, 'wb').write(bytes([0,0,1,0,1,0,1,1,0,0,1,0,24,0,48,0,0,0,22,0,0,0,
                40,0,0,0,1,0,0,0,2,0,0,0,1,0,32,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
            print(f'Created: {ico}')
        else:
            print(f'Exists: {ico}')
    except Exception as e:
        print(f'Error with {d}: {e}')

# 3. Suppress Broken pipe logs
for sp in settings_candidates:
    with open(sp, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'LOGGING' not in content:
        content += '''

# Suppress noisy logs during testing
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"quiet": {"class": "logging.NullHandler"}},
    "loggers": {
        "django.server": {"handlers": ["quiet"], "level": "ERROR"},
    },
}
'''
        with open(sp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Added LOGGING to: {sp}')

print('\nDone!')