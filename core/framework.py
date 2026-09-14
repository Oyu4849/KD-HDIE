"""
KD-HDIE Framework

Framework (Final v2.2)

Purpose
-------
Public entry point of the KD-HDIE Framework.

Responsibilities
----------------
• Framework facade
• Execute single-source interoperability
• Execute multi-source interoperability
• Expose framework information

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from typing import Any

from core.registry import registry

from core.interoperability.service import (
    InteroperabilityService,
)

from core.interoperability.result import (
    InteroperabilityResult,
)


class KDHDIEFramework:
    """
    Public facade of KD-HDIE Framework.

    Provides a stable application-level interface
    for single-source and multi-source execution.
    """

    def __init__(self):

        self._service = (
            InteroperabilityService()
        )

    # =====================================================
    # Execute — Single Source
    # =====================================================

    def execute(
        self,
        *,
        source_system: str,
        target_system: str = "KD-HDIE",
        connection_parameters: dict,
        operation: str = "INTEROPERABILITY",
        workflow: str = "DEFAULT",
    ) -> InteroperabilityResult:
        """
        Execute complete single-source
        interoperability pipeline.
        """

        return self._service.execute(

            source_system=source_system,

            target_system=target_system,

            connection_parameters=(
                connection_parameters
            ),

            operation=operation,

            workflow_name=workflow,

        )

    # =====================================================
    # Execute — Multi Source
    # =====================================================

    def execute_multi_source(
        self,
        *,
        sources: list[dict[str, Any]],
        workflow: str = "DEFAULT",
    ) -> InteroperabilityResult:
        """
        Execute complete multi-source
        interoperability pipeline.

        Parameters
        ----------
        sources:
            List of heterogeneous source definitions.

        Example
        -------
        [
            {
                "source_system": "OPENMETEO",
                "connection_parameters": {
                    "latitude": 45.0,
                    "longitude": 59.0,
                    "start_date": "2025-01-01",
                    "end_date": "2025-12-31",
                    "historical": True,
                },
            },
            {
                "source_system": "NASA",
                "connection_parameters": {
                    "latitude": 45.0,
                    "longitude": 59.0,
                    "start": "2025",
                    "end": "2025",
                    "parameters": [
                        "T2M",
                        "PRECTOTCORR",
                        "RH2M",
                        "WS2M",
                    ],
                },
            },
        ]

        Processing
        ----------
        Each source is processed independently
        before the source-level results are merged.

        After merging:

            Quality
                ↓
            Conflict
                ↓
            Reliability
                ↓
            Fusion
                ↓
            UnifiedModel
        """

        return (
            self._service.execute_multi_source(

                sources=sources,

                workflow_name=workflow,

            )
        )

    # =====================================================
    # Framework Information
    # =====================================================

    @property
    def algorithms(self):

        return registry.algorithms()

    # -----------------------------------------------------

    @property
    def workflows(self):

        return registry.workflows()

    # -----------------------------------------------------

    @property
    def adapters(self):

        return registry.adapters()

    # =====================================================
    # Information
    # =====================================================

    def info(self) -> dict:

        statistics = (
            registry.statistics()
        )

        return {

            "framework":
                "KD-HDIE",

            "version":
                "2.2",

            "algorithms":
                statistics["algorithms"],

            "adapters":
                statistics["adapters"],

            "workflows":
                statistics["workflows"],

            "multi_source":
                True,

        }
