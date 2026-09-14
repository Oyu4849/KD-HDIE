"""
KD-HDIE Framework

Unified Domain Models

Purpose
-------
Common data model used across all adapters,
algorithms and interoperability services.

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# Unified Attribute
# ==========================================================

@dataclass(slots=True)
class UnifiedAttribute:
    """
    Canonical representation of a single attribute.
    """

    source_name: str

    canonical_name: str

    value: Any

    unit: str = ""

    domain: str = ""

    source_system: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Unified Record
# ==========================================================

@dataclass(slots=True)
class UnifiedRecord:
    """
    Canonical representation of one observation.
    """

    timestamp: Any = None

    attributes: list[UnifiedAttribute] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    source_system: str = ""


# ==========================================================
# Unified Dataset
# ==========================================================

@dataclass(slots=True)
class UnifiedDataset:
    """
    Collection of unified records.
    """

    records: list[UnifiedRecord] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    statistics: dict[str, Any] = field(
        default_factory=dict
    )

    version: str = "2.0"
