"""Reproducible 107-day KD-HDIE multi-source experiment."""

from core.bootstrap import bootstrap
from core.framework import KDHDIEFramework

START_DATE = "2025-01-01"
END_DATE = "2025-04-17"  # exactly 107 calendar days, inclusive
LATITUDE = 45.0
LONGITUDE = 59.0


def main():
    bootstrap()
    framework = KDHDIEFramework()
    sources = [
        {
            "source_system": "OPENMETEO",
            "connection_parameters": {
                "latitude": LATITUDE,
                "longitude": LONGITUDE,
                "start_date": START_DATE,
                "end_date": END_DATE,
                "historical": True,
            },
        },
        {
            "source_system": "NASA",
            "connection_parameters": {
                "latitude": LATITUDE,
                "longitude": LONGITUDE,
                "start_date": START_DATE,
                "end_date": END_DATE,
                "temporal": "DAILY",
                "parameters": ["T2M", "PRECTOTCORR", "RH2M", "WS2M"],
            },
        },
    ]
    result = framework.execute_multi_source(
        sources=sources,
        workflow="DAILY",
    )
    print(result.to_dict())


if __name__ == "__main__":
    main()
