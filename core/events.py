from dataclasses import dataclass
from datetime import datetime


@dataclass
class FrameworkEvent:

    name: str

    timestamp: datetime

    payload: dict


class EventBus:

    def __init__(self):

        self.events = []

    def publish(

        self,

        name,

        **payload

    ):

        self.events.append(

            FrameworkEvent(

                name=name,

                timestamp=datetime.utcnow(),

                payload=payload

            )

        )

    def history(self):

        return self.events
