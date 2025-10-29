from dataclasses import dataclass, field
from typing import Tuple, List
import uuid

from dataclasses_json import dataclass_json

from models.enums.EnumGameObjectDirection import EnumGameObjectDirection
from models.enums.EnumGameObjectType import EnumGameObjectType

# ORM - Object Relational Mapping
@dataclass_json
@dataclass
class GameObject:
    position: Tuple[float, float] = field(default=(0.0, 0.0))
    direction: EnumGameObjectDirection = EnumGameObjectDirection.Up
    game_object_type: EnumGameObjectType = EnumGameObjectType.NotSet

    tank_level: int = 0
    movement_speed: float = 1e-3
    tank_next_move_time: float = 0

    animation_frame: int = 0
    animation_frame_max: int = 0
    animation_frame_duration: float = 0
    animation_frame_duration_max: float = 0
    animation_is_animating: bool = False

    object_uuid: uuid.UUID = field(default_factory=uuid.uuid4)
    
    def __hash__(self):
        return hash(self.object_uuid)

    def clone(self):
        json_obj = self.to_json(indent=4)
        result = GameObject.from_json(json_obj)
        result.object_uuid = uuid.uuid4()  # Generate a new UUID for the clone
        return result