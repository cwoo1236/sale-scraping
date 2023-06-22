import requests
from bs4 import BeautifulSoup
import json

def scrape_everlane_sale():
  master = {}
  
  print("Loading Everlane sale...")
  url = "https://www.everlane.com/collections/mens-sale-2"
  response = requests.get(url)
  
  # Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")
  json_string = json.loads(soup.find_all('script')[15].string)
  found = set()
  all_products = json_string['props']['pageProps']['fallbackData']['products']
  
  for p in all_products:
    if not p['displayName'] in found:
      name = p['displayName'] # + " -- " + p['color']['name']
      found.add(p['displayName'])
      link = "https://www.everlane.com/products/" + p['permalink']
      price = '$' + p['price'] + '*'    # price after discount isn't given in the BS4 output:?
      master[name] = {'price': price, 'link': link, 'from': 'Everlane'}
  
  return master