path = 'tests/unit/test_models_bookings.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '        booking = BookingFactory()\n        assert booking.status == "pending"'
new = '        booking = BookingFactory(status="pending")\n        assert booking.status == "pending"'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK")
else:
    print("FAIL")
