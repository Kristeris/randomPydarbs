import time
from dataclasses import dataclass
from typing import List

import pygame

from controllers.ControllerSettings import ControllerSettings
from controllers.ControllerGame import ControllerGame
from models.Settings import Settings
from utils.commands.CommandBase import CommandBase
from utils.commands.CommandRenamePlayer import CommandRenamePlayer
from views.components.ui.ReactButton import ReactButton, ReactPropsButton
from views.components.ui.ReactTextField import ReactTextField, ReactPropsTextField
from views.react.ReactComponent import ReactProps, ReactComponent, ReactState
from views.windows.WindowHighScores import ReactPropsWindowHighScores, WindowHighScores
from views.windows.WindowGame import WindowGame


@dataclass
class ReactPropsWindowMenu(ReactProps):
    pass


@dataclass
class ReactStateWindowMenu(ReactState):
    pass


class WindowMenu(ReactComponent):
    def __init__(self, props: ReactPropsWindowMenu):
        super().__init__(props)
        self.props = props

        self.state = ReactStateWindowMenu()

        self.settings = ControllerSettings.instance().settings
        self.command_history: List[CommandBase] = []
        self.window_main = WindowGame()

    def onClickStartGame(self):
        self.window_main = WindowGame()
        self.window_main.show()

        self.onShowHighScores()

    def onShowHighScores(self):
        self.window_high_scores = WindowHighScores(
            ReactPropsWindowHighScores(
                width=self.props.width,
                height=self.props.height,
                current_score= ControllerGame.instance().game.score
            )
        )
        self.window_high_scores.show(self.screen)
        self.forceUpdate()

    def onClickEditName(self):
        print("Enter new player name:")
        new_name = input().strip()
        if new_name:
            command = CommandRenamePlayer(self.settings, new_name)
            command.execute()
            self.command_history.append(command)
            self.forceUpdate()

    def onClickUndo(self):
        if len(self.command_history):
            command = self.command_history.pop()
            command.undo()
            self.forceUpdate()

    def onClickLoadGame(self):
        ControllerGame.instance().load_from_json_file()
        self.window_main.show()

    def onClickSaveGame(self):
        ControllerGame.instance().save_to_json_file()

    def onClickQuitGame(self):
        pygame.quit()

    def render(self):
        contents = []

        contents.append(ReactTextField(
            ReactPropsTextField(
                text=f"Player: {self.settings.player_name}",
                x=170,
                y=50,
                width=300,
                height=40
            )
        ))

        contents.append(ReactButton(
            ReactPropsButton(
                title="Start game",
                x=170,
                y=100,
                width=300,
                height=40,
                onPress=self.onClickStartGame
            )
        ))

        contents.append(ReactButton(
            ReactPropsButton(
                title="High Scores",
                x=170,
                y=150,
                width=300,
                height=40,
                onPress=self.onShowHighScores
            )
        ))

        contents.append(ReactButton(
            ReactPropsButton(
                title="Load game",
                x=170,
                y=200,
                width=300,
                height=40,
                onPress=self.onClickLoadGame
            )
        ))

        contents.append(ReactButton(
            ReactPropsButton(
                title="Save game",
                x=170,
                y=250,
                width=300,
                height=40,
                onPress=self.onClickSaveGame
            )
        ))

        contents.append(ReactButton(
            ReactPropsButton(
                title="Quit",
                x=170,
                y=300,
                width=300,
                height=40,
                onPress=self.onClickQuitGame
            )
        ))

        return contents

    def draw(self, screen):
        if self.shouldComponentUpdate(self.props, self.state):
            pygame.draw.rect(
                screen,
                color=(255, 255, 255),
                rect=pygame.Rect(
                    self.props.x,
                    self.props.y,
                    self.props.width,
                    self.props.height
                )
            )
        super().draw(screen)

    