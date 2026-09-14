"""
KD-HDIE Framework

Harmonization Algorithm (Final v2.1)

Purpose
-------
Standardizes heterogeneous environmental data
into a unified representation.

Responsibilities
----------------
• Normalize timestamps
• Normalize values
• Harmonize data types
• Update interoperability context

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from datetime import datetime

from core.algorithms.base import (
    BaseAlgorithm,
    AlgorithmResult,
)

from core.interoperability.context import (
    InteroperabilityContext,
)

from attributes.models import UnifiedRecord


class HarmonizationAlgorithm(BaseAlgorithm):
    """
    Data Harmonization Algorithm.
    """

    name = "Harmonization"

    order = 50

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        harmonized_records = 0
        harmonized_attributes = 0

        for record in data:

            #
            # Timestamp harmonization
            #

            record.timestamp = self._normalize_timestamp(
                record.timestamp
            )

            harmonized_records += 1

            #
            # Attribute harmonization
            #

            for attribute in record.attributes:

                attribute.value = self._normalize_value(
                    attribute.value
                )

                harmonized_attributes += 1

        statistics = {

            "harmonized_records":
                harmonized_records,

            "harmonized_attributes":
                harmonized_attributes,

        }

        context.statistics.update(
            statistics
        )

        context.increment(
            "algorithms"
        )

        context.log(
            "Data harmonization completed."
        )

        return AlgorithmResult(

            success=True,

            data=data,

            message="Data harmonization completed.",

            metadata=statistics,

        )

    # =====================================================
    # Normalize Timestamp
    # =====================================================

    def _normalize_timestamp(
        self,
        value,
    ):

        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        #
        # YYYY-MM
        #

        try:

            return datetime.strptime(
                str(value),
                "%Y-%m",
            )

        except ValueError:
            pass

        #
        # YYYY-MM-DD
        #

        try:

            return datetime.strptime(
                str(value),
                "%Y-%m-%d",
            )

        except ValueError:

            return value

    # =====================================================
    # Normalize Value
    # =====================================================

    def _normalize_value(
        self,
        value,
    ):

        if value is None:
            return None

        if isinstance(value, float):
            return round(value, 6)

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            return value.strip()

        return value

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (
            "Normalize heterogeneous values into "
            "a unified representation."
        )
