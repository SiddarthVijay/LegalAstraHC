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
payload = {'pageno': '1', 'frmaction': '', 'm_sideflg': 'C', 'actcode': '0', 'frmdate': '01-01-2018', 'todate': today_date, 'submit1': 'Submit'}

bombayhc_page = requests.post(bombayhc_URL, payload)

# Parsing into variable
bombayhc_content = BeautifulSoup(bombayhc_page.content, 'html.parser')

# Finding the judgements table
data_table = bombayhc_content.find_all('table')[4].find_all('td', {'align': ['center']})

for data_table_text in data_table:
    if "BOMBAY" in data_table_text.get_text():
        bench_date = data_table_text.get_text().strip()
        date = bench_date[:bench_date.find("BOMBAY")]
        bench = bench_date[bench_date.find("BOMBAY"):]
        print(bench)
