
import scrapy
#from items import Car
from urllib.parse import urljoin
import re
import time
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items
from spiders_utils import get_item_data_from_xpath


class JohnsAutoGroupSpider(scrapy.Spider):
    name = "johns_auto_group"
    start_urls = [
        'https://johnsautosales.com/newandusedcars?clearall=1',
    ]

    DEALERSHIP_INFO = {
      'dealership_name': "Johns Auto Sales",
      'address': '181 Somerville Avenue',
      'zipcode': '02143',
      'city': 'Somerville',
      'state': 'MA'
    }

    def parse(self, response):
      links = response.xpath("//h4[@class='vehicleTitleWrap d-none d-md-block']/a/@href").extract()
      for link in links:
        url = f"https://johnsautosales.com{link}"
        time.sleep(1)
        yield scrapy.Request(url, callback=self.parse_car)

      # next_page = response.xpath("//ul[@class='pagination']/li[@class='arrow']/a/@href").extract()

      # # Additional layer of logic required to correctly retrieve the next url:
      # if next_page:
      #   if len(next_page) == 2:
      #     next_page = next_page[0]
      #   elif len(next_page) > 2:
      #     next_page = next_page[1]
      # else:
      #   next_page = None
      # print("Next Page: ", next_page)
      # if next_page:
      #   next_page_url = f"https://www.streamautooutlet.com{next_page}"
      #   yield scrapy.Request(
      #       url=next_page_url,
      #       callback=self.parse
      #   )
      # else:
      #   print('No more pages to scrape')

    def parse_car(self, response):
      item = items.Car()

      get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optYear']/text()", item, 'year', 'int', 1)
      get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optMake']/text()", item, 'make', 'str', 1)
      get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optModel']/text()", item, 'model', 'str', 1)
      get_item_data_from_xpath(response, "//div[@class='col-sm-6']/p[@class='optTrim']/text()", item, 'trim', 'str', 1)
      item['title'] = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + str(item['trim'])

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
