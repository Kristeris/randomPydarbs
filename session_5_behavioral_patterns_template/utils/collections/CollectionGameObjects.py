from typing import List, Tuple

from models.GameObject import GameObject
from models.enums.EnumGameObjectType import EnumGameObjectType

# TODO iterator
class CollectionGameObjects:
    def __init__(self, game_objects: List[GameObject], types_to_filter: List[EnumGameObjectType] = None):
        super().__init__()

        if types_to_filter is None:
            types_to_filter = list[EnumGameObjectType]

        self.filtered: List[GameObject] = []
        for each in game_objects:
            if each.game_object_type in types_to_filter:
                self.filtered.append(each)

    def __iter__(self):
        self.idx = 0
        return self
    def __len__(self):
        return len(self.filtered)

    def __next__(self) -> Tuple[float, float, GameObject]:
        if self.idx >= len(self):
            raise StopIteration()
        obj = self.filtered[self.idx]
        result = (obj.position[0], obj.position[1], obj)
        self.idx += 1
        #return obj.position[0], obj.position[1], obj
        return result

if __name__ == "__main__":
    pass