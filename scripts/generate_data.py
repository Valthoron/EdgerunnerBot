import openpyxl
import csv

workbook_file_name = "Resources/Character Data.xlsx"
sheets = {
    "Attributes": "data/attributes.csv",
    "Stats": "data/stats.csv",
    "Skills": "data/skills.csv",
    "Attacks": "data/attacks.csv"
}

workbook = openpyxl.load_workbook(workbook_file_name)

for sheet_name, csv_file_name in sheets.items():
    sheet = workbook[sheet_name]
    with open(csv_file_name, "w", newline="") as file_handle:
        csv_writer = csv.writer(file_handle)
        for row in sheet.iter_rows():  # generator; was sh.rows
            csv_writer.writerow([cell.value for cell in row])
