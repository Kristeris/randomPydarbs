from abc import ABC, abstractmethod
from typing import Tuple

from pygame import Surface


class ComponentBase(ABC):

    @abstractmethod
    def render(self, screen: Surface):
        pass

    @abstractmethod
    def update(self, delta_milisec: float):
        pass

    @abstractmethod
    def on_mouse_move(self, mouse_position: Tuple[int, int]):
        pass

    @abstractmethod
    def on_mouse_button_down(self):
        pass

    @abstractmethod
    def on_mouse_button_up(self):
        pass

