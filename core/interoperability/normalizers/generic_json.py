"""
KD-HDIE Framework

Generic JSON Response Normalizer
Version: 1.3

Purpose
-------
Normalize heterogeneous REST/JSON API responses into a common
list[dict] record structure.

Supported structures
--------------------
- list of objects
- records / results / items
- data containers
- daily / hourly / monthly / weekly time-series
- NASA POWER-style parameter/date dictionaries
- nested NASA POWER structures such as:
      properties.parameter
      data.parameter
      result.parameter
- single JSON records

The normalizer is intentionally generic. It does not contain
source-specific semantic mappings; those are handled later by
the KD-HDIE semantic interoperability pipeline.
"""

from __future__ import annotations

from typing import Any

from core.interoperability.normalizers.base import (
    BaseResponseNormalizer,
)


class GenericJSONResponseNormalizer(BaseResponseNormalizer):

    source_type = "GENERIC_API"
    version = "1.3"

    # =====================================================
    # Main normalization entry point
    # =====================================================

    def normalize(
        self,
        data: Any,
    ) -> list[dict[str, Any]]:

        if isinstance(data, list):

            records = self._normalize_list(data)

            if records:
                return records

            raise ValueError(
                "Generic JSON list does not contain "
                "object records."
            )

        if not isinstance(data, dict):

            raise ValueError(
                "Generic API response must be a JSON "
                "object or list."
            )

        # -------------------------------------------------
        # 1. Standard record containers
        # -------------------------------------------------

        for key in (
            "records",
            "results",
            "items",
        ):

            value = data.get(key)

            if isinstance(value, list):

                records = self._normalize_list(value)

                if records:
                    return records

        # -------------------------------------------------
        # 2. Generic data container
        # -------------------------------------------------

        value = data.get("data")

        if isinstance(value, list):

            records = self._normalize_list(value)

            if records:
                return records

        if isinstance(value, dict):

            # First check for nested parameter structures.
            records = self._normalize_parameter_structure(
                value
            )

            if records:
                return records

            records = self._normalize_tabular_section(
                value
            )

            if records:
                return records

        # -------------------------------------------------
        # 3. NASA POWER-style parameter structure
        #
        # Supports:
        #     {"parameter": {...}}
        #
        # and nested structures such as:
        #     {"properties": {"parameter": {...}}}
        #
        #     {"data": {"parameter": {...}}}
        # -------------------------------------------------

        records = self._normalize_parameter_structure(
            data
        )

        if records:
            return records

        # -------------------------------------------------
        # 4. Time-series containers
        # -------------------------------------------------

        for key in (
            "daily",
            "hourly",
            "monthly",
            "weekly",
        ):

            section = data.get(key)

            if isinstance(section, dict):

                records = self._normalize_parameter_structure(
                    section
                )

                if records:
                    return records

                records = self._normalize_tabular_section(
                    section
                )

                if records:
                    return records

        # -------------------------------------------------
        # 5. Generic nested parameter search
        #
        # This is intentionally performed before treating
        # the root object as a single record. It prevents
        # NASA POWER metadata such as latitude/longitude
        # from hiding the actual parameter data.
        # -------------------------------------------------

        records = self._find_parameter_structure(
            data
        )

        if records:
            return records

        # -------------------------------------------------
        # 6. Root-level tabular object
        # -------------------------------------------------

        records = self._normalize_tabular_section(
            data
        )

        if records:
            return records

        # -------------------------------------------------
        # 7. Single record
        # -------------------------------------------------

        if self._looks_like_record(data):

            return [dict(data)]

        raise ValueError(
            "Generic JSON response does not contain "
            "a recognizable record structure."
        )

    # =====================================================
    # List normalization
    # =====================================================

    @staticmethod
    def _normalize_list(
        value: list[Any],
    ) -> list[dict[str, Any]]:

        return [
            dict(item)
            for item in value
            if isinstance(item, dict)
        ]

    # =====================================================
    # NASA POWER parameter/date normalization
    # =====================================================

    @classmethod
    def _normalize_parameter_structure(
        cls,
        data: dict[str, Any],
    ) -> list[dict[str, Any]]:

        parameter = data.get("parameter")

        if not isinstance(parameter, dict):

            return []

        return cls._parameter_dict_to_records(
            parameter
        )

    # =====================================================
    # Recursive search for nested "parameter"
    # =====================================================

    @classmethod
    def _find_parameter_structure(
        cls,
        data: Any,
        depth: int = 0,
        max_depth: int = 8,
    ) -> list[dict[str, Any]]:

        if depth > max_depth:
            return []

        if not isinstance(data, dict):
            return []

        # Prefer an explicit parameter key at the current level.
        parameter = data.get("parameter")

        if isinstance(parameter, dict):

            records = cls._parameter_dict_to_records(
                parameter
            )

            if records:
                return records

        # Search nested dictionaries.
        for value in data.values():

            if isinstance(value, dict):

                records = cls._find_parameter_structure(
                    value,
                    depth=depth + 1,
                    max_depth=max_depth,
                )

                if records:
                    return records

        # Search nested lists containing dictionaries.
        for value in data.values():

            if isinstance(value, list):

                for item in value:

                    if isinstance(item, dict):

                        records = cls._find_parameter_structure(
                            item,
                            depth=depth + 1,
                            max_depth=max_depth,
                        )

                        if records:
                            return records

        return []

    # =====================================================
    # Convert parameter maps into records
    #
    # Example:
    #
    # parameter = {
    #     "T2M": {
    #         "20250101": 12.3,
    #         "20250102": 13.1
    #     },
    #     "PRECTOTCORR": {
    #         "20250101": 0.2,
    #         "20250102": 1.4
    #     }
    # }
    #
    # becomes:
    #
    # [
    #     {
    #         "date": "20250101",
    #         "T2M": 12.3,
    #         "PRECTOTCORR": 0.2
    #     },
    #     ...
    # ]
    # =====================================================

    @classmethod
    def _parameter_dict_to_records(
        cls,
        parameter: dict[str, Any],
    ) -> list[dict[str, Any]]:

        parameter_maps = {
            key: value
            for key, value in parameter.items()
            if isinstance(value, dict)
        }

        if not parameter_maps:
            return []

        # Collect all date keys across all parameters.
        dates: set[str] = set()

        for values in parameter_maps.values():

            for key in values.keys():

                if cls._looks_like_date_key(key):

                    dates.add(str(key))

        if not dates:
            return []

        records: list[dict[str, Any]] = []

        for date_key in sorted(dates):

            record: dict[str, Any] = {
                "date": date_key
            }

            for parameter_name, values in parameter_maps.items():

                record[parameter_name] = values.get(
                    date_key
                )

            records.append(record)

        return records

    # =====================================================
    # Date-key detection
    # =====================================================

    @staticmethod
    def _looks_like_date_key(
        value: Any,
    ) -> bool:

        text = str(value).strip()

        # NASA POWER daily date:
        # YYYYMMDD
        if (
            len(text) == 8
            and text.isdigit()
        ):

            try:

                number = int(text)

                if (
                    19000000
                    <= number
                    <= 29991231
                ):
                    return True

            except ValueError:

                return False

        # ISO date / datetime:
        # YYYY-MM-DD
        # YYYY-MM-DDTHH:MM:SS
        if (
            len(text) >= 10
            and text[4] == "-"
            and text[7] == "-"
        ):

            return True

        return False

    # =====================================================
    # Generic tabular object
    # =====================================================

    @staticmethod
    def _normalize_tabular_section(
        section: dict[str, Any],
    ) -> list[dict[str, Any]]:

        if not section:
            return []

        list_fields = {
            key: value
            for key, value in section.items()
            if isinstance(value, list)
        }

        if not list_fields:
            return []

        # Prefer temporal axis.
        axis_key = None

        for candidate in (
            "time",
            "date",
            "datetime",
            "timestamp",
            "date_time",
        ):

            if candidate in list_fields:

                axis_key = candidate

                break

        if axis_key is None:

            axis_key = next(
                iter(list_fields)
            )

        axis = list_fields[axis_key]

        records: list[dict[str, Any]] = []

        for index in range(len(axis)):

            record: dict[str, Any] = {}

            for key, values in list_fields.items():

                record[key] = (
                    values[index]
                    if index < len(values)
                    else None
                )

            records.append(record)

        return records

    # =====================================================
    # Single-record detection
    # =====================================================

    @staticmethod
    def _looks_like_record(
        data: dict[str, Any],
    ) -> bool:

        if not data:
            return False

        scalar_count = sum(
            1
            for value in data.values()
            if not isinstance(
                value,
                (dict, list),
            )
        )

        return scalar_count > 0

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(
        self,
    ) -> dict[str, Any]:

        meta = super().metadata()

        meta.update(
            {
                "response_type": "JSON",
                "runtime_configurable": True,
                "supported_structures": [
                    "list",
                    "records",
                    "results",
                    "items",
                    "data.list",
                    "data.object",
                    "parameter",
                    "nested.parameter",
                    "properties.parameter",
                    "daily",
                    "hourly",
                    "monthly",
                    "weekly",
                    "tabular_object",
                    "single_record",
                ],
                "parameter_date_mapping": True,
                "recursive_parameter_detection": True,
            }
        )

        return meta
