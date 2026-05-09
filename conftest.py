# conftest.py
import os

# Allow Django database operations in async contexts (Playwright tests)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import pytest
import django
from django.conf import settings

# Ensure Django is set up
if not settings.configured:
    django.setup()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def db(db):
    """
    Override db fixture to populate airports before each test.
    """
    from tests.factories import AirportFactory
    from flights.models import Airport
    
    # Create airports with IATA codes used in tests if they don't exist
    airports_to_create = [
        {'code': 'TUN', 'name': 'Aéroport de Tunis', 'city': 'Tunis', 'country': 'Tunisia'},
        {'code': 'CDG', 'name': 'Aéroport de Paris Charles de Gaulle', 'city': 'Paris', 'country': 'France'},
        {'code': 'ORY', 'name': 'Aéroport de Paris Orly', 'city': 'Paris', 'country': 'France'},
        {'code': 'LHR', 'name': 'Aéroport de Londres Heathrow', 'city': 'London', 'country': 'United Kingdom'},
        {'code': 'MXP', 'name': 'Aéroport de Milan Malpensa', 'city': 'Milan', 'country': 'Italy'},
    ]
    
    for airport_data in airports_to_create:
        if not Airport.objects.filter(code=airport_data['code']).exists():
            AirportFactory(**airport_data)
    
    return db


@pytest.fixture(autouse=True)
def enable_db_for_all_tests(db):
    """Enable database access for all tests."""
    pass