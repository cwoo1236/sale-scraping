import requests
from bs4 import BeautifulSoup
import re

def scrape_kohls_clearance():

  master = {}
  ppp = 120
  pg_num = 0
  
  while True:
    url = "https://www.kohls.com/catalog/clearance-mens.jsp?CN=Promotions:Clearance+Gender:Mens&cc=sale-TN2.0-S-Clearance-Mens&PPP=%d&WS=%d" % (ppp, ppp * pg_num)
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    blocks = soup.find_all('li', class_=re.compile("products_grid.*"))
    
    if not blocks:
      break
    else:
      print("Loading Kohl's clearance page %d..." % (pg_num + 1))
      
    for block in blocks:
      item = block.find('img').get('title')
      link = "https://www.kohls.com" + block.find('a').get('href')
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

  return master