"""
KD-HDIE Framework

Framework Lifecycle Manager

Author:
Oybek Xolmuminov
"""

from enum import Enum


class LifecycleState(Enum):

    CREATED = "CREATED"

    INITIALIZED = "INITIALIZED"

    VALIDATING = "VALIDATING"

    DISCOVERING = "DISCOVERING"

    NEGOTIATING = "NEGOTIATING"

    TRANSFORMING = "TRANSFORMING"

    PROCESSING = "PROCESSING"

    EXCHANGING = "EXCHANGING"

    FINISHED = "FINISHED"

    FAILED = "FAILED"


class LifecycleManager:

    def __init__(self):

        self.state = LifecycleState.CREATED

    def change(self, state):

        self.state = state

    def current(self):

        return self.state
