# KD-HDIE Results Table Schema

These are **schemas, not experimental results**. Numeric cells must be populated only from validated execution outputs.

| Table | Purpose | Required fields |
|---|---|---|
| Table 1 | Dataset characteristics | period, days, sources, variables, missing observations |
| Table 2 | Main KD-HDIE performance | semantic coverage, matching, completeness, validity, quality, conflicts, resolution, reliability, runtime |
| Table 3 | Conflict analysis | checked groups, conflict groups, conflict rate, resolved conflicts, resolution rate |
| Table 4 | Baseline comparison | Direct Merge, Source Priority, KD-HDIE; identical metrics |
| Table 5 | Ablation | A0–A4; quality, conflicts, reliability, runtime, final records |
| Table 6 | Scalability | 30, 90, 180, 365 days; runtime and processing statistics |
