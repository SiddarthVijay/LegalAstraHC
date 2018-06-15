# Import Libraries
from bs4 import BeautifulSoup
import requests

bombayhc_URL = "http://www.bombayhighcourt.nic.in/ordqryrepact_action.php"
payload = {'pageno': '1', 'frmaction': '', 'm_sideflg': 'C', 'actcode': '0', 'frmdate': '01-01-2018', 'todate': '14-06-2018', 'submit1': 'Submit'}

bombayhc_page = requests.post(bombayhc_URL, payload)

# Parsing into variable
bombayhc_content = BeautifulSoup(bombayhc_page.content, 'html.parser')

# Finding the judgements table
data_table = bombayhc_content.find_all('table')[4].find_all('td', {'align': ['center']})

with open("../outputs/table_data_long.txt", "w") as text_file:
    for data_table_text in data_table:
        # Writing text into file for later use
        print(data_table_text.get_text(), file=text_file)