"""
KD-HDIE Framework

Monthly Aggregation Algorithm
Final v2.1

Purpose
-------
Convert daily UnifiedRecord objects into monthly
UnifiedRecord objects while preserving the canonical
data model.

Aggregation rules
-----------------
temperature    -> mean
wind_speed     -> mean
precipitation  -> sum

Generic numeric attributes
-------------------------
Other numeric attributes are aggregated using mean.

Non-numeric attributes
----------------------
The first valid value is retained.

Position in workflow
--------------------
Harmonization
      ↓
MonthlyAggregation
      ↓
Quality
      ↓
Conflict
      ↓
Reliability
      ↓
Fusion
      ↓
UnifiedModel

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from numbers import Number
from typing import Any

from attributes.models import (
    UnifiedAttribute,
    UnifiedRecord,
)

from core.algorithms.base import (
    AlgorithmResult,
    BaseAlgorithm,
)


class MonthlyAggregationAlgorithm(BaseAlgorithm):
    """
    Aggregate daily UnifiedRecord objects into
    monthly UnifiedRecord objects.
    """

    name = "MonthlyAggregation"

    order = 55

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        data: list[UnifiedRecord],
        context,
    ) -> AlgorithmResult:

        if not data:

            return AlgorithmResult(

                success=True,

                data=[],

                message=(
                    "No records available for "
                    "monthly aggregation."
                ),

                metadata={
                    "input_records": 0,
                    "output_records": 0,
                    "aggregation_period": "monthly",
                },

            )

        try:

            monthly_records = (
                self._aggregate_monthly(data)
            )

            metadata = {

                "aggregation_period":
                    "monthly",

                "input_records":
                    len(data),

                "output_records":
                    len(monthly_records),

                "reduction_ratio":
                    (
                        len(monthly_records)
                        / len(data)
                    )
                    if data
                    else 0.0,

                "aggregation_rules": {

                    "temperature": "mean",

                    "precipitation": "sum",

                    "wind_speed": "mean",

                    "numeric_other": "mean",

                    "non_numeric": "first_valid",

                },

            }

            return AlgorithmResult(

                success=True,

                data=monthly_records,

                message=(
                    "Daily records successfully "
                    "aggregated to monthly records."
                ),

                metadata=metadata,

            )

        except Exception as exc:

            return AlgorithmResult(

                success=False,

                data=data,

                message=(
                    "Monthly aggregation failed."
                ),

                metadata={

                    "input_records": len(data),

                    "error": str(exc),

                },

            )

    # ======================================================
    # Main Aggregation
    # ======================================================

    def _aggregate_monthly(
        self,
        records: list[UnifiedRecord],
    ) -> list[UnifiedRecord]:

        groups: dict[
            tuple[int, int],
            list[UnifiedRecord],
        ] = defaultdict(list)

        # --------------------------------------------------
        # Group records by year and month
        # --------------------------------------------------

        for record in records:

            parsed = self._parse_timestamp(
                record.timestamp
            )

            if parsed is None:

                continue

            groups[
                (
                    parsed.year,
                    parsed.month,
                )
            ].append(record)

        monthly_records: list[
            UnifiedRecord
        ] = []

        # --------------------------------------------------
        # Aggregate each month
        # --------------------------------------------------

        for (
            year,
            month,
        ), month_records in sorted(
            groups.items()
        ):

            monthly_record = (
                self._build_monthly_record(
                    year=year,
                    month=month,
                    records=month_records,
                )
            )

            monthly_records.append(
                monthly_record
            )

        return monthly_records

    # ======================================================
    # Build Monthly Record
    # ======================================================

    def _build_monthly_record(
        self,
        year: int,
        month: int,
        records: list[UnifiedRecord],
    ) -> UnifiedRecord:

        attribute_groups: dict[
            str,
            list[UnifiedAttribute],
        ] = defaultdict(list)

        # --------------------------------------------------
        # Group attributes by canonical name
        # --------------------------------------------------

        for record in records:

            for attribute in record.attributes:

                canonical_name = (
                    attribute.canonical_name
                    or attribute.source_name
                )

                attribute_groups[
                    canonical_name
                ].append(attribute)

        monthly_attributes: list[
            UnifiedAttribute
        ] = []

        # --------------------------------------------------
        # Aggregate attributes
        # --------------------------------------------------

        for (
            canonical_name,
            attributes,
        ) in sorted(
            attribute_groups.items()
        ):

            aggregated_value = (
                self._aggregate_attribute(
                    canonical_name=canonical_name,
                    attributes=attributes,
                )
            )

            if aggregated_value is None:

                continue

            first = attributes[0]

            monthly_attribute = (
                UnifiedAttribute(

                    source_name=(
                        first.source_name
                    ),

                    canonical_name=(
                        canonical_name
                    ),

                    value=aggregated_value,

                    unit=first.unit,

                    domain=first.domain,

                    source_system=(
                        first.source_system
                    ),

                    metadata={

                        **first.metadata,

                        "aggregation":
                            self._aggregation_method(
                                canonical_name
                            ),

                        "aggregation_period":
                            "monthly",

                        "observations":
                            len(attributes),

                        "year":
                            year,

                        "month":
                            month,

                    },

                )
            )

            monthly_attributes.append(
                monthly_attribute
            )

        # --------------------------------------------------
        # Source system
        # --------------------------------------------------

        source_systems = {

            record.source_system

            for record in records

            if record.source_system

        }

        source_system = (

            next(iter(source_systems))
            if len(source_systems) == 1
            else ",".join(
                sorted(source_systems)
            )

        )

        return UnifiedRecord(

            timestamp=datetime(
                year,
                month,
                1,
            ),

            attributes=monthly_attributes,

            metadata={

                "aggregation":
                    "monthly",

                "year":
                    year,

                "month":
                    month,

                "input_records":
                    len(records),

                "source_system":
                    source_system,

            },

            source_system=source_system,

        )

    # ======================================================
    # Attribute Aggregation
    # ======================================================

    def _aggregate_attribute(
        self,
        canonical_name: str,
        attributes: list[UnifiedAttribute],
    ) -> Any:

        values = [

            attribute.value

            for attribute in attributes

            if attribute.value is not None

        ]

        if not values:

            return None

        method = (
            self._aggregation_method(
                canonical_name
            )
        )

        numeric_values = [

            float(value)

            for value in values

            if isinstance(
                value,
                Number,
            )
            and not isinstance(
                value,
                bool,
            )

        ]

        # --------------------------------------------------
        # Precipitation -> SUM
        # --------------------------------------------------

        if method == "sum":

            if not numeric_values:

                return None

            return sum(
                numeric_values
            )

        # --------------------------------------------------
        # Mean
        # --------------------------------------------------

        if method == "mean":

            if not numeric_values:

                return None

            return (
                sum(numeric_values)
                / len(numeric_values)
            )

        # --------------------------------------------------
        # Non-numeric -> first valid
        # --------------------------------------------------

        return values[0]

    # ======================================================
    # Aggregation Method
    # ======================================================

    @staticmethod
    def _aggregation_method(
        canonical_name: str,
    ) -> str:

        name = (
            canonical_name
            .strip()
            .lower()
        )

        if name == "precipitation":

            return "sum"

        if name in {

            "temperature",

            "wind_speed",

        }:

            return "mean"

        return "mean"

    # ======================================================
    # Timestamp Parser
    # ======================================================

    @staticmethod
    def _parse_timestamp(
        value: Any,
    ) -> datetime | None:

        if value is None:
            return None

        # --------------------------------------------------
        # datetime
        # --------------------------------------------------

        if isinstance(
            value,
            datetime,
        ):
            return value

        # --------------------------------------------------
        # date
        # --------------------------------------------------

        if isinstance(
            value,
            date,
        ):

            return datetime(
                value.year,
                value.month,
                value.day,
            )

        # --------------------------------------------------
        # String formats
        # --------------------------------------------------

        if isinstance(
            value,
            str,
        ):

            text = value.strip()

            if not text:
                return None

            # ==============================================
            # NASA POWER monthly format
            #
            # Example:
            #   202501
            #   202502
            #   ...
            # ==============================================

            if (
                len(text) == 6
                and text.isdigit()
            ):

                try:

                    year = int(
                        text[:4]
                    )

                    month = int(
                        text[4:6]
                    )

                    if 1 <= month <= 12:

                        return datetime(
                            year,
                            month,
                            1,
                        )

                except ValueError:

                    return None

            # ==============================================
            # YYYYMMDD format
            #
            # Example:
            #   20250101
            # ==============================================

            if (
                len(text) == 8
                and text.isdigit()
            ):

                try:

                    return datetime(

                        int(text[:4]),

                        int(text[4:6]),

                        int(text[6:8]),

                    )

                except ValueError:

                    return None

            # ==============================================
            # ISO timestamp
            #
            # Example:
            #   2025-01-01T00:00:00
            # ==============================================

            try:

                return datetime.fromisoformat(

                    text.replace(
                        "Z",
                        "+00:00",
                    )

                )

            except ValueError:

                pass

            # ==============================================
            # ISO date
            #
            # Example:
            #   2025-01-01
            # ==============================================

            try:

                parsed_date = date.fromisoformat(
                    text
                )

                return datetime(

                    parsed_date.year,

                    parsed_date.month,

                    parsed_date.day,

                )

            except ValueError:

                return None

        return None
