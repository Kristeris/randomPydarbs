import copy
import time
from dataclasses import dataclass
from typing import Union, List

import pygame

from views.events.EventKey import EventKey
from views.events.EventMouse import EventMouse


@dataclass
class ReactProps:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0


@dataclass
class ReactState:
    pass


class DictToObj:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class ReactComponent:
    def __init__(self, props: ReactProps):
        self.children = []
        self.children_before = []

        self.props = props
        self.state = ReactState()
        self.screen = None

        self.propsPrevious = None
        self.statePrevious = None

        self.is_mounted = False

    def setState(self, state):
        self.state = state
        self.children = self.render()

    def forceUpdate(self):
        self.props = DictToObj(**self.props.__dict__)
        self.children = self.render()
        for each in self.children:
            each.forceUpdate()

    def componentDidMount(self):
        pass

    def componentDidUpdate(self):
        self.statePrevious = self.state
        self.propsPrevious = self.props

    def componentWillUnmount(self):
        pass

    def shouldComponentUpdate(self, nextProps, nextState):
        result = not self.is_mounted or self.propsPrevious != nextProps or self.statePrevious != nextState
        return result

    def render(self):
        return []

    def draw(self, screen):
        children_next = self.render()

        if not self.is_mounted:
            self.children = children_next
            self.componentDidMount()
            self.is_mounted = True

        if len(children_next) != len(self.children_before):
            for child in self.children_before:
                child.componentWillUnmount()
            self.children = children_next
            for child in self.children:
                child.draw(screen)
        else:
            for child, child_before in zip(self.children, self.children_before):
                if child_before.shouldComponentUpdate(child.props, child.state) or self.shouldComponentUpdate(self.props, self.state):
                    child.children = child.render()
                    child.draw(screen)

        self.children_before = self.children

        if self.shouldComponentUpdate(self.props, self.state):
            self.componentDidUpdate()

    def onPress(self, event: EventMouse):
        if not event.is_handled:
            for child in self.children:
                child.onPress(event)

    def onMouseMove(self, event: EventMouse):
        if not event.is_handled:
            for child in self.children:
                child.onMouseMove(event)

    def onKeyDown(self, event: EventKey):
        if not event.is_handled:
            for child in self.children:
                child.onKeyDown(event)

    def show(self, screen):

        self.screen = screen
        is_running = True
        is_mouse_down = False

        self.forceUpdate()

        while is_running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()

            if is_mouse_down and not any(mouse_buttons):
                event = EventMouse()
                event.x = mouse_pos[0]
                event.y = mouse_pos[1]
                event.is_mouse_down = False
                self.onPress(event)
            else:
                event = EventMouse()
                event.x = mouse_pos[0]
                event.y = mouse_pos[1]
                event.is_mouse_down = any(mouse_buttons)
                self.onMouseMove(event)
            is_mouse_down = any(mouse_buttons)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        is_running = False
                    else:
                        event = EventKey(
                            key_code=event.key,
                            key_name=pygame.key.name(event.key)
                        )
                        self.onKeyDown(event)

            self.draw(screen)
            pygame.display.flip()
            time.sleep(0.01)