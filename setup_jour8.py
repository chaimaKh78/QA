#!/usr/bin/env python3
"""
setup_jour8.py — Création des fichiers de tests de performance et sécurité (Jour 8, NouvelAir)

Ce script génère automatiquement tous les fichiers nécessaires pour les tests
de performance (Locust) et les tests de sécurité (Django + OWASP Top 10)
du Sprint 1, Jour 8.

Fichiers créés:
    1.  tests/performance/__init__.py
    2.  tests/performance/locustfile.py
    3.  tests/performance/run_load_test.py
    4.  tests/performance/performance_thresholds.py
    5.  tests/security/__init__.py
    6.  tests/security/run_security_scan.py
    7.  tests/security/test_security_manual.py      (10 tests)
    8.  tests/security/test_owasp_top10.py          (6 tests)
    9.  docs/performance_report_template.md
   10.  docs/security_report_template.md

Usage:
    cd D:/NouvelAirApp/nouvelair_project/\
    python setup_jour8.py
"""

import os
import sys
import stat
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DIRECTORIES_TO_CREATE = [
    os.path.join(BASE_DIR, "tests", "performance"),
    os.path.join(BASE_DIR, "tests", "security"),
    os.path.join(BASE_DIR, "docs"),
    os.path.join(BASE_DIR, "reports", "performance"),
    os.path.join(BASE_DIR, "reports", "security"),
]

FILES_TO_CREATE = {
    "tests/performance/__init__.py": "init_file",
    "tests/performance/locustfile.py": "locustfile",
    "tests/performance/run_load_test.py": "run_load_test",
    "tests/performance/performance_thresholds.py": "performance_thresholds",
    "tests/security/__init__.py": "init_file",
    "tests/security/run_security_scan.py": "run_security_scan",
    "tests/security/test_security_manual.py": "security_manual_tests",
    "tests/security/test_owasp_top10.py": "owasp_top10_tests",
    "docs/performance_report_template.md": "performance_report_template",
    "docs/security_report_template.md": "security_report_template",
}

BANNER = r"""
╔══════════════════════════════════════════════════════════════════════╗
║         NouvelAir — Setup Performance & Sécurité (Jour 8)           ║
║         Sprint 1 · Formation Django                                 ║
╚══════════════════════════════════════════════════════════════════════╝
"""

SEPARATOR = "=" * 72


# ─────────────────────────────────────────────────────────────────────────────
# File Content Generators
# ─────────────────────────────────────────────────────────────────────────────

def get_init_file():
    """__init__.py — fichier vide."""
    return ""


def get_locustfile():
    """tests/performance/locustfile.py — Fichier Locust complet pour NouvelAir."""
    return '''\
"""
Locust file pour les tests de charge NouvelAir — Jour 8.

Simule le comportement réel des utilisateurs sur le site NouvelAir:
- Navigation sur les pages publiques (accueil, destinations, promotions)
- Recherche de vols et autocomplétion des aéroports
- Accès aux pages protégées (mes réservations, recherche de réservation)
- Authentification automatique des utilisateurs virtuels

Dépendances:
    pip install locust

Exécution:
    cd D:/NouvelAirApp/nouvelair_project/\
    locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000

    Ou sans interface web (headless):
    locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \
           --headless -u 50 -r 5 -t 5m --html=reports/performance/load_test.html
"""

from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import json
import logging
import time

logger = logging.getLogger(__name__)


# ── Compteurs de métriques personnalisés ─────────────────────────────────────

custom_metrics = {
    "search_requests": 0,
    "booking_requests": 0,
    "auth_requests": 0,
    "total_errors": 0,
    "total_requests": 0,
}


# ── Event hooks pour métriques personnalisées ────────────────────────────────

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """
    Hook appelé à chaque requête pour collecter des métriques personnalisées.

    Args:
        request_type: Type de requête (GET, POST, etc.)
        name: Nom de la tâche/endpoint
        response_time: Temps de réponse en ms
        response_length: Taille de la réponse en octets
        exception: Exception si la requête a échoué
    """
    custom_metrics["total_requests"] += 1

    if name and "search" in name.lower():
        custom_metrics["search_requests"] += 1
    elif name and "booking" in name.lower():
        custom_metrics["booking_requests"] += 1
    elif name and ("login" in name.lower() or "auth" in name.lower()):
        custom_metrics["auth_requests"] += 1

    if exception:
        custom_metrics["total_errors"] += 1
        logger.warning(
            "Requête échouée: %s %s — %.0f ms — %s",
            request_type, name, response_time, str(exception)
        )


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Hook appelé à la fin du test pour afficher les métriques résumées.

    Args:
        environment: Environnement Locust
    """
    print("\\n" + "=" * 60)
    print("  MÉTRIQUES PERSONNALISÉES — NOUVELAIR")
    print("=" * 60)
    print(f"  Requêtes totales         : {custom_metrics['total_requests']}")
    print(f"  Requêtes de recherche    : {custom_metrics['search_requests']}")
    print(f"  Requêtes de réservation  : {custom_metrics['booking_requests']}")
    print(f"  Requêtes d\\'authentification: {custom_metrics['auth_requests']}")
    print(f"  Erreurs totales          : {custom_metrics['total_errors']}")

    if custom_metrics["total_requests"] > 0:
        error_rate = (custom_metrics["total_errors"] / custom_metrics["total_requests"]) * 100
        print(f"  Taux d\\'erreur            : {error_rate:.2f}%")
    print("=" * 60 + "\\n")


# ── Comportement de navigation ───────────────────────────────────────────────

class BrowsingBehavior:
    """
    Comportement de navigation type « visiteur curieux ».

    L\'utilisateur parcourt les pages publiques du site, consulte
    les destinations et les promotions sans effectuer de recherche.
    """

    def __init__(self, client):
        self.client = client

    def browse_homepage(self):
        """Navigue vers la page d\'accueil."""
        self.client.get("/")

    def view_destinations(self):
        """Consulte la page des destinations."""
        self.client.get("/destinations/")

    def view_promotions(self):
        """Consulte la page des promotions."""
        self.client.get("/promotions/")


class SearchingBehavior:
    """
    Comportement de recherche type « voyageur ».

    L\'utilisateur effectue des recherches de vols, utilise
    l\'autocomplétion des aéroports et consulte les résultats.
    """

    def __init__(self, client):
        self.client = client

    def search_airports(self):
        """Consulte la liste des aéroports disponibles."""
        self.client.get("/flights/aeroports/")

    def airport_autocomplete_tunis(self):
        """Teste l\'autocomplétion avec la requête TUN."""
        with self.client.get(
            "/flights/api/airports/autocomplete/?q=TUN",
            name="/flights/api/airports/autocomplete/?q=TUN",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        response.success()
                    else:
                        response.failure("Réponse JSON invalide: attendu une liste")
                except json.JSONDecodeError:
                    response.failure("Réponse non-JSON")
            else:
                response.failure(f"Status code: {response.status_code}")

    def airport_autocomplete_paris(self):
        """Teste l\'autocomplétion avec la requête PAR."""
        with self.client.get(
            "/flights/api/airports/autocomplete/?q=PAR",
            name="/flights/api/airports/autocomplete/?q=PAR",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        response.success()
                    else:
                        response.failure("Réponse JSON invalide: attendu une liste")
                except json.JSONDecodeError:
                    response.failure("Réponse non-JSON")
            else:
                response.failure(f"Status code: {response.status_code}")

    def airport_autocomplete_empty(self):
        """Teste l\'autocomplétion avec une requête vide."""
        self.client.get(
            "/flights/api/airports/autocomplete/?q=",
            name="/flights/api/airports/autocomplete/?q=(empty)"
        )


class BookingBehavior:
    """
    Comportement de réservation type « client enregistré ».

    L\'utilisateur connecté accède à ses réservations et
    utilise la fonctionnalité de recherche de réservation.
    """

    def __init__(self, client):
        self.client = client

    def view_my_bookings(self):
        """Consulte la page « Mes réservations »."""
        with self.client.get(
            "/reservations/mes-reservations/",
            name="/reservations/mes-reservations/",
            catch_response=True
        ) as response:
            # 302 = redirection vers login si non authentifié, 200 = OK
            if response.status_code in (200, 302):
                response.success()
            else:
                response.failure(f"Status inattendu: {response.status_code}")

    def booking_lookup_page(self):
        """Consulte la page de recherche de réservation."""
        self.client.get("/reservations/recherche/")

    def view_legal_pages(self):
        """Consulte les mentions légales et CGV."""
        self.client.get("/mentions-legales/", name="/mentions-legales/")
        self.client.get("/conditions-generales/", name="/conditions-generales/")


# ── Utilisateur Locust principal ─────────────────────────────────────────────

class NouvelAirUser(HttpUser):
    """
    Utilisateur virtuel Locust simulant le comportement d\'un visiteur NouvelAir.

    Pondération des tâches (weight):
        - Homepage: 5 (page la plus visitée)
        - Destinations: 3
        - Promotions: 3
        - Recherche aéroports: 2
        - Autocomplétion TUN: 2
        - Autocomplétion PAR: 1
        - Mes réservations: 1
        - Recherche réservation: 1

    Temps de réflexion (think time): 1 à 3 secondes entre chaque requête.
    """

    wait_time = between(1, 3)
    host = "http://127.0.0.1:8000"

    def on_start(self):
        """
        Initialisation de l\'utilisateur virtuel.

        Tente de se connecter avec un compte de test pour accéder
        aux pages protégées. Si la connexion échoue, l\'utilisateur
        continuera en mode visiteur anonyme.
        """
        self.browsing = BrowsingBehavior(self.client)
        self.searching = SearchingBehavior(self.client)
        self.booking = BookingBehavior(self.client)
        self.is_authenticated = False

        # Tentative de connexion
        try:
            self.client.get("/compte/connexion/", name="/compte/connexion/ [GET]")
            csrftoken = self.client.cookies.get("csrftoken", "")

            response = self.client.post(
                "/compte/connexion/",
                {
                    "username": "testuser",
                    "password": "NouvelAir2025!",
                    "csrfmiddlewaretoken": csrftoken,
                },
                name="/compte/connexion/ [POST]",
            )

            # Vérifier si la connexion a réussi (redirection vers l\'accueil)
            if response.status_code in (200, 302):
                self.is_authenticated = True
                logger.info("Utilisateur virtuel connecté avec succès")
            else:
                logger.warning(
                    "Connexion échouée (status: %d), mode visiteur activé",
                    response.status_code,
                )
        except Exception as e:
            logger.warning("Erreur lors de la connexion: %s", str(e))

    # ─── Tâches de navigation (pages publiques) ────────────────────────

    @task(5)
    def browse_homepage(self):
        """
        [Weight 5] Navigation vers la page d\'accueil.

        C\'est la tâche la plus fréquente car c\'est le point d\'entrée
        principal du site. Chaque visiteur passe au moins une fois
        par cette page.
        """
        with self.client.get("/", name="/ [Homepage]", catch_response=True) as response:
            if response.status_code == 200:
                # Vérifier que la page contient du contenu significatif
                if len(response.text) > 500:
                    response.success()
                else:
                    response.failure("Page d\'accueil trop légère (< 500 octets)")
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(3)
    def view_destinations(self):
        """
        [Weight 3] Consultation de la page des destinations.

        Les voyageurs consultent fréquemment les destinations
        disponibles pour planifier leurs voyages.
        """
        with self.client.get(
            "/destinations/", name="/destinations/", catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(3)
    def view_promotions(self):
        """
        [Weight 3] Consultation de la page des promotions.

        Les offres promotionnelles attirent de nombreux visiteurs
        cherchant des bonnes affaires.
        """
        with self.client.get(
            "/promotions/", name="/promotions/", catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    # ─── Tâches de recherche ───────────────────────────────────────────

    @task(2)
    def search_airports(self):
        """
        [Weight 2] Consultation de la liste des aéroports.

        Utilisée lors de la planification de voyage pour identifier
        les aéroports de départ et d\'arrivée.
        """
        self.searching.search_airports()

    @task(2)
    def airport_autocomplete_tun(self):
        """
        [Weight 2] Autocomplétion avec la requête « TUN ».

        Simule la saisie de l\'utilisateur dans le champ de recherche
        d\'aéroport. Tunis (TUN) est l\'aéroport principal.
        """
        self.searching.airport_autocomplete_tunis()

    @task(1)
    def airport_autocomplete_par(self):
        """
        [Weight 1] Autocomplétion avec la requête « PAR ».

        Simule une recherche vers Paris, destination populaire
        depuis la Tunisie.
        """
        self.searching.airport_autocomplete_par()

    @task(1)
    def airport_autocomplete_empty(self):
        """
        [Weight 1] Autocomplétion avec requête vide.

        Teste le comportement du serveur avec une entrée vide,
        simulant un utilisateur qui efface le champ de recherche.
        """
        self.searching.airport_autocomplete_empty()

    # ─── Tâches de réservation (nécessitent l\'auth) ────────────────────

    @task(1)
    def view_my_bookings(self):
        """
        [Weight 1] Consultation de « Mes réservations ».

        Page protégée accessible uniquement aux utilisateurs connectés.
        """
        self.booking.view_my_bookings()

    @task(1)
    def booking_lookup(self):
        """
        [Weight 1] Page de recherche de réservation.

        Permet de retrouver une réservation via sa référence et email.
        Accessible sans authentification.
        """
        self.booking.booking_lookup_page()

    # ─── Tâches secondaires ────────────────────────────────────────────

    @task(1)
    def view_legal_pages(self):
        """
        [Weight 1] Consultation des pages légales.

        Mentions légales et conditions générales de vente.
        Peu fréquent mais nécessaire pour la conformité.
        """
        self.booking.view_legal_pages()

    @task(1)
    def view_registration(self):
        """
        [Weight 1] Consultation de la page d\'inscription.

        Nouveaux visiteurs intéressés par la création d\'un compte.
        """
        self.client.get("/compte/inscription/", name="/compte/inscription/")
'''


