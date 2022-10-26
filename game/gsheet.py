from pydoc import doc

import gspread
import gspread.utils

import game.data
import game.gsheetdata

from game.character import Character, Skill, Attack


class GoogleSheet:
    def __init__(self):
        self.gsheet_service = gspread.service_account(filename="google-edgerunner.json")

    def load_character_from_url(self, url) -> Character:
        key = gspread.utils.extract_id_from_url(url)
        return self.load_character_from_key(key)

    def load_character_from_key(self, key) -> Character:
        document = self.gsheet_service.open_by_key(key)

        # Get all character data using a single batch call
        sheet_data = {}
        all_values = document.values_batch_get(game.gsheetdata.location_list)

        for result in all_values["valueRanges"]:
            loc = result["range"]
            key = game.gsheetdata.location_dictionary[loc]

            if "values" in result:
                value = result["values"][0][0]
            else:
                value = ""  # Empty cell

            sheet_data[key] = value

        # Parse attributes
        attributes = {}

        for key in game.data.attributes.keys():
            attributes[key] = sheet_data[key]

        # Parse stats
        stats = {}

        for key in game.data.stats.keys():
            stats[key] = sheet_data[key]

        # Parse skills
        skills = {}
        custom_skills = {}

        for key in game.data.skills.keys():
            name = game.data.skills[key]["name"]
            custom_name_key = key + "_name"

            if custom_name_key in sheet_data:
                custom_name = sheet_data[custom_name_key]
                if custom_name:
                    name = name.replace("*", custom_name)
                    custom_skill_key = "".join(custom_name.lower().split())
                    custom_skills[custom_skill_key] = key
                else:
                    continue

            if sheet_data[key]:
                base = int(sheet_data[key])
            else:
                base = 0  # Empty cell is zero

            skills[key] = Skill(name, base)

        # Parse attacks
        attacks = {}

        for key in game.data.attacks.keys():
            name = sheet_data[key + "_name"]
            base = sheet_data[key + "_total"]
            damage = sheet_data[key + "_damage"]

            if not name or not base or not damage:
                continue

            attacks[key] = Attack(name, base, damage)

        # Create character object
        name = attributes["name"]

        character = Character(document.id, attributes=attributes, stats=stats, skills=skills, custom_skills=custom_skills, attacks=attacks)

        return character
