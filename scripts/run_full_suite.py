#!/usr/bin/env python3
"""
scripts/run_full_suite.py - Exécution complète de la suite de tests
===================================================================
Script principal pour exécuter l'ensemble des tests du projet NouvelAir:
  1. Linting (flake8)
  2. Tests unitaires (pytest + couverture)
  3. Tests d'intégration (pytest)
  4. Tests BDD (behave)
  5. Rapport récapitulatif

Usage:
    python scripts/run_full_suite.py
    python scripts/run_full_suite.py --skip-bdd
    python scripts/run_full_suite.py --verbose

Auteurs: Équipe QA NouvelAir
Version: 1.0.0 - Jour 9
"""

import subprocess
import sys
import os
import time
from datetime import datetime

# Couleurs ANSI pour le terminal
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_header():
    """Affiche l'en-tête du script."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("=" * 70)
    print("  NouvelAir - Suite de Tests Complète")
    print(f"  Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 70)
    print(f"{Colors.END}\n")


def print_step(step_num, step_name):
    """Affiche l'en-tête d'une étape."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}[Étape {step_num}] {step_name}{Colors.END}")
    print("-" * 70)


def run_command(cmd, description, cwd=None):
    """
    Exécute une commande et retourne (success, output, elapsed_time).
    """
    start = time.time()
    print(f"  Exécution: {' '.join(cmd)}")
    print(f"  Description: {description}")

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True,
            text=True,
            timeout=300,
        )
        elapsed = time.time() - start
        success = result.returncode == 0
        return success, result.stdout + result.stderr, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return False, "TIMEOUT: Commande dépassée (> 300s)", elapsed
    except FileNotFoundError:
        elapsed = time.time() - start
        return False, f"Commande introuvable: {cmd[0]}", elapsed


def step1_flake8():
    """Étape 1: Vérification flake8."""
    print_step(1, "Linting - flake8")
    success, output, elapsed = run_command(
        ["flake8", ".", "--config=.flake8", "--count", "--statistics"],
        "Vérification du style de code avec flake8"
    )
    status = f"{Colors.GREEN}PASS{Colors.END}" if success else f"{Colors.RED}FAIL{Colors.END}"
    print(f"  Résultat: {status} ({elapsed:.1f}s)")
    if not success:
        # Afficher les erreurs mais tronquer si trop long
        lines = output.strip().split("\n")
        for line in lines[-20:]:
            print(f"    {line}")
    return success


def step2_unit_tests():
    """Étape 2: Tests unitaires avec couverture."""
    print_step(2, "Tests Unitaires - pytest avec couverture")
    success, output, elapsed = run_command(
        [
            "pytest", "tests/unit/", "-m", "unit",
            "--cov", "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-fail-under=80",
            "-v", "--tb=short",
        ],
        "Tests unitaires avec couverture minimale de 80%"
    )
    status = f"{Colors.GREEN}PASS{Colors.END}" if success else f"{Colors.RED}FAIL{Colors.END}"
    print(f"  Résultat: {status} ({elapsed:.1f}s)")

    # Extraire le pourcentage de couverture
    if "TOTAL" in output:
        for line in output.split("\n"):
            if "TOTAL" in line:
                print(f"  {line.strip()}")
                break
    return success


def step3_integration_tests():
    """Étape 3: Tests d'intégration."""
    print_step(3, "Tests d'Intégration - pytest")
    success, output, elapsed = run_command(
        [
            "pytest", "tests/integration/", "-m", "integration",
            "-v", "--tb=short", "--junitxml=integration-results.xml",
        ],
        "Tests d'intégration de tous les modules"
    )
    status = f"{Colors.GREEN}PASS{Colors.END}" if success else f"{Colors.RED}FAIL{Colors.END}"
    print(f"  Résultat: {status} ({elapsed:.1f}s)")
    return success


def step4_bdd_tests(skip_bdd=False):
    """Étape 4: Tests BDD avec behave."""
    print_step(4, "Tests BDD - behave")
    if skip_bdd:
        print(f"  {Colors.YELLOW}PASSÉ (skip-bdd activé){Colors.END}")
        return True

    success, output, elapsed = run_command(
        ["behave", "features/", "--tags=sprint1,sprint2", "-f", "pretty"],
        "Scénarios BDD pour les sprints 1 et 2"
    )
    status = f"{Colors.GREEN}PASS{Colors.END}" if success else f"{Colors.RED}FAIL{Colors.END}"
    print(f"  Résultat: {status} ({elapsed:.1f}s)")
    return success


def print_summary(results):
    """Affiche le récapitulatif final."""
    total_time = sum(r["time"] for r in results)
    all_passed = all(r["success"] for r in results)
    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed

    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("=" * 70)
    print("  RÉCAPITULATIF FINAL")
    print("=" * 70)
    print(f"{Colors.END}")

    print(f"  {'Étape':<50} {'Statut':<10} {'Durée':>8}")
    print(f"  {'-' * 50} {'-' * 10} {'-' * 8}")

    for result in results:
        status_icon = f"{Colors.GREEN}✅ PASS{Colors.END}" if result["success"] else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"  {result['name']:<50} {status_icon:<20} {result['time']:>6.1f}s")

    print(f"  {'-' * 50} {'-' * 10} {'-' * 8}")
    print(f"  {'':>50} {passed} passé(s), {failed} échoué(s), {total_time:.1f}s total")

    print()
    if all_passed:
        print(f"  {Colors.GREEN}{Colors.BOLD}🎉 Tous les tests sont passés !{Colors.END}")
        print(f"  {Colors.GREEN}Le projet est prêt pour la livraison.{Colors.END}")
    else:
        print(f"  {Colors.RED}{Colors.BOLD}❌ Certains tests ont échoué.{Colors.END}")
        print(f"  {Colors.YELLOW}Veuillez corriger les erreurs avant de continuer.{Colors.END}")

    print()
    print("=" * 70)
    return 0 if all_passed else 1


def main():
    """Point d'entrée principal."""
    skip_bdd = "--skip-bdd" in sys.argv

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nouvelair.settings")

    print_header()

    results = []

    # Étape 1: flake8
    success = step1_flake8()
    results.append({"name": "1. Linting (flake8)", "success": success, "time": 0})

    if not success:
        print(f"\n{Colors.YELLOW}⚠️  Le linting a échoué. Correction recommandée avant de continuer.{Colors.END}")

    # Étape 2: Tests unitaires
    success = step2_unit_tests()
    results.append({"name": "2. Tests unitaires (pytest + couverture)", "success": success, "time": 0})

    # Étape 3: Tests d'intégration
    success = step3_integration_tests()
    results.append({"name": "3. Tests d'intégration (pytest)", "success": success, "time": 0})

    # Étape 4: Tests BDD
    success = step4_bdd_tests(skip_bdd=skip_bdd)
    results.append({"name": "4. Tests BDD (behave)", "success": success, "time": 0})

    return print_summary(results)


if __name__ == "__main__":
    sys.exit(main())
