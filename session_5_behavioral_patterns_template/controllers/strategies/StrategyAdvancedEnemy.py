import random
from typing import Callable

from models.GameObject import GameObject
from controllers.strategies.IStrategyEnemy import IStrategyEnemy
from models.enums.EnumGameObjectDirection import EnumGameObjectDirection
from models.Game import Game


class StrategyAdvancedEnemy(IStrategyEnemy):
    def __init__(self):
        self.last_moves = []
    
    def update(self, tank: GameObject, game: Game, delta_time: float, fire: Callable ):
        tank.tank_next_move_time -= delta_time
        if tank.tank_next_move_time <= 0:
            if random.randint(0, 1) == 0:
                fire(game)
            else:
                tank.animation_is_animating = True
                    
                # remember last moves
                available_directions = list(EnumGameObjectDirection)
                if len(self.last_moves) > 0:                
                    if self.last_moves[-1] in available_directions:
                        available_directions.remove(self.last_moves[-1])
                
                tank.direction = random.choice(available_directions)
                            
                self.last_moves.append(tank.direction)
                if len(self.last_moves) > 2:
                    self.last_moves.pop(0)
                
                tank.tank_next_move_time = random.randint(1000, 3000)