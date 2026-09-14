"""
KD-HDIE Framework

Open-Meteo Response Normalizer (Final v1.0)
"""

from __future__ import annotations

from typing import Any

from core.interoperability.normalizers.base import (
    BaseResponseNormalizer,
)


class OpenMeteoResponseNormalizer(
    BaseResponseNormalizer
):
    """
    Normalize Open-Meteo API responses.

    Supported response sections:
        - current
        - hourly
        - daily
        - records
    """

    source_type = "OPENMETEO"

    # =====================================================
    # Normalize
    # =====================================================

    def normalize(
        self,
        data: Any,
    ) -> list[dict[str, Any]]:

        if not isinstance(data, dict):
            raise ValueError(
                "Open-Meteo response must be a JSON object."
            )

        records: list[dict[str, Any]] = []

        # -------------------------------------------------
        # Current weather
        # -------------------------------------------------

        if isinstance(data.get("current"), dict):

            records.extend(
                self._normalize_current(data)
            )

        # -------------------------------------------------
        # Hourly weather
        # -------------------------------------------------

        if isinstance(data.get("hourly"), dict):

            records.extend(
                self._normalize_tabular_section(
                    data["hourly"]
                )
            )

        # -------------------------------------------------
        # Daily weather
        # -------------------------------------------------

        if isinstance(data.get("daily"), dict):

            records.extend(
                self._normalize_tabular_section(
                    data["daily"]
                )
            )

        # -------------------------------------------------
        # Already normalized records
        # -------------------------------------------------

        if not records:

            if isinstance(
                data.get("records"),
                list,
            ):

                records = [
                    row
                    for row in data["records"]
                    if isinstance(row, dict)
                ]

        if not records:

            raise ValueError(
                "Open-Meteo response does not contain "
                "current, hourly, daily, or records data."
            )

        return records

    # =====================================================
    # Current Weather
    # =====================================================

    @staticmethod
    def _normalize_current(
        data: dict[str, Any],
    ) -> list[dict[str, Any]]:

        current = data["current"]

        record: dict[str, Any] = {}

        if current.get("time") is not None:

            record["time"] = current["time"]

        for key, value in current.items():

            if key == "time":
                continue

            record[key] = value

        # -------------------------------------------------
        # Legacy current_weather support
        # -------------------------------------------------

        legacy = data.get(
            "current_weather"
        )

        if isinstance(
            legacy,
            dict,
        ):

            if "time" not in record:

                if legacy.get("time") is not None:

                    record["time"] = (
                        legacy["time"]
                    )

            for key, value in legacy.items():

                if key != "time":

                    record.setdefault(
                        key,
                        value,
                    )

        return [record]

    # =====================================================
    # Hourly / Daily
    # =====================================================

    @staticmethod
    def _normalize_tabular_section(
        section: dict[str, Any],
    ) -> list[dict[str, Any]]:

        if not section:
            return []

        time_values = section.get("time")

        if not isinstance(
            time_values,
            list,
        ):
            return []

        variable_names = [
            key
            for key in section.keys()
            if key != "time"
            and isinstance(
                section[key],
                list,
            )
        ]

        records = []

        for index, timestamp in enumerate(
            time_values
        ):

            record = {
                "time": timestamp,
            }

            for variable in variable_names:

                values = section[variable]

                if index < len(values):

                    record[variable] = (
                        values[index]
                    )

                else:

                    record[variable] = None

            records.append(record)

        return records
