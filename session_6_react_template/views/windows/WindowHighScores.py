import os.path
import time
from dataclasses import dataclass, field
from typing import List

import pygame

from controllers.ControllerSettings import ControllerSettings
from models.HighScore import HighScore
from models.HighScores import HighScores
from views.components.ui.ReactButton import ReactButton, ReactPropsButton
from views.components.ui.ReactTextBox import ReactTextBox, ReactPropsTextBox
from views.components.ui.ReactTextField import ReactTextField, ReactPropsTextField
from views.events.EventKey import EventKey
from views.events.EventMouse import EventMouse
from views.react.ReactComponent import ReactProps, ReactComponent, ReactState


@dataclass
class ReactPropsWindowHighScores(ReactProps):
    current_score: int = 0


@dataclass
class ReactStateWindowHighScores(ReactState):    
    current_name: str = ""
    is_entering: bool = True
    high_scores: HighScores = field(default_factory=HighScores)


class WindowHighScores(ReactComponent):
    def __init__(self, props: ReactPropsWindowHighScores):
        super().__init__(props)
        self.props = props

        self.state = ReactStateWindowHighScores(
        )

        self.state.high_scores = ControllerSettings.instance().settings.high_scores

    def onPressSave(self):
        high_scores = self.state.high_scores
        high_scores.high_scores.append(HighScore(
            name=self.state.current_name,
            score=self.props.current_score
        ))

        #TODO
        # sort by score high_scores
        # cut top 10 items

        self.setState(
            ReactStateWindowHighScores(
                current_name="",
                is_entering=False,
                high_scores=high_scores
            )
        )
        ControllerSettings.instance().settings.high_scores = high_scores
        ControllerSettings.instance().save_to_json_file()

    def onKeyDown(self, event: EventKey):
        super().onKeyDown(event)

    def onTextChange(self, text):
        self.setState(
            ReactStateWindowHighScores(
                current_name=text,
                is_entering=self.state.is_entering,
                high_scores=self.state.high_scores
            )
        )

    def render(self):
        contents: List[ReactComponent] = []

        contents.append(ReactTextField(
            ReactPropsTextField(
                text="High scores",
                x=10,
                y=10
            )
        ))

        i = 0
        for highscore in self.state.high_scores.high_scores:
            contents.append(
                ReactTextField(
                    ReactPropsTextField(
                        text=f"{highscore.name} score: {highscore.score}",
                        x=10,
                        y=60+50*i

                    )
                )
            )
            i += 1

        if self.state.is_entering:
            contents.append(ReactTextField(
                ReactPropsTextField(
                    text="Enter your name",
                    x=10,
                    y=500
                )
            ))
            contents.append(ReactTextBox(
                ReactPropsTextBox(
                    text=self.state.current_name,
                    x=10,
                    y=550,
                    width=400,
                    height=50,
                    onTextChange=self.onTextChange
                )
            ))
            contents.append(ReactButton(
                ReactPropsButton(
                    title="Save",
                    x=450,
                    y=550,
                    width=100,
                    height=50,
                    onPress=self.onPressSave
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

