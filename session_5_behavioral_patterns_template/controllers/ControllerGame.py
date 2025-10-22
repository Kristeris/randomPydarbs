import random

from controllers.ControllerBullet import ControllerBullet
from controllers.ControllerPlayer import ControllerPlayer
from controllers.ControllerTank import ControllerTank
from controllers.ControllerFasterTank import ControllerFasterTank
from models.Game import Game
from models.GameObject import GameObject
from models.enums.EnumGameObjectDirection import EnumGameObjectDirection
from models.enums.EnumGameObjectType import EnumGameObjectType
from utils.collections.CollectionGameObjects import CollectionGameObjects
from utils.decorators.DecoratorTryCatch import decorator_try_catch


class ControllerGame:
    __instance = None

    def __init__(self):
        if ControllerGame.__instance is not None:
            raise Exception("Cannot create second instance of singleton")

        self._game: Game = None # non-static member variable
        self.player_controller = None
        self.game_objects_controllers = []
        ControllerGame.__instance = self

    @staticmethod
    def instance():
        if ControllerGame.__instance is None:
            ControllerGame() # new ControllerGame()
        return ControllerGame.__instance

    def player(self):
        game_object = None
        for game_object in self._game.game_objects:
            if game_object.game_object_type == EnumGameObjectType.Tank:
                break
        return game_object

    @property
    def game(self):
        return self._game

    def set_game(self, game):
        self._game = game

    def new_game(self):
        self._game = game = Game()

        # randomly choose map tile type
        game_object_options = [EnumGameObjectType.NotSet, EnumGameObjectType.Tank] * 300 + [
            EnumGameObjectType.Forest,
            EnumGameObjectType.Water,
            EnumGameObjectType.Brick,
            EnumGameObjectType.Steel,
            EnumGameObjectType.Enemy,          
        ] * 30 + [
            EnumGameObjectType.BonusStar
        ] * 3

        # prototype
        animated_game_object = GameObject()
        animated_game_object.animation_frame_duration = random.randint(0, int(animated_game_object.animation_frame_duration_max))
        animated_game_object.animation_frame_max = 2
        animated_game_object.animation_frame_duration_max = 500
        animated_game_object.animation_is_animating = True

        is_player_set = False
        for x in range(game.map_size[0]):
            for y in range(game.map_size[1]):
                game_object_type = random.choice(game_object_options)

                if game_object_type == EnumGameObjectType.Tank:
                    if not is_player_set:
                        is_player_set = True
                    else:
                        game_object_type = EnumGameObjectType.NotSet

                if game_object_type != EnumGameObjectType.NotSet:
                    game_object: GameObject = animated_game_object.clone()
                    game_object.position = [x, y]
                    game_object.game_object_type = game_object_type

                    if game_object_type in (EnumGameObjectType.Tank, EnumGameObjectType.Enemy, EnumGameObjectType.EnemyAdvanced):
                        game_object.direction = random.choice([
                            EnumGameObjectDirection.Up,
                            EnumGameObjectDirection.Right,
                            EnumGameObjectDirection.Down,
                            EnumGameObjectDirection.Left
                        ])  # Random direction for tanks

                    if game_object_type in (
                        EnumGameObjectType.Steel,
                        EnumGameObjectType.Brick,
                        EnumGameObjectType.Forest
                    ):
                        game_object.animation_is_animating = False

                    if game_object_type in (
                        EnumGameObjectType.BonusHelmet,
                        EnumGameObjectType.BonusClock,
                        EnumGameObjectType.BonusShovel,
                        EnumGameObjectType.BonusStar,
                        EnumGameObjectType.BonusTank,
                        EnumGameObjectType.BonusGrenade
                    ):
                        game_object.animation_frame_duration_max = random.randint(400, 600)

                    game.game_objects.append(game_object)

                    if game_object_type == EnumGameObjectType.Tank:
                        self.player_controller = ControllerPlayer(game_object)


    @decorator_try_catch
    def update(self, delta_time: float):
        game = self._game
        
        # Update game_objects_controllers based on game.game_objects
        game_objects_without_player = [game_object for game_object in game.game_objects if game_object.game_object_type != EnumGameObjectType.Tank]
        current_game_objects = set([game_object for game_object in game_objects_without_player])
        current_controlled_objects = set(controller.game_object for controller in self.game_objects_controllers)
        
        # Remove controllers for objects that no longer exist
        self.game_objects_controllers = [controller for controller in self.game_objects_controllers 
                                         if controller.game_object in current_game_objects]
        
        # Add controllers for new objects
        for game_object in current_game_objects - current_controlled_objects:
            if game_object.game_object_type in [EnumGameObjectType.EnemyAdvanced, EnumGameObjectType.Enemy]:
                self.game_objects_controllers.append(ControllerTank(game_object))
            elif game_object.game_object_type == EnumGameObjectType.Bullet:
                self.game_objects_controllers.append(ControllerBullet(game_object))

        # Update all controllers
        for controller in self.game_objects_controllers:
            controller.update(game, delta_time)
        self.player_controller.update(game, delta_time)

        # Check for collisions between tanks and bonuses
        self.game_objects_controllers.append(self.player_controller)
        # TODO iterator
        for bonus_position_x, bonus_position_y, game_object in CollectionGameObjects(game.game_objects, [EnumGameObjectType.BonusStar]):
        #for game_object in game.game_objects:
            #if game_object.game_object_type == EnumGameObjectType.BonusStar:
                #bonus_position_x, bonus_position_y = game_object.position
                for i, controller_tank in enumerate(self.game_objects_controllers):
                    if controller_tank.game_object.game_object_type in (
                    EnumGameObjectType.Tank, EnumGameObjectType.Enemy, EnumGameObjectType.EnemyAdvanced):
                        tank_position_x, tank_position_y = controller_tank.game_object.position
                        if (tank_position_x < bonus_position_x + 1 and
                                tank_position_x + 1 > bonus_position_x and
                                tank_position_y < bonus_position_y + 1 and
                                tank_position_y + 1 > bonus_position_y):

                            if game_object.game_object_type == EnumGameObjectType.BonusStar:
                                controller_tank = ControllerFasterTank(controller_tank)
                                self.game_objects_controllers[i] = controller_tank

                            game.game_objects.remove(game_object)
                            break
        self.player_controller = self.game_objects_controllers.pop(-1)



        for game_object in game.game_objects:
            if game_object.animation_is_animating:
                game_object.animation_frame_duration += delta_time
                if game_object.animation_frame_duration >= game_object.animation_frame_duration_max:
                    game_object.animation_frame_duration = 0
                    game_object.animation_frame += 1
                    if game_object.animation_frame >= game_object.animation_frame_max:
                        game_object.animation_frame = 0
