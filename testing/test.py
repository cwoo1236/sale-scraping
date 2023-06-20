import requests
from bs4 import BeautifulSoup
import re


master = {}
ppp = 120
pg_num = 0


url = "https://www.kohls.com/catalog/clearance-mens.jsp?CN=Promotions:Clearance+Gender:Mens&cc=sale-TN2.0-S-Clearance-Mens&PPP=%d&WS=%d" % (ppp, ppp * pg_num)
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
blocks = soup.find_all('li', class_=re.compile("products_grid.*"))


for block in blocks:
    item = block.find('img').get('title')
    link = block.find('a').get('href')
    price_raw = block.find('span', class_='prod_price_amount red_color')
    if price_raw:
        price = price_raw.string
    else:
        price = "UNKN"

    img_link = str(block.find('img').get('data-herosrc'))
    color = re.search("\d+(.*)\?", img_link).group(1)
    color = color.replace('_', ' ').strip()
    master[item] = {'price': price, 'link': link, 'color': color, 'from': 'kohls'}

pg_num += 1
