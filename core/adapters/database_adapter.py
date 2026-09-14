"""
KD-HDIE Framework

Database Adapter (Final)

Purpose
-------
Transforms database query results into
framework UnifiedRecord objects.
"""

from __future__ import annotations

from typing import Any

from core.adapters.base_adapter import BaseAdapter
from core.knowledge.reasoner import knowledge_reasoner

from attributes.models import (
    UnifiedAttribute,
    UnifiedRecord,
)


class DatabaseAdapter(BaseAdapter):
    """
    Adapter for relational databases.
    """

    source_type = "DATABASE"

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        records: list[dict[str, Any]],
    ) -> list[UnifiedRecord]:

        unified_records: list[UnifiedRecord] = []

        for row in records:

            unified_records.append(
                self._convert_row(row)
            )

        return unified_records

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

        if "date" in row:

            record.timestamp = row["date"]

        elif "timestamp" in row:

            record.timestamp = row["timestamp"]

        #
        # Attributes
        #

        for source_name, value in row.items():

            if source_name.lower() in (
                "date",
                "timestamp",
            ):
                continue

            match = knowledge_reasoner.resolve(
                source_name
            )

            if not match.success:
                continue

            concept = match.concept

            attribute = UnifiedAttribute(

                source_name=source_name,

                canonical_name=concept.canonical_name,

                value=self._convert_value(
                    value,
                    concept.data_type,
                ),

                unit=concept.unit,

                domain=concept.domain.value,

                source_system="DATABASE",

            )

            record.attributes.append(attribute)

        return record

    # =====================================================
    # Convert Value
    # =====================================================

    def _convert_value(
        self,
        value: Any,
        target_type: type,
    ):

        if value is None:
            return None

        try:

            if target_type is float:
                return float(value)

            if target_type is int:
                return int(float(value))

            if target_type is str:
                return str(value)

            return value

        except Exception:

            return value
