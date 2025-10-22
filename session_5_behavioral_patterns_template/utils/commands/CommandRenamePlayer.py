from models.Settings import Settings
from utils.commands.CommandBase import CommandBase


class CommandRenamePlayer(CommandBase):
    def __init__(self, settings: Settings, player_name: str):
        super().__init__()
        self.__settings = settings
        self.__old_player_name = settings.player_name
        self.__new_player_name = player_name

    def execute(self):
        self.__old_player_name = self.__settings.player_name
        self.__settings.player_name = self.__new_player_name

    def undo(self):
        self.__settings.player_name = self.__old_player_name
