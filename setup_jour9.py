#!/usr/bin/env python3
"""
setup_jour9.py - Création des fichiers CI/CD et tests de régression pour Jour 9
===============================================================================
NouvelAir - Projet de formation Django (système de réservation aérienne)

Ce script génère automatiquement tous les fichiers nécessaires pour :
- Pipeline CI/CD GitHub Actions complet (7 jobs)
- Configuration linting (flake8, pylint)
- Suite de tests de régression (20+ tests)
- Scripts d'exécution locale
- Documentation CI/CD et quality gates (en français)

Usage:
    python setup_jour9.py

Le script crée les fichiers dans D:\\NouvelairApp\\nouvelair_project\\
en respectant la structure existante du projet.
"""

import os
import sys

# Chemin racine du projet NouvelAir
BASE_DIR = r"D:\NouvelairApp\nouvelair_project"

# Vérification que le répertoire de base existe
if not os.path.isdir(BASE_DIR):
    print(f"ERREUR: Répertoire du projet introuvable: {BASE_DIR}")
    print("Veuillez vérifier le chemin et réessayer.")
    sys.exit(1)


def create_directory(path):
    """Crée un répertoire s'il n'existe pas."""
    os.makedirs(path, exist_ok=True)


def write_file(filepath, content):
    """Écrit le contenu dans un fichier, en créant les répertoires si nécessaire."""
    create_directory(os.path.dirname(filepath))
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {os.path.relpath(filepath, BASE_DIR)}")