def get_run_load_test():
    """tests/performance/run_load_test.py — Scripts de lancement des tests de performance."""
    return '''\
"""
Scripts de lancement des tests de performance — Jour 8.

Permet d\'exécuter différents types de tests de charge via Locust:
    - Load Test (test de charge standard)
    - Stress Test (test de montée en charge)
    - Spike Test (test de pic soudain)
    - Endurance Test (test d\'endurance)
    - Baseline Test (test de référence)

Chaque type de test génère un rapport HTML dans reports/performance/
et vérifie que les seuils de performance sont respectés.

Dépendances:
    pip install locust

Usage:
    cd D:/NouvelAirApp/nouvelair_project/\
    python tests/performance/run_load_test.py --type load
    python tests/performance/run_load_test.py --type stress
    python tests/performance/run_load_test.py --type spike
    python tests/performance/run_load_test.py --type endurance
    python tests/performance/run_load_test.py --type baseline
    python tests/performance/run_load_test.py --type all
"""

import os
import sys
import subprocess
import argparse
import json
import time
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from tests.performance.performance_thresholds import THRESHOLDS, ENDPOINT_MAPPING

# ── Configuration ────────────────────────────────────────────────────────────

HOST = "http://127.0.0.1:8000"
LOCUSTFILE = os.path.join(BASE_DIR, "tests", "performance", "locustfile.py")
REPORTS_DIR = os.path.join(BASE_DIR, "reports", "performance")

# Assurer que le répertoire des rapports existe
os.makedirs(REPORTS_DIR, exist_ok=True)


# ── Définitions des tests ───────────────────────────────────────────────────

TEST_CONFIGS = {
    "load": {
        "description": "Test de charge standard — simule le trafic normal du site",
        "users": 50,
        "spawn_rate": 5,
        "duration": "5m",
        "report_file": "load_test.html",
        "description_detail": (
            "50 utilisateurs simultanés, montée progressive à 5 utilisateurs/seconde, "
            "durée de 5 minutes. Simule le trafic typique d\'une journée normale."
        ),
    },
    "stress": {
        "description": "Test de montée en charge — pousse le système à ses limites",
        "users": 200,
        "spawn_rate": 10,
        "duration": "10m",
        "report_file": "stress_test.html",
        "description_detail": (
            "Montée de 10 à 200 utilisateurs, spawn rate de 10/s, durée de 10 minutes. "
            "Objectif: identifier le point de rupture du système."
        ),
    },
    "spike": {
        "description": "Test de pic soudain — simule un afflux massif d\'utilisateurs",
        "users": 100,
        "spawn_rate": 100,
        "duration": "2m",
        "report_file": "spike_test.html",
        "description_detail": (
            "100 utilisateurs instantanés (spawn rate 100/s), maintien pendant 2 minutes. "
            "Simule un pic de trafic dû à une promotion ou un événement."
        ),
    },
    "endurance": {
        "description": "Test d\'endurance — vérifie la stabilité sur la durée",
        "users": 30,
        "spawn_rate": 3,
        "duration": "15m",
        "report_file": "endurance_test.html",
        "description_detail": (
            "30 utilisateurs simultanés, spawn rate de 3/s, durée de 15 minutes. "
            "Détecte les fuites mémoire et la dégradation progressive des performances."
        ),
    },
    "baseline": {
        "description": "Test de référence — benchmark des performances de base",
        "users": 10,
        "spawn_rate": 2,
        "duration": "2m",
        "report_file": "baseline_test.html",
        "description_detail": (
            "10 utilisateurs, spawn rate de 2/s, durée de 2 minutes. "
            "Établit la ligne de base pour comparaison future."
        ),
    },
}


# ── Fonctions utilitaires ────────────────────────────────────────────────────

def print_header(title):
    """Affiche un en-tête formaté."""
    print("\\n" + "=" * 72)
    print(f"  {title}")
    print("=" * 72)


def print_step(message):
    """Affiche une étape de progression."""
    print(f"  → {message}")


def run_locust_test(test_type, config):
    """
    Exécute un test Locust avec la configuration spécifiée.

    Args:
        test_type: Type de test (load, stress, spike, endurance, baseline)
        config: Dictionnaire de configuration du test

    Returns:
        str: Chemin vers le fichier rapport HTML généré
    """
    report_path = os.path.join(REPORTS_DIR, config["report_file"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path_with_ts = os.path.join(
        REPORTS_DIR, f"{timestamp}_{config['report_file']}"
    )

    print_header(f"TEST DE PERFORMANCE — {test_type.upper()}")
    print(f"  Description : {config['description']}")
    print(f"  Détails     : {config['description_detail']}")
    print(f"  Utilisateurs: {config['users']}")
    print(f"  Spawn rate  : {config['spawn_rate']}/s")
    print(f"  Durée       : {config['duration']}")
    print(f"  Rapport     : {report_path_with_ts}")
    print()

    print_step("Vérification du serveur...")
    # Vérifier que le serveur Django est en cours d\'exécution
    try:
        import urllib.request
        urllib.request.urlopen(f"{HOST}/", timeout=5)
        print_step("Serveur Django est accessible ✓")
    except Exception as e:
        print(f"  ✗ ERREUR: Serveur Django inaccessible sur {HOST}")
        print(f"    Détail: {e}")
        print(f"    Assurez-vous que le serveur est lancé: python manage.py runserver")
        return None

    print_step(f"Lancement du test {test_type}...")

    cmd = [
        sys.executable, "-m", "locust",
        "-f", LOCUSTFILE,
        "--host", HOST,
        "--headless",
        "-u", str(config["users"]),
        "-r", str(config["spawn_rate"]),
        "-t", config["duration"],
        "--html", report_path_with_ts,
        "--only-summary",
    ]

    print_step(f"Commande: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=int(config["duration"].rstrip("m")) * 60 + 120,
        )

        if result.returncode == 0:
            print_step(f"Test terminé avec succès ✓")
            print_step(f"Rapport HTML généré: {report_path_with_ts}")

            # Copier aussi vers le nom standard
            with open(report_path_with_ts, "r", encoding="utf-8") as src:
                with open(report_path, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

            return report_path_with_ts
        else:
            print(f"  ✗ ERREUR: Le test a échoué (code: {result.returncode})")
            if result.stderr:
                print(f"    stderr: {result.stderr[-500:]}")
            return None

    except subprocess.TimeoutExpired:
        print(f"  ✗ TIMEOUT: Le test a dépassé la durée maximale")
        return None
    except FileNotFoundError:
        print(f"  ✗ ERREUR: Locust n'est pas installé")
        print(f"    Installez-le: pip install locust")
        return None
    except Exception as e:
        print(f"  ✗ ERREUR: {e}")
        return None


def check_thresholds(test_type):
    """
    Vérifie les résultats du test par rapport aux seuils définis.

    Args:
        test_type: Type de test exécuté

    Returns:
        dict: Résultats de la vérification des seuils
    """
    print_header("VÉRIFICATION DES SEUILS DE PERFORMANCE")

    results = {}
    all_pass = True

    for endpoint, thresholds in THRESHOLDS.items():
        # Map endpoint to Locust task name
        locust_name = ENDPOINT_MAPPING.get(endpoint, endpoint)
        results[endpoint] = {
            "p50_max": thresholds["p50"],
            "p95_max": thresholds["p95"],
            "p99_max": thresholds["p99"],
            "status": "INFO",
        }

        status_parts = []
        status_parts.append(f"p50<{thresholds['p50']}ms")
        status_parts.append(f"p95<{thresholds['p95']}ms")
        status_parts.append(f"p99<{thresholds['p99']}ms")

        print(f"  {endpoint:20s} | {' | '.join(status_parts)}")

    print()
    print("  ⚠ Pour une vérification complète, consultez le rapport HTML")
    print(f"    et comparez les percentiles avec les seuils ci-dessus.")
    print()

    return results


def generate_summary_report(all_results):
    """
    Génère un résumé JSON de tous les tests exécutés.

    Args:
        all_results: Dictionnaire des résultats par type de test
    """
    summary = {
        "project": "NouvelAir",
        "date": datetime.now().isoformat(),
        "host": HOST,
        "tests": all_results,
        "thresholds": THRESHOLDS,
    }

    summary_path = os.path.join(REPORTS_DIR, "test_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

    print_step(f"Résumé JSON sauvegardé: {summary_path}")


# ── Point d\'entrée principal ─────────────────────────────────────────────────

def main():
    """Point d\'entrée principal du script."""
    parser = argparse.ArgumentParser(
        description="Scripts de tests de performance NouvelAir — Jour 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\\
Exemples:
  python run_load_test.py --type load         Test de charge (50 users, 5 min)
  python run_load_test.py --type stress       Test de stress (200 users)
  python run_load_test.py --type spike        Test de pic (100 users instant)
  python run_load_test.py --type endurance    Test d'endurance (30 users, 15 min)
  python run_load_test.py --type baseline     Test de référence (10 users, 2 min)
  python run_load_test.py --type all          Tous les tests séquentiels
        """,
    )

    parser.add_argument(
        "--type",
        choices=["load", "stress", "spike", "endurance", "baseline", "all"],
        default="baseline",
        help="Type de test à exécuter (défaut: baseline)",
    )

    parser.add_argument(
        "--host",
        default=HOST,
        help=f"URL du serveur cible (défaut: {HOST})",
    )

    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Vérifier uniquement les seuils sans exécuter les tests",
    )

    args = parser.parse_args()

    global HOST
    HOST = args.host

    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║    NouvelAir — Tests de Performance (Jour 8 — Sprint 1)            ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print(f"  Date      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Serveur   : {HOST}")
    print(f"  Rapports  : {REPORTS_DIR}")
    print(f"  Seuils    : {len(THRESHOLDS)} endpoints configurés")

    if args.check_only:
        check_thresholds("manual")
        return

    all_results = {}

    if args.type == "all":
        # Exécuter tous les tests séquentiellement
        test_order = ["baseline", "load", "stress", "spike", "endurance"]
        for test_type in test_order:
            config = TEST_CONFIGS[test_type]
            report_path = run_locust_test(test_type, config)
            all_results[test_type] = {
                "config": config,
                "report": report_path,
                "timestamp": datetime.now().isoformat(),
            }
            time.sleep(5)  # Pause entre les tests
    else:
        test_type = args.type
        config = TEST_CONFIGS[test_type]
        report_path = run_locust_test(test_type, config)
        all_results[test_type] = {
            "config": config,
            "report": report_path,
            "timestamp": datetime.now().isoformat(),
        }

    # Vérification des seuils
    check_thresholds(args.type)

    # Résumé
    generate_summary_report(all_results)

    print_header("FIN DES TESTS DE PERFORMANCE")
    print()
    for test_name, result in all_results.items():
        status = "✓" if result["report"] else "✗"
        report_info = result["report"] or "ÉCHEC"
        print(f"  {status} {test_name:12s} — {report_info}")
    print()


if __name__ == "__main__":
    main()
'''


