"""
KD-HDIE Framework

Fusion Algorithm (Final v3.0)

Purpose
-------
Fuse heterogeneous observations into a unified
representation using reliability-aware conflict resolution.

Responsibilities
----------------
• Merge duplicate attributes
• Detect numerical value conflicts
• Evaluate value consistency
• Combine reliability and consistency scores
• Select the most appropriate value
• Produce unified records
• Update interoperability statistics

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from collections import defaultdict
from math import exp, isfinite

from core.algorithms.base import (
    BaseAlgorithm,
    AlgorithmResult,
)

from core.interoperability.context import (
    InteroperabilityContext,
)

from attributes.models import (
    UnifiedAttribute,
    UnifiedRecord,
)


class FusionAlgorithm(BaseAlgorithm):
    """
    Reliability-aware Data Fusion Algorithm.
    """

    name = "Fusion"

    order = 80

    # =====================================================
    # Final score weights
    # =====================================================

    RELIABILITY_WEIGHT = 0.60
    CONSISTENCY_WEIGHT = 0.40

    # Keep conflict-resolution accounting aligned with ConflictAlgorithm.
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

        grouped: dict = defaultdict(list)

        # -------------------------------------------------
        # Group records by timestamp
        # -------------------------------------------------

        for record in data:

            grouped[
                record.timestamp
            ].append(record)

        fused_records: list[UnifiedRecord] = []

        conflicts_resolved = 0
        attributes_selected = 0
        decision_records = []

        # -------------------------------------------------
        # Fuse each timestamp group
        # -------------------------------------------------

        for timestamp, records in grouped.items():

            fused_record, stats = self._fuse_records(
                timestamp,
                records,
            )

            fused_records.append(
                fused_record
            )

            conflicts_resolved += (
                stats["conflicts_resolved"]
            )

            attributes_selected += (
                stats["attributes_selected"]
            )
            decision_records.extend(stats.get("decision_records", []))

        statistics = {

            "input_records":
                len(data),

            "fused_records":
                len(fused_records),

            "fusion_groups":
                len(grouped),

            "conflicts_resolved":
                conflicts_resolved,

            "attributes_selected":
                attributes_selected,

            "decision_records":
                decision_records,

        }

        context.statistics.update(
            statistics
        )
        context.statistics["fusion_decision_records"] = decision_records

        context.increment(
            "algorithms"
        )

        context.log(
            "Reliability-aware data fusion completed."
        )

        return AlgorithmResult(

            success=True,

            data=fused_records,

            message=(
                "Reliability-aware data fusion completed."
            ),

            metadata=statistics,

        )

    # =====================================================
    # Fuse One Timestamp
    # =====================================================

    def _fuse_records(
        self,
        timestamp,
        records,
    ) -> tuple[UnifiedRecord, dict]:

        result = UnifiedRecord()

        result.timestamp = timestamp

        grouped_attributes = defaultdict(list)

        # -------------------------------------------------
        # Collect attributes by observation timestamp and
        # canonical attribute. Fusion must never combine
        # different dates into one observation.
        # -------------------------------------------------

        for record in records:

            for attribute in record.attributes:

                grouped_attributes[
                    (record.timestamp, attribute.canonical_name)
                ].append(
                    attribute
                )

        conflicts_resolved = 0
        attributes_selected = 0
        decision_records = []

        # -------------------------------------------------
        # Process duplicate attributes
        # -------------------------------------------------

        for (timestamp, canonical_name), values in (
            grouped_attributes.items()
        ):

            sample = values[0]

            numeric_values = [

                attribute

                for attribute in values

                if isinstance(
                    attribute.value,
                    (int, float),
                )

                and isfinite(
                    float(attribute.value)
                )

            ]

            # =============================================
            # Numerical attributes
            # =============================================

            if numeric_values:

                selected = (
                    self._select_best_value(
                        numeric_values
                    )
                )

                numeric = [float(attribute.value) for attribute in numeric_values]
                min_value = min(numeric)
                max_value = max(numeric)
                discrepancy = max_value - min_value
                scale = max(abs(min_value), abs(max_value), 1.0)
                threshold = max(
                    self.ABSOLUTE_THRESHOLD,
                    self.RELATIVE_THRESHOLD * scale,
                )
                if discrepancy > threshold:
                    conflicts_resolved += 1

                selected_attribute = (
                    selected["attribute"]
                )

                fused_value = (
                    selected_attribute.value
                )

                attributes_selected += 1

                # -----------------------------------------
                # Preserve decision information
                # -----------------------------------------

                metadata = dict(
                    selected_attribute.metadata
                    or {}
                )

                candidate_details = [
                    {
                        "source": (
                            candidate["attribute"].source_system
                            or candidate["attribute"].source_name
                            or "UNKNOWN"
                        ),
                        "value": candidate["attribute"].value,
                        "reliability_score": round(candidate["reliability"], 6),
                        "consistency_score": round(candidate["consistency_score"], 6),
                        "final_score": round(candidate["final_score"], 6),
                    }
                    for candidate in self._rank_candidates(numeric_values)
                ]

                metadata.update({

                    "fusion_method":
                        "reliability_consistency",

                    "consistency_score":
                        round(
                            selected[
                                "consistency_score"
                            ],
                            6,
                        ),

                    "final_selection_score":
                        round(
                            selected[
                                "final_score"
                            ],
                            6,
                        ),

                    "selected_source":
                        (
                            selected_attribute
                            .source_system
                            or selected_attribute.source_name
                        ),

                    "candidate_count":
                        len(numeric_values),

                    "candidate_values": [
                        candidate["value"] for candidate in candidate_details
                    ],

                    "candidate_sources": [
                        candidate["source"] for candidate in candidate_details
                    ],

                    "candidate_scores": candidate_details,

                })

            # =============================================
            # Non-numerical attributes
            # =============================================

            else:

                selected_attribute = (
                    self._select_non_numeric(
                        values
                    )
                )

                fused_value = (
                    selected_attribute.value
                )

                metadata = dict(
                    selected_attribute.metadata
                    or {}
                )

                metadata.update({
                    "fusion_method":
                        "reliability_selection",
                })

            decision_records.append({
                "timestamp": timestamp,
                "canonical_attribute": canonical_name,
                "candidate_count": len(values),
                "candidate_values": [
                    attribute.value for attribute in values
                ],
                "candidate_sources": [
                    attribute.source_system
                    or attribute.source_name
                    or "UNKNOWN"
                    for attribute in values
                ],
                "selected_value": fused_value,
                "selected_source": (
                    selected_attribute.source_system
                    or selected_attribute.source_name
                    or "UNKNOWN"
                ),
                "resolution_method": metadata.get(
                    "fusion_method", "reliability_selection"
                ),
                "final_selection_score": metadata.get(
                    "final_selection_score"
                ),
            })

            # ---------------------------------------------
            # Unified attribute
            # ---------------------------------------------

            result.attributes.append(

                UnifiedAttribute(

                    source_name="FUSION",

                    canonical_name=canonical_name,

                    value=fused_value,

                    unit=sample.unit,

                    domain=sample.domain,

                    source_system="FUSION",

                    metadata=metadata,

                )
            )

        return result, {

            "conflicts_resolved":
                conflicts_resolved,

            "attributes_selected":
                attributes_selected,

            "decision_records":
                decision_records,

        }

    def _rank_candidates(self, attributes):
        """Rank numeric candidates by reliability and cross-source consistency."""
        numeric = [
            a for a in attributes
            if isinstance(a.value, (int, float))
            and isfinite(float(a.value))
        ]
        if not numeric:
            return []

        values = [float(a.value) for a in numeric]
        ranked = []
        for attribute in numeric:
            x = float(attribute.value)
            others = [v for v in values if v != x]
            if not others:
                consistency = 1.0
            else:
                scale = max(abs(x), *(abs(v) for v in others), 1.0)
                mean_distance = sum(abs(x - v) for v in others) / len(others)
                consistency = max(0.0, 1.0 - (mean_distance / scale))

            reliability = float((attribute.metadata or {}).get(
                "reliability_score", 0.0
            ))
            final_score = (
                self.RELIABILITY_WEIGHT * reliability
                + self.CONSISTENCY_WEIGHT * consistency
            )
            ranked.append({
                "attribute": attribute,
                "reliability": reliability,
                "consistency_score": consistency,
                "final_score": final_score,
            })

        return sorted(
            ranked,
            key=lambda item: (item["final_score"], item["reliability"]),
            reverse=True,
        )

    # =====================================================
    # Select Best Numerical Value
    # =====================================================

    def _select_best_value(
        self,
        attributes,
    ) -> dict:
        return self._rank_candidates(attributes)[0]

    # =====================================================
    # Select Best Non-Numerical Value
    # =====================================================

    @staticmethod
    def _select_non_numeric(
        attributes,
    ):

        return max(

            attributes,

            key=lambda attribute:

                float(
                    (
                        attribute.metadata
                        or {}
                    ).get(
                        "reliability_score",
                        0.0,
                    )
                ),

        )

    # =====================================================
    # Description
    # =====================================================

    @property
    def description(self) -> str:

        return (

            "Fuse heterogeneous observations using "
            "source reliability and value consistency "
            "to select the most appropriate value."

        )