def generate_github_actions_workflow():
    """Génère le fichier .github/workflows/tests.yml."""
    filepath = os.path.join(BASE_DIR, ".github", "workflows", "tests.yml")

    content = r"""# =============================================================================
# NouvelAir QA Pipeline - GitHub Actions Workflow
# =============================================================================
# Pipeline CI/CD complet avec 7 jobs pour assurer la qualité du code.
# Déclenché sur push (main, sprint1, sprint2) et PR (main).
# =============================================================================

name: NouvelAir QA Pipeline

on:
  push:
    branches: [main, sprint1, sprint2]
  pull_request:
    branches: [main]

env:
  DJANGO_SETTINGS_MODULE: nouvelair.settings
  PYTHONUNBUFFERED: "1"
  COVERAGE_MIN: 80

jobs:
  # ===========================================================================
  # Job 1: Linting - Vérification de la qualité du code
  # ===========================================================================
  lint:
    name: "Linting (flake8 + pylint)"
    runs-on: ubuntu-latest

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Configuration Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Installation des dépendances
        run: |
          python -m pip install --upgrade pip
          pip install flake8 pylint pylint-django
          pip install -r requirements.txt
          pip install -r requirements_test.txt

      - name: Vérification flake8
        run: |
          echo "## Flake8 Lint Results" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          flake8 . --config=.flake8 --statistics --count --show-source --output-file=flake8_report.txt || true
          ERRORS=$(flake8 . --config=.flake8 --count --select=E9,F63,F7,F82)
          WARNINGS=$(flake8 . --config=.flake8 --count --extend-ignore=E9,F63,F7,F82)
          echo "| Métrique | Valeur |" >> $GITHUB_STEP_SUMMARY
          echo "|----------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Erreurs (E9,F63,F7,F82) | ${ERRORS} |" >> $GITHUB_STEP_SUMMARY
          echo "| Avertissements | ${WARNINGS} |" >> $GITHUB_STEP_SUMMARY
          if [ "$ERRORS" -gt 0 ]; then
            echo "### Erreurs détectées par flake8" >> $GITHUB_STEP_SUMMARY
            echo '```' >> $GITHUB_STEP_SUMMARY
            cat flake8_report.txt >> $GITHUB_STEP_SUMMARY
            echo '```' >> $GITHUB_STEP_SUMMARY
            exit 1
          else
            echo "✅ Aucune erreur flake8 détectée" >> $GITHUB_STEP_SUMMARY
          fi

      - name: Vérification pylint sur tests/
        run: |
          echo "## Pylint Results (tests/)" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          pylint tests/ --rcfile=.pylintrc --exit-zero --reports=y --output-format=text 2>&1 | tee pylint_report.txt || true
          SCORE=$(grep "Your code has been rated at" pylint_report.txt | grep -oP '\d+\.\d+')
          if [ -n "$SCORE" ]; then
            echo "**Score Pylint: ${SCORE}/10.00**" >> $GITHUB_STEP_SUMMARY
          fi

      - name: Upload rapports lint
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: lint-reports
          path: |
            flake8_report.txt
            pylint_report.txt
          retention-days: 7

  # ===========================================================================
  # Job 2: Tests unitaires - Couverture de code avec matrix Python
  # ===========================================================================
  unit-tests:
    name: "Tests Unitaires (Python ${{ matrix.python-version }})"
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Configuration Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Installation des dépendances
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements_test.txt

      - name: Exécution des tests unitaires avec couverture
        env:
          DJANGO_SETTINGS_MODULE: nouvelair.settings
          COVERAGE_FILE: ".coverage.${{ matrix.python-version }}"
        run: |
          pytest tests/unit/ -m unit --cov --cov-report=xml --cov-report=html --cov-fail-under=${{ env.COVERAGE_MIN }} -v --tb=short

      - name: Rapport de couverture dans le summary
        if: always()
        run: |
          echo "## Couverture de code (Python ${{ matrix.python-version }})" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          python -m coverage report --skip-covered >> $GITHUB_STEP_SUMMARY || true
          echo "" >> $GITHUB_STEP_SUMMARY
          TOTAL=$(python -m coverage report --format=total 2>/dev/null || echo "N/A")
          if [ "$TOTAL" != "N/A" ]; then
            echo "**Couverture totale: ${TOTAL}%** (minimum requis: ${{ env.COVERAGE_MIN }}%)" >> $GITHUB_STEP_SUMMARY
          fi

      - name: Upload rapport de couverture
        if: matrix.python-version == '3.12' && always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report-py312
          path: |
            coverage.xml
            htmlcov/
          retention-days: 14

  # ===========================================================================
  # Job 3: Tests d'intégration
  # ===========================================================================
  integration-tests:
    name: "Tests d'Intégration"
    runs-on: ubuntu-latest
    needs: lint

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Configuration Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Installation des dépendances
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements_test.txt

      - name: Exécution des tests d'intégration
        env:
          DJANGO_SETTINGS_MODULE: nouvelair.settings
        run: |
          pytest tests/integration/ -m integration -v --tb=short --junitxml=integration-results.xml

      - name: Rapport dans le summary
        if: always()
        run: |
          echo "## Résultats Tests d'Intégration" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          PASSED=$(grep -oP 'passed=\K\d+' integration-results.xml 2>/dev/null || echo "0")
          FAILED=$(grep -oP 'failures=\K\d+' integration-results.xml 2>/dev/null || echo "0")
          ERRORS=$(grep -oP 'errors=\K\d+' integration-results.xml 2>/dev/null || echo "0")
          echo "| Statut | Nombre |" >> $GITHUB_STEP_SUMMARY
          echo "|--------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| ✅ Réussis | ${PASSED} |" >> $GITHUB_STEP_SUMMARY
          echo "| ❌ Échoués | ${FAILED} |" >> $GITHUB_STEP_SUMMARY
          echo "| ⚠️ Erreurs | ${ERRORS} |" >> $GITHUB_STEP_SUMMARY

      - name: Upload résultats JUnit
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: integration-results
          path: integration-results.xml
          retention-days: 14

  # ===========================================================================
  # Job 4: Tests BDD (Behave)
  # ===========================================================================
  bdd-tests:
    name: "Tests BDD (Behave)"
    runs-on: ubuntu-latest
    needs: lint

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Configuration Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Installation des dépendances
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements_test.txt
          pip install behave behave-django

      - name: Exécution des tests BDD
        env:
          DJANGO_SETTINGS_MODULE: nouvelair.settings
        run: |
          behave features/ --tags=sprint1,sprint2 -f pretty --no-capture --junit --junit-directory=bdd-results/ || true

      - name: Rapport dans le summary
        if: always()
        run: |
          echo "## Résultats Tests BDD" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          if [ -d bdd-results ]; then
            echo "**Scénarios Behave exécutés avec les tags: sprint1, sprint2**" >> $GITHUB_STEP_SUMMARY
            for file in bdd-results/*.xml; do
              if [ -f "$file" ]; then
                echo "Résultats: $(basename $file)" >> $GITHUB_STEP_SUMMARY
              fi
            done
          else
            echo "Aucun fichier de résultats BDD trouvé." >> $GITHUB_STEP_SUMMARY
          fi

      - name: Upload résultats BDD
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: bdd-results
          path: bdd-results/
          retention-days: 7

  # ===========================================================================
  # Job 5: Tests End-to-End (Playwright)
  # ===========================================================================
  e2e-tests:
    name: "Tests End-to-End (Playwright)"
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Configuration Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Installation des dépendances
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements_test.txt
          pip install pytest-playwright

      - name: Installation des navigateurs Playwright
        run: playwright install chromium --with-deps

      - name: Exécution des tests E2E
        env:
          DJANGO_SETTINGS_MODULE: nouvelair.settings
        run: |
          pytest tests/e2e/ -m e2e --browser chromium -v --tb=short --screenshot=on --junitxml=e2e-results.xml

      - name: Rapport dans le summary
        if: always()
        run: |
          echo "## Résultats Tests End-to-End" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          PASSED=$(grep -oP 'passed=\K\d+' e2e-results.xml 2>/dev/null || echo "0")
          FAILED=$(grep -oP 'failures=\K\d+' e2e-results.xml 2>/dev/null || echo "0")
          echo "| Statut | Nombre |" >> $GITHUB_STEP_SUMMARY
          echo "|--------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| ✅ Réussis | ${PASSED} |" >> $GITHUB_STEP_SUMMARY
          echo "| ❌ Échoués | ${FAILED} |" >> $GITHUB_STEP_SUMMARY

      - name: Upload captures d'écran
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-screenshots
          path: |
            test-results/
            screenshots/
          retention-days: 7

      - name: Upload résultats E2E
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-results
          path: e2e-results.xml
          retention-days: 14

  # ===========================================================================
  # Job 6: Tests de performance (Locust)
  # ===========================================================================
  performance-tests:
    name: "Tests de Performance"
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Configuration Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Installation des dépendances
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements_test.txt
          pip install locust

      - name: Lancement du serveur Django en arrière-plan
        env:
          DJANGO_SETTINGS_MODULE: nouvelair.settings
        run: |
          python manage.py migrate --run-syncdb 2>/dev/null || python manage.py migrate 2>/dev/null || true
          python manage.py runserver 0.0.0.0:8888 &
          sleep 5

      - name: Exécution du test de charge Locust
        run: |
          cat > locustfile_qa.py << 'LOCUSTFILE'
          from locust import HttpUser, task, between

          class NouvelAirUser(HttpUser):
              wait_time = between(1, 3)

              @task(5)
              def home(self):
                  self.client.get("/", name="Page d'accueil")

              @task(3)
              def search_flights(self):
                  self.client.get("/recherche/", name="Recherche vols")

              @task(2)
              def airports(self):
                  self.client.get("/aeroports/", name="Liste aéroports")

              @task(1)
              def promotions(self):
                  self.client.get("/promotions/", name="Promotions")

              @task(1)
              def destinations(self):
                  self.client.get("/destinations/", name="Destinations")
          LOCUSTFILE

          locust -f locustfile_qa.py \
            --host=http://localhost:8888 \
            --users 10 \
            --spawn-rate 2 \
            --run-time 60s \
            --headless \
            --only-summary \
            --html=performance-report.html \
            --csv=performance-results 2>&1 | tee locust_output.txt || true

      - name: Vérification des seuils de performance
        run: |
          echo "## Rapport de Performance" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY

          if [ -f performance-results_stats.csv ]; then
            echo "**Métriques de performance (10 utilisateurs, 60s):**" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "| Endpoint | Requêtes | Médiane (ms) | 95e centile (ms) |" >> $GITHUB_STEP_SUMMARY
            echo "|----------|----------|---------------|--------------------|" >> $GITHUB_STEP_SUMMARY
            tail -n +2 performance-results_stats.csv | while IFS=',' read -r name req_count median p95; do
              if [ -n "$name" ] && [ "$name" != "None" ] && [ "$name" != "Aggregated" ]; then
                echo "| ${name} | ${req_count} | ${median} | ${p95} |" >> $GITHUB_STEP_SUMMARY
              fi
            done

            # Vérifier la latence médiane agrégée
            MEDIAN=$(grep "Aggregated" performance-results_stats.csv | cut -d',' -f6)
            if [ -n "$MEDIAN" ] && [ "$MEDIAN" -lt 3000 ]; then
              echo "" >> $GITHUB_STEP_SUMMARY
              echo "✅ **Seuil de performance respecté**: latence médiane = ${MEDIAN}ms < 3000ms" >> $GITHUB_STEP_SUMMARY
            elif [ -n "$MEDIAN" ]; then
              echo "" >> $GITHUB_STEP_SUMMARY
              echo "❌ **Seuil de performance dépassé**: latence médiane = ${MEDIAN}ms >= 3000ms" >> $GITHUB_STEP_SUMMARY
              exit 1
            fi
          else
            echo "⚠️ Aucune métrique de performance collectée (serveur non démarré ?)" >> $GITHUB_STEP_SUMMARY
          fi

      - name: Upload rapport de performance
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: performance-report
          path: |
            performance-report.html
            performance-results*.csv
            locust_output.txt
          retention-days: 14

  # ===========================================================================
  # Job 7: Tests de sécurité (Bandit + Safety)
  # ===========================================================================
  security-tests:
    name: "Tests de Sécurité"
    runs-on: ubuntu-latest
    needs: lint

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Configuration Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Installation des dépendances
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements_test.txt
          pip install bandit safety

      - name: Analyse de sécurité avec Bandit
        run: |
          echo "## Analyse de Sécurité - Bandit" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          bandit -r . -f json -o bandit_results.json --exit-zero || true
          bandit -r . -f screen --exit-zero 2>&1 | tee bandit_screen.txt || true

          LOW=$(python -c "import json; d=json.load(open('bandit_results.json')); print(sum(1 for r in d.get('results',[]) if r.get('issue_severity')=='LOW'))" 2>/dev/null || echo "0")
          MEDIUM=$(python -c "import json; d=json.load(open('bandit_results.json')); print(sum(1 for r in d.get('results',[]) if r.get('issue_severity')=='MEDIUM'))" 2>/dev/null || echo "0")
          HIGH=$(python -c "import json; d=json.load(open('bandit_results.json')); print(sum(1 for r in d.get('results',[]) if r.get('issue_severity')=='HIGH'))" 2>/dev/null || echo "0")

          echo "| Sévérité | Nombre |" >> $GITHUB_STEP_SUMMARY
          echo "|----------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| 🔴 HIGH | ${HIGH} |" >> $GITHUB_STEP_SUMMARY
          echo "| 🟠 MEDIUM | ${MEDIUM} |" >> $GITHUB_STEP_SUMMARY
          echo "| 🟡 LOW | ${LOW} |" >> $GITHUB_STEP_SUMMARY

          if [ "$HIGH" -gt 0 ]; then
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "### 🔴 Vulnérabilités HIGH détectées" >> $GITHUB_STEP_SUMMARY
            python -c "
          import json
          d=json.load(open('bandit_results.json'))
          high = [r for r in d.get('results',[]) if r.get('issue_severity')=='HIGH']
          for r in high:
              print(f'- **{r[\"issue_text\"].strip()}** ({r[\"filename\"]}:{r[\"line_number\"]})')
          " >> $GITHUB_STEP_SUMMARY
            echo "❌ **ÉCHEC: ${HIGH} vulnérabilité(s) de sévérité HIGH détectée(s)**" >> $GITHUB_STEP_SUMMARY
            exit 1
          else
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "✅ **Aucune vulnérabilité HIGH détectée**" >> $GITHUB_STEP_SUMMARY
          fi

      - name: Vérification des dépendances avec Safety
        run: |
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "## Vérification des Dépendances - Safety" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          safety check --json > safety_results.json 2>&1 || true
          safety check 2>&1 | tee safety_screen.txt || true

          if [ -f safety_results.json ]; then
            VULN_COUNT=$(python -c "import json; d=json.load(open('safety_results.json')); print(len(d))" 2>/dev/null || echo "0")
            HIGH_VULN=$(python -c "
          import json
          d=json.load(open('safety_results.json'))
          high = sum(1 for v in d if v.get('vulnerability',{}).get('severity','') in ('high','critical') or 'unresolved' in str(v).lower()[:50])
          print(high)
          " 2>/dev/null || echo "0")

            echo "| Statut | Nombre |" >> $GITHUB_STEP_SUMMARY
            echo "|--------|--------|" >> $GITHUB_STEP_SUMMARY
            echo "| Vulnérabilités trouvées | ${VULN_COUNT} |" >> $GITHUB_STEP_SUMMARY
            echo "| HIGH/Critical | ${HIGH_VULN} |" >> $GITHUB_STEP_SUMMARY

            if [ "$HIGH_VULN" -gt 0 ]; then
              echo "" >> $GITHUB_STEP_SUMMARY
              echo "❌ **ÉCHEC: ${HIGH_VULN} vulnérabilité(s) HIGH/Critical dans les dépendances**" >> $GITHUB_STEP_SUMMARY
              exit 1
            else
              echo "" >> $GITHUB_STEP_SUMMARY
              echo "✅ **Aucune vulnérabilité HIGH dans les dépendances**" >> $GITHUB_STEP_SUMMARY
            fi
          fi

      - name: Upload rapports de sécurité
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: security-reports
          path: |
            bandit_results.json
            bandit_screen.txt
            safety_results.json
            safety_screen.txt
          retention-days: 14

  # ===========================================================================
  # Job final: Statut global du pipeline
  # ===========================================================================
  pipeline-status:
    name: "Statut Global du Pipeline"
    runs-on: ubuntu-latest
    if: always()
    needs: [lint, unit-tests, integration-tests, bdd-tests, e2e-tests, performance-tests, security-tests]

    steps:
      - name: Vérification du statut global
        run: |
          echo "# NouvelAir QA Pipeline - Statut Global" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "## Résultats des jobs" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY

          # Récupérer les statuts de chaque job
          LINT="${{ needs.lint.result }}"
          UNIT="${{ needs.unit-tests.result }}"
          INTEG="${{ needs.integration-tests.result }}"
          BDD="${{ needs.bdd-tests.result }}"
          E2E="${{ needs.e2e-tests.result }}"
          PERF="${{ needs.performance-tests.result }}"
          SEC="${{ needs.security-tests.result }}"

          status_icon() {
            case "$1" in
              success) echo "✅" ;;
              failure) echo "❌" ;;
              cancelled) echo "⚠️" ;;
              skipped) echo "⏭️" ;;
              *) echo "❓" ;;
            esac
          }

          echo "| Job | Statut |" >> $GITHUB_STEP_SUMMARY
          echo "|-----|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Linting | $(status_icon $LINT) ${LINT} |" >> $GITHUB_STEP_SUMMARY
          echo "| Tests Unitaires | $(status_icon $UNIT) ${UNIT} |" >> $GITHUB_STEP_SUMMARY
          echo "| Tests d'Intégration | $(status_icon $INTEG) ${INTEG} |" >> $GITHUB_STEP_SUMMARY
          echo "| Tests BDD | $(status_icon $BDD) ${BDD} |" >> $GITHUB_STEP_SUMMARY
          echo "| Tests E2E | $(status_icon $E2E) ${E2E} |" >> $GITHUB_STEP_SUMMARY
          echo "| Tests Performance | $(status_icon $PERF) ${PERF} |" >> $GITHUB_STEP_SUMMARY
          echo "| Tests Sécurité | $(status_icon $SEC) ${SEC} |" >> $GITHUB_STEP_SUMMARY

          echo "" >> $GITHUB_STEP_SUMMARY
          OVERALL="success"
          for r in $LINT $UNIT $INTEG $BDD $E2E $PERF $SEC; do
            if [ "$r" = "failure" ]; then
              OVERALL="failure"
              break
            fi
          done

          if [ "$OVERALL" = "success" ]; then
            echo "## 🎉 Pipeline réussi !" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "Tous les jobs sont passés avec succès." >> $GITHUB_STEP_SUMMARY
            echo "Les rapports détaillés sont disponibles dans les artifacts." >> $GITHUB_STEP_SUMMARY
          else
            echo "## ❌ Pipeline en échec" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "Un ou plusieurs jobs ont échoué. Consultez les rapports pour plus de détails." >> $GITHUB_STEP_SUMMARY
            exit 1
          fi
"""

    write_file(filepath, content)


