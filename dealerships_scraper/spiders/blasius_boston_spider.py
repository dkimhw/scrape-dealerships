
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


class BlasiusBostonSpider(scrapy.Spider):
  name = "blasius_boston"
  user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
  start_urls = [
      'https://www.blasiusboston.com/used-cars-holliston-ma?page=1'
  ]

  DEALERSHIP_INFO = {
    'dealership_name': 'Blasius Boston',
    'address': '1286 Washington Street',
    'zipcode': '01746',
    'city': 'Holliston',
    'state': 'MA'
  }

  def parse(self, response):
    links = response.xpath("//div[@class='v-title']/a/@href").extract()

    if len(links) == 0:
      return

    for link in links:
      time.sleep(2)
      yield scrapy.Request(link, callback=self.parse_car)

    curr_page = int(re.search('page=([0-9])+', response.url)[0].replace('page=', ''))
    next_page_url = re.sub('page=([0-9])+', f'page={curr_page + 1}', response.url)
    yield scrapy.Request(
        url=next_page_url,
        callback=self.parse
    )

  def parse_car(self, response):
    item = items.Car()

    get_item_data_from_xpath(response, ".//meta[@itemprop='releaseDate']/@content", item, 'year', 'int')
    get_item_data_from_xpath(response, ".//meta[@itemprop='manufacturer']/@content", item, 'make', 'str')
    get_item_data_from_xpath(response, ".//meta[@itemprop='model']/@content", item, 'model', 'str')
    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'Trim:')]]]/text()", item, 'trim', 'str')
    item['title'] = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + ' ' + str(item['trim'])
    item['model_trim'] = str(item['model']) + ' ' + str(item['trim'])

    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'Mileage:')]]]/text()", item, 'mileage', 'int')
    get_item_data_from_xpath(response, "//span[@class='starting-price-value ']/text()", item, 'price', 'int')

    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'Transmission:')]]]/text()", item, 'transmission', 'str')
    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'VIN #:')]]]/text()", item, 'vin', 'str')
    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'Engine:')]]]/text()", item, 'engine', 'str')
    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'Interior:')]]]/text()", item, 'interior_color', 'str')
    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'Exterior:')]]]/text()", item, 'exterior_color', 'str')
    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'Drive:')]]]/text()", item, 'drivetrain', 'str')
    get_item_data_from_xpath(response, ".//li[@class='specification-item']/span[preceding-sibling::span[./strong/text()[contains(.,'Body:')]]]/text()", item, 'vehicle_type', 'str')

    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = response.url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
