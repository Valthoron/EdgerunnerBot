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


class Attack():
    def __init__(self, name: str = "", total: int = 0, damage: str = "0"):
        self._name = name
        self._total = total
        self._damage = damage

    @property
    def name(self) -> str:
        return self._name

    @property
    def total(self) -> int:
        return self._total

    @property
    def damage(self) -> str:
        return self._damage

    # Serialization
    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "total": self._total,
            "damage": self._damage
        }

    @ classmethod
    def from_dict(cls, dct) -> Attack:
        attack = cls(
            name=dct["name"],
            total=int(dct["total"]),
            damage=dct["damage"]
        )

        return attack


class Character():
    def __init__(self, id: str, attributes: dict = {}, stats: dict = {}, skills: dict[str, Skill] = {}, custom_skills: dict[str, str] = {}, attacks: dict[str, Attack] = {}):
        self._id = id
        self._attributes = attributes
        self._stats = stats
        self._skills = skills
        self._custom_skills = custom_skills
        self._attacks = attacks

        # Some common variables for quick access
        self._name = attributes["name"]
        self._handle = attributes["handle"]
        self._portrait = attributes["portrait"]

        # Derived variables
        self._attack_names = {}
        for key, attack in self._attacks.items():
            short_name = "".join(attack.name.lower().split())
            self._attack_names[short_name] = key

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

    def find_skill(self, skill_name: str) -> list[Skill]:
        short_key = "".join(skill_name.split()).lower()
        key_matches = list(filter(lambda key: key.startswith(short_key), self._skills.keys()))
        skill_list = [self._skills[key] for key in key_matches]

        if len(skill_list) == 0:
            key_matches = list(filter(lambda key: key.startswith(short_key), self._custom_skills.keys()))
            intermediate_keys = [self._custom_skills[key] for key in key_matches]
            skill_list = [self._skills[key] for key in intermediate_keys]

        return skill_list

    def find_attack(self, attack_name: str) -> list[Attack]:
        short_key = "".join(attack_name.split()).lower()
        key_matches = list(filter(lambda key: key.startswith(short_key), self._attack_names.keys()))
        attack_keys = [self._attack_names[key] for key in key_matches]
        attack_list = [self._attacks[key] for key in attack_keys]

        return attack_list

    # Serialization
    def to_dict(self) -> dict:
        skills_dict = {}
        for key, skill in self._skills.items():
            skills_dict[key] = skill.to_dict()

        attacks_dict = {}
        for key, attack in self._attacks.items():
            attacks_dict[key] = attack.to_dict()

        return {
            "cid": self._id,
            "name": self._name,
            "attributes": self._attributes,
            "stats": self._stats,
            "skills": skills_dict,
            "custom_skills": self._custom_skills,
            "attacks": attacks_dict
        }

    @ classmethod
    def from_dict(cls, dct) -> Character:
        skills_dict = {}
        for key, skill in dct["skills"].items():
            skills_dict[key] = Skill(name=skill["name"], base=int(skill["base"]))

        attacks_dict = {}
        for key, attack in dct["attacks"].items():
            attacks_dict[key] = Attack(name=attack["name"], total=int(attack["total"]), damage=attack["damage"])

        character = cls(
            dct["cid"],
            attributes=dct["attributes"],
            stats=dct["stats"],
            skills=skills_dict,
            custom_skills=dct["custom_skills"],
            attacks=attacks_dict
        )

        return character