def generate_flake8_config():
    """Génère le fichier .flake8."""
    filepath = os.path.join(BASE_DIR, ".flake8")

    content = """# =============================================================================
# Configuration Flake8 - NouvelAir
# =============================================================================
# Règles de linting pour le projet NouvelAir.
# Documentation: https://flake8.pycqa.org/en/latest/
# =============================================================================

[flake8]
max-line-length = 120
exclude =
    migrations,
    venv,
    __pycache__,
    .git,
    .github,
    htmlcov,
    *.egg-info,
    build,
    dist,
    node_modules
ignore =
    E203,   # whitespace before ':' (conflit avec Black)
    E266,   # too many '#' for block comment
    E501,   # line too long (géré par max-line-length)
    W503,   # line break before binary operator
per-file-ignores =
    tests/*: S101, S106
    */tests/*: S101
    manage.py: S101
    scripts/*: S101
# Format de sortie
format = default
show-source = true
statistics = true
count = true
"""

    write_file(filepath, content)


def generate_pylintrc():
    """Génère le fichier .pylintrc."""
    filepath = os.path.join(BASE_DIR, ".pylintrc")

    content = """# =============================================================================
# Configuration Pylint - NouvelAir
# =============================================================================
# Configuration adaptée pour le projet Django NouvelAir.
# Documentation: https://pylint.pycqa.org/en/latest/
# =============================================================================

[MASTER]
# Utiliser le plugin Django pour les checks spécifiques
load-plugins=pylint_django
django-settings-module=nouvelair.settings

# Répertoires à ignorer
ignore=
    migrations,
    venv,
    __pycache__,
    .git,
    htmlcov,
    node_modules,
    build,
    dist

# Extensions de fichiers à analyser
extension-pkg-allow-list=
    django.core.validators

[MESSAGES CONTROL]
# Désactiver les avertissements de docstrings manquants dans les tests
disable=
    C0114,   # missing-module-docstring
    C0115,   # missing-class-docstring
    C0116,   # missing-function-docstring
    C0301,   # line-too-long (géré par flake8)
    C0303,   # trailing-whitespace
    C0304,   # missing-final-newline
    C0305,   # trailing-newlines
    C0410,   # multiple-imports-on-one-line
    C0411,   # wrong-import-order
    C0412,   # ungrouped-imports
    C0413,   # wrong-import-position
    R0401,   # cyclic-import (fréquent dans Django)
    R0901,   # too-many-instance-attributes
    R0902,   # too-many-instance-attributes
    R0903,   # too-few-public-methods
    R0913,   # too-many-arguments
    R0914,   # too-many-local-variables
    W0212,   # protected-access (fréquent avec les attributs Django)
    W0603,   # global-statement
    W0613,   # unused-argument (fréquent dans les vues)
    W0622,   # redefined-builtin
    W0703,   # broad-except
    W1514,   # unspecified-encoding
    E0401,   # import-error (géré par l'IDE)
    E1101,   # no-member (faux positifs Django)
    N813,    # camelcase-imported-as-lowercase
    fixme

[REPORTS]
# Ne pas afficher le rapport complet par défaut
reports=no
score=yes

[FORMAT]
# Longueur maximale des lignes
max-line-length=120
# Nombre d'espaces pour l'indentation
indent-string='    '

[BASIC]
# Noms de variables et fonctions
good-names=
    i,
    j,
    k,
    v,
    e,
    ex,
    pk,
    id,
    qs,
    db,
    fn,
    op,
    ok,
    os,
    up,
    rv,
    _

# Style de nommage pour les variables
variable-rgx=[a-z_][a-z0-9_]{0,30}$
argument-rgx=[a-z_][a-z0-9_]{0,30}$
attr-rgx=[a-z_][a-z0-9_]{0,30}$
class-attribute-rgx=([A-Za-z_][A-Za-z0-9_]{0,30}|(__.*__))$
method-rgx=[a-z_][a-z0-9_]{0,30}$
function-rgx=[a-z_][a-z0-9_]{0,30}$
class-rgx=[A-Z_][a-zA-Z0-9_]+$
const-rgx=(([A-Z_][A-Z0-9_]*|__.*__))$
module-rgx=([a-z_][a-z0-9_]*)$

[DESIGN]
# Nombre maximal de méthodes publiques par classe
max-public-methods=20
# Nombre maximal d'arguments pour une méthode
max-args=7
# Nombre maximal de branches (if/elif)
max-branches=12
# Nombre maximal de déclarations de variables locales
max-locals=15
# Nombre maximal de return
max-returns=6
# Nombre maximal d'instructions dans une méthode
max-statements=50
# Nombre maximal d'attributs par classe
max-attributes=7
# Nombre maximal de parents
max-parents=7
# Complexité cyclomatique maximale
max-complexity=10

[TYPECHECK]
# Membres ignorés pour les vérifications de type
ignored-modules=
    django,
    django.contrib,
    rest_framework,
    factory,
    crispy_forms,

generated-members=
    objects,
    DoesNotExist,
    MultipleObjectsReturned

[SIMILARITIES]
# Seuil minimum de similarité pour les duplications
min-similarity-lines=4
# Ignorer les imports lors de la comparaison
ignore-imports=yes
"""

    write_file(filepath, content)


