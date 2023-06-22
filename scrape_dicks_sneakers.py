from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

def scrape_dicks_sneakers():
    master = {}
    pg_num = 0

    while True:
        url = "https://www.dickssportinggoods.com/f/sale-mens-athletic-sneakers?pageNumber=%d&pageSize=96" % (pg_num)
        with sync_playwright() as playwright:
            headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
        }
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.set_extra_http_headers(headers)

            print("Loading Dick's page %d..." % (pg_num + 1))
            page.goto(url)

            page.wait_for_load_state('networkidle')

            # Get the HTML content
            html = page.inner_html('body')
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            blocks = soup.find_all('div', class_='dsg-flex flex-column dsg-react-product-card rs_product_card dsg-react-product-card-col-4')
            if not blocks:
                break
            for block in blocks:
                color = block.find('li').find('img').get('title')
                name = block.find('a', class_='rs_product_description d-block').text + ' - ' + color
                price = block.find('p', class_=re.compile('offer-price|unlisted-price')).text
                link = "https://www.dickssportinggoods.com/" + block.find('a').get('href')

                master[name] = {'price': price, 'link': link, 'from': "Dick's"}
            
            pg_num += 1

    return master