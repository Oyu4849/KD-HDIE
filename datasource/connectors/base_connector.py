"""
KD-HDIE Framework

Base Connector

Purpose
-------
Abstract base connector for all heterogeneous
data sources.

Every connector in the framework must inherit
from this class.

Dissertation
------------
Chapter 3
Heterogeneous Data Source Connectors

Author:
Oybek Xolmuminov
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ==========================================================
# Connection Information
# ==========================================================

@dataclass
class ConnectionInfo:
    """
    Connection metadata.
    """

    name: str

    source_type: str

    connected: bool = False

    endpoint: str | None = None

    version: str | None = None

    last_connected: datetime | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Connector Result
# ==========================================================

@dataclass
class ConnectorResult:
    """
    Standard connector response.
    """

    success: bool

    data: Any = None

    message: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)

    execution_time: float = 0.0


# ==========================================================
# Base Connector
# ==========================================================

class BaseConnector(ABC):
    """
    Abstract connector for heterogeneous data sources.
    """

    name = "Base Connector"

    source_type = "UNKNOWN"

    version = "1.0"

    def __init__(self):

        self.connection = ConnectionInfo(

            name=self.name,

            source_type=self.source_type,

        )

    # =====================================================
    # Connection
    # =====================================================

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the data source.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close connection.
        """
        raise NotImplementedError

    @abstractmethod
    def is_connected(self) -> bool:
        """
        Return current connection state.
        """
        raise NotImplementedError

    # =====================================================
    # Data Operations
    # =====================================================

    @abstractmethod
    def read(
        self,
        **kwargs,
    ) -> ConnectorResult:
        """
        Read data from the source.
        """
        raise NotImplementedError

    def write(
        self,
        data: Any,
        **kwargs,
    ) -> ConnectorResult:
        """
        Optional write operation.
        """

        return ConnectorResult(

            success=False,

            message=(
                f"{self.name} does not support "
                "write operation."
            ),

        )

    # =====================================================
    # Metadata
    # =====================================================

    @abstractmethod
    def metadata(self) -> dict:
        """
        Return source metadata.
        """
        raise NotImplementedError

    # =====================================================
    # Health
    # =====================================================

    def health(self) -> dict:

        return {

            "connector": self.name,

            "source_type": self.source_type,

            "connected": self.is_connected(),

            "version": self.version,

        }

    # =====================================================
    # Utility
    # =====================================================

    def info(self) -> ConnectionInfo:

        return self.connection

    def __str__(self):

        return (

            f"{self.name}"

            f" ({self.source_type})"

        )
