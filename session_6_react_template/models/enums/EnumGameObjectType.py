from enum import Enum


class EnumGameObjectType(str, Enum):
    NotSet = "NotSet"
    Forest = "Forest"
    Water = "Water"
    Brick = "Brick"
    Steel = "Steel"
    Tank = "Tank" # Player
    Enemy = "Enemy"
    EnemyAdvanced = "EnemyAdvanced"
    Bullet = "Bullet"
    BonusHelmet = "BonusHelmet"
    BonusClock = "BonusClock"
    BonusShovel = "BonusShovel"
    BonusStar = "BonusStar"
    BonusTank = "BonusTank"
    BonusGrenade = "BonusGrenade"
