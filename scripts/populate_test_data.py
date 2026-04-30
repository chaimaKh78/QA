"""
Script de population des données de test pour l'application NouvelAir.
Génère des vols, réservations et utilisateurs fictifs pour les tests.
"""

import os
import sys
import django
import random
from datetime import date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nouvelair.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.contrib.auth.models import User
from flights.models import Airport, Aircraft, Flight
from bookings.models import Booking, Passenger, Payment
from accounts.models import UserProfile
from destinations.models import Destination
from promotions.models import Promotion


def create_airports():
    """Crée les aéroports principaux."""
    airports_data = [
        ("TUN", "Aéroport International Tunis-Carthage", "Tunis", "Tunisie", 36.8510, 10.2272),
        ("CDG", "Aéroport Charles de Gaulle", "Paris", "France", 49.0097, 2.5479),
        ("ORY", "Aéroport d'Orly", "Paris", "France", 48.7262, 2.3649),
        ("MIR", "Aéroport International Habib-Bourguiba", "Monastir", "Tunisie", 35.7643, 10.7563),
        ("NBE", "Aéroport International Enfidha-Hammamet", "Enfidha", "Tunisie", 36.0664, 10.4367),
        ("DJE", "Aéroport International Djerba-Zarzis", "Djerba", "Tunisie", 33.8833, 10.7750),
        ("MUC", "Aéroport de Munich", "Munich", "Allemagne", 48.3537, 11.7750),
        ("FRA", "Aéroport de Francfort", "Francfort", "Allemagne", 50.0379, 8.5622),
        ("CMN", "Aéroport Mohammed V", "Casablanca", "Maroc", 33.3675, -7.5898),
        ("ALG", "Aéroport Houari-Boumediene", "Alger", "Algérie", 36.6940, 3.2154),
    ]
    for code, name, city, country, lat, lon in airports_data:
        Airport.objects.get_or_create(
            code=code,
            defaults={
                'name': name, 'city': city, 'country': country,
                'latitude': lat, 'longitude': lon
            }
        )
    print(f"{Airport.objects.count()} aéroports créés.")


def create_aircrafts():
    """Crée les aéronefs."""
    aircrafts_data = [
        ("Airbus A320-200", "TS-INA", 174, 150, 24),
        ("Airbus A321neo", "TS-INC", 220, 192, 28),
        ("Boeing 737-800", "TS-IND", 189, 165, 24),
    ]
    for model, reg, total, eco, biz in aircrafts_data:
        Aircraft.objects.get_or_create(
            registration=reg,
            defaults={
                'model_name': model, 'total_seats': total,
                'economy_seats': eco, 'business_seats': biz
            }
        )
    print(f"{Aircraft.objects.count()} aéronefs créés.")


def create_flights():
    """Génère des vols sur les 30 prochains jours."""
    routes = [
        ("TUN", "CDG"), ("TUN", "ORY"), ("TUN", "MUC"), ("TUN", "FRA"),
        ("TUN", "DJE"), ("TUN", "NBE"), ("TUN", "MIR"),
        ("MIR", "CDG"), ("MIR", "ORY"), ("MIR", "MUC"),
        ("NBE", "CDG"), ("NBE", "ORY"), ("NBE", "FRA"),
        ("DJE", "CDG"), ("DJE", "MUC"), ("DJE", "CMN"),
        ("TUN", "ALG"), ("TUN", "CMN"),
    ]

    aircrafts = list(Aircraft.objects.all())
    flight_counter = 100

    for origin_code, dest_code in routes:
        origin = Airport.objects.get(code=origin_code)
        dest = Airport.objects.get(code=dest_code)

        for day_offset in range(0, 30, 2):  # Vols tous les 2 jours
            departure = date.today() + timedelta(days=day_offset)
            # 1 à 3 vols par jour par route
            for hour in [7, 12, 18][:random.randint(1, 3)]:
                departure_time = departure.replace(hour=hour, minute=random.choice([0, 15, 30, 45]))
                duration_hours = random.uniform(1.5, 4.0)
                arrival_time = departure_time + timedelta(hours=duration_hours)

                aircraft = random.choice(aircrafts)
                base_eco = random.uniform(180, 600)
                base_biz = base_eco * random.uniform(2.2, 3.5)

                Flight.objects.get_or_create(
                    flight_number=f"BJ{flight_counter}",
                    defaults={
                        'origin': origin, 'destination': dest,
                        'aircraft': aircraft,
                        'departure_time': departure_time,
                        'arrival_time': arrival_time,
                        'base_price_economy': round(base_eco, 2),
                        'base_price_business': round(base_biz, 2),
                        'available_seats_economy': aircraft.economy_seats - random.randint(0, 50),
                        'available_seats_business': aircraft.business_seats - random.randint(0, 10),
                        'status': 'scheduled',
                    }
                )
                flight_counter += 1

    print(f"{Flight.objects.count()} vols créés.")


