"""
KD-HDIE Framework

Knowledge Reasoner (Final v2.0)

Purpose
-------
Semantic reasoning engine responsible for
attribute resolution, semantic interoperability,
and rule-based inference.

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.knowledge.repository import (
    KnowledgeRepository,
    knowledge_repository,
)

from core.knowledge.rules import (
    RuleRepository,
    RuleType,
    knowledge_rules,
)

from core.knowledge.ontology import (
    AttributeConcept,
)


# ==========================================================
# Semantic Match
# ==========================================================

@dataclass(slots=True)
class SemanticMatch:
    """
    Result of semantic reasoning.
    """

    source_attribute: str

    canonical_name: str | None

    concept: AttributeConcept | None

    confidence: float

    matched_rule: str | None

    success: bool


# ==========================================================
# Knowledge Reasoner
# ==========================================================

class KnowledgeReasoner:
    """
    Rule-based semantic reasoner.
    """

    def __init__(
        self,
        repository: KnowledgeRepository = knowledge_repository,
        rules: RuleRepository = knowledge_rules,
    ):

        self._repository = repository

        self._rules = rules

    # ======================================================
    # Resolve
    # ======================================================

    def resolve(
        self,
        attribute: str,
    ) -> SemanticMatch:

        concept = self._repository.resolve(attribute)

        if concept is None:

            return SemanticMatch(

                source_attribute=attribute,

                canonical_name=None,

                concept=None,

                confidence=0.0,

                matched_rule=None,

                success=False,

            )

        rule = self._rules.find(attribute)

        return SemanticMatch(

            source_attribute=attribute,

            canonical_name=concept.canonical_name,

            concept=concept,

            confidence=1.0,

            matched_rule=None if rule is None else rule.name,

            success=True,

        )

    # ======================================================
    # Canonical Name
    # ======================================================

    def infer_attribute(
        self,
        attribute: str,
    ) -> str:

        match = self.resolve(attribute)

        if not match.success:

            return attribute

        return match.canonical_name

    # ======================================================
    # Validate
    # ======================================================

    def validate(
        self,
        attribute: str,
    ) -> bool:

        return self._repository.exists(attribute)

    # ======================================================
    # Unit
    # ======================================================

    def infer_unit(
        self,
        attribute: str,
    ) -> str | None:

        return self._repository.unit(attribute)

    # ======================================================
    # Data Type
    # ======================================================

    def infer_type(
        self,
        attribute: str,
    ) -> type | None:

        return self._repository.data_type(attribute)

    # ======================================================
    # Domain
    # ======================================================

    def infer_domain(
        self,
        attribute: str,
    ):

        return self._repository.domain(attribute)

    # ======================================================
    # Semantic Mapping
    # ======================================================

    def semantic_mapping(
        self,
        attributes: list[str],
    ) -> dict[str, str]:

        mapping = {}

        for attribute in attributes:

            mapping[attribute] = self.infer_attribute(
                attribute
            )

        return mapping

    # ======================================================
    # Compatibility
    # ======================================================

    def compatible(
        self,
        left: str,
        right: str,
    ) -> bool:

        left_domain = self.infer_domain(left)

        right_domain = self.infer_domain(right)

        return left_domain == right_domain

    # ======================================================
    # Statistics
    # ======================================================

    def statistics(
        self,
        attributes: list[str],
    ) -> dict[str, Any]:

        resolved = 0

        unresolved = 0

        for attribute in attributes:

            if self.validate(attribute):

                resolved += 1

            else:

                unresolved += 1

        return {

            "attributes": len(attributes),

            "resolved": resolved,

            "unresolved": unresolved,

            "coverage":

                resolved / len(attributes)

                if attributes

                else 0.0,

        }


# ==========================================================
# Global Reasoner
# ==========================================================

knowledge_reasoner = KnowledgeReasoner()
