

import scrapy
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items
from spiders_utils import get_item_data_from_xpath

class JMAutoSpider(scrapy.Spider):
  name = "jm_auto"
  start_urls = [
    'https://www.jmautomotive.com/cars-for-sale-in-Naugatuck-CT-Hartford-New-Haven/used_cars'
  ]

  DEALERSHIP_INFO = {
      'dealership_name': 'J&M Automotive',
      'address': '756/820 New Haven Road',
      'zipcode': '06770',
      'city': 'Naugatuck',
      'state': 'CT'
  }

  def parse(self, response):
    selectors = response.xpath("//div[@class='thumbnail']")
    for selector in selectors:
      yield from self.parse_car(selector, response.url)

    next_page = response.xpath("//div[@class='dwfloatL']/a[contains(text(), 'Next')]/@href").extract()

    if len(next_page) > 0:
      next_page = next_page[0]
      yield scrapy.Request(url=next_page, callback=self.parse)
    else:
      print('No more pages to scrape')

  def parse_car(self, response, current_url):
    item = items.Car()

    # ".//span[@itemprop='vehicleModelDate']/text()"
    get_item_data_from_xpath(response, ".//a[@class='listitemlink']/span/span[@itemprop='vehicleModelDate']/text()", item, 'year', 'int')

    get_item_data_from_xpath(response, ".//a[@class='listitemlink']/span/span[@itemprop='manufacturer']/text()", item, 'make', 'str')

    get_item_data_from_xpath(response, ".//a[@class='listitemlink']/span/span[@itemprop='model']/text()", item, 'model', 'str')

    get_item_data_from_xpath(response, ".//a[@class='listitemlink']/span/span[@itemprop='vehicleConfiguration']/text()", item, 'trim', 'str')

    title = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + str(item['trim'])
    item['title'] = title

    model_trim = str(item['model']) + ' ' + str(item['trim'])
    item['model_trim'] = model_trim

    get_item_data_from_xpath(response, ".//div[@class='pricetag']/div[@class='inv-price internet-price DWInvListPriceSpan']/span[@itemprop='price']/text()", item, 'price', 'float')

    get_item_data_from_xpath(response, ".//li[@class='list-group-item mileage']/span/span[@class='dw-p0']/text()", item, 'mileage', 'int')

    get_item_data_from_xpath(response, ".//li[@class='list-group-item InvEnginetype']/span/span[@class='dw-p0']/text()", item, 'engine', 'str')

    get_item_data_from_xpath(response, ".//span[@itemprop='vehicleTransmission']/text()", item, 'transmission', 'str')

    get_item_data_from_xpath(response, ".//span[@itemprop='driveWheelConfiguration']/text()", item, 'drivetrain', 'str')

    get_item_data_from_xpath(response, ".//span[@itemprop='color']/text()", item, 'exterior_color', 'str')

    get_item_data_from_xpath(response, ".//span[@itemprop='vehicleInteriorColor']/text()", item, 'interior_color', 'str')

    get_item_data_from_xpath(response, ".//span[@itemprop='vehicleIdentificationNumber']/text()", item, 'vin', 'str')

    # No vehicle type to scrape
    item['vehicle_type'] = None

    # Dealership info
    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = current_url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
