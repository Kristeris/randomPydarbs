import random
from controllers.strategies.IStrategyEnemy import IStrategyEnemy
from pygame import Rect
from models.Game import Game
from models.GameObject import GameObject
from models.enums.EnumGameObjectDirection import EnumGameObjectDirection
from models.enums.EnumGameObjectType import EnumGameObjectType
from controllers.strategies.StrategySimpleEnemy import StrategySimpleEnemy
from controllers.strategies.StrategyAdvancedEnemy import StrategyAdvancedEnemy

class ControllerTank:

    def __init__(self, tank: GameObject):
        self._tank = tank

    @property
    def game_object(self):
        return self._tank

    def update(self, game: Game, delta_time: float):
        # TODO implement strategy pattern for enemy tanks
        if self._tank.game_object_type in [EnumGameObjectType.Enemy, EnumGameObjectType.EnemyAdvanced]:
            self._tank.tank_next_move_time -= delta_time
            if self._tank.tank_next_move_time <= 0:
                if random.randint(0, 2) == 0:
                    self.fire(game)
                else:
                    self._tank.animation_is_animating = True
                    self._tank.direction = random.choice(list(EnumGameObjectDirection))
                    self._tank.tank_next_move_time = random.randint(1000, 3000)

        if self._tank.animation_is_animating:
            position = list(self._tank.position)
            if self._tank.direction == EnumGameObjectDirection.Up:
                position[1] -= self._tank.movement_speed * delta_time
            elif self._tank.direction == EnumGameObjectDirection.Down:
                position[1] += self._tank.movement_speed * delta_time
            elif self._tank.direction == EnumGameObjectDirection.Left:
                position[0] -= self._tank.movement_speed * delta_time
            elif self._tank.direction == EnumGameObjectDirection.Right:
                position[0] += self._tank.movement_speed * delta_time

            # if tank in map bounds
            if 0 <= position[0] <= game.map_size[0] - 1 and 0 <= position[1] <= game.map_size[1] - 1:
                is_colliding = False
                for other_object in game.game_objects:
                    if other_object != self._tank and other_object.game_object_type != EnumGameObjectType.Bullet:
                        other_position_rounded = [round(other_object.position[0], 1), round(other_object.position[1], 1)]
                        position_rounded = [round(position[0], 1), round(position[1], 1)]
                        rect_tank = [position_rounded[0], position_rounded[1], position_rounded[0] + 1, position_rounded[1] + 1]
                        rect_other_object = [other_position_rounded[0], other_position_rounded[1], other_position_rounded[0] + 1, other_position_rounded[1] + 1]
                        # check overlap
                        if rect_tank[0] < rect_other_object[2] and rect_tank[2] > rect_other_object[0] and rect_tank[1] < rect_other_object[3] and rect_tank[3] > rect_other_object[1]:
                            is_colliding = True
                            break

                if not is_colliding:
                    self._tank.position = position

    def fire(self, game: Game):
        bullet = GameObject()
        bullet.position = [self._tank.position[0], self._tank.position[1]]
        bullet.direction = self._tank.direction
        if self._tank.direction == EnumGameObjectDirection.Up:
            bullet.position[1] -= 1
        elif self._tank.direction == EnumGameObjectDirection.Down:
            bullet.position[1] += 1
        elif self._tank.direction == EnumGameObjectDirection.Left:
            bullet.position[0] -= 1
        elif self._tank.direction == EnumGameObjectDirection.Right:
            bullet.position[0] += 1
        bullet.movement_speed = 2e-3
        bullet.animation_is_animating = True
        bullet.game_object_type = EnumGameObjectType.Bullet
        game.game_objects.append(bullet)

    def set_direction(self, direction: EnumGameObjectDirection):
        if direction == EnumGameObjectDirection.NotSet:
            self._tank.animation_is_animating = False
        else:
            self._tank.animation_is_animating = True
            self._tank.direction = direction