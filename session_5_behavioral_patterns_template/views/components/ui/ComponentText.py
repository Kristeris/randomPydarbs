from typing import Tuple

import pygame
from pygame import Surface

from views.components.base.ComponentBase import ComponentBase


class ComponentText(ComponentBase):

    def __init__(
            self,
            rect: pygame.Rect,
            text: str = None,
            is_visible: bool = True,
            color_font: Tuple[int, int, int] = (0, 0, 0)
    ):
        super().__init__()

        self.is_visible = is_visible
        self.text_rect = rect
        self._text = text
        self.color_font = color_font
        self.text_surface = self.generate_text_surface()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text != value:
            self._text = value
            self.text_surface = self.generate_text_surface()

    def generate_text_surface(self):
        surface = pygame.Surface((self.text_rect.width, self.text_rect.height), pygame.SRCALPHA)
        if self._text:
            font = pygame.font.SysFont('arial', 24)
            img_font = font.render(self._text, True, self.color_font)
            surface.blit(img_font, (10, 5))
        return surface

    def render(self, surface: pygame.Surface):
        if self.is_visible:
            surface.blit(
                self.text_surface,
                (
                    self.text_rect.x,
                    self.text_rect.y
                )
            )

    def update(self, delta_milisec: float):
        pass

    def on_mouse_move(self, pos: Tuple[int, int]):
        pass

    def on_mouse_button_down(self):
        pass

    def on_mouse_button_up(self):
        pass
