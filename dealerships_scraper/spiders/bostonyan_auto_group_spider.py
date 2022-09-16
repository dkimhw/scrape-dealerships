
import scrapy
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname('dealerships_scraper')))
import items
from spiders_utils import get_item_data_from_xpath, get_vehicle_type


class BostonyanAutoGroupSpider(scrapy.Spider):
  name = "bostonyan_auto_group"
  user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
  start_urls = [
    'https://www.bostonyanautogroup.com/view-inventory',
  ]

  DEALERSHIP_INFO = {
    'dealership_name': 'Bostonyan Auto Group',
    'address': '119 Worcester St',
    'zipcode': '01760',
    'city': 'Natick',
    'state': 'MA'
  }

  def parse(self, response):
    selectors = response.xpath("//div[@class='col- dynamic-col']")
    for selector in selectors:
      yield from self.parse_car(selector, response.url)

  def parse_car(self, response, current_url):
    item = items.Car()

    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displayyear", item, 'year', 'int')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displaymake", item, 'make', 'str')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displaymodel", item, 'model', 'str')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displaytrim", item, 'trim', 'str')
    item['title'] = str(item['year']) + ' ' + str(item['make']) + ' ' + str(item['model']) + ' ' + str(item['trim']) if item['trim'] != None else ''
    item['model_trim'] = str(item['model']) + ' ' + str(item['trim']) if item['trim'] != None else ''

    get_item_data_from_xpath(response, ".//div[@class='pricevalue1 accent-color1']/b/text()", item, 'price', 'int')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displaymileage", item, 'mileage', 'int')

    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displayintcolor", item, 'interior_color', 'str')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displayextcolor", item, 'exterior_color', 'str')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displayengine", item, 'engine', 'str')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displaytransmission", item, 'transmission', 'str')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displaydrivetrain", item, 'drivetrain', 'str')
    get_item_data_from_xpath(response, ".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displaydrivetrain", item, 'vehicle_type', 'str')
    get_item_data_from_xpath(response, ".//span[@class='vin']/text()", item, 'vin', 'str')

    title = response.xpath(".//div[@class='clearfix inventory-panel   palette-bg2 vehicle  lot-00']/@data-displaytitle").get()
    if title != None:
      item['vehicle_type'] = get_vehicle_type(title)

    item['dealership_name'] = self.DEALERSHIP_INFO['dealership_name']
    item['dealership_address'] = self.DEALERSHIP_INFO['address']
    item['dealership_zipcode'] = self.DEALERSHIP_INFO['zipcode']
    item['dealership_city'] = self.DEALERSHIP_INFO['city']
    item['dealership_state'] = self.DEALERSHIP_INFO['state']
    item['scraped_url'] = current_url
    item['scraped_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yield item
