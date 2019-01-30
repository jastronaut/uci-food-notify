import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from datetime import date
import time
import json

ANTEATERY_LOC = 3056
PIPPIN_LOC = 4832
LUNCH = 106
BREAKFAST = 49
DINNER = 107
URL_ANTEATERY = "https://uci.campusdish.com/LocationsAndMenus/TheAnteatery?%s"
URL_PIPPIN = "https://uci.campusdish.com/LocationsAndMenus/PippinCommons?%s"


dining_halls = {
    'The Anteatery': {
        'url_base': URL_ANTEATERY,
        'loc_id': ANTEATERY_LOC
    },
    'Pippin Commons': {
        'url_base': URL_PIPPIN,
        'loc_id': PIPPIN_LOC
    }
}

menu = {}
def get_date():
    today = date.today()
    return str(today.month) + '/' + str(today.day) + '/' + str(today.year)


def create_food(item):
    try:
        itemName = item.find(class_='viewItem').get_text()
    except:
        itemName = item.find(class_='viewItem')
        # itemName = 'Unknown name'
    
    try:
        itemCalories = item.find(class_='item__calories').get_text()
    except:
        itemCalories = 'Unknown calories'
    
    try:
        itemContent = item.find(class_='item__content').get_text()
    except:
        itemContent = 'Unknown content'

    food = {
        'name': itemName,
        'calories': itemCalories,
        'desc': itemContent
    }

    return food

def gen_menus():
    for hall in dining_halls:
        menu[hall] = {}
        print(hall)
        params = urllib.parse.urlencode({
            'locationId': dining_halls[hall]['loc_id'],
            'storeId': '',
            'mode': 'Daily',
            'periodId': LUNCH,
            'date': get_date()
        })
        URL = dining_halls[hall]['url_base'] % params
        print(URL)
        menu[hall]['URL'] = URL
        resp = requests.get(URL)
        soup = BeautifulSoup(resp.text, 'html.parser')

        cats = soup.find_all(class_='menu__station')
        menu[hall]['menu'] = {}
        for cat in cats:
            place = cat.find('h2').get_text()
            menu[hall]['menu'][place] = []

            allItems = cat.find(class_='menu__category')
            try:
                items = allItems.find_all(class_='menu__items')
            except:
                continue
            for item in items:
                menu[hall]['menu'][place].append(create_food(item))
        print()
        time.sleep(1)

    json.dump(menu, open('menu.json', 'w'), indent=4)