"""
KD-HDIE Framework

Interoperability Context (Final v2.0)

Purpose
-------
Execution context shared across the entire
interoperability pipeline.

Responsibilities
----------------
• Source and target information
• Runtime metadata
• Pipeline state
• Shared execution data
• Execution logging
• Performance timing

Dissertation
------------
Chapter 3
Execution Context

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


# ==========================================================
# Context
# ==========================================================

@dataclass(slots=True)
class InteroperabilityContext:
    """
    Shared execution context.
    """

    # =====================================================
    # Request
    # =====================================================

    source_system: str

    target_system: str

    operation: str = "INTEROPERABILITY"

    workflow: str = "DEFAULT"

    # =====================================================
    # Runtime Data
    # =====================================================

    raw_data: Any = None

    unified_data: Any = None

    connection_parameters: dict[str, Any] = field(default_factory=dict)

    shared_data: dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # Metadata
    # =====================================================

    metadata: dict[str, Any] = field(default_factory=dict)

    statistics: dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # Execution
    # =====================================================

    execution_id: str = field(

        default_factory=lambda: str(uuid4())

    )

    started_at: datetime | None = None

    finished_at: datetime | None = None

    execution_time: float = 0.0

    # =====================================================
    # Status
    # =====================================================

    success: bool = False

    current_step: str = ""

    current_algorithm: str = ""

    # =====================================================
    # Diagnostics
    # =====================================================

    logs: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    # =====================================================
    # Lifecycle
    # =====================================================

    def start(self) -> None:

        self.started_at = datetime.utcnow()

        self.success = False

        self.logs.append("Execution started.")

    # -----------------------------------------------------

    def finish(self) -> None:

        self.finished_at = datetime.utcnow()

        if self.started_at:

            self.execution_time = (

                self.finished_at -

                self.started_at

            ).total_seconds()

        self.success = (

            len(self.errors) == 0

        )

        self.logs.append("Execution finished.")

    # =====================================================
    # Step Management
    # =====================================================

    def set_step(

        self,

        step: str,

    ) -> None:

        self.current_step = step

    # -----------------------------------------------------

    def set_algorithm(

        self,

        algorithm: str,

    ) -> None:

        self.current_algorithm = algorithm

    # =====================================================
    # Shared Data
    # =====================================================

    def put(

        self,

        key: str,

        value: Any,

    ) -> None:

        self.shared_data[key] = value

    # -----------------------------------------------------

    def get(

        self,

        key: str,

        default: Any = None,

    ) -> Any:

        return self.shared_data.get(

            key,

            default,

        )

    # =====================================================
    # Metadata
    # =====================================================

    def set_metadata(

        self,

        key: str,

        value: Any,

    ) -> None:

        self.metadata[key] = value

    # -----------------------------------------------------

    def metadata_value(

        self,

        key: str,

        default: Any = None,

    ) -> Any:

        return self.metadata.get(

            key,

            default,

        )

    # =====================================================
    # Statistics
    # =====================================================

    def increment(

        self,

        key: str,

        value: int = 1,

    ) -> None:

        self.statistics[key] = (

            self.statistics.get(key, 0)

            + value

        )

    # =====================================================
    # Logging
    # =====================================================

    def log(

        self,

        message: str,

    ) -> None:

        self.logs.append(message)

    # -----------------------------------------------------

    def warn(

        self,

        message: str,

    ) -> None:

        self.warnings.append(message)

    # -----------------------------------------------------

    def error(

        self,

        message: str,

    ) -> None:

        self.errors.append(message)

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "execution_id": self.execution_id,

            "source_system": self.source_system,

            "target_system": self.target_system,

            "operation": self.operation,

            "workflow": self.workflow,

            "success": self.success,

            "execution_time": self.execution_time,

            "current_step": self.current_step,

            "current_algorithm": self.current_algorithm,

            "statistics": self.statistics,

            "metadata": self.metadata,

            "warnings": self.warnings,

            "errors": self.errors,

        }
