"""Download and validate the 365-day 2025 real-data experiment inputs.

Downloads Open-Meteo Archive and NASA POWER Daily observations, saves raw JSON,
and creates a canonical CSV with one row per calendar day. No synthetic rows are
created. The script fails if either source does not cover all 365 dates.
"""
from __future__ import annotations
import argparse, json, time
from datetime import date, timedelta
from pathlib import Path
import requests
import pandas as pd

OPENMETEO_URL = "https://archive-api.open-meteo.com/v1/archive"
NASA_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"


def expected_dates(start, end):
    s, e = date.fromisoformat(start), date.fromisoformat(end)
    return [(s + timedelta(days=i)).isoformat() for i in range((e-s).days+1)]


def get_json(url, params, timeout=60, retries=3):
    last = None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json(), r.url
        except Exception as exc:
            last = exc
            if attempt < retries:
                time.sleep(2 ** (attempt - 1))
    raise RuntimeError(f"Request failed after {retries} attempts: {url}; {last}")


def openmeteo_frame(payload):
    daily = payload.get("daily") or {}
    dates = daily.get("time") or []
    if not dates:
        raise ValueError("Open-Meteo response contains no daily time series")
    return pd.DataFrame({
        "date": dates,
        "om_temperature": daily.get("temperature_2m_mean"),
        "om_precipitation": daily.get("precipitation_sum"),
        "om_wind_speed": daily.get("wind_speed_10m_mean"),
    })


def nasa_frame(payload):
    params = payload.get("properties", {}).get("parameter", {})
    if not params:
        raise ValueError("NASA POWER response contains no parameter data")
    keys = set().union(*(v.keys() for v in params.values()))
    rows = []
    for k in sorted(keys):
        d = date.fromisoformat(k[:4] + "-" + k[4:6] + "-" + k[6:8])
        rows.append({
            "date": d.isoformat(),
            "nasa_temperature": params.get("T2M", {}).get(k),
            "nasa_precipitation": params.get("PRECTOTCORR", {}).get(k),
            "nasa_relative_humidity": params.get("RH2M", {}).get(k),
            "nasa_wind_speed": params.get("WS2M", {}).get(k),
        })
    return pd.DataFrame(rows)


def validate(df, expected):
    got = sorted(pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d").dropna().unique())
    missing = sorted(set(expected) - set(got))
    extra = sorted(set(got) - set(expected))
    duplicates = int(pd.to_datetime(df["date"], errors="coerce").duplicated().sum())
    if len(df) != 365 or got != expected or duplicates:
        raise ValueError(f"Coverage validation failed: rows={len(df)}, unique={len(got)}, missing={len(missing)}, extra={len(extra)}, duplicate_rows={duplicates}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start-date", default="2025-01-01")
    p.add_argument("--end-date", default="2025-12-31")
    p.add_argument("--latitude", type=float, default=45.0)
    p.add_argument("--longitude", type=float, default=59.0)
    p.add_argument("--output-dir", default="data/experiment_365d_2025")
    args = p.parse_args()
    expected = expected_dates(args.start_date, args.end_date)
    if len(expected) != 365:
        raise ValueError(f"Expected exactly 365 days, got {len(expected)}")
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    om_params = {"latitude": args.latitude, "longitude": args.longitude, "start_date": args.start_date, "end_date": args.end_date, "daily": "temperature_2m_mean,precipitation_sum,wind_speed_10m_mean", "timezone": "UTC"}
    om, om_url = get_json(OPENMETEO_URL, om_params)
    (out / "openmeteo_raw.json").write_text(json.dumps(om, ensure_ascii=False, indent=2), encoding="utf-8")
    om_df = openmeteo_frame(om)
    validate(om_df, expected)

    nasa_params = {"parameters": "T2M,PRECTOTCORR,RH2M,WS2M", "community": "AG", "longitude": args.longitude, "latitude": args.latitude, "start": args.start_date.replace("-", ""), "end": args.end_date.replace("-", ""), "format": "JSON"}
    nasa, nasa_url = get_json(NASA_URL, nasa_params)
    (out / "nasa_power_raw.json").write_text(json.dumps(nasa, ensure_ascii=False, indent=2), encoding="utf-8")
    nasa_df = nasa_frame(nasa)
    validate(nasa_df, expected)

    merged = pd.DataFrame({"date": expected}).merge(om_df, on="date", how="left", validate="one_to_one").merge(nasa_df, on="date", how="left", validate="one_to_one")
    validate(merged, expected)
    merged.to_csv(out / "canonical_365d_2025.csv", index=False)
    manifest = {"protocol": "KD-HDIE-365D-2025-v1", "start_date": args.start_date, "end_date": args.end_date, "days": 365, "latitude": args.latitude, "longitude": args.longitude, "sources": {"Open-Meteo": om_url, "NASA POWER": nasa_url}, "synthetic_rows_added": False, "validated": True}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
