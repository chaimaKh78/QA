"""
Script de scan de sécurité automatisé — Jour 8.

Exécute plusieurs outils d'analyse de sécurité sur le projet NouvelAir:
    1. Bandit: analyse statique du code Python pour détecter les vulnérabilités
    2. Safety: vérification des dépendances contre les CVE connus
    3. Django checks: vérifications de sécurité intégrées à Django
    4. Tests manuels: CSRF, XSS, injection SQL, accès non autorisé

Dépendances:
    pip install bandit safety

Usage:
    cd D:/NouvelAirApp/nouvelair_project/    python tests/security/run_security_scan.py
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
    print("\n" + "=" * 72)
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
    Exécute Bandit pour l'analyse statique du code Python.

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

        for line in result.stdout.strip().split("\n"):
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
    - Validation du token CSRF sur la page d'accueil
    - Accès aux URL protégées sans authentification
    - Tentatives d'injection SQL via la recherche
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

    # ─ Test 1: CSRF Token sur la page d'accueil ─────────────────────────
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
    response = client.get("/bookings/mes-reservations/", follow=False)
    is_redirect = response.status_code == 302
    results.append({
        "test": "URL protégée sans auth (mes-réservations)",
        "passed": is_redirect,
        "detail": f"Status: {response.status_code} (attendu: 302)",
    })
    print(f"    {'✓' if is_redirect else '✗'} /mes-reservations/ → {response.status_code} ({'redirection OK' if is_redirect else 'ACCÈS DIRECT!'})")

    # ─ Test 2b: Profil sans auth ─────────────────────────────────────────
    response = client.get("/accounts/profil/", follow=False)
    is_redirect = response.status_code == 302
    results.append({
        "test": "URL protégée sans auth (profil)",
        "passed": is_redirect,
        "detail": f"Status: {response.status_code} (attendu: 302)",
    })
    print(f"    {'✓' if is_redirect else '✗'} /accounts/profil/ → {response.status_code} ({'redirection OK' if is_redirect else 'ACCÈS DIRECT!'})")

    # ─ Test 3: Injection SQL via recherche ──────────────────────────────
    print_step("Test: Injection SQL via recherche d'aéroport...")
    response = client.get("/api/airports/autocomplete/?q=' OR 1=1 --")
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
    response = client.get(f"/api/airports/autocomplete/?q={xss_payload}")
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

    print(f"\n  Résultat: {passed_count}/{total_count} tests réussis")


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

    print(f"\n  Rapport JSON: {report_path}")
    print(f"  Rapports HTML: {REPORTS_DIR}/")
    return report_path


# ── Point d'entrée principal ─────────────────────────────────────────────────

def main():
    """Point d'entrée principal."""
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

    print("\n" + "=" * 72)
    print("  Scan de sécurité terminé !")
    print("=" * 72 + "\n")


if __name__ == "__main__":
    main()
