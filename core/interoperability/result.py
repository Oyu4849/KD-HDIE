"""
KD-HDIE Framework

Interoperability Result (Final v2.0)

Purpose
-------
Standard execution result returned by the
Scientific Interoperability Engine.

Responsibilities
----------------
• Execution status
• Unified data
• Context reference
• Statistics
• Diagnostics
• Metadata

Dissertation
------------
Chapter 3
Execution Result Model

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.interoperability.context import (
    InteroperabilityContext,
)


# ==========================================================
# Result
# ==========================================================

@dataclass(slots=True)
class InteroperabilityResult:
    """
    Standard framework execution result.
    """

    # =====================================================
    # Status
    # =====================================================

    success: bool

    message: str = ""

    # =====================================================
    # Data
    # =====================================================

    data: Any = None

    context: InteroperabilityContext | None = None

    # =====================================================
    # Statistics
    # =====================================================

    records_processed: int = 0

    algorithms_executed: int = 0

    execution_time: float = 0.0

    # =====================================================
    # Diagnostics
    # =====================================================

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    # =====================================================
    # Metadata
    # =====================================================

    metadata: dict[str, Any] = field(default_factory=dict)

    statistics: dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # Factory Methods
    # =====================================================

    @classmethod
    def ok(
        cls,
        *,
        data: Any = None,
        context: InteroperabilityContext | None = None,
        message: str = "Execution completed successfully.",
        metadata: dict[str, Any] | None = None,
    ) -> "InteroperabilityResult":

        statistics = {}

        records = 0
        algorithms = 0
        execution_time = 0.0
        warnings = []

        if context is not None:

            statistics = dict(context.statistics)

            records = statistics.get("records", 0)

            algorithms = statistics.get(
                "algorithms",
                0,
            )

            execution_time = context.execution_time

            warnings = list(context.warnings)

        return cls(

            success=True,

            message=message,

            data=data,

            context=context,

            records_processed=records,

            algorithms_executed=algorithms,

            execution_time=execution_time,

            warnings=warnings,

            metadata=metadata or {},

            statistics=statistics,

        )

    # ------------------------------------------------------

    @classmethod
    def fail(
        cls,
        *,
        message: str,
        context: InteroperabilityContext | None = None,
        errors: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "InteroperabilityResult":

        execution_time = 0.0
        warnings = []
        statistics = {}

        if context is not None:

            execution_time = context.execution_time

            warnings = list(context.warnings)

            statistics = dict(context.statistics)

        return cls(

            success=False,

            message=message,

            context=context,

            execution_time=execution_time,

            warnings=warnings,

            errors=errors or [],

            metadata=metadata or {},

            statistics=statistics,

        )

    # =====================================================
    # Helpers
    # =====================================================

    @property
    def has_errors(self) -> bool:

        return len(self.errors) > 0

    # ------------------------------------------------------

    @property
    def has_warnings(self) -> bool:

        return len(self.warnings) > 0

    # ------------------------------------------------------

    def add_warning(

        self,

        message: str,

    ) -> None:

        self.warnings.append(message)

    # ------------------------------------------------------

    def add_error(

        self,

        message: str,

    ) -> None:

        self.errors.append(message)

        self.success = False

    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "success": self.success,

            "message": self.message,

            "records_processed":
                self.records_processed,

            "algorithms_executed":
                self.algorithms_executed,

            "execution_time":
                self.execution_time,

            "warnings":
                self.warnings,

            "errors":
                self.errors,

            "statistics":
                self.statistics,

            "metadata":
                self.metadata,

            "context":
                None

                if self.context is None

                else self.context.to_dict(),

        }
