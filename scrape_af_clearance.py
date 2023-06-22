import requests
from bs4 import BeautifulSoup


def scrape_af_clearance():
  master = {}
  ppp = 90
  pg_num = 0

  headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
  }

  while True:
    url = "https://www.abercrombie.com/shop/us/mens-clearance?filtered=true&rows=%d&start=%d" % (
      ppp, ppp * pg_num)

    response = requests.get(url, headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    blocks = soup.find_all('li',
                           class_="catalog-productCard-module__productCard")

    if not blocks:
      break
    print("Loading Abercrombie clearance page %d..." % (pg_num + 1))

    for block in blocks:
      name = "(Abercrombie) " + block.find('img').get('alt')
      color = name.split(', ')[-1]
      price = block.find(
        'span', {
          'data-variant': 'discount'
        },
        class_="product-price-text product-price-font-size").string
      link = "https://www.abercrombie.com" + block.find('a').get('href')

      master[name] = {
        'price': price,
        'link': link,
        'from': 'Abercrombie',
        'color': color
      }

    pg_num += 1

  return master
