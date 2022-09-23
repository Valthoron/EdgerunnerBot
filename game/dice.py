import math
import random

from enum import IntEnum


class GlitchType(IntEnum):
    NONE = 0
    GLITCH = 1
    CRITICAL = 2


class RollResult:
    def __init__(self, dice: list, hits: int, ones: int, glitch_type: GlitchType):
        self._dice = dice
        self._hits = hits
        self._ones = ones
        self._glitch_type = glitch_type

    @property
    def dice(self) -> list:
        return self._dice

    @property
    def dice_count(self) -> int:
        return len(self._dice)

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def ones(self) -> int:
        return self._ones

    @property
    def glitch_type(self) -> GlitchType:
        return self._glitch_type

    def __iter__(self) -> int:
        for die in self._dice:
            yield die

    def __getitem__(self, index: int) -> int:
        return self._dice[index]

    def __str__(self) -> str:
        string = f"{self.dice_count} "
        string += "(" + self.dice_string() + ")"
        string += f" -> `{self._hits}`"

        return string

    def dice_string(self) -> str:
        die_string = []

        for die in self._dice:
            if die > 4:
                die_string.append(f"**{die}**")
            elif die == 1:
                die_string.append(f"~~{die}~~")
            else:
                die_string.append(f"{die}")

        return ", ".join(die_string)


def roll(count: int) -> RollResult:
    if count < 1:
        return None

    if count > 200:
        return None

    dice = [
        random.choice(range(1, 7))
        for _ in range(count)
    ]

    count_hits = 0
    count_ones = 0
    glitch_threshold = math.ceil(count / 2)

    for roll in dice:
        if roll > 4:
            count_hits += 1
        elif 1 == roll:
            count_ones += 1

    glitch = False
    critical_glitch = False

    if count_ones >= glitch_threshold:
        glitch = True

        if count_hits == 0:
            critical_glitch = True

    # Form result object
    glitch_type = GlitchType.NONE

    if critical_glitch:
        glitch_type = GlitchType.CRITICAL
    elif glitch:
        glitch_type = GlitchType.GLITCH

    result = RollResult(dice, count_hits, count_ones, glitch_type)

    return result


def roll_d6(count: int) -> tuple[int, list[int]]:
    dice = [
        random.choice(range(1, 7))
        for _ in range(count)
    ]

    total = 0
    for die in dice:
        total += die

    return total, dice
