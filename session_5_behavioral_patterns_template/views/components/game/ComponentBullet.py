from typing import List

import pygame
from pygame import Surface

from models.GameObject import GameObject
from models.enums.EnumGameObjectDirection import EnumGameObjectDirection
from views.components.base.ComponentGameObject import ComponentGameObject


class ComponentBullet(ComponentGameObject):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)

        self.pygame_surfaces_up: List[pygame.Surface] = []
        self.pygame_surfaces_down: List[pygame.Surface] = []
        self.pygame_surfaces_left: List[pygame.Surface] = []
        self.pygame_surfaces_right: List[pygame.Surface] = []

        self.pygame_surfaces_up.append(self.load_surface(sprite_x=19, sprite_y=5))

        self.pygame_surfaces_left.append(self.load_surface(sprite_x=20, sprite_y=5))

        self.pygame_surfaces_down.append(self.load_surface(sprite_x=21, sprite_y=5))

        self.pygame_surfaces_right.append(self.load_surface(sprite_x=22, sprite_y=5))

        self.pygame_surfaces = self.pygame_surfaces_up


    def update(self, delta_milisec):
        if self.game_object.direction == EnumGameObjectDirection.Up:
            self.pygame_surfaces = self.pygame_surfaces_up
        elif self.game_object.direction == EnumGameObjectDirection.Down:
            self.pygame_surfaces = self.pygame_surfaces_down
        elif self.game_object.direction == EnumGameObjectDirection.Left:
            self.pygame_surfaces = self.pygame_surfaces_left
        elif self.game_object.direction == EnumGameObjectDirection.Right:
            self.pygame_surfaces = self.pygame_surfaces_right

        super().update(delta_milisec)


    def render(self, screen: Surface):
        super().render(screen)

