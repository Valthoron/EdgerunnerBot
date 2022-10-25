import game.data

location_dictionary = {}


def add_location(sheet: str, loc: str, key: str):
    loc = sheet + "!" + loc
    location_dictionary[loc] = key


for key, attribute in game.data.attributes.items():
    add_location("Attributes", attribute["loc"], key)

for key, stat in game.data.stats.items():
    add_location("Attributes", stat["loc"], key)

for key, skill in game.data.skills.items():
    add_location("Attributes", skill["loc"], key)

    if skill["nameloc"]:
        add_location("Attributes", skill["nameloc"], key + "_name")

for key, attack in game.data.attacks.items():
    add_location("Gear", attack["nameloc"], key + "_name")
    add_location("Gear", attack["totalloc"], key + "_total")
    add_location("Gear", attack["damageloc"], key + "_damage")

location_list = location_dictionary.keys()
