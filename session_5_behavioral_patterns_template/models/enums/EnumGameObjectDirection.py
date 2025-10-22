from enum import Enum


class EnumGameObjectDirection(str, Enum):
    Up = "Up"
    Down = "Down"
    Left = "Left"
    Right = "Right"
    NotSet = "NotSet"