# KD-HDIE 107-day real-data experiment protocol

## Scope
107 daily observations for 2025-01-01 through 2025-04-17 (inclusive).

## Active external sources
1. Open-Meteo historical daily API
2. NASA POWER daily API
3. Google Earth Engine exported CSV, only when an actual export is supplied

## Semantic integration
Source attributes are resolved to canonical ontology concepts before quality, conflict, reliability and fusion stages.

## Important provenance rule
The GEE connector represents an Earth Engine-derived exported dataset. It does not claim direct Earth Engine API execution.

## Important evaluation rule
All metrics must be computed from actual execution outputs. No target metric is hard-coded. Synthetic row duplication is prohibited.

## Canonical mappings
See `config/canonical_mapping.csv`.
