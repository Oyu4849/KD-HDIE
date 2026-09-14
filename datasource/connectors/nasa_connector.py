"""
KD-HDIE Framework

NASA POWER Connector

Purpose
-------
Connector implementation for NASA POWER
climate data service.

API
---
https://power.larc.nasa.gov/

Dissertation
------------
Chapter 3
NASA POWER Connector

Author:
Oybek Xolmuminov
"""

from __future__ import annotations

from typing import Any

from datasource.connectors.api_connector import (
    APIConfig,
    APIConnector,
)


class NASAConnector(APIConnector):
    """
    NASA POWER API Connector.
    """

    name = "NASA POWER Connector"

    source_type = "NASA"

    version = "1.0"

    def __init__(self):

        super().__init__(

            APIConfig(

                base_url="https://power.larc.nasa.gov",

                timeout=60,

            )

        )

    # =====================================================
    # Request Builder
    # =====================================================

    def build_request(

        self,

        latitude: float,

        longitude: float,

        start: str,

        end: str,

        parameters: list[str],

        community: str = "AG",

        temporal: str = "MONTHLY",

        format: str = "JSON",

    ) -> tuple[str, dict]:

        endpoint = "/api/temporal/monthly/point"

        params = {

            "parameters": ",".join(parameters),

            "community": community,

            "longitude": longitude,

            "latitude": latitude,

            "start": start,

            "end": end,

            "format": format,

        }

        return endpoint, params

    # =====================================================
    # Read Climate Data
    # =====================================================

    def read(

        self,

        latitude: float,
        longitude: float,
        start: str,
        end: str,
        parameters: list[str],
        temporal: str = "MONTHLY",

    ):
        """Read NASA POWER data at monthly or daily resolution."""

        temporal = str(temporal).upper().strip()

        if temporal == "DAILY":
            endpoint = "/api/temporal/daily/point"
            params = {
                "parameters": ",".join(parameters),
                "community": "AG",
                "longitude": longitude,
                "latitude": latitude,
                "start": start,
                "end": end,
                "format": "JSON",
            }
        else:
            endpoint, params = self.build_request(
                latitude=latitude,
                longitude=longitude,
                start=start,
                end=end,
                parameters=parameters,
            )

        return super().read(
            endpoint=endpoint,
            params=params,
        )

    # =====================================================
    # Convenience API
    # =====================================================

    def monthly_climate(

        self,

        latitude: float,

        longitude: float,

        start: str,

        end: str,

    ):

        return self.read(

            latitude=latitude,

            longitude=longitude,

            start=start,

            end=end,

            parameters=[

                "T2M",

                "PRECTOTCORR",

                "RH2M",

                "WS2M",

            ],

        )

    # -----------------------------------------------------
    # Daily Climate
    # -----------------------------------------------------

    def daily_climate(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ):
        """Return daily NASA POWER meteorological observations."""

        return self.read(
            latitude=latitude,
            longitude=longitude,
            start=start_date.replace("-", ""),
            end=end_date.replace("-", ""),
            parameters=[
                "T2M",
                "PRECTOTCORR",
                "RH2M",
                "WS2M",
            ],
            temporal="DAILY",
        )

    # -----------------------------------------------------

    def solar_radiation(

        self,

        latitude,

        longitude,

        start,

        end,

    ):

        return self.read(

            latitude=latitude,

            longitude=longitude,

            start=start,

            end=end,

            parameters=[

                "ALLSKY_SFC_SW_DWN"

            ],

        )

    # -----------------------------------------------------

    def metadata(self):

        meta = super().metadata()

        meta.update(

            {

                "provider": "NASA POWER",

                "temporal":

                    "DAILY_OR_MONTHLY",

                "community":

                    "AG",

            }

        )

        return meta
