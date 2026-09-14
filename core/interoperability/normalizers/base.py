"""
KD-HDIE Framework

Response Normalizer Base (Final v1.0)

Purpose
-------
Defines the common interface for transforming heterogeneous
API responses into a standardized list[dict] representation.

The normalizer does not perform semantic harmonization,
reliability assessment, conflict resolution, or fusion.
Those operations belong to later framework layers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseResponseNormalizer(ABC):
    """
    Base interface for API response normalizers.
    """

    source_type = "UNKNOWN"

    # =====================================================
    # Normalize
    # =====================================================

    @abstractmethod
    def normalize(
        self,
        data: Any,
    ) -> list[dict[str, Any]]:
        """
        Convert raw API response into standardized records.

        Parameters
        ----------
        data:
            Raw response returned by the API connector.

        Returns
        -------
        list[dict[str, Any]]
            Standardized records suitable for an adapter.
        """

        raise NotImplementedError

    # =====================================================
    # Validation
    # =====================================================

    def validate(
        self,
        data: Any,
    ) -> bool:
        """
        Basic validation of normalized data.
        """

        return isinstance(
            data,
            list,
        ) and all(
            isinstance(
                item,
                dict,
            )
            for item in data
        )

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(self) -> dict[str, Any]:
        """
        Return normalizer metadata.
        """

        return {
            "normalizer":
                self.__class__.__name__,

            "source_type":
                self.source_type,

            "version":
                "1.0",
        }
