from . import GameObject
from .Attacker import Attacker
from .Wall import Wall
from .Defender import Defender
from .Bush import Bush
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
            case _:
                return NotImplementedError("We does not recognise such symbol-object type")