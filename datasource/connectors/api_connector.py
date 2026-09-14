"""
KD-HDIE Framework

API Connector

Purpose
-------
Abstract REST API connector for heterogeneous
web services.

Supported APIs
--------------
- NASA POWER
- Open-Meteo
- OpenWeather
- Copernicus
- JRC
- USGS
- World Bank
- Any REST API

Dissertation
------------
Chapter 3
REST API Connector

Author:
Oybek Xolmuminov
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

import requests

from datasource.connectors.base_connector import (
    BaseConnector,
    ConnectorResult,
)


# ==========================================================
# Configuration
# ==========================================================

@dataclass
class APIConfig:
    """
    REST API configuration.
    """

    base_url: str

    timeout: int = 30

    api_key: str | None = None

    verify_ssl: bool = True

    headers: dict[str, str] = field(default_factory=dict)

    default_params: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# API Connector
# ==========================================================

class APIConnector(BaseConnector):
    """
    Base class for all REST API connectors.
    """

    name = "REST API Connector"

    source_type = "API"

    version = "1.0"

    def __init__(self, config: APIConfig):

        super().__init__()

        self.config = config

        self.session = requests.Session()

        self._connected = False

        if config.headers:
            self.session.headers.update(config.headers)

    # =====================================================
    # Connection
    # =====================================================

    def connect(self) -> bool:

        self._connected = True

        self.connection.connected = True

        self.connection.endpoint = self.config.base_url

        return True

    # -----------------------------------------------------

    def disconnect(self) -> None:

        self.session.close()

        self._connected = False

        self.connection.connected = False

    # -----------------------------------------------------

    def is_connected(self) -> bool:

        return self._connected

    # =====================================================
    # HTTP
    # =====================================================

    def get(
        self,
        endpoint: str = "",
        params: dict | None = None,
    ) -> requests.Response:

        merged = dict(
            self.config.default_params
        )

        if params:
            merged.update(params)

        # --------------------------------------------------
        # Support both relative and absolute endpoints.
        # --------------------------------------------------

        if endpoint.startswith("http://") or endpoint.startswith(
            "https://"
        ):

            url = endpoint

        else:

            url = (
                self.config.base_url.rstrip("/")
                + "/"
                + endpoint.lstrip("/")
            )

        return self.session.get(

            url=url,

            params=merged,

            timeout=self.config.timeout,

            verify=self.config.verify_ssl,

        )
    # -----------------------------------------------------

    def post(
        self,
        endpoint: str = "",
        json: dict | None = None,
    ) -> requests.Response:

        return self.session.post(

            url=self.config.base_url + endpoint,

            json=json,

            timeout=self.config.timeout,

            verify=self.config.verify_ssl,

        )

    # =====================================================
    # Read
    # =====================================================

    def read(
        self,
        endpoint: str = "",
        params: dict | None = None,
    ) -> ConnectorResult:

        started = perf_counter()

        if not self.is_connected():

            self.connect()

        response = self.get(

            endpoint=endpoint,

            params=params,

        )

        response.raise_for_status()

        elapsed = perf_counter() - started

        return ConnectorResult(

            success=True,

            data=response.json(),

            execution_time=round(elapsed, 6),

            metadata={

                "status_code": response.status_code,

                "endpoint": endpoint,

                "url": response.url,

            }

        )

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(self) -> dict:

        return {

            "connector": self.name,

            "source_type": self.source_type,

            "base_url": self.config.base_url,

            "timeout": self.config.timeout,

            "ssl": self.config.verify_ssl,

        }

    # =====================================================
    # Health
    # =====================================================

    def health(self) -> dict:

        report = super().health()

        report.update({

            "base_url": self.config.base_url,

            "timeout": self.config.timeout,

        })

        return report

    # =====================================================
    # API-specific implementation
    # =====================================================

    @abstractmethod
    def build_request(
        self,
        **kwargs,
    ) -> tuple[str, dict]:
        """
        Build endpoint and request parameters.

        Returns:
            (endpoint, parameters)
        """
        raise NotImplementedError
