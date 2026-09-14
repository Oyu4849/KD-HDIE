"""
KD-HDIE Framework

Quality Algorithm (Final v2.1)

Purpose
-------
Evaluate the quality of heterogeneous data after
semantic harmonization.

Responsibilities
----------------
• Assess completeness
• Assess validity
• Calculate quality score
• Update interoperability context

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from core.knowledge.reasoner import knowledge_reasoner

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


class QualityAlgorithm(BaseAlgorithm):
    """
    Data Quality Assessment Algorithm.
    """

    name = "Quality"

    order = 60

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        total_attributes = 0
        valid_attributes = 0
        missing_values = 0

        for record in data:

            for attribute in record.attributes:

                total_attributes += 1

                #
                # Missing value
                #

                if attribute.value is None:

                    missing_values += 1
                    continue

                #
                # Canonical name
                #

                if not attribute.canonical_name:
                    continue

                if not attribute.canonical_name:
                    continue

                expected_domain = knowledge_reasoner.infer_domain(
                    attribute.canonical_name
                )
                if expected_domain is not None and attribute.domain != expected_domain.value:
                    continue

                expected_unit = knowledge_reasoner.infer_unit(
                    attribute.canonical_name
                )
                if expected_unit is not None and attribute.unit != expected_unit:
                    continue

                if not self._value_in_domain(attribute.canonical_name, attribute.value):
                    continue

                valid_attributes += 1

        #
        # Quality Metrics
        #

        if total_attributes == 0:

            completeness = 0.0
            validity = 0.0

        else:

            completeness = (
                total_attributes - missing_values
            ) / total_attributes

            validity = (
                valid_attributes
            ) / total_attributes

        quality_score = (
            completeness + validity
        ) / 2

        statistics = {

            "total_attributes":
                total_attributes,

            "valid_attributes":
                valid_attributes,

            "missing_values":
                missing_values,

            "completeness":
                round(completeness, 4),

            "validity":
                round(validity, 4),

            "quality_score":
                round(quality_score, 4),

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
            f"Quality assessment completed "
            f"(score={quality_score:.4f})."
        )

        return AlgorithmResult(

            success=True,

            data=data,

            message=(
                "Data quality assessment completed."
            ),

            metadata=statistics,

        )


    @staticmethod
    def _value_in_domain(canonical_name, value) -> bool:
        if value is None:
            return False
        if not isinstance(value, (int, float)):
            return True
        x = float(value)
        if canonical_name in {"ndvi", "msavi", "mndwi", "bsi"}:
            return -1.0 <= x <= 1.0
        if canonical_name == "relative_humidity":
            return 0.0 <= x <= 100.0
        if canonical_name in {"precipitation", "wind_speed", "soil_moisture", "surface_water_area"}:
            return x >= 0.0
        return True

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (
            "Evaluate heterogeneous data quality "
            "using completeness and validity metrics."
        )
