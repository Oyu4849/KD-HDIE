"""Validate a daily CSV dataset for the KD-HDIE 365-day protocol."""
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--date-column", default="date")
    p.add_argument("--start-date", default="2025-01-01")
    p.add_argument("--end-date", default="2025-12-31")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    path = Path(args.csv)
    df = pd.read_csv(path)
    if args.date_column not in df.columns:
        raise ValueError(f"Missing date column: {args.date_column}")

    dates = pd.to_datetime(df[args.date_column], errors="coerce").dt.date
    expected_start = date.fromisoformat(args.start_date)
    expected_end = date.fromisoformat(args.end_date)
    expected = []
    d = expected_start
    while d <= expected_end:
        expected.append(d)
        d += timedelta(days=1)

    unique = sorted(set(x for x in dates.dropna()))
    missing = [x.isoformat() for x in expected if x not in set(unique)]
    extras = [x.isoformat() for x in unique if x < expected_start or x > expected_end]
    duplicate_rows = int(dates.duplicated(keep=False).sum())
    invalid_dates = int(dates.isna().sum())

    report = {
        "file": str(path.resolve()),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "expected_days": len(expected),
        "unique_dates": len(unique),
        "missing_dates": missing,
        "out_of_range_dates": extras,
        "duplicate_date_rows": duplicate_rows,
        "invalid_date_rows": invalid_dates,
        "exact_365_day_coverage": (
            len(df) == 365 and len(unique) == 365 and not missing and not extras
            and duplicate_rows == 0 and invalid_dates == 0
        ),
    }

    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")

    if not report["exact_365_day_coverage"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
