import requests
from bs4 import BeautifulSoup

def scrape_weekday_sale():

  print("Loading Weekday sale...")
  url = "https://www.weekday.com/en/sale/men/all.html"
  response = requests.get(url)
  
  # Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")
  blocks = soup.find_all('div', class_="o-product no-quick-buy productTrack")
  
  master = {}
  
  for block in blocks:
    item = block.find('span', class_='productName').string
    link = block.find('a').get('href')
    price_raw = block.find('span', class_='is-reduced')
    color = block.find(
      'div', class_='a-swatch js-swatch is-selected').find('input').get('value')
    name = "%s - %s" % (item, color)
    if price_raw:
      price = price_raw.string
    else:
      price = None
    master[name] = {'price': price, 'link': link, 'from': 'Weekday', 'color': color}

  return master