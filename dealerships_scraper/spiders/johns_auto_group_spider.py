
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

# scrapy shell 'https://johnsautosales.com/newandusedcars?page=1'
class JohnsAutoGroupSpider(scrapy.Spider):
  name = "johns_auto_group"
  start_urls = [
      'https://johnsautosales.com/newandusedcars?page=1'
  ]

  USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
  DEALERSHIP_INFO = {
    'dealership_name': "Johns Auto Sales",
    'address': '181 Somerville Avenue',
    'zipcode': '02143',
    'city': 'Somerville',
    'state': 'MA'
  }

  def parse(self, response):
    links = response.xpath("//h4[@class='vehicleTitleWrap d-none d-md-block']/a/@href").extract()

    if len(links) == 0:
      return

    for link in links:
      url = f"https://johnsautosales.com{link}"
      time.sleep(1)
      yield scrapy.Request(url, callback=self.parse_car)

    curr_page = int(re.search('page=([0-9])+', response.url)[0].replace('page=', ''))
    next_page_url = re.sub('page=([0-9])+', f'page={curr_page + 1}', response.url)
    yield scrapy.Request(
        url=next_page_url,
        callback=self.parse
    )

  def parse_car(self, response):
    item = items.Car()

    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optYear']/text()", item, 'year', 'int', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optMake']/text()", item, 'make', 'str', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optModel']/text()", item, 'model', 'str', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optTrim']/text()", item, 'trim', 'str', 1)
    item['title'] = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + ' ' + str(item['trim'])
    item['model_trim'] = str(item['model']) + ' ' + str(item['trim'])

    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optMileage']/text()", item, 'mileage', 'int', 1)
    get_item_data_from_xpath(response, "//span[@class='lblPrice']/text()", item, 'price', 'int')

    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optTrans']/text()", item, 'transmission', 'str', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optVin']/text()", item, 'vin', 'str', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optEngine']/text()", item, 'engine', 'str', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optInteriorColor']/text()", item, 'interior_color', 'str', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optColor']/text()", item, 'exterior_color', 'str', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optDrive']/text()", item, 'drivetrain', 'str', 1)
    get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optType']/text()", item, 'vehicle_type', 'str', 1)

    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = response.url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
