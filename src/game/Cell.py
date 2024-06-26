from typing import Literal

class Cell:
    def __init__(self):
        self.objects = dict()

    def __repr__(self) -> str:
        return f"Cell<id={id(self)}, objects={self.objects!r}>"

    def add_obj(self, obj) -> None:
        assert obj not in self.objects, RuntimeError(f"object {obj} already added in cell")
        self.objects[id(obj)] = obj
        obj.subscribe(self)

    def update(self, obj, signal : Literal["DEL", "ADD"], *args, **kwargs):
        match signal:
            case "DEL":
                self.objects.pop(id(obj))
            case "ADD":
                self.add_obj(obj)


    def obj_on_cell(self, obj):
        return obj in self.objects

    def can_stay_here(self):
        return all(obj.passability for obj in self.objects)