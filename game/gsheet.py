import gspread

from game.character import Character, Skill
import game.data


class GoogleSheet:
    def __init__(self):
        self.gsheet_service = gspread.service_account(filename="google-edgerunner.json")

    def load_character(self, url) -> Character:
        document = self.gsheet_service.open_by_url(url)
        sheet = document.get_worksheet(0)

        # Some stuff so that a single batch_get() can be used for everything
        all_locs = list(game.data.batch_locs.keys())
        all_locs.extend(list(game.data.batch_namelocs.keys()))
        all_values = sheet.batch_get(all_locs)
        index_attributes = 0
        index_attributes_end = index_attributes + len(game.data.attributes)
        index_stats = index_attributes_end
        index_stats_end = index_stats + len(game.data.stats)
        index_skills = index_stats_end
        index_skills_end = index_skills + len(game.data.skills)
        index_names = index_skills_end
        index_names_end = index_names + len(game.data.batch_namelocs)

        # Parse attributes
        attributes = {}

        for i in range(index_attributes, index_attributes_end):
            key = game.data.batch_locs[all_locs[i]]
            attributes[key] = all_values[i].first()

        # Parse stats
        stats = {}

        for i in range(index_stats, index_stats_end):
            key = game.data.batch_locs[all_locs[i]]
            stats[key] = all_values[i].first()

        # Parse skills
        skills = {}
        custom_skill_names = {}
        custom_skill_keys = {}

        for i in range(index_names, index_names_end):
            key = game.data.batch_namelocs[all_locs[i]]
            if all_values[i]:
                custom_skill_names[key] = all_values[i].first()

                custom_key = "".join(all_values[i].first().lower().split())
                custom_skill_keys[custom_key] = key

        for i in range(index_skills, index_skills_end):
            key = game.data.batch_locs[all_locs[i]]
            name = game.data.skills[key]["name"]

            if game.data.skills[key]["nameloc"]:
                if key in custom_skill_names:
                    name = name.replace("*", custom_skill_names[key])
                else:
                    continue

            skills[key] = Skill(name, int(all_values[i].first()))

        # Create character object
        name = attributes["name"]

        character = Character(document.id, attributes=attributes, stats=stats, skills=skills, custom_skills=custom_skill_keys)

        return character
