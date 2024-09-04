from . import GameObject
from .Attacker import Attacker
from .Wall import Wall
from .Defender import Defender
from .Bush import Bush
from .Hero import Hero
from ..strategy.Brain import KeeperBrain

class ObjFabric:
    @staticmethod
    def create_from_symbol(symbol : str) -> GameObject:
        match symbol:
            case "#":
                return Wall()
            case "@":
                obj = Attacker()
                obj.set_brain(KeeperBrain())
                return obj
            case "&":
                return Defender()
            case "b":
                return Bush()
            case "h":
                return Hero()
            case _:
                return NotImplementedError("We does not recognise such symbol-object type")