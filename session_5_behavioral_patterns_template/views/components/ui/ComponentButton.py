from typing import List, Tuple, Callable

import pygame
from pygame import Surface

from views.components.base.ComponentBase import ComponentBase


class ComponentButton(ComponentBase):

    def __init__(
            self,
            rect: pygame.Rect,
            text: str = None,
            is_visible: bool = True,
            is_toggle_button: bool = False
    ):
        super().__init__()

        self.is_visible = is_visible
        self.button_rect = rect
        self.button_text = text
        self.button_up = None
        self.button_over = None
        self.button_down = None
        self.offset_x = 0
        self.offset_y = 0
        self.is_button_down = False
        self.is_button_over = False
        self.is_button_toggled = False
        self.is_toggle_button = is_toggle_button


        self.button_up = self.generate_button_surface(
            color_background=(255, 255, 255),
            color_font=(0, 0, 0)
        )
        self.button_over = self.generate_button_surface(
            color_background=(155, 155, 155),
            color_font=(0, 0, 0)
        )
        self.button_down = self.generate_button_surface(
            color_background=(0, 0, 0),
            color_font=(255, 255, 255)
        )

        self.listeners: List[Callable] = []


    def generate_button_surface(self, color_background, color_font):
        surface = pygame.Surface((self.button_rect.width, self.button_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            surface,
            color=color_font,
            rect=pygame.Rect(0, 0, self.button_rect.width, self.button_rect.height)
        )
        pygame.draw.rect(
            surface,
            color=color_background,
            rect=pygame.Rect(2, 2, self.button_rect.width - 4, self.button_rect.height - 4)
        )
        if self.button_text:
            font = pygame.font.SysFont('arial', 24)
            img_font = font.render(self.button_text, True, color_font)
            surface.blit(img_font, (10, 5))
        return surface

    def render(self, surface: pygame.Surface):
        if self.is_visible:
            button_surface = self.button_up
            if self.is_button_down or self.is_button_toggled:
                button_surface = self.button_down
            elif self.is_button_over:
                button_surface = self.button_over
            surface.blit(
                button_surface,
                (
                    self.button_rect.x + self.offset_x,
                    self.button_rect.y + self.offset_y
                )
            )

    def update(self, delta_milisec:float):
        pass

    def on_mouse_move(self, mouse_position: Tuple[int, int]):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]

        is_button_over = False
        if self.button_rect.x < mouse_x < self.button_rect.x + self.button_rect.width:
            if self.button_rect.y < mouse_y < self.button_rect.y + self.button_rect.height:
                is_button_over = True
        self.is_button_over = is_button_over
        if not is_button_over:
            self.is_button_down = False

    def on_mouse_button_down(self):
        if self.is_button_over:
            self.is_button_down = True

    def on_mouse_button_up(self):
        if self.is_button_over:
            self.is_button_down = False
            for listener in self.listeners:
                listener()

    def add_listener_click(self, callback: Callable):
        self.listeners.append(callback)