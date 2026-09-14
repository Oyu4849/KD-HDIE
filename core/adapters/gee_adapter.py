"""Adapter for Google Earth Engine exported tabular datasets."""
from core.adapters.csv_adapter import CSVAdapter

class GEEAdapter(CSVAdapter):
    source_type = "GEE"
