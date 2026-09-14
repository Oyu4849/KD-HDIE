"""
KD-HDIE Framework

Workflow Definition
Final v2.1

Purpose
-------
Define execution sequences for KD-HDIE algorithms.

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ==========================================================
# Workflow Type
# ==========================================================

class WorkflowType(Enum):

    DEFAULT = "DEFAULT"

    VALIDATION = "VALIDATION"

    SYNCHRONIZATION = "SYNCHRONIZATION"


# ==========================================================
# Workflow Step
# ==========================================================

@dataclass(slots=True)
class WorkflowStep:

    algorithm: str

    priority: int

    enabled: bool = True

    parameters: dict = field(
        default_factory=dict
    )


# ==========================================================
# Workflow
# ==========================================================

@dataclass
class Workflow:

    name: str

    workflow_type: WorkflowType

    steps: list[WorkflowStep] = field(
        default_factory=list
    )

    # ======================================================
    # Add Step
    # ======================================================

    def add_step(
        self,
        algorithm: str,
        priority: int,
        parameters: dict | None = None,
    ):

        self.steps.append(

            WorkflowStep(

                algorithm=algorithm,

                priority=priority,

                parameters=(
                    parameters
                    if parameters is not None
                    else {}
                ),

            )

        )

    # ======================================================
    # Enabled Steps
    # ======================================================

    def enabled_steps(self):

        return sorted(

            [

                step

                for step in self.steps

                if step.enabled

            ],

            key=lambda step: step.priority,

        )


# ==========================================================
# Workflow Factory
# ==========================================================

class WorkflowFactory:

    # ======================================================
    # DEFAULT
    # ======================================================

    @staticmethod
    def default() -> Workflow:

        workflow = Workflow(

            name="Default",

            workflow_type=(
                WorkflowType.DEFAULT
            ),

        )

        workflow.add_step(
            "Metadata",
            priority=10,
        )

        workflow.add_step(
            "Resolver",
            priority=20,
        )

        workflow.add_step(
            "Semantic",
            priority=30,
        )

        workflow.add_step(
            "Mapping",
            priority=40,
        )

        workflow.add_step(
            "Harmonization",
            priority=50,
        )

        # --------------------------------------------------
        # NEW
        # Daily → Monthly
        # --------------------------------------------------

        workflow.add_step(
            "MonthlyAggregation",
            priority=55,
        )

        workflow.add_step(
            "Quality",
            priority=60,
        )

        workflow.add_step(
            "Conflict",
            priority=70,
        )

        workflow.add_step(
            "Reliability",
            priority=75,
        )

        workflow.add_step(
            "Fusion",
            priority=80,
        )

        workflow.add_step(
            "UnifiedModel",
            priority=90,
        )

        return workflow

    # ======================================================
    # DAILY
    # ======================================================

    @staticmethod
    def daily() -> Workflow:
        workflow = Workflow(
            name="Daily",
            workflow_type=WorkflowType.DEFAULT,
        )
        workflow.add_step("Metadata", priority=10)
        workflow.add_step("Resolver", priority=20)
        workflow.add_step("Semantic", priority=30)
        workflow.add_step("Mapping", priority=40)
        workflow.add_step("Harmonization", priority=50)
        workflow.add_step("Quality", priority=60)
        workflow.add_step("Conflict", priority=70)
        workflow.add_step("Reliability", priority=75)
        workflow.add_step("Fusion", priority=80)
        workflow.add_step("UnifiedModel", priority=90)
        return workflow

    # ======================================================
    # ABLATION VARIANTS
    # ======================================================

    @staticmethod
    def ablation_a1() -> Workflow:
        """Semantic mapping/harmonization only; no quality/conflict/fusion."""
        workflow = Workflow(name="Ablation-A1", workflow_type=WorkflowType.DEFAULT)
        for name, priority in [("Metadata",10),("Resolver",20),("Semantic",30),("Mapping",40),("Harmonization",50),("UnifiedModel",90)]:
            workflow.add_step(name, priority=priority)
        return workflow

    @staticmethod
    def ablation_a2() -> Workflow:
        """A1 plus quality validation."""
        workflow = WorkflowFactory.ablation_a1()
        workflow.steps = [step for step in workflow.steps if step.algorithm != "UnifiedModel"]
        workflow.add_step("Quality", priority=60)
        workflow.add_step("UnifiedModel", priority=90)
        workflow.name = "Ablation-A2"
        return workflow

    @staticmethod
    def ablation_a3() -> Workflow:
        """A2 plus conflict detection/resolution."""
        workflow = WorkflowFactory.ablation_a2()
        workflow.steps = [step for step in workflow.steps if step.algorithm != "UnifiedModel"]
        workflow.add_step("Conflict", priority=70)
        workflow.add_step("UnifiedModel", priority=90)
        workflow.name = "Ablation-A3"
        return workflow

    @staticmethod
    def ablation_a4() -> Workflow:
        """Full reliability-aware KD-HDIE fusion pipeline."""
        workflow = WorkflowFactory.daily()
        workflow.name = "Ablation-A4"
        return workflow

    # ======================================================
    # VALIDATION
    # ======================================================

    @staticmethod
    def validation() -> Workflow:

        workflow = Workflow(

            name="Validation",

            workflow_type=(
                WorkflowType.VALIDATION
            ),

        )

        workflow.add_step(
            "Metadata",
            priority=10,
        )

        workflow.add_step(
            "Resolver",
            priority=20,
        )

        workflow.add_step(
            "Semantic",
            priority=30,
        )

        workflow.add_step(
            "Mapping",
            priority=40,
        )

        workflow.add_step(
            "Harmonization",
            priority=50,
        )

        workflow.add_step(
            "MonthlyAggregation",
            priority=55,
        )

        workflow.add_step(
            "Quality",
            priority=60,
        )

        return workflow

    # ======================================================
    # SYNCHRONIZATION
    # ======================================================

    @staticmethod
    def synchronization() -> Workflow:

        workflow = Workflow(

            name="Synchronization",

            workflow_type=(
                WorkflowType.SYNCHRONIZATION
            ),

        )

        workflow.add_step(
            "Metadata",
            priority=10,
        )

        workflow.add_step(
            "Resolver",
            priority=20,
        )

        workflow.add_step(
            "Semantic",
            priority=30,
        )

        workflow.add_step(
            "Mapping",
            priority=40,
        )

        workflow.add_step(
            "Harmonization",
            priority=50,
        )

        workflow.add_step(
            "MonthlyAggregation",
            priority=55,
        )

        workflow.add_step(
            "Quality",
            priority=60,
        )

        workflow.add_step(
            "Conflict",
            priority=70,
        )

        workflow.add_step(
            "Reliability",
            priority=75,
        )

        workflow.add_step(
            "Fusion",
            priority=80,
        )

        workflow.add_step(
            "UnifiedModel",
            priority=90,
        )

        return workflow