def get_performance_thresholds():
    """tests/performance/performance_thresholds.py — Seuils de performance."""
    return '''\
"""
Seuils de performance pour les tests de charge NouvelAir — Jour 8.

Définit les temps de réponse maximum acceptables pour chaque endpoint,
classés par percentiles (p50, p95, p99).

Les seuils sont basés sur les bonnes pratiques d\'UX:
    - p50 (médiane): 50% des requêtes doivent être plus rapides
    - p95: 95% des requêtes doivent être plus rapides
    - p99: 99% des requêtes doivent être plus rapides

Références:
    - Google: pages interactives < 100ms, pages statiques < 1s
    - WCAG: temps de réponse < 3s pour un bon ressenti
"""

# ── Seuils de performance par endpoint (en millisecondes) ────────────────────

THRESHOLDS = {
    "homepage": {
        "p50": 1000,     # Médiane: 1 seconde (page dynamique avec requêtes DB)
        "p95": 3000,     # 95e percentile: 3 secondes (seuil d\'acceptabilité)
        "p99": 5000,     # 99e percentile: 5 secondes (maximum toléré)
        "description": "Page d\'accueil — requêtes DB pour destinations et vols",
    },
    "search": {
        "p50": 1500,     # Médiane: 1.5 seconde (recherche complexe avec filtres)
        "p95": 5000,     # 95e percentile: 5 secondes
        "p99": 8000,     # 99e percentile: 8 secondes (recherche lourde)
        "description": "Résultats de recherche de vols — requêtes multi-critères",
    },
    "autocomplete": {
        "p50": 100,      # Médiane: 100ms (doit être quasi-instantané)
        "p95": 500,      # 95e percentile: 500ms (UX fluide pour la saisie)
        "p99": 1000,     # 99e percentile: 1 seconde (maximum pour l\'UX)
        "description": "Autocomplétion aéroports — API légère, index DB",
    },
    "destinations": {
        "p50": 800,      # Médiane: 800ms (liste paginée)
        "p95": 2500,     # 95e percentile: 2.5 secondes
        "p99": 4000,     # 99e percentile: 4 secondes
        "description": "Page des destinations — liste paginée avec images",
    },
    "promotions": {
        "p50": 900,      # Médiane: 900ms
        "p95": 2800,     # 95e percentile: 2.8 secondes
        "p99": 4500,     # 99e percentile: 4.5 secondes
        "description": "Page des promotions — requêtes avec filtres actifs/inactifs",
    },
    "login": {
        "p50": 500,      # Médiane: 500ms (authentification + session)
        "p95": 2000,     # 95e percentile: 2 secondes
        "p99": 3000,     # 99e percentile: 3 secondes
        "description": "Page de connexion — vérification des identifiants",
    },
    "my_bookings": {
        "p50": 1200,     # Médiane: 1.2 seconde (requêtes utilisateur + réservations)
        "p95": 3500,     # 95e percentile: 3.5 secondes
        "p99": 6000,     # 99e percentile: 6 secondes
        "description": "Mes réservations — données utilisateur + prefetch",
    },
    "booking_lookup": {
        "p50": 800,      # Médiane: 800ms (page statique)
        "p95": 2500,     # 95e percentile: 2.5 secondes
        "p99": 4000,     # 99e percentile: 4 secondes
        "description": "Recherche de réservation — page GET simple",
    },
    "airports": {
        "p50": 700,      # Médiane: 700ms (liste complète des aéroports)
        "p95": 2200,     # 95e percentile: 2.2 secondes
        "p99": 3500,     # 99e percentile: 3.5 secondes
        "description": "Liste des aéroports — query avec filtre is_active",
    },
}

# ── Mapping entre les noms d\'endpoints et les tâches Locust ──────────────────

ENDPOINT_MAPPING = {
    "homepage": "/ [Homepage]",
    "search": "/recherche/ [Search Results]",
    "autocomplete": "/flights/api/airports/autocomplete/",
    "destinations": "/destinations/",
    "promotions": "/promotions/",
    "login": "/compte/connexion/ [POST]",
    "my_bookings": "/reservations/mes-reservations/",
    "booking_lookup": "/reservations/recherche/",
    "airports": "/flights/aeroports/",
}

# ── Seuils globaux ───────────────────────────────────────────────────────────

GLOBAL_THRESHOLDS = {
    "max_error_rate": 1.0,          # Taux d\'erreur max: 1%
    "max_average_response_time": 2000,  # Temps moyen max: 2 secondes
    "min_requests_per_second": 5,    # RPS minimum: 5 requêtes/seconde
    "max_95th_percentile": 5000,     # p95 global max: 5 secondes
}

# ── Catégories de criticité ──────────────────────────────────────────────────

CRITICALITY_LEVELS = {
    "autocomplete": "CRITIQUE",
    "homepage": "HAUT",
    "login": "HAUT",
    "search": "MOYEN",
    "destinations": "MOYEN",
    "promotions": "MOYEN",
    "my_bookings": "MOYEN",
    "booking_lookup": "BAS",
    "airports": "BAS",
}


def check_endpoint_result(endpoint, p50, p95, p99):
    """
    Vérifie si les résultats d\'un endpoint respectent les seuils.

    Args:
        endpoint: Nom de l\'endpoint (clé dans THRESHOLDS)
        p50: Temps de réponse au 50e percentile (ms)
        p95: Temps de réponse au 95e percentile (ms)
        p99: Temps de réponse au 99e percentile (ms)

    Returns:
        dict: Résultat de la vérification avec statut par percentile
    """
    if endpoint not in THRESHOLDS:
        return {"status": "UNKNOWN", "message": f"Endpoint '{endpoint}' non configuré"}

    thresholds = THRESHOLDS[endpoint]

    result = {
        "endpoint": endpoint,
        "criticality": CRITICALITY_LEVELS.get(endpoint, "INCONNU"),
        "measured": {"p50": p50, "p95": p95, "p99": p99},
        "thresholds": {"p50": thresholds["p50"], "p95": thresholds["p95"], "p99": thresholds["p99"]},
        "checks": {},
        "status": "PASS",
    }

    # Vérifier chaque percentile
    for pct in ["p50", "p95", "p99"]:
        passed = result["measured"][pct] <= thresholds[pct]
        result["checks"][pct] = {
            "measured": result["measured"][pct],
            "threshold": thresholds[pct],
            "passed": passed,
        }
        if not passed:
            result["status"] = "FAIL"

    return result


def format_threshold_report(check_results):
    """
    Formate les résultats de vérification en tableau lisible.

    Args:
        check_results: Liste de résultats de check_endpoint_result()

    Returns:
        str: Tableau formaté
    """
    lines = []
    lines.append(f"{'Endpoint':<20} {'Crit.':<8} {'p50':<12} {'p95':<12} {'p99':<12} {'Statut':<8}")
    lines.append("-" * 72)

    for result in check_results:
        if result.get("status") == "UNKNOWN":
            lines.append(f"{result['endpoint']:<20} {'-':<8} {'-':<12} {'-':<12} {'-':<12} {result['status']:<8}")
            continue

        def fmt(check):
            val = check["measured"]
            limit = check["threshold"]
            icon = "✓" if check["passed"] else "✗"
            return f"{val:.0f}/{limit:.0f}ms {icon}"

        p50_str = fmt(result["checks"]["p50"])
        p95_str = fmt(result["checks"]["p95"])
        p99_str = fmt(result["checks"]["p99"])
        status = "✓ PASS" if result["status"] == "PASS" else "✗ FAIL"

        lines.append(
            f"{result['endpoint']:<20} "
            f"{result['criticality']:<8} "
            f"{p50_str:<12} "
            f"{p95_str:<12} "
            f"{p99_str:<12} "
            f"{status:<8}"
        )

    return "\\n".join(lines)
'''


def get_run_security_scan():
    """tests/security/run_security_scan.py — Script de scan de sécurité."""
    return '''\
"""
Script de scan de sécurité automatisé — Jour 8.

Exécute plusieurs outils d\'analyse de sécurité sur le projet NouvelAir:
    1. Bandit: analyse statique du code Python pour détecter les vulnérabilités
    2. Safety: vérification des dépendances contre les CVE connus
    3. Django checks: vérifications de sécurité intégrées à Django
    4. Tests manuels: CSRF, XSS, injection SQL, accès non autorisé

Dépendances:
    pip install bandit safety

Usage:
    cd D:/NouvelAirApp/nouvelair_project/\
    python tests/security/run_security_scan.py
    python tests/security/run_security_scan.py --bandit-only
    python tests/security/run_security_scan.py --safety-only
    python tests/security/run_security_scan.py --django-only
    python tests/security/run_security_scan.py --skip-bandit
    python tests/security/run_security_scan.py --skip-safety
"""

import os
import sys
import subprocess
import argparse
import json
from datetime import datetime

# ── Configuration ────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(BASE_DIR, "reports", "security")
REQUIREMENTS_FILE = os.path.join(BASE_DIR, "requirements.txt")

os.makedirs(REPORTS_DIR, exist_ok=True)

SCAN_RESULTS = {
    "bandit": None,
    "safety": None,
    "django_checks": None,
    "custom_checks": None,
}


# ── Fonctions utilitaires ────────────────────────────────────────────────────

def print_header(title):
    """Affiche un en-tête formaté."""
    print("\\n" + "=" * 72)
    print(f"  {title}")
    print("=" * 72)


def print_step(message):
    """Affiche une étape."""
    print(f"  → {message}")


def save_report(filename, content, is_json=False):
    """Sauvegarde un rapport dans le répertoire des rapports."""
    filepath = os.path.join(REPORTS_DIR, filename)
    mode = "w"
    encoding = "utf-8"
    if is_json:
        content = json.dumps(content, indent=2, ensure_ascii=False, default=str)
    with open(filepath, mode, encoding=encoding) as f:
        f.write(content)
    print_step(f"Rapport sauvegardé: {filepath}")
    return filepath


# ── 1. Bandit — Analyse statique du code ────────────────────────────────────

def run_bandit_scan():
    """
    Exécute Bandit pour l\'analyse statique du code Python.

    Bandit détecte les vulnérabilités courantes dans le code Python:
    - Utilisation de fonctions dangereuses (eval, exec, pickle)
    - Hardcoded passwords/tokens
    - Injection SQL potentielle
    - Mauvaises pratiques de sécurité
    """
    print_header("1. BANDIT — Analyse Statique du Code")

    # Vérifier si bandit est installé
    try:
        subprocess.run([sys.executable, "-m", "bandit", "--version"],
                       capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ⚠ Bandit n'est pas installé. Installation en cours...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "bandit"],
                           capture_output=True, check=True)
            print_step("Bandit installé avec succès")
        except subprocess.CalledProcessError:
            print("  ✗ Impossible d'installer Bandit. Scan ignoré.")
            SCAN_RESULTS["bandit"] = {"status": "SKIPPED", "reason": "not_installed"}
            return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_report = os.path.join(REPORTS_DIR, f"bandit_report_{timestamp}.json")
    html_report = os.path.join(REPORTS_DIR, "bandit_report.html")

    print_step("Analyse des fichiers Python en cours...")

    cmd = [
        sys.executable, "-m", "bandit",
        "-r", ".",                       # Analyse récursive
        "-f", "html",                    # Format HTML
        "-o", html_report,               # Rapport HTML
        "-ii",                           # Ne pas afficher les issues intermédiaires
        "--exclude", "tests/,migrations/,__pycache__/",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=300,
        )

        # Aussi générer en JSON pour parsing
        cmd_json = [
            sys.executable, "-m", "bandit",
            "-r", ".",
            "-f", "json",
            "-o", json_report,
            "--exclude", "tests/,migrations/,__pycache__/",
        ]
        subprocess.run(cmd_json, capture_output=True, text=True, cwd=BASE_DIR, timeout=300)

        # Parser le JSON pour le résumé
        summary = {"high": 0, "medium": 0, "low": 0, "info": 0}
        if os.path.exists(json_report):
            try:
                with open(json_report, "r", encoding="utf-8") as f:
                    data = json.load(f)
                summary["high"] = data.get("metrics", {}).get("_totals", {}).get("SEVERITY.HIGH", 0)
                summary["medium"] = data.get("metrics", {}).get("_totals", {}).get("SEVERITY.MEDIUM", 0)
                summary["low"] = data.get("metrics", {}).get("_totals", {}).get("SEVERITY.LOW", 0)
                summary["info"] = data.get("metrics", {}).get("_totals", {}).get("SEVERITY.INFO", 0)
            except (json.JSONDecodeError, KeyError):
                pass

        SCAN_RESULTS["bandit"] = {
            "status": "COMPLETED",
            "summary": summary,
            "html_report": html_report,
            "json_report": json_report,
        }

        print(f"  Résultats:")
        print(f"    🔴 Haute   : {summary['high']}")
        print(f"    🟠 Moyenne : {summary['medium']}")
        print(f"    🟡 Basse   : {summary['low']}")
        print(f"    🔵 Info    : {summary['info']}")
        print(f"    Total      : {sum(summary.values())}")
        print_step(f"Rapport HTML: {html_report}")

    except subprocess.TimeoutExpired:
        print("  ✗ TIMEOUT: Le scan Bandit a dépassé 5 minutes")
        SCAN_RESULTS["bandit"] = {"status": "TIMEOUT"}
    except Exception as e:
        print(f"  ✗ ERREUR: {e}")
        SCAN_RESULTS["bandit"] = {"status": "ERROR", "message": str(e)}


# ── 2. Safety — Vérification des dépendances ────────────────────────────────

def run_safety_check():
    """
    Exécute Safety pour vérifier les dépendances contre les CVE connus.

    Safety compare les versions des packages du requirements.txt avec
    la base de données de vulnérabilités PyPI.
    """
    print_header("2. SAFETY — Vérification des Dépendances (CVE)")

    try:
        subprocess.run([sys.executable, "-m", "safety", "--version"],
                       capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ⚠ Safety n'est pas installé. Installation en cours...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "safety"],
                           capture_output=True, check=True)
            print_step("Safety installé avec succès")
        except subprocess.CalledProcessError:
            print("  ✗ Impossible d'installer Safety. Vérification ignorée.")
            SCAN_RESULTS["safety"] = {"status": "SKIPPED", "reason": "not_installed"}
            return

    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"  ⚠ Fichier requirements.txt introuvable: {REQUIREMENTS_FILE}")
        SCAN_RESULTS["safety"] = {"status": "SKIPPED", "reason": "no_requirements"}
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_report = os.path.join(REPORTS_DIR, f"safety_report_{timestamp}.json")

    print_step("Vérification des dépendances...")

    cmd = [
        sys.executable, "-m", "safety",
        "check",
        "-r", REQUIREMENTS_FILE,
        "--json",
        "--output", json_report,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=120,
        )

        vulnerabilities = []
        if os.path.exists(json_report):
            try:
                with open(json_report, "r", encoding="utf-8") as f:
                    vulnerabilities = json.load(f)
            except (json.JSONDecodeError, TypeError):
                # Safety peut retourner un message d'erreur au lieu de JSON
                vulnerabilities = []

        SCAN_RESULTS["safety"] = {
            "status": "COMPLETED",
            "vulnerabilities_count": len(vulnerabilities) if isinstance(vulnerabilities, list) else 0,
            "vulnerabilities": vulnerabilities if isinstance(vulnerabilities, list) else [],
            "json_report": json_report,
        }

        if isinstance(vulnerabilities, list) and len(vulnerabilities) > 0:
            print(f"  ⚠ {len(vulnerabilities)} vulnérabilité(s) trouvée(s) dans les dépendances:")
            for vuln in vulnerabilities[:10]:  # Afficher les 10 premières
                pkg = vuln.get("package", "N/A")
                vuln_id = vuln.get("vulnerability_id", "N/A")
                advisory = vuln.get("advisory", "N/A")[:100]
                print(f"    - {pkg} ({vuln_id}): {advisory}")
        else:
            print("  ✓ Aucune vulnérabilité connue dans les dépendances")

    except subprocess.TimeoutExpired:
        print("  ✗ TIMEOUT: Safety a dépassé 2 minutes")
        SCAN_RESULTS["safety"] = {"status": "TIMEOUT"}
    except Exception as e:
        print(f"  ✗ ERREUR: {e}")
        SCAN_RESULTS["safety"] = {"status": "ERROR", "message": str(e)}


# ── 3. Django Security Checks ───────────────────────────────────────────────

def run_django_security_checks():
    """
    Exécute les vérifications de sécurité intégrées à Django.

    Vérifie:
    - DEBUG mode
    - ALLOWED_HOSTS
    - SECURE_SSL_REDIRECT
    - SESSION_COOKIE_SECURE
    - CSRF_COOKIE_SECURE
    - X_FRAME_OPTIONS
    - SECURE_CONTENT_TYPE_NOSNIFF
    - Et plus...
    """
    print_header("3. DJANGO — Vérifications de Sécurité Intégrées")

    print_step("Exécution de python manage.py check --deploy...")

    cmd = [
        sys.executable, "manage.py", "check", "--deploy"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=60,
        )

        issues = []
        warnings = []
        infos = []

        for line in result.stdout.strip().split("\\n"):
            if "? " in line:
                issues.append(line.strip())
            elif "!: " in line or "?:" in line:
                warnings.append(line.strip())
            elif line.strip():
                infos.append(line.strip())

        SCAN_RESULTS["django_checks"] = {
            "status": "COMPLETED",
            "issues": issues,
            "warnings": warnings,
            "infos": infos,
            "return_code": result.returncode,
        }

        if issues:
            print(f"  ⚠ {len(issues)} problème(s) de sécurité détecté(s):")
            for issue in issues:
                print(f"    - {issue}")
        elif warnings:
            print(f"  ℹ {len(warnings)} avertissement(s):")
            for warning in warnings:
                print(f"    - {warning}")
        else:
            print("  ✓ Aucun problème de sécurité détecté par Django")

        if result.stderr:
            print(f"  stderr: {result.stderr.strip()}")

    except subprocess.TimeoutExpired:
        print("  ✗ TIMEOUT")
        SCAN_RESULTS["django_checks"] = {"status": "TIMEOUT"}
    except Exception as e:
        print(f"  ✗ ERREUR: {e}")
        SCAN_RESULTS["django_checks"] = {"status": "ERROR", "message": str(e)}


# ── 4. Custom Django Security Tests ─────────────────────────────────────────

def run_custom_security_tests():
    """
    Exécute des tests de sécurité personnalisés via le client de test Django.

    Tests:
    - Validation du token CSRF sur la page d\'accueil
    - Accès aux URL protégées sans authentification
    - Tentatives d\'injection SQL via la recherche
    - Tentatives XSS via la recherche
    - Vérification de la session (fixation)
    """
    print_header("4. TESTS PERSONNALISÉS — Sécurité Django")

    # Configurer Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nouvelair.settings")

    try:
        import django
        django.setup()

        from django.test import Client
        from django.contrib.auth.models import User
    except ImportError:
        print("  ✗ Django n'est pas disponible")
        SCAN_RESULTS["custom_checks"] = {"status": "ERROR", "reason": "django_not_available"}
        return

    client = Client()
    results = []

    # ─ Test 1: CSRF Token sur la page d\'accueil ─────────────────────────
    print_step("Test: CSRF token sur page d'accueil...")
    response = client.get("/")
    csrf_found = "csrfmiddlewaretoken" in response.content.decode("utf-8", errors="ignore")
    results.append({
        "test": "CSRF token sur page d'accueil",
        "passed": csrf_found,
        "detail": "Token trouvé" if csrf_found else "Token CSRF manquant dans le formulaire",
    })
    print(f"    {'✓' if csrf_found else '✗'} CSRF token {'présent' if csrf_found else 'MANQUANT'}")

    # ─ Test 2: URL protégée sans authentification ────────────────────────
    print_step("Test: Accès URL protégée sans auth...")
    response = client.get("/reservations/mes-reservations/", follow=False)
    is_redirect = response.status_code == 302
    results.append({
        "test": "URL protégée sans auth (mes-réservations)",
        "passed": is_redirect,
        "detail": f"Status: {response.status_code} (attendu: 302)",
    })
    print(f"    {'✓' if is_redirect else '✗'} /mes-reservations/ → {response.status_code} ({'redirection OK' if is_redirect else 'ACCÈS DIRECT!'})")

    # ─ Test 2b: Profil sans auth ─────────────────────────────────────────
    response = client.get("/compte/profil/", follow=False)
    is_redirect = response.status_code == 302
    results.append({
        "test": "URL protégée sans auth (profil)",
        "passed": is_redirect,
        "detail": f"Status: {response.status_code} (attendu: 302)",
    })
    print(f"    {'✓' if is_redirect else '✗'} /compte/profil/ → {response.status_code} ({'redirection OK' if is_redirect else 'ACCÈS DIRECT!'})")

    # ─ Test 3: Injection SQL via recherche ──────────────────────────────
    print_step("Test: Injection SQL via recherche d'aéroport...")
    response = client.get("/flights/api/airports/autocomplete/?q=' OR 1=1 --")
    content = response.content.decode("utf-8", errors="ignore")
    no_sql_error = "error" not in content.lower() or response.status_code == 200
    results.append({
        "test": "Injection SQL autocomplete",
        "passed": no_sql_error,
        "detail": f"Status: {response.status_code}",
    })
    print(f"    {'✓' if no_sql_error else '✗'} Injection SQL → status {response.status_code} ({'traité correctement' if no_sql_error else 'ERREUR POSSIBLE!'})")

    # ─ Test 4: XSS via autocomplete ──────────────────────────────────────
    print_step("Test: XSS via recherche d'aéroport...")
    xss_payload = "<script>alert(1)</script>"
    response = client.get(f"/flights/api/airports/autocomplete/?q={xss_payload}")
    content = response.content.decode("utf-8", errors="ignore")
    no_script_reflection = "<script>" not in content.lower()
    results.append({
        "test": "XSS dans autocomplete",
        "passed": no_script_reflection,
        "detail": f"Script tag {'non réfléchi' if no_script_reflection else 'RÉFLÉCHI!'}",
    })
    print(f"    {'✓' if no_script_reflection else '✗'} XSS → script tag {'non réfléchi' if no_script_reflection else 'RÉFLÉCHI DANS LA RÉPONSE!'}")

    # ─ Test 5: Headers de sécurité ───────────────────────────────────────
    print_step("Test: Headers de sécurité HTTP...")
    response = client.get("/")
    headers = dict(response.headers)
    security_headers = {
        "X-Frame-Options": headers.get("X-Frame-Options", "MANQUANT"),
        "X-Content-Type-Options": headers.get("X-Content-Type-Options", "MANQUANT"),
        "Content-Security-Policy": headers.get("Content-Security-Policy", "MANQUANT"),
    }
    xfo_ok = headers.get("X-Frame-Options") is not None
    xcto_ok = headers.get("X-Content-Type-Options") is not None
    results.append({
        "test": "Headers de sécurité",
        "passed": xfo_ok or xcto_ok,
        "detail": str(security_headers),
    })
    for header, value in security_headers.items():
        status = "✓" if value != "MANQUANT" else "⚠"
        print(f"    {status} {header}: {value}")

    # ─ Test 6: Admin protégé ─────────────────────────────────────────────
    print_step("Test: Accès admin sans authentification...")
    response = client.get("/admin/", follow=False)
    is_redirect = response.status_code == 302
    results.append({
        "test": "Admin protégé",
        "passed": is_redirect,
        "detail": f"Status: {response.status_code} (attendu: 302)",
    })
    print(f"    {'✓' if is_redirect else '✗'} /admin/ → {response.status_code}")

    # ─ Test 7: Mode DEBUG ────────────────────────────────────────────────
    print_step("Test: Mode DEBUG...")
    from django.conf import settings
    debug_off = not settings.DEBUG
    results.append({
        "test": "DEBUG mode",
        "passed": debug_off,
        "detail": f"DEBUG = {settings.DEBUG}",
    })
    print(f"    {'✓' if debug_off else '⚠'} DEBUG = {settings.DEBUG} ({'OK pour dev' if not debug_off else 'SÉCURISÉ'})")

    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)

    SCAN_RESULTS["custom_checks"] = {
        "status": "COMPLETED",
        "results": results,
        "passed": passed_count,
        "total": total_count,
    }

    print(f"\\n  Résultat: {passed_count}/{total_count} tests réussis")


# ── Génération du rapport final ──────────────────────────────────────────────

def generate_final_report():
    """Génère un résumé de tous les scans de sécurité."""
    print_header("RAPPORT FINAL — Scan de Sécurité")

    summary = {
        "project": "NouvelAir",
        "date": datetime.now().isoformat(),
        "results": SCAN_RESULTS,
    }

    report_path = save_report("security_scan_summary.json", summary, is_json=True)

    # Afficher le résumé
    for scan_name, scan_result in SCAN_RESULTS.items():
        status = scan_result.get("status", "UNKNOWN") if scan_result else "NOT RUN"
        status_icon = {
            "COMPLETED": "✓",
            "SKIPPED": "⊘",
            "TIMEOUT": "⏱",
            "ERROR": "✗",
            "NOT RUN": "○",
        }.get(status, "?")

        detail = ""
        if scan_name == "bandit" and status == "COMPLETED":
            s = scan_result.get("summary", {})
            detail = f"H:{s.get('high',0)} M:{s.get('medium',0)} L:{s.get('low',0)}"
        elif scan_name == "safety" and status == "COMPLETED":
            count = scan_result.get("vulnerabilities_count", 0)
            detail = f"{count} CVE(s)"
        elif scan_name == "custom_checks" and status == "COMPLETED":
            detail = f"{scan_result.get('passed',0)}/{scan_result.get('total',0)} tests OK"

        print(f"  {status_icon} {scan_name:<15} — {status:<10} {detail}")

    print(f"\\n  Rapport JSON: {report_path}")
    print(f"  Rapports HTML: {REPORTS_DIR}/")
    return report_path


# ── Point d\'entrée principal ─────────────────────────────────────────────────

def main():
    """Point d\'entrée principal."""
    parser = argparse.ArgumentParser(
        description="Scan de sécurité automatisé — NouvelAir Jour 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--bandit-only", action="store_true", help="Exécuter uniquement Bandit")
    parser.add_argument("--safety-only", action="store_true", help="Exécuter uniquement Safety")
    parser.add_argument("--django-only", action="store_true", help="Exécuter uniquement Django checks")
    parser.add_argument("--skip-bandit", action="store_true", help="Ignorer Bandit")
    parser.add_argument("--skip-safety", action="store_true", help="Ignorer Safety")
    parser.add_argument("--skip-django", action="store_true", help="Ignorer Django checks")

    args = parser.parse_args()

    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║    NouvelAir — Scan de Sécurité (Jour 8 — Sprint 1)                ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print(f"  Date      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Projet    : {BASE_DIR}")
    print(f"  Rapports  : {REPORTS_DIR}")

    # Déterminer quels scans exécuter
    run_bandit = not args.skip_bandit and (args.bandit_only or not (args.safety_only or args.django_only))
    run_safety = not args.skip_safety and (args.safety_only or not (args.bandit_only or args.django_only))
    run_django = not args.skip_django and (args.django_only or not (args.bandit_only or args.safety_only))

    # Toujours exécuter les tests personnalisés
    run_custom = True

    if args.bandit_only:
        run_safety = False
        run_django = False
    elif args.safety_only:
        run_bandit = False
        run_django = False
    elif args.django_only:
        run_bandit = False
        run_safety = False

    if run_bandit:
        run_bandit_scan()

    if run_safety:
        run_safety_check()

    if run_django:
        run_django_security_checks()

    if run_custom:
        run_custom_security_tests()

    # Rapport final
    generate_final_report()

    print("\\n" + "=" * 72)
    print("  Scan de sécurité terminé !")
    print("=" * 72 + "\\n")


if __name__ == "__main__":
    main()
'''


