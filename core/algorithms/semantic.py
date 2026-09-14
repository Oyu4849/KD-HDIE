"""
KD-HDIE Framework

Semantic Algorithm (Final v2.1)

Purpose
-------
Validate semantic consistency of heterogeneous
attributes using the ontology and knowledge base.

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from core.algorithms.base import (
    BaseAlgorithm,
    AlgorithmResult,
)

from core.interoperability.context import (
    InteroperabilityContext,
)

from core.knowledge.reasoner import (
    knowledge_reasoner,
)

from attributes.models import (
    UnifiedRecord,
)


class SemanticAlgorithm(BaseAlgorithm):
    """
    Semantic validation algorithm.
    """

    name = "Semantic"

    order = 30

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        validated = 0
        invalid = 0

        for record in data:

            for attribute in record.attributes:

                #
                # Canonical concept validation
                #

                if not knowledge_reasoner.validate(
                    attribute.canonical_name
                ):

                    invalid += 1
                    continue

                #
                # Domain inference
                #

                expected_domain = (
                    knowledge_reasoner.infer_domain(
                        attribute.canonical_name
                    )
                )

                if expected_domain is not None:
                    attribute.domain = (
                        expected_domain.value
                    )

                #
                # Unit inference
                #

                expected_unit = (
                    knowledge_reasoner.infer_unit(
                        attribute.canonical_name
                    )
                )

                if expected_unit:
                    attribute.unit = expected_unit

                #
                # Data type inference
                #

                expected_type = (
                    knowledge_reasoner.infer_type(
                        attribute.canonical_name
                    )
                )

                if expected_type is not None:

                    try:

                        attribute.value = expected_type(
                            attribute.value
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        invalid += 1
                        continue

                validated += 1

        total = validated + invalid

        coverage = (
            validated / total
            if total > 0
            else 1.0
        )

        statistics = {

            "semantic_validated": validated,

            "semantic_invalid": invalid,

            "semantic_coverage": round(
                coverage,
                4,
            ),

        }

        context.statistics.update(
            statistics
        )

        context.increment(
            "algorithms"
        )

        context.log(
            "Semantic validation completed."
        )

        return AlgorithmResult(

            success=True,

            data=data,

            message=(
                "Semantic validation completed successfully."
            ),

            metadata=statistics,

        )

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (
            "Validate semantic consistency "
            "using ontology and knowledge base."
        )
