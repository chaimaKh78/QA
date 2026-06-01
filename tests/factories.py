import random
from datetime import timedelta
from decimal import Decimal

import factory
from factory.django import DjangoModelFactory
from django.utils import timezone


class AirportFactory(DjangoModelFactory):
    class Meta:
        model = 'flights.Airport'
        django_get_or_create = ('code',)

    code = factory.Sequence(lambda n: 'T%03d' % n)
    name = factory.Sequence(lambda n: 'Aeroport Test %d' % n)
    city = factory.Faker('city')
    country = factory.Faker('country')
    is_active = True
    latitude = factory.LazyFunction(lambda: __import__("random").uniform(-90, 90))
    longitude = factory.LazyFunction(lambda: __import__("random").uniform(-180, 180))


class AircraftFactory(DjangoModelFactory):
    class Meta:
        model = 'flights.Aircraft'

    model_name = factory.Iterator(['Airbus A320', 'Airbus A321', 'Boeing 737-800'])
    registration = factory.Sequence(lambda n: 'TS-%c%03d' % (65 + n % 26, n))
    total_seats = factory.Iterator([150, 165, 180])
    economy_seats = factory.LazyAttribute(lambda o: int(o.total_seats * 0.8))
    business_seats = factory.LazyAttribute(lambda o: o.total_seats - o.economy_seats)
    is_active = True


class FlightFactory(DjangoModelFactory):
    class Meta:
        model = 'flights.Flight'
        django_get_or_create = ('flight_number',)

    flight_number = factory.Sequence(lambda n: 'BJ%04d' % n)
    origin = factory.SubFactory(AirportFactory)
    destination = factory.SubFactory(AirportFactory)
    aircraft = factory.SubFactory(AircraftFactory)
    departure_time = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=random.randint(1, 60), hours=random.randint(0, 23)))
    arrival_time = factory.LazyAttribute(
        lambda o: o.departure_time + timedelta(hours=random.randint(2, 6)))
    duration = factory.LazyAttribute(
        lambda o: int((o.arrival_time - o.departure_time).total_seconds() / 60))
    base_price_economy = factory.LazyFunction(
        lambda: Decimal(random.uniform(80, 500)).quantize(Decimal('0.01')))
    base_price_business = factory.LazyAttribute(
        lambda o: o.base_price_economy * Decimal('2.5'))
    available_seats_economy = factory.LazyAttribute(lambda o: o.aircraft.economy_seats)
    available_seats_business = factory.LazyAttribute(lambda o: o.aircraft.business_seats)
    base_price_economy = factory.LazyFunction(
        lambda: __import__("decimal").Decimal(__import__("random").uniform(100, 800)).quantize(__import__("decimal").Decimal("0.01")))
    base_price_business = factory.LazyFunction(
        lambda: __import__("decimal").Decimal(__import__("random").uniform(300, 2000)).quantize(__import__("decimal").Decimal("0.01")))
    available_seats_economy = 150
    available_seats_business = 20


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username', 'email')

    username = factory.Sequence(lambda n: 'testuser%d' % n)
    email = factory.Sequence(lambda n: 'user%d@test.com' % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'TestPass123!')
    is_active = True


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.UserProfile'
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    phone = factory.Faker('phone_number')
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    country = factory.Faker('country')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    nationality = factory.Faker('country')
    passport_number = factory.Sequence(lambda n: 'AB%06d' % n)
    gender = factory.Iterator(['M', 'F'])
    newsletter = False


class BookingFactory(DjangoModelFactory):
    class Meta:
        model = 'bookings.Booking'

    reference = factory.LazyFunction(lambda: __import__("uuid").uuid4())
    user = factory.SubFactory(UserFactory)
    contact_email = factory.LazyAttribute(lambda o: o.user.email)
    contact_phone = '+21612345678'
    status = factory.Iterator(['pending', 'confirmed', 'cancelled', 'completed', 'refunded'])
    total_amount = factory.LazyFunction(
        lambda: Decimal(random.uniform(100, 2000)).quantize(Decimal('0.01')))


class PassengerFactory(DjangoModelFactory):
    class Meta:
        model = 'bookings.Passenger'

    booking = factory.SubFactory(BookingFactory)
    flight = factory.SubFactory(FlightFactory)
    title = factory.Iterator(['mr', 'mme', 'mll', 'enf'])
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=2, maximum_age=65)
    nationality = factory.Faker('country')
    passport_number = factory.Sequence(lambda n: 'PP%06d' % n)
    passport_expiry = factory.LazyFunction(
        lambda: timezone.now().date() + timedelta(days=random.randint(180, 3650)))
    travel_class = factory.Iterator(['economy', 'business'])
    seat_number = factory.Sequence(lambda n: '%dA' % (n % 30 + 1))
    price = factory.LazyFunction(
        lambda: Decimal(random.uniform(80, 900)).quantize(Decimal('0.01')))


class PromotionFactory(DjangoModelFactory):
    class Meta:
        model = 'promotions.Promotion'

    code = factory.Sequence(lambda n: 'PROMO%d' % n)
    name = factory.Sequence(lambda n: 'Promotion %d' % n)
    description = factory.Faker('text', max_nb_chars=300)
    promo_type = factory.Iterator(['percentage', 'fixed', 'free_upgrade'])
    discount_percentage = factory.LazyFunction(lambda: round(random.uniform(5, 50), 2))
    discount_amount = factory.LazyFunction(
        lambda: Decimal(random.uniform(0, 100)).quantize(Decimal('0.01')))
    start_date = factory.LazyFunction(
        lambda: timezone.now() - timedelta(days=random.randint(1, 10)))
    end_date = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=random.randint(10, 60)))
    max_uses = 100
    current_uses = 0
    min_purchase_amount = Decimal('0.00')
    is_active = True
    is_featured = False