"""
KD-HDIE Framework

Interoperability Orchestrator

Purpose:
Coordinates the complete heterogeneous
software interoperability workflow.

Author:
Oybek Xolmuminov
"""

from core.algorithms.metadata import MetadataExtractionAlgorithm
from core.algorithms.semantic import SemanticHarmonizationAlgorithm
from core.algorithms.mapping import AdaptiveAttributeMappingAlgorithm
from core.algorithms.harmonization import UnitHarmonizationAlgorithm
from core.algorithms.quality import DataQualityAssessmentAlgorithm
from core.algorithms.conflict import ConflictResolutionAlgorithm
from core.algorithms.fusion import WeightedDataFusionAlgorithm
from core.algorithms.unified_model import UnifiedDataModelAlgorithm
from core.algorithms.dispatcher import AlgorithmDispatcher
from .result import InteroperabilityResult

class InteroperabilityOrchestrator:

    def __init__(self):

        self.dispatcher = AlgorithmDispatcher()

    def execute(self, workflow, context):

        unified = self.dispatcher.execute(

            workflow,

            context

        )

        context.raw_data = unified

        return unified
    
class InteroperabilityOrchestrator:
    """
    Executes the complete interoperability workflow.
    """

    def __init__(self):

        self.metadata_algorithm = MetadataExtractionAlgorithm()

        self.semantic_algorithm = SemanticHarmonizationAlgorithm()

        self.mapping_algorithm = AdaptiveAttributeMappingAlgorithm()

        self.unit_algorithm = UnitHarmonizationAlgorithm()

        self.quality_algorithm = DataQualityAssessmentAlgorithm()

        self.conflict_algorithm = ConflictResolutionAlgorithm()

        self.fusion_algorithm = WeightedDataFusionAlgorithm()

        self.unified_algorithm = UnifiedDataModelAlgorithm()

    # ------------------------------------------------

    def execute(
        self,
        source_system: str,
        raw_data: list,
        reference_attributes: list,
    ) -> InteroperabilityResult:

        result = InteroperabilityResult(
            success=True,
            source_system=source_system
        )

        try:

            metadata = self.metadata_algorithm.execute(raw_data)

            semantic = self.semantic_algorithm.execute(metadata)

            mapped = self.mapping_algorithm.execute(
                semantic,
                reference_attributes
            )

            normalized = self.unit_algorithm.execute(mapped)

            quality = self.quality_algorithm.execute(normalized)

            resolved = self.conflict_algorithm.execute(quality)

            fused = self.fusion_algorithm.execute(resolved)

            unified = self.unified_algorithm.execute(fused)

            result.unified_data = unified

            result.processed_records = len(unified)

            return result

        except Exception as exc:

            result.add_error(str(exc))

            return result
