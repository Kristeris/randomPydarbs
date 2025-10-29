
import os
from models.Settings import Settings


class ControllerSettings:
    __instance = None

    @staticmethod
    def instance():
        if ControllerSettings.__instance is None:
            ControllerSettings.__instance = ControllerSettings()
        return ControllerSettings.__instance

    def __init__(self):
        self._settings = Settings()
        self.load_from_json_file()
        ControllerSettings.__instance = self

    @property
    def settings(self):
        return self._settings

    def load_from_json_file(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                settings_json = file.read()
                self._settings = Settings.from_json(settings_json)
            print("Settings loaded")

    def save_to_json_file(self):
        with open("settings.json", "w") as file:
            settings_json = self._settings.to_json(indent=4)
            file.write(settings_json)
            print("Settings saved")
