# tests/performance/check_perf_gate.py

# Script appelé par le Job 6 pour vérifier le quality gate de performance
import sys
import csv
 
 
def check_performance_gate(csv_path: str, max_median_ms: int) -> None:
    """
    Lit le fichier CSV généré par Locust et vérifie que
    la latence médiane est sous le seuil maximum.
    Quitte avec code 1 (échec CI) si le seuil est dépassé.
    """
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        failures = []
        for row in reader:
            if row.get("Name") == "Aggregated":
                continue
            median = int(float(row.get("50%", 0)))
            if median > max_median_ms:
                failures.append(
                    f"  FAIL : {row['Name']} → médiane {median}ms > seuil {max_median_ms}ms"
                )
    if failures:
        print("❌ Performance gate FAILED :")
        for f in failures:
            print(f)
        sys.exit(1)
    else:
        print(f"✅ Performance gate OK — toutes les médianes < {max_median_ms}ms")
 
 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python check_perf_gate.py <csv_path> <max_median_ms>")
        sys.exit(1)
    check_performance_gate(sys.argv[1], int(sys.argv[2]))