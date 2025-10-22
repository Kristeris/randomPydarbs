import dataclasses
from dataclasses import field
from dataclasses import dataclass
from typing import List, Tuple

import dataclasses_json
from dataclasses_json import dataclass_json
from models.GameObject import GameObject


@dataclass_json
@dataclass
class Game:
    map_size: Tuple[int, int] = (20, 20)
    game_objects: List[GameObject] = field(default_factory=list)
    level: int = 0
    score: int = 0
