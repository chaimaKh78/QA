"""Test factories for NouvelAir project — matched to actual model fields."""

import uuid
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User


FRENCH_LOCALE = "fr_FR"


def french_city():
    from faker import Faker as RealFaker
    return RealFaker(FRENCH_LOCALE).city()


def french_first_name():
    from faker import Faker as RealFaker
    return RealFaker(FRENCH_LOCALE).first_name()


def french_last_name():
    from faker import Faker as RealFaker
    return RealFaker(FRENCH_LOCALE).last_name()


# ═══════════════════════════════════════════════════════════════════════
#  ACCOUNTS
# ═══════════════════════════════════════════════════════════════════════
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    skip_postgeneration_save = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.LazyFunction(french_first_name)
    last_name = factory.LazyFunction(french_last_name)
    password = factory.PostGenerationMethodCall("set_password", "TestPass123!")
    is_active = True


class UserProfileFactory(DjangoModelFactory):
    """Factory for the ``accounts.UserProfile`` model.
    
    Note: UserProfile is auto-created by a post_save signal on User.
    Use UserFactory instead of creating UserProfile directly in most tests.
    """

    class Meta:
        model = 'accounts.UserProfile'
        django_get_or_create = ('user',)

    user = factory.SubFactory('tests.factories.UserFactory')
    phone = factory.Faker('phone_number')
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    country = factory.Faker('country')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    nationality = factory.Faker('country')
    passport_number = factory.Faker('bothify', text='??######')
    gender = factory.Iterator(['M', 'F', 'O'])
    newsletter = False
class AirportFactory(DjangoModelFactory):
    """Factory for the ``flights.Airport`` model."""

    class Meta:
        model = 'flights.Airport'
        django_get_or_create = ('code',)

    code = factory.Sequence(lambda n: f"T{n:03d}")
    name = factory.Sequence(lambda n: f"Aeroport Test {n}")
    city = factory.Faker('city')
    country = factory.Faker('country')
    is_active = True
class AircraftFactory(DjangoModelFactory):
    class Meta:
        model = "flights.Aircraft"
        django_get_or_create = ("registration",)

    model_name = factory.Sequence(lambda n: f"Airbus A{n}00")
    registration = factory.Sequence(lambda n: f"TS-REG{n:04d}")
    total_seats = 180
    economy_seats = 150
    business_seats = 30
    is_active = True


class FlightFactory(DjangoModelFactory):
    class Meta:
        model = "flights.Flight"
        django_get_or_create = ("flight_number",)

    flight_number = factory.Sequence(lambda n: f"NA{n:04d}")
    origin = factory.SubFactory(AirportFactory, code=factory.Sequence(lambda n: f"DEP{n}"))
    destination = factory.SubFactory(AirportFactory, code=factory.Sequence(lambda n: f"ARR{n}"))
    aircraft = factory.SubFactory(AircraftFactory)
    departure_time = factory.Faker("date_time_between", start_date="+1d", end_date="+30d")
    arrival_time = factory.LazyAttribute(
        lambda o: o.departure_time + __import__("datetime").timedelta(hours=2)
    )
    duration = factory.LazyAttribute(lambda o: o.arrival_time - o.departure_time)
    status = "scheduled"
    base_price_economy = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    base_price_business = factory.LazyAttribute(lambda o: float(o.base_price_economy) * 2.5)
    available_seats_economy = 150
    available_seats_business = 30
    is_active = True


# ═══════════════════════════════════════════════════════════════════════
#  BOOKINGS
# ═══════════════════════════════════════════════════════════════════════
class BookingFactory(DjangoModelFactory):
    class Meta:
        model = "bookings.Booking"

    reference = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    contact_email = factory.Faker("email")
    contact_phone = factory.Faker("phone_number", locale=FRENCH_LOCALE)
    status = "pending"
    total_amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    special_requests = ""


class PassengerFactory(DjangoModelFactory):
    class Meta:
        model = "bookings.Passenger"

    booking = factory.SubFactory(BookingFactory)
    flight = factory.SubFactory(FlightFactory)
    first_name = factory.LazyFunction(french_first_name)
    last_name = factory.LazyFunction(french_last_name)
    title = "mr"
    date_of_birth = factory.Faker("date_of_birth", minimum_age=18, maximum_age=70)
    nationality = "Tunisienne"
    passport_number = factory.Faker("passport_number")
    passport_expiry = factory.LazyAttribute(
        lambda o: o.date_of_birth.replace(year=o.date_of_birth.year + 10) if o.date_of_birth else None
    )
    travel_class = "economy"
    seat_number = factory.Faker("bothify", text="??##")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    special_assistance = False
    meal_preference = "standard"


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = "bookings.Payment"

    booking = factory.SubFactory(BookingFactory)
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    method = "credit_card"
    status = "completed"
    transaction_id = factory.Faker("uuid4")


# ═══════════════════════════════════════════════════════════════════════
#  PROMOTIONS — fields matched to actual model
# ═══════════════════════════════════════════════════════════════════════
class PromotionFactory(DjangoModelFactory):
    """Factory for the ``promotions.Promotion`` model."""

    class Meta:
        model = 'promotions.Promotion'

    code = factory.Sequence(lambda n: f"PROMO{n:03d}")
    name = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=300)
    promo_type = factory.Iterator(['percentage', 'fixed', 'free_upgrade'])
    discount_percentage = factory.LazyFunction(lambda: round(__import__('random').uniform(5, 50), 2))
    discount_amount = factory.LazyFunction(
        lambda: __import__('decimal').Decimal(__import__('random').uniform(0, 100)).quantize(__import__('decimal').Decimal('0.01'))
    )
    start_date = factory.LazyFunction(
        lambda: __import__('django.utils.timezone').now() - __import__('datetime').timedelta(days=__import__('random').randint(1, 10))
    )
    end_date = factory.LazyFunction(
        lambda: __import__('django.utils.timezone').now() + __import__('datetime').timedelta(days=__import__('random').randint(10, 60))
    )
    max_uses = 100
    current_uses = 0
    min_purchase_amount = __import__('decimal').Decimal('0.00')
    is_active = True
    is_featured = False
class NewsletterSubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = "promotions.NewsletterSubscription"
        django_get_or_create = ("email",)

    email = factory.Faker("email")
    is_active = True
    subscribed_at = factory.Faker("date_time_this_year")
