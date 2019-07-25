import json
from bs4 import BeautifulSoup as bs
import requests
from CookieClone import Upgrade

# Upgrade Name, effect multipier, target, condition(int=buildings, str=cookies), price, possessed

page_link = 'https://cookieclicker.fandom.com/wiki/Upgrades'
page_response = requests.get(page_link, timeout=5).text
soup = bs(page_response, "html.parser")
# print(soup.prettify())

headers = soup.find_all('h3')
for header in headers:
    print(header.text)

# https://scipython.com/blog/scraping-a-wikipedia-table-with-beautiful-soup/
header_list = []
for i in range(0, 27):
    header = soup.find('h3')
    #print(header)
    header_list.append(header)


"""
table_list = []
for i in range()
    table = soup.find('table', {'class': 'wikitable mw-collapsible sortable mw-made-collapsible jquery-tablesorter'})
"""
"""
text_array = []
for i in range(0, 20):
    paragraphs = page_content.find_all("p")[i].text
    text_array.append(paragraphs)

upgrade_list = [
    ("Reinforced index finger", 2, "auto_clicker", 1, 100),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    ()
]
upgrade_list_json = []
for entry in upgrade_list:
    upgrade_list_json.append(vars(Upgrade(*entry, 0)))

with open('UpgradeJSON.json', 'w') as file:
    json.dump(upgrade_list_json, file, indent=2)
"""