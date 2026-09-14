from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from attributes.models import UnifiedRecord


# ==========================================================
# Algorithm Result
# ==========================================================

@dataclass(slots=True)
class AlgorithmResult:

    success: bool

    data: Any = None

    message: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Base Algorithm
# ==========================================================

class BaseAlgorithm(ABC):

    name: str = ""

    order: int = 0

    @abstractmethod
    def execute(
        self,
        data: list[UnifiedRecord],
        context,
    ) -> AlgorithmResult:
        pass
