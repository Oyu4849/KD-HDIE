"""
KD-HDIE Framework

Metadata Algorithm (Final v2.1)

Purpose
-------
Extract metadata from heterogeneous datasets and
update interoperability context.

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from collections import Counter

from core.algorithms.base import (
    BaseAlgorithm,
    AlgorithmResult,
)

from core.interoperability.context import (
    InteroperabilityContext,
)

from attributes.models import UnifiedRecord


class MetadataAlgorithm(BaseAlgorithm):
    """
    Metadata Extraction Algorithm.
    """

    name = "Metadata"

    order = 10

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        statistics = self._extract_statistics(data)

        context.statistics.update(statistics)

        context.increment("algorithms")

        context.log(
            "Metadata extraction completed."
        )

        return AlgorithmResult(
            success=True,
            data=data,
            message="Metadata successfully extracted.",
            metadata=statistics,
        )

    # =====================================================
    # Statistics
    # =====================================================

    def _extract_statistics(
        self,
        data: list[UnifiedRecord],
    ) -> dict:

        record_count = len(data)

        attribute_counter = Counter()

        domain_counter = Counter()

        missing_values = 0

        total_attributes = 0

        for record in data:

            for attribute in record.attributes:

                total_attributes += 1

                attribute_counter.update(
                    [attribute.canonical_name]
                )

                domain_counter.update(
                    [attribute.domain]
                )

                if attribute.value is None:
                    missing_values += 1

        return {

            "records": record_count,

            "total_attributes": total_attributes,

            "unique_attributes": len(attribute_counter),

            "unique_domains": len(domain_counter),

            "missing_values": missing_values,

            "attributes": dict(attribute_counter),

            "domains": dict(domain_counter),

        }

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (
            "Extract metadata from heterogeneous datasets."
        )
