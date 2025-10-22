from controllers.ControllerTank import ControllerTank
from models.Game import Game
from models.GameObject import GameObject
from models.enums.EnumGameObjectType import EnumGameObjectType


# singleton pattern of ControllerTank, will store pointer to GameObject player
class ControllerPlayer:

    def __init__(self, player: GameObject):
        self._player = player
        self._tank_controller = ControllerTank(player)

    @property
    def game_object(self):
        return self._player

    def fire(self, game: Game):
        self._tank_controller.fire(game)

    def set_direction(self, direction):
        self._tank_controller.set_direction(direction)
        
    def update(self, game: Game, delta_time: float):
        self._tank_controller.update(game, delta_time)
        