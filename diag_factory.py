# Check factories for UUID issue
import glob
for fpath in glob.glob('tests/**/factories.py', recursive=True) + glob.glob('**/factories.py'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'BookingFactory' in content or 'FlightFactory' in content:
        print(f"=== {fpath} ===")
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'BookingFactory' in line or 'FlightFactory' in line or 'class.*Factory' in line or 'flight' in line.lower() and 'uuid' in line.lower():
                start = max(0, i-1)
                end = min(len(lines), i+15)
                for j in range(start, end):
                    print(f"  {j+1}: {lines[j]}")
                print()