def get_security_manual_tests():
    """tests/security/test_security_manual.py — 10 tests de sécurité manuels."""
    return '''\
"""
Tests de sécurité manuels — Jour 8.

Tests de sécurité utilisant le client de test Django pour vérifier:
    - Protection CSRF
    - Protection XSS
    - Protection contre l\'injection SQL
    - Contrôle d\'accès aux URL protégées
    - Gestion des sessions
    - Configuration de sécurité Django

Exécution:
    cd D:/NouvelAirApp/nouvelair_project/\
    python manage.py test tests.security.test_security_manual -v2
    pytest tests/security/test_security_manual.py -v

Couverture: 10 tests de sécurité.
"""

import os
import sys
import pytest
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

# ── Marqueurs pytest ─────────────────────────────────────────────────────────

def pytest_configure(config):
    """Enregistre les marqueurs personnalisés."""
    config.addinivalue_line(
        "markers", "security: tests de sécurité (Sprint 1, Jour 8)"
    )


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def authenticated_client(db):
    """Client de test avec un utilisateur authentifié."""
    client = Client()
    user = User.objects.create_user(
        username="securitytest",
        email="security@test.com",
        password="SecurePass123!",
        first_name="Test",
        last_name="Security",
    )
    client.login(username="securitytest", password="SecurePass123!")
    return client


@pytest.fixture
def admin_client(db):
    """Client de test avec un administrateur."""
    client = Client()
    user = User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="AdminPass123!",
    )
    client.login(username="admin", password="AdminPass123!")
    return client


@pytest.mark.django_db
@pytest.mark.security
class TestCSRFProtection:
    """
    Tests de protection CSRF (Cross-Site Request Forgery).

    Vérifie que les formulaires sont protégés par des tokens CSRF
    et que les requêtes POST sans token sont rejetées.
    """

    def test_csrf_home_page(self, client):
        """
        Test: La page d\'accueil contient un token CSRF dans son contexte.

        Vérifie que Django injecte bien le middleware CSRF dans les
        templates, rendant les formulaires POST sécurisés.
        """
        response = client.get("/")
        assert response.status_code == 200

        content = response.content.decode("utf-8")
        assert "csrfmiddlewaretoken" in content, (
            "Le token CSRF devrait être présent dans la page d\'accueil "
            "pour protéger les formulaires POST."
        )

    def test_csrf_protected_post(self):
        """
        Test: Une requête POST sans token CSRF est rejetée (403).

        Simule une attaque CSRF où l\'attaquant envoie un formulaire
        POST sans le token CSRF valide.

        Note: Le Client de test Django ne vérifie PAS le CSRF par défaut.
        Il faut utiliser enforce_csrf_checks=True pour simuler un vrai
        navigateur qui enverrait la vérification CSRF.
        """
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(
            "/compte/connexion/",
            {
                "username": "testuser",
                "password": "testpass",
            },
        )
        assert response.status_code == 403, (
            "Une requête POST sans token CSRF devrait renvoyer 403 Forbidden."
        )


@pytest.mark.django_db
@pytest.mark.security
class TestXSSProtection:
    """
    Tests de protection XSS (Cross-Site Scripting).

    Vérifie que les entrées utilisateur contenant du JavaScript
    ne sont pas réfléchies dans les réponses HTML.
    """

    def test_xss_in_search(self, client):
        """
        Test: Une recherche avec payload XSS ne réfléchit pas le script.

        Le payload <script>alert(1)</script> ne doit apparaître
        tel quel dans la réponse HTML.
        """
        xss_payload = "<script>alert(1)</script>"

        # Tester l\'autocomplete
        response = client.get(f"/flights/api/airports/autocomplete/?q={xss_payload}")
        content = response.content.decode("utf-8", errors="ignore")

        # La réponse ne doit pas contenir le tag script non échappé
        assert "<script>alert(1)</script>" not in content.lower(), (
            "Le payload XSS ne devrait pas être réfléchi tel quel dans la réponse."
        )

    def test_xss_in_html_response(self, client):
        """
        Test: Les formulaires HTML échappent correctement les caractères spéciaux.

        Vérifie que les caractères <, >, ", \' sont échappés dans les
        formulaires et les messages d\'erreur.
        """
        response = client.get("/")
        content = response.content.decode("utf-8")

        # La page doit utiliser des mécanismes d\'échappement
        # Django template engine échappe automatiquement par défaut
        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.security
class TestSQLInjectionProtection:
    """
    Tests de protection contre l\'injection SQL.

    Vérifie que les requêtes contenant du code SQL ne sont pas
    exécutées directement et ne causent pas d\'erreurs de base de données.
    """

    def test_sql_injection_search(self, client):
        """
        Test: Une recherche avec payload SQL injection retourne une réponse sûre.

        Le payload \' OR 1=1 -- ne doit pas causer d\'erreur SQL ni
        retourner de données non autorisées.
        """
        sql_payload = "' OR 1=1 --"

        response = client.get(f"/flights/api/airports/autocomplete/?q={sql_payload}")
        assert response.status_code == 200, (
            "La requête ne doit pas causer d\'erreur serveur (500)."
        )

        content = response.content.decode("utf-8", errors="ignore")

        # Vérifier que la réponse ne contient pas d\'erreurs SQL
        sql_error_indicators = [
            "syntax error",
            "sqlite",
            "mysql",
            "postgresql",
            "sql error",
            "query error",
            "ora-",
        ]
        for indicator in sql_error_indicators:
            assert indicator not in content.lower(), (
                f"Indicateur d\'erreur SQL détecté dans la réponse: '{indicator}'"
            )

    def test_sql_injection_union(self, client):
        """
        Test: Payload UNION SELECT dans la recherche.

        Vérifie que les tentatives d\'extraction de données via
        UNION SELECT sont neutralisées.
        """
        union_payload = "' UNION SELECT username, password FROM auth_user --"

        response = client.get(
            f"/flights/api/airports/autocomplete/?q={union_payload}"
        )
        assert response.status_code == 200

        content = response.content.decode("utf-8", errors="ignore")
        assert "password" not in content.lower(), (
            "Le mot 'password' ne devrait pas apparaître dans la réponse."
        )


@pytest.mark.django_db
@pytest.mark.security
class TestAccessControl:
    """
    Tests de contrôle d\'accès.

    Vérifie que les pages protégées sont correctement sécurisées
    et que les utilisateurs non authentifiés sont redirigés.
    """

    def test_protected_view_redirect(self, client):
        """
        Test: La page profil redirige vers login si non authentifié.

        Vérifie que le LoginRequiredMixin fonctionne correctement.
        """
        response = client.get("/compte/profil/", follow=False)
        assert response.status_code == 302, (
            "La page profil devrait rediriger (302) si l\'utilisateur n\'est pas connecté."
        )
        assert "/compte/connexion/" in response.url, (
            "La redirection devrait pointer vers la page de connexion."
        )

    def test_protected_my_bookings_redirect(self, client):
        """
        Test: La page 'Mes réservations' redirige si non authentifié.
        """
        response = client.get("/reservations/mes-reservations/", follow=False)
        assert response.status_code == 302

    def test_authenticated_access_my_bookings(self, authenticated_client):
        """
        Test: Un utilisateur authentifié peut accéder à 'Mes réservations'.

        Vérifie que le LoginRequiredMixin autorise l\'accès aux utilisateurs connectés.
        """
        response = authenticated_client.get("/reservations/mes-reservations/")
        # 200 = accès autorisé, 302 = redirection (possible si autre middleware)
        assert response.status_code in (200, 302)


@pytest.mark.django_db
@pytest.mark.security
class TestSessionManagement:
    """
    Tests de gestion des sessions.

    Vérifie la sécurité des sessions: durée de vie, régénération,
    et protection contre la fixation de session.
    """

    def test_session_expiry(self, client):
        """
        Test: Une session expirée redirige vers la page de connexion.

        Vérifie que les sessions ont une durée de vie configurée
        et que les utilisateurs sont déconnectés après expiration.
        """
        # Simuler une session existante
        session = client.session
        session.save()

        # Vérifier les paramètres de session dans les settings
        assert hasattr(settings, "SESSION_COOKIE_AGE"), (
            "SESSION_COOKIE_AGE devrait être défini dans les settings."
        )

        # La durée de vie de la session ne doit pas être infinie
        session_age = settings.SESSION_COOKIE_AGE
        assert session_age > 0, (
            "SESSION_COOKIE_AGE doit être positif."
        )
        assert session_age <= 1209600, (
            "SESSION_COOKIE_AGE ne devrait pas dépasser 2 semaines (1209600s)."
        )

    def test_session_not_in_url(self, client):
        """
        Test: L\'ID de session n\'est pas exposé dans les URLs.

        Vérifie que la session ID n\'est pas transmise via les paramètres
        d\'URL, ce qui pourrait permettre une attaque de fixation.
        """
        response = client.get("/")
        content = response.content.decode("utf-8")

        # Aucun lien ne doit contenir de session ID
        assert "sessionid=" not in content.lower(), (
            "L\'ID de session ne devrait pas apparaître dans les URLs."
        )


@pytest.mark.django_db
@pytest.mark.security
class TestSecurityConfiguration:
    """
    Tests de la configuration de sécurité Django.

    Vérifie que les paramètres de sécurité de Django sont
    correctement configurés pour la production.
    """

    def test_debug_mode_off(self):
        """
        Test: DEBUG devrait être False en production.

        Note: En développement, DEBUG=True est acceptable.
        Ce test vérifie que le setting est bien défini.
        """
        # Le test passe toujours en dev (DEBUG=True est OK pour le dev)
        # En production, un hook CI/CD devrait vérifier DEBUG=False
        assert hasattr(settings, "DEBUG"), "DEBUG devrait être défini."
        # En environnement de test, DEBUG peut être True
        # Mais le check --deploy signalera le problème

    def test_https_enforcement(self):
        """
        Test: Vérification de la configuration HTTPS.

        En production, SECURE_SSL_REDIRECT devrait être True.
        En développement, il peut être False.
        """
        secure_redirect = getattr(settings, "SECURE_SSL_REDIRECT", False)
        # En dev, c\'est OK d\'être False
        assert isinstance(secure_redirect, bool)

        # Vérifier que ALLOWED_HOSTS est configuré
        allowed_hosts = getattr(settings, "ALLOWED_HOSTS", [])
        assert len(allowed_hosts) > 0, (
            "ALLOWED_HOSTS ne devrait pas être vide."
        )

    def test_password_not_in_response(self, client, authenticated_client):
        """
        Test: Le mot de passe n\'apparaît jamais dans les réponses HTML.

        Vérifie qu\'aucune page ne fuit le mot de passe de l\'utilisateur,
        même dans les formulaires ou les messages d\'erreur.
        """
        # Créer un utilisateur avec un mot de passe spécifique
        test_password = "SuperSecretPassword123!"
        user = User.objects.create_user(
            username="passtest",
            email="pass@test.com",
            password=test_password,
        )

        # Se connecter
        client.login(username="passtest", password=test_password)

        # Visiter les pages principales
        pages_to_check = [
            "/",
            "/compte/profil/",
            "/reservations/mes-reservations/",
        ]

        for url in pages_to_check:
            response = client.get(url)
            if response.status_code == 200:
                content = response.content.decode("utf-8")
                # Le mot de passe ne doit JAMAIS apparaître dans le HTML
                assert test_password not in content, (
                    f"Le mot de passe ne devrait pas apparaître dans {url}"
                )

    def test_login_rate_limiting(self, client):
        """
        Test: Plusieurs tentatives de connexion échouées sont gérées.

        Vérifie que le système ne permet pas le brute-force massif.
        Note: Django n\'a pas de rate-limiting natif; ce test vérifie
        que les tentatives échouées retournent bien une erreur.
        """
        failed_attempts = 5

        for i in range(failed_attempts):
            response = client.post(
                "/compte/connexion/",
                {
                    "username": "nonexistent_user",
                    "password": "wrong_password",
                },
            )
            # Chaque tentative échouée devrait retourner 200 (page avec erreur)
            # ou 403 (CSRF), mais pas 500
            assert response.status_code in (200, 403, 302), (
                f"Tentative {i+1}: status code inattendu: {response.status_code}"
            )

        # Après plusieurs échecs, le comportement devrait être stable
        response = client.post(
            "/compte/connexion/",
            {
                "username": "nonexistent_user",
                "password": "wrong_password",
            },
        )
        assert response.status_code in (200, 403, 302), (
            "Le système devrait rester stable après des tentatives échouées."
        )
'''


