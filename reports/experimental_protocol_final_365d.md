# KD-HDIE Final Experimental Protocol — 365 Daily Observations

## Primary experiment
- Period: 2025-01-01 through 2025-12-31
- Expected calendar days: 365
- Primary sources: Open-Meteo historical daily API and NASA POWER Daily API
- Optional third source: Google Earth Engine-derived exported CSV, only when a real export is supplied
- No synthetic row generation or duplication is permitted.

## Canonical variables
- Temperature: Open-Meteo `temperature_2m_mean` / NASA `T2M`
- Precipitation: Open-Meteo `precipitation_sum` / NASA `PRECTOTCORR`
- Wind speed: Open-Meteo `wind_speed_10m_mean` / NASA `WS2M`
- Relative humidity: NASA `RH2M`

## Processing pipeline
Metadata → semantic matching → canonical mapping → unit harmonization → quality validation → conflict detection → reliability assessment → conflict-aware fusion → unified representation.

## Reporting rule
All numerical results must be generated from the executed experiment JSON. No metric may be pre-filled as 100% or otherwise assumed.
