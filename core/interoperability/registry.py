"""
KD-HDIE Framework v1.0

Algorithm Registry

Purpose:
Central registry for all scientific algorithms.

Every new algorithm must be registered here.

Author:
Oybek Xolmuminov
"""

from algorithms.metadata import MetadataExtractionAlgorithm
from algorithms.semantic import SemanticHarmonizationAlgorithm
from algorithms.mapping import AdaptiveAttributeMappingAlgorithm
from algorithms.harmonization import UnitHarmonizationAlgorithm
from algorithms.quality import DataQualityAssessmentAlgorithm
from algorithms.conflict import ConflictResolutionAlgorithm
from algorithms.fusion import WeightedDataFusionAlgorithm
from algorithms.unified_model import UnifiedDataModelAlgorithm


class AlgorithmRegistry:
    """
    Central registry of KD-HDIE algorithms.
    """

    _registry = {}

    @classmethod
    def register(cls, name, algorithm):
        """
        Register new algorithm.
        """

        cls._registry[name] = algorithm

    @classmethod
    def get(cls, name):
        """
        Return registered algorithm.
        """

        if name not in cls._registry:

            raise KeyError(
                f"Algorithm '{name}' is not registered."
            )

        return cls._registry[name]

    @classmethod
    def exists(cls, name):

        return name in cls._registry

    @classmethod
    def unregister(cls, name):

        if name in cls._registry:

            del cls._registry[name]

    @classmethod
    def all(cls):

        return cls._registry

    @classmethod
    def names(cls):

        return list(cls._registry.keys())


# -------------------------------------------------------
# Default KD-HDIE Algorithms
# -------------------------------------------------------

AlgorithmRegistry.register(
    "metadata",
    MetadataExtractionAlgorithm,
)

AlgorithmRegistry.register(
    "semantic",
    SemanticHarmonizationAlgorithm,
)

AlgorithmRegistry.register(
    "mapping",
    AdaptiveAttributeMappingAlgorithm,
)

AlgorithmRegistry.register(
    "harmonization",
    UnitHarmonizationAlgorithm,
)

AlgorithmRegistry.register(
    "quality",
    DataQualityAssessmentAlgorithm,
)

AlgorithmRegistry.register(
    "conflict",
    ConflictResolutionAlgorithm,
)

AlgorithmRegistry.register(
    "fusion",
    WeightedDataFusionAlgorithm,
)

AlgorithmRegistry.register(
    "unified_model",
    UnifiedDataModelAlgorithm,
)