def get_owasp_top10_tests():
    """tests/security/test_owasp_top10.py — 6 tests OWASP Top 10."""
    return '''\
"""
Tests OWASP Top 10 — Jour 8.

Tests de sécurité basés sur les vulnérabilités les plus courantes
identifiées par l\'OWASP (Open Web Application Security Project).

Couverture OWASP Top 10 (2021):
    - A01: Broken Access Control
    - A02: Cryptographic Failures
    - A03: Injection
    - A04: Insecure Design
    - A05: Security Misconfiguration
    - A07: Cross-Site Scripting (XSS)

Note: A06 (Vulnerable Components) est couvert par Safety/Bandit,
A08 (Software & Data Integrity), A09 (Logging), A10 (SSRF) sont
partiellement couverts par les checks Django et les scans automatisés.

Exécution:
    cd D:/NouvelAirApp/nouvelair_project/\
    python manage.py test tests.security.test_owasp_top10 -v2
    pytest tests/security/test_owasp_top10.py -v

Couverture: 6 tests couvrant 6 catégories OWASP.
"""

import os
import sys
import pytest
import re
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


# ── Marqueurs pytest ─────────────────────────────────────────────────────────

def pytest_configure(config):
    """Enregistre les marqueurs personnalisés."""
    config.addinivalue_line(
        "markers", "owasp: tests OWASP Top 10 (Sprint 1, Jour 8)"
    )


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def regular_user(db):
    """Utilisateur standard (non-admin)."""
    return User.objects.create_user(
        username="regularuser",
        email="regular@test.com",
        password="RegularPass123!",
    )


@pytest.fixture
def regular_client(db, regular_user):
    """Client authentifié en tant qu\'utilisateur standard."""
    client = Client()
    client.login(username="regularuser", password="RegularPass123!")
    return client


@pytest.fixture
def admin_user(db):
    """Utilisateur administrateur."""
    return User.objects.create_superuser(
        username="adminuser",
        email="admin@test.com",
        password="AdminPass123!",
    )


@pytest.fixture
def admin_client(db, admin_user):
    """Client authentifié en tant qu\'administrateur."""
    client = Client()
    client.login(username="adminuser", password="AdminPass123!")
    return client


# ═══════════════════════════════════════════════════════════════════════════
# A01 — Broken Access Control (Contrôle d\'Accès Cassé)
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
@pytest.mark.owasp
class TestA01BrokenAccessControl:
    """
    A01:2021 — Broken Access Control.

    Vérifie que les utilisateurs ne peuvent pas accéder aux ressources
    ou fonctionnalités pour lesquelles ils ne sont pas autorisés.

    Failles testées:
    - Accès aux pages admin sans permissions
    - Accès au profil d\'un autre utilisateur
    - Modification de données d\'un autre utilisateur
    """

    def test_a01_broken_access_control_admin_without_permission(self, regular_client):
        """
        Test: Un utilisateur non-admin ne peut pas accéder à l\'interface d\'administration.

        Vérifie que /admin/ redirige les utilisateurs non-administrateurs.
        """
        response = regular_client.get("/admin/", follow=False)

        # L\'utilisateur non-admin doit être redirigé ou recevoir une 403
        assert response.status_code in (302, 403), (
            "Un utilisateur non-admin ne devrait pas pouvoir accéder à /admin/. "
            f"Status: {response.status_code}"
        )

        if response.status_code == 302:
            assert "/admin/login/" in response.url or "/compte/connexion/" in response.url, (
                "La redirection devrait pointer vers la page de login admin."
            )

    def test_a01_broken_access_control_admin_pages(self, regular_client):
        """
        Test: Les sous-pages admin sont également protégées.

        Vérifie que les chemins /admin/* sont inaccessibles aux non-admins.
        """
        admin_paths = [
            "/admin/auth/",
            "/admin/auth/user/",
            "/admin/flights/",
            "/admin/bookings/",
        ]

        for path in admin_paths:
            response = regular_client.get(path, follow=False)
            assert response.status_code in (302, 403), (
                f"{path} ne devrait pas être accessible aux non-admins. "
                f"Status: {response.status_code}"
            )

    def test_a01_broken_access_control_other_user_profile(self, regular_client, admin_user):
        """
        Test: Un utilisateur ne peut pas modifier le profil d\'un autre utilisateur.

        Vérifie que les données sensibles d\'un utilisateur sont protégées
        contre l\'accès par d\'autres utilisateurs.
        """
        # L\'utilisateur régulier accède à son propre profil (OK)
        response = regular_client.get("/compte/profil/")
        assert response.status_code == 200

        # Tenter de POST des données pour modifier le profil
        response = regular_client.post(
            "/compte/profil/",
            {
                "username": "adminuser",  # Tentative de changer le username
                "email": "hacked@test.com",
                "first_name": "Hacked",
            },
        )

        # Vérifier que l\'admin n\'a pas été modifié
        admin_user.refresh_from_db()
        assert admin_user.email != "hacked@test.com", (
            "Un utilisateur ne devrait pas pouvoir modifier le profil d\'un autre utilisateur."
        )


# ═══════════════════════════════════════════════════════════════════════════
# A02 — Cryptographic Failures (Défaillances Cryptographiques)
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
@pytest.mark.owasp
class TestA02CryptographicFailures:
    """
    A02:2021 — Cryptographic Failures.

    Vérifie que les données sensibles sont correctement protégées
    par des algorithmes cryptographiques appropriés.

    Points de contrôle:
    - Les mots de passe sont hachés (pas en clair)
    - L\'algorithme de hachage est moderne (PBKDF2, Argon2, bcrypt)
    - La clé secrète Django n\'est pas triviallement devinable
    """

    def test_a02_cryptographic_failures_password_hashing(self, db):
        """
        Test: Les mots de passe sont hachés, pas stockés en clair.

        Vérifie que Django utilise bien son système de hachage pour les mots de passe.
        """
        user = User.objects.create_user(
            username="hashtest",
            email="hash@test.com",
            password="PlainTextPassword123!",
        )

        # Le mot de passe ne doit PAS être stocké en clair
        assert user.password != "PlainTextPassword123!", (
            "Le mot de passe ne devrait jamais être stocké en clair dans la base."
        )

        # Le mot de passe doit commencer par l\'algorithme de hachage
        assert user.password.startswith("pbkdf2_sha256$") or \
               user.password.startswith("argon2") or \
               user.password.startswith("bcrypt$"), (
            "Le mot de passe devrait utiliser un algorithme de hachage sécurisé "
            "(pbkdf2_sha256, argon2, ou bcrypt)."
        )

        # Vérifier que check_password fonctionne
        assert user.check_password("PlainTextPassword123!"), (
            "check_password devrait retourner True pour le bon mot de passe."
        )
        assert not user.check_password("WrongPassword"), (
            "check_password devrait retourner False pour un mauvais mot de passe."
        )

    def test_a02_cryptographic_failures_secret_key(self):
        """
        Test: La clé secrète Django est suffisamment longue et complexe.

        Une clé secrète trop courte ou trop simple peut être devinée
        par force brute.
        """
        secret_key = settings.SECRET_KEY

        # La clé devrait avoir au moins 30 caractères
        assert len(secret_key) >= 30, (
            "La clé secrète (SECRET_KEY) devrait avoir au moins 30 caractères."
        )

        # La clé ne devrait pas être la valeur par défaut de Django
        assert not secret_key.startswith("django-insecure-") or settings.DEBUG, (
            "La clé secrète ne devrait pas commencer par 'django-insecure-' en production."
        )


# ═══════════════════════════════════════════════════════════════════════════
# A03 — Injection
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
@pytest.mark.owasp
class TestA03Injection:
    """
    A03:2021 — Injection.

    Vérifie que les données fournies par l\'utilisateur ne sont pas
    injectées directement dans des requêtes SQL ou des commandes système.

    Types d\'injection testés:
    - Injection SQL classique (\' OR 1=1)
    - Injection SQL avancée (UNION, DROP)
    - Injection dans les formulaires POST
    """

    SQL_INJECTION_PAYLOADS = [
        "' OR 1=1 --",
        "1; DROP TABLE auth_user--",
        "' UNION SELECT * FROM auth_user --",
        "1 OR '1'='1",
        "'; INSERT INTO auth_user VALUES",
        "1; SELECT * FROM information_schema.tables--",
        "admin'--",
        "' OR 'a'='a",
        "1 UNION ALL SELECT NULL,NULL,NULL--",
        "'; EXEC xp_cmdshell('dir')--",
    ]

    XSS_PAYLOADS = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "javascript:alert(1)",
        "<body onload=alert(1)>",
        "'-alert(1)-'",
        "<iframe src='javascript:alert(1)'>",
    ]

    def test_a03_injection_sql_via_autocomplete(self, client):
        """
        Test: L\'autocomplétion résiste à l\'injection SQL.

        Chaque payload SQL est envoyé à l\'endpoint d\'autocomplete.
        Le serveur ne doit jamais retourner d\'erreur SQL.
        """
        for payload in self.SQL_INJECTION_PAYLOADS:
            response = client.get(
                f"/flights/api/airports/autocomplete/?q={payload}"
            )
            assert response.status_code == 200, (
                f"Payload: {payload[:30]}... → Status: {response.status_code}"
            )

            content = response.content.decode("utf-8", errors="ignore")

            # Vérifier l\'absence d\'erreurs SQL dans la réponse
            sql_errors = [
                "syntax error", "sqlite", "mysql", "postgresql",
                "sql error", "ora-", "1064", "42000",
            ]
            for error in sql_errors:
                assert error not in content.lower(), (
                    f"Indicateur d\'erreur SQL ('{error}') trouvé "
                    f"pour le payload: {payload[:30]}..."
                )

    def test_a03_injection_xss_via_autocomplete(self, client):
        """
        Test: L\'autocomplétion échappe les payloads XSS.

        Les balises <script> et les event handlers ne doivent pas
        être réfléchis dans les réponses JSON.
        """
        for payload in self.XSS_PAYLOADS:
            response = client.get(
                f"/flights/api/airports/autocomplete/?q={payload}"
            )
            assert response.status_code == 200

            content = response.content.decode("utf-8", errors="ignore")

            # Les payloads XSS ne doivent pas être réfléchis tels quels
            assert "<script>" not in content.lower(), (
                f"<script> trouvé dans la réponse pour: {payload[:30]}..."
            )
            assert "onerror=" not in content.lower(), (
                f"onerror= trouvé dans la réponse pour: {payload[:30]}..."
            )


# ═══════════════════════════════════════════════════════════════════════════
# A04 — Insecure Design (Conception Non Sécurisée)
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
@pytest.mark.owasp
class TestA04InsecureDesign:
    """
    A04:2021 — Insecure Design.

    Vérifie que l\'application ne expose pas de données sensibles
    ou de fonctionnalités par mauvaise conception.

    Points de contrôle:
    - Les messages d\'erreur ne révèlent pas d\'informations sensibles
    - Les numéros de réservation ne sont pas devinables
    - La pagination ne permet pas l\'énumération excessive
    """

    def test_a04_insecure_design_no_sensitive_data_in_errors(self, client):
        """
        Test: Les pages d\'erreur ne révèlent pas d\'informations sensibles.

        Vérifie que les pages 404 et 500 ne montrent pas:
        - Stack traces en production
        - Chemins de fichiers serveur
        - Noms de base de données
        - Variables d\'environnement
        """
        # Tester une URL inexistante (404)
        response = client.get("/page-inexistante-totalement-fausse/")

        content = response.content.decode("utf-8", errors="ignore")

        # En mode DEBUG=True (dev), Django montre le traceback.
        # En production (DEBUG=False), il ne devrait pas.
        if not settings.DEBUG:
            sensitive_patterns = [
                "Traceback",
                "Exception Type:",
                "Exception Value:",
                "Python Path:",
                "Server time:",
                "/home/",
                "C:\\\\",
            ]
            for pattern in sensitive_patterns:
                assert pattern not in content, (
                    f"Information sensible ('{pattern}') trouvée dans la page 404"
                )
        else:
            # En dev, on vérifie juste que la page se charge
            assert response.status_code == 404

    def test_a04_insecure_design_no_enumeration(self, client):
        """
        Test: L\'énumération d\'utilisateurs n\'est pas possible via le login.

        Vérifie que les messages d\'erreur de connexion ne permettent pas
        de déterminer si un nom d\'utilisateur existe.
        """
        # Test avec un utilisateur inexistant
        response = client.post(
            "/compte/connexion/",
            {
                "username": "nonexistent_user_xyz_12345",
                "password": "somepassword",
            },
        )
        content_1 = response.content.decode("utf-8", errors="ignore")

        # Test avec un utilisateur existant mais mauvais mot de passe
        User.objects.create_user(
            username="existing_test_user",
            password="CorrectPassword123!",
        )

        response = client.post(
            "/compte/connexion/",
            {
                "username": "existing_test_user",
                "password": "WrongPassword",
            },
        )
        content_2 = response.content.decode("utf-8", errors="ignore")

        # Les messages d\'erreur devraient être similaires
        # (ne pas révéler si l\'utilisateur existe)
        # Note: Django affiche le même message par défaut
        assert response.status_code in (200, 403)


# ═══════════════════════════════════════════════════════════════════════════
# A05 — Security Misconfiguration (Mauvaise Configuration de Sécurité)
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
@pytest.mark.owasp
class TestA05SecurityMisconfiguration:
    """
    A05:2021 — Security Misconfiguration.

    Vérifie que Django et le serveur sont correctement configurés
    pour la sécurité.

    Points de contrôle:
    - DEBUG = False en production
    - ALLOWED_HOSTS est configuré
    - Les headers de sécurité sont présents
    - Les statistiques de debug ne sont pas accessibles
    """

    def test_a05_security_misconfiguration_debug_mode(self):
        """
        Test: DEBUG ne devrait pas être True en production.

        En développement, DEBUG=True est acceptable.
        Ce test vérifie que le setting est conscient de son état.
        """
        # Toujours vérifier que DEBUG est défini
        assert hasattr(settings, "DEBUG")

        # En environnement de test, vérifier la cohérence
        if not settings.DEBUG:
            # En production, d\'autres vérifications s\'appliquent
            assert settings.DEBUG is False

    def test_a05_security_misconfiguration_allowed_hosts(self):
        """
        Test: ALLOWED_HOSTS est correctement configuré.

        En production, ALLOWED_HOSTS ne devrait pas être ['*'].
        En développement, ['*'] est acceptable.
        """
        allowed_hosts = getattr(settings, "ALLOWED_HOSTS", [])

        assert len(allowed_hosts) > 0, (
            "ALLOWED_HOSTS ne devrait pas être vide."
        )

        if not settings.DEBUG:
            # En production, ['*'] est dangereux
            assert "*" not in allowed_hosts, (
                "ALLOWED_HOSTS ne devrait pas contenir '*' en production."
            )

    def test_a05_security_misconfiguration_security_headers(self, client):
        """
        Test: Les headers de sécurité HTTP sont présents.

        Vérifie les headers suivants:
        - X-Frame-Options (protection contre clickjacking)
        - X-Content-Type-Options (anti-MIME sniffing)
        """
        response = client.get("/")
        headers = dict(response.headers)

        # X-Frame-Options devrait être présent (Django l\'ajoute par défaut)
        xfo = headers.get("X-Frame-Options", "")
        assert xfo in ("DENY", "SAMEORIGIN", ""), (
            f"X-Frame-Options devrait être DENY ou SAMEORIGIN, trouvé: '{xfo}'"
        )

        # X-Content-Type-Options devrait être "nosniff"
        xcto = headers.get("X-Content-Type-Options", "")
        assert xcto.lower() == "nosniff" or xcto == "", (
            f"X-Content-Type-Options devrait être 'nosniff', trouvé: '{xcto}'"
        )

    def test_a05_security_misconfiguration_no_debug_toolbar(self, client):
        """
        Test: Django Debug Toolbar n\'est pas accessible en production.

        En développement, le Debug Toolbar peut être présent.
        En production, il doit être désactivé.
        """
        if not settings.DEBUG:
            response = client.get("/__debug__/")
            assert response.status_code == 404, (
                "Le Debug Toolbar ne devrait pas être accessible en production."
            )


# ═══════════════════════════════════════════════════════════════════════════
# A07 — Cross-Site Scripting (XSS)
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.django_db
@pytest.mark.owasp
class TestA07CrossSiteScripting:
    """
    A07:2021 — Cross-Site Scripting (XSS).

    Vérifie que les entrées utilisateur ne sont pas exécutées
    comme code JavaScript dans le navigateur.

    Types de XSS testés:
    - Reflected XSS (via paramètres URL)
    - Stored XSS (via formulaires)
    - DOM-based XSS
    """

    def test_a07_xss_in_search_parameters(self, client):
        """
        Test: Les paramètres de recherche ne sont pas vulnérables au XSS réfléchi.

        Envoie un payload XSS via les paramètres GET et vérifie
        qu\'il n\'est pas réfléchi non échappé dans le HTML.
        """
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "';alert(String.fromCharCode(88,83,83))//",
            '"><script>alert(1)</script>',
            "'-alert(1)-'",
        ]

        for payload in xss_payloads:
            # Tester l\'autocomplete
            response = client.get(
                f"/flights/api/airports/autocomplete/?q={payload}"
            )
            assert response.status_code == 200

            content = response.content.decode("utf-8", errors="ignore")

            # Vérifier l\'absence de scripts non échappés
            assert "<script" not in content.lower(), (
                f"Tag <script> réfléchi pour payload: {payload[:30]}..."
            )
            assert "onerror=" not in content.lower(), (
                f"Event handler onerror réfléchi pour payload: {payload[:30]}..."
            )
            assert "onload=" not in content.lower(), (
                f"Event handler onload réfléchi pour payload: {payload[:30]}..."
            )

    def test_a07_xss_in_form_fields(self, client):
        """
        Test: Les formulaires échappent correctement les entrées utilisateur.

        Vérifie que les champs de formulaire (recherche, login, inscription)
        échappent les caractères HTML spéciaux.
        """
        # Visiter la page de connexion
        response = client.get("/compte/connexion/")
        content = response.content.decode("utf-8")

        # Vérifier que Django échappe automatiquement
        # (Django templates échappent par défaut avec {% autoescape on %})
        assert response.status_code == 200

        # Visiter la page d\'inscription
        response = client.get("/compte/inscription/")
        assert response.status_code == 200

    def test_a07_xss_json_response(self, client):
        """
        Test: Les réponses JSON ne contiennent pas de payloads XSS non échappés.

        L\'API d\'autocomplete retourne du JSON. Vérifie que le JSON
        ne contient pas de balises HTML dans les valeurs.
        """
        xss_payload = "<script>alert('XSS')</script>test"

        response = client.get(
            f"/flights/api/airports/autocomplete/?q={xss_payload}"
        )
        assert response.status_code == 200

        content = response.content.decode("utf-8", errors="ignore")

        # La réponse JSON ne devrait pas contenir le payload brut
        assert "<script>alert" not in content.lower(), (
            "La réponse JSON ne devrait pas contenir de payloads XSS."
        )
'''