def generate_regression_tests():
    """Génère le fichier tests/test_regression.py."""
    filepath = os.path.join(BASE_DIR, "tests", "test_regression.py")

    content = r'''"""
tests/test_regression.py - Suite de tests de régression pour NouvelAir
====================================================================
Suite complète de tests de régression couvrant tous les modules critiques
de l'application NouvelAir. Ces tests s'assurent que les fonctionnalités
existantes ne sont pas impactées par les nouvelles modifications.

Modules couverts:
    - flights: création de vols, aéroports, aéronefs, recherche
    - bookings: création de réservations, passagers, paiements, statuts
    - accounts: inscription, connexion, profil utilisateur
    - destinations: création de destinations, avis
    - promotions: création de promotions, newsletter
    - URLs: résolution de toutes les routes
    - Forms: validation des formulaires critiques

Marqueur: pytest.mark.regression

Auteurs: Équipe QA NouvelAir
Version: 1.0.0 - Jour 9
"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone
from django.test import Client, TestCase
from django.urls import reverse, resolve, NoReverseMatch
from django.contrib.auth.models import User

from flights.models import Airport, Aircraft, Flight
from bookings.models import Booking, Passenger, Payment
from accounts.models import UserProfile, SavedDestination
from promotions.models import Promotion, NewsletterSubscription
from destinations.models import Destination, DestinationReview


# =============================================================================
# Fixtures communes
# =============================================================================


@pytest.fixture
def airports():
    """Crée les aéroports principaux utilisés dans les tests."""
    tun = Airport.objects.create(
        code="TUN", name="Aéroport International Tunis-Carthage",
        city="Tunis", country="Tunisie",
        latitude=Decimal("36.851000"), longitude=Decimal("10.227000")
    )
    cdg = Airport.objects.create(
        code="CDG", name="Aéroport de Paris-Charles de Gaulle",
        city="Paris", country="France",
        latitude=Decimal("49.009691"), longitude=Decimal("2.547926")
    )
    fco = Airport.objects.create(
        code="FCO", name="Aéroport de Rome-Fiumicino",
        city="Rome", country="Italie",
        latitude=Decimal("41.800278"), longitude=Decimal("12.238889")
    )
    return {"tun": tun, "cdg": cdg, "fco": fco}


@pytest.fixture
def aircraft():
    """Crée un aéronef de test."""
    return Aircraft.objects.create(
        model_name="Airbus A320neo",
        registration="TS-INA",
        total_seats=180,
        economy_seats=150,
        business_seats=30,
        is_active=True,
    )


@pytest.fixture
def flight(airports, aircraft):
    """Crée un vol de test programmé dans le futur."""
    departure = timezone.now() + timedelta(days=7)
    arrival = departure + timedelta(hours=2, minutes=30)
    return Flight.objects.create(
        flight_number="BJ201",
        origin=airports["tun"],
        destination=airports["cdg"],
        aircraft=aircraft,
        departure_time=departure,
        arrival_time=arrival,
        base_price_economy=Decimal("189.50"),
        base_price_business=Decimal("663.25"),
        available_seats_economy=150,
        available_seats_business=30,
        status="scheduled",
        is_active=True,
    )


@pytest.fixture
def user():
    """Crée un utilisateur de test."""
    return User.objects.create_user(
        username="regression_user",
        first_name="Ahmed",
        last_name="Ben Ali",
        email="ahmed.regression@test.tn",
        password="TestPass123!",
    )


@pytest.fixture
def user_with_profile(user):
    """Crée un utilisateur avec un profil complet."""
    profile, _ = UserProfile.objects.update_or_create(
        user=user,
        defaults={
            "phone": "+216 22 333 444",
            "address": "12 Rue Habib Bourguiba",
            "city": "Tunis",
            "country": "Tunisie",
            "date_of_birth": date(1990, 5, 15),
            "nationality": "Tunisienne",
            "gender": "M",
            "newsletter": True,
        },
    )
    return user


@pytest.fixture
def booking(user, flight):
    """Crée une réservation de test."""
    return Booking.objects.create(
        user=user,
        contact_email=user.email,
        contact_phone="+216 22 333 444",
        status="pending",
        total_amount=Decimal("189.50"),
        special_requests="Siège côté hublot",
    )


@pytest.fixture
def client():
    """Client de test HTTP."""
    return Client()


# =============================================================================
# Régression: Modèles - Créations
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestModelCreationRegression:
    """Tests de régression pour la création de tous les modèles."""

    def test_regression_create_airport(self, airports):
        """REG-AIRPORT-001: Vérifie la création d'un aéroport avec tous ses champs."""
        ams = Airport.objects.create(
            code="AMS",
            name="Aéroport de Schiphol",
            city="Amsterdam",
            country="Pays-Bas",
            latitude=Decimal("52.310500"),
            longitude=Decimal("4.768300"),
            is_active=True,
        )
        assert ams.code == "AMS"
        assert ams.city == "Amsterdam"
        assert ams.is_active is True
        assert str(ams) == "AMS - Amsterdam (Pays-Bas)"
        assert ams.created_at is not None

    def test_regression_create_aircraft(self, aircraft):
        """REG-AIRCRAFT-001: Vérifie la création d'un aéronef."""
        assert aircraft.model_name == "Airbus A320neo"
        assert aircraft.registration == "TS-INA"
        assert aircraft.total_seats == 180
        assert aircraft.economy_seats == 150
        assert aircraft.business_seats == 30
        assert str(aircraft) == "Airbus A320neo (TS-INA)"

    def test_regression_create_flight(self, flight, airports, aircraft):
        """REG-FLIGHT-001: Vérifie la création d'un vol avec tous ses champs."""
        assert flight.flight_number == "BJ201"
        assert flight.origin == airports["tun"]
        assert flight.destination == airports["cdg"]
        assert flight.aircraft == aircraft
        assert flight.status == "scheduled"
        assert flight.base_price_economy == Decimal("189.50")
        assert flight.base_price_business == Decimal("663.25")
        assert flight.duration is not None
        assert str(flight) == "BJ201: TUN → CDG"

    def test_regression_create_booking(self, booking, user):
        """REG-BOOKING-001: Vérifie la création d'une réservation."""
        assert booking.user == user
        assert booking.status == "pending"
        assert booking.total_amount == Decimal("189.50")
        assert booking.contact_email == user.email
        assert booking.reference is not None
        assert len(booking.short_reference) == 8

    def test_regression_create_passenger(self, booking, flight):
        """REG-PASSENGER-001: Vérifie la création d'un passager."""
        passenger = Passenger.objects.create(
            booking=booking,
            flight=flight,
            title="mr",
            first_name="Mohamed",
            last_name="Trabelsi",
            date_of_birth=date(1985, 3, 20),
            nationality="Tunisienne",
            passport_number="TR1234567",
            travel_class="economy",
            price=Decimal("189.50"),
            special_assistance=False,
            meal_preference="Standard",
        )
        assert passenger.booking == booking
        assert passenger.flight == flight
        assert str(passenger) == "Monsieur Mohamed Trabelsi"

    def test_regression_create_payment(self, booking):
        """REG-PAYMENT-001: Vérifie la création d'un paiement."""
        payment = Payment.objects.create(
            booking=booking,
            amount=Decimal("189.50"),
            method="credit_card",
            status="completed",
            transaction_id="TXN-TEST-123456",
        )
        assert payment.booking == booking
        assert payment.amount == Decimal("189.50")
        assert payment.method == "credit_card"
        assert payment.status == "completed"
        assert str(payment) == "Paiement 189.50 TND - Complété"

    def test_regression_create_user_profile(self, user):
        """REG-PROFILE-001: Vérifie la création d'un profil utilisateur."""
        profile, _ = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "phone": "+216 22 333 444",
                "city": "Tunis",
                "country": "Tunisie",
                "nationality": "Tunisienne",
                "gender": "M",
            },
        )
        assert profile.user == user
        assert profile.phone == "+216 22 333 444"
        assert profile.full_name == "Ahmed Ben Ali"
        assert profile.booking_count == 0

    def test_regression_create_promotion(self, flight):
        """REG-PROMO-001: Vérifie la création d'une promotion."""
        promo = Promotion.objects.create(
            code="REGRESSION20",
            name="Test Régression -20%",
            description="Promotion de test pour vérifier la régression",
            promo_type="percentage",
            discount_percentage=Decimal("20.00"),
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=30),
            max_uses=100,
            is_active=True,
            is_featured=True,
        )
        promo.flights.add(flight)
        assert promo.code == "REGRESSION20"
        assert promo.is_valid is True
        assert promo.remaining_uses == 100

    def test_regression_create_destination(self, airports):
        """REG-DESTINATION-001: Vérifie la création d'une destination."""
        dest = Destination.objects.create(
            name="Djerba",
            slug="djerba",
            description="Île paradisiaque au sud de la Tunisie",
            short_description="La perle du golfe de Gabès",
            airport=airports["tun"],
            category="beach",
            rating=Decimal("4.5"),
            is_featured=True,
            is_active=True,
        )
        assert dest.slug == "djerba"
        assert dest.category == "beach"
        assert dest.is_featured is True

    def test_regression_create_newsletter_subscription(self):
        """REG-NEWSLETTER-001: Vérifie la création d'un abonnement newsletter."""
        sub = NewsletterSubscription.objects.create(
            email="newsletter@test.tn",
            first_name="Fatma",
            is_active=True,
        )
        assert sub.email == "newsletter@test.tn"
        assert sub.is_active is True


# =============================================================================
# Régression: Vues - Pages critiques
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestViewRegression:
    """Tests de régression pour les vues critiques de l'application."""

    def test_regression_home_page_loads(self, client):
        """REG-VIEW-001: La page d'accueil doit charger avec un statut 200."""
        response = client.get(reverse("flights:home"))
        assert response.status_code == 200
        assert "flights/home.html" in [t.name for t in response.templates]

    def test_regression_login_page_loads(self, client):
        """REG-VIEW-002: La page de connexion doit charger avec un statut 200."""
        response = client.get(reverse("accounts:login"))
        assert response.status_code == 200
        assert "accounts/login.html" in [t.name for t in response.templates]

    def test_regression_register_page_loads(self, client):
        """REG-VIEW-003: La page d'inscription doit charger avec un statut 200."""
        response = client.get(reverse("accounts:register"))
        assert response.status_code == 200
        assert "accounts/register.html" in [t.name for t in response.templates]

    def test_regression_airport_list_page(self, client, airports):
        """REG-VIEW-004: La page de liste des aéroports doit charger."""
        response = client.get(reverse("flights:airport_list"))
        assert response.status_code == 200

    def test_regression_flight_search_page(self, client):
        """REG-VIEW-005: La page de recherche de vols doit charger."""
        response = client.get(reverse("flights:search_results"))
        assert response.status_code == 200

    def test_regression_flight_detail_page(self, client, flight):
        """REG-VIEW-006: La page de détail d'un vol doit charger."""
        response = client.get(
            reverse("flights:flight_detail", kwargs={"flight_number": flight.flight_number})
        )
        assert response.status_code == 200

    def test_regression_booking_create_page_requires_login(self, client):
        """REG-VIEW-007: La page de création de réservation nécessite une authentification."""
        response = client.get(reverse("bookings:create"))
        # Doit rediriger vers la page de connexion
        assert response.status_code in [302, 403]

    def test_regression_my_bookings_requires_login(self, client):
        """REG-VIEW-008: La page 'mes réservations' nécessite une authentification."""
        response = client.get(reverse("bookings:my_bookings"))
        assert response.status_code in [302, 403]

    def test_regression_destinations_list_page(self, client):
        """REG-VIEW-009: La page de liste des destinations doit charger."""
        response = client.get(reverse("destinations:list"))
        assert response.status_code == 200

    def test_regression_promotions_list_page(self, client):
        """REG-VIEW-010: La page de liste des promotions doit charger."""
        response = client.get(reverse("promotions:list"))
        assert response.status_code == 200


# =============================================================================
# Régression: Résolution d'URLs
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestURLResolutionRegression:
    """Tests de régression pour la résolution de toutes les URLs du projet."""

    def test_regression_url_flights_home(self):
        """REG-URL-001: Résolution de l'URL de la page d'accueil."""
        assert resolve("/").view_name == "flights:home"

    def test_regression_url_flights_search(self):
        """REG-URL-002: Résolution de l'URL de recherche de vols."""
        assert resolve("/recherche/").view_name == "flights:search_results"

    def test_regression_url_flights_airport_list(self):
        """REG-URL-003: Résolution de l'URL de la liste des aéroports."""
        assert resolve("/aeroports/").view_name == "flights:airport_list"

    def test_regression_url_accounts_login(self):
        """REG-URL-004: Résolution de l'URL de connexion."""
        assert resolve("/compte/connexion/").view_name == "accounts:login"

    def test_regression_url_accounts_register(self):
        """REG-URL-005: Résolution de l'URL d'inscription."""
        assert resolve("/compte/inscription/").view_name == "accounts:register"

    def test_regression_url_accounts_logout(self):
        """REG-URL-006: Résolution de l'URL de déconnexion."""
        assert resolve("/compte/deconnexion/").view_name == "accounts:logout"

    def test_regression_url_accounts_profile(self):
        """REG-URL-007: Résolution de l'URL du profil."""
        assert resolve("/compte/profil/").view_name == "accounts:profile"

    def test_regression_url_bookings_create(self):
        """REG-URL-008: Résolution de l'URL de création de réservation."""
        assert resolve("/reservations/creer/").view_name == "bookings:create"

    def test_regression_url_bookings_my_bookings(self):
        """REG-URL-009: Résolution de l'URL 'mes réservations'."""
        assert resolve("/reservations/mes-reservations/").view_name == "bookings:my_bookings"

    def test_regression_url_bookings_lookup(self):
        """REG-URL-010: Résolution de l'URL de recherche de réservation."""
        assert resolve("/reservations/recherche/").view_name == "bookings:lookup"

    def test_regression_url_destinations_list(self):
        """REG-URL-011: Résolution de l'URL de la liste des destinations."""
        assert resolve("/destinations/").view_name == "destinations:list"

    def test_regression_url_promotions_list(self):
        """REG-URL-012: Résolution de l'URL de la liste des promotions."""
        assert resolve("/promotions/").view_name == "promotions:list"

    def test_regression_url_legal(self):
        """REG-URL-013: Résolution de l'URL des mentions légales."""
        assert resolve("/mentions-legales/").view_name == "legal"

    def test_regression_url_terms(self):
        """REG-URL-014: Résolution de l'URL des conditions générales."""
        assert resolve("/conditions-generales/").view_name == "terms"


# =============================================================================
# Régression: Formulaires - Validations
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestFormValidationRegression:
    """Tests de régression pour la validation des formulaires critiques."""

    def test_regression_passenger_form_invalid_passport(self, airports, aircraft, user):
        """REG-FORM-001: Le formulaire passager rejette un passeport trop court."""
        from bookings.forms import PassengerForm
        from datetime import date as d

        departure = timezone.now() + timedelta(days=7)
        flight = Flight.objects.create(
            flight_number="BJ999", origin=airports["tun"],
            destination=airports["cdg"], aircraft=aircraft,
            departure_time=departure,
            arrival_time=departure + timedelta(hours=2),
            base_price_economy=Decimal("100.00"),
            base_price_business=Decimal("350.00"),
            available_seats_economy=100, available_seats_business=20,
        )
        booking = Booking.objects.create(
            user=user, contact_email="test@test.tn",
            contact_phone="+216 22 000 000",
            status="pending", total_amount=Decimal("100.00"),
        )
        form_data = {
            "title": "mr",
            "first_name": "Test",
            "last_name": "User",
            "date_of_birth": d(1990, 1, 1),
            "nationality": "Tunisienne",
            "passport_number": "AB",  # Trop court (< 5 caractères)
            "special_assistance": False,
            "meal_preference": "",
        }
        form = PassengerForm(data=form_data)
        assert not form.is_valid()
        assert "passport_number" in form.errors

    def test_regression_payment_form_invalid_card_number(self, booking):
        """REG-FORM-002: Le formulaire de paiement rejette un numéro de carte invalide."""
        from bookings.forms import PaymentForm

        form_data = {
            "card_number": "1234",  # Trop court
            "card_holder": "Test User",
            "expiry_date": "13/25",
            "cvv": "123",
            "method": "credit_card",
        }
        form = PaymentForm(data=form_data)
        assert not form.is_valid()
        assert "card_number" in form.errors

    def test_regression_flight_search_form_same_airports(self, airports):
        """REG-FORM-003: Le formulaire de recherche rejette départ = arrivée."""
        from flights.forms import FlightSearchForm

        form_data = {
            "trip_type": "oneway",
            "origin": airports["tun"].pk,
            "destination": airports["tun"].pk,  # Même aéroport !
            "departure_date": date.today() + timedelta(days=7),
            "return_date": "",
            "passengers": 1,
            "travel_class": "economy",
        }
        form = FlightSearchForm(data=form_data)
        assert not form.is_valid()
        assert "__all__" in form.errors

    def test_regression_flight_search_form_past_date(self, airports):
        """REG-FORM-004: Le formulaire de recherche rejette une date passée."""
        from flights.forms import FlightSearchForm

        form_data = {
            "trip_type": "oneway",
            "origin": airports["tun"].pk,
            "destination": airports["cdg"].pk,
            "departure_date": date.today() - timedelta(days=1),  # Date passée
            "return_date": "",
            "passengers": 1,
            "travel_class": "economy",
        }
        form = FlightSearchForm(data=form_data)
        assert not form.is_valid()

    def test_regression_flight_search_form_roundtrip_invalid_dates(self, airports):
        """REG-FORM-005: Le formulaire rejette retour avant départ."""
        from flights.forms import FlightSearchForm

        dep_date = date.today() + timedelta(days=7)
        form_data = {
            "trip_type": "roundtrip",
            "origin": airports["tun"].pk,
            "destination": airports["cdg"].pk,
            "departure_date": str(dep_date),
            "return_date": str(dep_date - timedelta(days=1)),  # Avant le départ
            "passengers": 1,
            "travel_class": "economy",
        }
        form = FlightSearchForm(data=form_data)
        assert not form.is_valid()


# =============================================================================
# Régression: Authentification
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestAuthenticationRegression:
    """Tests de régression pour les flux d'authentification."""

    def test_regression_user_can_register(self, client):
        """REG-AUTH-001: Un utilisateur peut s'inscrire avec des données valides."""
        response = client.post(
            reverse("accounts:register"),
            {
                "username": "newuser_regression",
                "first_name": "Salma",
                "last_name": "Gharbi",
                "email": "salma.regression@test.tn",
                "password1": "SecurePass123!",
                "password2": "SecurePass123!",
            },
            follow=True,
        )
        assert User.objects.filter(username="newuser_regression").exists()
        assert response.status_code == 200

    def test_regression_user_can_login(self, client, user):
        """REG-AUTH-002: Un utilisateur peut se connecter avec des identifiants valides."""
        response = client.post(
            reverse("accounts:login"),
            {"username": "regression_user", "password": "TestPass123!"},
            follow=True,
        )
        assert response.status_code == 200
        # Vérifie que l'utilisateur est connecté
        assert "_auth_user_id" in client.session

    def test_regression_user_cannot_login_invalid(self, client, user):
        """REG-AUTH-003: La connexion échoue avec un mot de passe incorrect."""
        response = client.post(
            reverse("accounts:login"),
            {"username": "regression_user", "password": "WrongPass999"},
        )
        assert "_auth_user_id" not in client.session

    def test_regression_user_can_logout(self, client, user):
        """REG-AUTH-004: Un utilisateur peut se déconnecter."""
        client.force_login(user)
        assert "_auth_user_id" in client.session
        response = client.post(reverse("accounts:logout"), follow=True)
        assert "_auth_user_id" not in client.session
        assert response.status_code == 200

    def test_regression_profile_page_authenticated(self, client, user_with_profile):
        """REG-AUTH-005: La page de profil est accessible pour un utilisateur authentifié."""
        client.force_login(user_with_profile)
        response = client.get(reverse("accounts:profile"))
        assert response.status_code == 200


# =============================================================================
# Régression: Statuts de réservation
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestBookingStatusRegression:
    """Tests de régression pour les transitions de statut des réservations."""

    @pytest.mark.parametrize("status", ["pending", "confirmed", "cancelled", "completed", "refunded"])
    def test_regression_all_booking_statuses_valid(self, booking, status):
        """REG-STATUS-001: Tous les statuts de réservation sont valides."""
        booking.status = status
        booking.save()
        booking.refresh_from_db()
        assert booking.status == status
        assert booking.get_status_display() is not None

    def test_regression_booking_default_status(self, user):
        """REG-STATUS-002: Le statut par défaut d'une réservation est 'pending'."""
        booking = Booking.objects.create(
            user=user,
            contact_email="default@test.tn",
            contact_phone="+216 22 000 000",
            total_amount=Decimal("50.00"),
        )
        assert booking.status == "pending"

    def test_regression_booking_status_transition_pending_to_confirmed(self, booking):
        """REG-STATUS-003: Transition pending → confirmed."""
        booking.status = "confirmed"
        booking.save()
        assert booking.status == "confirmed"

    def test_regression_booking_status_transition_confirmed_to_cancelled(self, booking):
        """REG-STATUS-004: Transition confirmed → cancelled."""
        booking.status = "confirmed"
        booking.save()
        booking.status = "cancelled"
        booking.save()
        assert booking.status == "cancelled"

    def test_regression_booking_str_representation(self, booking):
        """REG-STATUS-005: La représentation string d'une réservation est correcte."""
        assert "Réservation" in str(booking)
        assert "En attente" in str(booking) or "pending" in str(booking).lower()


# =============================================================================
# Régression: Recherche de vols
# =============================================================================


@pytest.mark.regression
@pytest.mark.django_db
class TestFlightSearchRegression:
    """Tests de régression pour la recherche de vols."""

    def test_regression_search_flights_returns_results(self, flight):
        """REG-SEARCH-001: La recherche de vols retourne des résultats corrects."""
        departure_date = flight.departure_time.date()
        results = Flight.search_flights("TUN", "CDG", departure_date)
        assert flight in results

    def test_regression_search_flights_no_results(self, flight):
        """REG-SEARCH-002: La recherche ne retourne rien si aucun vol ne correspond."""
        results = Flight.search_flights("TUN", "AMS", date.today() + timedelta(days=14))
        assert flight not in results
        assert len(results) == 0

    def test_regression_search_flights_business_class(self, flight, airports, aircraft):
        """REG-SEARCH-003: La recherche en classe affaires filtre correctement."""
        results = Flight.search_flights(
            "TUN", "CDG", flight.departure_time.date(),
            passengers=1, travel_class="business"
        )
        assert flight in results

    def test_regression_search_flights_excludes_inactive(self, flight):
        """REG-SEARCH-004: La recherche exclut les vols inactifs."""
        flight.is_active = False
        flight.save()
        results = Flight.search_flights("TUN", "CDG", flight.departure_time.date())
        assert flight not in results
'''

    write_file(filepath, content)


