"""
KD-HDIE Framework

CSV Connector
"""

from __future__ import annotations

import csv
from pathlib import Path
from time import perf_counter

from datasource.connectors.base_connector import (
    BaseConnector,
    ConnectorResult,
)


class CSVConnector(BaseConnector):
    """
    Connector for CSV files.
    """

    name = "CSV Connector"

    source_type = "CSV"

    version = "2.0"

    def __init__(self):

        super().__init__()

        self.file_path: Path | None = None

        self._connected = False

    # =====================================================
    # Connection
    # =====================================================

    def connect(self) -> bool:

        if self.file_path is None:

            raise ValueError(
                "CSV file path is not specified."
            )

        if not self.file_path.exists():

            raise FileNotFoundError(
                f"CSV file not found: {self.file_path}"
            )

        self._connected = True

        self.connection.connected = True

        self.connection.endpoint = str(self.file_path)

        return True

    # -----------------------------------------------------

    def disconnect(self) -> None:

        self._connected = False

        self.connection.connected = False

    # -----------------------------------------------------

    def is_connected(self) -> bool:

        return self._connected

    # =====================================================
    # Read
    # =====================================================

    def read(
        self,
        *,
        file_path: str | Path,
        encoding: str = "utf-8",
        delimiter: str = ",",
    ) -> ConnectorResult:

        started = perf_counter()

        self.file_path = Path(file_path)

        if not self.is_connected():

            self.connect()

        records = []

        with open(
            self.file_path,
            mode="r",
            encoding=encoding,
            newline="",
        ) as csv_file:

            reader = csv.DictReader(
                csv_file,
                delimiter=delimiter,
            )

            for row in reader:

                records.append(dict(row))

            columns = reader.fieldnames or []

        elapsed = perf_counter() - started

        return ConnectorResult(

            success=True,

            data=records,

            execution_time=round(elapsed, 6),

            metadata={

                "file": str(self.file_path),

                "records": len(records),

                "columns": columns,

            },

        )

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(self) -> dict:

        if self.file_path is None:

            return {}

        if not self.is_connected():

            self.connect()

        with open(
            self.file_path,
            mode="r",
            encoding="utf-8",
            newline="",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            columns = reader.fieldnames or []

        return {

            "connector": self.name,

            "source_type": self.source_type,

            "file_name": self.file_path.name,

            "path": str(self.file_path),

            "columns": columns,

            "column_count": len(columns),

        }

    # =====================================================
    # Statistics
    # =====================================================

    def row_count(self) -> int:

        if self.file_path is None:

            return 0

        if not self.is_connected():

            self.connect()

        with open(
            self.file_path,
            mode="r",
            encoding="utf-8",
            newline="",
        ) as csv_file:

            reader = csv.reader(csv_file)

            next(reader, None)

            return sum(1 for _ in reader)

    # -----------------------------------------------------

    def exists(self) -> bool:

        if self.file_path is None:

            return False

        return self.file_path.exists()

    # -----------------------------------------------------

    def __str__(self):

        if self.file_path is None:

            return "CSVConnector(<uninitialized>)"

        return f"CSVConnector({self.file_path.name})"
