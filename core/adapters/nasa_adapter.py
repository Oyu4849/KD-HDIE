"""
KD-HDIE Framework

NASA POWER Adapter (Final v2.0)

Purpose
-------
Transforms NASA POWER API response into
framework UnifiedRecord objects.

Responsibilities
----------------
• Convert NASA POWER records into UnifiedRecord objects
• Resolve source attributes through Knowledge Reasoner
• Convert values according to canonical data types
• Preserve source and semantic metadata
• Return standardized AdapterResult
"""

from __future__ import annotations

from core.utils.time import normalize_observation_date

from typing import Any

from core.adapters.base_adapter import (
    BaseAdapter,
    AdapterResult,
)

from core.knowledge.reasoner import (
    knowledge_reasoner,
)

from attributes.models import (
    UnifiedRecord,
    UnifiedAttribute,
)


class NASAAdapter(BaseAdapter):
    """
    Adapter for NASA POWER API.

    Transforms heterogeneous NASA POWER
    response records into KD-HDIE
    UnifiedRecord objects.
    """

    source_type = "NASA"

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        records: list[dict[str, Any]],
    ) -> AdapterResult:

        unified_records: list[UnifiedRecord] = []

        skipped_attributes = 0

        for row in records:

            record, skipped = (
                self._convert_row(row)
            )

            unified_records.append(
                record
            )

            skipped_attributes += skipped

        return AdapterResult(

            success=True,

            records=unified_records,

            message=(
                "NASA POWER records "
                "successfully transformed."
            ),

            metadata={

                "source_type":
                    self.source_type,

                "input_records":
                    len(records),

                "output_records":
                    len(unified_records),

                "skipped_attributes":
                    skipped_attributes,

            },
        )

    # =====================================================
    # Convert One Row
    # =====================================================

    def _convert_row(
        self,
        row: dict[str, Any],
    ) -> tuple[UnifiedRecord, int]:

        record = UnifiedRecord()

        skipped_attributes = 0

        # -------------------------------------------------
        # Timestamp
        # -------------------------------------------------

        if "DATE" in row:

            record.timestamp = normalize_observation_date(row["DATE"])

        elif "date" in row:

            record.timestamp = normalize_observation_date(row["date"])

        elif "timestamp" in row:

            record.timestamp = normalize_observation_date(row["timestamp"])

        # -------------------------------------------------
        # Attributes
        # -------------------------------------------------

        for source_name, value in row.items():

            # NASA POWER uses DATE as a timestamp field.
            if source_name.upper() in (
                "DATE",
                "TIME",
                "TIMESTAMP",
            ):
                continue

            # -------------------------------------------------
            # Semantic resolution
            # -------------------------------------------------

            match = knowledge_reasoner.resolve(
                source_name
            )

            if not match.success:

                skipped_attributes += 1

                continue

            concept = match.concept

            # -------------------------------------------------
            # Value conversion
            # -------------------------------------------------

            converted_value = (
                self._convert_value(
                    value,
                    concept.data_type,
                )
            )

            # -------------------------------------------------
            # Unified attribute
            # -------------------------------------------------

            attribute = UnifiedAttribute(

                source_name=source_name,

                canonical_name=(
                    concept.canonical_name
                ),

                value=converted_value,

                unit=concept.unit,

                domain=(
                    concept.domain.value
                ),

                source_system=(
                    self.source_type
                ),

                metadata={

                    "adapter":
                        "NASAAdapter",

                    "source_type":
                        self.source_type,

                },
            )

            record.attributes.append(
                attribute
            )

        return (
            record,
            skipped_attributes,
        )

    # =====================================================
    # Value Conversion
    # =====================================================

    @staticmethod
    def _convert_value(
        value: Any,
        target_type: type,
    ) -> Any:

        if value is None:

            return None

        try:

            if target_type is float:

                return float(value)

            if target_type is int:

                return int(
                    float(value)
                )

            if target_type is str:

                return str(value)

            if target_type is bool:

                if isinstance(
                    value,
                    str,
                ):

                    return (
                        value.strip()
                        .lower()
                        in (
                            "true",
                            "1",
                            "yes",
                        )
                    )

                return bool(value)

            return value

        except (
            TypeError,
            ValueError,
        ):

            # Preserve the original value
            # when conversion is impossible.
            return value
