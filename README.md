# KD-HDIE

**Knowledge-Driven Heterogeneous Data Integration and Evaluation (KD-HDIE)**

KD-HDIE is a research framework for integrating heterogeneous data sources through source reliability assessment, conflict detection, reliability-aware data fusion, interoperability services, and knowledge-driven processing.

> **Research prototype:** This repository accompanies the experimental work reported in the associated research project. Interfaces and implementation details may evolve as the framework is refined.

## Overview

Heterogeneous data integration can involve differences in source systems, schemas, units, attribute semantics, data quality, and observed values. KD-HDIE provides an implementation-oriented pipeline for bringing such observations into a unified representation while retaining information about source reliability and fusion decisions.

The current implementation includes:

- heterogeneous data-source connectors and adapters;
- canonical attribute mapping and normalization;
- source reliability assessment based on completeness, validity, historical stability, and optional reference-based accuracy;
- semantic and value conflict detection;
- reliability- and consistency-aware data fusion;
- interoperability context, pipeline, workflow, validation, and registry components;
- knowledge and reasoning components;
- a Django-based monitoring and exploration interface;
- reproducibility-oriented experimental scripts and reports;
- 365-day experimental data and supporting raw source data.

## Core processing logic

```text
Heterogeneous Sources
        |
        v
Source Connectors / Adapters
        |
        v
Normalization & Canonical Mapping
        |
        v
Source Reliability Assessment
        |
        v
Conflict Detection
        |
        v
Reliability-Aware Data Fusion
        |
        v
Unified Representation
        |
        v
Knowledge / System-Level Processing
```

The implementation keeps reliability information in attribute metadata and records fusion decisions, including candidate values, candidate sources, reliability scores, consistency scores, and the selected value.

## Repository structure

```text
KD-HDIE/
├── accounts/                 # Django account application
├── attributes/               # Unified attribute and record models
├── config/                   # Django configuration and canonical mapping
├── core/
│   ├── adapters/             # Data adapters
│   ├── algorithms/           # Reliability, conflict, fusion, etc.
│   ├── interoperability/    # Interoperability services and workflow
│   ├── knowledge/            # Knowledge and reasoning components
│   └── metadata/             # Metadata components
├── data/
│   └── experiment_365d_2025/ # 365-day experimental data
├── datasource/               # Data-source connectors
├── media/                    # Supporting heterogeneous dataset
├── reports/                  # Experimental protocols and reproducibility material
├── scripts/                  # Experiment and validation scripts
├── static/                   # Front-end assets
├── systems/                  # System/API and monitoring interface
├── templates/                # Django templates
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Reliability assessment

The implemented reliability algorithm evaluates source attributes using:

- **completeness**;
- **validity**;
- **historical stability**;
- optional **reference-based accuracy** when a trusted reference value is available.

Without a trusted reference, the implementation uses the configured completeness, validity, and stability weights. With a reference value, the reference-based accuracy term is incorporated into the reliability score.

## Conflict detection and data fusion

The conflict component checks duplicate observations for a canonical attribute and identifies unit conflicts and numerical/value discrepancies using configurable absolute and relative thresholds.

The fusion component combines source reliability with cross-source consistency. For numerical candidates, the current implementation uses:

```text
Final score = 0.60 × reliability + 0.40 × consistency
```

Fusion also records decision-level metadata so that selected values can be traced back to candidate sources and scores.

## Experimental reproducibility

The repository contains reproducibility material under `reports/` and executable experiment/validation scripts under `scripts/`.

Important files include:

- `reports/REPRODUCIBILITY_GATE_v1.md`
- `reports/experimental_protocol_final_365d.md`
- `reports/experimental_design_v2.md`
- `reports/results_table_schema_v1.md`
- `scripts/run_365_day_experiment.py`
- `scripts/run_ablation_experiment.py`
- `scripts/run_baseline_comparison.py`
- `scripts/run_scalability_experiment.py`
- `scripts/validate_365_protocol.py`
- `scripts/validate_experiment_invariants.py`

The `data/experiment_365d_2025/` directory contains the canonical 365-day dataset together with supporting source data and a manifest used by the experimental workflow.

## Installation

Create a Python virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file based on `.env.example` and provide a local value for `DJANGO_SECRET_KEY`.

Initialize the Django database:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

## Running experiments

The main experimental entry points are located in `scripts/`. Before running an experiment, consult the corresponding protocol and reproducibility documentation in `reports/`.

Example:

```bash
python scripts/run_365_day_experiment.py
```

Ablation and baseline comparisons:

```bash
python scripts/run_ablation_experiment.py
python scripts/run_baseline_comparison.py
```

## Data

The repository includes experimental data used by the current research workflow. The 365-day experiment package contains canonicalized data and source-level files associated with the NASA POWER and Open-Meteo connectors.

Please consult the manifests and experimental protocols before reusing the data or reproducing reported experiments.

## Security and configuration

Secrets and local configuration should not be committed to the repository. Use environment variables for deployment-specific values. The public repository intentionally excludes the local Django SQLite database and Python cache files.

## Research status

KD-HDIE is under active research and development. The reproducibility materials are included to support inspection and replication of the experimental workflow. The framework should be treated as a research prototype rather than a production data-integration platform.

## Citation

If you use KD-HDIE in academic work, please cite the associated paper when its final bibliographic information is available.

## License

A repository license will be added together with the final publication and code-release policy.
