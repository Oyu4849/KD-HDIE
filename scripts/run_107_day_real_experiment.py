"""Run a reproducible 107-day real-data KD-HDIE experiment.

Sources:
- Open-Meteo historical daily API
- NASA POWER daily API
- Optional Google Earth Engine exported CSV (GEE source)

No synthetic rows are generated. The GEE source is included only when an
actual Earth Engine export CSV is supplied.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.bootstrap import bootstrap
from core.framework import KDHDIEFramework


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
        sources.append({
            "source_system": "GEE",
            "connection_parameters": {
                "file_path": str(Path(args.gee_csv).resolve()),
            },
        })
    return sources


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start-date", default="2025-01-01")
    p.add_argument("--end-date", default="2025-04-17")
    p.add_argument("--latitude", type=float, default=45.0)
    p.add_argument("--longitude", type=float, default=59.0)
    p.add_argument("--gee-csv", default=None)
    p.add_argument("--output", default="reports/real_107_day_experiment.json")
    args = p.parse_args()

    bootstrap()
    framework = KDHDIEFramework()
    result = framework.execute_multi_source(
        sources=build_sources(args),
        workflow="DAILY",
    )
    payload = result.to_dict()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    print(json.dumps({
        "success": payload.get("success"),
        "output": str(out),
        "sources": [s["source_system"] for s in build_sources(args)],
        "start_date": args.start_date,
        "end_date": args.end_date,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
