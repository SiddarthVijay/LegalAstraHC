# Import Libraries
import json
import urllib3
from bs4 import BeautifulSoup
# import requests

# Getting the HTML data from the website
http = urllib3.PoolManager()
bombayhc_URL = http.request(
    'POST',
    'http://www.bombayhighcourt.nic.in/ordqryrepact_action.php',
    fields={'pageno': '1',
            'frmaction': '',
            'm_sideflg': 'C',
            'actcode': '0',
            'frmdate': '01-01-2018',
            'todate': '14-06-2018',
            'submit1': 'Submit'})

json.loads(bombayhc_URL.data.decode('utf-8'))['form']
# {'pageno': '1', 'frmaction': '', 'm_sideflg': 'C', 'actcode': '0', 'frmdate': '01-01-2018', 'todate': '14-06-2018','submit1': 'Submit'})

# Parsing into variable
bombayhc_content = BeautifulSoup(bombayhc_URL.data, 'html.parser')
print(bombayhc_content.content)

# # Opening output file
# # outputFile = open("../outputs/com_books.csv", "w")

# # Finding the judgements table
# data_table = bombayhc_content.find_all('table')[4].find_all('td', {'align': 'center'})

# with open("../outputs/table_data.txt", "w") as text_file:
    # for data_table_text in data_table:
        # # Writing text into file for later use
        # print(data_table_text.get_text(), file=text_file)
