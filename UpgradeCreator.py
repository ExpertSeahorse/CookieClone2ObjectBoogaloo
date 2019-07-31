import json
from bs4 import BeautifulSoup
import requests

from Packages import undisplay_num, float_extract
from CookieClone import Upgrade

# The link to the page being scraped
page_link = 'https://cookieclicker.fandom.com/wiki/Upgrades'
# Downloads the HTML of the page
page_response = requests.get(page_link, timeout=5).text
# Soups the HTML of the file
soup = BeautifulSoup(page_response, "html.parser")


# Pulls out all of the tables with upgrades
raw_tables = soup.find_all('table', class_='wikitable mw-collapsible sortable')
filled_tables = []
# Within each of the tables...
for table in raw_tables:
    # Pull out every row...
    raw_rows = table.find_all('tr')
    filled_rows = []
    # Within every row...
    for row in raw_rows:
        # find table's title or the column headers...
        name = row.find('th')
        filled_cells = []
        if name:
            t = name.text
            # if the row is the column headers, ignore them
            if t == " Icon\n":
                continue
            # Add the title to the row
            filled_cells.append(t.strip())

        # find all of the content in the table
        raw_cells = row.find_all('td')
        # For that content...
        for cell in raw_cells:
            t = cell.text
            # Add it to an array
            filled_cells.append(t.strip())
        # Add all of the cells to the row
        filled_rows.append(filled_cells)
    # Add all of the rows to the table
    filled_tables.append(filled_rows)

# For the first set of tables (general building upgrades)
building_upgrades = []
for table in filled_tables[:-13]:
    for i, row in enumerate(table):
        if i > 0:
            # if "twice" in the effect, change it to 2x
            if 'twice' in row[4]:
                row[4] = 2
            # if "+" in the effect, pull out the number
            elif '+' in row[4]:
                row[4] = float_extract(row[4])

            # if the price is a string, extract the number it means
            if type(row[3]) == str:
                row[3] = undisplay_num(row[3])

            # If the
            if 'Cursor' in table[0][0]:
                table[0][0] = 'auto clicker'
            elif 'upgrades' in table[0][0]:
                table[0][0] = table[0][0].lower().replace('upgrades', '').strip()

            if type(row[2]) == str:
                row[2] = int(float_extract(row[2]))

            building_upgrades.append(Upgrade(row[1], row[4], table[0][0], row[2], row[3], 0))

upgrade_list_json = []
for entry in building_upgrades:
    upgrade_list_json.append(vars(entry))

with open('UpgradeJSON.json', 'w') as file:
    json.dump(upgrade_list_json, file, indent=2)
