from controllers.ControllerTank import ControllerTank
from models.GameObject import GameObject
from models.Game import Game
import time

class ControllerFasterTank(ControllerTank):
    def __init__(self, controller: ControllerTank):
        self._parent_controller = controller
        self._original_speed = controller.game_object.movement_speed
        self._boost_time = 10_000
        if isinstance(self._parent_controller, ControllerFasterTank):
            self._parent_controller._boost_time += self._boost_time

        self._parent_controller.game_object.movement_speed *= 2.0
        self._tank = self._parent_controller.game_object
        print("Tank upgraded")
    @property
    def game_object(self):
        return self._parent_controller.game_object

    def update(self, game: Game, delta_time: float):
        if self._boost_time > 0:
            self._boost_time -= delta_time
        else:
            self._parent_controller.game_object.movement_speed = self._original_speed
        self._parent_controller.update(game, delta_time)

    def __getattr__(self, name):
        return getattr(self._parent_controller, name)
