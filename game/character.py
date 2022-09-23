from __future__ import annotations

#import game.dice as dice


class Character():
    def __init__(self, name: str = ""):
        self._name = name

    def __str__(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self._name

    # Database
    def commit(self):
        pass

    @classmethod
    def from_context(cls, context) -> Character:
        pass

    # Serialization
    def to_dict(self) -> dict:
        return {
            "name": self._name,
        }

    @classmethod
    def from_dict(cls, dct) -> Character:
        character = cls(
            dct["name"],
        )

        return character
