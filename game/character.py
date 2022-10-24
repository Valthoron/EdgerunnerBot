from __future__ import annotations

import difflib

from typing import Any


class Skill():
    def __init__(self, name: str = "", base: int = 0):
        self._name = name
        self._base = base

    @property
    def name(self) -> str:
        return self._name

    @property
    def base(self) -> int:
        return self._base

     # Serialization
    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "base": self._base
        }

    @ classmethod
    def from_dict(cls, dct) -> Skill:
        skill = cls(
            name=dct["name"],
            base=int(dct["base"])
        )

        return skill


class Character():
    def __init__(self, id: str, attributes: dict = {}, stats: dict = {}, skills: dict[str, Skill] = {}, custom_skills: dict[str, str] = {}):
        self._id = id
        self._attributes = attributes
        self._stats = stats
        self._skills = skills
        self._custom_skills = custom_skills

        # Some common variables for quick access
        self._name = attributes["name"]
        self._handle = attributes["handle"]
        self._portrait = attributes["portrait"]

    def __str__(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def handle(self) -> str:
        return self._handle

    @property
    def portrait(self) -> str:
        return self._portrait

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills

    def find_skill(self, skill_name: str):
        short_key = "".join(skill_name.split()).lower()
        key_matches = list(filter(lambda key: key.startswith(short_key), self._skills.keys()))
        skill_list = [self._skills[key] for key in key_matches]

        if len(skill_list) == 0:
            key_matches = list(filter(lambda key: key.startswith(short_key), self._custom_skills.keys()))
            intermediate_keys = [self._custom_skills[key] for key in key_matches]
            skill_list = [self._skills[key] for key in intermediate_keys]

        return skill_list

    # Serialization
    def to_dict(self) -> dict:
        skills_dict = {}
        for key, skill in self._skills.items():
            skills_dict[key] = skill.to_dict()

        return {
            "cid": self._id,
            "name": self._name,
            "attributes": self._attributes,
            "stats": self._stats,
            "skills": skills_dict,
            "custom_skills": self._custom_skills
        }

    @ classmethod
    def from_dict(cls, dct) -> Character:
        skills_dict = {}
        for key, skill in dct["skills"].items():
            skills_dict[key] = Skill(skill["name"], int(skill["base"]))

        character = cls(
            dct["cid"],
            attributes=dct["attributes"],
            stats=dct["stats"],
            skills=skills_dict,
            custom_skills=dct["custom_skills"]
        )

        return character
