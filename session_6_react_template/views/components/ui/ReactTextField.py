from dataclasses import dataclass
from typing import Tuple

import pygame

from views.react.ReactComponent import ReactComponent, ReactProps, ReactState


@dataclass
class ReactPropsTextField(ReactProps):
    text: str = ''
    color_font: Tuple = (0, 0, 0)


@dataclass
class ReactStateTextField(ReactState):
    pass


class ReactTextField(ReactComponent):
    def __init__(self, props: ReactPropsTextField):
        super().__init__(props)
        if self.props.color_font is None:
            self.props.color_font = (0, 0, 0)

    def render(self):
        return []

    def draw(self, screen):
        if self.shouldComponentUpdate(self.props, self.state):
            font = pygame.font.SysFont('arial', 24)
            img_font = font.render(self.props.text, True, self.props.color_font)
            screen.blit(img_font, (self.props.x, self.props.y))
        super().draw(screen)