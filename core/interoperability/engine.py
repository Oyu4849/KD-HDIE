"""
KD-HDIE Framework

Scientific Interoperability Engine
Final v4.1

Purpose
-------
Central execution engine of the KD-HDIE Framework.

Execution modes
---------------
Single-source:

    Connector
        ↓
    Response Normalizer
        ↓
    Adapter
        ↓
    Workflow Algorithms
        ↓
    Unified Data Model


Multi-source:

    Source A
        ↓
    Connector
        ↓
    Normalizer
        ↓
    Adapter
        ↓
    Pre-fusion Workflow
        ↓
    Monthly Aggregation
        │
        ├───────────────┐
        ↓               ↓
    Source A        Source B
        │               │
        └───────┬───────┘
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
          Unified Model

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from typing import Any

from core.registry import Registry

from datasource.connectors.manager import ConnectorManager

from core.interoperability.context import (
    InteroperabilityContext,
)

from core.interoperability.result import (
    InteroperabilityResult,
)

from core.interoperability.workflow import (
    Workflow,
)

from core.interoperability.normalizers.base import (
    BaseResponseNormalizer,
)

from core.interoperability.normalizers.openmeteo import (
    OpenMeteoResponseNormalizer,
)

from core.interoperability.normalizers.nasa import (
    NASAResponseNormalizer,
)
from core.interoperability.normalizers.tabular import TabularResponseNormalizer

from core.interoperability.normalizers.generic_json import (
    GenericJSONResponseNormalizer,
)

class InteroperabilityEngine:
    """
    Scientific interoperability execution engine.

    Supports:

    1. Single-source execution
    2. Multi-source execution
    3. Response normalization
    4. Adapter execution
    5. Workflow execution
    6. Multi-source data fusion
    """

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(
        self,
        *,
        registry: Registry,
        connector_manager: ConnectorManager,
    ):

        self._registry = registry

        self._connector_manager = (
            connector_manager
        )

        # ==================================================
        # Response Normalizers
        # ==================================================

        self._normalizers: dict[
            str,
            BaseResponseNormalizer,
        ] = {

            "OPENMETEO":
                OpenMeteoResponseNormalizer(),

            "NASA":
                NASAResponseNormalizer(),

            "GENERIC_API":
                GenericJSONResponseNormalizer(),

            "GEE":
                TabularResponseNormalizer(),

        }

    # ======================================================
    # Normalizer
    # ======================================================

    def _normalizer(
        self,
        source_system: str,
    ) -> BaseResponseNormalizer:

        key = source_system.upper()

        if key not in self._normalizers:

            raise ValueError(
                f"Response normalizer "
                f"'{source_system}' "
                f"is not registered."
            )

        return self._normalizers[key]

    # ======================================================
    # Execute — Single Source
    # ======================================================

    def execute(
        self,
        workflow: Workflow,
        context: InteroperabilityContext,
    ) -> InteroperabilityResult:
        """
        Execute the standard single-source workflow.

        This method preserves the Final v4.0 behaviour
        while correcting algorithm execution counting.
        """

        context.start()

        try:

            # ==================================================
            # 1. CONNECTOR
            # ==================================================

            connector = (
                self._connector_manager.connector(
                    context.source_system
                )
            )

            connector_result = connector.read(
                **context.connection_parameters
            )

            if not connector_result.success:

                context.error(
                    connector_result.message
                )

                context.finish()

                return InteroperabilityResult.fail(
                    message=(
                        connector_result.message
                    ),
                    context=context,
                )

            # Preserve raw API response.

            context.raw_data = (
                connector_result.data
            )

            # ==================================================
            # 2. RESPONSE NORMALIZATION
            # ==================================================

            normalizer = self._normalizer(
                context.source_system
            )

            normalized_data = (
                normalizer.normalize(
                    connector_result.data
                )
            )

            if not normalizer.validate(
                normalized_data
            ):

                raise ValueError(
                    "Response normalization "
                    "returned invalid data."
                )

            context.shared_data[
                "normalized_data"
            ] = normalized_data

            context.metadata[
                "normalizer"
            ] = normalizer.metadata()

            # ==================================================
            # 3. ADAPTER
            # ==================================================

            adapter = self._registry.adapter(
                context.source_system
            )

            adapter_result = adapter.execute(
                normalized_data
            )

            if not adapter_result.success:

                context.error(
                    adapter_result.message
                )

                context.finish()

                return InteroperabilityResult.fail(
                    message=(
                        adapter_result.message
                    ),
                    context=context,
                )

            current_data = (
                adapter_result.records
            )

            context.unified_data = (
                current_data
            )

            context.increment(
                "records",
                len(current_data),
            )

            # ==================================================
            # 4. WORKFLOW
            # ==================================================

            for step in (
                workflow.enabled_steps()
            ):

                context.set_step(
                    step.algorithm
                )

                context.set_algorithm(
                    step.algorithm
                )

                algorithm = (
                    self._registry.algorithm(
                        step.algorithm
                    )
                )

                algorithm_result = (
                    algorithm.execute(

                        data=current_data,

                        context=context,

                    )
                )

                if not algorithm_result.success:

                    context.error(
                        algorithm_result.message
                    )

                    context.finish()

                    return (
                        InteroperabilityResult.fail(

                            message=(
                                algorithm_result.message
                            ),

                            context=context,

                        )
                    )

                current_data = (
                    algorithm_result.data
                )

                context.unified_data = (
                    current_data
                )

                # ----------------------------------------------
                # Preserve algorithm metadata
                # ----------------------------------------------

                context.shared_data[
                    f"algorithm_{step.algorithm}"
                ] = (
                    algorithm_result.metadata
                )

                context.log(
                    f"{step.algorithm} "
                    f"completed."
                )

            # ==================================================
            # 5. FINISH
            # ==================================================

            context.finish()

            return InteroperabilityResult.ok(

                data=current_data,

                context=context,

                metadata={

                    "framework":
                        "KD-HDIE",

                    "workflow":
                        workflow.name,

                    "workflow_type":
                        workflow.workflow_type.value,

                    "source_system":
                        context.source_system,

                    "normalizer":
                        normalizer.__class__.__name__,

                    "records_processed":
                        context.statistics.get(
                            "records",
                            0,
                        ),

                    "algorithms_executed":
                        context.statistics.get(
                            "algorithms",
                            0,
                        ),

                },

            )

        except Exception as ex:

            import traceback

            traceback.print_exc()

            context.error(
                str(ex)
            )

            context.finish()

            return (
                InteroperabilityResult.fail(

                    message=(
                        "Engine execution failed."
                    ),

                    context=context,

                    errors=[

                        str(ex),

                        traceback.format_exc(),

                    ],

                )
            )

    # ======================================================
    # Execute Multi Source
    # ======================================================

    def execute_multi_source(
        
        self,
        workflow: Workflow,
        sources: list[dict[str, Any]],
    ) -> InteroperabilityResult:
        """
        Execute multiple heterogeneous sources through
        a common interoperability and fusion pipeline.

        Parameters
        ----------
        workflow:
            Workflow definition.

        sources:
            List of source definitions.

            Example:

                [
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

        Execution strategy
        ------------------
        Each source independently executes the workflow
        through MonthlyAggregation.

        After source-level harmonization and temporal
        aggregation, records are merged.

        The merged records then pass through:

            Quality
                ↓
            Conflict
                ↓
            Reliability
                ↓
            Fusion
                ↓
            UnifiedModel

        This preserves source-specific values until
        conflict resolution.
        """

        import traceback
        import time
        multi_context = None
        execution_start = time.perf_counter()

        if not sources:

            return InteroperabilityResult.fail(
                message=(
                    "No source systems were "
                    "provided for multi-source execution."
                ),
                errors=[
                    "sources must contain at least "
                    "one source definition."
                ],
            )

        try:

            # ==================================================
            # 1. Separate Workflow Stages
            # ==================================================

            steps = (
                workflow.enabled_steps()
            )

            # --------------------------------------------------
            # Algorithms executed independently by each source
            #
            # Everything through MonthlyAggregation belongs
            # to source-level preprocessing.
            # --------------------------------------------------

            pre_fusion_steps = []

            post_fusion_steps = []

            aggregation_found = False

            for step in steps:

                if step.algorithm == (
                    "MonthlyAggregation"
                ):

                    pre_fusion_steps.append(
                        step
                    )

                    aggregation_found = True

                    continue

                if not aggregation_found:

                    pre_fusion_steps.append(
                        step
                    )

                else:

                    post_fusion_steps.append(
                        step
                    )

            # --------------------------------------------------
            # Daily workflow support
            # --------------------------------------------------
            if not aggregation_found:
                pre_fusion_steps = []
                post_fusion_steps = []
                merge_stage_found = False
                post_merge_algorithms = {"Quality", "Conflict", "Reliability", "Fusion", "UnifiedModel"}

                for step in steps:
                    if step.algorithm in post_merge_algorithms:
                        merge_stage_found = True
                        post_fusion_steps.append(step)
                    elif merge_stage_found:
                        post_fusion_steps.append(step)
                    else:
                        pre_fusion_steps.append(step)

                if not merge_stage_found:
                    raise ValueError(
                        "A multi-source workflow without MonthlyAggregation "
                        "requires a post-merge stage (Quality/Conflict/"
                        "Reliability/Fusion/UnifiedModel)."
                    )

            # ==================================================
            # 2. Process Each Source Independently
            # ==================================================

            source_records: list[
                Any
            ] = []

            source_contexts: list[
                InteroperabilityContext
            ] = []

            source_statistics: dict[
                str,
                dict[str, Any],
            ] = {}

            total_algorithms = 0

            for source_definition in sources:

                source_system = str(
                    source_definition.get(
                        "source_system",
                        "",
                    )
                ).upper().strip()

                connection_parameters = (
                    source_definition.get(
                        "connection_parameters",
                        {},
                    )
                )

                if not source_system:

                    raise ValueError(
                        "Each source definition "
                        "must contain 'source_system'."
                    )

                # --------------------------------------------------
                # Context
                # --------------------------------------------------

                source_context = (
                    InteroperabilityContext(

                        source_system=(
                            source_system
                        ),

                        target_system="KD-HDIE",

                        operation="INTEROPERABILITY",

                        workflow=(
                            workflow.name
                        ),

                        connection_parameters=(
                            connection_parameters
                        ),

                    )
                )

                source_context.start()

                # --------------------------------------------------
                # Connector
                # --------------------------------------------------

                connector = (
                    self._connector_manager.connector(
                        source_system
                    )
                )

                connector_result = (
                    connector.read(
                        **connection_parameters
                    )
                )

                if not connector_result.success:

                    source_context.error(
                        connector_result.message
                    )

                    source_context.finish()

                    raise RuntimeError(
                        f"{source_system} connector failed: "
                        f"{connector_result.message}"
                    )

                source_context.raw_data = (
                    connector_result.data
                )

                # --------------------------------------------------
                # Normalizer
                # --------------------------------------------------

                normalizer = self._normalizer(
                    source_system
                )

                normalized_data = (
                    normalizer.normalize(
                        connector_result.data
                    )
                )

                if not normalizer.validate(
                    normalized_data
                ):

                    raise ValueError(
                        f"{source_system} response "
                        f"normalization returned invalid data."
                    )

                source_context.shared_data[
                    "normalized_data"
                ] = normalized_data

                source_context.metadata[
                    "normalizer"
                ] = normalizer.metadata()

                # --------------------------------------------------
                # Adapter
                # --------------------------------------------------

                adapter = (
                    self._registry.adapter(
                        source_system
                    )
                )

                adapter_result = (
                    adapter.execute(
                        normalized_data
                    )
                )

                if not adapter_result.success:

                    raise RuntimeError(
                        f"{source_system} adapter failed: "
                        f"{adapter_result.message}"
                    )

                current_data = (
                    adapter_result.records
                )

                source_context.unified_data = (
                    current_data
                )

                source_context.increment(
                    "records",
                    len(current_data),
                )

                # --------------------------------------------------
                # Source-level workflow
                # --------------------------------------------------

                for step in pre_fusion_steps:

                    source_context.set_step(
                        step.algorithm
                    )

                    source_context.set_algorithm(
                        step.algorithm
                    )

                    algorithm = (
                        self._registry.algorithm(
                            step.algorithm
                        )
                    )

                    algorithm_result = (
                        algorithm.execute(

                            data=current_data,

                            context=source_context,

                        )
                    )

                    if not algorithm_result.success:

                        raise RuntimeError(
                            f"{source_system} "
                            f"{step.algorithm} failed: "
                            f"{algorithm_result.message}"
                        )

                    current_data = (
                        algorithm_result.data
                    )

                    source_context.unified_data = (
                        current_data
                    )


                    source_context.shared_data[
                        f"algorithm_{step.algorithm}"
                    ] = (
                        algorithm_result.metadata
                    )

                    source_context.log(
                        f"{step.algorithm} "
                        f"completed for "
                        f"{source_system}."
                    )
                    # --------------------------------------------------
                    # Normalize algorithm output
                    # --------------------------------------------------
                    #
                    # Some algorithms, especially UnifiedModel,
                    # may return a model object instead of a raw
                    # list of UnifiedRecord objects.
                    #
                    # Multi-source processing requires a record list
                    # before source-level merging.
                    # --------------------------------------------------

                    if hasattr(current_data, "records"):

                        current_data = (
                            current_data.records
                        )

                    source_context.unified_data = (
                        current_data
                    )


                # --------------------------------------------------
                # Preserve source information
                # --------------------------------------------------

                for record in current_data:

                    if not record.source_system:

                        record.source_system = (
                            source_system
                        )

                    for attribute in (
                        record.attributes
                    ):

                        if not attribute.source_system:

                            attribute.source_system = (
                                source_system
                            )

                source_records.extend(
                    current_data
                )

                source_context.finish()

                source_contexts.append(
                    source_context
                )

                source_statistics[
                    source_system
                ] = {

                    "input_records":
                        len(
                            adapter_result.records
                        ),

                    "output_records":
                        len(current_data),

                    "algorithms_executed":
                        source_context.statistics.get(
                            "algorithms",
                            0,
                        ),

                }

                total_algorithms += (
                    source_context.statistics.get(
                        "algorithms",
                        0,
                    )
                )

            # ==================================================
            # 3. Merge Source Records
            # ==================================================

            merged_data = list(
                source_records
            )

            # ==================================================
            # 4. Shared Multi-Source Context
            # ==================================================

            source_names = [

                str(
                    source.get(
                        "source_system",
                        "",
                    )
                ).upper()

                for source in sources

            ]

            multi_context = (
                InteroperabilityContext(

                    source_system=(
                        "MULTI_SOURCE"
                    ),

                    target_system="KD-HDIE",

                    operation="INTEROPERABILITY",

                    workflow=(
                        workflow.name
                    ),

                )
            )

            multi_context.start()

            multi_context.shared_data[
                "source_systems"
            ] = source_names

            multi_context.shared_data[
                "source_records"
            ] = source_records

            multi_context.shared_data[
                "source_statistics"
            ] = source_statistics

            multi_context.unified_data = (
                merged_data
            )

            multi_context.increment(
                "records",
                len(merged_data),
            )

            # --------------------------------------------------
            # Preserve source contexts
            # --------------------------------------------------

            multi_context.shared_data[
                "source_contexts"
            ] = source_contexts

            # ==================================================
            # 5. Post-Fusion Workflow
            # ==================================================

            current_data = (
                merged_data
            )

            for step in post_fusion_steps:

                multi_context.set_step(
                    step.algorithm
                )

                multi_context.set_algorithm(
                    step.algorithm
                )

                algorithm = (
                    self._registry.algorithm(
                        step.algorithm
                    )
                )

                algorithm_result = (
                    algorithm.execute(

                        data=current_data,

                        context=multi_context,

                    )
                )

                if not algorithm_result.success:

                    multi_context.error(
                        algorithm_result.message
                    )

                    multi_context.finish()

                    return (
                        InteroperabilityResult.fail(

                            message=(
                                algorithm_result.message
                            ),

                            context=multi_context,

                        )
                    )

                current_data = (
                    algorithm_result.data
                )

                multi_context.unified_data = (
                    current_data
                )

                multi_context.shared_data[
                    f"algorithm_{step.algorithm}"
                ] = (
                    algorithm_result.metadata
                )

                multi_context.log(
                    f"{step.algorithm} "
                    f"completed in multi-source mode."
                )

            # ==================================================
            # 6. Final Statistics
            # ==================================================

            execution_time = (
                time.perf_counter()
                - execution_start
            )

            # --------------------------------------------------
            # Normalize final record representation
            # --------------------------------------------------
            #
            # UnifiedModel returns UnifiedInformationModel.
            # Earlier stages use list[UnifiedRecord].
            #
            # Keep current_data unchanged as the final payload,
            # but use its records collection for record-level
            # statistics.
            # --------------------------------------------------

            if hasattr(
                current_data,
                "records",
            ):

                final_records = (
                    current_data.records
                )

            else:

                final_records = (
                    current_data
                )

            multi_context.metadata[
                "multi_source"
            ] = True

            multi_context.metadata[
                "source_systems"
            ] = source_names

            multi_context.metadata[
                "source_count"
            ] = len(
                source_names
            )

            multi_context.metadata[
                "source_statistics"
            ] = source_statistics

            multi_context.metadata[
                "pre_fusion_algorithms"
            ] = total_algorithms

            multi_context.metadata[
                "post_fusion_algorithms"
            ] = multi_context.statistics.get(
                "algorithms",
                0,
            )

            multi_context.metadata[
                "total_algorithm_executions"
            ] = (
                total_algorithms
                +
                multi_context.statistics.get(
                    "algorithms",
                    0,
                )
            )

            multi_context.metadata[
                "execution_time"
            ] = round(
                execution_time,
                6,
            )

            multi_context.metadata[
                "final_records"
            ] = len(
                final_records
            )

            multi_context.finish()

            # ==================================================
            # 7. Result
            # ==================================================

            return InteroperabilityResult.ok(

                data=current_data,

                context=multi_context,

                metadata={

                    "framework":
                        "KD-HDIE",

                    "workflow":
                        workflow.name,

                    "workflow_type":
                        workflow.workflow_type.value,

                    "multi_source":
                        True,

                    "source_systems":
                        source_names,

                    "source_count":
                        len(source_names),

                    "records_processed":
                        len(final_records),

                    "final_records":
                        len(final_records),

                    "source_statistics":
                        source_statistics,

                    "pre_fusion_algorithms":
                        total_algorithms,

                    "post_fusion_algorithms":
                        multi_context.statistics.get(
                            "algorithms",
                            0,
                        ),

                    "total_algorithm_executions":
                        (
                            total_algorithms
                            +
                            multi_context.statistics.get(
                                "algorithms",
                                0,
                            )
                        ),

                    "execution_time":
                        round(
                            execution_time,
                            6,
                        ),

                },

            )

        except Exception as ex:

            traceback.print_exc()

            execution_time = (
                time.perf_counter()
                - execution_start
            )

            if multi_context is not None:

                multi_context.error(str(ex))

                multi_context.metadata[
                    "execution_time"
                ] = round(
                    execution_time,
                    6,
                )

                multi_context.finish()

            return InteroperabilityResult.fail(

                message=(
                    "Multi-source engine "
                    "execution failed."
                ),

                context=multi_context,

                errors=[
                    str(ex),
                    traceback.format_exc(),
                ],

            )            
