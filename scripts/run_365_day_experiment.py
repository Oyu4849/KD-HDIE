"""Run the final 365-day KD-HDIE real-data experiment.

Default period: 2025-01-01 .. 2025-12-31 (365 calendar days).
Sources: Open-Meteo historical daily API + NASA POWER daily API.
Optional: a real Google Earth Engine CSV export via --gee-csv.

This runner never fabricates observations. It validates the requested period
and records an experiment manifest alongside the KD-HDIE result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.bootstrap import bootstrap
from core.framework import KDHDIEFramework


def day_count(start: str, end: str) -> int:
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    if e < s:
        raise ValueError("end-date must not be earlier than start-date")
    return (e - s).days + 1


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_sources(args):
    sources = [
        {
            "source_system": "OPENMETEO",
            "connection_parameters": {
                "latitude": args.latitude,
                "longitude": args.longitude,
                "start_date": args.start_date,
                "end_date": args.end_date,
                "daily": [
                    "temperature_2m_mean",
                    "precipitation_sum",
                    "wind_speed_10m_mean",
                ],
                "historical": True,
            },
        },
        {
            "source_system": "NASA",
            "connection_parameters": {
                "latitude": args.latitude,
                "longitude": args.longitude,
                "start": args.start_date.replace("-", ""),
                "end": args.end_date.replace("-", ""),
                "parameters": ["T2M", "PRECTOTCORR", "RH2M", "WS2M"],
                "temporal": "DAILY",
            },
        },
    ]
    if args.gee_csv:
        gee = Path(args.gee_csv).resolve()
        if not gee.exists():
            raise FileNotFoundError(f"GEE export not found: {gee}")
        sources.append({
            "source_system": "GEE",
            "connection_parameters": {"file_path": str(gee)},
        })
    return sources


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start-date", default="2025-01-01")
    p.add_argument("--end-date", default="2025-12-31")
    p.add_argument("--latitude", type=float, default=45.0)
    p.add_argument("--longitude", type=float, default=59.0)
    p.add_argument("--gee-csv", default=None)
    p.add_argument("--output", default="reports/experiment_365_day_2025.json")
    args = p.parse_args()

    expected_days = day_count(args.start_date, args.end_date)
    if expected_days != 365:
        raise ValueError(
            f"Final experiment requires exactly 365 daily observations; "
            f"requested period contains {expected_days} days."
        )

    sources = build_sources(args)
    bootstrap()
    framework = KDHDIEFramework()

    started = time.perf_counter()
    result = framework.execute_multi_source(
        sources=sources,
        workflow="DAILY",
    )
    elapsed = time.perf_counter() - started
    payload = result.to_dict()

    # Hard gate: every real daily source must return exactly 365 source-level records.
    if not payload.get("success"):
        raise RuntimeError("KD-HDIE execution failed; no experimental result is accepted.")
    metadata = payload.get("metadata", {}) or {}
    source_stats = metadata.get("source_statistics", {}) or {}
    required_sources = ["OPENMETEO", "NASA"]
    for source_name in required_sources:
        src_stats = source_stats.get(source_name, {})
        observed = src_stats.get("output_records")
        if observed != expected_days:
            raise RuntimeError(
                f"{source_name} returned {observed} source-level records; "
                f"expected exactly {expected_days}. Experiment rejected."
            )

    payload.setdefault("experiment", {})
    payload["experiment"].update({
        "protocol": "KD-HDIE-365D-2025-v1",
        "start_date": args.start_date,
        "end_date": args.end_date,
        "expected_calendar_days": expected_days,
        "latitude": args.latitude,
        "longitude": args.longitude,
        "sources": [s["source_system"] for s in sources],
        "execution_wall_time_seconds": round(elapsed, 6),
        "synthetic_rows_added": False,
    })

    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    manifest = {
        "protocol": "KD-HDIE-365D-2025-v1",
        "result_file": str(out),
        "result_sha256": sha256_file(out),
        "start_date": args.start_date,
        "end_date": args.end_date,
        "expected_calendar_days": expected_days,
        "latitude": args.latitude,
        "longitude": args.longitude,
        "sources": [s["source_system"] for s in sources],
        "synthetic_rows_added": False,
        "completed_unix": time.time(),
    }
    manifest_path = out.with_name(out.stem + "_manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps({
        "success": payload.get("success"),
        "output": str(out),
        "manifest": str(manifest_path),
        "period_days": expected_days,
        "sources": [s["source_system"] for s in sources],
        "execution_wall_time_seconds": round(elapsed, 6),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
