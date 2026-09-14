# KD-HDIE Reproducibility Gate v1

The final 365-day experiment is accepted only when:

1. The period is exactly 2025-01-01 through 2025-12-31 (365 calendar days).
2. Open-Meteo and NASA POWER each return exactly 365 source-level daily records.
3. The execution reports `success=true`.
4. No synthetic rows are added.
5. Baseline comparison receives the same validated 365-date input.
6. Scalability runs reject any source that returns fewer or more records than its requested prefix length.
7. Experiment-invariant validation is run before reporting.

A failed gate means the result must not be reported as an experimental finding.
