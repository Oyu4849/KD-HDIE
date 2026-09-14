"""
KD-HDIE Framework

Open-Meteo Connector

Version
-------
2.0

Purpose
-------
Connector implementation for Open-Meteo Weather API.

Supported modes
---------------
1. Current weather
2. Forecast hourly/daily
3. Historical weather
4. Historical daily data for monthly aggregation

API
---
https://open-meteo.com/

Historical API
--------------
https://archive-api.open-meteo.com/v1/archive

Dissertation
------------
Chapter 3
Open-Meteo Connector

Author:
Oybek Xolmuminov
"""

from __future__ import annotations

from datasource.connectors.api_connector import (
    APIConfig,
    APIConnector,
)


class OpenMeteoConnector(APIConnector):
    """
    Open-Meteo API Connector.

    Supports both forecast and historical
    weather data.
    """

    name = "Open-Meteo Connector"

    source_type = "OPENMETEO"

    version = "2.0"

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        # Default endpoint for current/forecast data.
        super().__init__(

            APIConfig(

                base_url=(
                    "https://api.open-meteo.com"
                ),

                timeout=30,

            )

        )

    # =====================================================
    # Forecast Request Builder
    # =====================================================

    def build_request(

        self,

        latitude: float,

        longitude: float,

        hourly: list[str] | None = None,

        daily: list[str] | None = None,

        current: list[str] | None = None,

        timezone: str = "auto",

    ) -> tuple[str, dict]:

        endpoint = "/v1/forecast"

        params = {

            "latitude": latitude,

            "longitude": longitude,

            "timezone": timezone,

        }

        if hourly:

            params["hourly"] = ",".join(hourly)

        if daily:

            params["daily"] = ",".join(daily)

        if current:

            params["current"] = ",".join(current)

        return endpoint, params

    # =====================================================
    # Historical Request Builder
    # =====================================================

    def build_historical_request(

        self,

        latitude: float,

        longitude: float,

        start_date: str,

        end_date: str,

        hourly: list[str] | None = None,

        daily: list[str] | None = None,

        timezone: str = "auto",

    ) -> tuple[str, dict]:

        endpoint = (
            "https://archive-api.open-meteo.com"
            "/v1/archive"
        )

        params = {

            "latitude": latitude,

            "longitude": longitude,

            "start_date": start_date,

            "end_date": end_date,

            "timezone": timezone,

        }

        if hourly:

            params["hourly"] = ",".join(
                hourly
            )

        if daily:

            params["daily"] = ",".join(
                daily
            )

        return endpoint, params

    # =====================================================
    # Forecast Read
    # =====================================================

    def read(

        self,

        latitude: float,

        longitude: float,

        hourly: list[str] | None = None,

        daily: list[str] | None = None,

        current: list[str] | None = None,

        start_date: str | None = None,

        end_date: str | None = None,

        historical: bool = False,

    ):
        """
        Read Open-Meteo data.

        If historical=True or start/end dates are supplied,
        the historical archive endpoint is used.
        """

        # ==================================================
        # Historical
        # ==================================================

        if historical or (
            start_date is not None
            and end_date is not None
        ):

            if not start_date or not end_date:

                raise ValueError(
                    "start_date and end_date "
                    "are required for historical data."
                )

            return self.historical_daily_weather(

                latitude=latitude,

                longitude=longitude,

                start_date=start_date,

                end_date=end_date,

            )

        # ==================================================
        # Forecast / Current
        # ==================================================

        endpoint, params = self.build_request(

            latitude=latitude,

            longitude=longitude,

            hourly=hourly,

            daily=daily,

            current=current,

        )

        return super().read(

            endpoint=endpoint,

            params=params,

        )
    # =====================================================
    # Historical Read
    # =====================================================

    def historical_weather(

        self,

        latitude: float,

        longitude: float,

        start_date: str,

        end_date: str,

        hourly: list[str] | None = None,

        daily: list[str] | None = None,

        timezone: str = "auto",

    ):

        endpoint, params = (
            self.build_historical_request(

                latitude=latitude,

                longitude=longitude,

                start_date=start_date,

                end_date=end_date,

                hourly=hourly,

                daily=daily,

                timezone=timezone,

            )
        )

        # -------------------------------------------------
        # Historical endpoint is absolute, therefore we
        # call APIConnector with its full endpoint.
        # -------------------------------------------------

        return super().read(

            endpoint=endpoint,

            params=params,

        )

    # =====================================================
    # Current Weather
    # =====================================================

    def current_weather(

        self,

        latitude: float,

        longitude: float,

    ):

        return self.read(

            latitude=latitude,

            longitude=longitude,

            current=[

                "temperature_2m",

                "relative_humidity_2m",

                "wind_speed_10m",

                "precipitation",

            ],

        )

    # =====================================================
    # Hourly Weather
    # =====================================================

    def hourly_weather(

        self,

        latitude: float,

        longitude: float,

    ):

        return self.read(

            latitude=latitude,

            longitude=longitude,

            hourly=[

                "temperature_2m",

                "relative_humidity_2m",

                "precipitation",

                "soil_moisture_0_to_1cm",

                "wind_speed_10m",

            ],

        )

    # =====================================================
    # Daily Forecast
    # =====================================================

    def daily_weather(

        self,

        latitude: float,

        longitude: float,

    ):

        return self.read(

            latitude=latitude,

            longitude=longitude,

            daily=[

                "temperature_2m_max",

                "temperature_2m_min",

                "temperature_2m_mean",

                "precipitation_sum",

                "wind_speed_10m_max",

                "wind_speed_10m_mean",

            ],

        )

    # =====================================================
    # Historical Daily Weather
    # =====================================================

    def historical_daily_weather(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ):

        endpoint = (
            "https://archive-api.open-meteo.com"
            "/v1/archive"
        )

        params = {

            "latitude": latitude,

            "longitude": longitude,

            "start_date": start_date,

            "end_date": end_date,

            "daily": ",".join([

                "temperature_2m_mean",

                "precipitation_sum",

                "wind_speed_10m_mean",

            ]),

            "timezone": "auto",

        }

        return super().read(

            endpoint=endpoint,

            params=params,

        )
    # =====================================================
    # Metadata
    # =====================================================

    def metadata(self):

        meta = super().metadata()

        meta.update(

            {

                "provider":
                    "Open-Meteo",

                "api_version":
                    "v1",

                "forecast":
                    True,

                "historical":
                    True,

                "current_weather":
                    True,

                "hourly":
                    True,

                "daily":
                    True,

                "historical_daily":
                    True,

                "historical_endpoint":
                    "/v1/archive",

            }

        )

        return meta
