from typing import Literal

class Cell:
    def __init__(self):
        self.objects = dict()

    def __repr__(self) -> str:
        return f"Cell<id={id(self)}, objects={self.objects!r}>"

    def add_obj(self, obj) -> None:
        print(self.objects, id(obj))
        if str(id(obj)) in self.objects:
            raise RuntimeError(f"object {obj} already added in cell")
        self.objects[str(id(obj))] = obj
        obj.cell_subscribe(self)

    def del_obj(self, obj) -> None:
        print(self.objects, id(obj))
        if str(id(obj)) not in self.objects:
            raise RuntimeError(f"object {obj} already deleted from cell")
        self.objects.pop(str(id(obj)))
        obj.cell_unsubscribe(self)

    def update(self, obj, signal : Literal["DEL", "ADD"], *args, **kwargs):
        match signal:
            case "DEL":
                self.del_obj(obj)
            case "ADD":
                self.add_obj(obj)


    def obj_on_cell(self, obj):
        return obj in self.objects

    def can_stay_here(self):
        return all(obj.passability for obj in self.objects)

    def passable(self) -> bool:
        print("objs: ", self.objects)
        return all(obj.passability for obj in self.objects.values())