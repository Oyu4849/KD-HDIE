"""
KD-HDIE Framework

Knowledge Ontology
Final v2.1

Purpose
-------
Semantic ontology for heterogeneous environmental
data interoperability.

Version
-------
2.1

Changes in v2.1
----------------
• Added Open-Meteo historical daily aliases
• Added temporal TIME alias
• Preserved existing canonical concepts
• Preserved existing ontology domains
• Maintained backward compatibility

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ==========================================================
# Ontology Domain
# ==========================================================

class OntologyDomain(Enum):

    TEMPORAL = "Temporal"

    CLIMATE = "Climate"

    VEGETATION = "Vegetation"

    WATER = "Water"

    SOIL = "Soil"

    QUALITY = "ObservationQuality"


# ==========================================================
# Attribute Concept
# ==========================================================

@dataclass(slots=True)
class AttributeConcept:
    """
    Canonical semantic description of an attribute.
    """

    canonical_name: str

    domain: OntologyDomain

    data_type: type

    unit: str

    description: str

    synonyms: set[str] = field(default_factory=set)

    # ------------------------------------------------------
    # Semantic Matching
    # ------------------------------------------------------

    def matches(
        self,
        attribute: str,
    ) -> bool:

        value = attribute.upper().strip()

        return (

            value == self.canonical_name.upper()

            or

            value in {
                synonym.upper().strip()
                for synonym in self.synonyms
            }

        )


# ==========================================================
# Ontology
# ==========================================================

class KnowledgeOntology:
    """
    Semantic ontology used by the KD-HDIE Framework.
    """

    def __init__(self):

        self._concepts: dict[
            str,
            AttributeConcept,
        ] = {}

        self._load_default_concepts()

    # ======================================================
    # Registration
    # ======================================================

    def register(
        self,
        concept: AttributeConcept,
    ) -> None:

        self._concepts[
            concept.canonical_name.upper()
        ] = concept

    # ======================================================
    # Lookup
    # ======================================================

    def resolve(
        self,
        attribute: str,
    ) -> AttributeConcept | None:
        """
        Resolve heterogeneous attribute name
        into a canonical ontology concept.
        """

        if not attribute:

            return None

        attribute = attribute.upper().strip()

        for concept in self._concepts.values():

            if concept.matches(attribute):

                return concept

        return None

    # ======================================================
    # Default Ontology
    # ======================================================

    def _load_default_concepts(self):

        concepts = [

            # ==================================================
            # TEMPORAL
            # ==================================================

            AttributeConcept(

                canonical_name="timestamp",

                domain=OntologyDomain.TEMPORAL,

                data_type=str,

                unit="",

                description="Observation date or timestamp",

                synonyms={

                    "DATE",

                    "TIME",

                    "TIMESTAMP",

                    "DATETIME",

                    "OBSERVATION_DATE",

                },

            ),

            # ==================================================
            # CLIMATE - TEMPERATURE
            # ==================================================

            AttributeConcept(

                canonical_name="temperature",

                domain=OntologyDomain.CLIMATE,

                data_type=float,

                unit="°C",

                description="Air temperature",

                synonyms={

                    # NASA POWER
                    "T2M",

                    # Open-Meteo current
                    "TEMPERATURE_2M",

                    # Open-Meteo historical daily
                    "TEMPERATURE_2M_MEAN",

                    # Generic aliases
                    "TEMP_C",

                    "TEMP",

                    "AIR_TEMPERATURE",

                    "AIR_TEMP",

                },

            ),

            # ==================================================
            # CLIMATE - PRECIPITATION
            # ==================================================

            AttributeConcept(

                canonical_name="precipitation",

                domain=OntologyDomain.CLIMATE,

                data_type=float,

                unit="mm",

                description="Precipitation amount",

                synonyms={

                    # NASA POWER
                    "PRECTOTCORR",

                    # Open-Meteo current
                    "PRECIPITATION",

                    # Open-Meteo historical daily
                    "PRECIPITATION_SUM",

                    # Generic aliases
                    "PRECIP_MM",

                    "RAIN",

                    "RAINFALL",

                },

            ),

            # ==================================================
            # CLIMATE - WIND SPEED
            # ==================================================

            AttributeConcept(

                canonical_name="wind_speed",

                domain=OntologyDomain.CLIMATE,

                data_type=float,

                unit="m/s",

                description="Wind speed",

                synonyms={

                    # NASA POWER
                    "WS2M",

                    # Open-Meteo current
                    "WIND_SPEED_10M",

                    # Open-Meteo historical daily
                    "WIND_SPEED_10M_MEAN",

                    # Generic aliases
                    "WIND_MS",

                    "WIND_SPEED",

                },

            ),

            # ==================================================
            # CLIMATE - RELATIVE HUMIDITY
            # ==================================================

            AttributeConcept(

                canonical_name="relative_humidity",

                domain=OntologyDomain.CLIMATE,

                data_type=float,

                unit="%",

                description="Relative humidity",

                synonyms={

                    "RH2M",

                    "RELATIVE_HUMIDITY",

                    "RELATIVE_HUMIDITY_2M",

                },

            ),

            # ==================================================
            # SOIL
            # ==================================================

            AttributeConcept(

                canonical_name="soil_moisture",

                domain=OntologyDomain.SOIL,

                data_type=float,

                unit="m³/m³",

                description="Soil moisture",

                synonyms={

                    "SOIL_MOISTURE",

                    "SOIL_MOISTURE_0_TO_1CM",

                    "SOIL_MOISTURE_0_1CM",

                },

            ),

            # ==================================================
            # VEGETATION - NDVI
            # ==================================================

            AttributeConcept(

                canonical_name="ndvi",

                domain=OntologyDomain.VEGETATION,

                data_type=float,

                unit="ratio",

                description=(
                    "Normalized Difference "
                    "Vegetation Index"
                ),

                synonyms={

                    "NDVI",

                    "NORMALIZED_DIFFERENCE_VEGETATION_INDEX",

                },

            ),

            # ==================================================
            # VEGETATION - MSAVI
            # ==================================================

            AttributeConcept(

                canonical_name="msavi",

                domain=OntologyDomain.VEGETATION,

                data_type=float,

                unit="ratio",

                description=(
                    "Modified Soil Adjusted "
                    "Vegetation Index"
                ),

                synonyms={

                    "MSAVI",

                    "MODIFIED_SOIL_ADJUSTED_VEGETATION_INDEX",

                },

            ),

            # ==================================================
            # WATER - MNDWI
            # ==================================================

            AttributeConcept(

                canonical_name="mndwi",

                domain=OntologyDomain.WATER,

                data_type=float,

                unit="ratio",

                description=(
                    "Modified Normalized "
                    "Difference Water Index"
                ),

                synonyms={

                    "MNDWI",

                    "MODIFIED_NORMALIZED_DIFFERENCE_WATER_INDEX",

                },

            ),

            # ==================================================
            # SOIL - BSI
            # ==================================================

            AttributeConcept(

                canonical_name="bsi",

                domain=OntologyDomain.SOIL,

                data_type=float,

                unit="ratio",

                description="Bare Soil Index",

                synonyms={

                    "BSI",

                    "BARE_SOIL_INDEX",

                },

            ),

            # ==================================================
            # WATER - SURFACE WATER AREA
            # ==================================================

            AttributeConcept(

                canonical_name="surface_water_area",

                domain=OntologyDomain.WATER,

                data_type=float,

                unit="km²",

                description="Surface water area",

                synonyms={

                    "S2_WATER_AREA_KM2",

                    "JRC_WATER_AREA_KM2",

                    "SURFACE_WATER_AREA",

                    "WATER_AREA",

                },

            ),

            # ==================================================
            # QUALITY - SENTINEL SCENE COUNT
            # ==================================================

            AttributeConcept(

                canonical_name="scene_count",

                domain=OntologyDomain.QUALITY,

                data_type=int,

                unit="count",

                description="Number of valid scenes",

                synonyms={

                    "S2_SCENE_COUNT",

                    "SCENE_COUNT",

                },

            ),

            # ==================================================
            # QUALITY - VALID PIXEL COUNT
            # ==================================================

            AttributeConcept(

                canonical_name="valid_pixel_count",

                domain=OntologyDomain.QUALITY,

                data_type=int,

                unit="pixels",

                description="Valid pixels",

                synonyms={

                    "S2_VALID_PIXEL_COUNT",

                    "VALID_PIXEL_COUNT",

                },

            ),

            # ==================================================
            # QUALITY - ERA5 IMAGE COUNT
            # ==================================================

            AttributeConcept(

                canonical_name="era5_image_count",

                domain=OntologyDomain.QUALITY,

                data_type=int,

                unit="count",

                description="ERA5 image count",

                synonyms={

                    "ERA5_IMAGE_COUNT",

                },

            ),

            # ==================================================
            # QUALITY - JRC IMAGE COUNT
            # ==================================================

            AttributeConcept(

                canonical_name="jrc_image_count",

                domain=OntologyDomain.QUALITY,

                data_type=int,

                unit="count",

                description="JRC image count",

                synonyms={

                    "JRC_IMAGE_COUNT",

                },

            ),

        ]

        # ------------------------------------------------------
        # Register all concepts
        # ------------------------------------------------------

        for concept in concepts:

            self.register(concept)


# ==========================================================
# Global Ontology
# ==========================================================

ontology = KnowledgeOntology()
