# Import Libraries
from bs4 import BeautifulSoup
import requests
import datetime
import csv
# import re

print("Getting data from bombayhighcourt.nic.in...")

# Getting todays date from the system
today_date = datetime.date.today()
today_date = today_date.strftime("%d-%m-%Y")

# Filling form for to and from dates
bombayhc_URL = "http://www.bombayhighcourt.nic.in/ordqryrepact_action.php"
payload = {'pageno': '1', 'frmaction': '', 'm_sideflg': 'C', 'actcode': '0', 'frmdate': '01-01-2005', 'todate': today_date, 'submit1': 'Submit'}

bombayhc_page = requests.post(bombayhc_URL, payload)

# Parsing into variable
bombayhc_content = BeautifulSoup(bombayhc_page.content, 'html.parser')

# Finding the judgements table
data_table = bombayhc_content.find_all('table')[4].find_all('td', {'align': ['center']})

# Write to
outputFile = open("../outputs/judgement_data.csv", "w")

with outputFile:
    csvWriter = csv.writer(outputFile)
    csvWriter.writerow(["Case No", "Judge Name", "Petitioner", "Respondent", "Bench", "Judgement Date", "PDF Link"])

# Check record existance
record_exist = 0

with open("../outputs/table_data.txt", "w") as text_file:
    for data_table_text in data_table:

        outputFile = open("../outputs/judgement_data.csv", "a")

        data_table_justified = data_table_text.find_all('td', {'align': ['justified']})

        for data_table_justified_one in data_table_justified:
            respondents_and_petitioners = data_table_justified_one.get_text()
            petitioner = respondents_and_petitioners[:respondents_and_petitioners.find("Vs") - 1]
            respondent = respondents_and_petitioners[respondents_and_petitioners.find("Vs") + 3:]

        if "JUSTICE" in data_table_text.get_text() or "REGISTRAR" in data_table_text.get_text():
            justice_text = data_table_text.get_text().strip()
            justice_cleantext = justice_text.replace(respondents_and_petitioners, '')

        if "BOMBAY" in data_table_text.get_text():
            bench_date = data_table_text.get_text().strip()
            date = bench_date[:bench_date.find("BOMBAY")]
            bench = bench_date[bench_date.find("BOMBAY"):]

        data_table_links = data_table_text.find('a')
        if data_table_links:
            if data_table_links.get("href"):
                pdf_link = "http://www.bombayhighcourt.nic.in/" + str(data_table_links.get("href"))
                case_id = data_table_links.get_text().strip()
                record_exist = 1

        if record_exist == 0:
            continue

        with outputFile:
            csvWriter = csv.writer(outputFile)
            csvWriter.writerow([case_id, justice_cleantext, petitioner, respondent, bench, date, pdf_link])

        record_exist = 0

# End of script
print("HTML data from 01-01-2005 to {} stored in ../outputs/table_data.txt".format(today_date))
print("The final CSV file is stored in ../outputs/judgement_data.csv")
