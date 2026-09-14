"""
KD-HDIE Framework

Knowledge Repository (Final v2.0)

Purpose
-------
Central semantic repository for heterogeneous
environmental data interoperability.

Responsibilities
----------------
• Ontology access
• Canonical attribute resolution
• Semantic search
• Domain-based lookup
• Adapter support
• Reasoner support

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from typing import Iterable

from core.knowledge.ontology import (
    AttributeConcept,
    KnowledgeOntology,
    OntologyDomain,
    ontology,
)


class KnowledgeRepository:
    """
    Central semantic repository.
    """

    def __init__(
        self,
        ontology_instance: KnowledgeOntology = ontology,
    ):

        self._ontology = ontology_instance

    # ======================================================
    # Canonical Resolution
    # ======================================================

    def resolve(
        self,
        attribute: str,
    ) -> AttributeConcept | None:
        """
        Resolve any heterogeneous attribute into
        canonical ontology concept.
        """

        return self._ontology.resolve(attribute)

    # ======================================================
    # Canonical Name
    # ======================================================

    def canonical_name(
        self,
        attribute: str,
    ) -> str | None:

        concept = self.resolve(attribute)

        if concept is None:
            return None

        return concept.canonical_name

    # ======================================================
    # Domain
    # ======================================================

    def domain(
        self,
        attribute: str,
    ) -> OntologyDomain | None:

        concept = self.resolve(attribute)

        if concept is None:
            return None

        return concept.domain

    # ======================================================
    # Unit
    # ======================================================

    def unit(
        self,
        attribute: str,
    ) -> str | None:

        concept = self.resolve(attribute)

        if concept is None:
            return None

        return concept.unit

    # ======================================================
    # Data Type
    # ======================================================

    def data_type(
        self,
        attribute: str,
    ) -> type | None:

        concept = self.resolve(attribute)

        if concept is None:
            return None

        return concept.data_type

    # ======================================================
    # Description
    # ======================================================

    def description(
        self,
        attribute: str,
    ) -> str | None:

        concept = self.resolve(attribute)

        if concept is None:
            return None

        return concept.description

    # ======================================================
    # Synonyms
    # ======================================================

    def synonyms(
        self,
        attribute: str,
    ) -> set[str]:

        concept = self.resolve(attribute)

        if concept is None:
            return set()

        return set(concept.synonyms)

    # ======================================================
    # Validation
    # ======================================================

    def exists(
        self,
        attribute: str,
    ) -> bool:

        return self.resolve(attribute) is not None

    # ======================================================
    # Domain Search
    # ======================================================

    def concepts_by_domain(
        self,
        domain: OntologyDomain,
    ) -> list[AttributeConcept]:

        concepts = []

        for concept in self._ontology._concepts.values():

            if concept.domain == domain:

                concepts.append(concept)

        return concepts

    # ======================================================
    # All Concepts
    # ======================================================

    def concepts(self) -> Iterable[AttributeConcept]:

        return self._ontology._concepts.values()

    # ======================================================
    # Statistics
    # ======================================================

    def statistics(self) -> dict:

        domains = {}

        for concept in self.concepts():

            name = concept.domain.value

            domains[name] = domains.get(name, 0) + 1

        return {

            "concepts": len(list(self.concepts())),

            "domains": domains,

        }

    # ======================================================
    # Semantic Mapping
    # ======================================================

    def semantic_mapping(
        self,
        attributes: list[str],
    ) -> dict[str, str]:

        """
        Convert heterogeneous attribute names
        into canonical attribute names.
        """

        mapping = {}

        for attribute in attributes:

            canonical = self.canonical_name(attribute)

            if canonical:

                mapping[attribute] = canonical

            else:

                mapping[attribute] = attribute

        return mapping


# ==========================================================
# Global Repository
# ==========================================================

knowledge_repository = KnowledgeRepository()
