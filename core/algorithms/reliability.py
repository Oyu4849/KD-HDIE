"""
KD-HDIE Framework

Source Reliability Algorithm

Purpose
-------
Heterogeneous data source reliability assessment.

The algorithm evaluates:
1. Completeness
2. Validity
3. Historical stability
4. Optional reference-based accuracy

The final value selection is performed later by Fusion.
"""

from __future__ import annotations

from collections import defaultdict
from math import isfinite
from statistics import mean, pstdev
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


class SourceReliabilityAlgorithm(BaseAlgorithm):
    """
    Assess reliability of heterogeneous source attributes.
    """

    name = "Reliability"

    order = 75

    # -----------------------------------------------------
    # Weights without a trusted reference value
    # -----------------------------------------------------

    DEFAULT_WEIGHTS = {
        "completeness": 0.35,
        "validity": 0.35,
        "stability": 0.30,
    }

    # -----------------------------------------------------
    # Weights when a trusted reference value exists
    # -----------------------------------------------------

    REFERENCE_WEIGHTS = {
        "accuracy": 0.35,
        "completeness": 0.20,
        "validity": 0.25,
        "stability": 0.20,
    }

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context: InteroperabilityContext,
    ) -> AlgorithmResult:

        source_values = self._collect_source_values(data)

        reference_values = context.shared_data.get(
            "reference_values",
            {},
        )

        reliability_scores = {}
        attribute_scores = {}

        total_attributes = 0

        for record in data:

            for attribute in record.attributes:

                total_attributes += 1

                source = (
                    attribute.source_system
                    or attribute.source_name
                    or "UNKNOWN"
                )

                key = (
                    source,
                    attribute.canonical_name,
                )

                values = source_values.get(
                    key,
                    [],
                )

                # -----------------------------------------
                # 1. Completeness
                # -----------------------------------------

                completeness = (
                    1.0
                    if attribute.value is not None
                    else 0.0
                )

                # -----------------------------------------
                # 2. Validity
                # -----------------------------------------

                validity = self._validity_score(
                    attribute
                )

                # -----------------------------------------
                # 3. Historical stability
                # -----------------------------------------

                stability = self._stability_score(
                    values
                )

                # -----------------------------------------
                # 4. Optional reference accuracy
                # -----------------------------------------

                reference = reference_values.get(
                    attribute.canonical_name
                )

                accuracy = None

                if (
                    reference is not None
                    and isinstance(
                        attribute.value,
                        (int, float),
                    )
                    and isfinite(
                        float(attribute.value)
                    )
                ):
                    accuracy = self._accuracy_score(
                        float(attribute.value),
                        float(reference),
                    )

                # -----------------------------------------
                # 5. Final reliability
                # -----------------------------------------

                reliability = (
                    self._calculate_reliability(
                        accuracy=accuracy,
                        completeness=completeness,
                        validity=validity,
                        stability=stability,
                    )
                )

                # -----------------------------------------
                # Save to attribute metadata
                # -----------------------------------------

                attribute.metadata.update({

                    "reliability_accuracy": (
                        round(accuracy, 6)
                        if accuracy is not None
                        else None
                    ),

                    "reliability_completeness":
                        round(
                            completeness,
                            6,
                        ),

                    "reliability_validity":
                        round(
                            validity,
                            6,
                        ),

                    "reliability_stability":
                        round(
                            stability,
                            6,
                        ),

                    "reliability_score":
                        round(
                            reliability,
                            6,
                        ),
                })

                source_key = (
                    f"{source}:"
                    f"{attribute.canonical_name}"
                )

                reliability_scores[
                    source_key
                ] = reliability

                attribute_scores[
                    source_key
                ] = {

                    "accuracy": (
                        accuracy
                        if accuracy is not None
                        else None
                    ),

                    "completeness":
                        completeness,

                    "validity":
                        validity,

                    "stability":
                        stability,

                    "reliability":
                        reliability,
                }

        scores = list(
            reliability_scores.values()
        )

        statistics = {

            "reliability_attributes":
                total_attributes,

            "reliability_mean":
                round(
                    mean(scores),
                    4,
                ) if scores else 0.0,

            "reliability_min":
                round(
                    min(scores),
                    4,
                ) if scores else 0.0,

            "reliability_max":
                round(
                    max(scores),
                    4,
                ) if scores else 0.0,

            "reference_available":
                bool(reference_values),

            "reliability_method": (
                "reference_weighted"
                if reference_values
                else "quality_stability_weighted"
            ),
        }

        # =================================================
        # Context
        # =================================================

        context.shared_data[
            "reliability_scores"
        ] = reliability_scores

        context.shared_data[
            "attribute_reliability"
        ] = attribute_scores

        context.statistics.update(
            statistics
        )

        context.metadata[
            "reliability_weights"
        ] = (
            self.REFERENCE_WEIGHTS
            if reference_values
            else self.DEFAULT_WEIGHTS
        )

        context.increment(
            "algorithms"
        )

        context.log(
            "Source reliability assessment completed "
            f"(mean={statistics['reliability_mean']:.4f})."
        )

        return AlgorithmResult(

            success=True,

            data=data,

            message=(
                "Source reliability assessment completed."
            ),

            metadata=statistics,
        )

    # =====================================================
    # Collect source values
    # =====================================================

    @staticmethod
    def _collect_source_values(
        data: list[UnifiedRecord],
    ):

        grouped = defaultdict(list)

        for record in data:

            for attribute in record.attributes:

                if not isinstance(
                    attribute.value,
                    (int, float),
                ):
                    continue

                if not isfinite(
                    float(attribute.value)
                ):
                    continue

                source = (
                    attribute.source_system
                    or attribute.source_name
                    or "UNKNOWN"
                )

                grouped[
                    (
                        source,
                        attribute.canonical_name,
                    )
                ].append(
                    float(attribute.value)
                )

        return grouped

    # =====================================================
    # Validity score
    # =====================================================

    @staticmethod
    def _validity_score(
        attribute: Any,
    ) -> float:

        if attribute.value is None:
            return 0.0

        score = 0.0

        if attribute.canonical_name:
            score += 0.25

        if attribute.domain:
            score += 0.25

        if attribute.unit is not None:
            score += 0.25

        if (
            isinstance(
                attribute.value,
                (int, float),
            )
            and isfinite(
                float(attribute.value)
            )
        ) or isinstance(
            attribute.value,
            str,
        ):
            score += 0.25

        return score

    # =====================================================
    # Historical stability
    # =====================================================

    @staticmethod
    def _stability_score(
        values: list[float],
    ) -> float:

        if not values:
            return 0.0

        if len(values) == 1:
            return 1.0

        dispersion = pstdev(values)

        return 1.0 / (
            1.0 + dispersion
        )

    # =====================================================
    # Reference accuracy
    # =====================================================

    @staticmethod
    def _accuracy_score(
        value: float,
        reference: float,
    ) -> float:

        error = abs(
            value - reference
        )

        return 1.0 / (
            1.0 + error
        )

    # =====================================================
    # Reliability calculation
    # =====================================================

    def _calculate_reliability(
        self,
        *,
        accuracy: float | None,
        completeness: float,
        validity: float,
        stability: float,
    ) -> float:

        if accuracy is not None:

            weights = (
                self.REFERENCE_WEIGHTS
            )

            score = (

                weights["accuracy"]
                * accuracy

                + weights["completeness"]
                * completeness

                + weights["validity"]
                * validity

                + weights["stability"]
                * stability
            )

        else:

            weights = (
                self.DEFAULT_WEIGHTS
            )

            score = (

                weights["completeness"]
                * completeness

                + weights["validity"]
                * validity

                + weights["stability"]
                * stability
            )

        return max(
            0.0,
            min(
                1.0,
                score,
            ),
        )

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (
            "Assess source reliability using "
            "completeness, validity, historical "
            "stability and optional reference-based "
            "accuracy."
        )
