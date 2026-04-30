#!/usr/bin/env python3
"""
scripts/run_regression.py - Exécution rapide des tests de régression
=====================================================================
Script pour exécuter uniquement les tests marqués avec @pytest.mark.regression.
Génère un rapport JSON et un résumé HTML.

Usage:
    python scripts/run_regression.py
    python scripts/run_regression.py --json
    python scripts/run_regression.py --html
    python scripts/run_regression.py --output results/

Auteurs: Équipe QA NouvelAir
Version: 1.0.0 - Jour 9
"""

import subprocess
import sys
import os
import json
import argparse
from datetime import datetime

# Couleurs ANSI
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
END = "\033[0m"


def parse_args():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Exécute les tests de régression NouvelAir"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Générer un rapport JSON des résultats"
    )
    parser.add_argument(
        "--html", action="store_true",
        help="Générer un résumé HTML des résultats"
    )
    parser.add_argument(
        "--output", "-o", default=".",
        help="Répertoire de sortie pour les rapports (défaut: .)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Afficher les résultats détaillés"
    )
    return parser.parse_args()


def run_regression_tests(output_dir):
    """Exécute les tests de régression avec pytest."""
    os.makedirs(output_dir, exist_ok=True)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nouvelair.settings")

    # Construire la commande pytest
    cmd = [
        "pytest", "tests/test_regression.py",
        "-m", "regression",
        "-v", "--tb=short",
        f"--junitxml={os.path.join(output_dir, 'regression-results.xml')}",
    ]

    print(f"\n{BOLD}NouvelAir - Tests de Régression{END}")
    print(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Commande: {' '.join(cmd)}")
    print("-" * 60)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
    )

    output = result.stdout + result.stderr
    if args.verbose:
        print(output)

    return result.returncode == 0, output


def generate_json_report(output_dir, pytest_output):
    """Génère un rapport JSON à partir des résultats."""
    xml_path = os.path.join(output_dir, "regression-results.xml")

    # Analyser la sortie pytest pour extraire les résultats
    report = {
        "project": "NouvelAir",
        "suite": "Regression Tests",
        "timestamp": datetime.now().isoformat(),
        "results": [],
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
        },
    }

    # Parser la sortie pytest
    lines = pytest_output.split("\n")
    for line in lines:
        if " PASSED" in line or " FAILED" in line or " ERROR" in line or " SKIPPED" in line:
            parts = line.strip().split()
            test_name = parts[0] if parts else "unknown"

            status = "passed"
            if " FAILED" in line:
                status = "failed"
            elif " ERROR" in line:
                status = "error"
            elif " SKIPPED" in line:
                status = "skipped"

            report["results"].append({
                "test": test_name,
                "status": status,
            })
            report["summary"]["total"] += 1
            report["summary"][status + "d" if status != "passed" else "passed"] += 1

    json_path = os.path.join(output_dir, "regression_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n  Rapport JSON: {json_path}")
    return report


