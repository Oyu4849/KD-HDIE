"""Orchestrate the reproducible KD-HDIE experiment suite.

The orchestrator intentionally requires a validated real-data result before
comparison/reporting stages are run. It never fabricates missing observations.
"""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--result', default='reports/experiment_365_day_2025.json')
    args=p.parse_args()
    result=Path(args.result)
    if not result.exists():
        raise SystemExit('No completed 365-day result found. Run download/run experiment first.')
    checks=[ROOT/'scripts'/'validate_experiment_invariants.py', result]
    subprocess.run([sys.executable, *map(str,checks)], check=True)
    print('PASS: experiment invariants validated. Comparison/reporting may proceed.')

if __name__=='__main__': main()
