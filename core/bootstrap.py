"""
KD-HDIE Framework

Bootstrap (Final v4.1)

Initial registration of all framework components.
"""

from __future__ import annotations

import logging

from datasource.connectors.manager import connector_manager
from datasource.connectors.csv_connector import CSVConnector
from datasource.connectors.gee_export_connector import GEEExportConnector
from datasource.connectors.generic_api_connector import GenericAPIConnector

from core.registry import registry

from core.adapters.csv_adapter import CSVAdapter
from core.adapters.gee_adapter import GEEAdapter
from core.adapters.openmeteo_adapter import OpenMeteoAdapter
from core.adapters.nasa_adapter import NASAAdapter
from core.adapters.generic_api_adapter import GenericAPIAdapter

from core.algorithms.metadata import MetadataAlgorithm
from core.algorithms.resolver import ResolverAlgorithm
from core.algorithms.semantic import SemanticAlgorithm
from core.algorithms.mapping import MappingAlgorithm
from core.algorithms.harmonization import HarmonizationAlgorithm
from core.algorithms.quality import QualityAlgorithm
from core.algorithms.conflict import ConflictAlgorithm
from core.algorithms.reliability import SourceReliabilityAlgorithm
from core.algorithms.fusion import FusionAlgorithm
from core.algorithms.unified_model import UnifiedModelAlgorithm

from core.interoperability.workflow import WorkflowFactory
from datasource.connectors.openmeteo_connector import OpenMeteoConnector
from datasource.connectors.nasa_connector import NASAConnector
from core.interoperability.normalizers.tabular import TabularResponseNormalizer
from core.algorithms.monthly_aggregation import MonthlyAggregationAlgorithm

logger = logging.getLogger(__name__)

_initialized = False


def bootstrap() -> None:
    """
    Initialize KD-HDIE Framework.
    """

    global _initialized

    if _initialized:
        return

    # =====================================================
    # CONNECTORS
    # =====================================================

    try:

        connector_manager.register(
            CSVConnector()
        )

        connector_manager.register(
            OpenMeteoConnector()
        )

        connector_manager.register(
            GEEExportConnector()
        )

        connector_manager.register(
            NASAConnector()
        )

        # Generic runtime-configurable REST/JSON API.
        connector_manager.register(
            GenericAPIConnector()
        )

    except Exception as ex:

        logger.exception(ex)

        raise

    # =====================================================
    # ADAPTERS
    # =====================================================

    registry.register_adapter(
        "CSV",
        CSVAdapter(),
    )

    registry.register_adapter(
        "OPENMETEO",
        OpenMeteoAdapter(),
    )

    registry.register_adapter(
        "GEE",
        GEEAdapter(),
    )

    registry.register_adapter(
        "NASA",
        NASAAdapter(),
    )

    registry.register_adapter(
        "GENERIC_API",
        GenericAPIAdapter(),
    )

    # =====================================================
    # ALGORITHMS
    # =====================================================

    algorithms = [

        MetadataAlgorithm(),

        ResolverAlgorithm(),

        SemanticAlgorithm(),

        MappingAlgorithm(),

        HarmonizationAlgorithm(),

        MonthlyAggregationAlgorithm(),

        QualityAlgorithm(),

        ConflictAlgorithm(),

        SourceReliabilityAlgorithm(),

        FusionAlgorithm(),

        UnifiedModelAlgorithm(),

    ]

    for algorithm in algorithms:

        registry.register_algorithm(
            algorithm
        )

    # =====================================================
    # WORKFLOW
    # =====================================================

    registry.register_workflow(
        WorkflowFactory.default()
    )

    # =====================================================
    # READY
    # =====================================================

    _initialized = True

    logger.info(
        "KD-HDIE Framework initialized successfully."
    )
