"""Google Earth Engine export connector for KD-HDIE.

Reads CSV exported from Google Earth Engine. The connector does not
claim to call Earth Engine directly; provenance records the export as
an Earth Engine-derived source.
"""
from __future__ import annotations
from pathlib import Path
from datasource.connectors.csv_connector import CSVConnector

class GEEExportConnector(CSVConnector):
    name = "Google Earth Engine Export Connector"
    source_type = "GEE"
    version = "1.0"

    def read(self, *, file_path: str | Path, encoding: str = "utf-8", delimiter: str = ","):
        result = super().read(file_path=file_path, encoding=encoding, delimiter=delimiter)
        if result.metadata is not None:
            result.metadata.update({
                "source_type": "GEE",
                "provider": "Google Earth Engine",
                "provenance": "Earth Engine exported dataset",
            })
        return result
