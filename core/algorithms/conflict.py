"""
KD-HDIE Framework

Conflict Algorithm (Final v2.1)

Purpose
-------
Detect semantic conflicts between heterogeneous
software systems before data fusion.

Responsibilities
----------------
• Detect duplicate attributes
• Detect unit conflicts
• Detect value conflicts
• Update interoperability context

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from collections import defaultdict
from math import isfinite

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


class ConflictAlgorithm(BaseAlgorithm):
    """
    Semantic Conflict Detection Algorithm.
    """

    name = "Conflict"

    order = 70

    # Configurable discrepancy threshold. These are experimental
    # parameters, not universal constants.
    RELATIVE_THRESHOLD = 0.05
    ABSOLUTE_THRESHOLD = 0.10

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        grouped = defaultdict(
            lambda: defaultdict(list)
        )

        #
        # timestamp -> canonical -> attributes
        #

        for record in data:

            timestamp = record.timestamp

            for attribute in record.attributes:

                grouped[
                    timestamp
                ][
                    attribute.canonical_name
                ].append(attribute)

        checked_groups = 0
        conflict_count = 0
        duplicate_groups = 0
        unit_conflicts = 0
        value_conflicts = 0

        #
        # Conflict Detection
        #

        for _, attributes in grouped.items():

            for _, values in attributes.items():

                checked_groups += 1

                if len(values) < 2:
                    continue

                duplicate_groups += 1

                #
                # Unit conflict
                #

                units = {

                    value.unit

                    for value in values

                }

                if len(units) > 1:

                    unit_conflicts += 1
                    conflict_count += 1

                    continue

                #
                # Value conflict
                #

                numeric = [
                    float(value.value)
                    for value in values
                    if isinstance(value.value, (int, float))
                    and isfinite(float(value.value))
                ]

                if len(numeric) >= 2:
                    min_value = min(numeric)
                    max_value = max(numeric)
                    discrepancy = max_value - min_value
                    scale = max(abs(min_value), abs(max_value), 1.0)
                    threshold = max(
                        self.ABSOLUTE_THRESHOLD,
                        self.RELATIVE_THRESHOLD * scale,
                    )
                    is_conflict = discrepancy > threshold
                else:
                    unique_values = {value.value for value in values}
                    is_conflict = len(unique_values) > 1

                if is_conflict:
                    value_conflicts += 1
                    conflict_count += 1

        #
        # Statistics
        #

        statistics = {

            "checked_groups":
                checked_groups,

            "duplicate_groups":
                duplicate_groups,

            "conflicts":
                conflict_count,

            "unit_conflicts":
                unit_conflicts,

            "value_conflicts":
                value_conflicts,

            "relative_threshold": self.RELATIVE_THRESHOLD,

            "absolute_threshold": self.ABSOLUTE_THRESHOLD,

            "conflict_rate":

                round(

                    conflict_count
                    / checked_groups,

                    4,

                )

                if checked_groups

                else 0.0,

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

            f"Conflict detection completed "

            f"({conflict_count} conflicts found)."

        )

        return AlgorithmResult(

            success=True,

            data=data,

            message=(
                "Conflict detection completed."
            ),

            metadata=statistics,

        )

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (

            "Detect semantic conflicts "

            "between heterogeneous systems."

        )
