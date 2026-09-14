"""
KD-HDIE Framework

Generic API Adapter
Version: 1.0
"""

from __future__ import annotations

from typing import Any

from core.adapters.base_adapter import (
    BaseAdapter,
    AdapterResult,
)

from core.knowledge.reasoner import knowledge_reasoner

from attributes.models import (
    UnifiedRecord,
    UnifiedAttribute,
)


class GenericAPIAdapter(BaseAdapter):
    """
    Adapter for runtime-configured generic REST/JSON APIs.

    Semantic resolution is delegated to the existing
    Knowledge Reasoner and Knowledge Ontology.
    """

    source_type = "GENERIC_API"

    def execute(
        self,
        records: list[dict[str, Any]],
    ) -> AdapterResult:

        unified_records: list[UnifiedRecord] = []
        skipped_attributes = 0

        for row in records:

            record, skipped = self._convert_row(row)

            unified_records.append(record)
            skipped_attributes += skipped

        return AdapterResult(
            success=True,
            records=unified_records,
            message=(
                "Generic API records "
                "successfully transformed."
            ),
            metadata={
                "source_type": self.source_type,
                "input_records": len(records),
                "output_records": len(unified_records),
                "skipped_attributes": skipped_attributes,
            },
        )

    def _convert_row(
        self,
        row: dict[str, Any],
    ) -> tuple[UnifiedRecord, int]:

        record = UnifiedRecord()
        skipped_attributes = 0

        timestamp_key = self._find_timestamp_key(row)

        if timestamp_key is not None:
            record.timestamp = row[timestamp_key]

        for source_name, value in row.items():

            if self._is_timestamp_field(source_name):
                continue

            match = knowledge_reasoner.resolve(source_name)

            if not match.success:
                skipped_attributes += 1
                continue

            concept = match.concept

            converted_value = self._convert_value(
                value,
                concept.data_type,
            )

            attribute = UnifiedAttribute(
                source_name=source_name,
                canonical_name=concept.canonical_name,
                value=converted_value,
                unit=concept.unit,
                domain=concept.domain.value,
                source_system=self.source_type,
                metadata={
                    "adapter": "GenericAPIAdapter",
                    "source_type": self.source_type,
                },
            )

            record.attributes.append(attribute)

        return record, skipped_attributes

    @staticmethod
    def _find_timestamp_key(
        row: dict[str, Any],
    ) -> str | None:

        candidates = (
            "time",
            "date",
            "datetime",
            "timestamp",
            "date_time",
            "created_at",
            "observed_at",
        )

        lowered = {
            str(key).lower(): key
            for key in row.keys()
        }

        for candidate in candidates:
            if candidate in lowered:
                return lowered[candidate]

        return None

    @staticmethod
    def _is_timestamp_field(
        source_name: str,
    ) -> bool:

        return (
            str(source_name).lower()
            in {
                "time",
                "date",
                "datetime",
                "timestamp",
                "date_time",
                "created_at",
                "observed_at",
            }
        )

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
                return int(float(value))

            if target_type is str:
                return str(value)

            if target_type is bool:

                if isinstance(value, str):
                    return (
                        value.strip().lower()
                        in ("true", "1", "yes")
                    )

                return bool(value)

            return value

        except (TypeError, ValueError):
            return value
