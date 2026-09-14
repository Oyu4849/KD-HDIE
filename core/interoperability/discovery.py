"""
KD-HDIE Framework

Interoperability Discovery

Purpose:
Discover capabilities of heterogeneous software systems.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class SystemCapability:

    protocol: str

    data_format: str

    authentication: str | None = None

    version: str | None = None

    endpoints: List[str] = field(default_factory=list)


class InteroperabilityDiscovery:

    """
    Discovers technical capabilities of external systems.
    """

    def discover(self, connector):

        capability = SystemCapability(

            protocol=connector.protocol,

            data_format=connector.data_format,

            authentication=getattr(
                connector,
                "authentication",
                None
            ),

            version=getattr(
                connector,
                "version",
                None
            ),

            endpoints=getattr(
                connector,
                "available_endpoints",
                []
            )

        )

        return capability
