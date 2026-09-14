"""
KD-HDIE Framework

Attribute Repository

Purpose
-------
Repository layer for accessing the heterogeneous
attribute knowledge base.

Responsibilities
----------------
* Canonical attribute lookup
* Alias lookup
* Category lookup
* Similarity search
* Metadata retrieval

Author:
Oybek Xolmuminov
"""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import Optional

from django.db.models import Q

from .models import (
    CanonicalAttribute,
    AttributeAlias,
    AttributeCategory,
    MeasurementUnit,
)


class AttributeRepository:
    """
    Repository for the Attribute Knowledge Repository.
    """

    # ======================================================
    # Canonical Attribute
    # ======================================================

    def find_by_name(
        self,
        name: str
    ) -> Optional[CanonicalAttribute]:

        if not name:
            return None

        return (
            CanonicalAttribute.objects
            .filter(name__iexact=name.strip())
            .first()
        )

    # ======================================================
    # Alias Search
    # ======================================================

    def find_by_alias(
        self,
        alias: str
    ) -> Optional[CanonicalAttribute]:

        if not alias:
            return None

        obj = (
            AttributeAlias.objects
            .select_related("attribute")
            .filter(alias__iexact=alias.strip())
            .order_by("-confidence", "-priority")
            .first()
        )

        return obj.attribute if obj else None

    # ======================================================
    # Combined Search
    # ======================================================

    def resolve(
        self,
        attribute_name: str
    ) -> Optional[CanonicalAttribute]:
        """
        Exact name search,
        then alias search.
        """

        attribute = self.find_by_name(attribute_name)

        if attribute:
            return attribute

        return self.find_by_alias(attribute_name)

    # ======================================================
    # Category
    # ======================================================

    def find_category(
        self,
        code: str
    ) -> Optional[AttributeCategory]:

        if not code:
            return None

        return (
            AttributeCategory.objects
            .filter(code__iexact=code)
            .first()
        )

    # ======================================================
    # Units
    # ======================================================

    def find_unit(
        self,
        symbol: str
    ) -> Optional[MeasurementUnit]:

        if not symbol:
            return None

        return (
            MeasurementUnit.objects
            .filter(symbol__iexact=symbol)
            .first()
        )

    # ======================================================
    # Attribute List
    # ======================================================

    def all_attributes(self):

        return (
            CanonicalAttribute.objects
            .filter(is_active=True)
            .select_related(
                "category",
                "default_unit"
            )
        )

    # ======================================================
    # Similarity Search
    # ======================================================

    def find_similar(
        self,
        attribute_name: str,
        threshold: float = 0.75
    ):
        """
        Finds the most similar canonical attribute.
        """

        if not attribute_name:
            return None

        attribute_name = attribute_name.lower()

        best_match = None
        best_score = 0.0

        for attribute in self.all_attributes():

            score = SequenceMatcher(

                None,

                attribute_name,

                attribute.name.lower()

            ).ratio()

            if score > best_score:

                best_match = attribute
                best_score = score

        if best_score >= threshold:

            return {

                "attribute": best_match,

                "score": round(best_score, 3)

            }

        return None

    # ======================================================
    # Alias Similarity
    # ======================================================

    def find_similar_alias(
        self,
        alias: str,
        threshold: float = 0.75
    ):

        if not alias:
            return None

        alias = alias.lower()

        best = None
        score = 0.0

        aliases = AttributeAlias.objects.select_related(
            "attribute"
        )

        for item in aliases:

            ratio = SequenceMatcher(

                None,

                alias,

                item.alias.lower()

            ).ratio()

            if ratio > score:

                score = ratio
                best = item

        if best and score >= threshold:

            return {

                "attribute": best.attribute,

                "score": round(score, 3),

                "alias": best.alias

            }

        return None

    # ======================================================
    # Generic Resolution
    # ======================================================

    def resolve_attribute(
        self,
        attribute_name: str
    ):
        """
        Scientific attribute resolution.

        Search order

        1. Exact canonical name
        2. Exact alias
        3. Similar canonical
        4. Similar alias
        """

        attribute = self.find_by_name(attribute_name)

        if attribute:

            return {

                "attribute": attribute,

                "confidence": 1.0,

                "method": "EXACT"

            }

        attribute = self.find_by_alias(attribute_name)

        if attribute:

            return {

                "attribute": attribute,

                "confidence": 0.98,

                "method": "ALIAS"

            }

        similar = self.find_similar(attribute_name)

        if similar:

            return {

                "attribute": similar["attribute"],

                "confidence": similar["score"],

                "method": "SIMILAR_NAME"

            }

        similar = self.find_similar_alias(attribute_name)

        if similar:

            return {

                "attribute": similar["attribute"],

                "confidence": similar["score"],

                "method": "SIMILAR_ALIAS"

            }

        return None

    # ======================================================
    # Search
    # ======================================================

    def search(
        self,
        keyword: str
    ):

        return CanonicalAttribute.objects.filter(

            Q(name__icontains=keyword)

            |

            Q(description__icontains=keyword)

        ).distinct()
