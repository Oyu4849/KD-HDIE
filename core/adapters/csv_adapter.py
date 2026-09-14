"""
KD-HDIE Framework

CSV Adapter (Final v2.1)

Purpose
-------
Transforms CSV connector output into
UnifiedRecord objects used by the KD-HDIE Framework.
"""

from __future__ import annotations

from core.utils.time import normalize_observation_date

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


class CSVAdapter(BaseAdapter):
    """
    Adapter for CSV heterogeneous datasets.
    """

    source_type = "CSV"

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        records: list[dict[str, Any]],
    ) -> AdapterResult:

        unified_records: list[UnifiedRecord] = []

        for row in records:
            unified_records.append(
                self._convert_row(row)
            )

        return AdapterResult(
            success=True,
            records=unified_records,
            message="CSV records successfully transformed.",
            metadata={
                "source_type": self.source_type,
                "input_records": len(records),
                "output_records": len(unified_records),
            },
        )

    # =====================================================
    # Convert One Row
    # =====================================================

    def _convert_row(
        self,
        row: dict[str, Any],
    ) -> UnifiedRecord:

        record = UnifiedRecord()

        #
        # Timestamp
        #

        record.timestamp = normalize_observation_date(row.get("date") or row.get("DATE") or row.get("timestamp"))

        #
        # Attributes
        #

        for source_name, value in row.items():

            if source_name.lower() == "date":
                continue

            match = knowledge_reasoner.resolve(
                source_name
            )

            if not match.success:
                continue

            concept = match.concept

            record.attributes.append(

                UnifiedAttribute(

                    source_name=source_name,

                    canonical_name=concept.canonical_name,

                    value=self._convert_value(
                        value,
                        concept.data_type,
                    ),

                    unit=concept.unit,

                    domain=concept.domain.value,

                    source_system=self.source_type,

                )

            )

        return record

    # =====================================================
    # Value Conversion
    # =====================================================

    def _convert_value(
        self,
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
                    return value.strip().lower() in (
                        "true",
                        "1",
                        "yes",
                    )

                return bool(value)

            return value

        except (TypeError, ValueError):

            return value
