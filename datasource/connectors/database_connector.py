"""
KD-HDIE Framework

Database Connector

Purpose
-------
Abstract SQL database connector for heterogeneous
database management systems.

Supported Databases
-------------------
- PostgreSQL
- MySQL
- MariaDB
- SQLite
- Oracle
- Microsoft SQL Server

Dissertation
------------
Chapter 3
Database Connector

Author:
Oybek Xolmuminov
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from time import perf_counter
from typing import Any

from datasource.connectors.base_connector import (
    BaseConnector,
    ConnectorResult,
)


# ==========================================================
# Configuration
# ==========================================================

@dataclass
class DatabaseConfig:

    engine: str

    host: str

    port: int

    database: str

    username: str

    password: str

    options: dict[str, Any] | None = None


# ==========================================================
# Connector
# ==========================================================

class DatabaseConnector(BaseConnector):
    """
    Base connector for SQL databases.
    """

    name = "Database Connector"

    source_type = "DATABASE"

    version = "1.0"

    def __init__(
        self,
        config: DatabaseConfig,
    ):

        super().__init__()

        self.config = config

        self.connection_object = None

        self._connected = False

    # =====================================================
    # Connection
    # =====================================================

    @abstractmethod
    def connect(self) -> bool:
        """
        Create database connection.
        """
        raise NotImplementedError

    # -----------------------------------------------------

    def disconnect(self):

        if self.connection_object:

            self.connection_object.close()

        self.connection_object = None

        self._connected = False

        self.connection.connected = False

    # -----------------------------------------------------

    def is_connected(self):

        return self._connected

    # =====================================================
    # Query
    # =====================================================

    @abstractmethod
    def execute(
        self,
        sql: str,
        parameters: tuple | None = None,
    ):
        """
        Execute SQL query.
        """
        raise NotImplementedError

    # =====================================================
    # Read
    # =====================================================

    def read(
        self,
        query: str,
        parameters: tuple | None = None,
    ) -> ConnectorResult:

        started = perf_counter()

        if not self.is_connected():

            self.connect()

        rows = self.execute(

            sql=query,

            parameters=parameters,

        )

        elapsed = perf_counter() - started

        return ConnectorResult(

            success=True,

            data=rows,

            execution_time=round(elapsed, 6),

            metadata={

                "database": self.config.database,

                "engine": self.config.engine,

                "rows": len(rows)

                if hasattr(rows, "__len__")

                else None,

            }

        )

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(self):

        return {

            "connector": self.name,

            "source_type": self.source_type,

            "database": self.config.database,

            "engine": self.config.engine,

            "host": self.config.host,

            "port": self.config.port,

        }

    # =====================================================
    # Helpers
    # =====================================================

    def test_connection(self) -> bool:

        try:

            return self.connect()

        except Exception:

            return False