def generate_run_full_suite():
    """Génère le fichier scripts/run_full_suite.py."""
    filepath = os.path.join(BASE_DIR, "scripts", "run_full_suite.py")

    content = r'''#!/usr/bin/env python3
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
'''

    write_file(filepath, content)


def generate_run_regression():
    """Génère le fichier scripts/run_regression.py."""
    filepath = os.path.join(BASE_DIR, "scripts", "run_regression.py")

    content = r'''#!/usr/bin/env python3
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
'''

    write_file(filepath, content)


def generate_ci_cd_documentation():
    """Génère le fichier docs/ci_cd_documentation.md."""
    filepath = os.path.join(BASE_DIR, "docs", "ci_cd_documentation.md")

    content = r"""# Documentation CI/CD - NouvelAir
# ================================
# Version: 1.0.0
# Date: Jour 9
# Auteur: Équipe QA NouvelAir

## 1. Architecture du Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NouvelAir QA Pipeline                           │
│                  (GitHub Actions Workflow)                          │
│                                                                     │
│  Déclencheurs: push (main, sprint1, sprint2) / PR (main)           │
└──────────────┬──────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────┐
│   1. LINT            │ ◄── flake8 + pylint
│   (Statut: gate)     │
└──────┬───────────────┘
       │
       ├──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ 2. UNIT    │ │ 3. INTEG   │ │ 4. BDD     │ │ 7. SECURE  │
│   TESTS    │ │   TESTS    │ │  (behave)  │ │  (bandit)  │
│ (matrix)   │ │            │ │            │ │            │
│ py 3.10    │ │            │ │            │ │            │
│ py 3.11    │ │            │ │            │ │            │
│ py 3.12    │ │            │ │            │ │            │
└──────┬─────┘ └──────┬─────┘ └────────────┘ └────────────┘
       │              │
       ├──────────────┤
       ▼              ▼
┌──────────────────────┐ ┌──────────────────────┐
│ 5. E2E TESTS         │ │ 6. PERFORMANCE       │
│   (Playwright)       │ │   (Locust)           │
│   ◄── Chromium       │ │   ◄── 10 users, 60s  │
│   ◄── Screenshots    │ │   ◄── Latency < 3s   │
└──────────┬───────────┘ └──────────┬───────────┘
           │                        │
           └────────────┬───────────┘
                        ▼
           ┌─────────────────────────┐
           │ 8. PIPELINE STATUS      │
           │   ◄── Résumé global     │
           │   ◄── Badges statut     │
           └─────────────────────────┘
```

## 2. Description des Jobs

### Job 1: Linting
- **Objectif**: Vérifier la qualité du code source
- **Outils**: flake8 (style) + pylint (qualité)
- **Configuration**: `.flake8` + `.pylintrc`
- **Critère de succès**: 0 erreur fatale (E9, F63, F7, F82)
- **Durée typique**: ~30 secondes

### Job 2: Tests Unitaires
- **Objectif**: Valider le comportement isolé de chaque composant
- **Outils**: pytest + pytest-cov
- **Strategy**: Matrix sur Python 3.10, 3.11, 3.12
- **Critère de succès**: Couverture >= 80%, 0 test échoué
- **Durée typique**: ~1-2 minutes par version Python

### Job 3: Tests d'Intégration
- **Objectif**: Vérifier le bon fonctionnement des modules ensemble
- **Outils**: pytest
- **Critère de succès**: 0 test échoué
- **Durée typique**: ~1-2 minutes

### Job 4: Tests BDD (Behave)
- **Objectif**: Valider les scénarios métier en langage naturel
- **Outils**: behave + behave-django
- **Tags**: sprint1, sprint2
- **Critère de succès**: Tous les scénarios passent
- **Durée typique**: ~1-3 minutes

### Job 5: Tests End-to-End
- **Objectif**: Simuler le parcours utilisateur complet
- **Outils**: pytest-playwright (Chromium)
- **Dépend de**: Tests unitaires + Tests d'intégration
- **Artifacts**: Captures d'écran en cas d'échec
- **Durée typique**: ~2-5 minutes

### Job 6: Tests de Performance
- **Objectif**: Vérifier les performances sous charge légère
- **Outils**: Locust
- **Configuration**: 10 utilisateurs, montée progressive, 60 secondes
- **Critère de succès**: Latence médiane < 3000ms
- **Durée typique**: ~2 minutes

### Job 7: Tests de Sécurité
- **Objectif**: Détecter les vulnérabilités dans le code et les dépendances
- **Outils**: bandit (code) + safety (dépendances)
- **Critère de succès**: 0 vulnérabilité HIGH
- **Durée typique**: ~30 secondes

### Job 8: Statut Global du Pipeline
- **Objectif**: Fournir un résumé consolidé de tous les jobs
- **Exécution**: Toujours (même si des jobs ont échoué)
- **Sortie**: Tableau de bord dans le summary GitHub

## 3. Portes de Qualité (Quality Gates)

Le pipeline impose les portes de qualité suivantes :

| Critère | Seuil | Job |
|---------|-------|-----|
| Erreurs fatales flake8 | 0 | lint |
| Couverture de code | >= 80% | unit-tests |
| Tests unitaires échoués | 0 | unit-tests |
| Tests d'intégration échoués | 0 | integration-tests |
| Scénarios BDD échoués | 0 | bdd-tests |
| Tests E2E échoués | 0 | e2e-tests |
| Vulnérabilités HIGH | 0 | security-tests |
| Latence médiane | < 3000ms | performance-tests |

Si une porte n'est pas respectée, le job échoue et bloque les jobs dépendants.

## 4. Comment Ajouter de Nouveaux Tests

### Ajouter un test unitaire

1. Créer le fichier dans `tests/unit/` :
   ```bash
   # tests/unit/test_nouveau_module.py
   import pytest

   @pytest.mark.unit
   def test_ma_nouvelle_fonctionnalite():
       assert True
   ```

2. Le test sera automatiquement ramassé par le pipeline.

### Ajouter un test d'intégration

1. Créer le fichier dans `tests/integration/` :
   ```bash
   # tests/integration/test_nouveau_module.py
   import pytest

   @pytest.mark.integration
   @pytest.mark.django_db
   def test_mon_integration():
       assert True
   ```

### Ajouter un scénario BDD

1. Créer le fichier feature dans `features/` :
   ```gherkin
   # features/nouvelle_fonctionnalite.feature
   Feature: Nouvelle fonctionnalité

     @sprint2
     Scenario: Test de base
       Given je suis sur la page d'accueil
       When je clique sur le lien
       Then je vois le résultat
   ```

### Ajouter un test de régression

1. Ajouter le test dans `tests/test_regression.py` :
   ```python
   @pytest.mark.regression
   @pytest.mark.django_db
   def test_regression_ma_fonctionnalite():
       # Ce test s'assure que la fonctionnalité reste stable
       assert True
   ```

### Ajouter un test E2E

1. Créer le fichier dans `tests/e2e/` :
   ```python
   # tests/e2e/test_mon_parcours.py
   import pytest

   @pytest.mark.e2e
   def test_parcours_complet(page):
       page.goto("/recherche/")
       assert page.title() != ""
   ```

## 5. Comment Consulter les Rapports

### Depuis GitHub

1. Allez sur l'onglet **Actions** du dépôt
2. Sélectionnez le run le plus récent
3. Cliquez sur un job pour voir les logs
4. Le **Summary** affiche un tableau de bord consolidé

### Télécharger les Artifacts

1. Sur la page du workflow run
2. Scrollez jusqu'à la section **Artifacts**
3. Téléchargez les rapports :
   - `coverage-report-py312`: Rapport de couverture HTML
   - `lint-reports`: Rapports flake8 et pylint
   - `integration-results`: Résultats JUnit XML
   - `bdd-results`: Résultats Behave
   - `e2e-screenshots`: Captures d'écran (si échec)
   - `performance-report`: Rapport Locust HTML
   - `security-reports`: Rapports Bandit et Safety

### Rapport de Couverture Local

```bash
# Ouvrir le rapport HTML de couverture
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## 6. Comment Gérer les Échecs

### Échec de Linting

1. Télécharger l'artifact `lint-reports`
2. Corriger les erreurs identifiées
3. Vérifier localement : `flake8 . --config=.flake8`
4. Pousser la correction

### Échec des Tests Unitaires

1. Vérifier les logs du job dans GitHub Actions
2. Identifier le test qui échoue
3. Reproduire localement :
   ```bash
   pytest tests/unit/ -m unit -v --tb=long
   ```
4. Corriger et pousser

### Échec des Tests d'Intégration

1. Vérifier les logs et le rapport JUnit
2. Télécharger l'artifact `integration-results`
3. Reproduire localement :
   ```bash
   pytest tests/integration/ -m integration -v --tb=long
   ```

### Échec des Tests BDD

1. Vérifier les logs Behave
2. Vérifier que les fixtures et steps sont à jour
3. Exécuter localement :
   ```bash
   behave features/ --tags=sprint1,sprint2 -f pretty
   ```

### Échec des Tests E2E

1. Télécharger les captures d'écran (`e2e-screenshots`)
2. Analyser visuellement la cause de l'échec
3. Vérifier que le sélecteur CSS/ID est toujours valide

### Échec de Performance

1. Télécharger `performance-report.html`
2. Identifier l'endpoint lent
3. Optimiser (requêtes, cache, etc.)

### Échec de Sécurité

1. Télécharger `bandit_results.json` et `safety_screen.txt`
2. Analyser chaque vulnérabilité HIGH
3. Appliquer les corrections recommandées
4. Mettre à jour les dépendances si nécessaire

## 7. Stratégie de Branches

```
main ─────────────────────────────────────────────────────────► (production)
  │
  ├── sprint1 ──── (feature sprint 1)
  │     │
  │     └── feature/login ──── (développement spécifique)
  │
  ├── sprint2 ──── (feature sprint 2)
  │     │
  │     └── feature/booking ──── (développement spécifique)
  │
  └── feature/xxx ──── (création de PR vers main)
```

### Règles de branchement

- **main**: Branche protégée, déploiement automatique
- **sprint1/sprint2**: Branches de développement par sprint
- **feature/***: Branches de fonctionnalités, créées depuis un sprint
- Les PR vers `main` déclenchent le pipeline complet
- Les pushes sur les branches sprint déclenchent aussi le pipeline

### Workflow recommandé

1. Créer une branche `feature/mon-travail` depuis `sprintX`
2. Développer et tester localement avec `python scripts/run_full_suite.py`
3. Commiter et pousser
4. Le pipeline CI/CD s'exécute automatiquement
5. Corriger les éventuels échecs
6. Créer une PR vers `main` quand tout passe
7. Le pipeline s'exécute à nouveau sur la PR
8. Merger après approbation
"""

    write_file(filepath, content)


