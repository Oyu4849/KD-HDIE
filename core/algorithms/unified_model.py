"""
KD-HDIE Framework

Unified Model Algorithm (Final v2.1)

Purpose
-------
Build the final unified information model from
harmonized heterogeneous data.

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.algorithms.base import (
    BaseAlgorithm,
    AlgorithmResult,
)

from core.interoperability.context import (
    InteroperabilityContext,
)

from attributes.models import (
    UnifiedRecord,
)


# ==========================================================
# Unified Information Model
# ==========================================================

@dataclass(slots=True)
class UnifiedInformationModel:

    records: list[UnifiedRecord]

    metadata: dict[str, Any] = field(default_factory=dict)

    statistics: dict[str, Any] = field(default_factory=dict)

    generated_by: str = "KD-HDIE Framework"

    version: str = "2.1"


# ==========================================================
# Unified Model Algorithm
# ==========================================================

class UnifiedModelAlgorithm(BaseAlgorithm):
    """
    Final algorithm of KD-HDIE Framework.
    """

    name = "UnifiedModel"

    order = 90

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        model = UnifiedInformationModel(

            records=data,

            metadata=dict(context.metadata),

            statistics=dict(context.statistics),

        )

        statistics = {

            "final_records": len(data),

            "fusion_decision_records": len(
                context.statistics.get("decision_records", [])
            ),

            "framework_version": model.version,

            "workflow": context.workflow,

            "source_system": context.source_system,

            "target_system": context.target_system,

        }

        #
        # Update Context
        #

        context.statistics.update(
            statistics
        )

        context.increment(
            "algorithms"
        )

        context.log(
            "Unified information model created."
        )

        return AlgorithmResult(

            success=True,

            data=model,

            message=(
                "Unified information model successfully created."
            ),

            metadata=statistics,

        )

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (
            "Build the final unified information model."
        )
