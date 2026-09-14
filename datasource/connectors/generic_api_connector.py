"""
KD-HDIE Framework

Generic REST API Connector
Version: 1.0

Runtime-configurable connector for generic REST/JSON APIs.
"""

from __future__ import annotations

from typing import Any
import time

import requests

from datasource.connectors.api_connector import (
    APIConfig,
    APIConnector,
)
from datasource.connectors.base_connector import ConnectorResult


class GenericAPIConnector(APIConnector):
    """
    Generic runtime-configurable REST/JSON API connector.

    The endpoint, HTTP method, parameters and headers can be
    supplied at runtime. Source-specific connectors such as
    OpenMeteoConnector and NASAConnector remain unchanged.
    """

    name = "Generic REST API Connector"
    source_type = "GENERIC_API"
    version = "1.0"

    def __init__(
        self,
        base_url: str = "",
        timeout: int = 30,
        api_key: str | None = None,
        verify_ssl: bool = True,
        headers: dict[str, str] | None = None,
        default_params: dict[str, Any] | None = None,
    ):
        super().__init__(
            APIConfig(
                base_url=base_url,
                timeout=timeout,
                api_key=api_key,
                verify_ssl=verify_ssl,
                headers=headers or {},
                default_params=default_params or {},
            )
        )

    def build_request(
        self,
        url: str | None = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any]]:
        endpoint = url or self.config.base_url

        request_params = dict(
            self.config.default_params or {}
        )
        request_params.update(params or {})

        return endpoint, request_params

    def configure(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        default_params: dict[str, Any] | None = None,
        timeout: int | None = None,
        verify_ssl: bool | None = None,
    ) -> None:
        self.config.base_url = url

        if headers is not None:
            self.config.headers = dict(headers)
            self.session.headers.clear()
            self.session.headers.update(headers)

        if default_params is not None:
            self.config.default_params = dict(
                default_params
            )

        if timeout is not None:
            self.config.timeout = timeout

        if verify_ssl is not None:
            self.config.verify_ssl = verify_ssl

    def read(
        self,
        url: str | None = None,
        params: dict[str, Any] | None = None,
        method: str = "GET",
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> ConnectorResult:
        """
        Execute a generic REST request and return ConnectorResult.
        """

        started = time.perf_counter()
        method = method.upper().strip()

        if method not in {"GET", "POST"}:
            return ConnectorResult(
                success=False,
                message=(
                    f"Unsupported HTTP method: {method}. "
                    "Supported methods: GET, POST."
                ),
            )

        endpoint, request_params = self.build_request(
            url=url,
            params=params,
        )

        if not endpoint:
            return ConnectorResult(
                success=False,
                message="API URL is required.",
            )

        if not self.is_connected():
            self.connect()

        request_headers = dict(headers or {})

        try:
            if method == "GET":
                response = self.session.get(
                    url=endpoint,
                    params=request_params,
                    headers=request_headers or None,
                    timeout=self.config.timeout,
                    verify=self.config.verify_ssl,
                )
            else:
                response = self.session.post(
                    url=endpoint,
                    params=request_params,
                    json=json,
                    headers=request_headers or None,
                    timeout=self.config.timeout,
                    verify=self.config.verify_ssl,
                )

            response.raise_for_status()

            try:
                data = response.json()
            except ValueError:
                data = response.text

            elapsed = time.perf_counter() - started

            return ConnectorResult(
                success=True,
                data=data,
                execution_time=round(elapsed, 6),
                metadata={
                    "status_code": response.status_code,
                    "method": method,
                    "url": response.url,
                    "content_type": response.headers.get(
                        "Content-Type"
                    ),
                },
            )

        except requests.RequestException as ex:
            elapsed = time.perf_counter() - started

            return ConnectorResult(
                success=False,
                message=str(ex),
                execution_time=round(elapsed, 6),
                metadata={
                    "method": method,
                    "url": endpoint,
                },
            )

    def metadata(self) -> dict[str, Any]:
        meta = super().metadata()

        meta.update(
            {
                "provider": "Generic REST API",
                "runtime_configurable": True,
                "supported_methods": ["GET", "POST"],
                "json_response": True,
            }
        )

        return meta
