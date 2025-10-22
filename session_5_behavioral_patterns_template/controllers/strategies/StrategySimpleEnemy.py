import random
from typing import Callable

from models.GameObject import GameObject
from controllers.strategies.IStrategyEnemy import IStrategyEnemy
from models.enums.EnumGameObjectDirection import EnumGameObjectDirection
from models.Game import Game


class StrategySimpleEnemy(IStrategyEnemy):
    def update(self, tank: GameObject, game: Game, delta_time: float, fire: Callable ):
        tank.tank_next_move_time -= delta_time
        if tank.tank_next_move_time <= 0:
            if random.randint(0, 2) == 0:
                fire(game)
            else:
                tank.animation_is_animating = True
                tank.direction = random.choice(list(EnumGameObjectDirection))
                tank.tank_next_move_time = random.randint(1000, 3000)