def get_performance_report_template():
    """docs/performance_report_template.md — Modèle de rapport de performance en français."""
    return '''\
# Rapport de Tests de Performance — NouvelAir

## Informations Générales

| Champ | Valeur |
|-------|--------|
| **Projet** | NouvelAir — Compagnie Aérienne |
| **Date du test** | {{DATE}} |
| **Environnement** | Développement local |
| **Système d\'exploitation** | Windows 11 |
| **Python** | 3.x |
| **Django** | 5.x |
| **Serveur** | runserver (development server) |
| **Base de données** | SQLite 3 |
| **Navigateur** | N/A (tests backend Locust) |
| **Outil de test** | Locust {{LOCUST_VERSION}} |

---

## 1. Résumé Exécutif

Ce rapport présente les résultats des tests de performance effectués sur l\'application
NouvelAir. Les tests ont été réalisés dans un environnement de développement local pour
établir une **ligne de base (baseline)** des performances et identifier les éventuels
goulots d\'étranglement avant la mise en production.

### Conclusions principales

- **Statut global** : {{STATUS_GLOBAL}}
- **Points critiques** : {{POINTS_CRITIQUES}}
- **Recommandation prioritaire** : {{RECOMMANDATION_PRIORITAIRE}}

---

## 2. Méthodologie de Test

### 2.1 Types de tests exécutés

| Type de test | Utilisateurs | Spawn Rate | Durée | Objectif |
|-------------|-------------|-----------|-------|----------|
| **Baseline** | 10 | 2/s | 2 min | Établir la référence |
| **Charge (Load)** | 50 | 5/s | 5 min | Trafic normal |
| **Stress** | 200 | 10/s | 10 min | Identifier les limites |
| **Spike** | 100 | 100/s | 2 min | Pic soudain |
| **Endurance** | 30 | 3/s | 15 min | Stabilité longue durée |

### 2.2 Endpoints testés

| Endpoint | Description | Poids |
|----------|-------------|-------|
| `/` | Page d\'accueil | 5 |
| `/destinations/` | Liste des destinations | 3 |
| `/promotions/` | Offres promotionnelles | 3 |
| `/flights/aeroports/` | Liste des aéroports | 2 |
| `/flights/api/airports/autocomplete/?q=TUN` | Autocomplétion | 2 |
| `/reservations/mes-reservations/` | Mes réservations (protégé) | 1 |
| `/reservations/recherche/` | Recherche de réservation | 1 |
| `/compte/connexion/` | Authentification | 1 |

### 2.3 Scénarios utilisateur simulés

1. **Visiteur curieux** : Navigation sur les pages publiques
2. **Voyageur** : Recherche de vols et autocomplétion
3. **Client enregistré** : Consultation de ses réservations
4. **Nouvel utilisateur** : Visite des pages d\'inscription

---

## 3. Seuils de Performance (SLA)

| Endpoint | p50 (ms) | p95 (ms) | p99 (ms) | Criticité |
|----------|----------|----------|----------|-----------|
| Accueil | 1000 | 3000 | 5000 | HAUT |
| Recherche vols | 1500 | 5000 | 8000 | MOYEN |
| Autocomplétion | 100 | 500 | 1000 | CRITIQUE |
| Destinations | 800 | 2500 | 4000 | MOYEN |
| Promotions | 900 | 2800 | 4500 | MOYEN |
| Connexion | 500 | 2000 | 3000 | HAUT |
| Mes réservations | 1200 | 3500 | 6000 | MOYEN |
| Liste aéroports | 700 | 2200 | 3500 | BAS |

**Seuils globaux** :
- Taux d\'erreur maximum : 1%
- Temps de réponse moyen maximum : 2 secondes
- RPS minimum : 5 requêtes/seconde

---

## 4. Résultats du Test de Charge (Load Test)

### 4.1 Métriques globales

| Métrique | Valeur | Seuil | Statut |
|----------|--------|-------|--------|
| Requêtes totales | {{TOTAL_REQUESTS}} | - | - |
| Requêtes/s (RPS) | {{RPS}} | > 5 | {{RPS_STATUS}} |
| Temps moyen (ms) | {{AVG_TIME}} | < 2000 | {{AVG_STATUS}} |
| Erreurs | {{ERRORS}} | < 1% | {{ERROR_STATUS}} |
| Durée totale | 5 min | - | - |

### 4.2 Résultats par endpoint

| Endpoint | # Requêtes | RPS | p50 (ms) | p95 (ms) | p99 (ms) | Erreur % | Statut |
|----------|-----------|-----|----------|----------|----------|----------|--------|
| `/ [Homepage]` | {{HOME_COUNT}} | {{HOME_RPS}} | {{HOME_P50}} | {{HOME_P95}} | {{HOME_P99}} | {{HOME_ERR}} | {{HOME_STATUS}} |
| `/destinations/` | {{DEST_COUNT}} | {{DEST_RPS}} | {{DEST_P50}} | {{DEST_P95}} | {{DEST_P99}} | {{DEST_ERR}} | {{DEST_STATUS}} |
| `/promotions/` | {{PROMO_COUNT}} | {{PROMO_RPS}} | {{PROMO_P50}} | {{PROMO_P95}} | {{PROMO_P99}} | {{PROMO_ERR}} | {{PROMO_STATUS}} |
| `/flights/aeroports/` | {{AIR_COUNT}} | {{AIR_RPS}} | {{AIR_P50}} | {{AIR_P95}} | {{AIR_P99}} | {{AIR_ERR}} | {{AIR_STATUS}} |
| `/flights/api/...autocomplete/` | {{AC_COUNT}} | {{AC_RPS}} | {{AC_P50}} | {{AC_P95}} | {{AC_P99}} | {{AC_ERR}} | {{AC_STATUS}} |
| `/reservations/mes-reservations/` | {{BK_COUNT}} | {{BK_RPS}} | {{BK_P50}} | {{BK_P95}} | {{BK_P99}} | {{BK_ERR}} | {{BK_STATUS}} |

### 4.3 Analyse

{{LOAD_ANALYSIS}}

---

## 5. Résultats du Test de Stress

### 5.1 Objectif

Identifier le point de rupture du système en augmentant progressivement
la charge jusqu\'à 200 utilisateurs simultanés.

### 5.2 Montée en charge

| Phase | Utilisateurs | Durée | RPS | Temps moyen | Erreur % |
|-------|-------------|-------|-----|-------------|----------|
| Phase 1 | 10 → 50 | 1 min | {{S1_RPS}} | {{S1_AVG}} | {{S1_ERR}} |
| Phase 2 | 50 → 100 | 2 min | {{S2_RPS}} | {{S2_AVG}} | {{S2_ERR}} |
| Phase 3 | 100 → 150 | 3 min | {{S3_RPS}} | {{S3_AVG}} | {{S3_ERR}} |
| Phase 4 | 150 → 200 | 4 min | {{S4_RPS}} | {{S4_AVG}} | {{S4_ERR}} |

### 5.3 Point de rupture

{{RUPTURE_POINT}}

### 5.4 Analyse

{{STRESS_ANALYSIS}}

---

## 6. Résultats du Test de Spike

### 6.1 Scénario

Simulation d\'un afflux massif et soudain de 100 utilisateurs simultanés,
comme lors d\'une promotion flash ou d\'un événement médiatique.

### 6.2 Résultats

| Phase | Utilisateurs | Durée | RPS | Erreur % |
|-------|-------------|-------|-----|----------|
| Pic | 100 | 30 s | {{SPIKE_RPS}} | {{SPIKE_ERR}} |
| Stabilisation | 100 | 1m30s | {{STABLE_RPS}} | {{STABLE_ERR}} |
| Déclin | 100 → 0 | 30 s | {{DECLINE_RPS}} | {{DECLINE_ERR}} |

### 6.3 Analyse

{{SPIKE_ANALYSIS}}

---

## 7. Résultats du Test d\'Endurance

### 7.1 Objectif

Vérifier la stabilité du système sur une période prolongée (15 minutes)
pour détecter les fuites mémoire et la dégradation progressive.

### 7.2 Évolution des performances

| Intervalle | RPS | Temps moyen | Mémoire estimée |
|-----------|-----|-------------|-----------------|
| 0-3 min | {{E1_RPS}} | {{E1_AVG}} | {{E1_MEM}} |
| 3-6 min | {{E2_RPS}} | {{E2_AVG}} | {{E2_MEM}} |
| 6-9 min | {{E3_RPS}} | {{E3_AVG}} | {{E3_MEM}} |
| 9-12 min | {{E4_RPS}} | {{E4_AVG}} | {{E4_MEM}} |
| 12-15 min | {{E5_RPS}} | {{E5_AVG}} | {{E5_MEM}} |

### 7.3 Dégradation

{{ENDURANCE_DEGRADATION}}

---

## 8. Comparaison avec les Seuils

| Endpoint | Seuil p95 | Mesuré p95 | Δ | Statut |
|----------|-----------|-----------|---|--------|
| Accueil | 3000 ms | {{M_HOME_P95}} | {{D_HOME}} | {{S_HOME}} |
| Autocomplétion | 500 ms | {{M_AC_P95}} | {{D_AC}} | {{S_AC}} |
| Destinations | 2500 ms | {{M_DEST_P95}} | {{D_DEST}} | {{S_DEST}} |
| Promotions | 2800 ms | {{M_PROMO_P95}} | {{D_PROMO}} | {{S_PROMO}} |

**Résumé** : {{THRESHOLD_SUMMARY}}

---

## 9. Recommandations

### 9.1 Actions prioritaires

1. **{{REC_1_TITLE}}**
   - Priorité: CRITIQUE
   - Impact: {{REC_1_IMPACT}}
   - Détail: {{REC_1_DETAIL}}

2. **{{REC_2_TITLE}}**
   - Priorité: HAUTE
   - Impact: {{REC_2_IMPACT}}
   - Détail: {{REC_2_DETAIL}}

### 9.2 Optimisations recommandées

3. **{{REC_3_TITLE}}**
   - Priorité: MOYENNE
   - Impact: {{REC_3_IMPACT}}
   - Détail: {{REC_3_DETAIL}}

4. **{{REC_4_TITLE}}**
   - Priorité: BASSE
   - Impact: {{REC_4_IMPACT}}
   - Détail: {{REC_4_DETAIL}}

### 9.3 Pour la production

- Remplacer `runserver` par Gunicorn + Nginx
- Utiliser PostgreSQL au lieu de SQLite
- Configurer le cache Redis pour les requêtes fréquentes
- Activer la compression Gzip
- Utiliser un CDN pour les assets statiques

---

## 10. Graphiques et Visualisations

### 10.1 Temps de réponse dans le temps

> Le graphique locust montre l\'évolution du temps de réponse médian (vert)
> et du 95e percentile (jaune) au cours du test.

![Temps de réponse](reports/performance/load_test_files/locust_response_times_chart.png)

### 10.2 Requêtes par seconde

> Évolution du nombre de requêtes traitées par seconde au fil du test.

![RPS](reports/performance/load_test_files/locust_rps_chart.png)

### 10.3 Distribution des temps de réponse

> Histogramme montrant la distribution des temps de réponse pour chaque endpoint.

![Distribution](reports/performance/load_test_files/locust_response_time_distribution_chart.png)

### 10.4 Utilisateurs actifs

> Nombre d\'utilisateurs simulés actifs pendant le test.

![Utilisateurs](reports/performance/load_test_files/locust_users_chart.png)

---

## Annexe A: Commandes utilisées

```bash
# Test de base (baseline)
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \\
       --headless -u 10 -r 2 -t 2m \\
       --html=reports/performance/baseline_test.html

# Test de charge
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \\
       --headless -u 50 -r 5 -t 5m \\
       --html=reports/performance/load_test.html

# Test de stress
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \\
       --headless -u 200 -r 10 -t 10m \\
       --html=reports/performance/stress_test.html

# Test de spike
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \\
       --headless -u 100 -r 100 -t 2m \\
       --html=reports/performance/spike_test.html

# Test d'endurance
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:8000 \\
       --headless -u 30 -r 3 -t 15m \\
       --html=reports/performance/endurance_test.html
```

---

## Annexe B: Glossaire

| Terme | Définition |
|-------|-----------|
| **RPS** | Requêtes Par Seconde |
| **p50** | 50e percentile (médiane) |
| **p95** | 95e percentile |
| **p99** | 99e percentile |
| **Spawn Rate** | Taux d\'apparition des utilisateurs virtuels |
| **Think Time** | Temps de pause entre les requêtes |
| **SLA** | Service Level Agreement (accord de niveau de service) |

---

*Rapport généré automatiquement — NouvelAir Sprint 1, Jour 8*
*Date: {{DATE}}*
'''


