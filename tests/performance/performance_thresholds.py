"""
Seuils de performance pour les tests de charge NouvelAir — Jour 8.

Définit les temps de réponse maximum acceptables pour chaque endpoint,
classés par percentiles (p50, p95, p99).

Les seuils sont basés sur les bonnes pratiques d'UX:
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
        "p95": 3000,     # 95e percentile: 3 secondes (seuil d'acceptabilité)
        "p99": 5000,     # 99e percentile: 5 secondes (maximum toléré)
        "description": "Page d'accueil — requêtes DB pour destinations et vols",
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
        "p99": 1000,     # 99e percentile: 1 seconde (maximum pour l'UX)
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

# ── Mapping entre les noms d'endpoints et les tâches Locust ──────────────────

ENDPOINT_MAPPING = {
    "homepage": "/ [Homepage]",
    "search": "/recherche/ [Search Results]",
    "autocomplete": "/api/airports/autocomplete/",
    "destinations": "/destinations/",
    "promotions": "/promotions/",
    "login": "/accounts/connexion/ [POST]",
    "my_bookings": "/bookings/mes-reservations/",
    "booking_lookup": "/bookings/recherche/",
    "airports": "/flights/aeroports/",
}

# ── Seuils globaux ───────────────────────────────────────────────────────────

GLOBAL_THRESHOLDS = {
    "max_error_rate": 1.0,          # Taux d'erreur max: 1%
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
    Vérifie si les résultats d'un endpoint respectent les seuils.

    Args:
        endpoint: Nom de l'endpoint (clé dans THRESHOLDS)
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

    return "\n".join(lines)
