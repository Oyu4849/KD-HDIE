"""
KD-HDIE Framework v1.0

Metadata Repository

Author:
Oybek Xolmuminov

Purpose:
Central repository for all standardized metadata
used by heterogeneous integration algorithms.
"""

from copy import deepcopy
from typing import Dict, List, Optional


class MetadataRepository:
    """
    Central metadata repository.

    Stores standardized metadata definitions
    used by all algorithms.
    """

    def __init__(self):

        self._metadata: Dict[str, Dict] = {}

    # --------------------------------------------------
    # CRUD Operations
    # --------------------------------------------------

    def register(self, metadata: Dict):
        """
        Register metadata definition.

        Required keys:
            semantic_name
            data_type
            unit
        """

        semantic_name = metadata.get("semantic_name")

        if not semantic_name:
            raise ValueError(
                "'semantic_name' is required."
            )

        self._metadata[
            semantic_name.lower()
        ] = deepcopy(metadata)

    # --------------------------------------------------

    def update(
        self,
        semantic_name: str,
        metadata: Dict
    ):

        key = semantic_name.lower()

        if key not in self._metadata:

            raise KeyError(
                f"{semantic_name} not found."
            )

        self._metadata[key].update(metadata)

    # --------------------------------------------------

    def remove(
        self,
        semantic_name: str
    ):

        self._metadata.pop(
            semantic_name.lower(),
            None
        )

    # --------------------------------------------------

    def exists(
        self,
        semantic_name: str
    ) -> bool:

        return (
            semantic_name.lower()
            in self._metadata
        )

    # --------------------------------------------------

    def get(
        self,
        semantic_name: str
    ) -> Optional[Dict]:

        metadata = self._metadata.get(
            semantic_name.lower()
        )

        if metadata is None:
            return None

        return deepcopy(metadata)

    # --------------------------------------------------

    def all(self) -> List[Dict]:

        return [

            deepcopy(item)

            for item in self._metadata.values()

        ]

    # --------------------------------------------------

    def names(self):

        return sorted(

            self._metadata.keys()

        )

    # --------------------------------------------------

    def count(self):

        return len(self._metadata)

    # --------------------------------------------------

    def clear(self):

        self._metadata.clear()

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search(
        self,
        keyword: str
    ) -> List[Dict]:

        keyword = keyword.lower()

        result = []

        for metadata in self._metadata.values():

            semantic = metadata.get(
                "semantic_name",
                ""
            ).lower()

            description = metadata.get(
                "description",
                ""
            ).lower()

            if (

                keyword in semantic

                or

                keyword in description

            ):

                result.append(
                    deepcopy(metadata)
                )

        return result

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def statistics(self):

        return {

            "total_attributes":
                self.count(),

            "attribute_names":
                self.names()

        }

    # --------------------------------------------------

    def __len__(self):

        return self.count()

    # --------------------------------------------------

    def __contains__(
        self,
        semantic_name
    ):

        return self.exists(
            semantic_name
        )

    # --------------------------------------------------

    def __repr__(self):

        return (

            f"<MetadataRepository "

            f"count={self.count()}>"

        )
