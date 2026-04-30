path = 'tests/unit/test_models_flights.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        departure_date = (timezone.now() + timedelta(days=3)).date()
        FlightFactory(
            flight_number="BJ501",
            origin=origin,
            destination=destination,
            aircraft=aircraft,
            departure_time=timezone.now() + timedelta(days=3, hours=8),
            arrival_time=timezone.now() + timedelta(days=3, hours=11),
            status="scheduled",
            available_seats_economy=50,
            is_active=True,
        )
        results = Flight.search_flights("TUN", "CDG", departure_date, passengers=1)
        assert results.count() >= 1
        assert results.first().flight_number == "BJ501"'''

new = '''        departure_dt = timezone.now() + timedelta(days=3, hours=8)
        departure_date = departure_dt.date()
        FlightFactory(
            flight_number="BJ501",
            origin=origin,
            destination=destination,
            aircraft=aircraft,
            departure_time=departure_dt,
            arrival_time=departure_dt + timedelta(hours=3),
            status="scheduled",
            available_seats_economy=50,
            is_active=True,
        )
        results = Flight.search_flights("TUN", "CDG", departure_date, passengers=1)
        assert results.count() >= 1
        assert results.first().flight_number == "BJ501"'''

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK")
else:
    print("FAIL")
