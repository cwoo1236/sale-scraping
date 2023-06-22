from search import query_master, print_search_results
from scrape_weekday_sale import scrape_weekday_sale
from scrape_kohls_clearance import scrape_kohls_clearance
from scrape_everlane_sale import scrape_everlane_sale
from scrape_af_clearance import scrape_af_clearance
from scrape_cos_sale import scrape_cos_sale
from scrape_arket_sale import scrape_arket_sale
import webbrowser

# Scrape & format different sites
# Macy's clearance alone is like 56k mens items
# Superdry doesn't seem to be willing to give html

weekday_master = scrape_weekday_sale()
kohls_master = scrape_kohls_clearance()
everlane_master = scrape_everlane_sale()
af_master = scrape_af_clearance()
cos_master = scrape_cos_sale()
arket_master = scrape_arket_sale()

# Put all them together and search
master = weekday_master | kohls_master | everlane_master | af_master | cos_master | arket_master

search_results = query_master(master)

item_to_open = ''
search_history = []
while not item_to_open == "q":
  item_to_open = input(
    "Enter the number of an item to view, 'q' to quit, or '$' to search for a different keyword: "
  )

  if item_to_open == 'q':
    print("In this session, you viewed %d items." % (len(search_history)))
    for (item, link) in search_history:
      print("%s | %s" % (item, link))
    break
  elif item_to_open == '$':
    search_results = query_master(master)
  elif item_to_open.isnumeric():
    num = int(item_to_open) 
    try:
      item_name = search_results[num][0]
    except KeyError:
      print("Invalid number given. Try again")
      continue
    print("Opening product page...")
    item_viewed_link = master[item_name]['link']
    webbrowser.open(item_viewed_link)
    search_history.append((item_name, item_viewed_link))
  
    print_search_results(search_results)
  else:
    print("Invalid input. Try again")
    continue

  

  
