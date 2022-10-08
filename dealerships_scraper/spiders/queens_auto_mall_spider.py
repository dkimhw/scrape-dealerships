
import scrapy
from urllib.parse import urljoin
import re
import time
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items
from spiders_utils import get_item_data_from_xpath


class QueensAutoMallSpider(scrapy.Spider):
  name = "queens_auto_mall"
  VEHICLES = 0
  SCRAPED = False
  user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
  start_urls = [
    'https://www.queensauction.com/cars-for-sale-richmond-hill-ny'
  ]

  DEALERSHIP_INFO = {
    'dealership_name': "Queeens Auto Mall",
    'address': '134-01 Atlantic Ave',
    'zipcode': '11418',
    'city': 'Richmond Hill',
    'state': 'NY'
  }

  def parse(self, response):
    num_of_cars = response.xpath("//div[@class='inventory-heading__count hidden-xs hidden-sm hidden-md']/text()").extract_first()

    if self.VEHICLES == 0:
      self.VEHICLES = int(re.sub("[^0-9]", "", num_of_cars))

    if self.SCRAPED == False:
      self.SCRAPED == True
      next_url = f'https://www.queensauction.com/cars-for-sale-richmond-hill-ny?limit={self.VEHICLES}'
      yield scrapy.Request(
          url=next_url,
          callback=self.parse
      )

    links = response.xpath("//a[@class='js-vehicle-item-link vehicle-item__link_no-decoration']/@href").extract()

    for link in links:
      url = f"https://www.queensauction.com{link}"
      yield scrapy.Request(url, callback=self.parse_car)
      time.sleep(1.5)

  def parse_car(self, response):
    item = items.Car()

    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Year')]]]/text()", item, 'year', 'int')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Make')]]]/text()", item, 'make', 'str')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Model')]]]/text()", item, 'model', 'str')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Trim')]]]/text()", item, 'trim', 'str')
    item['title'] = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + ' ' + str(item['trim'])
    item['model_trim'] = str(item['model']) + ' ' + str(item['trim'])

    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Mileage')]]]/text()", item, 'mileage', 'int')
    get_item_data_from_xpath(response, "//div[@class='price_value']/text()", item, 'price', 'int')

    response.xpath("//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Year')]]]/text()").extract()


    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Transmission')]]]/text()", item, 'transmission', 'str')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'VIN')]]]/text()", item, 'vin', 'str')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Description')]]]/text()", item, 'engine', 'str')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Interior Color')]]]/text()", item, 'interior_color', 'str')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Exterior Color')]]]/text()", item, 'exterior_color', 'str')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Drivetrain')]]]/text()", item, 'drivetrain', 'str')
    get_item_data_from_xpath(response, "//table[@class='fields']/tr/td[preceding-sibling::td[./div[@class='name_wrapper']/text()[contains(., 'Body Style')]]]/text()", item, 'vehicle_type', 'str')

    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = response.url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
