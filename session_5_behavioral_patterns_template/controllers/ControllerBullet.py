from models.Game import Game
from models.GameObject import GameObject
from models.enums.EnumGameObjectDirection import EnumGameObjectDirection
from models.enums.EnumGameObjectType import EnumGameObjectType


class ControllerBullet:

    def __init__(self, bullet: GameObject):
        self._bullet = bullet

    @property
    def game_object(self):
        return self._bullet


    def update(self, game: Game, delta_time: float):
        if self._bullet.animation_is_animating:
            position = list(self._bullet.position)
            if self._bullet.direction == EnumGameObjectDirection.Up:
                position[1] -= self._bullet.movement_speed * delta_time
            elif self._bullet.direction == EnumGameObjectDirection.Down:
                position[1] += self._bullet.movement_speed * delta_time
            elif self._bullet.direction == EnumGameObjectDirection.Left:
                position[0] -= self._bullet.movement_speed * delta_time
            elif self._bullet.direction == EnumGameObjectDirection.Right:
                position[0] += self._bullet.movement_speed * delta_time

            is_colliding = False
            other_object_remove = None

            if 0 <= position[0] <= game.map_size[0] - 1 and 0 <= position[1] <= game.map_size[1] - 1:
                for other_object in game.game_objects:
                    if other_object != self._bullet:
                        other_position_rounded = [round(other_object.position[0], 1), round(other_object.position[1], 1)]
                        position_rounded = [round(position[0], 1), round(position[1], 1)]
                        rect_tank = [position_rounded[0], position_rounded[1], position_rounded[0] + 1, position_rounded[1] + 1]
                        rect_other_object = [other_position_rounded[0], other_position_rounded[1], other_position_rounded[0] + 1, other_position_rounded[1] + 1]
                        # check overlap
                        if rect_tank[0] < rect_other_object[2] and rect_tank[2] > rect_other_object[0] and rect_tank[1] < rect_other_object[3] and rect_tank[3] > rect_other_object[1]:
                            is_colliding = True
                            other_object_remove = other_object
                            break
            else:
                is_colliding = True

            if not is_colliding:
                self._bullet.position = position
            else:
                game.game_objects.remove(self._bullet)
                if other_object_remove is not None:
                    game.game_objects.remove(other_object_remove)
                    if other_object_remove.game_object_type in (EnumGameObjectType.Enemy, EnumGameObjectType.EnemyAdvanced):
                        game.score += 1