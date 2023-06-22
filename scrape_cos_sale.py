import requests
from bs4 import BeautifulSoup

def scrape_cos_sale():
  master = {}
  ppp = 72
  pg_num = 1
  
  headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
  }
  
  while True:
    url = "https://www.cos.com/en_usd/men/sale.html?page=%d" % (pg_num)
    response = requests.get(url, headers=headers)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
  
    total_items = int(soup.find('div', {'id': 'productCount'}).get('class')[0])

    if pg_num * ppp > total_items:
      break
    else:
      print("Loading COS sale page %d..." % (pg_num))
      
    blocks = soup.find_all('div', class_="column")

    for block in blocks:
      color = block.find('span', class_='colorName').text.title()
      name = "(COS) %s - %s" % (block.find('span', class_='productName').text.title(), color)
      price = "$%s0" % (block.find('span', class_='price').text)
      link = block.find('a').get('href')
      master[name] = {'price': price, 'link': link, 'from': 'COS', 'color': color}
  
    pg_num += 1
    
  return master