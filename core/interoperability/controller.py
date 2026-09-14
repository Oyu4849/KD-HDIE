"""
KD-HDIE Framework

Interoperability Controller (Final v2.0)

Presentation Layer
"""

from __future__ import annotations

from core.interoperability.service import (

    InteroperabilityService,

)

from core.interoperability.result import (

    InteroperabilityResult,

)


class InteroperabilityController:

    def __init__(

        self,

        service=None,

    ):

        self.service = (

            service

            or

            InteroperabilityService()

        )

    # =====================================================
    # Execute
    # =====================================================

    def execute(

        self,

        source_system: str,

        target_system: str,

        connection_parameters: dict,

        operation="INTEROPERABILITY",

        workflow="DEFAULT",

    ) -> InteroperabilityResult:

        return self.service.execute(

            source_system=source_system,

            target_system=target_system,

            connection_parameters=

                connection_parameters,

            operation=operation,

            workflow_name=workflow,

        )

    # =====================================================
    # Health
    # =====================================================

    def health(self):

        return {

            "framework": "KD-HDIE",

            "status": "READY",

            "version": "2.0",

        }
