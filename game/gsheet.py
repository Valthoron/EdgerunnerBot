import gspread

from game.character import Character

cells = {
    "name": "B4",
    "handle": "B7",
    "role": "B10",
    "role_ability": "F10",
    "role_rank": "J10",
    "humanity": "B14",
    "humanity_max": "E14",
    "hp": "G14",
    "hp_max": "J14",
    "reputation": "B18",
    "imp_points": "B22",
    "imp_points_max": "E22",

    "stat_int": "L4",
    "stat_ref": "L7",
    "stat_dex": "L10",
    "stat_tech": "l13",
    "stat_cool": "L16",
    "stat_will": "L19",
    "stat_luck": "L22",
    "stat_luck_max": "N22",
    "stat_move": "L25",
    "stat_body": "L28",
    "stat_emp": "L31",
    "stat_emp_max": "N31",

    "skill_concentration": "U4",
    "skill_conceal": "U5",
    "skill_lipreading": "U6",
    "skill_perception": "U7",
    "skill_tracking": "U8",
    "skill_athletics": "U10",
    "skill_contortionist": "U11",
    "skill_dance": "U12",
    "skill_endurance": "U13",
    "skill_resist": "U14",
    "skill_stealth": "U15",

    "skill_drive": "U17",
    "skill_pilotair": "U18",
    "skill_pilotsea": "U19",
    "skill_riding": "U20",

    "skill_accounting": "U22",
    "skill_animal": "U23",
    "skill_bureaucracy": "U24",
    "skill_business": "U25",
    "skill_composition": "U26",
    "skill_criminology": "U27",
    "skill_cryptography": "U28",
    "skill_deduction": "U29",
    "skill_education": "U30",
    "skill_gamble": "U31",
    "skill_language_streetslang": "U33",
    "skill_language_2": "U34",
    "skill_language_3": "U35",
    "skill_language_4": "U36",

    "skill_library": "AB4",
    "skill_local_yourhome": "AB6",
    "skill_local_2": "AB7",
    "skill_local_3": "AB8",
    "skill_local_4": "AB9",
    "skill_science_1": "AB11",
    "skill_science_2": "AB12",
    "skill_science_3": "AB13",
    "skill_science_4": "AB14",
    "skill_tactics": "AB15",
    "skill_wilderness": "AB16",

    "skill_brawling": "AB18",
    "skill_evasion": "AB19",
    "skill_martial_1": "AB21",
    "skill_martial_2": "AB22",
    "skill_martial_3": "AB23",
    "skill_melee": "AB24",

    "skill_acting": "AB26",
    "skill_play": "AB29",
    "skill_play": "AB28",
    "skill_play": "AB30",

    "skill_archery": "AB32",
    "skill_autofire": "AB33",
    "skill_handgun": "AB34",
    "skill_heavy": "AB35",
    "skill_shoulder": "AB36",

    "skill_bribery": "AI4",
    "skill_conversation": "AI5",
    "skill_human": "AI6",
    "skill_interrogation": "AI7",
    "skill_persuasion": "AI8",
    "skill_grooming": "AI9",
    "skill_streetwise": "AI10",
    "skill_trading": "AI11",
    "skill_wardrobe": "AI12",

    "skill_airtech": "AI14",
    "skill_basictech": "AI15",
    "skill_cybertech": "AI16",
    "skill_demolitions": "AI17",
    "skill_electronics": "AI18",
    "skill_firstaid": "AI19",
    "skill_forgery": "AI20",
    "skill_landtech": "AI21",
    "skill_paint": "AI22",
    "skill_paramedic": "AI23",
    "skill_photography": "AI24",
    "skill_picklock": "AI25",
    "skill_pickpocket": "AI26",
    "skill_seatech": "AI27",
    "skill_weaponstech": "AI28",

    "skill_custom_1": "AI30",
    "skill_custom_2": "AI31",
    "skill_custom_3": "AI32",
    "skill_custom_4": "AI33",
    "skill_custom_5": "AI34",
    "skill_custom_6": "AI35",
    "skill_custom_7": "AI36",
}


class GoogleSheet:
    def __init__(self):
        self.gsheet_service = gspread.service_account(filename="google-edgerunner.json")

    def load_character(self, url) -> Character:
        sheet = self.gsheet_service.open_by_url(url).get_worksheet(0)

        # Parse general information
        name = sheet.get("B4").first()

        # Parse attributes
        character = Character(name)

        return character
