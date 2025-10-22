from typing import Callable

from models import Game
from models.GameObject import GameObject
from abc import ABC
from abc import abstractmethod


class IStrategyEnemy(ABC):
    @abstractmethod    
    def update(self, tank: GameObject, game: Game, delta_time: float, fire: Callable ):
        pass