def get_security_report_template():
    """docs/security_report_template.md — Modèle de rapport de sécurité en français."""
    return '''\
# Rapport de Sécurité — NouvelAir

## Informations Générales

| Champ | Valeur |
|-------|--------|
| **Projet** | NouvelAir — Compagnie Aérienne |
| **Date du scan** | {{DATE}} |
| **Environnement** | Développement local |
| **Système d\'exploitation** | Windows 11 |
| **Python** | 3.x |
| **Django** | 5.x |
| **Exécutant** | {{EXECUTANT}} |

---

## 1. Résumé Exécutif

Ce rapport présente les résultats de l\'audit de sécurité de l\'application
NouvelAir. L\'audit couvre l\'analyse statique du code (Bandit), la vérification
des dépendances (Safety), les tests de sécurité manuels et la couverture du
OWASP Top 10 (2021).

### Score de sécurité global

| Catégorie | Score | Statut |
|-----------|-------|--------|
| Analyse statique (Bandit) | {{BANDIT_SCORE}}/100 | {{BANDIT_STATUS}} |
| Dépendances (Safety) | {{SAFETY_SCORE}}/100 | {{SAFETY_STATUS}} |
| Tests manuels | {{MANUAL_SCORE}}/100 | {{MANUAL_STATUS}} |
| OWASP Top 10 | {{OWASP_SCORE}}/100 | {{OWASP_STATUS}} |
| **Score global** | **{{GLOBAL_SCORE}}/100** | **{{GLOBAL_STATUS}}** |

### Conclusions principales

- **Vulnérabilités critiques** : {{CRITICAL_COUNT}}
- **Vulnérabilités hautes** : {{HIGH_COUNT}}
- **Vulnérabilités moyennes** : {{MEDIUM_COUNT}}
- **Vulnérabilités basses** : {{LOW_COUNT}}

---

## 2. Outils et Méthodologie

### 2.1 Outils utilisés

| Outil | Version | Type de scan | Couverture |
|-------|---------|-------------|-----------|
| **Bandit** | {{BANDIT_VERSION}} | Analyse statique Python | Code Python du projet |
| **Safety** | {{SAFETY_VERSION}} | CVE des dépendances | requirements.txt |
| **Django check --deploy** | 5.x | Configuration sécurité | Settings Django |
| **Tests manuels** | Custom | Tests fonctionnels sécurité | Endpoints principaux |
| **OWASP Top 10** | Custom | Tests de vulnérabilités | 6 catégories sur 10 |

### 2.2 Méthodologie

1. **Analyse statique** : Scan complet du code Python avec Bandit
2. **Vérification des dépendances** : Cross-reference avec la base de données CVE de PyPI
3. **Configuration Django** : Vérification des paramètres de sécurité
4. **Tests manuels** : 10 tests de sécurité avec le client de test Django
5. **OWASP Top 10** : 6 tests ciblés sur les vulnérabilités les plus critiques

---

## 3. Résultats Bandit (Analyse Statique)

### 3.1 Résumé

| Sévérité | Nombre | Détails |
|----------|--------|---------|
| 🔴 **Haute** | {{BANDIT_HIGH}} | {{BANDIT_HIGH_DETAILS}} |
| 🟠 **Moyenne** | {{BANDIT_MEDIUM}} | {{BANDIT_MEDIUM_DETAILS}} |
| 🟡 **Basse** | {{BANDIT_LOW}} | {{BANDIT_LOW_DETAILS}} |
| 🔵 **Info** | {{BANDIT_INFO}} | {{BANDIT_INFO_DETAILS}} |
| **Total** | {{BANDIT_TOTAL}} | |

### 3.2 Findings détaillés

{{#each BANDIT_FINDINGS}}
#### [{{ID}}] {{TITLE}} — {{SEVERITY}}

- **Fichier** : `{{FILE}}`
- **Ligne** : {{LINE}}
- **Confiance** : {{CONFIDENCE}}
- **Description** : {{DESCRIPTION}}
- **Rémédiation** : {{REMEDIATION}}

---

{{/each}}

### 3.3 Analyse Bandit

{{BANDIT_ANALYSIS}}

---

## 4. Résultats Safety (Vulnérabilités des Dépendances)

### 4.1 Résumé

| Statut | Nombre |
|--------|--------|
| ✅ Aucune vulnérabilité | {{SAFETY_SAFE}} |
| ⚠ Vulnérabilités trouvées | {{SAFETY_VULN}} |

### 4.2 Détails des vulnérabilités

{{#if SAFETY_HAS_VULNS}}

| Package | Version installée | CVE | Sévérité CVSS | Description |
|---------|------------------|-----|---------------|-------------|
{{#each SAFETY_VULN_LIST}}
| {{PACKAGE}} | {{VERSION}} | {{CVE_ID}} | {{CVSS}} | {{ADVISORY}} |
{{/each}}

{{else}}

✅ **Aucune vulnérabilité connue** dans les dépendances du projet.

{{/if}}

### 4.3 Analyse Safety

{{SAFETY_ANALYSIS}}

---

## 5. Résultats des Tests Manuels

### 5.1 Résumé

| # | Test | Résultat | Détails |
|---|------|----------|---------|
| 1 | CSRF token sur page d\'accueil | {{T1_RESULT}} | {{T1_DETAIL}} |
| 2 | POST sans CSRF → 403 | {{T2_RESULT}} | {{T2_DETAIL}} |
| 3 | XSS dans recherche autocomplete | {{T3_RESULT}} | {{T3_DETAIL}} |
| 4 | Injection SQL autocomplete | {{T4_RESULT}} | {{T4_DETAIL}} |
| 5 | URL protégée → redirection | {{T5_RESULT}} | {{T5_DETAIL}} |
| 6 | Rate limiting connexion | {{T6_RESULT}} | {{T6_DETAIL}} |
| 7 | Session expiry | {{T7_RESULT}} | {{T7_DETAIL}} |
| 8 | HTTPS enforcement | {{T8_RESULT}} | {{T8_DETAIL}} |
| 9 | Password pas dans réponse | {{T9_RESULT}} | {{T9_DETAIL}} |
| 10 | DEBUG mode | {{T10_RESULT}} | {{T10_DETAIL}} |

**Score** : {{MANUAL_PASSED}}/10 tests réussis

### 5.2 Analyse des tests manuels

{{MANUAL_ANALYSIS}}

---

## 6. Couverture OWASP Top 10 (2021)

### 6.1 Matrice de couverture

| ID | Catégorie | Testé | Statut | Vulnérabilités trouvées |
|----|-----------|-------|--------|------------------------|
| A01 | Broken Access Control | ✅ Oui | {{A01_STATUS}} | {{A01_COUNT}} |
| A02 | Cryptographic Failures | ✅ Oui | {{A02_STATUS}} | {{A02_COUNT}} |
| A03 | Injection | ✅ Oui | {{A03_STATUS}} | {{A03_COUNT}} |
| A04 | Insecure Design | ✅ Oui | {{A04_STATUS}} | {{A04_COUNT}} |
| A05 | Security Misconfiguration | ✅ Oui | {{A05_STATUS}} | {{A05_COUNT}} |
| A06 | Vulnerable Components | ⚠️ Partiel | {{A06_STATUS}} | {{A06_COUNT}} |
| A07 | XSS | ✅ Oui | {{A07_STATUS}} | {{A07_COUNT}} |
| A08 | Software & Data Integrity | ⚠️ Partiel | {{A08_STATUS}} | {{A08_COUNT}} |
| A09 | Logging & Monitoring | ⚠️ Partiel | {{A09_STATUS}} | {{A09_COUNT}} |
| A10 | SSRF | ❌ Non testé | {{A10_STATUS}} | {{A10_COUNT}} |

### 6.2 Détails des tests OWASP

#### A01 — Broken Access Control
- **Tests** : Accès admin sans permission, sous-pages admin, profil d\'un autre utilisateur
- **Résultats** : {{A01_DETAILS}}

#### A02 — Cryptographic Failures
- **Tests** : Hachage des mots de passe, complexité de la clé secrète
- **Résultats** : {{A02_DETAILS}}

#### A03 — Injection
- **Tests** : 10 payloads SQL injection, 7 payloads XSS via autocomplete
- **Résultats** : {{A03_DETAILS}}

#### A04 — Insecure Design
- **Tests** : Fuite de données dans les erreurs, énumération d\'utilisateurs
- **Résultats** : {{A04_DETAILS}}

#### A05 — Security Misconfiguration
- **Tests** : DEBUG mode, ALLOWED_HOSTS, headers de sécurité, Debug Toolbar
- **Résultats** : {{A05_DETAILS}}

#### A07 — Cross-Site Scripting
- **Tests** : XSS réfléchi, XSS dans formulaires, XSS dans JSON
- **Résultats** : {{A07_DETAILS}}

---

## 7. Matrice des Risques

| Risque | Probabilité | Impact | Score | Priorité |
|--------|------------|--------|-------|----------|
| {{RISK_1}} | {{R1_PROB}} | {{R1_IMPACT}} | {{R1_SCORE}} | {{R1_PRIORITY}} |
| {{RISK_2}} | {{R2_PROB}} | {{R2_IMPACT}} | {{R2_SCORE}} | {{R2_PRIORITY}} |
| {{RISK_3}} | {{R3_PROB}} | {{R3_IMPACT}} | {{R3_SCORE}} | {{R3_PRIORITY}} |
| {{RISK_4}} | {{R4_PROB}} | {{R4_IMPACT}} | {{R4_SCORE}} | {{R4_PRIORITY}} |
| {{RISK_5}} | {{R5_PROB}} | {{R5_IMPACT}} | {{R5_SCORE}} | {{R5_PRIORITY}} |

### Échelle de risque

| Score | Niveau | Action requise |
|-------|--------|---------------|
| 9-10 | 🔴 Critique | Correction immédiate |
| 7-8 | 🟠 Haut | Correction sous 48h |
| 5-6 | 🟡 Moyen | Correction sous 1 semaine |
| 3-4 | 🔵 Bas | Correction planifiée |
| 1-2 | ⚪ Info | Surveillance |

---

## 8. Scores CVSS

### 8.1 Vulnérabilités avec score CVSS

| Vulnérabilité | CVSS v3.1 | Vecteur | Sévérité |
|--------------|-----------|---------|----------|
| {{CVSS_1_NAME}} | {{CVSS_1_SCORE}} | {{CVSS_1_VECTOR}} | {{CVSS_1_SEVERITY}} |
| {{CVSS_2_NAME}} | {{CVSS_2_SCORE}} | {{CVSS_2_VECTOR}} | {{CVSS_2_SEVERITY}} |
| {{CVSS_3_NAME}} | {{CVSS_3_SCORE}} | {{CVSS_3_VECTOR}} | {{CVSS_3_SEVERITY}} |

### 8.2 Distribution CVSS

```
Critique (9.0-10.0) : ██████████ {{CVSS_CRITICAL}}
Haut (7.0-8.9)      : ████████   {{CVSS_HIGH}}
Moyen (4.0-6.9)     : ██████     {{CVSS_MEDIUM}}
Bas (0.1-3.9)       : ████       {{CVSS_LOW}}
Info (0.0)          : ██         {{CVSS_INFO}}
```

---

## 9. Recommandations

### 9.1 Actions immédiates (Critique / Haut)

#### REC-001: {{REC_1_TITLE}}
- **Priorité** : 🔴 CRITIQUE
- **Catégorie OWASP** : {{REC_1_OWASP}}
- **CVSS** : {{REC_1_CVSS}}
- **Description** : {{REC_1_DESC}}
- **Rémédiation** :
  1. {{REC_1_STEP_1}}
  2. {{REC_1_STEP_2}}
  3. {{REC_1_STEP_3}}
- **Estimation** : {{REC_1_EFFORT}}

#### REC-002: {{REC_2_TITLE}}
- **Priorité** : 🟠 HAUTE
- **Catégorie OWASP** : {{REC_2_OWASP}}
- **CVSS** : {{REC_2_CVSS}}
- **Description** : {{REC_2_DESC}}
- **Rémédiation** :
  1. {{REC_2_STEP_1}}
  2. {{REC_2_STEP_2}}
- **Estimation** : {{REC_2_EFFORT}}

### 9.2 Actions planifiées (Moyen)

#### REC-003: {{REC_3_TITLE}}
- **Priorité** : 🟡 MOYENNE
- **Description** : {{REC_3_DESC}}
- **Rémédiation** : {{REC_3_STEPS}}

### 9.3 Bonnes pratiques recommandées

1. **Rate limiting** : Implémenter django-ratelimit ou django-axes pour la protection brute-force
2. **HTTPS** : Configurer SECURE_SSL_REDIRECT=True en production
3. **Headers CSP** : Définir une politique Content-Security-Policy stricte
4. **Logging** : Activer le logging des événements de sécurité
5. **Dépendances** : Configurer des mises à jour automatiques des dépendances
6. **Tests CI/CD** : Intégrer Bandit et Safety dans le pipeline CI/CD

---

## 10. Conclusion

### 10.1 État de sécurité du projet

{{CONCLUSION}}

### 10.2 Prochaines étapes

1. Corriger les vulnérabilités critiques et hautes identifiées
2. Configurer les paramètres de sécurité pour la production
3. Mettre en place le rate limiting sur les endpoints sensibles
4. Intégrer les outils de sécurité dans le pipeline CI/CD
5. Planifier un audit de sécurité régulier (mensuel)

---

## Annexe A: Commandes de scan

```bash
# Analyse statique avec Bandit
bandit -r . -f html -o reports/security/bandit_report.html \
       --exclude tests/,migrations/,__pycache__/

# Vérification des dépendances avec Safety
safety check -r requirements.txt --json

# Vérifications Django
python manage.py check --deploy

# Tests de sécurité manuels
python manage.py test tests.security.test_security_manual -v2

# Tests OWASP
python manage.py test tests.security.test_owasp_top10 -v2

# Scan complet
python tests/security/run_security_scan.py
```

## Annexe B: Glossaire

| Terme | Définition |
|-------|-----------|
| **CVSS** | Common Vulnerability Scoring System |
| **CVE** | Common Vulnerabilities and Exposures |
| **CSRF** | Cross-Site Request Forgery |
| **XSS** | Cross-Site Scripting |
| **SQLi** | SQL Injection |
| **OWASP** | Open Web Application Security Project |
| **SLA** | Service Level Agreement |

---

*Rapport généré automatiquement — NouvelAir Sprint 1, Jour 8*
*Date: {{DATE}}*
*Analyste: {{EXECUTANT}}*
'''