def create_destinations():
    """Crée les destinations touristiques."""
    destinations = [
        ("Djerba", "djerba", "L'île aux mille couleurs", "Djerba est une magnifique île tunisienne réputée pour ses plages de sable fin, ses villages traditionnels et son climat méditerranéen.", "beach", "DJE", 4.5, True),
        ("Sousse", "sousse", "Perle du Sahel", "Sousse allie patrimoine historique et stations balnéaires modernes. Sa médina est classée au patrimoine mondial de l'UNESCO.", "beach", "MIR", 4.3, True),
        ("Hammamet", "hammamet", "La Côte des Jasmins", "Hammamet est célèbre pour ses plages immaculées, sa citadelle historique et ses jardins fleuris.", "beach", "NBE", 4.2, True),
        ("Tunis", "tunis", "Capitale millénaire", "Tunis, la capitale, offre un mélange unique entre la médina historique et la ville moderne.", "culture", "TUN", 4.1, True),
        ("Paris", "paris", "La Ville Lumière", "Paris, destination emblématique, séduit par ses monuments, sa gastronomie et son art de vivre.", "urban", "CDG", 4.7, True),
        ("Munich", "munich", "Capitale bavaroise", "Munich combine tradition bavaroise, architecture remarquable et proximité des Alpes.", "culture", "MUC", 4.4, False),
        ("Sfax", "sfax", "Capitale du Sud", "Sfax est la deuxième ville de Tunisie, réputée pour son port de pêche et son artisanat.", "culture", None, 3.9, False),
        ("Tabarka", "tabarka", "La perle du Nord-Ouest", "Tabarka est un joyau naturel avec ses falaises spectaculaires, ses forêts et ses plages sauvages.", "nature", None, 4.0, False),
    ]

    for name, slug, short_desc, desc, cat, airport_code, rating, featured in destinations:
        airport = Airport.objects.filter(code=airport_code).first() if airport_code else None
        Destination.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name, 'short_description': short_desc,
                'description': desc, 'category': cat,
                'airport': airport, 'rating': rating,
                'is_featured': featured,
            }
        )
    print(f"{Destination.objects.count()} destinations créées.")


def create_promotions():
    """Crée des promotions d'exemple."""
    promotions = [
        ("BIENVENUE20", "Bienvenue -20%", "Obtenez 20% de réduction sur votre premier vol avec le code BIENVENUE20.", "percentage", 20, 30, 200),
        ("ETE30", "Spécial Été -30%", "Profitez de -30% sur tous les vols estivaux vers les destinations méditerranéennes.", "percentage", 30, 60, 500),
        ("WEEKEND", "Offre Week-end", "Tarifs spéciaux pour les séjours du week-end, départ vendredi retour dimanche.", "percentage", 15, 45, 300),
        ("VIP", "Surclassement VIP", "Surclassement gratuit en classe Affaires pour les réservations Économie supérieures à 500 TND.", "free_upgrade", 0, 90, 50),
    ]
    from django.utils import timezone
    for code, name, desc, ptype, discount, days, max_uses in promotions:
        Promotion.objects.get_or_create(
            code=code,
            defaults={
                'name': name, 'description': desc,
                'promo_type': ptype,
                'discount_percentage': discount,
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=days),
                'max_uses': max_uses,
            }
        )
    print(f"{Promotion.objects.count()} promotions créées.")


def create_test_users():
    """Crée des utilisateurs de test."""
    users = [
        ('admin', 'admin@nouvelair.com', 'Admin', 'NouvelAir', True),
        ('testuser', 'test@example.com', 'Test', 'User', False),
        ('voyageur', 'voyageur@example.com', 'Ahmed', 'Ben Mohamed', False),
        ('paul', 'paul@example.com', 'Paul', 'Dupont', False),
    ]
    for username, email, first, last, is_admin in users:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email, 'first_name': first,
                'last_name': last, 'is_staff': is_admin,
                'is_superuser': is_admin,
            }
        )
        if created:
            user.set_password('TestPass123!')
            user.save()
    print(f"{User.objects.count()} utilisateurs créés (mot de passe: TestPass123!).")


def main():
    print("=" * 50)
    print("NouvelAir - Peuplement des données de test")
    print("=" * 50)

    create_airports()
    create_aircrafts()
    create_flights()
    create_destinations()
    create_promotions()
    create_test_users()

    print("\n" + "=" * 50)
    print("Données de test créées avec succès !")
    print("=" * 50)


if __name__ == '__main__':
    main()
