from ..game_types import EventType

class GameEvent:
    def __init__(self, event : EventType, *args, **kwargs) -> None:
        self.event = event
        self.args = args
        self.kwargs = kwargs
