"""
Tests API - Autocomplétion des aéroports (Jour 5).

Teste le endpoint GET /api/airports/autocomplete/?q=<query>
qui retourne une liste JSON d'aéroports correspondant à la recherche.

Couverture:
    - Requêtes valides et invalides
    - Structure de la réponse JSON
    - Filtrage par is_active
    - Tri et performance
"""

import time
import re
import pytest
from django.test import Client
from django.contrib.auth.models import User
from flights.models import Airport


# ── Helpers ───────────────────────────────────────────────────────────────────

def _create_airport(code, name, city, country, is_active=True):
    """Crée un aéroport de test avec les champs requis."""
    return Airport.objects.create(
        code=code,
        name=name,
        city=city,
        country=country,
        latitude="36.806500",
        longitude="10.181500",
        is_active=is_active,
    )


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.django_db
class TestAirportAutocompleteAPI:
    """Suite de tests pour l'endpoint d'autocomplétion des aéroports."""

    def setup_method(self):
        """Crée les aéroports de test avant chaque test."""
        self.client = Client()
        self.url = "/api/airports/autocomplete/"

        # Aéroports actifs
        _create_airport("TUN", "Aéroport Tunis-Carthage", "Tunis", "Tunisie")
        _create_airport("SFA", "Aéroport Sfax-Thyna", "Sfax", "Tunisie")
        _create_airport("MIR", "Aéroport Monastir Habib-Bourguiba", "Monastir", "Tunisie")
        _create_airport("TAB", "Aéroport Tabarka-Aïn Draham", "Tabarka", "Tunisie")
        _create_airport("TOE", "Aéroport Tozeur-Nefta", "Tozeur", "Tunisie")

        # Aéroport inactif (ne doit PAS apparaître dans les résultats)
        _create_airport("TBJ", "Aéroport Djerba-Zarzis", "Djerba", "Tunisie", is_active=False)

    # ─── Test 1: Requête valide avec query 'TUN' ──────────────────────────

    def test_autocomplete_valid_query(self):
        """GET avec q='TUN' → 200, JSON list avec au moins 1 résultat."""
        response = self.client.get(self.url, {"q": "TUN"})

        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Vérifier que l'aéroport Tunis-Carthage est dans les résultats
        codes = [airport["code"] for airport in data]
        assert "TUN" in codes

    # ─── Test 2: Requête avec query 'TU' → résultats multiples ───────────

    def test_autocomplete_multiple_results(self):
        """q='TU' → retourne plusieurs aéroports dont le code ou ville contient 'TU'."""
        response = self.client.get(self.url, {"q": "TU"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # 'TU' matche le code TUN et potentiellement d'autres (ville contenant 'Tu')
        # Au minimum Tunis (TUN) doit être présent
        codes = [airport["code"] for airport in data]
        assert len(data) >= 1
        assert "TUN" in codes

    # ─── Test 3: Query d'un seul caractère ────────────────────────────────

    def test_autocomplete_single_char(self):
        """q='T' → résultats possibles ou liste vide."""
        response = self.client.get(self.url, {"q": "T"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Tous les aéroports actifs ont un code commençant par 'T',
        # donc on s'attend à des résultats (limités à 10 par la vue)
        if len(data) > 0:
            # Vérifier que chaque résultat contient bien 'T' dans code, name ou city
            for airport in data:
                matches = (
                    "T" in airport.get("code", "").upper()
                    or "T" in airport.get("name", "").upper()
                    or "T" in airport.get("city", "").upper()
                )
                assert matches, (
                    f"L'aéroport {airport.get('code')} ne correspond pas à 'T'"
                )

    # ─── Test 4: Query vide → liste vide ──────────────────────────────────

    def test_autocomplete_empty_query(self):
        """q='' → retourne une liste vide."""
        response = self.client.get(self.url, {"q": ""})

        assert response.status_code == 200
        data = response.json()
        assert data == []

    # ─── Test 5: Query sans résultats ─────────────────────────────────────

    def test_autocomplete_no_results(self):
        """q='XYZ' → liste vide (aucun aéroport ne correspond)."""
        response = self.client.get(self.url, {"q": "XYZ"})

        assert response.status_code == 200
        data = response.json()
        assert data == []

    # ─── Test 6: Structure de la réponse JSON ─────────────────────────────

    def test_autocomplete_response_structure(self):
        """Chaque aéroport dans la réponse possède les clés: id, code, name, city, country."""
        response = self.client.get(self.url, {"q": "TUN"})

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

        expected_keys = {"id", "code", "name", "city", "country"}
        for airport in data:
            assert isinstance(airport, dict), f"Résultat non-dict: {type(airport)}"
            missing_keys = expected_keys - set(airport.keys())
            assert not missing_keys, (
                f"Clés manquantes dans la réponse: {missing_keys}. "
                f"Clés trouvées: {set(airport.keys())}"
            )

    # ─── Test 7: Format du code IATA ──────────────────────────────────────

    def test_autocomplete_code_format(self):
        """Le champ 'code' doit être exactement 3 lettres majuscules."""
        response = self.client.get(self.url, {"q": "T"})

        assert response.status_code == 200
        data = response.json()

        iata_pattern = re.compile(r"^[A-Z]{3}$")
        for airport in data:
            code = airport.get("code", "")
            assert iata_pattern.match(code), (
                f"Code IATA invalide: '{code}'. Attendu: 3 lettres majuscules."
            )

    # ─── Test 8: Seuls les aéroports actifs ───────────────────────────────

    def test_autocomplete_active_airports_only(self):
        """Seuls les aéroports avec is_active=True sont retournés."""
        response = self.client.get(self.url, {"q": "T"})

        assert response.status_code == 200
        data = response.json()

        # L'aéroport inactif (TBJ - Djerba) ne doit PAS apparaître
        codes = [airport["code"] for airport in data]
        assert "TBJ" not in codes, (
            "L'aéroport inactif TBJ ne devrait pas apparaître dans les résultats."
        )

        # Vérifier explicitement que tous les codes retournés correspondent
        # à des aéroports actifs en base
        for airport in data:
            db_airport = Airport.objects.get(pk=airport["id"])
            assert db_airport.is_active, (
                f"L'aéroport {db_airport.code} est inactif mais apparaît dans les résultats."
            )

    # ─── Test 9: Résultats triés par ville ────────────────────────────────

    def test_autocomplete_ordered_by_city(self):
        """Les résultats sont triés alphabétiquement par ville."""
        response = self.client.get(self.url, {"q": "T"})

        assert response.status_code == 200
        data = response.json()

        if len(data) >= 2:
            cities = [airport["city"] for airport in data]
            sorted_cities = sorted(cities)
            assert cities == sorted_cities, (
                f"Les résultats ne sont pas triés par ville. "
                f"Ordre actuel: {cities}, Attendu: {sorted_cities}"
            )

    # ─── Test 10: Temps de réponse < 500ms ────────────────────────────────

    def test_autocomplete_response_time(self):
        """L'endpoint répond en moins de 500ms."""
        start_time = time.time()
        response = self.client.get(self.url, {"q": "TUN"})
        elapsed_ms = (time.time() - start_time) * 1000

        assert response.status_code == 200
        assert elapsed_ms < 500, (
            f"Temps de réponse trop lent: {elapsed_ms:.1f}ms (limite: 500ms)"
        )
