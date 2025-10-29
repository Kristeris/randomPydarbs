from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from models.HighScores import HighScores


@dataclass_json
@dataclass
class Settings:
    player_name: str = "Player"
    high_scores: HighScores = field(default_factory=HighScores)
