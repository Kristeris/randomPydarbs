import random
from typing import List

import pygame
from pygame import Surface

from models.GameObject import GameObject
from models.enums.EnumGameObjectType import EnumGameObjectType
from views.components.base.ComponentGameObject import ComponentGameObject, SPRITE_WIDTH


class ComponentBonus(ComponentGameObject):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)

        self.pygame_surfaces: List[pygame.Surface] = []

        # Load bonus sprites based on the bonus type
        if self.game_object.game_object_type == EnumGameObjectType.BonusHelmet:
            self.load_surface(sprite_x=16, sprite_y=7)
        elif self.game_object.game_object_type == EnumGameObjectType.BonusClock:
            self.load_surface(sprite_x=17, sprite_y=7)
        elif self.game_object.game_object_type == EnumGameObjectType.BonusShovel:
            self.load_surface(sprite_x=18, sprite_y=7)
        elif self.game_object.game_object_type == EnumGameObjectType.BonusStar:
            self.load_surface(sprite_x=19, sprite_y=7)
        elif self.game_object.game_object_type == EnumGameObjectType.BonusTank:
            self.load_surface(sprite_x=20, sprite_y=7)
        elif self.game_object.game_object_type == EnumGameObjectType.BonusGrenade:
            self.load_surface(sprite_x=21, sprite_y=7)


    def update(self, delta_milisec):
        if self.game_object.animation_is_animating:
            self.game_object.animation_frame_duration += delta_milisec
            if self.game_object.animation_frame_duration >= self.game_object.animation_frame_duration_max:
                self.game_object.animation_frame_duration = 0
                self.game_object.animation_frame = (self.game_object.animation_frame + 1) % (self.game_object.animation_frame_max + 1)

    def render(self, screen: Surface):
        if self.game_object.animation_frame == 0 and len(self.pygame_surfaces) > 0:
            screen.blit(
                self.pygame_surfaces[0],
                (self.game_object.position[0] * SPRITE_WIDTH, self.game_object.position[1] * SPRITE_WIDTH)
            )
