import math
import random

from enum import IntEnum


class CriticalType(IntEnum):
    NONE = 0
    SUCCESS = 1
    FAILURE = 2


class RollResult:
    def __init__(self, roll: int, bonus: int, critical_roll: int = 0):
        self._roll = roll
        self._bonus = bonus
        self._total = roll + bonus
        self._critical_roll = critical_roll

        if roll == 10:
            self._critical_type = CriticalType.SUCCESS
            self._total += critical_roll
        elif roll == 1:
            self._critical_type = CriticalType.FAILURE
            self._total -= critical_roll
        else:
            self._critical_type = CriticalType.NONE

    @property
    def roll(self) -> int:
        return self._roll

    @property
    def bonus(self) -> int:
        return self._bonus

    @property
    def total(self) -> int:
        return self._total

    @property
    def critical_type(self) -> CriticalType:
        return self._critical_type

    @property
    def critical_roll(self) -> int:
        return self._critical_roll

    def __str__(self) -> str:
        string = self.dice_string()
        string += f" = `{self._total}`"
        return string

    def dice_string(self) -> str:
        string = f"1d10 ({self._roll}) + {self._bonus}"

        if self._critical_type is not CriticalType.NONE:
            if self._critical_type is CriticalType.SUCCESS:
                string += " + "
            else:
                string += " - "

            string += f"1d10 ({self._critical_roll})"

        return string


def roll(bonus: int) -> RollResult:
    roll = random.choice(range(1, 11))
    crit_roll = 0

    if (roll == 10) or (roll == 1):
        crit_roll = random.choice(range(1, 11))

    return RollResult(roll, bonus, crit_roll)
