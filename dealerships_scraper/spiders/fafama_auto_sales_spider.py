import scrapy
import time
import datetime
import os
import sys
import re
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items
from spiders_utils import get_item_data_from_xpath, get_car_make_model, get_vehicle_type

class FafamaAutoSalesSpider(scrapy.Spider):
  name = "fafama_auto_sales"
  user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
  start_urls = [
      'https://www.fafama.com/inventory.aspx?_page=1'
  ]

  DEALERSHIP_INFO = {
    'dealership_name': 'Fafama Auto Sales',
    'address': '5 Cape Road',
    'zipcode': '01757',
    'city': 'Milford',
    'state': 'MA'
  }


  def parse(self, response):
    links = response.xpath("//div[@class='srp-card-header']/a/@href").extract()

    print(links)

    if len(links) == 0:
      print(f"No links were found in {self.name} spider")
      return

    for link in links:
      time.sleep(1)
      url = f'https:{link}'
      yield scrapy.Request(url, callback=self.parse_car)

    curr_page = int(re.search('page=([0-9])+', response.url)[0].replace('page=', ''))
    next_page_url = re.sub('page=([0-9])+', f'page={curr_page + 1}', response.url)
    yield scrapy.Request(
      url=next_page_url,
      callback=self.parse
    )

  def parse_car(self, response):
    item = items.Car()

    year_make_model = response.xpath(".//h1[@class='ebiz-vdp-title color m-0']/text()").extract()[0].strip()
    year, make, model = get_car_make_model(year_make_model)
    item['year'] = year if year != '' else None
    item['make'] = make if make != '' else None
    item['model'] = model if model != '' else None
    get_item_data_from_xpath(response, ".//span[@class='ebiz-vdp-subtitle h3 body-color d-block m-0']/text()", item, 'trim', 'str')
    item['title'] = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + ' ' + str(item['trim']) if item['trim'] != None else ''
    item['model_trim'] = str(item['model']) + ' ' + str(item['trim']) if item['trim'] != None else ''

    get_item_data_from_xpath(response, ".//tr[@class='miles-row']/td[@class='tright']/text()", item, 'mileage', 'int')
    get_item_data_from_xpath(response, ".//h2[@class='money-sign-disp body-font d-inline m-0 color h3']/text()", item, 'price', 'int')

    get_item_data_from_xpath(response, ".//tr[@class='transmission-row']/td[@class='tright']/text()", item, 'transmission', 'str')
    get_item_data_from_xpath(response, ".//tr[@class='vin-row']/td[@class='tright']/text()", item, 'vin', 'str')
    get_item_data_from_xpath(response, ".//tr[@class='engine-row']/td[@class='tright']/text()", item, 'engine', 'str')
    get_item_data_from_xpath(response, ".//tr[@class='int-color-row']/td[@class='tright']/text()", item, 'interior_color', 'str')
    get_item_data_from_xpath(response, ".//tr[@class='ext-color-row']/td[@class='tright']/text()", item, 'exterior_color', 'str')
    get_item_data_from_xpath(response, ".//tr[@class='drivetrain-row']/td[@class='tleft']/text()", item, 'drivetrain', 'str')

    trim_data = response.xpath(".//span[@class='ebiz-vdp-subtitle h3 body-color d-block m-0']/text()").get()
    if trim_data != None:
      item['vehicle_type'] = get_vehicle_type(trim_data)

    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = response.url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
