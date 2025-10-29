from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json

from models.HighScore import HighScore


@dataclass_json
@dataclass
class HighScores:
    high_scores: List[HighScore] = field(default_factory=list)