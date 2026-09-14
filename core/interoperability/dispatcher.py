"""
KD-HDIE Framework

Algorithm Dispatcher

Purpose:
Dynamically executes interoperability algorithms
according to the configured workflow.

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


class AlgorithmDispatcher:

    """
    Executes interoperability algorithms
    dynamically.
    """

    def __init__(self):

        self.algorithms = {

            "metadata":
                MetadataExtractionAlgorithm(),

            "semantic":
                SemanticHarmonizationAlgorithm(),

            "mapping":
                AdaptiveAttributeMappingAlgorithm(),

            "harmonization":
                UnitHarmonizationAlgorithm(),

            "quality":
                DataQualityAssessmentAlgorithm(),

            "conflict":
                ConflictResolutionAlgorithm(),

            "fusion":
                WeightedDataFusionAlgorithm(),

            "unified_model":
                UnifiedDataModelAlgorithm()

        }

    # -------------------------------------------------

    def execute(

        self,

        workflow,

        context

    ):

        data = context.raw_data

        for step in workflow.get_steps():

            algorithm = self.algorithms.get(

                step.name

            )

            if algorithm is None:

                continue

            context.algorithm(step.name)

            context.log(
                f"Executing {step.name}"
            )

            data = algorithm.execute(
                data=data,
                context=context
            )

        return data

    # -------------------------------------------------

    def register(

        self,

        name,

        algorithm

    ):

        self.algorithms[name] = algorithm

    # -------------------------------------------------

    def unregister(

        self,

        name

    ):

        self.algorithms.pop(name, None)
