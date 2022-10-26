import csv

attributes = {}
stats = {}
skills = {}
attacks = {}

with open("data/attributes.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        key = row["key"].lower()
        attributes[key] = row

with open("data/stats.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        key = row["key"].lower()
        stats[key] = row

with open("data/skills.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        key = row["key"].lower()
        skills[key] = row

with open("data/attacks.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        key = row["key"].lower()
        attacks[key] = row
