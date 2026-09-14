"""
KD-HDIE Framework

Knowledge Rules (Final v2.0)

Purpose
-------
Semantic rules used by the Knowledge Reasoner
to organize interoperability between heterogeneous
software systems.

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ==========================================================
# Rule Type
# ==========================================================

class RuleType(Enum):

    SYNONYM = "Synonym"

    DATATYPE = "DataType"

    UNIT = "Unit"

    DOMAIN = "Domain"

    REQUIRED = "Required"

    COMPATIBILITY = "Compatibility"


# ==========================================================
# Semantic Rule
# ==========================================================

@dataclass(slots=True)
class SemanticRule:

    name: str

    rule_type: RuleType

    source: str

    target: str

    enabled: bool = True

    priority: int = 100

    description: str = ""

# ==========================================================
# Rule Repository
# ==========================================================

class RuleRepository:
    """
    Repository of semantic rules.
    """

    def __init__(self):

        self._rules: list[SemanticRule] = []

    # ------------------------------------------------------

    def register(
        self,
        rule: SemanticRule,
    ) -> None:

        self._rules.append(rule)

    # ------------------------------------------------------

    def find(
        self,
        source: str,
    ) -> SemanticRule | None:

        source = source.lower()

        for rule in self._rules:

            if rule.source.lower() == source:

                return rule

        return None

    # ------------------------------------------------------

    def all(self) -> list[SemanticRule]:

        return list(self._rules)


# ==========================================================
# Global Repository
# ==========================================================

knowledge_rules = RuleRepository()
