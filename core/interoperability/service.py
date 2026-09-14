"""
KD-HDIE Framework

Interoperability Service
Final v2.1

Purpose
-------
Application service layer for the KD-HDIE Framework.

Responsibilities
----------------
• Create interoperability contexts
• Select workflows
• Execute single-source interoperability
• Execute multi-source interoperability
• Provide a stable application-level API

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from typing import Any

from core.registry import registry

from datasource.connectors.manager import (
    connector_manager,
)

from core.knowledge.reasoner import (
    KnowledgeReasoner,
)

from core.interoperability.context import (
    InteroperabilityContext,
)

from core.interoperability.engine import (
    InteroperabilityEngine,
)

from core.interoperability.result import (
    InteroperabilityResult,
)

from core.interoperability.workflow import (
    WorkflowFactory,
)


class InteroperabilityService:
    """
    Application service for KD-HDIE interoperability.

    Provides:

    1. Single-source execution
    2. Multi-source execution
    3. Workflow selection
    4. Framework-level execution metadata
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        self.engine = InteroperabilityEngine(

            registry=registry,

            connector_manager=connector_manager,

        )

    # =====================================================
    # Execute — Single Source
    # =====================================================

    def execute(

        self,

        source_system: str,

        target_system: str,

        connection_parameters: dict,

        operation: str = "INTEROPERABILITY",

        workflow_name: str = "DEFAULT",

    ) -> InteroperabilityResult:

        """
        Execute complete single-source
        interoperability pipeline.
        """

        context = InteroperabilityContext(

            source_system=source_system,

            target_system=target_system,

            operation=operation,

            workflow=workflow_name,

            connection_parameters=(
                connection_parameters
            ),

        )

        workflow = self._select_workflow(

            workflow_name

        )

        context.log(

            f"Workflow: {workflow.name}"

        )

        result = self.engine.execute(

            workflow=workflow,

            context=context,

        )

        result.metadata.update(

            {

                "framework":
                    "KD-HDIE",

                "workflow":
                    workflow.name,

                "workflow_type":
                    workflow.workflow_type.value,

            }

        )

        return result

    # =====================================================
    # Execute — Multi Source
    # =====================================================

    def execute_multi_source(

        self,

        sources: list[dict[str, Any]],

        workflow_name: str = "DEFAULT",

    ) -> InteroperabilityResult:

        """
        Execute multiple heterogeneous sources
        through the KD-HDIE multi-source pipeline.

        Parameters
        ----------
        sources:
            List of source definitions.

        Example
        -------

        sources = [

            {
                "source_system": "OPENMETEO",

                "connection_parameters": {
                    ...
                },
            },

            {
                "source_system": "NASA",

                "connection_parameters": {
                    ...
                },
            },

        ]

        Processing
        ----------

        Each source independently passes through:

            Connector
                ↓
            Normalizer
                ↓
            Adapter
                ↓
            Metadata
                ↓
            Resolver
                ↓
            Semantic
                ↓
            Mapping
                ↓
            Harmonization
                ↓
            MonthlyAggregation

        Then:

            Source A + Source B
                    ↓
                  Merge
                    ↓
                 Quality
                    ↓
                 Conflict
                    ↓
               Reliability
                    ↓
                  Fusion
                    ↓
              UnifiedModel
        """

        if not sources:

            return InteroperabilityResult.fail(

                message=(

                    "No source systems were "
                    "provided."

                ),

                errors=[

                    (
                        "At least one source "
                        "definition is required."
                    )

                ],

            )

        workflow = self._select_workflow(

            workflow_name

        )

        # -------------------------------------------------
        # Validate source definitions
        # -------------------------------------------------

        for index, source in enumerate(
            sources
        ):

            if not isinstance(
                source,
                dict,
            ):

                return InteroperabilityResult.fail(

                    message=(

                        "Invalid source definition."
                    ),

                    errors=[

                        (
                            f"Source at index {index} "
                            f"must be a dictionary."
                        )

                    ],

                )

            source_system = str(

                source.get(
                    "source_system",
                    "",
                )

            ).strip()

            if not source_system:

                return InteroperabilityResult.fail(

                    message=(

                        "Invalid source definition."
                    ),

                    errors=[

                        (
                            f"Source at index {index} "
                            f"does not contain "
                            f"'source_system'."
                        )

                    ],

                )

            parameters = source.get(

                "connection_parameters",
                {},

            )

            if not isinstance(
                parameters,
                dict,
            ):

                return InteroperabilityResult.fail(

                    message=(

                        "Invalid connection parameters."
                    ),

                    errors=[

                        (
                            f"Connection parameters "
                            f"for source "
                            f"'{source_system}' "
                            f"must be a dictionary."
                        )

                    ],

                )

        # -------------------------------------------------
        # Execute multi-source engine
        # -------------------------------------------------

        result = (
            self.engine.execute_multi_source(

                workflow=workflow,

                sources=sources,

            )
        )

        # -------------------------------------------------
        # Service-level metadata
        # -------------------------------------------------

        result.metadata.update(

            {

                "framework":
                    "KD-HDIE",

                "workflow":
                    workflow.name,

                "workflow_type":
                    workflow.workflow_type.value,

                "multi_source":
                    True,

                "source_systems": [

                    str(
                        source.get(
                            "source_system",
                            "",
                        )
                    ).upper()

                    for source in sources

                ],

                "source_count":
                    len(sources),

            }

        )

        return result

    # =====================================================
    # Workflow Selection
    # =====================================================

    def _select_workflow(

        self,

        workflow_name: str,

    ):

        """
        Select workflow implementation by name.
        """

        workflow_name = (
            workflow_name.upper()
        )

        if workflow_name == "DAILY":

            return WorkflowFactory.daily()

        # Reproducible ablation variants for the experimental protocol.
        if workflow_name == "ABLATION_A1":
            return WorkflowFactory.ablation_a1()

        if workflow_name == "ABLATION_A2":
            return WorkflowFactory.ablation_a2()

        if workflow_name == "ABLATION_A3":
            return WorkflowFactory.ablation_a3()

        if workflow_name == "ABLATION_A4":
            return WorkflowFactory.ablation_a4()

        if workflow_name == "VALIDATION":

            return WorkflowFactory.validation()

        if workflow_name == "SYNCHRONIZATION":

            return (
                WorkflowFactory.synchronization()
            )

        return WorkflowFactory.default()
