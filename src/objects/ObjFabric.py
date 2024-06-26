from . import GameObject
from .Attacker import Attacker
from .Wall import Wall
from .Defender import Defender

class ObjFabric:
    @staticmethod
    def create_from_symbol(symbol : str) -> GameObject:
        match symbol:
            case "#":
                return Wall()
            case "@":
                return Attacker()
            case "&":
                return Defender()