def generate_html_summary(report, output_dir):
    """Génère un résumé HTML des résultats."""
    summary = report["summary"]
    total = summary["total"]
    passed = summary["passed"]
    failed = summary["failed"]
    skipped = summary.get("skipped", 0)
    pct = (passed / total * 100) if total > 0 else 0

    if pct == 100:
        status_color = "#28a745"
        status_text = "TOUS LES TESTS PASSENT"
        status_emoji = "✅"
    elif pct >= 80:
        status_color = "#ffc107"
        status_text = "CERTAINS TESTS ONT ÉCHOUÉ"
        status_emoji = "⚠️"
    else:
        status_color = "#dc3545"
        status_text = "PLUSIEURS TESTS ONT ÉCHOUÉ"
        status_emoji = "❌"

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NouvelAir - Rapport de Régression</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            color: #333;
            padding: 40px 20px;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{
            color: #1a365d;
            margin-bottom: 8px;
            font-size: 28px;
        }}
        .timestamp {{
            color: #718096;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        .status-bar {{
            background: {status_color};
            color: white;
            padding: 16px 24px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 24px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .metric-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        .metric-value {{
            font-size: 36px;
            font-weight: bold;
        }}
        .metric-label {{
            color: #718096;
            font-size: 13px;
            margin-top: 4px;
        }}
        .metric-card.passed .metric-value {{ color: #28a745; }}
        .metric-card.failed .metric-value {{ color: #dc3545; }}
        .metric-card.skipped .metric-value {{ color: #ffc107; }}
        .metric-card.total .metric-value {{ color: #1a365d; }}
        .progress-bar {{
            background: #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            height: 12px;
            margin-bottom: 24px;
        }}
        .progress-fill {{
            height: 100%;
            background: {status_color};
            border-radius: 8px;
            transition: width 0.3s;
        }}
        .tests-list {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            overflow: hidden;
        }}
        .tests-list h2 {{
            padding: 16px 20px;
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
            font-size: 16px;
            color: #4a5568;
        }}
        .test-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 20px;
            border-bottom: 1px solid #f0f0f0;
            font-size: 14px;
        }}
        .test-item:last-child {{ border-bottom: none; }}
        .test-item .status {{
            font-weight: bold;
            font-size: 12px;
            padding: 2px 8px;
            border-radius: 4px;
        }}
        .status.passed {{ background: #c6f6d5; color: #22543d; }}
        .status.failed {{ background: #fed7d7; color: #742a2a; }}
        .status.error {{ background: #fefcbf; color: #744210; }}
        .status.skipped {{ background: #e9d8fd; color: #44337a; }}
        footer {{
            text-align: center;
            margin-top: 30px;
            color: #a0aec0;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>NouvelAir - Rapport de Régression</h1>
        <p class="timestamp">{report['timestamp'][:19].replace('T', ' à ')}</p>

        <div class="status-bar">{status_emoji} {status_text}</div>

        <div class="metrics">
            <div class="metric-card total">
                <div class="metric-value">{total}</div>
                <div class="metric-label">Total</div>
            </div>
            <div class="metric-card passed">
                <div class="metric-value">{passed}</div>
                <div class="metric-label">Réussis</div>
            </div>
            <div class="metric-card failed">
                <div class="metric-value">{failed}</div>
                <div class="metric-label">Échoués</div>
            </div>
            <div class="metric-card skipped">
                <div class="metric-value">{skipped}</div>
                <div class="metric-label">Ignorés</div>
            </div>
        </div>

        <div class="progress-bar">
            <div class="progress-fill" style="width: {pct:.1f}%"></div>
        </div>
        <p style="text-align:center; font-size:13px; color:#718096; margin-bottom:24px;">
            Couverture de régression: {pct:.1f}%
        </p>

        <div class="tests-list">
            <h2>Détail des tests ({total} tests)</h2>
"""

    for result in report["results"]:
        status_class = result["status"]
        if status_class == "error":
            status_label = "ERREUR"
        elif status_class == "failed":
            status_label = "ÉCHOUÉ"
        elif status_class == "skipped":
            status_label = "IGNORÉ"
        else:
            status_label = "RÉUSSI"
        html += f"""            <div class="test-item">
                <span>{result['test']}</span>
                <span class="status {status_class}">{status_label}</span>
            </div>
"""

    html += f"""        </div>

        <footer>
            Généré automatiquement par scripts/run_regression.py &mdash; NouvelAir QA
        </footer>
    </div>
</body>
</html>"""

    html_path = os.path.join(output_dir, "regression_report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Rapport HTML: {html_path}")


def main():
    """Point d'entrée principal."""
    global args
    args = parse_args()

    # Déterminer le répertoire de base du projet
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, args.output)

    # Exécuter les tests
    success, output = run_regression_tests(output_dir)

    # Afficher le résultat rapide
    if success:
        print(f"\n{GREEN}{BOLD}✅ Tous les tests de régression sont passés !{END}")
    else:
        print(f"\n{RED}{BOLD}❌ Certains tests de régression ont échoué.{END}")

    # Générer les rapports
    if args.json or args.html:
        print(f"\n{BOLD}Génération des rapports:{END}")
        report = generate_json_report(output_dir, output)

        if args.html:
            generate_html_summary(report, output_dir)

        print()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
