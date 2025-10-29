from dataclasses import dataclass
from typing import Tuple

import pygame

from views.components.ui.ReactTextField import ReactTextField, ReactPropsTextField, ReactStateTextField
from views.events.EventKey import EventKey
from views.react.ReactComponent import ReactComponent, ReactProps, ReactState


@dataclass
class ReactPropsTextBox(ReactPropsTextField):
    color_border: Tuple = (0, 0, 0)
    color_background: Tuple = (255, 255, 255)
    onTextChange: callable = None


@dataclass
class ReactStateTextBox(ReactStateTextField):
    text: str = ""
    onTextChange: callable = None


class ReactTextBox(ReactComponent):
    def __init__(self, props: ReactPropsTextBox):
        super().__init__(props)
        self.props = props
        self.state = ReactStateTextBox(text=props.text)

    def render(self):
        return [
            ReactTextField(
                ReactPropsTextField(
                    self.props.x + 5,
                    self.props.y + 5,
                    width=self.props.width - 10,
                    height=self.props.height - 10,
                    text=self.state.text
                )
            )
        ]

    def onKeyDown(self, event: EventKey):
        event.is_handled = True
        text = self.state.text
        if len(event.key_name) == 1:
            text += event.key_name
        if event.key_code == pygame.K_SPACE:
            text += " "
        elif event.key_code == pygame.K_BACKSPACE:
            text = text[:-1]

        self.setState(ReactStateTextBox(
            text=text
        ))
        if self.props.onTextChange:
            self.props.onTextChange(text)

    def draw(self, screen):
        if self.shouldComponentUpdate(self.props, self.state):
            pygame.draw.rect(
                screen,
                self.props.color_background,
                (self.props.x, self.props.y, self.props.width, self.props.height),
            )
            pygame.draw.rect(
                screen,
                self.props.color_border,
                (self.props.x, self.props.y, self.props.width, self.props.height),
                width=1
            )
        super().draw(screen)