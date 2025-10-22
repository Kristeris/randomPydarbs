from typing import List

from models.enums.EnumGameObjectType import EnumGameObjectType
from models.GameObject import GameObject
from views.components.game.ComponentBonus import ComponentBonus
from views.components.game.ComponentBullet import ComponentBullet
from views.components.game.ComponentEnemy import ComponentEnemy
from views.components.base.ComponentGameObject import ComponentGameObject
from views.components.game.ComponentTank import ComponentTank


class FactoryGameObject:

    def create_component(self, game_object:GameObject) -> ComponentGameObject:
        obj_type = game_object.game_object_type
        if obj_type == EnumGameObjectType.Tank:
            result = ComponentTank(game_object)
        elif obj_type == EnumGameObjectType.Bullet:
            result = ComponentBullet(game_object)
        elif obj_type in [EnumGameObjectType.Enemy, EnumGameObjectType.EnemyAdvanced]:
            result = ComponentEnemy(game_object)
        elif obj_type in [EnumGameObjectType.BonusHelmet, EnumGameObjectType.BonusClock, 
                          EnumGameObjectType.BonusShovel, EnumGameObjectType.BonusStar, 
                          EnumGameObjectType.BonusTank, EnumGameObjectType.BonusGrenade]:
            result = ComponentBonus(game_object)
        else:
            result = ComponentGameObject(game_object)
        return result

