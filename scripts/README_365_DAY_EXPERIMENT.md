# KD-HDIE — 365-day final experiment

## Protocol

- Period: **2025-01-01 through 2025-12-31**
- Expected calendar observations: **365 days**
- Primary meteorological sources: **Open-Meteo historical daily API** and **NASA POWER daily API**
- Optional remote-sensing source: a **real Google Earth Engine CSV export** supplied with `--gee-csv`
- Synthetic row generation: **disabled**

## Run

From `hdie/`:

```bash
python scripts/run_365_day_experiment.py --latitude 45.0 --longitude 59.0
```

Optional GEE export:

```bash
python scripts/run_365_day_experiment.py --latitude 45.0 --longitude 59.0 --gee-csv /path/to/gee_export.csv
```

The runner writes the KD-HDIE result and a SHA-256 manifest into `reports/`.

## Dataset validation

```bash
python scripts/validate_daily_dataset.py /path/to/dataset.csv
```

The validator checks row count, unique dates, missing dates, duplicate dates,
out-of-range dates and invalid date values. It exits with code 2 when the
365-day protocol is not satisfied.

## Scientific reporting rule

Do not enter expected values into the paper before execution. Report the values
produced by the actual run, including semantic coverage, completeness, validity,
quality, conflict rate, conflict-resolution rate, reliability, fusion decisions,
and execution time.
