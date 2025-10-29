from dataclasses import dataclass
from typing import Callable

import pygame

from views.components.ui.ReactTextField import ReactTextField, ReactPropsTextField
from views.events.EventMouse import EventMouse
from views.react.ReactComponent import ReactProps, ReactState, ReactComponent


@dataclass
class ReactPropsButton(ReactProps):
    title: str = ''
    onPress: Callable = None


@dataclass
class ReactStateButton(ReactState):
    isMouseOver: bool = False


class ReactButton(ReactComponent):
    def __init__(self, props: ReactPropsButton):
        super().__init__(props)

        self.props = props
        self.state = ReactStateButton()

    def onPress(self, event: EventMouse):
        if self.state.isMouseOver:
            event.is_handled = True
            if self.props.onPress:
                self.props.onPress()

    def onMouseMove(self, event: EventMouse):
        isMouseOver = False
        if self.props.x < event.x < self.props.x + self.props.width:
            if self.props.y < event.y < self.props.y + self.props.height:
                # self.state.isMouseOver = isMouseOver
                isMouseOver = True
        if isMouseOver!= self.state.isMouseOver:
            self.setState(ReactStateButton(
                isMouseOver=isMouseOver
            ))

    def render(self):
        return [
            ReactTextField(
                ReactPropsTextField(
                    x=self.props.x + 5,
                    y=self.props.y + 5,
                    width=self.props.width - 5,
                    height=self.props.height - 5,
                    text=self.props.title
                )
            )
        ]

    def draw(self, screen):
        if self.shouldComponentUpdate(self.props, self.state):
            color = (100, 100, 100)
            if self.state.isMouseOver:
                color = (200, 200, 200)
            pygame.draw.rect(
                screen,
                color,
                rect=(self.props.x, self.props.y, self.props.width, self.props.height)
            )
        super().draw(screen)