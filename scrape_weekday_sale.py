from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_weekday_sale():
  with sync_playwright() as playwright:
      browser = playwright.chromium.launch()
      page = browser.new_page()
      page.goto('https://www.weekday.com/en/sale/men/all.html')
      print("Loading Weekday sale...")

      # Scroll to the bottom of the page
      page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

      # Wait for any dynamic content to load
      # Adjust the timeout as needed
      print("Scrolling down...")
      page.wait_for_timeout(5000)

      # Get the HTML content
      html = page.inner_html('body')
      # Parse the HTML content using BeautifulSoup
      soup = BeautifulSoup(html, "html.parser")

      blocks = soup.find_all('div', class_="o-product no-quick-buy productTrack")
  
      master = {}
      
      for block in blocks:
        item = block.find('span', class_='productName').string
        link = block.find('a').get('href')
        price_raw = block.find('span', class_='is-reduced')
        color = block.find(
          'div', class_='a-swatch js-swatch is-selected').find('input').get('value')
        name = "(Weekday) %s - %s" % (item, color)
        if price_raw:
          price = price_raw.string
        else:
          price = None
        master[name] = {'price': price, 'link': link, 'from': 'Weekday', 'color': color}

      browser.close()
      return master

