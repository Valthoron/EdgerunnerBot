import csv

attributes = {}
stats = {}
skills = {}
batch_locs = {}
batch_namelocs = {}

with open("data/attributes.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile, dialect="excel", delimiter=";")
    for row in reader:
        key = row["key"].lower()
        attributes[key] = row
        batch_locs[row["loc"]] = key

with open("data/stats.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile, dialect="excel", delimiter=";")
    for row in reader:
        key = row["key"].lower()
        stats[key] = row
        batch_locs[row["loc"]] = key

with open("data/skills.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile, dialect="excel", delimiter=";")
    for row in reader:
        key = row["key"].lower()
        skills[key] = row
        batch_locs[row["loc"]] = key

        if row["nameloc"]:
            batch_namelocs[row["nameloc"]] = key
