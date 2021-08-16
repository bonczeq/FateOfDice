from dataclasses import dataclass, field
from typing import Any

from fate_of_dice.common.dice import DicesBasicArguments


@dataclass
class SkillCheckArguments(DicesBasicArguments):
    skill_value: int = field(default=None)
    bonus_dice_amount: int = field(default=0)
    penalty_dice_amount: int = field(default=0)

    def fill_from_directory(self, directory: dict[str, Any]) -> 'SkillCheckArguments':
        super().fill_from_directory(directory)
        self.skill_value = directory.get('skillValue', self.skill_value)
        self.bonus_dice_amount = directory.get('bonusDiceAmount', self.bonus_dice_amount)
        self.penalty_dice_amount = directory.get('penaltyDiceAmount', self.penalty_dice_amount)
        return self
