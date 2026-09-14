"""Pass-through normalizer for already tabular records."""
from __future__ import annotations
from typing import Any
from core.interoperability.normalizers.base import BaseResponseNormalizer

class TabularResponseNormalizer(BaseResponseNormalizer):
    source_type = "TABULAR"
    version = "1.0"

    def normalize(self, data: Any) -> list[dict[str, Any]]:
        if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
            raise ValueError("Tabular source must provide a list of record dictionaries.")
        return [dict(row) for row in data]

    def validate(self, data: Any) -> bool:
        return isinstance(data, list) and all(isinstance(row, dict) for row in data)