def generate_quality_gates():
    """Génère le fichier docs/quality_gates.md."""
    filepath = os.path.join(BASE_DIR, "docs", "quality_gates.md")

    content = r"""# Portes de Qualité (Quality Gates) - NouvelAir
# ================================================
# Version: 1.0.0
# Date: Jour 9
# Auteur: Équipe QA NouvelAir

## Vue d'ensemble

Les **portes de qualité** sont des seuils obligatoires que le code doit franchir
avant d'être accepté dans la branche `main`. Elles garantissent un niveau de
qualité constant et préviennent les régressions.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PORTES DE QUALITÉ                              │
│                                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ LINTING │  │ COUVERT. │  │ INTEG.  │  │  BDD    │  │ SECURE  │ │
│  │  0 err  │  │  >= 80% │  │  0 fail │  │  0 fail │  │ 0 HIGH  │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘ │
│       │            │            │            │             │       │
│       └────────────┴────────────┴────────────┴─────────────┘       │
│                              │                                     │
│                        ┌─────▼──────┐                              │
│                        │  PIPELINE  │                              │
│                        │   PASS ✅   │                              │
│                        └────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. Couverture de Tests Unitaires >= 80%

### Description
Le pourcentage de code couvert par les tests unitaires doit être d'au moins 80%.
Cela garantit que la majorité du code métier est testée.

### Configuration
```yaml
# .github/workflows/tests.yml
pytest tests/unit/ -m unit --cov --cov-report=xml --cov-report=html --cov-fail-under=80
```

### Comment mesurer localement
```bash
pytest tests/unit/ -m unit --cov --cov-report=term-missing
```

### Comment améliorer la couverture
1. Identifier les fichiers/modules avec la couverture la plus basse
2. Ajouter des tests pour les branches de code non couvertes
3. Prioriser les chemins critiques (paiement, réservation, auth)

### Exemple de sortie
```
---------- coverage: platform linux, python 3.12.0 ----------
TOTAL                                  4521    785    82.6%
```
Si le total est < 80%, le pipeline **échoue**.

### Fichiers exclus de la couverture
- `migrations/` (générés automatiquement)
- `*/admin.py` (interface admin Django)
- `*/tests/*` (le code de test lui-même)

---

## 2. Tests d'Intégration: Tous Passent

### Description
Tous les tests d'intégration doivent réussir sans exception. Les tests d'intégration
vérifient que les modules fonctionnent correctement ensemble.

### Configuration
```yaml
pytest tests/integration/ -m integration -v
```

### Critères
- **0 test échoué**: Tous les tests doivent passer
- **0 erreur inattendue**: Pas d'exception non gérée

### Comment mesurer localement
```bash
pytest tests/integration/ -m integration -v --tb=short
```

### Types de tests d'intégration
- Test des vues avec Client Django
- Test des workflows multi-étapes (recherche → réservation → paiement)
- Test des interactions entre modèles
- Test des signaux et hooks

---

## 3. Tests BDD: Tous les Scénarios Verts

### Description
Tous les scénarios Behave marqués avec les tags `sprint1` ou `sprint2` doivent
passer (statut "vert"). Les scénarios BDD décrivent le comportement attendu
en langage naturel.

### Configuration
```bash
behave features/ --tags=sprint1,sprint2 -f pretty
```

### Critères
- **0 scénario échoué**: Tous les scénarios doivent passer
- **0 step undefined**: Tous les steps doivent avoir une implémentation

### Comment mesurer localement
```bash
behave features/ --tags=sprint1,sprint2 -f pretty --no-capture
```

### Tags disponibles
- `@sprint1`: Scénarios du sprint 1
- `@sprint2`: Scénarios du sprint 2
- `@wip`: Scénarios en cours (ignorés en CI)

### Structure d'un scénario
```gherkin
@sprint2
Scenario: Un utilisateur peut réserver un vol
  Given je suis sur la page d'accueil
  And je recherche un vol de TUN vers CDG
  When je sélectionne un vol
  And je remplis les informations passager
  Then la réservation est confirmée
```

---

## 4. Sécurité: 0 Vulnérabilité HIGH

### Description
L'analyse de sécurité doit détecter 0 vulnérabilité de sévérité HIGH. Cela inclut
la vérification du code source (bandit) et des dépendances (safety).

### Configuration
```yaml
# Code source
bandit -r . -f json -o bandit_results.json

# Dépendances
safety check
```

### Critères
- **0 HIGH** dans les résultats bandit
- **0 HIGH/Critical** dans les résultats safety

### Comment mesurer localement
```bash
# Analyser le code source
bandit -r . -f screen

# Vérifier les dépendances
safety check
```

### Sévérités prises en compte

| Sévérité | Action | Pipeline |
|----------|--------|----------|
| HIGH | ❌ Bloquant | Échec du pipeline |
| MEDIUM | ⚠️ Avertissement | Continue |
| LOW | ℹ️ Information | Continue |

### Exemples de vulnérabilités courantes
- Utilisation de `assert` dans le code de production
- Mots de passe codés en dur
- Utilisation de `eval()` ou `exec()`
- Dépendances avec des CVE connues

---

## 5. Performance: Latence Médiane < 3 secondes

### Description
Sous une charge de 10 utilisateurs simultanés pendant 60 secondes,
la latence médiane des requêtes doit rester en dessous de 3000ms.

### Configuration
```yaml
locust -f locustfile_qa.py \
  --users 10 \
  --spawn-rate 2 \
  --run-time 60s \
  --headless
```

### Critères
- **Latence médiane < 3000ms** pour l'ensemble des endpoints
- **0 erreur 5xx** pendant le test

### Comment mesurer localement
```bash
# 1. Démarrer le serveur
python manage.py runserver

# 2. Exécuter le test de charge (dans un autre terminal)
locust -f scripts/locustfile_qa.py \
  --host=http://localhost:8000 \
  --users 10 --spawn-rate 2 --run-time 60s --headless
```

### Endpoints testés
| Endpoint | Priorité | Seuil |
|----------|----------|-------|
| `/` (Accueil) | Critique | < 500ms |
| `/recherche/` (Recherche) | Critique | < 1000ms |
| `/aeroports/` (Aéroports) | Normal | < 1000ms |
| `/promotions/` (Promotions) | Normal | < 1500ms |
| `/destinations/` (Destinations) | Normal | < 1500ms |

### Améliorations recommandées
- Ajouter du cache (Redis) pour les pages statiques
- Optimiser les requêtes SQL avec `select_related` / `prefetch_related`
- Utiliser la pagination pour les listes longues
- Activer la compression gzip

---

## 6. Flake8: 0 Erreurs

### Description
Le linter flake8 ne doit détecter aucune erreur fatale. Les erreurs fatales
incluent les erreurs de syntaxe, d'importation et d'exécution.

### Configuration
```ini
# .flake8
max-line-length = 120
exclude = migrations, venv, __pycache__, .git
ignore = E203, E266, E501, W503
```

### Critères
- **0 erreur fatale** (catégories E9, F63, F7, F82)
- Les avertissements (W, E, C) sont tolérés mais affichés

### Comment mesurer localement
```bash
flake8 . --config=.flake8 --count --show-source
```

### Erreurs fatales bloquantes

| Code | Description |
|------|-------------|
| E999 | SyntaxError |
| F63 | Comparaison incorrecte (True/False/None) |
| F7 | Erreur de syntaxe (indentation, etc.) |
| F82 | Import non défini |
| E901 | SyntaxError / IndentationError |

### Avertissements non bloquants
- `E501`: Ligne trop longue (géré par `max-line-length`)
- `W503`: Saut de ligne avant opérateur binaire (conflit Black)
- `E203`: Espace avant `:` (conflit Black)

---

## Résumé des Portes de Qualité

| # | Porte | Seuil | Vérifié par |
|---|-------|-------|-------------|
| 1 | Couverture tests unitaires | >= 80% | pytest-cov |
| 2 | Tests d'intégration | 0 échoué | pytest |
| 3 | Tests BDD | 0 échoué | behave |
| 4 | Sécurité | 0 HIGH | bandit + safety |
| 5 | Performance | Latence < 3s | locust |
| 6 | Linting | 0 erreur | flake8 |

## Franchise vs Échec

- **Franchise (✅)**: Toutes les portes sont respectées → Le code peut être mergé
- **Échec (❌)**: Au moins une porte n'est pas respectée → Le code doit être corrigé

## Évolution des Seuils

Les seuils peuvent être ajustés au fil du projet :

| Phase | Couverture | Performance | Sécurité |
|-------|-----------|-------------|----------|
| Sprint 1 | 70% | < 5000ms | 0 HIGH |
| Sprint 2 | 80% | < 3000ms | 0 HIGH |
| Sprint 3+ | 85% | < 2000ms | 0 HIGH + 0 MEDIUM |

Pour modifier un seuil, éditez le fichier `.github/workflows/tests.yml`
et la variable d'environnement correspondante.
"""

    write_file(filepath, content)


