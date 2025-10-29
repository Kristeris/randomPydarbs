from typing import List, Tuple

from models.GameObject import GameObject
from models.enums.EnumGameObjectType import EnumGameObjectType


class CollectionGameObjects:
    def __init__(self, game_objects: List[GameObject], types_to_filter: List[EnumGameObjectType] = None):
        super().__init__()

        if types_to_filter is None:
            types_to_filter = list(EnumGameObjectType) # [EnumGameObjectType.Tank]

        self.__filtered = [it for it in game_objects if it.game_object_type in types_to_filter] # map type of func
        self.__idx = 0

    def __iter__(self):
        self.__idx = 0
        return self

    def __len__(self):
        return len(self.__filtered)

    def __next__(self) -> Tuple[float, float, GameObject]:
        if self.__idx >= len(self):
            raise StopIteration()
        obj = self.__filtered[self.__idx]
        self.__idx += 1
        return obj.position[0], obj.position[1], obj

if __name__ == "__main__":
    pass