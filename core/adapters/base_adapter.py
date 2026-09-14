from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from attributes.models import UnifiedRecord


# ==========================================================
# Adapter Result
# ==========================================================

@dataclass(slots=True)
class AdapterResult:

    success: bool

    records: list[UnifiedRecord] = field(default_factory=list)

    message: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Base Adapter
# ==========================================================

class BaseAdapter(ABC):

    source_type: str = ""

    @abstractmethod
    def execute(
        self,
        records: list[dict],
    ) -> AdapterResult:
        """
        Transform source records into unified records.
        """
        raise NotImplementedError
