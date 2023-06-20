import requests
from bs4 import BeautifulSoup


def scrape_arket_sale():
  print("Loading Arket sale...")
  master = {}

  headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
  }

  url = "https://www.arket.com/en/men/sale.html"  # scrolling page
  response = requests.get(url, headers=headers)

  # Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")

  blocks = soup.find_all('div', class_="o-product productTrack")

  for block in blocks:
    color = block.find('div',
                       class_='color').text.replace('\n',
                                                    '').replace('Color', '')
    name = block.find('div', class_='product').text.replace('\n', '').replace(
      'Product', '')
    name = "(Arket) %s - %s" % (name, color)
    price = block.find('span', class_='is-reduced').text
    link = block.find('a').get('href')
    master[name] = {
      'price': price,
      'link': link,
      'from': 'Arket',
      'color': color
    }

  return master