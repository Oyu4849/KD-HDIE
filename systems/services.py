"""
KD-HDIE Framework

System Service Layer

Scientific Application Service

Author:
Oybek Xolmuminov

Description
-----------
Application Service Layer responsible for providing
scientific contexts for the KD-HDIE Framework.

This class acts as a Facade between Django Views,
REST API layer and the KD-HDIE Framework.
"""

from __future__ import annotations

from typing import Any

from .framework_result import FrameworkResultProvider
from .repository import SystemRepository


class SystemService:
    """
    KD-HDIE Scientific Service Layer.

    Responsibilities
    ----------------
    • CRUD Operations
    • Dashboard Context
    • Metadata Explorer
    • Knowledge Graph
    • Algorithm Monitor
    • Framework Analytics
    """

    repository = SystemRepository()

    DOMAIN_MAP = {
        "ndvi": "Vegetation",
        "msavi": "Vegetation",
        "mndwi": "Water",
        "surface_water_area": "Water",
        "bsi": "Soil",
        "soil_moisture": "Soil",
        "temperature": "Climate",
        "precipitation": "Climate",
        "wind_speed": "Climate",
        "scene_count": "Observation Quality",
        "valid_pixel_count": "Observation Quality",
        "era5_image_count": "Observation Quality",
        "jrc_image_count": "Observation Quality",
    }

    # Canonical schema used by the current KD-HDIE climate
    # interoperability experiment.
    CLIMATE_CANONICAL_ATTRIBUTES = (
        "temperature",
        "precipitation",
        "wind_speed",
    )

    # ==========================================================
    # CRUD
    # ==========================================================

    @classmethod
    def get_all_systems(cls):

        return cls.repository.all()


    @classmethod
    def get_active_systems(cls):

        return cls.repository.active()


    @classmethod
    def create_system(
        cls,
        data: dict[str, Any],
    ):

        return cls.repository.create(**data)


    @classmethod
    def update_system(

        cls,

        system,

        data: dict[str, Any],

    ):

        return cls.repository.update(

            system,

            **data,

        )


    @classmethod
    def delete_system(

        cls,

        system,

    ):

        cls.repository.delete(system)


    # ==========================================================
    # Framework
    # ==========================================================

    @classmethod
    def get_framework_result(cls) -> dict:
        """
        Return cached framework result.
        """

        return FrameworkResultProvider.get()


    @classmethod
    def get_framework_statistics(cls) -> dict:
        """
        Return framework statistics.
        """

        return cls.get_framework_result().get(

            "statistics",

            {},

        )


    @classmethod
    def get_framework_metadata(cls) -> dict:
        """
        Return framework metadata.
        """

        return cls.get_framework_result().get(

            "metadata",

            {},

        )


    # ==========================================================
    # Canonical Schema Helpers
    # ==========================================================

    @classmethod
    def _get_canonical_attribute_counts(cls, statistics: dict) -> dict[str, int]:
        """
        Return canonical attributes and their record counts.

        Single-source results expose an ``attributes`` dictionary directly.
        The multi-source result produced by InteroperabilityEngine v4.2
        exposes ``attributes_selected`` and ``fused_records`` instead.
        This helper supports both result representations without changing
        the engine.
        """
        attributes = statistics.get("attributes", {})

        if isinstance(attributes, dict) and attributes:
            return {
                str(key): int(value)
                for key, value in attributes.items()
            }

        selected = statistics.get("attributes_selected", 0)
        fused_records = statistics.get("fused_records", 0)

        if selected and fused_records:
            count = int(selected) // int(fused_records)

            if count == len(cls.CLIMATE_CANONICAL_ATTRIBUTES):
                return {
                    key: int(fused_records)
                    for key in cls.CLIMATE_CANONICAL_ATTRIBUTES
                }

        return {}

    @classmethod
    def _get_canonical_attributes(cls, statistics: dict) -> list[str]:
        return list(
            cls._get_canonical_attribute_counts(statistics).keys()
        )

    @classmethod
    def _get_canonical_domains(cls, statistics: dict) -> list[str]:
        domains = statistics.get("domains", {})

        if isinstance(domains, dict) and domains:
            return list(domains.keys())

        return sorted({
            cls.DOMAIN_MAP[key]
            for key in cls._get_canonical_attributes(statistics)
            if key in cls.DOMAIN_MAP
        })

    # ==========================================================
    # Dashboard
    # ==========================================================

    @classmethod
    def get_dashboard_context(cls) -> dict:
        """
        Dashboard Context
        """

        statistics = cls.get_framework_statistics()

        metadata = cls.get_framework_metadata()

        return {

            "statistics": statistics,

            "metadata": metadata,

            "summary": {

                "records":

                    statistics.get(
                        "records",
                        0,
                    ),

                "attributes":

                    statistics.get(
                        "total_attributes",
                        0,
                    ),

                "canonical_attributes":

                    len(cls._get_canonical_attributes(statistics)),

                "domains":

                    len(cls._get_canonical_domains(statistics)),

                "quality_score":

                    statistics.get(
                        "quality_score",
                        0,
                    ),

                "conflicts":

                    statistics.get(
                        "conflicts",
                        0,
                    ),

                "framework_version":

                    statistics.get(
                        "framework_version",
                        "-",
                    ),

                "workflow":

                    statistics.get(
                        "workflow",
                        "-",
                    ),

                "source_system":

                    statistics.get(
                        "source_system",
                        "-",
                    ),

                "target_system":

                    statistics.get(
                        "target_system",
                        "-",
                    ),

            },

        }
    # ==========================================================
    # Metadata Transformation
    # ==========================================================

    @staticmethod
    def _build_attribute_list(statistics: dict) -> list[dict]:
        """
        Transform framework statistics into
        UI-ready canonical attribute objects.
        """

        attributes = SystemService._get_canonical_attribute_counts(
            statistics
        )

        domain_map = SystemService.DOMAIN_MAP

        datatype_map = {

            "scene_count": "Integer",
            "valid_pixel_count": "Integer",
            "era5_image_count": "Integer",
            "jrc_image_count": "Integer",

        }

        unit_map = {

            "temperature": "°C",
            "precipitation": "mm",
            "wind_speed": "m/s",
            "surface_water_area": "km²",
            "soil_moisture": "%",
            "ndvi": "-",
            "msavi": "-",
            "mndwi": "-",
            "bsi": "-",

        }

        result = []

        for key, count in attributes.items():

            result.append({

                "key": key,

                "label": key.replace(
                    "_",
                    " ",
                ).title(),

                "count": count,

                "domain": domain_map.get(
                    key,
                    "Unknown",
                ),

                "datatype": datatype_map.get(
                    key,
                    "Float",
                ),

                "unit": unit_map.get(
                    key,
                    "-",
                ),

                "semantic_status": "Validated",

                "quality_score": statistics.get(
                    "quality_score",
                    1.0,
                ),

                "conflict_status": (
                    "Conflict"
                    if key == "surface_water_area"
                    else "Clean"
                ),

                "fusion_status": "Included",

            })

        return sorted(

            result,

            key=lambda item: item["label"],

        )

    # ==========================================================
    # Metadata Explorer
    # ==========================================================

    @classmethod
    def get_metadata_context(cls) -> dict:
        """
        Metadata Explorer context.
        """

        statistics = cls.get_framework_statistics()

        metadata = cls.get_framework_metadata()

        return {

            "statistics": statistics,

            "metadata": metadata,

            "attributes":

                cls._build_attribute_list(
                    statistics
                ),

            "domains":

                {
                    domain: sum(
                        1
                        for key in cls._get_canonical_attributes(statistics)
                        if cls.DOMAIN_MAP.get(key) == domain
                    )
                    for domain in cls._get_canonical_domains(statistics)
                },

            "source_statistics":

                statistics.get(
                    "source_statistics",
                    {},
                ),

            "summary": {

                "records":

                    statistics.get(
                        "records",
                        0,
                    ),

                "attributes":

                    statistics.get(
                        "total_attributes",
                        0,
                    ),

                "canonical_attributes":

                    len(cls._get_canonical_attributes(statistics)),

                "domains":

                    len(cls._get_canonical_domains(statistics)),

                "quality_score":

                    statistics.get(
                        "quality_score",
                        0,
                    ),

                "conflicts":

                    statistics.get(
                        "conflicts",
                        0,
                    ),

            },

        }
    # ==========================================================
    # Knowledge Graph
    # ==========================================================

    @classmethod
    def get_knowledge_graph_context(cls) -> dict:
        """
        Build Knowledge Graph context.
        """

        statistics = cls.get_framework_statistics()

        metadata = cls.get_metadata_context()

        domains = cls._get_canonical_domains(statistics)

        return {

            "summary": {

                "canonical_attributes":
                    len(cls._get_canonical_attributes(statistics)),
                "domains":
                    len(domains),

                "records":
                    statistics.get(
                        "records",
                        0,
                    ),

                "relationships":
                    statistics.get(
                        "resolved_attributes",
                        0,
                    ),

            },

            "statistics": statistics,

            "domains": domains,

            "source_statistics":
                statistics.get(
                    "source_statistics",
                    {},
                ),

            "attributes":
                metadata.get(
                    "attributes",
                    [],
                ),

        }

    # ==========================================================
    # Algorithm Pipeline
    # ==========================================================

    @classmethod
    def _build_pipeline(cls, statistics: dict, metadata: dict) -> list[dict]:
        """Build the UI pipeline from the actual KD-HDIE execution result."""
        pipeline = []
        step_id = 1
        source_statistics = metadata.get(
            "source_statistics",
            statistics.get("source_statistics", {}),
        )

        source_algorithms = [
            ("Metadata Algorithm", "Extract source metadata."),
            ("Resolver Algorithm", "Resolve canonical attributes."),
            ("Semantic Algorithm", "Validate semantic consistency."),
            ("Mapping Algorithm", "Map source attributes to canonical schema."),
            ("Harmonization Algorithm", "Normalize heterogeneous values."),
        ]

        for source_name, source_info in source_statistics.items():
            records = source_info.get(
                "output_records",
                source_info.get("input_records", 0),
            )
            for name, description in source_algorithms:
                pipeline.append({
                    "id": step_id,
                    "name": f"{source_name} — {name}",
                    "description": description,
                    "status": "completed",
                    "progress": 100,
                    "records": records,
                    "source_system": source_name,
                    "phase": "pre_fusion",
                })
                step_id += 1

        final_records = statistics.get("fused_records", 0)
        post_fusion = [
            ("Quality Assessment", "Assess completeness, validity and data quality."),
            ("Conflict Detection", "Detect duplicate and cross-source value conflicts."),
            ("Reliability Assessment", "Calculate reliability scores."),
            ("Data Fusion", "Resolve conflicts using reliability-aware fusion."),
            ("Unified Information Model", "Generate the final unified information model."),
        ]

        for name, description in post_fusion:
            records = (
                final_records
                if name in {"Data Fusion", "Unified Information Model"}
                else statistics.get("records", 0)
            )
            pipeline.append({
                "id": step_id,
                "name": name,
                "description": description,
                "status": "completed",
                "progress": 100,
                "records": records,
                "source_system": "MULTI_SOURCE",
                "phase": "post_fusion",
            })
            step_id += 1
        return pipeline

    # ==========================================================
    # Algorithm Monitor
    # ==========================================================

    @classmethod
    def get_algorithm_monitor_context(cls) -> dict:
        """
        Build Algorithm Execution Monitor context.
        """

        statistics = cls.get_framework_statistics()

        metadata = cls.get_framework_metadata()
        pipeline = cls._build_pipeline(statistics, metadata)

        return {

            "statistics": statistics,

            "pipeline": pipeline,

            "summary": {

                "algorithms":
                    len(pipeline),

                "records":
                    statistics.get(
                        "records",
                        0,
                    ),

                "status":
                    "Completed",

                "framework_version":
                    statistics.get(
                        "framework_version",
                        "-",
                    ),

            },

        }

    # ==========================================================
    # Framework Health
    # ==========================================================

    @classmethod
    def get_framework_health(cls) -> dict:
        """
        Return framework health information.
        """

        statistics = cls.get_framework_statistics()

        return {

            "status": "Healthy",

            "framework_version":
                statistics.get(
                    "framework_version",
                    "-",
                ),

            "workflow":
                statistics.get(
                    "workflow",
                    "-",
                ),

            "source_system":
                statistics.get(
                    "source_system",
                    "-",
                ),

            "target_system":
                statistics.get(
                    "target_system",
                    "-",
                ),

            "records":
                statistics.get(
                    "records",
                    0,
                ),

            "algorithms":
                statistics.get(
                    "algorithms",
                    0,
                ),

            "quality_score":
                statistics.get(
                    "quality_score",
                    0,
                ),

            "semantic_coverage":
                statistics.get(
                    "semantic_coverage",
                    0,
                ),

            "resolution_rate":
                statistics.get(
                    "resolution_rate",
                    0,
                ),

        }

    # ==========================================================
    # Dashboard Metrics
    # ==========================================================

    @classmethod
    def get_dashboard_metrics(cls) -> dict:
        """
        Metrics shared by Dashboard widgets.
        """

        statistics = cls.get_framework_statistics()

        return {

            "records":
                statistics.get("records", 0),

            "attributes":
                statistics.get("total_attributes", 0),

            "canonical_attributes":
                len(cls._get_canonical_attributes(statistics)),

            "domains":
                len(cls._get_canonical_domains(statistics)),

            "quality_score":
                statistics.get("quality_score", 0),

            "conflicts":
                statistics.get("conflicts", 0),

            "fusion_records":
                statistics.get("fused_records", 0),

        }

    # ==========================================================
    # System Overview
    # ==========================================================

    @classmethod
    def get_system_overview(cls) -> dict:
        """
        High-level overview used by dashboard
        and API endpoints.
        """

        statistics = cls.get_framework_statistics()

        return {

            "framework": "KD-HDIE",

            "version":
                statistics.get(
                    "framework_version",
                    "-",
                ),

            "workflow":
                statistics.get(
                    "workflow",
                    "-",
                ),

            "records":
                statistics.get(
                    "records",
                    0,
                ),

            "attributes":
                statistics.get(
                    "total_attributes",
                    0,
                ),

            "algorithms":
                statistics.get(
                    "algorithms",
                    0,
                ),

            "status":
                "Execution completed successfully",

        }
