"""
KD-HDIE Framework

Interoperability Negotiation Engine

Purpose:
Negotiates interoperability capabilities
between heterogeneous software systems.

Dissertation:
Chapter 3
Interoperability Negotiation Algorithm

Author:
Oybek Xolmuminov
"""

from dataclasses import dataclass
from typing import List


SUPPORTED_PROTOCOLS = {

    "REST",

    "SOAP",

    "GRAPHQL",

    "DATABASE",

    "CSV",

    "JSON",

    "XML"

}


SUPPORTED_ENCODINGS = {

    "UTF-8",

    "UTF-16"

}


SUPPORTED_AUTH = {

    "NONE",

    "API_KEY",

    "BASIC",

    "BEARER",

    "OAUTH2"

}


@dataclass
class NegotiationResult:

    success: bool

    protocol: str | None = None

    encoding: str | None = None

    authentication: str | None = None

    messages: List[str] = None

    def __post_init__(self):

        if self.messages is None:

            self.messages = []


class InteroperabilityNegotiator:

    """
    Negotiates communication capabilities
    between two software systems.
    """

    def negotiate(

        self,

        source,

        target

    ) -> NegotiationResult:

        result = NegotiationResult(

            success=True

        )

        protocol = self._protocol(

            source.protocol,

            target.protocol

        )

        if protocol is None:

            result.success = False

            result.messages.append(

                "Protocol negotiation failed."

            )

            return result

        result.protocol = protocol

        encoding = self._encoding(

            source.encoding,

            target.encoding

        )

        result.encoding = encoding

        auth = self._authentication(

            source.authentication,

            target.authentication

        )

        result.authentication = auth

        result.messages.append(

            "Negotiation completed successfully."

        )

        return result

    # ------------------------------------------------

    def _protocol(

        self,

        source,

        target

    ):

        if source == target:

            return source

        if source in SUPPORTED_PROTOCOLS:

            return source

        return None

    # ------------------------------------------------

    def _encoding(

        self,

        source,

        target

    ):

        if source == target:

            return source

        return "UTF-8"

    # ------------------------------------------------

    def _authentication(

        self,

        source,

        target

    ):

        if source == target:

            return source

        if source == "NONE":

            return target

        return source
