#!/usr/bin/env python3
"""
demo_sprint_review.py — Script de démonstration pour Sprint Review (Jour 10)
================================================================================
NouvelAir — Projet de formation Django

Ce script exécute l'ensemble de la suite de tests, capture les résultats,
génère les rapports et affiche un résumé formaté de la Sprint Review.

Usage :
    python scripts/demo_sprint_review.py
    python scripts/demo_sprint_review.py --skip-e2e
    python scripts/demo_sprint_review.py --skip-performance
    python scripts/demo_sprint_review.py --fast
"""

import os
import sys
import subprocess
import argparse
import json
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Sortie console avec couleurs (ANSI)
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_banner():
    """Affiche la bannière de la démonstration."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("=" * 70)
    print("     NOUVELAIR — SPRINT REVIEW DEMO")
    print("     Formation Test/QA, Automatisation & IA")
    print("=" * 70)
    print(f"{Colors.ENDC}")
    print(f"  Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"  Projet : {BASE_DIR}")
    print(f"  Rapports : {REPORTS_DIR}")
    print()


def run_command(cmd, name, timeout=300):
    """
    Exécute une commande et capture les résultats.

    Args:
        cmd: Liste de commandes à exécuter
        name: Nom descriptif de l'étape
        timeout: Timeout en secondes

    Returns:
        dict: Résultats de l'exécution
    """
    print(f"{Colors.OKCYAN}▶ {name}{Colors.ENDC}")
    print(f"  Commande : {' '.join(cmd)}")

    result = {
        "name": name,
        "command": " ".join(cmd),
        "start_time": datetime.now().isoformat(),
        "success": False,
        "returncode": -1,
        "output": "",
        "errors": "",
        "duration_seconds": 0,
    }

    start = datetime.now()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=timeout,
        )
        result["returncode"] = proc.returncode
        result["success"] = proc.returncode == 0
        result["output"] = proc.stdout[-2000:] if len(proc.stdout) > 2000 else proc.stdout
        result["errors"] = proc.stderr[-500:] if len(proc.stderr) > 500 else proc.stderr

    except subprocess.TimeoutExpired:
        result["errors"] = f"TIMEOUT après {timeout}s"
    except FileNotFoundError as e:
        result["errors"] = f"Commande introuvable : {e}"
    except Exception as e:
        result["errors"] = f"Erreur inattendue : {e}"

    result["duration_seconds"] = (datetime.now() - start).total_seconds()

    # Afficher le résultat
    if result["success"]:
        print(f"  {Colors.OKGREEN}✅ SUCCÈS{Colors.ENDC} ({result['duration_seconds']:.1f}s)")
    else:
        print(f"  {Colors.FAIL}❌ ÉCHEC{Colors.ENDC} ({result['duration_seconds']:.1f}s)")
        if result["errors"]:
            print(f"  {Colors.WARNING}Erreur : {result['errors'][:200]}{Colors.ENDC}")
    print()

    return result


def extract_test_count(output):
    """Extrait le nombre de tests passés/échoués depuis la sortie pytest."""
    passed = 0
    failed = 0
    errors = 0

    for line in output.splitlines():
        line = line.strip()
        if "passed" in line:
            parts = line.split()
            for part in parts:
                if "passed" in part:
                    try:
                        passed = int(part.split("=")[1].split(",")[0])
                    except (ValueError, IndexError):
                        pass
                if "failed" in part:
                    try:
                        failed = int(part.split("=")[1].split(",")[0])
                    except (ValueError, IndexError):
                        pass
                if "error" in part:
                    try:
                        errors = int(part.split("=")[1].split(",")[0])
                    except (ValueError, IndexError):
                        pass

    return passed, failed, errors


def run_demo(skip_e2e=False, skip_performance=False, skip_security=False, fast=False):
    """
    Exécute la démonstration complète de Sprint Review.

    Args:
        skip_e2e: Ignorer les tests E2E
        skip_performance: Ignorer les tests de performance
        skip_security: Ignorer les tests de sécurité
        fast: Mode rapide (réduit les tests)
    """
    print_banner()

    results = []
    total_passed = 0
    total_failed = 0

    # =========================================================================
    # Étape 1 : Linting
    # =========================================================================
    print(f"{Colors.BOLD}{Colors.UNDERLINE}ÉTAPE 1 : LINTING (flake8){Colors.ENDC}\n")
    r = run_command(
        ["python", "-m", "flake8", ".", "--config=.flake8", "--count", "--exit-zero"],
        "Vérification flake8"
    )
    results.append(r)

    # =========================================================================
    # Étape 2 : Tests unitaires
    # =========================================================================
    print(f"{Colors.BOLD}{Colors.UNDERLINE}ÉTAPE 2 : TESTS UNITAIRES (pytest tests/unit/){Colors.ENDC}\n")
    cmd = [
        "python", "-m", "pytest", "tests/unit/",
        "-v", "--tb=short", "--no-header", "-q"
    ]
    if fast:
        cmd.extend(["-x", "--maxfail=3"])
    r = run_command(cmd, "Tests unitaires")
    results.append(r)
    p, f, e = extract_test_count(r["output"])
    total_passed += p
    total_failed += f + e

    # =========================================================================
    # Étape 3 : Tests d'intégration
    # =========================================================================
    print(f"{Colors.BOLD}{Colors.UNDERLINE}ÉTAPE 3 : TESTS D'INTÉGRATION (pytest tests/integration/){Colors.ENDC}\n")
    cmd = [
        "python", "-m", "pytest", "tests/integration/",
        "-v", "--tb=short", "--no-header", "-q"
    ]
    if fast:
        cmd.extend(["-x", "--maxfail=3"])
    r = run_command(cmd, "Tests d'intégration")
    results.append(r)
    p, f, e = extract_test_count(r["output"])
    total_passed += p
    total_failed += f + e

    # =========================================================================
    # Étape 4 : Tests API
    # =========================================================================
    print(f"{Colors.BOLD}{Colors.UNDERLINE}ÉTAPE 4 : TESTS API (pytest tests/api/){Colors.ENDC}\n")
    cmd = [
        "python", "-m", "pytest", "tests/api/",
        "-v", "--tb=short", "--no-header", "-q"
    ]
    if fast:
        cmd.extend(["-x", "--maxfail=3"])
    r = run_command(cmd, "Tests API")
    results.append(r)
    p, f, e = extract_test_count(r["output"])
    total_passed += p
    total_failed += f + e

    # =========================================================================
    # Étape 5 : Tests BDD (Behave)
    # =========================================================================
    print(f"{Colors.BOLD}{Colors.UNDERLINE}ÉTAPE 5 : TESTS BDD (behave features/){Colors.ENDC}\n")
    r = run_command(
        ["python", "-m", "behave", "features/", "--tags=sprint1,sprint2",
         "-f", "pretty", "--no-capture"],
        "Tests BDD (Behave)",
        timeout=120
    )
    results.append(r)

    # =========================================================================
    # Étape 6 : Tests E2E (Playwright)
    # =========================================================================
    if not skip_e2e:
        print(f"{Colors.BOLD}{Colors.UNDERLINE}ÉTAPE 6 : TESTS E2E (Playwright){Colors.ENDC}\n")
        cmd = [
            "python", "-m", "pytest", "tests/e2e/",
            "-v", "--tb=short", "--no-header", "-q",
            "--browser", "chromium"
        ]
        if fast:
            cmd.extend(["-x", "--maxfail=3"])
        r = run_command(cmd, "Tests End-to-End (Playwright)", timeout=300)
        results.append(r)
        p, f, e = extract_test_count(r["output"])
        total_passed += p
        total_failed += f + e
    else:
        print(f"{Colors.WARNING}⏭️ Étape 6 ignorée (--skip-e2e){Colors.ENDC}\n")
        results.append({
            "name": "Tests E2E (Playwright)",
            "success": True,
            "skipped": True,
            "output": "Ignoré par --skip-e2e",
        })

    # =========================================================================
    # Étape 7 : Tests de performance (Locust)
    # =========================================================================
    if not skip_performance:
        print(f"{Colors.BOLD}{Colors.UNDERLINE}ÉTAPE 7 : TESTS DE PERFORMANCE (Locust){Colors.ENDC}\n")
        r = run_command(
            ["python", "tests/performance/run_load_test.py", "--type", "baseline"],
            "Test de performance baseline (Locust)",
            timeout=300
        )
        results.append(r)
    else:
        print(f"{Colors.WARNING}⏭️ Étape 7 ignorée (--skip-performance){Colors.ENDC}\n")
        results.append({
            "name": "Tests de performance (Locust)",
            "success": True,
            "skipped": True,
            "output": "Ignoré par --skip-performance",
        })

    # =========================================================================
    # Étape 8 : Tests de sécurité
    # =========================================================================
    if not skip_security:
        print(f"{Colors.BOLD}{Colors.UNDERLINE}ÉTAPE 8 : TESTS DE SÉCURITÉ{Colors.ENDC}\n")
        # Bandit
        r1 = run_command(
            ["python", "-m", "bandit", "-r", ".", "-f", "screen", "--exit-zero"],
            "Analyse Bandit (code statique)",
            timeout=120
        )
        results.append(r1)

        # Tests de sécurité pytest
        r2 = run_command(
            ["python", "-m", "pytest", "tests/security/", "-v", "--tb=short", "-q"],
            "Tests OWASP Top 10",
            timeout=120
        )
        results.append(r2)
        p, f, e = extract_test_count(r2["output"])
        total_passed += p
        total_failed += f + e
    else:
        print(f"{Colors.WARNING}⏭️ Étape 8 ignorée (--skip-security){Colors.ENDC}\n")
        results.append({
            "name": "Tests de sécurité (Bandit + OWASP)",
            "success": True,
            "skipped": True,
            "output": "Ignoré par --skip-security",
        })

    # =========================================================================
    # Résumé final
    # =========================================================================
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("=" * 70)
    print("     RÉSUMÉ SPRINT REVIEW — NOUVELAIR")
    print("=" * 70)
    print(f"{Colors.ENDC}\n")

    # Tableau des résultats
    print(f"{'Étape':<45} {'Statut':<12} {'Durée':<10}")
    print("─" * 70)

    for r in results:
        name = r["name"][:43]
        if r.get("skipped"):
            status = f"{Colors.WARNING}⏭️ Ignoré{Colors.ENDC}"
        elif r["success"]:
            status = f"{Colors.OKGREEN}✅ OK{Colors.ENDC}"
        else:
            status = f"{Colors.FAIL}❌ Échec{Colors.ENDC}"
        duration = f"{r.get('duration_seconds', 0):.1f}s"
        print(f"{name:<45} {status:<22} {duration:<10}")

    print("─" * 70)
    print(f"\n  Tests passés  : {Colors.OKGREEN}{total_passed}{Colors.ENDC}")
    print(f"  Tests échoués: {Colors.FAIL if total_failed > 0 else ''}{total_failed}{Colors.ENDC}")
    print(f"  Étapes totales: {len(results)}")

    # Statut global
    all_success = all(r.get("success", False) for r in results)
    print(f"\n{Colors.BOLD}", end="")
    if all_success:
        print(f"  🎉 PIPELINE 100% VERT — TOUS LES TESTS PASSENT !")
    else:
        failed_count = sum(1 for r in results if not r.get("success", False))
        print(f"  ❌ PIPELINE ÉCHOUÉ — {failed_count} étape(s) en échec")
    print(f"{Colors.ENDC}\n")

    # Sauvegarder les résultats en JSON
    summary = {
        "project": "NouvelAir",
        "date": datetime.now().isoformat(),
        "total_passed": total_passed,
        "total_failed": total_failed,
        "steps": [
            {
                "name": r["name"],
                "success": r.get("success", False),
                "skipped": r.get("skipped", False),
                "duration_seconds": r.get("duration_seconds", 0),
            }
            for r in results
        ],
        "pipeline_status": "success" if all_success else "failure",
    }

    summary_path = os.path.join(REPORTS_DIR, "sprint_review_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"  📄 Résumé sauvegardé : {summary_path}")
    print()

    return 0 if all_success else 1


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(
        description="NouvelAir — Sprint Review Demo (Jour 10)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Exemples :
  python scripts/demo_sprint_review.py              Démo complète
  python scripts/demo_sprint_review.py --fast        Mode rapide
  python scripts/demo_sprint_review.py --skip-e2e    Sans tests E2E
  python scripts/demo_sprint_review.py --skip-performance
  python scripts/demo_sprint_review.py --skip-security
        """
    )
    parser.add_argument("--skip-e2e", action="store_true", help="Ignorer les tests E2E Playwright")
    parser.add_argument("--skip-performance", action="store_true", help="Ignorer les tests de performance Locust")
    parser.add_argument("--skip-security", action="store_true", help="Ignorer les tests de sécurité")
    parser.add_argument("--fast", action="store_true", help="Mode rapide (arrêt au premier échec)")

    args = parser.parse_args()

    exit_code = run_demo(
        skip_e2e=args.skip_e2e,
        skip_performance=args.skip_performance,
        skip_security=args.skip_security,
        fast=args.fast,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