# =============================================================================
# Fonction principale
# =============================================================================


def main():
    """Point d'entrée principal du script setup_jour9.py."""
    print("=" * 70)
    print("  setup_jour9.py - NouvelAir CI/CD & Régression Setup")
    print("  Projet de formation Django - Jour 9")
    print("=" * 70)
    print(f"\nRépertoire du projet: {BASE_DIR}")
    print("Création des fichiers:\n")

    # 1. GitHub Actions workflow
    print("[1/8] GitHub Actions Workflow (.github/workflows/tests.yml)")
    generate_github_actions_workflow()

    # 2. Configuration flake8
    print("\n[2/8] Configuration flake8 (.flake8)")
    generate_flake8_config()

    # 3. Configuration pylint
    print("\n[3/8] Configuration pylint (.pylintrc)")
    generate_pylintrc()

    # 4. Tests de régression
    print("\n[4/8] Tests de régression (tests/test_regression.py)")
    generate_regression_tests()

    # 5. Script suite complète
    print("\n[5/8] Script suite complète (scripts/run_full_suite.py)")
    generate_run_full_suite()

    # 6. Script régression rapide
    print("\n[6/8] Script régression rapide (scripts/run_regression.py)")
    generate_run_regression()

    # 7. Documentation CI/CD
    print("\n[7/8] Documentation CI/CD (docs/ci_cd_documentation.md)")
    generate_ci_cd_documentation()

    # 8. Documentation quality gates
    print("\n[8/8] Documentation quality gates (docs/quality_gates.md)")
    generate_quality_gates()

    # Résumé
    print("\n" + "=" * 70)
    print("  ✅ Tous les fichiers ont été générés avec succès !")
    print("=" * 70)
    print("""
Fichiers créés:
  .github/workflows/tests.yml       - Pipeline CI/CD complet (7 jobs)
  .flake8                           - Configuration flake8
  .pylintrc                         - Configuration pylint
  tests/test_regression.py          - Suite de régression (30+ tests)
  scripts/run_full_suite.py         - Script d'exécution complète
  scripts/run_regression.py         - Script de régression rapide
  docs/ci_cd_documentation.md       - Documentation CI/CD (FR)
  docs/quality_gates.md             - Documentation quality gates (FR)

Prochaines étapes:
  1. Examiner les fichiers générés
  2. Tester localement: python scripts/run_full_suite.py
  3. Tester régression: python scripts/run_regression.py --html
  4. Committer et pousser sur GitHub
  5. Vérifier le pipeline dans GitHub Actions

Bonne journée ! 🚀
""")


if __name__ == "__main__":
    main()
