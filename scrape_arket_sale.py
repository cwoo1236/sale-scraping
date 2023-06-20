from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_arket_sale():
  with sync_playwright() as playwright:
      browser = playwright.chromium.launch()
      page = browser.new_page()
      page.goto('https://www.arket.com/en/men/sale.html')
      print("Loading Arket sale...")

      # Scroll to the bottom of the page
      page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

      # Wait for any dynamic content to load
      # Adjust the timeout as needed
      print("Scrolling down...")
      page.wait_for_timeout(2000)

      # Get the HTML content
      html = page.inner_html('body')
      # Parse the HTML content using BeautifulSoup
      soup = BeautifulSoup(html, "html.parser")

      blocks = soup.find_all('div', class_="o-product productTrack")
      master = {}
      for block in blocks:
          color = block.find('div',
                          class_='color').text.replace('\n', '').replace('Color', '')
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

      browser.close()
      
  return master
