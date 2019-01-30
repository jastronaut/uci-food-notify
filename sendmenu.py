import json
import requests
import getmenu

API_URL = ''
API_KEY = ''
SRC_EMAIL = ''
DEST_EMAIL = ''

def get_menu():
    try:
        f = open('menu.json', 'r')
    except:
        print('Could not open json file')
        exit()
    menu = json.load(f)
    f.close()
    return menu


def prepare_menu_email():
    menu = get_menu()
    content = '<html>Here are today\'s foods:<br>'
    
    for hall in menu:
        content = content + '<h1>' + hall + '</h1>'
        content = content + '<a href="' + menu[hall]['URL'] + '">Go to Menu</a>'
        for loc in menu[hall]['menu']:
            content = content + '<h2>' + loc + '</h2>'
            for item in menu[hall]['menu'][loc]:
                content = content + '<b>' + item['name'] + '</b>'
                food = (
                   '<ul>'
                   '<li>' + item['calories'] + '</li>'
                   '<li>' + item['desc'] + '</li>'
                   '</ul>')
                content = content + food
        content = content + '<hr>'
    
    return content + '</html>'

def create_email():
    to = DEST_EMAIL
    subject = 'Menu for ' + getmenu.get_date()
    body = prepare_menu_email()

    return requests.post(
        API_URL,
        auth=('api', API_KEY),
        data={'to': [to],
        'from': 'Test dining hall app ' + SRC_EMAIL,
            'subject': subject,
            'html': body
        }
    )


if __name__ == '__main__':
    getmenu.gen_menus()
    create_email()