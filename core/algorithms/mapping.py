"""
KD-HDIE Framework

Mapping Algorithm (Final v2.1)

Purpose
-------
Creates interoperability mapping between
heterogeneous software systems.

Responsibilities
----------------
• Generate canonical attribute mapping
• Detect duplicate mappings
• Collect source statistics
• Update interoperability context

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from collections import defaultdict

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


class MappingAlgorithm(BaseAlgorithm):
    """
    Interoperability Mapping Algorithm.
    """

    name = "Mapping"

    order = 40

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        attribute_mapping: dict[str, set[str]] = defaultdict(set)

        source_statistics: dict[str, int] = defaultdict(int)

        mapped_attributes = 0

        #
        # Build interoperability mapping
        #

        for record in data:

            for attribute in record.attributes:

                attribute_mapping[
                    attribute.canonical_name
                ].add(attribute.source_name)

                source_statistics[
                    attribute.source_system
                ] += 1

                mapped_attributes += 1

        interoperability_map = {

            canonical: sorted(source_names)

            for canonical, source_names

            in attribute_mapping.items()

        }

        statistics = {

            "mapped_attributes":
                mapped_attributes,

            "canonical_attributes":
                len(interoperability_map),

            "source_systems":
                len(source_statistics),

            "source_statistics":
                dict(source_statistics),

        }

        #
        # Update Context
        #

        context.metadata[
            "attribute_mapping"
        ] = interoperability_map

        context.statistics.update(
            statistics
        )

        context.increment(
            "algorithms"
        )

        context.log(
            "Interoperability mapping created."
        )

        return AlgorithmResult(

            success=True,

            data=data,

            message=(
                "Attribute mapping successfully generated."
            ),

            metadata=statistics,

        )

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (
            "Generate canonical interoperability mapping "
            "between heterogeneous systems."
        )
