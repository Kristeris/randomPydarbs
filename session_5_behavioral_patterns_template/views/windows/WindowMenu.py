import os.path
import time
from typing import List
from tkinter import simpledialog

import pygame
from pygame import Surface

from controllers.ControllerGame import ControllerGame
from controllers.ControllerTank import ControllerTank
from models.Game import Game
from models.Settings import Settings
from models.enums.EnumGameObjectDirection import EnumGameObjectDirection
from models.enums.EnumGameObjectType import EnumGameObjectType
from views.components.base.ComponentGameObject import ComponentGameObject
from views.components.base.ComponentBase import ComponentBase
from views.components.ui.ComponentButton import ComponentButton
from views.windows.WindowGame import WindowGame
from views.components.ui.ComponentText import ComponentText
from utils.commands.CommandBase import CommandBase
from utils.commands.CommandRenamePlayer import CommandRenamePlayer

class WindowMenu():
    def __init__(self):
        super().__init__()

        self.screen = pygame.display.set_mode(
            (640, 640)
        )
        self.is_window_visible = True
        self.ui_components: List[ComponentBase] = []
        self.settings = Settings()

        self.command_history: List[CommandBase] = []

        # Add player name text component
        self.player_name_text = ComponentText(
            rect=pygame.Rect(170, 50, 300, 40),
            text=f"Player: {self.settings.player_name}",
            color_font=(255, 255, 255)
        )
        self.ui_components.append(self.player_name_text)

        button_start = ComponentButton(
            rect=pygame.Rect(170, 100, 300, 40),
            text="Start game",
        )
        self.ui_components.append(button_start)
        button_start.add_listener_click(self.on_click_start_game)

        button_edit_name = ComponentButton(
            rect=pygame.Rect(170, 150, 300, 40),
            text="Edit name",
        )
        self.ui_components.append(button_edit_name)
        button_edit_name.add_listener_click(self.on_click_edit_name)

        button_undo = ComponentButton(
            rect=pygame.Rect(170, 200, 300, 40),
            text="Undo",
        )
        self.ui_components.append(button_undo)
        button_undo.add_listener_click(self.on_click_undo)
        button_load = ComponentButton(
            rect=pygame.Rect(170, 250, 300, 40),
            text="Load game",
        )
        self.ui_components.append(button_load)
        button_load.add_listener_click(self.on_click_load_game)

        button_save = ComponentButton(
            rect=pygame.Rect(170, 300, 300, 40),
            text="Save game",
        )
        self.ui_components.append(button_save)
        button_save.add_listener_click(self.on_click_save_game)

        button_exit = ComponentButton(
            rect=pygame.Rect(170, 350, 300, 40),
            text="Quit",
        )
        self.ui_components.append(button_exit)
        button_exit.add_listener_click(self.on_click_quit_game)
        self.window_main = WindowGame()

    def on_click_start_game(self):
        self.window_main = WindowGame()
        self.window_main.show()

    def on_click_edit_name(self):
        print("Enter new player name:")
        new_name = input().strip()
        if new_name:
            command = CommandRenamePlayer(self.settings, new_name)
            command.execute()
            self.command_history.append(command)

    def on_click_undo(self):
        if len(self.command_history) > 0:
            command = self.command_history.pop()
            command.undo()

    def on_click_load_game(self):
        if os.path.exists("game.json"):
            with open("game.json", "r") as file:
                game = Game.from_json(file.read())
                ControllerGame.instance().set_game(game)
            print("Game loaded")
            self.window_main.show()

    def on_click_save_game(self):
        game_json = ControllerGame.instance().game.to_json(indent=4)
        with open("game.json", "w") as file:
            file.write(game_json)
        print("Game save")
        self.window_main.show()

    def on_click_quit_game(self):
        self.is_window_visible = False
        pass

    def show(self):
        # main game loop
        time_last = pygame.time.get_ticks()
        while self.is_window_visible:
            # get delta seconds
            time_current = pygame.time.get_ticks()
            delta_milisec = time_current - time_last
            time_last = time_current

            # update
            self.update(delta_milisec)

            # draw
            self.render()

            # update display
            pygame.display.flip()
            time.sleep(0.1)

    def update(self, delta_milisec):
        self.player_name_text.text = f"Player: {self.settings.player_name}"

        for ui_component in self.ui_components:
            ui_component.update(delta_milisec)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_window_visible = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_window_visible = False
            elif event.type == pygame.MOUSEMOTION:
                for ui_component in self.ui_components:
                    ui_component.on_mouse_move(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for ui_component in self.ui_components:
                    ui_component.on_mouse_button_down()
            elif event.type == pygame.MOUSEBUTTONUP:
                for ui_component in self.ui_components:
                    ui_component.on_mouse_button_up()

    def render(self):
        self.screen.fill((0, 0, 0))
        for ui_component in self.ui_components:
            ui_component.render(self.screen)