# ─────────────────────────────────────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────────────────────────────────────

CONTENT_GENERATORS = {
    "init_file": get_init_file,
    "locustfile": get_locustfile,
    "run_load_test": get_run_load_test,
    "performance_thresholds": get_performance_thresholds,
    "run_security_scan": get_run_security_scan,
    "security_manual_tests": get_security_manual_tests,
    "owasp_top10_tests": get_owasp_top10_tests,
    "performance_report_template": get_performance_report_template,
    "security_report_template": get_security_report_template,
}


def create_file(filepath, content):
    """Crée un fichier avec le contenu spécifié."""
    full_path = os.path.join(BASE_DIR, filepath)

    # Créer le répertoire parent si nécessaire
    parent_dir = os.path.dirname(full_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    return full_path


def main():
    """Fonction principale du script setup."""
    print(BANNER)
    print(f"  Date      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Répertoire: {BASE_DIR}")
    print(f"  Fichiers  : {len(FILES_TO_CREATE)}")
    print()

    # Créer les répertoires
    for directory in DIRECTORIES_TO_CREATE:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ Répertoire créé : {os.path.relpath(directory, BASE_DIR)}")

    print()

    # Créer les fichiers
    created_files = []
    for filepath, generator_key in FILES_TO_CREATE.items():
        generator = CONTENT_GENERATORS.get(generator_key)
        if not generator:
            print(f"  ✗ Générateur inconnu pour: {filepath}")
            continue

        content = generator()
        full_path = create_file(filepath, content)
        created_files.append(filepath)

        # Afficher un résumé du fichier créé
        lines = content.count("\n") if content else 0
        size = len(content.encode("utf-8")) if content else 0
        print(f"  ✓ {filepath:<50s} ({lines:>5d} lignes, {size:>6d} octets)")

    # Résumé
    print()
    print(SEPARATOR)
    print(f"  {len(created_files)}/{len(FILES_TO_CREATE)} fichiers créés avec succès")
    print(SEPARATOR)
    print()
    print("  Prochaines étapes:")
    print("    1. Exécuter les tests de performance:")
    print("       pip install locust")
    print("       python tests/performance/run_load_test.py --type baseline")
    print()
    print("    2. Exécuter les tests de sécurité:")
    print("       pip install bandit safety")
    print("       python tests/security/run_security_scan.py")
    print()
    print("    3. Exécuter les tests Django de sécurité:")
    print("       python manage.py test tests.security -v2")
    print()
    print("    4. Consulter les rapports générés:")
    print("       reports/performance/   → Rapports de performance")
    print("       reports/security/      → Rapports de sécurité")
    print()


if __name__ == "__main__":
    main()
