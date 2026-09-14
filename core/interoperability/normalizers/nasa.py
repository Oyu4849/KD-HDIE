"""
KD-HDIE Framework

NASA POWER Response Normalizer (Final v1.0)
"""

from __future__ import annotations

from typing import Any

from core.interoperability.normalizers.base import (
    BaseResponseNormalizer,
)


class NASAResponseNormalizer(
    BaseResponseNormalizer
):
    """
    Normalize NASA POWER API responses.

    Supports NASA POWER parameterized
    temporal responses, including monthly data.
    """

    source_type = "NASA"

    # =====================================================
    # Normalize
    # =====================================================

    def normalize(
        self,
        data: Any,
    ) -> list[dict[str, Any]]:

        if not isinstance(
            data,
            dict,
        ):
            raise ValueError(
                "NASA POWER response must be a JSON object."
            )

        # -------------------------------------------------
        # Already normalized records
        # -------------------------------------------------

        if isinstance(
            data.get("records"),
            list,
        ):

            return [
                row
                for row in data["records"]
                if isinstance(
                    row,
                    dict,
                )
            ]

        # -------------------------------------------------
        # NASA POWER parameter structure
        # -------------------------------------------------

        properties = data.get(
            "properties"
        )

        if not isinstance(
            properties,
            dict,
        ):
            raise ValueError(
                "NASA POWER response does not contain "
                "'properties'."
            )

        parameters = properties.get(
            "parameter"
        )

        if not isinstance(
            parameters,
            dict,
        ):
            raise ValueError(
                "NASA POWER response does not contain "
                "'properties.parameter'."
            )

        return self._normalize_parameters(
            parameters
        )

    # =====================================================
    # Parameters
    # =====================================================

    @staticmethod
    def _normalize_parameters(
        parameters: dict[str, Any],
    ) -> list[dict[str, Any]]:

        dates = set()

        # -------------------------------------------------
        # Collect dates
        # -------------------------------------------------

        for values in parameters.values():

            if not isinstance(
                values,
                dict,
            ):
                continue

            dates.update(
                values.keys()
            )

        records = []

        # -------------------------------------------------
        # Build one record per date
        # -------------------------------------------------

        for date in sorted(dates):

            record: dict[str, Any] = {
                "DATE": date,
            }

            for (
                parameter_name,
                values,
            ) in parameters.items():

                if not isinstance(
                    values,
                    dict,
                ):
                    continue

                record[
                    parameter_name
                ] = values.get(date)

            records.append(
                record
            )

        return records
