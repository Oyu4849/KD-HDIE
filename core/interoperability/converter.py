"""
KD-HDIE Framework

Interoperability Converter

Purpose:
Convert heterogeneous source records into
Unified Internal Data Model.

Author:
Oybek Xolmuminov
"""

from typing import Dict, List


class InteroperabilityConverter:
    """
    Converts heterogeneous records into a
    unified internal representation.
    """

    DEFAULT_MAPPING = {

        "T2M": "temperature",
        "temperature_2m": "temperature",
        "Temperature": "temperature",
        "temp": "temperature",

        "RH2M": "humidity",
        "relative_humidity_2m": "humidity",

        "WS2M": "wind_speed",
        "wind_speed_10m": "wind_speed"

    }

    DEFAULT_UNITS = {

        "temperature": "°C",

        "humidity": "%",

        "wind_speed": "m/s"

    }

    def convert(

        self,

        records: List[Dict]

    ) -> List[Dict]:

        unified = []

        for record in records:

            for key, value in record.items():

                attribute = self.DEFAULT_MAPPING.get(

                    key,

                    key.lower()

                )

                unified.append({

                    "attribute": attribute,

                    "value": value,

                    "unit": self.DEFAULT_UNITS.get(attribute),

                    "source_attribute": key

                })

        return unified
