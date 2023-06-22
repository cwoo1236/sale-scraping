from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


with sync_playwright() as playwright:
      browser = playwright.chromium.launch()
      page = browser.new_page()
      page.goto('https://www.weekday.com/en/sale/men/all.html')
      print("Loading Weekday sale...")

      # Wait for any dynamic content to load
      print("Scrolling down...")
      page.wait_for_load_state('networkidle')

      # Get the HTML content
      html = page.inner_html('body')
      # Parse the HTML content using BeautifulSoup
      soup = BeautifulSoup(html, "html.parser")