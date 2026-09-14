"""
KD-HDIE Framework

Connector Manager

Purpose
-------
Central manager responsible for registration,
selection and execution of heterogeneous
data source connectors.

Dissertation
------------
Chapter 3
Heterogeneous Data Source Management

Author:
Oybek Xolmuminov
"""

from __future__ import annotations

from typing import Dict

from datasource.connectors.base_connector import (
    BaseConnector,
    ConnectorResult,
)


class ConnectorManager:
    """
    Central connector manager.
    """

    def __init__(self):

        self._connectors: Dict[str, BaseConnector] = {}

    # =====================================================
    # Registration
    # =====================================================

    def register(
        self,
        connector: BaseConnector,
    ) -> None:
        """
        Register connector.
        """

        key = connector.source_type.upper()

        self._connectors[key] = connector

    # -----------------------------------------------------

    def unregister(
        self,
        source_type: str,
    ) -> None:

        self._connectors.pop(
            source_type.upper(),
            None,
        )

    # =====================================================
    # Lookup
    # =====================================================

    def connector(
        self,
        source_type: str,
    ) -> BaseConnector:

        key = source_type.upper()

        if key not in self._connectors:

            raise ValueError(

                f"Connector '{source_type}' "

                f"is not registered."

            )

        return self._connectors[key]

    # =====================================================
    # Connection
    # =====================================================

    def connect(
        self,
        source_type: str,
    ) -> bool:

        connector = self.connector(
            source_type
        )

        return connector.connect()

    # -----------------------------------------------------

    def disconnect(
        self,
        source_type: str,
    ) -> None:

        connector = self.connector(
            source_type
        )

        connector.disconnect()

    # =====================================================
    # Read
    # =====================================================

    def read(
        self,
        source_type: str,
        **kwargs,
    ) -> ConnectorResult:

        connector = self.connector(
            source_type
        )

        if not connector.is_connected():

            connector.connect()

        return connector.read(
            **kwargs
        )

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(
        self,
        source_type: str,
    ) -> dict:

        connector = self.connector(
            source_type
        )

        return connector.metadata()

    # =====================================================
    # Health
    # =====================================================

    def health(self):

        report = {}

        for name, connector in self._connectors.items():

            report[name] = connector.health()

        return report

    # =====================================================
    # Utility
    # =====================================================

    def contains(
        self,
        source_type: str,
    ) -> bool:

        return (

            source_type.upper()

            in self._connectors

        )

    # -----------------------------------------------------

    def connectors(self):

        return list(

            self._connectors.keys()

        )

    # -----------------------------------------------------

    def count(self):

        return len(

            self._connectors

        )

    # -----------------------------------------------------

    def clear(self):

        self._connectors.clear()


# ==========================================================
# Global Manager
# ==========================================================

connector_manager = ConnectorManager()
