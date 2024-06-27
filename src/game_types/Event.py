from . import EventType

class GameEvent:
    def __init__(self, event : EventType, *args, **kwargs) -> None:
        self.event = event
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f"GameEvent<id={id(self)}, event={self.event}>"