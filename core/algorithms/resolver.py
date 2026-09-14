"""
KD-HDIE Framework

Resolver Algorithm (Final v2.1)

Purpose
-------
Resolve heterogeneous source attributes into
canonical semantic attributes using the
knowledge base.

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


class ResolverAlgorithm(BaseAlgorithm):
    """
    Semantic Attribute Resolver.
    """

    name = "Resolver"

    order = 20

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        resolved = 0
        unresolved = 0

        for record in data:

            for attribute in record.attributes:

                match = knowledge_reasoner.resolve(
                    attribute.source_name
                )

                if not match.success:

                    unresolved += 1
                    continue

                attribute.canonical_name = (
                    match.canonical_name
                )

                resolved += 1

        statistics = {

            "resolved_attributes": resolved,

            "unresolved_attributes": unresolved,

            "resolution_rate": (
                round(
                    resolved / (resolved + unresolved),
                    4,
                )
                if (resolved + unresolved) > 0
                else 1.0
            ),

        }

        context.statistics.update(statistics)

        context.increment("algorithms")

        context.log(
            f"Resolver completed ({resolved} resolved, "
            f"{unresolved} unresolved)."
        )

        return AlgorithmResult(

            success=True,

            data=data,

            message="Semantic attribute resolution completed.",

            metadata=statistics,

        )

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (
            "Resolve heterogeneous attribute names "
            "into canonical semantic concepts."
        )
