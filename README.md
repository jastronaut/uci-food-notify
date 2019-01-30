# uci-food-notify

get lunch menus from uci's dining halls and send an email with their contents

## what i used

- python3
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for parsing dining hall website
- [Mailgun](https://www.mailgun.com) for their email API
- Dreamhost's cron job service to run this script daily

## usage

- replace `API_KEY`, `API_URL`, `SRC_EMAIL`, `DEST_EMAIL` in `sendmenu.py` with your mailgun information
- run this script daily to get uci dining hall menus in your inbox every day!