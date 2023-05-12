

import scrapy
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items
from spiders_utils import get_item_data_from_xpath, get_car_make_model
import re


class AvonAutoBrokersSpider(scrapy.Spider):
  name = "avon_auto_brokers"
  user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
  start_urls = [
    'https://avonautobrokers.com/newandusedcars?page=1'
  ]

  DEALERSHIP_INFO = {
    'dealership_name': 'Avon Auto Brokers',
    'address': '159 Memorial Drive',
    'zipcode': '02322',
    'city': 'Avon',
    'state': 'MA'
  }

  def parse(self, response):
    selectors = response.xpath("//div[@class='i11r-vehicle infinite-scroll-current-page']")

    if len(selectors) == 0:
      return

    for selector in selectors:
      yield from self.parse_car(selector, response.url)

    curr_page = int(re.search('page=([0-9])+', response.url)[0].replace('page=', ''))
    next_page_url = re.sub('page=([0-9])+', f'page={curr_page + 1}', response.url)
    yield scrapy.Request(
        url=next_page_url,
        callback=self.parse
    )

  def parse_car(self, response, current_url):
    item = items.Car()

    year_make_model = response.xpath(".//h4[@class='i11r_vehicleTitle']/a/text()").extract()[0].strip()
    year, make, model = get_car_make_model(year_make_model)
    item['year'] = year if year != '' else None
    item['make'] = make if make != '' else None
    item['model'] = model if model != '' else None
    get_item_data_from_xpath(response, ".//span[@class='vehicleTrim']/text()", item, 'trim', 'str')

    title = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + ' ' + str(item['trim'])
    item['title'] = title
    model_trim = str(item['model']) + ' ' + str(item['trim'])
    item['model_trim'] = model_trim

    get_item_data_from_xpath(response, ".//div[@class='retailWrap pricebox-2 hide-grid-price']/span[@class='price-2']/text()", item, 'price', 'float')
    get_item_data_from_xpath(response, ".//div[@class='col-md-6']/p[@class='i11r_optMileage']/text()", item, 'mileage', 'int', 1)

    get_item_data_from_xpath(response, ".//div[@class='col-md-6']/p[@class='i11r_optEngine2']/text()", item, 'engine', 'str', 1)
    get_item_data_from_xpath(response, ".//div[@class='col-md-6']/p[@class='i11r_optTrans2']/text()", item, 'transmission', 'str', 1)
    get_item_data_from_xpath(response, ".//div[@class='col-md-6']/p[@class='i11r_optDrive']/text()", item, 'drivetrain', 'str', 1)
    get_item_data_from_xpath(response, ".//div[@class='col-md-6']/p[@class='i11r_optColor']/text()", item, 'exterior_color', 'str', 1)
    get_item_data_from_xpath(response, ".//div[@class='col-md-6']/p[@class='i11r_optInteriorColor']/text()", item, 'interior_color', 'str', 1)
    get_item_data_from_xpath(response, ".//div[@class='col-md-6']/p[@class='i11r_optVin']/text()", item, 'vin', 'str', 1)
    get_item_data_from_xpath(response, ".//div[@class='col-md-6']/p[@class='i11r_optBody']/text()", item, 'vehicle_type', 'str', 1)

    # Dealership info
    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = current_url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
