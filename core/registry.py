"""
KD-HDIE Framework

Central Registry (Final v2.0)

Purpose
-------
Central registry responsible for managing all
framework components.

Responsibilities
----------------
• Algorithm Registry
• Adapter Registry
• Workflow Registry

Dissertation
------------
Chapter 3
Framework Core

Author
------
Oybek Xolmuminov
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Generic, TypeVar

from core.algorithms.base import BaseAlgorithm
from core.adapters.base_adapter import BaseAdapter
from core.interoperability.workflow import Workflow


T = TypeVar("T")


# ==========================================================
# Registry Item
# ==========================================================

@dataclass(slots=True)
class RegistryItem(Generic[T]):
    """
    Registry entry.
    """

    name: str

    instance: T

    enabled: bool = True

    description: str = ""


# ==========================================================
# Registry
# ==========================================================

class Registry:
    """
    Central registry of KD-HDIE Framework.
    """

    def __init__(self):

        self._algorithms: Dict[str, RegistryItem[BaseAlgorithm]] = {}

        self._adapters: Dict[str, RegistryItem[BaseAdapter]] = {}

        self._workflows: Dict[str, RegistryItem[Workflow]] = {}

    # ======================================================
    # Internal
    # ======================================================

    @staticmethod
    def _normalize(name: str) -> str:

        return name.strip().upper()

    # ======================================================
    # Algorithms
    # ======================================================

    def register_algorithm(

        self,

        algorithm: BaseAlgorithm,

        description: str = "",

    ) -> None:

        key = self._normalize(algorithm.name)

        self._algorithms[key] = RegistryItem(

            name=algorithm.name,

            instance=algorithm,

            description=description,

        )

    # ------------------------------------------------------

    def algorithm(

        self,

        name: str,

    ) -> BaseAlgorithm:

        key = self._normalize(name)

        if key not in self._algorithms:

            raise KeyError(

                f"Algorithm '{name}' is not registered."

            )

        return self._algorithms[key].instance

    # ------------------------------------------------------

    def algorithms(self) -> list[BaseAlgorithm]:

        return [

            item.instance

            for item in self._algorithms.values()

            if item.enabled

        ]

    # ======================================================
    # Adapters
    # ======================================================

    def register_adapter(

        self,

        source_type: str,

        adapter: BaseAdapter,

        description: str = "",

    ) -> None:

        key = self._normalize(source_type)

        self._adapters[key] = RegistryItem(

            name=source_type,

            instance=adapter,

            description=description,

        )

    # ------------------------------------------------------

    def adapter(

        self,

        source_type: str,

    ) -> BaseAdapter:

        key = self._normalize(source_type)

        if key not in self._adapters:

            raise KeyError(

                f"Adapter '{source_type}' "

                "is not registered."

            )

        return self._adapters[key].instance

    # ------------------------------------------------------

    def adapters(self):

        return {

            key: item.instance

            for key, item

            in self._adapters.items()

            if item.enabled

        }

    # ======================================================
    # Workflows
    # ======================================================

    def register_workflow(

        self,

        workflow: Workflow,

    ) -> None:

        key = self._normalize(

            workflow.name

        )

        self._workflows[key] = RegistryItem(

            name=workflow.name,

            instance=workflow,

        )

    # ------------------------------------------------------

    def workflow(

        self,

        name: str,

    ) -> Workflow:

        key = self._normalize(name)

        if key not in self._workflows:

            raise KeyError(

                f"Workflow '{name}' "

                "is not registered."

            )

        return self._workflows[key].instance

    # ------------------------------------------------------

    def workflows(self):

        return [

            item.instance

            for item

            in self._workflows.values()

            if item.enabled

        ]

    # ======================================================
    # Enable / Disable
    # ======================================================

    def enable(self, name: str):

        key = self._normalize(name)

        for collection in (

            self._algorithms,

            self._adapters,

            self._workflows,

        ):

            if key in collection:

                collection[key].enabled = True

                return

        raise KeyError(name)

    # ------------------------------------------------------

    def disable(self, name: str):

        key = self._normalize(name)

        for collection in (

            self._algorithms,

            self._adapters,

            self._workflows,

        ):

            if key in collection:

                collection[key].enabled = False

                return

        raise KeyError(name)

    # ======================================================
    # Statistics
    # ======================================================

    def statistics(self):

        return {

            "algorithms": len(self._algorithms),

            "adapters": len(self._adapters),

            "workflows": len(self._workflows),

            "total": (

                len(self._algorithms)

                + len(self._adapters)

                + len(self._workflows)

            ),

        }

    # ======================================================
    # Bootstrap
    # ======================================================

    def bootstrap(

        self,

        algorithms: Iterable[BaseAlgorithm] = (),
        
        adapters: Iterable[tuple[str, BaseAdapter]] = (),

        workflows: Iterable[Workflow] = (),

    ):

        for algorithm in algorithms:

            self.register_algorithm(

                algorithm

            )

        for source, adapter in adapters:

            self.register_adapter(

                source,

                adapter,

            )

        for workflow in workflows:

            self.register_workflow(

                workflow

            )

    # ======================================================
    # Reset
    # ======================================================

    def clear(self):

        self._algorithms.clear()

        self._adapters.clear()

        self._workflows.clear()


# ==========================================================
# Global Registry
# ==========================================================

registry = Registry()
