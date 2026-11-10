"""main.py — week 1 end-to-end runner.

Steps:
  1. fetch_data.py  → downloads CSVs into data/
  2. analyze_data   → computes statistics + plots into output/

Run:
  ./venv/bin/python main.py
"""
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "fetch_data.py")
ANALYZE = os.path.join(BASE, "analyze_data.py")


def step(name: str, script: str) -> None:
    print(f"\n▶ Running {name} …")
    res = subprocess.run([sys.executable, script], cwd=BASE)
    if res.returncode != 0:
        print(f"✗ {name} FAILED (exit {res.returncode})")
        sys.exit(res.returncode)
    print(f"✓ {name} finished")


def main() -> None:
    step("fetch_data", SRC)
    step("analyze_data", ANALYZE)
    print("\n✅ Week 1 complete. Check data/, output/, and the README.")


if __name__ == "__main__":
    main()
