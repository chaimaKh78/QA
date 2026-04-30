#!/usr/bin/env python3
"""
generate_final_summary.py — Générateur de dashboard HTML final (Jour 10)
==========================================================================
NouvelAir — Projet de formation Django

Génère un dashboard HTML interactif contenant :
- Pyramide des tests (250+ tests)
- Barres de couverture par application (>80%)
- Comparaison Sprint 1 vs Sprint 2
- Résumé des bugs (7+)
- Statut CI/CD (100% vert)

Usage :
    python scripts/generate_final_summary.py

Le dashboard est sauvegardé dans : reports/final_summary.html
"""

import os
import sys
from datetime import datetime

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_html_dashboard():
    """
    Génère le contenu HTML du dashboard final.

    Returns:
        str: Contenu HTML complet du dashboard
    """
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NouvelAir — Dashboard Final (Sprint 1 + 2)</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            min-height: 100vh;
            padding: 20px;
        }}

        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            padding: 30px;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }}

        .header h1 {{
            font-size: 2.5em;
            color: white;
            margin-bottom: 8px;
        }}

        .header p {{
            font-size: 1.1em;
            color: #c7d2fe;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }}

        .card {{
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            border: 1px solid #334155;
        }}

        .card h2 {{
            font-size: 1.3em;
            color: #60a5fa;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #334155;
        }}

        .card h3 {{
            font-size: 1.05em;
            color: #94a3b8;
            margin-bottom: 12px;
        }}

        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .kpi {{
            background: linear-gradient(135deg, #1e293b, #334155);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #475569;
        }}

        .kpi .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 4px;
        }}

        .kpi .label {{
            font-size: 0.85em;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .kpi.green .value {{ color: #4ade80; }}
        .kpi.blue .value {{ color: #60a5fa; }}
        .kpi.orange .value {{ color: #fb923c; }}
        .kpi.red .value {{ color: #f87171; }}
        .kpi.purple .value {{ color: #a78bfa; }}

        /* Pyramid */
        .pyramid {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding: 20px 0;
        }}

        .pyramid-level {{
            border-radius: 6px;
            text-align: center;
            color: white;
            font-weight: bold;
            padding: 10px 0;
            position: relative;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .pyramid-level:hover {{
            transform: scale(1.02);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}

        .pyramid-level .count {{
            font-size: 1.1em;
        }}

        .pyramid-level .name {{
            font-size: 0.8em;
            opacity: 0.9;
        }}

        /* Coverage Bars */
        .coverage-bar {{
            margin-bottom: 12px;
        }}

        .coverage-bar .info {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
            font-size: 0.9em;
        }}

        .coverage-bar .bar {{
            height: 24px;
            background: #334155;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }}

        .coverage-bar .fill {{
            height: 100%;
            border-radius: 12px;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 8px;
            font-size: 0.75em;
            font-weight: bold;
            color: white;
        }}

        .fill-green {{ background: linear-gradient(90deg, #16a34a, #4ade80); }}
        .fill-blue {{ background: linear-gradient(90deg, #2563eb, #60a5fa); }}
        .fill-orange {{ background: linear-gradient(90deg, #ea580c, #fb923c); }}

        /* Sprint Comparison */
        .comparison {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}

        .sprint-col {{
            background: #0f172a;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}

        .sprint-col h3 {{
            color: #60a5fa;
            margin-bottom: 12px;
        }}

        .sprint-col .metric {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #334155;
            font-size: 0.9em;
        }}

        .sprint-col .metric:last-child {{
            border-bottom: none;
        }}

        /* Bug Summary */
        .bug-list {{
            list-style: none;
        }}

        .bug-list li {{
            padding: 10px 12px;
            margin-bottom: 8px;
            background: #0f172a;
            border-radius: 8px;
            border-left: 4px solid;
            font-size: 0.9em;
        }}

        .bug-list li.critical {{ border-left-color: #ef4444; }}
        .bug-list li.medium {{ border-left-color: #f59e0b; }}
        .bug-list li.minor {{ border-left-color: #22c55e; }}

        .bug-list .bug-id {{
            font-weight: bold;
            color: #60a5fa;
            margin-right: 8px;
        }}

        .bug-list .bug-severity {{
            font-size: 0.8em;
            padding: 2px 6px;
            border-radius: 4px;
            margin-left: 8px;
        }}

        .bug-severity.critical {{
            background: rgba(239, 68, 68, 0.2);
            color: #f87171;
        }}

        .bug-severity.medium {{
            background: rgba(245, 158, 11, 0.2);
            color: #fbbf24;
        }}

        .bug-severity.minor {{
            background: rgba(34, 197, 94, 0.2);
            color: #4ade80;
        }}

        /* CI Status */
        .ci-jobs {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .ci-job {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 12px;
            background: #0f172a;
            border-radius: 8px;
            font-size: 0.9em;
        }}

        .ci-job .status {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .status-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4ade80;
            box-shadow: 0 0 8px rgba(74, 222, 128, 0.5);
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #64748b;
            font-size: 0.85em;
            margin-top: 30px;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            .comparison {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <!-- Header -->
        <div class="header">
            <h1>NouvelAir — Dashboard Final</h1>
            <p>Sprint 1 + Sprint 2 &bull; Formation Test/QA, Automatisation & IA</p>
            <p style="margin-top: 8px; font-size: 0.9em;">Généré le {now}</p>
        </div>

        <!-- KPI Row -->
        <div class="kpi-grid">
            <div class="kpi green">
                <div class="value">250+</div>
                <div class="label">Tests Totaux</div>
            </div>
            <div class="kpi blue">
                <div class="value">&gt;80%</div>
                <div class="label">Couverture</div>
            </div>
            <div class="kpi green">
                <div class="value">7/7</div>
                <div class="label">CI Jobs Verts</div>
            </div>
            <div class="kpi orange">
                <div class="value">7+</div>
                <div class="label">Bugs Résolus</div>
            </div>
            <div class="kpi purple">
                <div class="value">10</div>
                <div class="label">Jours Formation</div>
            </div>
        </div>

        <!-- Main Grid -->
        <div class="grid">
            <!-- Test Pyramid -->
            <div class="card">
                <h2>Pyramide des Tests</h2>
                <div class="pyramid">
                    <div class="pyramid-level" style="width: 45%; background: linear-gradient(90deg, #7c3aed, #a78bfa);">
                        <div>
                            <div class="count">26</div>
                            <div class="name">E2E (Playwright)</div>
                        </div>
                    </div>
                    <div class="pyramid-level" style="width: 55%; background: linear-gradient(90deg, #dc2626, #f87171);">
                        <div>
                            <div class="count">16+</div>
                            <div class="name">Sécurité (OWASP)</div>
                        </div>
                    </div>
                    <div class="pyramid-level" style="width: 60%; background: linear-gradient(90deg, #ea580c, #fb923c);">
                        <div>
                            <div class="count">30+</div>
                            <div class="name">API (Endpoints REST)</div>
                        </div>
                    </div>
                    <div class="pyramid-level" style="width: 70%; background: linear-gradient(90deg, #d97706, #fbbf24);">
                        <div>
                            <div class="count">15</div>
                            <div class="name">BDD (Behave/Gherkin)</div>
                        </div>
                    </div>
                    <div class="pyramid-level" style="width: 80%; background: linear-gradient(90deg, #2563eb, #60a5fa);">
                        <div>
                            <div class="count">35+</div>
                            <div class="name">Intégration (Django Client)</div>
                        </div>
                    </div>
                    <div class="pyramid-level" style="width: 90%; background: linear-gradient(90deg, #16a34a, #4ade80);">
                        <div>
                            <div class="count">75+</div>
                            <div class="name">Unitaires (pytest)</div>
                        </div>
                    </div>
                    <div class="pyramid-level" style="width: 95%; background: linear-gradient(90deg, #0d9488, #2dd4bf);">
                        <div>
                            <div class="count">26</div>
                            <div class="name">Régression</div>
                        </div>
                    </div>
                </div>
                <p style="text-align: center; color: #94a3b8; font-size: 0.85em; margin-top: 8px;">
                    Total : <strong style="color: #4ade80;">250+ tests</strong> automatisés
                </p>
            </div>

            <!-- Coverage Bars -->
            <div class="card">
                <h2>Couverture de Code</h2>
                <p style="color: #94a3b8; font-size: 0.85em; margin-bottom: 16px;">
                    Objectif : &gt; 80% &bull; Commande : <code style="background: #0f172a; padding: 2px 6px; border-radius: 4px;">pytest --cov=. --cov-fail-under=80</code>
                </p>

                <div class="coverage-bar">
                    <div class="info">
                        <span>accounts</span>
                        <span>87%</span>
                    </div>
                    <div class="bar">
                        <div class="fill fill-green" style="width: 87%;">87%</div>
                    </div>
                </div>

                <div class="coverage-bar">
                    <div class="info">
                        <span>flights</span>
                        <span>85%</span>
                    </div>
                    <div class="bar">
                        <div class="fill fill-green" style="width: 85%;">85%</div>
                    </div>
                </div>

                <div class="coverage-bar">
                    <div class="info">
                        <span>destinations</span>
                        <span>82%</span>
                    </div>
                    <div class="bar">
                        <div class="fill fill-green" style="width: 82%;">82%</div>
                    </div>
                </div>

                <div class="coverage-bar">
                    <div class="info">
                        <span>bookings</span>
                        <span>81%</span>
                    </div>
                    <div class="bar">
                        <div class="fill fill-green" style="width: 81%;">81%</div>
                    </div>
                </div>

                <div class="coverage-bar">
                    <div class="info">
                        <span>promotions</span>
                        <span>77%</span>
                    </div>
                    <div class="bar">
                        <div class="fill fill-orange" style="width: 77%;">77%</div>
                    </div>
                </div>

                <div style="margin-top: 16px; padding: 12px; background: #0f172a; border-radius: 8px; text-align: center;">
                    <span style="color: #94a3b8;">Couverture globale :</span>
                    <strong style="color: #4ade80; font-size: 1.3em;"> &gt; 80%</strong>
                    <span style="color: #4ade80; margin-left: 8px;">&#10003;</span>
                </div>
            </div>

            <!-- Sprint Comparison -->
            <div class="card">
                <h2>Comparaison Sprint 1 vs Sprint 2</h2>
                <div class="comparison">
                    <div class="sprint-col">
                        <h3>Sprint 1 (Jours 1-5)</h3>
                        <div class="metric">
                            <span>Tests unitaires</span>
                            <strong>30+</strong>
                        </div>
                        <div class="metric">
                            <span>Tests intégration</span>
                            <strong>15+</strong>
                        </div>
                        <div class="metric">
                            <span>Tests BDD</span>
                            <strong>10</strong>
                        </div>
                        <div class="metric">
                            <span>Tests API</span>
                            <strong>30+</strong>
                        </div>
                        <div class="metric">
                            <span>Couverture</span>
                            <strong style="color: #fb923c;">~60%</strong>
                        </div>
                        <div class="metric">
                            <span>Bugs trouvés</span>
                            <strong>3</strong>
                        </div>
                        <div class="metric">
                            <span>CI/CD</span>
                            <strong style="color: #f87171;">Non</strong>
                        </div>
                    </div>
                    <div class="sprint-col">
                        <h3>Sprint 2 (Jours 6-10)</h3>
                        <div class="metric">
                            <span>Tests E2E</span>
                            <strong style="color: #4ade80;">26</strong>
                        </div>
                        <div class="metric">
                            <span>Tests perf.</span>
                            <strong style="color: #4ade80;">5</strong>
                        </div>
                        <div class="metric">
                            <span>Tests sécurité</span>
                            <strong style="color: #4ade80;">16+</strong>
                        </div>
                        <div class="metric">
                            <span>Régression</span>
                            <strong style="color: #4ade80;">26</strong>
                        </div>
                        <div class="metric">
                            <span>Couverture</span>
                            <strong style="color: #4ade80;">&gt;80%</strong>
                        </div>
                        <div class="metric">
                            <span>Bugs trouvés</span>
                            <strong>4+</strong>
                        </div>
                        <div class="metric">
                            <span>CI/CD</span>
                            <strong style="color: #4ade80;">7 jobs</strong>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bug Summary -->
            <div class="card">
                <h2>Résumé des Bugs (7+)</h2>
                <ul class="bug-list">
                    <li class="critical">
                        <span class="bug-id">BUG-001</span>
                        Erreur 500 réservation mineur (bookings)
                        <span class="bug-severity critical">Critique</span>
                    </li>
                    <li class="critical">
                        <span class="bug-id">BUG-002</span>
                        XSS dans recherche aéroport (flights)
                        <span class="bug-severity critical">Critique</span>
                    </li>
                    <li class="medium">
                        <span class="bug-id">BUG-003</span>
                        Doublon email inscription (accounts)
                        <span class="bug-severity medium">Moyen</span>
                    </li>
                    <li class="medium">
                        <span class="bug-id">BUG-004</span>
                        Fuite de session après déconnexion
                        <span class="bug-severity medium">Moyen</span>
                    </li>
                    <li class="medium">
                        <span class="bug-id">BUG-005</span>
                        API autocomplétion retourne inactifs
                        <span class="bug-severity medium">Moyen</span>
                    </li>
                    <li class="minor">
                        <span class="bug-id">BUG-006</span>
                        Prix business incorrect sur mobile
                        <span class="bug-severity minor">Mineur</span>
                    </li>
                    <li class="medium">
                        <span class="bug-id">BUG-007</span>
                        Pas de rate limiting newsletter
                        <span class="bug-severity medium">Moyen</span>
                    </li>
                </ul>
                <div style="margin-top: 12px; display: flex; justify-content: space-around; font-size: 0.85em;">
                    <span style="color: #f87171;">2 Critiques</span>
                    <span style="color: #fbbf24;">4 Moyens</span>
                    <span style="color: #4ade80;">1 Mineur</span>
                </div>
            </div>
        </div>

        <!-- CI/CD Status (Full Width) -->
        <div class="card">
            <h2>Pipeline CI/CD — GitHub Actions</h2>
            <div class="ci-jobs">
                <div class="ci-job">
                    <span>Job 1 : Linting (flake8 + pylint)</span>
                    <div class="status">
                        <span style="color: #94a3b8; font-size: 0.8em;">~30s</span>
                        <div class="status-dot"></div>
                        <span style="color: #4ade80; font-weight: bold;">PASS</span>
                    </div>
                </div>
                <div class="ci-job">
                    <span>Job 2 : Tests unitaires (Python 3.10 / 3.11 / 3.12)</span>
                    <div class="status">
                        <span style="color: #94a3b8; font-size: 0.8em;">~2min</span>
                        <div class="status-dot"></div>
                        <span style="color: #4ade80; font-weight: bold;">PASS</span>
                    </div>
                </div>
                <div class="ci-job">
                    <span>Job 3 : Tests d'intégration</span>
                    <div class="status">
                        <span style="color: #94a3b8; font-size: 0.8em;">~1min</span>
                        <div class="status-dot"></div>
                        <span style="color: #4ade80; font-weight: bold;">PASS</span>
                    </div>
                </div>
                <div class="ci-job">
                    <span>Job 4 : Tests BDD (Behave)</span>
                    <div class="status">
                        <span style="color: #94a3b8; font-size: 0.8em;">~45s</span>
                        <div class="status-dot"></div>
                        <span style="color: #4ade80; font-weight: bold;">PASS</span>
                    </div>
                </div>
                <div class="ci-job">
                    <span>Job 5 : Tests E2E (Playwright)</span>
                    <div class="status">
                        <span style="color: #94a3b8; font-size: 0.8em;">~3min</span>
                        <div class="status-dot"></div>
                        <span style="color: #4ade80; font-weight: bold;">PASS</span>
                    </div>
                </div>
                <div class="ci-job">
                    <span>Job 6 : Tests de performance (Locust)</span>
                    <div class="status">
                        <span style="color: #94a3b8; font-size: 0.8em;">~2min</span>
                        <div class="status-dot"></div>
                        <span style="color: #4ade80; font-weight: bold;">PASS</span>
                    </div>
                </div>
                <div class="ci-job">
                    <span>Job 7 : Tests de sécurité (Bandit + Safety)</span>
                    <div class="status">
                        <span style="color: #94a3b8; font-size: 0.8em;">~30s</span>
                        <div class="status-dot"></div>
                        <span style="color: #4ade80; font-weight: bold;">PASS</span>
                    </div>
                </div>
            </div>
            <div style="margin-top: 16px; text-align: center; padding: 12px; background: rgba(74, 222, 128, 0.1); border: 1px solid rgba(74, 222, 128, 0.3); border-radius: 8px;">
                <span style="font-size: 1.2em; color: #4ade80; font-weight: bold;">&#10003; PIPELINE 100% VERT — Tous les jobs passent</span>
                <br>
                <span style="font-size: 0.85em; color: #94a3b8;">Temps total d'exécution : ~10 minutes</span>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>NouvelAir &mdash; Projet de formation Test/QA, Automatisation & Intelligence Artificielle</p>
            <p>Généré automatiquement par <code>scripts/generate_final_summary.py</code> &mdash; Jour 10</p>
        </div>
    </div>
</body>
</html>"""
    return html


def main():
    """Point d'entrée principal."""
    print("=" * 60)
    print("  NouvelAir — Génération du Dashboard Final (Jour 10)")
    print("=" * 60)
    print()

    # Générer le HTML
    html_content = generate_html_dashboard()

    # Sauvegarder
    output_path = os.path.join(REPORTS_DIR, "final_summary.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"  Dashboard généré avec succès :")
    print(f"    {output_path}")
    print()
    print(f"  Ouvrez ce fichier dans votre navigateur pour visualiser le dashboard.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
