# KD-HDIE Q1 Experimental Design v2

## E1 Main experiment
365 daily observations from 2025-01-01 through 2025-12-31. Open-Meteo and NASA POWER are the primary heterogeneous sources. A Google Earth Engine export is optional and must be an actual exported file.

## E2 Baselines
1. Direct merge: concatenate source records after date alignment, without semantic/quality/conflict-aware processing.
2. Source-priority: for common attributes, select one declared source consistently (reported as a deterministic baseline, not as ground truth).
3. KD-HDIE: full pipeline with semantic alignment, mapping/harmonization, quality, conflict detection, reliability, fusion, and unified representation.

Baseline metrics must be computed from the same validated observations. No baseline is treated as ground truth.

## E3 Ablation
Ablation variants should be executed only when the corresponding pipeline implementation is available:
- A0: direct merge
- A1: + semantic matching/mapping
- A2: + quality validation
- A3: + conflict detection/resolution
- A4: + reliability-aware fusion (full KD-HDIE)

For every variant report semantic coverage, completeness, validity, quality, conflict rate, resolution rate, and runtime. The same input and random-free configuration must be used across variants.

## E4 Scalability
Run the same protocol on prefixes of the 2025 dataset: 30, 90, 180, and 365 days. Report runtime, records processed, fusion groups, conflicts, and peak memory if measured by the execution environment.

## Reporting rule
All numerical results in the manuscript must originate from an executed run. Do not replace missing values with 100%, estimated values, or duplicated rows.
