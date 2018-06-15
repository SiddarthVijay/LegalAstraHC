# Import Libraries
from bs4 import BeautifulSoup
import requests
import datetime
import csv

print("Getting data from bombayhighcourt.nic.in...")

# Getting todays date from the system
today_date = datetime.date.today()
today_date = today_date.strftime("%d-%m-%Y")

# Filling form for to and from dates
bombayhc_URL = "http://www.bombayhighcourt.nic.in/ordqryrepact_action.php"
payload = {'pageno': '1', 'frmaction': '', 'm_sideflg': 'C', 'actcode': '0', 'frmdate': '01-01-2018', 'todate': today_date, 'submit1': 'Submit'}

bombayhc_page = requests.post(bombayhc_URL, payload)

# Parsing into variable
bombayhc_content = BeautifulSoup(bombayhc_page.content, 'html.parser')

# Finding the judgements table
data_table = bombayhc_content.find_all('table')[4].find_all('td', {'align': ['center']})

# Write to
outputFile = open("../outputs/judgement_data.csv", "w")

with outputFile:
    csvWriter = csv.writer(outputFile)
    # csvWriter.writerow(["Judge Name", "Petitioner", "Respondent", "Bench", "Judgement Date", "Case No", "PDF Link"])
    csvWriter.writerow(["Link", "Case No"])

# Check record existance
record_exist = 0

with open("../outputs/table_data.txt", "w") as text_file:
    for data_table_text in data_table:

        outputFile = open("../outputs/judgement_data.csv", "a")

        data_table_text = data_table_text.find('a')
        if data_table_text:
            if data_table_text.get("href"):
                pdf_link = "http://www.bombayhighcourt.nic.in/" + str(data_table_text.get("href"))
                case_id = data_table_text.get_text().strip()
                record_exist = 1

        if record_exist == 0:
            continue

        with outputFile:
            csvWriter = csv.writer(outputFile)
            csvWriter.writerow([pdf_link, case_id])

        record_exist = 0

# End of script
print("HTML data from 01-01-2005 to {} stored in ../outputs/table_data.txt".format(today_date))
