
import parse_inventory as pi
import parse_dealership
import requests
import re
from bs4 import BeautifulSoup
import numpy as np

# Dealership Info Dictionary
dealerships = {
    'Stream Auto Outlet': {
        'url': 'https://www.streamautooutlet.com/inventory?type=used',
        'pagination_url': 'https://www.streamautooutlet.com/inventory?type=used&pg=2',
        'vehicle_detail_url': 'https://www.streamautooutlet.com/vehicle-details',
        'dealership_name': 'Stream Auto Outlet',
        'address': '324 W Merrick Rd',
        'zipcode': '11580',
        'city': 'Valley Stream',
        'state': 'NY'
    }
}

if __name__ == '__main__':
  # Set scrapping parameters
  headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  }

  TABLE_NAME = 'inventory_test'
  ERROR_TBL_NAME = 'parsing_errors'
  DB_NAME = 'cars_test.db'
  TIME_BTWN_SCRAPE = 21


  for key in dealerships:
    print("Processing: ", key)
    if key == 'Stream Auto Outlet':
        days_since= pi.days_since_last_scrape(key, DB_NAME, TABLE_NAME)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_stream_auto_outlet_inventory_data(soup, dealerships[key], dealerships[key]['url'], headers)

            if 'error' in data.columns:
                pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
            else:
                pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

            # Parse out other pages if there are any available
            pagination_url = dealerships[key]['pagination_url']
            page_counter = 2

            while (True):
                response = requests.get(pagination_url, headers = headers)
                soup_pagination = BeautifulSoup(response.text, "html.parser")
                title = pi.clean_text_data(pi.parse_subsection_all(soup_pagination, 'h4', 'span', 'srp-vehicle-title'))

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_stream_auto_outlet_inventory_data(soup_pagination, dealerships[key], pagination_url, headers)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('pg=[0-9]+', f'pg={page_counter}', pagination_url)
